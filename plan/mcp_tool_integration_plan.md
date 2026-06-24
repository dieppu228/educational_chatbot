# Plan: Web Search tool qua MCP cho Slide Service (output = ảnh / GIF / animation theo instructions)

> **Đối tượng thực thi:** codex coder. Plan mô tả từng file, signature, chỗ khởi tạo, chỗ consume.
> Làm đúng thứ tự Step. Không đổi tên file/class đã tồn tại trừ khi plan nói rõ.

---

## 0. Context — tại sao & phạm vi

**Hiện trạng (đã verify):**

- Tầng MCP (`src/tools/`) đã viết đủ class (`BaseTool`, `ToolRegistry`, `MCPToolServer`,
  `MCPToolClient`, `mcp_protocol`) nhưng là **dead code** — không chỗ nào khởi tạo runtime
  (chỉ xuất hiện trong docstring `tool_registry.py:6-12`). Không dùng FastMCP/MCP SDK; đây là
  bản **in-process tự viết** (client giữ ref trực tiếp tới server, gọi `server.handle_request(req)`,
  không transport mạng). **Giữ nguyên kiến trúc in-process.**
- `WebSearchTool` (`src/tools/implementations/web_search_tool.py`, `name="web_search"`) **đã sẵn
  sàng**, không cần sửa logic `execute()`:
  - Hỗ trợ `search_mode ∈ {text, media, mixed}`, `media_types ∈ {image, gif, animation, diagram, infographic}`.
  - Trả `WebSearchOutput{results[], media_items[], total_results, total_media, query_used, search_mode}`.
  - `media_items[]` mỗi phần tử = `MediaItem{url, description, source_url, source_title, media_type, relevance_score}`.
  - `_detect_media_type()` phân loại gif/animation/diagram/infographic/image từ URL + description.
  - Backing service `TavilyService` (base_url đang **mock** — fail nhanh, raise `TavilyServiceError`).
- Consumer media hiện tại: `MediaAgent._execute`
  (`src/llm/handlers/content/slide_agents/media_agent.py`) gọi LLM theo prompt
  `src/llm/prompts/md/slide_media.md`, sinh:
  ```json
  { "hero_media":  [{"caption": "...", "type": "image"}],
    "inline_media":[{"caption": "...", "type": "image", "for_slide_type": "content"}] }
  ```
  rồi **set `url=None` cho mọi item** (placeholder). → Đây là "instructions": `caption` + `type`
  của từng item chính là chỉ dẫn để web_search đi tìm đúng loại media.

**Phạm vi plan này (HẸP — chỉ web search):**
1. Khởi tạo tầng MCP in-process 1 lần lúc startup, **đăng ký `web_search`** (singleton client).
2. Cho slide flow (`MediaResearchAgent`) gọi `web_search` qua MCP client, dùng **instructions
   (caption + type)** của LLM làm query/loại media → **output là ảnh/GIF/animation... URL thật**.
3. Best-effort + guard latency + fallback giữ `url=None` khi mock/lỗi (không vỡ luồng).

**NGOÀI phạm vi (KHÔNG làm — risk cao, đã loại):**
- KHÔNG ép RAG/`knowledge_retrieval` đi qua MCP. 6 call-site `rag_service.get_context(...)`
  (slide/quiz/explain, sync+async) **giữ nguyên gọi trực tiếp**. (Tùy chọn: vẫn có thể *đăng ký*
  `knowledge_retrieval` vào registry như system tool có sẵn — KHÔNG reroute caller — zero risk;
  xem note ở Step 1, mặc định bật.)
- KHÔNG đụng orchestration tools (`src/llm/graphs/tools.py`), `content_supervisor.py`, `SlideMerger`
  logic, `TavilyService`, schema trong `src/tools/schemas.py`.

**Lưu ý 2 tầng tool (đừng nhầm):** `graphs/tools.py` (`@tool` LangChain) = orchestration, supervisor
quyết định gọi specialist — KHÔNG đổi. `src/tools/` (MCP) = data-access tool cho specialist agent —
đây là phần wire (chỉ `web_search` trong iteration này).

---

## 1. Step 1 — Bootstrap module (singleton MCP layer)

**File mới:** `src/tools/bootstrap.py`

Dùng singleton process-global thay vì DI xuyên suốt, vì `generate_media` (graphs/tools.py) khởi tạo
`MediaResearchAgent()` trực tiếp, `MediaResearchAgent._run` khởi tạo `MediaAgent()` trực tiếp — không
có sẵn đường DI. Singleton + accessor là cách gọn nhất.

```python
# src/tools/bootstrap.py
"""bootstrap.py — Khởi tạo tầng MCP in-process 1 lần và cấp client singleton.

web_search: luôn đăng ký (tool chính của iteration này).
knowledge_retrieval: đăng ký như SYSTEM TOOL có sẵn nếu truyền rag_service (KHÔNG reroute caller).
content_formatter: luôn đăng ký.
"""
import logging
from typing import Optional

from src.tools.implementations.tool_registry import ToolRegistry
from src.tools.implementations.web_search_tool import WebSearchTool
from src.tools.implementations.content_formatter_tool import ContentFormatterTool
from src.tools.implementations.knowledge_retrieval_tool import KnowledgeRetrievalTool
from src.tools.mcp_server import MCPToolServer
from src.tools.mcp_client import MCPToolClient

logger = logging.getLogger("chatbot.tools.bootstrap")

_client: Optional[MCPToolClient] = None


def init_tool_layer(rag_service=None, tavily_service=None) -> MCPToolClient:
    """Build registry → server → client (gọi lúc startup). Idempotent: gọi lại sẽ rebuild."""
    global _client
    registry = ToolRegistry()
    registry.register(WebSearchTool(tavily_service))      # TOOL CHÍNH
    registry.register(ContentFormatterTool())
    if rag_service is not None:
        registry.register(KnowledgeRetrievalTool(rag_service))  # system tool có sẵn, không reroute
    server = MCPToolServer(registry)
    _client = MCPToolClient(server)
    logger.info("MCP tool layer initialized: %s", [t.name for t in registry.list_all()])
    return _client


def get_mcp_client() -> MCPToolClient:
    """Trả client singleton. Lazy-init (chỉ web_search + formatter, KHÔNG RAG) nếu chưa init."""
    global _client
    if _client is None:
        logger.warning("MCP client chưa init — lazy-init web_search/formatter (không RAG).")
        init_tool_layer()
    return _client


def reset_tool_layer() -> None:
    """Cho test."""
    global _client
    _client = None
```

**Export** trong `src/tools/__init__.py`: thêm
`from src.tools.bootstrap import init_tool_layer, get_mcp_client, reset_tool_layer` và 3 tên vào `__all__`.

---

## 2. Step 2 — Init lúc startup

**File sửa:** `src/llm/orchestrator.py` — trong `Orchestrator.__init__`, ngay sau dòng 47
`self.rag_service = RAGService(retriever, reranker)`:

```python
self.rag_service = RAGService(retriever, reranker)

# ── MCP tool layer (in-process) ──
from src.tools.bootstrap import init_tool_layer
init_tool_layer(rag_service=self.rag_service)
```

Orchestrator dựng đúng 1 lần ở `app/api.py:38` và `src/e2e_debug_runner.py:100` → không cần đụng
`app/api.py`. Sau dòng này mọi `get_mcp_client()` trong process đều có `web_search`.

---

## 3. Step 3 — Cho instructions yêu cầu được cả GIF/animation (không chỉ image)

**File sửa:** `src/llm/prompts/md/slide_media.md`

Hiện prompt chỉ gợi `"type": "image"`. Mở rộng để LLM được phép yêu cầu loại media động khi phù hợp
(ví dụ minh hoạ vòng lặp → GIF/animation). Sửa QUY TẮC + ví dụ JSON:

- Cho phép `"type" ∈ {"image", "gif", "animation", "diagram", "infographic"}`.
- Thêm hướng dẫn: dùng `"gif"`/`"animation"` cho khái niệm có chuyển động (thuật toán, vòng lặp,
  mô phỏng); `"diagram"`/`"infographic"` cho cấu trúc/quan hệ; còn lại `"image"`.
- Giữ nguyên `caption` (mô tả rõ → dùng làm query) và `for_slide_type`.

> `caption` + `type` = "instructions" điều khiển web_search ở Step 4.

---

## 4. Step 4 — `MediaResearchAgent` gọi `web_search` qua MCP → điền media thật

Giữ `MediaAgent` là pure-LLM handler (KHÔNG đụng). Enrich ở `MediaResearchAgent._run` (đúng ranh
giới agent, có field `used_tools`).

**File sửa:** `src/llm/agents/media_research.py`

```python
from src.tools.bootstrap import get_mcp_client

# Guard latency: chặn trên số lần search; chỉ search item chưa có url.
_MAX_MEDIA_LOOKUPS = 4

def _run(self, task: AgentTask) -> AgentTaskResult:
    inputs = task.inputs
    agent = MediaAgent()
    result = agent.run(topic=inputs.get("topic", ""),
                       grade=inputs.get("grade", ""),
                       book=inputs.get("book", ""))
    payload = result.payload or {}
    used_tools = ["llm_generation"]
    if result.status == "success" and self._enrich_media_urls(
        payload, topic=inputs.get("topic", ""),
        grade=inputs.get("grade", ""), book=inputs.get("book", "")):
        used_tools.append("web_search")
    return AgentTaskResult(
        task_id=task.task_id, agent_id=self.agent_id, status=result.status,
        artifact_type=task.expected_artifact or "media_payload",
        artifact=payload,
        confidence=0.75 if result.status == "success" else None,
        used_tools=used_tools, latency_ms=result.latency_ms,
        error_code=result.error_code, error_message=result.error_message,
    )

def _enrich_media_urls(self, payload: dict, *, topic, grade, book) -> bool:
    items = (payload.get("hero_media") or []) + (payload.get("inline_media") or [])
    items = [it for it in items if not it.get("url")][: self._MAX_MEDIA_LOOKUPS]
    if not items:
        return False
    client = get_mcp_client()
    touched = False
    for it in items:
        q = (it.get("caption") or it.get("description") or topic or "").strip()
        if not q:
            continue
        media_type = it.get("type") or "image"            # instructions → loại media
        resp = client.search_media(                        # mode "media" (xem mcp_client.py:90)
            query=q, topic=topic, grade=grade, book=book,
            media_types=[media_type], top_k=3,
        )
        if not resp.success or not resp.data:
            continue                                        # mock/lỗi → giữ url=None (fallback)
        media = (resp.data or {}).get("media_items") or []
        # Ưu tiên item đúng media_type instructions yêu cầu; nếu không có thì lấy item đầu.
        pick = next((m for m in media if m.get("media_type") == media_type), media[0] if media else None)
        if pick:
            it["url"] = pick.get("url") or it.get("url")
            it["media_type"] = pick.get("media_type", media_type)
            it.setdefault("source_url", pick.get("source_url", ""))
            it.setdefault("source_title", pick.get("source_title", ""))
            touched = True
    return touched
```

**Kết nối vấn đề latency:** mỗi lookup = 1 HTTP Tavily. `_MAX_MEDIA_LOOKUPS=4` + `search_mode="media"`
+ `top_k=3` + timeout `settings.TAVILY_TIMEOUT_SECONDS` chặn trên chi phí. Khi `TAVILY_BASE_URL` còn
mock → `resp.success=False` → giữ `url=None`, **không raise, không chậm thêm đáng kể** (httpx fail nhanh).

---

## 5. Step 5 — Đảm bảo media URL chảy được tới slide cuối

Sau enrich, `media_payload` item có `url` thật. Cần xác nhận `SlideMerger.merge(... media_result ...)`
gắn media vào `MergedSlide.media` (không drop). **Đọc `src/llm/services/slide_merger.py` phần map media**
trước khi sửa:
- Nếu merger đã map `media_payload` → `MergedSlide.media` đầy đủ (url + media_type) → **không cần sửa**.
- Nếu merger chỉ map theo `caption`/bỏ `url` → bổ sung map `url`, `media_type`, `source_url` vào
  `MergedSlide.media`. Tương tự kiểm `slide_export_service.py` có render `media[].url` không.

> Đây là bước "làm media thật sự hiển thị". Chỉ sửa nếu phát hiện drop; ưu tiên thay đổi tối thiểu.

---

## 6. Files tổng hợp

| File | Hành động |
|---|---|
| `src/tools/bootstrap.py` | **TẠO MỚI** — `init_tool_layer` / `get_mcp_client` / `reset_tool_layer`. |
| `src/tools/__init__.py` | Export 3 hàm bootstrap. |
| `src/llm/orchestrator.py` | Gọi `init_tool_layer(rag_service=self.rag_service)` sau dòng 47. |
| `src/llm/prompts/md/slide_media.md` | Cho phép `type ∈ {image,gif,animation,diagram,infographic}`. |
| `src/llm/agents/media_research.py` | Thêm `_enrich_media_urls` + gọi `get_mcp_client().search_media`. |
| `src/llm/services/slide_merger.py` | (Có điều kiện) map `url/media_type/source_url` vào `MergedSlide.media` nếu đang drop. |
| `tests/` | Test mới (Step 7). |

**KHÔNG đụng:** `WebSearchTool`/`TavilyService` logic, `MediaAgent` handler, `graphs/tools.py`,
`content_supervisor.py`, schema `src/tools/schemas.py`, và toàn bộ đường RAG (`get_context`).

---

## 7. Verification (end-to-end)

**A. Unit — tool layer khởi tạo & list đúng tool:**
```python
from src.tools.bootstrap import init_tool_layer, reset_tool_layer
reset_tool_layer()
client = init_tool_layer()                                   # không rag_service
names = {t["name"] for t in client.list_available_tools()}
assert "web_search" in names and "content_formatter" in names
```

**B. Unit — web_search trả media qua MCP (mock TavilyService):** inject `TavilyService` giả vào
`init_tool_layer(tavily_service=fake)`, fake trả `{"results":[...], "images":[{"url":".../loop.gif","description":"animated for loop"}]}`.
Gọi `client.search_media(query="vòng lặp for", media_types=["gif"])`; assert `resp.success`,
`resp.data["media_items"][0]["media_type"] == "gif"` và có `url`. Fallback: fake raise
`TavilyServiceError` → `resp.success is False`.

**C. Unit — MediaResearchAgent enrich từ instructions:** monkeypatch `get_mcp_client` trả client mock.
Cho `MediaAgent` (monkeypatch hoặc stub) trả payload có `hero_media=[{"caption":"...","type":"gif"}]`,
`url=None`. Chạy `MediaResearchAgent()._run(task)`; assert item có `url` được điền,
`media_type == "gif"`, và `"web_search" in result.used_tools`. Fallback: client mock `success=False`
→ `url` vẫn `None`, `used_tools` không có `web_search`, **không raise**.

**D. Smoke — full slide flow (base_url mock):** chạy generate slide qua orchestrator. Xác nhận:
pipeline xong bình thường, log `MCP tool layer initialized: [...web_search...]` xuất hiện đúng 1 lần,
media item giữ `url=None` (vì mock) mà KHÔNG vỡ luồng, slide vẫn export. (Khi cắm Tavily thật →
`url` được điền ảnh/GIF.)

**E. Lệnh chạy test:**
```bash
cd /home/dieppu/educational_chatbot
python -m pytest tests/ -k "mcp or web_search or media" -q
```

---

## 8. Ngoài phạm vi (ghi chú lần sau)

- Thay `TAVILY_BASE_URL` mock bằng endpoint Tavily thật (user tự làm) → media URL sẽ sống.
- Route RAG qua MCP (đã loại vì risk cao do `get_context` mutate `RequestContext`).
- Latency loop supervisor (LLM mỗi vòng) — task riêng.
