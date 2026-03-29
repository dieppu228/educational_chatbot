"""
Response formatting prompts for displaying MCQ questions.
"""

from src.prompts.base import PromptTemplate

# ============================================================
# RESPONSE FORMATTING PROMPT
# ============================================================

RESPONSE_FORMATTING_PROMPT = """
Bạn là công cụ định dạng câu hỏi trắc nghiệm.

=== INPUT FORMAT ===
JSON string chứa danh sách câu hỏi:
{{
  "mcq": [
    {{
      "index": 1,
      "question": "Nội dung câu hỏi",
      "options": {{
        "A": "Phương án A",
        "B": "Phương án B",
        "C": "Phương án C",
        "D": "Phương án D"
      }},
      "correct_answer": "C",
      "explanation": "Giải thích chi tiết"
    }},
    {{
      "index": 2,
      "question": "Câu hỏi thứ 2",
      ...
    }}
  ]
}}

INPUT DATA:
{options}

=== NHIỆM VỤ ===
Định dạng lại các câu hỏi thành TEXT READABLE format (KHÔNG JSON).

=== OUTPUT FORMAT ===

Câu hỏi 1:
<Nội dung câu hỏi đầy đủ>

A. <Phương án A>
B. <Phương án B>
C. <Phương án C>
D. <Phương án D>

________________________________________

Câu hỏi 2:
<Nội dung câu hỏi>

A. <Phương án A>
B. <Phương án B>
C. <Phương án C>
D. <Phương án D>

________________________________________

=== YÊU CẦU ===
1. KHÔNG bao gồm correct_answer hoặc explanation trong output
2. KHÔNG in đáp án đúng hoặc giải thích
3. KHÔNG trả về JSON - chỉ text thuần
4. Mỗi câu hỏi cách nhau bằng dòng gạch ngang
5. Format: "Câu hỏi N:" rồi nội dung, rồi 4 options A, B, C, D
6. Giữ nguyên nội dung câu hỏi và options từ input
7. KHÔNG thêm text trước hoặc sau danh sách câu hỏi
8. Đảm bảo đầy đủ tất cả câu hỏi từ input
"""

# ============================================================
# TEMPLATE OBJECT
# ============================================================

FORMAT_TEMPLATE = PromptTemplate(
    name="response_formatting",
    template=RESPONSE_FORMATTING_PROMPT,
    required_vars=["options"],
    version="1.0",
    description="Format MCQ JSON to human-readable text"
)


__all__ = ["RESPONSE_FORMATTING_PROMPT", "FORMAT_TEMPLATE"]
