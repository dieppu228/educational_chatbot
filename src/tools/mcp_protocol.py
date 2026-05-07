"""mcp_protocol.py — MCP protocol definitions.

MCP dùng format tương tự JSON-RPC 2.0 để giao tiếp:
  - Client gửi MCPRequest (method + params)
  - Server trả MCPResponse (result hoặc error)

Hai method chính:
  - "tools/list"  → liệt kê tools available
  - "tools/call"  → gọi một tool cụ thể
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Dict
from enum import Enum


class MCPMethod(Enum):
    """Các method mà MCP Server hỗ trợ."""
    TOOLS_LIST = "tools/list"
    TOOLS_CALL = "tools/call"


@dataclass
class MCPRequest:
    """Request từ Client → Server (theo format JSON-RPC).

    Ví dụ tools/call:
        MCPRequest(
            method=MCPMethod.TOOLS_CALL,
            params={"name": "knowledge_retrieval", "arguments": {"query": "..."}}
        )
    """
    method: MCPMethod
    params: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None  # Request ID để match response


@dataclass
class MCPResponse:
    """Response từ Server → Client.

    Ví dụ success:
        MCPResponse(result={"chunks": [...]}, id="req-1")

    Ví dụ error:
        MCPResponse(error={"code": -1, "message": "Tool not found"}, id="req-1")
    """
    result: Any = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

    @property
    def is_error(self) -> bool:
        return self.error is not None


# ── Helper functions ──────────────────────────────────────────

def create_list_request(request_id: str = None) -> MCPRequest:
    """Tạo request liệt kê tools."""
    return MCPRequest(method=MCPMethod.TOOLS_LIST, id=request_id)


def create_call_request(
    tool_name: str,
    arguments: dict,
    request_id: str = None,
) -> MCPRequest:
    """Tạo request gọi tool."""
    return MCPRequest(
        method=MCPMethod.TOOLS_CALL,
        params={"name": tool_name, "arguments": arguments},
        id=request_id,
    )


__all__ = [
    "MCPMethod",
    "MCPRequest",
    "MCPResponse",
    "create_list_request",
    "create_call_request",
]
