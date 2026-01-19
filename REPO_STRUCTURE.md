# 📊 Repository Structure

```
Educational-Chatbot/
│
├── 📁 config/                          ← Centralized configuration
│   ├── __init__.py
│   ├── config.py                       (Pydantic BaseSettings)
│   └── constants.py                    (Global constants)
│
├── 📁 core/                            ← Data models & types
│   └── __init__.py                     (Pydantic models: MCQQuestion, Chunk, etc.)
│
├── 📁 utils/                           ← Utilities & infrastructure
│   └── __init__.py                     (Logger setup)
│
├── 📁 LLM/                             ← Language Model handlers
│   ├── 📁 handlers/                    (Modular handler classes)
│   │   ├── __init__.py
│   │   ├── base_handler.py             (BaseHandler ABC)
│   │   ├── question_handler.py         (QuestionGenerator)
│   │   ├── response_handler.py         (ResponseFormatter, AnswerScorer)
│   │   └── fallback_handler.py         (FallbackHandler)
│   │
│   ├── __init__.py                     (Clean exports)
│   ├── prompts.py                      (All prompt templates)
│   ├── validators.py                   (Input validation)
│   ├── utils.py                        (Helper functions)
│   ├── context_analyzer.py             (Query context analysis)
│   ├── conversation.py                 (Conversation management)
│   ├── build_context.py
│   ├── format_context.py
│   ├── router.py
│   └── test.ipynb
│
├── 📁 RAG/                             ← Retrieval & Reranking
│   ├── __init__.py
│   ├── retriever.py                    (Hybrid search: BM25 + FAISS)
│   ├── reranker.py                     (Document reranking)
│   ├── embedding.py                    (Embedding utilities)
│   ├── classification_query.py
│   └── __pycache__/
│
├── 📁 Notebook/                        ← Jupyter notebooks
│   ├── classification_model.ipynb
│   ├── finetune_embedding.ipynb
│   ├── preprocess_chunking.ipynb       (Data preprocessing)
│   ├── rag.ipynb                       (RAG pipeline)
│   ├── scan_text.ipynb
│   └── triplets_output.json
│
├── 📁 CanhDieu/                        ← Application interface
│   └── (Gradio UI)
│
├── 📁 data/                            ← Data files
│   ├── du_lieu_mapped.csv
│   ├── du_lieu_mapped1.csv
│   ├── embeddings.npy                  (Precomputed embeddings)
│   ├── final_chunks_clean.json
│   ├── final_chunks_cleaned.json
│   ├── final_chunks_output.json
│   ├── final_chunks_output.txt
│   ├── query_label_clean.csv
│   └── query_label.csv
│
├── 📁 RawData/                         ← Original textbook data
│   ├── SGK_Tin10_CD_clean.md           (Grade 10 - cleaned)
│   ├── SGK_Tin10_CD.md                 (Grade 10 - original)
│   ├── SGK_Tin11_CD_clean.md           (Grade 11 - cleaned)
│   ├── SGK_Tin11_CD.md                 (Grade 11 - original)
│   ├── SGK_Tin12_CD_clean.md           (Grade 12 - cleaned)
│   └── SGK_Tin12_CD.md                 (Grade 12 - original)
│
├── 📁 logs/                            ← Application logs
│   └── app.log                         (Rotating log file)
│
├── 📁 temp_images/
├── 📁 .git/                            ← Git repository
├── 📁 .vscode/                         ← VS Code settings
├── 📁 .gradio/                         ← Gradio cache
│
├── 📄 .env                             ← Environment variables (API keys)
├── 📄 .gitignore                       ← Git ignore rules
├── 📄 rag_chunks.json                  ← Processed chunks (645 documents)
├── 📄 triplets_output1.json            ← Training triplets
├── 📄 requirements.txt                 ← Python dependencies
├── 📄 README.md                        ← Project documentation
├── 📄 REFACTOR_PLAN.md                 ← Refactor specification
├── 📄 REFACTOR_SUMMARY.md              ← Refactor summary
└── 📄 test_refactor.py                 ← Integration tests

```

---

## 📋 File Count & Sizes

```
Total Directories: 15
Total Python Files: 25+
Total Notebooks: 5
Total Config Files: 3

Key Statistics:
- LLM Module: 11 Python files (900+ lines refactored)
- RAG Module: 4 Python files (800+ lines)
- Notebooks: 5 (Data processing & RAG)
- Config: 3 files (Centralized settings)
- Data: 645 chunks processed
```

---

## 🎯 Module Organization

### **config/** - Configuration Management
```
- Settings (Pydantic)
- Constants (temperature, grades, patterns)
- Environment variables (.env)
```

### **core/** - Data Models
```
- MCQQuestion, MCQOption, MCQResponse
- Chunk, ChunkMetadata
- ScoringResult, Query
- ConversationContext
```

### **utils/** - Infrastructure
```
- setup_logger() - Centralized logging
- Rotating file handler
```

### **LLM/** - Language Model Pipeline
```
handlers/
├── BaseHandler (ABC)
├── QuestionGenerator
├── ResponseFormatter
├── AnswerScorer
└── FallbackHandler

prompts.py - All LLM prompts
validators.py - Input validation
utils.py - Helper functions
context_analyzer.py - Query analysis
```

### **RAG/** - Retrieval & Ranking
```
- Retriever (Hybrid BM25 + FAISS)
- Reranker (FlagReranker)
- Embedding utilities
```

### **Notebook/** - Data Processing
```
- preprocess_chunking.ipynb (645 chunks)
- rag.ipynb (RAG demo)
- finetune_embedding.ipynb
```

### **CanhDieu/** - UI Layer
```
- Gradio interface
```

### **data/** - Processed Data
```
- Chunks (645 MCQ-like documents)
- Embeddings (precomputed)
- Metadata (grade, lesson, idea)
```

### **RawData/** - Source Data
```
- 6 markdown files (Grade 10/11/12 - Tin học)
- Cleaned & original versions
```

---

## 🔄 Data Flow

```
RawData/
  ↓ (preprocess_chunking.ipynb)
data/
  ├── final_chunks*.json
  ├── embeddings.npy
  └── query_label*.csv
    ↓
rag_chunks.json (645 documents)
    ↓
RAG/ (Retriever + Reranker)
    ↓
LLM/ (Question Generation + Scoring)
    ↓
CanhDieu/ (Gradio UI)
```

---

## 📦 Key Files Breakdown

| File | Lines | Purpose |
|------|-------|---------|
| `LLM/handlers/base_handler.py` | 150+ | Base class for all handlers |
| `LLM/handlers/question_handler.py` | 200+ | Question generation |
| `LLM/prompts.py` | 300+ | All LLM prompt templates |
| `RAG/retriever.py` | 300+ | Hybrid search (BM25 + FAISS) |
| `core/__init__.py` | 150+ | Pydantic models |
| `config/config.py` | 50+ | Settings management |
| `LLM/validators.py` | 100+ | Input validation |
| `rag_chunks.json` | - | 645 processed documents |

---

## 🚀 Typical Workflow

### 1. **Data Preparation** (One-time)
```
RawData/*.md → preprocess_chunking.ipynb → rag_chunks.json
```

### 2. **User Query → Response**
```
Query
  ↓ (router.py - route to handler)
  ├→ Question Request
  │    ↓ (QuestionGenerator)
  │    ├ RAG.Retriever.hybrid_search()
  │    ├ RAG.Reranker.rerank()
  │    └ LLM API (Generate MCQ JSON)
  │
  ├→ Answer Scoring
  │    ↓ (AnswerScorer)
  │    └ LLM API (Grade & Feedback)
  │
  └→ Off-topic
       ↓ (FallbackHandler)
       └ LLM API (Chitchat response)
```

### 3. **Logging & Monitoring**
```
Every operation → utils.setup_logger() → logs/app.log
```

---

## 🛠️ Development Environment

```
Python Version: 3.12+
Package Manager: pip
Virtual Environment: venv
Version Control: Git
Testing: pytest (via test_refactor.py)
Notebooks: Jupyter
```

---

## 📊 Repository Stats (After Refactor)

```
✅ Total Python Files: 25+
✅ Total Lines of Code: ~4000+
✅ Modules: 6 (config, core, utils, LLM, RAG, CanhDieu)
✅ Classes: 20+ (Pydantic models + handlers)
✅ Functions: 50+ (utilities & helpers)
✅ Test Coverage: Integration test passing
✅ Documentation: 100% (REFACTOR_PLAN + REFACTOR_SUMMARY)
```

---

## 🎯 Next Steps (If Needed)

1. **Unit Tests** - Add pytest for each handler
2. **API Endpoints** - FastAPI wrapper
3. **Deployment** - Docker containerization
4. **Monitoring** - Add metrics/dashboards
5. **CI/CD** - GitHub Actions
