
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from src.llm.intent_router import IntentResult
from src.llm.action_planner import ActionPlan
from src.llm.memory import Session


@dataclass
class RequestContext:

    # ── Input ──────────────────────────────────────────────
    query: str                                  # Query gốc từ user
    ui_book: Optional[str] = None               # Book từ UI dropdown
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

    # ── Debug / Trace ──────────────────────────────────────
    request_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    debug_steps: List[Dict[str, Any]] = field(default_factory=list)
    t0: float = field(default_factory=time.time)

    def __post_init__(self):
        if not self.enriched_query:
            self.enriched_query = self.query
        if not self.queries_for_rag:
            self.queries_for_rag = [self.query]

    # ── Convenience methods ────────────────────────────────

    def add_debug_step(self, node: str, **kwargs):
        step = {"node": node, **kwargs}
        self.debug_steps.append(step)

    def resolve_book(self):
        self.effective_book = (
            self.ui_book
            or (self.intent_result.book if self.intent_result else None)
            or (self.session.book if self.session else None)
        )
        # Persist vào session nếu session chưa có book
        if self.effective_book and self.session and not self.session.book:
            self.session.book = self.effective_book

    def to_debug_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "query": self.query,
            "timestamp": self.timestamp,
            "effective_book": self.effective_book,
            "steps": self.debug_steps,
        }

    @property
    def elapsed_time(self) -> float:
        return round(time.time() - self.t0, 2)


__all__ = ["RequestContext"]
