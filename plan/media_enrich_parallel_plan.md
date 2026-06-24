# Plan: Song song hóa media URL enrichment

## Mục tiêu
Giảm latency của bước enrich media trong `MediaResearchAgent._enrich_media_urls`.
Hiện tại tới 4 lần `search_media()` (mỗi lần là 1 HTTP call Tavily blocking) chạy
**tuần tự** → tổng thời gian = tổng 4 call. Chuyển sang **chạy song song** →
tổng thời gian ≈ call chậm nhất.

KHÔNG làm: cache, đổi sang async/HTTP MCP, đổi pipeline khác.

## Hiện trạng (đã xác minh)
- `src/llm/agents/media_research.py:50-118` — `_enrich_media_urls` loop `for item in items` tuần tự, mỗi item gọi `client.search_media(...)` rồi mutate `item` in-place, set cờ `touched`.
- `items` tối đa 4 (`_MAX_MEDIA_LOOKUPS = 4`), lọc item chưa có url.
- Mỗi item độc lập: đọc caption riêng, ghi vào chính object item đó → **không chia sẻ state giữa các item** ngoài cờ `touched` và `client` singleton.
- Pattern parallel đã có sẵn trong repo: `content_agent.py:4,48` dùng
  `ThreadPoolExecutor(max_workers=MAX_CONTENT_WORKERS=3)` + `as_completed`. Sẽ bám theo cho nhất quán.
- `get_mcp_client()` trả singleton MCPToolClient; `search_media → server.handle_request → tool.execute` là sync, in-process, gọi Tavily qua httpx.

## Vì sao ThreadPoolExecutor (không phải asyncio)
- Tool stack hiện tại toàn **sync blocking** (`def execute`). Threadpool giải phóng
  thời gian chờ I/O (HTTP Tavily) mà không phải async hóa toàn bộ chuỗi tool.
- Đồng nhất với cách `content_agent` đã làm → dễ đọc, dễ bảo trì.
- I/O-bound nên GIL không cản (thread nhả GIL khi chờ socket).

## Thay đổi cụ thể

### File: `src/llm/agents/media_research.py`

1. Thêm import:
   ```python
   from concurrent.futures import ThreadPoolExecutor, as_completed
   ```

2. Thêm hằng số workers (cạnh `_MAX_MEDIA_LOOKUPS`):
   ```python
   _MEDIA_LOOKUP_WORKERS = 4   # = _MAX_MEDIA_LOOKUPS, mỗi item 1 worker
   ```

3. Tách phần xử lý 1 item ra method riêng `_enrich_single_item(item, *, client, topic, grade, book) -> bool`:
   - Chứa nguyên logic hiện tại trong thân vòng lặp (dòng 59-116): build query, chuẩn hóa media_type, gọi `client.search_media`, chọn `picked`, mutate `item` in-place, return True nếu set được url, False nếu không.
   - try/except giữ nguyên: lỗi 1 item → log warning, return False (không làm hỏng item khác).
   - Vì mỗi worker chỉ ghi vào **item của riêng nó** → không cần lock.

4. Viết lại `_enrich_media_urls` để fan-out:
   ```python
   def _enrich_media_urls(self, payload, *, topic, grade, book) -> bool:
       items = (payload.get("hero_media") or []) + (payload.get("inline_media") or [])
       items = [item for item in items if not item.get("url")][:_MAX_MEDIA_LOOKUPS]
       if not items:
           return False

       client = get_mcp_client()
       results = []
       with ThreadPoolExecutor(max_workers=min(_MEDIA_LOOKUP_WORKERS, len(items))) as executor:
           futures = [
               executor.submit(
                   self._enrich_single_item,
                   item, client=client, topic=topic, grade=grade, book=book,
               )
               for item in items
           ]
           for future in as_completed(futures):
               try:
                   results.append(future.result())
               except Exception as exc:
                   logger.warning("Media enrich worker failed | error=%s", str(exc)[:160])
                   results.append(False)
       return any(results)
   ```

## An toàn / rủi ro
- **Mutate in-place an toàn**: mỗi item là object dict riêng, mỗi worker xử lý đúng 1 item → không có 2 thread ghi cùng object. `touched`/`any(results)` thay cờ cũ.
- **Thread-safety của client singleton**: `search_media → handle_request → tool.execute` cần stateless. `WebSearchTool.execute` gọi Tavily qua httpx mỗi lần độc lập, không giữ state mutable dùng chung. → an toàn cho đọc song song. (Nếu sau này tool có state mutable, cần xem lại — note trong PR.)
- **Thứ tự**: media items không phụ thuộc thứ tự xử lý (mỗi cái tự ghi url của mình) → `as_completed` không gây sai lệch. Thứ tự hiển thị do merger/exporter quyết định theo list gốc, không đổi.
- **Số worker**: `min(4, len(items))` — nhỏ, không gây quá tải Tavily (vốn đã cap 4 lookups).

## Tests — `tests/test_mcp_tool_integration.py`
- Test cũ `test_media_research_agent_enriches_instruction`,
  `test_media_enrichment_limits_lookups_and_normalizes_type`,
  `test_media_research_agent_keeps_placeholder_on_failure` PHẢI vẫn pass
  (kết quả giống hệt, chỉ khác thứ tự thực thi).
- Thêm 1 test khẳng định nhiều item được enrich song song vẫn đúng:
  `test_media_enrichment_parallel_populates_all_items` — fake client trả url khác nhau theo query, assert cả N item đều có url đúng (không bị lẫn item).
- Chạy: `./venv/bin/python -m pytest tests/test_mcp_tool_integration.py -q`.

## Không đụng tới
- `slide_export_service.py`, `slide_merger.py`, schema — không liên quan.
- Cache (theo yêu cầu: không thêm cache).
- Cơ chế MCP in-process (không đổi sang HTTP ở plan này).
