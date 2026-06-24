import ipaddress
import logging
import re
import socket
import uuid
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import httpx
from PIL import Image
from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from src.config.config import project_path, settings

logger = logging.getLogger("chatbot.slide_export")


class SlideExportService:
    """Render generated slide artifacts into a downloadable PPTX deck."""

    LAYOUT_INDEX = {
        "title": 0,
        "section": 2,
        "content": 1,
        "content_media_wide": 7,
        "content_media_tall": 8,
        "content_media": 3,
        "two_content": 3,
        "exercise": 1,
    }

    def __init__(
        self,
        template_path: Optional[Path] = None,
        export_dir: Optional[Path] = None,
        download_base_url: Optional[str] = None,
    ):
        self.template_path = template_path or project_path(settings.SLIDE_TEMPLATE_PATH)
        self.export_dir = export_dir or project_path(settings.SLIDE_EXPORT_DIR)
        self.download_base_url = (
            download_base_url or settings.SLIDE_DOWNLOAD_BASE_URL
        ).rstrip("/")
        self._media_cache: Dict[str, Optional[bytes]] = {}

    def export_pptx(self, lesson_title: str, slides: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self._media_cache.clear()
        prs = Presentation(str(self.template_path)) if self.template_path.exists() else Presentation()

        file_id = f"{uuid.uuid4().hex}.pptx"
        filename = f"{self._slugify(lesson_title) or 'slide_bai_giang'}.pptx"

        for index, slide_data in enumerate(slides, start=1):
            self._add_slide(prs, slide_data, index, lesson_title)

        output_path = self.export_dir / file_id
        prs.save(output_path)
        return {
            "file_id": file_id,
            "filename": filename,
            "download_url": f"{self.download_base_url}/{file_id}",
            "format": "pptx",
        }

    def _add_slide(self, prs, slide_data: Dict[str, Any], index: int, lesson_title: str) -> None:
        slide_type = slide_data.get("slide_type") or "content"
        media = self._select_media(slide_data)
        media_bytes = self._download_media(media["url"]) if media and media.get("url") else None
        layout_name = self._resolve_render_layout(slide_data, media_bytes)
        slide = prs.slides.add_slide(self._pick_layout(prs, layout_name))

        if slide_type == "title":
            self._render_title_slide(slide, slide_data, lesson_title)
        elif slide_type == "exercise":
            self._render_exercise_slide(slide, slide_data, index)
        elif slide_type == "summary":
            self._render_content_slide(slide, slide_data, index, media, media_bytes)
        else:
            self._render_content_slide(slide, slide_data, index, media, media_bytes)

        self._write_notes(slide, slide_data)

    def _render_title_slide(self, slide, slide_data: Dict[str, Any], lesson_title: str) -> None:
        title = slide_data.get("title") or lesson_title or "Bài giảng"
        if not self._set_placeholder_text(slide, 0, [title]):
            self._add_textbox(slide, title, Inches(0.8), Inches(1.5), Inches(11.7), Inches(1.2), 34, bold=True)
        bullets = slide_data.get("bullets") or slide_data.get("key_points") or []
        subtitle = "\n".join(str(item) for item in bullets[:3])
        if subtitle:
            if not self._set_placeholder_text(slide, 1, [subtitle]):
                self._add_textbox(slide, subtitle, Inches(1.0), Inches(3.0), Inches(11.2), Inches(1.4), 18)

    def _render_content_slide(
        self,
        slide,
        slide_data: Dict[str, Any],
        index: int,
        media: Optional[Dict[str, Any]] = None,
        media_bytes: Optional[bytes] = None,
    ) -> None:
        self._add_slide_title(slide, slide_data, index)
        bullets = (
            self._lesson_plan_display_lines(slide_data)
            if slide_data.get("content_detail")
            else self._display_bullets(slide_data)
        )
        if media:
            if bullets:
                text_inserted = self._set_placeholder_text(slide, 1, bullets)
                if not text_inserted:
                    self._add_bullet_box(slide, bullets, Inches(0.7), Inches(1.45), Inches(7.3), Inches(4.7))
                self._add_media_slot(slide, slide_data, media=media, media_bytes=media_bytes, placeholder_idx=2)
            else:
                self._add_media_slot(
                    slide,
                    slide_data,
                    media=media,
                    media_bytes=media_bytes,
                    placeholder_idx=1,
                    caption_idx=2,
                )
            return

        if not self._set_placeholder_text(slide, 1, bullets):
            self._add_bullet_box(slide, bullets, Inches(0.7), Inches(1.45), Inches(11.2), Inches(4.7))

    def _render_exercise_slide(self, slide, slide_data: Dict[str, Any], index: int) -> None:
        self._add_slide_title(slide, slide_data, index)
        lines = []
        for q_idx, question in enumerate(slide_data.get("questions") or [], start=1):
            lines.append(f"Câu {q_idx}. {question.get('question', '')}")
            options = question.get("options") or {}
            for key in ("A", "B", "C", "D"):
                if options.get(key):
                    lines.append(f"{key}. {options[key]}")
            if q_idx >= 3:
                break
        if not lines:
            lines = self._display_bullets(slide_data)
        if not self._set_placeholder_text(slide, 1, lines):
            self._add_bullet_box(slide, lines, Inches(0.7), Inches(1.45), Inches(11.2), Inches(4.7))

    def _add_slide_title(self, slide, slide_data: Dict[str, Any], index: int) -> None:
        prefix = f"{index:02d}"
        title = slide_data.get("title") or "Nội dung"
        if self._set_placeholder_text(slide, 0, [title]):
            return
        self._add_textbox(slide, prefix, Inches(0.55), Inches(0.35), Inches(0.7), Inches(0.35), 12, bold=True)
        self._add_textbox(slide, title, Inches(1.25), Inches(0.28), Inches(11.0), Inches(0.7), 24, bold=True)

    def _add_bullet_box(self, slide, bullets: List[str], left, top, width, height) -> None:
        box = slide.shapes.add_textbox(left, top, width, height)
        frame = box.text_frame
        frame.clear()
        frame.word_wrap = True
        font_size = self._fit_font_size(bullets)
        for idx, bullet in enumerate(bullets or ["Nội dung đang được cập nhật"]):
            paragraph = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
            paragraph.text = self._shorten(str(bullet), 160)
            paragraph.level = 0
            paragraph.font.size = Pt(font_size)
            paragraph.space_after = Pt(8)

    def _add_media_slot(
        self,
        slide,
        slide_data: Dict[str, Any],
        media: Optional[Dict[str, Any]] = None,
        media_bytes: Optional[bytes] = None,
        placeholder_idx: int = 2,
        caption_idx: int = 3,
    ) -> None:
        media = media or self._select_media(slide_data) or {}
        caption = media.get("caption") or "Ảnh minh họa"
        url = media.get("url")
        if media_bytes is None and url:
            media_bytes = self._download_media(url)
        if media_bytes:
            try:
                if not self._insert_picture(slide, placeholder_idx, media_bytes):
                    slide.shapes.add_picture(
                        BytesIO(media_bytes),
                        Inches(8.4),
                        Inches(1.55),
                        width=Inches(3.6),
                    )
                if not self._set_placeholder_text(slide, caption_idx, [self._shorten(caption, 120)]):
                    self._add_textbox(
                        slide,
                        self._shorten(caption, 120),
                        Inches(8.4),
                        Inches(5.2),
                        Inches(3.6),
                        Inches(0.55),
                        11,
                    )
                return
            except Exception as exc:
                logger.warning(
                    "Unable to embed media in PPTX | url=%s error=%s",
                    url,
                    str(exc)[:160],
                )

        text = caption if not url else f"{caption}\n{url}"
        box = slide.shapes.add_textbox(Inches(8.4), Inches(1.55), Inches(3.6), Inches(3.8))
        frame = box.text_frame
        frame.word_wrap = True
        frame.text = self._shorten(text, 260)
        for paragraph in frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            paragraph.font.size = Pt(13)

    def _pick_layout(self, prs, name: str):
        idx = self.LAYOUT_INDEX.get(name, self.LAYOUT_INDEX["content"])
        if idx < len(prs.slide_layouts):
            return prs.slide_layouts[idx]
        blank_idx = 6 if len(prs.slide_layouts) > 6 else 0
        logger.warning("Slide layout %s(%s) missing; falling back to layout %s", name, idx, blank_idx)
        return prs.slide_layouts[blank_idx]

    def _resolve_render_layout(self, slide_data: Dict[str, Any], media_bytes: Optional[bytes] = None) -> str:
        layout = slide_data.get("layout")
        slide_type = slide_data.get("slide_type") or "content"
        if slide_type == "title":
            return "title"
        if slide_type == "exercise":
            return "exercise"
        if slide_type == "summary" and not slide_data.get("media"):
            return "section"
        if not slide_data.get("media"):
            return layout if layout in ("title", "section", "content", "exercise") else "content"

        lines = (
            self._lesson_plan_display_lines(slide_data)
            if slide_data.get("content_detail")
            else self._display_bullets(slide_data)
        )
        if lines:
            return "two_content"

        size = self._image_size(media_bytes) if media_bytes else None
        if size and size[1] > size[0]:
            return "content_media_tall"
        return "content_media_wide"

    def _placeholder(self, slide, idx: int):
        try:
            return slide.placeholders[idx]
        except (KeyError, IndexError):
            return None

    def _set_placeholder_text(self, slide, idx: int, lines: List[str]) -> bool:
        placeholder = self._placeholder(slide, idx)
        if placeholder is None:
            return False
        if not hasattr(placeholder, "text_frame"):
            return False
        frame = placeholder.text_frame
        frame.clear()
        frame.word_wrap = True
        font_size = self._fit_font_size([str(item) for item in lines])
        for line_idx, line in enumerate(lines or ["Nội dung đang được cập nhật"]):
            paragraph = frame.paragraphs[0] if line_idx == 0 else frame.add_paragraph()
            paragraph.text = self._shorten(str(line), 180)
            paragraph.level = 0
            paragraph.space_after = Pt(6)
            if len(lines) >= 4 or sum(len(str(item)) for item in lines) > 420:
                paragraph.font.size = Pt(font_size)
        return True

    def _insert_picture(self, slide, idx: int, media_bytes: bytes) -> bool:
        placeholder = self._placeholder(slide, idx)
        if placeholder is None:
            return False
        try:
            if hasattr(placeholder, "insert_picture"):
                placeholder.insert_picture(BytesIO(media_bytes))
                return True
        except Exception:
            logger.debug("Placeholder insert_picture failed; falling back to add_picture", exc_info=True)
        try:
            slide.shapes.add_picture(
                BytesIO(media_bytes),
                placeholder.left,
                placeholder.top,
                width=placeholder.width,
            )
            return True
        except Exception:
            logger.debug("Fallback add_picture failed", exc_info=True)
            return False

    def _select_media(self, slide_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        items = [self._as_dict(item) for item in slide_data.get("media") or []]
        items = [item for item in items if item]
        if not items:
            return None
        return sorted(
            items,
            key=lambda item: item.get("relevance_score") if item.get("relevance_score") is not None else -1,
            reverse=True,
        )[0]

    @staticmethod
    def _image_size(media_bytes: Optional[bytes]) -> Optional[Tuple[int, int]]:
        if not media_bytes:
            return None
        try:
            with Image.open(BytesIO(media_bytes)) as image:
                return image.size
        except Exception:
            return None

    def _download_media(self, url: str) -> Optional[bytes]:
        if url in self._media_cache:
            return self._media_cache[url]
        if not self._is_public_media_url(url):
            logger.warning("Blocked non-public media URL: %s", url)
            self._media_cache[url] = None
            return None

        current_url = url
        try:
            with httpx.Client(
                timeout=settings.MEDIA_DOWNLOAD_TIMEOUT_SECONDS,
                follow_redirects=False,
            ) as client:
                for _ in range(3):
                    response = client.get(current_url)
                    if response.is_redirect:
                        location = response.headers.get("location")
                        if not location:
                            break
                        current_url = urljoin(current_url, location)
                        if not self._is_public_media_url(current_url):
                            break
                        continue

                    response.raise_for_status()
                    content_type = response.headers.get("content-type", "").lower()
                    content = response.content
                    if (
                        not content_type.startswith("image/")
                        or len(content) > settings.MEDIA_DOWNLOAD_MAX_BYTES
                    ):
                        break
                    self._media_cache[url] = content
                    return content
        except Exception as exc:
            logger.warning(
                "Media download failed | url=%s error=%s",
                url,
                str(exc)[:160],
            )

        self._media_cache[url] = None
        return None

    @staticmethod
    def _is_public_media_url(url: str) -> bool:
        try:
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname:
                return False
            addresses = {
                item[4][0]
                for item in socket.getaddrinfo(parsed.hostname, parsed.port or 443)
            }
            if not addresses:
                return False
            return all(
                not (
                    ipaddress.ip_address(address).is_private
                    or ipaddress.ip_address(address).is_loopback
                    or ipaddress.ip_address(address).is_link_local
                    or ipaddress.ip_address(address).is_reserved
                    or ipaddress.ip_address(address).is_multicast
                    or ipaddress.ip_address(address).is_unspecified
                )
                for address in addresses
            )
        except (OSError, ValueError):
            return False

    def _add_textbox(self, slide, text: str, left, top, width, height, font_size: int, bold: bool = False) -> None:
        box = slide.shapes.add_textbox(left, top, width, height)
        frame = box.text_frame
        frame.word_wrap = True
        frame.text = text
        for paragraph in frame.paragraphs:
            paragraph.font.size = Pt(font_size)
            paragraph.font.bold = bold

    def _write_notes(self, slide, slide_data: Dict[str, Any]) -> None:
        notes = []
        if slide_data.get("notes"):
            notes.append(str(slide_data["notes"]))
        lesson_plan_notes = self._lesson_plan_notes(slide_data)
        if lesson_plan_notes:
            notes.append(lesson_plan_notes)
        overflow = self._overflow_notes(slide_data)
        if overflow:
            notes.append(overflow)
        sources = slide_data.get("source_chunk_ids") or []
        if sources:
            notes.append("Nguồn chunk: " + ", ".join(str(item) for item in sources))
        if notes:
            slide.notes_slide.notes_text_frame.text = "\n\n".join(notes)

    def _display_bullets(self, slide_data: Dict[str, Any]) -> List[str]:
        bullets = slide_data.get("bullets") or slide_data.get("key_points") or []
        return [str(item) for item in bullets[:6]]

    def _lesson_plan_display_lines(self, slide_data: Dict[str, Any]) -> List[str]:
        lines = []
        if slide_data.get("duration_minutes"):
            lines.append(f"Thời lượng: {slide_data['duration_minutes']} phút")
        for item in slide_data.get("objectives") or []:
            lines.append(f"Mục tiêu: {item}")
        for detail in slide_data.get("content_detail") or []:
            detail = self._as_dict(detail)
            heading = detail.get("heading")
            explanation = detail.get("explanation")
            if heading:
                lines.append(heading)
            if explanation:
                lines.append(explanation)
        for item in slide_data.get("assessment") or []:
            lines.append(f"Đánh giá: {item}")
        return lines or self._display_bullets(slide_data)

    def _lesson_plan_notes(self, slide_data: Dict[str, Any]) -> str:
        parts = []
        if slide_data.get("teacher_activities"):
            parts.append("Hoạt động GV:\n" + "\n".join(f"- {item}" for item in slide_data["teacher_activities"]))
        if slide_data.get("student_activities"):
            parts.append("Hoạt động HS:\n" + "\n".join(f"- {item}" for item in slide_data["student_activities"]))
        detail_parts = []
        for detail in slide_data.get("content_detail") or []:
            detail = self._as_dict(detail)
            lines = [str(detail.get("heading") or "Đề mục")]
            field_labels = [
                ("explanation", "Nội dung"),
                ("example", "Ví dụ"),
                ("teacher_prompt", "Câu hỏi GV"),
                ("expected_student_response", "Dự kiến HS"),
                ("common_mistake", "Sai lầm thường gặp"),
                ("wrap_up", "Chốt"),
            ]
            for key, label in field_labels:
                if detail.get(key):
                    lines.append(f"{label}: {detail[key]}")
            sources = detail.get("source_chunk_ids") or []
            if sources:
                lines.append("Nguồn: " + ", ".join(str(item) for item in sources))
            detail_parts.append("\n".join(lines))
        if detail_parts:
            parts.append("Nội dung chi tiết:\n" + "\n\n".join(detail_parts))
        if slide_data.get("assessment"):
            parts.append("Đánh giá:\n" + "\n".join(f"- {item}" for item in slide_data["assessment"]))
        if slide_data.get("transition"):
            parts.append(f"Chuyển ý: {slide_data['transition']}")
        return "\n\n".join(parts)

    @staticmethod
    def _as_dict(value: Any) -> Dict[str, Any]:
        if isinstance(value, dict):
            return value
        if hasattr(value, "model_dump"):
            return value.model_dump()
        return {}

    def _overflow_notes(self, slide_data: Dict[str, Any]) -> str:
        bullets = slide_data.get("bullets") or slide_data.get("key_points") or []
        extras = [str(item) for item in bullets[6:]]
        if not extras:
            return ""
        return "Nội dung bổ sung:\n" + "\n".join(f"- {item}" for item in extras)

    def _fit_font_size(self, bullets: List[str]) -> int:
        total_chars = sum(len(item) for item in bullets)
        if len(bullets) >= 6 or total_chars > 650:
            return 16
        if len(bullets) >= 5 or total_chars > 450:
            return 18
        return 21

    def _slugify(self, value: str) -> str:
        value = re.sub(r"[^\w\s-]", "", value or "", flags=re.UNICODE).strip().lower()
        value = re.sub(r"[-\s]+", "_", value)
        return value[:80]

    def _shorten(self, value: str, limit: int) -> str:
        value = " ".join(value.split())
        return value if len(value) <= limit else value[: limit - 3].rstrip() + "..."
