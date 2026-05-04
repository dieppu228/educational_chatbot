
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class LessonProgress:
    topic: str
    attempts: int = 0
    scores: List[float] = field(default_factory=list)  # Normalized to 0-1
    last_attempted: Optional[str] = None
    
    @property
    def avg_score(self) -> float:
        return sum(self.scores) / len(self.scores) if self.scores else 0.0
    
    @property
    def last_score(self) -> float:
        return self.scores[-1] if self.scores else 0.0
    
    @property
    def mastered(self) -> bool:
        return self.avg_score >= 0.8 and self.attempts >= 3
    
    @property
    def difficulty(self) -> str:
        if self.avg_score >= 0.85:
            return "easy"
        elif self.avg_score >= 0.65:
            return "medium"
        else:
            return "hard"
    
    def record_attempt(self, score: float) -> None:
        # Auto-normalize to 0-1
        normalized = score / 10.0 if score > 1.0 else score
        normalized = max(0.0, min(1.0, normalized))  # Clamp to [0, 1]
        
        self.scores.append(normalized)
        self.attempts += 1
        self.last_attempted = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "attempts": self.attempts,
            "scores": self.scores,
            "last_attempted": self.last_attempted,
            "avg_score": self.avg_score,
            "last_score": self.last_score,
            "mastered": self.mastered,
            "difficulty": self.difficulty,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LessonProgress":
        return cls(
            topic=data.get("topic", ""),
            attempts=data.get("attempts", 0),
            scores=data.get("scores", []),
            last_attempted=data.get("last_attempted"),
        )


@dataclass
class StudentProfile:
    user_id: str
    
    # Lesson data
    lessons_studied: List[str] = field(default_factory=list)
    lesson_progress: Dict[str, LessonProgress] = field(default_factory=dict)
    
    # Timestamps
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def weak_topics(self) -> List[str]:
        return [
            topic for topic, progress in self.lesson_progress.items()
            if progress.avg_score < 0.65 and progress.attempts >= 2
        ]
    
    @property
    def strong_topics(self) -> List[str]:
        return [
            topic for topic, progress in self.lesson_progress.items()
            if progress.avg_score >= 0.8 and progress.attempts >= 2
        ]
    
    @property
    def total_attempts(self) -> int:
        return sum(p.attempts for p in self.lesson_progress.values())
    
    @property
    def avg_score_overall(self) -> float:
        if not self.lesson_progress:
            return 0.0
        total_score = sum(p.avg_score * p.attempts for p in self.lesson_progress.values())
        return total_score / self.total_attempts if self.total_attempts > 0 else 0.0
    
    def record_attempt(self, topic: str, score: float) -> None:
        # Create or get LessonProgress
        if topic not in self.lesson_progress:
            self.lesson_progress[topic] = LessonProgress(topic=topic)
            if topic not in self.lessons_studied:
                self.lessons_studied.append(topic)
        
        # Record the attempt
        self.lesson_progress[topic].record_attempt(score)
        self.last_active = datetime.now().isoformat()
    
    def get_summary(self) -> str:
        if not self.lessons_studied:
            return "Chưa có dữ liệu học tập."
        
        lines = [
            f"📚 Đã học: {len(self.lessons_studied)} bài",
            f"📊 Tổng nỗ lực: {self.total_attempts} lần",
            f"⭐ Điểm trung bình: {self.avg_score_overall:.0%}",
        ]
        
        if self.strong_topics:
            lines.append(f"🎯 Mạnh: {', '.join(self.strong_topics)}")
        
        if self.weak_topics:
            lines.append(f"📖 Cần ôn: {', '.join(self.weak_topics)}")
        
        return "\n".join(lines)
    
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "lessons_studied": self.lessons_studied,
            "lesson_progress": {
                topic: progress.to_dict()
                for topic, progress in self.lesson_progress.items()
            },
            "created_at": self.created_at,
            "last_active": self.last_active,
            "weak_topics": self.weak_topics,
            "strong_topics": self.strong_topics,
            "total_attempts": self.total_attempts,
            "avg_score_overall": self.avg_score_overall,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StudentProfile":
        profile = cls(
            user_id=data.get("user_id", ""),
            lessons_studied=data.get("lessons_studied", []),
            created_at=data.get("created_at", datetime.now().isoformat()),
            last_active=data.get("last_active", datetime.now().isoformat()),
        )
        
        # Deserialize lesson_progress
        for topic, progress_data in data.get("lesson_progress", {}).items():
            profile.lesson_progress[topic] = LessonProgress.from_dict(progress_data)
        
        return profile


class StudentProfileManager:
    
    def __init__(self):
        self.profiles: Dict[str, StudentProfile] = {}
    
    def get_or_create(self, user_id: str) -> StudentProfile:
        if user_id not in self.profiles:
            self.profiles[user_id] = StudentProfile(user_id=user_id)
        return self.profiles[user_id]
    
    def get(self, user_id: str) -> Optional[StudentProfile]:
        return self.profiles.get(user_id)
    
    def record_attempt(self, user_id: str, topic: str, score: float) -> None:
        profile = self.get_or_create(user_id)
        profile.record_attempt(topic, score)
    
    def get_summary(self, user_id: str) -> str:
        profile = self.get(user_id)
        if profile is None:
            return "Người dùng chưa có dữ liệu."
        return profile.get_summary()
    
    def list_all_profiles(self) -> Dict[str, StudentProfile]:
        return self.profiles.copy()
