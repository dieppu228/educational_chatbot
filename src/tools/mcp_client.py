"""mcp_client.py — MCP Client phía Agent gọi tool.

Client là interface mà Agent sử dụng để:
  1. Xem danh sách tools available (list_available_tools)
  2. Gọi một tool cụ thể (call_tool)

Trong scope ĐATN, Client gọi Server trực tiếp (in-process).
"""

import uuid
import logging
from typing import List, Optional

from src.tools.mcp_server import MCPToolServer
from src.tools.mcp_protocol import (
    MCPRequest, MCPResponse, MCPMethod,
    create_list_request, create_call_request,
)
from src.tools.schemas import ToolCallResponse

logger = logging.getLogger("chatbot.tools.mcp_client")


class MCPToolClient:
    """MCP Client — phía Agent gọi tool thông qua MCP Server."""

    def __init__(self, server: MCPToolServer):
        self.server = server

    def list_available_tools(self) -> List[dict]:
        """Lấy danh sách tools available từ server.

        Returns:
            List[dict] — mỗi dict chứa name, description, inputSchema
        """
        request = create_list_request(request_id=uuid.uuid4().hex[:8])
        response = self.server.handle_request(request)
        return response.result or []

    def call_tool(self, name: str, params: dict) -> ToolCallResponse:
        """Gọi một tool cụ thể.

        Args:
            name: Tên tool (vd: "knowledge_retrieval")
            params: Dict params theo tool's input_schema

        Returns:
            ToolCallResponse với success/data/error
        """
        request = create_call_request(
            tool_name=name,
            arguments=params,
            request_id=uuid.uuid4().hex[:8],
        )
        response = self.server.handle_request(request)

        if response.is_error:
            logger.error(f"MCP error: {response.error}")
            return ToolCallResponse(
                tool_name=name,
                success=False,
                error=str(response.error),
            )

        # response.result is already a ToolCallResponse dict
        return ToolCallResponse(**response.result)

    def retrieve_knowledge(self, query: str, **kwargs) -> ToolCallResponse:
        """Shortcut: gọi knowledge_retrieval tool.

        Args:
            query: Câu hỏi cần tra cứu
            **kwargs: book, grade, topic_name, intent_hint, task_type, ...
        """
        params = {"query": query, **kwargs}
        return self.call_tool("knowledge_retrieval", params)

    def format_content(self, chunks: list, action: str = None) -> ToolCallResponse:
        """Shortcut: gọi content_formatter tool."""
        params = {"chunks": chunks}
        if action:
            params["action"] = action
        return self.call_tool("content_formatter", params)


__all__ = ["MCPToolClient"]
