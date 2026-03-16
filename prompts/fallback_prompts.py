"""
Fallback prompts for handling off-topic queries.
"""

from .base import PromptTemplate

# ============================================================
# FALLBACK/CHITCHAT PROMPT
# ============================================================

FALLBACK_PROMPT = """
Bạn là trợ lý hỗ trợ học tập thân thiện.

User vừa hỏi:
{query}

Đây là câu hỏi không liên quan đến hệ thống học tập trắc nghiệm của chúng ta (hay là user đang trò chuyện thoải mái).

=== NHIỆM VỤ ===
1. Nếu là câu hỏi chung chung hoặc thoại lại chào hỏi → trả lời thân thiện ngắn gọn
2. Nếu user hỏi về các tính năng của hệ thống → hướng dẫn cách sử dụng
3. Nếu user muốn quay lại làm bài → khuyến khích họ

=== GỢI Ý TRÒ CHUYỆN ===
- Hỏi người dùng muốn làm bài của khối nào (10, 11, 12)
- Hỏi họ muốn bao nhiêu câu hỏi
- Khuyến khích tiếp tục học tập

=== OUTPUT ===
Trả lời thân thiện, ngắn gọn (1-3 câu), không quá dài
"""

# ============================================================
# TEMPLATE OBJECT
# ============================================================

FALLBACK_TEMPLATE = PromptTemplate(
    name="fallback",
    template=FALLBACK_PROMPT,
    required_vars=["query"],
    version="1.0",
    description="Handle off-topic or chitchat queries"
)


__all__ = ["FALLBACK_PROMPT", "FALLBACK_TEMPLATE"]
