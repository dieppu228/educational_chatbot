"""
Memory Manager — Quản lý conversation memory và session state.

Chức năng:
    - Quản lý sessions (tạo, lưu, load)
    - Context window (giữ N tin nhắn gần nhất)
    - Lưu TaskItem linh hoạt (MCQ, essay, fill_blank, slide, lesson_plan)
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


@dataclass
class SessionState:
    """
    State của một phiên làm việc.
    
    Mỗi session gắn với 1 intent + task_type cụ thể.
    """
    session_id: int
    intent: str = "chat"
    task_type: Optional[str] = None
    topic: Optional[str] = None
    items: List[TaskItem] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


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
    
    def get_items(self, item_type: str = None) -> List[TaskItem]:
        """Lấy items trong session, filter theo type nếu cần."""
        if not self.current_session:
            return []
        items = self.current_session.items
        if item_type:
            items = [i for i in items if i.type == item_type]
        return items
