import json
import logging
import re
from typing import Any, Dict, List, Optional

from google.genai.types import GenerateContentConfig

from src.config.config import settings
from src.config.genai_client import create_genai_client
from src.llm.prompts import PARAM_EXTRACT_PROMPT

logger = logging.getLogger("chatbot.param_extractor")


_VALID_GRADES = {"10", "11", "12"}
_VALID_BOOKS = {"CD", "KNTT"}
_VALID_TASK_TYPES = {"mcq", "essay", "fill_blank", "true_false", "slide", "lesson_plan"}


class ParamExtractor:
    """Extract shared request params once, then let all downstream services reuse them."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GENAI_API_KEY
        self.model_name = model_name or settings.PARAM_EXTRACT_MODEL
        self.client = None
        if self.api_key and settings.ENABLE_LLM_PARAM_EXTRACT:
            try:
                self.client = create_genai_client(
                    api_key=self.api_key,
                    timeout_seconds=settings.PARAM_EXTRACT_TIMEOUT_SECONDS,
                )
            except Exception as exc:
                logger.warning("Failed to init param extractor client: %s", exc)

    def extract(
        self,
        *,
        query: str,
        enriched_query: str = "",
        rag_queries: Optional[List[str]] = None,
        history_context: str = "",
    ) -> Dict[str, Any]:
        params = self._deterministic_extract(query, source="query")
        for source, text in (
            ("rewrite", enriched_query),
            ("rewrite", "\n".join(rag_queries or [])),
            ("history", history_context),
        ):
            self._merge_missing(params, self._deterministic_extract(text, source=source))

        if not self.client:
            params["used_llm"] = False
            return params

        try:
            prompt = PARAM_EXTRACT_PROMPT.format(
                query=query or "",
                enriched_query=enriched_query or "",
                rag_queries=json.dumps(rag_queries or [], ensure_ascii=False),
                history_context=history_context or "",
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.0,
                    response_mime_type="application/json",
                ),
            )
            llm_params = self._parse_llm_params(self._extract_text(response))
            self._merge_missing(params, llm_params)
            params["used_llm"] = True
            params["model"] = self.model_name
        except Exception as exc:
            logger.warning("ParamExtractor LLM failed: %s", str(exc)[:160])
            params["used_llm"] = False
            params["error"] = str(exc)[:160]
        return params

    async def extract_async(
        self,
        *,
        query: str,
        enriched_query: str = "",
        rag_queries: Optional[List[str]] = None,
        history_context: str = "",
    ) -> Dict[str, Any]:
        params = self._deterministic_extract(query, source="query")
        for source, text in (
            ("rewrite", enriched_query),
            ("rewrite", "\n".join(rag_queries or [])),
            ("history", history_context),
        ):
            self._merge_missing(params, self._deterministic_extract(text, source=source))

        if not self.client:
            params["used_llm"] = False
            return params

        try:
            prompt = PARAM_EXTRACT_PROMPT.format(
                query=query or "",
                enriched_query=enriched_query or "",
                rag_queries=json.dumps(rag_queries or [], ensure_ascii=False),
                history_context=history_context or "",
            )
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.0,
                    response_mime_type="application/json",
                ),
            )
            llm_params = self._parse_llm_params(self._extract_text(response))
            self._merge_missing(params, llm_params)
            params["used_llm"] = True
            params["model"] = self.model_name
        except Exception as exc:
            logger.warning("ParamExtractor LLM failed: %s", str(exc)[:160])
            params["used_llm"] = False
            params["error"] = str(exc)[:160]
        return params

    @classmethod
    def _deterministic_extract(cls, text: Optional[str], *, source: str) -> Dict[str, Any]:
        text = text or ""
        params = cls._empty_params()
        evidence = params["evidence"]

        grade = cls._extract_grade(text)
        if grade:
            params["grade"] = grade
            evidence["grade"] = source

        book = cls._extract_book(text)
        if book:
            params["book"] = book
            evidence["book"] = source

        lesson_reference = cls._extract_lesson_reference(text)
        if lesson_reference:
            params["lesson_reference"] = lesson_reference
            evidence["lesson_reference"] = source
            lesson_num = cls._extract_lesson_num(lesson_reference)
            topic_ref = cls._extract_topic_ref(lesson_reference)
            if lesson_num:
                params["lesson_num"] = lesson_num
            if topic_ref:
                params["topic_ref"] = topic_ref

        count, count_range = cls._extract_question_count(text)
        if count:
            params["question_count"] = count
            params["question_count_range"] = count_range
            evidence["question_count"] = source

        task_type = cls._extract_task_type(text)
        if task_type:
            params["task_type"] = task_type
            evidence["task_type"] = source

        params["confidence"] = 0.95 if any(params.get(k) for k in (
            "grade", "book", "lesson_reference", "question_count", "task_type"
        )) else 0.0
        return params

    @staticmethod
    def _empty_params() -> Dict[str, Any]:
        return {
            "grade": None,
            "book": None,
            "topic_ref": None,
            "lesson_num": None,
            "lesson_reference": None,
            "question_count": None,
            "question_count_range": None,
            "task_type": None,
            "confidence": 0.0,
            "evidence": {
                "grade": None,
                "book": None,
                "lesson_reference": None,
                "question_count": None,
                "task_type": None,
            },
        }

    @classmethod
    def _merge_missing(cls, base: Dict[str, Any], extra: Dict[str, Any]) -> None:
        evidence = base.setdefault("evidence", {})
        extra_evidence = extra.get("evidence") or {}
        for key in ("grade", "book", "topic_ref", "lesson_num", "lesson_reference", "question_count", "task_type"):
            if not base.get(key) and extra.get(key):
                base[key] = extra[key]
                if key in evidence:
                    evidence[key] = extra_evidence.get(key)
        if not base.get("question_count_range") and extra.get("question_count_range"):
            base["question_count_range"] = extra["question_count_range"]
        base["confidence"] = max(float(base.get("confidence") or 0.0), float(extra.get("confidence") or 0.0))

    @classmethod
    def _parse_llm_params(cls, raw: str) -> Dict[str, Any]:
        text = raw.strip()
        text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"^```\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return cls._empty_params()

        params = cls._empty_params()
        grade = str(data.get("grade") or "").strip()
        if grade in _VALID_GRADES:
            params["grade"] = grade
        book = str(data.get("book") or "").strip().upper()
        if book in _VALID_BOOKS:
            params["book"] = book
        task_type = str(data.get("task_type") or "").strip()
        if task_type in _VALID_TASK_TYPES:
            params["task_type"] = task_type

        for key in ("topic_ref", "lesson_num", "lesson_reference"):
            value = data.get(key)
            if isinstance(value, str) and value.strip() and value.strip().lower() != "null":
                params[key] = value.strip()

        count = data.get("question_count")
        if isinstance(count, int):
            params["question_count"] = max(1, min(10, count))
        count_range = data.get("question_count_range")
        if (
            isinstance(count_range, list)
            and len(count_range) == 2
            and all(isinstance(item, int) for item in count_range)
        ):
            low, high = sorted(count_range)
            params["question_count_range"] = [max(1, low), min(10, high)]
            if not params["question_count"]:
                params["question_count"] = params["question_count_range"][0]

        try:
            params["confidence"] = max(0.0, min(1.0, float(data.get("confidence") or 0.0)))
        except (TypeError, ValueError):
            pass

        evidence = data.get("evidence")
        if isinstance(evidence, dict):
            for key in params["evidence"]:
                value = evidence.get(key)
                if value in ("query", "rewrite", "history"):
                    params["evidence"][key] = value
        return params

    @staticmethod
    def _extract_text(response) -> str:
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

    @staticmethod
    def _extract_grade(text: str) -> Optional[str]:
        match = re.search(r"(?:lớp|lop|tin(?:\s*học)?|grade)\s*(10|11|12)", text, re.IGNORECASE)
        return match.group(1) if match else None

    @staticmethod
    def _extract_book(text: str) -> Optional[str]:
        text_lower = text.lower()
        if re.search(r"\b(kntt|kết\s*nối\s*tri\s*thức|ket\s*noi\s*tri\s*thuc)\b", text_lower):
            return "KNTT"
        if re.search(r"\b(cd|cánh\s*diều|canh\s*dieu)\b", text_lower):
            return "CD"
        return None

    @staticmethod
    def _extract_lesson_reference(text: str) -> Optional[str]:
        match = re.search(
            r"((?:bài|bai)\s*\d+(?:\s*(?:chủ đề|chu de|chương|chuong)\s*[a-zA-Z0-9]+)?|"
            r"(?:chủ đề|chu de|chương|chuong)\s*[a-zA-Z0-9]+(?:\s*(?:bài|bai)\s*\d+)?)",
            text,
            re.IGNORECASE,
        )
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_lesson_num(text: str) -> Optional[str]:
        match = re.search(r"(?:bài|bai)\s*(\d+)", text, re.IGNORECASE)
        return match.group(1) if match else None

    @staticmethod
    def _extract_topic_ref(text: str) -> Optional[str]:
        match = re.search(r"(?:chủ đề|chu de|chương|chuong)\s*([a-zA-Z0-9]+)", text, re.IGNORECASE)
        return match.group(1).upper() if match else None

    @staticmethod
    def _extract_question_count(text: str) -> tuple[Optional[int], Optional[List[int]]]:
        range_match = re.search(
            r"(\d+)\s*(?:[-–—]|đến|toi|tới)\s*(\d+)\s*(?:câu(?:\s*hỏi)?|question(?:s)?)",
            text,
            re.IGNORECASE,
        )
        if range_match:
            low, high = sorted((int(range_match.group(1)), int(range_match.group(2))))
            low = max(1, min(10, low))
            high = max(1, min(10, high))
            return low, [low, high]

        single_match = re.search(
            r"(\d+)\s*(?:câu(?:\s*hỏi)?|question(?:s)?)",
            text,
            re.IGNORECASE,
        )
        if single_match:
            num = max(1, min(10, int(single_match.group(1))))
            return num, None
        return None, None

    @staticmethod
    def _extract_task_type(text: str) -> Optional[str]:
        text_lower = text.lower()
        if re.search(r"\b(slide|slides|bài\s*giảng|bai\s*giang)\b", text_lower):
            return "slide"
        if re.search(r"\b(giáo\s*án|giao\s*an|lesson\s*plan)\b", text_lower):
            return "lesson_plan"
        if re.search(r"\b(trắc\s*nghiệm|trac\s*nghiem|mcq|multiple\s*choice)\b", text_lower):
            return "mcq"
        if re.search(r"\b(tự\s*luận|tu\s*luan|essay)\b", text_lower):
            return "essay"
        if re.search(r"\b(điền\s*khuyết|dien\s*khuyet|fill\s*blank)\b", text_lower):
            return "fill_blank"
        if re.search(r"\b(đúng\s*sai|dung\s*sai|true\s*false)\b", text_lower):
            return "true_false"
        return None


__all__ = ["ParamExtractor"]
