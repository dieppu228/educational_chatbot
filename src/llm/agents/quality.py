from src.llm.agents.base import BaseAgent
from src.llm.services.quality_reviewer import get_quality_reviewer
from src.schemas.agent_protocol import AgentTask, AgentTaskResult


class QualityReviewerAgent(BaseAgent):
    agent_id = "quality_reviewer_agent"
    default_error_code = "QUALITY_AGENT_ERROR"

    def _run(self, task: AgentTask) -> AgentTaskResult:
        inputs = task.inputs
        task_type = inputs.get("task_type", "slide")
        reviewer = get_quality_reviewer(task_type)
        review = reviewer.review(
            query=inputs.get("query", ""),
            context=inputs.get("context", ""),
            output=inputs.get("output"),
        )
        artifact = review.model_dump()

        return AgentTaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            status="success" if review.passed else "blocked",
            artifact_type=task.expected_artifact or "quality_review",
            artifact=artifact,
            confidence=min(max(review.score / 10, 0), 1),
            used_tools=["llm_review"],
            error_code=review.reason_fail,
            error_message=None if review.passed else review.summary,
        )


__all__ = ["QualityReviewerAgent"]
