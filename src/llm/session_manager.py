"""
Session Manager — Session Lifecycle & Topic Change Detection.

Trách nhiệm:
    - Quyết định giữ session hiện tại hay tạo session mới
    - Auto-save session cũ khi chuyển session
    - Tích hợp với SessionStore cho persistence
"""

import logging
from typing import Optional, List

from src.llm.memory import Session, MemoryManager
from src.llm.session_store import SessionStore
from src.llm.intent_router import IntentResult

logger = logging.getLogger("chatbot.session_manager")


class SessionManager:
    """
    Quản lý session lifecycle.

    Quy tắc tạo session mới:
        1. is_new_topic = True (LLM detect topic change)
        2. Intent thay đổi loại chính (generate quiz → generate slide)
        3. Không có session hiện tại
    """

    # Intent groups that are compatible (same session)
    COMPATIBLE_INTENTS = {
        # interact/analyze/explain can stay in same session as generate
        "interact", "analyze", "explain", "chat",
    }

    def __init__(self, session_store: SessionStore, memory: MemoryManager):
        self.store = session_store
        self.memory = memory

    def resolve_session(
        self,
        intent_result: IntentResult,
    ) -> Session:
        """
        Determine which session to use.

        Logic:
            1. No current session → create new
            2. is_new_topic → save current, create new
            3. Generate-type intent change (quiz→slide) → save current, create new
            4. Otherwise → keep current session

        Args:
            intent_result: Output from IntentRouter

        Returns:
            Session to use for this interaction
        """
        current = self.memory.current_session_v2

        # Case 1: No current session
        if current is None:
            logger.info("No current session, creating new")
            return self._create_new_session(intent_result)

        # Case 2: Topic changed (detected by LLM)
        if intent_result.is_new_topic and intent_result.topic:
            logger.info(
                f"Topic changed: '{current.topic}' -> '{intent_result.topic}', "
                f"creating new session"
            )
            self._save_and_archive(current)
            return self._create_new_session(intent_result)

        # Case 3: Generate intent with different task type
        if intent_result.primary_intent == "generate":
            if self._is_generate_type_change(current, intent_result):
                logger.info(
                    f"Generate type change detected, creating new session"
                )
                self._save_and_archive(current)
                return self._create_new_session(intent_result)

        # Case 4: Keep current session
        logger.debug(f"Keeping current session: {current.session_id}")

        # Update topic if LLM detected one and current has none
        if intent_result.topic and not current.topic:
            current.topic = intent_result.topic

        current.touch()
        return current

    def _is_generate_type_change(
        self,
        current: Session,
        intent_result: IntentResult,
    ) -> bool:
        """
        Check if the generate request is a fundamentally different type.

        Quiz → more quiz (same type) → KEEP session
        Quiz → slide → NEW session
        Slide → quiz → NEW session
        """
        new_task_type = intent_result.task_type

        if not new_task_type:
            return False

        # Quiz types: mcq, essay, fill_blank, true_false
        quiz_types = {"mcq", "essay", "fill_blank", "true_false"}

        # Current session is quiz-based
        if current.quiz_state and current.quiz_state.rounds:
            if new_task_type in quiz_types:
                return False    # Same category → keep session, add round
            if new_task_type == "slide":
                return True     # Quiz → Slide → new session

        # Current session is slide-based
        if current.slide_state:
            if new_task_type in quiz_types:
                return True     # Slide → Quiz → new session

        return False

    def _create_new_session(self, intent_result: IntentResult) -> Session:
        """Create a new session based on intent result."""
        session = self.memory.create_session_v2(
            topic=intent_result.topic or "",
            intent=intent_result.primary_intent,
        )
        logger.info(
            f"New session created: id={session.session_id}, "
            f"topic='{session.topic}', intent={session.intent}"
        )
        return session

    def _save_and_archive(self, session: Session) -> None:
        """Save current session before switching."""
        self.store.auto_save(session)
        logger.debug(f"Session archived: {session.session_id}")

    def load_previous_session(self, session_id: str) -> Optional[Session]:
        """Load a previously saved session."""
        session = self.store.load_session(session_id)
        if session:
            self.memory.current_session_v2 = session
            if session not in self.memory.sessions_v2:
                self.memory.sessions_v2.append(session)
        return session

    def list_sessions(self) -> list:
        """List all saved sessions (metadata only)."""
        return self.store.list_sessions()


__all__ = ["SessionManager"]
