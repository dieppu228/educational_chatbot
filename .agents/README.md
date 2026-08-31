# Agent guidance

Read these files before changing the repository:

1. `PROJECT_CONTEXT.md` for runtime ownership and architecture boundaries.
2. `AGENT_RULES.md` for repository-specific safety and compatibility rules.
3. `TESTING_GUIDE.md` for focused and full verification commands.

The canonical runtime is the FastAPI app in `app/api.py`; notebooks and thesis artifacts are not runtime entrypoints. Long-form slide and lesson-plan generation uses the LangGraph content supervisor, while top-level request routing remains code-driven in the orchestrator.
