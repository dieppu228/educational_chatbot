import asyncio
from typing import Generator, Dict, Callable, AsyncGenerator

from src.llm.action_planner import Action, ActionPlan
from src.schemas.context import RequestContext
from src.llm.handlers.chat_handler import ChatHandler
from src.llm.handlers.explain_handler import ExplainHandler
from src.rag.context_builder import ContextBuilder
from src.llm.services.quiz_service import QuizService
from src.llm.services.slide_service import SlideService
from src.rag.rag_service import RAGService
from src.utils.error_handling import safe_execute


class ExecutionDispatcher:

    def __init__(
        self,
        quiz_service: QuizService,
        slide_service: SlideService,
        rag_service: RAGService,
    ):
        self.quiz_service = quiz_service
        self.slide_service = slide_service
        self.rag_service = rag_service
        self.chat_handler = ChatHandler()
        self.explain_handler = ExplainHandler()
        self.context_builder = ContextBuilder()

        # ── Handler Registry ──────────────────────────────
        self._handlers: Dict[Action, Callable] = {
            Action.GENERATE_QUIZ:       self._dispatch_generate_quiz,
            Action.GENERATE_SLIDE:      self._dispatch_generate_slide,
            Action.CHECK_ANSWER:        self._dispatch_check_answer,
            Action.REVIEW_WRONG:        self._dispatch_review_wrong,
            Action.GET_STATS:           self._dispatch_get_stats,
            Action.EXPLAIN_QUESTION:    self._dispatch_explain_question,
            Action.EXPLAIN_CONCEPT:     self._dispatch_explain_concept,
            Action.ANSWER_EXERCISE:     self._dispatch_answer_exercise,
            Action.GENERATE_LESSON_PLAN: self._dispatch_lesson_plan,
            Action.CHAT:                self._dispatch_chat,
        }

        self._async_handlers: Dict[Action, Callable] = {
            Action.GENERATE_QUIZ:       self._dispatch_generate_quiz_async,
            Action.GENERATE_SLIDE:      self._dispatch_generate_slide_async,
            Action.CHECK_ANSWER:        self._dispatch_check_answer_async,
            Action.REVIEW_WRONG:        self._dispatch_review_wrong_async,
            Action.GET_STATS:           self._dispatch_get_stats_async,
            Action.EXPLAIN_QUESTION:    self._dispatch_explain_question_async,
            Action.EXPLAIN_CONCEPT:     self._dispatch_explain_concept_async,
            Action.ANSWER_EXERCISE:     self._dispatch_answer_exercise_async,
            Action.GENERATE_LESSON_PLAN: self._dispatch_lesson_plan_async,
            Action.CHAT:                self._dispatch_chat_async,
        }

    def dispatch(
        self,
        plan: ActionPlan,
        ctx: RequestContext,
    ) -> Generator[str, None, None]:
        handler = self._handlers.get(plan.action, self._dispatch_chat)
        yield from handler(plan, ctx)

    async def dispatch_async(
        self,
        plan: ActionPlan,
        ctx: RequestContext,
    ) -> AsyncGenerator[str, None]:
        handler = self._async_handlers.get(plan.action, self._dispatch_chat_async)
        async for chunk in handler(plan, ctx):
            yield chunk

    # ── Individual dispatchers (sync - for backward compat) ──

    def _dispatch_generate_quiz(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        task_type = ctx.intent_result.task_type or "mcq" if ctx.intent_result else "mcq"
        yield from self.quiz_service.generate_quiz(ctx, task_type)

    def _dispatch_generate_slide(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield from self.slide_service.generate_slide(ctx)

    def _dispatch_check_answer(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield from self.quiz_service.check_answer(ctx, ctx.query)

    def _dispatch_review_wrong(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield from self.quiz_service.review_wrong(ctx, ctx.query, plan.round_id)

    def _dispatch_get_stats(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield from self.quiz_service.get_stats(ctx)

    def _dispatch_explain_question(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        for chunk in self.quiz_service.explain_question(ctx, ctx.query):
            if chunk is None:
                # Fallback: không có câu hỏi trong session
                yield from self._dispatch_explain_concept(plan, ctx)
                return
            yield chunk

    @safe_execute(fallback_message="Lỗi giải thích", log_prefix="Dispatcher.explain")
    def _dispatch_explain_concept(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        import time
        yield "Đang tìm tài liệu để giải thích..."

        contexts = self.rag_service.get_context(ctx, intent_hint="explain")
        context_text = self.context_builder.build(
            query=ctx.enriched_query, chunks=contexts, action="explain_concept"
        ) if contexts else ""

        t0 = time.time()
        response = self.explain_handler.handle(ctx.enriched_query, context=context_text)
        explain_time = time.time() - t0

        ctx.session.add_message("assistant", response)
        ctx.add_debug_step(
            "Handler", action="explain_concept", status="success",
            rag_chunks=len(contexts) if contexts else 0,
            explain_time_s=round(explain_time, 2),
            response_length=len(response),
        )
        yield "\n\n" + response

    @safe_execute(fallback_message="Lỗi trả lời", log_prefix="Dispatcher.chat")
    def _dispatch_chat(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        import time

        t0 = time.time()
        response = self.chat_handler.handle(ctx.enriched_query, context="")
        chat_time = time.time() - t0

        ctx.session.add_message("assistant", response)
        ctx.add_debug_step(
            "Handler", action="chat", status="success",
            rag_chunks=0,
            chat_time_s=round(chat_time, 2),
            response_length=len(response),
        )
        yield response

    def _dispatch_lesson_plan(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield from self.slide_service.generate_lesson_plan(ctx)

    def _dispatch_answer_exercise(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield from self.slide_service.answer_exercise(ctx, ctx.query)

    # ── Individual dispatchers (async versions) ──

    async def _dispatch_generate_quiz_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        task_type = ctx.intent_result.task_type or "mcq" if ctx.intent_result else "mcq"
        async for chunk in self.quiz_service.generate_quiz_async(ctx, task_type):
            yield chunk

    async def _dispatch_generate_slide_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.slide_service.generate_slide_async(ctx):
            yield chunk

    async def _dispatch_check_answer_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.quiz_service.check_answer_async(ctx, ctx.query):
            yield chunk

    async def _dispatch_review_wrong_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.quiz_service.review_wrong_async(ctx, ctx.query, plan.round_id):
            yield chunk

    async def _dispatch_get_stats_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.quiz_service.get_stats_async(ctx):
            yield chunk

    async def _dispatch_explain_question_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.quiz_service.explain_question_async(ctx, ctx.query):
            if chunk is None:
                # Fallback: không có câu hỏi trong session
                async for c in self._dispatch_explain_concept_async(plan, ctx):
                    yield c
                return
            yield chunk

    @safe_execute(fallback_message="Lỗi giải thích", log_prefix="Dispatcher.explain")
    async def _dispatch_explain_concept_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        import time
        yield "Đang tìm tài liệu để giải thích..."

        contexts = await self.rag_service.get_context_async(ctx, intent_hint="explain")
        context_text = await self.context_builder.build_async(
            query=ctx.enriched_query, chunks=contexts, action="explain_concept"
        ) if contexts else ""

        t0 = time.time()
        response = await self.explain_handler.handle_async(ctx.enriched_query, context=context_text)
        explain_time = time.time() - t0

        ctx.session.add_message("assistant", response)
        ctx.add_debug_step(
            "Handler", action="explain_concept", status="success",
            rag_chunks=len(contexts) if contexts else 0,
            explain_time_s=round(explain_time, 2),
            response_length=len(response),
        )
        yield "\n\n" + response

    @safe_execute(fallback_message="Lỗi trả lời", log_prefix="Dispatcher.chat")
    async def _dispatch_chat_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        import time

        t0 = time.time()
        response = await self.chat_handler.handle_async(ctx.enriched_query, context="")
        chat_time = time.time() - t0

        ctx.session.add_message("assistant", response)
        ctx.add_debug_step(
            "Handler", action="chat", status="success",
            rag_chunks=0,
            chat_time_s=round(chat_time, 2),
            response_length=len(response),
        )
        yield response

    async def _dispatch_lesson_plan_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.slide_service.generate_lesson_plan_async(ctx):
            yield chunk

    async def _dispatch_answer_exercise_async(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.slide_service.answer_exercise_async(ctx, ctx.query):
            yield chunk


__all__ = ["ExecutionDispatcher"]
