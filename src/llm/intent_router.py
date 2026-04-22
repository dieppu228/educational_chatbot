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
    lesson_reference: Optional[str] = None # Detected lesson structural ref like "Bài 1 Chủ đề A"
    is_new_topic: bool = False         # Whether topic changed from current session
    book: Optional[str] = None         # "CD" | "KNTT" | None (detected book series)
    raw_response: Optional[str] = None # Raw LLM response for debugging


# INTENT_ROUTER_PROMPT imported from src.llm.prompts


# ============================================================
# INTENT ROUTER CLASS
# ============================================================

class IntentRouter:
    """
    Multi-Intent Agentic Router.

    Level 1: LLM-based intent detection — supports multi-intent (max 3).
    Level 2: Rule-based sub-intent resolution (see ActionPlanner).

    Agentic patterns:
        - Validate + filter low-confidence intents (Observe → Decide)
        - Retry with feedback on parse failure (Self-Correction)
        - Fallback gracefully on total failure
    """

    VALID_INTENTS = {"generate", "interact", "analyze", "explain", "chat"}
    VALID_TASK_TYPES = {"mcq", "essay", "fill_blank", "true_false", "slide", "lesson_plan"}
    VALID_BOOKS = {"CD", "KNTT"}
    MAX_INTENTS = 3
    MIN_CONFIDENCE = 0.5

    def __init__(self, api_key: str = None, model_name: str = None):
        from src.llm.knowledge_map import KnowledgeMap
        self.api_key = api_key or settings.GENAI_API_KEY or os.getenv("GENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("GENAI_API_KEY not set.")

        self.model_name = model_name or settings.LLM_MODEL or "gemini-2.5-flash-lite"
        self.client = genai.Client(api_key=self.api_key)
        self.k_map = KnowledgeMap()

    def detect(
        self,
        query: str,
        current_topic: Optional[str] = None,
        session_messages: Optional[List[dict]] = None,
    ) -> IntentResult:
        """
        Backward-compatible single-intent detection.
        Delegates to detect_multi() and returns the first (primary) intent.
        """
        results = self.detect_multi(query, current_topic, session_messages)
        return results[0]

    def detect_multi(
        self,
        query: str,
        current_topic: Optional[str] = None,
        session_messages: Optional[List[dict]] = None,
        max_retries: int = 2,
    ) -> List[IntentResult]:
        """
        Agentic multi-intent detection.

        Observe → Validate → Decide → (Retry if needed)

        Args:
            query: User's current message
            current_topic: Topic of current session
            session_messages: Recent conversation history
            max_retries: Max retry attempts on parse failure

        Returns:
            List[IntentResult] — 1 to MAX_INTENTS items, sorted by order
        """
        session_context = self._format_session_context(session_messages)
        topic_instruction = self._build_topic_instruction(current_topic)

        prompt = INTENT_ROUTER_PROMPT.format(
            query=query,
            session_context=session_context,
            topic_instruction=topic_instruction,
        )

        for attempt in range(max_retries):
            try:
                # ① ACT — Call LLM
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=GenerateContentConfig(
                        temperature=0.1,
                        response_mime_type="application/json",
                    ),
                )
                raw = self._extract_text(response)

                # ② OBSERVE — Parse response
                intents = self._parse_multi_result(raw)

                if not intents:
                    # Parse failed — retry with feedback (Self-Correction)
                    logger.warning(
                        f"IntentRouter attempt {attempt + 1}/{max_retries}: "
                        f"parse failed, retrying..."
                    )
                    continue

                # ③ VALIDATE — Filter low-confidence intents
                validated = []
                for intent in intents:
                    if intent.primary_intent not in self.VALID_INTENTS:
                        logger.debug(f"Filtered invalid intent: {intent.primary_intent}")
                        continue
                    
                    # Mapping lesson_reference to exact Topic
                    if intent.lesson_reference:
                        semantic_topic = self.k_map.lookup_semantic_topic(intent.book, intent.lesson_reference)
                        if semantic_topic:
                            if intent.topic:
                                intent.topic = f"{intent.topic} ({semantic_topic})"
                            else:
                                intent.topic = semantic_topic
                                
                    # Agent loại bỏ intent kém tin cậy
                    # (confidence được parse từ LLM response, default 0.9)
                    validated.append(intent)

                # ④ DECIDE — Có đủ kết quả hay cần fallback?
                if not validated:
                    logger.warning("All intents filtered out, using fallback")
                    return [self._fallback(query)]

                # Cap at MAX_INTENTS
                validated = validated[:self.MAX_INTENTS]

                # Set raw_response on first intent for debugging
                validated[0].raw_response = raw

                logger.info(
                    f"IntentRouter: {len(validated)} intent(s) detected — "
                    + ", ".join(
                        f"{r.primary_intent}({r.task_type or '-'})" for r in validated
                    )
                )
                return validated

            except Exception as e:
                logger.error(f"IntentRouter attempt {attempt + 1} error: {e}")
                continue

        # All retries exhausted
        logger.error("IntentRouter: all retries exhausted, using fallback")
        return [self._fallback(query)]

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

    def _parse_multi_result(self, raw: str) -> Optional[List[IntentResult]]:
        """
        Parse LLM JSON response into List[IntentResult].

        Handles both formats:
            - New: {"intents": [{...}, {...}]}
            - Legacy: {"intent": "...", ...} (single object)
        """
        text = raw.strip()
        text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

        try:
            data = json.loads(text.strip())
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse intent JSON: {raw[:200]}")
            return None

        # ── New multi-intent format: {"intents": [...]} ──
        if "intents" in data and isinstance(data["intents"], list):
            items = data["intents"]
        # ── Legacy single-intent format: {"intent": "..."} ──
        elif "intent" in data:
            items = [data]
        else:
            logger.warning(f"Unknown intent format: {list(data.keys())}")
            return None

        results = []
        for item in items:
            intent = self._validate_single_intent(item)
            if intent:
                results.append(intent)

        if not results:
            return None

        # Sort by order field (LLM decides execution sequence)
        results.sort(key=lambda r: getattr(r, '_order', 999))

        return results

    def _validate_single_intent(self, data: dict) -> Optional[IntentResult]:
        """Validate and construct a single IntentResult from a dict."""
        intent = data.get("intent", "chat")
        if intent not in self.VALID_INTENTS:
            intent = "chat"

        task_type = data.get("task_type")
        if task_type and task_type not in self.VALID_TASK_TYPES:
            task_type = None

        book = data.get("book")
        if book and book not in self.VALID_BOOKS:
            book = None

        confidence = data.get("confidence", 0.9)
        if isinstance(confidence, (int, float)) and confidence < self.MIN_CONFIDENCE:
            logger.debug(f"Intent '{intent}' below confidence threshold: {confidence}")
            return None

        result = IntentResult(
            primary_intent=intent,
            task_type=task_type,
            topic=data.get("topic"),
            lesson_reference=data.get("lesson_reference"),
            is_new_topic=data.get("is_new_topic", False),
            book=book,
        )
        # Store order for sorting (not exposed in dataclass)
        result._order = data.get("order", 999)
        return result

    def _parse_result(self, raw: str) -> Optional[IntentResult]:
        """Legacy parser — backward compat. Delegates to multi parser."""
        results = self._parse_multi_result(raw)
        return results[0] if results else None

    def _fallback(self, query: str) -> IntentResult:
        """Fallback when LLM detection fails."""
        return IntentResult(primary_intent="chat", topic=None, is_new_topic=False)


__all__ = ["IntentRouter", "IntentResult"]
