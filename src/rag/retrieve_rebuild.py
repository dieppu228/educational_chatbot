import json
import logging
import numpy as np
import math
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import Counter

from src.rag.embedding import EmbeddingModel

try:
    from underthesea import word_tokenize as vn_tokenize
    _HAS_UNDERTHESEA = True
except ImportError:
    _HAS_UNDERTHESEA = False

logger = logging.getLogger("chatbot")


class CustomSearch:
    
    def __init__(self, chunks_path: str, embeddings_path: str, k1: float = 1.2, b: float = 0.75, rrf_k: int = 60):
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
        logger.info(f"Tokenizing {self.corpus_size} docs with {'underthesea' if _HAS_UNDERTHESEA else 'split()'}...")
        self.tokenized_corpus = [self._tokenize(chunk["content"]) for chunk in self.chunks]
        self.doc_lens = np.array([len(doc) for doc in self.tokenized_corpus], dtype=np.float64)
        self.avgdl = np.mean(self.doc_lens)
        
        self.tf = self._compute_tf()
        self.df = self._compute_df()
        self.idf = self._compute_idf()
        
        # === Embedding model (lazy load) ===
        self._model = None
        
        print(f"CustomSearch initialized: {self.corpus_size} docs, "
              f"vocab={len(self.df)}, avgdl={self.avgdl:.1f}")
    
    @property
    def model(self):
        if self._model is None:
            self._model = EmbeddingModel()
        return self._model
    
    # ============================================================
    # TOKENIZER
    # ============================================================

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        if _HAS_UNDERTHESEA:
            tokenized = vn_tokenize(text.lower(), format="text")
            return tokenized.split()
        return text.lower().split()

    # ============================================================
    # BM25 INTERNALS
    # ============================================================
    
    def _compute_tf(self) -> List[Dict[str, int]]:
        return [dict(Counter(doc)) for doc in self.tokenized_corpus]
    
    def _compute_df(self) -> Dict[str, int]:
        df = {}
        for doc in self.tokenized_corpus:
            for word in set(doc):  # set() → unique per doc
                df[word] = df.get(word, 0) + 1
        return df
    
    def _compute_idf(self) -> Dict[str, float]:
        idf = {}
        for term, df_val in self.df.items():
            idf[term] = math.log(
                (self.corpus_size - df_val + 0.5) / (df_val + 0.5) + 1.0
            )
        return idf
    
    def _bm25_score_doc(self, query_tokens: List[str], doc_idx: int) -> float:
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
        query_tokens = self._tokenize(query)
        
        scores = np.array([
            self._bm25_score_doc(query_tokens, i)
            for i in range(self.corpus_size)
        ])
        
        top_n = min(top_n, self.corpus_size)
        top_indices = np.argsort(scores)[::-1][:top_n]
        
        return [(int(idx), float(scores[idx])) for idx in top_indices]
    
    def _semantic_search(self, query: str, top_n: int = 30) -> List[Tuple[int, float]]:
        query_embedding = self.model.encode_query(query)
        scores = np.dot(self.embeddings, query_embedding)
        
        top_n = min(top_n, self.corpus_size)
        top_indices = np.argsort(scores)[::-1][:top_n]
        
        return [(int(idx), float(scores[idx])) for idx in top_indices]
    
    def _rrf_combine(self, bm25_results: List[Tuple[int, float]], 
                     semantic_results: List[Tuple[int, float]], 
                     top_k: int = 10) -> List[Tuple[int, float]]:
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
        bm25_results = self._bm25_search(query, top_n=top_n)
        try:
            semantic_results = self._semantic_search(query, top_n=top_n)
        except Exception as e:
            logger.warning(f"Semantic search failed, falling back to BM25 only: {e}")
            semantic_results = []
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

    def search_by_metadata(
        self,
        grade: str = None,
        topic_name: str = None,
        lesson_name: str = None,
        chunk_types: List[str] = None,
        max_per_lesson: int = 2,
    ) -> List[Dict]:
        results = []
        lesson_count = {}  # track số chunk per lesson

        for doc_id, chunk in enumerate(self.chunks):
            m = chunk.get("metadata", {})

            # Filter logic
            if grade and m.get("grade") != grade:
                continue
            if topic_name and topic_name.lower() not in m.get("topic_name", "").lower():
                continue
            if lesson_name and lesson_name.lower() not in m.get("lesson_name", "").lower():
                continue
            if chunk_types and m.get("type") not in chunk_types:
                continue

            # Giới hạn per lesson
            lesson_key = m.get("lesson_name", "")
            lesson_count[lesson_key] = lesson_count.get(lesson_key, 0) + 1
            if lesson_count[lesson_key] > max_per_lesson:
                continue

            results.append({
                "doc_id": doc_id,
                "score": 1.0,  # metadata match = score cố định
                "content": chunk["content"],
                "context": chunk.get("context", ""),
                "metadata": m,
            })

        return results

    def search_scoped(
        self,
        query: str,
        doc_indices: List[int],
        top_k: int = 10,
        top_n: int = 30,
    ) -> List[Dict]:
        if not doc_indices:
            return []

        doc_indices = [
            int(i)
            for i in doc_indices
            if 0 <= int(i) < self.corpus_size and 0 <= int(i) < self.embeddings.shape[0]
        ]
        if not doc_indices:
            return []

        top_n = min(top_n, len(doc_indices))

        # === BM25 scoped ===
        query_tokens = self._tokenize(query)
        bm25_scored = []
        for i in doc_indices:
            score = self._bm25_score_doc(query_tokens, i)
            bm25_scored.append((i, score))
        bm25_scored.sort(key=lambda x: x[1], reverse=True)
        bm25_results = bm25_scored[:top_n]

        # === Semantic scoped ===
        try:
            query_embedding = self.model.encode_query(query)
            # Chỉ tính cosine trên subset
            subset_embeddings = self.embeddings[doc_indices]
            scores = np.dot(subset_embeddings, query_embedding)
            # Map lại về global indices
            local_top = np.argsort(scores)[::-1][:top_n]
            semantic_results = [
                (doc_indices[li], float(scores[li])) for li in local_top
            ]
        except Exception as e:
            logger.warning(f"Scoped semantic search failed, falling back to BM25 only: {e}")
            semantic_results = []

        # === RRF ===
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
