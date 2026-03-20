"""Document retriever with hybrid search (BM25 + FAISS)"""

import faiss
import numpy as np
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi
from typing import List, Dict, Tuple, Optional


class Retriever:
    """
    Hybrid document retriever combining BM25 keyword search and FAISS vector search.

    Uses Reciprocal Rank Fusion (RRF) to combine ranking signals from both methods.
    """

    def __init__(self, model):
        """
        Initialize retriever.

        Args:
            model: Sentence transformer model for embeddings
        """
        self.model = model
        self.bm25 = None
        self.index = None
        self.data = None

    def set_data(self, data: List[Dict]) -> None:
        """
        Set chunk data for retrieval.

        Args:
            data: List of chunk dictionaries
        """
        if not data:
            raise ValueError("Data cannot be empty")

        self.data = data

    def build_bm25(self, corpus_texts: List[str]) -> BM25Okapi:
        """
        Build BM25 index from corpus texts.

        Args:
            corpus_texts: List of text documents

        Returns:
            BM25Okapi instance
        """
        if not corpus_texts:
            raise ValueError("corpus_texts cannot be empty")

        tokenized_corpus = [word_tokenize(text.lower()) for text in corpus_texts]
        self.bm25 = BM25Okapi(tokenized_corpus)
        return self.bm25

    def bm25_search(
        self,
        query: str,
        top_k: int = 5
    ) -> Tuple[List[Tuple[int, int, float]], List[float]]:
        """
        Search using BM25 keyword matching.

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            Tuple of:
                - List of (rank, doc_index, score) tuples
                - List of scores for top_k results
        """
        if self.bm25 is None:
            raise ValueError("BM25 not initialized. Call build_bm25() first")

        tokenized_query = word_tokenize(query.lower())
        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = np.argsort(scores)[::-1][:top_k]
        ranked_results = [
            (rank, int(idx), float(scores[idx]))
            for rank, idx in enumerate(ranked_indices)
        ]

        return ranked_results, [float(scores[i]) for i in ranked_indices]

    def build_faiss_index(
        self,
        embeddings: np.ndarray,
        metric: str = "IP"
    ) -> faiss.Index:
        """
        Build FAISS vector index.

        Args:
            embeddings: Document embeddings matrix (n_docs x embedding_dim)
            metric: Distance metric ("IP" for inner product or "L2" for Euclidean)

        Returns:
            FAISS index instance
        """
        if metric not in ["IP", "L2"]:
            raise ValueError("metric must be 'IP' or 'L2'")

        dim = embeddings.shape[1]

        if metric == "IP":
            self.index = faiss.IndexFlatIP(dim)
        else:
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(embeddings.astype(np.float32))
        return self.index

    def faiss_search(
        self,
        query: str,
        top_k: int = 5
    ) -> Tuple[List[Tuple[int, int, float]], List[float]]:
        """
        Search using FAISS vector similarity.

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            Tuple of:
                - List of (rank, doc_index, score) tuples
                - List of scores for top_k results
        """
        if self.index is None:
            raise ValueError("FAISS index not initialized. Call build_faiss_index() first")

        query_vec = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype(np.float32)

        scores, indices = self.index.search(query_vec, top_k)

        ranked_results = [
            (rank, int(idx), float(scores[0][rank]))
            for rank, idx in enumerate(indices[0])
        ]

        return ranked_results, [float(s) for s in scores[0]]

    def hybrid_search_RRF(
        self,
        query: str,
        top_k: int = 5,
        k: int = 60,
        weight_bm25: float = 0.3,
        weight_faiss: float = 0.7
    ) -> List[Dict]:
        """
        Hybrid search using Reciprocal Rank Fusion (RRF).

        Combines BM25 and FAISS rankings using RRF formula:
            RRF(d) = sum(1 / (k + rank_i(d)))

        Args:
            query: Search query
            top_k: Number of top results to return
            k: RRF parameter (constant, typically 60)
            weight_bm25: Weight for BM25 component (0-1)
            weight_faiss: Weight for FAISS component (0-1)

        Returns:
            List of ranked documents with metadata and RRF scores
        """
        if self.data is None:
            raise ValueError("Data not set. Call set_data() first")

        # Get BM25 results
        bm25_ranked, _ = self.bm25_search(query, top_k=top_k * 2)

        # Get FAISS results
        faiss_ranked, _ = self.faiss_search(query, top_k=top_k * 2)

        # Combine using RRF
        rrf_scores: Dict[int, float] = {}

        # Add BM25 contributions
        for rank, idx, _ in bm25_ranked:
            rrf_scores[idx] = rrf_scores.get(idx, 0) + (1 / (k + rank + 1)) * weight_bm25

        # Add FAISS contributions
        for rank, idx, _ in faiss_ranked:
            rrf_scores[idx] = rrf_scores.get(idx, 0) + (1 / (k + rank + 1)) * weight_faiss

        # Sort by RRF score
        sorted_rrf = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        # Build result list
        results_for_retrieval = []
        for idx, score in sorted_rrf[:top_k]:
            chunk = self.data[idx]
            results_for_retrieval.append({
                "rrf_score": float(score),
                "context": chunk.get("context"),
                "content": chunk.get("content"),
                "metadata": chunk.get("metadata", {})
            })

        return results_for_retrieval


__all__ = ["Retriever"]
