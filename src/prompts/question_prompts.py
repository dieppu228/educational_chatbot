"""
Question generation prompts for MCQ creation.
"""

from .base import PromptTemplate

# ============================================================
# QUESTION GENERATION PROMPT
# ============================================================

QUESTION_GENERATION_PROMPT = """
Bạn là trợ lý giáo dục chuyên tạo câu hỏi trắc nghiệm chất lượng cao.

=== YÊU CẦU CỦA NGƯỜI DÙNG ===
{query}

=== KIẾN THỨC TỪ TÀI LIỆU (RAG) ===
{context}

=== NHIỆM VỤ ===
Dựa trên yêu cầu của người dùng và kiến thức được cung cấp, hãy tạo **chính xác {num_questions} câu hỏi** trắc nghiệm theo các quy tắc sau:

1. CHẤT LƯỢNG CÂU HỎI:
- Câu hỏi phải dựa trên kiến thức được cung cấp ở trên
- Mỗi câu hỏi có đúng 1 đáp án đúng duy nhất
- Các phương án nhiễu (sai) phải hợp lý, không quá dễ loại trừ
- Câu hỏi phải rõ ràng, không mơ hồ
- Độ khó phù hợp với nội dung kiến thức

2. CẤU TRÚC OUTPUT:
- CHỈ trả về JSON thuần túy
- KHÔNG thêm markdown, KHÔNG thêm ```json
- KHÔNG thêm lời giải thích bên ngoài JSON
- KHÔNG thêm text mở đầu hoặc kết thúc

3. ĐỊNH DẠNG JSON BẮT BUỘC:
{{
"mcq": [
    {{
    "index": 1,
    "question": "Nội dung câu hỏi đầy đủ, rõ ràng?",
    "options": {{
        "A": "Phương án A",
        "B": "Phương án B",
        "C": "Phương án C",
        "D": "Phương án D"
    }},
    "correct_answer": "A",
    "explanation": "Giải thích chi tiết tại sao đáp án này đúng, dẫn chứng từ kiến thức đã cung cấp"
    }},
    {{
    "index": 2,
    "question": "Câu hỏi thứ hai...",
    "options": {{
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
    }},
    "correct_answer": "B",
    "explanation": "..."
    }}
]
}}

4. QUY TẮC VALIDATION:
- "index" BẮT ĐẦU TỪ 1 và tăng dần (1, 2, 3, ..., {num_questions})
- PHẢI CÓ ĐÚNG {num_questions} CÂU HỎI trong mảng
- "correct_answer" CHỈ nhận: "A", "B", "C", hoặc "D"
- "options" PHẢI có đúng 4 key: A, B, C, D
- "explanation" PHẢI rõ ràng, tham chiếu đến kiến thức đã cho
- Mỗi phương án phải khác biệt rõ ràng

5. XỬ LÝ TRƯỜNG HỢP ĐẶC BIỆT:
- Nếu kiến thức không đủ để tạo {num_questions} câu chất lượng → giảm số lượng xuống
- Nếu yêu cầu không rõ ràng → tạo câu hỏi tổng quát về nội dung chính
- Nếu tạo {num_questions} câu hỏi → tạo đa dạng về góc độ kiến thức

=== BẮT ĐẦU TẠO {num_questions} CÂU HỎI ===
"""

# ============================================================
# TEMPLATE OBJECT
# ============================================================

QUESTION_GENERATION_TEMPLATE = PromptTemplate(
    name="question_generation",
    template=QUESTION_GENERATION_PROMPT,
    required_vars=["query", "context", "num_questions"],
    version="1.1",
    description="Generate multiple choice questions from retrieved context"
)


__all__ = ["QUESTION_GENERATION_PROMPT", "QUESTION_GENERATION_TEMPLATE"]
