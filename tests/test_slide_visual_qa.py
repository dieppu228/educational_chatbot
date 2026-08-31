import shutil

import pytest

from scripts.qa_slides import inspect_deck
from src.llm.services.slide_export_service import SlideExportService


@pytest.mark.visual
def test_visual_fixture_renders_without_repair(tmp_path):
    if not shutil.which("soffice"):
        pytest.skip("LibreOffice/soffice chưa được cài")

    export_dir = tmp_path / "exports"
    service = SlideExportService(export_dir=export_dir)
    meta = service.export_pptx(
        "Visual QA",
        [
            {
                "slide_id": "s1",
                "slide_type": "title",
                "title": "Bài giảng Tin học",
                "bullets": ["Kiểm thử tiếng Việt"],
            },
            {
                "slide_id": "s2",
                "slide_type": "content",
                "title": "Nội dung và hình ảnh",
                "blocks": [{"type": "bullets", "items": ["Khái niệm", "Ví dụ"]}],
                "media": [{"url": None, "caption": "Sơ đồ minh hoạ"}],
            },
            {
                "slide_id": "s3",
                "slide_type": "content",
                "title": "Ví dụ mã nguồn",
                "blocks": [{"type": "code", "language": "python", "code": "for item in data:\n    print(item)"}],
            },
            {
                "slide_id": "s4",
                "slide_type": "content",
                "title": "Bảng dữ liệu",
                "blocks": [{"type": "table", "columns": ["Mục", "Giá trị"], "rows": [["A", "10"], ["B", "20"]]}],
            },
            {
                "slide_id": "s5",
                "slide_type": "content",
                "title": "Biểu đồ dữ liệu",
                "blocks": [{"type": "chart", "chart_type": "column", "categories": ["A", "B"], "series": [{"name": "Giá trị", "values": [10, 20]}]}],
            },
            {
                "slide_id": "s6",
                "slide_type": "content",
                "title": "Quy trình xử lý",
                "blocks": [{"type": "process", "steps": ["Nhập", "Xử lý", "Xuất"]}],
            },
            {
                "slide_id": "s7",
                "slide_type": "content",
                "title": "So sánh",
                "blocks": [{"type": "comparison", "left_title": "A", "left_items": ["Nhanh"], "right_title": "B", "right_items": ["Ổn định"]}],
            },
            {
                "slide_id": "s8",
                "slide_type": "exercise",
                "title": "Luyện tập",
                "questions": [{
                    "question": "Thiết bị nào định tuyến gói tin?",
                    "options": {"A": "Router", "B": "Chuột", "C": "Loa", "D": "Máy in"},
                    "correct_answer": "A",
                    "explanation": "Router kết nối và định tuyến giữa các mạng.",
                }],
            },
            {
                "slide_id": "s9",
                "slide_type": "summary",
                "title": "Tổng kết",
                "blocks": [{"type": "bullets", "items": ["Ghi nhớ kiến thức chính"]}],
            },
        ],
    )

    result = inspect_deck(export_dir / meta["file_id"], tmp_path / "visual")
    assert result["pages"] == meta["exported_slide_count"]
    assert result["contact_sheet"].is_file()
