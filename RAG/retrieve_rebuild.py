"""
Custom Retriever - Built from scratch (không dùng rank_bm25, faiss)
Module test trước khi thay thế retriever.py cũ.

Author: KhacDiep
"""

import numpy as np
import math
from typing import List, Dict, Tuple, Optional
from collections import Counter


# ============================================================
# CUSTOM BM25
# ============================================================

class CustomBM25:
    """
    BM25 (Okapi BM25) implementation từ đầu.
    
    BM25 scoring formula:
        score(q, d) = Σ IDF(qi) * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * |d| / avgdl))
    
    Trong đó:
        - qi: query term thứ i
        - tf: term frequency của qi trong document d
        - |d|: độ dài document d (số tokens)
        - avgdl: trung bình độ dài tất cả documents
        - k1: tham số điều chỉnh term frequency saturation (default 1.5)
        - b: tham số điều chỉnh document length normalization (default 0.75)
        - IDF(qi) = log((N - df(qi) + 0.5) / (df(qi) + 0.5) + 1)
        - N: tổng số documents
        - df(qi): số documents chứa term qi
    
    Tham khảo:
        - Robertson, S. E., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        """
        Khởi tạo BM25.

        Args:
            k1: Tham số term frequency saturation. 
                k1 lớn → tf ảnh hưởng nhiều hơn.
                Typical range: [1.2, 2.0]
            b: Tham số document length normalization.
                b = 0 → không normalize theo length.
                b = 1 → normalize hoàn toàn theo length.
                Typical range: [0.5, 0.8]
        """
        self.k1 = k1
        self.b = b

        # Sẽ được set khi gọi fit()
        self.corpus_size: int = 0           # N: tổng số documents
        self.avgdl: float = 0.0             # Trung bình document length
        self.doc_lengths: np.ndarray = None  # Độ dài mỗi document
        self.df: Dict[str, int] = {}        # Document frequency cho mỗi term
        self.idf: Dict[str, float] = {}     # IDF score cho mỗi term
        self.tf: List[Dict[str, int]] = []  # Term frequency cho mỗi document
        self._fitted = False

    def fit(self, tokenized_corpus: List[List[str]]) -> None:
        """
        Fit BM25 trên corpus đã tokenize.

        Args:
            tokenized_corpus: List các document, mỗi document là list tokens.
                Ví dụ: [["xin", "chào", "thế", "giới"], ["máy", "tính", "là"]]
        
        Raises:
            ValueError: Nếu corpus rỗng
        """
        if not tokenized_corpus:
            raise ValueError("Corpus không được rỗng")

        self.corpus_size = len(tokenized_corpus)

        # === Bước 1: Tính document lengths và avgdl ===
        self.doc_lengths = np.array([len(doc) for doc in tokenized_corpus], dtype=np.float64)
        self.avgdl = np.mean(self.doc_lengths)

        # === Bước 2: Tính Term Frequency (TF) cho mỗi document ===
        self.tf = []
        for doc in tokenized_corpus:
            term_counts = Counter(doc)
            self.tf.append(dict(term_counts))

        # === Bước 3: Tính Document Frequency (DF) ===
        # DF(term) = số documents chứa term đó
        self.df = {}
        for doc in tokenized_corpus:
            unique_terms = set(doc)  # Mỗi term chỉ đếm 1 lần per document
            for term in unique_terms:
                self.df[term] = self.df.get(term, 0) + 1

        # === Bước 4: Tính IDF cho mỗi term ===
        # IDF(qi) = log((N - df + 0.5) / (df + 0.5) + 1)
        self.idf = {}
        for term, df_val in self.df.items():
            self.idf[term] = math.log(
                (self.corpus_size - df_val + 0.5) / (df_val + 0.5) + 1.0
            )

        self._fitted = True
        print(f"✅ CustomBM25 fitted: {self.corpus_size} docs, "
              f"vocab size = {len(self.df)}, avgdl = {self.avgdl:.1f}")

    def _score_document(self, query_tokens: List[str], doc_idx: int) -> float:
        """
        Tính BM25 score cho 1 document với query.

        Args:
            query_tokens: List các query tokens
            doc_idx: Index của document trong corpus

        Returns:
            float: BM25 score
        """
        score = 0.0
        doc_len = self.doc_lengths[doc_idx]
        doc_tf = self.tf[doc_idx]

        for q_term in query_tokens:
            if q_term not in self.df:
                # Term không có trong corpus → bỏ qua
                continue

            # Term frequency của q_term trong document
            tf_val = doc_tf.get(q_term, 0)
            if tf_val == 0:
                continue

            # IDF
            idf_val = self.idf[q_term]

            # BM25 formula
            # numerator = tf * (k1 + 1)
            # denominator = tf + k1 * (1 - b + b * doc_len / avgdl)
            numerator = tf_val * (self.k1 + 1.0)
            denominator = tf_val + self.k1 * (1.0 - self.b + self.b * doc_len / self.avgdl)

            score += idf_val * (numerator / denominator)

        return score

    def get_scores(self, query_tokens: List[str]) -> np.ndarray:
        """
        Tính BM25 scores cho toàn bộ corpus.

        Args:
            query_tokens: List các query tokens

        Returns:
            np.ndarray: Array scores shape (corpus_size,)
        """
        if not self._fitted:
            raise RuntimeError("Chưa fit. Gọi fit() trước")

        scores = np.array([
            self._score_document(query_tokens, i)
            for i in range(self.corpus_size)
        ])

        return scores

    def search(self, query_tokens: List[str], top_k: int = 10) -> List[Tuple[int, int, float]]:
        """
        Tìm kiếm top_k documents phù hợp nhất với query.

        Args:
            query_tokens: List các query tokens
            top_k: Số kết quả trả về

        Returns:
            List of (rank, doc_index, score) tuples, sắp xếp theo score giảm dần
        """
        scores = self.get_scores(query_tokens)

        # Lấy top_k indices, sắp xếp theo score giảm dần
        top_k = min(top_k, self.corpus_size)
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = [
            (rank, int(idx), float(scores[idx]))
            for rank, idx in enumerate(top_indices)
        ]

        return results

    def get_stats(self) -> Dict:
        """Trả về thống kê của BM25 model."""
        if not self._fitted:
            return {"fitted": False}

        return {
            "fitted": True,
            "corpus_size": self.corpus_size,
            "vocab_size": len(self.df),
            "avgdl": round(self.avgdl, 2),
            "k1": self.k1,
            "b": self.b,
            "top_10_common_terms": sorted(
                self.df.items(), key=lambda x: x[1], reverse=True
            )[:10]
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TEST CUSTOM BM25")
    print("=" * 60)

    # === Test với sample data ===
    sample_corpus = [
        ["máy", "tính", "là", "thiết", "bị", "xử", "lí", "thông", "tin"],
        ["mạng", "máy", "tính", "kết", "nối", "các", "thiết", "bị", "với", "nhau"],
        ["lập", "trình", "python", "là", "ngôn", "ngữ", "lập", "trình", "bậc", "cao"],
        ["bảo", "mật", "thông", "tin", "rất", "quan", "trọng", "trong", "tin", "học"],
        ["internet", "thay", "đổi", "xã", "hội", "loài", "người"],
    ]

    bm25 = CustomBM25(k1=1.5, b=0.75)
    bm25.fit(sample_corpus)

    # Test search
    query = ["máy", "tính", "thông", "tin"]
    results = bm25.search(query, top_k=5)

    print(f"\n🔍 Query: {query}")
    print(f"{'Rank':<6}{'Doc Index':<12}{'Score':<10}{'Document'}")
    print("-" * 60)
    for rank, idx, score in results:
        doc_text = " ".join(sample_corpus[idx][:8]) + "..."
        print(f"{rank:<6}{idx:<12}{score:<10.4f}{doc_text}")

    print(f"\n📊 Stats: {bm25.get_stats()}")

    # === Test với real data ===
    print("\n" + "=" * 60)
    print("TEST VỚI REAL CHUNKS DATA")
    print("=" * 60)

    import json
    import os

    chunks_path = os.path.join(os.path.dirname(__file__), "..", "data", "rag_chunks.json")

    if os.path.exists(chunks_path):
        with open(chunks_path, "r", encoding="utf-8") as f:
            chunks_data = json.load(f)

        print(f"📦 Loaded {len(chunks_data)} chunks")

        # Tokenize corpus (đơn giản: split by whitespace + lowercase)
        corpus_texts = [chunk["content"] for chunk in chunks_data]
        tokenized = [text.lower().split() for text in corpus_texts]

        # Fit BM25
        bm25_real = CustomBM25(k1=1.5, b=0.75)
        bm25_real.fit(tokenized)

        # Test queries
        test_queries = [
            "mã hóa đối xứng bảo mật",
            "lập trình python",
            "mạng máy tính internet",
        ]

        for q in test_queries:
            q_tokens = q.lower().split()
            results = bm25_real.search(q_tokens, top_k=3)

            print(f"\n🔍 Query: '{q}'")
            for rank, idx, score in results:
                content_preview = chunks_data[idx]["content"][:80] + "..."
                metadata = chunks_data[idx].get("metadata", {})
                print(f"  [{rank}] score={score:.4f} | {metadata} | {content_preview}")
    else:
        print(f"⚠️  Không tìm thấy file: {chunks_path}")

    print("\n✅ Test hoàn tất!")
