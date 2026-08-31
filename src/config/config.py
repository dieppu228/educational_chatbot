from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """Runtime configuration. OS environment overrides values from `.env`."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ===== API / Server =====
    EDUBOT_HOST: str = "127.0.0.1"
    EDUBOT_PORT: int = 8000
    EDUBOT_API_TITLE: str = "EduBot API"

    # ===== Gemini / LLM =====
    GENAI_API_KEY: str = ""
    GENAI_BASE_URL: Optional[str] = None
    GENAI_API_VERSION: Optional[str] = None
    GENAI_TIMEOUT_SECONDS: int = 60
    LLM_MODEL: str = "gemini-2.5-flash-lite"
    ENABLE_LLM_PARAM_EXTRACT: bool = True
    PARAM_EXTRACT_MODEL: str = "gemini-2.5-flash-lite"
    PARAM_EXTRACT_TIMEOUT_SECONDS: int = 20

    # ===== Retrieval =====
    RETRIEVER_TOP_K: int = 25
    RERANKER_TOP_N: int = 5
    RERANKER_TOP_N_SLIDE: int = 15
    RERANKER_TOP_N_LESSON_PLAN: int = 20
    RERANKER_MIN_SCORE: float = 0.00
    RRF_K_WEIGHT: int = 60
    RAG_BROAD_MAX_CHUNKS: int = 30
    RAG_PRE_RERANK_MAX_CANDIDATES: int = 25
    RAG_PRE_RERANK_MAX_CANDIDATES_SLIDE: int = 28
    RAG_PRE_RERANK_MAX_CANDIDATES_LESSON_PLAN: int = 34
    RAG_PRE_RERANK_HRAG_QUOTA_SLIDE: int = 10
    RAG_PRE_RERANK_HRAG_QUOTA_LESSON_PLAN: int = 12

    # ===== Question Generation / Scoring =====
    MIN_QUESTIONS: int = 1
    MAX_QUESTIONS: int = 10
    DEFAULT_QUESTIONS: int = 3
    QUESTION_GENERATION_TEMPERATURE: float = 0.5
    SCORING_TEMPERATURE: float = 0.0

    # ===== Local Models =====
    EMBEDDING_MODEL: str = "dangvantuan/vietnamese-document-embedding"
    EMBEDDING_DEVICE: Optional[str] = None
    EMBEDDING_BATCH_SIZE: int = 64
    RERANKER_MODEL: str = "AITeamVN/Vietnamese_Reranker"
    RERANKER_DEVICE: Optional[str] = None
    RERANKER_BATCH_SIZE: int = 8

    # ===== File Paths =====
    DATA_DIR: str = "data"
    CHUNKS_FILE: str = "rag_chunks_v2.json"
    EMBEDDINGS_FILE: str = "embeddings.npy"
    EMBEDDINGS_META_FILE: str = "embeddings.meta.json"
    SESSION_STORAGE_DIR: str = "data/sessions"
    FRONTEND_DIST_DIR: str = "app/frontend/dist"
    SLIDE_TEMPLATE_PATH: str = "app/templates/academic_vi_slide_template.pptx"
    SLIDE_TEMPLATE_MANIFEST_PATH: str = "app/templates/academic_vi_slide_template.json"
    SLIDE_EXPORT_DIR: str = "app/data/exports"
    SLIDE_DOWNLOAD_BASE_URL: str = "/api/exports"

    # ===== Qdrant =====
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "educational_chatbot"
    QDRANT_VECTOR_SIZE: int = 768
    QDRANT_TIMEOUT_SECONDS: int = 60
    QDRANT_UPLOAD_BATCH_SIZE: int = 128
    QDRANT_SCROLL_BATCH_SIZE: int = 512

    # ===== Chunk Classification =====
    CHUNK_TYPE_MODEL: str = "gemini-2.5-flash-lite"
    CHUNK_TYPE_CACHE_FILE: str = "chunk_type_cache.json"
    CHUNK_TYPE_BATCH_SIZE: int = 20
    CHUNK_TYPE_TIMEOUT_SECONDS: int = 45

    # ===== Logging / E2E =====
    LOG_DIR: str = "logs"
    LOG_FILE: str = "app.log"
    EMBEDDING_FAILURE_LOG_FILE: str = "embedding_failures.txt"
    LOG_LEVEL: str = "INFO"
    E2E_LOG_DIR: str = "logs/e2e_runs"
    E2E_TIMEOUT_SECONDS: int = 10000

    # ===== Evaluation =====
    EVAL_NUM_SAMPLES: int = 250
    EVAL_LLM_MODEL: str = "gemini-2.5-flash-lite"
    EVAL_EMBEDDING_MODEL: str = "dangvantuan/vietnamese-document-embedding"
    EVAL_OUTPUT_DIR: str = "data/eval/ragas"
    EVAL_MAX_WORKERS: int = 2
    EVAL_MAX_RETRIES: int = 10
    EVAL_MAX_WAIT_SECONDS: int = 30

    # ===== Tavily / Web Search =====
    TAVILY_API_KEY: str = ""
    TAVILY_BASE_URL: str = "https://api.tavily.com"
    TAVILY_SEARCH_DEPTH: str = "advanced"
    TAVILY_MAX_RESULTS: int = 5
    TAVILY_INCLUDE_IMAGES: bool = True
    TAVILY_INCLUDE_IMAGE_DESCRIPTIONS: bool = True
    TAVILY_TIMEOUT_SECONDS: int = 15

    # ===== Remote Media Export =====
    MEDIA_DOWNLOAD_TIMEOUT_SECONDS: float = 8.0
    MEDIA_DOWNLOAD_MAX_BYTES: int = 8388608

    # ===== Quality Degradation =====
    SLIDE_QUALITY_HARD_FLOOR: float = 0.0


settings = Settings()


def project_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


project_path(settings.LOG_DIR).mkdir(parents=True, exist_ok=True)
project_path(settings.DATA_DIR).mkdir(parents=True, exist_ok=True)


__all__ = ["ENV_FILE", "PROJECT_ROOT", "Settings", "project_path", "settings"]
