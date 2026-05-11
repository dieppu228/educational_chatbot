import asyncio
from typing import Optional
from src.llm.student_profile import StudentProfileManager, StudentProfile
from src.llm.memory import Session


class StudentTracker:
    
    def __init__(self, profile_manager: Optional[StudentProfileManager] = None):
        self.profile_manager = profile_manager or StudentProfileManager()
    
    def record_attempt(self, user_id: str, topic: str, score: float) -> None:
        self.profile_manager.record_attempt(user_id, topic, score)
    
    async def record_attempt_async(self, user_id: str, topic: str, score: float) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.record_attempt, user_id, topic, score)
    
    def get_profile(self, user_id: str) -> StudentProfile:
        return self.profile_manager.get_or_create(user_id)
    
    async def get_profile_async(self, user_id: str) -> StudentProfile:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_profile, user_id)
    
    def get_summary(self, user_id: str) -> str:
        return self.profile_manager.get_summary(user_id)
    
    async def get_summary_async(self, user_id: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_summary, user_id)
