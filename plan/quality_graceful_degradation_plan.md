# Plan: Graceful degradation cho quality review (không vứt deck)

## Context / Vấn đề
Hiện tại khi quality reviewer fail và hết lượt revise, pipeline trả về **rỗng** —
người dùng chờ 5–7 phút rồi nhận "Không thể tạo slide", dù **deck đã được tạo xong**
(`merged_slides` tồn tại đầy đủ). Trải nghiệm rất tệ.

Reviewer thường bắt trúng lỗi thật (vd slide thiếu code), nhưng dùng nó làm **cổng chặn
nhị phân** là sai về sản phẩm: một deck loại B + ghi chú "phần nào chưa đạt" vẫn hữu ích
hơn nhiều so với con số 0, và đúng triết lý "bản nháp chất lượng cao để giáo viên chỉnh sửa".

Mục tiêu: **chỉ chặn hẳn khi nội dung thực sự nghiêm trọng** (unsafe / ungrounded / quá vỡ /
không có deck). Còn lại → **trả deck kèm cảnh báo** các điểm chưa đạt cho user tự sửa.

## Hiện trạng (đã xác minh)
- `content_supervisor.reflection_decision_node` (`content_supervisor.py:222-281`):
  hết `MAX_REFLECTION_ATTEMPTS` (=2, dòng 30) → terminal branch `:276` set
  `quality_blocked=True, status="failed"`. **Không** null `merged_slides` → deck vẫn còn trong state.
- 2 cổng chặn ở consumer (`slide_service.py`):
  - sync `_process_completed_result` `:323`: `if result.get("quality_blocked") or self.should_block_by_quality(quality_review): yield block_msg; return`
  - streaming twin `:761`/`:798`: pattern y hệt.
- `should_block_by_quality` (`slide_service.py:32-36`): chặn nếu `reflection_action in ("block","ask_human")` — **bỏ qua score/severity hoàn toàn**.
- `QualityReviewResult` (`slide_schemas.py:264-297`) ĐÃ có sẵn dữ liệu để chấm mềm:
  `score: float (0-10)`, `issues: List[QualityIssue]` mỗi cái có `severity: minor|major|critical`,
  `reason_fail`, `summary`, `revision_instruction`, `requires_human_review`.
- Khi `merged` rỗng / `status=="failed"` đã có nhánh riêng (`:358`) → giữ nguyên, không đụng.
- Cả `content_supervisor` và `slide_service` đều đã import từ `slide_schemas` → đặt policy ở đó là chỗ trung lập, không tạo vòng import.

## Thiết kế: 3 mức thay vì nhị phân
Phân loại kết quả thành `approve | warn | block`:
- **approve**: `passed=True` và `reflection_action=="approve"` → render bình thường (như cũ).
- **block (hard)**: chỉ khi THỰC SỰ nghiêm trọng:
  - không có deck (`merged` rỗng) — đã xử lý sẵn ở nhánh `:358`, không cần policy, nhưng policy vẫn return block để an toàn; HOẶC
  - có issue `severity=="critical"`; HOẶC
  - `reason_fail` thuộc tập HARD (unsafe/ungrounded/hallucination); HOẶC
  - `score < HARD_FLOOR`.
- **warn (soft)**: mọi trường hợp fail còn lại (major/minor, score ổn, deck có) →
  **render deck + đính kèm cảnh báo** dựng từ `issues`/`summary`/`revision_instruction`.

> Quyết định: reviewer tự crash (`fallback_fail` → `reason_fail=FORMAT_INVALID`, `requires_human_review=True`)
> coi là **soft/warn** ("chưa kiểm định được chất lượng") miễn là deck tồn tại — vì đó là lỗi hạ tầng,
> không phải phán xét nội dung; ưu tiên trả kết quả cho user. (Có thể chỉnh sau nếu muốn chặt hơn.)

## Thay đổi cụ thể

### 1. `src/config/config.py` — thêm ngưỡng (chỉnh được qua .env)
```python
SLIDE_QUALITY_HARD_FLOOR: float = 4.0     # score < ngưỡng này → chặn hẳn
# (HARD reason codes để hardcode trong policy, không cần env)
```
Thêm dòng tương ứng vào `.env.example`.

### 2. `src/schemas/slide_schemas.py` — policy tập trung (single source of truth)
Thêm hàm thuần (đặt cạnh `QualityReviewResult`), nhận dict (vì state lưu dict đã `model_dump`):
```python
_HARD_REASONS = {"UNSAFE", "UNGROUNDED", "HALLUCINATION", "UNSAFE_CONTENT"}

def classify_quality(review: Optional[dict], has_deck: bool, *, hard_floor: float) -> str:
    """Trả 'approve' | 'warn' | 'block'."""
    if not has_deck:
        return "block"
    if not isinstance(review, dict):
        return "warn"                      # không review được nhưng có deck → cho qua + cảnh báo
    if review.get("passed") and review.get("reflection_action") == "approve":
        return "approve"
    issues = review.get("issues") or []
    if any((i or {}).get("severity") == "critical" for i in issues):
        return "block"
    reason = (review.get("reason_fail") or "").upper()
    if reason in _HARD_REASONS:
        return "block"
    try:
        if float(review.get("score") or 0.0) < hard_floor:
            return "block"
    except (TypeError, ValueError):
        pass
    return "warn"

def build_quality_warnings(review: Optional[dict]) -> list[str]:
    """Dựng các dòng cảnh báo từ issues (major/minor) + summary cho user."""
    # lấy issue.message (+ suggestion nếu có), fallback summary/revision_instruction
```
(Export cả hai trong `__all__`.)

### 3. `src/llm/graphs/content_supervisor.py` — terminal branch không chặn mù
Sửa `reflection_decision_node:276-281`: thay vì luôn `quality_blocked=True`,
gọi `classify_quality(review, has_deck=bool(state.get("merged_slides")), hard_floor=settings.SLIDE_QUALITY_HARD_FLOOR)`:
- `"block"` → giữ như cũ (`quality_blocked=True, status="failed"`).
- ngược lại (`"warn"`) → `quality_blocked=False, status="success"`, **giữ nguyên `merged_slides` + `quality_review`** (không null), để consumer render kèm cảnh báo.

> Lưu ý: `route_after_reflection` (`:448`) vẫn END ở nhánh này (action vẫn là block/không phải revise) — đúng, ta muốn dừng vòng lặp, chỉ khác là không chặn output.

### 4. `src/llm/services/slide_service.py` — render deck + cảnh báo thay vì chặn
- Thay `should_block_by_quality(quality_review)` bằng policy mới ở **cả 2 nhánh** (`:323` và `:761`):
  ```python
  verdict = classify_quality(quality_review, has_deck=bool(merged), hard_floor=settings.SLIDE_QUALITY_HARD_FLOOR)
  if result.get("quality_blocked") and verdict == "block":   # chỉ chặn khi hard
      ... yield _quality_block_user_message ...; return
  ```
  (Giữ `_quality_block_user_message` cho nhánh hard.)
- Khi `verdict == "warn"`: đi tiếp xuống path render bình thường (`:368+`), và **trước khi kết thúc**:
  - lưu `slide_state.slide_output["quality_warnings"] = build_quality_warnings(quality_review)` để API/frontend dùng.
  - `yield` thêm một khối cảnh báo, ví dụ:
    ```
    ⚠️ Slide đã tạo nhưng còn vài điểm nên chỉnh sửa thêm:
    - <message> (gợi ý: <suggestion>)
    📌 Bạn có thể tải file và bổ sung trực tiếp các phần này.
    ```
- DRY: tách phần "dựng + yield khối cảnh báo" thành 1 helper dùng chung cho cả 2 consumer để khỏi lệch nhau.

## Tests — `tests/test_*` (theo pattern hiện có)
- `classify_quality`: approve / warn / block cho từng case (critical issue → block; score < floor → block; major-only + score ổn → warn; no deck → block; review=None + deck → warn).
- `build_quality_warnings`: lấy đúng message + suggestion, fallback summary.
- `reflection_decision_node`: soft fail (issues major, score 6, có merged) → `quality_blocked=False`, giữ `merged_slides`; critical issue → `quality_blocked=True`.
- `slide_service` consumer: result có `merged` + quality_review fail-mềm → output chứa display deck **và** dòng "⚠️ ... nên chỉnh sửa", KHÔNG chứa "Không thể tạo"; fail-cứng (critical) → vẫn ra block message.
- Chạy: `./venv/bin/python -m pytest tests/ -q`.

## Ngoài phạm vi (làm riêng nếu cần)
- Sửa `ContentAgent` để bắt buộc trích code/output từ context vào slide ví dụ (chữa gốc cái reviewer phàn nàn) — plan riêng, đụng prompt.
- Không tăng `MAX_REFLECTION_ATTEMPTS` (tốn thêm LLM call, không giải quyết gốc).
- Không đổi prompt reviewer.

## Rủi ro
- **Hai consumer dễ lệch**: bắt buộc dùng chung policy + helper cảnh báo, không copy-paste logic.
- **Nới quá tay**: HARD_FLOOR + critical-severity + HARD_REASONS giữ cho nội dung nguy hiểm/bịa vẫn bị chặn. Ngưỡng để ở config, tinh chỉnh được sau khi quan sát thực tế.
- **reviewer-crash thành "warn"**: chấp nhận có rủi ro cho qua nội dung chưa kiểm định khi reviewer lỗi hạ tầng — đánh đổi có chủ đích, ưu tiên trả kết quả; ghi rõ trong cảnh báo cho user.
