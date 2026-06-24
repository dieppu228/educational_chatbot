from io import BytesIO

from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

from src.llm.services.slide_export_service import SlideExportService
from src.llm.services.slide_merger import SlideMerger
from src.schemas.slide_schemas import AgentResult


def test_merger_sets_layout_field_for_content_with_media():
    slides = SlideMerger().merge(
        outline_result=AgentResult(
            agent="outline",
            status="success",
            latency_ms=0,
            payload={
                "lesson_title": "Vòng lặp",
                "slides": [
                    {
                        "slide_id": "s1",
                        "slide_type": "content",
                        "title": "Vòng lặp for",
                        "key_points": ["Cú pháp", "Ví dụ"],
                        "source_chunk_ids": ["c1"],
                    }
                ],
            },
        ),
        content_result=AgentResult(
            agent="content",
            status="success",
            latency_ms=0,
            payload={
                "slides": [
                    {
                        "slide_id": "s1",
                        "title": "Vòng lặp for",
                        "bullets": ["Lặp qua dãy"],
                    }
                ]
            },
        ),
        media_result=AgentResult(
            agent="media",
            status="success",
            latency_ms=0,
            payload={
                "hero_media": [],
                "inline_media": [
                    {
                        "caption": "Minh họa vòng lặp",
                        "for_slide_type": "content",
                        "url": "https://example.edu/loop.png",
                    }
                ],
            },
        ),
        quiz_result=AgentResult(agent="quiz", status="failed", latency_ms=0, payload={}),
    )

    assert slides[0].layout == "content_media"


def _png(width: int, height: int) -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (width, height), color=(24, 124, 98)).save(buffer, format="PNG")
    return buffer.getvalue()


def _has_rendered_picture(slide) -> bool:
    for shape in slide.shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            return True
        if getattr(shape, "image", None) is not None:
            return True
    return False


def test_export_uses_named_layout(tmp_path):
    service = SlideExportService(export_dir=tmp_path)

    meta = service.export_pptx(
        "Bài kiểm thử",
        [
            {
                "slide_id": "s1",
                "slide_type": "content",
                "layout": "content",
                "title": "Khái niệm",
                "bullets": ["Ý chính"],
            }
        ],
    )

    deck = Presentation(str(tmp_path / meta["file_id"]))
    assert deck.slides[0].slide_layout.name == "Title and Content"


def test_export_picks_media_layout_by_image_aspect_and_inserts_picture(monkeypatch, tmp_path):
    service = SlideExportService(export_dir=tmp_path)
    images = {
        "https://example.edu/wide.png": _png(4, 2),
        "https://example.edu/tall.png": _png(2, 4),
    }
    monkeypatch.setattr(service, "_download_media", lambda url: images[url])

    meta = service.export_pptx(
        "Bài kiểm thử media",
        [
            {
                "slide_id": "s1",
                "slide_type": "image",
                "layout": "content_media",
                "title": "Ảnh ngang",
                "media": [{"url": "https://example.edu/wide.png", "caption": "Ảnh ngang"}],
            },
            {
                "slide_id": "s2",
                "slide_type": "image",
                "layout": "content_media",
                "title": "Ảnh dọc",
                "media": [{"url": "https://example.edu/tall.png", "caption": "Ảnh dọc"}],
            },
        ],
    )

    deck = Presentation(str(tmp_path / meta["file_id"]))
    assert deck.slides[0].slide_layout.name == "Content with Caption"
    assert deck.slides[1].slide_layout.name == "Picture with Caption"
    assert _has_rendered_picture(deck.slides[0])
    assert _has_rendered_picture(deck.slides[1])
