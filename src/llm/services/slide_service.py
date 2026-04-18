"""
SlideService — Domain logic cho Slide generation.

v3: Tích hợp LangGraph ContentSupervisor thay SlidePipeline custom.
    - generate_slide() → gọi graph.invoke() (sync)
    - resume_outline() → resume HITL sau khi user review outline
    - answer_exercise() → giữ nguyên logic chấm bài tập slide
"""

import time
import uuid
import logging
import re
from typing import Generator, Optional, Dict, Any

from src.schemas.context import RequestContext
from src.llm.memory import Session, QuestionRecord
from src.llm.handlers.question.scorer import QuestionScorer
from src.rag.rag_service import RAGService
from src.llm.graphs.content_supervisor import build_content_supervisor, RECURSION_LIMIT
from src.llm.graphs.stream_wrapper import invoke_graph_sync, resume_graph
from src.utils.error_handling import safe_execute

logger = logging.getLogger("chatbot.slide_service")


class SlideService:
    """
    Quản lý domain logic liên quan đến Slide:
        - Sinh slide bài giảng (LangGraph supervisor)
        - Resume HITL sau outline review
        - Chấm bài tập slide
    """

    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service
        self.graph = build_content_supervisor()
        self.scorer = QuestionScorer()

    # ────────────────────────────────────────────────────────
    # GENERATE SLIDE (v3 — LangGraph Supervisor)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi tạo slide", log_prefix="SlideService.generate")
    def generate_slide(
        self, ctx: RequestContext
    ) -> Generator[str, None, None]:
        """Sinh slide bài giảng bằng LangGraph ContentSupervisor."""
        session = ctx.session
        query = ctx.enriched_query

        yield "Đang phân tích nội dung để thiết kế bài giảng..."

        # ① RAG Search
        contexts = self.rag_service.get_context(ctx, intent_hint="generate")
        if not contexts:
            yield "Không tìm thấy nội dung bài học phù hợp."
            return

        if len(contexts) < 3:
            yield "Không đủ tài liệu để tạo slide (cần ít nhất 3 nguồn)."
            return

        yield f"Đã tìm thấy {len(contexts)} nguồn tài liệu. Đang khởi tạo pipeline..."

        # ② Build initial state
        topic = (ctx.intent_result.topic if ctx.intent_result else None) or session.topic or "Bài học"
        grade = self._extract_grade(topic, contexts)
        book = ctx.effective_book or "KNTT"
        thread_id = f"slide-{ctx.request_id or uuid.uuid4().hex[:8]}"

        initial_state = {
            "task_type": "slide",
            "request_id": ctx.request_id or thread_id,
            "query": query,
            "topic": topic,
            "grade": grade,
            "book": book,
            "rag_chunks": contexts,
            "messages": [],
            # Initialize optional fields
            "context_map": "",
            "chunk_map": {},
            "outline_payload": None,
            "content_payload": None,
            "media_payload": None,
            "quiz_payload": None,
            "merged_slides": None,
            "final_output": None,
            "status": "pending",
            "error_message": None,
        }

        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": RECURSION_LIMIT,
        }

        # ③ Run graph (sync)
        yield "Đang chạy supervisor pipeline..."

        t0 = time.time()
        result = invoke_graph_sync(self.graph, initial_state, config)
        pipeline_time = time.time() - t0

        # ④ Check for HITL interrupt
        interrupts = result.get("__interrupt__")
        if interrupts:
            # Store thread_id và config cho resume sau
            slide_state = session.ensure_slide_state()
            slide_state.slide_output = {
                "_graph_thread_id": thread_id,
                "_graph_config": config,
                "_interrupt": True,
            }

            # Lấy interrupt payload
            interrupt_value = interrupts[0].value if hasattr(interrupts[0], 'value') else interrupts[0]
            if isinstance(interrupt_value, dict):
                outline = interrupt_value.get("outline", {})
                msg = interrupt_value.get("message", "Review outline")

                # Hiển thị outline cho user
                yield f"\n\n📋 **Dàn ý bài giảng đã tạo xong** (⏱️ {pipeline_time:.1f}s)"
                yield f"\n{msg}"

                if isinstance(outline, dict):
                    slides = outline.get("slides", [])
                    yield f"\n📊 '{outline.get('lesson_title', topic)}' — {len(slides)} slides:"
                    for i, s in enumerate(slides, 1):
                        icon = {"title": "🎯", "content": "📖", "exercise": "✏️",
                                "summary": "📋"}.get(s.get("slide_type", ""), "📄")
                        yield f"\n  {i}. [{icon} {s.get('slide_type', '')}] {s.get('title', '')}"

                yield "\n\n💡 Gửi 'ok' để duyệt, hoặc mô tả chỉnh sửa bạn muốn."
            else:
                yield f"\n⏸️ Pipeline đang chờ input: {interrupt_value}"

            ctx.add_debug_step(
                "Handler", action="generate_slide", status="hitl_waiting",
                pipeline_time_s=round(pipeline_time, 2),
                thread_id=thread_id,
            )
            return

        # ⑤ No interrupt — pipeline hoàn thành
        yield from self._process_completed_result(result, session, ctx, pipeline_time)

    # ────────────────────────────────────────────────────────
    # RESUME HITL (sau khi user review outline)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi resume pipeline", log_prefix="SlideService.resume")
    def resume_outline(
        self, ctx: RequestContext, user_feedback: str
    ) -> Generator[str, None, None]:
        """Resume graph sau HITL interrupt (outline review)."""
        session = ctx.session
        slide_state = session.slide_state

        if not slide_state or not slide_state.slide_output:
            yield "Không có pipeline nào đang chờ."
            return

        stored = slide_state.slide_output
        if not stored.get("_interrupt"):
            yield "Pipeline đã hoàn thành, không cần resume."
            return

        thread_id = stored["_graph_thread_id"]
        config = stored["_graph_config"]

        # Parse user feedback
        feedback_lower = user_feedback.strip().lower()
        if feedback_lower in ("ok", "yes", "duyệt", "đồng ý", "approve", "oke"):
            resume_value = True  # Approve as-is
            yield "Đã duyệt dàn ý. Đang tiếp tục sinh nội dung..."
        else:
            resume_value = {"feedback": user_feedback}
            yield f"Đã nhận phản hồi. Đang chỉnh sửa và tiếp tục..."

        t0 = time.time()
        result = resume_graph(self.graph, resume_value, config)
        pipeline_time = time.time() - t0

        # Check for another interrupt (unlikely but possible)
        interrupts = result.get("__interrupt__")
        if interrupts:
            yield "⏸️ Pipeline cần thêm input..."
            return

        yield from self._process_completed_result(result, session, ctx, pipeline_time)

    # ────────────────────────────────────────────────────────
    # PROCESS COMPLETED RESULT
    # ────────────────────────────────────────────────────────

    def _process_completed_result(
        self,
        result: dict,
        session,
        ctx: RequestContext,
        pipeline_time: float,
    ) -> Generator[str, None, None]:
        """Xử lý kết quả khi graph hoàn thành (không interrupt)."""

        status = result.get("status", "unknown")
        merged = result.get("merged_slides")
        outline = result.get("outline_payload", {})
        lesson_title = outline.get("lesson_title", "") if isinstance(outline, dict) else ""

        if not merged or status == "failed":
            error_msg = result.get("error_message", "Pipeline không trả về kết quả")
            yield f"Không thể tạo slide: {error_msg}"
            ctx.add_debug_step(
                "Handler", action="generate_slide", status="failed",
                error_message=error_msg,
                pipeline_time_s=round(pipeline_time, 2),
            )
            return

        # Extract slides
        slides_data = merged.get("slides", []) if isinstance(merged, dict) else merged
        total_slides = len(slides_data) if isinstance(slides_data, list) else 0

        # Store state
        slide_state = session.ensure_slide_state()
        slide_state.slide_output = {
            "status": status,
            "lesson_title": lesson_title,
            "slides": slides_data,
            "total_slides": total_slides,
            "_interrupt": False,
        }

        # Extract exercises
        exercise_count = 0
        for slide in (slides_data if isinstance(slides_data, list) else []):
            if isinstance(slide, dict) and slide.get("slide_type") == "exercise":
                questions = slide.get("questions", [])
                if questions:
                    for j, q_data in enumerate(questions):
                        slide_state.add_exercise(
                            question_type="mcq",
                            content=q_data if isinstance(q_data, dict) else {},
                            slide_idx=slides_data.index(slide),
                            q_idx=j,
                        )
                        exercise_count += 1

        # Display
        display = self._format_slides_display(lesson_title, slides_data)
        session.add_message("assistant", display)

        yield f"\n\n✅ Đã tạo {total_slides} slides cho '{lesson_title}' (⏱️ {pipeline_time:.1f}s)"
        yield "\n\n" + display

        if slide_state.has_exercises:
            yield f"\n📝 Slide có {slide_state.total_exercises} câu hỏi bài tập. Bạn có thể trả lời ngay!"

        ctx.add_debug_step(
            "Handler", action="generate_slide", status="success",
            pipeline_time_s=round(pipeline_time, 2),
            total_slides=total_slides,
            lesson_title=lesson_title,
            exercises_extracted=exercise_count,
        )

    def _format_slides_display(self, lesson_title: str, slides: list) -> str:
        """Format slides thành text display."""
        if not slides:
            return "Không có slides."

        lines = [f"📊 {lesson_title} ({len(slides)} slides)", "=" * 50, ""]
        for i, slide in enumerate(slides, 1):
            if not isinstance(slide, dict):
                continue
            slide_type = slide.get("slide_type", "content")
            icon = {"title": "🎯", "content": "📖", "exercise": "✏️",
                    "image": "🖼️", "summary": "📋"}.get(slide_type, "📄")
            lines.append(f"--- Slide {i} [{icon} {slide_type}] ---")
            lines.append(f"  {slide.get('title', '')}")
            for b in slide.get("bullets", []):
                lines.append(f"  • {b}")
            if slide.get("questions"):
                lines.append(f"  📝 {len(slide['questions'])} câu hỏi bài tập")
            lines.append("")
        return "\n".join(lines)

    # ────────────────────────────────────────────────────────
    # ANSWER EXERCISE (giữ nguyên)
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

            icon = "✅ Chính xác!" if result.is_correct else "❌ Sai rồi!"
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

    # ────────────────────────────────────────────────────────
    # HELPERS
    # ────────────────────────────────────────────────────────

    def _extract_grade(self, topic: str, contexts: list) -> str:
        """Extract grade từ topic hoặc context metadata."""
        match = re.search(r'(?:lớp|lop|grade)\s*(10|11|12)', topic.lower())
        if match:
            return match.group(1)

        for ctx in contexts[:5]:
            meta = ctx.get("metadata", {})
            grade = meta.get("grade")
            if grade in ("10", "11", "12"):
                return grade

        return "10"

    def is_waiting_hitl(self, session) -> bool:
        """Check xem pipeline có đang chờ HITL input không."""
        slide_state = session.slide_state
        if not slide_state or not slide_state.slide_output:
            return False
        return slide_state.slide_output.get("_interrupt", False)


__all__ = ["SlideService"]
