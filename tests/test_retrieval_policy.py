from types import SimpleNamespace

from src.rag.adaptive_rag import AdaptiveRAGAgent, RAGStrategy


class PolicyFakeRetriever:
    def __init__(self):
        self.chunks = [
            {
                "chunk_id": "parent-network",
                "content": "Chủ đề mạng máy tính.",
                "metadata": {
                    "book": "KNTT",
                    "grade": "10",
                    "topic_name": "Mạng máy tính",
                    "lesson_name": "Bài mạng máy tính",
                    "title": "Mạng máy tính",
                    "level": 2,
                },
            },
            {
                "chunk_id": "child-network",
                "content": "Mạng máy tính kết nối các thiết bị để chia sẻ dữ liệu.",
                "metadata": {
                    "book": "KNTT",
                    "grade": "10",
                    "topic_name": "Mạng máy tính",
                    "lesson_name": "Bài mạng máy tính",
                    "title": "Khái niệm mạng",
                    "level": 3,
                },
            },
            {
                "chunk_id": "child-security",
                "content": "An toàn trên không gian mạng cần cảnh giác mã độc.",
                "metadata": {
                    "book": "KNTT",
                    "grade": "10",
                    "topic_name": "An toàn mạng",
                    "lesson_name": "Bài an toàn mạng",
                    "title": "An toàn mạng",
                    "level": 3,
                },
            },
            {
                "chunk_id": "cd-network",
                "content": "Nội dung mạng máy tính Cánh Diều.",
                "metadata": {
                    "book": "CD",
                    "grade": "10",
                    "topic_name": "Mạng máy tính",
                    "lesson_name": "Bài mạng máy tính",
                    "title": "Mạng máy tính",
                    "level": 3,
                },
            },
        ]
        self.last_search_stats = {}
        self.scoped_calls = []

    def _metadata_for_chunk(self, chunk):
        return chunk["metadata"]

    def search_scoped(self, query, doc_indices, top_k=10, top_n=30):
        indices = list(doc_indices)
        self.scoped_calls.append(indices)
        self.last_search_stats = {
            "bm25_chunks": len(indices),
            "vector_chunks": len(indices),
            "combined_chunks": len(indices),
        }
        return [
            {
                "doc_id": self.chunks[index]["chunk_id"],
                "score": 1.0 - (rank * 0.05),
                "content": self.chunks[index]["content"],
                "context": "",
                "metadata": self.chunks[index]["metadata"],
            }
            for rank, index in enumerate(indices[:top_k])
        ]

    def search(self, query, top_k=10):
        return self.search_scoped(query, range(len(self.chunks)), top_k=top_k)


def _agent(retriever):
    return AdaptiveRAGAgent(
        retriever=retriever,
        reranker=None,
        settings=SimpleNamespace(
            RETRIEVER_TOP_K=10,
            RAG_PRE_RERANK_MAX_CANDIDATES=25,
            RAG_PRE_RERANK_MAX_CANDIDATES_SLIDE=28,
            RAG_PRE_RERANK_MAX_CANDIDATES_LESSON_PLAN=34,
            RAG_PRE_RERANK_HRAG_QUOTA_SLIDE=10,
            RAG_PRE_RERANK_HRAG_QUOTA_LESSON_PLAN=12,
        ),
    )


def test_loose_topic_without_scope_uses_standard_first_without_hrag():
    retriever = PolicyFakeRetriever()
    result = _agent(retriever).retrieve(
        "sinh cho tôi slide về mạng máy tính có ảnh minh họa",
        intent_hint="generate",
        topic_hint="mạng máy tính",
        task_type="slide",
    )

    assert result.strategy_used == RAGStrategy.STANDARD
    assert result.debug_stats["standard_candidates"] == 4
    assert result.debug_stats["hrag_enabled"] is False
    assert result.debug_stats["hrag_candidates"] == 0
    assert retriever.scoped_calls == [[0, 1, 2, 3]]
    assert all(chunk["retrieval_sources"] == ["standard"] for chunk in result.chunks)


def test_structured_slide_with_book_and_topic_adds_auxiliary_hrag():
    retriever = PolicyFakeRetriever()
    result = _agent(retriever).retrieve(
        "sinh cho tôi slide về mạng máy tính có ảnh minh họa",
        intent_hint="generate",
        topic_hint="mạng máy tính",
        book="KNTT",
        task_type="slide",
    )

    assert result.strategy_used == RAGStrategy.STANDARD_WITH_HRAG
    assert result.debug_stats["standard_candidates"] == 3
    assert result.debug_stats["hrag_enabled"] is True
    assert result.debug_stats["hrag_candidates"] >= 1
    assert retriever.scoped_calls[0] == [0, 1, 2]
    assert {chunk["metadata"]["book"] for chunk in result.chunks} == {"KNTT"}
    assert any("hrag" in chunk["retrieval_sources"] for chunk in result.chunks)


def test_explicit_lesson_reference_merges_standard_with_auxiliary_hrag():
    retriever = PolicyFakeRetriever()
    result = _agent(retriever).retrieve(
        "sinh slide bài 1 về mạng máy tính Tin học 10",
        intent_hint="generate",
        topic_hint="mạng máy tính",
        grade_hint="10",
        book="KNTT",
        task_type="slide",
        lesson_reference="Bài 1",
    )

    assert result.strategy_used == RAGStrategy.STANDARD_WITH_HRAG
    assert result.debug_stats["hrag_enabled"] is True
    assert result.debug_stats["standard_candidates"] == 3
    assert result.debug_stats["hrag_candidates"] >= 1
    assert result.debug_stats["merged_candidates"] == len(result.chunks)
    assert len(retriever.scoped_calls) >= 3
    assert any("hrag" in chunk["retrieval_sources"] for chunk in result.chunks)
    assert any(chunk["retrieval_sources"] == ["standard", "hrag"] for chunk in result.chunks)


def test_exact_lesson_context_uses_lesson_scoped_retrieval_without_standard():
    retriever = PolicyFakeRetriever()
    result = _agent(retriever).retrieve(
        "sinh slide bài 1 về mạng máy tính Tin học 10",
        intent_hint="generate",
        topic_hint="mạng máy tính",
        grade_hint="10",
        book="KNTT",
        task_type="slide",
        lesson_reference="Bài 1",
        lesson_context={
            "book": "KNTT",
            "grade": "10",
            "topic_ref": "1",
            "topic_name": "Mạng máy tính",
            "lesson_num": "1",
            "lesson_name": "Bài mạng máy tính",
        },
    )

    assert result.strategy_used == RAGStrategy.LESSON_SCOPED
    assert result.debug_stats["lesson_scoped"] is True
    assert result.debug_stats["lesson_scoped_candidates"] == 2
    assert result.debug_stats["standard_candidates"] == 0
    assert result.debug_stats["hrag_candidates"] == 0
    assert retriever.scoped_calls == []
    assert {chunk["doc_id"] for chunk in result.chunks} == {"parent-network", "child-network"}
    assert all(chunk["retrieval_sources"] == ["lesson_scoped"] for chunk in result.chunks)


def test_lesson_context_does_not_match_nonnumeric_lesson_label():
    agent = _agent(PolicyFakeRetriever())
    context = {
        "book": "CD",
        "grade": "11",
        "topic_ref": "F",
        "topic_name": "GIẢI QUYẾT VẤN ĐỀ VỚI SỰ TRỢ GIÚP CỦA MÁY TÍNH",
        "lesson_num": "1",
        "lesson_name": "Bài toán quản lí và cơ sở dữ liệu",
    }

    assert agent._matches_lesson_context(
        {
            "book": "CD",
            "grade": "11",
            "topic": "F",
            "lesson": "Bài 1",
            "lesson_name": "BÀI TOÁN QUẢN LÍ VÀ CƠ SỞ DỮ LIỆU",
        },
        context,
    )
    assert not agent._matches_lesson_context(
        {
            "book": "CD",
            "grade": "11",
            "topic": "F",
            "lesson": "Bài G",
            "lesson_name": "Bài G: Nghề Quản trị cơ sở dữ liệu",
        },
        context,
    )


def test_weighted_merge_deduplicates_and_preserves_branch_scores():
    agent = _agent(PolicyFakeRetriever())
    merged = agent._merge_weighted_results(
        (
            "standard",
            [{"doc_id": "a", "score": 1.0}, {"doc_id": "b", "score": 0.8}],
            1.0,
        ),
        (
            "hrag",
            [{"doc_id": "a", "score": 0.9}, {"doc_id": "c", "score": 0.7}],
            0.5,
        ),
    )

    by_id = {chunk["doc_id"]: chunk for chunk in merged}
    assert list(by_id) == ["a", "b", "c"]
    assert by_id["a"]["retrieval_sources"] == ["standard", "hrag"]
    assert by_id["a"]["standard_score"] == 1.0
    assert by_id["a"]["hrag_score"] == 0.9
    assert by_id["a"]["score"] == 1.0
    assert by_id["c"]["retrieval_sources"] == ["hrag"]
    assert by_id["c"]["score"] == 0.35


def test_pre_rerank_cap_keeps_overlap_and_hrag_quota():
    agent = AdaptiveRAGAgent(
        retriever=PolicyFakeRetriever(),
        reranker=None,
        settings=SimpleNamespace(
            RETRIEVER_TOP_K=10,
            RAG_PRE_RERANK_MAX_CANDIDATES_SLIDE=5,
            RAG_PRE_RERANK_HRAG_QUOTA_SLIDE=2,
        ),
    )
    chunks = [
        {"doc_id": "overlap", "score": 1.0, "retrieval_sources": ["standard", "hrag"]},
        {"doc_id": "h1", "score": 0.9, "retrieval_sources": ["hrag"]},
        {"doc_id": "h2", "score": 0.8, "retrieval_sources": ["hrag"]},
        {"doc_id": "h3", "score": 0.7, "retrieval_sources": ["hrag"]},
        {"doc_id": "s1", "score": 0.95, "retrieval_sources": ["standard"]},
        {"doc_id": "s2", "score": 0.85, "retrieval_sources": ["standard"]},
        {"doc_id": "s3", "score": 0.75, "retrieval_sources": ["standard"]},
    ]

    capped = agent._cap_pre_rerank_candidates(chunks, task_type="slide")
    ids = [chunk["doc_id"] for chunk in capped]

    assert len(capped) == 5
    assert "overlap" in ids
    assert sum("hrag" in chunk["retrieval_sources"] for chunk in capped) == 2
    assert "s1" in ids
