from typing import Optional, List, Dict, Any
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import FILL_BLANK_GENERATION_TEMPLATE
from src.schemas.llm_outputs import FillBlankGenerationOutput
from src.config.config import settings

class FillHandler(BaseHandler):
    
    def handle(
        self, 
        query: str, 
        context: str, 
        num_questions: int = 3,
        **kwargs
    ) -> FillBlankGenerationOutput:
        # 1. Build prompt
        prompt = FILL_BLANK_GENERATION_TEMPLATE.format(
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
            return FillBlankGenerationOutput.from_json_string(response)
        except Exception as e:
            self._handle_error(f"Lỗi parse FillBlank JSON: {e}")
    
    async def handle_async(
        self, 
        query: str, 
        context: str, 
        num_questions: int = 3,
        **kwargs
    ) -> FillBlankGenerationOutput:
        # 1. Build prompt
        prompt = FILL_BLANK_GENERATION_TEMPLATE.format(
            query=query,
            context=context,
            num_questions=num_questions
        )
        
        # 2. Call API async
        response = await self._call_api_async(
            prompt,
            temperature=settings.QUESTION_GENERATION_TEMPERATURE,
            response_mime="application/json"
        )
        
        # 3. Parse & Validate
        try:
            return FillBlankGenerationOutput.from_json_string(response)
        except Exception as e:
            self._handle_error(f"Lỗi parse FillBlank JSON: {e}")
