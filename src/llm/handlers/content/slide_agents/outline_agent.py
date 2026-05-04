
import logging
from src.llm.handlers.content.slide_agents.base_slide_agent import BaseSlideAgent
from src.llm.prompts import SLIDE_OUTLINE_TEMPLATE, LESSON_PLAN_OUTLINE_TEMPLATE

logger = logging.getLogger("chatbot.slide_agent.outline")

# Map task_type → prompt template
_OUTLINE_TEMPLATES = {
    "slide": SLIDE_OUTLINE_TEMPLATE,
    "lesson_plan": LESSON_PLAN_OUTLINE_TEMPLATE,
}


class OutlineAgent(BaseSlideAgent):

    agent_name = "outline"
    max_retries = 2
    error_code = "OUTLINE_FAILED"

    def _execute(self, *, context_map: str, topic: str, grade: str, book: str,
                 task_type: str = "slide", **kwargs) -> dict:
        template = _OUTLINE_TEMPLATES.get(task_type, SLIDE_OUTLINE_TEMPLATE)

        prompt = template.format(
            topic=topic,
            grade=grade,
            book=book,
            context_map=context_map,
        )

        response = self._call_llm(prompt, temperature=0.3)
        payload = self._parse_json(response)

        # Validate cơ bản
        slides = payload.get("slides", [])
        if not slides:
            raise ValueError("Outline trống — không có slide nào")

        # Kiểm tra có đủ loại slide bắt buộc
        slide_types = {s.get("slide_type") for s in slides}
        required_types = {"title", "summary", "exercise"}
        missing = required_types - slide_types
        if missing:
            logger.warning(f"Outline thiếu slide types: {missing}")
            # Tự bổ sung nếu thiếu
            slides = self._patch_missing_types(slides, missing, payload.get("lesson_title", ""))

        payload["slides"] = slides

        logger.info(
            f"Outline agent [{task_type}]: '{payload.get('lesson_title')}' — "
            f"{len(slides)} slides, types={[s.get('slide_type') for s in slides]}"
        )
        return payload

    def _patch_missing_types(self, slides: list, missing: set, lesson_title: str) -> list:
        next_id = len(slides) + 1

        if "title" in missing:
            slides.insert(0, {
                "slide_id": f"s{next_id}",
                "slide_type": "title",
                "title": lesson_title or "Bài học",
                "objective": "Giới thiệu bài học",
                "key_points": ["Mục tiêu bài học"],
                "source_chunk_ids": [],
            })
            next_id += 1

        if "exercise" in missing:
            slides.append({
                "slide_id": f"s{next_id}",
                "slide_type": "exercise",
                "title": "Bài tập luyện tập",
                "objective": "Củng cố kiến thức",
                "key_points": ["Bài tập trắc nghiệm"],
                "source_chunk_ids": [],
            })
            next_id += 1

        if "summary" in missing:
            slides.append({
                "slide_id": f"s{next_id}",
                "slide_type": "summary",
                "title": "Tóm tắt bài học",
                "objective": "Tổng kết kiến thức",
                "key_points": ["Kiến thức cần nhớ"],
                "source_chunk_ids": [],
            })

        return slides


__all__ = ["OutlineAgent"]

