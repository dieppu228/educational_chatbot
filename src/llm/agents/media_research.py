from src.llm.agents.base import BaseAgent
from src.llm.handlers.content.slide_agents import MediaAgent
from src.schemas.agent_protocol import AgentTask, AgentTaskResult


class MediaResearchAgent(BaseAgent):
    agent_id = "media_research_agent"
    default_error_code = "MEDIA_AGENT_ERROR"

    def _run(self, task: AgentTask) -> AgentTaskResult:
        inputs = task.inputs
        agent = MediaAgent()
        result = agent.run(
            topic=inputs.get("topic", ""),
            grade=inputs.get("grade", ""),
            book=inputs.get("book", ""),
        )

        return AgentTaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            status=result.status,
            artifact_type=task.expected_artifact or "media_payload",
            artifact=result.payload or {},
            confidence=0.75 if result.status == "success" else None,
            used_tools=["llm_generation"],
            latency_ms=result.latency_ms,
            error_code=result.error_code,
            error_message=result.error_message,
        )


__all__ = ["MediaResearchAgent"]
