import time
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict

logger = logging.getLogger("chatbot")


# ============================================================
# DATA MODELS
# ============================================================

class RAGStrategy(Enum):
    STANDARD     = "standard"
    BROAD        = "broad"
    CURRICULUM   = "curriculum"
    HIERARCHICAL = "hierarchical"


@dataclass
class QueryProfile:
    strategy: RAGStrategy
    grade: Optional[str] = None
    topic_hint: Optional[str] = None
    top_k_override: Optional[int] = None
    reason: str = ""


@dataclass
class RAGResult:
    chunks: List[Dict]
    strategy_used: RAGStrategy
    metadata_filter: dict
    total_time_s: float
    reason: str


# ============================================================
# QUERY CLASSIFIER — pure code, không LLM
# ============================================================

class QueryClassifier:

    BROAD_KEYWORDS = [
        "tổng quan", "tổng quát", "toàn cảnh", "tổng hợp",
        "giới thiệu", "mở đầu", "khái quát",
        "tất cả", "toàn bộ", "toàn diện",
        "tổng thể", "tóm tắt", "tóm lược",
        "overview", "general", "comprehensive", "summary",
        "all", "entire", "complete",
        "những gì", "gồm những", "bao gồm", "các chủ đề",
    ]

    # Lưu ý: CURRICULUM_KEYWORDS nên CỤ THỂ hơn BROAD
    # để tránh false positive (vd: "bài" có trong quá nhiều query)
    CURRICULUM_KEYWORDS = [
        "chương trình học", "cấu trúc môn",
        "môn tin học lớp", "học những gì",
        "bao nhiêu bài", "bao nhiêu chủ đề",
        "danh sách bài", "danh sách chủ đề",
        "nội dung chương trình",
        # Bổ sung: các cụm phổ biến chứa "bài" / "chủ đề"
        "có những bài nào", "những bài gì", "các bài học", "mấy bài",
        "có những chủ đề nào", "những chủ đề gì", "các chủ đề", "mấy chủ đề",
        "gồm những bài", "gồm những chủ đề",
        "bài học nào", "chủ đề nào",
    ]

    GRADE_PATTERNS = {
        "10": ["lớp 10", "tin 10", "grade 10", "lớp mười "],
        "11": ["lớp 11", "tin 11", "grade 11", "lớp mười một"],
        "12": ["lớp 12", "tin 12", "grade 12", "lớp mười hai"],
    }

    def classify(
        self,
        query: str,
        intent_hint: str = None,
        grade_hint: Optional[str] = None,
        topic_hint: Optional[str] = None,
    ) -> QueryProfile:
        q_lower = query.lower()

        # Ưu tiên grade từ IntentRouter (LLM đã reasoning)
        # Chỉ tự detect nếu IntentRouter không cung cấp
        grade = grade_hint or self._detect_grade(q_lower)

        # Nếu topic_hint chứa grade (vd: "Kiến thức Tin học lớp 12") → extract
        if not grade and topic_hint:
            grade = self._detect_grade(topic_hint.lower())

        # 1. Check CURRICULUM
        if any(kw in q_lower for kw in self.CURRICULUM_KEYWORDS):
            return QueryProfile(
                strategy=RAGStrategy.CURRICULUM,
                grade=grade,
                topic_hint=topic_hint,
                reason="Hỏi về cấu trúc chương trình",
            )

        # 2. Check BROAD
        is_broad = any(kw in q_lower for kw in self.BROAD_KEYWORDS)
        has_grade_no_lesson = grade is not None and not self._has_lesson_hint(q_lower)
        # Topic-specific broad: có topic rõ ràng + intent explain + không có bài cụ thể
        is_topic_broad = (
            topic_hint is not None
            and not self._has_lesson_hint(q_lower)
            and intent_hint == "explain"
        )

        if (is_broad or has_grade_no_lesson or is_topic_broad) and intent_hint in ("explain", None):
            return QueryProfile(
                strategy=RAGStrategy.BROAD,
                grade=grade,
                topic_hint=topic_hint,
                reason=(
                    f"Query tổng quát: broad={is_broad}, "
                    f"grade_only={has_grade_no_lesson}, "
                    f"topic_broad={is_topic_broad}"
                ),
            )

        # 3. Check HIERARCHICAL — query cụ thể + có grade/topic context
        if intent_hint in ("explain", "generate") and (grade or topic_hint):
            return QueryProfile(
                strategy=RAGStrategy.HIERARCHICAL,
                grade=grade,
                topic_hint=topic_hint,
                reason=f"Query cụ thể + context (grade={grade}, topic={topic_hint is not None}) → HRAG",
            )

        # 4. Mặc định: STANDARD (flat search, không có context)
        return QueryProfile(
            strategy=RAGStrategy.STANDARD,
            grade=grade,
            topic_hint=topic_hint,
            reason="Query cụ thể, không có grade/topic context",
        )

    def _detect_grade(self, q_lower: str) -> Optional[str]:
        for grade, patterns in self.GRADE_PATTERNS.items():
            if any(p in q_lower for p in patterns):
                return grade
        return None

    def _has_lesson_hint(self, q_lower: str) -> bool:
        # Chỉ match khi đi kèm số (vd: "bài 3", "chủ đề 2")
        import re
        return bool(re.search(r'(bài|chủ đề|mục|tiết|phần)\s*\d', q_lower))


# ============================================================
# ADAPTIVE RAG AGENT
# ============================================================

class AdaptiveRAGAgent:

    def __init__(self, retriever, reranker, settings):
        self.retriever = retriever
        self.reranker  = reranker
        self.settings  = settings
        self.classifier = QueryClassifier()

    def retrieve(
        self,
        query: str,
        intent_hint: str = None,
        topic_hint: str = None,
        grade_hint: str = None,
        book: str = None,
    ) -> RAGResult:
        t0 = time.time()

        # === Pre-compute book-scoped indices (if book provided) ===
        book_indices = self._get_book_indices(book) if book else None
        if book:
            logger.info(f"RAGAgent: book filter='{book}' → {len(book_indices) if book_indices else 0} chunks in scope")

        # === OBSERVE — tích hợp signals từ IntentRouter ===
        profile = self.classifier.classify(
            query,
            intent_hint=intent_hint,
            grade_hint=grade_hint,
            topic_hint=topic_hint,
        )
        logger.info(
            f"RAGAgent: strategy={profile.strategy.value} | "
            f"grade={profile.grade} | topic={profile.topic_hint} | "
            f"book={book} | {profile.reason}"
        )

        # === ACT ===
        if profile.strategy == RAGStrategy.CURRICULUM:
            chunks = self._curriculum_lookup(profile, book=book)

        elif profile.strategy == RAGStrategy.BROAD:
            chunks = self._broad_retrieval(query, profile, book=book)
            # Fallback: nếu broad trả về < 3 chunks → bổ sung standard
            if len(chunks) < 3:
                logger.info("RAGAgent: BROAD < 3 chunks → fallback standard")
                standard = self._standard_retrieval(query, book_indices=book_indices)
                chunks = self._merge_deduplicate(chunks, standard)

        elif profile.strategy == RAGStrategy.HIERARCHICAL:
            chunks = self._hierarchical_retrieval(query, profile, book_indices=book_indices)
            # Fallback: nếu HRAG < 3 chunks → bổ sung standard
            if len(chunks) < 3:
                logger.info("RAGAgent: HIERARCHICAL < 3 chunks → fallback standard")
                standard = self._standard_retrieval(query, book_indices=book_indices)
                chunks = self._merge_deduplicate(chunks, standard)

        else:  # STANDARD
            chunks = self._standard_retrieval(query, book_indices=book_indices)

        total_time = time.time() - t0
        logger.info(f"RAGAgent done: {len(chunks)} chunks, {total_time:.2f}s")

        return RAGResult(
            chunks=chunks,
            strategy_used=profile.strategy,
            metadata_filter={"grade": profile.grade, "topic": profile.topic_hint, "book": book},
            total_time_s=round(total_time, 2),
            reason=profile.reason,
        )

    # ============================================================
    # Strategy Implementations
    # ============================================================

    def _standard_retrieval(self, query: str, book_indices: List[int] = None) -> List[Dict]:
        if book_indices is not None:
            results = self.retriever.search_scoped(
                query, doc_indices=book_indices, top_k=self.settings.RETRIEVER_TOP_K
            )
        else:
            results = self.retriever.search(query, top_k=self.settings.RETRIEVER_TOP_K)
        if not results:
            return []
        return self.reranker.rerank(query, results, top_n=self.settings.RERANKER_TOP_N)

    def _broad_retrieval(self, query: str, profile: QueryProfile, book: str = None) -> List[Dict]:
        raw = self.retriever.search_by_metadata(
            grade=profile.grade,
            topic_name=profile.topic_hint,
            chunk_types=["objective"],
            max_per_lesson=1,
        )
        # Apply book filter
        if book:
            raw = [c for c in raw if c.get("metadata", {}).get("book") == book]

        if not raw:
            # Fallback 1: bỏ topic filter, giữ grade + book
            raw = self.retriever.search_by_metadata(
                grade=profile.grade,
                chunk_types=["objective"],
                max_per_lesson=1,
            )
            if book:
                raw = [c for c in raw if c.get("metadata", {}).get("book") == book]

        if not raw:
            # Fallback 2: lấy content nếu không có objective
            raw = self.retriever.search_by_metadata(
                grade=profile.grade,
                chunk_types=["content"],
                max_per_lesson=1,
            )
            if book:
                raw = [c for c in raw if c.get("metadata", {}).get("book") == book]

        max_chunks = getattr(self.settings, 'RAG_BROAD_MAX_CHUNKS', 30)
        return raw[:max_chunks]

    def _curriculum_lookup(self, profile: QueryProfile, book: str = None) -> List[Dict]:
        raw = self.retriever.search_by_metadata(
            grade=profile.grade,
            topic_name=profile.topic_hint,
            chunk_types=["objective"],
            max_per_lesson=1,
        )
        if book:
            raw = [c for c in raw if c.get("metadata", {}).get("book") == book]

        if not raw:
            # Fallback: bỏ topic filter
            raw = self.retriever.search_by_metadata(
                grade=profile.grade,
                chunk_types=["objective"],
                max_per_lesson=1,
            )
            if book:
                raw = [c for c in raw if c.get("metadata", {}).get("book") == book]

        if not raw:
            return []

        # Deduplicate theo (topic_name, lesson_name)
        seen: set = set()
        summary_chunks: List[Dict] = []

        for chunk in raw:
            m = chunk["metadata"]
            key = (m.get("topic_name", ""), m.get("lesson_name", ""))
            if key in seen:
                continue
            seen.add(key)

            summary_chunks.append({
                "doc_id": chunk["doc_id"],
                "score": 1.0,
                "content": (
                    f"Chủ đề: {m.get('topic_name', '')}\n"
                    f"Bài học: {m.get('lesson_name', '')}\n"
                    f"---\n{chunk['content'][:300]}"
                ),
                "context": chunk["context"],
                "metadata": m,
            })

        return summary_chunks[:25]

    def _hierarchical_retrieval(self, query: str, profile: QueryProfile, book_indices: List[int] = None) -> List[Dict]:
        all_chunks = self.retriever.chunks
        # If book_indices provided, use as base scope
        scope_set = set(book_indices) if book_indices else None

        # ── Phase 1: Coarse — tìm parents (Level 1-2) ──────────────
        parent_indices = []
        for i, chunk in enumerate(all_chunks):
            if scope_set is not None and i not in scope_set:
                continue
            m = chunk.get("metadata", {})
            level = m.get("level", 99)
            if level > 2:
                continue
            # Filter by grade nếu có
            if profile.grade and m.get("grade") != profile.grade:
                continue
            parent_indices.append(i)

        if not parent_indices:
            logger.warning("HRAG Phase 1: no parent chunks found → fallback standard")
            return self._standard_retrieval(query, book_indices=book_indices)

        # Semantic search chỉ trên parents
        parent_results = self.retriever.search_scoped(
            query, doc_indices=parent_indices, top_k=3, top_n=min(30, len(parent_indices))
        )

        # Extract parent keys: (topic_name, lesson_name)
        parent_keys = set()
        for res in parent_results:
            m = res["metadata"]
            parent_keys.add((m.get("topic_name", ""), m.get("lesson_name", "")))

        logger.info(
            f"HRAG Phase 1: {len(parent_indices)} parents searched → "
            f"{len(parent_results)} selected → {len(parent_keys)} unique lessons"
        )

        # ── Phase 2: Fine — search children (Level 3+) ─────────────
        child_indices = []
        for i, chunk in enumerate(all_chunks):
            if scope_set is not None and i not in scope_set:
                continue
            m = chunk.get("metadata", {})
            level = m.get("level", 0)
            if level < 3:
                continue
            key = (m.get("topic_name", ""), m.get("lesson_name", ""))
            if key in parent_keys:
                child_indices.append(i)

        if not child_indices:
            logger.warning("HRAG Phase 2: no children found → returning parent chunks")
            return parent_results

        logger.info(f"HRAG Phase 2: scoped search on {len(child_indices)} child chunks")

        # Scoped hybrid search (BM25 + Semantic + RRF) trên children
        child_results = self.retriever.search_scoped(
            query,
            doc_indices=child_indices,
            top_k=self.settings.RETRIEVER_TOP_K,
            top_n=min(30, len(child_indices)),
        )

        if not child_results:
            return parent_results

        # Rerank kết quả
        reranked = self.reranker.rerank(
            query, child_results, top_n=self.settings.RERANKER_TOP_N
        )
        return reranked if reranked else child_results

    def _merge_deduplicate(self, primary: List[Dict], secondary: List[Dict]) -> List[Dict]:
        seen_ids = {c["doc_id"] for c in primary}
        merged = list(primary)
        for c in secondary:
            if c["doc_id"] not in seen_ids:
                merged.append(c)
                seen_ids.add(c["doc_id"])
        return merged

    def _get_book_indices(self, book: str) -> List[int]:
        indices = []
        for i, chunk in enumerate(self.retriever.chunks):
            if chunk.get("metadata", {}).get("book") == book:
                indices.append(i)
        return indices


__all__ = ["AdaptiveRAGAgent", "RAGStrategy", "RAGResult", "QueryClassifier"]
