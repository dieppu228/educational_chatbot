import asyncio
import json
import time
import logging
import re
from typing import Generator, Optional, List, Dict, AsyncGenerator

from src.schemas.context import RequestContext
from src.llm.memory import Session, QuestionRecord, QuizRound
from src.llm.handlers.question.scorer import QuestionScorer
from src.llm.validators.question_validator import QuestionValidator
from src.llm.handlers.explain_handler import ExplainHandler
from src.llm.services.quality_reviewer import get_quality_reviewer
from src.llm.student_tracker import StudentTracker
from src.llm.utils import extract_num_questions, extract_question_index_from_query
from src.llm.prompts import QUIZ_REVISION_QUERY_PROMPT
from src.rag.context_builder import ContextBuilder
from src.rag.rag_service import RAGService
from src.utils.error_handling import safe_execute, user_facing_error_message

logger = logging.getLogger("chatbot.quiz_service")

_QUERY_STOPWORDS = {
    "cho", "tao", "tạo", "sinh", "cau", "câu", "hoi", "hỏi", "trac", "trắc",
    "nghiem", "nghiệm", "dien", "điền", "khuyet", "khuyết", "ve", "về", "va",
    "và", "he", "hệ", "quan", "quản", "tri", "trị", "co", "cơ", "so", "sở",
    "du", "dữ", "lieu", "liệu", "mcq", "fill", "blank", "true", "false",
    "hay", "bai", "bài", "lop", "lớp", "bo", "bộ", "sach", "sách",
}


class QuizService:

    def __init__(self, question_handlers: dict, rag_service: RAGService):
        self.question_handlers = question_handlers
        self.rag_service = rag_service
        self.scorer = QuestionScorer()
        self.validator = QuestionValidator()
        self.explain_handler = ExplainHandler()
        self.student_tracker = StudentTracker()
        self.context_builder = ContextBuilder()

    # ────────────────────────────────────────────────────────
    # GENERATE QUIZ (sync)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi sinh câu hỏi", log_prefix="QuizService.generate")
    def generate_quiz(
        self, ctx: RequestContext, task_type: str
    ) -> Generator[str, None, None]:
        session = ctx.session
        query = ctx.enriched_query

        yield "Đang tìm kiếm tài liệu liên quan..."

        # RAG Search
        t0 = time.time()
        contexts = self.rag_service.get_context(ctx, intent_hint="generate")
        rag_time = time.time() - t0
        logger.info(f"RAG Search: {len(contexts)} chunks ({rag_time:.2f}s)")

        if not contexts:
            yield "Không tìm thấy tài liệu phù hợp để tạo câu hỏi."
            return

        if ctx.scope_fallback_notice:
            yield ctx.scope_fallback_notice

        if self._should_block_generation_for_irrelevant_context(ctx, query, contexts):
            ctx.add_debug_step(
                "QuizContextGuard",
                status="blocked",
                reason="fallback_context_not_relevant",
                rag_chunks=len(contexts),
            )
            yield (
                "Mình đã mở rộng tìm kiếm ra toàn bộ SGK nhưng vẫn chưa tìm thấy tài liệu "
                "đủ liên quan tới yêu cầu này để tạo câu hỏi đáng tin cậy. "
                "Bạn thử đổi sang chủ đề có trong SGK hoặc cung cấp thêm nội dung nguồn nhé."
            )
            return

        context_text = self.context_builder.build(
            query=query, chunks=contexts, action="generate_quiz"
        )
        handler = self.question_handlers.get(task_type, self.question_handlers["mcq"])
        num_q = (
            ctx.extracted_params.get("question_count")
            or extract_num_questions(ctx.query)
            or extract_num_questions(query)
            or 3
        )
        logger.info(f"Generate: type={task_type}, num={num_q}")

        yield f"Đang soạn {num_q} câu hỏi {task_type.upper()}..."

        # Retry loop
        max_retries = 2
        for attempt in range(max_retries):
            try:
                t1 = time.time()
                raw_questions = handler.handle(query, context_text, num_questions=num_q)
                gen_time = time.time() - t1
                logger.info(f"Handler.handle() -> {gen_time:.2f}s (attempt {attempt+1})")

                if raw_questions is None:
                    logger.warning(f"Handler returned None (attempt {attempt+1})")
                    yield "Lỗi khi sinh câu hỏi. Đang thử lại..."
                    continue

                quality_reviewer = get_quality_reviewer(f"quiz:{task_type}")
                quality_review = quality_reviewer.review(
                    query=query,
                    context=context_text,
                    output=raw_questions.model_dump(),
                )
                reflection_attempts = 0

                if quality_review.reflection_action == "revise_quiz":
                    reflection_attempts = 1
                    revised_query = QUIZ_REVISION_QUERY_PROMPT.format(
                        query=query,
                        revision_instruction=(
                            quality_review.revision_instruction or quality_review.summary
                        ),
                    )
                    raw_questions = handler.handle(revised_query, context_text, num_questions=num_q)
                    if raw_questions is None:
                        yield "Câu hỏi chưa đạt chất lượng sau reflection. Bạn thử hỏi cụ thể hơn nhé!"
                        continue
                    quality_review = quality_reviewer.review(
                        query=query,
                        context=context_text,
                        output=raw_questions.model_dump(),
                    )

                ctx.add_debug_step(
                    "QualityReviewer",
                    target=f"quiz:{task_type}",
                    passed=quality_review.passed,
                    score=quality_review.score,
                    reason_fail=quality_review.reason_fail,
                    summary=quality_review.summary,
                    reflection_action=quality_review.reflection_action,
                    reflection_attempts=reflection_attempts,
                    issues=[issue.model_dump() for issue in quality_review.issues],
                )

                if quality_review.reflection_action in ("block", "ask_human") or not quality_review.passed:
                    logger.warning(
                        "Quality review failed: reason=%s summary=%s",
                        quality_review.reason_fail,
                        quality_review.summary,
                    )
                    if attempt == max_retries - 1:
                        yield "Câu hỏi chưa đạt chất lượng. Bạn thử hỏi cụ thể hơn hoặc cung cấp thêm tài liệu nguồn nhé."
                    continue

                # Validate
                yield "Đang kiểm duyệt chất lượng..."
                t2 = time.time()
                validation_result = self.validator.validate(
                    question_type=task_type,
                    context=context_text,
                    questions_json=json.dumps(raw_questions.model_dump()),
                )
                val_time = time.time() - t2
                logger.info(
                    f"Validator: all_valid={validation_result.all_valid}, "
                    f"approved={len(validation_result.approved_questions)} ({val_time:.2f}s)"
                )

                if validation_result.all_valid or validation_result.approved_questions:
                    # Create QuizRound
                    quiz_state = session.ensure_quiz_state()
                    quiz_round = quiz_state.create_round(
                        question_type=task_type,
                        query=query,
                    )

                    for i, q_data in enumerate(validation_result.approved_questions):
                        record = QuestionRecord(
                            question_id=f"r{quiz_round.round_id}_q{i}",
                            question_type=task_type,
                            content=q_data,
                            source="quiz",
                        )
                        quiz_round.questions.append(record)

                    logger.info(
                        f"Saved {len(quiz_round.questions)} questions to "
                        f"round {quiz_round.round_id}"
                    )

                    # Display
                    display = raw_questions.to_display_format()
                    session.add_message("assistant", display)
                    yield "\n\n" + display
                    yield (
                        "\n\nMình đã lưu bộ câu hỏi này trong phiên hiện tại. "
                        "Khi bạn sẵn sàng, hãy gửi đáp án theo dạng `1A 2B 3C` nhé."
                    )

                    ctx.add_debug_step(
                        "Handler",
                        handler=handler.__class__.__name__,
                        action="generate_quiz",
                        task_type=task_type,
                        num_questions=num_q,
                        rag_chunks=len(contexts),
                        rag_time_s=round(rag_time, 2),
                        generation_time_s=round(gen_time, 2),
                        generation_attempts=attempt + 1,
                        validator_all_valid=validation_result.all_valid,
                        validator_approved=len(validation_result.approved_questions),
                        validator_time_s=round(val_time, 2),
                        questions_saved=len(quiz_round.questions),
                        round_id=quiz_round.round_id,
                        status="success",
                    )
                    return  # Success — exit retry loop
                else:
                    logger.warning(f"Validation FAILED (attempt {attempt+1})")
                    if attempt == max_retries - 1:
                        ctx.add_debug_step(
                            "Handler", action="generate_quiz",
                            status="validation_failed", attempts=max_retries,
                        )
                        yield "Hệ thống đang gặp khó khăn khi tạo câu hỏi. Bạn thử hỏi cụ thể hơn nhé!"

            except Exception as e:
                logger.error(f"Exception (attempt {attempt+1}): {e}", exc_info=True)
                if attempt == max_retries - 1:
                    ctx.add_debug_step(
                        "Handler", action="generate_quiz",
                        status="error", error=str(e)[:200],
                    )
                    yield f"Lỗi sinh câu hỏi. {user_facing_error_message(e)}"

    # ────────────────────────────────────────────────────────
    # CHECK ANSWER (sync)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi chấm điểm", log_prefix="QuizService.check_answer")
    def check_answer(
        self, ctx: RequestContext, original_query: str
    ) -> Generator[str, None, None]:
        session = ctx.session
        all_questions = session.get_all_question_records()

        if not all_questions:
            yield "Bạn chưa có câu hỏi nào. Hãy yêu cầu tạo câu hỏi trước nhé!"
            return

        yield "Đang chấm điểm..."

        direct_msg = self._try_grade_direct_mcq_answers(
            session=session,
            questions=all_questions,
            original_query=original_query,
            ctx=ctx,
        )
        if direct_msg:
            yield direct_msg
            return

        task_items = [q.to_task_item() for q in all_questions]

        t0 = time.time()
        result = self.scorer.handle(original_query, task_items)
        score_time = time.time() - t0
        logger.info(
            f"Scorer: status={result.status}, correct={result.is_correct}, "
            f"score={result.score} ({score_time:.2f}s)"
        )

        if result.status == "found":
            # Update QuestionRecord
            if result.question_index is not None and result.question_index < len(all_questions):
                record = all_questions[result.question_index]
                record.record_attempt(
                    user_answer=result.user_answer,
                    is_correct=result.is_correct or False,
                    score=result.score,
                )

                # Track to StudentProfile
                # score: 0-10 or 0-1, StudentProfile auto-normalizes
                score = result.score if result.score is not None else (1.0 if result.is_correct else 0.0)
                self.student_tracker.record_attempt(
                    user_id=session.user_id,
                    topic=session.topic or "Chung",
                    score=score,
                )

            # Response
            icon = "Chính xác!" if result.is_correct else "Sai rồi!"
            msg = f"\n\n{icon} {result.explanation or ''}"
            if result.score is not None:
                msg += f"\nĐiểm số: {result.score}/10"

            session.add_message("assistant", msg)
            yield msg

            # Periodic summary
            if session.quiz_state:
                answered = session.quiz_state.total_answered
                if answered > 0 and answered % 3 == 0:
                    summary = session.quiz_state.get_summary()
                    yield "\n\n---\n" + summary

            ctx.add_debug_step(
                "Handler", action="check_answer", status="found",
                scorer_time_s=round(score_time, 2),
                is_correct=result.is_correct,
                score=result.score,
                question_index=result.question_index,
            )
        else:
            ctx.add_debug_step(
                "Handler", action="check_answer", status="not_found",
                scorer_time_s=round(score_time, 2),
            )
            yield f"\nKhông thể xác định câu trả lời. {result.explanation or 'Vui lòng nói rõ hơn.'}"

    # ────────────────────────────────────────────────────────
    # REVIEW WRONG (sync)
    # ────────────────────────────────────────────────────────

    def review_wrong(
        self, ctx: RequestContext, original_query: str, round_id: Optional[int] = None
    ) -> Generator[str, None, None]:
        session = ctx.session
        quiz_state = session.quiz_state

        if not quiz_state:
            yield "Bạn chưa có câu hỏi nào để ôn tập."
            return

        wrong = quiz_state.get_wrong_questions(round_id=round_id)

        if not wrong:
            if round_id is not None:
                yield f"Không có câu sai nào trong round {round_id + 1}!"
            else:
                yield "Bạn chưa có câu sai nào. Tuyệt vời!"
            return

        # Create review round
        source_ids = [round_id] if round_id is not None else None
        review_round = quiz_state.create_review_round(source_round_ids=source_ids)

        if not review_round:
            yield "Không tạo được bài ôn tập."
            return

        # Display
        lines = []
        round_label = f"round {round_id + 1}" if round_id is not None else "tất cả các round"
        lines.append(f"ÔN TẬP CÂU SAI ({round_label}): {len(review_round.questions)} câu\n")

        for q in review_round.questions:
            content = q.content
            q_type = q.question_type

            if q_type == "mcq":
                lines.append(f"Câu hỏi: {content.get('question', '')}")
                options = content.get("options", {})
                if isinstance(options, dict):
                    for key, val in options.items():
                        lines.append(f"  {key}. {val}")
                lines.append("")
            elif q_type == "true_false":
                lines.append(f"Mệnh đề: {content.get('statement', '')}")
                lines.append("  -> Đúng hay Sai?")
                lines.append("")
            elif q_type == "fill_blank":
                lines.append(f"Điền khuyết: {content.get('text_with_blanks', '')}")
                lines.append("")
            elif q_type == "essay":
                lines.append(f"Câu hỏi: {content.get('question', '')}")
                lines.append("")

            lines.append("_" * 40)
            lines.append("")

        display = "\n".join(lines)
        session.add_message("assistant", display)
        ctx.add_debug_step(
            "Handler", action="review_wrong", status="success",
            round_id=round_id,
            wrong_questions=len(wrong),
            review_questions=len(review_round.questions),
        )
        yield display

    # ────────────────────────────────────────────────────────
    # GET STATS (sync)
    # ────────────────────────────────────────────────────────

    def get_stats(self, ctx: RequestContext) -> Generator[str, None, None]:
        session = ctx.session
        lines = []

        if session.quiz_state:
            lines.append(session.quiz_state.get_summary())

        if session.slide_state and session.slide_state.has_exercises:
            ss = session.slide_state
            lines.append(
                f"\nBài tập slide: {ss.correct_exercises}/{ss.total_exercises} đúng"
            )
            wrong_ex = ss.get_wrong_exercises()
            if wrong_ex:
                lines.append(f"Câu sai: {len(wrong_ex)}")

        if not lines:
            yield "Chưa có dữ liệu học tập trong phiên này."
            return

        ctx.add_debug_step(
            "Handler", action="get_stats", status="success",
            has_quiz=session.quiz_state is not None,
            has_slide_exercises=bool(session.slide_state and session.slide_state.has_exercises),
        )
        yield "\n".join(lines)

    # ────────────────────────────────────────────────────────
    # EXPLAIN QUESTION (sync)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi giải thích", log_prefix="QuizService.explain_question")
    def explain_question(
        self, ctx: RequestContext, original_query: str
    ) -> Generator[str, None, None]:
        session = ctx.session
        all_questions = session.get_all_question_records()

        if not all_questions:
            # Fallback: không có câu hỏi → trả về None để dispatcher xử lý
            yield None
            return

        stored_response = self._stored_question_explanation(original_query, all_questions)
        if stored_response:
            session.add_message("assistant", stored_response)
            ctx.add_debug_step(
                "Handler", action="explain_question", status="success",
                source="stored_explanation",
                questions_available=len(all_questions),
                response_length=len(stored_response),
            )
            yield "\n\n" + stored_response
            return

        q_context = "\n".join(
            f"Câu {i+1}: {q.content.get('question', q.content.get('statement', ''))}"
            for i, q in enumerate(all_questions[-5:])
        )

        full_context = f"Các câu hỏi trong session:\n{q_context}"
        t0 = time.time()
        response = self.explain_handler.handle(original_query, context=full_context)
        explain_time = time.time() - t0

        session.add_message("assistant", response)
        ctx.add_debug_step(
            "Handler", action="explain_question", status="success",
            questions_available=len(all_questions),
            explain_time_s=round(explain_time, 2),
            response_length=len(response),
        )
        yield "\n\n" + response

    # ────────────────────────────────────────────────────────
    # GENERATE QUIZ (async)
    # ────────────────────────────────────────────────────────

    @safe_execute(fallback_message="Lỗi sinh câu hỏi", log_prefix="QuizService.generate_async")
    async def generate_quiz_async(
        self, ctx: RequestContext, task_type: str
    ) -> AsyncGenerator[str, None]:
        session = ctx.session
        query = ctx.enriched_query

        yield "Đang tìm kiếm tài liệu liên quan..."

        # RAG Search (async)
        t0 = time.time()
        contexts = await self.rag_service.get_context_async(ctx, intent_hint="generate")
        rag_time = time.time() - t0
        logger.info(f"RAG Search: {len(contexts)} chunks ({rag_time:.2f}s)")

        if not contexts:
            yield "Không tìm thấy tài liệu phù hợp để tạo câu hỏi."
            return

        if ctx.scope_fallback_notice:
            yield ctx.scope_fallback_notice

        if self._should_block_generation_for_irrelevant_context(ctx, query, contexts):
            ctx.add_debug_step(
                "QuizContextGuard",
                status="blocked",
                reason="fallback_context_not_relevant",
                rag_chunks=len(contexts),
            )
            yield (
                "Mình đã mở rộng tìm kiếm ra toàn bộ SGK nhưng vẫn chưa tìm thấy tài liệu "
                "đủ liên quan tới yêu cầu này để tạo câu hỏi đáng tin cậy. "
                "Bạn thử đổi sang chủ đề có trong SGK hoặc cung cấp thêm nội dung nguồn nhé."
            )
            return

        context_text = await self.context_builder.build_async(
            query=query, chunks=contexts, action="generate_quiz"
        )
        handler = self.question_handlers.get(task_type, self.question_handlers["mcq"])
        num_q = (
            ctx.extracted_params.get("question_count")
            or extract_num_questions(ctx.query)
            or extract_num_questions(query)
            or 3
        )
        logger.info(f"Generate: type={task_type}, num={num_q}")

        yield f"Đang soạn {num_q} câu hỏi {task_type.upper()}..."

        # Retry loop
        max_retries = 2
        for attempt in range(max_retries):
            try:
                t1 = time.time()
                raw_questions = await handler.handle_async(query, context_text, num_questions=num_q)
                gen_time = time.time() - t1
                logger.info(f"Handler.handle_async() -> {gen_time:.2f}s (attempt {attempt+1})")

                if raw_questions is None:
                    logger.warning(f"Handler returned None (attempt {attempt+1})")
                    yield "Lỗi khi sinh câu hỏi. Đang thử lại..."
                    continue

                yield "Đang kiểm duyệt chất lượng..."
                quality_reviewer = get_quality_reviewer(f"quiz:{task_type}")
                questions_json = json.dumps(raw_questions.model_dump())
                t2 = time.time()
                quality_review, validation_result = await asyncio.gather(
                    quality_reviewer.review_async(
                        query=query,
                        context=context_text,
                        output=raw_questions.model_dump(),
                    ),
                    self.validator.validate_async(
                        question_type=task_type,
                        context=context_text,
                        questions_json=questions_json,
                    ),
                )
                val_time = time.time() - t2
                reflection_attempts = 0

                if quality_review.reflection_action == "revise_quiz":
                    reflection_attempts = 1
                    revised_query = QUIZ_REVISION_QUERY_PROMPT.format(
                        query=query,
                        revision_instruction=(
                            quality_review.revision_instruction or quality_review.summary
                        ),
                    )
                    raw_questions = await handler.handle_async(
                        revised_query,
                        context_text,
                        num_questions=num_q,
                    )
                    if raw_questions is None:
                        yield "Câu hỏi chưa đạt chất lượng sau reflection. Bạn thử hỏi cụ thể hơn nhé!"
                        continue
                    quality_review = await quality_reviewer.review_async(
                        query=query,
                        context=context_text,
                        output=raw_questions.model_dump(),
                    )
                    t2 = time.time()
                    validation_result = await self.validator.validate_async(
                        question_type=task_type,
                        context=context_text,
                        questions_json=json.dumps(raw_questions.model_dump()),
                    )
                    val_time += time.time() - t2

                ctx.add_debug_step(
                    "QualityReviewer",
                    target=f"quiz:{task_type}",
                    passed=quality_review.passed,
                    score=quality_review.score,
                    reason_fail=quality_review.reason_fail,
                    summary=quality_review.summary,
                    reflection_action=quality_review.reflection_action,
                    reflection_attempts=reflection_attempts,
                    issues=[issue.model_dump() for issue in quality_review.issues],
                )

                if quality_review.reflection_action in ("block", "ask_human") or not quality_review.passed:
                    logger.warning(
                        "Quality review failed: reason=%s summary=%s",
                        quality_review.reason_fail,
                        quality_review.summary,
                    )
                    if attempt == max_retries - 1:
                        yield "Câu hỏi chưa đạt chất lượng. Bạn thử hỏi cụ thể hơn hoặc cung cấp thêm tài liệu nguồn nhé."
                    continue

                logger.info(
                    f"Validator: all_valid={validation_result.all_valid}, "
                    f"approved={len(validation_result.approved_questions)} ({val_time:.2f}s)"
                )

                if validation_result.all_valid or validation_result.approved_questions:
                    # Create QuizRound
                    quiz_state = session.ensure_quiz_state()
                    quiz_round = quiz_state.create_round(
                        question_type=task_type,
                        query=query,
                    )

                    for i, q_data in enumerate(validation_result.approved_questions):
                        record = QuestionRecord(
                            question_id=f"r{quiz_round.round_id}_q{i}",
                            question_type=task_type,
                            content=q_data,
                            source="quiz",
                        )
                        quiz_round.questions.append(record)

                    logger.info(
                        f"Saved {len(quiz_round.questions)} questions to "
                        f"round {quiz_round.round_id}"
                    )

                    # Display
                    display = raw_questions.to_display_format()
                    session.add_message("assistant", display)
                    yield "\n\n" + display
                    yield (
                        "\n\nMình đã lưu bộ câu hỏi này trong phiên hiện tại. "
                        "Khi bạn sẵn sàng, hãy gửi đáp án theo dạng `1A 2B 3C` nhé."
                    )

                    ctx.add_debug_step(
                        "Handler",
                        handler=handler.__class__.__name__,
                        action="generate_quiz",
                        task_type=task_type,
                        num_questions=num_q,
                        rag_chunks=len(contexts),
                        rag_time_s=round(rag_time, 2),
                        generation_time_s=round(gen_time, 2),
                        generation_attempts=attempt + 1,
                        validator_all_valid=validation_result.all_valid,
                        validator_approved=len(validation_result.approved_questions),
                        validator_time_s=round(val_time, 2),
                        questions_saved=len(quiz_round.questions),
                        round_id=quiz_round.round_id,
                        status="success",
                    )
                    return  # Success — exit retry loop
                else:
                    logger.warning(f"Validation FAILED (attempt {attempt+1})")
                    if attempt == max_retries - 1:
                        ctx.add_debug_step(
                            "Handler", action="generate_quiz",
                            status="validation_failed", attempts=max_retries,
                        )
                        yield "Hệ thống đang gặp khó khăn khi tạo câu hỏi. Bạn thử hỏi cụ thể hơn nhé!"

            except Exception as e:
                logger.error(f"Exception (attempt {attempt+1}): {e}", exc_info=True)
                if attempt == max_retries - 1:
                    ctx.add_debug_step(
                        "Handler", action="generate_quiz",
                        status="error", error=str(e)[:200],
                    )
                    yield f"Lỗi sinh câu hỏi. {user_facing_error_message(e)}"

    # ────────────────────────────────────────────────────────
    # CHECK ANSWER (async)
    # ────────────────────────────────────────────────────────

    async def check_answer_async(
        self, ctx: RequestContext, original_query: str
    ) -> AsyncGenerator[str, None]:
        session = ctx.session
        all_questions = session.get_all_question_records()

        if not all_questions:
            yield "Bạn chưa có câu hỏi nào. Hãy yêu cầu tạo câu hỏi trước nhé!"
            return

        yield "Đang chấm điểm..."

        direct_msg = self._try_grade_direct_mcq_answers(
            session=session,
            questions=all_questions,
            original_query=original_query,
            ctx=ctx,
        )
        if direct_msg:
            yield direct_msg
            return

        task_items = [q.to_task_item() for q in all_questions]

        t0 = time.time()
        timeout_s = getattr(self.scorer, "timeout_seconds", 20)
        try:
            result = await asyncio.wait_for(
                self.scorer.handle_async(original_query, task_items),
                timeout=timeout_s,
            )
        except asyncio.TimeoutError:
            score_time = time.time() - t0
            logger.warning("Scorer timed out after %.2fs", score_time)
            ctx.add_debug_step(
                "Handler",
                action="check_answer",
                status="scorer_timeout",
                scorer_time_s=round(score_time, 2),
            )
            yield "\nKhông chấm được câu trả lời vì scorer quá thời gian. Bạn thử gửi lại đáp án theo mẫu: câu 1 A, câu 2 B."
            return
        score_time = time.time() - t0
        logger.info(
            f"Scorer: status={result.status}, correct={result.is_correct}, "
            f"score={result.score} ({score_time:.2f}s)"
        )

        if result.status == "found":
            # Update QuestionRecord
            if result.question_index is not None and result.question_index < len(all_questions):
                record = all_questions[result.question_index]
                record.record_attempt(
                    user_answer=result.user_answer,
                    is_correct=result.is_correct or False,
                    score=result.score,
                )

                # Track to StudentProfile
                score = result.score if result.score is not None else (1.0 if result.is_correct else 0.0)
                self.student_tracker.record_attempt(
                    user_id=session.user_id,
                    topic=session.topic or "Chung",
                    score=score,
                )

            # Response
            icon = "Chính xác!" if result.is_correct else "Sai rồi!"
            msg = f"\n\n{icon} {result.explanation or ''}"
            if result.score is not None:
                msg += f"\nĐiểm số: {result.score}/10"

            session.add_message("assistant", msg)
            yield msg

            # Periodic summary
            if session.quiz_state:
                answered = session.quiz_state.total_answered
                if answered > 0 and answered % 3 == 0:
                    summary = session.quiz_state.get_summary()
                    yield "\n\n---\n" + summary

            ctx.add_debug_step(
                "Handler", action="check_answer", status="found",
                scorer_time_s=round(score_time, 2),
                is_correct=result.is_correct,
                score=result.score,
                question_index=result.question_index,
            )
        else:
            ctx.add_debug_step(
                "Handler", action="check_answer", status="not_found",
                scorer_time_s=round(score_time, 2),
            )
            yield f"\nKhông thể xác định câu trả lời. {result.explanation or 'Vui lòng nói rõ hơn.'}"

    def _try_grade_direct_mcq_answers(
        self,
        session: Session,
        questions: List[QuestionRecord],
        original_query: str,
        ctx: RequestContext,
    ) -> Optional[str]:
        answers = self._extract_direct_mcq_answers(
            original_query,
            total_questions=len(questions),
        )
        if not answers:
            return None

        graded = []
        skipped = []
        for display_index, user_answer in answers:
            question_index = display_index - 1
            if question_index < 0 or question_index >= len(questions):
                skipped.append({
                    "question_display_index": display_index,
                    "user_answer": user_answer,
                    "reason": "question_index_out_of_range",
                })
                continue

            record = questions[question_index]
            if record.question_type != "mcq":
                skipped.append({
                    "question_display_index": display_index,
                    "question_id": record.question_id,
                    "question_type": record.question_type,
                    "user_answer": user_answer,
                    "reason": "not_mcq",
                })
                continue

            correct_answer = str(record.content.get("correct_answer", "")).strip().upper()
            if correct_answer not in {"A", "B", "C", "D"}:
                skipped.append({
                    "question_display_index": display_index,
                    "question_id": record.question_id,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "reason": "invalid_correct_answer",
                })
                continue

            is_correct = user_answer == correct_answer
            record.record_attempt(
                user_answer=user_answer,
                is_correct=is_correct,
                score=1.0 if is_correct else 0.0,
            )
            self.student_tracker.record_attempt(
                user_id=session.user_id,
                topic=session.topic or "Chung",
                score=1.0 if is_correct else 0.0,
            )
            graded.append((display_index, user_answer, correct_answer, is_correct))

        if not graded:
            ctx.add_debug_step(
                "DirectMCQAnswerParser",
                status="parsed_but_not_graded",
                raw_query=original_query,
                parsed_answers=[
                    {"question_display_index": idx, "user_answer": ans}
                    for idx, ans in answers
                ],
                skipped=skipped,
            )
            return None

        correct_count = sum(1 for _, _, _, is_correct in graded if is_correct)
        lines = [f"\n\nĐã chấm {len(graded)} câu: {correct_count}/{len(graded)} đúng."]
        for display_index, user_answer, correct_answer, is_correct in graded:
            status = "Đúng" if is_correct else "Sai"
            lines.append(
                f"Câu {display_index}: {status} - bạn chọn {user_answer}, đáp án đúng {correct_answer}."
            )

        msg = "\n".join(lines)
        session.add_message("assistant", msg)
        ctx.add_debug_step(
            "DirectMCQAnswerParser",
            status="graded",
            raw_query=original_query,
            parsed_answers=[
                {"question_display_index": idx, "user_answer": ans}
                for idx, ans in answers
            ],
            graded_answers=[
                {
                    "question_display_index": display_index,
                    "question_record_index": display_index - 1,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct,
                }
                for display_index, user_answer, correct_answer, is_correct in graded
            ],
            skipped=skipped,
        )
        ctx.add_debug_step(
            "Handler",
            action="check_answer",
            status="direct_mcq",
            answers_detected=len(answers),
            answers_graded=len(graded),
            correct=correct_count,
        )
        return msg

    @classmethod
    def _extract_direct_mcq_answers(
        cls,
        text: str,
        total_questions: Optional[int] = None,
    ) -> List[tuple[int, str]]:
        raw = text or ""
        max_index = total_questions or 99

        explicit = cls._extract_indexed_answers(
            raw,
            patterns=[
                r"(?:câu|cau|question|ques|q)\s*(\d{1,2})\s*[:.)-]?\s*(?:đáp\s*án|dap\s*an|chọn|chon|là|la|=)?\s*([ABCD])\b",
                r"\b(\d{1,2})\s*[:.)-]\s*(?:đáp\s*án|dap\s*an|chọn|chon|là|la|=)?\s*([ABCD])\b",
                r"\b(\d{1,2})\s*([ABCD])\b",
            ],
            max_index=max_index,
        )
        if explicit:
            return explicit

        sequential = cls._extract_sequential_answers(raw, max_index=max_index)
        if sequential:
            return sequential
        return []

    @staticmethod
    def _extract_indexed_answers(
        text: str,
        patterns: List[str],
        max_index: int,
    ) -> List[tuple[int, str]]:
        answers_by_index: Dict[int, str] = {}
        for pattern in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                display_index = int(match.group(1))
                if display_index < 1 or display_index > max_index:
                    continue
                answers_by_index[display_index] = match.group(2).upper()

        return sorted(answers_by_index.items())

    @staticmethod
    def _extract_sequential_answers(text: str, max_index: int) -> List[tuple[int, str]]:
        cleaned = re.sub(
            r"\b(?:đáp\s*án|dap\s*an|answer|answers|em\s*chọn|em\s*chon|chọn|chon|là|la)\b",
            " ",
            text or "",
            flags=re.IGNORECASE,
        )
        tokens = re.findall(r"\b[ABCD]\b", cleaned.upper())
        if not tokens or len(tokens) > max_index:
            return []

        non_answer_text = re.sub(r"\b[ABCD]\b", " ", cleaned.upper())
        non_answer_text = re.sub(r"[\s,;:.()\\/_|+-]+", " ", non_answer_text).strip()
        if non_answer_text:
            return []

        return [(idx + 1, answer) for idx, answer in enumerate(tokens)]

    def _should_block_generation_for_irrelevant_context(
        self,
        ctx: RequestContext,
        query: str,
        contexts: List[Dict],
    ) -> bool:
        if not ctx.scope_fallback_used or not contexts:
            return False

        terms = self._important_query_terms(query)
        if ctx.intent_result and ctx.intent_result.topic:
            terms.update(self._important_query_terms(ctx.intent_result.topic))

        if not terms:
            return False

        joined = " ".join(
            " ".join(
                str(part or "")
                for part in (
                    chunk.get("content"),
                    chunk.get("context"),
                    chunk.get("metadata", {}).get("topic_name"),
                    chunk.get("metadata", {}).get("lesson_name"),
                )
            ).lower()
            for chunk in contexts
        )
        matches = {term for term in terms if term in joined}
        logger.info(
            "Quiz context relevance | terms=%s matches=%s fallback=%s",
            sorted(terms),
            sorted(matches),
            ctx.scope_fallback_used,
        )
        return len(matches) == 0

    @staticmethod
    def _important_query_terms(text: str) -> set:
        normalized = (text or "").lower()
        tokens = re.findall(r"[a-zA-Z0-9À-ỹ]+", normalized)
        return {
            token
            for token in tokens
            if len(token) >= 3 and token not in _QUERY_STOPWORDS
        }

    # ────────────────────────────────────────────────────────
    # REVIEW WRONG (async)
    # ────────────────────────────────────────────────────────

    async def review_wrong_async(
        self, ctx: RequestContext, original_query: str, round_id: Optional[int] = None
    ) -> AsyncGenerator[str, None]:
        session = ctx.session
        quiz_state = session.quiz_state

        if not quiz_state:
            yield "Bạn chưa có câu hỏi nào để ôn tập."
            return

        wrong = quiz_state.get_wrong_questions(round_id=round_id)

        if not wrong:
            if round_id is not None:
                yield f"Không có câu sai nào trong round {round_id + 1}!"
            else:
                yield "Bạn chưa có câu sai nào. Tuyệt vời!"
            return

        # Create review round
        source_ids = [round_id] if round_id is not None else None
        review_round = quiz_state.create_review_round(source_round_ids=source_ids)

        if not review_round:
            yield "Không tạo được bài ôn tập."
            return

        # Display
        lines = []
        round_label = f"round {round_id + 1}" if round_id is not None else "tất cả các round"
        lines.append(f"ÔN TẬP CÂU SAI ({round_label}): {len(review_round.questions)} câu\n")

        for q in review_round.questions:
            content = q.content
            q_type = q.question_type

            if q_type == "mcq":
                lines.append(f"Câu hỏi: {content.get('question', '')}")
                options = content.get("options", {})
                if isinstance(options, dict):
                    for key, val in options.items():
                        lines.append(f"  {key}. {val}")
                lines.append("")
            elif q_type == "true_false":
                lines.append(f"Mệnh đề: {content.get('statement', '')}")
                lines.append("  -> Đúng hay Sai?")
                lines.append("")
            elif q_type == "fill_blank":
                lines.append(f"Điền khuyết: {content.get('text_with_blanks', '')}")
                lines.append("")
            elif q_type == "essay":
                lines.append(f"Câu hỏi: {content.get('question', '')}")
                lines.append("")

            lines.append("_" * 40)
            lines.append("")

        display = "\n".join(lines)
        session.add_message("assistant", display)
        ctx.add_debug_step(
            "Handler", action="review_wrong", status="success",
            round_id=round_id,
            wrong_questions=len(wrong),
            review_questions=len(review_round.questions),
        )
        yield display

    # ────────────────────────────────────────────────────────
    # GET STATS (async)
    # ────────────────────────────────────────────────────────

    async def get_stats_async(self, ctx: RequestContext) -> AsyncGenerator[str, None]:
        session = ctx.session
        lines = []

        if session.quiz_state:
            lines.append(session.quiz_state.get_summary())

        if session.slide_state and session.slide_state.has_exercises:
            ss = session.slide_state
            lines.append(
                f"\nBài tập slide: {ss.correct_exercises}/{ss.total_exercises} đúng"
            )
            wrong_ex = ss.get_wrong_exercises()
            if wrong_ex:
                lines.append(f"Câu sai: {len(wrong_ex)}")

        if not lines:
            yield "Chưa có dữ liệu học tập trong phiên này."
            return

        ctx.add_debug_step(
            "Handler", action="get_stats", status="success",
            has_quiz=session.quiz_state is not None,
            has_slide_exercises=bool(session.slide_state and session.slide_state.has_exercises),
        )
        yield "\n".join(lines)

    # ────────────────────────────────────────────────────────
    # EXPLAIN QUESTION (async)
    # ────────────────────────────────────────────────────────

    async def explain_question_async(
        self, ctx: RequestContext, original_query: str
    ) -> AsyncGenerator[str, None]:
        session = ctx.session
        all_questions = session.get_all_question_records()

        if not all_questions:
            # Fallback: không có câu hỏi → trả về None để dispatcher xử lý
            yield None
            return

        stored_response = self._stored_question_explanation(original_query, all_questions)
        if stored_response:
            session.add_message("assistant", stored_response)
            ctx.add_debug_step(
                "Handler", action="explain_question", status="success",
                source="stored_explanation",
                questions_available=len(all_questions),
                response_length=len(stored_response),
            )
            yield "\n\n" + stored_response
            return

        q_context = "\n".join(
            f"Câu {i+1}: {q.content.get('question', q.content.get('statement', ''))}"
            for i, q in enumerate(all_questions[-5:])
        )

        full_context = f"Các câu hỏi trong session:\n{q_context}"
        t0 = time.time()
        response = await self.explain_handler.handle_async(original_query, context=full_context)
        explain_time = time.time() - t0

        session.add_message("assistant", response)
        ctx.add_debug_step(
            "Handler", action="explain_question", status="success",
            questions_available=len(all_questions),
            explain_time_s=round(explain_time, 2),
            response_length=len(response),
        )
        yield "\n\n" + response

    @staticmethod
    def _stored_question_explanation(
        original_query: str,
        questions: List[QuestionRecord],
    ) -> Optional[str]:
        if not questions:
            return None

        question_index = extract_question_index_from_query(original_query)
        if question_index is not None:
            if question_index < 1 or question_index > len(questions):
                return None
            record = questions[question_index - 1]
            display_index = question_index
        else:
            record = questions[-1]
            display_index = len(questions)

        content = record.content or {}
        explanation = str(content.get("explanation") or "").strip()
        if not explanation:
            return None

        question_text = (
            content.get("question")
            or content.get("statement")
            or content.get("prompt")
            or ""
        )
        correct_answer = (
            content.get("correct_answer")
            or content.get("answer")
            or content.get("correct")
        )

        lines = [f"**Giải thích câu {display_index}:**"]
        if question_text:
            lines.append(str(question_text).strip())
        if correct_answer:
            lines.append(f"Đáp án đúng: {correct_answer}")
        lines.append(explanation)
        return "\n\n".join(lines)


__all__ = ["QuizService"]
