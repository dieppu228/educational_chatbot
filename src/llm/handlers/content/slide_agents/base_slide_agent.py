
import time
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from src.config.config import settings
from src.schemas.slide_schemas import AgentResult

logger = logging.getLogger("chatbot.slide_agent")


class BaseSlideAgent(ABC):

    agent_name: str = "base"
    max_retries: int = 1
    error_code: str = "AGENT_ERROR"

    def __init__(self):
        try:
            from google import genai
            self.client = genai.Client(api_key=settings.GENAI_API_KEY)
        except Exception as e:
            logger.error(f"Failed to init GenAI client: {e}")
            self.client = None
        self.model = settings.LLM_MODEL

    def run(self, **kwargs) -> AgentResult:
        t0 = time.time()
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                payload = self._execute(**kwargs)
                latency_ms = int((time.time() - t0) * 1000)
                logger.info(
                    f"[{self.agent_name}] success "
                    f"(attempt {attempt + 1}, {latency_ms}ms)"
                )
                return AgentResult(
                    agent=self.agent_name,
                    status="success",
                    latency_ms=latency_ms,
                    payload=payload,
                )
            except Exception as e:
                last_error = e
                logger.warning(
                    f"[{self.agent_name}] attempt {attempt + 1} failed: {e}"
                )
                if attempt < self.max_retries:
                    continue

        # All retries exhausted
        latency_ms = int((time.time() - t0) * 1000)
        logger.error(
            f"[{self.agent_name}] FAILED after {self.max_retries + 1} attempts: {last_error}"
        )
        return AgentResult(
            agent=self.agent_name,
            status="failed",
            latency_ms=latency_ms,
            error_code=self.error_code,
            error_message=str(last_error)[:200] if last_error else None,
        )

    @abstractmethod
    def _execute(self, **kwargs) -> dict:
        pass

    def _call_llm(
        self,
        prompt: str,
        temperature: float = 0.3,
        response_mime: str = "application/json",
    ) -> str:
        if not self.client:
            raise RuntimeError("GenAI client not initialized")

        from src.llm.prompts import SYSTEM_PROMPT_SHORT

        full_prompt = f"{SYSTEM_PROMPT_SHORT}\n\n{prompt}"
        config = {
            "temperature": temperature,
            "response_mime_type": response_mime,
            "top_p": 0.95,
        }
        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
            config=config,
        )
        return response.text

    def _parse_json(self, text: str) -> dict:
        cleaned = text.strip()
        # Remove markdown code fences if present
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            # Remove first and last lines (```json and ```)
            lines = [l for l in lines[1:] if not l.strip() == "```"]
            cleaned = "\n".join(lines)
        return json.loads(cleaned)


__all__ = ["BaseSlideAgent"]
