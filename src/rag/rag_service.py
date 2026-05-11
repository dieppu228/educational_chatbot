import re
import asyncio
from typing import Optional, List, Dict, AsyncGenerator

from src.config.config import settings
from src.schemas.context import RequestContext
from src.rag.adaptive_rag import AdaptiveRAGAgent
from src.utils.trace_decorator import trace_node


class RAGService:

    def __init__(self, retriever, reranker):
        self.rag_agent = AdaptiveRAGAgent(
            retriever=retriever,
            reranker=reranker,
            settings=settings,
        )
        self.reranker = reranker

    @trace_node("RAGService.get_context")
    def get_context(
        self,
        ctx: RequestContext,
        intent_hint: Optional[str] = None,
        task_type: Optional[str] = None,
    ) -> List[Dict]:
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
            ctx.add_debug_step("RAG", status="error", error=str(e)[:200])
            # Trả về empty thay vì crash pipeline,
            # nhưng log đủ thông tin để debug
            return []

    @trace_node("RAGService.get_context_async")
    async def get_context_async(
        self,
        ctx: RequestContext,
        intent_hint: Optional[str] = None,
        task_type: Optional[str] = None,
    ) -> List[Dict]:
        # Run blocking I/O in thread pool to not block event loop
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            lambda: self.get_context(ctx, intent_hint=intent_hint, task_type=task_type)
        )

    @staticmethod
    def _extract_grade_from_topic(topic: str) -> Optional[str]:
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
        if task_type in ("slide", "slide_generate"):
            return getattr(settings, 'RERANKER_TOP_N_SLIDE', 15)
        elif task_type in ("lesson_plan", "giao_an"):
            return getattr(settings, 'RERANKER_TOP_N_LESSON_PLAN', 20)
        return getattr(settings, 'RERANKER_TOP_N', 5)


__all__ = ["RAGService"]
