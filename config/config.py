"""Configuration management using Pydantic Settings"""

from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import os


class Settings(BaseSettings):
    """Main application settings"""
    
    # ===== API Configuration =====
    GENAI_API_KEY: str = Field(default="", env="GENAI_API_KEY")
    LLM_MODEL: str = "gemini-2.5-flash-lite"
    
    # ===== Retrieval Configuration =====
    RETRIEVER_TOP_K: int = 60
    RERANKER_TOP_N: int = 10
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
    RERANKER_MODEL: str = "BAAI/bge-reranker-v2-m3"
    
    # ===== File Paths =====
    DATA_DIR: str = "data"
    CHUNKS_FILE: str = "rag_chunks.json"
    EMBEDDINGS_FILE: str = "embeddings.npy"
    
    # ===== Logging =====
    LOG_DIR: str = "logs"
    LOG_FILE: str = "app.log"
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Create singleton instance
settings = Settings()

# Ensure log directory exists
Path(settings.LOG_DIR).mkdir(exist_ok=True)
Path(settings.DATA_DIR).mkdir(exist_ok=True)
