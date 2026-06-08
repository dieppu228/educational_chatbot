
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import os


class Settings(BaseSettings):
    
    # ===== API Configuration =====
    GENAI_API_KEY: str = Field(default="", env="GENAI_API_KEY")
    LLM_MODEL: str = "gemini-2.5-flash-lite"
    
    # ===== Retrieval Configuration =====
    RETRIEVER_TOP_K: int = 25
    RERANKER_TOP_N: int = 5
    RERANKER_TOP_N_SLIDE: int = 15        # Slide cần phủ toàn bộ bài
    RERANKER_TOP_N_LESSON_PLAN: int = 10  # Giáo án cần nhiều nhất
    RERANKER_MIN_SCORE: float = 0.00      # Cutoff chunks score quá thấp
    RRF_K_WEIGHT: int = 60
    
    # ===== Question Generation =====
    MIN_QUESTIONS: int = 1
    MAX_QUESTIONS: int = 10
    DEFAULT_QUESTIONS: int = 3
    QUESTION_GENERATION_TEMPERATURE: float = 0.5
    
    # ===== Answer Scoring =====
    SCORING_TEMPERATURE: float = 0.0
    
    # ===== Model Names =====
    EMBEDDING_MODEL: str = "dangvantuan/vietnamese-document-embedding"
    RERANKER_MODEL: str = "AITeamVN/Vietnamese_Reranker"
    
    # ===== File Paths =====
    DATA_DIR: str = "data"
    CHUNKS_FILE: str = "rag_chunks_v2.json"
    EMBEDDINGS_FILE: str = "embeddings.npy"
    EMBEDDINGS_META_FILE: str = "embeddings.meta.json"

    # ===== Qdrant Storage =====
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "educational_chatbot"
    QDRANT_VECTOR_SIZE: int = 768
    QDRANT_UPLOAD_BATCH_SIZE: int = 128
    QDRANT_SCROLL_BATCH_SIZE: int = 512
    CHUNK_TYPE_MODEL: str = "gemini-2.5-flash-lite"
    CHUNK_TYPE_CACHE_FILE: str = "chunk_type_cache.json"
    CHUNK_TYPE_BATCH_SIZE: int = 20
    CHUNK_TYPE_TIMEOUT_SECONDS: int = 45
    
    # ===== Logging =====
    LOG_DIR: str = "logs"
    LOG_FILE: str = "app.log"
    LOG_LEVEL: str = "INFO"
    
    # ===== Evaluation (RAGAS) =====
    EVAL_NUM_SAMPLES: int = 250
    EVAL_LLM_MODEL: str = "gemini-2.5-flash-lite"
    EVAL_EMBEDDING_MODEL: str = "dangvantuan/vietnamese-document-embedding"
    EVAL_OUTPUT_DIR: str = "data/eval/ragas"
    
    # RAG Strategy
    RAG_BROAD_MAX_CHUNKS: int = 30  # Gioi han BROAD strategy


    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Create singleton instance
settings = Settings()

# Ensure log directory exists
Path(settings.LOG_DIR).mkdir(exist_ok=True)
Path(settings.DATA_DIR).mkdir(exist_ok=True)
