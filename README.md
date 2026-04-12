# Intelligent Educational Assistant System (Educational Chatbot)

Graduation Thesis project to design and build an Intelligent Virtual Assistant supporting teaching and learning of Computer Science at the High School level (Grades 10-12). The system is developed based on the RAG (Retrieval-Augmented Generation) architecture combined with a Multi-Agent LLM approach to overcome information hallucination and enhance accuracy by closely following textbooks.

## 1. General Introduction

The system aims to provide a tool that automates complex academic tasks, serving both students and teachers.

**Core Functions:**

- **Knowledge Query (QA):** Answer questions based on a standardized textbook corpus (Canh Dieu and Ket Noi Tri Thuc).
- **Extraction and Question Generation (Quiz Generation):** Automatically initialize exercise systems in various formats (Multiple choice, Fill-in-the-blank, True/False, Essay) with customizable quantity and difficulty.
- **Evaluation and Scoring (Answer Scoring):** Automatically score answers and provide reasoning for corrections based on actual context instead of just keyword matching.
- **Lecture Structure Generation (Slide/Lesson Plan Generation):** Convert text content into summary structures for creating presentations or lesson plans.

---

## 2. Detailed System Pipeline

The system is engineered around a Clean Architecture approach with a **Thin Pipeline Controller (Orchestrator v3)** dynamically resolving requests without hardcoupled domain logic. The data flows encapsulated within a `RequestContext` through the following End-to-End steps:

```text
┌───────────────────────────────────────────────────────────────────────────┐
│               User Message / Query  ──▶  [RequestContext]                 │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                  1. Context Analysis & Intent Routing                     │
│                                                                           │
│ [ContextAnalyzer (Code)] ──▶ Evaluates history context dependency         │
│          │                                                                │
│ [QueryRewriter (LLM)] ─────▶ (If needed) Generates multi-queries for RAG  │
│          │                                                                │
│          ▼             [  1st LLM Call  ]                                 │
│ [IntentRouter (LLM)] ──────▶ (Extracts: Intent, Task Type, Topic, Grade)  │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                2. Core Pipeline Controller (Pure Code)                    │
│                                                                           │
│ [SessionManager] ──▶ Resolves Current Session State (Memory & Store)      │
│          │                                                                │
│ [ActionPlanner] ───▶ Decides Action Plan (GenerateQuiz, Slide, Score...)  │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
                ┌───────── Execution Dispatcher ─────────┐
                │     (Dictionary-based Registry)        │
                └─────────┬────────────────────┬─────────┘   
                          ▼                    ▼             
    ┌───────────────────────────┐       ┌───────────────────────────────┐
    │     Domain Services       │──────▶│         3. RAG Service        │
    │                           │       │                               │
    │ • QuizService (Generate,  │       │ • AdaptiveRAGAgent (Strategy) │
    │   Score, Review, Stats)   │       │   ──▶ STANDARD / BROAD /      │
    │ • SlideService (Slides),  │       │       CURRICULUM / HRAG       │
    │ • Specialized Handlers    │       │                               │
    │   (Explain, Chat)         │       │ • Handles Multi-query Dedup   │
    └──────────────┬────────────┘       │ • Cross-Encoder Reranking     │
                   │                    └───────────────────────────────┘
                   ▼                                         
    ┌───────────────────────────┐                            
    │ 4. Generation & Validator │                            
    │                           │                            
    │ • Generator LLM Call      │                            
    │ • Validator Agent         │                            
    └──────────────┬────────────┘                            
                   ▼                                         
┌───────────────────────────────────────────────────────────────────────────┐
│   Final Response Output  ──▶  TraceService log  ──▶  Session Auto-Save    │
└───────────────────────────────────────────────────────────────────────────┘
```

### 2.1. Context Extraction & Intent Routing

When the system receives a natural language query, it invokes a `RequestContext` spanning the entire operation:

1. **ContextAnalyzer**: Evaluates if the query requires historical session context. If true, it extracts past conversations using a Keyword/Recency hybrid scoring algorithm.
2. **QueryRewriter Agent**: When context enrichment occurs, it rewrites the single natural query into 2-3 transparent queries optimized exclusively for deep semantic retrieval.
3. **IntentRouter Agent**: Performs the first major **LLM Call** to run semantic analysis extracting key entities: `intent`, `task_type`, `topic`, and `grade`. It also detects topic switching logic (`is_new_topic`).

### 2.2. Thin Pipeline Controller (Pure Code)

To optimize latency, the core pipeline acts as a non-mutating router purely passing states:

1. **SessionManager**: Resolves and syncs the current session context via Memory Manager or persistent JSON Storage based on intent compatibility.
2. **ActionPlanner**: Consumes the context to construct an `ActionPlan` mapping accurately to a predefined action sequence (e.g., `GENERATE_QUIZ`, `EXPLAIN_CONCEPT`).
3. **ExecutionDispatcher**: Uses a dictionary-based registry (Strategy Pattern) bridging the pipeline layer directly down to domain-specific services, maintaining single-responsibility and highly scalable code abstraction.

### 2.3. Domain Services & Adaptive RAG

Action plans flow dynamically into the respective **Domain Services** (`QuizService`, `SlideService`). Operations requiring textbook knowledge pass through the decoupled **RAGService**.

The internal `AdaptiveRAGAgent` observes the query intent and dynamically decides the most performant retrieval strategy using heuristic-based `QueryClassifier`:

- **STANDARD**: For regular specific queries, implementing Hybrid Search (Lexical Custom BM25 + Semantic Cosine) followed by RRF normalization.
- **BROAD**: For large systemic queries, exclusively querying Metadata properties extracting top-level "objective" chunks.
- **CURRICULUM**: Rapid metadata aggregation over the curriculum textbook structure returning mapped out lessons.
- **HIERARCHICAL (HRAG)**: A complex Two-Phase semantic hierarchy. Phase 1 runs semantic search purely on Coarse chunks (Level 1-2). Phase 2 executes a scoped Hybrid Search localized only on the Fine chunks (Level 3+) directly descending from Phase 1 parents.

### 2.4. Generation & Self-Reflection

Filtered and reranked contexts act as the grounded information provided to the **Generator LLMs**.
Outputs corresponding to structured formats (e.g., Quiz JSON Arrays, Raw HTML Slides) are intercepted by a recursive **Self-Reflection mechanism** using the `QuestionValidator` Agent. This agent scrutinizes accuracy and cross-checks the response against original textbook contexts and strict evaluation rubrics, optionally looping regeneration until rigid logical standards and quality benchmarks are fully met.

### 2.5. RAGAS Evaluation Pipeline

To quantitatively evaluate the RAG system's performance, the project integrates an independent automated evaluation pipeline:

- **Testset Generator:** Automatically synthesizes 50-100 random samples (Query, Ground Truth Answer) from the textbook JSON chunks.
- **RAGAS Evaluator:** Uses a standard framework to measure 4 coefficients: _Answer Relevancy_, _Faithfulness_, _Context Precision_, and _Context Recall_.

---

## 3. Repository Structure (Pipeline Modules)

The project's codebase focuses on a highly modular architecture, mapping perfectly to the End-to-End Pipeline. Below is the comprehensive structure of the `src/` directory:

```text
src/
├── llm/                     # CORE LLM & MULTI-AGENT ORCHESTRATION
│   ├── orchestrator.py      # Main Dispatcher: Receives queries and coordinates the entire system workflow.
│   ├── intent_router.py     # Intent Sensor: Classifies queries (Generate, Interact, Explain, Analyze, Chat).
│   ├── action_planner.py    # High-level Brain: Plans multi-step tasks (e.g., slide generation workflow).
│   ├── context_analyzer.py  # Context Extractor: Retrieves historical context using Hybrid scoring (Keyword + Recency).
│   ├── prompts.py           # Prompt Hub: Centralizes and manages all LLM prompts with metadata.
│   ├── memory.py            # & session_manager/store: Manages conversation state and context tracking.
│   ├── validators/          # Self-Reflection Module:
│   │   └── question_validator.py # Auto cross-checks generated answers against ground-truth context.
│   └── handlers/            # Specialist Agents: Executes specific domain tasks.
│       ├── base_handler.py  # Common interface for all handlers.
│       ├── chat_handler.py  # Performs free-form chat conversations.
│       ├── explain_handler.py # Provides in-depth explanations for concepts.
│       ├── question/        # Agent cluster specialized in generating & grading educational questions:
│       │   ├── mcq_handler.py, essay_handler.py, fill_handler.py, true_false_handler.py
│       │   └── scorer.py    # Grading module based on Context and predefined Rubrics.
│       └── content/         # Generation module for extensive content (slide_handler.py, slide_template.py)...
│
├── rag/                     # ADVANCED RAG PIPELINE
│   ├── adaptive_rag.py      # Dynamic Retrieval Router: Chooses strategies (Standard, Broad, Curriculum, Hierarchical).
│   ├── retrieve_rebuild.py  # Core Search Engine: Combines Custom pure Python BM25, Semantic, RRF & Scoped Search.
│   ├── embedding.py         # Embedding Module: Loads & infers specialized Vietnamese HuggingFace models.
│   ├── reranker.py          # Cross-Encoder Reranking: Filters noise and re-ranks chunks post-retrieval.
│   └── chunking.py          # Data Engineering Module: Decomposes Markdown text into a Hierarchical tree structure.
│
├── evaluation/              # RAGAS EVALUATION PIPELINE
│   ├── run_eval.py          # CLI Controller: Executes entire testing & RAGAS pipeline.
│   ├── testset_generator.py # Synthetic Generator: Auto-generates QA Ground Truth from textbook chunks.
│   ├── ragas_eval.py        # Assessment Framework: Calculates 4 RAG metrics (Faithfulness, Relevance, Precision, Recall).
│   ├── report.py            # Reporting Module: Transforms and visualizes RAGAS evaluation metrics.
│   └── data_collector.py    # Data Preparation: Parses logs and datasets to feed the eval pipeline.
│
├── config/                  # CONFIGURATION HUB
│   └── config.py            # Central Config: Environment variables, LLM params (Gemini), and DB/File paths.
│
├── schemas/                 # DATA TYPES & STANDARDS
│   ├── message.py, session.py # Object Modeling Architecture (Session, Message, User).
│   └── state.py             # State Management Pattern across the Multi-Agent Pipeline.
│
└── utils/                   # UTILITIES & HELPER
    └── ...                  # Helper libraries: File IO, formatting, custom logging, and struct parsing.
```

---

## 4. Tech Stack

The system is developed in separate modules to ensure high scalability.

**1. Core LLM & Orchestration:**

- **Language Model:** Google Gemini (`gemini-2.5-pro` & `gemini-2.5-flash`) via `google-genai` SDK.
- **Agent Management:** Object-Oriented Python (OOP) builds an internal State Machine architecture instead of heavy frameworks.

**2. Retrieval & Vector Core:**

- **Embedding Model:** `dangvantuan/vietnamese-document-embedding` (Based on `HuggingFaceEmbeddings` / `SentenceTransformer` architecture, 768 dimensions).
- **Reranker Model:** `AITeamVN/Vietnamese_Reranker` (Cross-Encoder architecture running on torch/CUDA).
- **Search Engine:** Vector space is mathematicalized using pure `Numpy` + a self-programmed `BM25 TF-IDF Analyzer` algorithm to avoid resource waste and native library dependencies (like FAISS).

**3. Infrastructure & UI:**

- **User Interface:** `Gradio` Web Framework.
- **Evaluation System:** `ragas==0.4.3` running via CLI Argument Parser (`run_eval.py`).
- **Data Engineering:** Regular Expression (Regex) combined with Hierarchical Document Splitting handles unstructured text (Markdown).

---

## 5. Local Setup Guide

The local deployment process requires a Python environment >= 3.12:

```bash
# 1. Clone Source Code
git clone https://github.com/KhacDiep08/Educational-Chatbot.git
cd Educational-Chatbot

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Assign API Keys
echo GENAI_API_KEY=your_key_here > .env

# 4. Launch UI Server Application
python app_gradio.py
```

Run the RAGAS Metric Report evaluation script (Optional):

```bash
python -m src.evaluation.run_eval --step all
```

---

_Student Information: Khac Diep (Hanoi University of Science and Technology)._
