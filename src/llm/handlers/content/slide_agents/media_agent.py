
import logging
import json
from src.llm.handlers.content.slide_agents.base_slide_agent import BaseSlideAgent
from src.llm.prompts import SLIDE_MEDIA_TEMPLATE

logger = logging.getLogger("chatbot.slide_agent.media")


class MediaAgent(BaseSlideAgent):

    agent_name = "media"
    max_retries = 1
    error_code = "MEDIA_FAILED"

    def _execute(self, *, topic: str, grade: str, book: str, **kwargs) -> dict:
        slide_plan = self._build_slide_plan(
            kwargs.get("outline_payload") or {},
            kwargs.get("content_payload") or {},
        )
        prompt = SLIDE_MEDIA_TEMPLATE.format(
            topic=topic,
            grade=grade,
            book=book,
            slide_plan=slide_plan,
        )

        response = self._call_llm(prompt, temperature=0.5)
        payload = self._parse_json(response)

        # Đảm bảo có đủ keys
        payload.setdefault("hero_media", [])
        payload.setdefault("inline_media", [])

        # url = None cho tất cả items (placeholder)
        for item in payload["hero_media"] + payload["inline_media"]:
            item["url"] = None

        logger.info(
            f"Media agent: {len(payload['hero_media'])} hero, "
            f"{len(payload['inline_media'])} inline"
        )
        return payload

    @staticmethod
    def _build_slide_plan(outline_payload: dict, content_payload: dict) -> str:
        content_by_id = {
            slide.get("slide_id"): slide
            for slide in content_payload.get("slides", [])
            if isinstance(slide, dict) and slide.get("slide_id")
        }
        slides = []
        for slide in outline_payload.get("slides", []):
            if not isinstance(slide, dict):
                continue
            content = content_by_id.get(slide.get("slide_id"), {})
            slides.append({
                "slide_id": slide.get("slide_id"),
                "slide_type": slide.get("slide_type"),
                "title": slide.get("title"),
                "key_points": slide.get("key_points", [])[:4],
                "bullets": content.get("bullets", [])[:4],
            })
        if not slides:
            return "Không có dàn ý chi tiết. Chỉ gợi ý media khi thật sự cần minh họa."
        return json.dumps(slides, ensure_ascii=False, indent=2)


__all__ = ["MediaAgent"]
