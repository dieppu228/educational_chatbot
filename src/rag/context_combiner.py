"""
ContextCombiner — Task-Aware Context Formatting.

Sau khi RAG trả về danh sách chunks, module này sắp xếp & format
context string tùy theo loại task:

    Task cụ thể (mcq, true_false, fill_blank, explain, chat):
        → Sort by rerank_score giảm dần, không group.
        → Chunk quan trọng nhất lên đầu.

    Task tổng hợp (slide, lesson_plan, essay):
        → Group by (topic_name → lesson_name).
        → Sort group theo thứ tự tự nhiên SGK (alphabetical).
        → Bên trong mỗi group: sort by score giảm dần.
"""

import logging
from collections import defaultdict
from typing import List, Dict, Optional

logger = logging.getLogger("chatbot.context_combiner")

# Actions yêu cầu giữ cấu trúc SGK (group by topic/lesson)
COMPREHENSIVE_ACTIONS = {
    "generate_slide", "generate_lesson_plan",
    "slide", "lesson_plan", "essay",
}

# Actions chỉ cần top chunks (sort by score)
SPECIFIC_ACTIONS = {
    "generate_quiz", "explain_concept", "chat",
    "mcq", "true_false", "fill_blank", "explain",
}


def format_contexts(
    contexts: List[Dict],
    action: Optional[str] = None,
) -> str:
    """
    Format danh sách chunks thành context string cho LLM prompt.

    Args:
        contexts: List[Dict] — mỗi dict có 'content', 'metadata', 'rerank_score'
        action: Action string từ ActionPlanner (VD: "generate_slide", "generate_quiz")
                Nếu None → dùng logic mặc định (sort by score).

    Returns:
        str: Context string đã format, sẵn sàng chèn vào prompt.
    """
    if not contexts:
        return "[Không có context]"

    if action and action in COMPREHENSIVE_ACTIONS:
        return _format_grouped(contexts)
    else:
        return _format_flat(contexts)


def _format_flat(contexts: List[Dict]) -> str:
    """
    Sort by rerank_score giảm dần → render đơn giản.

    Dùng cho: mcq, true_false, fill_blank, explain, chat.
    Chunk quan trọng nhất lên đầu → LLM thấy ngay thông tin cần thiết.
    """
    sorted_chunks = sorted(
        contexts,
        key=lambda c: c.get("rerank_score", 0),
        reverse=True,
    )

    formatted = []
    for i, ctx in enumerate(sorted_chunks, 1):
        content = ctx.get("content", "")
        formatted.append(f"Context {i}:\n{content}")

    return "\n\n---\n\n".join(formatted)


def _format_grouped(contexts: List[Dict]) -> str:
    """
    Group by (topic_name → lesson_name) → sort by score bên trong.

    Dùng cho: slide, lesson_plan, essay.
    Giữ nguyên flow kiến thức SGK để LLM sinh nội dung mạch lạc.

    Cấu trúc output:
        ## Chủ đề: <topic_name>
        ### Bài: <lesson_name>
        [Context 1] ...
        [Context 2] ...
    """
    # Group: topic_name → lesson_name → list of chunks
    groups: Dict[str, Dict[str, List[Dict]]] = defaultdict(lambda: defaultdict(list))

    for chunk in contexts:
        meta = chunk.get("metadata", {})
        topic_name = meta.get("topic_name", "Khác")
        lesson_name = meta.get("lesson_name", "Khác")
        groups[topic_name][lesson_name].append(chunk)

    # Sort groups theo thứ tự tự nhiên SGK (alphabetical)
    sorted_topics = sorted(groups.keys())

    formatted = []
    ctx_index = 1

    for topic in sorted_topics:
        formatted.append(f"## Chủ đề: {topic}")

        sorted_lessons = sorted(groups[topic].keys())

        for lesson in sorted_lessons:
            formatted.append(f"### Bài: {lesson}")

            # Sort chunks trong mỗi lesson theo rerank_score giảm dần
            lesson_chunks = sorted(
                groups[topic][lesson],
                key=lambda c: c.get("rerank_score", 0),
                reverse=True,
            )

            for chunk in lesson_chunks:
                content = chunk.get("content", "")
                score = chunk.get("rerank_score")
                score_tag = f" [score={score:.4f}]" if score is not None else ""
                formatted.append(f"Context {ctx_index}{score_tag}:\n{content}")
                ctx_index += 1

            formatted.append("")  # blank line giữa các lesson

    logger.info(
        f"ContextCombiner: grouped mode | "
        f"{len(sorted_topics)} topics, {ctx_index - 1} chunks"
    )

    return "\n\n".join(formatted)


__all__ = ["format_contexts"]
