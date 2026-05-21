from src.llm.agents.base import BaseAgent
from src.llm.handlers.content.slide_agents import ContentAgent
from src.schemas.agent_protocol import AgentTask, AgentTaskResult


class ContentDraftingAgent(BaseAgent):
    agent_id = "content_drafting_agent"
    default_error_code = "CONTENT_DRAFTING_AGENT_ERROR"

    def _run(self, task: AgentTask) -> AgentTaskResult:
        inputs = task.inputs
        outline_payload = inputs.get("outline_payload") or {}
        outline_slides = outline_payload.get("slides", inputs.get("outline_slides") or [])

        agent = ContentAgent()
        result = agent.run(
            outline_slides=outline_slides,
            chunk_map=inputs.get("chunk_map") or {},
            task_type=inputs.get("task_type", "slide"),
            revision_instruction=task.revision_instruction,
        )

        used_tools = ["llm_generation"]
        if inputs.get("chunk_map"):
            used_tools.append("chunk_lookup")

        return AgentTaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            status=result.status,
            artifact_type=task.expected_artifact or "content_payload",
            artifact=result.payload or {},
            confidence=0.85 if result.status == "success" else None,
            used_tools=used_tools,
            latency_ms=result.latency_ms,
            error_code=result.error_code,
            error_message=result.error_message,
        )


__all__ = ["ContentDraftingAgent"]
