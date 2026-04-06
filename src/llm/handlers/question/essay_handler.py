from typing import Optional, List, Dict, Any
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import ESSAY_GENERATION_TEMPLATE
from src.schemas.llm_outputs import EssayGenerationOutput
from src.config.config import settings

class EssayHandler(BaseHandler):
    """Sinh câu hỏi tự luận từ nội dung bài học."""
    
    def handle(
        self, 
        query: str, 
        context: str, 
        num_questions: int = 2,
        **kwargs
    ) -> EssayGenerationOutput:
        """
        Sinh câu hỏi tự luận.
        
        Args:
            query: Yêu cầu của user
            context: Nội dung bài học từ RAG
            num_questions: Số câu cần sinh
            
        Returns:
            EssayGenerationOutput: Object chứa danh sách câu tự luận
        """
        # 1. Build prompt
        prompt = ESSAY_GENERATION_TEMPLATE.format(
            query=query,
            context=context,
            num_questions=num_questions
        )
        
        # 2. Call API
        response = self._call_api(
            prompt,
            temperature=settings.QUESTION_GENERATION_TEMPERATURE,
            response_mime="application/json"
        )
        
        # 3. Parse & Validate
        try:
            return EssayGenerationOutput.from_json_string(response)
        except Exception as e:
            self._handle_error(f"Lỗi parse Essay JSON: {e}")
