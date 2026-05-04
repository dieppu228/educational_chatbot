import logging
from typing import Optional, List

from src.llm.memory import Session, MemoryManager
from src.llm.session_store import SessionStore
from src.llm.intent_router import IntentResult

logger = logging.getLogger("chatbot.session_manager")


class SessionManager:

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
        user_id: str = "anonymous",
    ) -> Session:
        current = self.memory.get_current_session(user_id)

        # Case 1: No current session
        if current is None:
            logger.info("No current session, creating new")
            return self._create_new_session(intent_result, user_id)

        # Case 2: Topic changed (detected by LLM)
        if intent_result.is_new_topic and intent_result.topic:
            logger.info(
                f"Topic changed: '{current.topic}' -> '{intent_result.topic}', "
                f"creating new session"
            )
            self._save_and_archive(current)
            return self._create_new_session(intent_result, user_id)

        # Case 3: Generate intent with different task type
        if intent_result.primary_intent == "generate":
            if self._is_generate_type_change(current, intent_result):
                logger.info(
                    f"Generate type change detected, creating new session"
                )
                self._save_and_archive(current)
                return self._create_new_session(intent_result, user_id)

        # Case 4: Keep current session
        logger.debug(f"Keeping current session: {current.session_id}")

        # Update topic if LLM detected one and current has none
        if intent_result.topic and not current.topic:
            current.topic = intent_result.topic

        # Update book if LLM detected one and current has none
        if intent_result.book and not current.book:
            current.book = intent_result.book

        current.touch()
        return current

    def _is_generate_type_change(
        self,
        current: Session,
        intent_result: IntentResult,
    ) -> bool:
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

    def _create_new_session(self, intent_result: IntentResult, user_id: str) -> Session:
        session = self.memory.create_session(
            topic=intent_result.topic or "",
            intent=intent_result.primary_intent,
            user_id=user_id,
        )
        # Set book from intent detection
        session.book = intent_result.book
        logger.info(
            f"New session created: id={session.session_id}, "
            f"topic='{session.topic}', intent={session.intent}, "
            f"book={session.book}"
        )
        return session

    def _save_and_archive(self, session: Session) -> None:
        self.store.auto_save(session)
        logger.debug(f"Session archived: {session.session_id}")

    def load_previous_session(self, session_id: str) -> Optional[Session]:
        session = self.store.load_session(session_id)
        if session:
            self.memory.set_current_session(session.user_id, session)
            if session not in self.memory.sessions_v2:
                self.memory.sessions_v2.append(session)
        return session

    def list_sessions(self) -> list:
        return self.store.list_sessions()


__all__ = ["SessionManager"]
