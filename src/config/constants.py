"""Global constants for the application"""

# ===== LLM Configuration =====
TEMP_CREATIVE = 0.7
TEMP_DETERMINISTIC = 0.0
TEMP_BALANCED = 0.5

# ===== Question Generation =====
MIN_QUESTIONS = 1
MAX_QUESTIONS = 10
DEFAULT_QUESTIONS = 3

# ===== Question Difficulty Levels =====
DIFFICULTY_EASY = "easy"
DIFFICULTY_MEDIUM = "medium"
DIFFICULTY_HARD = "hard"

# ===== Status Codes =====
STATUS_FOUND = "found"
STATUS_NOT_FOUND = "not_found"
STATUS_AMBIGUOUS = "ambiguous"

# ===== Retrieval Configuration =====
DEFAULT_TOP_K = 60
DEFAULT_RERANK_TOP_N = 10
RRF_K_WEIGHT = 60  # Reciprocal Rank Fusion parameter

# ===== Grades/Khối =====
VALID_GRADES = ["10", "11", "12"]

# ===== Response Format =====
RESPONSE_MIME_JSON = "application/json"
RESPONSE_MIME_TEXT = "text/plain"

# ===== Logging =====
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"

# ===== Regex Patterns =====
PATTERN_EXTRACT_ANSWER = r'[A-Da-d]'
PATTERN_EXTRACT_NUM_QUESTIONS = [
    r'(\d+)\s*(?:câu|bài|question)',
    r'(?:cho|tạo)\s+(\d+)\s*(?:câu|bài)',
]
PATTERN_EXTRACT_GRADE = r'tin(\d+)'
PATTERN_EXTRACT_LESSON = r'(?:bài|lesson)\s*[\:\-]?\s*(\d+)'
