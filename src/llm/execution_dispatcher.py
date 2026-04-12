"""
ExecutionDispatcher — Action → Handler mapping (Strategy Pattern).

Thay thế chuỗi if-elif-else khổng lồ trong _execute() cũ
bằng dictionary dispatch (handler registry).
"""

import logging
from typing import Generator, Dict, Callable

from src.llm.action_planner import Action, ActionPlan
from src.schemas.context import RequestContext
from src.llm.handlers.chat_handler import ChatHandler
from src.llm.handlers.explain_handler import ExplainHandler
from src.llm.utils import format_contexts
from src.llm.services.quiz_service import QuizService
from src.llm.services.slide_service import SlideService
from src.rag.rag_service import RAGService
from src.utils.error_handling import safe_execute

logger = logging.getLogger("chatbot.dispatcher")


class ExecutionDispatcher:
    """
    Registry-based handler dispatch.

    Mỗi Action enum → 1 handler function.
    Clean, dễ mở rộng: chỉ cần thêm entry vào _handlers dict.
    """

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

    def dispatch(
        self,
        plan: ActionPlan,
        ctx: RequestContext,
    ) -> Generator[str, None, None]:
        """
        Dispatch action → handler.

        Args:
            plan: ActionPlan từ ActionPlanner
            ctx: RequestContext chứa toàn bộ data

        Yields:
            str: Response chunks
        """
        handler = self._handlers.get(plan.action, self._dispatch_chat)
        yield from handler(plan, ctx)

    # ── Individual dispatchers ─────────────────────────────

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
        """Giải thích câu hỏi cụ thể. Fallback sang explain concept nếu không có câu hỏi."""
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
        """Giải thích khái niệm tổng quát (RAG + ExplainHandler)."""
        yield "Đang tìm tài liệu để giải thích..."

        import time
        contexts = self.rag_service.get_context(ctx, intent_hint="explain")
        context_text = format_contexts(contexts) if contexts else ""

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
        """Chat tự do (RAG + ChatHandler)."""
        import time

        contexts = self.rag_service.get_context(ctx, intent_hint="chat")
        context_text = format_contexts(contexts) if contexts else ""

        t0 = time.time()
        response = self.chat_handler.handle(ctx.enriched_query, context=context_text)
        chat_time = time.time() - t0

        ctx.session.add_message("assistant", response)
        ctx.add_debug_step(
            "Handler", action="chat", status="success",
            rag_chunks=len(contexts) if contexts else 0,
            chat_time_s=round(chat_time, 2),
            response_length=len(response),
        )
        yield response

    def _dispatch_lesson_plan(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield "Chức năng tạo giáo án đang được phát triển."

    def _dispatch_answer_exercise(
        self, plan: ActionPlan, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield from self.slide_service.answer_exercise(ctx, ctx.query)


__all__ = ["ExecutionDispatcher"]
