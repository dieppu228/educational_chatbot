"""
Orchestrator v2 — Code-Level Orchestrator for EduBot.

Replaces the monolithic ChatBot class with a clean architecture:
    IntentRouter → SessionManager → ActionPlanner → Handler → SessionStore

conversation.py (ChatBot) is kept for backward compatibility.
"""

import re
import json
import time
import logging
from typing import Generator, Optional, List, Dict
from pathlib import Path

from src.config.config import settings

# Core components
from src.llm.intent_router import IntentRouter, IntentResult
from src.llm.action_planner import ActionPlanner, ActionPlan, Action
from src.llm.session_manager import SessionManager
from src.llm.session_store import SessionStore
from src.llm.memory import (
    MemoryManager, Session, QuestionRecord, QuizRound,
    QuizSessionState, SlideSessionState
)
from src.llm.context_analyzer import ContextAnalyzer

# Handlers
from src.llm.handlers.question.mcq_handler import MCQHandler
from src.llm.handlers.question.essay_handler import EssayHandler
from src.llm.handlers.question.fill_handler import FillHandler
from src.llm.handlers.question.true_false_handler import TrueFalseHandler
from src.llm.handlers.question.scorer import QuestionScorer
from src.llm.handlers.chat_handler import ChatHandler
from src.llm.handlers.explain_handler import ExplainHandler
from src.llm.handlers.content.slide_handler import SlideHandler
from src.llm.handlers.content.slide_template import SlideTemplate
from src.llm.validators.question_validator import QuestionValidator
from src.llm.knowledge_map import KnowledgeMap
from src.llm.student_tracker import StudentTracker
from src.llm.utils import extract_num_questions, format_contexts
from src.rag.adaptive_rag import AdaptiveRAGAgent


# ============================================================
# LOGGER
# ============================================================

_project_root = Path(__file__).resolve().parent.parent.parent
_log_dir = _project_root / "logs"
_log_dir.mkdir(exist_ok=True)
_log_file = _log_dir / "app.log"
_trace_file = _log_dir / "pipeline_trace.log"

logger = logging.getLogger("chatbot")
logger.setLevel(logging.DEBUG)
logger.propagate = False

_fmt = logging.Formatter(
    "[%(asctime)s] %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S"
)

if not logger.handlers:
    _ch = logging.StreamHandler()
    _ch.setLevel(logging.INFO)
    _ch.setFormatter(_fmt)
    logger.addHandler(_ch)

    _fh = logging.FileHandler(str(_log_file), encoding="utf-8", mode="a")
    _fh.setLevel(logging.DEBUG)
    _fh.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(_fh)


def _write_json_trace(debug_info: dict):
    """Write debug_info as JSON to pipeline_trace.log."""
    try:
        with open(str(_trace_file), 'w', encoding='utf-8') as f:
            json.dump(debug_info, f, indent=2, ensure_ascii=False, default=str)
    except Exception as e:
        logger.error(f"Failed to write JSON trace: {e}")


class Orchestrator:
    """
    Code-level Orchestrator for EduBot.

    Flow:
        1. IntentRouter.detect() → IntentResult (1 LLM call)
        2. SessionManager.resolve() → Session (pure code)
        3. ActionPlanner.plan() → ActionPlan (pure code)
        4. execute() → Handler (LLM calls for content generation)
        5. SessionStore.auto_save() → JSON persistence
    """

    def __init__(self, retriever, reranker):
        self.retriever = retriever
        self.reranker = reranker

        # Debug trace — populated during each ask() call
        self.last_debug_info: Dict = {}
        # Intent result từ IntentRouter — dùng để truyền context vào RAG Agent
        self._current_intent_result = None

        # Core pipeline components
        self.intent_router = IntentRouter()
        self.context_analyzer = ContextAnalyzer()
        self.memory = MemoryManager()
        self.session_store = SessionStore(
            storage_path=str(_project_root / "data" / "sessions")
        )
        self.session_manager = SessionManager(
            session_store=self.session_store,
            memory=self.memory,
        )
        self.action_planner = ActionPlanner()

        # Handlers
        self.question_handlers = {
            "mcq": MCQHandler(),
            "essay": EssayHandler(),
            "fill_blank": FillHandler(),
            "true_false": TrueFalseHandler(),
        }
        self.scorer = QuestionScorer()
        self.chat_handler = ChatHandler()
        self.explain_handler = ExplainHandler()
        self.slide_handler = SlideHandler()
        self.validator = QuestionValidator()
        self.knowledge_map = KnowledgeMap()
        self.student_tracker = StudentTracker()
        self.rag_agent = AdaptiveRAGAgent(
            retriever=self.retriever,
            reranker=self.reranker,
            settings=settings,
        )

    # ============================================================
    # MAIN ENTRY POINT
    # ============================================================

    def ask(self, query: str, **kwargs) -> Generator[str, None, None]:
        """
        Main processing pipeline.

        Args:
            query: User's message

        Yields:
            str: Response chunks (for streaming display)
        """
        t0 = time.time()
        # Reset debug trace
        self.last_debug_info = {
            "query": query,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "steps": [],
        }

        logger.info("=" * 60)
        logger.info(f"QUERY: '{query[:80]}...'" if len(query) > 80 else f"QUERY: '{query}'")

        # ① Context enrichment (if needed)
        current_session = self.memory.current_session_v2
        history_text = ""
        if current_session:
            history_text = "\n".join(
                f"{m.role}: {m.content}" for m in current_session.messages[-5:]
            )

        enriched_query = query
        ctx_enriched = False
        if history_text and self.context_analyzer.needs_contextualization(query, history_text):
            context_snippet = self.context_analyzer.extract_context_from_history(query, history_text)
            enriched_query = f"Ngu canh truoc do:\n{context_snippet}\n\nCau hoi hien tai: {query}"
            ctx_enriched = True
            logger.info("ContextAnalyzer: enriched query with history")

        self.last_debug_info["steps"].append({
            "node": "ContextAnalyzer",
            "enriched": ctx_enriched,
        })

        # ② Intent Detection (1 LLM call)
        t1 = time.time()
        current_topic = current_session.topic if current_session else None
        session_messages = current_session.get_context_messages() if current_session else None

        intent_result = self.intent_router.detect(
            query=enriched_query,
            current_topic=current_topic,
            session_messages=session_messages,
        )
        intent_time = time.time() - t1
        logger.info(
            f"IntentRouter ({intent_time:.2f}s): "
            f"intent={intent_result.primary_intent}, "
            f"task_type={intent_result.task_type}, "
            f"topic={intent_result.topic}, "
            f"is_new_topic={intent_result.is_new_topic}"
        )

        # Lưu lại để RAG Agent dùng topic/grade từ LLM reasoning
        self._current_intent_result = intent_result

        self.last_debug_info["steps"].append({
            "node": "IntentRouter",
            "primary_intent": intent_result.primary_intent,
            "task_type": intent_result.task_type,
            "topic": intent_result.topic,
            "is_new_topic": intent_result.is_new_topic,
            "time_s": round(intent_time, 2),
        })

        # ③ Session Resolution (pure code)
        session = self.session_manager.resolve_session(intent_result)
        logger.info(
            f"Session: id={session.session_id}, "
            f"topic='{session.topic}', "
            f"msgs={len(session.messages)}"
        )

        self.last_debug_info["steps"].append({
            "node": "SessionManager",
            "session_id": session.session_id,
            "topic": session.topic,
            "intent": session.intent,
            "total_messages": len(session.messages),
            "has_quiz_state": session.quiz_state is not None,
            "has_slide_state": session.slide_state is not None,
        })

        # Save user message
        session.add_message("user", query)

        # ④ Action Planning (pure code)
        action_plan = self.action_planner.plan(intent_result, session, query)
        logger.info(f"ActionPlan: {action_plan.action.value} ({action_plan.reason})")

        self.last_debug_info["steps"].append({
            "node": "ActionPlanner",
            "action": action_plan.action.value,
            "reason": action_plan.reason,
            "round_id": action_plan.round_id,
        })

        # ⑤ Execute
        response_chunks = []
        for chunk in self._execute(action_plan, intent_result, session, enriched_query, query):
            response_chunks.append(chunk)
            yield chunk

        # ⑥ Auto-save
        full_response = "".join(response_chunks)
        self.session_store.auto_save(session)

        total_time = time.time() - t0
        self.last_debug_info["total_time_s"] = round(total_time, 2)
        self.last_debug_info["response"] = {
            "length": len(full_response),
            "preview": full_response[:500],
        }

        # Write JSON trace to pipeline_trace.log
        _write_json_trace(self.last_debug_info)

        logger.info(f"Total time: {total_time:.2f}s")
        logger.info("=" * 60)

    # ============================================================
    # EXECUTE — Dispatch to handlers
    # ============================================================

    def _execute(
        self,
        plan: ActionPlan,
        intent_result: IntentResult,
        session: Session,
        enriched_query: str,
        original_query: str,
    ) -> Generator[str, None, None]:
        """Dispatch to the appropriate handler based on ActionPlan."""

        action = plan.action

        if action == Action.GENERATE_QUIZ:
            yield from self._handle_generate_quiz(
                enriched_query, session, intent_result.task_type or "mcq"
            )
        elif action == Action.GENERATE_SLIDE:
            yield from self._handle_generate_slide(enriched_query, session)
        elif action == Action.CHECK_ANSWER:
            yield from self._handle_check_answer(original_query, session)
        elif action == Action.REVIEW_WRONG:
            yield from self._handle_review_wrong(original_query, session, plan.round_id)
        elif action == Action.GET_STATS:
            yield from self._handle_get_stats(session)
        elif action == Action.EXPLAIN_QUESTION:
            yield from self._handle_explain_question(original_query, session)
        elif action == Action.EXPLAIN_CONCEPT:
            yield from self._handle_explain(enriched_query, session)
        elif action == Action.ANSWER_EXERCISE:
            yield from self._handle_answer_exercise(original_query, session)
        elif action == Action.GENERATE_LESSON_PLAN:
            yield "Chuc nang tao giao an dang duoc phat trien."
        else:
            yield from self._handle_chat(enriched_query, session)

    # ============================================================
    # HANDLER: Generate Quiz
    # ============================================================

    def _handle_generate_quiz(
        self, query: str, session: Session, task_type: str
    ) -> Generator[str, None, None]:
        """Generate quiz questions and create a new QuizRound."""
        yield "Dang tim kiem tai lieu lien quan..."

        # RAG Search
        t0 = time.time()
        contexts = self._get_rag_context(query, intent_hint="generate")
        rag_time = time.time() - t0
        logger.info(f"RAG Search: {len(contexts)} chunks ({rag_time:.2f}s)")
        if not contexts:
            yield "Khong tim thay tai lieu phu hop de tao cau hoi."
            return

        context_text = format_contexts(contexts)
        handler = self.question_handlers.get(task_type, self.question_handlers["mcq"])
        num_q = extract_num_questions(query) or 3
        logger.info(f"Generate: type={task_type}, num={num_q}")

        yield f"Dang soan {num_q} cau hoi {task_type.upper()}..."

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
                    yield "Loi khi sinh cau hoi. Dang thu lai..."
                    continue

                # Validate
                yield "Dang kiem duyet chat luong..."
                t2 = time.time()
                validation_result = self.validator.validate(
                    question_type=task_type,
                    context=context_text,
                    questions_json=json.dumps(raw_questions.model_dump())
                )
                val_time = time.time() - t2
                logger.info(
                    f"Validator: all_valid={validation_result.all_valid}, "
                    f"approved={len(validation_result.approved_questions)} ({val_time:.2f}s)"
                )

                if validation_result.all_valid or validation_result.approved_questions:
                    # Create QuizRound and save questions
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
                        f"round {quiz_round.round_id} (total rounds: {len(quiz_state.rounds)})"
                    )

                    # Display
                    display = raw_questions.to_display_format()
                    session.add_message("assistant", display)
                    yield "\n\n" + display

                    # Round info
                    yield (
                        f"\n\n[Round {quiz_round.round_id + 1}] "
                        f"Da tao {len(quiz_round.questions)} cau hoi."
                    )
                    self.last_debug_info["steps"].append({
                        "node": "Handler",
                        "handler": handler.__class__.__name__,
                        "action": "generate_quiz",
                        "task_type": task_type,
                        "num_questions": num_q,
                        "rag_chunks": len(contexts),
                        "rag_time_s": round(rag_time, 2),
                        "context_length": len(context_text),
                        "generation_time_s": round(gen_time, 2),
                        "generation_attempts": attempt + 1,
                        "validator_all_valid": validation_result.all_valid,
                        "validator_approved": len(validation_result.approved_questions),
                        "validator_time_s": round(val_time, 2),
                        "questions_saved": len(quiz_round.questions),
                        "round_id": quiz_round.round_id,
                        "status": "success",
                    })
                    break
                else:
                    logger.warning(f"Validation FAILED (attempt {attempt+1})")
                    if attempt == max_retries - 1:
                        self.last_debug_info["steps"].append({
                            "node": "Handler", "action": "generate_quiz",
                            "status": "validation_failed", "attempts": max_retries,
                        })
                        yield "He thong dang gap kho khan khi tao cau hoi. Ban thu hoi cu the hon nhe!"

            except Exception as e:
                logger.error(f"Exception (attempt {attempt+1}): {e}")
                if attempt == max_retries - 1:
                    self.last_debug_info["steps"].append({
                        "node": "Handler", "action": "generate_quiz",
                        "status": "error", "error": str(e)[:200],
                    })
                    yield f"Loi sinh cau hoi: {str(e)[:100]}"

    # ============================================================
    # HANDLER: Check Answer
    # ============================================================

    def _handle_check_answer(
        self, query: str, session: Session
    ) -> Generator[str, None, None]:
        """Score user's answer against questions in session."""
        all_questions = session.get_all_question_records()

        if not all_questions:
            yield "Ban chua co cau hoi nao. Hay yeu cau tao cau hoi truoc nhe!"
            return

        yield "Dang cham diem..."

        try:
            task_items = [q.to_task_item() for q in all_questions]

            t0 = time.time()
            result = self.scorer.handle(query, task_items)
            score_time = time.time() - t0
            logger.info(
                f"Scorer: status={result.status}, correct={result.is_correct}, "
                f"score={result.score} ({score_time:.2f}s)"
            )

            if result.status == "found":
                # Update the QuestionRecord
                if result.question_index is not None and result.question_index < len(all_questions):
                    record = all_questions[result.question_index]
                    record.record_attempt(
                        user_answer=result.user_answer,
                        is_correct=result.is_correct or False,
                        score=result.score,
                    )

                # Track stats
                self.student_tracker.update_stats_v2(
                    session=session,
                    topic=session.topic or "Chung",
                    question_type=record.question_type if result.question_index is not None else "unknown",
                    is_correct=result.is_correct or False,
                )

                # Response
                icon = "Chinh xac!" if result.is_correct else "Sai roi!"
                msg = f"\n\n{icon} {result.explanation or ''}"
                if result.score is not None:
                    msg += f"\nDiem so: {result.score}/10"

                session.add_message("assistant", msg)
                yield msg

                # Periodic summary
                if session.quiz_state:
                    answered = session.quiz_state.total_answered
                    if answered > 0 and answered % 3 == 0:
                        summary = session.quiz_state.get_summary()
                        yield "\n\n---\n" + summary

                self.last_debug_info["steps"].append({
                    "node": "Handler", "action": "check_answer",
                    "status": "found",
                    "scorer_time_s": round(score_time, 2),
                    "is_correct": result.is_correct,
                    "score": result.score,
                    "question_index": result.question_index,
                    "explanation_preview": (result.explanation or "")[:200],
                })
            else:
                self.last_debug_info["steps"].append({
                    "node": "Handler", "action": "check_answer",
                    "status": "not_found",
                    "scorer_time_s": round(score_time, 2),
                })
                yield f"\nKhong the xac dinh cau tra loi. {result.explanation or 'Vui long noi ro hon.'}"

        except Exception as e:
            logger.error(f"Check answer error: {e}")
            self.last_debug_info["steps"].append({
                "node": "Handler", "action": "check_answer",
                "status": "error", "error": str(e)[:200],
            })
            yield f"Loi cham diem: {str(e)[:100]}"

    # ============================================================
    # HANDLER: Review Wrong Questions
    # ============================================================

    def _handle_review_wrong(
        self, query: str, session: Session, round_id: Optional[int] = None
    ) -> Generator[str, None, None]:
        """Show wrong questions for review."""
        quiz_state = session.quiz_state

        if not quiz_state:
            yield "Ban chua co cau hoi nao de on tap."
            return

        wrong = quiz_state.get_wrong_questions(round_id=round_id)

        if not wrong:
            if round_id is not None:
                yield f"Khong co cau sai nao trong round {round_id + 1}!"
            else:
                yield "Ban chua co cau sai nao. Tuyet voi!"
            return

        # Create review round
        source_ids = [round_id] if round_id is not None else None
        review_round = quiz_state.create_review_round(source_round_ids=source_ids)

        if not review_round:
            yield "Khong tao duoc bai on tap."
            return

        # Display wrong questions for retry
        lines = []
        round_label = f"round {round_id + 1}" if round_id is not None else "tat ca cac round"
        lines.append(f"ON TAP CAU SAI ({round_label}): {len(review_round.questions)} cau\n")

        for q in review_round.questions:
            content = q.content
            q_type = q.question_type

            if q_type == "mcq":
                lines.append(f"Cau hoi: {content.get('question', '')}")
                options = content.get("options", {})
                if isinstance(options, dict):
                    for key, val in options.items():
                        lines.append(f"  {key}. {val}")
                lines.append("")
            elif q_type == "true_false":
                lines.append(f"Menh de: {content.get('statement', '')}")
                lines.append("  -> Dung hay Sai?")
                lines.append("")
            elif q_type == "fill_blank":
                lines.append(f"Dien khuyet: {content.get('text_with_blanks', '')}")
                lines.append("")
            elif q_type == "essay":
                lines.append(f"Cau hoi: {content.get('question', '')}")
                lines.append("")

            lines.append("_" * 40)
            lines.append("")

        display = "\n".join(lines)
        session.add_message("assistant", display)
        self.last_debug_info["steps"].append({
            "node": "Handler", "action": "review_wrong",
            "status": "success",
            "round_id": round_id,
            "wrong_questions": len(wrong),
            "review_questions": len(review_round.questions),
        })
        yield display

    # ============================================================
    # HANDLER: Get Stats
    # ============================================================

    def _handle_get_stats(self, session: Session) -> Generator[str, None, None]:
        """Show quiz statistics/progress."""
        lines = []

        if session.quiz_state:
            lines.append(session.quiz_state.get_summary())

        if session.slide_state and session.slide_state.has_exercises:
            ss = session.slide_state
            lines.append(
                f"\nBai tap slide: {ss.correct_exercises}/{ss.total_exercises} dung"
            )
            wrong_ex = ss.get_wrong_exercises()
            if wrong_ex:
                lines.append(f"Cau sai: {len(wrong_ex)}")

        if not lines:
            yield "Chua co du lieu hoc tap trong phien nay."
            return

        self.last_debug_info["steps"].append({
            "node": "Handler", "action": "get_stats",
            "status": "success",
            "has_quiz": session.quiz_state is not None,
            "has_slide_exercises": bool(session.slide_state and session.slide_state.has_exercises),
        })
        yield "\n".join(lines)

    # ============================================================
    # HANDLER: Explain Question (specific question in session)
    # ============================================================

    def _handle_explain_question(
        self, query: str, session: Session
    ) -> Generator[str, None, None]:
        """Explain a specific question from the session."""
        all_questions = session.get_all_question_records()

        if not all_questions:
            # Fallback to general explain
            yield from self._handle_explain(query, session)
            return

        # Format all questions as context and let explain handler work
        q_context = "\n".join(
            f"Cau {i+1}: {q.content.get('question', q.content.get('statement', ''))}"
            for i, q in enumerate(all_questions[-5:])  # Last 5
        )

        try:
            full_context = f"Cac cau hoi trong session:\n{q_context}"
            t0 = time.time()
            response = self.explain_handler.handle(query, context=full_context)
            explain_time = time.time() - t0
            session.add_message("assistant", response)
            self.last_debug_info["steps"].append({
                "node": "Handler", "action": "explain_question",
                "status": "success",
                "questions_available": len(all_questions),
                "explain_time_s": round(explain_time, 2),
                "response_length": len(response),
            })
            yield "\n\n" + response
        except Exception as e:
            self.last_debug_info["steps"].append({
                "node": "Handler", "action": "explain_question",
                "status": "error", "error": str(e)[:200],
            })
            yield f"Loi giai thich: {str(e)[:100]}"

    # ============================================================
    # HANDLER: Answer Slide Exercise
    # ============================================================

    def _handle_answer_exercise(
        self, query: str, session: Session
    ) -> Generator[str, None, None]:
        """Score answer for slide exercise questions."""
        slide_state = session.slide_state

        if not slide_state or not slide_state.has_exercises:
            yield "Khong co bai tap slide nao de tra loi."
            return

        # Delegate to scorer using exercise questions
        task_items = [q.to_task_item() for q in slide_state.exercise_questions]

        try:
            t0 = time.time()
            result = self.scorer.handle(query, task_items)
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

                icon = "Chinh xac!" if result.is_correct else "Sai roi!"
                msg = f"\n\n{icon} {result.explanation or ''}"
                session.add_message("assistant", msg)
                self.last_debug_info["steps"].append({
                    "node": "Handler", "action": "answer_exercise",
                    "status": "found",
                    "scorer_time_s": round(score_time, 2),
                    "is_correct": result.is_correct,
                    "question_index": result.question_index,
                })
                yield msg
            else:
                yield f"\nKhong xac dinh duoc cau tra loi. {result.explanation or ''}"

        except Exception as e:
            yield f"Loi cham bai tap: {str(e)[:100]}"

    # ============================================================
    # HANDLER: Generate Slide
    # ============================================================

    def _handle_generate_slide(
        self, query: str, session: Session
    ) -> Generator[str, None, None]:
        """Generate slide deck with exercise extraction."""
        yield "Dang phan tich noi dung de thiet ke bai giang..."

        contexts = self._get_rag_context(query, intent_hint="generate")
        if not contexts:
            yield "Khong tim thay noi dung bai hoc phu hop."
            return

        context_text = format_contexts(contexts)

        try:
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

            # Store slide in session
            slide_state = session.ensure_slide_state()
            slide_state.slide_output = slide_output.model_dump()
            slide_state.slide_html = SlideTemplate.render_to_html(slide_output)

            # Extract exercise questions from slides
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

            yield f"\n\nDa tao {slide_output.total_slides} slides cho '{slide_output.lesson_title}'."
            yield "\n\n" + display

            if slide_state.has_exercises:
                yield f"\nSlide co {slide_state.total_exercises} cau hoi bai tap. Ban co the tra loi ngay!"

            self.last_debug_info["steps"].append({
                "node": "Handler", "action": "generate_slide",
                "status": "success",
                "slide_time_s": round(slide_time, 2),
                "total_slides": slide_output.total_slides,
                "lesson_title": slide_output.lesson_title,
                "slide_types": slide_types,
                "exercises_extracted": exercise_count,
            })

        except Exception as e:
            logger.error(f"Slide generation error: {e}")
            yield f"Loi tao slide: {str(e)[:100]}"

    # ============================================================
    # HANDLER: Explain Concept (general)
    # ============================================================

    def _handle_explain(
        self, query: str, session: Session
    ) -> Generator[str, None, None]:
        """Explain a general concept using RAG context."""
        yield "Dang tim tai lieu de giai thich..."

        contexts = self._get_rag_context(query, intent_hint="explain")
        context_text = format_contexts(contexts) if contexts else ""

        try:
            t0 = time.time()
            response = self.explain_handler.handle(query, context=context_text)
            explain_time = time.time() - t0
            session.add_message("assistant", response)
            self.last_debug_info["steps"].append({
                "node": "Handler", "action": "explain_concept",
                "status": "success",
                "rag_chunks": len(contexts) if contexts else 0,
                "explain_time_s": round(explain_time, 2),
                "response_length": len(response),
            })
            yield "\n\n" + response
        except Exception as e:
            self.last_debug_info["steps"].append({
                "node": "Handler", "action": "explain_concept",
                "status": "error", "error": str(e)[:200],
            })
            yield f"Loi: {str(e)[:100]}"

    # ============================================================
    # HANDLER: Chat
    # ============================================================

    def _handle_chat(
        self, query: str, session: Session
    ) -> Generator[str, None, None]:
        """Free-form chat with RAG context."""
        contexts = self._get_rag_context(query, intent_hint="chat")
        context_text = format_contexts(contexts) if contexts else ""

        try:
            t0 = time.time()
            response = self.chat_handler.handle(query, context=context_text)
            chat_time = time.time() - t0
            session.add_message("assistant", response)
            self.last_debug_info["steps"].append({
                "node": "Handler", "action": "chat",
                "status": "success",
                "rag_chunks": len(contexts) if contexts else 0,
                "chat_time_s": round(chat_time, 2),
                "response_length": len(response),
            })
            yield response
        except Exception as e:
            self.last_debug_info["steps"].append({
                "node": "Handler", "action": "chat",
                "status": "fallback", "error": str(e)[:200],
            })
            yield (
                "Chao ban! Minh la tro ly hoc tap Tin hoc THPT. "
                "Minh co the giup ban tao cau hoi on tap, cham bai, "
                "giai thich kien thuc hoac tao slide bai giang."
            )

    # ============================================================
    # RAG SEARCH
    # ============================================================

    def _get_rag_context(self, query: str, intent_hint: str = None) -> List[Dict]:
        """Adaptive RAG Agent — tự chọn chiến lược retrieval.

        Truyền topic_hint và grade_hint từ IntentRouter để agent
        filter metadata chính xác hơn (không cần LLM call thêm).
        """
        # Lấy topic và grade từ IntentRouter đã chạy upstream
        topic_hint = None
        grade_hint = None
        if self._current_intent_result:
            topic_hint = self._current_intent_result.topic
            # Extract grade từ topic string (vd: "Kiến thức Tin học lớp 12" → "12")
            if topic_hint:
                grade_hint = self._extract_grade_from_topic(topic_hint)

        try:
            result = self.rag_agent.retrieve(
                query,
                intent_hint=intent_hint,
                topic_hint=topic_hint,
                grade_hint=grade_hint,
            )

            self.last_debug_info["steps"].append({
                "node": "RAG",
                "strategy": result.strategy_used.value,
                "chunks_returned": len(result.chunks),
                "time_s": result.total_time_s,
                "filter": result.metadata_filter,
                "reason": result.reason,
            })
            return result.chunks

        except Exception as e:
            logger.error(f"RAG Agent Error: {e}")
            self.last_debug_info["steps"].append({
                "node": "RAG", "error": str(e)[:100],
            })
            return []

    @staticmethod
    def _extract_grade_from_topic(topic: str) -> Optional[str]:
        """Extract grade (10/11/12) từ topic string của IntentRouter.

        Ví dụ:
            "Kiến thức Tin học lớp 12" → "12"
            "Tin 10 - Bài 3"          → "10"
            "Lập trình Python"        → None
        """
        topic_lower = topic.lower()
        # Pattern 1: "lớp 12", "lớp 10"
        match = re.search(r'lớp\s*(10|11|12)', topic_lower)
        if match:
            return match.group(1)
        # Pattern 2: "tin 10", "grade 10"
        match = re.search(r'(?:tin|grade)\s*(10|11|12)', topic_lower)
        if match:
            return match.group(1)
        return None



__all__ = ["Orchestrator"]
