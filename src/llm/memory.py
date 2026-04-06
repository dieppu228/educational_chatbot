"""
Memory Manager v2 — State & Session Management for EduBot.

New data models:
    - QuestionRecord: Chi tiết 1 câu hỏi + kết quả trả lời
    - QuizRound: 1 lần user yêu cầu sinh câu hỏi
    - QuizSessionState: State chuyên biệt cho quiz session
    - SlideSessionState: State cho slide session (kế thừa quiz exercise)
    - Session: Thay thế SessionState cũ

Backward-compatible: TaskItem, SessionState, QuizStats vẫn giữ lại.
"""

import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


# ============================================================
# BACKWARD-COMPATIBLE DATA MODELS (giữ lại cho conversation.py cũ)
# ============================================================

@dataclass
class TaskItem:
    """
    Item linh hoạt — lưu bất kỳ loại output nào.
    DEPRECATED: Dùng QuestionRecord thay thế cho code mới.
    """
    type: str
    content: Dict[str, Any]
    index: int = 0


@dataclass
class Message:
    """Tin nhắn trong hội thoại."""
    role: str       # "user" | "assistant"
    content: str

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        return cls(role=data["role"], content=data["content"])


# ============================================================
# BACKWARD-COMPATIBLE: QuizStats, TopicStats, SessionState
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
    """DEPRECATED: Dùng QuizSessionState thay thế."""
    total_questions: int = 0
    correct_answers: int = 0
    by_topic: Dict[str, TopicStats] = field(default_factory=dict)
    by_type: Dict[str, int] = field(default_factory=dict)

    @property
    def accuracy(self) -> float:
        return self.correct_answers / self.total_questions if self.total_questions > 0 else 0.0

    def record_answer(self, topic: str, question_type: str, is_correct: bool):
        self.total_questions += 1
        if is_correct:
            self.correct_answers += 1
        if topic not in self.by_topic:
            self.by_topic[topic] = TopicStats()
        self.by_topic[topic].total += 1
        if is_correct:
            self.by_topic[topic].correct += 1
        self.by_type[question_type] = self.by_type.get(question_type, 0) + 1

    def get_weak_topics(self, threshold: float = 0.5) -> List[str]:
        return [t for t, s in self.by_topic.items() if s.total >= 2 and s.accuracy < threshold]

    def get_strong_topics(self, threshold: float = 0.8) -> List[str]:
        return [t for t, s in self.by_topic.items() if s.total >= 2 and s.accuracy >= threshold]

    def get_summary(self) -> str:
        if self.total_questions == 0:
            return "Chua co cau hoi nao."
        lines = [f"Tong ket: {self.correct_answers}/{self.total_questions} dung ({self.accuracy:.0%})"]
        weak = self.get_weak_topics()
        if weak:
            lines.append(f"Can on tap: {', '.join(weak)}")
        strong = self.get_strong_topics()
        if strong:
            lines.append(f"Tot o: {', '.join(strong)}")
        return "\n".join(lines)


@dataclass
class SessionState:
    """DEPRECATED: Dùng Session thay thế cho code mới."""
    session_id: int
    intent: str = "chat"
    task_type: Optional[str] = None
    topic: Optional[str] = None
    items: List[TaskItem] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    quiz_stats: QuizStats = field(default_factory=QuizStats)


# ============================================================
# NEW DATA MODELS — v2
# ============================================================

@dataclass
class QuestionRecord:
    """
    Lưu chi tiết 1 câu hỏi + kết quả trả lời.

    question_id format:
        Quiz: "r{round_id}_q{index}"       → "r0_q0", "r2_q3"
        Slide exercise: "slide_ex{slide_idx}_q{index}" → "slide_ex0_q1"
        Review: "rev{round_id}_q{index}"    → "rev0_q0"
    """
    question_id: str
    question_type: str              # "mcq" | "essay" | "fill_blank" | "true_false"
    content: Dict[str, Any]         # Full question content from schema output

    # Tracking results
    user_answer: Optional[Any] = None
    is_correct: Optional[bool] = None
    score: Optional[float] = None       # For essay scoring (0-10)
    answered_at: Optional[str] = None   # ISO timestamp
    attempt_count: int = 0

    # Source tracking
    source: str = "quiz"                # "quiz" | "slide_exercise" | "review"

    def record_attempt(self, user_answer: Any, is_correct: bool, score: float = None):
        """Record a user's attempt at answering this question."""
        self.user_answer = user_answer
        self.is_correct = is_correct
        self.score = score
        self.answered_at = datetime.now().isoformat()
        self.attempt_count += 1

    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "question_type": self.question_type,
            "content": self.content,
            "user_answer": self.user_answer,
            "is_correct": self.is_correct,
            "score": self.score,
            "answered_at": self.answered_at,
            "attempt_count": self.attempt_count,
            "source": self.source,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "QuestionRecord":
        return cls(**data)

    def to_task_item(self) -> TaskItem:
        """Convert to legacy TaskItem for backward compatibility."""
        return TaskItem(type=self.question_type, content=self.content, index=0)


@dataclass
class QuizRound:
    """
    Đại diện cho 1 lần user yêu cầu sinh câu hỏi.

    Ví dụ:
        Round 0: User yêu cầu "Tạo 3 câu MCQ về mạng LAN"
        Round 1: User yêu cầu "Thêm 5 câu nữa"
        Round 2: User yêu cầu "Tạo 2 câu tự luận"
    """
    round_id: int
    question_type: str              # "mcq" | "essay" | "fill_blank" | "true_false"
    query: str                      # Original user query
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    questions: List[QuestionRecord] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.questions)

    @property
    def answered(self) -> int:
        return sum(1 for q in self.questions if q.user_answer is not None)

    @property
    def correct(self) -> int:
        return sum(1 for q in self.questions if q.is_correct is True)

    @property
    def wrong_questions(self) -> List[QuestionRecord]:
        """Return questions answered incorrectly."""
        return [q for q in self.questions if q.is_correct is False]

    @property
    def unanswered_questions(self) -> List[QuestionRecord]:
        """Return questions not yet answered."""
        return [q for q in self.questions if q.user_answer is None]

    def to_dict(self) -> dict:
        return {
            "round_id": self.round_id,
            "question_type": self.question_type,
            "query": self.query,
            "created_at": self.created_at,
            "questions": [q.to_dict() for q in self.questions],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "QuizRound":
        questions = [QuestionRecord.from_dict(q) for q in data.get("questions", [])]
        return cls(
            round_id=data["round_id"],
            question_type=data["question_type"],
            query=data["query"],
            created_at=data.get("created_at", datetime.now().isoformat()),
            questions=questions,
        )


@dataclass
class QuizSessionState:
    """
    State chuyên biệt cho quiz session.
    Lưu trữ nhiều rounds, hỗ trợ ôn tập câu sai.
    """
    rounds: List[QuizRound] = field(default_factory=list)

    @property
    def total_questions(self) -> int:
        return sum(r.total for r in self.rounds)

    @property
    def total_answered(self) -> int:
        return sum(r.answered for r in self.rounds)

    @property
    def total_correct(self) -> int:
        return sum(r.correct for r in self.rounds)

    @property
    def accuracy(self) -> float:
        answered = self.total_answered
        return self.total_correct / answered if answered > 0 else 0.0

    def create_round(self, question_type: str, query: str) -> QuizRound:
        """Create a new quiz round and append to rounds list."""
        round_obj = QuizRound(
            round_id=len(self.rounds),
            question_type=question_type,
            query=query,
        )
        self.rounds.append(round_obj)
        return round_obj

    def get_round(self, round_id: int) -> Optional[QuizRound]:
        """Get a specific round by ID."""
        for r in self.rounds:
            if r.round_id == round_id:
                return r
        return None

    def get_latest_round(self) -> Optional[QuizRound]:
        """Get the most recent round."""
        return self.rounds[-1] if self.rounds else None

    def get_all_questions(self) -> List[QuestionRecord]:
        """Get all questions across all rounds."""
        all_q = []
        for r in self.rounds:
            all_q.extend(r.questions)
        return all_q

    def get_wrong_questions(self, round_id: Optional[int] = None) -> List[QuestionRecord]:
        """
        Get wrong questions.
        round_id=None → all rounds, round_id=0 → only round 0.
        """
        if round_id is not None:
            target_round = self.get_round(round_id)
            return target_round.wrong_questions if target_round else []
        
        wrong = []
        for r in self.rounds:
            wrong.extend(r.wrong_questions)
        return wrong

    def get_wrong_questions_by_type(self, q_type: str) -> List[QuestionRecord]:
        """Get wrong questions filtered by question type."""
        return [q for q in self.get_wrong_questions() if q.question_type == q_type]

    def create_review_round(self, source_round_ids: List[int] = None) -> Optional[QuizRound]:
        """
        Create a review round from wrong questions of specified rounds.
        source_round_ids=None → collect from all rounds.
        """
        wrong = []
        if source_round_ids:
            for rid in source_round_ids:
                wrong.extend(self.get_wrong_questions(round_id=rid))
        else:
            wrong = self.get_wrong_questions()

        if not wrong:
            return None

        review_round = QuizRound(
            round_id=len(self.rounds),
            question_type="review",
            query="On tap cau sai",
        )
        for i, q in enumerate(wrong):
            review_q = QuestionRecord(
                question_id=f"rev{review_round.round_id}_q{i}",
                question_type=q.question_type,
                content=q.content,
                source="review",
            )
            review_round.questions.append(review_q)

        self.rounds.append(review_round)
        return review_round

    def get_summary(self) -> str:
        """Generate a text summary of quiz progress."""
        if not self.rounds:
            return "Chua co cau hoi nao."

        lines = []
        lines.append(f"Tong cong: {self.total_questions} cau | "
                      f"Da tra loi: {self.total_answered} | "
                      f"Dung: {self.total_correct} ({self.accuracy:.0%})")

        for r in self.rounds:
            status = f"Round {r.round_id} ({r.question_type}): "
            status += f"{r.correct}/{r.total} dung"
            if r.wrong_questions:
                status += f" | {len(r.wrong_questions)} cau sai"
            lines.append(f"  - {status}")

        wrong_total = len(self.get_wrong_questions())
        if wrong_total > 0:
            lines.append(f"Tong cau sai can on tap: {wrong_total}")

        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {"rounds": [r.to_dict() for r in self.rounds]}

    @classmethod
    def from_dict(cls, data: dict) -> "QuizSessionState":
        rounds = [QuizRound.from_dict(r) for r in data.get("rounds", [])]
        return cls(rounds=rounds)


@dataclass
class SlideSessionState:
    """
    State chuyên biệt cho slide session.
    Kế thừa quiz mechanism cho exercise questions trong slide.
    """
    slide_output: Optional[Dict] = None     # SlideGenerationOutput serialized
    slide_html: Optional[str] = None        # HTML rendered

    # Exercise tracking (inherits quiz mechanism)
    exercise_questions: List[QuestionRecord] = field(default_factory=list)

    @property
    def has_exercises(self) -> bool:
        return len(self.exercise_questions) > 0

    @property
    def total_exercises(self) -> int:
        return len(self.exercise_questions)

    @property
    def answered_exercises(self) -> int:
        return sum(1 for q in self.exercise_questions if q.user_answer is not None)

    @property
    def correct_exercises(self) -> int:
        return sum(1 for q in self.exercise_questions if q.is_correct is True)

    def get_wrong_exercises(self) -> List[QuestionRecord]:
        """Get exercise questions answered incorrectly."""
        return [q for q in self.exercise_questions if q.is_correct is False]

    def get_unanswered_exercises(self) -> List[QuestionRecord]:
        """Get exercises not yet attempted."""
        return [q for q in self.exercise_questions if q.user_answer is None]

    def add_exercise(self, question_type: str, content: dict, slide_idx: int, q_idx: int):
        """Add an exercise question extracted from a slide."""
        record = QuestionRecord(
            question_id=f"slide_ex{slide_idx}_q{q_idx}",
            question_type=question_type,
            content=content,
            source="slide_exercise",
        )
        self.exercise_questions.append(record)
        return record

    def to_dict(self) -> dict:
        return {
            "slide_output": self.slide_output,
            "slide_html": self.slide_html,
            "exercise_questions": [q.to_dict() for q in self.exercise_questions],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SlideSessionState":
        exercises = [QuestionRecord.from_dict(q) for q in data.get("exercise_questions", [])]
        return cls(
            slide_output=data.get("slide_output"),
            slide_html=data.get("slide_html"),
            exercise_questions=exercises,
        )


@dataclass
class Session:
    """
    Session v2 — 1 topic + 1 primary intent.
    Replaces the old SessionState for new code.
    """
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    topic: str = ""
    intent: str = "chat"                # Primary intent: generate|interact|analyze|explain|chat
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # Conversation history
    messages: List[Message] = field(default_factory=list)

    # Intent-specific state (only one should be active)
    quiz_state: Optional[QuizSessionState] = None
    slide_state: Optional[SlideSessionState] = None

    # General metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def touch(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now().isoformat()

    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.messages.append(Message(role=role, content=content))
        self.touch()

    def get_context_messages(self, max_messages: int = 10) -> List[dict]:
        """Get recent messages as list of dicts for LLM context."""
        recent = self.messages[-max_messages:]
        return [m.to_dict() for m in recent]

    def ensure_quiz_state(self) -> QuizSessionState:
        """Ensure quiz_state exists, create if needed."""
        if self.quiz_state is None:
            self.quiz_state = QuizSessionState()
        return self.quiz_state

    def ensure_slide_state(self) -> SlideSessionState:
        """Ensure slide_state exists, create if needed."""
        if self.slide_state is None:
            self.slide_state = SlideSessionState()
        return self.slide_state

    def get_all_question_records(self) -> List[QuestionRecord]:
        """Get all questions from both quiz and slide states."""
        records = []
        if self.quiz_state:
            records.extend(self.quiz_state.get_all_questions())
        if self.slide_state:
            records.extend(self.slide_state.exercise_questions)
        return records

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "topic": self.topic,
            "intent": self.intent,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "messages": [m.to_dict() for m in self.messages],
            "quiz_state": self.quiz_state.to_dict() if self.quiz_state else None,
            "slide_state": self.slide_state.to_dict() if self.slide_state else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        messages = [Message.from_dict(m) for m in data.get("messages", [])]
        quiz_state = QuizSessionState.from_dict(data["quiz_state"]) if data.get("quiz_state") else None
        slide_state = SlideSessionState.from_dict(data["slide_state"]) if data.get("slide_state") else None
        return cls(
            session_id=data.get("session_id", str(uuid.uuid4())[:8]),
            topic=data.get("topic", ""),
            intent=data.get("intent", "chat"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
            messages=messages,
            quiz_state=quiz_state,
            slide_state=slide_state,
            metadata=data.get("metadata", {}),
        )


# ============================================================
# MEMORY MANAGER v2
# ============================================================

class MemoryManager:
    """
    Quản lý sessions và conversation context.
    v2: Hỗ trợ cả Session mới và SessionState cũ.
    """

    def __init__(self, max_context_messages: int = 10):
        # New v2 sessions
        self.sessions_v2: List[Session] = []
        self.current_session_v2: Optional[Session] = None
        self.max_context_messages = max_context_messages

        # Legacy (backward-compat for conversation.py cũ)
        self.sessions: List[SessionState] = []
        self.current_session: Optional[SessionState] = None

    # ── v2 Methods ──────────────────────────────────────────

    def create_session_v2(self, topic: str = "", intent: str = "chat") -> Session:
        """Create a new v2 session."""
        session = Session(topic=topic, intent=intent)
        self.sessions_v2.append(session)
        self.current_session_v2 = session
        return session

    def get_session_v2(self, session_id: str) -> Optional[Session]:
        """Get a v2 session by ID."""
        for s in self.sessions_v2:
            if s.session_id == session_id:
                self.current_session_v2 = s
                return s
        return None

    def get_or_create_session_v2(self, topic: str = "", intent: str = "chat") -> Session:
        """Get current session or create new one."""
        if self.current_session_v2 is not None:
            return self.current_session_v2
        return self.create_session_v2(topic=topic, intent=intent)

    def switch_session_v2(self, topic: str, intent: str) -> Session:
        """Save current session and create a new one."""
        new_session = self.create_session_v2(topic=topic, intent=intent)
        return new_session

    def get_context_v2(self) -> List[dict]:
        """Get context window from current v2 session."""
        if not self.current_session_v2:
            return []
        return self.current_session_v2.get_context_messages(self.max_context_messages)

    # ── Legacy Methods (giữ cho conversation.py cũ) ────────

    def start_session(self, intent: str, task_type: str = None,
                      topic: str = None, metadata: dict = None) -> SessionState:
        session = SessionState(
            session_id=len(self.sessions),
            intent=intent, task_type=task_type,
            topic=topic, metadata=metadata or {},
        )
        self.sessions.append(session)
        self.current_session = session
        return session

    def add_message(self, role: str, content: str):
        if self.current_session:
            self.current_session.messages.append(Message(role=role, content=content))

    def add_item(self, item_type: str, content: dict):
        if self.current_session:
            item = TaskItem(type=item_type, content=content, index=len(self.current_session.items))
            self.current_session.items.append(item)
            return item

    def get_context(self) -> List[dict]:
        if not self.current_session:
            return []
        recent = self.current_session.messages[-self.max_context_messages:]
        return [{"role": m.role, "content": m.content} for m in recent]

    def get_session(self, session_id: int) -> Optional[SessionState]:
        for s in self.sessions:
            if s.session_id == session_id:
                self.current_session = s
                return s
        return None

    def create_session(self, intent: str = "chat", **kwargs) -> SessionState:
        return self.start_session(intent=intent, **kwargs)

    def get_items(self, item_type: str = None) -> List[TaskItem]:
        if not self.current_session:
            return []
        items = self.current_session.items
        if item_type:
            items = [i for i in items if i.type == item_type]
        return items
