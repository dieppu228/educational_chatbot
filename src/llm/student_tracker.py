from typing import Optional, Dict, Any
from src.llm.memory import SessionState, QuizStats, Session

class StudentTracker:
    """
    Quản lý in-memory tracking trong session.
    v2: Hỗ trợ cả SessionState cũ và Session mới.
    """
    
    # ── v2 Methods (dùng với Session mới) ──────────────────

    @staticmethod
    def update_stats_v2(
        session: Session,
        topic: str,
        question_type: str,
        is_correct: bool,
    ) -> None:
        """Record answer result in session metadata (lightweight tracking)."""
        # Store in metadata for simple tracking
        stats = session.metadata.setdefault("tracking", {
            "total": 0,
            "correct": 0,
            "by_topic": {},
            "by_type": {},
        })
        
        stats["total"] += 1
        if is_correct:
            stats["correct"] += 1
        
        # By topic
        topic_key = topic or "Chung"
        if topic_key not in stats["by_topic"]:
            stats["by_topic"][topic_key] = {"total": 0, "correct": 0}
        stats["by_topic"][topic_key]["total"] += 1
        if is_correct:
            stats["by_topic"][topic_key]["correct"] += 1
        
        # By type
        stats["by_type"][question_type] = stats["by_type"].get(question_type, 0) + 1

    @staticmethod
    def get_summary_v2(session: Session) -> str:
        """Get learning progress summary from v2 session."""
        # Prefer quiz_state summary if available
        if session.quiz_state:
            return session.quiz_state.get_summary()
        
        # Fallback to metadata tracking
        stats = session.metadata.get("tracking")
        if not stats or stats["total"] == 0:
            return "Chua co du lieu hoc tap."
        
        accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        return (
            f"Tong: {stats['correct']}/{stats['total']} dung ({accuracy:.0%})"
        )

    # ── Legacy Methods (giữ cho conversation.py cũ) ────────

    @staticmethod
    def update_stats(
        session: SessionState, 
        topic: str, 
        question_type: str, 
        is_correct: bool
    ) -> QuizStats:
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
        if not session.quiz_stats:
            return "Chua co du lieu hoc tap."
        return session.quiz_stats.get_summary()

    @staticmethod
    def get_mastery_level(session: SessionState, topic: str) -> float:
        if not session.quiz_stats or topic not in session.quiz_stats.by_topic:
            return 0.0
        return session.quiz_stats.by_topic[topic].accuracy
