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
    LESSON_SCOPED = "lesson_scoped"
    STANDARD_WITH_HRAG = "standard+hierarchical"


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
    debug_stats: Dict = field(default_factory=dict)


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
        "10": ["lớp 10", "tin 10", "tin học 10", "grade 10", "lớp mười "],
        "11": ["lớp 11", "tin 11", "tin học 11", "grade 11", "lớp mười một"],
        "12": ["lớp 12", "tin 12", "tin học 12", "grade 12", "lớp mười hai"],
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
        task_type: str = None,
        lesson_reference: str = None,
        lesson_context: Dict = None,
    ) -> RAGResult:
        t0 = time.time()

        # === OBSERVE — tích hợp signals từ IntentRouter ===
        profile = self.classifier.classify(
            query,
            intent_hint=intent_hint,
            grade_hint=grade_hint,
            topic_hint=topic_hint,
        )
        scope_indices = (
            self._get_scope_indices(book=book, grade=profile.grade)
            if book or profile.grade
            else None
        )

        debug_stats = {
            "standard_candidates": 0,
            "broad_candidates": 0,
            "hrag_candidates": 0,
            "lesson_scoped_candidates": 0,
            "merged_candidates": 0,
            "pre_rerank_candidates": 0,
            "pre_rerank_cap_applied": False,
            "hrag_enabled": False,
            "hrag_reason": None,
            "lesson_scoped": False,
        }

        # === ACT ===
        lesson_scoped = self._lesson_scoped_retrieval(lesson_context)
        if lesson_context and lesson_scoped:
            chunks = self._cap_pre_rerank_candidates(lesson_scoped, task_type=task_type)
            debug_stats.update({
                "lesson_scoped": True,
                "lesson_scoped_candidates": len(lesson_scoped),
                "merged_candidates": len(lesson_scoped),
                "pre_rerank_candidates": len(chunks),
                "pre_rerank_cap_applied": len(chunks) < len(lesson_scoped),
                "lesson_context": {
                    "book": lesson_context.get("book"),
                    "grade": lesson_context.get("grade"),
                    "topic_ref": lesson_context.get("topic_ref"),
                    "lesson_num": lesson_context.get("lesson_num"),
                    "lesson_name": lesson_context.get("lesson_name"),
                },
            })

        elif profile.strategy == RAGStrategy.CURRICULUM:
            chunks = self._curriculum_lookup(profile, book=book)
            debug_stats["merged_candidates"] = len(chunks)

        elif profile.strategy == RAGStrategy.BROAD:
            standard = self._standard_retrieval(query, book_indices=scope_indices)
            broad = self._broad_retrieval(query, profile, book=book)
            chunks = self._merge_weighted_results(
                ("standard", standard, 1.0),
                ("broad", broad, 0.5),
            )
            merged_count = len(chunks)
            chunks = self._cap_pre_rerank_candidates(chunks, task_type=task_type)
            debug_stats.update({
                "standard_candidates": len(standard),
                "broad_candidates": len(broad),
                "merged_candidates": merged_count,
                "pre_rerank_candidates": len(chunks),
                "pre_rerank_cap_applied": len(chunks) < merged_count,
            })

        elif profile.strategy == RAGStrategy.HIERARCHICAL:
            standard = self._standard_retrieval(query, book_indices=scope_indices)
            hrag_enabled, hrag_reason = self._should_use_hrag(
                query=query,
                profile=profile,
                book=book,
                book_indices=scope_indices,
                task_type=task_type,
                lesson_reference=lesson_reference,
            )
            hrag = []
            if hrag_enabled:
                hrag = self._hierarchical_retrieval(query, profile, book_indices=scope_indices)
            hrag_weight = self._hrag_weight(query, lesson_reference)
            chunks = self._merge_weighted_results(
                ("standard", standard, 1.0),
                ("hrag", hrag, hrag_weight),
            )
            merged_count = len(chunks)
            chunks = self._cap_pre_rerank_candidates(chunks, task_type=task_type)
            debug_stats.update({
                "standard_candidates": len(standard),
                "hrag_candidates": len(hrag),
                "merged_candidates": merged_count,
                "pre_rerank_candidates": len(chunks),
                "pre_rerank_cap_applied": len(chunks) < merged_count,
                "hrag_enabled": hrag_enabled,
                "hrag_reason": hrag_reason,
                "hrag_weight": hrag_weight if hrag_enabled else 0.0,
            })

        else:  # STANDARD
            chunks = self._standard_retrieval(query, book_indices=scope_indices)
            debug_stats.update({
                "standard_candidates": len(chunks),
                "merged_candidates": len(chunks),
                "pre_rerank_candidates": len(chunks),
            })

        total_time = time.time() - t0
        strategy_used = profile.strategy
        if debug_stats.get("lesson_scoped"):
            strategy_used = RAGStrategy.LESSON_SCOPED
        elif profile.strategy == RAGStrategy.HIERARCHICAL:
            strategy_used = (
                RAGStrategy.STANDARD_WITH_HRAG
                if debug_stats.get("hrag_enabled")
                else RAGStrategy.STANDARD
            )
        elif profile.strategy == RAGStrategy.BROAD:
            strategy_used = RAGStrategy.BROAD

        reason = profile.reason
        if debug_stats.get("lesson_scoped"):
            reason = (
                "Lesson-scoped retrieval from table_of_contents; "
                f"lesson={lesson_context.get('lesson_name')} "
                f"({lesson_context.get('book')} lớp {lesson_context.get('grade')})."
            )
        elif profile.strategy == RAGStrategy.HIERARCHICAL:
            reason = (
                "Standard-first retrieval; "
                f"HRAG {'enabled' if debug_stats.get('hrag_enabled') else 'disabled'} "
                f"({debug_stats.get('hrag_reason')}). Original classifier: {profile.reason}"
            )
        elif profile.strategy == RAGStrategy.BROAD:
            reason = f"Standard-first broad retrieval; broad metadata merged. Original classifier: {profile.reason}"

        return RAGResult(
            chunks=chunks,
            strategy_used=strategy_used,
            metadata_filter={"grade": profile.grade, "topic": profile.topic_hint, "book": book},
            total_time_s=round(total_time, 2),
            reason=reason,
            debug_stats=debug_stats,
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
                logger.info(
                    "HRAG result | no topic parents in scope -> fallback standard scoped search"
                )
                return self._standard_retrieval(query, book_indices=book_indices)
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

    def _lesson_scoped_retrieval(self, lesson_context: Optional[Dict]) -> List[Dict]:
        if not lesson_context:
            return []

        results = []
        for index, chunk in enumerate(self.retriever.chunks):
            metadata = self._metadata_for_chunk(chunk)
            if not self._matches_lesson_context(metadata, lesson_context):
                continue
            results.append({
                "doc_id": chunk.get("chunk_id") or chunk.get("doc_id") or str(index),
                "score": 1.0,
                "content": chunk.get("content", ""),
                "context": chunk.get("context") or chunk.get("breadcrumb", ""),
                "metadata": metadata,
                "retrieval_sources": ["lesson_scoped"],
                "lesson_scoped_score": 1.0,
                "retrieval_weight": 1.0,
            })

        logger.info(
            "Lesson-scoped retrieval | book=%s grade=%s topic=%s lesson=%s chunks=%s",
            lesson_context.get("book"),
            lesson_context.get("grade"),
            lesson_context.get("topic_name"),
            lesson_context.get("lesson_name"),
            len(results),
        )
        return results

    def _matches_lesson_context(self, metadata: Dict, lesson_context: Dict) -> bool:
        for meta_key, ctx_key in (("book", "book"), ("grade", "grade")):
            expected = lesson_context.get(ctx_key)
            if expected is not None and str(metadata.get(meta_key)) != str(expected):
                return False

        expected_topic_ref = str(lesson_context.get("topic_ref") or "").strip()
        actual_topic_ref = str(
            metadata.get("topic") or metadata.get("topic_ref") or ""
        ).strip()
        topic_ref_matched = False
        if expected_topic_ref and actual_topic_ref:
            if self._normalize_text(expected_topic_ref) != self._normalize_text(actual_topic_ref):
                return False
            topic_ref_matched = True

        expected_lesson_num = str(lesson_context.get("lesson_num") or "").strip()
        actual_lesson_label = str(metadata.get("lesson") or metadata.get("lesson_num") or "")
        actual_lesson_num = self._extract_lesson_number(actual_lesson_label)
        lesson_num_matched = False
        if expected_lesson_num and actual_lesson_label:
            if not actual_lesson_num or expected_lesson_num != actual_lesson_num:
                return False
            lesson_num_matched = True

        structural_match = topic_ref_matched and lesson_num_matched

        if not topic_ref_matched and not self._text_fields_match(
            lesson_context.get("topic_name"),
            metadata.get("topic_name"),
            allow_one_way=False,
        ):
            return False

        return self._text_fields_match(
            lesson_context.get("lesson_name"),
            metadata.get("lesson_name"),
            allow_one_way=structural_match,
        )

    def _text_fields_match(
        self,
        expected_value: Optional[str],
        actual_value: Optional[str],
        allow_one_way: bool = False,
    ) -> bool:
        expected = str(expected_value or "")
        actual = str(actual_value or "")
        if not expected:
            return True
        if not actual:
            return False

        expected_norm = self._normalize_text(expected)
        actual_norm = self._normalize_text(actual)
        if expected_norm == actual_norm:
            return True

        expected_to_actual = self._token_overlap_ratio(expected, actual)
        actual_to_expected = self._token_overlap_ratio(actual, expected)
        if allow_one_way:
            return max(expected_to_actual, actual_to_expected) >= 0.75

        return expected_to_actual >= 0.75 and actual_to_expected >= 0.75

    @staticmethod
    def _extract_lesson_number(value: str) -> Optional[str]:
        match = re.search(r"\b(?:bài|bai)?\s*(\d+)\b", str(value).lower())
        return match.group(1) if match else None
        return True

    def _merge_weighted_results(self, *branches) -> List[Dict]:
        merged_by_id: Dict[str, Dict] = {}
        order: List[str] = []
        for source, chunks, weight in branches:
            for chunk in chunks or []:
                doc_id = chunk.get("doc_id") or chunk.get("chunk_id")
                if doc_id is None:
                    continue
                raw_score = float(chunk.get("score", 0.0) or 0.0)
                weighted_score = raw_score * weight
                if doc_id not in merged_by_id:
                    item = dict(chunk)
                    item["doc_id"] = doc_id
                    item["score"] = weighted_score
                    item["retrieval_sources"] = [source]
                    item["retrieval_weight"] = weight
                    item[f"{source}_score"] = raw_score
                    merged_by_id[doc_id] = item
                    order.append(doc_id)
                    continue

                item = merged_by_id[doc_id]
                sources = item.setdefault("retrieval_sources", [])
                if source not in sources:
                    sources.append(source)
                item[f"{source}_score"] = raw_score
                item["retrieval_weight"] = max(float(item.get("retrieval_weight", 0.0)), weight)
                item["score"] = max(float(item.get("score", 0.0) or 0.0), weighted_score)

        return [merged_by_id[doc_id] for doc_id in order]

    def _cap_pre_rerank_candidates(self, chunks: List[Dict], task_type: str = None) -> List[Dict]:
        max_candidates = self._pre_rerank_max_candidates(task_type)
        if max_candidates <= 0 or len(chunks) <= max_candidates:
            return chunks

        overlap = [
            chunk for chunk in chunks
            if len(chunk.get("retrieval_sources") or []) > 1
        ]
        selected: List[Dict] = []
        selected_ids = set()

        for item in self._sort_candidates(overlap):
            if len(selected) >= max_candidates:
                break
            doc_id = item.get("doc_id") or item.get("chunk_id")
            if doc_id not in selected_ids:
                selected.append(item)
                selected_ids.add(doc_id)

        hrag_quota = self._pre_rerank_hrag_quota(task_type)
        hrag_items = [
            chunk for chunk in chunks
            if "hrag" in (chunk.get("retrieval_sources") or [])
        ]
        hrag_selected = sum(
            1 for chunk in selected
            if "hrag" in (chunk.get("retrieval_sources") or [])
        )
        for item in self._sort_candidates(hrag_items):
            if len(selected) >= max_candidates or hrag_selected >= hrag_quota:
                break
            doc_id = item.get("doc_id") or item.get("chunk_id")
            if doc_id in selected_ids:
                continue
            selected.append(item)
            selected_ids.add(doc_id)
            hrag_selected += 1

        standard_items = [
            chunk for chunk in chunks
            if "standard" in (chunk.get("retrieval_sources") or [])
        ]
        for item in self._sort_candidates(standard_items):
            if len(selected) >= max_candidates:
                break
            doc_id = item.get("doc_id") or item.get("chunk_id")
            if doc_id in selected_ids:
                continue
            selected.append(item)
            selected_ids.add(doc_id)

        for item in self._sort_candidates(chunks):
            if len(selected) >= max_candidates:
                break
            doc_id = item.get("doc_id") or item.get("chunk_id")
            if doc_id in selected_ids:
                continue
            selected.append(item)
            selected_ids.add(doc_id)

        return selected

    @staticmethod
    def _sort_candidates(chunks: List[Dict]) -> List[Dict]:
        return sorted(
            chunks,
            key=lambda chunk: (
                len(chunk.get("retrieval_sources") or []),
                float(chunk.get("score", 0.0) or 0.0),
            ),
            reverse=True,
        )

    def _pre_rerank_max_candidates(self, task_type: str = None) -> int:
        if task_type in ("slide", "slide_generate"):
            return int(getattr(self.settings, "RAG_PRE_RERANK_MAX_CANDIDATES_SLIDE", 28))
        if task_type in ("lesson_plan", "giao_an"):
            return int(getattr(self.settings, "RAG_PRE_RERANK_MAX_CANDIDATES_LESSON_PLAN", 34))
        return int(getattr(self.settings, "RAG_PRE_RERANK_MAX_CANDIDATES", 25))

    def _pre_rerank_hrag_quota(self, task_type: str = None) -> int:
        if task_type in ("lesson_plan", "giao_an"):
            return int(getattr(self.settings, "RAG_PRE_RERANK_HRAG_QUOTA_LESSON_PLAN", 12))
        if task_type in ("slide", "slide_generate"):
            return int(getattr(self.settings, "RAG_PRE_RERANK_HRAG_QUOTA_SLIDE", 10))
        return max(4, self._pre_rerank_max_candidates(task_type) // 3)

    def _should_use_hrag(
        self,
        query: str,
        profile: QueryProfile,
        book: str = None,
        book_indices: List[int] = None,
        task_type: str = None,
        lesson_reference: str = None,
    ) -> tuple[bool, str]:
        if lesson_reference:
            return True, "lesson_reference present"
        if self._has_explicit_structure_reference(query):
            return True, "explicit lesson/chapter/topic reference in query"
        if (
            task_type in ("slide", "slide_generate", "lesson_plan", "giao_an")
            and book
            and profile.topic_hint
        ):
            if profile.grade:
                return True, "structured generation with book+grade+topic"
            return True, "structured generation with book+topic"
        if profile.topic_hint and (profile.grade or book_indices is not None):
            return False, "topic context is available but not strong enough for auxiliary HRAG"
        return False, "no structural retrieval signal"

    def _hrag_weight(self, query: str, lesson_reference: str = None) -> float:
        if lesson_reference:
            return 0.75
        if self._has_explicit_structure_reference(query):
            return 0.65
        return 0.45

    @staticmethod
    def _has_explicit_structure_reference(query: str) -> bool:
        q = query.lower()
        return bool(
            re.search(
                r"\b(bài|bai|chương|chuong|mục|muc|phần|phan)\s*([0-9]+|[a-h])\b",
                q,
            )
            or re.search(r"\b(chủ\s*đề|chu\s*de)\s*([0-9]+|[a-h])\b", q)
        )

    def _get_book_indices(self, book: str) -> List[int]:
        return self._get_scope_indices(book=book, grade=None)

    def _get_scope_indices(self, book: str = None, grade: str = None) -> List[int]:
        indices = []
        for i, chunk in enumerate(self.retriever.chunks):
            metadata = self._metadata_for_chunk(chunk)
            if book and metadata.get("book") != book:
                continue
            if grade and metadata.get("grade") != grade:
                continue
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

        if " - " in topic_hint:
            topic_part, lesson_part = topic_hint.split(" - ", 1)
            return (
                self._token_overlap_ratio(topic_part, haystack) >= 0.75
                and self._token_overlap_ratio(lesson_part, haystack) >= 0.75
            )

        hint_tokens = self._meaningful_tokens(topic_hint)
        if not hint_tokens:
            return False
        haystack_tokens = set(self._meaningful_tokens(haystack))
        if len(hint_tokens) > 2:
            return self._token_overlap_ratio(topic_hint, haystack) >= 0.75
        return all(token in haystack_tokens for token in hint_tokens)

    @classmethod
    def _token_overlap_ratio(cls, needle: str, haystack: str) -> float:
        needle_tokens = set(cls._meaningful_tokens(needle))
        if not needle_tokens:
            return 0.0
        haystack_tokens = set(cls._meaningful_tokens(haystack))
        return len(needle_tokens.intersection(haystack_tokens)) / len(needle_tokens)

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
