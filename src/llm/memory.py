"""
Memory Manager — Quản lý conversation memory và session state.

Chức năng:
    - Quản lý sessions (tạo, lưu, load)
    - Context window (giữ N tin nhắn gần nhất)
    - Lưu TaskItem linh hoạt (MCQ, essay, fill_blank, slide, lesson_plan)
    - In-memory student tracking (QuizStats) — không cần login/database
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class TaskItem:
    """
    Item linh hoạt — lưu bất kỳ loại output nào.
    
    type: "mcq" | "essay" | "fill_blank" | "true_false" | "slide" | "lesson_plan"
    content: dict chứa nội dung theo type
    
    Ví dụ content:
        MCQ:       {"question": "...", "options": {"A":..}, "correct": "A", "explanation": "..."}
        Essay:     {"question": "...", "sample_answer": "...", "rubric": "..."}
        Fill:      {"text_with_blanks": "Mạng ___ là ...", "answers": ["LAN"]}
        TrueFalse: {"statement": "...", "correct": True, "explanation": "..."}
        Slide:     {"title": "...", "bullets": [...], "notes": "..."}
        Plan:      {"objective": "...", "activities": [...], "assessment": "..."}
    """
    type: str
    content: Dict[str, Any]
    index: int = 0


@dataclass
class Message:
    """Tin nhắn trong hội thoại."""
    role: str       # "user" | "assistant"  
    content: str


# ============================================================
# IN-MEMORY STUDENT TRACKING (không cần login/database)
# ============================================================

@dataclass
class TopicStats:
    """Thống kê cho 1 chủ đề cụ thể trong session."""
    total: int = 0
    correct: int = 0

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total > 0 else 0.0


@dataclass
class QuizStats:
    """
    Tracking progress trong conversation.
    
    Tồn tại trong SessionState → data sống trong conversation,
    mất khi đóng tab (không cần login).
    """
    total_questions: int = 0
    correct_answers: int = 0
    by_topic: Dict[str, TopicStats] = field(default_factory=dict)
    by_type: Dict[str, int] = field(default_factory=dict)  # {"mcq": 5, "essay": 2}

    @property
    def accuracy(self) -> float:
        return self.correct_answers / self.total_questions if self.total_questions > 0 else 0.0

    def record_answer(self, topic: str, question_type: str, is_correct: bool):
        """Ghi nhận 1 câu trả lời."""
        self.total_questions += 1
        if is_correct:
            self.correct_answers += 1
        
        # Update by_topic
        if topic not in self.by_topic:
            self.by_topic[topic] = TopicStats()
        self.by_topic[topic].total += 1
        if is_correct:
            self.by_topic[topic].correct += 1
        
        # Update by_type
        self.by_type[question_type] = self.by_type.get(question_type, 0) + 1

    def get_weak_topics(self, threshold: float = 0.5) -> List[str]:
        """Tìm chủ đề yếu (accuracy < threshold)."""
        weak = []
        for topic, stats in self.by_topic.items():
            if stats.total >= 2 and stats.accuracy < threshold:
                weak.append(topic)
        return weak

    def get_strong_topics(self, threshold: float = 0.8) -> List[str]:
        """Tìm chủ đề mạnh (accuracy >= threshold)."""
        strong = []
        for topic, stats in self.by_topic.items():
            if stats.total >= 2 and stats.accuracy >= threshold:
                strong.append(topic)
        return strong

    def get_summary(self) -> str:
        """Tóm tắt progress trong session."""
        if self.total_questions == 0:
            return "Chưa có câu hỏi nào được trả lời."
        
        lines = [
            f"📊 Tổng kết: {self.correct_answers}/{self.total_questions} đúng "
            f"({self.accuracy:.0%})",
        ]
        
        weak = self.get_weak_topics()
        if weak:
            lines.append(f"⚠️ Cần ôn tập: {', '.join(weak)}")
        
        strong = self.get_strong_topics()
        if strong:
            lines.append(f"💪 Tốt ở: {', '.join(strong)}")
        
        return "\n".join(lines)


@dataclass
class SessionState:
    """
    State của một phiên làm việc.
    
    Mỗi session gắn với 1 intent + task_type cụ thể.
    quiz_stats: tracking progress trong session (in-memory, không cần login).
    """
    session_id: int
    intent: str = "chat"
    task_type: Optional[str] = None
    topic: Optional[str] = None
    items: List[TaskItem] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    quiz_stats: QuizStats = field(default_factory=QuizStats)


# ============================================================
# MEMORY MANAGER
# ============================================================

class MemoryManager:
    """Quản lý sessions và conversation context."""
    
    def __init__(self, max_context_messages: int = 10):
        self.sessions: List[SessionState] = []
        self.current_session: Optional[SessionState] = None
        self.max_context_messages = max_context_messages
    
    def start_session(self, intent: str, task_type: str = None, 
                      topic: str = None, metadata: dict = None) -> SessionState:
        """Tạo session mới."""
        session = SessionState(
            session_id=len(self.sessions),
            intent=intent,
            task_type=task_type,
            topic=topic,
            metadata=metadata or {},
        )
        self.sessions.append(session)
        self.current_session = session
        return session
    
    def add_message(self, role: str, content: str):
        """Thêm tin nhắn vào session hiện tại."""
        if self.current_session:
            self.current_session.messages.append(Message(role=role, content=content))
    
    def add_item(self, item_type: str, content: dict):
        """Thêm TaskItem vào session hiện tại."""
        if self.current_session:
            item = TaskItem(
                type=item_type,
                content=content,
                index=len(self.current_session.items),
            )
            self.current_session.items.append(item)
            return item
    
    def get_context(self) -> List[dict]:
        """Lấy context window (N tin nhắn gần nhất) dạng list dict."""
        if not self.current_session:
            return []
        recent = self.current_session.messages[-self.max_context_messages:]
        return [{"role": m.role, "content": m.content} for m in recent]
    
    def get_session(self, session_id: int) -> Optional[SessionState]:
        """Lấy session theo ID."""
        for s in self.sessions:
            if s.session_id == session_id:
                self.current_session = s
                return s
        return None

    def create_session(self, intent: str = "chat", **kwargs) -> SessionState:
        """Tạo session mới (alias cho start_session)."""
        return self.start_session(intent=intent, **kwargs)

    def get_items(self, item_type: str = None) -> List[TaskItem]:
        """Lấy items trong session, filter theo type nếu cần."""
        if not self.current_session:
            return []
        items = self.current_session.items
        if item_type:
            items = [i for i in items if i.type == item_type]
        return items
