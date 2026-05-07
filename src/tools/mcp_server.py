"""mcp_server.py — MCP Server nhận request và dispatch tới tool.

Server là "cầu nối" giữa Agent (qua Client) và các Tools:
  Client → MCPRequest → Server → ToolRegistry → Tool.execute() → MCPResponse

Trong scope ĐATN, server chạy in-process (cùng Python process).
Không cần HTTP/gRPC — Client gọi Server trực tiếp qua method calls.
"""

import uuid
import logging
from typing import List

from src.tools.base_tool import ToolResult
from src.tools.implementations.tool_registry import ToolRegistry
from src.tools.mcp_protocol import (
    MCPMethod, MCPRequest, MCPResponse,
)
from src.tools.schemas import ToolCallResponse

logger = logging.getLogger("chatbot.tools.mcp_server")


class MCPToolServer:
    """MCP Server — nhận MCPRequest, dispatch tới tool, trả MCPResponse."""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        logger.info(f"MCPToolServer initialized with {len(registry)} tools")

    def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Entry point: nhận MCPRequest, trả MCPResponse.

        Tự động route theo request.method:
          - tools/list → trả danh sách tool definitions
          - tools/call → gọi tool cụ thể
        """
        req_id = request.id or uuid.uuid4().hex[:8]

        if request.method == MCPMethod.TOOLS_LIST:
            return MCPResponse(
                result=self.list_tools(),
                id=req_id,
            )

        if request.method == MCPMethod.TOOLS_CALL:
            tool_name = request.params.get("name", "")
            arguments = request.params.get("arguments", {})
            result = self.call_tool(tool_name, arguments)
            return MCPResponse(
                result=result.model_dump(),
                id=req_id,
            )

        return MCPResponse(
            error={"code": -1, "message": f"Unknown method: {request.method}"},
            id=req_id,
        )

    def list_tools(self) -> List[dict]:
        """Trả về danh sách MCP definitions cho tất cả tools."""
        return self.registry.get_mcp_definitions()

    def call_tool(self, name: str, params: dict) -> ToolCallResponse:
        """Gọi tool theo tên, trả về ToolCallResponse chuẩn hoá."""
        tool = self.registry.get(name)
        if tool is None:
            logger.warning(f"Tool not found: {name}")
            return ToolCallResponse(
                tool_name=name,
                success=False,
                error=f"Tool '{name}' not found. Available: {[t.name for t in self.registry.list_all()]}",
            )

        logger.info(f"Calling tool: {name}")
        result: ToolResult = tool.safe_execute(params)

        return ToolCallResponse(
            tool_name=name,
            success=result.success,
            data=result.data,
            error=result.error,
            metadata=result.metadata,
        )


__all__ = ["MCPToolServer"]
