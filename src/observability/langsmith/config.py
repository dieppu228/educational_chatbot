import os
from dataclasses import dataclass


TRUE_VALUES = {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class LangSmithLocalSettings:
    """LangSmith settings read from environment variables.

    "Local" here means the instrumentation is scoped to this codebase and can
    be turned on only for selected pipelines. Traces are still sent to the
    configured LangSmith endpoint when enabled.
    """

    enabled: bool = False
    project: str = "educational-chatbot-local"
    endpoint: str = "https://api.smith.langchain.com"
    api_key: str = ""


def get_langsmith_settings() -> LangSmithLocalSettings:
    return LangSmithLocalSettings(
        enabled=os.getenv("LANGSMITH_TRACING", "").lower() in TRUE_VALUES,
        project=os.getenv("LANGSMITH_PROJECT", "educational-chatbot-local"),
        endpoint=os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com"),
        api_key=os.getenv("LANGSMITH_API_KEY", ""),
    )


__all__ = ["LangSmithLocalSettings", "get_langsmith_settings"]

