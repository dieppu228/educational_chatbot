
import json
from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from langgraph.types import interrupt


# ════════════════════════════════════════════════════════
# TOOL 1: Generate Outline (CRITICAL + HITL)
# ════════════════════════════════════════════════════════

@tool
def generate_outline(
    topic: str,
    grade: str,
    book: str,
    state: Annotated[dict, InjectedState],
) -> str:
    """Tạo dàn ý bài giảng/giáo án từ context."""

    from src.llm.handlers.content.slide_agents import OutlineAgent

    context_map = state.get("context_map", "")
    task_type = state.get("task_type", "slide")
    revision_instruction = state.get("revision_instruction")

    if not context_map:
        return json.dumps({"error": "Chưa có context_map. Cần preprocess trước.", "status": "failed"})

    agent = OutlineAgent()
    result = agent.run(
        context_map=context_map,
        topic=topic,
        grade=grade,
        book=book,
        task_type=task_type,
        revision_instruction=revision_instruction,
    )

    if result.status == "failed":
        return json.dumps({"error": result.error_message, "status": "failed"})

    if revision_instruction:
        return json.dumps(result.payload)

    # ── HITL: pause cho user review ──
    task_label = "giáo án" if task_type == "lesson_plan" else "bài giảng"
    feedback = interrupt({
        "type": "outline_review",
        "outline": result.payload,
        "message": f"Dàn ý {task_label} đã được tạo. Bạn có muốn chỉnh sửa không?",
    })

    # User có thể approve (True) hoặc gửi edited outline (dict)
    if isinstance(feedback, dict) and "edited_outline" in feedback:
        return json.dumps(feedback["edited_outline"])

    return json.dumps(result.payload)


# ════════════════════════════════════════════════════════
# TOOL 2: Generate Content (CRITICAL, cần outline trước)
# ════════════════════════════════════════════════════════

@tool
def generate_content(
    state: Annotated[dict, InjectedState],
) -> str:
    """Viết nội dung chi tiết cho từng slide dựa trên outline."""

    from src.llm.handlers.content.slide_agents import ContentAgent

    outline_payload = state.get("outline_payload")
    chunk_map = state.get("chunk_map", {})
    task_type = state.get("task_type", "slide")

    if not outline_payload:
        return json.dumps({"error": "Chưa có outline. Gọi generate_outline trước.", "status": "failed"})

    outline_slides = outline_payload.get("slides", [])
    if not outline_slides:
        return json.dumps({"error": "Outline trống.", "status": "failed"})

    revision_instruction = state.get("revision_instruction")

    agent = ContentAgent()
    result = agent.run(
        outline_slides=outline_slides,
        chunk_map=chunk_map,
        task_type=task_type,
        revision_instruction=revision_instruction,
    )

    if result.status == "failed":
        return json.dumps({"error": result.error_message, "status": "failed"})

    return json.dumps(result.payload)


# ════════════════════════════════════════════════════════
# TOOL 3: Generate Media (OPTIONAL)
# ════════════════════════════════════════════════════════

@tool
def generate_media(
    topic: str,
    grade: str,
    book: str,
) -> str:
    """Gợi ý media minh họa cho bài giảng."""

    from src.llm.handlers.content.slide_agents import MediaAgent

    agent = MediaAgent()
    result = agent.run(topic=topic, grade=grade, book=book)

    if result.status == "failed":
        return json.dumps({"hero_media": [], "inline_media": [], "status": "failed"})

    return json.dumps(result.payload)


# ════════════════════════════════════════════════════════
# TOOL 4: Generate Quiz (OPTIONAL)
# ════════════════════════════════════════════════════════

@tool
def generate_quiz(
    topic: str,
    state: Annotated[dict, InjectedState],
) -> str:
    """Sinh câu hỏi luyện tập cho bài giảng."""

    from src.llm.handlers.content.slide_agents import QuizAgent

    context = state.get("context_map", "")

    agent = QuizAgent()
    result = agent.run(topic=topic, context=context)

    if result.status == "failed":
        return json.dumps({"quiz_items": [], "status": "failed"})

    return json.dumps(result.payload)


# ════════════════════════════════════════════════════════
# TOOL 5: Merge Results
# ════════════════════════════════════════════════════════

@tool
def merge_results(
    state: Annotated[dict, InjectedState],
) -> str:
    """Ghép outline + content + media + quiz thành slides hoàn chỉnh."""

    from src.llm.services.slide_merger import SlideMerger
    from src.schemas.slide_schemas import AgentResult

    outline_payload = state.get("outline_payload", {})
    content_payload = state.get("content_payload", {})
    media_payload = state.get("media_payload", {})
    quiz_payload = state.get("quiz_payload", {})

    if not outline_payload or not content_payload:
        return json.dumps({"error": "Thiếu outline hoặc content để merge.", "status": "failed"})

    # Wrap thành AgentResult cho merger
    outline_result = AgentResult(
        agent="outline", status="success", payload=outline_payload, latency_ms=0
    )
    content_result = AgentResult(
        agent="content", status="success", payload=content_payload, latency_ms=0
    )
    media_result = AgentResult(
        agent="media",
        status="success" if media_payload else "failed",
        payload=media_payload or {},
        latency_ms=0,
    )
    quiz_result = AgentResult(
        agent="quiz",
        status="success" if quiz_payload else "failed",
        payload=quiz_payload or {},
        latency_ms=0,
    )

    merger = SlideMerger()
    merged = merger.merge(
        outline_result=outline_result,
        content_result=content_result,
        media_result=media_result,
        quiz_result=quiz_result,
    )

    merged_dicts = [s.model_dump() for s in merged]
    return json.dumps({"slides": merged_dicts, "total": len(merged_dicts), "status": "success"})


# ════════════════════════════════════════════════════════
# TOOL 6: Quality Gate
# ════════════════════════════════════════════════════════

@tool
def check_quality(
    state: Annotated[dict, InjectedState],
) -> str:
    """Review chất lượng slide/giáo án sau khi merge."""

    from src.llm.services.quality_reviewer import get_quality_reviewer

    merged_data = state.get("merged_slides")
    if not merged_data:
        return json.dumps({
            "passed": False,
            "score": 0,
            "reason_fail": "FORMAT_INVALID",
            "summary": "Chưa có output để kiểm tra.",
            "issues": [{
                "case": "FORMAT_INVALID",
                "severity": "critical",
                "target": "merged_slides",
                "message": "merged_slides rỗng hoặc không tồn tại",
                "suggestion": "Kiểm tra lại bước merge_results",
            }],
            "reflection_action": "block",
            "revision_instruction": "Cần chạy lại merge_results trước khi quality check.",
            "requires_human_review": True,
        }, ensure_ascii=False)

    task_type = state.get("task_type", "slide")
    reviewer = get_quality_reviewer(task_type)
    review = reviewer.review(
        query=state.get("query", ""),
        context=state.get("synthesized_context") or state.get("context_map", ""),
        output=merged_data,
    )
    return json.dumps(review.model_dump(), ensure_ascii=False)


# ════════════════════════════════════════════════════════
# REGISTRY
# ════════════════════════════════════════════════════════

ALL_TOOLS = [
    generate_outline,
    generate_content,
    generate_media,
    generate_quiz,
    merge_results,
    check_quality,
]

# Map tool name → state field to store result
TOOL_STATE_MAPPING = {
    "generate_outline": "outline_payload",
    "generate_content": "content_payload",
    "generate_media": "media_payload",
    "generate_quiz": "quiz_payload",
    "merge_results": "merged_slides",
    "check_quality": "quality_review",
}


__all__ = ["ALL_TOOLS", "TOOL_STATE_MAPPING"]
