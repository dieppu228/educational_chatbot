"""tavily_service.py — Lớp service gọi Tavily Search API qua HTTP.

Tách riêng phần giao tiếp mạng khỏi WebSearchTool để:
  - WebSearchTool chỉ lo validate I/O + parse kết quả (business logic của tool)
  - TavilyService chỉ lo gọi HTTP tới Tavily endpoint (transport)

Nhờ vậy `base_url` có thể trỏ tới mock server khi dev/test, và đổi sang
endpoint thật chỉ cần sửa `settings.TAVILY_BASE_URL` — không động vào tool.

Tham chiếu format request/response Tavily:
  POST {base_url}/search
  body: {api_key, query, search_depth, max_results, include_images, ...}
  resp: {results: [{title,url,content,score}], images: [{url,description}], ...}
"""

import logging
from typing import Optional, List

import httpx

from src.config.config import settings

logger = logging.getLogger("chatbot.tools.tavily")


class TavilyServiceError(Exception):
    """Lỗi khi gọi Tavily API (network, HTTP, thiếu key)."""


class TavilyService:
    """HTTP client gọi Tavily Search API.

    Args:
        api_key: Tavily API key. Mặc định lấy từ settings.TAVILY_API_KEY.
        base_url: Endpoint gốc. Mặc định settings.TAVILY_BASE_URL (mock được).
        timeout: Timeout giây cho mỗi request.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self.api_key = api_key if api_key is not None else settings.TAVILY_API_KEY
        self.base_url = (base_url or settings.TAVILY_BASE_URL).rstrip("/")
        self.timeout = timeout or settings.TAVILY_TIMEOUT_SECONDS

    def search(
        self,
        query: str,
        *,
        search_depth: Optional[str] = None,
        max_results: Optional[int] = None,
        include_images: bool = True,
        include_image_descriptions: bool = True,
        include_answer: bool = False,
    ) -> dict:
        """Gọi Tavily /search và trả về JSON thô (dict).

        Raises:
            TavilyServiceError: nếu thiếu api_key hoặc request thất bại.
        """
        if not self.api_key:
            raise TavilyServiceError(
                "TAVILY_API_KEY chưa được cấu hình. Thêm TAVILY_API_KEY=tvly-xxx vào .env"
            )

        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth or settings.TAVILY_SEARCH_DEPTH,
            "max_results": max_results or settings.TAVILY_MAX_RESULTS,
            "include_images": include_images,
            "include_image_descriptions": include_image_descriptions,
            "include_answer": include_answer,
        }

        url = f"{self.base_url}/search"
        try:
            resp = httpx.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            status = e.response.status_code if e.response is not None else "?"
            raise TavilyServiceError(
                f"Tavily trả HTTP {status} cho query={query!r}"
            ) from e
        except httpx.HTTPError as e:
            raise TavilyServiceError(
                f"Lỗi mạng khi gọi Tavily: {type(e).__name__}: {str(e)[:160]}"
            ) from e
        except ValueError as e:  # JSON decode
            raise TavilyServiceError(
                f"Tavily trả về body không phải JSON hợp lệ: {str(e)[:160]}"
            ) from e


__all__ = ["TavilyService", "TavilyServiceError"]
