from src.llm.agents.base import BaseAgent
from src.llm.handlers.content.slide_agents import OutlineAgent
from src.schemas.agent_protocol import AgentTask, AgentTaskResult


class PedagogyPlannerAgent(BaseAgent):
    agent_id = "pedagogy_planner_agent"
    default_error_code = "PLANNER_AGENT_ERROR"

    def _run(self, task: AgentTask) -> AgentTaskResult:
        inputs = task.inputs
        agent = OutlineAgent()
        result = agent.run(
            context_map=inputs.get("context_map", ""),
            topic=inputs.get("topic", ""),
            grade=inputs.get("grade", ""),
            book=inputs.get("book", ""),
            task_type=inputs.get("task_type", "slide"),
            revision_instruction=task.revision_instruction,
        )

        return AgentTaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            status=result.status,
            artifact_type=task.expected_artifact or "outline_payload",
            artifact=result.payload or {},
            confidence=0.9 if result.status == "success" else None,
            used_tools=["llm_generation"],
            latency_ms=result.latency_ms,
            error_code=result.error_code,
            error_message=result.error_message,
        )


__all__ = ["PedagogyPlannerAgent"]
