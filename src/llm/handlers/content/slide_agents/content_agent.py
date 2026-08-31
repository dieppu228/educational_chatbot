
import logging
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.llm.handlers.content.slide_agents.base_slide_agent import BaseSlideAgent
from src.llm.prompts import (
    LESSON_PLAN_CONTENT_TEMPLATE,
    LESSON_PLAN_OUTLINE_CONTEXT_PROMPT,
    QUALITY_REVISION_INSTRUCTION_PROMPT,
    SLIDE_CONTENT_TEMPLATE,
)
from src.schemas.slide_schemas import OutlineSlide, normalize_slide_blocks

logger = logging.getLogger("chatbot.slide_agent.content")

# ── Maximum concurrent slide writers ──
MAX_CONTENT_WORKERS = 3

# Map task_type → prompt template
_CONTENT_TEMPLATES = {
    "slide": SLIDE_CONTENT_TEMPLATE,
    "lesson_plan": LESSON_PLAN_CONTENT_TEMPLATE,
}


class ContentAgent(BaseSlideAgent):

    agent_name = "content"
    max_retries = 1
    error_code = "CONTENT_FAILED"

    def _execute(
        self,
        *,
        outline_slides: List[Dict[str, Any]],
        chunk_map: Dict[str, str],
        task_type: str = "slide",
        **kwargs,
    ) -> dict:
        content_slides = []
        failed_slides = []

        template = _CONTENT_TEMPLATES.get(task_type, SLIDE_CONTENT_TEMPLATE)
        revision_instruction = kwargs.get("revision_instruction")

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
                    template=template,
                    task_type=task_type,
                    revision_instruction=revision_instruction,
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
            f"Content agent [{task_type}]: {len(content_slides)} slides written, "
            f"{len(failed_slides)} fallback"
        )
        return {"slides": content_slides}

    def _write_single_slide(
        self,
        slide_data: Dict[str, Any],
        chunk_map: Dict[str, str],
        template=None,
        task_type: str = "slide",
        revision_instruction: Optional[str] = None,
    ) -> dict:
        if template is None:
            template = SLIDE_CONTENT_TEMPLATE

        slide_id = slide_data.get("slide_id", "s0")
        slide_type = slide_data.get("slide_type", "content")
        title = slide_data.get("title", "")
        objective = slide_data.get("objective", "")
        key_points = slide_data.get("key_points", [])
        key_points_text = ", ".join(self._stringify_list(key_points))
        source_ids = slide_data.get("source_chunk_ids", [])

        # Lấy context subset từ chunk_map
        context_parts = []
        for cid in source_ids:
            if cid in chunk_map:
                context_parts.append(f"[{cid}]: {chunk_map[cid]}")
        context_subset = "\n\n".join(context_parts) if context_parts else "(Không có context cụ thể)"

        prompt = template.format(
            slide_id=slide_id,
            slide_type=slide_type,
            slide_title=title,
            slide_objective=objective or "N/A",
            key_points=key_points_text,
            context_subset=context_subset,
        )
        is_lesson_plan = task_type == "lesson_plan"
        if is_lesson_plan:
            prompt += LESSON_PLAN_OUTLINE_CONTEXT_PROMPT.format(
                duration_minutes=slide_data.get("duration_minutes") or "N/A",
                teaching_goal=slide_data.get("teaching_goal") or objective or "N/A",
                activity_type=slide_data.get("activity_type") or slide_type,
                knowledge_units=", ".join(
                    self._stringify_list(slide_data.get("knowledge_units") or key_points)
                ) or "N/A",
            )
        if revision_instruction:
            prompt += QUALITY_REVISION_INSTRUCTION_PROMPT.format(
                revision_instruction=revision_instruction,
            )

        response = self._call_llm(prompt, temperature=0.3)
        result = self._parse_json(response)

        # Enforce constraints
        bullets = result.get("bullets", [])
        if not is_lesson_plan:
            bullets = bullets[:6]  # Max 6 bullets for slide output.
        result["bullets"] = bullets
        result["slide_id"] = slide_id  # Đảm bảo slide_id khớp
        if not is_lesson_plan:
            blocks, legacy_bullets = normalize_slide_blocks(
                result.get("blocks"),
                fallback_bullets=bullets,
                source_chunk_ids=result.get("source_chunk_ids") or source_ids,
            )
            result["blocks"] = [block.model_dump() for block in blocks]
            result["bullets"] = legacy_bullets[:6]
        if is_lesson_plan:
            result = self._normalize_lesson_plan_result(
                result=result,
                slide_data=slide_data,
                source_ids=source_ids,
                context_subset=context_subset,
            )

        return result

    def _fallback_from_outline(self, slide_data: Dict[str, Any]) -> dict:
        fallback = {
            "slide_id": slide_data.get("slide_id", "s0"),
            "title": slide_data.get("title", ""),
            "bullets": slide_data.get("key_points", [])[:6],
            "notes": None,
            "source_chunk_ids": slide_data.get("source_chunk_ids", []),
        }
        if not (slide_data.get("knowledge_units") or slide_data.get("duration_minutes")):
            blocks, _ = normalize_slide_blocks(
                [],
                fallback_bullets=fallback["bullets"],
                source_chunk_ids=fallback["source_chunk_ids"],
            )
            fallback["blocks"] = [block.model_dump() for block in blocks]
        if slide_data.get("knowledge_units") or slide_data.get("duration_minutes"):
            fallback.update({
                "duration_minutes": slide_data.get("duration_minutes"),
                "objectives": [slide_data.get("teaching_goal")] if slide_data.get("teaching_goal") else [],
                "teacher_activities": [],
                "student_activities": [],
                "content_detail": [
                    {
                        "heading": unit,
                        "explanation": "Cần bổ sung nội dung chi tiết từ context.",
                        "source_chunk_ids": slide_data.get("source_chunk_ids", []),
                    }
                    for unit in slide_data.get("knowledge_units", [])
                ],
                "assessment": [],
                "transition": None,
            })
        return fallback

    def _normalize_lesson_plan_result(
        self,
        *,
        result: Dict[str, Any],
        slide_data: Dict[str, Any],
        source_ids: List[str],
        context_subset: str,
    ) -> Dict[str, Any]:
        source_ids = source_ids or slide_data.get("source_chunk_ids", [])
        source_ids = [str(item) for item in source_ids]
        fallback_units = self._stringify_list(
            slide_data.get("knowledge_units")
            or slide_data.get("key_points")
            or result.get("bullets")
        )
        context_hint = self._context_hint(context_subset)

        result.setdefault("duration_minutes", slide_data.get("duration_minutes"))
        result.setdefault("source_chunk_ids", source_ids)
        result.setdefault("notes", "")

        objectives = self._stringify_list(result.get("objectives"))
        if not objectives:
            goal = slide_data.get("teaching_goal") or slide_data.get("objective")
            objectives = [goal] if goal else [
                f"HS trình bày được nội dung trọng tâm của mục {result.get('title', '')}."
            ]
        result["objectives"] = objectives

        details = self._normalize_content_details(
            result.get("content_detail"),
            fallback_units=fallback_units,
            source_ids=source_ids,
            context_hint=context_hint,
        )
        result["content_detail"] = details

        headings = [item["heading"] for item in details]
        teacher_activities = self._stringify_list(result.get("teacher_activities"))
        if len(teacher_activities) < max(2, min(len(headings), 3)):
            teacher_activities = self._default_teacher_activities(headings)
        result["teacher_activities"] = teacher_activities

        student_activities = self._stringify_list(result.get("student_activities"))
        if len(student_activities) < max(2, min(len(headings), 3)):
            student_activities = self._default_student_activities(headings)
        result["student_activities"] = student_activities

        assessment = self._stringify_list(result.get("assessment"))
        if len(assessment) < 2:
            assessment = self._default_assessment(headings)
        result["assessment"] = assessment

        if not result.get("transition"):
            result["transition"] = "GV tổng kết ý chính và chuyển sang hoạt động tiếp theo."

        if not result.get("notes"):
            result["notes"] = (
                "GV tổ chức theo tiến trình: nêu vấn đề, cho HS phân tích ví dụ, "
                "chốt kiến thức theo từng đề mục và kiểm tra nhanh cuối hoạt động."
            )

        return result

    def _normalize_content_details(
        self,
        items: Any,
        *,
        fallback_units: List[str],
        source_ids: List[str],
        context_hint: str,
    ) -> List[Dict[str, Any]]:
        parsed = []
        raw_items = items if isinstance(items, list) else []
        for raw in raw_items:
            if hasattr(raw, "model_dump"):
                raw = raw.model_dump()
            if isinstance(raw, str):
                raw = {"heading": raw}
            if not isinstance(raw, dict):
                continue
            heading = str(raw.get("heading") or "").strip()
            if not heading:
                continue
            parsed.append(self._complete_content_detail(raw, source_ids, context_hint))

        existing = {item["heading"].strip().lower() for item in parsed}
        for unit in fallback_units:
            heading = str(unit).strip()
            if not heading or heading.lower() in existing:
                continue
            parsed.append(self._complete_content_detail({"heading": heading}, source_ids, context_hint))
            existing.add(heading.lower())

        if not parsed:
            parsed.append(
                self._complete_content_detail(
                    {"heading": "Nội dung trọng tâm"},
                    source_ids,
                    context_hint,
                )
            )

        return parsed

    @staticmethod
    def _complete_content_detail(
        item: Dict[str, Any],
        source_ids: List[str],
        context_hint: str,
    ) -> Dict[str, Any]:
        heading = str(item.get("heading") or "Nội dung trọng tâm").strip()
        sources = item.get("source_chunk_ids") or source_ids
        sources = [str(source) for source in sources]
        explanation = str(item.get("explanation") or "").strip()
        if not explanation:
            explanation = (
                f"GV triển khai '{heading}' dựa trên tài liệu nguồn: {context_hint}. "
                "Làm rõ khái niệm, vai trò và mối liên hệ với nội dung bài học."
            )

        return {
            "heading": heading,
            "explanation": explanation,
            "example": str(item.get("example") or f"GV nêu một tình huống gần gũi để HS nhận diện: {heading}.").strip(),
            "teacher_prompt": str(item.get("teacher_prompt") or f"Em hãy giải thích hoặc lấy ví dụ cho '{heading}'?").strip(),
            "expected_student_response": str(item.get("expected_student_response") or f"HS nêu được ý chính của '{heading}' và minh họa bằng ví dụ phù hợp.").strip(),
            "common_mistake": str(item.get("common_mistake") or "HS dễ trả lời bằng ví dụ rời rạc nhưng chưa khái quát thành khái niệm.").strip(),
            "wrap_up": str(item.get("wrap_up") or f"GV chốt lại điểm cốt lõi của '{heading}' và liên hệ với mục tiêu bài học.").strip(),
            "source_chunk_ids": sources,
        }

    @staticmethod
    def _default_teacher_activities(headings: List[str]) -> List[str]:
        activities = []
        for heading in headings[:4]:
            activities.append(
                f"GV nêu vấn đề về '{heading}', yêu cầu HS quan sát tài liệu/ ví dụ và trả lời câu hỏi gợi mở."
            )
            activities.append(
                f"GV nhận xét câu trả lời, chuẩn hóa thuật ngữ và chốt kiến thức về '{heading}'."
            )
        return activities or ["GV dẫn dắt, tổ chức thảo luận và chốt kiến thức trọng tâm."]

    @staticmethod
    def _default_student_activities(headings: List[str]) -> List[str]:
        activities = []
        for heading in headings[:4]:
            activities.append(
                f"HS đọc ngữ liệu, trao đổi cặp đôi và nêu hiểu biết ban đầu về '{heading}'."
            )
            activities.append(
                f"HS trình bày ví dụ hoặc sản phẩm ngắn để chứng minh đã hiểu '{heading}'."
            )
        return activities or ["HS tham gia trả lời, thảo luận và ghi lại kết luận chính."]

    @staticmethod
    def _default_assessment(headings: List[str]) -> List[str]:
        if not headings:
            return ["HS trả lời đúng câu hỏi kiểm tra nhanh cuối hoạt động.", "HS vận dụng được kiến thức vào ví dụ mới."]
        return [
            f"HS giải thích đúng nội dung: {heading}."
            for heading in headings[:4]
        ] + ["HS nêu được ví dụ phù hợp và tránh nhầm lẫn thường gặp."]

    @staticmethod
    def _context_hint(context_subset: str) -> str:
        text = " ".join((context_subset or "").split())
        if not text or text == "(Không có context cụ thể)":
            return "các chunk đã truy xuất cho bài học"
        return text[:220]

    @staticmethod
    def _stringify_list(items: List[Any]) -> List[str]:
        values = []
        for item in items or []:
            if isinstance(item, str):
                values.append(item)
            elif isinstance(item, dict):
                values.append(
                    str(
                        item.get("heading")
                        or item.get("title")
                        or item.get("name")
                        or item
                    )
                )
            else:
                values.append(str(item))
        return values


__all__ = ["ContentAgent"]
