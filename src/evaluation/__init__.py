"""
Evaluation Package — Đánh giá RAG pipeline bằng RAGAS framework.

Modules:
    - testset_generator: Sinh synthetic test set từ chunks SGK
    - data_collector: Chạy pipeline thu thập (question, contexts, answer, ground_truth)
    - ragas_eval: Chạy RAGAS metrics (Faithfulness, Relevancy, Precision, Recall)
    - report: Xuất báo cáo + biểu đồ
    - run_eval: CLI chạy end-to-end
"""

from src.evaluation.testset_generator import TestsetGenerator
from src.evaluation.data_collector import DataCollector
from src.evaluation.ragas_eval import RAGASEvaluator
from src.evaluation.report import EvalReporter

__all__ = [
    "TestsetGenerator",
    "DataCollector", 
    "RAGASEvaluator",
    "EvalReporter",
]
