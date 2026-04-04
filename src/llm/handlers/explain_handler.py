"""
Explain Handler — Giải thích chuyên sâu một khái niệm.

Khác ChatHandler: tập trung vào 1 chủ đề, giải thích từng bước,
kèm ví dụ minh họa từ SGK.
"""

from src.llm.handlers.base_handler import BaseHandler
from src.config.config import settings


EXPLAIN_PROMPT = """Bạn là giáo viên Tin học THPT giải thích chuyên sâu cho học sinh.

=== KIẾN THỨC TỪ TÀI LIỆU ===
{context}

=== YÊU CẦU CỦA HỌC SINH ===
{query}

=== HƯỚNG DẪN GIẢI THÍCH ===
Hãy giải thích theo cấu trúc sau:

1. **Khái niệm cốt lõi**: Định nghĩa ngắn gọn, dễ hiểu
2. **Giải thích chi tiết**: Phân tích từng khía cạnh quan trọng
3. **Ví dụ minh họa**: Ví dụ cụ thể, gần gũi với đời sống
4. **So sánh (nếu phù hợp)**: So sánh với khái niệm tương tự để làm rõ
5. **Tóm tắt**: 2-3 điểm cần nhớ

YÊU CẦU:
- Sử dụng ngôn ngữ đơn giản, phù hợp học sinh THPT
- Dùng emoji để tạo trải nghiệm thân thiện
- Ưu tiên kiến thức từ tài liệu, bổ sung kiến thức chung nếu cần
- Nếu khái niệm phức tạp, chia nhỏ thành từng bước

=== BẮT ĐẦU GIẢI THÍCH ==="""


class ExplainHandler(BaseHandler):
    """Giải thích chuyên sâu 1 khái niệm."""
    
    def handle(self, query: str, context: str = "", **kwargs) -> str:
        """
        Giải thích chuyên sâu một khái niệm.
        
        Args:
            query: Yêu cầu giải thích từ user
            context: Nội dung tài liệu từ RAG (có thể rỗng)
            
        Returns:
            str: Bài giải thích chi tiết
        """
        if not context:
            context = "[Không tìm thấy tài liệu liên quan — sẽ giải thích dựa trên kiến thức chung]"
        
        prompt = EXPLAIN_PROMPT.format(query=query, context=context)
        
        try:
            response = self._call_api(
                prompt,
                temperature=0.4,
                response_mime="text/plain"
            )
            return response
        except Exception as e:
            return f"⚠️ Không thể giải thích lúc này. Vui lòng thử lại sau."


__all__ = ["ExplainHandler"]
