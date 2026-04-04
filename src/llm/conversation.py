import json
import logging
import time
from typing import List, Optional, Dict, Any, Union, Generator
from pathlib import Path

# ============================================================
# LOGGER SETUP — ghi ra terminal + logs/app.log
# ============================================================
_project_root = Path(__file__).resolve().parent.parent.parent  # src/llm/ → src/ → project root
_log_dir = _project_root / "logs"
_log_dir.mkdir(exist_ok=True)
_log_file = _log_dir / "app.log"

logger = logging.getLogger("chatbot")
logger.setLevel(logging.DEBUG)
logger.propagate = False  # Không lan truyền lên root logger

# Format chung
_fmt = logging.Formatter(
    "[%(asctime)s] %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S"
)

# Console handler (terminal)
if not logger.handlers:
    _ch = logging.StreamHandler()
    _ch.setLevel(logging.INFO)
    _ch.setFormatter(_fmt)
    logger.addHandler(_ch)

    # File handler (logs/app.log) — absolute path
    _fh = logging.FileHandler(str(_log_file), encoding="utf-8", mode="a")
    _fh.setLevel(logging.DEBUG)
    _fh.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    _fh.flush = lambda: None  # Force flush trên Windows
    logger.addHandler(_fh)

logger.info(f"Logger initialized → {_log_file}")

from src.llm.intent_detector import IntentDetector
from src.llm.context_analyzer import ContextAnalyzer
from src.llm.memory import MemoryManager, SessionState, TaskItem, Message
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
from src.llm.student_tracker import StudentTracker
from src.llm.knowledge_map import KnowledgeMap
from src.llm.utils import extract_num_questions, format_contexts
from src.config.config import settings

class ChatBot:
    """
    Orchestrator chính cho Phase 2.
    Điều phối Intent Detection -> RAG -> Generation -> Validation -> Tracking.
    """
    
    def __init__(self, retriever, reranker):
        self.retriever = retriever
        self.reranker = reranker
        
        # Core Components
        self.intent_detector = IntentDetector()
        self.context_analyzer = ContextAnalyzer()
        self.memory = MemoryManager()
        
        # Handlers
        self.question_handlers = {
            "mcq": MCQHandler(),
            "essay": EssayHandler(),
            "fill_blank": FillHandler(),
            "true_false": TrueFalseHandler()
        }
        self.scorer = QuestionScorer()
        self.chat_handler = ChatHandler()
        self.explain_handler = ExplainHandler()
        self.slide_handler = SlideHandler()
        self.validator = QuestionValidator()
        self.knowledge_map = KnowledgeMap()
        self.student_tracker = StudentTracker()

    def ask(self, query: str, session_id: Optional[int] = None, **kwargs) -> Generator[str, None, None]:
        """Luồng xử lý chính."""
        t0 = time.time()
        logger.info("="*60)
        logger.info(f"QUERY: '{query[:80]}...'" if len(query) > 80 else f"QUERY: '{query}'")
        
        # 1. Get/Create Session
        session = None
        if session_id is not None:
            session = self.memory.get_session(session_id)
        if session is None:
            session = self.memory.create_session()
        session_id = session.session_id
        logger.debug(f"Session ID: {session_id}, messages: {len(session.messages)}, items: {len(session.items)}")
        
        # 2. Context Analyzer — bổ sung ngữ cảnh nếu cần
        history_text = "\n".join(
            f"{m.role}: {m.content}" for m in session.messages[-5:]
        )
        enriched_query = query
        needs_ctx = self.context_analyzer.needs_contextualization(query, history_text)
        if needs_ctx:
            context_snippet = self.context_analyzer.extract_context_from_history(history_text)
            enriched_query = f"Ngữ cảnh trước đó:\n{context_snippet}\n\nCâu hỏi hiện tại: {query}"
            logger.info(f"ContextAnalyzer: needs contextualization (history={len(session.messages)} msgs)")
        else:
            logger.debug("ContextAnalyzer: no contextualization needed")
        
        # Lưu message user
        self.memory.add_message("user", query)
        
        # 3. Detect Intent
        t1 = time.time()
        memory_context = self.memory.get_context()
        intent_result = self.intent_detector.detect(enriched_query, memory_state=memory_context)
        session.intent = intent_result.get("intent", "chat")
        session.task_type = intent_result.get("task_type")
        session.topic = intent_result.get("topic")
        logger.info(f"Intent: {session.intent} | task_type: {session.task_type} | topic: {session.topic} ({time.time()-t1:.2f}s)")
        
        # 4. Handle Intents
        if session.intent == "generate_question":
            yield from self._handle_generate_question(enriched_query, session)
        elif session.intent == "check_answer":
            yield from self._handle_check_answer(query, session)
        elif session.intent == "generate_slide":
            yield from self._handle_generate_slide(enriched_query, session)
        elif session.intent == "explain":
            yield from self._handle_explain(enriched_query, session)
        else:
            yield from self._handle_chat(enriched_query, session)
        
        logger.info(f"Total processing time: {time.time()-t0:.2f}s")
        logger.info("="*60)

    def _handle_generate_question(self, query: str, session: SessionState) -> Generator[str, None, None]:
        yield "🔍 Đang tìm kiếm tài liệu liên quan..."
        
        # RAG Search
        t0 = time.time()
        contexts = self._get_rag_context(query)
        logger.info(f"RAG Search: {len(contexts)} chunks ({time.time()-t0:.2f}s)")
        if not contexts:
            logger.warning("RAG returned 0 results")
            yield "Xin lỗi, mình không tìm thấy tài liệu phù hợp trong kho SGK để tạo câu hỏi."
            return
            
        context_text = format_contexts(contexts)
        task_type = session.task_type or "mcq"
        handler = self.question_handlers.get(task_type, self.question_handlers["mcq"])
        num_q = extract_num_questions(query) or 3
        logger.info(f"Generate: type={task_type}, num={num_q}, handler={handler.__class__.__name__}")
        
        yield f"✏️ Đang soạn {num_q} câu hỏi {task_type.upper()}..."
        
        # Loop để retry nếu validation fail (tối đa 2 lần)
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # Generate
                t1 = time.time()
                raw_questions = handler.handle(query, context_text, num_questions=num_q)
                logger.info(f"   Handler.handle() → {time.time()-t1:.2f}s (attempt {attempt+1}/{max_retries})")
                
                if raw_questions is None:
                    logger.warning(f"   Handler returned None (attempt {attempt+1})")
                    yield "⚠️ Lỗi khi sinh câu hỏi. Đang thử lại..."
                    continue
                
                # Validate (Node #2)
                yield "🔎 Đang kiểm duyệt chất lượng..."
                t2 = time.time()
                validation_result = self.validator.validate(
                    question_type=task_type,
                    context=context_text,
                    questions_json=json.dumps(raw_questions.model_dump())
                )
                logger.info(f"   Validator → all_valid={validation_result.all_valid}, approved={len(validation_result.approved_questions)} ({time.time()-t2:.2f}s)")
                
                if validation_result.all_valid or validation_result.approved_questions:
                    # Lưu vào session
                    for q in validation_result.approved_questions:
                        session.items.append(TaskItem(type=task_type, content=q, index=len(session.items)))
                    logger.info(f"   Saved {len(validation_result.approved_questions)} questions to session (total items: {len(session.items)})")
                    
                    # Hiển thị
                    display = raw_questions.to_display_format()
                    self.memory.add_message("assistant", display)
                    yield "\n\n" + display
                    
                    # Knowledge relation (optional)
                    try:
                        relations = self.knowledge_map.find_relations(context_text)
                        if relations:
                            topics = ", ".join([r.get('topic', '') for r in relations[:2]])
                            logger.debug(f"   KnowledgeMap: {topics}")
                            yield f"\n\n💡 *Kiến thức liên quan:* {topics}"
                    except Exception as e:
                        logger.debug(f"   KnowledgeMap skipped: {e}")
                    break
                else:
                    logger.warning(f"   Validation FAILED (attempt {attempt+1}): {[v.issues for v in validation_result.validations]}")
                    if attempt == max_retries - 1:
                        yield "⚠️ Hệ thống đang gặp khó khăn khi tạo câu hỏi chính xác. Bạn thử hỏi cụ thể hơn nhé!"
            except Exception as e:
                logger.error(f"   Exception (attempt {attempt+1}): {e}")
                if attempt == max_retries - 1:
                    yield f"❌ Lỗi sinh câu hỏi: {str(e)[:100]}"

    def _handle_check_answer(self, query: str, session: SessionState) -> Generator[str, None, None]:
        logger.info(f"CheckAnswer: session has {len(session.items)} items")
        if not session.items:
            logger.warning("Session has no items to grade")
            yield "Bạn chưa có câu hỏi nào để trả lời. Hãy yêu cầu mình tạo câu hỏi trước nhé!"
            return
            
        yield "📝 Đang chấm điểm..."
        
        try:
            # Scorer
            t0 = time.time()
            result = self.scorer.handle(query, session.items)
            logger.info(f"   Scorer → status={result.status}, correct={result.is_correct}, score={result.score} ({time.time()-t0:.2f}s)")
            
            if result.status == "found":
                # Track progress (in-memory)
                q_type = "unknown"
                if result.question_index is not None and result.question_index < len(session.items):
                    q_type = session.items[result.question_index].type
                
                self.student_tracker.update_stats(
                    session=session,
                    topic=session.topic or "Chung",
                    question_type=q_type,
                    is_correct=result.is_correct or False
                )
                
                # Response message
                icon = "✅" if result.is_correct else "❌"
                msg = f"\n\n{icon} **{result.explanation}**"
                if result.score is not None:
                    msg += f"\n📊 Điểm số: {result.score}/10"
                
                self.memory.add_message("assistant", msg)
                yield msg
                
                # Show overall summary periodically
                if session.quiz_stats.total_questions > 0 and session.quiz_stats.total_questions % 3 == 0:
                    summary = self.student_tracker.get_summary(session)
                    yield "\n\n---\n" + summary
            else:
                yield f"\n\n🤔 {result.explanation or 'Không thể xác định câu trả lời. Vui lòng nói rõ hơn.'}"
        except Exception as e:
            yield f"❌ Lỗi chấm điểm: {str(e)[:100]}"

    def _handle_generate_slide(self, query: str, session: SessionState) -> Generator[str, None, None]:
        yield "📊 Đang phân tích nội dung để thiết kế bài giảng..."
        
        # RAG Search
        contexts = self._get_rag_context(query)
        if not contexts:
            yield "Không tìm thấy nội dung bài học phù hợp để tạo slide."
            return
            
        context_text = format_contexts(contexts)
        
        try:
            # Sinh slide
            slide_output = self.slide_handler.handle(
                book="Kết nối tri thức", grade="10", lesson="Bài học", 
                context=context_text
            )
            
            # Render HTML
            html_output = SlideTemplate.render_to_html(slide_output)
            
            display = slide_output.to_display_format()
            self.memory.add_message("assistant", display)
            
            yield f"\n\n📊 Đã tạo xong {slide_output.total_slides} slides bài giảng cho '{slide_output.lesson_title}'."
            yield "\n\n" + display
            
            # Metadata chứa HTML để UI render
            session.metadata["last_slide_html"] = html_output
        except Exception as e:
            yield f"❌ Lỗi tạo slide: {str(e)[:100]}"

    def _handle_explain(self, query: str, session: SessionState) -> Generator[str, None, None]:
        """Giải thích chuyên sâu 1 khái niệm, sử dụng RAG context."""
        yield "📖 Đang tìm tài liệu để giải thích..."
        
        contexts = self._get_rag_context(query)
        context_text = format_contexts(contexts) if contexts else ""
        
        try:
            response = self.explain_handler.handle(query, context=context_text)
            self.memory.add_message("assistant", response)
            yield "\n\n" + response
        except Exception as e:
            yield f"❌ Lỗi: {str(e)[:100]}"

    def _handle_chat(self, query: str, session: SessionState) -> Generator[str, None, None]:
        """Hỏi đáp chung, sử dụng RAG context nếu có."""
        contexts = self._get_rag_context(query)
        context_text = format_contexts(contexts) if contexts else ""
        
        try:
            response = self.chat_handler.handle(query, context=context_text)
            self.memory.add_message("assistant", response)
            yield response
        except Exception as e:
            # Fallback tĩnh nếu handler lỗi
            fallback = ("Chào bạn! Mình là trợ lý học tập Tin học THPT. "
                       "Mình có thể giúp bạn tạo câu hỏi ôn tập, chấm bài, "
                       "giải thích kiến thức hoặc tạo slide bài giảng. Bạn cần gì nhé?")
            yield fallback

    def _get_rag_context(self, query: str) -> List[Dict]:
        """RAG Search — CustomSearch (BM25+Semantic+RRF) → Reranker."""
        try:
            t0 = time.time()
            if hasattr(self.retriever, 'search'):
                results = self.retriever.search(query, top_k=settings.RETRIEVER_TOP_K)
                logger.debug(f"   CustomSearch.search() → {len(results)} results ({time.time()-t0:.2f}s)")
                if not results:
                    return []
                t1 = time.time()
                reranked = self.reranker.rerank(query, results, top_n=settings.RERANKER_TOP_N)
                logger.debug(f"   Reranker → {len(reranked)} results ({time.time()-t1:.2f}s)")
                return reranked
            return []
        except Exception as e:
            logger.error(f"RAG Error: {e}")
            return []

