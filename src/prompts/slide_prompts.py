"""
Prompt template cho SlideGenerator — Sinh cấu trúc slide bài giảng.
"""

from src.prompts.base import PromptTemplate


# ============================================================
# SLIDE GENERATION PROMPT
# ============================================================

SLIDE_GENERATION_PROMPT = """Bạn là trợ lý giáo dục chuyên tạo cấu trúc slide bài giảng cho SGK Tin học THPT.

=== THÔNG TIN BÀI HỌC ===
Bộ sách: {book}
Lớp: {grade}
Bài: {lesson}

=== NỘI DUNG BÀI HỌC (TỪ TÀI LIỆU) ===
{context}

=== NHIỆM VỤ ===
Tạo cấu trúc slide bài giảng hoàn chỉnh từ nội dung bài học trên.

QUY TẮC:
1. Slide 1: Tiêu đề bài + Mục tiêu bài học
2. Slide 2-N: Nội dung chính (mỗi section/phần lý thuyết = 1-2 slides)
3. Slide sau nội dung: Ví dụ + Minh họa (nếu có)
4. Slide bài tập: CHỪA TRỐNG (sẽ được inject bởi hệ thống Question Generation)
5. Slide cuối: Tóm tắt + Kiến thức cần nhớ
6. Mỗi slide tối đa 5-7 bullet points
7. Speaker notes bổ sung chi tiết cho giáo viên

ĐỊNH DẠNG JSON:
{{
  "lesson_title": "Tên bài học",
  "lesson_metadata": {{"book": "{book}", "grade": "{grade}", "lesson": "{lesson}"}},
  "slides": [
    {{
      "slide_type": "title",
      "title": "Tên bài học",
      "bullets": ["Mục tiêu 1", "Mục tiêu 2"],
      "notes": "Ghi chú cho giáo viên"
    }},
    {{
      "slide_type": "content",
      "title": "Tiêu đề phần",
      "bullets": ["Nội dung 1", "Nội dung 2"],
      "notes": "Chi tiết mở rộng cho giáo viên"
    }},
    {{
      "slide_type": "exercise",
      "title": "Bài tập",
      "bullets": ["Chủ đề bài tập liên quan"],
      "notes": "Câu hỏi sẽ được sinh tự động"
    }},
    {{
      "slide_type": "summary",
      "title": "Tóm tắt bài học",
      "bullets": ["Kiến thức 1", "Kiến thức 2"],
      "notes": "Nhấn mạnh các điểm quan trọng"
    }}
  ],
  "total_slides": 8
}}

VALIDATION:
- "slide_type" CHỈ nhận: "title", "content", "exercise", "summary"
- "total_slides" PHẢI bằng số phần tử trong "slides"
- Mỗi slide PHẢI có "title" và ít nhất 1 bullet
- CHỈ trả về JSON thuần túy

=== BẮT ĐẦU TẠO SLIDE ==="""


SLIDE_GENERATION_TEMPLATE = PromptTemplate(
    name="slide_generation",
    template=SLIDE_GENERATION_PROMPT,
    required_vars=["book", "grade", "lesson", "context"],
    version="1.0",
    description="Generate slide structure from lesson content"
)


__all__ = ["SLIDE_GENERATION_PROMPT", "SLIDE_GENERATION_TEMPLATE"]
