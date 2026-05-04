import json
import re
import os
from typing import List, Optional

from google import genai
from google.genai.types import GenerateContentConfig

from src.config.config import settings
from src.llm.prompts import QUERY_REWRITE_PROMPT
from src.utils.trace_decorator import trace_node


class QueryRewriter:

    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or settings.GENAI_API_KEY or os.getenv("GENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("GENAI_API_KEY not set.")

        # Dùng model nhẹ để giảm latency (flash-lite khuyến khích)
        self.model_name = model_name or settings.LLM_MODEL or "gemini-2.5-flash-lite"
        self.client = genai.Client(api_key=self.api_key)

    @trace_node("QueryRewriter.rewrite")
    def rewrite(self, query: str, history_context: str) -> List[str]:
        if not query or not query.strip():
            return [query]

        try:
            prompt = QUERY_REWRITE_PROMPT.format(
                query=query,
                context=history_context or "",
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )

            raw = self._extract_text(response)
            result = self._parse_result(raw, query)

            return result["queries"]

        except Exception as e:
            return [query]

    def _extract_text(self, response) -> str:
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    return part.text.strip()
        return ""

    def _parse_result(self, raw: str, original_query: str) -> dict:
        text = raw.strip()
        # Clean markdown code blocks if present
        text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

        try:
            data = json.loads(text.strip())

            needs_rewrite = data.get("needs_rewrite", False)
            queries = data.get("queries", [])

            # Validate queries
            if not isinstance(queries, list) or len(queries) == 0:
                return {"needs_rewrite": False, "queries": [original_query]}

            # Filter empty strings
            queries = [q.strip() for q in queries if isinstance(q, str) and q.strip()]

            if not queries:
                return {"needs_rewrite": False, "queries": [original_query]}

            # Cap at 3 queries max
            queries = queries[:3]

            return {"needs_rewrite": needs_rewrite, "queries": queries}

        except json.JSONDecodeError:
            return {"needs_rewrite": False, "queries": [original_query]}


__all__ = ["QueryRewriter"]
