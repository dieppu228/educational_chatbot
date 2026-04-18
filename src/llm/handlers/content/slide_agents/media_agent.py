"""
MediaAgent — Agent 1: Gợi ý media minh họa cho slide.

Vai trò: optional — fail không block pipeline.
Output: MediaPayload (hero_media + inline_media captions)
Timeout: 2500ms | Retry: 1
"""

import logging
from src.llm.handlers.content.slide_agents.base_slide_agent import BaseSlideAgent
from src.llm.prompts import SLIDE_MEDIA_TEMPLATE

logger = logging.getLogger("chatbot.slide_agent.media")


class MediaAgent(BaseSlideAgent):

    agent_name = "media"
    max_retries = 1
    error_code = "MEDIA_FAILED"

    def _execute(self, *, topic: str, grade: str, book: str, **kwargs) -> dict:
        """
        Sinh gợi ý media cho slide.

        Returns:
            dict — MediaPayload format: {hero_media: [...], inline_media: [...]}
        """
        prompt = SLIDE_MEDIA_TEMPLATE.format(
            topic=topic,
            grade=grade,
            book=book,
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


__all__ = ["MediaAgent"]
