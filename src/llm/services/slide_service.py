
import time
import uuid
import asyncio
import logging
import re
from typing import Generator, Optional, Dict, Any, AsyncGenerator

from src.schemas.context import RequestContext
from src.schemas.slide_schemas import ContentPipelineInput
from src.llm.memory import Session, QuestionRecord
from src.llm.handlers.question.scorer import QuestionScorer
from src.rag.rag_service import RAGService
from src.llm.graphs.content_supervisor import build_content_supervisor, RECURSION_LIMIT
from src.llm.graphs.stream_wrapper import invoke_graph_sync, resume_graph
from langgraph.types import Command
from src.utils.error_handling import safe_execute

logger = logging.getLogger("chatbot.slide_service")


class SlideService:

    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service
        self.graph = build_content_supervisor()
        self.scorer = QuestionScorer()

    @staticmethod
    def should_block_by_quality(quality_review: Optional[dict]) -> bool:
        if not isinstance(quality_review, dict):
            return False
        action = quality_review.get("reflection_action")
        return action in ("block", "ask_human")

    def _run_graph_for_ctx(self, graph_input, config: dict, ctx: RequestContext, phase: str) -> dict:
        if not getattr(ctx, "graph_debug_stream", False):
            return invoke_graph_sync(self.graph, graph_input, config)
        return self._stream_graph_for_ctx(graph_input, config, ctx, phase)

    def _resume_graph_for_ctx(self, resume_value, config: dict, ctx: RequestContext, phase: str) -> dict:
        if not getattr(ctx, "graph_debug_stream", False):
            return resume_graph(self.graph, resume_value, config)
        return self._stream_graph_for_ctx(Command(resume=resume_value), config, ctx, phase)

    def _stream_graph_for_ctx(self, graph_input, config: dict, ctx: RequestContext, phase: str) -> dict:
        try:
            for chunk in self.graph.stream(graph_input, config=config):
                if "__interrupt__" in chunk:
                    ctx.add_debug_step(
                        "GraphNode",
                        graph_node="__interrupt__",
                        phase=phase,
                        status="interrupt",
                    )
                    return {"__interrupt__": chunk["__interrupt__"]}

                for node_name, node_output in chunk.items():
                    if node_name.startswith("__"):
                        continue
                    output_keys = list(node_output.keys()) if isinstance(node_output, dict) else []
                    ctx.add_debug_step(
                        "GraphNode",
                        graph_node=node_name,
                        phase=phase,
                        output_keys=output_keys,
                        status=(
                            node_output.get("status")
                            if isinstance(node_output, dict)
                            else None
                        ),
                    )

            state = self.graph.get_state(config)
            return dict(state.values) if state and state.values else {}
        except Exception as e:
            return {
                "status": "failed",
                "error_message": str(e),
            }

    # ────────────────────────────────────────────────────────
    # GENERATE SLIDE (v4 — Narrow Interface)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi tạo slide", log_prefix="SlideService.generate")
    def generate_slide(
        self, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield from self._run_content_pipeline(ctx, task_type="slide")

    # ────────────────────────────────────────────────────────
    # GENERATE LESSON PLAN
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi tạo giáo án", log_prefix="SlideService.lesson_plan")
    def generate_lesson_plan(
        self, ctx: RequestContext
    ) -> Generator[str, None, None]:
        yield from self._run_content_pipeline(ctx, task_type="lesson_plan")

    # ────────────────────────────────────────────────────────
    # SHARED PIPELINE (slide + lesson_plan)
    # ────────────────────────────────────────────────────────

    def _run_content_pipeline(
        self, ctx: RequestContext, task_type: str = "slide"
    ) -> Generator[str, None, None]:
        session = ctx.session
        task_label = "giáo án" if task_type == "lesson_plan" else "slide"

        yield f"Đang phân tích nội dung để thiết kế {task_label}..."

        # ① RAG Search
        contexts = self.rag_service.get_context(ctx, intent_hint="generate", task_type=task_type)
        if not contexts:
            yield f"Không tìm thấy nội dung bài học phù hợp."
            return

        if len(contexts) < 3:
            yield f"Không đủ tài liệu để tạo {task_label} (cần ít nhất 3 nguồn)."
            return

        yield f"Đã tìm thấy {len(contexts)} nguồn tài liệu. Đang khởi tạo pipeline..."

        # ② Build input via narrow DTO
        pipeline_input = ContentPipelineInput.from_context(ctx, contexts, task_type=task_type)
        thread_id = f"{task_type}-{pipeline_input.request_id or uuid.uuid4().hex[:8]}"
        initial_state = pipeline_input.to_graph_state()

        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": RECURSION_LIMIT,
        }

        # ③ Run graph (sync)
        yield f"Đang chạy supervisor pipeline ({task_label})..."

        t0 = time.time()
        result = self._run_graph_for_ctx(initial_state, config, ctx, phase="initial")
        pipeline_time = time.time() - t0

        # ④ Check for HITL interrupt
        interrupts = result.get("__interrupt__")
        if interrupts:
            if getattr(ctx, "auto_approve_outline", False):
                yield "Auto-approve dàn ý để chạy end-to-end debug..."
                result = self._resume_graph_for_ctx(True, config, ctx, phase="auto_resume")
                pipeline_time = time.time() - t0
                if not result.get("__interrupt__"):
                    yield from self._process_completed_result(result, session, ctx, pipeline_time, task_type)
                    return

            # Store thread_id và config cho resume sau
            slide_state = session.ensure_slide_state()
            slide_state.slide_output = {
                "_graph_thread_id": thread_id,
                "_graph_config": config,
                "_interrupt": True,
                "_task_type": task_type,
            }

            # Lấy interrupt payload
            interrupt_value = interrupts[0].value if hasattr(interrupts[0], 'value') else interrupts[0]
            if isinstance(interrupt_value, dict):
                outline = interrupt_value.get("outline", {})
                msg = interrupt_value.get("message", "Review outline")

                # Hiển thị outline cho user
                yield f"\n\n📋 **Dàn ý {task_label} đã tạo xong** (⏱️ {pipeline_time:.1f}s)"
                yield f"\n{msg}"

                if isinstance(outline, dict):
                    slides = outline.get("slides", [])
                    yield f"\n📊 '{outline.get('lesson_title', pipeline_input.topic)}' — {len(slides)} sections:"
                    for i, s in enumerate(slides, 1):
                        icon = {"title": "🎯", "content": "📖", "exercise": "✏️",
                                "summary": "📋"}.get(s.get("slide_type", ""), "📄")
                        yield f"\n  {i}. [{icon} {s.get('slide_type', '')}] {s.get('title', '')}"

                yield f"\n\n💡 Gửi 'ok' để duyệt, hoặc mô tả chỉnh sửa bạn muốn."
            else:
                yield f"\n⏸️ Pipeline đang chờ input: {interrupt_value}"

            ctx.add_debug_step(
                "Handler", action=f"generate_{task_type}", status="hitl_waiting",
                pipeline_time_s=round(pipeline_time, 2),
                thread_id=thread_id,
            )
            return

        # ⑤ No interrupt — pipeline hoàn thành
        yield from self._process_completed_result(result, session, ctx, pipeline_time, task_type)

    # ────────────────────────────────────────────────────────
    # RESUME HITL (sau khi user review outline)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi resume pipeline", log_prefix="SlideService.resume")
    def resume_outline(
        self, ctx: RequestContext, user_feedback: str
    ) -> Generator[str, None, None]:
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
        task_type = stored.get("_task_type", "slide")

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

        yield from self._process_completed_result(result, session, ctx, pipeline_time, task_type)

    # ────────────────────────────────────────────────────────
    # PROCESS COMPLETED RESULT
    # ────────────────────────────────────────────────────────

    def _process_completed_result(
        self,
        result: dict,
        session,
        ctx: RequestContext,
        pipeline_time: float,
        task_type: str = "slide",
    ) -> Generator[str, None, None]:

        task_label = "giáo án" if task_type == "lesson_plan" else "slide"
        action_name = f"generate_{task_type}"

        status = result.get("status", "unknown")
        merged = result.get("merged_slides")
        outline = result.get("outline_payload", {})
        quality_review = result.get("quality_review")
        reflection_attempts = int(result.get("reflection_attempts") or 0)
        lesson_title = outline.get("lesson_title", "") if isinstance(outline, dict) else ""

        if result.get("quality_blocked") or self.should_block_by_quality(quality_review):
            reason = (
                quality_review.get("reason_fail")
                if isinstance(quality_review, dict)
                else "QUALITY_REVIEW_FAILED"
            )
            summary = (
                quality_review.get("summary")
                if isinstance(quality_review, dict)
                else result.get("error_message", "Quality review failed")
            )
            instruction = result.get("revision_instruction") or summary
            yield f"Không thể tạo {task_label}: quality review failed ({reason}). {instruction}"
            ctx.add_debug_step(
                "QualityReviewer",
                target=task_type,
                passed=False,
                reason_fail=reason,
                summary=summary,
                reflection_action=(
                    quality_review.get("reflection_action")
                    if isinstance(quality_review, dict)
                    else "block"
                ),
                reflection_attempts=reflection_attempts,
                quality_review=quality_review,
            )
            return

        if not merged or status == "failed":
            error_msg = result.get("error_message", "Pipeline không trả về kết quả")
            yield f"Không thể tạo {task_label}: {error_msg}"
            ctx.add_debug_step(
                "Handler", action=action_name, status="failed",
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
            "quality_review": quality_review,
            "reflection_attempts": reflection_attempts,
            "_interrupt": False,
            "_task_type": task_type,
        }

        # Extract exercises (chỉ cho slide, lesson plan không cần quiz state)
        exercise_count = 0
        if task_type == "slide":
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
        if task_type == "lesson_plan":
            display = self._format_lesson_plan_display(lesson_title, slides_data)
        else:
            display = self._format_slides_display(lesson_title, slides_data)

        session.add_message("assistant", display)

        yield f"\n\n✅ Đã tạo {total_slides} {task_label} sections cho '{lesson_title}' (⏱️ {pipeline_time:.1f}s)"
        if reflection_attempts > 0 and isinstance(quality_review, dict) and quality_review.get("passed"):
            yield "\n\nQuality reviewer đã yêu cầu chỉnh sửa và hệ thống đã regenerate output đạt yêu cầu."
        yield "\n\n" + display

        if task_type == "slide" and slide_state.has_exercises:
            yield f"\n📝 Slide có {slide_state.total_exercises} câu hỏi bài tập. Bạn có thể trả lời ngay!"

        ctx.add_debug_step(
            "Handler", action=action_name, status="success",
            pipeline_time_s=round(pipeline_time, 2),
            total_slides=total_slides,
            lesson_title=lesson_title,
            exercises_extracted=exercise_count,
        )
        if isinstance(quality_review, dict):
            ctx.add_debug_step(
                "QualityReviewer",
                target=task_type,
                passed=quality_review.get("passed"),
                score=quality_review.get("score"),
                reason_fail=quality_review.get("reason_fail"),
                summary=quality_review.get("summary"),
                reflection_action=quality_review.get("reflection_action"),
                reflection_attempts=reflection_attempts,
                issues=quality_review.get("issues", []),
            )

    # ────────────────────────────────────────────────────────
    # DISPLAY FORMATTERS
    # ────────────────────────────────────────────────────────

    def _format_slides_display(self, lesson_title: str, slides: list) -> str:
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

    def _format_lesson_plan_display(self, lesson_title: str, sections: list) -> str:
        if not sections:
            return "Không có nội dung giáo án."

        lines = [f"📝 {lesson_title} ({len(sections)} phần)", "═" * 50, ""]
        for i, section in enumerate(sections, 1):
            if not isinstance(section, dict):
                continue
            slide_type = section.get("slide_type", "content")
            icon = {"title": "📋", "content": "📖", "exercise": "✏️",
                    "summary": "📝"}.get(slide_type, "📄")
            lines.append(f"╔══ Phần {i} [{icon} {slide_type.upper()}] ══╗")
            lines.append(f"  📌 {section.get('title', '')}")
            for b in section.get("bullets", []):
                lines.append(f"  ▸ {b}")
            notes = section.get("notes")
            if notes:
                lines.append(f"  📎 Ghi chú GV: {notes[:150]}{'...' if len(notes) > 150 else ''}")
            if section.get("questions"):
                lines.append(f"  🎯 {len(section['questions'])} tiêu chí đánh giá")
            lines.append("")
        return "\n".join(lines)

    # ────────────────────────────────────────────────────────
    # ANSWER EXERCISE (giữ nguyên)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi chấm bài tập", log_prefix="SlideService.answer_exercise")
    def answer_exercise(
        self, ctx: RequestContext, original_query: str
    ) -> Generator[str, None, None]:
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

    def is_waiting_hitl(self, session) -> bool:
        slide_state = session.slide_state
        if not slide_state or not slide_state.slide_output:
            return False
        return slide_state.slide_output.get("_interrupt", False)

    # ────────────────────────────────────────────────────────
    # ASYNC VERSIONS (run blocking graph ops in thread pool)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi tạo slide", log_prefix="SlideService.generate_async")
    async def generate_slide_async(
        self, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        async for chunk in self._run_content_pipeline_async(ctx, task_type="slide"):
            yield chunk

    @safe_execute(fallback_message="Lỗi tạo giáo án", log_prefix="SlideService.lesson_plan_async")
    async def generate_lesson_plan_async(
        self, ctx: RequestContext
    ) -> AsyncGenerator[str, None]:
        async for chunk in self._run_content_pipeline_async(ctx, task_type="lesson_plan"):
            yield chunk

    async def _run_content_pipeline_async(
        self, ctx: RequestContext, task_type: str = "slide"
    ) -> AsyncGenerator[str, None]:
        session = ctx.session
        task_label = "giáo án" if task_type == "lesson_plan" else "slide"

        yield f"Đang phân tích nội dung để thiết kế {task_label}..."

        # ① RAG Search (async)
        contexts = await self.rag_service.get_context_async(ctx, intent_hint="generate", task_type=task_type)
        if not contexts:
            yield f"Không tìm thấy nội dung bài học phù hợp."
            return

        if len(contexts) < 3:
            yield f"Không đủ tài liệu để tạo {task_label} (cần ít nhất 3 nguồn)."
            return

        yield f"Đã tìm thấy {len(contexts)} nguồn tài liệu. Đang khởi tạo pipeline..."

        # ② Build input via narrow DTO
        pipeline_input = ContentPipelineInput.from_context(ctx, contexts, task_type=task_type)
        thread_id = f"{task_type}-{pipeline_input.request_id or uuid.uuid4().hex[:8]}"
        initial_state = pipeline_input.to_graph_state()

        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": RECURSION_LIMIT,
        }

        # ③ Run graph in thread pool (blocking)
        yield f"Đang chạy supervisor pipeline ({task_label})..."

        t0 = time.time()
        result = await asyncio.to_thread(
            self._run_graph_for_ctx,
            initial_state,
            config,
            ctx,
            "initial",
        )
        pipeline_time = time.time() - t0

        # ④ Check for HITL interrupt
        interrupts = result.get("__interrupt__")
        if interrupts:
            if getattr(ctx, "auto_approve_outline", False):
                yield "Auto-approve dàn ý để chạy end-to-end debug..."
                result = await asyncio.to_thread(
                    self._resume_graph_for_ctx,
                    True,
                    config,
                    ctx,
                    "auto_resume",
                )
                pipeline_time = time.time() - t0
                if not result.get("__interrupt__"):
                    async for chunk in self._process_completed_result_async(
                        result,
                        session,
                        ctx,
                        pipeline_time,
                        task_type,
                    ):
                        yield chunk
                    return

            slide_state = session.ensure_slide_state()
            slide_state.slide_output = {
                "_graph_thread_id": thread_id,
                "_graph_config": config,
                "_interrupt": True,
                "_task_type": task_type,
            }

            interrupt_value = interrupts[0].value if hasattr(interrupts[0], 'value') else interrupts[0]
            if isinstance(interrupt_value, dict):
                outline = interrupt_value.get("outline", {})
                msg = interrupt_value.get("message", "Review outline")

                yield f"\n\n📋 **Dàn ý {task_label} đã tạo xong** (⏱️ {pipeline_time:.1f}s)"
                yield f"\n{msg}"

                if isinstance(outline, dict):
                    slides = outline.get("slides", [])
                    yield f"\n📊 '{outline.get('lesson_title', pipeline_input.topic)}' — {len(slides)} sections:"
                    for i, s in enumerate(slides, 1):
                        icon = {"title": "🎯", "content": "📖", "exercise": "✏️",
                                "summary": "📋"}.get(s.get("slide_type", ""), "📄")
                        yield f"\n  {i}. [{icon} {s.get('slide_type', '')}] {s.get('title', '')}"

                yield f"\n\n💡 Gửi 'ok' để duyệt, hoặc mô tả chỉnh sửa bạn muốn."
            else:
                yield f"\n⏸️ Pipeline đang chờ input: {interrupt_value}"

            ctx.add_debug_step(
                "Handler", action=f"generate_{task_type}", status="hitl_waiting",
                pipeline_time_s=round(pipeline_time, 2),
                thread_id=thread_id,
            )
            return

        # ⑤ No interrupt — completed
        async for chunk in self._process_completed_result_async(result, session, ctx, pipeline_time, task_type):
            yield chunk

    async def _process_completed_result_async(
        self,
        result: dict,
        session,
        ctx: RequestContext,
        pipeline_time: float,
        task_type: str = "slide",
    ) -> AsyncGenerator[str, None]:

        task_label = "giáo án" if task_type == "lesson_plan" else "slide"
        action_name = f"generate_{task_type}"

        status = result.get("status", "unknown")
        merged = result.get("merged_slides")
        outline = result.get("outline_payload", {})
        quality_review = result.get("quality_review")
        reflection_attempts = int(result.get("reflection_attempts") or 0)
        lesson_title = outline.get("lesson_title", "") if isinstance(outline, dict) else ""

        if result.get("quality_blocked") or self.should_block_by_quality(quality_review):
            reason = (
                quality_review.get("reason_fail")
                if isinstance(quality_review, dict)
                else "QUALITY_REVIEW_FAILED"
            )
            summary = (
                quality_review.get("summary")
                if isinstance(quality_review, dict)
                else result.get("error_message", "Quality review failed")
            )
            instruction = result.get("revision_instruction") or summary
            yield f"Không thể tạo {task_label}: quality review failed ({reason}). {instruction}"
            ctx.add_debug_step(
                "QualityReviewer",
                target=task_type,
                passed=False,
                reason_fail=reason,
                summary=summary,
                reflection_action=(
                    quality_review.get("reflection_action")
                    if isinstance(quality_review, dict)
                    else "block"
                ),
                reflection_attempts=reflection_attempts,
                quality_review=quality_review,
            )
            return

        if not merged or status == "failed":
            error_msg = result.get("error_message", "Pipeline không trả về kết quả")
            yield f"Không thể tạo {task_label}: {error_msg}"
            ctx.add_debug_step(
                "Handler", action=action_name, status="failed",
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
            "quality_review": quality_review,
            "reflection_attempts": reflection_attempts,
            "_interrupt": False,
            "_task_type": task_type,
        }

        # Extract exercises
        exercise_count = 0
        if task_type == "slide":
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
        if task_type == "lesson_plan":
            display = self._format_lesson_plan_display(lesson_title, slides_data)
        else:
            display = self._format_slides_display(lesson_title, slides_data)

        session.add_message("assistant", display)

        yield f"\n\n✅ Đã tạo {total_slides} {task_label} sections cho '{lesson_title}' (⏱️ {pipeline_time:.1f}s)"
        if reflection_attempts > 0 and isinstance(quality_review, dict) and quality_review.get("passed"):
            yield "\n\nQuality reviewer đã yêu cầu chỉnh sửa và hệ thống đã regenerate output đạt yêu cầu."
        yield "\n\n" + display

        if task_type == "slide" and slide_state.has_exercises:
            yield f"\n📝 Slide có {slide_state.total_exercises} câu hỏi bài tập. Bạn có thể trả lời ngay!"

        ctx.add_debug_step(
            "Handler", action=action_name, status="success",
            pipeline_time_s=round(pipeline_time, 2),
            total_slides=total_slides,
            lesson_title=lesson_title,
            exercises_extracted=exercise_count,
        )
        if isinstance(quality_review, dict):
            ctx.add_debug_step(
                "QualityReviewer",
                target=task_type,
                passed=quality_review.get("passed"),
                score=quality_review.get("score"),
                reason_fail=quality_review.get("reason_fail"),
                summary=quality_review.get("summary"),
                reflection_action=quality_review.get("reflection_action"),
                reflection_attempts=reflection_attempts,
                issues=quality_review.get("issues", []),
            )

    async def answer_exercise_async(
        self, ctx: RequestContext, original_query: str
    ) -> AsyncGenerator[str, None]:
        session = ctx.session
        slide_state = session.slide_state

        if not slide_state or not slide_state.has_exercises:
            yield "Không có bài tập slide nào để trả lời."
            return

        task_items = [q.to_task_item() for q in slide_state.exercise_questions]

        t0 = time.time()
        result = await self.scorer.handle_async(original_query, task_items)
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


__all__ = ["SlideService"]
