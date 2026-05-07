"""base_tool.py — Abstract base class cho mọi tool trong hệ thống MCP.

MCP (Model Context Protocol) cho phép Agent gọi các tool bên ngoài.
Mỗi tool cần implement interface này để Agent biết:
  1. Tool tên gì (name)
  2. Tool làm gì (description)
  3. Tool nhận input gì (input_schema)
  4. Tool trả về gì (execute → ToolResult)

Ví dụ thực tế:
  - KnowledgeRetrievalTool: tra cứu SGK qua RAG pipeline
  - WebSearchTool: tìm kiếm trên internet
  - ContentFormatterTool: format kết quả cho LLM
"""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Dict


# ============================================================
# TOOL RESULT — Kết quả trả về sau khi tool thực thi
# ============================================================

@dataclass
class ToolResult:
    """Kết quả chuẩn hoá mà mọi tool đều trả về.

    Attributes:
        success: True nếu tool chạy thành công, False nếu lỗi.
        data: Dữ liệu kết quả (list chunks, formatted text, ...).
        error: Thông báo lỗi nếu success=False.
        metadata: Thông tin bổ sung (thời gian chạy, strategy, ...).
    """
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# BASE TOOL — Interface mà mọi tool phải implement
# ============================================================

class BaseTool(ABC):
    """Abstract base class cho mọi MCP tool.

    Mỗi tool khi kế thừa BaseTool cần định nghĩa:
      - name: tên unique của tool (vd: "knowledge_retrieval")
      - description: mô tả ngắn cho Agent hiểu tool làm gì
      - input_schema: JSON schema mô tả input mà tool nhận
      - execute(): logic chính của tool

    Ví dụ:
        class MyTool(BaseTool):
            name = "my_tool"
            description = "Mô tả tool"
            input_schema = {"query": {"type": "string", "description": "..."}}

            def execute(self, params: dict) -> ToolResult:
                # Xử lý logic
                return ToolResult(success=True, data=result)
    """

    # ── Subclass PHẢI override 3 thuộc tính này ──────────────
    name: str = ""
    description: str = ""
    input_schema: Dict[str, Any] = {}

    @abstractmethod
    def execute(self, params: dict) -> ToolResult:
        """Thực thi tool với params đầu vào.

        Args:
            params: Dictionary chứa input theo input_schema.
                    Ví dụ: {"query": "biến trong Python", "book": "CD"}

        Returns:
            ToolResult với success=True/False và data hoặc error.
        """
        ...

    def safe_execute(self, params: dict) -> ToolResult:
        """Wrapper tự động bắt lỗi và đo thời gian.

        Agent nên gọi safe_execute() thay vì execute() trực tiếp
        để đảm bảo mọi lỗi đều được handle gracefully.
        """
        t0 = time.time()
        try:
            result = self.execute(params)
            result.metadata["execution_time_s"] = round(time.time() - t0, 3)
            return result
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"[{self.name}] {type(e).__name__}: {str(e)[:200]}",
                metadata={"execution_time_s": round(time.time() - t0, 3)},
            )

    def to_mcp_definition(self) -> dict:
        """Export tool definition theo chuẩn MCP.

        MCP Server sẽ gọi method này để trả về danh sách tools
        cho Agent biết tool nào available và cách gọi.

        Returns:
            Dict theo format MCP:
            {
                "name": "knowledge_retrieval",
                "description": "Tra cứu SGK...",
                "inputSchema": {
                    "type": "object",
                    "properties": { ... }
                }
            }
        """
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": self.input_schema,
            },
        }

    def __repr__(self) -> str:
        return f"<Tool:{self.name}>"


__all__ = ["BaseTool", "ToolResult"]
