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
        task_type: Optional[str] = None,
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

                # Task-aware rerank: slide/lesson_plan giữ nhiều chunks hơn
                rerank_top_n = self._get_rerank_top_n(task_type)
                if len(result.chunks) > rerank_top_n:
                    result_chunks = self.reranker.rerank(
                        queries[0] if queries else ctx.query,
                        result.chunks,
                        top_n=rerank_top_n,
                    )
                else:
                    result_chunks = result.chunks

                # Score cutoff: loại chunks chất lượng thấp
                min_score = getattr(settings, 'RERANKER_MIN_SCORE', 0.15)
                before_count = len(result_chunks)
                filtered = self.reranker.filter_context(
                    result_chunks, min_score=min_score,
                )
                # Safety net: nếu cutoff loại hết, giữ top 3
                if not filtered and result_chunks:
                    filtered = result_chunks[:3]
                    logger.warning(
                        f"Score cutoff dropped ALL {before_count} chunks "
                        f"(min_score={min_score}), keeping top 3 as fallback"
                    )
                elif len(filtered) < before_count:
                    logger.info(
                        f"Score cutoff: {before_count} -> {len(filtered)} chunks "
                        f"(min_score={min_score})"
                    )

                return filtered

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

            # Task-aware rerank: slide/lesson_plan giữ nhiều chunks hơn
            rerank_top_n = self._get_rerank_top_n(task_type)
            if len(all_chunks) > rerank_top_n:
                primary_query = queries[0]
                all_chunks = self.reranker.rerank(
                    primary_query, all_chunks,
                    top_n=rerank_top_n,
                )

            # Score cutoff: loại chunks chất lượng thấp
            min_score = getattr(settings, 'RERANKER_MIN_SCORE', 0.15)
            before_count = len(all_chunks)
            filtered = self.reranker.filter_context(
                all_chunks, min_score=min_score,
            )
            # Safety net
            if not filtered and all_chunks:
                filtered = all_chunks[:3]
                logger.warning(
                    f"Score cutoff dropped ALL {before_count} chunks "
                    f"(min_score={min_score}), keeping top 3 as fallback"
                )
            elif len(filtered) < before_count:
                logger.info(
                    f"Score cutoff: {before_count} -> {len(filtered)} chunks "
                    f"(min_score={min_score})"
                )
            all_chunks = filtered

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

    @staticmethod
    def _get_rerank_top_n(task_type: Optional[str] = None) -> int:
        """Trả về rerank limit phù hợp với task type.

        Slide/lesson_plan cần nhiều chunks hơn để phủ toàn bộ nội dung bài.
        """
        if task_type in ("slide", "slide_generate"):
            return getattr(settings, 'RERANKER_TOP_N_SLIDE', 15)
        elif task_type in ("lesson_plan", "giao_an"):
            return getattr(settings, 'RERANKER_TOP_N_LESSON_PLAN', 20)
        return getattr(settings, 'RERANKER_TOP_N', 5)


__all__ = ["RAGService"]
