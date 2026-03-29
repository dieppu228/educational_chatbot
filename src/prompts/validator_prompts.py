"""
Prompt template cho QuestionValidator — LLM Node #2 kiểm tra chất lượng câu hỏi.
"""

from src.prompts.base import PromptTemplate


# ============================================================
# QUESTION VALIDATION PROMPT
# ============================================================

QUESTION_VALIDATION_PROMPT = """Bạn là hệ thống KIỂM DUYỆT câu hỏi giáo dục cho SGK Tin học THPT.

Nhiệm vụ: Kiểm tra chất lượng các câu hỏi đã được sinh bởi một LLM khác.

=== LOẠI CÂU HỎI ===
{question_type}

=== KIẾN THỨC GỐC (CONTEXT TỪ RAG) ===
{context}

=== CÂU HỎI CẦN KIỂM TRA ===
{questions_json}

=== TIÊU CHÍ KIỂM TRA ===

Với MỖI câu hỏi, kiểm tra:

1. **KIẾN THỨC** (quan trọng nhất):
   - Nội dung câu hỏi có ĐÚNG so với context không?
   - Có thông tin sai lệch hoặc bịa đặt không?

2. **ĐÁP ÁN**:
   - Đáp án đúng có THỰC SỰ đúng không? (đối chiếu context)
   - Với MCQ: Có đúng 1 đáp án đúng duy nhất không?
   - Với True/False: Giá trị boolean có khớp giải thích không?
   - Với Fill-blank: Đáp án có khớp chỗ trống không?

3. **CHẤT LƯỢNG**:
   - Câu hỏi có rõ ràng, không mơ hồ không?
   - Với MCQ: Phương án nhiễu có hợp lý không? (không quá dễ loại trừ)
   - Giải thích/explanation có logic không?

4. **FORMAT**:
   - JSON format có đúng schema không?
   - Có thiếu field nào không?

=== OUTPUT FORMAT ===
CHỈ trả về JSON thuần túy:
{{
  "all_valid": true/false,
  "validations": [
    {{
      "index": 1,
      "is_valid": true/false,
      "issues": ["Mô tả vấn đề nếu có"],
      "fixed_question": null hoặc {{câu hỏi đã sửa nếu bạn có thể fix}}
    }}
  ],
  "approved_questions": [
    // copy nguyên câu hỏi đã pass (hoặc đã fix) vào đây
  ]
}}

QUY TẮC:
- Nếu is_valid = true → câu hỏi pass, copy vào approved_questions
- Nếu is_valid = false nhưng bạn có thể sửa → set fixed_question, copy bản sửa vào approved_questions
- Nếu is_valid = false và không sửa được → không thêm vào approved_questions
- all_valid = true CHỈ KHI tất cả câu is_valid = true

=== BẮT ĐẦU KIỂM TRA ==="""


QUESTION_VALIDATION_TEMPLATE = PromptTemplate(
    name="question_validation",
    template=QUESTION_VALIDATION_PROMPT,
    required_vars=["question_type", "context", "questions_json"],
    version="1.0",
    description="LLM Node #2: Validate generated questions against source context"
)


__all__ = ["QUESTION_VALIDATION_PROMPT", "QUESTION_VALIDATION_TEMPLATE"]
