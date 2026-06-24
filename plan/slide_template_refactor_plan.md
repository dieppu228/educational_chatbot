# Plan: Refactor render slide sang placeholder-based + nâng cấp media

## Mục tiêu
Chuyển `SlideExportService` từ "vẽ textbox theo tọa độ tuyệt đối trên layout trống"
sang "đổ nội dung vào placeholder của layout thiết kế sẵn". Media fit đúng khung,
chọn layout theo tỉ lệ ảnh. **Không thêm LLM call nào** — toàn bộ là code deterministic.

## Hiện trạng (đã xác minh)
- `slide_export_service.py:40` load template nhưng `:58` mọi slide dùng `slide_layouts[6]` (Blank) → bỏ phí template.
- Template `app/templates/default_slide_template.pptx`: theme Office mặc định, 16:9 (13.33"x7.5"), 11 layout chuẩn CÓ SẴN placeholder dùng được ngay:
  - 0 `Title Slide`: idx0 CENTER_TITLE, idx1 SUBTITLE
  - 1 `Title and Content`: idx0 TITLE, idx1 OBJECT(body)
  - 2 `Section Header`: idx0 TITLE, idx1 BODY
  - 3 `Two Content`: idx0 TITLE, idx1 OBJECT, idx2 OBJECT
  - 7 `Content with Caption`: idx0 TITLE, idx1 OBJECT, idx2 BODY(caption)
  - 8 `Picture with Caption`: idx0 TITLE, idx1 PICTURE, idx2 BODY(caption)
- `MergedSlide` là Pydantic, được `model_dump()` thành dict trước khi tới exporter (slide_service nhận List[dict]).
- PIL đã cài sẵn (transitive qua python-pptx). httpx, python-pptx đã có trong requirements.
- Test pattern: `tests/test_mcp_tool_integration.py` (monkeypatch `_download_media`, assert shape types).

## Quyết định layout (deterministic, không LLM)
Map `slide_type` + có media + tỉ lệ ảnh → layout index:

| Điều kiện | Layout dùng |
|---|---|
| `slide_type=title` | 0 Title Slide (title→idx0, bullets→idx1 subtitle) |
| `slide_type=summary` hoặc section | 2 Section Header |
| `slide_type=exercise` | 1 Title and Content (text-only) |
| `content`, KHÔNG media | 1 Title and Content |
| `content` + ảnh DỌC (h>w) | 8 Picture with Caption (ảnh 1 cột) hoặc 3 Two Content (text trái/ảnh phải) |
| `content` + ảnh NGANG (w≥h) | 7 Content with Caption (text trên, ảnh khung dưới) |

Quyết định này tính trong **SlideMerger** (Option 1 — có đủ context), lưu vào field mới
`layout` của `MergedSlide`. Exporter chỉ đọc field này → render. Lý do tách:
merger biết tất cả (media count, content_detail, questions), exporter chỉ thực thi.

Lưu ý: tỉ lệ ảnh chỉ biết SAU khi download. Nên:
- Merger set layout "dự kiến" theo slide_type + có/không media.
- Exporter download ảnh → đọc kích thước bằng PIL → nếu cần đổi giữa layout ảnh-dọc/ảnh-ngang thì chọn lại tại render-time (việc này thuần tọa độ, rẻ).

## Các thay đổi cụ thể

### 1. `src/schemas/slide_schemas.py`
- Thêm field vào `MergedSlide`:
  ```python
  layout: Optional[str] = None  # gợi ý layout: "title"|"section"|"content"|"content_media"|"exercise"
  ```
  Optional + default None → backward compatible, không vỡ test/call cũ.

### 2. `src/llm/services/slide_merger.py`
- Trong `_merge_single_slide()` (sau khi attach media/quiz, trước return), thêm:
  ```python
  slide.layout = self._resolve_layout(slide)
  ```
- Thêm method `_resolve_layout(slide) -> str` thuần if/else dựa trên
  `slide_type`, `bool(slide.media)`, `bool(slide.content_detail)`, `len(slide.questions)`.

### 3. `src/llm/services/slide_export_service.py` (thay đổi chính)
Refactor `_add_slide` và các `_render_*`:
- Thêm bảng `LAYOUT_INDEX = {"title":0, "section":2, "content":1, "content_media_wide":7, "content_media_tall":8, "two_content":3, "exercise":1}` — map tên layout → index trong template. Có fallback nếu template thiếu layout (dùng Blank như cũ).
- Helper `_pick_layout(prs, name)` trả layout object, fallback an toàn.
- Helper `_set_placeholder_text(ph, lines, ...)`: clear text_frame, đổ từng dòng vào paragraph (kế thừa font/size/màu từ layout — KHÔNG set cứng size nữa, chỉ set khi cần fit).
- `_render_title_slide`: dùng layout Title Slide, gán `slide.placeholders[0].text=title`, `[1].text=subtitle`.
- `_render_content_slide`:
  - Không media → layout Title and Content, title→idx0, bullets→idx1 body placeholder.
  - Có media → download trước, đọc tỉ lệ bằng PIL:
    - ảnh dọc → layout Picture with Caption (8): `placeholders[1].insert_picture(BytesIO)` (tự fit khung), caption→placeholders[2]; bullets đặt vào... (layout 8 không có body cho bullet → fallback: dùng Two Content (3): bullets→idx1, ảnh→thêm vào idx2 placeholder bằng insert_picture).
    - ảnh ngang → Content with Caption (7): bullets→idx1, ảnh chèn khung dưới (idx1 là object — cân nhắc dùng add_picture canh theo bbox của placeholder idx1), caption→idx2.
  - **insert_picture tự crop-fit theo khung placeholder** → hết méo ảnh.
- `_render_exercise_slide`: layout Title and Content, câu hỏi→body placeholder.
- Giữ nguyên: `_download_media`, `_is_public_media_url`, `_write_notes`, validation, cache. GIF: content-type `image/gif` vẫn pass filter `image/` hiện có (slide_export_service.py:195) → embed được; chỉ động khi mở bằng PowerPoint thật (LibreOffice/preview ảnh tĩnh) — sẽ ghi chú.
- Media chọn theo `relevance_score` (nếu có) thay vì luôn `[0]`: sort media desc theo score trước khi lấy.
- Đọc kích thước ảnh: `from PIL import Image; Image.open(BytesIO(bytes)).size`. Thêm `Pillow` vào requirements.txt cho tường minh (dù đang có transitive).

### 4. `requirements.txt`
- Thêm `Pillow>=10.0` (làm rõ dependency, tránh vỡ khi python-pptx bỏ transitive).

### 5. Tests — `tests/test_mcp_tool_integration.py`
- Thêm/cập nhật:
  - `test_merger_sets_layout_field`: merge xong, content+media slide có `layout` đúng.
  - `test_export_uses_named_layout`: export 1 deck, assert slide dùng đúng layout (kiểm tra qua `slide.slide_layout.name`).
  - `test_export_inserts_picture_into_placeholder` (mở rộng test cũ): ảnh dọc/ngang → đúng layout, có PICTURE shape.
  - Giữ test cũ `_is_public_media_url` chặn 127.0.0.1 — không đổi.

## QA offline (mượn từ pptx skill — KHÔNG vào runtime)
Tạo script `scripts/qa_slides.py` (tùy chọn, chạy tay/CI):
- `soffice --headless --convert-to pdf <deck>.pptx` → `pdftoppm -jpeg -r 150` → ảnh.
- `python -m markitdown <deck>.pptx | grep -iE "xxxx|lorem|placeholder"` bắt text sót.
- Dùng để kiểm thử khi đổi template, không nằm trong hot-path.

## Thứ tự thực hiện
1. Schema: thêm `layout` field (an toàn, không vỡ gì).
2. Merger: `_resolve_layout` + gán field.
3. Exporter: refactor render sang placeholder + media aspect-aware.
4. requirements: thêm Pillow.
5. Tests: thêm 3 test, chạy `venv/bin/pytest tests/test_mcp_tool_integration.py`.
6. (tùy chọn) script QA offline.

## Rủi ro & cách giảm
- **Template hiện chỉ là theme Office mặc định** (chưa đẹp). Plan này làm cho code DÙNG ĐÚNG placeholder; còn việc làm template ĐẸP (palette/motif/font theo pptx skill) là bước thiết kế riêng sau — code không phụ thuộc template cụ thể, chỉ cần layout có đúng placeholder idx. Nếu sau này thay template đẹp hơn (giữ tên layout/idx), code không phải sửa.
- **Layout thiếu placeholder mong đợi** → helper `_pick_layout` + `_set_placeholder_text` có fallback về cách vẽ textbox cũ, không crash.
- **insert_picture đổi behavior** so với add_picture → giữ fallback add_picture nếu placeholder không phải PICTURE type.
- **Backward compat**: `layout=None` (slide cũ/đường khác) → exporter suy ra layout từ slide_type như cũ.

## Không làm (ngoài phạm vi)
- Không thêm LLM/agent nào.
- Không tự generate template đẹp trong plan này (tách thành task thiết kế riêng).
- Không đổi pipeline LLM, không đổi MCP media search.
