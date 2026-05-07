"""content_formatter_tool.py — Wrap ContextCombiner thành MCP tool.

Agent dùng tool này để format chunks từ RAG (hoặc web search)
thành context text sẵn sàng đưa vào LLM prompt.

Hai chế độ format:
  - 'grouped': group by topic/lesson → dùng cho slide, lesson plan
  - 'flat': sort by relevance score → dùng cho quiz, explain
"""

import logging
from src.tools.base_tool import BaseTool, ToolResult
from src.tools.schemas import ContentFormatterInput, ContentFormatterOutput
from src.rag.context_combiner import format_contexts

logger = logging.getLogger("chatbot.tools.content_formatter")


class ContentFormatterTool(BaseTool):

    name = "content_formatter"
    description = (
        "Format và sắp xếp các chunks từ RAG hoặc web search "
        "thành context text tối ưu cho LLM prompt. "
        "Hỗ trợ 2 chế độ: grouped (theo bài/chủ đề) và flat (theo score)."
    )
    input_schema = {
        "chunks": {"type": "array", "description": "Danh sách chunks cần format"},
        "action": {"type": "string", "description": "generate_slide, generate_quiz, explain_concept, ..."},
    }

    def execute(self, params: dict) -> ToolResult:
        try:
            input_data = ContentFormatterInput(**params)
        except Exception as e:
            return ToolResult(success=False, error=f"Invalid input: {e}")

        if not input_data.chunks:
            return ToolResult(
                success=True,
                data=ContentFormatterOutput(
                    formatted_text="[Không có context]",
                    total_chunks=0,
                    format_mode="flat",
                ).model_dump(),
            )

        # Gọi context_combiner
        formatted = format_contexts(input_data.chunks, action=input_data.action)

        # Xác định mode đã dùng
        from src.rag.context_combiner import COMPREHENSIVE_ACTIONS
        mode = "grouped" if input_data.action in COMPREHENSIVE_ACTIONS else "flat"

        output = ContentFormatterOutput(
            formatted_text=formatted,
            total_chunks=len(input_data.chunks),
            format_mode=mode,
        )

        logger.info(
            f"ContentFormatterTool: {len(input_data.chunks)} chunks → "
            f"mode={mode}, output_len={len(formatted)}"
        )

        return ToolResult(
            success=True,
            data=output.model_dump(),
            metadata={"format_mode": mode, "output_length": len(formatted)},
        )


__all__ = ["ContentFormatterTool"]
