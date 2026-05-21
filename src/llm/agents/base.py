import time
from abc import ABC, abstractmethod

from src.schemas.agent_protocol import AgentTask, AgentTaskResult


class BaseAgent(ABC):
    agent_id: str = "base_agent"
    default_error_code: str = "AGENT_ERROR"

    def run_task(self, task: AgentTask) -> AgentTaskResult:
        t0 = time.time()
        try:
            result = self._run(task)
            if result.latency_ms <= 0:
                result.latency_ms = int((time.time() - t0) * 1000)
            if result.task is None:
                result.task = task.to_dict()
            return result
        except Exception as exc:
            return AgentTaskResult(
                task_id=task.task_id,
                agent_id=self.agent_id,
                status="failed",
                task=task.to_dict(),
                artifact_type=task.expected_artifact,
                latency_ms=int((time.time() - t0) * 1000),
                error_code=self.default_error_code,
                error_message=str(exc)[:200],
            )

    @abstractmethod
    def _run(self, task: AgentTask) -> AgentTaskResult:
        pass


__all__ = ["BaseAgent"]
