"""
StreamWrapper — Bridge giữa LangGraph graph.stream() và Python generator.

Chuyển đổi output dạng LangGraph chunks thành generator yield
để tương thích với SlideService interface hiện tại.
"""

import json
import logging
from typing import Generator, Dict, Any, Optional

from langgraph.types import Command

logger = logging.getLogger("chatbot.graph.stream")


def stream_graph_to_generator(
    graph,
    input_state: dict,
    config: dict,
) -> Generator[Dict[str, Any], None, None]:
    """
    Chạy graph.stream() và yield events dạng dict.

    Yields:
        {"type": "progress", "node": str, "data": dict}
        {"type": "interrupt", "data": list}  — HITL interrupt
        {"type": "result", "data": dict}     — final state

    Usage:
        for event in stream_graph_to_generator(graph, state, config):
            if event["type"] == "progress":
                print(f"Running: {event['node']}")
            elif event["type"] == "interrupt":
                # Handle HITL
                user_response = get_user_input(event["data"])
                # Resume with: graph.invoke(Command(resume=user_response), config)
    """
    try:
        for chunk in graph.stream(input_state, config=config):
            # Check for interrupt
            if "__interrupt__" in chunk:
                interrupt_data = chunk["__interrupt__"]
                logger.info(f"HITL interrupt detected: {interrupt_data}")
                yield {
                    "type": "interrupt",
                    "data": interrupt_data,
                }
                return  # Caller phải resume manually

            # Normal node output
            for node_name, node_output in chunk.items():
                if node_name.startswith("__"):
                    continue

                yield {
                    "type": "progress",
                    "node": node_name,
                    "data": node_output if isinstance(node_output, dict) else {},
                }

    except Exception as e:
        logger.error(f"Graph stream error: {e}")
        yield {
            "type": "error",
            "message": str(e),
        }


def invoke_graph_sync(
    graph,
    input_state: dict,
    config: dict,
) -> Dict[str, Any]:
    """
    Chạy graph.invoke() synchronous — đơn giản nhất.

    Returns:
        Final state dict hoặc dict chứa __interrupt__ nếu HITL.
    """
    try:
        result = graph.invoke(input_state, config=config)
        return result
    except Exception as e:
        logger.error(f"Graph invoke error: {e}")
        return {
            "status": "failed",
            "error_message": str(e),
        }


def resume_graph(
    graph,
    resume_value: Any,
    config: dict,
) -> Dict[str, Any]:
    """
    Resume graph sau HITL interrupt.

    Args:
        resume_value: User feedback — True (approve) hoặc dict (edited outline)
        config: Cùng config (thread_id) với lần invoke trước
    """
    try:
        result = graph.invoke(Command(resume=resume_value), config=config)
        return result
    except Exception as e:
        logger.error(f"Graph resume error: {e}")
        return {
            "status": "failed",
            "error_message": str(e),
        }


__all__ = ["stream_graph_to_generator", "invoke_graph_sync", "resume_graph"]
