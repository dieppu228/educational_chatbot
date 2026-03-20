"""Input validation utilities"""

from typing import Optional
import re
from src.config.constants import MIN_QUESTIONS, MAX_QUESTIONS, PATTERN_EXTRACT_ANSWER


def validate_num_questions(num: Optional[int]) -> int:
    """
    Validate and constrain number of questions to valid range.
    
    Args:
        num: Number of questions (can be None)
    
    Returns:
        int: Constrained number between MIN_QUESTIONS and MAX_QUESTIONS
    """
    if num is None:
        return 3
    return max(MIN_QUESTIONS, min(MAX_QUESTIONS, num))


def validate_json_response(response: str) -> bool:
    """
    Validate JSON response format.
    
    Args:
        response: JSON string to validate
    
    Returns:
        bool: True if valid MCQ JSON format, False otherwise
    """
    try:
        import json
        data = json.loads(response)
        
        # Check basic structure
        if "mcq" not in data or not isinstance(data["mcq"], list):
            return False
        
        # Check each question
        for i, q in enumerate(data["mcq"], 1):
            if not all(k in q for k in ["index", "question", "options", "correct_answer", "explanation"]):
                return False
            if q["correct_answer"] not in ["A", "B", "C", "D"]:
                return False
            if not isinstance(q["options"], dict) or set(q["options"].keys()) != {"A", "B", "C", "D"}:
                return False
        
        return True
    except Exception:
        return False


def extract_answer_from_query(query: str) -> Optional[str]:
    """
    Extract answer letter (A/B/C/D) from user query.
    
    Args:
        query: User query text
    
    Returns:
        str: Answer letter (A, B, C, or D) if found, None otherwise
    """
    match = re.search(PATTERN_EXTRACT_ANSWER, query, re.IGNORECASE)
    if match:
        return match.group(0).upper()
    return None


def validate_grade(grade: str) -> bool:
    """
    Validate grade value.
    
    Args:
        grade: Grade string
    
    Returns:
        bool: True if valid grade (10, 11, 12)
    """
    return grade in ["10", "11", "12"]


__all__ = [
    "validate_num_questions",
    "validate_json_response",
    "extract_answer_from_query",
    "validate_grade",
]
