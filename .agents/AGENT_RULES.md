# Repository rules

- Preserve backward compatibility for persisted sessions and existing slide payloads; schema additions should use defaults.
- Keep slide and lesson-plan behavior separated by `task_type` even when they share services.
- Do not move LLM orchestration into PPTX rendering. Export decisions must be deterministic.
- Treat retrieved textbook chunks as the factual source of generated teaching content.
- Preserve media URL SSRF protections, redirect checks, response size limits, and graceful degradation.
- Do not edit generated frontend assets under `app/frontend/dist` directly; rebuild from `app/frontend/src`.
- Do not rewrite thesis or evaluation artifacts as part of runtime work unless explicitly requested.
- Existing user changes are authoritative. Inspect `git status` and avoid unrelated cleanup.
