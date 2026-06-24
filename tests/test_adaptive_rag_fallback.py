from types import SimpleNamespace

from src.rag.adaptive_rag import AdaptiveRAGAgent, QueryClassifier
from src.rag.rag_service import RAGService


class FakeRetriever:
    def __init__(self):
        self.chunks = [
            {
                "chunk_id": "k10-parent",
                "content": "Chủ đề lập trình.",
                "metadata": {
                    "book": "KNTT",
                    "grade": "10",
                    "topic_name": "Chủ đề lập trình",
                    "lesson_name": "Bài cấu trúc lặp",
                    "title": "Lập trình",
                    "level": 2,
                },
            },
            {
                "chunk_id": "k10-child",
                "content": "Vòng lặp for và while trong Python.",
                "metadata": {
                    "book": "KNTT",
                    "grade": "10",
                    "topic_name": "Chủ đề lập trình",
                    "lesson_name": "Bài cấu trúc lặp",
                    "title": "For while",
                    "level": 3,
                },
            },
            {
                "chunk_id": "k11-child",
                "content": "Nội dung lớp 11.",
                "metadata": {
                    "book": "KNTT",
                    "grade": "11",
                    "topic_name": "Lớp 11",
                    "lesson_name": "Bài khác",
                    "title": "Khác",
                    "level": 3,
                },
            },
            {
                "chunk_id": "cd10-child",
                "content": "Nội dung Cánh Diều.",
                "metadata": {
                    "book": "CD",
                    "grade": "10",
                    "topic_name": "CD",
                    "lesson_name": "Bài khác",
                    "title": "Khác",
                    "level": 3,
                },
            },
        ]
        self.last_search_stats = {}
        self.scoped_calls = []

    def _metadata_for_chunk(self, chunk):
        return chunk["metadata"]

    def search_scoped(self, query, doc_indices, top_k=10, top_n=30):
        self.scoped_calls.append(list(doc_indices))
        self.last_search_stats = {
            "bm25_chunks": len(doc_indices),
            "vector_chunks": len(doc_indices),
            "combined_chunks": len(doc_indices),
        }
        return [
            {
                "doc_id": self.chunks[index]["chunk_id"],
                "score": 1.0,
                "content": self.chunks[index]["content"],
                "context": "",
                "metadata": self.chunks[index]["metadata"],
            }
            for index in doc_indices[:top_k]
        ]

    def search(self, query, top_k=10):
        raise AssertionError("Expected scoped fallback, not global search")


def test_hierarchical_topic_miss_falls_back_to_book_grade_scoped_hybrid():
    retriever = FakeRetriever()
    agent = AdaptiveRAGAgent(
        retriever=retriever,
        reranker=None,
        settings=SimpleNamespace(RETRIEVER_TOP_K=5),
    )

    result = agent.retrieve(
        "Bài giảng cấu trúc lặp trong Python Tin học 10 Kết Nối Tri Thức",
        intent_hint="generate",
        topic_hint=(
            "Tin học 10 - cấu trúc lặp trong Python, gồm khái niệm câu lệnh lặp, "
            "vòng lặp for, vòng lặp while"
        ),
        grade_hint=None,
        book="KNTT",
    )

    assert result.chunks
    assert result.metadata_filter["grade"] == "10"
    assert retriever.scoped_calls == [[0, 1]]
    assert {chunk["metadata"]["book"] for chunk in result.chunks} == {"KNTT"}
    assert {chunk["metadata"]["grade"] for chunk in result.chunks} == {"10"}


def test_grade_extractors_accept_tin_hoc_pattern():
    assert QueryClassifier()._detect_grade("tin học 10 cấu trúc lặp") == "10"
    assert RAGService._extract_grade_from_topic("Tin học 10 - cấu trúc lặp") == "10"
