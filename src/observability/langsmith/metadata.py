from typing import Any, Dict, Mapping


def _safe_get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key, default)
    return getattr(obj, key, default)


def build_supervisor_metadata(state: Mapping[str, Any]) -> Dict[str, Any]:
    """Extract stable metadata from ContentSupervisorState for trace filters."""

    return {
        "request_id": state.get("request_id"),
        "task_type": state.get("task_type"),
        "topic": state.get("topic"),
        "grade": state.get("grade"),
        "book": state.get("book"),
        "status": state.get("status"),
        "reflection_attempts": state.get("reflection_attempts"),
        "quality_blocked": state.get("quality_blocked"),
    }


def build_agent_task_metadata(task: Any) -> Dict[str, Any]:
    """Extract metadata from AgentTask without logging full prompt/context."""

    return {
        "task_id": _safe_get(task, "task_id"),
        "from_agent": _safe_get(task, "from_agent"),
        "to_agent": _safe_get(task, "to_agent"),
        "task_type": _safe_get(task, "task_type"),
        "expected_artifact": _safe_get(task, "expected_artifact"),
    }


__all__ = ["build_agent_task_metadata", "build_supervisor_metadata"]

