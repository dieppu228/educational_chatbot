# Project context

EduBot is a Vietnamese high-school Computer Science RAG assistant. Runtime requests enter through `app/api.py`, flow through `src/llm/orchestrator.py`, and are dispatched to task services. Retrieval uses local chunks and embeddings by default. Slide and lesson-plan artifacts use the shared content-supervisor graph, specialist agents, deterministic merging, quality review, and optional PPTX export.

Important boundaries:

- `src/rag/` owns retrieval and context assembly.
- `src/llm/graphs/` owns the slide/lesson-plan LangGraph workflow.
- `src/llm/handlers/content/slide_agents/` owns LLM-facing content workers.
- `src/llm/services/slide_service.py` owns pipeline consumption, session persistence, and export attachment.
- `src/llm/services/slide_export_service.py` owns PPTX generation.
- `src/schemas/slide_schemas.py` is the shared contract for content artifacts.

Runtime configuration comes from process environment, then `.env`, with defaults in `src/config/config.py`. At minimum the live LLM path requires `GENAI_API_KEY`; media search additionally uses `TAVILY_API_KEY`. Export paths are controlled by `SLIDE_TEMPLATE_PATH`, `SLIDE_EXPORT_DIR`, and `SLIDE_DOWNLOAD_BASE_URL`.
