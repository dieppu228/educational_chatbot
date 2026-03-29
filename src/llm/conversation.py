import json
from typing import List, Optional, Dict, Any, Union, Generator

from src.llm.intent_detector import IntentDetector
from src.llm.memory import MemoryManager, SessionState, TaskItem, Message
from src.llm.handlers.question.mcq_handler import MCQHandler
from src.llm.handlers.question.essay_handler import EssayHandler
from src.llm.handlers.question.fill_handler import FillHandler
from src.llm.handlers.question.true_false_handler import TrueFalseHandler
from src.llm.handlers.question.scorer import QuestionScorer
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
        self.memory = MemoryManager()
        
        # Handlers
        self.question_handlers = {
            "mcq": MCQHandler(),
            "essay": EssayHandler(),
            "fill_blank": FillHandler(),
            "true_false": TrueFalseHandler()
        }
        self.scorer = QuestionScorer()
        self.slide_handler = SlideHandler()
        self.validator = QuestionValidator()
        self.knowledge_map = KnowledgeMap()
        self.student_tracker = StudentTracker()

    def ask(self, query: str, session_id: Optional[int] = None) -> Generator[str, None, None]:
        """Luồng xử lý chính."""
        # 1. Get/Create Session
        session = self.memory.get_session(session_id) if session_id else self.memory.create_session()
        session_id = session.session_id
        
        # 2. Detect Intent
        intent_result = self.intent_detector.detect(query)
        session.intent = intent_result.get("intent", "chat")
        session.task_type = intent_result.get("task_type")
        
        # 3. Handle Intents
        if session.intent == "generate_question":
            yield from self._handle_generate_question(query, session)
        elif session.intent == "check_answer":
            yield from self._handle_check_answer(query, session)
        elif session.intent == "generate_slide":
            yield from self._handle_generate_slide(query, session)
        else:
            # Fallback chat
            yield "Chào bạn! Mình có thể giúp bạn tạo câu hỏi ôn tập, chấm bài hoặc tạo slide bài giảng. Bạn đang quan tâm đến nội dung nào?"

    def _handle_generate_question(self, query: str, session: SessionState) -> Generator[str, None, None]:
        yield " đang tìm kiếm tài liệu liên quan..."
        
        # RAG Search
        contexts = self._get_rag_context(query)
        if not contexts:
            yield "Xin lỗi, mình không tìm thấy tài liệu phù hợp trong kho SGK để tạo câu hỏi."
            return
            
        context_text = format_contexts(contexts)
        task_type = session.task_type or "mcq"
        handler = self.question_handlers.get(task_type, self.question_handlers["mcq"])
        num_q = extract_num_questions(query) or 3
        
        yield f" đang soạn {num_q} câu hỏi {task_type.upper()}..."
        
        # Loop để retry nếu validation fail (tối đa 2 lần)
        max_retries = 2
        for attempt in range(max_retries):
            # Generate
            raw_questions = handler.handle(query, context_text, num_questions=num_q)
            
            # Validate (Node #2)
            yield " đang kiểm duyệt chất lượng..."
            validation_result = self.validator.validate(
                question_type=task_type,
                context=context_text,
                questions_json=json.dumps(raw_questions.model_dump())
            )
            
            if validation_result.all_valid or validation_result.approved_questions:
                # Lưu vào session
                for q in validation_result.approved_questions:
                    session.items.append(TaskItem(type=task_type, content=q, index=len(session.items)))
                
                # Hiển thị
                yield "\n\n" + raw_questions.to_display_format()
                
                # Knowledge relation (optional)
                relations = self.knowledge_map.find_relations(context_text)
                if relations:
                    yield "\n\n💡 *Kiến thức liên quan:* " + ", ".join([r['topic'] for r in relations[:2]])
                break
            else:
                if attempt == max_retries - 1:
                    yield "Hệ thống đang gặp chút khó khăn khi tạo câu hỏi chính xác. Bạn thử hỏi cụ thể hơn nhé!"

    def _handle_check_answer(self, query: str, session: SessionState) -> Generator[str, None, None]:
        if not session.items:
            yield "Bạn chưa có câu hỏi nào để trả lời. Hãy yêu cầu mình tạo câu hỏi trước nhé!"
            return
            
        yield " đang chấm điểm..."
        
        # Scorer
        result = self.scorer.handle(query, session.items)
        
        if result.status == "found":
            # Track progress (in-memory)
            self.student_tracker.update_stats(
                session=session,
                topic=session.topic or "Chung",
                question_type=session.items[result.question_index].type if result.question_index is not None else "unknown",
                is_correct=result.is_correct
            )
            
            # Response message
            icon = "✅" if result.is_correct else "❌"
            yield f"\n\n{icon} **{result.explanation}**"
            if result.score is not None:
                yield f"\n📊 Điểm số: {result.score}/10"
            
            # Show overall summary periodically
            if session.quiz_stats.total_questions % 3 == 0:
                yield "\n\n---\n" + self.student_tracker.get_summary(session)
        else:
            yield f"\n\n🤔 {result.explanation}"

    def _handle_generate_slide(self, query: str, session: SessionState) -> Generator[str, None, None]:
        yield " đang phân tích nội dung để thiết kế bài giảng..."
        
        # RAG Search
        contexts = self._get_rag_context(query)
        if not contexts:
            yield "Không tìm thấy nội dung bài học phù hợp để tạo slide."
            return
            
        context_text = format_contexts(contexts)
        
        # Sinh slide
        # Giả định metadata lấy từ query hoặc context (simple version)
        slide_output = self.slide_handler.handle(
            book="Kết nối tri thức", grade="10", lesson="Bài học", 
            context=context_text
        )
        
        # Render HTML
        html_output = SlideTemplate.render_to_html(slide_output)
        
        # Trả về link hoặc nội dung (Trong Gradio/Web sẽ render HTML này)
        yield f"\n\n📊 Đã tạo xong {slide_output.total_slides} slides bài giảng cho '{slide_output.lesson_title}'."
        yield "\n\n" + slide_output.to_display_format()
        
        # Metadata chứa HTML để UI render
        session.metadata["last_slide_html"] = html_output

    def _get_rag_context(self, query: str) -> List[Dict]:
        """BM25 + FAISS + Rerank."""
        results = self.retriever.hybrid_search_RRF(query, top_k=settings.RETRIEVER_TOP_K)
        if not results: return []
        return self.reranker.rerank(query, results, top_n=settings.RERANKER_TOP_N)
    


