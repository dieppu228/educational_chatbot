from typing import Optional
from src.llm.student_profile import StudentProfileManager, StudentProfile
from src.llm.memory import Session


class StudentTracker:
    
    def __init__(self, profile_manager: Optional[StudentProfileManager] = None):
        self.profile_manager = profile_manager or StudentProfileManager()
    
    def record_attempt(self, user_id: str, topic: str, score: float) -> None:
        self.profile_manager.record_attempt(user_id, topic, score)
    
    def get_profile(self, user_id: str) -> StudentProfile:
        return self.profile_manager.get_or_create(user_id)
    
    def get_summary(self, user_id: str) -> str:
        return self.profile_manager.get_summary(user_id)
