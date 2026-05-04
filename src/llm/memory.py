import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


# ============================================================
# BACKWARD-COMPATIBLE DATA MODELS (giữ lại cho conversation.py cũ)
# ============================================================

@dataclass
class TaskItem:
    type: str
    content: Dict[str, Any]
    index: int = 0


@dataclass
class Message:
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
        return TaskItem(type=self.question_type, content=self.content, index=0)


@dataclass
class QuizRound:
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
        return [q for q in self.questions if q.is_correct is False]

    @property
    def unanswered_questions(self) -> List[QuestionRecord]:
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
        round_obj = QuizRound(
            round_id=len(self.rounds),
            question_type=question_type,
            query=query,
        )
        self.rounds.append(round_obj)
        return round_obj

    def get_round(self, round_id: int) -> Optional[QuizRound]:
        for r in self.rounds:
            if r.round_id == round_id:
                return r
        return None

    def get_latest_round(self) -> Optional[QuizRound]:
        return self.rounds[-1] if self.rounds else None

    def get_all_questions(self) -> List[QuestionRecord]:
        all_q = []
        for r in self.rounds:
            all_q.extend(r.questions)
        return all_q

    def get_wrong_questions(self, round_id: Optional[int] = None) -> List[QuestionRecord]:
        if round_id is not None:
            target_round = self.get_round(round_id)
            return target_round.wrong_questions if target_round else []
        
        wrong = []
        for r in self.rounds:
            wrong.extend(r.wrong_questions)
        return wrong

    def get_wrong_questions_by_type(self, q_type: str) -> List[QuestionRecord]:
        return [q for q in self.get_wrong_questions() if q.question_type == q_type]

    def create_review_round(self, source_round_ids: Optional[List[int]] = None) -> Optional[QuizRound]:
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
        return [q for q in self.exercise_questions if q.is_correct is False]

    def get_unanswered_exercises(self) -> List[QuestionRecord]:
        return [q for q in self.exercise_questions if q.user_answer is None]

    def add_exercise(self, question_type: str, content: dict, slide_idx: int, q_idx: int):
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
        self.updated_at = datetime.now().isoformat()

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role=role, content=content))
        self.touch()

    def get_context_messages(self, max_messages: int = 10) -> List[dict]:
        recent = self.messages[-max_messages:]
        return [m.to_dict() for m in recent]

    def ensure_quiz_state(self) -> QuizSessionState:
        if self.quiz_state is None:
            self.quiz_state = QuizSessionState()
        return self.quiz_state

    def ensure_slide_state(self) -> SlideSessionState:
        if self.slide_state is None:
            self.slide_state = SlideSessionState()
        return self.slide_state

    def get_all_question_records(self) -> List[QuestionRecord]:
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
        uid = self._normalize_user_id(user_id)
        session = Session(topic=topic, intent=intent, user_id=uid)
        self.sessions_v2.append(session)
        self.current_session_v2 = session
        self.current_sessions_by_user[uid] = session
        return session

    def get_session(self, session_id: str, user_id: Optional[str] = None) -> Optional[Session]:
        for s in self.sessions_v2:
            if s.session_id == session_id:
                uid = self._normalize_user_id(user_id or s.user_id)
                self.current_session_v2 = s
                self.current_sessions_by_user[uid] = s
                return s
        return None

    def get_current_session(self, user_id: Optional[str] = None) -> Optional[Session]:
        uid = self._normalize_user_id(user_id)
        return self.current_sessions_by_user.get(uid)

    def set_current_session(self, user_id: Optional[str], session: Session) -> None:
        uid = self._normalize_user_id(user_id or session.user_id)
        self.current_session_v2 = session
        self.current_sessions_by_user[uid] = session

    def get_or_create_session(
        self,
        topic: str = "",
        intent: str = "chat",
        user_id: Optional[str] = None,
    ) -> Session:
        current = self.get_current_session(user_id)
        if current is not None:
            return current
        return self.create_session(topic=topic, intent=intent, user_id=user_id)

    def switch_session(self, topic: str, intent: str, user_id: Optional[str] = None) -> Session:
        new_session = self.create_session(topic=topic, intent=intent, user_id=user_id)
        return new_session

    def get_context(self, user_id: Optional[str] = None) -> List[dict]:
        current = self.get_current_session(user_id)
        if not current:
            return []
        return current.get_context_messages(self.max_context_messages)

    def clear_user_session(self, user_id: Optional[str] = None) -> None:
        uid = self._normalize_user_id(user_id)
        current = self.current_sessions_by_user.pop(uid, None)
        if current and self.current_session_v2 and self.current_session_v2.session_id == current.session_id:
            self.current_session_v2 = None
