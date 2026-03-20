"""
RAG Evaluation Module — Đánh giá chất lượng pipeline RAG.

Metrics:
    - Recall@k: % expected docs được tìm thấy trong top-k
    - MRR (Mean Reciprocal Rank): Trung bình 1/rank của doc đúng đầu tiên
    - nDCG@k: Normalized Discounted Cumulative Gain
    - Latency: Thời gian xử lý từng bước
    - Ablation: So sánh BM25 only / Semantic only / Hybrid / +Rewrite / +Rerank

Benchmark:
    - Tự tạo 50 câu hỏi + expected doc_ids (file data/eval_benchmark.json)
    - Cover cả 6 sách (CD + KNTT, lớp 10-12)
    - Đa dạng loại: kiến thức, so sánh, ứng dụng, bài tập

TODO:
    [ ] Tạo eval_benchmark.json (50 câu)
    [ ] Implement Recall@k, MRR, nDCG@k
    [ ] Ablation study: BM25 / Semantic / Hybrid / +Rewrite / +Rerank
    [ ] LLM-as-Judge (Gemini chấm relevance 1-5)
    [ ] Generate report + charts
"""

# === PLACEHOLDER: sẽ implement sau ===
