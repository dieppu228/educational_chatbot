"""
Query Rewriter — Viết lại query dựa trên ngữ cảnh hội thoại.

Nhận query gốc + context từ ContextAnalyzer, quyết định có cần rewrite không,
và sinh ra 2-3 queries tối ưu cho việc tìm kiếm RAG.

Input:  query + history_context (từ ContextAnalyzer)
Output: List[str] — danh sách 2-3 queries đã rewrite (hoặc [query] nếu không cần)
"""

import json
import re
import os
import logging
from typing import List, Optional

from google import genai
from google.genai.types import GenerateContentConfig

from src.config.config import settings
from src.llm.prompts import QUERY_REWRITE_PROMPT

logger = logging.getLogger("chatbot.query_rewriter")


class QueryRewriter:
    """
    LLM-based query rewriter cho RAG pipeline.

    Sử dụng conversation history (từ ContextAnalyzer) để:
    1. Xác định query có cần viết lại hay không
    2. Sinh 2-3 queries tường minh, đa dạng từ khóa
    3. Fallback về [query gốc] nếu LLM call thất bại
    """

    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or settings.GENAI_API_KEY or os.getenv("GENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("GENAI_API_KEY not set.")

        # Dùng model nhẹ để giảm latency (flash-lite khuyến khích)
        self.model_name = model_name or settings.LLM_MODEL or "gemini-2.5-flash-lite"
        self.client = genai.Client(api_key=self.api_key)

    def rewrite(self, query: str, history_context: str) -> List[str]:
        """
        Viết lại query dựa trên ngữ cảnh hội thoại.

        Args:
            query: Câu hỏi hiện tại của user
            history_context: Context đã trích xuất từ ContextAnalyzer
                             (đã qua extract_context_from_history)

        Returns:
            List[str]: 2-3 queries đã rewrite, hoặc [query] nếu không cần/lỗi
        """
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

            logger.info(
                f"QueryRewriter: needs_rewrite={result['needs_rewrite']}, "
                f"queries={result['queries']}"
            )

            return result["queries"]

        except Exception as e:
            logger.error(f"QueryRewriter error: {e}")
            return [query]

    def _extract_text(self, response) -> str:
        """Extract text from API response."""
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    return part.text.strip()
        return ""

    def _parse_result(self, raw: str, original_query: str) -> dict:
        """
        Parse LLM JSON response.

        Returns:
            dict: {"needs_rewrite": bool, "queries": List[str]}
        """
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
                logger.warning(f"QueryRewriter: invalid queries format, fallback")
                return {"needs_rewrite": False, "queries": [original_query]}

            # Filter empty strings
            queries = [q.strip() for q in queries if isinstance(q, str) and q.strip()]

            if not queries:
                return {"needs_rewrite": False, "queries": [original_query]}

            # Cap at 3 queries max
            queries = queries[:3]

            return {"needs_rewrite": needs_rewrite, "queries": queries}

        except json.JSONDecodeError:
            logger.warning(f"QueryRewriter: failed to parse JSON: {raw[:200]}")
            return {"needs_rewrite": False, "queries": [original_query]}


__all__ = ["QueryRewriter"]
