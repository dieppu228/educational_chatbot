
import logging
from typing import List, Tuple, Optional

from src.schemas.slide_schemas import (
    AgentResult,
    OutlinePayload, OutlineSlide,
    ContentPayload, ContentSlide,
    MediaPayload, MediaItem,
    QuizPayload, SlideQuizItem,
    ContentDetailItem, MergedSlide,
)

logger = logging.getLogger("chatbot.slide_merger")


# ============================================================
# SLIDER MERGER
# ============================================================

class SlideMerger:

    def merge(
        self,
        outline_result: AgentResult,
        content_result: AgentResult,
        media_result: AgentResult,
        quiz_result: AgentResult,
    ) -> List[MergedSlide]:
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
        used_media_keys = set()
        for outline_slide in outline_payload.slides:
            merged_slide = self._merge_single_slide(
                outline_slide=outline_slide,
                content_data=content_map.get(outline_slide.slide_id),
                media_payload=media_payload,
                quiz_items=quiz_items,
                used_media_keys=used_media_keys,
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

        media_attached = sum(len(slide.media) for slide in merged)
        unique_media_urls = len({
            media.url for slide in merged for media in slide.media if media.url
        })
        logger.info(
            f"Merged: {len(merged)} slides, "
            f"content={len(content_map)}, "
            f"media={'yes' if media_payload else 'no'}, "
            f"quiz={len(quiz_items)}, "
            f"media_attached={media_attached}, "
            f"unique_media_urls={unique_media_urls}"
        )
        return merged

    def _merge_single_slide(
        self,
        outline_slide: OutlineSlide,
        content_data: Optional[dict],
        media_payload: Optional[MediaPayload],
        quiz_items: List[SlideQuizItem],
        used_media_keys: set,
    ) -> MergedSlide:

        # Base từ outline
        slide = MergedSlide(
            slide_id=outline_slide.slide_id,
            slide_type=outline_slide.slide_type,
            title=outline_slide.title,
            bullets=outline_slide.key_points,  # fallback
            source_chunk_ids=outline_slide.source_chunk_ids,
            duration_minutes=outline_slide.duration_minutes,
            objectives=[outline_slide.teaching_goal] if outline_slide.teaching_goal else [],
            content_detail=[
                ContentDetailItem(
                    heading=unit,
                    explanation="",
                    source_chunk_ids=outline_slide.source_chunk_ids,
                )
                for unit in outline_slide.knowledge_units
            ],
        )

        # Override với content (nếu có)
        if content_data:
            slide.bullets = content_data.get("bullets", slide.bullets)
            slide.notes = content_data.get("notes")
            slide.duration_minutes = content_data.get("duration_minutes", slide.duration_minutes)
            slide.objectives = content_data.get("objectives", slide.objectives) or []
            slide.teacher_activities = content_data.get("teacher_activities", []) or []
            slide.student_activities = content_data.get("student_activities", []) or []
            slide.content_detail = self._parse_content_detail(
                content_data.get("content_detail", slide.content_detail)
            )
            slide.assessment = content_data.get("assessment", []) or []
            slide.transition = content_data.get("transition")
            # Merge source_chunk_ids
            content_sources = content_data.get("source_chunk_ids", [])
            if content_sources:
                merged_sources = list(set(slide.source_chunk_ids + content_sources))
                slide.source_chunk_ids = merged_sources

        # Gắn media
        if media_payload:
            slide.media = self._match_media(slide, media_payload, used_media_keys)

        # Gắn quiz vào exercise slides
        if outline_slide.slide_type == "exercise" and quiz_items:
            slide.questions = list(quiz_items)
            slide.bullets = ["Trả lời các câu hỏi trắc nghiệm sau"]

        slide.layout = self._resolve_layout(slide)
        return slide

    @staticmethod
    def _parse_content_detail(items) -> List[ContentDetailItem]:
        parsed = []
        for item in items or []:
            if isinstance(item, ContentDetailItem):
                parsed.append(item)
            elif isinstance(item, dict) and item.get("heading"):
                parsed.append(ContentDetailItem(**item))
        return parsed

    def _match_media(
        self, slide: MergedSlide, media_payload: MediaPayload, used_media_keys: set
    ) -> List[MediaItem]:
        if slide.slide_type in ("exercise", "summary"):
            return []
        if slide.slide_type == "title":
            return self._pick_one_media(
                slide=slide,
                candidates=media_payload.hero_media,
                used_media_keys=used_media_keys,
            )
        if slide.slide_type in ("content", "image"):
            return self._pick_one_media(
                slide=slide,
                candidates=media_payload.inline_media,
                used_media_keys=used_media_keys,
            )

        return []

    def _pick_one_media(
        self,
        slide: MergedSlide,
        candidates: List[MediaItem],
        used_media_keys: set,
    ) -> List[MediaItem]:
        exact = [
            item for item in candidates
            if item.for_slide_id and item.for_slide_id == slide.slide_id
        ]
        legacy = [
            item for item in candidates
            if not item.for_slide_id and item.for_slide_type in (slide.slide_type, None)
        ]
        for item in exact + legacy:
            key = self._media_key(item)
            if not key or key in used_media_keys:
                continue
            used_media_keys.add(key)
            return [item]
        return []

    @staticmethod
    def _media_key(item: MediaItem) -> Optional[str]:
        if not item.url:
            return None
        return item.url.strip()

    @staticmethod
    def _resolve_layout(slide: MergedSlide) -> str:
        if slide.slide_type == "title":
            return "title"
        if slide.slide_type == "exercise" or slide.questions:
            return "exercise"
        if slide.slide_type == "summary":
            return "section"
        if slide.media:
            return "content_media"
        return "content"


# ============================================================
# QUALITY GATE
# ============================================================

class SlideQualityGate:

    def validate(self, slides: List[MergedSlide]) -> Tuple[bool, List[str]]:
        issues = []

        # 1. Structural
        if not slides:
            issues.append("STRUCTURAL: Không có slide nào")
            return False, issues

        for slide in slides:
            if not slide.title:
                issues.append(f"STRUCTURAL: Slide {slide.slide_id} thiếu title")
            if not slide.bullets and not slide.content_detail and slide.slide_type not in ("title", "image"):
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
