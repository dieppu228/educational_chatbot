from typing import Optional
from src.llm.student_profile import StudentProfileManager, StudentProfile
from src.llm.memory import Session


class StudentTracker:
    """
    Quản lý student learning tracking.
    v3: Dùng StudentProfile in-memory, loại bỏ legacy QuizStats.
    """
    
    def __init__(self, profile_manager: Optional[StudentProfileManager] = None):
        self.profile_manager = profile_manager or StudentProfileManager()
    
    def record_attempt(self, user_id: str, topic: str, score: float) -> None:
        """
        Record learning attempt.
        
        Args:
            user_id: Unique student identifier (session_id)
            topic: Topic/lesson name
            score: Score 0-1 or 0-10 (auto-normalized)
        """
        self.profile_manager.record_attempt(user_id, topic, score)
    
    def get_profile(self, user_id: str) -> StudentProfile:
        """Get or create student profile."""
        return self.profile_manager.get_or_create(user_id)
    
    def get_summary(self, user_id: str) -> str:
        """Get summary of student progress."""
        return self.profile_manager.get_summary(user_id)
