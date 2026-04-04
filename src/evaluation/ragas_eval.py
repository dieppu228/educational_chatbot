"""
RAGAS Evaluator — Tính toán các metrics đánh giá chất lượng RAG.

Input:  eval_results.json (từ DataCollector)
Output: eval_metrics.json (điểm số của từng sample)
Metrics: Answer Relevancy, Faithfulness, Context Precision, Context Recall.

Tương thích: ragas >= 0.4.x, langchain-google-genai >= 4.x
"""

import os
import json
import logging
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional

# Ragas 0.4.x imports
from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics import (
    Faithfulness,
    ResponseRelevancy,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings as LCHuggingFaceEmbeddings

from src.config.config import settings

logger = logging.getLogger("evaluation.ragas")


class RAGASEvaluator:
    """
    Class tính điểm hệ thống RAG bằng RAGAS.
    """
    
    def __init__(
        self,
        llm_model: Optional[str] = None,
        embedding_model: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Khởi tạo RAGAS Evaluator với mô hình LLM và Embedding.
        """
        self.llm_model = llm_model or settings.EVAL_LLM_MODEL
        self.embedding_model = embedding_model or settings.EVAL_EMBEDDING_MODEL
        self.api_key = api_key or settings.GENAI_API_KEY or os.getenv("GENAI_API_KEY", "")
        
        if not self.api_key:
            raise ValueError("GENAI_API_KEY chưa được thiết lập.")
            
        self.output_dir = Path(settings.EVAL_OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        
        # Init metrics list — ragas 0.4.x dùng class-based metrics
        self.metrics = [
            Faithfulness(),
            ResponseRelevancy(),
            LLMContextPrecisionWithReference(),
            LLMContextRecall(),
        ]

    def _init_ragas_models(self):
        """Khởi tạo wrappers cho Language models dành cho RAGAS."""
        logger.info(f"Initializing models for RAGAS: LLM={self.llm_model}, Embeddings={self.embedding_model}")
        
        llm = ChatGoogleGenerativeAI(
            model=self.llm_model,
            google_api_key=self.api_key,
            temperature=0,  # Nên fix temperature=0 khi evaluate
        )
        ragas_llm = LangchainLLMWrapper(llm)

        # Dùng langchain HuggingFaceEmbeddings + LangchainEmbeddingsWrapper
        # để đảm bảo có cả embed_query (cho ResponseRelevancy) và embed_text (cho ragas)
        lc_embeddings = LCHuggingFaceEmbeddings(
            model_name="dangvantuan/vietnamese-document-embedding",
            model_kwargs={"trust_remote_code": True},
        )
        ragas_embeddings = LangchainEmbeddingsWrapper(lc_embeddings)
        
        return ragas_llm, ragas_embeddings

    def evaluate(self, dataset: List[Dict]) -> List[Dict]:
        """
        Chạy đánh giá các metrics trên tập dữ liệu đã thu thập.
        
        Args:
            dataset: List[Dict] (có keys: user_input, response, retrieved_contexts, reference).
                     Nếu file cũ dùng các key khác như question, answer, contexts, ground_truths,
                     hàm này sẽ tự động ánh xạ lại cho phù hợp với RAGAS API.
        
        Returns:
            List[Dict]: dữ liệu đánh giá chi tiết với các cột điểm mới.
        """
        logger.info(f"Starting RAGAS evaluation for {len(dataset)} samples...")
        
        if not dataset:
            logger.warning("Dataset is empty, skipping evaluation.")
            return []
            
        # 1. Build EvaluationDataset (ragas 0.4.x format)
        samples = []
        for row in dataset:
            samples.append(SingleTurnSample(
                user_input=row.get("user_input", row.get("question", "")),
                response=row.get("response", row.get("answer", "")),
                retrieved_contexts=row.get("retrieved_contexts", row.get("contexts", [])),
                reference=row.get("reference", row.get("ground_truth", "")),
            ))
        eval_dataset = EvaluationDataset(samples=samples)
        
        # 2. Setup models
        ragas_llm, ragas_embeddings = self._init_ragas_models()
        
        # Gán thủ công llm/embeddings cho từng metric (tránh lỗi 'LLM is not set')
        for metric in self.metrics:
            if hasattr(metric, "llm"):
                metric.llm = ragas_llm
            if hasattr(metric, "embeddings"):
                metric.embeddings = ragas_embeddings
        
        # 3. Apply RunConfig cho Rate Limiting
        from ragas.run_config import RunConfig
        
        # Free Tier Gemini cho phép rpm thấp, chúng ta cần bóp concurrency lại
        run_config = RunConfig(
            max_workers=2,         # Chạy tối đa 2 tác vụ cùng lúc
            max_retries=10,        # Thử lại tối đa 10 lần nếu gặp lỗi (ví dụ 429)
            max_wait=30            # Chờ tối đa 30s giữa các lần retry
        )
        
        # 4. Evaluate
        try:
            result = evaluate(
                dataset=eval_dataset,
                metrics=self.metrics,
                llm=ragas_llm,
                embeddings=ragas_embeddings,
                run_config=run_config,
            )
        except Exception as e:
            logger.error(f"Error running RAGAS evaluate: {e}")
            raise

        # 4. Save results
        eval_df = result.to_pandas()
        
        # Kết hợp timing từ bộ ban đầu nếu có (để báo cáo có đầy đủ insight)
        if "timing" in dataset[0]:
            try:
                timings = [row["timing"] for row in dataset]
                eval_df["timing"] = timings
            except KeyError:
                pass

        results_list = eval_df.to_dict(orient="records")
        output_path = self.output_dir / "eval_metrics.json"
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_list, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Saved results ({len(results_list)} samples) to {output_path}")
        return results_list
        
    def load(self) -> List[Dict]:
        """Tải file đã được evaluate."""
        path = self.output_dir / "eval_metrics.json"
        if not path.exists():
            raise FileNotFoundError(f"Chưa có kết quả tại {path}. Hãy chạy evaluate().")
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        logger.info(f"Loaded {len(data)} evaluation results from {path}")
        return data
