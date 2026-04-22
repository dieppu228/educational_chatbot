"""
Tools — Wrap existing agents thành LangChain tools cho supervisor.

Mỗi tool:
    - Dùng InjectedState để truy cập large data (context_map, chunk_map)
    - Gọi agent logic hiện tại (giữ nguyên)
    - Trả về JSON string cho supervisor messages

HITL: generate_outline có interrupt() để user review dàn ý.
"""

import json
import logging
from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from langgraph.types import interrupt

logger = logging.getLogger("chatbot.graph.tools")


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
    """Thiết kế dàn ý (outline) bài giảng / giáo án gồm 7-12 slides/sections.
    Gọi tool này ĐẦU TIÊN trước bất kỳ tool nào khác.
    Sau khi tạo outline, user sẽ được review và có thể chỉnh sửa."""

    from src.llm.handlers.content.slide_agents import OutlineAgent

    context_map = state.get("context_map", "")
    task_type = state.get("task_type", "slide")

    if not context_map:
        return json.dumps({"error": "Chưa có context_map. Cần preprocess trước.", "status": "failed"})

    agent = OutlineAgent()
    result = agent.run(
        context_map=context_map,
        topic=topic,
        grade=grade,
        book=book,
        task_type=task_type,
    )

    if result.status == "failed":
        logger.warning(f"Outline agent failed: {result.error_message}")
        return json.dumps({"error": result.error_message, "status": "failed"})

    # ── HITL: pause cho user review ──
    task_label = "giáo án" if task_type == "lesson_plan" else "bài giảng"
    feedback = interrupt({
        "type": "outline_review",
        "outline": result.payload,
        "message": f"Dàn ý {task_label} đã được tạo. Bạn có muốn chỉnh sửa không?",
    })

    # User có thể approve (True) hoặc gửi edited outline (dict)
    if isinstance(feedback, dict) and "edited_outline" in feedback:
        logger.info("User edited outline — sử dụng bản chỉnh sửa")
        return json.dumps(feedback["edited_outline"])

    logger.info(f"Outline approved: {len(result.payload.get('slides', []))} slides")
    return json.dumps(result.payload)


# ════════════════════════════════════════════════════════
# TOOL 2: Generate Content (CRITICAL, cần outline trước)
# ════════════════════════════════════════════════════════

@tool
def generate_content(
    state: Annotated[dict, InjectedState],
) -> str:
    """Viết nội dung chi tiết cho từng slide/section dựa trên outline đã được duyệt.
    CHỈ gọi tool này SAU KHI generate_outline đã hoàn thành."""

    from src.llm.handlers.content.slide_agents import ContentAgent

    outline_payload = state.get("outline_payload")
    chunk_map = state.get("chunk_map", {})
    task_type = state.get("task_type", "slide")

    if not outline_payload:
        return json.dumps({"error": "Chưa có outline. Gọi generate_outline trước.", "status": "failed"})

    outline_slides = outline_payload.get("slides", [])
    if not outline_slides:
        return json.dumps({"error": "Outline trống.", "status": "failed"})

    agent = ContentAgent()
    result = agent.run(
        outline_slides=outline_slides,
        chunk_map=chunk_map,
        task_type=task_type,
    )

    if result.status == "failed":
        logger.warning(f"Content agent failed: {result.error_message}")
        return json.dumps({"error": result.error_message, "status": "failed"})

    logger.info(f"Content generated: {len(result.payload.get('slides', []))} slides")
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
    """Gợi ý media minh họa (hình ảnh, biểu đồ) cho slide.
    Tool này OPTIONAL — có thể gọi song song với các tool khác."""

    from src.llm.handlers.content.slide_agents import MediaAgent

    agent = MediaAgent()
    result = agent.run(topic=topic, grade=grade, book=book)

    if result.status == "failed":
        logger.warning(f"Media agent failed: {result.error_message}")
        return json.dumps({"hero_media": [], "inline_media": [], "status": "failed"})

    logger.info("Media suggestions generated")
    return json.dumps(result.payload)


# ════════════════════════════════════════════════════════
# TOOL 4: Generate Quiz (OPTIONAL)
# ════════════════════════════════════════════════════════

@tool
def generate_quiz(
    topic: str,
    state: Annotated[dict, InjectedState],
) -> str:
    """Sinh 3-5 câu hỏi trắc nghiệm (MCQ) cho phần luyện tập.
    Tool này OPTIONAL — có thể gọi song song với các tool khác."""

    from src.llm.handlers.content.slide_agents import QuizAgent

    context = state.get("context_map", "")

    agent = QuizAgent()
    result = agent.run(topic=topic, context=context)

    if result.status == "failed":
        logger.warning(f"Quiz agent failed: {result.error_message}")
        return json.dumps({"quiz_items": [], "status": "failed"})

    logger.info(f"Quiz generated: {len(result.payload.get('quiz_items', []))} items")
    return json.dumps(result.payload)


# ════════════════════════════════════════════════════════
# TOOL 5: Merge Results
# ════════════════════════════════════════════════════════

@tool
def merge_results(
    state: Annotated[dict, InjectedState],
) -> str:
    """Merge kết quả từ outline, content, media, quiz thành danh sách slides hoàn chỉnh.
    Gọi SAU KHI ít nhất generate_outline và generate_content đã xong."""

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
    logger.info(f"Merged: {len(merged_dicts)} slides")
    return json.dumps({"slides": merged_dicts, "total": len(merged_dicts), "status": "success"})


# ════════════════════════════════════════════════════════
# TOOL 6: Quality Gate
# ════════════════════════════════════════════════════════

@tool
def check_quality(
    state: Annotated[dict, InjectedState],
) -> str:
    """Kiểm tra chất lượng slides đã merge. Nếu không đạt sẽ tự auto-fix.
    Gọi SAU merge_results."""

    from src.llm.services.slide_merger import SlideQualityGate
    from src.schemas.slide_schemas import MergedSlide

    merged_data = state.get("merged_slides")
    if not merged_data:
        return json.dumps({"passed": False, "issues": ["Chưa có slides để kiểm tra."]})

    # Parse slides
    slides_raw = merged_data.get("slides", []) if isinstance(merged_data, dict) else merged_data
    slides = []
    for s in slides_raw:
        if isinstance(s, dict):
            slides.append(MergedSlide(**s))
        elif isinstance(s, MergedSlide):
            slides.append(s)

    gate = SlideQualityGate()
    passed, issues = gate.validate(slides)

    if not passed:
        logger.warning(f"Quality gate failed: {issues}")
        fixed_slides = gate.auto_fix(slides, issues)
        passed_after_fix, issues_after = gate.validate(fixed_slides)
        return json.dumps({
            "passed": passed_after_fix,
            "auto_fixed": True,
            "issues": issues_after,
            "slides": [s.model_dump() for s in fixed_slides],
        })

    logger.info("Quality gate passed")
    return json.dumps({"passed": True, "issues": [], "slides": [s.model_dump() for s in slides]})


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
}


__all__ = ["ALL_TOOLS", "TOOL_STATE_MAPPING"]
