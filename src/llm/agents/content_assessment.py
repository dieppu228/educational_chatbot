from src.llm.agents.base import BaseAgent
from src.llm.handlers.content.slide_agents import QuizAgent
from src.schemas.agent_protocol import AgentTask, AgentTaskResult


class ContentAssessmentAgent(BaseAgent):
    agent_id = "content_assessment_agent"
    default_error_code = "CONTENT_ASSESSMENT_AGENT_ERROR"

    def _run(self, task: AgentTask) -> AgentTaskResult:
        inputs = task.inputs
        agent = QuizAgent()
        result = agent.run(
            topic=inputs.get("topic", ""),
            context=inputs.get("context_map") or inputs.get("context", ""),
        )

        return AgentTaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            status=result.status,
            artifact_type=task.expected_artifact or "quiz_payload",
            artifact=result.payload or {},
            confidence=0.82 if result.status == "success" else None,
            used_tools=["llm_generation"],
            latency_ms=result.latency_ms,
            error_code=result.error_code,
            error_message=result.error_message,
        )


__all__ = ["ContentAssessmentAgent"]
