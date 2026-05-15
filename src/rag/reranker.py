import numpy as np
from typing import List, Dict, Tuple, Optional
from sentence_transformers import CrossEncoder

import torch
from src.utils.trace_decorator import trace_node

class Reranker:
    
    def __init__(self, model_name: str = "AITeamVN/Vietnamese_Reranker", device: Optional[str] = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._model = None  # Lazy load
        self._load_failed = False
    
    def _load_model(self):
        if self._load_failed:
            raise RuntimeError(f"Reranker model unavailable: {self.model_name}")
        if self._model is None:
            try:
                self._model = CrossEncoder(
                    self.model_name,
                    device=self.device,
                    trust_remote_code=True
                )
            except Exception:
                self._load_failed = True
                raise
    
    @trace_node("Reranker.rerank")
    def rerank(self, query: str, results: List[Dict], top_n: int = 10) -> List[Dict]:
        if not results:
            return []

        try:
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
        except Exception:
            return results[:top_n]
    
    @trace_node("Reranker.rerank_async")
    async def rerank_async(self, query: str, results: List[Dict], top_n: int = 10) -> List[Dict]:
        import asyncio
        # Cross-encoder scoring là CPU/GPU bound, chạy trong thread pool để không chặn event loop
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.rerank, query, results, top_n)
    
    def filter_context(self, results: List[Dict], min_len: int = 50, 
                       min_score: float = 0.0, top_n: Optional[int] = None) -> List[Dict]:
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
