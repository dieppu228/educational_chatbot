from typing import Optional, List, Dict, Any
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import QUESTION_GENERATION_TEMPLATE
from src.schemas.llm_outputs import MCQGenerationOutput
from src.config.config import settings

class MCQHandler(BaseHandler):
    """Sinh câu hỏi trắc nghiệm ABCD từ context."""
    
    def handle(
        self, 
        query: str, 
        context: str, 
        num_questions: int = 3,
        **kwargs
    ) -> MCQGenerationOutput:
        """
        Sinh câu hỏi trắc nghiệm.
        
        Args:
            query: Yêu cầu của user (VD: "Sinh 5 câu về mạng LAN")
            context: Nội dung bài học từ RAG
            num_questions: Số câu cần sinh
            
        Returns:
            MCQGenerationOutput: Object chứa danh sách câu hỏi
        """
        # 1. Build prompt
        prompt = QUESTION_GENERATION_TEMPLATE.format(
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
            return MCQGenerationOutput.from_json_string(response)
        except Exception as e:
            self._handle_error(f"Lỗi parse MCQ JSON: {e}")
