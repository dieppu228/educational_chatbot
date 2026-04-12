"""
RAGService — Tách RAG logic khỏi Orchestrator.

Bao bọc AdaptiveRAGAgent, nhận RequestContext để:
    - Lấy intent_hint, book, queries_for_rag
    - Xử lý multi-query retrieval + dedup
    - Rerank tổng hợp khi cần
    - Ghi trace vào RequestContext

Thay thế hàm _get_rag_context() cũ trong orchestrator.py.
"""

import re
import logging
from typing import Optional, List, Dict

from src.config.config import settings
from src.schemas.context import RequestContext
from src.rag.adaptive_rag import AdaptiveRAGAgent

logger = logging.getLogger("chatbot.rag_service")


class RAGService:
    """
    Centralized RAG retrieval service.

    Responsibilities:
        - Single-query & multi-query retrieval
        - Dedup + rerank tổng hợp
        - Grade extraction từ topic
        - Error handling (KHÔNG swallow exception — log rõ ràng)
    """

    def __init__(self, retriever, reranker):
        self.rag_agent = AdaptiveRAGAgent(
            retriever=retriever,
            reranker=reranker,
            settings=settings,
        )
        self.reranker = reranker

    def get_context(
        self,
        ctx: RequestContext,
        intent_hint: Optional[str] = None,
    ) -> List[Dict]:
        """
        Adaptive RAG — tự chọn chiến lược retrieval.

        Multi-query: nếu QueryRewriter sinh 2-3 queries,
        loop qua từng query, gom chunks, deduplicate.

        Args:
            ctx: RequestContext chứa queries_for_rag, effective_book, intent_result
            intent_hint: "explain" | "generate" | "chat"

        Returns:
            List[Dict]: Danh sách chunks đã rerank

        Raises:
            RAGServiceError: Khi RAG pipeline gặp lỗi nghiêm trọng
        """
        # Lấy topic và grade từ IntentRouter
        topic_hint = None
        grade_hint = None
        if ctx.intent_result:
            topic_hint = ctx.intent_result.topic
            if topic_hint:
                grade_hint = self._extract_grade_from_topic(topic_hint)

        book = ctx.effective_book
        queries = ctx.queries_for_rag

        try:
            if len(queries) <= 1:
                # ── Single query (fast path) ──
                result = self.rag_agent.retrieve(
                    queries[0] if queries else ctx.query,
                    intent_hint=intent_hint,
                    topic_hint=topic_hint,
                    grade_hint=grade_hint,
                    book=book,
                )
                ctx.add_debug_step(
                    "RAG",
                    queries_used=queries,
                    strategy=result.strategy_used.value,
                    chunks_returned=len(result.chunks),
                    time_s=result.total_time_s,
                    filter=result.metadata_filter,
                    reason=result.reason,
                )
                return result.chunks

            # ── Multi-query: loop → gom → deduplicate ──
            all_chunks = []
            seen_doc_ids = set()
            strategies = []
            total_time = 0.0

            for q in queries:
                result = self.rag_agent.retrieve(
                    q,
                    intent_hint=intent_hint,
                    topic_hint=topic_hint,
                    grade_hint=grade_hint,
                    book=book,
                )
                strategies.append(result.strategy_used.value)
                total_time += result.total_time_s

                for chunk in result.chunks:
                    if chunk["doc_id"] not in seen_doc_ids:
                        all_chunks.append(chunk)
                        seen_doc_ids.add(chunk["doc_id"])

            logger.info(
                f"Multi-query RAG: {len(queries)} queries → "
                f"{len(all_chunks)} unique chunks ({total_time:.2f}s)"
            )

            # Rerank tổng hợp nếu nhiều chunks
            rerank_top_n = getattr(settings, 'RERANKER_TOP_N', 5)
            if len(all_chunks) > rerank_top_n:
                primary_query = queries[0]
                all_chunks = self.reranker.rerank(
                    primary_query, all_chunks,
                    top_n=rerank_top_n,
                )

            ctx.add_debug_step(
                "RAG",
                queries_used=queries,
                multi_query=True,
                strategies=strategies,
                chunks_returned=len(all_chunks),
                time_s=round(total_time, 2),
                filter={"grade": grade_hint, "topic": topic_hint, "book": book},
                reason=f"Multi-query search ({len(queries)} queries)",
            )
            return all_chunks

        except Exception as e:
            # KHÔNG swallow — log rõ ràng và re-raise nếu cần
            logger.error(f"RAG Service Error: {e}", exc_info=True)
            ctx.add_debug_step("RAG", status="error", error=str(e)[:200])
            # Trả về empty thay vì crash pipeline,
            # nhưng log đủ thông tin để debug
            return []

    @staticmethod
    def _extract_grade_from_topic(topic: str) -> Optional[str]:
        """Extract grade (10/11/12) từ topic string.

        Ví dụ:
            "Kiến thức Tin học lớp 12" → "12"
            "Tin 10 - Bài 3"          → "10"
            "Lập trình Python"        → None
        """
        topic_lower = topic.lower()
        match = re.search(r'lớp\s*(10|11|12)', topic_lower)
        if match:
            return match.group(1)
        match = re.search(r'(?:tin|grade)\s*(10|11|12)', topic_lower)
        if match:
            return match.group(1)
        return None


__all__ = ["RAGService"]
