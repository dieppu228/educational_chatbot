---
status: done
created: 2026-08-31
last_updated: 2026-08-31
---

# Plan: Nâng cấp hệ thống xuất slide bằng `python-pptx`

## Implementation result

- Hoàn thành 45/45 implementation tasks ngày 2026-08-31, gồm offline mock runner follow-up.
- Automated regression và LibreOffice visual QA: `109 passed` ngày 2026-08-31.
- `py_compile`, template contract validation, deterministic template rebuild và `git diff --check` đều pass.
- LibreOffice đã convert fixture deck sang PDF/PNG, xác nhận đủ trang và không có trang trắng; checklist PowerPoint thủ công bên dưới vẫn để mở cho nghiệm thu Presenter View/khả năng chỉnh sửa trực tiếp.

## Summary

Nâng `SlideExportService` từ exporter text/ảnh cơ bản thành engine tạo PowerPoint theo template, hỗ trợ văn bản, ảnh, code, bảng, biểu đồ, quy trình, so sánh và quiz bằng dữ liệu có cấu trúc.

Kết quả cần đạt:

- Dùng bundled template học thuật hiện đại 16:9 và manifest mô tả layout/placeholder.
- Không hard-code thứ tự layout hoặc placeholder trong renderer.
- Pipeline sinh typed content blocks có `source_chunk_ids`.
- Nội dung dài tự tách slide, không cắt giữa câu.
- Slide quiz không lộ đáp án; đáp án nằm trong notes và answer-key cuối deck.
- Payload cũ chỉ có `bullets`, `media`, `questions` vẫn export được.
- PPTX mở được trong PowerPoint và LibreOffice mà không yêu cầu repair.
- Không thêm LLM call; chỉ mở rộng output của content call hiện có.
- Giữ nguyên API tải file hiện tại.

Plan này mở rộng baseline đã triển khai trong `plan/slide_template_refactor_plan.md`; không thực hiện lại refactor placeholder cơ bản.

## Public interfaces và schemas

### Typed content blocks

Mở rộng `OutlineSlide`:

```python
layout_hint: Literal[
    "auto",
    "content",
    "image",
    "code",
    "table",
    "chart",
    "process",
    "comparison",
] = "auto"
```

Mở rộng `ContentSlide` và `MergedSlide`:

```python
blocks: list[SlideContentBlock] = []
```

`SlideContentBlock` là Pydantic discriminated union theo `type`:

| Block | Fields bắt buộc |
|---|---|
| `bullets` | `items`, `source_chunk_ids` |
| `paragraph` | `text`, `source_chunk_ids` |
| `code` | `code`, `language`, `caption`, `source_chunk_ids` |
| `table` | `columns`, `rows`, `caption`, `source_chunk_ids` |
| `chart` | `chart_type`, `categories`, `series`, `caption`, `source_chunk_ids` |
| `process` | `steps`, `source_chunk_ids` |
| `comparison` | `left_title`, `left_items`, `right_title`, `right_items`, `source_chunk_ids` |
| `callout` | `text`, `tone`, `source_chunk_ids` |

Quy tắc tương thích:

- `blocks` là canonical input của exporter mới.
- Nếu `blocks` rỗng nhưng `bullets` có dữ liệu, merger tạo một `bullets` block.
- Nếu LLM trả `blocks`, content normalizer tạo lại `bullets` từ bullet block đầu tiên để UI/session cũ tiếp tục hoạt động.
- `media` và `questions` tiếp tục là artifact riêng; render planner chuyển chúng thành image/quiz regions khi export.
- Không xóa hoặc đổi tên field cũ.

### Export metadata

Giữ nguyên `file_id`, `filename`, `download_url`, `format`; bổ sung:

```json
{
  "template_id": "academic_vi",
  "template_version": "1.0",
  "source_slide_count": 10,
  "exported_slide_count": 14,
  "warnings": []
}
```

## Tasks

### GOAL-001: Chuẩn hóa contract sinh nội dung

| ID | Task | Done | Date |
|---|---|---|---|
| TASK-001 | Thêm `layout_hint`, typed block models và `blocks` vào slide schemas bằng Pydantic discriminated union. | ✅ | 2026-08-31 |
| TASK-002 | Validate table phải hình chữ nhật; chart phải có số category bằng số value của mọi series; process tối thiểu 2 bước; comparison phải có đủ hai phía. | ✅ | 2026-08-31 |
| TASK-003 | Giới hạn chart V1 ở `column`, `bar`, `line`, `pie`, `doughnut`; dữ liệu không hợp lệ downgrade thành table hoặc bullets kèm warning. | ✅ | 2026-08-31 |
| TASK-004 | Cập nhật slide outline prompt để chọn `layout_hint` theo mục tiêu sư phạm. | ✅ | 2026-08-31 |
| TASK-005 | Cập nhật content prompt để trả `blocks`; chỉ tạo chart/table khi context có dữ liệu và mỗi block phải có `source_chunk_ids`. | ✅ | 2026-08-31 |
| TASK-006 | Chuẩn hóa output trong `ContentAgent`; block không hợp lệ fallback về bullet từ `key_points`, không làm hỏng pipeline. | ✅ | 2026-08-31 |
| TASK-007 | Thread `blocks` qua content agent, agent protocol, `SlideMerger`, graph artifact và session persistence. | ✅ | 2026-08-31 |
| TASK-008 | Cập nhật quality-review prompt để kiểm tra grounding của code, bảng và biểu đồ; số liệu không có nguồn phải `revise_content`. | ✅ | 2026-08-31 |
| TASK-009 | Sửa media matching để media chưa có URL vẫn gắn theo `for_slide_id`, sau đó theo `query + caption`; exporter render placeholder khi tải ảnh thất bại. | ✅ | 2026-08-31 |

### GOAL-002: Tạo bundled template và template contract

| ID | Task | Done | Date |
|---|---|---|---|
| TASK-010 | Tạo template `academic_vi` 16:9 với palette navy `#17324D`, teal `#0F766E`, mint `#DDF4F1`, amber `#F59E0B`, nền `#F7FAFC`, chữ `#1F2937`. | ✅ | 2026-08-31 |
| TASK-011 | Dùng Arial cho title/body và Courier New cho code; title 28–32 pt, body 18–22 pt, caption 11–12 pt. | ✅ | 2026-08-31 |
| TASK-012 | Tạo layout `EDU_TITLE`, `EDU_SECTION`, `EDU_CONTENT`, `EDU_CONTENT_MEDIA`, `EDU_CODE`, `EDU_TABLE`, `EDU_CHART`, `EDU_PROCESS`, `EDU_COMPARISON`, `EDU_EXERCISE`, `EDU_ANSWER_KEY`, `EDU_SUMMARY`. | ✅ | 2026-08-31 |
| TASK-013 | Tạo manifest JSON cạnh template, chứa template ID/version, aspect ratio, layout name và semantic role → placeholder `idx` + expected type. | ✅ | 2026-08-31 |
| TASK-014 | Viết `TemplateRegistry` lookup layout bằng tên và placeholder bằng manifest; không dùng `slide_layouts[n]` trong renderer. | ✅ | 2026-08-31 |
| TASK-015 | Validate template khi exporter khởi tạo: file đọc được, đúng 16:9, đủ layout, placeholder và type. | ✅ | 2026-08-31 |
| TASK-016 | Template contract sai phải tạo `export_error`; nội dung generate và session vẫn được giữ, không trả PPTX lỗi. | ✅ | 2026-08-31 |
| TASK-017 | Giữ template hiện tại làm fixture legacy; runtime chuyển sang template `academic_vi`. | ✅ | 2026-08-31 |

### GOAL-003: Tạo render planner và overflow engine

Luồng mới:

```text
MergedSlide
→ backward-compat normalization
→ SlideRenderPlanner
→ overflow expansion
→ RenderSlideModel[]
→ layout renderer
→ post-render validation
→ PPTX
```

Layout precedence:

1. `title`, `summary`, `exercise` theo `slide_type`.
2. `chart`, `table`, `code`, `comparison`, `process` theo rich block.
3. Text + media dùng `EDU_CONTENT_MEDIA`.
4. Media không tải được vẫn dùng layout media với placeholder.
5. Còn lại dùng `EDU_CONTENT`.

Nếu một logical slide có nhiều rich block không vừa cùng layout, mỗi rich block trở thành một physical slide; slide sau thêm hậu tố `(tiếp theo)`.

| ID | Task | Done | Date |
|---|---|---|---|
| TASK-018 | Tạo `SlideRenderModel` nội bộ, tách schema generate khỏi placeholder và tọa độ. | ✅ | 2026-08-31 |
| TASK-019 | Implement layout selection theo precedence; `layout_hint` chỉ là gợi ý và không ép layout không chứa được block. | ✅ | 2026-08-31 |
| TASK-020 | Implement capacity estimator theo số dòng ước tính, chiều dài nội dung và vùng placeholder. | ✅ | 2026-08-31 |
| TASK-021 | Text body bắt đầu 22 pt, giảm tới tối thiểu 18 pt; nếu vẫn vượt 12 dòng hoặc khoảng 650 weighted characters thì tách slide. | ✅ | 2026-08-31 |
| TASK-022 | Bullet tối đa 5 item/physical slide; tách giữa bullet, không cắt giữa câu. | ✅ | 2026-08-31 |
| TASK-023 | Paragraph tách theo đoạn rồi theo câu; bỏ truncation làm mất nội dung. | ✅ | 2026-08-31 |
| TASK-024 | Code tối đa 18 dòng/slide; ưu tiên tách ở dòng trống hoặc ranh giới hàm/lớp, sau đó theo dòng; giữ indentation. | ✅ | 2026-08-31 |
| TASK-025 | Table tối đa 8 data rows/slide và 6 cột; lặp header khi tách row; table rộng chia nhóm cột và lặp cột định danh đầu tiên. | ✅ | 2026-08-31 |
| TASK-026 | Chart tối đa 8 categories và 4 series/slide; nhiều category được chia thành chart tiếp theo với cùng legend. | ✅ | 2026-08-31 |
| TASK-027 | Process tối đa 6 bước/slide; comparison tối đa 5 item mỗi bên; phần dư tạo continuation slide. | ✅ | 2026-08-31 |
| TASK-028 | Quiz tối đa 2 câu/slide; không render `correct_answer` hoặc `explanation` trên question slide. | ✅ | 2026-08-31 |
| TASK-029 | Sinh answer-key cuối deck, tối đa 4 câu/slide; mỗi mục có số câu, đáp án và giải thích ngắn. | ✅ | 2026-08-31 |
| TASK-030 | Ghi đáp án đầy đủ vào speaker notes của question slide; notes chứa source IDs và media attribution khi có. | ✅ | 2026-08-31 |

### GOAL-004: Modular hóa `python-pptx` exporter

Giữ `src/llm/services/slide_export_service.py` làm façade để không đổi import hiện tại. Tách logic nội bộ thành render models/planner, template registry, overflow engine và renderer registry.

| ID | Task | Done | Date |
|---|---|---|---|
| TASK-031 | Giữ signature `export_pptx(lesson_title, slides)` và bổ sung typed internal result; sync/async dùng chung một đường export. | ✅ | 2026-08-31 |
| TASK-032 | Implement renderer title, section, summary và content text, kế thừa theme/format từ placeholder. | ✅ | 2026-08-31 |
| TASK-033 | Implement image renderer với crop-fit, không kéo méo ảnh, caption và media-source notes. | ✅ | 2026-08-31 |
| TASK-034 | Implement code renderer bằng textbox nền tối, monospace, giữ khoảng trắng và syntax-neutral formatting. | ✅ | 2026-08-31 |
| TASK-035 | Implement native editable PowerPoint table bằng `insert_table()` hoặc `add_table()`, gồm header style và zebra rows. | ✅ | 2026-08-31 |
| TASK-036 | Implement native editable chart bằng `CategoryChartData` và `XL_CHART_TYPE`, đồng bộ màu theme. | ✅ | 2026-08-31 |
| TASK-037 | Implement process bằng autoshapes + connectors và comparison bằng hai vùng cân đối; không dùng SmartArt. | ✅ | 2026-08-31 |
| TASK-038 | Giữ media cache, redirect validation, kích thước tải tối đa và SSRF protection hiện tại. | ✅ | 2026-08-31 |
| TASK-039 | Thay truncation bằng overflow engine; chỉ rút gọn caption ở 140 ký tự và ghi warning nếu rút gọn. | ✅ | 2026-08-31 |
| TASK-040 | Post-render validation: slide có title, shape không vượt canvas, content placeholder không rỗng bất thường và file reopen được. | ✅ | 2026-08-31 |
| TASK-041 | Save vào file tạm, validate thành công rồi mới publish sang export path; file lỗi không được trả download URL. | ✅ | 2026-08-31 |
| TASK-042 | Pin `python-pptx~=1.0.2`; giữ Pillow và httpx là dependency trực tiếp. | ✅ | 2026-08-31 |

### GOAL-005: Chạy PPTX maker độc lập bằng mock payload

| ID | Task | Done | Date |
|---|---|---|---|
| TASK-043 | Thêm CLI đọc JSON mock và gọi trực tiếp `SlideExportService`, mặc định không dùng network hoặc application runtime. | ✅ | 2026-08-31 |
| TASK-044 | Thêm fixture rich deck, local media map và requirements tối giản không gồm LLM/retrieval dependencies. | ✅ | 2026-08-31 |
| TASK-045 | Thêm subprocess tests, hướng dẫn README và xác minh deck bằng LibreOffice từ môi trường dependency tối giản. | ✅ | 2026-08-31 |

## Test Plan

### Schema và normalization

- [x] `layout_hint` nhận đủ giá trị hợp lệ và từ chối giá trị lạ.
- [x] Mỗi block parse đúng qua discriminated union.
- [x] Table từ chối row sai số cột.
- [x] Chart từ chối series không khớp categories.
- [x] Chart từ chối value không phải số.
- [x] Process thiếu bước fallback thành bullets.
- [x] Comparison thiếu một phía fallback thành bullets.
- [x] Payload legacy chỉ có `bullets` tạo được bullet block.
- [x] Payload typed blocks sinh lại `bullets` cho UI cũ.
- [x] `source_chunk_ids` được giữ qua content → merger → graph → session.
- [x] Content-agent fallback vẫn tạo slide hợp lệ khi JSON LLM sai.

### Template contract

- [x] Load được bundled template và manifest.
- [x] Template đúng 16:9.
- [x] Tìm layout bằng tên, không phụ thuộc thứ tự.
- [x] Tìm placeholder bằng semantic role và `idx`.
- [x] Thiếu layout bắt buộc tạo lỗi cụ thể.
- [x] Placeholder sai type tạo lỗi cụ thể.
- [x] Manifest version không tương thích bị từ chối.
- [x] Template PPTX corrupt không tạo download URL.
- [x] Template legacy vẫn export được qua compatibility fallback.

### Render planner và overflow

- [x] Mỗi block type chọn đúng layout.
- [x] Rich block precedence thắng `layout_hint` không phù hợp.
- [x] Text + media chọn `EDU_CONTENT_MEDIA`.
- [x] Media không URL vẫn tạo placeholder hình.
- [x] Nhiều rich blocks sinh đúng số continuation slides.
- [x] Bullet giữ nguyên thứ tự sau khi chia slide.
- [x] Không bullet hoặc câu nào bị cắt giữa chừng.
- [x] Paragraph tách đúng theo đoạn/câu.
- [x] Code giữ indentation và đủ toàn bộ dòng.
- [x] Table lặp header trên slide tiếp theo.
- [x] Table rộng lặp cột định danh.
- [x] Chart chia categories nhưng giữ series/legend.
- [x] Process và comparison không vượt giới hạn layout.
- [x] Title continuation có hậu tố nhất quán.
- [x] `source_slide_count` và `exported_slide_count` phản ánh đúng trước/sau expansion.

### Renderer PPTX

- [x] Title, subtitle và section text nằm đúng placeholder.
- [x] Bullet paragraph có đúng cấp và font-size tối thiểu 18 pt.
- [x] Ảnh ngang, dọc và vuông giữ tỉ lệ.
- [x] Ảnh không tải được sinh placeholder có caption.
- [x] Code block dùng monospace và giữ whitespace.
- [x] Table đọc lại được dưới dạng native `GraphicFrame.table`.
- [x] Chart đọc lại được dưới dạng native `GraphicFrame.chart`.
- [x] Process có đúng số node và connector.
- [x] Comparison có đủ hai tiêu đề và danh sách.
- [x] Notes thường được giữ nguyên.
- [x] Notes có source IDs và media attribution.
- [x] Exported PPTX reopen được bằng `python-pptx`.
- [x] Không shape nào có bounding box vượt kích thước slide.
- [x] Core metadata có title và template version.
- [x] Filename/download URL giữ format API cũ.

### Quiz và answer key

- [x] Question slide không chứa `Đáp án:` hoặc explanation.
- [x] Correct answer và explanation có trong speaker notes.
- [x] Tối đa hai câu trên một question slide.
- [x] Answer-key nằm sau nội dung chính.
- [x] Answer-key tối đa bốn câu trên một slide.
- [x] Số câu ở answer-key khớp question slide.
- [x] Quiz không có explanation vẫn export được.
- [x] Không có quiz thì không sinh answer-key.
- [x] Session interaction vẫn giữ `questions` trong logical slides.

### Media và bảo mật

- [x] URL HTTP/HTTPS công khai được xử lý.
- [x] Loopback, private, link-local, reserved và redirect về mạng nội bộ bị chặn.
- [x] File vượt `MEDIA_DOWNLOAD_MAX_BYTES` bị từ chối.
- [x] Content-Type không phải image bị từ chối.
- [x] Timeout media không làm hỏng export.
- [x] URL trùng chỉ tải một lần nhờ cache.
- [x] Media relevance cao nhất được chọn.
- [x] Media không URL vẫn được merge và render placeholder.
- [x] Không ghi URL hoặc nội dung nhạy cảm vào lỗi frontend.

### Integration và regression

- [x] Fixture deck chứa title, content, image, code, table, chart, process, comparison, quiz, answer-key và summary.
- [x] Full path `MergedSlide → export_pptx → reopen` giữ đủ text và object type.
- [x] `SlideService` lưu metadata mới nhưng frontend cũ vẫn hiển thị nút tải.
- [x] Sync và async processing trả cùng metadata.
- [x] Export lỗi không làm mất `slide_state.slide_output`.
- [x] HITL outline edit giữ `layout_hint`.
- [x] Quality revision giữ typed blocks sau regenerate.
- [x] Existing slide routing, media, quiz, quality-degradation và service-message tests pass.
- [x] Lesson-plan path không bị ép qua PPTX renderer.
- [x] Không tăng số LLM call của pipeline.

### Visual QA

Tạo visual suite có marker riêng:

```bash
python -m pytest -m visual
```

Suite phải:

- Sinh fixture deck đầy đủ.
- Convert PPTX sang PDF bằng LibreOffice headless.
- Kiểm tra số trang bằng `pdfinfo`.
- Render từng trang thành PNG bằng `pdftoppm`.
- Tạo contact sheet để review.
- Fail nếu LibreOffice báo repair, PDF thiếu trang hoặc có trang trắng hoàn toàn.
- Skip với thông báo rõ nếu máy chưa có LibreOffice; môi trường nghiệm thu/CI phải cài LibreOffice.

Checklist thủ công trên PowerPoint:

- [ ] Mở không có hộp thoại repair.
- [ ] Theme, font, màu và spacing nhất quán.
- [ ] Tiếng Việt hiển thị đúng dấu.
- [ ] Không text tràn hoặc body font dưới 18 pt.
- [ ] Ảnh không méo và caption đọc được.
- [ ] Chart/table vẫn chỉnh sửa được.
- [ ] Question slide không lộ đáp án.
- [ ] Presenter View hiển thị đáp án trong notes.
- [ ] Answer-key cuối deck đầy đủ.
- [ ] Deck vẫn hợp lý khi toàn bộ media thất bại.

### Commands

```bash
python -m pip install -r requirements.txt
python -m pytest tests/test_slide_template_export.py
python -m pytest tests/test_slide_quiz_routing.py tests/test_slide_service_messages.py
python -m pytest tests/test_mcp_tool_integration.py tests/test_quality_graceful_degradation.py
python -m pytest
python -m pytest -m visual
```

## Acceptance criteria

- Tất cả automated tests pass.
- Fixture rich-content deck mở được trong PowerPoint và LibreOffice.
- Không mất nội dung do truncation.
- Không lộ quiz answer trên question slide.
- Không hard-code layout index trong runtime renderer.
- Mọi template role được validate trước export.
- Table và chart là object PowerPoint chỉnh sửa được.
- Media failure chỉ tạo warning/placeholder, không chặn deck.
- Payload cũ vẫn export thành công.
- API download và frontend không có breaking change.

## Assumptions

- V1 chỉ có bundled template `academic_vi`; không có upload hoặc chọn nhiều template.
- Template được author sẵn và kiểm soát bằng manifest; runtime không tạo slide master/layout mới.
- Không hỗ trợ SmartArt, shape animation, transition nâng cao, video hoặc audio trong V1.
- Diagram/process dùng native shapes và connectors.
- Không cho AI sinh tọa độ; render planner deterministic quyết định bố cục.
- Arial/Courier New là theme fonts; font substitution phải qua visual QA.
- Môi trường hiện có `pdftoppm` nhưng chưa có `soffice`; visual acceptance cần cài LibreOffice.
