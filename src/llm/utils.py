
import random
import re
from typing import Optional, List, Dict
from src.config.constants import PATTERN_EXTRACT_NUM_QUESTIONS


def extract_num_questions(query: str) -> Optional[int]:
    for pattern in PATTERN_EXTRACT_NUM_QUESTIONS:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            try:
                num = int(match.group(1))
                return max(1, min(10, num))  # Constrain to 1-10
            except (ValueError, IndexError):
                continue
    
    return None


def calculate_adaptive_questions(context_count: int) -> int:
    if context_count <= 5:
        return random.randint(2, 3)
    elif context_count <= 15:
        return random.randint(3, 4)
    else:
        return random.randint(4, 5)





def extract_question_index_from_query(query: str) -> Optional[int]:
    patterns = [
        r'(?:câu|question|bài)\s+(?:thứ|number|no\.?)?(?:\s*[:]?)?\s*(\d+)',
        r'(?:thứ)\s+(\d+)',
        r'no\.?\s*(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                continue
    
    return None


def fuzzy_match_option(query: str, options: Dict[str, str]) -> Optional[str]:
    query_lower = query.lower()
    
    # First try exact substring matching
    for letter, option_text in options.items():
        if option_text.lower() in query_lower:
            return letter
    
    # Try reverse substring (content in query)
    for letter, option_text in options.items():
        # Get first 30 chars of option as key phrases
        key_phrases = option_text.lower().split()[:5]
        if any(phrase in query_lower for phrase in key_phrases if len(phrase) > 3):
            return letter
    
    return None


__all__ = [
    "extract_num_questions",
    "calculate_adaptive_questions",
    "extract_question_index_from_query",
    "fuzzy_match_option",
]
