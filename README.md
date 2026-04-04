# Hệ Thống Trợ Lý Học Tập Thông Minh (Educational Chatbot)

Dự án Đồ án Tốt nghiệp thiết kế và xây dựng một hệ thống Trợ lý ảo hỗ trợ dạy và học chuyên môn Tin học cấp THPT (Lớp 10-12). Hệ thống được phát triển dựa trên kiến trúc RAG (Retrieval-Augmented Generation) kết hợp với mô hình LLM theo hướng tiếp cận Multi-Agent, nhằm khắc phục các hạn chế về ảo giác thông tin (Hallucination) và nâng cao độ chính xác theo sát sách giáo khoa.

## 1. Giới thiệu chung

Mục tiêu của hệ thống là cung cấp một công cụ tự động hóa các tác vụ học thuật phức tạp, phục vụ cả học sinh và giáo viên.

**Các chức năng cốt lõi:**

- **Truy vấn kiến thức chuyên môn (QA):** Trả lời các câu hỏi dựa trên kho ngữ liệu sách giáo khoa chuẩn (Cánh Diều và Kết Nối Tri Thức).
- **Trích xuất và Sinh câu hỏi (Quiz Generation):** Tự động khởi tạo hệ thống bài tập theo nhiều định dạng (Trắc nghiệm nhiều lựa chọn, Điền khuyết, Đúng/Sai, Tự luận) với số lượng và độ khó tùy chỉnh.
- **Đánh giá và Chấm điểm (Answer Scoring):** Chấm điểm tự động và cung cấp lập luận sửa ý sai dựa trên context thực tế thay vì chỉ đối chiếu từ khóa.
- **Sinh cấu trúc bài giảng (Slide/Lesson Plan Generation):** Chuyển đổi nội dung văn bản thành cấu trúc tóm tắt phục vụ cho việc tạo trình chiếu hoặc giáo án.

---

## 2. Pipeline hệ thống chi tiết

Hệ thống được thiết kế theo luồng xử lý Multi-Agent kết hợp với cơ chế RAG chuyên sâu. Quy trình (End-to-End Workflow) đi qua các giai đoạn độc lập:
```text
┌────────────────────────────────────────────────────────┐
│                   User Message / Query                 │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│               1. Intent Detector Agent                 │
│  (Extracts: Intent, Task Type, Topic, Specific Info)   │
└───────────────────────────┬────────────────────────────┘
                            ▼
                    [ Dispatcher ] ────────────┐
                            │                  │
                      (Match Task)             │
                            ▼                  ▼
┌──────────────────────────────────┐   ┌───────────────┐
│        Specialist Handlers       │   │ General Chat  │
│  (Question / Explain / Slide...) │   │   Handler     │
└─────────────────┬────────────────┘   └───────────────┘
                  │
                  ▼
┌────────────────────────────────────────────────────────┐
│            2. Advanced RAG Pipeline Core               │
│                                                        │
│  a. Query Rewriting (Expands query context)            │
│          │                                             │
│  b. Hybrid Search ──▶ Lexical (Custom BM25)            │
│                   ──▶ Semantic (Vector Embedding)      │
│          │                                             │
│  c. RRF (Reciprocal Rank Fusion - Score merging)       │
│          │                                             │
│  d. Reranking (Cross-Encoder threshold filtering)      │
└─────────────────────────┬──────────────────────────────┘
                          │      ┌───────────────────────┐
                          ├──────┤  Document Datastore   │
                          │      │  (Text Chunks / JSON) │
                          ▼      └───────────────────────┘
┌────────────────────────────────────────────────────────┐
│          3. Generation & Validator (Reflection)        │
│                                                        │
│   ┌───────────────────┐        ┌───────────────────┐   │
│   │   Generator LLM   │───────▶│  Validator Agent  │   │
│   │ (Drafts Content)  │◀───────│ (Check & Reflect) │   │
│   └───────────────────┘        └───────────────────┘   │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                 Final Response / UI Output             │
└────────────────────────────────────────────────────────┘
```

### 2.1. Phân loại Ý định (Intent Detection)

Khi hệ thống tiếp nhận truy vấn ngôn ngữ tự nhiên từ người dùng, `IntentDetector Agent` sẽ phân tích ngữ nghĩa để trích xuất 3 thực thể tham số (Entities):

- `intent`: Mục đích thực thụ của câu lenh (Chat, Generate Question, Explain, v.v).
- `task_type`: Định dạng đầu ra mong muốn (Ví dụ: `mcq`, `essay`).
- `topic`: Chủ đề kiến thức người dùng đang muốn nhắm tới.

Lệnh trích xuất sau đó được bộ Dispatcher định tuyến tới Specialist Handler (Tác tử chuyên môn) tương ứng.

### 2.2. Xử lý Truy xuất Hệ thống RAG (Advanced RAG Pipeline)

Để đảm bảo LLM nhận được tập tài liệu (Context) chính xác nhất, hệ thống triển khai pipeline Retrieval với 4 bước tối ưu độ trễ và độ chụm:

1. **Query Rewriting:** LLM Agent phân tách và viết lại câu hỏi gốc thành các biến thể (queries) nhằm bao quát không gian ngữ nghĩa, tăng chỉ số Recall.
2. **Hybrid Search:** Thực hiện tìm kiếm song song trên không gian Vector:
   - **Lexical Search:** Sử dụng module `Custom BM25` độc lập (TF-IDF cải tiến) để truy vết chính xác từ khóa đặc thù ngành.
   - **Semantic Search:** Sử dụng Cosine Similarity trên mô hình Embedding để tìm sự tương đồng về ngữ nghĩa.
3. **Reciprocal Rank Fusion (RRF):** Thuật toán chuẩn hóa và hòa trộn (Merge) kết quả xếp hạng từ hai bộ máy tìm kiếm ở bước 2.
4. **Cross-Encoder Reranking:** Sử dụng mô hình `Vietnamese_Reranker` để tính toán khoảng cách vector tuyến tính giữa Query và Top N Document. Lọc bỏ các chunk bị nhiễu do trùng lặp hoặc chứa điểm số liên quan (`rerank_score`) dưới ngưỡng.

### 2.3. Sinh nội dung và Vùng Phản Biện (Generation & Self-Reflection)

Tài liệu sau khi lọc được đóng gói cùng Query và nạp vào LLM để sinh kết quả (JSON Formatting).
Tại pha này, hệ thống áp dụng cơ chế Self-Reflection thông qua một `Validator Agent`. Kết quả sau khi sinh sẽ được Agent này trích xuất ngược để đối soát chéo với Context ban đầu nhằm đảm bảo các yêu cầu cấu trúc và không vi phạm điều kiện logic. Nếu xác thực thất bại, tiến trình Generation sẽ được gọi đệ quy để thực thi lại đến khi đạt quy chuẩn.

### 2.4. Đo lường độc lập (RAGAS Evaluation Pipeline)

Để đánh giá định lượng hiệu năng hệ thống RAG, dự án tích hợp một pipeline đánh giá độc lập tự động:

- **Testset Generator:** Tự động tổng hợp 50-100 Samples (Query, Ground Truth Answer) ngẫu nhiên từ kho JSON chunks SGK.
- **RAGAS Evaluator:** Sử dụng framework chuẩn đo lường 4 hệ số: _Answer Relevancy_, _Faithfulness_, _Context Precision_, và _Context Recall_.

---

## 3. Tech Stack (Công nghệ triển khai)

Hệ thống được phát triển tách biệt thành các modules để đảm bảo tính mở rộng cao (Scalability).

**1. Core LLM & Orchestration:**

- **Mô hình ngôn ngữ:** Google Gemini (`gemini-2.5-pro` & `gemini-2.5-flash`) thông qua `google-genai` SDK.
- **Quản lý Agent:** Python hướng đối tượng (OOP) xây dựng kiến trúc State Machine nội bộ thay cho các framework nặng.

**2. Retrieval & Vector Core:**

- **Mô hình Nhúng (Embedding):** `dangvantuan/vietnamese-document-embedding` (Dựa trên kiến trúc `HuggingFaceEmbeddings` / `SentenceTransformer`, không gian 768 chiều).
- **Mô hình Xếp hạng lại (Reranker):** `AITeamVN/Vietnamese_Reranker` (Kiến trúc Cross-Encoder chạy trên torch/CUDA).
- **Search Engine:** Vector không gian được thực toán hóa bằng `Numpy` Thuần + Thuật toán `BM25 TF-IDF Analyzer` tự lập trình để tránh hao tổn tài nguyên và dependency thư viện native (như FAISS).

**3. Infrastructure & UI:**

- **Giao diện Người dùng:** `Gradio` Web Framework.
- **Hệ thống Đo lường (Evaluation):** `ragas==0.4.3` chạy qua CLI Argument Parser (`run_eval.py`).
- **Data Engineering:** Regular Expression (Regex) kết hợp Chunking phân cấp (Hierarchical Document Splitting) xử lý văn bản phi cấu trúc (Markdown).

---

## 4. Hướng dẫn Local Setup

Quá trình triển khai Local Requirement yêu cầu môi trường Python >= 3.12:

```bash
# 1. Clone Source Code
git clone https://github.com/KhacDiep08/Educational-Chatbot.git
cd Educational-Chatbot

# 2. Cài đặt Dependencies
pip install -r requirements.txt

# 3. Phân bổ API Keys
echo GENAI_API_KEY=your_key_here > .env

# 4. Khởi chạy Ứng dụng Server UI
python app_gradio.py
```

Khởi chạy tập lệnh đo lường Metric RAGAS Report (Option):

```bash
python -m src.evaluation.run_eval --step all
```

---

_Thông tin sinh viên thực hiện: Khắc Diệp (Đại học Bách Khoa Hà Nội)._
