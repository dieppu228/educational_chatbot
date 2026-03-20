"""
Metadata extraction prompts for filtering RAG results.
"""

from .base import PromptTemplate

# ============================================================
# EXTRACT METADATA PROMPT
# ============================================================

EXTRACT_PROMPT = """
Bạn là hệ thống trích xuất metadata cho hệ thống RAG sách giáo khoa THPT.

Nhiệm vụ:
Từ câu hỏi của người dùng, hãy trích xuất:
- lesson: tên bài học (string bất kỳ) hoặc null
- grade: khối lớp ("10", "11", "12") hoặc null
- topic: chủ đề chính hoặc null

Yêu cầu:
- Chỉ trả về JSON hợp lệ
- Không giải thích
- Không thêm text ngoài JSON

Câu hỏi:
"{query}"

Output format:
{{"lesson": "...", "grade": "...", "topic": "..."}}
"""

# ============================================================
# TEMPLATE OBJECT
# ============================================================

EXTRACT_TEMPLATE = PromptTemplate(
    name="extract_metadata",
    template=EXTRACT_PROMPT,
    required_vars=["query"],
    version="1.0",
    description="Extract metadata (lesson, grade, topic) from user query"
)


__all__ = ["EXTRACT_PROMPT", "EXTRACT_TEMPLATE"]
