"""
Feedback generation prompts for educational responses.
"""

from src.prompts.base import PromptTemplate

# ============================================================
# FEEDBACK GENERATION PROMPT
# ============================================================

FEEDBACK_GENERATION_PROMPT = """
Bạn là giáo viên tạo phản hồi giáo dục tích cực.

=== THÔNG TIN CÂU HỎI ===
Câu hỏi #{question_index}:
{question_text}

Phương án đúng: {correct_answer}
Phương án người dùng chọn: {user_answer}
Kết quả: {result_status}

Giải thích đáp án:
{explanation}

=== NHIỆM VỤ ===
Tạo phản hồi giáo dục tích cực:
1. Nếu ĐÚNG: khích lệ, giải thích tại sao đúng
2. Nếu SAI: giải thích lỗi sai, hướng dẫn lại kiến thức

=== OUTPUT ===
Phản hồi ngắn gọn, rõ ràng, có tính xây dựng
"""

# ============================================================
# TEMPLATE OBJECT
# ============================================================

FEEDBACK_TEMPLATE = PromptTemplate(
    name="feedback_generation",
    template=FEEDBACK_GENERATION_PROMPT,
    required_vars=[
        "question_index",
        "question_text", 
        "correct_answer",
        "user_answer",
        "result_status",
        "explanation"
    ],
    version="1.0",
    description="Generate educational feedback for answered questions"
)


__all__ = ["FEEDBACK_GENERATION_PROMPT", "FEEDBACK_TEMPLATE"]
