import re
import logging
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass

from src.llm.memory import Session
from src.llm.intent_router import IntentResult

logger = logging.getLogger("chatbot.action_planner")


# ============================================================
# ACTION ENUM
# ============================================================

class Action(Enum):

    # Generate
    GENERATE_QUIZ = "generate_quiz"
    GENERATE_SLIDE = "generate_slide"
    GENERATE_LESSON_PLAN = "generate_lesson_plan"

    # Interact
    CHECK_ANSWER = "check_answer"
    REVIEW_WRONG = "review_wrong"
    EXPLAIN_QUESTION = "explain_question"
    ANSWER_EXERCISE = "answer_exercise"

    # Analyze
    GET_STATS = "get_stats"

    # Explain / Chat
    EXPLAIN_CONCEPT = "explain_concept"
    CHAT = "chat"


# ============================================================
# ACTION PLAN (result)
# ============================================================

@dataclass
class ActionPlan:
    action: Action
    reason: str                     # Why this action was chosen (for logging)
    round_id: Optional[int] = None  # For review: which round to review


# ============================================================
# KEYWORD PATTERNS
# ============================================================

# Keywords for detecting review intent
REVIEW_KEYWORDS = [
    r"ôn\s*lại", r"on\s*lai", r"câu\s*sai", r"cau\s*sai",
    r"làm\s*lại", r"lam\s*lai", r"xem\s*lại", r"xem\s*lai",
    r"review", r"ôn\s*tập", r"on\s*tap",
]

# Keywords for explain question (specific question, not general concept)
EXPLAIN_QUESTION_KEYWORDS = [
    r"giải\s*thích\s*câu", r"giai\s*thich\s*cau",
    r"giải\s*thích\s*(?:giúp|cho)?", r"giai\s*thich\s*(?:giup|cho)?",
    r"tại\s*sao\s*câu", r"tai\s*sao\s*cau",
    r"tại\s*sao\s*đáp\s*án", r"tai\s*sao\s*dap\s*an",
    r"vì\s*sao\s*đáp\s*án", r"vi\s*sao\s*dap\s*an",
    r"vì\s*sao", r"vi\s*sao",
    r"câu\s*\d+\s*(là|sao|thế)", r"cau\s*\d+",
]

# Keywords for stats/progress
STATS_KEYWORDS = [
    r"điểm\s*số", r"diem\s*so", r"thống\s*kê", r"thong\s*ke",
    r"tiến\s*độ", r"tien\s*do", r"đánh\s*giá", r"danh\s*gia",
    r"kết\s*quả", r"ket\s*qua", r"bao\s*nhiêu\s*câu",
    r"accuracy", r"progress",
]

# Regex for extracting round number: "lần 1", "round 2", "lượt 3"
ROUND_ID_PATTERN = re.compile(
    r"(?:lần|lan|round|luot|lượt)\s*(\d+)",
    re.IGNORECASE
)

ANSWER_KEY_KEYWORDS = [
    r"đưa\s*(?:ra\s*)?đáp\s*án", r"dua\s*(?:ra\s*)?dap\s*an",
    r"cho\s*(?:tôi|toi|mình|minh|em)?\s*(?:xem\s*)?đáp\s*án",
    r"cho\s*(?:toi|minh|em)?\s*(?:xem\s*)?dap\s*an",
    r"xem\s*đáp\s*án", r"xem\s*dap\s*an",
    r"đáp\s*án\s*câu\s*\d+", r"dap\s*an\s*cau\s*\d+",
    r"đáp\s*án\s*(?:đúng|dung|là\s*gì|la\s*gi|nào|nao)",
    r"dap\s*an\s*(?:dung|la\s*gi|nao)",
    r"answer\s*key",
]

ASSESSMENT_FOLLOWUP_KEYWORDS = [
    *ANSWER_KEY_KEYWORDS,
    r"\bcâu\s*\d+\b", r"\bcau\s*\d+\b",
    r"\b(?:đáp\s*án|dap\s*an|chọn|chon)\s*[ABCD]\b",
    r"\b[ABCD]\b",
    r"giải\s*thích\s*câu", r"giai\s*thich\s*cau",
]


def has_assessment_context(session: Optional[Session]) -> bool:
    if not session:
        return False
    has_quiz = bool(session.quiz_state and session.quiz_state.get_all_questions())
    has_slide_exercises = bool(session.slide_state and session.slide_state.has_exercises)
    return has_quiz or has_slide_exercises


def is_answer_key_request(message: str) -> bool:
    return any(re.search(pattern, message, re.IGNORECASE) for pattern in ANSWER_KEY_KEYWORDS)


def is_assessment_followup_message(message: str) -> bool:
    return any(re.search(pattern, message, re.IGNORECASE) for pattern in ASSESSMENT_FOLLOWUP_KEYWORDS)


# ============================================================
# ACTION PLANNER CLASS
# ============================================================

class ActionPlanner:

    def plan(
        self,
        intent_result: IntentResult,
        session: Optional[Session],
        message: str,
    ) -> ActionPlan:
        primary = intent_result.primary_intent
        msg_lower = message.lower()

        if has_assessment_context(session):
            if is_answer_key_request(msg_lower):
                return self._plan_interact(intent_result, session, msg_lower)
            if primary == "chat" and is_assessment_followup_message(msg_lower):
                return self._plan_interact(intent_result, session, msg_lower)

        if primary == "generate":
            return self._plan_generate(intent_result, msg_lower)

        elif primary == "interact":
            return self._plan_interact(intent_result, session, msg_lower)

        elif primary == "analyze":
            return self._plan_analyze(session, msg_lower)

        elif primary == "explain":
            return self._plan_explain(session, msg_lower)

        else:  # chat
            return ActionPlan(action=Action.CHAT, reason="Default chat intent")

    def plan_all(
        self,
        intent_results: List[IntentResult],
        session: Optional[Session],
        message: str,
    ) -> List[ActionPlan]:
        plans = []
        for intent_result in intent_results:
            plan = self.plan(intent_result, session, message)
            # Deduplicate: skip if same action as previous
            if plans and plans[-1].action == plan.action:
                logger.debug(
                    f"Skipping duplicate action: {plan.action.value}"
                )
                continue
            plans.append(plan)
        if any(plan.action != Action.CHAT for plan in plans):
            plans = [plan for plan in plans if plan.action != Action.CHAT]
        return plans

    # ── Generate ────────────────────────────────────────────

    def _plan_generate(self, intent_result: IntentResult, msg: str) -> ActionPlan:
        task_type = intent_result.task_type

        if task_type == "slide":
            return ActionPlan(action=Action.GENERATE_SLIDE, reason=f"task_type={task_type}")

        if task_type == "lesson_plan":
            return ActionPlan(action=Action.GENERATE_LESSON_PLAN, reason=f"task_type={task_type}")

        # Default to quiz generation (mcq/essay/fill/tf)
        return ActionPlan(action=Action.GENERATE_QUIZ, reason=f"task_type={task_type or 'mcq'}")

    # ── Interact ────────────────────────────────────────────

    def _plan_interact(
        self,
        intent_result: IntentResult,
        session: Optional[Session],
        msg: str,
    ) -> ActionPlan:

        # 1. Check for review/ôn tập keywords
        if self._matches_keywords(msg, REVIEW_KEYWORDS):
            round_id = self._extract_round_id(msg)
            return ActionPlan(
                action=Action.REVIEW_WRONG,
                reason=f"Review keywords detected, round_id={round_id}",
                round_id=round_id,
            )

        # 2. Check for explain specific question
        if self._matches_keywords(msg, EXPLAIN_QUESTION_KEYWORDS):
            return ActionPlan(
                action=Action.EXPLAIN_QUESTION,
                reason="Explain-question keywords detected",
            )

        # 3. Determine based on session state
        if session:
            # If session has slide exercises and user asks for answer key or answers,
            # keep the interaction with slide exercises instead of older quiz rounds.
            if session.slide_state and session.slide_state.has_exercises:
                if is_answer_key_request(msg) or is_assessment_followup_message(msg):
                    return ActionPlan(
                        action=Action.ANSWER_EXERCISE,
                        reason="Session has slide exercises",
                    )

            # If session has quiz state with questions → check answer
            if session.quiz_state and session.quiz_state.get_all_questions():
                return ActionPlan(
                    action=Action.CHECK_ANSWER,
                    reason="Session has quiz questions, assuming answer check",
                )

            # If session has slide exercises → answer exercise
            if session.slide_state and session.slide_state.has_exercises:
                return ActionPlan(
                    action=Action.ANSWER_EXERCISE,
                    reason="Session has slide exercises",
                )

        # Fallback: treat as chat
        return ActionPlan(
            action=Action.CHAT,
            reason="No matching interact context, fallback to chat",
        )

    # ── Analyze ─────────────────────────────────────────────

    def _plan_analyze(self, session: Optional[Session], msg: str) -> ActionPlan:
        return ActionPlan(action=Action.GET_STATS, reason="Analyze intent → stats")

    # ── Explain ─────────────────────────────────────────────

    def _plan_explain(self, session: Optional[Session], msg: str) -> ActionPlan:
        # If asking about a specific question in context
        if session and self._matches_keywords(msg, EXPLAIN_QUESTION_KEYWORDS):
            if (session.quiz_state and session.quiz_state.get_all_questions()) or \
               (session.slide_state and session.slide_state.has_exercises):
                return ActionPlan(
                    action=Action.EXPLAIN_QUESTION,
                    reason="Explain about specific question in session",
                )

        # General concept explanation
        return ActionPlan(action=Action.EXPLAIN_CONCEPT, reason="General concept explanation")

    # ── Helpers ─────────────────────────────────────────────

    def _matches_keywords(self, msg: str, patterns: list) -> bool:
        for pattern in patterns:
            if re.search(pattern, msg, re.IGNORECASE):
                return True
        return False

    def _extract_round_id(self, msg: str) -> Optional[int]:
        match = ROUND_ID_PATTERN.search(msg)
        if match:
            # User says "lần 1" meaning round_id 0
            return int(match.group(1)) - 1
        return None


__all__ = ["ActionPlanner", "ActionPlan", "Action"]
