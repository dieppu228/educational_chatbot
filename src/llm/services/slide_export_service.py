import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


class SlideExportService:
    """Render generated slide artifacts into a downloadable PPTX deck."""

    def __init__(
        self,
        template_path: Optional[Path] = None,
        export_dir: Optional[Path] = None,
        download_base_url: str = "/api/exports",
    ):
        project_root = Path(__file__).resolve().parents[3]
        self.template_path = template_path or project_root / "app" / "templates" / "default_slide_template.pptx"
        self.export_dir = export_dir or project_root / "app" / "data" / "exports"
        self.download_base_url = download_base_url.rstrip("/")

    def export_pptx(self, lesson_title: str, slides: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.export_dir.mkdir(parents=True, exist_ok=True)
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
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide_type = slide_data.get("slide_type") or "content"

        if slide_type == "title":
            self._render_title_slide(slide, slide_data, lesson_title)
        elif slide_type == "exercise":
            self._render_exercise_slide(slide, slide_data, index)
        elif slide_type == "summary":
            self._render_content_slide(slide, slide_data, index)
        else:
            self._render_content_slide(slide, slide_data, index)

        self._write_notes(slide, slide_data)

    def _render_title_slide(self, slide, slide_data: Dict[str, Any], lesson_title: str) -> None:
        title = slide_data.get("title") or lesson_title or "Bài giảng"
        self._add_textbox(slide, title, Inches(0.8), Inches(1.5), Inches(11.7), Inches(1.2), 34, bold=True)
        bullets = slide_data.get("bullets") or slide_data.get("key_points") or []
        subtitle = "\n".join(str(item) for item in bullets[:3])
        if subtitle:
            self._add_textbox(slide, subtitle, Inches(1.0), Inches(3.0), Inches(11.2), Inches(1.4), 18)

    def _render_content_slide(self, slide, slide_data: Dict[str, Any], index: int) -> None:
        self._add_slide_title(slide, slide_data, index)
        bullets = self._display_bullets(slide_data)
        has_media = bool(slide_data.get("media"))
        bullet_width = Inches(7.3 if has_media else 11.2)
        self._add_bullet_box(slide, bullets, Inches(0.7), Inches(1.45), bullet_width, Inches(4.7))
        if has_media:
            self._add_media_slot(slide, slide_data)

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
        self._add_bullet_box(slide, lines, Inches(0.7), Inches(1.45), Inches(11.2), Inches(4.7))

    def _add_slide_title(self, slide, slide_data: Dict[str, Any], index: int) -> None:
        prefix = f"{index:02d}"
        self._add_textbox(slide, prefix, Inches(0.55), Inches(0.35), Inches(0.7), Inches(0.35), 12, bold=True)
        title = slide_data.get("title") or "Nội dung"
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

    def _add_media_slot(self, slide, slide_data: Dict[str, Any]) -> None:
        media = (slide_data.get("media") or [{}])[0]
        caption = media.get("caption") or "Ảnh minh họa"
        url = media.get("url")
        text = caption if not url else f"{caption}\n{url}"
        box = slide.shapes.add_textbox(Inches(8.4), Inches(1.55), Inches(3.6), Inches(3.8))
        frame = box.text_frame
        frame.word_wrap = True
        frame.text = self._shorten(text, 260)
        for paragraph in frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            paragraph.font.size = Pt(13)

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
