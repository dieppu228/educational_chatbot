# Plan: Web Search & Media Tool (Tavily) — MCP Integration

> **Mục tiêu**: Implement `WebSearchTool` sử dụng Tavily API, giao tiếp qua MCP layer in-process có sẵn trong repo, hỗ trợ tìm kiếm text + ảnh/GIF/animation liên quan tới bài học Tin học THPT.

> **Trạng thái hiện tại**: File `src/tools/implementations/web_search_tool.py` đang trống. Schemas placeholder (`WebSearchInput`, `WebSearchOutput`, `WebSearchResult`) đã có trong `src/tools/schemas.py`. MCP layer (protocol, server, client, registry) đã hoạt động.

---

## 1. Tổng quan kiến trúc

```text
MediaResearchAgent / Orchestrator / bất kỳ caller nào
        |
        v
  MCPToolClient.call_tool("web_search", params)
        |
        v
  MCPToolServer → ToolRegistry → WebSearchTool.execute(params)
        |
        v
  TavilyClient.search(query, include_images=True, ...)
        |
        v
  Parse response → WebSearchOutput (text results + media items)
        |
        v
  MCPResponse → trả về cho caller
```

**Nguyên tắc thiết kế:**
- Tool giao tiếp hoàn toàn qua MCP protocol hiện có (in-process, không cần HTTP).
- Tuân theo pattern `BaseTool` → `ToolRegistry` → `MCPToolServer` giống `KnowledgeRetrievalTool`.
- Fallback graceful: nếu Tavily fail (hết quota, network), trả kết quả rỗng thay vì crash pipeline.
- Tách biệt text search và media search thành 2 mode trong cùng 1 tool.

---

## 2. Dependencies cần thêm

### 2.1. Python package

```bash
pip install tavily-python
```

Thêm vào `requirements.txt`:
```
tavily-python>=0.5.0
```

### 2.2. Environment variable

Thêm vào `.env`:
```env
TAVILY_API_KEY=tvly-YOUR_API_KEY
```

### 2.3. Config

Thêm vào `src/config/config.py` class `Settings`:
```python
# ===== Web Search (Tavily) =====
TAVILY_API_KEY: str = Field(default="", env="TAVILY_API_KEY")
TAVILY_SEARCH_DEPTH: str = "advanced"      # basic | advanced
TAVILY_MAX_RESULTS: int = 5
TAVILY_INCLUDE_IMAGES: bool = True
TAVILY_INCLUDE_IMAGE_DESCRIPTIONS: bool = True
```

---

## 3. Schema Updates — `src/tools/schemas.py`

Mở rộng placeholder schemas hiện có để hỗ trợ media.

### 3.1. Input Schema

```python
class WebSearchInput(BaseModel):
    """Input cho WebSearchTool."""
    query: str = Field(..., description="Từ khoá tìm kiếm")
    top_k: int = Field(5, ge=1, le=20, description="Số kết quả text trả về")

    # ── Search mode ──
    search_mode: str = Field(
        "mixed",
        description=(
            "Chế độ tìm kiếm: "
            "'text' (chỉ text), "
            "'media' (chỉ ảnh/GIF/animation), "
            "'mixed' (cả text + media)"
        )
    )

    # ── Educational context hints ──
    topic: Optional[str] = Field(None, description="Tên chủ đề/bài học để refine query")
    grade: Optional[str] = Field(None, description="Lớp: 10, 11, 12")
    book: Optional[str] = Field(None, description="Bộ sách: CD hoặc KNTT")
    media_types: Optional[List[str]] = Field(
        None,
        description="Loại media mong muốn: ['image', 'gif', 'animation', 'diagram', 'infographic']"
    )
    language: str = Field("vi", description="Ngôn ngữ ưu tiên kết quả: 'vi' hoặc 'en'")
```

### 3.2. Output Schemas

```python
class MediaItem(BaseModel):
    """Một media item (ảnh, GIF, animation) từ web search."""
    url: str = Field(..., description="URL trực tiếp tới media")
    description: str = Field("", description="Mô tả nội dung media")
    source_url: str = Field("", description="URL trang nguồn chứa media")
    source_title: str = Field("", description="Tiêu đề trang nguồn")
    media_type: str = Field(
        "image",
        description="Loại: 'image' | 'gif' | 'animation' | 'diagram' | 'infographic'"
    )
    relevance_score: Optional[float] = Field(None, description="Điểm liên quan (0-1)")

class WebSearchResult(BaseModel):
    """Một kết quả tìm kiếm web (text)."""
    title: str = Field("", description="Tiêu đề trang")
    url: str = Field("", description="URL trang")
    snippet: str = Field("", description="Đoạn trích nội dung")
    score: Optional[float] = Field(None, description="Relevance score từ Tavily")

class WebSearchOutput(BaseModel):
    """Output đầy đủ của WebSearchTool."""
    results: List[WebSearchResult] = Field(default_factory=list, description="Kết quả text")
    media_items: List[MediaItem] = Field(default_factory=list, description="Media tìm được")
    total_results: int = Field(0, description="Tổng số kết quả text")
    total_media: int = Field(0, description="Tổng số media items")
    query_used: str = Field("", description="Query thực tế đã gửi Tavily (sau khi refine)")
    search_mode: str = Field("mixed", description="Mode đã dùng")
```

---

## 4. Tool Implementation — `src/tools/implementations/web_search_tool.py`

### 4.1. Core logic

```python
"""web_search_tool.py — WebSearchTool backed by Tavily API.

Cung cấp khả năng tìm kiếm web cho hệ thống:
  - Tìm kiếm text (bài viết, tài liệu bổ sung)
  - Tìm kiếm media (ảnh, GIF, animation, diagram) minh hoạ bài học
  - Mixed mode (cả text + media)

Giao tiếp qua MCP layer in-process:
  MCPToolClient → MCPToolServer → ToolRegistry → WebSearchTool
"""

import logging
import re
from typing import Optional, List

from src.tools.base_tool import BaseTool, ToolResult
from src.tools.schemas import (
    WebSearchInput, WebSearchOutput,
    WebSearchResult, MediaItem,
)
from src.config.config import settings

logger = logging.getLogger("chatbot.tools.web_search")


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
        "media_types": {"type": "array", "description": "image, gif, animation, ..."},
        "language": {"type": "string", "description": "vi hoặc en"},
    }

    def __init__(self):
        self._client = None  # Lazy init

    @property
    def client(self):
        """Lazy initialize TavilyClient."""
        if self._client is None:
            api_key = settings.TAVILY_API_KEY
            if not api_key:
                raise RuntimeError(
                    "TAVILY_API_KEY chưa được cấu hình. "
                    "Thêm TAVILY_API_KEY=tvly-xxx vào .env"
                )
            from tavily import TavilyClient
            self._client = TavilyClient(api_key=api_key)
        return self._client

    def execute(self, params: dict) -> ToolResult:
        """Thực thi web search qua Tavily."""

        # ① Validate input
        try:
            inp = WebSearchInput(**params)
        except Exception as e:
            return ToolResult(success=False, error=f"Invalid input: {e}")

        # ② Refine query cho educational context
        refined_query = self._refine_query(inp)

        # ③ Gọi Tavily
        try:
            include_images = inp.search_mode in ("media", "mixed")
            raw = self.client.search(
                query=refined_query,
                search_depth=settings.TAVILY_SEARCH_DEPTH,
                max_results=inp.top_k,
                include_images=include_images,
                include_image_descriptions=include_images,
                include_answer=False,
            )
        except Exception as e:
            logger.error(f"Tavily API error: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error=f"Web search failed: {str(e)[:200]}",
                metadata={"query_used": refined_query},
            )

        # ④ Parse text results
        text_results = []
        if inp.search_mode in ("text", "mixed"):
            for r in raw.get("results", []):
                text_results.append(WebSearchResult(
                    title=r.get("title", ""),
                    url=r.get("url", ""),
                    snippet=r.get("content", ""),
                    score=r.get("score"),
                ))

        # ⑤ Parse media items
        media_items = []
        if inp.search_mode in ("media", "mixed"):
            media_items = self._parse_media(
                raw.get("images", []),
                raw.get("results", []),
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
            },
        )

    def _refine_query(self, inp: WebSearchInput) -> str:
        """Thêm educational context vào query."""
        parts = [inp.query]

        if inp.topic:
            parts.append(f'"{inp.topic}"')
        if inp.grade:
            parts.append(f"lớp {inp.grade}")

        # Nếu mode media, thêm keywords giúp tìm visual
        if inp.search_mode == "media":
            media_kw = " ".join(inp.media_types or ["hình ảnh", "minh họa"])
            parts.append(media_kw)

        # Thêm language hint
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
        items = []
        GIF_PATTERN = re.compile(r"\.gif(\?|$)", re.IGNORECASE)

        for img in images:
            # Tavily trả images dạng dict {url, description} hoặc string URL
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

            # Detect media type từ URL
            mtype = "image"
            if GIF_PATTERN.search(url):
                mtype = "gif"
            elif any(kw in url.lower() for kw in ["animation", "animated", "webm"]):
                mtype = "animation"
            elif any(kw in desc.lower() for kw in ["diagram", "sơ đồ", "biểu đồ"]):
                mtype = "diagram"
            elif any(kw in desc.lower() for kw in ["infographic"]):
                mtype = "infographic"

            # Filter by requested media types
            if media_type_filter and mtype not in media_type_filter:
                # Nhưng vẫn cho "image" qua nếu filter chứa loại generic
                if "image" not in media_type_filter:
                    continue

            # Tìm source info từ results
            source_url, source_title = self._find_source(url, results)

            items.append(MediaItem(
                url=url,
                description=desc,
                source_url=source_url,
                source_title=source_title,
                media_type=mtype,
            ))

        return items

    def _find_source(self, image_url: str, results: list) -> tuple[str, str]:
        """Tìm source page chứa image từ search results."""
        # Heuristic: match domain
        from urllib.parse import urlparse
        img_domain = urlparse(image_url).netloc

        for r in results:
            r_domain = urlparse(r.get("url", "")).netloc
            if r_domain and r_domain == img_domain:
                return r.get("url", ""), r.get("title", "")

        return "", ""
```

### 4.2. MCP definition output

Tool tự export theo chuẩn MCP qua `to_mcp_definition()` kế thừa từ `BaseTool`:

```json
{
  "name": "web_search",
  "description": "Tìm kiếm trên internet để lấy thông tin bổ sung và media minh họa...",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "Từ khoá tìm kiếm"},
      "top_k": {"type": "integer", "description": "Số kết quả text (1-20)"},
      "search_mode": {"type": "string", "description": "text | media | mixed"},
      ...
    }
  }
}
```

---

## 5. Registration & Integration

### 5.1. Đăng ký tool vào registry — `src/tools/implementations/__init__.py`

```python
from src.tools.implementations.web_search_tool import WebSearchTool

__all__ = [
    "KnowledgeRetrievalTool",
    "ContentFormatterTool",
    "WebSearchTool",
    "ToolRegistry",
]
```

### 5.2. Đăng ký vào ToolRegistry tại startup

Tại nơi khởi tạo registry (trong `app/api.py` hoặc factory):

```python
from src.tools.implementations.web_search_tool import WebSearchTool

# Trong hàm khởi tạo registry
registry.register(WebSearchTool())
```

### 5.3. Thêm shortcut vào MCPToolClient — `src/tools/mcp_client.py`

```python
def search_web(self, query: str, **kwargs) -> ToolCallResponse:
    """Shortcut: gọi web_search tool."""
    params = {"query": query, **kwargs}
    return self.call_tool("web_search", params)

def search_media(self, query: str, **kwargs) -> ToolCallResponse:
    """Shortcut: gọi web_search ở mode media."""
    params = {"query": query, "search_mode": "media", **kwargs}
    return self.call_tool("web_search", params)
```

---

## 6. Tích hợp với MediaResearchAgent

### 6.1. Cập nhật `src/llm/agents/media_research.py`

```python
class MediaResearchAgent(BaseAgent):
    agent_id = "media_research_agent"
    default_error_code = "MEDIA_AGENT_ERROR"

    def __init__(self, mcp_client=None):
        self.mcp_client = mcp_client  # Optional MCP client

    def _run(self, task: AgentTask) -> AgentTaskResult:
        inputs = task.inputs
        used_tools = []

        # ① Thử MCP web_search trước (nếu có client)
        web_media = []
        if self.mcp_client:
            try:
                response = self.mcp_client.search_media(
                    query=inputs.get("topic", ""),
                    topic=inputs.get("topic"),
                    grade=inputs.get("grade"),
                    media_types=["image", "gif", "diagram", "animation"],
                )
                if response.success and response.data:
                    web_media = response.data.get("media_items", [])
                    used_tools.append("web_search")
            except Exception as e:
                logger.warning(f"MCP web_search fallback: {e}")

        # ② Fallback: dùng LLM generate media suggestions (behavior cũ)
        agent = MediaAgent()
        result = agent.run(
            topic=inputs.get("topic", ""),
            grade=inputs.get("grade", ""),
            book=inputs.get("book", ""),
        )
        used_tools.append("llm_generation")

        # ③ Merge: web media + LLM suggestions
        payload = result.payload or {}
        if web_media:
            payload["web_media"] = web_media

        return AgentTaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            status="success" if web_media or result.status == "success" else result.status,
            artifact_type=task.expected_artifact or "media_payload",
            artifact=payload,
            confidence=0.85 if web_media else 0.75,
            used_tools=used_tools,
            latency_ms=result.latency_ms,
            error_code=result.error_code,
            error_message=result.error_message,
        )
```

### 6.2. Cập nhật `generate_media` tool trong `src/llm/graphs/tools.py`

Inject MCP client vào MediaResearchAgent:

```python
@tool
def generate_media(topic, grade, book, state):
    """Gợi ý media minh họa cho bài giảng."""
    # Lấy MCP client từ state (inject lúc graph init)
    mcp_client = state.get("mcp_client")
    result = MediaResearchAgent(mcp_client=mcp_client).run_task(task)
    ...
```

---

## 7. Flow hoạt động end-to-end

```text
1. User yêu cầu tạo slide cho "Bài 3: Biến và kiểu dữ liệu" (lớp 10, CD)
2. ContentSupervisor gọi generate_media tool
3. generate_media → MediaResearchAgent._run()
4. MediaResearchAgent gọi MCPToolClient.search_media(
       query="Biến và kiểu dữ liệu",
       topic="Biến và kiểu dữ liệu",
       grade="10",
       media_types=["image", "gif", "diagram"]
   )
5. MCPToolClient → MCPToolServer → WebSearchTool.execute()
6. WebSearchTool:
   a. Refine query: "Biến và kiểu dữ liệu tin học THPT Việt Nam hình ảnh minh họa"
   b. Gọi Tavily API: search(query, include_images=True, ...)
   c. Parse response → WebSearchOutput với media_items[]
7. Trả về MCPResponse → MediaResearchAgent
8. Agent merge web media + LLM suggestions → artifact
9. SlideMerger nhận media_payload, gắn media vào slides
```

---

## 8. File changes summary

| File | Thay đổi | Mức độ |
|---|---|---|
| `requirements.txt` | Thêm `tavily-python>=0.5.0` | Nhỏ |
| `.env` | Thêm `TAVILY_API_KEY` | Nhỏ |
| `src/config/config.py` | Thêm Tavily config fields | Nhỏ |
| `src/tools/schemas.py` | Mở rộng `WebSearchInput`, `WebSearchOutput`, thêm `MediaItem` | Trung bình |
| `src/tools/implementations/web_search_tool.py` | **Implement toàn bộ** — file chính | **Lớn** |
| `src/tools/implementations/__init__.py` | Export `WebSearchTool` | Nhỏ |
| `src/tools/mcp_client.py` | Thêm shortcut `search_web()`, `search_media()` | Nhỏ |
| `app/api.py` (hoặc factory) | Register `WebSearchTool` vào registry | Nhỏ |
| `src/llm/agents/media_research.py` | Inject MCP client, merge web + LLM media | Trung bình |
| `src/llm/graphs/tools.py` | Truyền MCP client cho `generate_media` | Nhỏ |

---

## 9. Thứ tự triển khai

### Phase 1: Foundation (không cần API key để test)
- [ ] **Step 1.1**: Thêm `tavily-python` vào `requirements.txt`
- [ ] **Step 1.2**: Thêm Tavily config vào `src/config/config.py`
- [ ] **Step 1.3**: Mở rộng schemas trong `src/tools/schemas.py` (thêm `MediaItem`, update `WebSearchInput/Output`)
- [ ] **Step 1.4**: Verify: `python3 -m py_compile src/tools/schemas.py`

### Phase 2: Tool Implementation
- [ ] **Step 2.1**: Implement `src/tools/implementations/web_search_tool.py` (core logic)
- [ ] **Step 2.2**: Export trong `__init__.py`
- [ ] **Step 2.3**: Verify: `python3 -m py_compile src/tools/implementations/web_search_tool.py`

### Phase 3: MCP Registration
- [ ] **Step 3.1**: Register `WebSearchTool` vào `ToolRegistry` tại startup
- [ ] **Step 3.2**: Thêm shortcuts `search_web()`, `search_media()` vào `MCPToolClient`
- [ ] **Step 3.3**: Verify: instantiate registry, list tools, thấy `web_search` trong danh sách

### Phase 4: Agent Integration
- [ ] **Step 4.1**: Cập nhật `MediaResearchAgent` nhận MCP client
- [ ] **Step 4.2**: Cập nhật `generate_media` tool truyền MCP client
- [ ] **Step 4.3**: Verify: compile check toàn bộ `src/llm/agents` và `src/llm/graphs`

### Phase 5: Testing & Verification
- [ ] **Step 5.1**: Thêm `.env` key, chạy standalone test: `WebSearchTool.execute({"query": "biến trong Python", "search_mode": "mixed"})`
- [ ] **Step 5.2**: Test MCP flow: `MCPToolClient → MCPToolServer → WebSearchTool`
- [ ] **Step 5.3**: Test fallback: không set `TAVILY_API_KEY`, đảm bảo pipeline không crash
- [ ] **Step 5.4**: Test integration: chạy slide generation, kiểm tra media_payload có web_media

---

## 10. Fallback & Error Handling

| Tình huống | Xử lý |
|---|---|
| `TAVILY_API_KEY` trống | Tool trả `ToolResult(success=False, error="...")` — agent fallback về LLM suggestions |
| Tavily API timeout/error | Catch exception → `ToolResult(success=False)` — không crash pipeline |
| Không tìm thấy media | Trả `media_items=[]` — slide vẫn generate bình thường không có media |
| Rate limit Tavily | Log warning, trả empty → MediaAgent dùng LLM-only path |
| Network offline | Timeout → graceful failure giống trên |

---

## 11. Tavily API Key

- **Free tier**: 1000 searches/month — đủ cho development + demo đồ án
- **Đăng ký**: https://tavily.com → lấy key dạng `tvly-xxxxxxxxxx`
- **Pricing**: Free tier không cần credit card

---

## 12. Ghi chú cho luận văn

- Tool này implement Phase 5 (MCP Integration) trong `docs/multi_agent_slide_lesson_plan_refactor.md`.
- Trong luận văn, mô tả `WebSearchTool` như **MCP-backed capability** cho `MediaResearchAgent`.
- Có thể vẽ sequence diagram: Supervisor → Agent → MCP Client → MCP Server → Tavily → Response.
- Nhấn mạnh fallback design: hệ thống vẫn hoạt động khi web search không available.
