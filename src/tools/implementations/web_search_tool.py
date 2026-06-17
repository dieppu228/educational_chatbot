"""web_search_tool.py — WebSearchTool (MCP) backed by Tavily.

Cung cấp khả năng tìm kiếm web cho hệ thống:
  - text: bài viết, tài liệu bổ sung
  - media: ảnh, GIF, animation, diagram minh hoạ bài học
  - mixed: cả hai

Kiến trúc phân lớp:
  Agent → MCPToolClient.call_tool("web_search")
        → MCPToolServer → ToolRegistry → WebSearchTool.execute()   (lớp này)
        → TavilyService.search()                                    (HTTP transport)

WebSearchTool chỉ lo validate I/O, refine query và parse kết quả; phần gọi
mạng được uỷ cho TavilyService (base_url mock được qua settings).
"""

import logging
import re
from typing import Optional, List, Tuple
from urllib.parse import urlparse

from src.tools.base_tool import BaseTool, ToolResult
from src.tools.schemas import (
    WebSearchInput, WebSearchOutput,
    WebSearchResult, MediaItem,
)
from src.tools.services.tavily_service import TavilyService, TavilyServiceError
from src.config.config import settings

logger = logging.getLogger("chatbot.tools.web_search")

_GIF_PATTERN = re.compile(r"\.gif(\?|$)", re.IGNORECASE)


class WebSearchTool(BaseTool):
    """MCP Tool tìm kiếm web + media qua Tavily API."""

    name = "web_search"
    description = (
        "Tìm kiếm trên internet để lấy thông tin bổ sung và media minh họa "
        "(ảnh, GIF, animation, diagram) liên quan tới bài học Tin học THPT. "
        "Dùng khi kiến thức SGK không đủ hoặc cần visual minh hoạ."
    )
    input_schema = {
        "query": {"type": "string", "description": "Từ khoá tìm kiếm"},
        "top_k": {"type": "integer", "description": "Số kết quả text (1-20)"},
        "search_mode": {"type": "string", "description": "text | media | mixed"},
        "topic": {"type": "string", "description": "Tên bài học/chủ đề"},
        "grade": {"type": "string", "description": "Lớp 10, 11, 12"},
        "book": {"type": "string", "description": "CD hoặc KNTT"},
        "media_types": {"type": "array", "description": "image, gif, animation, ..."},
        "language": {"type": "string", "description": "vi hoặc en"},
    }

    def __init__(self, service: Optional[TavilyService] = None):
        """
        Args:
            service: TavilyService đã khởi tạo. Nếu None → lazy-init mặc định
                     (đọc base_url/api_key từ settings). Cho phép inject mock khi test.
        """
        self._service = service

    @property
    def service(self) -> TavilyService:
        if self._service is None:
            self._service = TavilyService()
        return self._service

    def execute(self, params: dict) -> ToolResult:
        # ① Validate input
        try:
            inp = WebSearchInput(**params)
        except Exception as e:
            return ToolResult(success=False, error=f"Invalid input: {e}")

        # ② Refine query cho educational context
        refined_query = self._refine_query(inp)

        # ③ Gọi Tavily qua service
        include_images = inp.search_mode in ("media", "mixed")
        try:
            raw = self.service.search(
                refined_query,
                search_depth=settings.TAVILY_SEARCH_DEPTH,
                max_results=inp.top_k,
                include_images=include_images,
                include_image_descriptions=include_images,
                include_answer=False,
            )
        except TavilyServiceError as e:
            # Fallback graceful: không crash pipeline, agent sẽ dùng path khác
            logger.warning(f"WebSearchTool: Tavily không khả dụng — {e}")
            return ToolResult(
                success=False,
                error=f"Web search failed: {str(e)[:200]}",
                metadata={"query_used": refined_query},
            )

        # ④ Parse text results
        text_results: List[WebSearchResult] = []
        if inp.search_mode in ("text", "mixed"):
            for r in raw.get("results", []) or []:
                text_results.append(WebSearchResult(
                    title=r.get("title", ""),
                    url=r.get("url", ""),
                    snippet=r.get("content", ""),
                    score=r.get("score"),
                ))

        # ⑤ Parse media items
        media_items: List[MediaItem] = []
        if include_images:
            media_items = self._parse_media(
                raw.get("images", []) or [],
                raw.get("results", []) or [],
                inp.media_types,
            )

        # ⑥ Build output
        output = WebSearchOutput(
            results=text_results,
            media_items=media_items,
            total_results=len(text_results),
            total_media=len(media_items),
            query_used=refined_query,
            search_mode=inp.search_mode,
        )

        logger.info(
            f"WebSearchTool: query='{refined_query[:60]}' "
            f"→ {len(text_results)} text, {len(media_items)} media"
        )

        return ToolResult(
            success=True,
            data=output.model_dump(),
            metadata={
                "total_results": len(text_results),
                "total_media": len(media_items),
                "search_mode": inp.search_mode,
                "query_used": refined_query,
            },
        )

    # ── helpers ──────────────────────────────────────────────

    def _refine_query(self, inp: WebSearchInput) -> str:
        """Thêm educational context vào query."""
        parts = [inp.query]
        if inp.topic:
            parts.append(f'"{inp.topic}"')
        if inp.grade:
            parts.append(f"lớp {inp.grade}")
        if inp.search_mode == "media":
            media_kw = " ".join(inp.media_types or ["hình ảnh", "minh họa"])
            parts.append(media_kw)
        if inp.language == "vi":
            parts.append("tin học THPT Việt Nam")
        return " ".join(parts)

    def _parse_media(
        self,
        images: list,
        results: list,
        media_type_filter: Optional[List[str]],
    ) -> List[MediaItem]:
        """Parse images từ Tavily response thành MediaItem list."""
        items: List[MediaItem] = []

        for img in images:
            if isinstance(img, dict):
                url = img.get("url", "")
                desc = img.get("description", "")
            elif isinstance(img, str):
                url = img
                desc = ""
            else:
                continue

            if not url:
                continue

            mtype = self._detect_media_type(url, desc)

            # Filter theo loại yêu cầu (generic "image" vẫn cho qua nếu filter có)
            if media_type_filter and mtype not in media_type_filter:
                if "image" not in media_type_filter:
                    continue

            source_url, source_title = self._find_source(url, results)
            items.append(MediaItem(
                url=url,
                description=desc,
                source_url=source_url,
                source_title=source_title,
                media_type=mtype,
            ))

        return items

    @staticmethod
    def _detect_media_type(url: str, desc: str) -> str:
        url_l = url.lower()
        desc_l = desc.lower()
        if _GIF_PATTERN.search(url):
            return "gif"
        if any(kw in url_l for kw in ("animation", "animated", "webm")):
            return "animation"
        if any(kw in desc_l for kw in ("diagram", "sơ đồ", "biểu đồ")):
            return "diagram"
        if "infographic" in desc_l:
            return "infographic"
        return "image"

    @staticmethod
    def _find_source(image_url: str, results: list) -> Tuple[str, str]:
        """Tìm source page chứa image (heuristic match domain)."""
        img_domain = urlparse(image_url).netloc
        for r in results:
            r_domain = urlparse(r.get("url", "")).netloc
            if r_domain and r_domain == img_domain:
                return r.get("url", ""), r.get("title", "")
        return "", ""


__all__ = ["WebSearchTool"]
