# 📚 Educational Chatbot — Vietnamese RAG System

Hệ thống chatbot giáo dục thông minh phục vụ dạy-học **Tin học THPT** (lớp 10-12), xây dựng trên kiến trúc **RAG (Retrieval-Augmented Generation)** kết hợp LLM.

Hỗ trợ đa tác vụ: hỏi đáp kiến thức, sinh câu hỏi (trắc nghiệm, tự luận, đục lỗ), sinh slide bài giảng, sinh giáo án.

---

## 🏗️ Kiến trúc tổng quan

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Gradio)                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Intent     │  Gemini Flash Lite
                    │  Detector   │  → {intent, task_type, topic}
                    └──────┬──────┘
                           │
          ┌────────────────┼─────────────────────────┐
          │                │                         │
   ┌──────▼──────┐  ┌─────▼──────┐          ┌──────▼──────┐
   │  Question   │  │  Content   │          │  Knowledge  │
   │  Handlers   │  │  Handlers  │          │  Handlers   │
   │             │  │            │          │             │
   │ • MCQ       │  │ • Slide    │          │ • Chat      │
   │ • Essay     │  │ • Lesson   │          │ • Explain   │
   │ • Fill      │  │   Plan     │          │ • Scorer    │
   └──────┬──────┘  └─────┬──────┘          └──────┬──────┘
          │                │                       │
          └────────────────┼───────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  RAG Core   │
                    │             │
                    │ Query       │
                    │ Rewriter    │──→ Gemini Flash Lite
                    │    ↓        │
                    │ Hybrid      │
                    │ Search      │──→ BM25 + Semantic + RRF
                    │    ↓        │
                    │ Reranker    │──→ Vietnamese_Reranker
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Memory      │
                    │ Manager     │──→ Session, TaskItems
                    └─────────────┘
```

---

## 🔄 End-to-End Flow

### Phase 0: Data Preparation (Offline — chạy 1 lần)

```
SGK PDF (6 sách: CD + KNTT, lớp 10-12)
    │
    ▼  OCR + Clean
rawdata/*.md (6 file markdown)
    │
    ▼  Hierarchical Chunking (src/rag/chunking.py)
data/rag_chunks_v2.json (2348 chunks)
    │   Mỗi chunk có: content, context (breadcrumb), metadata (book, grade, lesson, topic, type)
    │
    ▼  Embedding (src/rag/embedding.py)
data/embeddings.npy (2348 × 768 vectors, L2-normalized)
    │   Model: dangvantuan/vietnamese-document-embedding
    │
    ▼  BM25 Index (build on-the-fly)
    Tokenize → TF/DF/IDF → vocab 17139 terms
```

### Phase 1: User Query → Intent Detection

```
User: "Tạo 5 câu trắc nghiệm về mạng LAN"
    │
    ▼  IntentDetector (Gemini Flash Lite, ~0.3s)
{
    "intent": "generate_question",
    "task_type": "mcq",
    "topic": "mạng LAN"
}
    │
    ▼  Dispatch → MCQHandler
```

Các intents hỗ trợ:

| Intent | Mô tả | Task Types |
|---|---|---|
| `generate_question` | Sinh câu hỏi | `mcq`, `essay`, `fill_blank`, `true_false` |
| `check_answer` | Chấm đáp án | — |
| `generate_slide` | Sinh slide bài giảng | — |
| `generate_lesson_plan` | Sinh giáo án | — |
| `explain` | Giải thích chuyên sâu | — |
| `chat` | Hỏi đáp chung | — |

### Phase 2: RAG Retrieval

```
Topic: "mạng LAN"
    │
    ▼  Query Rewriter (Gemini Flash Lite, ~1s)
    Sinh 2-3 truy vấn bổ sung:
      [0] "mạng LAN"
      [1] "khái niệm mạng cục bộ LAN, kết nối thiết bị phạm vi nhỏ"
      [2] "phân loại mạng máy tính LAN WAN Internet"
    │
    ▼  Hybrid Search per query (CustomSearch, ~0.2s)
    ┌────────────────────────────────────┐
    │  BM25 Search (keyword matching)    │
    │  • Tokenize query → TF-IDF score   │
    │  • k1=1.2, b=0.75                  │
    │                                    │
    │  Semantic Search (vector matching)  │
    │  • Encode query → 768-dim          │
    │  • Cosine similarity (numpy dot)   │
    │                                    │
    │  RRF Fusion (k=60)                 │
    │  • Merge BM25 + Semantic ranks     │
    │  • score = Σ 1/(k + rank_i)        │
    └──────────────┬─────────────────────┘
                   │
                   ▼  Merge unique docs từ tất cả queries
              ~15-30 candidate docs
    │
    ▼  Reranker (AITeamVN/Vietnamese_Reranker, ~20s CPU)
    Cross-encoder scoring: (query, doc) → relevance score
    │
    ▼  Filter & Top-K
    Bỏ trùng lặp, quá ngắn → top 5 docs
```

### Phase 3: LLM Generation

```
Top 5 docs (context) + User query + Prompt
    │
    ▼  Handler tương ứng (Gemini API)
    ┌────────────────────────────────────┐
    │  MCQHandler:                       │
    │    Context + "Sinh 5 câu trắc      │
    │    nghiệm ABCD" → JSON response   │
    │                                    │
    │  EssayHandler:                     │
    │    Context + "Sinh câu tự luận"    │
    │    → câu hỏi + đáp án mẫu         │
    │                                    │
    │  SlideHandler:                     │
    │    All chunks of lesson → danh     │
    │    sách slides (title + bullets)   │
    │                                    │
    │  ChatHandler:                      │
    │    Context + query → trả lời tự    │
    │    nhiên bằng tiếng Việt           │
    └──────────────┬─────────────────────┘
                   │
                   ▼
              Response
```

### Phase 4: Memory & Response

```
Response
    │
    ▼  MemoryManager
    Lưu vào SessionState:
    • intent, task_type, topic
    • items: List[TaskItem] (linh hoạt theo type)
    • messages: List[Message] (conversation history)
    │
    ▼  Return to User (Gradio UI)
```

---

## 🛠️ Tech Stack

| Component | Technology | Ghi chú |
|---|---|---|
| **LLM API** | Gemini 2.5 Flash Lite | Intent detection, query rewrite, generation |
| **Embedding** | dangvantuan/vietnamese-document-embedding | 768-dim, SentenceTransformer |
| **Reranker** | AITeamVN/Vietnamese_Reranker | CrossEncoder, tiếng Việt |
| **Search** | Custom BM25 + Semantic + RRF | Tự build, không dùng FAISS/rank_bm25 |
| **UI** | Gradio | Web interface |
| **Config** | Pydantic Settings + dotenv | Quản lý API keys, paths |

---

## 📊 Baseline Performance

| Metric | Giá trị |
|---|---|
| Corpus | 2348 chunks (6 sách THPT) |
| Embedding | 768-dim, L2-normalized |
| BM25 vocab | 17139 terms |
| Latency tổng | ~21s (CPU) |
| Rewrite | ~1s |
| Search | ~0.2s |
| Rerank | ~20s (bottleneck — CPU cross-encoder) |
| Top-1 accuracy (manual) | Cao — "mạng máy tính" → đúng chunk CD-12 Bài 1 (score=0.999) |

---

## 🚀 Cài đặt & Chạy

### 1. Clone & Install

```bash
git clone https://github.com/KhacDiep08/Educational-Chatbot.git
cd Educational-Chatbot
pip install -r requirements.txt
```

### 2. Setup API Key

```bash
# Tạo file .env
echo GENAI_API_KEY=your_key_here > .env
```

### 3. Chạy RAG Pipeline (test)

```bash
# Chạy notebook baseline
jupyter notebook src/rag/pipeline_baseline.ipynb
```

### 4. Chạy Gradio UI

```bash
python app_gradio.py
# Mở http://127.0.0.1:7860
```

---

## 📦 Cấu trúc project

> Chi tiết xem [REPO_STRUCTURE.md](REPO_STRUCTURE.md)

```
ĐATN/
├── src/                    Source code chính
│   ├── rag/                RAG Pipeline (search, rerank, embed, eval)
│   ├── llm/                LLM Generation (handlers, intents, memory)
│   ├── config/             Cấu hình (API keys, constants)
│   ├── schemas/            Pydantic schemas
│   └── prompts/            Prompt templates
├── data/                   Chunks + Embeddings
├── rawdata/                SGK raw markdown
├── CD/, KNTT/              PDF gốc
├── app_gradio.py           Entry point
├── plan.md                 Roadmap
└── requirements.txt
```

---

## 📋 Dữ liệu đầu vào

| Bộ SGK | Lớp | Số chunks |
|---|---|---|
| Cánh Diều (CD) | 10, 11, 12 | ~1200 |
| Kết Nối Tri Thức (KNTT) | 10, 11, 12 | ~1100 |
| **Tổng** | | **2348** |

Mỗi chunk bao gồm:
- `content`: Nội dung văn bản
- `context`: Breadcrumb (Topic → Lesson → Section → Title)
- `metadata`: book, grade, topic, lesson, section, type (theory/exercise/summary)

---

## 📈 Roadmap

> Chi tiết xem [plan.md](plan.md)

- [x] **Phase 1**: RAG Pipeline (BM25 + Semantic + RRF + Reranker + Query Rewrite)
- [ ] **Phase 1.5**: RAG Evaluation (benchmark 50 câu, Recall@k, MRR)
- [ ] **Phase 2**: Gemini API features (Slide + Giáo án)
- [ ] **Phase 3**: LLM Self-host + Fine-tune (7B model, QLoRA)

---

## 👨‍💼 Thông tin

- **Sinh viên**: Khắc Diệp
- **Trường**: Đại học Bách khoa Hà Nội (HUST)
- **Đồ án tốt nghiệp**: 2025-2026

---

**Last Updated**: March 21, 2026 | **Version**: 2.0.0
