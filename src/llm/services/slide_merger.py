"""
SlideMerger — Merge kết quả từ 4 agents thành output cuối cùng.
SlideQualityGate — Kiểm tra chất lượng output trước khi trả về.

Merge policy (deterministic, theo spec §5):
    1. Skeleton từ Agent 2 (outline — nguồn sự thật cho cấu trúc)
    2. Chèn content từ Agent 3 theo slide_id
    3. Gắn media từ Agent 1 (nếu success) theo slide_type
    4. Append quiz từ Agent 4 vào slide exercise
    5. Recompute total_slides
"""

import logging
from typing import List, Tuple, Optional

from src.schemas.slide_schemas import (
    AgentResult,
    OutlinePayload, OutlineSlide,
    ContentPayload, ContentSlide,
    MediaPayload, MediaItem,
    QuizPayload, SlideQuizItem,
    MergedSlide,
)

logger = logging.getLogger("chatbot.slide_merger")


# ============================================================
# SLIDER MERGER
# ============================================================

class SlideMerger:
    """
    Merge deterministic kết quả từ 4 agents.
    Outline luôn ưu tiên cao hơn content khi mâu thuẫn slide_type.
    """

    def merge(
        self,
        outline_result: AgentResult,
        content_result: AgentResult,
        media_result: AgentResult,
        quiz_result: AgentResult,
    ) -> List[MergedSlide]:
        """
        Merge tất cả agent results thành danh sách MergedSlide.

        Returns:
            List[MergedSlide] — slides đã merge, sẵn sàng cho quality gate
        """
        # 1. Parse outline (source of truth)
        outline_payload = OutlinePayload(**outline_result.payload)

        # 2. Parse content (nếu có)
        content_map = {}
        if content_result.status != "failed":
            content_slides = content_result.payload.get("slides", [])
            for cs in content_slides:
                content_map[cs.get("slide_id")] = cs

        # 3. Parse media (nếu có)
        media_payload = None
        if media_result.status == "success":
            try:
                media_payload = MediaPayload(**media_result.payload)
            except Exception:
                media_payload = None

        # 4. Parse quiz (nếu có)
        quiz_items = []
        if quiz_result.status == "success":
            try:
                quiz_payload = QuizPayload(**quiz_result.payload)
                quiz_items = quiz_payload.quiz_items
            except Exception:
                quiz_items = []

        # 5. Build merged slides
        merged = []
        for outline_slide in outline_payload.slides:
            merged_slide = self._merge_single_slide(
                outline_slide=outline_slide,
                content_data=content_map.get(outline_slide.slide_id),
                media_payload=media_payload,
                quiz_items=quiz_items,
            )
            merged.append(merged_slide)

        # 6. Nếu có quiz nhưng không có slide exercise → tạo mới
        if quiz_items and not any(s.slide_type == "exercise" for s in merged):
            exercise_slide = MergedSlide(
                slide_id=f"s{len(merged) + 1}",
                slide_type="exercise",
                title="Bài tập luyện tập",
                bullets=["Trả lời các câu hỏi trắc nghiệm sau"],
                questions=[qi for qi in quiz_items],
                source_chunk_ids=[],
            )
            # Chèn trước slide summary (nếu có)
            summary_idx = next(
                (i for i, s in enumerate(merged) if s.slide_type == "summary"),
                len(merged)
            )
            merged.insert(summary_idx, exercise_slide)

        logger.info(
            f"Merged: {len(merged)} slides, "
            f"content={len(content_map)}, "
            f"media={'yes' if media_payload else 'no'}, "
            f"quiz={len(quiz_items)}"
        )
        return merged

    def _merge_single_slide(
        self,
        outline_slide: OutlineSlide,
        content_data: Optional[dict],
        media_payload: Optional[MediaPayload],
        quiz_items: List[SlideQuizItem],
    ) -> MergedSlide:
        """Merge 1 slide từ các sources."""

        # Base từ outline
        slide = MergedSlide(
            slide_id=outline_slide.slide_id,
            slide_type=outline_slide.slide_type,
            title=outline_slide.title,
            bullets=outline_slide.key_points,  # fallback
            source_chunk_ids=outline_slide.source_chunk_ids,
        )

        # Override với content (nếu có)
        if content_data:
            slide.bullets = content_data.get("bullets", slide.bullets)
            slide.notes = content_data.get("notes")
            # Merge source_chunk_ids
            content_sources = content_data.get("source_chunk_ids", [])
            if content_sources:
                merged_sources = list(set(slide.source_chunk_ids + content_sources))
                slide.source_chunk_ids = merged_sources

        # Gắn media
        if media_payload:
            slide.media = self._match_media(slide, media_payload)

        # Gắn quiz vào exercise slides
        if outline_slide.slide_type == "exercise" and quiz_items:
            slide.questions = list(quiz_items)
            slide.bullets = ["Trả lời các câu hỏi trắc nghiệm sau"]

        return slide

    def _match_media(
        self, slide: MergedSlide, media_payload: MediaPayload
    ) -> List[MediaItem]:
        """Match media items vào slide theo slide_type."""
        matched = []

        if slide.slide_type == "title":
            matched.extend(media_payload.hero_media)
        elif slide.slide_type in ("content", "image"):
            for item in media_payload.inline_media:
                if item.for_slide_type in (slide.slide_type, None):
                    matched.append(item)
                    break  # Max 1 inline media per slide

        return matched


# ============================================================
# QUALITY GATE
# ============================================================

class SlideQualityGate:
    """
    Kiểm tra chất lượng output slide trước khi trả về.

    Checks (theo spec §6):
        - Structural: fields đầy đủ
        - Coverage: có đủ title/content/exercise/summary
        - Grounding: mỗi slide có source_chunk_ids
        - Pedagogy: flow hợp lý
    """

    def validate(self, slides: List[MergedSlide]) -> Tuple[bool, List[str]]:
        """
        Validate danh sách slides.

        Returns:
            (passed, issues) — passed=True nếu OK, issues là list vấn đề
        """
        issues = []

        # 1. Structural
        if not slides:
            issues.append("STRUCTURAL: Không có slide nào")
            return False, issues

        for slide in slides:
            if not slide.title:
                issues.append(f"STRUCTURAL: Slide {slide.slide_id} thiếu title")
            if not slide.bullets and slide.slide_type not in ("title", "image"):
                issues.append(f"STRUCTURAL: Slide {slide.slide_id} thiếu bullets")

        # 2. Coverage
        types = {s.slide_type for s in slides}
        required_coverage = {"title", "summary"}  # exercise optional nếu quiz fail
        missing = required_coverage - types
        if missing:
            issues.append(f"COVERAGE: Thiếu slide types: {missing}")

        # 3. Grounding
        ungrounded = [
            s.slide_id for s in slides
            if not s.source_chunk_ids and s.slide_type not in ("exercise",)
        ]
        if ungrounded:
            issues.append(f"GROUNDING: Slides thiếu source_chunk_ids: {ungrounded}")

        # 4. Pedagogy — check flow cơ bản
        if slides and slides[0].slide_type != "title":
            issues.append("PEDAGOGY: Slide đầu tiên không phải title")

        passed = len(issues) == 0
        if not passed:
            logger.warning(f"Quality gate: {len(issues)} issues — {issues}")
        else:
            logger.info("Quality gate: PASSED")

        return passed, issues

    def auto_fix(self, slides: List[MergedSlide], issues: List[str]) -> List[MergedSlide]:
        """
        Thử auto-fix các vấn đề đơn giản.

        Chỉ fix được:
            - Thiếu source_chunk_ids → gán rỗng (grounding warning)
            - Slide đầu không phải title → di chuyển title lên đầu
            - Thiếu title slide → tạo mới
        """
        # Fix pedagogy: di chuyển title lên đầu
        title_slides = [s for s in slides if s.slide_type == "title"]
        if title_slides and slides[0].slide_type != "title":
            slides.remove(title_slides[0])
            slides.insert(0, title_slides[0])
            logger.info("Auto-fix: moved title slide to position 0")

        # Fix coverage: thêm title nếu thiếu
        types = {s.slide_type for s in slides}
        if "title" not in types:
            slides.insert(0, MergedSlide(
                slide_id=f"s{len(slides) + 1}",
                slide_type="title",
                title="Bài học",
                bullets=["Bài giảng Tin học THPT"],
                source_chunk_ids=[],
            ))
            logger.info("Auto-fix: added missing title slide")

        if "summary" not in types:
            slides.append(MergedSlide(
                slide_id=f"s{len(slides) + 1}",
                slide_type="summary",
                title="Tóm tắt bài học",
                bullets=["Kiến thức cần nhớ"],
                source_chunk_ids=[],
            ))
            logger.info("Auto-fix: added missing summary slide")

        return slides


__all__ = ["SlideMerger", "SlideQualityGate"]
