import time
import asyncio
import logging
import re
import threading
from typing import Generator, Optional, Dict, AsyncGenerator

from src.config.config import project_path, settings

# Core pipeline components
from src.llm.intent_router import IntentRouter
from src.llm.action_planner import (
    ActionPlanner,
    Action,
    has_assessment_context,
    is_assessment_followup_message,
)
from src.llm.session_manager import SessionManager
from src.llm.session_store import SessionStore
from src.llm.memory import MemoryManager
from src.llm.context_analyzer import ContextAnalyzer
from src.llm.query_rewriter import QueryRewriter
from src.llm.param_extractor import ParamExtractor

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


class Orchestrator:

    # Actions that REQUIRE book filter (involve RAG search)
    ACTIONS_REQUIRING_BOOK = {
        Action.GENERATE_QUIZ, Action.GENERATE_SLIDE,
        Action.GENERATE_LESSON_PLAN, Action.EXPLAIN_CONCEPT,
    }

    def __init__(self, retriever, reranker):
        # ── Services ───────────────────────────────────────
        self.rag_service = RAGService(retriever, reranker)

        # ── MCP tool layer (in-process) ────────────────────
        from src.tools.bootstrap import init_tool_layer
        init_tool_layer(rag_service=self.rag_service)

        # ── Pipeline components ────────────────────────────
        self.intent_router = IntentRouter()
        self.context_analyzer = ContextAnalyzer()
        self.query_rewriter = QueryRewriter()
        self.param_extractor = ParamExtractor()
        self.memory = MemoryManager()
        self.session_store = SessionStore(
            storage_path=str(project_path(settings.SESSION_STORAGE_DIR))
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

        # ── Debug info per user/session ────────────────────
        self.last_debug_info: Dict = {}
        self._debug_info_by_user: Dict[str, Dict] = {}
        self._debug_lock = threading.RLock()

    def get_debug_info(self, user_id: Optional[str] = None) -> Dict:
        uid = user_id or "anonymous"
        with self._debug_lock:
            return dict(self._debug_info_by_user.get(uid) or self.last_debug_info)

    def get_pending_hitl(self, user_id: Optional[str] = None) -> Optional[Dict]:
        session = self.memory.get_current_session(user_id or "anonymous")
        if not session:
            return None
        return self.slide_service.get_pending_hitl(session)

    def get_last_export(self, user_id: Optional[str] = None) -> Optional[Dict]:
        session = self.memory.get_current_session(user_id or "anonymous")
        if not session or not session.slide_state or not session.slide_state.slide_output:
            return None
        export = session.slide_state.slide_output.get("export")
        return export if isinstance(export, dict) else None

    def _set_debug_info(self, ctx: RequestContext, full_response: str):
        debug_info = ctx.to_debug_dict()
        debug_info["total_time_s"] = ctx.elapsed_time
        debug_info["response"] = {
            "length": len(full_response),
            "preview": full_response[:500],
        }
        with self._debug_lock:
            self.last_debug_info = debug_info
            self._debug_info_by_user[ctx.user_id] = debug_info

    # ============================================================
    # MAIN ENTRY POINT (sync)
    # ============================================================

    def ask(
        self,
        query: str,
        ui_book: Optional[str] = None,
        ui_grade: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs,
    ) -> Generator[str, None, None]:
        # Run async pipeline in sync context for backward compatibility
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            gen = self.ask_async(query, ui_book=ui_book, ui_grade=ui_grade, user_id=user_id, **kwargs)
            while True:
                try:
                    chunk = loop.run_until_complete(gen.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        finally:
            loop.close()

    # ============================================================
    # ASYNC ENTRY POINT
    # ============================================================

    async def ask_async(
        self,
        query: str,
        ui_book: Optional[str] = None,
        ui_grade: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        # ① Tạo RequestContext — thay thế toàn bộ global state
        ctx = RequestContext(
            query=query,
            ui_book=ui_book,
            ui_grade=ui_grade,
            user_id=user_id or "anonymous",
            hitl_type=kwargs.get("hitl_type"),
            hitl_approved=kwargs.get("hitl_approved"),
            edited_outline=kwargs.get("edited_outline"),
        )
        ctx.auto_approve_outline = bool(kwargs.get("auto_approve_outline", False))
        ctx.graph_debug_stream = bool(kwargs.get("graph_debug_stream", True))

        logger.info("=" * 60)
        logger.info(
            f"QUERY [{ctx.request_id}] (user={ctx.user_id}): '{query[:80]}'"
            if len(query) > 80
            else f"QUERY [{ctx.request_id}] (user={ctx.user_id}): '{query}'"
        )

        hitl_response_chunks = await self._resume_hitl_if_waiting_async(ctx)
        if hitl_response_chunks is not None:
            for chunk in hitl_response_chunks:
                yield chunk
            return
        if ctx.hitl_type:
            msg = "Không có pipeline nào đang chờ duyệt dàn ý."
            ctx.add_debug_step("HITLResume", status="not_waiting", hitl_type=ctx.hitl_type)
            self._set_debug_info(ctx, msg)
            yield msg
            return

        self._prepare_history_context(ctx)

        # ② Context enrichment + Query Rewriting (async)
        await self._enrich_context_async(ctx)

        # ③ Shared parameter extraction (LLM + deterministic fallback)
        await self._extract_params_async(ctx)

        # ④ Intent Detection (LLM call - async)
        await self._detect_intent_async(ctx)

        # Keep active quiz/slide exercise sessions for terse follow-ups like
        # "câu 1 A" or "cho tôi đáp án", even if the router guesses a new topic.
        self._preserve_active_assessment_session(ctx)

        # ⑤ Session Resolution (pure code)
        self._resolve_session(ctx)

        # Save user message
        ctx.session.add_message("user", query)

        # ⑥ Action Planning (pure code)
        self._plan_action(ctx)

        # ⑦ Book Resolution
        ctx.resolve_book()
        ctx.resolve_grade()
        self._normalize_intents_for_scope(ctx)
        logger.info(f"Book: ui={ui_book}, llm={ctx.intent_result.book if ctx.intent_result else None}, "
                     f"session={ctx.session.book} -> effective={ctx.effective_book}")
        logger.info(f"Grade: ui={ui_grade} -> effective={ctx.effective_grade}")
        ctx.add_debug_step(
            "ScopeResolver",
            ui_book=ui_book,
            llm_book=ctx.intent_result.book if ctx.intent_result else None,
            effective_book=ctx.effective_book,
            ui_grade=ui_grade,
            effective_grade=ctx.effective_grade,
            scope_source=ctx.scope_source,
            scope_is_soft=ctx.scope_is_soft,
            requested_scope=ctx.requested_scope,
        )

        # ⑧ Execute via Dispatcher — Agentic multi-action loop
        response_chunks = []
        scope_notice = self._build_scope_override_notice(ctx)
        if scope_notice:
            response_chunks.append(scope_notice)
            yield scope_notice

        for i, plan in enumerate(ctx.action_plans):
            # OBSERVE: Swap context to match current sub-task
            ctx.action_plan = plan
            if i < len(ctx.intent_results):
                ctx.intent_result = ctx.intent_results[i]
                ctx.resolve_book()
                ctx.resolve_grade()
                self._normalize_intents_for_scope(ctx)

            # DECIDE: Check if this action can proceed
            if plan.action in self.ACTIONS_REQUIRING_BOOK and not ctx.effective_book:
                async for chunk in self._handle_no_book_async(ctx):
                    response_chunks.append(chunk)
                    yield chunk
                continue  # Skip this action, try next

            # ACT: Insert separator between multi-action outputs
            if i > 0:
                separator = "\n\n---\n\n"
                response_chunks.append(separator)
                yield separator

            async for chunk in self.dispatcher.dispatch_async(plan, ctx):
                response_chunks.append(chunk)
                yield chunk

        # ⑧ Auto-save (async)
        full_response = "".join(response_chunks)
        await self.session_store.auto_save_async(ctx.session)

        # ⑨ Write trace
        self._set_debug_info(ctx, full_response)
        trace_service.write_trace(ctx, full_response)

        logger.info(f"Total tigit stame: {ctx.elapsed_time}s")
        logger.info("=" * 60)

    def _build_scope_override_notice(self, ctx: RequestContext) -> Optional[str]:
        query_book = RequestContext._extract_book(ctx.query)
        intent_book = ctx.intent_result.book if ctx.intent_result else None
        param_book = ctx.extracted_params.get("book")
        query_grade = RequestContext._extract_grade(ctx.query)
        intent_grade = RequestContext._extract_grade(ctx.intent_result.topic) if ctx.intent_result else None
        param_grade = ctx.extracted_params.get("grade")

        explicit_book = query_book or intent_book or param_book
        explicit_grade = query_grade or intent_grade or param_grade
        overrides = []

        if ctx.ui_book and explicit_book and explicit_book != ctx.ui_book:
            overrides.append(f"bộ sách {self._book_label(explicit_book)}")
        if ctx.ui_grade and explicit_grade and explicit_grade != ctx.ui_grade:
            overrides.append(f"lớp {explicit_grade}")

        if not overrides:
            return None

        return (
            "Mình sẽ dùng " + ", ".join(overrides) +
            " theo nội dung câu hỏi của bạn.\n\n"
        )

    def _normalize_intents_for_scope(self, ctx: RequestContext) -> None:
        before = [
            {
                "topic": intent.topic,
                "lesson_reference": intent.lesson_reference,
                "book": intent.book,
            }
            for intent in ctx.intent_results
        ]
        self.intent_router.normalize_intents_for_scope(
            ctx.intent_results,
            book_hint=ctx.effective_book,
            grade_hint=ctx.effective_grade,
        )
        after = [
            {
                "topic": intent.topic,
                "lesson_reference": intent.lesson_reference,
                "book": intent.book,
            }
            for intent in ctx.intent_results
        ]
        if ctx.intent_results:
            ctx.intent_result = ctx.intent_results[0]
        if ctx.session and ctx.intent_result and ctx.intent_result.topic:
            ctx.session.topic = ctx.intent_result.topic
        if before != after:
            ctx.add_debug_step(
                "CatalogResolver",
                effective_book=ctx.effective_book,
                effective_grade=ctx.effective_grade,
                before=before,
                after=after,
            )

    def _preserve_active_assessment_session(self, ctx: RequestContext) -> None:
        current_session = self.memory.get_current_session(ctx.user_id)
        if not has_assessment_context(current_session):
            return
        followup_intents = {"interact", "chat", "explain", "analyze"}
        if not any(intent.primary_intent in followup_intents for intent in ctx.intent_results):
            return
        if not is_assessment_followup_message(ctx.query.lower()):
            return

        changed = False
        for intent in ctx.intent_results:
            if intent.is_new_topic:
                intent.is_new_topic = False
                changed = True
            if intent.primary_intent == "chat":
                intent.primary_intent = "interact"
                changed = True

        if ctx.intent_results:
            ctx.intent_result = ctx.intent_results[0]

        if changed:
            ctx.add_debug_step(
                "SessionGuard",
                status="preserved_assessment_session",
                reason="assessment_followup",
                session_id=current_session.session_id,
                has_quiz_state=current_session.quiz_state is not None,
                has_slide_state=current_session.slide_state is not None,
            )

    @staticmethod
    def _book_label(book: str) -> str:
        return {"CD": "Cánh Diều", "KNTT": "Kết Nối Tri Thức"}.get(book, book)

    async def _resume_hitl_if_waiting_async(self, ctx: RequestContext) -> Optional[list[str]]:
        current_session = self.memory.get_current_session(ctx.user_id)
        if not current_session or not self.slide_service.is_waiting_hitl(current_session):
            return None

        ctx.session = current_session
        ctx.resolve_book()
        ctx.resolve_grade()
        ctx.session.add_message("user", ctx.query)
        ctx.add_debug_step(
            "HITLResume",
            status="resuming",
            session_id=current_session.session_id,
            feedback=ctx.query,
            hitl_type=ctx.hitl_type,
            hitl_approved=ctx.hitl_approved,
        )

        response_chunks = await asyncio.to_thread(
            lambda: list(self.slide_service.resume_outline(
                ctx,
                ctx.query,
                hitl_type=ctx.hitl_type,
                hitl_approved=ctx.hitl_approved,
                edited_outline=ctx.edited_outline,
            ))
        )
        full_response = "".join(response_chunks)
        await self.session_store.auto_save_async(ctx.session)
        self._set_debug_info(ctx, full_response)
        trace_service.write_trace(ctx, full_response)
        logger.info("HITL resume complete: %s", ctx.elapsed_time)
        return response_chunks

    # ============================================================
    # PIPELINE STAGES (async versions)
    # ============================================================

    def _prepare_history_context(self, ctx: RequestContext) -> None:
        current_session = self.memory.get_current_session(ctx.user_id)
        if not current_session or not current_session.messages:
            ctx.history_context = ""
            ctx.history_mode = "none"
            ctx.history_reason = "no_current_history"
            ctx.add_debug_step(
                "HistoryPolicy",
                mode=ctx.history_mode,
                reason=ctx.history_reason,
                messages_used=0,
            )
            return

        history_text = self._format_history_messages(current_session.messages[-5:])
        if is_assessment_followup_message(ctx.query.lower()) and has_assessment_context(current_session):
            ctx.history_context = history_text
            ctx.history_mode = "same_topic"
            ctx.history_reason = "assessment_followup"
        elif self._should_reset_history_for_topic(ctx.query, current_session.topic, history_text):
            ctx.history_context = ""
            ctx.history_mode = "reset"
            ctx.history_reason = "topic_changed"
        else:
            ctx.history_context = history_text
            ctx.history_mode = "same_topic"
            ctx.history_reason = "same_or_ambiguous_topic"

        ctx.add_debug_step(
            "HistoryPolicy",
            mode=ctx.history_mode,
            reason=ctx.history_reason,
            current_topic=current_session.topic,
            messages_used=len(current_session.messages[-5:]) if ctx.history_context else 0,
        )

    @staticmethod
    def _format_history_messages(messages) -> str:
        return "\n".join(f"{m.role}: {m.content}" for m in messages)

    def _should_reset_history_for_topic(self, query: str, current_topic: str, history_text: str) -> bool:
        if not current_topic:
            return self._looks_like_explicit_generate(query)
        if self._has_contextual_reference(query, history_text):
            return False
        if self._topic_has_overlap(query, current_topic):
            return False
        if self._looks_like_explicit_generate(query):
            return True
        return len(self._content_keywords(query)) >= 2

    def _has_contextual_reference(self, query: str, history_text: str) -> bool:
        text = query.lower()
        if self.context_analyzer.needs_contextualization(query, history_text):
            return True
        patterns = [
            r"\bcâu\s*\d+\b", r"\bcau\s*\d+\b",
            r"\b(?:bài|bai|chủ\s*đề|chu\s*de|nội\s*dung|noi\s*dung)\s*(?:này|nay|đó|do)\b",
            r"\b(?:cái|cai|phần|phan)\s*(?:này|nay|đó|do)\b",
            r"\b(?:vừa|vua|trên|tren|tiếp|tiep|thêm|them|nữa|nua|lại|lai)\b",
            r"\b(?:đáp\s*án|dap\s*an|giải\s*thích\s*câu|giai\s*thich\s*cau)\b",
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)

    @staticmethod
    def _looks_like_explicit_generate(query: str) -> bool:
        text = query.lower()
        return bool(
            re.search(r"\b(?:sinh|tạo|tao|soạn|soan|thiết\s*kế|thiet\s*ke|lập|lap)\b", text)
            and re.search(
                r"\b(?:slide|bài\s*giảng|bai\s*giang|giáo\s*án|giao\s*an|quiz|bài\s*tập|bai\s*tap|câu\s*hỏi|cau\s*hoi|trắc\s*nghiệm|trac\s*nghiem|tự\s*luận|tu\s*luan)\b",
                text,
            )
        )

    @classmethod
    def _topic_has_overlap(cls, query: str, current_topic: str) -> bool:
        query_keywords = cls._content_keywords(query)
        topic_keywords = cls._content_keywords(current_topic)
        return bool(query_keywords and topic_keywords and query_keywords.intersection(topic_keywords))

    @staticmethod
    def _content_keywords(text: str) -> set[str]:
        stopwords = {
            "sinh", "tao", "tạo", "soan", "soạn", "thiet", "thiết", "ke", "kế",
            "slide", "bai", "bài", "giang", "giảng", "giao", "giáo", "an", "án",
            "quiz", "tap", "tập", "cau", "câu", "hoi", "hỏi", "trac", "trắc",
            "nghiem", "nghiệm", "tu", "tự", "luan", "luận", "ve", "về", "cho",
            "toi", "tôi", "minh", "mình", "hay", "hãy", "lop", "lớp", "bo", "bộ",
            "sach", "sách", "tin", "học", "hoc", "may", "máy", "tinh", "tính",
            "cd", "kntt", "canh", "cánh", "dieu", "diều", "ket", "kết", "noi", "nối",
            "tri", "thuc", "thức", "la", "là", "gi", "gì", "va", "và", "cua", "của",
        }
        tokens = set(re.findall(r"\w{2,}", text.lower(), flags=re.UNICODE))
        return {token for token in tokens if token not in stopwords}

    async def _enrich_context_async(self, ctx: RequestContext):
        history_text = ctx.history_context

        if history_text and self.context_analyzer.needs_contextualization(ctx.query, history_text):
            context_snippet = self.context_analyzer.extract_context_from_history(ctx.query, history_text)
            ctx.enriched_query = f"Ngu canh truoc do:\n{context_snippet}\n\nCau hoi hien tai: {ctx.query}"
            ctx.context_enriched = True
            logger.info("ContextAnalyzer: enriched query with history")

            # Query Rewriting (async)
            t_rw = time.time()
            rewritten = await self.query_rewriter.rewrite_async(ctx.query, context_snippet)
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

    async def _extract_params_async(self, ctx: RequestContext):
        history_text = ctx.history_context

        t0 = time.time()
        params = await self.param_extractor.extract_async(
            query=ctx.query,
            enriched_query=ctx.enriched_query,
            rag_queries=ctx.queries_for_rag,
            history_context=history_text,
        )
        elapsed = time.time() - t0
        ctx.extracted_params = params or {}
        ctx.add_debug_step(
            "ParamExtractor",
            grade=ctx.extracted_params.get("grade"),
            book=ctx.extracted_params.get("book"),
            task_type=ctx.extracted_params.get("task_type"),
            lesson_reference=ctx.extracted_params.get("lesson_reference"),
            question_count=ctx.extracted_params.get("question_count"),
            question_count_range=ctx.extracted_params.get("question_count_range"),
            confidence=ctx.extracted_params.get("confidence"),
            used_llm=ctx.extracted_params.get("used_llm"),
            model=ctx.extracted_params.get("model"),
            time_s=round(elapsed, 2),
        )

    async def _detect_intent_async(self, ctx: RequestContext):
        current_session = self.memory.get_current_session(ctx.user_id)
        current_topic = current_session.topic if current_session else None
        session_messages = current_session.get_context_messages() if current_session and ctx.history_context else None

        t1 = time.time()
        intent_results = await self.intent_router.detect_multi_async(
            query=ctx.enriched_query,
            current_topic=current_topic,
            session_messages=session_messages,
        )
        intent_time = time.time() - t1

        # Populate both list and singular field (backward-compat)
        ctx.intent_results = intent_results
        self._apply_extracted_params_to_intents(ctx)
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

    @staticmethod
    def _apply_extracted_params_to_intents(ctx: RequestContext) -> None:
        params = ctx.extracted_params or {}
        if not params or not ctx.intent_results:
            return
        for intent in ctx.intent_results:
            if not intent.book and params.get("book"):
                intent.book = params["book"]
            if not intent.task_type and params.get("task_type") and intent.primary_intent == "generate":
                intent.task_type = params["task_type"]
            if not intent.lesson_reference and params.get("lesson_reference"):
                intent.lesson_reference = params["lesson_reference"]

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

    async def _handle_no_book_async(self, ctx: RequestContext) -> AsyncGenerator[str, None]:
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
        self._set_debug_info(ctx, msg)
        trace_service.write_trace(ctx, msg)


__all__ = ["Orchestrator"]
