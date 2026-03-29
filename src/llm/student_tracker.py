from typing import Optional, Dict, Any
from src.llm.memory import SessionState, QuizStats

class StudentTracker:
    """
    Quản lý in-memory tracking trong session.
    Không lưu file/DB, dữ liệu tồn tại trong suốt conversation.
    """
    
    @staticmethod
    def update_stats(
        session: SessionState, 
        topic: str, 
        question_type: str, 
        is_correct: bool
    ) -> QuizStats:
        """
        Ghi nhận kết quả trả lời của học sinh vào session state.
        
        Args:
            session: SessionState hiện tại
            topic: Chủ đề của câu hỏi
            question_type: Loại câu hỏi (mcq, essay, ...)
            is_correct: Trả lời đúng hay sai
            
        Returns:
            QuizStats: Thống kê đã cập nhật
        """
        if session.quiz_stats is None:
            session.quiz_stats = QuizStats()
            
        session.quiz_stats.record_answer(
            topic=topic or "Chung",
            question_type=question_type,
            is_correct=is_correct
        )
        
        return session.quiz_stats

    @staticmethod
    def get_summary(session: SessionState) -> str:
        """Lấy chuỗi tóm tắt tiến độ học tập trong session."""
        if not session.quiz_stats:
            return "Chưa có dữ liệu học tập trong phiên này."
        return session.quiz_stats.get_summary()

    @staticmethod
    def get_mastery_level(session: SessionState, topic: str) -> float:
        """Lấy mức độ thành thạo của một chủ đề (0.0 - 1.0)."""
        if not session.quiz_stats or topic not in session.quiz_stats.by_topic:
            return 0.0
        return session.quiz_stats.by_topic[topic].accuracy
