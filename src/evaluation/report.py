"""
Evaluation Reporter — Trích xuất và định dạng kết quả đánh giá RAGAS.

Đọc file eval_metrics.json và sinh ra các báo cáo dạng:
- Bảng Markdown (eval_report.md)
"""

import json
import logging
from pathlib import Path
from typing import List, Dict

import pandas as pd

from src.config.config import settings

logger = logging.getLogger("evaluation.report")


class EvalReporter:
    """
    Class sinh báo cáo từ kết quả RAGAS.
    """
    def __init__(self, metrics_file: str = "eval_metrics.json"):
        self.output_dir = Path(settings.EVAL_OUTPUT_DIR)
        self.metrics_path = self.output_dir / metrics_file
        
    def _load_metrics(self) -> List[Dict]:
        """Load data JSON từ file."""
        if not self.metrics_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy {self.metrics_path}. "
                "Cần chạy RAGASEvaluator trước."
            )
        with open(self.metrics_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_report(self) -> str:
        """
        Tạo báo cáo dạng Markdown.
        
        Returns:
            str: Nội dung markdown của báo cáo
        """
        data = self._load_metrics()
        df = pd.DataFrame(data)
        
        logger.info(f"📊 Đang sinh báo cáo cho {len(df)} mẫu thử...")

        # Các cột metric tiêu biểu của RAGAS (hỗ trợ cả 0.1.x và 0.4.x)
        target_metrics = [
            "faithfulness", 
            "answer_relevancy", "response_relevancy",
            "context_precision", "llm_context_precision_with_reference",
            "context_recall", "llm_context_recall",
        ]
        
        # Chỉ giữ lại các metric thực tế có trong dataframe
        available_metrics = [m for m in target_metrics if m in df.columns]

        # 1. Bảng số liệu tổng quan (Mean)
        summary = {}
        for metric in available_metrics:
            summary[metric] = df[metric].mean()
            
        # Thống kê thời gian (nếu có cột timing)
        avg_retrieve = 0.0
        avg_generate = 0.0
        avg_total = 0.0
        if "timing" in df.columns:
            timings = df["timing"].dropna().tolist()
            if timings:
                avg_retrieve = sum(t.get("retrieve_s", 0) for t in timings) / len(timings)
                avg_generate = sum(t.get("generate_s", 0) for t in timings) / len(timings)
                avg_total = sum(t.get("total_s", 0) for t in timings) / len(timings)

        # 2. Sinh Markdown content
        md_lines = [
            "# Báo Cáo Đánh Giá RAG (Post-Eval)",
            "",
            f"**Số lượng mẫu (samples):** {len(df)}",
            "",
            "## Tổng Quan Điểm Số (Average)",
            "| Chỉ số (Metric) | Điểm trung bình |",
            "| :--- | :---: |"
        ]
        
        for metric in available_metrics:
            md_lines.append(f"| {metric.replace('_', ' ').title()} | **{summary[metric]:.4f}** |")

        if "timing" in df.columns:
            md_lines.extend([
                "",
                "## Thống Kê Thời Gian Phản Hồi",
                "| Thành phần | Thời gian trung bình (Giây) |",
                "| :--- | :---: |",
                f"| Retriever | {avg_retrieve:.3f} s |",
                f"| Generator (LLM) | {avg_generate:.3f} s |",
                f"| **Tổng thời gian pipeline** | **{avg_total:.3f} s** |"
            ])

        # Phân tích sơ bộ
        md_lines.extend([
            "",
            "## Phân Tích Cơ Bản",
            "1. **Faithfulness** (Độ trung thực): Điểm cao có nghĩa câu trả lời không bịa thông tin ngoài ngữ cảnh (hallucinations).",
            "2. **Answer Relevancy** (Độ phù hợp): Câu trả lời đi thẳng vào trọng tâm câu hỏi.",
            "3. **Context Precision** (Độ chính xác ngữ cảnh): Các chunk giá trị nhất được xếp ở ưu tiên cao.",
            "4. **Context Recall** (Độ bao phủ ngữ cảnh): Retriever đã tìm được bao nhiêu phần trăm thông tin cần thiết so với reference."
        ])

        md_content = "\n".join(md_lines)
        
        # Save to markdown file
        report_path = self.output_dir / "eval_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        logger.info(f"✅ Báo cáo sinh xong tại: {report_path}")
        
        # Save CSV backup
        csv_path = self.output_dir / "eval_metrics.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8")
        
        return md_content

    def print_summary(self):
        """In nhanh bảng tóm tắt trung bình."""
        data = self._load_metrics()
        df = pd.DataFrame(data)
        
        target_metrics = [
            "faithfulness", 
            "answer_relevancy", "response_relevancy",
            "context_precision", "llm_context_precision_with_reference",
            "context_recall", "llm_context_recall",
        ]
        available = [m for m in target_metrics if m in df.columns]
        
        print("\n" + "="*40)
        print("📊 TỔNG KẾT ĐÁNH GIÁ (RAGAS)")
        print("="*40)
        for m in available:
            print(f"- {m:20}: {df[m].mean():.4f}")
        print("="*40 + "\n")
