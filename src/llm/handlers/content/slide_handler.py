"""
Slide Handler — Sinh nội dung slide bài giảng từ context chunks.

Input: query + filtered chunks (theo bài/chủ đề)
Output: List slide items (title, bullets, notes)

TODO: Implement logic sinh slide dùng Gemini API.
"""

from ..base_handler import BaseHandler


class SlideHandler(BaseHandler):
    """Sinh nội dung slide từ context."""
    
    def handle(self, query: str, **kwargs):
        # TODO: Implement
        raise NotImplementedError("SlideHandler chưa implement")
