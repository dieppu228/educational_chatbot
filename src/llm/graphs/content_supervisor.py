
import json
from typing import Dict, List, Any, Optional

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from src.llm.graphs.state import ContentSupervisorState
from src.llm.graphs.tools import ALL_TOOLS, TOOL_STATE_MAPPING

# ── Config ──
RECURSION_LIMIT = 15


# ════════════════════════════════════════════════════════
# SYSTEM PROMPT cho Supervisor
# ════════════════════════════════════════════════════════

SUPERVISOR_SYSTEM_PROMPT = """Bạn là Content Supervisor — điều phối viên tạo nội dung giáo dục.

NHIỆM VỤ: Điều phối các công cụ (tools) để tạo {task_description}.
Bạn KHÔNG tự viết nội dung. Bạn CHỈ quyết định gọi tool nào, với tham số gì, theo thứ tự nào.

THÔNG TIN BÀI HỌC:
- Chủ đề: {topic}
- Lớp: {grade}
- Bộ sách: {book}

=== BỐI CẢNH KIẾN THỨC (để bạn hiểu phạm vi bài học, KHÔNG dùng để tự sinh nội dung) ===
{synthesized_context}

CÔNG CỤ CÓ SẴN:
1. generate_outline — Thiết kế dàn ý (GỌI ĐẦU TIÊN, bắt buộc). Sub-agent sẽ dùng tài liệu gốc để tạo outline.
2. generate_content — Viết nội dung chi tiết (cần outline trước). Sub-agent sẽ dùng tài liệu gốc.
3. generate_media — Gợi ý media minh họa (tùy chọn)
4. generate_quiz — Sinh câu hỏi luyện tập (tùy chọn)
5. merge_results — Ghép tất cả thành slides hoàn chỉnh (sau khi có outline + content)
6. check_quality — Kiểm tra chất lượng cuối (sau merge)

QUY TẮC NGHIÊM NGẶT:
- LUÔN gọi generate_outline TRƯỚC TIÊN
- generate_content CHỈ được gọi SAU KHI outline đã có
- merge_results CHỈ được gọi SAU KHI có outline + content
- check_quality CHỈ được gọi SAU merge_results
- Nếu một tool trả về lỗi, KHÔNG retry quá 1 lần
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

    # Scan messages từ cuối lên, tìm ToolMessages mới nhất
    for msg in reversed(state.get("messages", [])):
        if not isinstance(msg, ToolMessage):
            continue

        tool_name = getattr(msg, "name", None)
        if tool_name and tool_name in TOOL_STATE_MAPPING:
            state_key = TOOL_STATE_MAPPING[tool_name]
            # Chỉ update nếu chưa có (lấy kết quả mới nhất)
            if state_key not in updates:
                try:
                    parsed = json.loads(msg.content)
                    # Bỏ qua kết quả lỗi
                    if isinstance(parsed, dict) and parsed.get("status") != "failed":
                        updates[state_key] = parsed
                except (json.JSONDecodeError, TypeError):
                    pass



    return updates


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
    builder.add_edge("post_tool", "supervisor")

    graph = builder.compile(checkpointer=checkpointer)


    
    return graph


__all__ = ["build_content_supervisor", "RECURSION_LIMIT"]
