"""tool_registry.py — Auto-discovery & registration of MCP tools.

Registry pattern: mỗi tool đăng ký 1 lần, MCP Server dùng registry
để tìm và dispatch tool calls.

Ví dụ:
    registry = ToolRegistry()
    registry.register(KnowledgeRetrievalTool(rag_service))
    registry.register(ContentFormatterTool())

    tool = registry.get("knowledge_retrieval")
    result = tool.safe_execute({"query": "biến trong Python"})
"""

import logging
from typing import Dict, List, Optional
from src.tools.base_tool import BaseTool

logger = logging.getLogger("chatbot.tools.registry")


class ToolRegistry:
    """Registry quản lý tất cả tools available cho MCP Server."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Đăng ký một tool vào registry.

        Raises:
            ValueError: nếu tool.name trùng với tool đã đăng ký
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get(self, name: str) -> Optional[BaseTool]:
        """Lấy tool theo tên. Trả về None nếu không tìm thấy."""
        return self._tools.get(name)

    def list_all(self) -> List[BaseTool]:
        """Trả về danh sách tất cả tools đã đăng ký."""
        return list(self._tools.values())

    def get_mcp_definitions(self) -> List[dict]:
        """Export tất cả tool definitions theo chuẩn MCP.

        Agent dùng output này để biết tool nào available và cách gọi.
        """
        return [tool.to_mcp_definition() for tool in self._tools.values()]

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)

    def __repr__(self) -> str:
        names = ", ".join(self._tools.keys())
        return f"<ToolRegistry: [{names}]>"


__all__ = ["ToolRegistry"]
