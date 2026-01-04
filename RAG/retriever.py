import faiss
import numpy as np
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi
from typing import List, Dict


class Retriever:

    def __init__(self, model):
        self.model = model
        self.bm25 = None
        self.index = None
        self.data = None

    def set_data(self, data: List[Dict]):
        self.data = data

    def build_bm25(self, corpus_texts: List[str]):
        tokenized_corpus = [word_tokenize(text.lower()) for text in corpus_texts]
        self.bm25 = BM25Okapi(tokenized_corpus)
        return self.bm25

    def bm25_search(self, query, top_k=5):
        if self.bm25 is None:
            raise ValueError("BM25 chưa được build! Hãy gọi build_bm25 trước.")
        tokenized_query = word_tokenize(query.lower())
        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = np.argsort(scores)[::-1][:top_k]
        ranked_results = [
            (rank, int(idx), float(scores[idx]))
            for rank, idx in enumerate(ranked_indices)
        ]
        return ranked_results, [float(scores[i]) for i in ranked_indices]

    def build_faiss_index(self, embeddings: np.ndarray, metric: str = "IP"):
        dim = embeddings.shape[1]
        if metric == "IP":
            self.index = faiss.IndexFlatIP(dim)
        elif metric == "L2":
            self.index = faiss.IndexFlatL2(dim)
        else:
            raise ValueError("metric must be 'IP' or 'L2'")
        self.index.add(embeddings.astype(np.float32))
        return self.index

    def faiss_search(self, query, top_k=5):
        if self.index is None:
            raise ValueError("FAISS index chưa được build! Hãy gọi build_faiss_index trước.")
        query_vec = self.model.encode([query], normalize_embeddings=True).astype(np.float32)
        scores, indices = self.index.search(query_vec, top_k)

        ranked_results = [
            (rank, int(idx), float(scores[0][rank]))
            for rank, idx in enumerate(indices[0])
        ]
        return ranked_results, [float(s) for s in scores[0]]

    def hybrid_search_RRF(self, query, top_k=5, k=60, weight_bm25=0.3, weight_faiss=0.7):
        if self.data is None:
            raise ValueError("Data chưa được gán! Hãy gọi set_data trước.")

        bm25_ranked, _ = self.bm25_search(query, top_k=top_k * 2)
        faiss_ranked, _ = self.faiss_search(query, top_k=top_k * 2)

        rrf_scores = {}

        for rank, idx, _ in bm25_ranked:
            rrf_scores[idx] = rrf_scores.get(idx, 0) + (1 / (k + rank + 1)) * weight_bm25

        for rank, idx, _ in faiss_ranked:
            rrf_scores[idx] = rrf_scores.get(idx, 0) + (1 / (k + rank + 1)) * weight_faiss

        sorted_rrf = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

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
