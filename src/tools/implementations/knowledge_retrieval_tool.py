"""knowledge_retrieval_tool.py — Wrap RAGService thành MCP tool.

Đây là tool quan trọng nhất: cho phép Agent gọi RAG pipeline
thông qua chuẩn MCP thay vì gọi trực tiếp RAGService.

Luồng xử lý:
  Agent gửi KnowledgeRetrievalInput (query, book, grade, ...)
    → Tool build minimal RequestContext từ params
    → Gọi RAGService.get_context()
    → Convert chunks → RetrievedChunk schema
    → Trả về ToolResult chứa KnowledgeRetrievalOutput

Lưu ý:
  - Tool KHÔNG thay thế RAGService — chỉ wrap nó
  - Các service cũ (QuizService, SlideService) vẫn gọi RAGService trực tiếp
  - Tool cung cấp thêm interface MCP-compatible cho agent mới
"""

import logging
from typing import Optional

from src.tools.base_tool import BaseTool, ToolResult
from src.tools.schemas import (
    KnowledgeRetrievalInput,
    KnowledgeRetrievalOutput,
    RetrievedChunk,
    ChunkMetadataSchema,
)

logger = logging.getLogger("chatbot.tools.knowledge_retrieval")


class KnowledgeRetrievalTool(BaseTool):
    """MCP Tool wrap RAGService để tra cứu SGK Tin học THPT.

    Khi Agent cần kiến thức từ sách giáo khoa, nó gọi tool này
    thay vì trực tiếp gọi RAGService. Điều này cho phép:
      1. Agent chọn tool phù hợp (RAG vs Web Search)
      2. Chuẩn hoá I/O qua schema validation
      3. Tự động error handling + timing metrics
    """

    name = "knowledge_retrieval"
    description = (
        "Tra cứu kiến thức từ sách giáo khoa Tin học THPT "
        "(Cánh Diều và Kết Nối Tri Thức, lớp 10-12). "
        "Trả về các đoạn văn bản (chunks) liên quan nhất với câu hỏi, "
        "kèm metadata (bài học, chủ đề, lớp) và điểm relevance."
    )
    input_schema = {
        "query": {"type": "string", "description": "Câu hỏi cần tra cứu"},
        "intent_hint": {"type": "string", "description": "explain hoặc generate"},
        "task_type": {"type": "string", "description": "slide, mcq, essay, ..."},
        "book": {"type": "string", "description": "CD hoặc KNTT"},
        "grade": {"type": "string", "description": "10, 11, 12"},
        "topic_name": {"type": "string", "description": "Tên chủ đề"},
    }

    def __init__(self, rag_service):
        """
        Args:
            rag_service: Instance của RAGService (đã khởi tạo với retriever + reranker)
        """
        self.rag_service = rag_service

    def execute(self, params: dict) -> ToolResult:
        """Thực thi tra cứu RAG.

        Args:
            params: Dict matching KnowledgeRetrievalInput schema

        Returns:
            ToolResult chứa KnowledgeRetrievalOutput trong .data
        """
        # ① Validate input
        try:
            input_data = KnowledgeRetrievalInput(**params)
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Invalid input: {e}",
            )

        # ② Build minimal RequestContext
        #    Tool không cần session/history — chỉ cần đủ fields
        #    cho RAGService.get_context() hoạt động
        from src.schemas.context import RequestContext
        from src.llm.intent_router import IntentResult

        ctx = RequestContext(
            query=input_data.query,
            queries_for_rag=[input_data.query],
        )

        # Gắn book nếu có
        if input_data.book:
            ctx.effective_book = input_data.book

        # Gắn intent_result nếu có topic/grade hints
        if input_data.topic_name or input_data.grade:
            ctx.intent_result = IntentResult(
                primary_intent=input_data.intent_hint or "explain",
                topic=input_data.topic_name,
                book=input_data.book,
            )

        # ③ Gọi RAGService
        try:
            chunks = self.rag_service.get_context(
                ctx,
                intent_hint=input_data.intent_hint,
                task_type=input_data.task_type,
            )
        except Exception as e:
            logger.error(f"RAGService error: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error=f"RAG retrieval failed: {str(e)[:200]}",
            )

        # ④ Convert chunks → RetrievedChunk schema
        retrieved_chunks = []
        for chunk in chunks:
            raw_meta = chunk.get("metadata", {})
            meta_schema = ChunkMetadataSchema(
                book=raw_meta.get("book", ""),
                grade=raw_meta.get("grade", ""),
                topic=raw_meta.get("topic", ""),
                topic_name=raw_meta.get("topic_name", ""),
                lesson=raw_meta.get("lesson", ""),
                lesson_name=raw_meta.get("lesson_name", ""),
                section=raw_meta.get("section", ""),
                title=raw_meta.get("title", ""),
                level=raw_meta.get("level", 0),
                type=raw_meta.get("type", "theory"),
            )
            retrieved_chunks.append(RetrievedChunk(
                doc_id=chunk.get("doc_id", 0),
                content=chunk.get("content", ""),
                context=chunk.get("context", ""),
                metadata=meta_schema,
                score=chunk.get("score"),
                rerank_score=chunk.get("rerank_score"),
            ))

        # ⑤ Lấy strategy info từ debug_steps
        strategy_used = None
        reason = ""
        metadata_filter = {}
        retrieval_time = None
        for step in ctx.debug_steps:
            if step.get("node") == "RAG":
                strategy_used = step.get("strategy")
                reason = step.get("reason", "")
                metadata_filter = step.get("filter", {})
                retrieval_time = step.get("time_s")
                break

        output = KnowledgeRetrievalOutput(
            chunks=retrieved_chunks,
            strategy_used=strategy_used,
            total_chunks=len(retrieved_chunks),
            query=input_data.query,
            reason=reason,
            metadata_filter=metadata_filter,
            retrieval_time_s=retrieval_time,
        )

        logger.info(
            f"KnowledgeRetrievalTool: query='{input_data.query[:50]}' "
            f"→ {len(retrieved_chunks)} chunks, strategy={strategy_used}"
        )

        return ToolResult(
            success=True,
            data=output.model_dump(),
            metadata={
                "strategy": strategy_used,
                "total_chunks": len(retrieved_chunks),
            },
        )


__all__ = ["KnowledgeRetrievalTool"]
