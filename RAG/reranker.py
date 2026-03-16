from FlagEmbedding import FlagReranker  
import google.generativeai as genai
from RAG.retriever import Retriever      
from LLM.format_context import format_context  


class RerankerModule:
    def __init__(self, model_name="BAAI/bge-reranker-v2-m3", use_fp16=True, trust_remote_code=True):
        self.reranker = FlagReranker(model_name_or_path=model_name, use_fp16=use_fp16, trust_remote_code=trust_remote_code)

    def rerank(self, query, results, top_n=10):
        pairs = [[query, item["content"]] for item in results]
        scores = self.reranker.compute_score(pairs)
        for i, score in enumerate(scores):
            results[i]["rerank_score"] = float(score)
        results_sorted = sorted(results, key=lambda x: x["rerank_score"], reverse=True)
        return results_sorted[:top_n]

    def filter_context(self, results, min_len=50, min_score=0.0, domain_keywords=None, top_n=None):
        if domain_keywords is None:
            domain_keywords = []
        filtered = []
        texts_seen = set()
        for r in results:
            text = r["content"].strip()
            if len(text) < min_len or text in texts_seen or r.get("rerank_score", 1) < min_score:
                continue
            # Only filter by keywords if keywords are provided
            if domain_keywords and not any(keyword in text.lower() for keyword in domain_keywords):
                continue
            texts_seen.add(text)
            filtered.append(r)
        if top_n:
            filtered = filtered[:top_n]
        return filtered
