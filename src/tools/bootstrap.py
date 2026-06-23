"""Khởi tạo tầng MCP in-process và cấp client singleton cho specialist agents."""

import logging
from typing import Optional

from src.tools.implementations.content_formatter_tool import ContentFormatterTool
from src.tools.implementations.knowledge_retrieval_tool import KnowledgeRetrievalTool
from src.tools.implementations.tool_registry import ToolRegistry
from src.tools.implementations.web_search_tool import WebSearchTool
from src.tools.mcp_client import MCPToolClient
from src.tools.mcp_server import MCPToolServer

logger = logging.getLogger("chatbot.tools.bootstrap")

_client: Optional[MCPToolClient] = None


def init_tool_layer(rag_service=None, tavily_service=None) -> MCPToolClient:
    """Build registry, server và client; gọi lại sẽ rebuild singleton."""
    global _client

    registry = ToolRegistry()
    registry.register(WebSearchTool(tavily_service))
    registry.register(ContentFormatterTool())
    if rag_service is not None:
        registry.register(KnowledgeRetrievalTool(rag_service))

    server = MCPToolServer(registry)
    _client = MCPToolClient(server)
    logger.info(
        "MCP tool layer initialized: %s",
        [tool.name for tool in registry.list_all()],
    )
    return _client


def get_mcp_client() -> MCPToolClient:
    """Trả client singleton, lazy-init không kèm RAG nếu startup chưa chạy."""
    global _client
    if _client is None:
        logger.warning(
            "MCP client chưa init - lazy-init web_search/formatter (không RAG)."
        )
        init_tool_layer()
    return _client


def reset_tool_layer() -> None:
    """Reset singleton cho test."""
    global _client
    _client = None


__all__ = ["init_tool_layer", "get_mcp_client", "reset_tool_layer"]
