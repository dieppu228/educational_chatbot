
import json
import uuid
from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from langgraph.types import interrupt

from src.llm.agents import (
    ContentAssessmentAgent,
    ContentDraftingAgent,
    MediaResearchAgent,
    PedagogyPlannerAgent,
    QualityReviewerAgent,
)
from src.schemas.agent_protocol import AgentTask, AgentTaskResult


def _task_id(state: dict, suffix: str) -> str:
    request_id = state.get("request_id") or uuid.uuid4().hex[:8]
    return f"{request_id}:{suffix}"


def _dump_result(result: AgentTaskResult) -> str:
    return json.dumps(result.to_dict(), ensure_ascii=False)


def _failed_result(
    *,
    state: dict,
    suffix: str,
    to_agent: str,
    artifact_type: str,
    error_message: str,
    error_code: str = "INVALID_AGENT_INPUT",
) -> str:
    return _dump_result(AgentTaskResult(
        task_id=_task_id(state, suffix),
        agent_id=to_agent,
        status="failed",
        artifact_type=artifact_type,
        error_code=error_code,
        error_message=error_message,
    ))


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

    context_map = state.get("context_map", "")
    task_type = state.get("task_type", "slide")
    revision_instruction = state.get("revision_instruction")

    if not context_map:
        return _failed_result(
            state=state,
            suffix="outline",
            to_agent="pedagogy_planner_agent",
            artifact_type="outline_payload",
            error_message="Chưa có context_map. Cần preprocess trước.",
        )

    task = AgentTask(
        task_id=_task_id(state, "outline"),
        from_agent="content_supervisor",
        to_agent="pedagogy_planner_agent",
        task_type="plan_content_outline",
        objective="Thiết kế dàn ý bài giảng/giáo án từ context đã truy xuất.",
        inputs={
            "context_map": context_map,
            "topic": topic,
            "grade": grade,
            "book": book,
            "task_type": task_type,
        },
        constraints={
            "must_include_title": True,
            "must_include_summary": True,
            "must_include_exercise": task_type == "slide",
        },
        expected_artifact="outline_payload",
        revision_instruction=revision_instruction,
    )
    result = PedagogyPlannerAgent().run_task(task)

    if result.status == "failed":
        return _dump_result(result)

    if revision_instruction:
        return _dump_result(result)

    # ── HITL: pause cho user review ──
    task_label = "giáo án" if task_type == "lesson_plan" else "bài giảng"
    feedback = interrupt({
        "type": "outline_review",
        "outline": result.artifact,
        "message": f"Dàn ý {task_label} đã được tạo. Bạn có muốn chỉnh sửa không?",
    })

    # User có thể approve (True) hoặc gửi edited outline (dict)
    if isinstance(feedback, dict) and "edited_outline" in feedback:
        result.artifact = feedback["edited_outline"]
        result.warnings.append("Outline was edited by human feedback.")

    return _dump_result(result)


# ════════════════════════════════════════════════════════
# TOOL 2: Generate Content (CRITICAL, cần outline trước)
# ════════════════════════════════════════════════════════

@tool
def generate_content(
    state: Annotated[dict, InjectedState],
) -> str:
    """Viết nội dung chi tiết cho từng slide dựa trên outline."""

    outline_payload = state.get("outline_payload")
    chunk_map = state.get("chunk_map", {})
    task_type = state.get("task_type", "slide")

    if not outline_payload:
        return _failed_result(
            state=state,
            suffix="content",
            to_agent="content_drafting_agent",
            artifact_type="content_payload",
            error_message="Chưa có outline. Gọi generate_outline trước.",
        )

    outline_slides = outline_payload.get("slides", [])
    if not outline_slides:
        return _failed_result(
            state=state,
            suffix="content",
            to_agent="content_drafting_agent",
            artifact_type="content_payload",
            error_message="Outline trống.",
        )

    revision_instruction = state.get("revision_instruction")

    task = AgentTask(
        task_id=_task_id(state, "content"),
        from_agent="content_supervisor",
        to_agent="content_drafting_agent",
        task_type="draft_learning_content",
        objective="Viết nội dung chi tiết cho từng slide hoặc section giáo án dựa trên outline đã duyệt.",
        inputs={
            "outline_payload": outline_payload,
            "chunk_map": chunk_map,
            "task_type": task_type,
        },
        constraints={
            "max_bullets_per_slide": 6 if task_type != "lesson_plan" else None,
            "lesson_plan_requires_detailed_sections": task_type == "lesson_plan",
            "must_use_source_chunks": True,
            "language": "vi",
        },
        context_refs=list(chunk_map.keys()),
        expected_artifact="content_payload",
        revision_instruction=revision_instruction,
    )
    result = ContentDraftingAgent().run_task(task)

    if result.status == "failed":
        return _dump_result(result)

    return _dump_result(result)


# ════════════════════════════════════════════════════════
# TOOL 3: Generate Media (OPTIONAL)
# ════════════════════════════════════════════════════════

@tool
def generate_media(
    topic: str,
    grade: str,
    book: str,
    state: Annotated[dict, InjectedState],
) -> str:
    """Gợi ý media minh họa cho bài giảng."""

    task = AgentTask(
        task_id=_task_id(state, "media"),
        from_agent="content_supervisor",
        to_agent="media_research_agent",
        task_type="research_media",
        objective="Gợi ý media minh họa phù hợp với bài học.",
        inputs={
            "topic": topic,
            "grade": grade,
            "book": book,
            "outline_payload": state.get("outline_payload") or {},
            "content_payload": state.get("content_payload") or {},
        },
        constraints={
            "media_types": ["image", "gif"],
            "url_optional": True,
        },
        expected_artifact="media_payload",
    )
    result = MediaResearchAgent().run_task(task)

    if result.status == "failed":
        result.status = "partial"
        result.artifact = {"hero_media": [], "inline_media": []}

    return _dump_result(result)


# ════════════════════════════════════════════════════════
# TOOL 4: Generate Quiz (OPTIONAL)
# ════════════════════════════════════════════════════════

@tool
def generate_quiz(
    topic: str,
    state: Annotated[dict, InjectedState],
) -> str:
    """Sinh câu hỏi luyện tập cho bài giảng."""

    context = state.get("context_map", "")

    task = AgentTask(
        task_id=_task_id(state, "quiz"),
        from_agent="content_supervisor",
        to_agent="content_assessment_agent",
        task_type="generate_embedded_assessment",
        objective="Sinh câu hỏi hoặc hoạt động đánh giá nhúng trong artifact slide/giáo án.",
        inputs={
            "topic": topic,
            "context_map": context,
        },
        constraints={
            "question_type": "mcq",
            "max_questions": 5,
            "language": "vi",
        },
        expected_artifact="quiz_payload",
    )
    result = ContentAssessmentAgent().run_task(task)

    if result.status == "failed":
        result.status = "partial"
        result.artifact = {"quiz_items": []}

    return _dump_result(result)


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

    merged_data = state.get("merged_slides")
    if not merged_data:
        result = AgentTaskResult(
            task_id=_task_id(state, "quality"),
            agent_id="quality_reviewer_agent",
            status="blocked",
            artifact_type="quality_review",
            artifact={
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
            },
            error_code="FORMAT_INVALID",
            error_message="Chưa có output để kiểm tra.",
        )
        return _dump_result(result)

    task_type = state.get("task_type", "slide")
    task = AgentTask(
        task_id=_task_id(state, "quality"),
        from_agent="content_supervisor",
        to_agent="quality_reviewer_agent",
        task_type="review_content_quality",
        objective="Kiểm tra chất lượng factuality, coverage, pedagogy và format của output.",
        inputs={
            "task_type": task_type,
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
    return _dump_result(result)


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
