from typing import Optional, List, Dict, Any
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import ESSAY_GENERATION_TEMPLATE
from src.schemas.llm_outputs import EssayGenerationOutput
from src.config.config import settings

class EssayHandler(BaseHandler):
    
    def handle(
        self, 
        query: str, 
        context: str, 
        num_questions: int = 2,
        difficulty: str = "medium",
        **kwargs
    ) -> EssayGenerationOutput:
        # 1. Build prompt
        prompt = ESSAY_GENERATION_TEMPLATE.format(
            query=query,
            context=context,
            num_questions=num_questions,
            difficulty=difficulty,
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
    
    async def handle_async(
        self, 
        query: str, 
        context: str, 
        num_questions: int = 2,
        difficulty: str = "medium",
        **kwargs
    ) -> EssayGenerationOutput:
        # 1. Build prompt
        prompt = ESSAY_GENERATION_TEMPLATE.format(
            query=query,
            context=context,
            num_questions=num_questions,
            difficulty=difficulty,
        )
        
        # 2. Call API async
        response = await self._call_api_async(
            prompt,
            temperature=settings.QUESTION_GENERATION_TEMPERATURE,
            response_mime="application/json"
        )
        
        # 3. Parse & Validate
        try:
            return EssayGenerationOutput.from_json_string(response)
        except Exception as e:
            self._handle_error(f"Lỗi parse Essay JSON: {e}")
