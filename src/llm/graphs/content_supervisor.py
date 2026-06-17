
import json
from typing import Dict, List, Any, Optional

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from src.llm.graphs.state import ContentSupervisorState
from src.llm.graphs.tools import ALL_TOOLS, TOOL_STATE_MAPPING
from src.llm.agents import QualityReviewerAgent
from src.llm.prompts import (
    SUPERVISOR_AFTER_CONTENT_PROMPT,
    SUPERVISOR_AFTER_OUTLINE_PROMPT,
    SUPERVISOR_REVISION_REQUEST_PROMPT,
    SUPERVISOR_SYSTEM_PROMPT,
    SUPERVISOR_USER_PROMPT,
)
from src.llm.services.slide_merger import SlideMerger
from src.schemas.agent_protocol import AgentTask
from src.schemas.slide_schemas import AgentResult
from src.schemas.agent_protocol import is_agent_task_result

# ── Config ──
RECURSION_LIMIT = 25
MAX_REFLECTION_ATTEMPTS = 2
REVISION_ACTIONS = {"revise_outline", "revise_content", "revise_quiz"}


# ════════════════════════════════════════════════════════
# GRAPH NODES
# ════════════════════════════════════════════════════════

def preprocess_node(state: ContentSupervisorState) -> dict:
    rag_chunks = state.get("rag_chunks", [])
    chunk_map: Dict[str, str] = {}
    grouped: Dict[str, Dict[str, List[str]]] = {}

    for i, chunk in enumerate(rag_chunks):
        chunk_id = f"c{i + 1}"
        content = chunk.get("content", "")
        chunk_map[chunk_id] = content

        meta = chunk.get("metadata", {})
        topic_name = meta.get("topic_name", "Khác")
        lesson_name = meta.get("lesson_name", "Khác")

        if topic_name not in grouped:
            grouped[topic_name] = {}
        if lesson_name not in grouped[topic_name]:
            grouped[topic_name][lesson_name] = []

        preview = content[:300] + "..." if len(content) > 300 else content
        grouped[topic_name][lesson_name].append(f"[{chunk_id}] {preview}")

    lines = []
    for topic_name in sorted(grouped.keys()):
        lines.append(f"## Chủ đề: {topic_name}")
        for lesson_name in sorted(grouped[topic_name].keys()):
            lines.append(f"### Bài: {lesson_name}")
            for chunk_text in grouped[topic_name][lesson_name]:
                lines.append(chunk_text)
            lines.append("")

    context_map = "\n".join(lines)



    # ── Synthesize context bằng ContextBuilder (LLM call) ──
    task_type = state.get("task_type", "slide")
    task_desc = "slide bài giảng" if task_type == "slide" else "giáo án bài giảng"
    query = state.get("query", "")
    action = f"generate_{task_type}"

    synthesized = ""
    try:
        from src.rag.context_builder import ContextBuilder
        builder = ContextBuilder()
        synthesized = builder.build(
            query=query,
            chunks=rag_chunks,
            action=action,
        )

    except Exception as e:
        synthesized = context_map  # Fallback: dùng raw grouped context

    # Build system message cho supervisor (synthesized_context → system prompt)
    system_msg = SUPERVISOR_SYSTEM_PROMPT.format(
        task_description=task_desc,
        topic=state.get("topic", ""),
        grade=state.get("grade", ""),
        book=state.get("book", ""),
        synthesized_context=synthesized,
    )

    user_msg = SUPERVISOR_USER_PROMPT.format(
        task_description=task_desc,
        topic=state.get("topic", ""),
        grade=state.get("grade", ""),
        book=state.get("book", ""),
    )

    return {
        "synthesized_context": synthesized,
        "context_map": context_map,
        "chunk_map": chunk_map,
        "messages": [
            SystemMessage(content=system_msg),
            HumanMessage(content=user_msg),
        ],
        "status": "processing",
    }


def supervisor_node(state: ContentSupervisorState) -> dict:
    from src.config.config import settings

    llm = ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        google_api_key=settings.GENAI_API_KEY,
        temperature=0.2,
    )
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    messages = list(state["messages"])

    # ── Post-HITL nudge: nếu đã có outline nhưng chưa có content → nhắc supervisor ──
    has_outline = state.get("outline_payload") is not None
    has_content = state.get("content_payload") is not None
    has_merged = state.get("merged_slides") is not None

    if has_outline and not has_content:
        messages.append(HumanMessage(content=SUPERVISOR_AFTER_OUTLINE_PROMPT))
    elif has_content and not has_merged:
        messages.append(HumanMessage(content=SUPERVISOR_AFTER_CONTENT_PROMPT))

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


def post_tool_processor(state: ContentSupervisorState) -> dict:
    updates = {}
    processed_state_keys = set()
    agent_results = list(state.get("agent_results", []))
    agent_tasks = list(state.get("agent_tasks", []))
    artifacts = dict(state.get("artifacts", {}))
    seen_results = {
        (r.get("task_id"), r.get("agent_id"))
        for r in agent_results
        if isinstance(r, dict)
    }
    seen_tasks = {
        t.get("task_id")
        for t in agent_tasks
        if isinstance(t, dict)
    }

    # Scan messages từ cuối lên, tìm ToolMessages mới nhất
    for msg in reversed(state.get("messages", [])):
        if not isinstance(msg, ToolMessage):
            continue

        tool_name = getattr(msg, "name", None)
        if tool_name and tool_name in TOOL_STATE_MAPPING:
            state_key = TOOL_STATE_MAPPING[tool_name]
            # Chỉ update nếu chưa có (lấy kết quả mới nhất)
            if state_key not in processed_state_keys:
                processed_state_keys.add(state_key)
                try:
                    parsed = json.loads(msg.content)
                    if is_agent_task_result(parsed):
                        result_key = (parsed.get("task_id"), parsed.get("agent_id"))
                        if result_key not in seen_results:
                            agent_results.append(parsed)
                            seen_results.add(result_key)

                        task = parsed.get("task")
                        if isinstance(task, dict) and task.get("task_id") not in seen_tasks:
                            agent_tasks.append(task)
                            seen_tasks.add(task.get("task_id"))

                        artifact_type = parsed.get("artifact_type") or state_key
                        artifact = parsed.get("artifact") or {}
                        if parsed.get("status") != "failed" or artifact:
                            artifacts[artifact_type] = artifact
                            updates[state_key] = artifact
                    # Bỏ qua kết quả lỗi legacy
                    elif isinstance(parsed, dict) and parsed.get("status") != "failed":
                        artifacts[state_key] = parsed
                        updates[state_key] = parsed
                except (json.JSONDecodeError, TypeError):
                    pass

    if agent_results != list(state.get("agent_results", [])):
        updates["agent_results"] = agent_results
    if agent_tasks != list(state.get("agent_tasks", [])):
        updates["agent_tasks"] = agent_tasks
    if artifacts != dict(state.get("artifacts", {})):
        updates["artifacts"] = artifacts

    return updates


def _latest_tool_name(state: ContentSupervisorState) -> Optional[str]:
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, ToolMessage):
            return getattr(msg, "name", None)
    return None


def reflection_decision_node(state: ContentSupervisorState) -> dict:
    review = state.get("quality_review")
    if not isinstance(review, dict):
        return {
            "status": "failed",
            "quality_blocked": True,
            "revision_instruction": "Quality reviewer không trả về JSON hợp lệ.",
            "error_message": "Quality review result missing or invalid.",
        }

    action = review.get("reflection_action", "block")
    passed = bool(review.get("passed"))
    attempts = int(state.get("reflection_attempts") or 0)
    instruction = (
        review.get("revision_instruction")
        or review.get("summary")
        or "Sửa output theo các issues của quality reviewer."
    )

    if passed and action == "approve":
        return {
            "status": "success",
            "quality_blocked": False,
            "revision_instruction": None,
        }

    if action in REVISION_ACTIONS and attempts < MAX_REFLECTION_ATTEMPTS:
        updates = {
            "reflection_attempts": attempts + 1,
            "revision_instruction": instruction,
            "quality_blocked": False,
            "messages": [HumanMessage(content=SUPERVISOR_REVISION_REQUEST_PROMPT.format(
                action=action,
                instruction=instruction,
            ))],
        }
        if action == "revise_outline":
            updates.update({
                "outline_payload": None,
                "content_payload": None,
                "merged_slides": None,
            })
        elif action == "revise_content":
            updates.update({
                "content_payload": None,
                "merged_slides": None,
            })
        elif action == "revise_quiz":
            updates.update({
                "quiz_payload": None,
                "merged_slides": None,
            })
        return updates

    return {
        "status": "failed",
        "quality_blocked": True,
        "revision_instruction": instruction,
        "error_message": f"Quality review blocked output: {review.get('reason_fail') or action}",
    }


# ════════════════════════════════════════════════════════
# ROUTING LOGIC
# ════════════════════════════════════════════════════════

def should_continue(state: ContentSupervisorState) -> str:
    messages = state.get("messages", [])
    if not messages:
        return END

    last_msg = messages[-1]

    # Check tool_calls
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"

    return END


def route_after_post_tool(state: ContentSupervisorState) -> str:
    latest_tool = _latest_tool_name(state)
    if latest_tool == "check_quality":
        return "reflection_decision"
    if state.get("content_payload") is not None and state.get("merged_slides") is None:
        return "merge_direct"
    if state.get("merged_slides") is not None and state.get("quality_review") is None:
        return "quality_direct"
    return "supervisor"


def merge_direct_node(state: ContentSupervisorState) -> dict:
    outline_payload = state.get("outline_payload") or {}
    content_payload = state.get("content_payload") or {}
    media_payload = state.get("media_payload") or {}
    quiz_payload = state.get("quiz_payload") or {}
    if not outline_payload or not content_payload:
        return {
            "status": "failed",
            "error_message": "Thiếu outline hoặc content để merge.",
        }

    merged = SlideMerger().merge(
        outline_result=AgentResult(agent="outline", status="success", payload=outline_payload, latency_ms=0),
        content_result=AgentResult(agent="content", status="success", payload=content_payload, latency_ms=0),
        media_result=AgentResult(
            agent="media",
            status="success" if media_payload else "failed",
            payload=media_payload or {},
            latency_ms=0,
        ),
        quiz_result=AgentResult(
            agent="quiz",
            status="success" if quiz_payload else "failed",
            payload=quiz_payload or {},
            latency_ms=0,
        ),
    )
    merged_dicts = [slide.model_dump() for slide in merged]
    artifact = {"slides": merged_dicts, "total": len(merged_dicts), "status": "success"}
    artifacts = dict(state.get("artifacts", {}))
    artifacts["merged_slides"] = artifact
    return {
        "merged_slides": artifact,
        "artifacts": artifacts,
    }


def quality_direct_node(state: ContentSupervisorState) -> dict:
    merged_data = state.get("merged_slides")
    if not merged_data:
        return {
            "quality_review": {
                "passed": False,
                "score": 0,
                "reason_fail": "FORMAT_INVALID",
                "summary": "Chưa có output để kiểm tra.",
                "issues": [],
                "reflection_action": "block",
                "revision_instruction": "Cần chạy lại merge_results trước khi quality check.",
                "requires_human_review": True,
            }
        }

    task = AgentTask(
        task_id=f"{state.get('request_id') or 'request'}:quality",
        from_agent="content_supervisor",
        to_agent="quality_reviewer_agent",
        task_type="review_content_quality",
        objective="Kiểm tra chất lượng factuality, coverage, pedagogy và format của output.",
        inputs={
            "task_type": state.get("task_type", "slide"),
            "query": state.get("query", ""),
            "context": state.get("synthesized_context") or state.get("context_map", ""),
            "output": merged_data,
        },
        constraints={
            "must_block_unsafe_or_ungrounded_output": True,
            "language": "vi",
        },
        expected_artifact="quality_review",
    )
    result = QualityReviewerAgent().run_task(task)
    result_dict = result.to_dict()
    review = result_dict.get("artifact") or {}
    agent_results = list(state.get("agent_results", []))
    agent_results.append(result_dict)
    artifacts = dict(state.get("artifacts", {}))
    artifacts["quality_review"] = review
    return {
        "quality_review": review,
        "agent_results": agent_results,
        "artifacts": artifacts,
    }


def route_after_reflection(state: ContentSupervisorState) -> str:
    if state.get("quality_blocked"):
        return END

    review = state.get("quality_review")
    if isinstance(review, dict) and review.get("passed") and review.get("reflection_action") == "approve":
        return END

    action = review.get("reflection_action") if isinstance(review, dict) else "block"
    if action in REVISION_ACTIONS and int(state.get("reflection_attempts") or 0) <= MAX_REFLECTION_ATTEMPTS:
        return "supervisor"

    return END


# ════════════════════════════════════════════════════════
# BUILD GRAPH
# ════════════════════════════════════════════════════════

def build_content_supervisor(checkpointer=None):
    if checkpointer is None:
        checkpointer = MemorySaver()

    # Tool node (standard LangGraph ToolNode)
    tool_node = ToolNode(ALL_TOOLS)

    # Build graph
    builder = StateGraph(ContentSupervisorState)

    # Nodes
    builder.add_node("preprocess", preprocess_node)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("tools", tool_node)
    builder.add_node("post_tool", post_tool_processor)
    builder.add_node("merge_direct", merge_direct_node)
    builder.add_node("quality_direct", quality_direct_node)
    builder.add_node("reflection_decision", reflection_decision_node)

    # Edges
    builder.add_edge(START, "preprocess")
    builder.add_edge("preprocess", "supervisor")

    # Supervisor → tools (nếu có tool_calls) hoặc → END
    builder.add_conditional_edges(
        "supervisor",
        should_continue,
        {"tools": "tools", END: END},
    )

    # Tools → post_tool → supervisor (vòng lặp)
    builder.add_edge("tools", "post_tool")
    builder.add_conditional_edges(
        "post_tool",
        route_after_post_tool,
        {
            "reflection_decision": "reflection_decision",
            "supervisor": "supervisor",
            "merge_direct": "merge_direct",
            "quality_direct": "quality_direct",
        },
    )
    builder.add_edge("merge_direct", "quality_direct")
    builder.add_edge("quality_direct", "reflection_decision")
    builder.add_conditional_edges(
        "reflection_decision",
        route_after_reflection,
        {
            "supervisor": "supervisor",
            END: END,
        },
    )

    graph = builder.compile(checkpointer=checkpointer)


    
    return graph


__all__ = ["build_content_supervisor", "RECURSION_LIMIT", "MAX_REFLECTION_ATTEMPTS"]
