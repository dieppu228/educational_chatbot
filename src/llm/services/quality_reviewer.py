import json
import logging
import re
from typing import Any, Optional

from google import genai
from google.genai.types import GenerateContentConfig

from src.config.config import settings
from src.llm.prompts import (
    QUIZ_QUALITY_REVIEW_PROMPT,
    SLIDE_QUALITY_REVIEW_PROMPT,
    LESSON_PLAN_QUALITY_REVIEW_PROMPT,
)
from src.schemas.slide_schemas import QualityReviewResult

logger = logging.getLogger("chatbot.quality_reviewer")


class BaseQualityReviewer:
    prompt_template: str = ""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GENAI_API_KEY
        self.model_name = model_name or settings.LLM_MODEL
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as exc:
            logger.warning(f"Failed to init quality reviewer client: {exc}")
            self.client = None

    def review(self, query: str, context: str, output: Any) -> QualityReviewResult:
        if not self.client:
            return QualityReviewResult.fallback_fail(
                reason="FORMAT_INVALID",
                message="Quality reviewer client is not initialized.",
            )

        prompt = self._build_prompt(query, context, output)
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )
            text = self._extract_text(response)
            data = json.loads(self._strip_fences(text))
            return QualityReviewResult(**data)
        except Exception as exc:
            return QualityReviewResult.fallback_fail(
                reason="FORMAT_INVALID",
                message=f"Quality reviewer failed: {str(exc)[:200]}",
            )

    async def review_async(self, query: str, context: str, output: Any) -> QualityReviewResult:
        if not self.client:
            return QualityReviewResult.fallback_fail(
                reason="FORMAT_INVALID",
                message="Quality reviewer client is not initialized.",
            )

        prompt = self._build_prompt(query, context, output)
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )
            text = self._extract_text(response)
            data = json.loads(self._strip_fences(text))
            return QualityReviewResult(**data)
        except Exception as exc:
            return QualityReviewResult.fallback_fail(
                reason="FORMAT_INVALID",
                message=f"Quality reviewer failed: {str(exc)[:200]}",
            )

    def _build_prompt(self, query: str, context: str, output: Any) -> str:
        output_text = (
            json.dumps(output, ensure_ascii=False, indent=2)
            if not isinstance(output, str)
            else output
        )
        return self.prompt_template.format(
            query=query,
            context=context[:12000],
            output=output_text[:16000],
        )

    def _extract_text(self, response) -> str:
        if getattr(response, "text", None):
            return response.text.strip()
        candidates = getattr(response, "candidates", None) or []
        if candidates:
            content = getattr(candidates[0], "content", None)
            parts = getattr(content, "parts", None) or []
            for part in parts:
                if hasattr(part, "text") and part.text:
                    return part.text.strip()
        return ""

    def _strip_fences(self, text: str) -> str:
        cleaned = text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned.strip()


class QuizQualityReviewer(BaseQualityReviewer):
    prompt_template = QUIZ_QUALITY_REVIEW_PROMPT


class SlideQualityReviewer(BaseQualityReviewer):
    prompt_template = SLIDE_QUALITY_REVIEW_PROMPT


class LessonPlanQualityReviewer(BaseQualityReviewer):
    prompt_template = LESSON_PLAN_QUALITY_REVIEW_PROMPT


def get_quality_reviewer(task_type: str) -> BaseQualityReviewer:
    if task_type.startswith("quiz") or task_type in ("mcq", "essay", "fill_blank", "true_false"):
        return QuizQualityReviewer()
    if task_type == "lesson_plan":
        return LessonPlanQualityReviewer()
    return SlideQualityReviewer()


__all__ = [
    "BaseQualityReviewer",
    "QuizQualityReviewer",
    "SlideQualityReviewer",
    "LessonPlanQualityReviewer",
    "get_quality_reviewer",
]
