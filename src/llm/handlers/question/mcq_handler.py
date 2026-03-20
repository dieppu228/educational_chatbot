"""
MCQ Handler — Sinh câu hỏi trắc nghiệm ABCD.

Migrate từ question_handler.py cũ.

TODO: Migrate logic từ handlers/question_handler.py
"""

from ..base_handler import BaseHandler


class MCQHandler(BaseHandler):
    """Sinh câu hỏi trắc nghiệm ABCD từ context."""
    
    def handle(self, query: str, **kwargs):
        # TODO: Migrate logic từ question_handler.py cũ
        raise NotImplementedError("MCQHandler chưa migrate")
