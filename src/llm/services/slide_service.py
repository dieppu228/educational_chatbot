"""
SlideService — Domain logic cho Slide generation.

Tách từ _handle_generate_slide() và _handle_answer_exercise()
trong orchestrator.py cũ.
"""

import time
import logging
from typing import Generator

from src.schemas.context import RequestContext
from src.llm.memory import Session, QuestionRecord
from src.llm.handlers.content.slide_handler import SlideHandler
from src.llm.handlers.content.slide_template import SlideTemplate
from src.llm.handlers.question.scorer import QuestionScorer
from src.rag.context_combiner import format_contexts
from src.rag.rag_service import RAGService
from src.utils.error_handling import safe_execute

logger = logging.getLogger("chatbot.slide_service")


class SlideService:
    """
    Quản lý domain logic liên quan đến Slide:
        - Sinh slide bài giảng
        - Trích bài tập từ slide
        - Chấm bài tập slide
    """

    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service
        self.slide_handler = SlideHandler()
        self.scorer = QuestionScorer()

    # ────────────────────────────────────────────────────────
    # GENERATE SLIDE
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi tạo slide", log_prefix="SlideService.generate")
    def generate_slide(
        self, ctx: RequestContext
    ) -> Generator[str, None, None]:
        """Sinh slide bài giảng với bài tập tự động."""
        session = ctx.session
        query = ctx.enriched_query

        yield "Đang phân tích nội dung để thiết kế bài giảng..."

        contexts = self.rag_service.get_context(ctx, intent_hint="generate")
        if not contexts:
            yield "Không tìm thấy nội dung bài học phù hợp."
            return

        context_text = format_contexts(contexts, action="generate_slide")

        t0 = time.time()
        slide_output = self.slide_handler.handle(
            book="Ket noi tri thuc",
            grade="10",
            lesson=session.topic or "Bai hoc",
            context=context_text,
        )
        slide_time = time.time() - t0

        # Log slide types
        slide_types = [s.slide_type for s in slide_output.slides]

        # Store state
        slide_state = session.ensure_slide_state()
        slide_state.slide_output = slide_output.model_dump()
        slide_state.slide_html = SlideTemplate.render_to_html(slide_output)

        # Extract exercises
        exercise_count = 0
        for i, slide in enumerate(slide_output.slides):
            if slide.slide_type == "exercise" and slide.questions:
                for j, q_data in enumerate(slide.questions):
                    slide_state.add_exercise(
                        question_type="mcq",
                        content=q_data,
                        slide_idx=i,
                        q_idx=j,
                    )
                    exercise_count += 1

        display = slide_output.to_display_format()
        session.add_message("assistant", display)

        yield f"\n\nĐã tạo {slide_output.total_slides} slides cho '{slide_output.lesson_title}'."
        yield "\n\n" + display

        if slide_state.has_exercises:
            yield f"\nSlide có {slide_state.total_exercises} câu hỏi bài tập. Bạn có thể trả lời ngay!"

        ctx.add_debug_step(
            "Handler", action="generate_slide", status="success",
            slide_time_s=round(slide_time, 2),
            total_slides=slide_output.total_slides,
            lesson_title=slide_output.lesson_title,
            slide_types=slide_types,
            exercises_extracted=exercise_count,
        )

    # ────────────────────────────────────────────────────────
    # ANSWER EXERCISE
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi chấm bài tập", log_prefix="SlideService.answer_exercise")
    def answer_exercise(
        self, ctx: RequestContext, original_query: str
    ) -> Generator[str, None, None]:
        """Chấm điểm câu trả lời bài tập slide."""
        session = ctx.session
        slide_state = session.slide_state

        if not slide_state or not slide_state.has_exercises:
            yield "Không có bài tập slide nào để trả lời."
            return

        task_items = [q.to_task_item() for q in slide_state.exercise_questions]

        t0 = time.time()
        result = self.scorer.handle(original_query, task_items)
        score_time = time.time() - t0

        if result.status == "found" and result.question_index is not None:
            idx = result.question_index
            if idx < len(slide_state.exercise_questions):
                record = slide_state.exercise_questions[idx]
                record.record_attempt(
                    user_answer=result.user_answer,
                    is_correct=result.is_correct or False,
                    score=result.score,
                )

            icon = "Chính xác!" if result.is_correct else "Sai rồi!"
            msg = f"\n\n{icon} {result.explanation or ''}"
            session.add_message("assistant", msg)
            ctx.add_debug_step(
                "Handler", action="answer_exercise", status="found",
                scorer_time_s=round(score_time, 2),
                is_correct=result.is_correct,
                question_index=result.question_index,
            )
            yield msg
        else:
            yield f"\nKhông xác định được câu trả lời. {result.explanation or ''}"


__all__ = ["SlideService"]
