import asyncio
from typing import Optional, List, Dict, Any
import json
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import QUESTION_VALIDATION_TEMPLATE
from src.schemas.llm_outputs import ValidationResult
from src.config.config import settings

class QuestionValidator(BaseHandler):
    
    def validate(
        self, 
        question_type: str, 
        context: str, 
        questions_json: str
    ) -> ValidationResult:
        # 1. Build prompt
        prompt = QUESTION_VALIDATION_TEMPLATE.format(
            question_type=question_type,
            context=context,
            questions_json=questions_json
        )
        
        # 2. Call API (sử dụng temperature thấp để đảm bảo tính khách quan)
        response = self._call_api(
            prompt,
            temperature=0.1,  # Rất thấp để tránh LLM "sáng tạo" thêm
            response_mime="application/json"
        )
        
        # 3. Parse & Validate
        try:
            return ValidationResult.from_json_string(response)
        except Exception as e:
            # Fallback nếu validator lỗi JSON: coi như không pass để đảm bảo an toàn
            self._handle_error(f"Lỗi parse Validation JSON: {e}", raise_error=False)
            return ValidationResult(all_valid=False, validations=[], approved_questions=[])
    
    async def validate_async(
        self, 
        question_type: str, 
        context: str, 
        questions_json: str
    ) -> ValidationResult:
        # 1. Build prompt
        prompt = QUESTION_VALIDATION_TEMPLATE.format(
            question_type=question_type,
            context=context,
            questions_json=questions_json
        )
        
        # 2. Call API async
        response = await self._call_api_async(
            prompt,
            temperature=0.1,
            response_mime="application/json"
        )
        
        # 3. Parse & Validate
        try:
            return ValidationResult.from_json_string(response)
        except Exception as e:
            # Fallback nếu validator lỗi JSON: coi như không pass để đảm bảo an toàn
            self._handle_error(f"Lỗi parse Validation JSON: {e}", raise_error=False)
            return ValidationResult(all_valid=False, validations=[], approved_questions=[])
            
    def handle(self, query: str, **kwargs):
        pass
