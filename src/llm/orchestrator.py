
import time
import logging
from typing import Generator, Optional, Dict

from src.config.config import settings

# Core pipeline components
from src.llm.intent_router import IntentRouter
from src.llm.action_planner import ActionPlanner, Action
from src.llm.session_manager import SessionManager
from src.llm.session_store import SessionStore
from src.llm.memory import MemoryManager
from src.llm.context_analyzer import ContextAnalyzer
from src.llm.query_rewriter import QueryRewriter

# Handlers (chỉ dùng cho question_handlers dict)
from src.llm.handlers.question.mcq_handler import MCQHandler
from src.llm.handlers.question.essay_handler import EssayHandler
from src.llm.handlers.question.fill_handler import FillHandler
from src.llm.handlers.question.true_false_handler import TrueFalseHandler

# Refactored services
from src.schemas.context import RequestContext
from src.rag.rag_service import RAGService
from src.llm.services.quiz_service import QuizService
from src.llm.services.slide_service import SlideService
from src.llm.execution_dispatcher import ExecutionDispatcher
from src.utils.trace_service import trace_service, logger

from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent


class Orchestrator:

    # Actions that REQUIRE book filter (involve RAG search)
    ACTIONS_REQUIRING_BOOK = {
        Action.GENERATE_QUIZ, Action.GENERATE_SLIDE,
        Action.GENERATE_LESSON_PLAN, Action.EXPLAIN_CONCEPT,
    }

    def __init__(self, retriever, reranker):
        # ── Services ───────────────────────────────────────
        self.rag_service = RAGService(retriever, reranker)

        # ── Pipeline components ────────────────────────────
        self.intent_router = IntentRouter()
        self.context_analyzer = ContextAnalyzer()
        self.query_rewriter = QueryRewriter()
        self.memory = MemoryManager()
        self.session_store = SessionStore(
            storage_path=str(_project_root / "data" / "sessions")
        )
        self.session_manager = SessionManager(
            session_store=self.session_store,
            memory=self.memory,
        )
        self.action_planner = ActionPlanner()

        # ── Question handlers (passed to QuizService) ──────
        question_handlers = {
            "mcq": MCQHandler(),
            "essay": EssayHandler(),
            "fill_blank": FillHandler(),
            "true_false": TrueFalseHandler(),
        }

        # ── Domain services ────────────────────────────────
        self.quiz_service = QuizService(question_handlers, self.rag_service)
        self.slide_service = SlideService(self.rag_service)

        # ── Dispatcher ─────────────────────────────────────
        self.dispatcher = ExecutionDispatcher(
            quiz_service=self.quiz_service,
            slide_service=self.slide_service,
            rag_service=self.rag_service,
        )

        # ── Debug (backward compat cho app_gradio.py) ──────
        self.last_debug_info: Dict = {}

    # ============================================================
    # MAIN ENTRY POINT
    # ============================================================

    def ask(
        self,
        query: str,
        ui_book: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs,
    ) -> Generator[str, None, None]:
        # ① Tạo RequestContext — thay thế toàn bộ global state
        ctx = RequestContext(query=query, ui_book=ui_book, user_id=user_id or "anonymous")

        logger.info("=" * 60)
        logger.info(
            f"QUERY [{ctx.request_id}] (user={ctx.user_id}): '{query[:80]}'"
            if len(query) > 80
            else f"QUERY [{ctx.request_id}] (user={ctx.user_id}): '{query}'"
        )

        # ② Context enrichment + Query Rewriting
        self._enrich_context(ctx)

        # ③ Intent Detection (1 LLM call)
        self._detect_intent(ctx)

        # ④ Session Resolution (pure code)
        self._resolve_session(ctx)

        # Save user message
        ctx.session.add_message("user", query)

        # ⑤ Action Planning (pure code)
        self._plan_action(ctx)

        # ⑥ Book Resolution
        ctx.resolve_book()
        logger.info(f"Book: ui={ui_book}, llm={ctx.intent_result.book if ctx.intent_result else None}, "
                     f"session={ctx.session.book} -> effective={ctx.effective_book}")

        # ⑦ Execute via Dispatcher — Agentic multi-action loop
        response_chunks = []
        for i, plan in enumerate(ctx.action_plans):
            # OBSERVE: Swap context to match current sub-task
            ctx.action_plan = plan
            if i < len(ctx.intent_results):
                ctx.intent_result = ctx.intent_results[i]

            # DECIDE: Check if this action can proceed
            if plan.action in self.ACTIONS_REQUIRING_BOOK and not ctx.effective_book:
                yield from self._handle_no_book(ctx)
                continue  # Skip this action, try next

            # ACT: Insert separator between multi-action outputs
            if i > 0:
                separator = "\n\n---\n\n"
                response_chunks.append(separator)
                yield separator

            for chunk in self.dispatcher.dispatch(plan, ctx):
                response_chunks.append(chunk)
                yield chunk

        # ⑧ Auto-save
        full_response = "".join(response_chunks)
        self.session_store.auto_save(ctx.session)

        # ⑨ Write trace
        self.last_debug_info = ctx.to_debug_dict()
        self.last_debug_info["total_time_s"] = ctx.elapsed_time
        self.last_debug_info["response"] = {
            "length": len(full_response),
            "preview": full_response[:500],
        }
        trace_service.write_trace(ctx, full_response)

        logger.info(f"Total tigit stame: {ctx.elapsed_time}s")
        logger.info("=" * 60)

    # ============================================================
    # PIPELINE STAGES (thin wrappers)
    # ============================================================

    def _enrich_context(self, ctx: RequestContext):
        current_session = self.memory.get_current_session(ctx.user_id)
        history_text = ""
        if current_session:
            history_text = "\n".join(
                f"{m.role}: {m.content}" for m in current_session.messages[-5:]
            )

        if history_text and self.context_analyzer.needs_contextualization(ctx.query, history_text):
            context_snippet = self.context_analyzer.extract_context_from_history(ctx.query, history_text)
            ctx.enriched_query = f"Ngu canh truoc do:\n{context_snippet}\n\nCau hoi hien tai: {ctx.query}"
            ctx.context_enriched = True
            logger.info("ContextAnalyzer: enriched query with history")

            # Query Rewriting
            t_rw = time.time()
            rewritten = self.query_rewriter.rewrite(ctx.query, context_snippet)
            rw_time = time.time() - t_rw

            if rewritten and len(rewritten) > 0:
                ctx.queries_for_rag = rewritten
                logger.info(f"QueryRewriter ({rw_time:.2f}s): {len(rewritten)} queries → {rewritten}")
                ctx.rewrite_info = {
                    "rewritten_queries": rewritten,
                    "time_s": round(rw_time, 2),
                }

        ctx.add_debug_step(
            "ContextAnalyzer",
            enriched=ctx.context_enriched,
            rewrite=ctx.rewrite_info,
        )

    def _detect_intent(self, ctx: RequestContext):
        current_session = self.memory.get_current_session(ctx.user_id)
        current_topic = current_session.topic if current_session else None
        session_messages = current_session.get_context_messages() if current_session else None

        t1 = time.time()
        intent_results = self.intent_router.detect_multi(
            query=ctx.enriched_query,
            current_topic=current_topic,
            session_messages=session_messages,
        )
        intent_time = time.time() - t1

        # Populate both list and singular field (backward-compat)
        ctx.intent_results = intent_results
        ctx.intent_result = intent_results[0] if intent_results else None

        logger.info(
            f"IntentRouter ({intent_time:.2f}s): "
            f"{len(intent_results)} intent(s) — "
            + ", ".join(
                f"{r.primary_intent}({r.task_type or '-'})" for r in intent_results
            )
        )

        ctx.add_debug_step(
            "IntentRouter",
            total_intents=len(intent_results),
            intents=[
                {
                    "intent": r.primary_intent,
                    "task_type": r.task_type,
                    "topic": r.topic,
                    "is_new_topic": r.is_new_topic,
                    "book": r.book,
                }
                for r in intent_results
            ],
            time_s=round(intent_time, 2),
        )

    def _resolve_session(self, ctx: RequestContext):
        session = self.session_manager.resolve_session(ctx.intent_result, user_id=ctx.user_id)
        ctx.session = session
        logger.info(
            f"Session: id={session.session_id}, user={session.user_id}, topic='{session.topic}', msgs={len(session.messages)}"
        )

        ctx.add_debug_step(
            "SessionManager",
            session_id=session.session_id,
            user_id=session.user_id,
            topic=session.topic,
            intent=session.intent,
            book=session.book,
            total_messages=len(session.messages),
            has_quiz_state=session.quiz_state is not None,
            has_slide_state=session.slide_state is not None,
        )

    def _plan_action(self, ctx: RequestContext):
        action_plans = self.action_planner.plan_all(
            ctx.intent_results, ctx.session, ctx.query
        )

        # Populate both list and singular field (backward-compat)
        ctx.action_plans = action_plans
        ctx.action_plan = action_plans[0] if action_plans else None

        logger.info(
            f"ActionPlanner: {len(action_plans)} plan(s) — "
            + ", ".join(f"{p.action.value}" for p in action_plans)
        )

        ctx.add_debug_step(
            "ActionPlanner",
            total_plans=len(action_plans),
            plans=[
                {
                    "action": p.action.value,
                    "reason": p.reason,
                    "round_id": p.round_id,
                }
                for p in action_plans
            ],
        )

    def _handle_no_book(self, ctx: RequestContext) -> Generator[str, None, None]:
        msg = (
            "📚 Hệ thống hỗ trợ 2 bộ sách SGK Tin học THPT:\n"
            "- **Cánh Diều** (CD)\n"
            "- **Kết Nối Tri Thức** (KNTT)\n\n"
            "Vui lòng cho mình biết bạn đang học theo bộ sách nào "
            "để mình tra cứu chính xác nhất nhé! 🎯"
        )
        ctx.session.add_message("assistant", msg)
        ctx.add_debug_step(
            "BookFilter",
            status="blocked",
            reason="No book specified for RAG-dependent action",
            action=ctx.action_plan.action.value,
        )
        yield msg

        # Write trace for this early return
        self.last_debug_info = ctx.to_debug_dict()
        self.last_debug_info["total_time_s"] = ctx.elapsed_time
        trace_service.write_trace(ctx, msg)


__all__ = ["Orchestrator"]
