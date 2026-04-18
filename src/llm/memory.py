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

    def record_attempt(self, user_answer: Any, is_correct: bool, score: Optional[float] = None):
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

    def create_review_round(self, source_round_ids: Optional[List[int]] = None) -> Optional[QuizRound]:
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
    slide_output: Optional[Dict] = None     # Graph output (slides, status, HITL data)
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
    user_id: str = "anonymous"        # Owner user id (from UI/client)
    topic: str = ""
    intent: str = "chat"                # Primary intent: generate|interact|analyze|explain|chat
    book: Optional[str] = None          # "CD" | "KNTT" | None (book series filter)
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
            "user_id": self.user_id,
            "topic": self.topic,
            "intent": self.intent,
            "book": self.book,
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
            user_id=data.get("user_id") or data.get("metadata", {}).get("user_id", "anonymous"),
            topic=data.get("topic", ""),
            intent=data.get("intent", "chat"),
            book=data.get("book"),
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
    v3: Chỉ dùng Session mới (v2). Legacy SessionState removed.
    """

    def __init__(self, max_context_messages: int = 10):
        # Sessions v2
        self.sessions_v2: List[Session] = []
        self.current_session_v2: Optional[Session] = None
        self.current_sessions_by_user: Dict[str, Session] = {}
        self.max_context_messages = max_context_messages

    def _normalize_user_id(self, user_id: Optional[str]) -> str:
        return user_id or "anonymous"

    # ── v2 Methods ──────────────────────────────────────────

    def create_session(
        self,
        topic: str = "",
        intent: str = "chat",
        user_id: Optional[str] = None,
    ) -> Session:
        """Create a new v2 session."""
        uid = self._normalize_user_id(user_id)
        session = Session(topic=topic, intent=intent, user_id=uid)
        self.sessions_v2.append(session)
        self.current_session_v2 = session
        self.current_sessions_by_user[uid] = session
        return session

    def get_session(self, session_id: str, user_id: Optional[str] = None) -> Optional[Session]:
        """Get a v2 session by ID."""
        for s in self.sessions_v2:
            if s.session_id == session_id:
                uid = self._normalize_user_id(user_id or s.user_id)
                self.current_session_v2 = s
                self.current_sessions_by_user[uid] = s
                return s
        return None

    def get_current_session(self, user_id: Optional[str] = None) -> Optional[Session]:
        """Get current active session for a specific user."""
        uid = self._normalize_user_id(user_id)
        return self.current_sessions_by_user.get(uid)

    def set_current_session(self, user_id: Optional[str], session: Session) -> None:
        """Set current active session for a specific user."""
        uid = self._normalize_user_id(user_id or session.user_id)
        self.current_session_v2 = session
        self.current_sessions_by_user[uid] = session

    def get_or_create_session(
        self,
        topic: str = "",
        intent: str = "chat",
        user_id: Optional[str] = None,
    ) -> Session:
        """Get current session or create new one."""
        current = self.get_current_session(user_id)
        if current is not None:
            return current
        return self.create_session(topic=topic, intent=intent, user_id=user_id)

    def switch_session(self, topic: str, intent: str, user_id: Optional[str] = None) -> Session:
        """Save current session and create a new one."""
        new_session = self.create_session(topic=topic, intent=intent, user_id=user_id)
        return new_session

    def get_context(self, user_id: Optional[str] = None) -> List[dict]:
        """Get context window from current v2 session."""
        current = self.get_current_session(user_id)
        if not current:
            return []
        return current.get_context_messages(self.max_context_messages)

    def clear_user_session(self, user_id: Optional[str] = None) -> None:
        """Detach current active session mapping for one user (keeps stored history)."""
        uid = self._normalize_user_id(user_id)
        current = self.current_sessions_by_user.pop(uid, None)
        if current and self.current_session_v2 and self.current_session_v2.session_id == current.session_id:
            self.current_session_v2 = None
