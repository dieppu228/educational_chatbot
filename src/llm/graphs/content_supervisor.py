
import json
from typing import Dict, List, Any, Optional

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from src.llm.graphs.state import ContentSupervisorState
from src.llm.graphs.tools import ALL_TOOLS, TOOL_STATE_MAPPING
from src.schemas.agent_protocol import is_agent_task_result

# ── Config ──
RECURSION_LIMIT = 25
MAX_REFLECTION_ATTEMPTS = 1
REVISION_ACTIONS = {"revise_outline", "revise_content", "revise_quiz"}


# ════════════════════════════════════════════════════════
# SYSTEM PROMPT cho Supervisor
# ════════════════════════════════════════════════════════

SUPERVISOR_SYSTEM_PROMPT = """Bạn là Content Supervisor — điều phối viên tạo nội dung giáo dục.

NHIỆM VỤ: Điều phối các specialist agent để tạo {task_description}.
Bạn KHÔNG tự viết nội dung. Bạn CHỈ quyết định delegate task nào, cho agent nào, theo thứ tự nào.
Các tool được bind dưới đây là adapter để gửi AgentTask và nhận AgentTaskResult từ specialist agents.

THÔNG TIN BÀI HỌC:
- Chủ đề: {topic}
- Lớp: {grade}
- Bộ sách: {book}

=== BỐI CẢNH KIẾN THỨC (để bạn hiểu phạm vi bài học, KHÔNG dùng để tự sinh nội dung) ===
{synthesized_context}

AGENT ADAPTERS CÓ SẴN:
1. generate_outline — Delegate cho PedagogyPlannerAgent thiết kế dàn ý (GỌI ĐẦU TIÊN, bắt buộc).
2. generate_content — Delegate cho ContentDraftingAgent viết nội dung chi tiết cho slide/section giáo án (cần outline trước).
3. generate_media — Delegate cho MediaResearchAgent gợi ý media minh họa (tùy chọn).
4. generate_quiz — Delegate cho ContentAssessmentAgent sinh đánh giá nhúng trong slide/giáo án (tùy chọn, KHÔNG phải quiz standalone).
5. merge_results — Deterministic service ghép tất cả artifacts thành slides hoàn chỉnh (sau khi có outline + content).
6. check_quality — Delegate cho QualityReviewerAgent kiểm tra chất lượng cuối (sau merge).

QUY TẮC NGHIÊM NGẶT:
- LUÔN gọi generate_outline TRƯỚC TIÊN
- generate_content CHỈ được gọi SAU KHI outline đã có
- merge_results CHỈ được gọi SAU KHI có outline + content
- check_quality CHỈ được gọi SAU merge_results
- Nếu một agent trả về lỗi, KHÔNG retry quá 1 lần
- Sau check_quality thành công, KHÔNG gọi thêm tool nào nữa — trả lời tóm tắt kết quả

THỨ TỰ KHUYẾN NGHỊ:
1. generate_outline(topic, grade, book)
2. generate_content()
3. generate_media(topic, grade, book) + generate_quiz(topic) [tùy chọn]
4. merge_results()
5. check_quality()
6. Trả lời: "Đã tạo xong [N] slides cho bài [tên bài]."
"""


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

    user_msg = (
        f"Hãy tạo {task_desc} cho chủ đề '{state.get('topic', '')}', "
        f"lớp {state.get('grade', '')}, bộ sách {state.get('book', '')}. "
        f"Bắt đầu bằng cách gọi generate_outline()."
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
        messages.append(HumanMessage(
            content=(
                "Outline đã được duyệt. Bây giờ hãy tiếp tục workflow: "
                "1) Gọi generate_content() để viết nội dung chi tiết, "
                "2) Gọi generate_media() và generate_quiz() nếu cần, "
                "3) Gọi merge_results() để ghép slides, "
                "4) Gọi check_quality() để kiểm tra. "
                "KHÔNG trả lời text — hãy gọi generate_content() NGAY."
            )
        ))
    elif has_content and not has_merged:
        messages.append(HumanMessage(
            content=(
                "Content đã sẵn sàng. Hãy gọi merge_results() để ghép "
                "outline + content thành slides hoàn chỉnh. "
                "KHÔNG trả lời text — hãy gọi merge_results() NGAY."
            )
        ))

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
            "messages": [HumanMessage(content=(
                "Quality reviewer yêu cầu sửa output trước khi trả cho user.\n"
                f"Action: {action}\n"
                f"Instruction: {instruction}\n"
                "Hãy gọi tool phù hợp để regenerate phần bị lỗi, sau đó merge_results và check_quality lại."
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
    return "supervisor"


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
        },
    )
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
