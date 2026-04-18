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
    """All possible actions the Orchestrator can execute."""

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
    """Result of action planning."""
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
    r"tại\s*sao\s*câu", r"tai\s*sao\s*cau",
    r"vì\s*sao\s*đáp\s*án", r"vi\s*sao\s*dap\s*an",
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


# ============================================================
# ACTION PLANNER CLASS
# ============================================================

class ActionPlanner:
    """
    Rule-based action planner.
    Maps (IntentResult + Session state + message) → ActionPlan.

    No LLM calls. Pure Python logic.
    """

    def plan(
        self,
        intent_result: IntentResult,
        session: Optional[Session],
        message: str,
    ) -> ActionPlan:
        """
        Determine the action to execute.

        Args:
            intent_result: Output from IntentRouter (Level 1)
            session: Current session (may be None for new sessions)
            message: Original user message

        Returns:
            ActionPlan with action enum and reason
        """
        primary = intent_result.primary_intent
        msg_lower = message.lower()

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
        """
        Map List[IntentResult] → List[ActionPlan].

        Deduplicates consecutive identical actions to avoid
        running the same handler twice in a row.

        Args:
            intent_results: All detected intents (max 3)
            session: Current session
            message: Original user message

        Returns:
            List[ActionPlan] — 1 to N plans in execution order
        """
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
        return plans

    # ── Generate ────────────────────────────────────────────

    def _plan_generate(self, intent_result: IntentResult, msg: str) -> ActionPlan:
        """Resolve generate sub-intent from task_type."""
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
        """Resolve interact sub-intent based on session state + keywords."""

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
        """Resolve analyze sub-intent."""
        return ActionPlan(action=Action.GET_STATS, reason="Analyze intent → stats")

    # ── Explain ─────────────────────────────────────────────

    def _plan_explain(self, session: Optional[Session], msg: str) -> ActionPlan:
        """Resolve explain sub-intent."""
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
        """Check if message matches any keyword pattern."""
        for pattern in patterns:
            if re.search(pattern, msg, re.IGNORECASE):
                return True
        return False

    def _extract_round_id(self, msg: str) -> Optional[int]:
        """
        Extract round number from message.
        "ôn lại câu sai lần 1" → 0 (convert to 0-indexed)
        "review round 2" → 1
        """
        match = ROUND_ID_PATTERN.search(msg)
        if match:
            # User says "lần 1" meaning round_id 0
            return int(match.group(1)) - 1
        return None


__all__ = ["ActionPlanner", "ActionPlan", "Action"]
