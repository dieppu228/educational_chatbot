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

The system is designed with a Code-Level Orchestrator resolving sessions, coupled with Multi-Agent execution. The End-to-End Workflow goes through the following distinct stages:

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                           User Message / Query                            │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                   1. Context Extraction & Intent Routing                  │
│                                                                           │
│ [ContextAnalyzer (Code)] ── (If needed, enrich query with Session History)│
│          │                                                                │
│          ▼             [  1st LLM Call  ]                                 │
│ [IntentDetector (LLM)] ──── (Extracts: Intent, Task Type, Topic, Grade)   │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     2. Core Orchestration (Pure Code)                     │
│                                                                           │
│ [SessionManager] ──▶ Resolves Current Session State (Memory & Store)      │
│          │                                                                │
│          ▼                                                                │
│ [ActionPlanner] ───▶ Decides Action Plan (GenerateQuiz, Slide, Scorer...) │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
     ┌───────────────────────── Dispatcher ─────────────────────────┐
     │                                                              │
(Direct Executions)                                      (Needs Retrieval)
     │                                                              │
     ▼                                                              ▼
┌───────────────────────┐                    ┌──────────────────────────────┐
│  Specialist Handlers  │                    │     3. Adaptive RAG Agent    │
│  (Chat, Scorer, Stats,│                    │                              │
│   Review_Wrong)       │                    │    [QueryClassifier (Logic)] │
│                       │                    │   ──▶ STANDARD (BM25+Vector) │
│  ──▶ Direct Logic /   │                    │   ──▶ BROAD (Metadata Filter)│
│      [LLM Call]       │                    │   ──▶ CURRICULUM (Lessons)   │
└────────────┬──────────┘                    │   ──▶ HIERARCHICAL (HRAG)    │
             │                               │               │              │
             │                               │    [Cross-Encoder Reranker]  │
             │                               └───────────────┬──────────────┘
             │                                               ▼
             │                               ┌──────────────────────────────┐
             │                               │  4. Generation & Validator   │
             │                               │                              │
             │                               │ [Generator LLM] (in Handlers)│
             │                               │  [  Next LLM Call  ]         │
             │                               │               │              │
             │                               │               ▼              │
             │                               │ [Validator Agent] (Reflect)  │
             │                               │  [  Validation LLM Call  ]   │
             │                               └───────────────┬──────────────┘
             └───────────────────────┬───────────────────────┘
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│             Final Response Output & Auto-Save Session State               │
└───────────────────────────────────────────────────────────────────────────┘
```

### 2.1. Context Extraction & Intent Routing

When the system receives a natural language query:

1. **ContextAnalyzer**: Evaluates if the query requires historical session context. If true, it extracts past conversations and injects them into the query.
2. **IntentDetector Agent**: Performs the first major **LLM Call** to run semantic analysis extracting 4 key entities:
   - `intent`: The actual purpose (Chat, Generate Question, Explain, Answer, Review, etc.).
   - `task_type`: Desired output format (e.g., `mcq`, `essay`).
   - `topic`: The knowledge topic the user is targeting.
   - `grade`: The grade level if specified.

### 2.2. Core Orchestration (Pure Code)

To optimize latency, routing and state management are handled strictly by pure Python code logic:

1. **SessionManager**: Resolves and syncs the current session state via memory or JSON storage based on intent and topic.
2. **ActionPlanner**: Consumes the context and state to chart an `ActionPlan` mapping to specific internal tools (e.g., `GENERATE_QUIZ`, `EXPLAIN_CONCEPT`, `CHECK_ANSWER`).
3. **Dispatcher**: Forwards the request into designated **Specialist Handlers** (e.g., `MCQHandler`, `Scorer`, `SlideHandler`). Actions requiring curriculum knowledge activate the RAG pipeline.

### 2.3. Adaptive RAG Agent

Instead of a flat pipeline, the system uses an `AdaptiveRAGAgent` that observes the query intent and dynamically decides the most performant retrieval strategy using `QueryClassifier`:

- **STANDARD**: For regular specific queries, implementing Hybrid Search (Lexical Custom BM25 + Semantic Cosine Similarity) followed by RRF normalization.
- **BROAD**: For overall overview queries, heavily relies on Document Metadata filtering filtering top-level objective chunks.
- **CURRICULUM**: Rapid metadata aggregation over the curriculum textbook structure returning lesson topics.
- **HIERARCHICAL (HRAG)**: A complex Two-Phase setup. Phase 1 runs semantic search purely on Coarse/Parent chunks (Level 1-2). Phase 2 executes a scoped Hybrid Search isolated on the Fine/Child chunks (Level 3+) belonging strictly to Phase 1 parents.

All retrieved chunks are subjected to **Cross-Encoder Reranking** filtering out non-relevant duplications using linear vector distances.

### 2.4. Generation & Self-Reflection

Filtered chunks act as the grounded context fed into the Handler's **Generator LLMs** for generation (**Next LLM Call**).
The output (Formatted JSON Data, Markdown, HTML Slides) is intercepted by a recursive **Self-Reflection mechanism** using the `Validator Agent` (**Validation LLM Call**). This Agent reflects and cross-checks the response against original contexts and strict evaluation rubrics, optionally triggering regeneration until structural and logical requirements are fully met.

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
