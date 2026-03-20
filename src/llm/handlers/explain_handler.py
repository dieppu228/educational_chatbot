"""
Explain Handler — Giải thích chuyên sâu một khái niệm.

Khác ChatHandler: tập trung vào 1 chủ đề, giải thích từng bước,
kèm ví dụ minh họa từ SGK.

TODO: Implement.
"""

from .base_handler import BaseHandler


class ExplainHandler(BaseHandler):
    """Giải thích chuyên sâu 1 khái niệm."""
    
    def handle(self, query: str, **kwargs):
        # TODO: Implement
        raise NotImplementedError("ExplainHandler chưa implement")
