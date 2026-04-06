"""
Chat Handler — Hỏi đáp kiến thức chung dựa trên RAG context.
"""

from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import CHAT_PROMPT


class ChatHandler(BaseHandler):
    """Hỏi đáp kiến thức dựa trên RAG context."""
    
    def handle(self, query: str, context: str = "", **kwargs) -> str:
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
