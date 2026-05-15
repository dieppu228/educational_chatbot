
import time
import uuid
import json
import logging
import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from src.llm.intent_router import IntentResult
from src.llm.action_planner import ActionPlan
from src.llm.memory import Session

logger = logging.getLogger("chatbot.node")


@dataclass
class RequestContext:

    # ── Input ──────────────────────────────────────────────
    query: str                                  # Query gốc từ user
    ui_book: Optional[str] = None               # Book từ UI dropdown
    ui_grade: Optional[str] = None              # Grade từ UI dropdown
    user_id: str = "anonymous"                 # User identity from client/UI

    # ── Enrichment (ContextAnalyzer) ───────────────────────
    enriched_query: str = ""                    # Query đã bổ sung context
    queries_for_rag: List[str] = field(default_factory=list)
    context_enriched: bool = False
    rewrite_info: Optional[Dict] = None

    # ── Intent (IntentRouter) ──────────────────────────────
    intent_result: Optional[IntentResult] = None          # Intent chính (= intent_results[0]), backward-compat
    intent_results: List[IntentResult] = field(default_factory=list)  # Multi-intent list (max 3)

    # ── Session (SessionManager) ───────────────────────────
    session: Optional[Session] = None

    # ── Action (ActionPlanner) ─────────────────────────────
    action_plan: Optional[ActionPlan] = None              # Plan chính (= action_plans[0]), backward-compat
    action_plans: List[ActionPlan] = field(default_factory=list)      # Multi-action list

    # ── Book Resolution ────────────────────────────────────
    effective_book: Optional[str] = None
    effective_grade: Optional[str] = None

    # ── Debug / Trace ──────────────────────────────────────
    request_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    debug_steps: List[Dict[str, Any]] = field(default_factory=list)
    t0: float = field(default_factory=time.time)
    auto_approve_outline: bool = False
    graph_debug_stream: bool = True

    def __post_init__(self):
        if not self.enriched_query:
            self.enriched_query = self.query
        if not self.queries_for_rag:
            self.queries_for_rag = [self.query]

    # ── Convenience methods ────────────────────────────────

    def add_debug_step(self, node: str, **kwargs):
        step = {"node": node, **kwargs}
        self.debug_steps.append(step)
        logger.info(
            "[%s] %s | %s",
            self.request_id,
            node,
            self._summarize_debug_step(kwargs),
        )

    @staticmethod
    def _summarize_debug_step(step: Dict[str, Any]) -> str:
        compact = {}
        for key, value in step.items():
            if isinstance(value, (str, int, float, bool)) or value is None:
                compact[key] = value
            elif isinstance(value, list):
                compact[key] = f"List[{len(value)}]"
            elif isinstance(value, dict):
                compact[key] = f"Dict[{len(value)} keys]"
            else:
                compact[key] = value.__class__.__name__

        text = json.dumps(compact, ensure_ascii=False, default=str)
        return text[:1200] + "..." if len(text) > 1200 else text

    def resolve_book(self):
        query_book = self._extract_book(self.query)
        intent_book = self.intent_result.book if self.intent_result else None
        self.effective_book = (
            query_book
            or intent_book
            or self.ui_book
            or (self.session.book if self.session else None)
        )
        # Persist explicit query/router book for follow-up turns.
        if self.effective_book and self.session and (query_book or intent_book or self.ui_book or not self.session.book):
            self.session.book = self.effective_book

    def resolve_grade(self):
        query_grade = self._extract_grade(self.query)
        intent_grade = self._extract_grade(self.intent_result.topic) if self.intent_result else None
        session_grade = self.session.metadata.get("grade") if self.session else None
        self.effective_grade = query_grade or intent_grade or self.ui_grade or session_grade
        if self.effective_grade and self.session and (query_grade or intent_grade or self.ui_grade or not session_grade):
            self.session.metadata["grade"] = self.effective_grade

    @staticmethod
    def _extract_grade(text: Optional[str]) -> Optional[str]:
        if not text:
            return None
        text_lower = text.lower()
        match = re.search(r'(?:lớp|lop|tin|grade)\s*(10|11|12)', text_lower)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def _extract_book(text: Optional[str]) -> Optional[str]:
        if not text:
            return None
        text_lower = text.lower()
        if re.search(r'\b(kntt|kết\s*nối\s*tri\s*thức|ket\s*noi\s*tri\s*thuc)\b', text_lower):
            return "KNTT"
        if re.search(r'\b(cd|cánh\s*diều|canh\s*dieu)\b', text_lower):
            return "CD"
        return None

    def to_debug_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "query": self.query,
            "timestamp": self.timestamp,
            "effective_book": self.effective_book,
            "effective_grade": self.effective_grade,
            "steps": self.debug_steps,
        }

    @property
    def elapsed_time(self) -> float:
        return round(time.time() - self.t0, 2)


__all__ = ["RequestContext"]
