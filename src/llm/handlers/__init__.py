# handlers package — tất cả handlers cho LLM generation

# Question handlers
from .question import MCQHandler, EssayHandler, FillHandler, QuestionScorer

# Content handlers
from .content import SlideHandler, LessonPlanHandler

# Other handlers
from .chat_handler import ChatHandler
from .explain_handler import ExplainHandler

# Base (dùng khi tạo handler mới)
from .base_handler import BaseHandler

# Legacy (giữ tạm để backward-compatible, sẽ xóa sau)
# from .question_handler import QuestionGenerator
# from .response_handler import ResponseFormatter, AnswerScorer
# from .fallback_handler import FallbackHandler
