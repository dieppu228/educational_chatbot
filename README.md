# Intelligent Educational Assistant System (Educational Chatbot)

Graduation Thesis project to design and build an Intelligent Virtual Assistant supporting teaching and learning of Computer Science at the High School level (Grades 10-12). The system is developed based on the RAG (Retrieval-Augmented Generation) architecture combined with a Multi-Agent LLM approach to overcome information hallucination and enhance accuracy by closely following textbooks.

## 1. General Introduction

The system aims to provide a tool that automates complex academic tasks, serving both students and teachers.

**Core Functions:**

- **Knowledge Query (QA):** Answer questions based on a standardized textbook corpus (Canh Dieu and Ket Noi Tri Thuc).
- **Extraction and Question Generation (Quiz Generation):** Automatically initialize exercise systems in various formats (Multiple choice, Fill-in-the-blank, True/False, Essay) with customizable quantity and difficulty.
- **Evaluation and Scoring (Answer Scoring):** Automatically score answers and provide reasoning for corrections based on actual context instead of just keyword matching.
- **Lecture Structure Generation (Slide/Lesson Plan Generation):** Generate grounded slide decks or lesson-plan sections through a shared multi-agent content pipeline.
- **Media & Resource Suggestion:** Use a dedicated Media Research Agent to propose relevant visuals for generated teaching artifacts. MCP-backed image search is planned as an extension point.

---

## 2. Detailed System Pipeline

The system is engineered around a Clean Architecture approach with a **Thin Pipeline Controller (Orchestrator)** and **Multi-Intent Agentic Planning**, dynamically resolving up to 3 concurrent user intents per query without hardcoupled domain logic. The data flows encapsulated within a `RequestContext` through the following End-to-End steps:

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
│ [IntentRouter.detect_multi()] ─▶ Returns List[IntentResult] — max 3       │
│                                  (Intent, Task Type, Topic, Grade, Order) │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│              2. Core Pipeline Controller (Pure Code)                      │
│                                                                           │
│ [SessionManager] ──▶ Resolves Current Session State (Memory & Store)      │
│          │                                                                │
│ [ActionPlanner.plan_all()] ─▶ Returns List[ActionPlan] (deduped)          │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
        ┌──────────── Agentic Multi-Action Loop ────────────┐
        │  for each ActionPlan in List[ActionPlan]:         │
        │    ctx.intent_result ← swap to current sub-task   │
        │    [ExecutionDispatcher] ──▶ Domain Service        │
        │    Separator injected between multi-action outputs│
        └────────────────────┬──────────────────────────────┘
                             ▼
    ┌───────────────────────────────────────────────────────────────────────────┐
    │                         3. Domain Services                               │
    │                                                                           │
    │ • QuizService: standalone quiz generation, scoring, review, stats         │
    │ • SlideService: shared content pipeline for slides + lesson plans         │
    │ • Handlers: Explain, Chat, Fallback                                       │
    └────────────────────────────────────┬──────────────────────────────────────┘
                                         ▼
    ┌───────────────────────────────────────────────────────────────────────────┐
    │             4. Content Multi-Agent Pipeline (Slide/Lesson Plan)           │
    │                                                                           │
    │ [ContentSupervisor / LangGraph]                                           │
    │      │                                                                    │
    │      ├── AgentTask ─▶ PedagogyPlannerAgent      ─▶ outline_payload        │
    │      ├── AgentTask ─▶ ContentDraftingAgent      ─▶ content_payload        │
    │      ├── AgentTask ─▶ MediaResearchAgent        ─▶ media_payload          │
    │      ├── AgentTask ─▶ ContentAssessmentAgent    ─▶ embedded assessment    │
    │      ├── deterministic merge_results service    ─▶ merged_slides         │
    │      └── AgentTask ─▶ QualityReviewerAgent      ─▶ quality_review         │
    │                                                                           │
    │ Communication contract: AgentTask -> AgentTaskResult -> artifacts         │
    └────────────────────────────────────┬──────────────────────────────────────┘
                                         ▼
    ┌───────────────────────────────────────────────────────────────────────────┐
    │                   5. Tool / Retrieval Capability Layer                    │
    │                                                                           │
    │ [RAGService] -> [AdaptiveRAGAgent] -> Hybrid Search / HRAG / Reranker     │
    │ [MCPToolClient/MCPToolServer] -> optional external tools                  │
    └────────────────────────────────────┬──────────────────────────────────────┘
                                         ▼
    ┌───────────────────────────────────────────────────────────────────────────┐
    │                  6. Generation, Validation & Reflection                   │
    │                                                                           │
    │ • QuizService: Generator -> QualityReviewer -> QuestionValidator          │
    │ • Content pipeline: Specialist Agents -> Merge -> QualityReviewerAgent    │
    └────────────────────────────────────┬──────────────────────────────────────┘
                                         ▼
┌───────────────────────────────────────────────────────────────────────────┐
│   Streamed Response  ──▶  TraceService log  ──▶  SessionStore Auto-Save   │
└───────────────────────────────────────────────────────────────────────────┘
```

### 2.1. Context Extraction & Intent Routing

When the system receives a natural language query, it initializes a `RequestContext` object that flows through the entire pipeline:

1. **ContextAnalyzer**: Evaluates if the query requires historical session context. If true, it extracts past conversations using a Keyword/Recency hybrid scoring algorithm.
2. **QueryRewriter Agent**: When context enrichment occurs, it rewrites the single natural query into 2-3 semantically rich sub-queries optimized exclusively for deep RAG retrieval.
3. **IntentRouter Agent** (`detect_multi()`): Performs the first major **LLM Call** to run semantic analysis. Returns a `List[IntentResult]` (up to 3 items), each containing: `primary_intent`, `task_type`, `topic`, `grade`, `book`, and `is_new_topic`. Includes confidence-based filtering and a self-correction retry loop on parse failure.

### 2.2. Thin Pipeline Controller (Pure Code)

To optimize latency, all post-routing logic is entirely rule-based — zero additional LLM calls:

1. **SessionManager**: Resolves and syncs the current session context via Memory Manager or persistent JSON Storage (`session_store.py`) based on intent and topic compatibility.
2. **ActionPlanner** (`plan_all()`): Maps the full `List[IntentResult]` → `List[ActionPlan]` using pure rule-based logic. Deduplicates consecutive identical actions. Each `ActionPlan` contains an `Action` enum (e.g., `GENERATE_QUIZ`, `GENERATE_SLIDE`, `EXPLAIN_CONCEPT`) and execution metadata.
3. **Agentic Multi-Action Loop**: The Orchestrator iterates over all `ActionPlan`s. For each iteration, `ctx.intent_result` is swapped to align with the current sub-task before delegating to the `ExecutionDispatcher`. Multi-action outputs are separated by a visual delimiter in the streamed response.

### 2.3. Domain Services

Each dispatched action flows into its respective **Domain Service** (`QuizService`, `SlideService`) or **Handler** (`ExplainHandler`, `ChatHandler`).

- **QuizService** owns the standalone quiz lifecycle: generation, validation, answer scoring, review wrong questions, statistics, and `StudentTracker` updates. This stateful interaction layer stays service-based for maintainability.
- **SlideService** owns HITL resume, session persistence, display formatting, and delegates slide/lesson-plan generation to the content multi-agent pipeline.
- **Explain/Chat/Fallback handlers** execute narrower conversational tasks with RAG context when needed.

### 2.4. Content Multi-Agent Pipeline for Slide & Lesson Plan

Slide and lesson-plan generation share the same business workflow, so both are handled by one `ContentSupervisor` LangGraph pipeline. The difference is passed through `task_type` (`"slide"` or `"lesson_plan"`) and prompt/template constraints, not by duplicating supervisors.

Supervisor-sub-agent communication uses an internal A2A-lite contract:

```text
ContentSupervisor
  ── AgentTask ──▶ Specialist Agent
  ◀─ AgentTaskResult ── artifact + metadata
```

The specialist agents are:

1. **`PedagogyPlannerAgent`**: creates the learning outline and sequence.
2. **`ContentDraftingAgent`**: writes detailed slide content or lesson-plan sections from outline and source chunks.
3. **`MediaResearchAgent`**: proposes visual/media metadata. MCP-backed search can be plugged in later.
4. **`ContentAssessmentAgent`**: creates embedded assessment for the generated teaching artifact. This is not the standalone quiz flow.
5. **`QualityReviewerAgent`**: checks factuality, coverage, pedagogy, and format after merge.

`merge_results` remains a deterministic service/tool, not an agent. The graph records `agent_tasks`, `agent_results`, and an `artifacts` registry in `ContentSupervisorState`; `SlideService` persists only compact agent execution summaries in the session.

### 2.5. Retrieval and MCP Tool Layer

`RAGService` remains the main retrieval interface consumed by domain services. The codebase also includes an in-process MCP tool architecture (`MCPToolClient`, `MCPToolServer`, `ToolRegistry`) for standardized tool calls and future external capabilities.

Current tool candidates include:

1. **`knowledge_retrieval`**: wraps `RAGService` as a reusable tool.
2. **`content_formatter`**: formats chunks for downstream LLM prompts.
3. **`web_search`**: extension point for media/resource search.

The internal `AdaptiveRAGAgent` classifies the query using a heuristic-based `QueryClassifier` (no LLM) and selects the optimal retrieval strategy:

- **STANDARD**: For specific queries — Hybrid Search (Custom BM25 + Semantic Cosine) with RRF normalization → Cross-Encoder Reranking.
- **BROAD**: For overview queries — Metadata-only filter on `objective` chunks (1 per lesson). Falls back to STANDARD if fewer than 3 chunks returned.
- **CURRICULUM**: For curriculum-structure queries — Metadata aggregation returning deduplicated lesson list (topic + lesson name), no vector search.
- **HIERARCHICAL (HRAG)**: For specific queries with grade/topic context — Two-phase retrieval: Phase 1 semantic search on Level 1-2 (coarse) chunks to identify relevant lessons; Phase 2 scoped Hybrid+RRF search only on Level 3+ (fine) child chunks of selected parents → Reranker.

After retrieval, a **ContextCombiner** formats the retrieved chunks in a task-aware manner: grouping by topic/lesson for generative tasks (slides, lesson plans) or sorting by relevance score for targeted tasks (MCQ, explanation).

### 2.6. Generation & Self-Reflection

Filtered and reranked contexts act as the grounded information provided to the **Generator LLMs**.
Outputs corresponding to structured formats are intercepted by quality layers:

- Standalone quiz generation uses `QualityReviewer` and `QuestionValidator` before persisting `QuizRound` and `QuestionRecord`.
- Slide/lesson-plan generation uses `QualityReviewerAgent` after merging artifacts. If the reviewer requests revision, the supervisor routes back to the responsible specialist artifact (`outline`, `content`, or embedded assessment).

### 2.7. RAGAS Evaluation Pipeline

To quantitatively evaluate the RAG system's performance, the project integrates an independent automated evaluation pipeline:

- **Testset Generator:** Automatically synthesizes 50-100 random samples (Query, Ground Truth Answer) from the textbook JSON chunks.
- **RAGAS Evaluator:** Uses a standard framework to measure 4 coefficients: _Answer Relevancy_, _Faithfulness_, _Context Precision_, and _Context Recall_.

---

## 3. Repository Structure (Pipeline Modules)

The project's codebase focuses on a highly modular architecture, mapping perfectly to the End-to-End Pipeline. Below is the comprehensive structure of the `src/` directory:

```text
src/
├── llm/                        # CORE LLM & MULTI-AGENT ORCHESTRATION
│   ├── orchestrator.py         # Thin Pipeline Controller: coordinates the full E2E workflow & multi-action loop.
│   ├── intent_router.py        # Multi-Intent Router: detect_multi() returns List[IntentResult] (max 3 intents).
│   ├── action_planner.py       # Rule-based Planner: plan_all() maps List[IntentResult] → List[ActionPlan].
│   ├── execution_dispatcher.py # Registry Dispatcher: routes ActionPlan to the correct Domain Service.
│   ├── context_analyzer.py     # Context Extractor: Hybrid Keyword+Recency scoring on conversation history.
│   ├── query_rewriter.py       # Query Rewriter: expands query into 2-3 RAG-optimized sub-queries.
│   ├── prompts.py              # Prompt Hub: centralized repository of all LLM system prompts.
│   ├── memory.py               # In-memory Session Manager: tracks live session state per user.
│   ├── session_manager.py      # Session Resolver: determines continuity vs. new session creation.
│   ├── session_store.py        # Persistent Storage: serializes/deserializes sessions as JSON files.
│   ├── knowledge_map.py        # Knowledge Map: maps topic/lesson metadata for curriculum queries.
│   ├── student_profile.py      # Student Profile: tracks per-user learning history & performance stats.
│   ├── student_tracker.py      # Tracker: lightweight wrapper for profile update events.
│   ├── agents/                 # A2A-lite specialist agents for content generation:
│   │   ├── base.py             # BaseAgent: AgentTask -> AgentTaskResult contract.
│   │   ├── slide_planner.py    # PedagogyPlannerAgent: outline and learning sequence.
│   │   ├── content_drafting.py # ContentDraftingAgent: slide/lesson-plan section drafting.
│   │   ├── content_assessment.py # ContentAssessmentAgent: embedded assessment for content artifacts.
│   │   ├── media_research.py   # MediaResearchAgent: visual/media suggestions.
│   │   └── quality.py          # QualityReviewerAgent: artifact quality review.
│   ├── graphs/                 # LangGraph content supervisor pipeline:
│   │   ├── state.py            # ContentSupervisorState: messages, artifacts, agent logs.
│   │   ├── tools.py            # Agent dispatch adapters + deterministic merge tool.
│   │   └── content_supervisor.py # Supervisor routing, HITL, reflection, quality loop.
│   ├── validators/             # Self-Reflection Module:
│   │   └── question_validator.py  # Validates generated questions against source context & rubrics.
│   ├── services/               # Domain Services (high-level orchestration per task type):
│   │   ├── quiz_service.py     # QuizService: orchestrates Generate, Score, Review, Stats workflows.
│   │   ├── slide_service.py    # SlideService: HITL/session facade for slide & lesson-plan workflows.
│   │   ├── slide_merger.py     # Deterministic merge of outline/content/media/assessment artifacts.
│   │   └── quality_reviewer.py # Shared quality reviewer wrappers.
│   └── handlers/               # Atomic Task Executors:
│       ├── base_handler.py     # Abstract base: shared interface for all handlers.
│       ├── chat_handler.py     # Free-form conversational chat.
│       ├── explain_handler.py  # In-depth concept explanation with RAG context.
│       ├── fallback_handler.py # Graceful fallback for unrecognized or ambiguous intents.
│       ├── question/           # Question-type cluster:
│       │   ├── mcq_handler.py, essay_handler.py, fill_handler.py, true_false_handler.py
│       │   └── scorer.py       # Context-aware answer grading with rubric comparison.
│       └── content/            # Long-form content implementation workers:
│           ├── lesson_plan_handler.py  # Legacy lesson-plan handler.
│           └── slide_agents/           # Worker classes wrapped by src/llm/agents adapters.
│
├── tools/                      # MODEL CONTEXT PROTOCOL (MCP) ARCHITECTURE
│   ├── base_tool.py            # Base interface for all tools
│   ├── mcp_client.py           # Client interface for Agents/Services to call tools
│   ├── mcp_server.py           # In-process MCP server handling tool execution
│   ├── mcp_protocol.py         # Standard MCP schemas (Tool, ToolResult, etc.)
│   ├── schemas.py              # Pydantic schemas for specific tool inputs/outputs
│   └── implementations/        # Concrete tool implementations:
│       ├── tool_registry.py    # Registry managing available tools
│       ├── knowledge_retrieval_tool.py # Wraps RAGService as an MCP Tool
│       ├── web_search_tool.py          # Extension point for web/media search
│       └── content_formatter_tool.py   # Utility formatting tool
│
├── rag/                        # ADVANCED RAG PIPELINE
│   ├── rag_service.py          # RAGService: public interface consumed by Domain Services.
│   ├── adaptive_rag.py         # AdaptiveRAGAgent: heuristic QueryClassifier + 4-strategy retrieval.
│   ├── context_combiner.py     # ContextCombiner: task-aware post-retrieval formatting of chunks.
│   ├── retrieve_rebuild.py     # Core Search Engine: Custom BM25, Semantic Cosine, RRF, Scoped Search.
│   ├── embedding.py            # Embedding Module: Vietnamese HuggingFace SentenceTransformer (768-dim).
│   ├── reranker.py             # Cross-Encoder Reranker: noise filtering & relevance re-scoring.
│   └── chunking.py             # Data Engineering: Markdown → Hierarchical chunk tree (Level 1-4).
│
├── schemas/                    # DATA CONTRACTS & TYPE DEFINITIONS
│   ├── agent_protocol.py       # A2A-lite AgentTask / AgentTaskResult contracts.
│   ├── context.py              # RequestContext: the central state object flowing through the pipeline.
│   ├── llm_outputs.py          # Typed LLM output schemas (Quiz, Slide, LessonPlan structures).
│   ├── slide_schemas.py        # Content pipeline payloads and merged slide contracts.
│   └── rag_outputs.py          # Typed RAG output schemas (RAGResult, QueryProfile).
│
├── evaluation/                 # RAGAS EVALUATION PIPELINE
│   ├── run_eval.py             # CLI Controller: executes the full evaluation pipeline.
│   ├── testset_generator.py    # Synthetic QA generator from textbook chunk corpus.
│   ├── ragas_eval.py           # RAGAS metrics: Faithfulness, Relevancy, Precision, Recall.
│   ├── report.py               # Report Generator: visualizes RAGAS metric results.
│   └── data_collector.py       # Data Preparation: parses logs and datasets.
│
├── config/                     # CONFIGURATION HUB
│   └── config.py               # Central Config: API keys, LLM params (Gemini), paths.
│
└── utils/                      # UTILITIES & INFRASTRUCTURE
    ├── trace_service.py        # TraceService: structured request/response logging.
    ├── logger.py               # Logger setup and configuration.
    └── error_handling.py       # Centralized error handling utilities.
```

---

## 4. Tech Stack

The system is developed in separate modules to ensure high scalability.

**1. Core LLM & Orchestration:**

- **Language Model:** Google Gemini (`gemini-2.5-pro` & `gemini-2.5-flash`) via `google-genai` SDK.
- **Agent Management:** LangGraph coordinates the content supervisor; internal A2A-lite `AgentTask` / `AgentTaskResult` contracts connect the supervisor with specialist agents.

**2. Retrieval & Vector Core:**

- **Embedding Model:** `dangvantuan/vietnamese-document-embedding` (Based on `HuggingFaceEmbeddings` / `SentenceTransformer` architecture, 768 dimensions).
- **Reranker Model:** `AITeamVN/Vietnamese_Reranker` (Cross-Encoder architecture running on torch/CUDA).
- **Search Engine:** Vector space is mathematicalized using pure `Numpy` + a self-programmed `BM25 TF-IDF Analyzer` algorithm to avoid resource waste and native library dependencies (like FAISS).

**3. Infrastructure & UI:**

- **User Interface:** FastAPI serving the custom HTML/CSS/JavaScript frontend in `app/frontend`.
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

# 4. Launch API + UI Server Application
python app/api.py
```

Run the RAGAS Metric Report evaluation script (Optional):

```bash
python -m src.evaluation.run_eval --step all
```

---

_Student Information: Khac Diep (Hanoi University of Science and Technology)._
