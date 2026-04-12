"""Utility functions for LLM module"""

import random
import re
from typing import Optional, List, Dict
from src.config.constants import PATTERN_EXTRACT_NUM_QUESTIONS


def extract_num_questions(query: str) -> Optional[int]:
    """
    Extract number of questions from user query.
    
    Examples:
        "cho 3 câu hỏi" → 3
        "tạo 5 câu" → 5
        "5 bài trắc nghiệm" → 5
    
    Args:
        query: User query text
    
    Returns:
        int if found and valid, None otherwise
    """
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
    """
    Calculate adaptive number of questions based on retrieved context count.
    
    Rules:
        - context <= 5  → random(2-3)
        - 5 < context <= 15 → random(3-4)
        - context > 15 → random(4-5)
    
    Args:
        context_count: Number of retrieved context chunks
    
    Returns:
        int: Recommended number of questions
    """
    if context_count <= 5:
        return random.randint(2, 3)
    elif context_count <= 15:
        return random.randint(3, 4)
    else:
        return random.randint(4, 5)





def extract_question_index_from_query(query: str) -> Optional[int]:
    """
    Extract question index from user query.
    
    Examples:
        "câu 1" → 1
        "câu thứ 2" → 2
        "question 3" → 3
        "No. 4" → 4
    
    Args:
        query: User query text
    
    Returns:
        int: Question number (1-indexed) or None if not found
    """
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
    """
    Fuzzy match user query to one of the options.
    
    Args:
        query: User query text (could be option content)
        options: Dict with keys A,B,C,D and option contents as values
    
    Returns:
        str: Matched option letter (A/B/C/D) or None if no match
    """
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
