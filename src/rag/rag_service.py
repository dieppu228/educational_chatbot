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
        grade_hint = ctx.effective_grade
        if ctx.intent_result:
            topic_hint = ctx.intent_result.topic
            if topic_hint and not grade_hint:
                grade_hint = self._extract_grade_from_topic(topic_hint)

        book = ctx.effective_book
        queries = ctx.queries_for_rag
        ctx.scope_fallback_used = False
        ctx.actual_scope = {}
        ctx.scope_fallback_notice = None

        try:
            primary_chunks = self._retrieve_filtered(
                ctx=ctx,
                queries=queries,
                intent_hint=intent_hint,
                topic_hint=topic_hint,
                grade_hint=grade_hint,
                book=book,
                task_type=task_type,
                debug_node="RAG",
            )
            if not self._should_fallback_scope(ctx, primary_chunks, task_type):
                return primary_chunks

            fallback_chunks = self._retrieve_filtered(
                ctx=ctx,
                queries=queries,
                intent_hint=intent_hint,
                topic_hint=topic_hint,
                grade_hint=None,
                book=None,
                task_type=task_type,
                debug_node="RAGFallbackSearch",
            )

            if fallback_chunks and len(fallback_chunks) > len(primary_chunks):
                ctx.scope_fallback_used = True
                ctx.actual_scope = self._extract_actual_scope(fallback_chunks)
                ctx.scope_fallback_notice = self._build_scope_fallback_notice(ctx)
                ctx.add_debug_step(
                    "ScopeFallback",
                    requested_scope=ctx.requested_scope,
                    primary_chunks=len(primary_chunks),
                    fallback_chunks=len(fallback_chunks),
                    actual_scope=ctx.actual_scope,
                    status="used",
                )
                return fallback_chunks

            ctx.add_debug_step(
                "ScopeFallback",
                requested_scope=ctx.requested_scope,
                primary_chunks=len(primary_chunks),
                fallback_chunks=len(fallback_chunks),
                status="not_used",
            )
            return primary_chunks

        except Exception as e:
            # KHÔNG swallow — log rõ ràng và re-raise nếu cần
            ctx.add_debug_step("RAG", status="error", error=str(e)[:200])
            # Trả về empty thay vì crash pipeline,
            # nhưng log đủ thông tin để debug
            return []

    def _retrieve_filtered(
        self,
        ctx: RequestContext,
        queries: List[str],
        intent_hint: Optional[str],
        topic_hint: Optional[str],
        grade_hint: Optional[str],
        book: Optional[str],
        task_type: Optional[str],
        debug_node: str,
    ) -> List[Dict]:
        if len(queries) <= 1:
            query = queries[0] if queries else ctx.query
            result = self.rag_agent.retrieve(
                query,
                intent_hint=intent_hint,
                topic_hint=topic_hint,
                grade_hint=grade_hint,
                book=book,
            )
            ctx.add_debug_step(
                debug_node,
                queries_used=queries,
                strategy=result.strategy_used.value,
                chunks_returned=len(result.chunks),
                time_s=result.total_time_s,
                filter=result.metadata_filter,
                reason=result.reason,
            )
            return self._rerank_and_filter(query, result.chunks, task_type)

        return self._retrieve_multi_query(
            ctx=ctx,
            queries=queries,
            intent_hint=intent_hint,
            topic_hint=topic_hint,
            grade_hint=grade_hint,
            book=book,
            task_type=task_type,
            debug_node=debug_node,
        )

    def _retrieve_multi_query(
        self,
        ctx: RequestContext,
        queries: List[str],
        intent_hint: Optional[str],
        topic_hint: Optional[str],
        grade_hint: Optional[str],
        book: Optional[str],
        task_type: Optional[str],
        debug_node: str,
    ) -> List[Dict]:
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

        ctx.add_debug_step(
            debug_node,
            queries_used=queries,
            multi_query=True,
            strategies=strategies,
            chunks_returned=len(all_chunks),
            time_s=round(total_time, 2),
            filter={"grade": grade_hint, "topic": topic_hint, "book": book},
            reason=f"Multi-query search ({len(queries)} queries)",
        )
        return self._rerank_and_filter(queries, all_chunks, task_type)

    def _rerank_and_filter(
        self,
        queries,
        chunks: List[Dict],
        task_type: Optional[str],
    ) -> List[Dict]:
        if not chunks:
            return []
        if isinstance(queries, str):
            queries = [queries]
        # Single rerank pass with task-aware top_n.
        # Strategies return raw candidates (up to RETRIEVER_TOP_K); reranking
        # happens only here so task_type (slide/lesson_plan) gets the full pool.
        # Multi-query: score each chunk against every sub-query, keep the max.
        rerank_top_n = self._get_rerank_top_n(task_type)
        if len(queries) > 1:
            result_chunks = self.reranker.rerank_multi_query(
                queries, chunks, top_n=rerank_top_n,
            )
        else:
            result_chunks = self.reranker.rerank(
                queries[0], chunks, top_n=rerank_top_n,
            )

        min_score = getattr(settings, 'RERANKER_MIN_SCORE', 0.15)
        filtered = self.reranker.filter_context(
            result_chunks, min_score=min_score,
        )
        if not filtered and result_chunks:
            filtered = result_chunks[:3]
        return filtered

    @staticmethod
    def _should_fallback_scope(
        ctx: RequestContext,
        chunks: List[Dict],
        task_type: Optional[str],
    ) -> bool:
        if not ctx.scope_is_soft:
            return False
        if not (ctx.effective_book or ctx.effective_grade):
            return False
        min_chunks = 3 if task_type in ("slide", "slide_generate", "lesson_plan", "giao_an") else 1
        return len(chunks) < min_chunks

    @staticmethod
    def _extract_actual_scope(chunks: List[Dict]) -> Dict[str, Optional[str]]:
        books = set()
        grades = set()
        for chunk in chunks:
            metadata = chunk.get("metadata", {})
            if metadata.get("book"):
                books.add(metadata["book"])
            if metadata.get("grade"):
                grades.add(metadata["grade"])

        return {
            "book": next(iter(books)) if len(books) == 1 else ("mixed" if books else None),
            "grade": next(iter(grades)) if len(grades) == 1 else ("mixed" if grades else None),
            "source": "fallback",
        }

    @classmethod
    def _build_scope_fallback_notice(cls, ctx: RequestContext) -> str:
        requested = cls._scope_label(ctx.requested_scope)
        actual = cls._scope_label(ctx.actual_scope)
        return (
            f"Mình chưa tìm thấy đủ tài liệu phù hợp trong {requested}, "
            "nên đã mở rộng tìm kiếm trong toàn bộ SGK. "
            f"Nguồn đang dùng: {actual}.\n\n"
        )

    @classmethod
    def _scope_label(cls, scope: Dict[str, Optional[str]]) -> str:
        book = scope.get("book")
        grade = scope.get("grade")
        parts = []
        if book:
            parts.append(cls._book_label(book))
        if grade:
            parts.append(f"Lớp {grade}" if grade != "mixed" else "nhiều lớp")
        return " - ".join(parts) if parts else "phạm vi đã chọn"

    @staticmethod
    def _book_label(book: str) -> str:
        labels = {"CD": "Cánh Diều", "KNTT": "Kết nối tri thức", "mixed": "nhiều bộ sách"}
        return labels.get(book, book)

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
