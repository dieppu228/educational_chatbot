# 📊 Repository Structure

```
Educational-Chatbot/
│
├── 📁 src/                                 ← Source code chính
│   ├── __init__.py
│   │
│   ├── 📁 rag/                             ← RAG Pipeline
│   │   ├── __init__.py
│   │   ├── retrieve_rebuild.py             CustomSearch (BM25 + Semantic + RRF)
│   │   ├── reranker.py                     Reranker (AITeamVN/Vietnamese_Reranker)
│   │   ├── query_rewriter.py               Query Rewrite (Gemini Flash Lite)
│   │   ├── embedding.py                    EmbeddingModel (vietnamese-document-embedding)
│   │   ├── chunking.py                     HierarchicalChunker
│   │   ├── retriever.py                    Retriever cũ (legacy)
│   │   ├── filter.py                       Metadata filter
│   │   ├── classification_query.py         Query classification
│   │   ├── evaluation.py                   RAG Evaluation (placeholder)
│   │   └── pipeline_baseline.ipynb         Notebook chạy full pipeline
│   │
│   ├── 📁 llm/                             ← LLM Generation
│   │   ├── __init__.py
│   │   ├── intent_detector.py              Intent + TaskType detection (Gemini)
│   │   ├── memory.py                       SessionState, TaskItem, MemoryManager
│   │   ├── conversation.py                 ChatBot orchestrator (đang refactor)
│   │   ├── prompts.py                      Tất cả prompt templates
│   │   ├── extract_keyword.py              Trích xuất keyword (Gemini)
│   │   ├── validators.py                   Input validation
│   │   ├── utils.py                        Helper functions
│   │   ├── router.py                       PhoBERT router (legacy → thay bằng intent_detector)
│   │   ├── context_analyzer.py             Query context analysis
│   │   ├── build_context.py                Build context cho LLM
│   │   ├── format_context.py               Format context string
│   │   │
│   │   └── 📁 handlers/
│   │       ├── __init__.py                 Export tất cả handlers
│   │       ├── base_handler.py             BaseHandler (ABC)
│   │       │
│   │       ├── 📁 question/                Sinh câu hỏi (mọi dạng)
│   │       │   ├── mcq_handler.py          Trắc nghiệm ABCD
│   │       │   ├── essay_handler.py        Tự luận
│   │       │   ├── fill_handler.py         Đục lỗ / điền khuyết
│   │       │   └── scorer.py              Chấm điểm (mọi dạng)
│   │       │
│   │       ├── 📁 content/                 Sinh nội dung giảng dạy
│   │       │   ├── slide_handler.py        Sinh slide bài giảng
│   │       │   └── lesson_plan_handler.py  Sinh giáo án
│   │       │
│   │       ├── chat_handler.py             Hỏi đáp kiến thức
│   │       ├── explain_handler.py          Giải thích chuyên sâu
│   │       │
│   │       ├── (legacy — sẽ xóa sau khi migrate)
│   │       ├── question_handler.py         QuestionGenerator cũ
│   │       ├── response_handler.py         ResponseFormatter cũ
│   │       └── fallback_handler.py         FallbackHandler cũ
│   │
│   ├── 📁 config/                          Cấu hình
│   │   ├── __init__.py
│   │   ├── config.py                       Pydantic Settings (API keys, paths)
│   │   └── constants.py                    Constants (temperature, patterns)
│   │
│   ├── 📁 schemas/                         Pydantic schemas
│   │   ├── __init__.py
│   │   ├── llm_outputs.py                  MCQResponse, ScoringResult
│   │   └── rag_outputs.py                  SearchResult
│   │
│   ├── 📁 prompts/                         Prompt templates (module riêng)
│   │   ├── __init__.py
│   │   └── base.py, extract_prompts.py, ...
│   │
│   ├── 📁 utils/                           Utilities
│   │   └── __init__.py                     Logger setup
│   │
│   └── 📁 notebook/                        Jupyter notebooks
│       ├── chunking.ipynb
│       ├── rag.ipynb
│       ├── classification_model.ipynb
│       ├── finetune_embedding.ipynb
│       └── scan_text_v2.ipynb
│
├── 📁 data/                                Data files
│   ├── rag_chunks_v2.json                  2348 chunks (hierarchical)
│   └── embeddings.npy                      768-dim embeddings
│
├── 📁 rawdata/                             SGK raw + clean (6 sách)
│
├── 📁 CD/                                  PDF SGK Cánh Diều (lớp 10-12)
│
├── 📁 KNTT/                                PDF SGK Kết Nối Tri Thức
│
├── 📄 app_gradio.py                        Entry point (Gradio UI)
├── 📄 plan.md                              Roadmap tổng thể
├── 📄 requirements.txt                     Python dependencies
├── 📄 README.md                            Project documentation
├── 📄 .env                                 API keys (GENAI_API_KEY)
└── 📄 .gitignore
```

---

## 🔄 Data Flow

```
rawdata/*.md → chunking.py → data/rag_chunks_v2.json (2348 chunks)
                            → data/embeddings.npy (768-dim)

User Query
    ↓
IntentDetector (Gemini Flash Lite)
    → {intent, task_type, topic}
    ↓
┌─── generate_question ──→ RAG Search → MCQ/Essay/Fill Handler
├─── check_answer ────────→ QuestionScorer (dựa trên SessionState)
├─── generate_slide ──────→ RAG Filter → SlideHandler
├─── generate_lesson_plan → RAG Filter → LessonPlanHandler
├─── explain ─────────────→ RAG Search → ExplainHandler
└─── chat ────────────────→ RAG Search → ChatHandler
    ↓
Response → MemoryManager (lưu session) → User
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM API | Gemini 2.5 Flash Lite (google-genai SDK) |
| Embedding | dangvantuan/vietnamese-document-embedding (768d) |
| Reranker | AITeamVN/Vietnamese_Reranker (CrossEncoder) |
| Search | Custom BM25 + Semantic + RRF (from scratch) |
| UI | Gradio |
| Config | Pydantic Settings + dotenv |

---

## 📊 Key Stats

```
Corpus:     2348 chunks (6 sách, lớp 10-12)
Embedding:  768-dim, L2-normalized
BM25 Vocab: 17139 terms
Latency:    ~21s (CPU) — bottleneck: reranker
```
