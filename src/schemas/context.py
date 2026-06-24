
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
    hitl_type: Optional[str] = None             # Structured HITL action type from UI
    hitl_approved: Optional[bool] = None        # True approve, False submit edited payload
    edited_outline: Optional[Dict[str, Any]] = None

    # ── Enrichment (ContextAnalyzer) ───────────────────────
    enriched_query: str = ""                    # Query đã bổ sung context
    queries_for_rag: List[str] = field(default_factory=list)
    context_enriched: bool = False
    rewrite_info: Optional[Dict] = None
    extracted_params: Dict[str, Any] = field(default_factory=dict)

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
    scope_source: str = "none"
    scope_is_soft: bool = False
    scope_fallback_used: bool = False
    scope_book_source: Optional[str] = None
    scope_grade_source: Optional[str] = None
    requested_scope: Dict[str, Optional[str]] = field(default_factory=dict)
    actual_scope: Dict[str, Optional[str]] = field(default_factory=dict)
    scope_fallback_notice: Optional[str] = None

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
        param_book = self.extracted_params.get("book")
        session_book = self.session.book if self.session else None
        self.effective_book = (
            query_book
            or intent_book
            or param_book
            or self.ui_book
            or session_book
        )
        self.scope_book_source = self._first_scope_source(
            ("query", query_book),
            ("intent", intent_book),
            ("param", param_book),
            ("ui", self.ui_book),
            ("session", session_book),
        )
        # Persist explicit query/router book for follow-up turns.
        if (
            self.effective_book
            and self.session
            and (query_book or intent_book or param_book or self.ui_book or not self.session.book)
        ):
            self.session.book = self.effective_book
        self._refresh_scope_metadata()

    def resolve_grade(self):
        query_grade = self._extract_grade(self.query)
        intent_grade = self._extract_grade(self.intent_result.topic) if self.intent_result else None
        param_grade = self.extracted_params.get("grade")
        rewrite_grade = self._extract_grade_from_texts(
            [self.enriched_query, *self.queries_for_rag]
        )
        session_grade = self.session.metadata.get("grade") if self.session else None
        self.effective_grade = (
            query_grade
            or intent_grade
            or param_grade
            or rewrite_grade
            or self.ui_grade
            or session_grade
        )
        self.scope_grade_source = self._first_scope_source(
            ("query", query_grade),
            ("intent", intent_grade),
            ("param", param_grade),
            ("rewrite", rewrite_grade),
            ("ui", self.ui_grade),
            ("session", session_grade),
        )
        if (
            self.effective_grade
            and self.session
            and (query_grade or intent_grade or param_grade or rewrite_grade or self.ui_grade or not session_grade)
        ):
            self.session.metadata["grade"] = self.effective_grade
        self._refresh_scope_metadata()

    @staticmethod
    def _first_scope_source(*candidates) -> Optional[str]:
        for source, value in candidates:
            if value:
                return source
        return None

    def _refresh_scope_metadata(self):
        sources = {s for s in (self.scope_book_source, self.scope_grade_source) if s}
        if not sources:
            self.scope_source = "none"
        elif len(sources) == 1:
            self.scope_source = next(iter(sources))
        else:
            self.scope_source = "mixed"

        has_hard_scope = bool(sources.intersection({"query", "intent", "param"}))
        self.scope_is_soft = not has_hard_scope and "ui" in sources
        self.requested_scope = {
            "book": self.effective_book,
            "grade": self.effective_grade,
            "source": self.scope_source,
        }

    @staticmethod
    def _extract_grade(text: Optional[str]) -> Optional[str]:
        if not text:
            return None
        text_lower = text.lower()
        match = re.search(r'(?:lớp|lop|tin(?:\s*học)?|grade)\s*(10|11|12)', text_lower)
        if match:
            return match.group(1)
        return None

    @classmethod
    def _extract_grade_from_texts(cls, texts: List[Optional[str]]) -> Optional[str]:
        for text in texts:
            grade = cls._extract_grade(text)
            if grade:
                return grade
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
            "scope_source": self.scope_source,
            "scope_is_soft": self.scope_is_soft,
            "scope_fallback_used": self.scope_fallback_used,
            "requested_scope": self.requested_scope,
            "actual_scope": self.actual_scope,
            "extracted_params": self.extracted_params,
            "steps": self.debug_steps,
        }

    @property
    def elapsed_time(self) -> float:
        return round(time.time() - self.t0, 2)


__all__ = ["RequestContext"]
