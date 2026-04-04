"""
Chat Handler — Hỏi đáp kiến thức chung dựa trên RAG context.

Sử dụng RAG context để trả lời câu hỏi về SGK Tin học THPT.
Nếu không có context, trả lời dựa trên kiến thức chung và hướng dẫn user.
"""

from src.llm.handlers.base_handler import BaseHandler
from src.config.config import settings


CHAT_PROMPT = """Bạn là trợ lý giáo dục chuyên về SGK Tin học THPT Việt Nam.

=== KIẾN THỨC TỪ TÀI LIỆU ===
{context}

=== CÂU HỎI CỦA HỌC SINH ===
{query}

=== HƯỚNG DẪN TRẢ LỜI ===
1. Trả lời ngắn gọn, chính xác, dễ hiểu
2. Ưu tiên sử dụng kiến thức từ tài liệu được cung cấp
3. Nếu tài liệu không đủ, dùng kiến thức chung nhưng phải ghi chú
4. Khi phù hợp, gợi ý cho học sinh thử tạo câu hỏi ôn tập
5. Sử dụng emoji phù hợp để tạo trải nghiệm thân thiện
6. Nếu câu hỏi ngoài phạm vi Tin học THPT, nhẹ nhàng hướng dẫn học sinh quay lại chủ đề

=== TRẢ LỜI ==="""


class ChatHandler(BaseHandler):
    """Hỏi đáp kiến thức dựa trên RAG context."""
    
    def handle(self, query: str, context: str = "", **kwargs) -> str:
        """
        Trả lời câu hỏi chung dựa trên context từ RAG.
        
        Args:
            query: Câu hỏi của user
            context: Nội dung tài liệu từ RAG (có thể rỗng)
            
        Returns:
            str: Câu trả lời
        """
        if not context:
            context = "[Không tìm thấy tài liệu liên quan trong kho SGK]"
        
        prompt = CHAT_PROMPT.format(query=query, context=context)
        
        try:
            response = self._call_api(
                prompt,
                temperature=0.3,
                response_mime="text/plain"
            )
            return response
        except Exception as e:
            return (
                "Xin chào! Mình là trợ lý học tập Tin học THPT. "
                "Bạn có thể hỏi mình về kiến thức trong SGK, "
                "hoặc yêu cầu tạo câu hỏi ôn tập nhé! 📚"
            )


__all__ = ["ChatHandler"]
