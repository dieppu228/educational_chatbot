"""
Chat Handler — Hỏi đáp kiến thức chung (thay fallback_handler cũ).

Sử dụng RAG context để trả lời câu hỏi về SGK Tin học THPT.

TODO: Migrate logic từ fallback_handler.py cũ + cải tiến.
"""

from src.llm.handlers.base_handler import BaseHandler


class ChatHandler(BaseHandler):
    """Hỏi đáp kiến thức dựa trên RAG context."""
    
    def handle(self, query: str, **kwargs):
        # TODO: Migrate từ fallback_handler.py
        raise NotImplementedError("ChatHandler chưa migrate")
