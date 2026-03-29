# 📝 Review Notes — Phase 2: Question Generation Pipeline

> File ghi lại các thắc mắc, ghi chú và điểm cần kiểm tra trong quá trình review.

---

## Thắc mắc / Câu hỏi

### Q1: Pydantic, BaseModel, Field là gì? Dùng để làm gì?
- **Pydantic**: Thư viện validate & parse dữ liệu tự động cho Python.
- **BaseModel**: Class nền. Kế thừa nó → tự động có type checking, auto-parsing, serialization (→ JSON/dict).
- **Field**: Thêm ràng buộc chi tiết (`ge=0.0`, `le=1.0`, ...).
- **field_validator**: Viết logic validate tuỳ chỉnh phức tạp.
- **Lý do dùng**: LLM trả JSON không đáng tin 100% → Pydantic giúp parse an toàn, bắt lỗi sớm.

### Q2: Chi tiết các trường của từng schema trong `llm_outputs.py`

**Phase 1:**
- `MCQOption`: `A`, `B`, `C`, `D` (str)
- `MCQQuestion`: `index` (int≥1), `question` (str), `options` (MCQOption), `correct_answer` (A/B/C/D), `explanation` (str)
- `MCQGenerationOutput`: `mcq` (List[MCQQuestion])
- `ScoringOutput`: `status` (found/not_found/ambiguous), `question_index` (int?), `question_text` (str?), `user_answer` (Any?), `correct_answer` (Any?), `is_correct` (bool?), `score` (float 0-10?), `explanation` (str?), `confidence` (float 0-1?)
- `FallbackOutput`: `response` (str), `is_redirect` (bool)
- `FeedbackOutput`: `feedback` (str), `encouragement` (str?), `next_steps` (str?)
- `ExtractMetadataOutput`: `lesson` (str?), `grade` (10/11/12?), `topic` (str?)

**Phase 2 — Question Types:**
- `EssayQuestion`: `index` (int≥1), `question` (str), `sample_answer` (str), `rubric` (str), `difficulty` (easy/medium/hard)
- `EssayGenerationOutput`: `essays` (List[EssayQuestion])
- `FillBlankQuestion`: `index` (int≥1), `text_with_blanks` (str), `answers` (List[str]), `explanation` (str)
- `FillBlankGenerationOutput`: `fill_blanks` (List[FillBlankQuestion])
- `TrueFalseQuestion`: `index` (int≥1), `statement` (str), `correct_answer` (bool), `explanation` (str)
- `TrueFalseGenerationOutput`: `true_false` (List[TrueFalseQuestion])

**Phase 2 — Validation:**
- `QuestionValidation`: `index` (int), `is_valid` (bool), `issues` (List[str]), `fixed_question` (dict?)
- `ValidationResult`: `all_valid` (bool), `validations` (List[QuestionValidation]), `approved_questions` (List[dict])

**Phase 2 — Slide:**
- `SlideItem`: `slide_type` (title/content/exercise/image/summary), `title` (str), `bullets` (List[str]), `notes` (str?), `questions` (List[dict]?), `related_lessons` (List[str]?)
- `SlideGenerationOutput`: `lesson_title` (str), `lesson_metadata` (dict), `slides` (List[SlideItem]), `total_slides` (int)

> Ký hiệu: `?` = Optional (có thể null), `≥1` = giá trị tối thiểu

### Q3: `__init__.py` của package `prompts` để làm gì?
- **Đánh dấu folder là Python package** (không có → import lỗi).
- **Re-export tập trung**: gom tất cả prompt từ các file con → import gọn `from src.prompts import X`.
- **`__all__`**: khai báo rõ những gì được phép export ra ngoài.

---

## Ghi chú khi review

- 

---

## Điểm cần sửa / cải thiện

- 

