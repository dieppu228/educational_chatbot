"""
Question generation prompts for all question types:
MCQ, Essay, Fill-in-the-Blank, True/False.
"""

from src.prompts.base import PromptTemplate

# ============================================================
# MCQ GENERATION PROMPT
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

=== BẮT ĐẦU TẠO {num_questions} CÂU HỎI ===
"""


# ============================================================
# ESSAY GENERATION PROMPT
# ============================================================

ESSAY_GENERATION_PROMPT = """Bạn là trợ lý giáo dục chuyên tạo câu hỏi tự luận cho SGK Tin học THPT.

=== YÊU CẦU CỦA NGƯỜI DÙNG ===
{query}

=== KIẾN THỨC TỪ TÀI LIỆU (RAG) ===
{context}

=== NHIỆM VỤ ===
Tạo **chính xác {num_questions} câu hỏi tự luận** với đáp án mẫu và rubric chấm điểm.

QUY TẮC:
1. Câu hỏi PHẢI dựa trên kiến thức được cung cấp
2. Đáp án mẫu phải đầy đủ, chính xác
3. Rubric phải rõ ràng, có tiêu chí cụ thể
4. Độ khó đa dạng: easy, medium, hard
5. CHỈ trả về JSON thuần túy, KHÔNG thêm markdown

ĐỊNH DẠNG JSON:
{{
  "essays": [
    {{
      "index": 1,
      "question": "Trình bày khái niệm...",
      "sample_answer": "Đáp án mẫu chi tiết...",
      "rubric": "- 2đ: Nêu đúng khái niệm\\n- 1đ: Cho ví dụ...",
      "difficulty": "medium"
    }}
  ]
}}

VALIDATION:
- "difficulty" CHỈ nhận: "easy", "medium", hoặc "hard"
- "sample_answer" phải đủ chi tiết để làm chuẩn chấm
- "rubric" phải có tiêu chí rõ ràng

=== BẮT ĐẦU TẠO {num_questions} CÂU HỎI TỰ LUẬN ==="""


# ============================================================
# FILL-IN-THE-BLANK GENERATION PROMPT
# ============================================================

FILL_BLANK_GENERATION_PROMPT = """Bạn là trợ lý giáo dục chuyên tạo câu hỏi đục lỗ / điền khuyết cho SGK Tin học THPT.

=== YÊU CẦU CỦA NGƯỜI DÙNG ===
{query}

=== KIẾN THỨC TỪ TÀI LIỆU (RAG) ===
{context}

=== NHIỆM VỤ ===
Tạo **chính xác {num_questions} câu đục lỗ** với đáp án đúng.

QUY TẮC:
1. Mỗi câu phải dựa trên kiến thức được cung cấp
2. Dùng ___ (3 gạch dưới) để đánh dấu chỗ trống
3. Mỗi câu có thể có 1 hoặc nhiều chỗ trống
4. Đáp án phải theo đúng thứ tự chỗ trống
5. CHỈ trả về JSON thuần túy

ĐỊNH DẠNG JSON:
{{
  "fill_blanks": [
    {{
      "index": 1,
      "text_with_blanks": "Mạng ___ là mạng máy tính trong phạm vi ___ như phòng học, tòa nhà.",
      "answers": ["LAN", "nhỏ"],
      "explanation": "LAN (Local Area Network) là mạng cục bộ, hoạt động trong phạm vi nhỏ."
    }}
  ]
}}

VALIDATION:
- Số phần tử trong "answers" PHẢI bằng số ___ trong "text_with_blanks"
- Chỗ trống phải ở vị trí từ khóa quan trọng
- "explanation" giải thích tại sao đáp án đúng

=== BẮT ĐẦU TẠO {num_questions} CÂU ĐỤC LỖ ==="""


# ============================================================
# TRUE/FALSE GENERATION PROMPT
# ============================================================

TRUE_FALSE_GENERATION_PROMPT = """Bạn là trợ lý giáo dục chuyên tạo câu hỏi Đúng/Sai cho SGK Tin học THPT.

=== YÊU CẦU CỦA NGƯỜI DÙNG ===
{query}

=== KIẾN THỨC TỪ TÀI LIỆU (RAG) ===
{context}

=== NHIỆM VỤ ===
Tạo **chính xác {num_questions} câu hỏi Đúng/Sai** với giải thích.

QUY TẮC:
1. Mỗi câu là 1 phát biểu, người dùng phải xác định Đúng hay Sai
2. Phát biểu PHẢI dựa trên kiến thức được cung cấp
3. Cân bằng số câu Đúng và Sai (xấp xỉ 50/50)
4. Câu Sai phải sai ở điểm tinh tế, không quá dễ nhận ra
5. CHỈ trả về JSON thuần túy

ĐỊNH DẠNG JSON:
{{
  "true_false": [
    {{
      "index": 1,
      "statement": "Mạng LAN có phạm vi hoạt động trong một thành phố.",
      "correct_answer": false,
      "explanation": "Sai. Mạng LAN hoạt động trong phạm vi nhỏ (phòng, tòa nhà). Mạng MAN mới có phạm vi thành phố."
    }}
  ]
}}

VALIDATION:
- "correct_answer" CHỈ nhận: true hoặc false (boolean)
- "statement" phải rõ ràng, không mơ hồ
- "explanation" PHẢI giải thích cụ thể tại sao Đúng/Sai

=== BẮT ĐẦU TẠO {num_questions} CÂU ĐÚNG/SAI ==="""


# ============================================================
# TEMPLATE OBJECTS
# ============================================================

QUESTION_GENERATION_TEMPLATE = PromptTemplate(
    name="question_generation",
    template=QUESTION_GENERATION_PROMPT,
    required_vars=["query", "context", "num_questions"],
    version="1.1",
    description="Generate multiple choice questions from retrieved context"
)

ESSAY_GENERATION_TEMPLATE = PromptTemplate(
    name="essay_generation",
    template=ESSAY_GENERATION_PROMPT,
    required_vars=["query", "context", "num_questions"],
    version="1.0",
    description="Generate essay questions with sample answers and rubrics"
)

FILL_BLANK_GENERATION_TEMPLATE = PromptTemplate(
    name="fill_blank_generation",
    template=FILL_BLANK_GENERATION_PROMPT,
    required_vars=["query", "context", "num_questions"],
    version="1.0",
    description="Generate fill-in-the-blank questions"
)

TRUE_FALSE_GENERATION_TEMPLATE = PromptTemplate(
    name="true_false_generation",
    template=TRUE_FALSE_GENERATION_PROMPT,
    required_vars=["query", "context", "num_questions"],
    version="1.0",
    description="Generate true/false questions"
)


# ============================================================
# ESSAY SCORING PROMPT
# ============================================================

ESSAY_SCORING_PROMPT = """Bạn là giáo viên chấm điểm câu hỏi tự luận Tin học THPT.

=== CÂU HỎI & HƯỚNG DẪN CHẤM ===
Câu hỏi: {question}
Đáp án mẫu: {sample_answer}
Rubric: {rubric}

=== CÂU TRẢ LỜI CỦA HỌC SINH ===
{user_answer}

=== NHIỆM VỤ ===
Chấm điểm câu trả lời của học sinh dựa trên rubric và đáp án mẫu.

YÊU CẦU:
1. Đánh giá tính chính xác về kiến thức
2. So khớp với các tiêu chí trong rubric
3. Trả về kết quả dưới định dạng JSON

ĐỊNH DẠNG JSON:
{{
  "is_correct": true/false, // true nếu đạt trên 50% yêu cầu
  "score": 0.0-10.0,
  "explanation": "Nhận xét chi tiết về ưu điểm và những điểm cần cải thiện...",
  "confidence": 0.9
}}

VALIDATION:
- "is_correct" là boolean
- "score" là số thực từ 0 đến 10
- "explanation" phải mang tính giáo dục và xây dựng
- CHỈ trả về JSON thuần túy

=== BẮT ĐẦU CHẤM ĐIỂM ==="""


ESSAY_SCORING_TEMPLATE = PromptTemplate(
    name="essay_scoring",
    template=ESSAY_SCORING_PROMPT,
    required_vars=["question", "sample_answer", "rubric", "user_answer"],
    version="1.0",
    description="Score essay answers using LLM based on rubrics"
)


__all__ = [
    "QUESTION_GENERATION_PROMPT",
    "ESSAY_GENERATION_PROMPT",
    "FILL_BLANK_GENERATION_PROMPT",
    "TRUE_FALSE_GENERATION_PROMPT",
    "QUESTION_GENERATION_TEMPLATE",
    "ESSAY_GENERATION_TEMPLATE",
    "FILL_BLANK_GENERATION_TEMPLATE",
    "TRUE_FALSE_GENERATION_TEMPLATE",
    "ESSAY_SCORING_PROMPT",
    "ESSAY_SCORING_TEMPLATE",
]
