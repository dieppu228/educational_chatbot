import time
import re
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict

from src.utils.trace_decorator import trace_node

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

    @trace_node("AdaptiveRAG.retrieve")
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

        # === OBSERVE — tích hợp signals từ IntentRouter ===
        profile = self.classifier.classify(
            query,
            intent_hint=intent_hint,
            grade_hint=grade_hint,
            topic_hint=topic_hint,
        )

        # === ACT ===
        if profile.strategy == RAGStrategy.CURRICULUM:
            chunks = self._curriculum_lookup(profile, book=book)

        elif profile.strategy == RAGStrategy.BROAD:
            chunks = self._broad_retrieval(query, profile, book=book)
            # Fallback: nếu broad trả về < 3 chunks → bổ sung standard
            if len(chunks) < 3:
                standard = self._standard_retrieval(query, book_indices=book_indices)
                chunks = self._merge_deduplicate(chunks, standard)

        elif profile.strategy == RAGStrategy.HIERARCHICAL:
            chunks = self._hierarchical_retrieval(query, profile, book_indices=book_indices)
            # Fallback: nếu HRAG < 3 chunks → bổ sung standard
            if len(chunks) < 3 and not self._is_scoped_topic_search(profile, book_indices):
                standard = self._standard_retrieval(query, book_indices=book_indices)
                chunks = self._merge_deduplicate(chunks, standard)

        else:  # STANDARD
            chunks = self._standard_retrieval(query, book_indices=book_indices)

        total_time = time.time() - t0

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
        # Rerank deferred to RAGService._rerank_and_filter (task-aware top_n)
        stats = getattr(self.retriever, "last_search_stats", {})
        logger.info(
            "RAG retrieve | strategy=standard bm25_chunks=%s vector_chunks=%s combined_chunks=%s candidates=%s",
            stats.get("bm25_chunks", 0),
            stats.get("vector_chunks", 0),
            stats.get("combined_chunks", len(results)),
            len(results),
        )
        return results

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
        scoped_topic = self._is_scoped_topic_search(profile, book_indices)

        # ── Phase 1: Coarse — tìm parents (Level 1-2) ──────────────
        parent_indices = []
        topic_parent_indices = []
        for i, chunk in enumerate(all_chunks):
            if scope_set is not None and i not in scope_set:
                continue
            m = self._metadata_for_chunk(chunk)
            level = m.get("level", 99)
            if level > 2:
                continue
            # Filter by grade nếu có
            if profile.grade and m.get("grade") != profile.grade:
                continue
            parent_indices.append(i)
            if profile.topic_hint and self._matches_topic_hint(chunk, profile.topic_hint):
                topic_parent_indices.append(i)

        logger.info(
            "HRAG scope | grade=%s topic=%s book_scoped=%s parents=%s topic_parents=%s",
            profile.grade,
            profile.topic_hint,
            book_indices is not None,
            len(parent_indices),
            len(topic_parent_indices),
        )

        if scoped_topic:
            if not topic_parent_indices:
                logger.info("HRAG result | no topic parents in scope -> 0 chunks")
                return []
            parent_indices = topic_parent_indices

        if not parent_indices:
            # HRAG Phase 1: no parent chunks found → fallback standard
            logger.info("HRAG result | no parents -> 0 chunks")
            return []

        # Semantic search chỉ trên parents
        parent_results = self.retriever.search_scoped(
            query, doc_indices=parent_indices, top_k=3, top_n=min(30, len(parent_indices))
        )
        logger.info(
            "HRAG phase1 | parent_candidates=%s parent_results=%s",
            len(parent_indices),
            len(parent_results),
        )

        # Extract parent keys: (topic_name, lesson_name)
        parent_keys = set()
        for res in parent_results:
            m = res["metadata"]
            parent_keys.add((m.get("topic_name", ""), m.get("lesson_name", "")))



        # ── Phase 2: Fine — search children (Level 3+) ─────────────
        child_indices = []
        for i, chunk in enumerate(all_chunks):
            if scope_set is not None and i not in scope_set:
                continue
            m = self._metadata_for_chunk(chunk)
            level = m.get("level", 0)
            if level < 3:
                continue
            key = (m.get("topic_name", ""), m.get("lesson_name", ""))
            if key in parent_keys:
                child_indices.append(i)

        if not child_indices:
            # HRAG Phase 2: no children found → returning parent chunks
            final = parent_results if not scoped_topic else []
            logger.info(
                "HRAG phase2 | child_candidates=0 final_chunks=%s",
                len(final),
            )
            return final



        # Scoped hybrid search (BM25 + Semantic + RRF) trên children
        child_results = self.retriever.search_scoped(
            query,
            doc_indices=child_indices,
            top_k=self.settings.RETRIEVER_TOP_K,
            top_n=min(30, len(child_indices)),
        )

        if not child_results:
            logger.info(
                "HRAG phase2 | child_candidates=%s child_results=0 final_chunks=%s",
                len(child_indices),
                len(parent_results),
            )
            return parent_results

        # Rerank deferred to RAGService._rerank_and_filter (task-aware top_n)
        final = child_results
        stats = getattr(self.retriever, "last_search_stats", {})
        logger.info(
            "HRAG phase2 | child_candidates=%s child_results=%s bm25_chunks=%s vector_chunks=%s candidates=%s",
            len(child_indices),
            len(child_results),
            stats.get("bm25_chunks", 0),
            stats.get("vector_chunks", 0),
            len(final),
        )
        return final

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
            if self._metadata_for_chunk(chunk).get("book") == book:
                indices.append(i)
        return indices

    def _metadata_for_chunk(self, chunk: Dict) -> Dict:
        metadata_getter = getattr(self.retriever, "_metadata_for_chunk", None)
        if callable(metadata_getter):
            return metadata_getter(chunk)
        return chunk.get("metadata", {})

    @staticmethod
    def _is_scoped_topic_search(profile: QueryProfile, book_indices: List[int] = None) -> bool:
        return bool(profile.topic_hint and (profile.grade or book_indices is not None))

    def _matches_topic_hint(self, chunk: Dict, topic_hint: str) -> bool:
        metadata = self._metadata_for_chunk(chunk)
        haystack = " ".join(
            str(metadata.get(key, ""))
            for key in ("topic_name", "lesson_name", "title")
        )
        haystack = f"{haystack} {chunk.get('context', '')}"
        normalized_hint = self._normalize_text(topic_hint)
        normalized_haystack = self._normalize_text(haystack)
        if normalized_hint and normalized_hint in normalized_haystack:
            return True

        hint_tokens = self._meaningful_tokens(topic_hint)
        if not hint_tokens or len(hint_tokens) > 2:
            return False
        haystack_tokens = set(self._meaningful_tokens(haystack))
        return all(token in haystack_tokens for token in hint_tokens)

    @staticmethod
    def _normalize_text(text: str) -> str:
        normalized = text.lower()
        normalized = (
            normalized
            .replace("á", "a").replace("à", "a").replace("ả", "a").replace("ã", "a").replace("ạ", "a")
            .replace("ă", "a").replace("ắ", "a").replace("ằ", "a").replace("ẳ", "a").replace("ẵ", "a").replace("ặ", "a")
            .replace("â", "a").replace("ấ", "a").replace("ầ", "a").replace("ẩ", "a").replace("ẫ", "a").replace("ậ", "a")
            .replace("é", "e").replace("è", "e").replace("ẻ", "e").replace("ẽ", "e").replace("ẹ", "e")
            .replace("ê", "e").replace("ế", "e").replace("ề", "e").replace("ể", "e").replace("ễ", "e").replace("ệ", "e")
            .replace("í", "i").replace("ì", "i").replace("ỉ", "i").replace("ĩ", "i").replace("ị", "i")
            .replace("ó", "o").replace("ò", "o").replace("ỏ", "o").replace("õ", "o").replace("ọ", "o")
            .replace("ô", "o").replace("ố", "o").replace("ồ", "o").replace("ổ", "o").replace("ỗ", "o").replace("ộ", "o")
            .replace("ơ", "o").replace("ớ", "o").replace("ờ", "o").replace("ở", "o").replace("ỡ", "o").replace("ợ", "o")
            .replace("ú", "u").replace("ù", "u").replace("ủ", "u").replace("ũ", "u").replace("ụ", "u")
            .replace("ư", "u").replace("ứ", "u").replace("ừ", "u").replace("ử", "u").replace("ữ", "u").replace("ự", "u")
            .replace("ý", "y").replace("ỳ", "y").replace("ỷ", "y").replace("ỹ", "y").replace("ỵ", "y")
            .replace("đ", "d")
        )
        return " ".join(re.findall(r"[a-z0-9]+", normalized))

    @classmethod
    def _meaningful_tokens(cls, text: str) -> List[str]:
        stopwords = {"ve", "về", "va", "và", "cua", "của", "cac", "các", "hoc", "học"}
        normalized = cls._normalize_text(text)
        return [
            token
            for token in re.findall(r"[a-z0-9]+", normalized)
            if len(token) > 1 and token not in stopwords
        ]


__all__ = ["AdaptiveRAGAgent", "RAGStrategy", "RAGResult", "QueryClassifier"]
