"""tools package — MCP infrastructure cho Educational Chatbot.

Cung cấp:
  - BaseTool / ToolResult: abstract base cho mọi tool
  - MCPToolServer / MCPToolClient: giao tiếp MCP in-process
  - ToolRegistry: auto-discovery và quản lý tools
  - Schemas: Pydantic models cho I/O validation
"""

from src.tools.base_tool import BaseTool, ToolResult
from src.tools.mcp_protocol import MCPMethod, MCPRequest, MCPResponse
from src.tools.mcp_server import MCPToolServer
from src.tools.mcp_client import MCPToolClient
from src.tools.implementations.tool_registry import ToolRegistry

__all__ = [
    "BaseTool", "ToolResult",
    "MCPMethod", "MCPRequest", "MCPResponse",
    "MCPToolServer", "MCPToolClient",
    "ToolRegistry",
]
