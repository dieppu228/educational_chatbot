"""LLM Module - Question generation, scoring, and response handling"""

from .handlers import (
    BaseHandler,
    QuestionGenerator,
    ResponseFormatter,
    AnswerScorer,
    FallbackHandler,
)
from .context_analyzer import ContextAnalyzer
from .prompts import (
    QUESTION_GENERATION_PROMPT,
    RESPONSE_FORMATTING_PROMPT,
    UTILITY_SCORING_PROMPT,
    FALLBACK_PROMPT,
)
from .validators import (
    validate_num_questions,
    validate_json_response,
    extract_answer_from_query,
    validate_grade,
)
from .utils import (
    extract_num_questions,
    calculate_adaptive_questions,
    format_contexts,
    extract_question_index_from_query,
    fuzzy_match_option,
)

__all__ = [
    # Handlers
    "BaseHandler",
    "QuestionGenerator",
    "ResponseFormatter",
    "AnswerScorer",
    "FallbackHandler",
    # Analyzer
    "ContextAnalyzer",
    # Prompts
    "QUESTION_GENERATION_PROMPT",
    "RESPONSE_FORMATTING_PROMPT",
    "UTILITY_SCORING_PROMPT",
    "FALLBACK_PROMPT",
    # Validators
    "validate_num_questions",
    "validate_json_response",
    "extract_answer_from_query",
    "validate_grade",
    # Utils
    "extract_num_questions",
    "calculate_adaptive_questions",
    "format_contexts",
    "extract_question_index_from_query",
    "fuzzy_match_option",
]
