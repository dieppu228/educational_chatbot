"""
Prompts module - Centralized prompt management for LLM nodes.
Provides PromptTemplate class and all prompt constants.
"""

from .base import PromptTemplate
from .question_prompts import (
    QUESTION_GENERATION_PROMPT,
    QUESTION_GENERATION_TEMPLATE,
)
from .scoring_prompts import (
    UTILITY_SCORING_PROMPT,
    SCORING_TEMPLATE,
)
from .format_prompts import (
    RESPONSE_FORMATTING_PROMPT,
    FORMAT_TEMPLATE,
)
from .fallback_prompts import (
    FALLBACK_PROMPT,
    FALLBACK_TEMPLATE,
)
from .extract_prompts import (
    EXTRACT_PROMPT,
    EXTRACT_TEMPLATE,
)
from .feedback_prompts import (
    FEEDBACK_GENERATION_PROMPT,
    FEEDBACK_TEMPLATE,
)

__all__ = [
    # Base
    "PromptTemplate",
    # Question Generation
    "QUESTION_GENERATION_PROMPT",
    "QUESTION_GENERATION_TEMPLATE",
    # Scoring
    "UTILITY_SCORING_PROMPT",
    "SCORING_TEMPLATE",
    # Formatting
    "RESPONSE_FORMATTING_PROMPT",
    "FORMAT_TEMPLATE",
    # Fallback
    "FALLBACK_PROMPT",
    "FALLBACK_TEMPLATE",
    # Extract
    "EXTRACT_PROMPT",
    "EXTRACT_TEMPLATE",
    # Feedback
    "FEEDBACK_GENERATION_PROMPT",
    "FEEDBACK_TEMPLATE",
]
