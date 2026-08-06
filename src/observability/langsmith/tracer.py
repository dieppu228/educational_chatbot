from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Dict, Iterable, Optional

from src.observability.langsmith.config import get_langsmith_settings

try:
    from langsmith import traceable, tracing_context
except Exception:  # pragma: no cover - optional dependency
    traceable = None
    tracing_context = None


def _noop_decorator(func: Callable) -> Callable:
    return func


def _traceable_or_noop(
    *,
    name: str,
    run_type: str,
    tags: Optional[Iterable[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Callable[[Callable], Callable]:
    settings = get_langsmith_settings()
    if not settings.enabled or traceable is None:
        return _noop_decorator

    return traceable(
        name=name,
        run_type=run_type,
        project_name=settings.project,
        tags=list(tags or []),
        metadata=metadata or {},
    )


def trace_supervisor(name: str, **metadata: Any) -> Callable[[Callable], Callable]:
    return _traceable_or_noop(
        name=name,
        run_type="chain",
        tags=["multi-agent", "supervisor"],
        metadata=metadata,
    )


def trace_agent(agent_id: str, **metadata: Any) -> Callable[[Callable], Callable]:
    return _traceable_or_noop(
        name=agent_id,
        run_type="chain",
        tags=["multi-agent", "agent"],
        metadata=metadata,
    )


def trace_tool(tool_name: str, **metadata: Any) -> Callable[[Callable], Callable]:
    return _traceable_or_noop(
        name=tool_name,
        run_type="tool",
        tags=["multi-agent", "tool"],
        metadata=metadata,
    )


def trace_chain(name: str, **metadata: Any) -> Callable[[Callable], Callable]:
    return _traceable_or_noop(
        name=name,
        run_type="chain",
        tags=["multi-agent"],
        metadata=metadata,
    )


@contextmanager
def langsmith_tracing_context(enabled: Optional[bool] = None, project_name: Optional[str] = None):
    settings = get_langsmith_settings()
    should_trace = settings.enabled if enabled is None else enabled

    if tracing_context is None:
        yield
        return

    with tracing_context(
        enabled=should_trace,
        project_name=project_name or settings.project,
    ):
        yield


def traced_call(
    func: Callable,
    *,
    name: str,
    run_type: str = "chain",
    tags: Optional[Iterable[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Callable:
    decorator = _traceable_or_noop(
        name=name,
        run_type=run_type,
        tags=tags,
        metadata=metadata,
    )

    @decorator
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


__all__ = [
    "langsmith_tracing_context",
    "trace_agent",
    "trace_chain",
    "trace_supervisor",
    "trace_tool",
    "traced_call",
]

