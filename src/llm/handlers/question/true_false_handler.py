from typing import Optional, List, Dict, Any
from src.llm.handlers.base_handler import BaseHandler
from src.prompts.question_prompts import TRUE_FALSE_GENERATION_TEMPLATE
from src.schemas.llm_outputs import TrueFalseGenerationOutput
from src.config.config import settings

class TrueFalseHandler(BaseHandler):
    """Sinh câu hỏi Đúng/Sai từ nội dung bài học."""
    
    def handle(
        self, 
        query: str, 
        context: str, 
        num_questions: int = 3,
        **kwargs
    ) -> TrueFalseGenerationOutput:
        """
        Sinh câu hỏi Đúng/Sai.
        
        Args:
            query: Yêu cầu của user
            context: Nội dung bài học từ RAG
            num_questions: Số câu cần sinh
            
        Returns:
            TrueFalseGenerationOutput: Object chứa danh sách câu Đúng/Sai
        """
        # 1. Build prompt
        prompt = TRUE_FALSE_GENERATION_TEMPLATE.format(
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
            return TrueFalseGenerationOutput.from_json_string(response)
        except Exception as e:
            self._handle_error(f"Lỗi parse TrueFalse JSON: {e}")
