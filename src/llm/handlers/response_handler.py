"""Response handling and answer scoring"""

import json
from typing import Optional, Dict, Any
from src.llm.handlers.base_handler import BaseHandler
from src.prompts.format_prompts import RESPONSE_FORMATTING_PROMPT
from src.prompts.scoring_prompts import UTILITY_SCORING_PROMPT
from src.llm.validation_utils import validate_json_response, extract_answer_from_query
from src.llm.utils import extract_question_index_from_query, fuzzy_match_option
from src.config.config import settings
from core import ScoringResult


class ResponseFormatter(BaseHandler):
    """Format MCQ responses from JSON to readable text."""
    
    def handle(self, json_string: str, max_index: int) -> str:
        """
        Format JSON MCQ to readable text.
        
        Args:
            json_string: JSON string with MCQ data
            max_index: Total number of questions (for validation)
        
        Returns:
            str: Formatted readable text
        """
        try:
            # Validate input JSON
            if not validate_json_response(json_string):
                raise ValueError("Invalid MCQ JSON format")
            
            prompt = RESPONSE_FORMATTING_PROMPT.format(
                options=json_string,
                max_index=max_index
            )
            
            response = self._call_api(
                prompt,
                temperature=0.0,
                response_mime='text/plain'
            )
            
            return response
        
        except Exception as e:
            self._handle_error(e)


class AnswerScorer(BaseHandler):
    """Score user answers against questions."""
    
    def handle(self, query: str, session_state: str) -> Dict[str, Any]:
        """
        Score user answer.
        
        Args:
            query: User query containing their answer
            session_state: JSON string of current session with questions
        
        Returns:
            Dict: Scoring result with status, correctness, explanation
        """
        try:
            # Build prompt
            prompt = UTILITY_SCORING_PROMPT.format(
                query=query,
                state_text=session_state
            )
            
            # Call API
            response = self._call_api(
                prompt,
                temperature=settings.SCORING_TEMPERATURE,
                response_mime='application/json'
            )
            
            # Validate and parse response
            if not self._validate_json_response(response):
                # Return default result
                return self._default_scoring_result("ambiguous")
            
            result = json.loads(response)
            return result
        
        except json.JSONDecodeError as e:
            return self._default_scoring_result("ambiguous")
        
        except Exception as e:
            return self._default_scoring_result("ambiguous")
    
    def _default_scoring_result(self, status: str = "not_found") -> Dict[str, Any]:
        """
        Return default scoring result when API call fails.
        
        Args:
            status: Default status
        
        Returns:
            Dict: Default scoring result
        """
        return {
            "status": status,
            "question_index": None,
            "question_text": None,
            "user_answer": None,
            "correct_answer": None,
            "is_correct": None,
            "explanation": "Không thể xử lý câu trả lời. Vui lòng thử lại.",
            "confidence": 0.0
        }


__all__ = ["ResponseFormatter", "AnswerScorer"]
