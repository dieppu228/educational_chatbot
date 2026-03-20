"""
Lesson Plan Handler — Sinh giáo án cho giáo viên.

Input: query + filtered chunks (theo bài học)
Output: Giáo án (mục tiêu, hoạt động, đánh giá)

TODO: Implement logic sinh giáo án dùng Gemini API.
"""

from ..base_handler import BaseHandler


class LessonPlanHandler(BaseHandler):
    """Sinh giáo án từ context."""
    
    def handle(self, query: str, **kwargs):
        # TODO: Implement
        raise NotImplementedError("LessonPlanHandler chưa implement")
