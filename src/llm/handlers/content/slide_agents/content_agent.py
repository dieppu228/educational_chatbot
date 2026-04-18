"""
ContentAgent — Agent 3: Viết nội dung chi tiết cho từng slide.

Vai trò: CRITICAL — phụ thuộc vào outline từ Agent 2.
Output: ContentPayload (bullets + notes cho mỗi slide)
Timeout per slide: 2500ms | Retry per slide: 1
Worker pool: max 3 concurrent slides.
"""

import logging
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.llm.handlers.content.slide_agents.base_slide_agent import BaseSlideAgent
from src.llm.prompts import SLIDE_CONTENT_TEMPLATE
from src.schemas.slide_schemas import OutlineSlide

logger = logging.getLogger("chatbot.slide_agent.content")

# ── Maximum concurrent slide writers ──
MAX_CONTENT_WORKERS = 3


class ContentAgent(BaseSlideAgent):

    agent_name = "content"
    max_retries = 1
    error_code = "CONTENT_FAILED"

    def _execute(
        self,
        *,
        outline_slides: List[Dict[str, Any]],
        chunk_map: Dict[str, str],
        **kwargs,
    ) -> dict:
        """
        Viết nội dung cho tất cả slides (parallel, max 3 workers).

        Args:
            outline_slides: List outline slides từ Agent 2
            chunk_map: Dict[chunk_id → chunk_content] để lấy context subset

        Returns:
            dict — ContentPayload format: {slides: [...]}
        """
        content_slides = []
        failed_slides = []

        # Dùng ThreadPoolExecutor cho parallel slide writing
        with ThreadPoolExecutor(max_workers=MAX_CONTENT_WORKERS) as executor:
            futures = {}
            for slide_data in outline_slides:
                # Bỏ qua exercise slides — quiz agent xử lý
                if slide_data.get("slide_type") == "exercise":
                    continue

                future = executor.submit(
                    self._write_single_slide,
                    slide_data=slide_data,
                    chunk_map=chunk_map,
                )
                futures[future] = slide_data

            for future in as_completed(futures):
                slide_data = futures[future]
                slide_id = slide_data.get("slide_id", "?")
                try:
                    result = future.result()
                    content_slides.append(result)
                except Exception as e:
                    logger.warning(f"Slide {slide_id} failed: {e}")
                    # Fallback: dùng key_points từ outline
                    fallback = self._fallback_from_outline(slide_data)
                    content_slides.append(fallback)
                    failed_slides.append(slide_id)

        # Sort theo slide_id để giữ thứ tự
        content_slides.sort(key=lambda s: s.get("slide_id", ""))

        logger.info(
            f"Content agent: {len(content_slides)} slides written, "
            f"{len(failed_slides)} fallback"
        )
        return {"slides": content_slides}

    def _write_single_slide(
        self,
        slide_data: Dict[str, Any],
        chunk_map: Dict[str, str],
    ) -> dict:
        """Viết nội dung cho 1 slide cụ thể."""
        slide_id = slide_data.get("slide_id", "s0")
        slide_type = slide_data.get("slide_type", "content")
        title = slide_data.get("title", "")
        objective = slide_data.get("objective", "")
        key_points = slide_data.get("key_points", [])
        source_ids = slide_data.get("source_chunk_ids", [])

        # Lấy context subset từ chunk_map
        context_parts = []
        for cid in source_ids:
            if cid in chunk_map:
                context_parts.append(f"[{cid}]: {chunk_map[cid]}")
        context_subset = "\n\n".join(context_parts) if context_parts else "(Không có context cụ thể)"

        prompt = SLIDE_CONTENT_TEMPLATE.format(
            slide_id=slide_id,
            slide_type=slide_type,
            slide_title=title,
            slide_objective=objective or "N/A",
            key_points=", ".join(key_points),
            context_subset=context_subset,
        )

        response = self._call_llm(prompt, temperature=0.3)
        result = self._parse_json(response)

        # Enforce constraints
        bullets = result.get("bullets", [])[:6]  # Max 6 bullets
        result["bullets"] = bullets
        result["slide_id"] = slide_id  # Đảm bảo slide_id khớp

        return result

    def _fallback_from_outline(self, slide_data: Dict[str, Any]) -> dict:
        """Tạo content fallback từ outline khi LLM call fail."""
        return {
            "slide_id": slide_data.get("slide_id", "s0"),
            "title": slide_data.get("title", ""),
            "bullets": slide_data.get("key_points", [])[:6],
            "notes": None,
            "source_chunk_ids": slide_data.get("source_chunk_ids", []),
        }


__all__ = ["ContentAgent"]
