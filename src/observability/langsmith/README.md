# LangSmith tracing skeleton

This folder keeps LangSmith instrumentation separate from business logic.
The first target is the multi-agent supervisor pipeline in:

- `src/llm/graphs/content_supervisor.py`
- `src/llm/graphs/tools.py`
- `src/llm/agents/base.py`

## Environment

Tracing is disabled by default. Enable it only when running local experiments:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_PROJECT=educational-chatbot-multi-agent
export LANGSMITH_API_KEY=...
```

Optional endpoint override:

```bash
export LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

## Suggested trace hierarchy

```text
content_supervisor_pipeline
  preprocess
  supervisor
  generate_outline tool
    pedagogy_planner_agent
  generate_content tool
    content_drafting_agent
  generate_media tool
    media_research_agent
  generate_quiz tool
    content_assessment_agent
  quality_review tool
    quality_reviewer_agent
  reflection_decision
```

## Metadata contract

Every supervisor trace should include:

```text
request_id
task_type
topic
grade
book
status
reflection_attempts
quality_blocked
```

Every agent trace should include:

```text
task_id
from_agent
to_agent
task_type
expected_artifact
```

## Rollout plan

1. Keep existing local logs in `src/utils/trace_service.py`.
2. Add LangSmith decorators only to the multi-agent supervisor path.
3. Start with `BaseAgent.run_task()` because all specialist agents pass through it.
4. Add tool-level traces in `src/llm/graphs/tools.py`.
5. Add supervisor node traces in `src/llm/graphs/content_supervisor.py`.

This keeps the learning scope small and avoids touching unrelated RAG QA code.
