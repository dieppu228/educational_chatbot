import numpy as np
from typing import List, Dict, Tuple, Optional
from sentence_transformers import CrossEncoder


class Reranker:
    """
    Reranker dùng Cross-Encoder model AITeamVN/Vietnamese_Reranker.
    
    Cross-encoder nhận (query, document) pair → score relevance.
    Chính xác hơn bi-encoder nhưng chậm hơn → chỉ dùng rerank top-N.
    """
    
    def __init__(self, model_name: str = "AITeamVN/Vietnamese_Reranker", device: str = "cpu"):
        """
        Args:
            model_name: Tên model cross-encoder trên HuggingFace
            device: "cpu" hoặc "cuda"
        """
        self.model_name = model_name
        self.device = device
        self._model = None  # Lazy load
    
    def _load_model(self):
        """Load model lần đầu khi cần."""
        if self._model is None:
            print(f"🔄 Loading reranker: {self.model_name}...")
            self._model = CrossEncoder(
                self.model_name,
                device=self.device,
                trust_remote_code=True
            )
            print(f"✅ Reranker loaded on {self.device}")
    
    def rerank(self, query: str, results: List[Dict], top_n: int = 10) -> List[Dict]:
        """
        Rerank danh sách kết quả search.
        
        Args:
            query: Câu truy vấn gốc
            results: List[Dict] từ CustomSearch.search() — cần có key "content"
            top_n: Số kết quả trả về sau rerank
            
        Returns:
            List[Dict] đã sắp xếp theo rerank_score, thêm key "rerank_score"
        """
        if not results:
            return []
        
        self._load_model()
        
        # Tạo (query, doc) pairs
        pairs = [[query, r["content"]] for r in results]
        
        # Cross-encoder scoring
        scores = self._model.predict(pairs)
        
        # Gắn score vào results
        for i, score in enumerate(scores):
            results[i]["rerank_score"] = float(score)
        
        # Sort giảm dần theo rerank_score
        results_sorted = sorted(results, key=lambda x: x["rerank_score"], reverse=True)
        
        return results_sorted[:top_n]
    
    def filter_context(self, results: List[Dict], min_len: int = 50, 
                       min_score: float = 0.0, top_n: Optional[int] = None) -> List[Dict]:
        """
        Lọc kết quả: bỏ trùng lặp, quá ngắn, score thấp.
        
        Args:
            results: Kết quả sau rerank
            min_len: Độ dài tối thiểu content (chars)
            min_score: Rerank score tối thiểu
            top_n: Giới hạn số kết quả
            
        Returns:
            List[Dict] đã lọc
        """
        filtered = []
        seen = set()
        
        for r in results:
            text = r["content"].strip()
            
            # Bỏ quá ngắn
            if len(text) < min_len:
                continue
            
            # Bỏ trùng lặp
            if text in seen:
                continue
            
            # Bỏ score thấp
            if r.get("rerank_score", 1.0) < min_score:
                continue
            
            seen.add(text)
            filtered.append(r)
        
        if top_n:
            filtered = filtered[:top_n]
        
        return filtered


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    # Fake results để test
    fake_results = [
        {"content": "Mạng máy tính là một hệ thống các thiết bị số được kết nối với nhau.", "context": "test", "metadata": {}, "score": 0.9, "doc_id": 0},
        {"content": "Hệ điều hành quản lý tài nguyên phần cứng và phần mềm.", "context": "test", "metadata": {}, "score": 0.8, "doc_id": 1},
        {"content": "Python là ngôn ngữ lập trình bậc cao.", "context": "test", "metadata": {}, "score": 0.7, "doc_id": 2},
        {"content": "Internet là mạng diện rộng toàn cầu kết nối hàng tỷ thiết bị.", "context": "test", "metadata": {}, "score": 0.6, "doc_id": 3},
        {"content": "CSS dùng để tạo kiểu cho trang web.", "context": "test", "metadata": {}, "score": 0.5, "doc_id": 4},
    ]
    
    reranker = Reranker()
    
    query = "mạng máy tính là gì"
    print(f"🔍 Query: '{query}'")
    print(f"📥 Input: {len(fake_results)} docs")
    
    reranked = reranker.rerank(query, fake_results, top_n=3)
    
    print(f"\n📤 Reranked top 3:")
    for i, r in enumerate(reranked):
        print(f"  [{i+1}] score={r['rerank_score']:.4f} | {r['content'][:80]}...")
    
    print("\n✅ Reranker test done!")
