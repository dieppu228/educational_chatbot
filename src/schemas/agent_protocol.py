from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Optional


AgentStatus = Literal["success", "partial", "failed", "blocked"]


@dataclass
class AgentTask:
    task_id: str
    from_agent: str
    to_agent: str
    task_type: str
    objective: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    context_refs: List[str] = field(default_factory=list)
    expected_artifact: Optional[str] = None
    revision_instruction: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentTask":
        return cls(
            task_id=data["task_id"],
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            task_type=data["task_type"],
            objective=data["objective"],
            inputs=data.get("inputs") or {},
            constraints=data.get("constraints") or {},
            context_refs=data.get("context_refs") or [],
            expected_artifact=data.get("expected_artifact"),
            revision_instruction=data.get("revision_instruction"),
        )


@dataclass
class AgentTaskResult:
    task_id: str
    agent_id: str
    status: AgentStatus
    task: Optional[Dict[str, Any]] = None
    artifact_type: Optional[str] = None
    artifact: Dict[str, Any] = field(default_factory=dict)
    confidence: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    used_tools: List[str] = field(default_factory=list)
    latency_ms: int = 0
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentTaskResult":
        return cls(
            task_id=data["task_id"],
            agent_id=data["agent_id"],
            status=data["status"],
            task=data.get("task"),
            artifact_type=data.get("artifact_type"),
            artifact=data.get("artifact") or {},
            confidence=data.get("confidence"),
            warnings=data.get("warnings") or [],
            used_tools=data.get("used_tools") or [],
            latency_ms=int(data.get("latency_ms") or 0),
            error_code=data.get("error_code"),
            error_message=data.get("error_message"),
        )


def is_agent_task_result(data: Any) -> bool:
    return (
        isinstance(data, dict)
        and "task_id" in data
        and "agent_id" in data
        and "status" in data
        and "artifact" in data
    )


__all__ = [
    "AgentStatus",
    "AgentTask",
    "AgentTaskResult",
    "is_agent_task_result",
]
