# Educational Chatbot for Vietnamese High School Computer Science

Graduation thesis project for building a textbook-grounded educational assistant for Vietnamese high school Computer Science (`Tin học THPT`), covering grades `10-12` and two textbook series: `Cánh Diều (CD)` and `Kết Nối Tri Thức (KNTT)`.

The project is organized as a research-oriented RAG system rather than a generic chatbot. The main goal is to answer questions and generate teaching artifacts while staying grounded in official textbook content.

Technical writing references used for the thesis:

- [`docs/project_technical_reference_vi.md`](docs/project_technical_reference_vi.md)
- [`docs/latex_writing_guidelines_vi.md`](docs/latex_writing_guidelines_vi.md)

## Scope

The current system supports three main task families:

- `Question answering` based on textbook content.
- `Quiz generation` and quiz-related interactions.
- `Slide / lesson-plan generation` through a multi-agent content pipeline.

The current codebase is still a thesis prototype. It already includes API, retrieval, orchestration, evaluation, and LaTeX thesis artifacts, but it is not yet a production-ready multi-user application.

## Current architecture

The implementation is centered around four layers.

### 1. Orchestration layer

The orchestration layer receives the user request, analyzes conversation context, detects intent, resolves session state, and dispatches the request to the correct service.

Main modules:

- `src/llm/orchestrator.py`
- `src/llm/context_analyzer.py`
- `src/llm/intent_router.py`
- `src/llm/action_planner.py`
- `src/llm/execution_dispatcher.py`
- `src/llm/session_manager.py`
- `src/llm/session_store.py`

### 2. Retrieval layer

The retrieval core uses:

- `keyword search` with a BM25-style implementation,
- `dense retrieval` with Vietnamese embeddings,
- `RRF` for rank fusion,
- optional `cross-encoder reranking`,
- `adaptive retrieval` strategies for different query types.

Main modules:

- `src/rag/rag_service.py`
- `src/rag/retrieve_rebuild.py`
- `src/rag/reranker.py`
- `src/rag/adaptive_rag.py`
- `src/rag/context_combiner.py`
- `src/rag/chunking.py`
- `src/rag/embedding.py`

### 3. Content generation layer

Long-form teaching artifacts such as slides and lesson plans are generated through a `supervisor-specialist` multi-agent workflow built on LangGraph.

Main modules:

- `src/llm/graphs/content_supervisor.py`
- `src/llm/graphs/state.py`
- `src/llm/graphs/tools.py`
- `src/llm/agents/slide_planner.py`
- `src/llm/agents/content_drafting.py`
- `src/llm/agents/media_research.py`
- `src/llm/agents/content_assessment.py`
- `src/llm/agents/quality.py`

### 4. Service and handler layer

This layer contains the task-specific business logic used by the orchestrator.

Main modules:

- `src/llm/services/quiz_service.py`
- `src/llm/services/slide_service.py`
- `src/llm/services/slide_merger.py`
- `src/llm/services/slide_export_service.py`
- `src/llm/handlers/question/*.py`
- `src/llm/handlers/chat_handler.py`
- `src/llm/handlers/explain_handler.py`
- `src/llm/handlers/fallback_handler.py`

## Repository structure

The repository is currently organized into these major areas:

```text
app/                    FastAPI app and static frontend
data/                   Local chunks, embeddings, benchmark files, eval outputs, sessions
docs/                   Technical notes and thesis-writing references
latex/                  Thesis source and generated PDF artifacts
plan/                   Internal writing / implementation plans
src/
  config/               Runtime settings
  evaluation/           Retrieval evaluation and RAGAS-related scripts
  llm/                  Orchestration, services, agents, graphs, handlers
  rag/                  Chunking, embeddings, retrieval, reranking
  schemas/              Shared contracts and structured outputs
  tools/                Internal tool abstractions
  utils/                Logging, tracing, upload helpers
CD/, KNTT/              Textbook-derived source material by series and grade
RawData/                Raw source assets used during preprocessing
```

## Data and artifacts

Important local files and folders:

- `data/rag_chunks_v2.json`: structured chunk corpus used by the runtime.
- `data/embeddings.npy`: dense embeddings for the chunk corpus.
- `data/embeddings.meta.json`: embedding metadata / fingerprint.
- `data/eval/retrieval/`: retrieval benchmark and reports.
- `data/eval/ragas/`: generation evaluation outputs.
- `data/sessions/`: persisted user/session state.

The default runtime path in `app/api.py` uses the local chunk file and local embedding file directly. Qdrant is still supported in the project for indexing and experimentation, but it is not the default path used by the API entrypoint.

## Evaluation status

The thesis evaluates the system at two separate nodes instead of only end-to-end.

### Retrieval evaluation

Retrieval is evaluated with a `single-gold` benchmark at lesson level.

Current benchmark files:

- `data/eval/retrieval/benchmark_eval.jsonl`
- `data/eval/retrieval/with_rerank/`

The main retrieval evaluation script is:

- `src/evaluation/eval_retrieval.py`

Example command:

```bash
python -m src.evaluation.eval_retrieval \
  --benchmark data/eval/retrieval/benchmark_eval.jsonl \
  --output-dir data/eval/retrieval/with_rerank
```

To run the same benchmark without reranking:

```bash
python -m src.evaluation.eval_retrieval \
  --benchmark data/eval/retrieval/benchmark_eval.jsonl \
  --output-dir data/eval/retrieval/no_rerank \
  --skip-rerank
```

### Generation evaluation

Generation quality is evaluated separately with RAGAS outputs stored under:

- `data/eval/ragas/eval_metrics.json`
- `data/eval/ragas/eval_metrics.csv`
- `data/eval/ragas/eval_report.md`

The current repo keeps the RAGAS outputs and supporting scripts under `src/evaluation/`, but the thesis results should be read from the generated files in `data/eval/ragas/`.

## Running the project

### Requirements

- Python 3.11+ is recommended.
- Install dependencies from `requirements.txt`.
- Set `GENAI_API_KEY` in `.env`.
- Make sure `data/rag_chunks_v2.json` and `data/embeddings.npy` already exist.

Install dependencies:

```bash
pip install -r requirements.txt
```

Minimal `.env`:

```env
GENAI_API_KEY=your_gemini_api_key
```

### Start the API + frontend

The current entrypoint is:

- `app/api.py`

Run:

```bash
python app/api.py
```

Default address:

- `http://127.0.0.1:8000`

Available endpoints:

- `POST /api/chat`
- `GET /api/frontend-info`
- `GET /api/exports/{file_id}`

The frontend is served from:

- `app/frontend/index.html`

## Rebuilding embeddings

If the chunk corpus changes, embeddings must be rebuilt.

Current embedding script:

```bash
python -m src.rag.embedding
```

By default, this script reads:

- `data/rag_chunks_v2.json`

and rewrites:

- `data/embeddings.npy`

The current implementation embeds `full_content` when available.

## Thesis artifacts

The thesis source is maintained in:

- `latex/DoAn.tex`
- `latex/Chuong/`

Generated evaluation results used in the thesis are stored in:

- `data/eval/retrieval/`
- `data/eval/ragas/`

## Notes

- This repository contains both research artifacts and runnable application code.
- Some notebooks and helper scripts are exploratory and were used during development; they should not be treated as the canonical runtime path.
- The current prototype is single-node and local-first. Full multi-user deployment, production-grade user management, and cross-subject expansion are future-work items, not completed features.
