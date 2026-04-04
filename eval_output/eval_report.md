# Báo Cáo Đánh Giá RAG (Post-Eval)

**Số lượng mẫu (samples):** 246

## Tổng Quan Điểm Số (Average)
| Chỉ số (Metric) | Điểm trung bình |
| :--- | :---: |
| Faithfulness | **0.9757** |
| Answer Relevancy | **0.8571** |
| Llm Context Precision With Reference | **0.8555** |
| Context Recall | **0.9593** |

## Thống Kê Thời Gian Phản Hồi
| Thành phần | Thời gian trung bình (Giây) |
| :--- | :---: |
| Retriever | 4.579 s |
| Generator (LLM) | 1.979 s |
| **Tổng thời gian pipeline** | **6.558 s** |

## Phân Tích Cơ Bản
1. **Faithfulness** (Độ trung thực): Điểm cao có nghĩa câu trả lời không bịa thông tin ngoài ngữ cảnh (hallucinations).
2. **Answer Relevancy** (Độ phù hợp): Câu trả lời đi thẳng vào trọng tâm câu hỏi.
3. **Context Precision** (Độ chính xác ngữ cảnh): Các chunk giá trị nhất được xếp ở ưu tiên cao.
4. **Context Recall** (Độ bao phủ ngữ cảnh): Retriever đã tìm được bao nhiêu phần trăm thông tin cần thiết so với reference.