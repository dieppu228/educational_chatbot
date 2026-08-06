from typing import Any, Dict, Mapping


def _preview(value: Any, max_len: int = 600) -> Any:
    if isinstance(value, str):
        return value if len(value) <= max_len else value[:max_len] + "..."
    if isinstance(value, list):
        return [_preview(item, max_len=max_len) for item in value[:5]]
    if isinstance(value, dict):
        return {key: _preview(val, max_len=max_len) for key, val in list(value.items())[:20]}
    return value


def serialize_agent_task(task: Any) -> Dict[str, Any]:
    if hasattr(task, "to_dict"):
        data = task.to_dict()
    elif isinstance(task, Mapping):
        data = dict(task)
    else:
        data = getattr(task, "__dict__", {"value": repr(task)})

    return _preview(data)


def serialize_agent_result(result: Any) -> Dict[str, Any]:
    if hasattr(result, "to_dict"):
        data = result.to_dict()
    elif isinstance(result, Mapping):
        data = dict(result)
    else:
        data = getattr(result, "__dict__", {"value": repr(result)})

    return _preview(data)


def serialize_supervisor_state(state: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "request_id": state.get("request_id"),
        "task_type": state.get("task_type"),
        "topic": state.get("topic"),
        "grade": state.get("grade"),
        "book": state.get("book"),
        "status": state.get("status"),
        "agent_results": _preview(state.get("agent_results", {}), max_len=300),
        "quality_review": _preview(state.get("quality_review", {}), max_len=300),
    }


__all__ = ["serialize_agent_result", "serialize_agent_task", "serialize_supervisor_state"]

