import json
import re
import os
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from google import genai
from google.genai.types import GenerateContentConfig

from src.config.config import settings
from src.llm.prompts import INTENT_ROUTER_PROMPT

logger = logging.getLogger("chatbot.intent_router")


# ============================================================
# INTENT RESULT
# ============================================================

@dataclass
class IntentResult:
    """Kết quả phân loại intent 2 tầng."""
    primary_intent: str         # "generate" | "interact" | "analyze" | "explain" | "chat"
    sub_intent: Optional[str] = None   # Filled by ActionPlanner
    task_type: Optional[str] = None    # "mcq" | "essay" | "fill_blank" | "true_false" | "slide" | ...
    topic: Optional[str] = None        # Detected topic
    is_new_topic: bool = False         # Whether topic changed from current session
    book: Optional[str] = None         # "CD" | "KNTT" | None (detected book series)
    raw_response: Optional[str] = None # Raw LLM response for debugging


# INTENT_ROUTER_PROMPT imported from src.llm.prompts


# ============================================================
# INTENT ROUTER CLASS
# ============================================================

class IntentRouter:
    """
    2-Level Intent Router.

    Level 1: LLM-based primary intent detection (1 API call).
    Level 2: Rule-based sub-intent resolution (see ActionPlanner).
    """

    VALID_INTENTS = {"generate", "interact", "analyze", "explain", "chat"}
    VALID_TASK_TYPES = {"mcq", "essay", "fill_blank", "true_false", "slide", "lesson_plan"}
    VALID_BOOKS = {"CD", "KNTT"}

    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or settings.GENAI_API_KEY or os.getenv("GENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("GENAI_API_KEY not set.")

        self.model_name = model_name or settings.LLM_MODEL or "gemini-2.5-flash-lite"
        self.client = genai.Client(api_key=self.api_key)

    def detect(
        self,
        query: str,
        current_topic: Optional[str] = None,
        session_messages: Optional[List[dict]] = None,
    ) -> IntentResult:
        """
        Detect primary intent + topic + is_new_topic in 1 LLM call.

        Args:
            query: User's current message
            current_topic: Topic of current session (for detecting topic change)
            session_messages: Recent conversation history

        Returns:
            IntentResult with primary_intent, task_type, topic, is_new_topic
        """
        try:
            # Build prompt
            session_context = self._format_session_context(session_messages)
            topic_instruction = self._build_topic_instruction(current_topic)

            prompt = INTENT_ROUTER_PROMPT.format(
                query=query,
                session_context=session_context,
                topic_instruction=topic_instruction,
            )

            # LLM call
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )

            raw = self._extract_text(response)
            result = self._parse_result(raw)

            if result:
                result.raw_response = raw
                logger.info(
                    f"IntentRouter: intent={result.primary_intent}, "
                    f"task_type={result.task_type}, topic={result.topic}, "
                    f"is_new_topic={result.is_new_topic}, book={result.book}"
                )
                return result

            return self._fallback(query)

        except Exception as e:
            logger.error(f"IntentRouter error: {e}")
            return self._fallback(query)

    def _build_topic_instruction(self, current_topic: Optional[str]) -> str:
        """Build instruction for topic change detection."""
        if current_topic:
            return (
                f"Session hien tai dang o chu de: \"{current_topic}\". "
                f"is_new_topic = true NEU query nay la ve 1 chu de KHAC HOAN TOAN. "
                f"is_new_topic = false NEU van lien quan den \"{current_topic}\"."
            )
        return "Khong co session truoc do. is_new_topic = true neu co topic moi."

    def _format_session_context(self, messages: Optional[List[dict]]) -> str:
        """Format recent messages for context."""
        if not messages:
            return ""
        recent = messages[-3:]
        lines = [f"  - {m.get('role', 'user')}: {m.get('content', '')[:150]}" for m in recent]
        return "\nNgu canh hoi thoai:\n" + "\n".join(lines) + "\n"

    def _extract_text(self, response) -> str:
        """Extract text from API response."""
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    return part.text.strip()
        return ""

    def _parse_result(self, raw: str) -> Optional[IntentResult]:
        """Parse LLM JSON response into IntentResult."""
        text = raw.strip()
        # Clean markdown code blocks if present
        text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

        try:
            data = json.loads(text.strip())

            # Validate primary intent
            intent = data.get("intent", "chat")
            if intent not in self.VALID_INTENTS:
                intent = "chat"

            # Validate task_type
            task_type = data.get("task_type")
            if task_type and task_type not in self.VALID_TASK_TYPES:
                task_type = None

            # Validate book
            book = data.get("book")
            if book and book not in self.VALID_BOOKS:
                book = None

            return IntentResult(
                primary_intent=intent,
                task_type=task_type,
                topic=data.get("topic"),
                is_new_topic=data.get("is_new_topic", False),
                book=book,
            )

        except json.JSONDecodeError:
            logger.warning(f"Failed to parse intent JSON: {raw[:200]}")
            return None

    def _fallback(self, query: str) -> IntentResult:
        """Fallback when LLM detection fails."""
        return IntentResult(primary_intent="chat", topic=None, is_new_topic=False)


__all__ = ["IntentRouter", "IntentResult"]
