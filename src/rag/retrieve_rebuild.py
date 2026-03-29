import json
import numpy as np
import math
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import Counter

from src.rag.embedding import EmbeddingModel


class CustomSearch:
    """
    Hybrid Search: BM25 (keyword) + Semantic (cosine similarity) + RRF Fusion.
    
    - BM25: Tính TF, DF, IDF từ scratch, scoring theo BM25 formula.
    - Semantic: Cosine similarity = dot product trên L2-normalized embeddings.
    - RRF: Reciprocal Rank Fusion kết hợp 2 ranked lists.
    """
    
    def __init__(self, chunks_path: str, embeddings_path: str, k1: float = 1.2, b: float = 0.75, rrf_k: int = 60):
        """
        Khởi tạo CustomSearch.
        
        Args:
            chunks_path: Đường dẫn file JSON chunks (data/rag_chunks_v2.json)
            embeddings_path: Đường dẫn file numpy embeddings (data/embeddings.npy)
            k1: BM25 param — term frequency saturation
            b: BM25 param — document length normalization
            rrf_k: RRF constant (default 60)
        """
        # === Load data ===
        with open(chunks_path, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        self.embeddings = np.load(embeddings_path)
        
        self.corpus_size = len(self.chunks)
        assert self.corpus_size == self.embeddings.shape[0], \
            f"Chunks ({self.corpus_size}) và embeddings ({self.embeddings.shape[0]}) không khớp!"
        
        # === BM25 params ===
        self.k1 = k1
        self.b = b
        self.rrf_k = rrf_k
        
        # === Tokenize corpus + tính BM25 stats ===
        self.tokenized_corpus = [chunk["content"].lower().split() for chunk in self.chunks]
        self.doc_lens = np.array([len(doc) for doc in self.tokenized_corpus], dtype=np.float64)
        self.avgdl = np.mean(self.doc_lens)
        
        self.tf = self._compute_tf()
        self.df = self._compute_df()
        self.idf = self._compute_idf()
        
        # === Embedding model (lazy load) ===
        self._model = None
        
        print(f" CustomSearch initialized: {self.corpus_size} docs, "
              f"vocab={len(self.df)}, avgdl={self.avgdl:.1f}")
    
    @property
    def model(self):
        """Lazy load embedding model — chỉ load khi cần encode query."""
        if self._model is None:
            self._model = EmbeddingModel()
        return self._model
    
    # ============================================================
    # BM25 INTERNALS
    # ============================================================
    
    def _compute_tf(self) -> List[Dict[str, int]]:
        """Tính Term Frequency cho mỗi document."""
        return [dict(Counter(doc)) for doc in self.tokenized_corpus]
    
    def _compute_df(self) -> Dict[str, int]:
        """
        Tính Document Frequency — số docs chứa mỗi term.
        Mỗi term chỉ đếm 1 lần per doc (dùng set).
        """
        df = {}
        for doc in self.tokenized_corpus:
            for word in set(doc):  # set() → unique per doc
                df[word] = df.get(word, 0) + 1
        return df
    
    def _compute_idf(self) -> Dict[str, float]:
        """
        Tính IDF từ DF.
        IDF(term) = log((N - df + 0.5) / (df + 0.5) + 1)
        """
        idf = {}
        for term, df_val in self.df.items():
            idf[term] = math.log(
                (self.corpus_size - df_val + 0.5) / (df_val + 0.5) + 1.0
            )
        return idf
    
    def _bm25_score_doc(self, query_tokens: List[str], doc_idx: int) -> float:
        """Tính BM25 score cho 1 document."""
        score = 0.0
        doc_len = self.doc_lens[doc_idx]
        doc_tf = self.tf[doc_idx]
        
        for q_term in query_tokens:
            if q_term not in self.idf:
                continue
            
            tf_val = doc_tf.get(q_term, 0)
            if tf_val == 0:
                continue
            
            idf_val = self.idf[q_term]
            numerator = tf_val * (self.k1 + 1.0)
            denominator = tf_val + self.k1 * (1.0 - self.b + self.b * doc_len / self.avgdl)
            
            score += idf_val * (numerator / denominator)
        
        return score
    
    # ============================================================
    # SEARCH METHODS
    # ============================================================
    
    def _bm25_search(self, query: str, top_n: int = 30) -> List[Tuple[int, float]]:
        """
        BM25 keyword search.
        
        Args:
            query: Câu truy vấn (string)
            top_n: Số kết quả trả về
            
        Returns:
            List[(doc_index, bm25_score)] sắp xếp giảm dần
        """
        query_tokens = query.lower().split()
        
        scores = np.array([
            self._bm25_score_doc(query_tokens, i)
            for i in range(self.corpus_size)
        ])
        
        top_n = min(top_n, self.corpus_size)
        top_indices = np.argsort(scores)[::-1][:top_n]
        
        return [(int(idx), float(scores[idx])) for idx in top_indices]
    
    def _semantic_search(self, query: str, top_n: int = 30) -> List[Tuple[int, float]]:
        """
        Semantic search bằng cosine similarity (dot product trên normalized vectors).
        
        Args:
            query: Câu truy vấn (string)
            top_n: Số kết quả trả về
            
        Returns:
            List[(doc_index, cosine_score)] sắp xếp giảm dần
        """
        query_embedding = self.model.encode_query(query)
        scores = np.dot(self.embeddings, query_embedding)
        
        top_n = min(top_n, self.corpus_size)
        top_indices = np.argsort(scores)[::-1][:top_n]
        
        return [(int(idx), float(scores[idx])) for idx in top_indices]
    
    def _rrf_combine(self, bm25_results: List[Tuple[int, float]], 
                     semantic_results: List[Tuple[int, float]], 
                     top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Reciprocal Rank Fusion — kết hợp 2 ranked lists.
        
        RRF_score(doc) = 1/(k + rank_bm25) + 1/(k + rank_semantic)
        
        Args:
            bm25_results: Kết quả BM25 [(doc_id, score), ...]
            semantic_results: Kết quả Semantic [(doc_id, score), ...]
            top_k: Số kết quả cuối cùng
            
        Returns:
            List[(doc_id, rrf_score)] sắp xếp giảm dần
        """
        rrf_scores = {}
        
        # BM25 ranks
        for rank, (doc_id, _) in enumerate(bm25_results, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (self.rrf_k + rank)
        
        # Semantic ranks
        for rank, (doc_id, _) in enumerate(semantic_results, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (self.rrf_k + rank)
        
        # Sort giảm dần
        sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_results[:top_k]
    
    # ============================================================
    # PUBLIC API
    # ============================================================
    
    def search(self, query: str, top_k: int = 10, top_n: int = 30) -> List[Dict]:
        """
        Hybrid search: BM25 + Semantic + RRF.
        
        Args:
            query: Câu truy vấn
            top_k: Số kết quả cuối cùng trả về
            top_n: Số kết quả mỗi method retrieve trước khi fusion (nên > top_k)
            
        Returns:
            List[Dict] với keys: doc_id, score, content, context, metadata
        """
        bm25_results = self._bm25_search(query, top_n=top_n)
        semantic_results = self._semantic_search(query, top_n=top_n)
        combined = self._rrf_combine(bm25_results, semantic_results, top_k=top_k)
        
        return [
            {
                "doc_id": doc_id,
                "score": score,
                "content": self.chunks[doc_id]["content"],
                "context": self.chunks[doc_id].get("context", ""),
                "metadata": self.chunks[doc_id].get("metadata", {}),
            }
            for doc_id, score in combined
        ]
