
import argparse
import logging
import sys

# Thiết lập logging cho module chạy này
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("eval_runner")

from src.evaluation.testset_generator import TestsetGenerator
from src.evaluation.data_collector import DataCollector
from src.evaluation.ragas_eval import RAGASEvaluator
from src.evaluation.report import EvalReporter

# Gọi import các component xử lý Retrieve/Rerank nếu có 
# (Dựa trên runtime pipeline của bạn, giả sử cấu trúc như sau)
# Nếu runtime RAG pipeline bị lỗi import, bạn cần sửa đường dẫn ở đây nhé.
try:
    from src.rag.retrieve_rebuild import CustomSearch
    from src.rag.reranker import Reranker
except ImportError as e:
    logger.warning(f"Could not import rag elements: {e}. Please check if running '--step collect'!")
    CustomSearch = None
    Reranker = None


def main():
    parser = argparse.ArgumentParser(description="Chạy bộ đánh giá hệ thống RAG (Ragas Evaluation).")
    parser.add_argument(
        "--step",
        choices=["testset", "collect", "evaluate", "report", "all"],
        default="all",
        help="Bước cần thực thi theo trình tự: testset -> collect -> evaluate -> report",
    )
    parser.add_argument(
        "--num_samples",
        type=int,
        default=250,
        help="Số lượng mẫu sẽ tạo khi sinh Testset (Mặc định 50).",
    )
    
    args = parser.parse_args()
    logger.info(f"Starting Eval Runner, mode: {args.step.upper()}")

    # 1. Sinh Testset
    if args.step in ["all", "testset"]:
        logger.info("\n--- STEP 1: TESTSET GENERATION ---")
        gen = TestsetGenerator()
        gen.generate(num_samples=args.num_samples)
    
    # 2. Thu thập dữ liệu
    if args.step in ["all", "collect"]:
        logger.info("\n--- STEP 2: DATA COLLECTION ---")
        if CustomSearch is None or Reranker is None:
            logger.error("Failed to initialize CustomSearch/Reranker. Stopping collect process.")
            sys.exit(1)
            
        from pathlib import Path
        from src.config.config import settings
        chunks_path = str(Path(settings.DATA_DIR) / settings.CHUNKS_FILE)
        embeddings_path = str(Path(settings.DATA_DIR) / settings.EMBEDDINGS_FILE)
        
        # Khởi tạo instance cho Retriever và Reranker
        retriever = CustomSearch(chunks_path=chunks_path, embeddings_path=embeddings_path)
        reranker = Reranker()
        
        gen = TestsetGenerator()
        try:
            testset = gen.load()
        except FileNotFoundError:
            logger.error("Testset file not found. Please run `--step testset` first.")
            sys.exit(1)
            
        collector = DataCollector(retriever=retriever, reranker=reranker)
        collector.collect(testset)
        
    # 3. Đánh giá RAGAS (Compute metrics)
    if args.step in ["all", "evaluate"]:
        logger.info("\n--- STEP 3: RAGAS METRICS EVALUATION ---")
        collector = DataCollector(retriever=None, reranker=None)
        
        try:
            results = collector.load()
        except FileNotFoundError:
            logger.error("Results file not found. Please run `--step collect` first.")
            sys.exit(1)
            
        evaluator = RAGASEvaluator()
        evaluator.evaluate(results)
        
    # 4. Xuất báo cáo
    if args.step in ["all", "report"]:
        logger.info("\n--- STEP 4: REPORT GENERATION ---")
        reporter = EvalReporter()
        try:
            reporter.generate_report()
            reporter.print_summary()
        except FileNotFoundError:
            logger.error("Metrics file not found. Please run `--step evaluate` first.")
            sys.exit(1)
            
    logger.info("\n=== Evaluation pipeline completed successfully! ===")


if __name__ == "__main__":
    main()
