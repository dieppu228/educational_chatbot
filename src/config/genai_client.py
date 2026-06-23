from typing import Optional

from google import genai
from google.genai.types import HttpOptions

from src.config.config import settings


def create_genai_client(
    api_key: Optional[str] = None,
    timeout_seconds: Optional[int] = None,
) -> genai.Client:
    """Create a Gemini client using centralized environment-backed settings."""
    options = {
        "timeout": int(
            (timeout_seconds or settings.GENAI_TIMEOUT_SECONDS) * 1000
        ),
    }
    if settings.GENAI_BASE_URL:
        options["base_url"] = settings.GENAI_BASE_URL
    if settings.GENAI_API_VERSION:
        options["api_version"] = settings.GENAI_API_VERSION

    return genai.Client(
        api_key=api_key or settings.GENAI_API_KEY,
        http_options=HttpOptions(**options),
    )


__all__ = ["create_genai_client"]
