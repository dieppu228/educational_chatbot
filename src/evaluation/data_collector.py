
import json
import os
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional

from google import genai
from google.genai.types import GenerateContentConfig

from src.config.config import settings

logger = logging.getLogger("evaluation.collector")


# Prompt để LLM trả lời câu hỏi dựa trên context (giống runtime pipeline)
ANSWER_PROMPT = """Bạn là trợ lý học tập Tin học THPT. Dựa vào tài liệu được cung cấp, 
hãy trả lời câu hỏi sau một cách chính xác, rõ ràng.

Tài liệu tham khảo:
{context}

Câu hỏi: {question}

Hãy trả lời dựa trên tài liệu. Nếu tài liệu không chứa đủ thông tin, nói rõ."""


class DataCollector:
    
    def __init__(
        self,
        retriever,
        reranker,
        api_key: Optional[str] = None,
        llm_model: Optional[str] = None,
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.api_key = api_key or settings.GENAI_API_KEY or os.getenv("GENAI_API_KEY", "")
        self.llm_model = llm_model or settings.EVAL_LLM_MODEL
        
        if not self.api_key:
            raise ValueError("GENAI_API_KEY chưa được set")
        
        self.client = genai.Client(api_key=self.api_key)
        self.output_dir = Path(settings.EVAL_OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
    
    def _retrieve_and_rerank(self, query: str) -> List[str]:
        # Hybrid search
        results = self.retriever.search(
            query, 
            top_k=settings.RETRIEVER_TOP_K,
        )
        
        if not results:
            return []
        
        # Rerank
        reranked = self.reranker.rerank(
            query, 
            results, 
            top_n=settings.RERANKER_TOP_N,
        )
        
        # Extract context strings
        contexts = [r["content"] for r in reranked if r.get("content")]
        return contexts
    
    def _generate_answer(self, question: str, contexts: List[str]) -> str:
        context_text = "\n\n---\n\n".join(contexts)
        prompt = ANSWER_PROMPT.format(context=context_text, question=question)
        
        try:
            response = self.client.models.generate_content(
                model=f"models/{self.llm_model}",
                contents=prompt,
                config=GenerateContentConfig(temperature=0.1),
            )
            
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "text") and part.text:
                        return part.text.strip()
            return ""
        except Exception as e:
            logger.error(f"LLM generate error: {e}")
            return ""
    
    def collect(self, testset: List[Dict]) -> List[Dict]:
        logger.info(f"Collecting data for {len(testset)} samples...")
        
        results = []
        total = len(testset)
        
        for i, sample in enumerate(testset):
            question = sample["user_input"]
            ground_truth = sample.get("reference", "")
            
            t0 = time.time()
            
            # Step 1: Retrieve + Rerank
            contexts = self._retrieve_and_rerank(question)
            t_retrieve = time.time() - t0
            
            # Step 2: Generate answer
            t1 = time.time()
            answer = self._generate_answer(question, contexts)
            t_generate = time.time() - t1
            
            result = {
                "user_input": question,
                "retrieved_contexts": contexts,
                "response": answer,
                "reference": ground_truth,
                "timing": {
                    "retrieve_s": round(t_retrieve, 3),
                    "generate_s": round(t_generate, 3),
                    "total_s": round(time.time() - t0, 3),
                }
            }
            results.append(result)
            
            logger.info(
                f"  [{i+1}/{total}] Q: '{question[:50]}...' "
                f"| ctx={len(contexts)} | {result['timing']['total_s']:.1f}s"
            )
            
            # Rate limiting — tránh bị throttle bởi API
            time.sleep(1.0)
        
        # Save results
        output_path = self.output_dir / "eval_results.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {len(results)} results to {output_path}")
        return results
    
    def load(self) -> List[Dict]:
        path = self.output_dir / "eval_results.json"
        if not path.exists():
            raise FileNotFoundError(
                f"Chưa có kết quả tại {path}. Chạy collect() trước."
            )
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        logger.info(f"Loaded {len(data)} results from {path}")
        return data
