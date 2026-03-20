"""
Question Scorer — Chấm điểm câu trả lời (mọi dạng).

Hỗ trợ: MCQ (match đáp án), Essay (LLM chấm), Fill (exact match).

TODO: Migrate logic từ response_handler.py cũ + mở rộng cho essay/fill.
"""

from ..base_handler import BaseHandler


class QuestionScorer(BaseHandler):
    """Chấm điểm câu trả lời dựa vào items trong session."""
    
    def handle(self, query: str, **kwargs):
        # TODO: Migrate từ response_handler.py cũ
        raise NotImplementedError("QuestionScorer chưa migrate")
