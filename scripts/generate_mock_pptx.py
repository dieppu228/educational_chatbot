#!/usr/bin/env python3
"""Generate a PPTX directly from a mock JSON payload, without app runtime services."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.llm.services.slide_export_service import SlideExportService  # noqa: E402


DEFAULT_INPUT = PROJECT_ROOT / "examples/mock_slide_deck.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "app/data/mock_exports"
DEFAULT_TEMPLATE = PROJECT_ROOT / "app/templates/academic_vi_slide_template.pptx"
DEFAULT_MANIFEST = PROJECT_ROOT / "app/templates/academic_vi_slide_template.json"


def load_deck_payload(path: Path) -> tuple[str, list[dict[str, Any]]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Không đọc được mock payload {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Mock payload phải là JSON object")
    lesson_title = str(payload.get("lesson_title") or "Mock slide deck")
    slides = payload.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("Mock payload phải có slides là một danh sách không rỗng")
    if any(not isinstance(slide, dict) for slide in slides):
        raise ValueError("Mỗi phần tử trong slides phải là JSON object")
    return lesson_title, slides


def load_media_map(path: Optional[Path]) -> dict[str, Path]:
    if path is None:
        return {}
    try:
        raw_map = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Không đọc được media map {path}: {exc}") from exc
    if not isinstance(raw_map, dict):
        raise ValueError("Media map phải là JSON object dạng URL → local path")

    resolved = {}
    for url, local_path in raw_map.items():
        candidate = Path(str(local_path)).expanduser()
        if not candidate.is_absolute():
            candidate = path.parent / candidate
        candidate = candidate.resolve()
        if not candidate.is_file():
            raise ValueError(f"Không tìm thấy media local cho {url}: {candidate}")
        resolved[str(url)] = candidate
    return resolved


def build_media_loader(
    media_map: dict[str, Path],
    network_loader: Callable[[str], Optional[bytes]],
    *,
    allow_network: bool,
) -> Callable[[str], Optional[bytes]]:
    def load(url: str) -> Optional[bytes]:
        local_path = media_map.get(url)
        if local_path is not None:
            return local_path.read_bytes()
        if allow_network:
            return network_loader(url)
        return None

    return load


def generate_mock_deck(args: argparse.Namespace) -> dict[str, Any]:
    input_path = args.input.resolve()
    output_dir = args.output_dir.resolve()
    lesson_title, slides = load_deck_payload(input_path)
    media_map = load_media_map(args.media_map.resolve() if args.media_map else None)

    service = SlideExportService(
        template_path=args.template.resolve(),
        manifest_path=args.manifest.resolve(),
        export_dir=output_dir,
        download_base_url="/mock-exports",
    )
    service._download_media = build_media_loader(
        media_map,
        service._download_media,
        allow_network=args.allow_network_media,
    )
    result = service.export_pptx(lesson_title, slides)
    result["output_path"] = str((output_dir / result["file_id"]).resolve())
    result["input_path"] = str(input_path)
    result["network_media_enabled"] = bool(args.allow_network_media)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Sinh PPTX trực tiếp từ JSON mock; mặc định không gọi LLM, Qdrant, "
            "embedding hoặc tải media qua mạng."
        )
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--media-map",
        type=Path,
        help="JSON object ánh xạ URL trong payload sang đường dẫn ảnh local",
    )
    parser.add_argument(
        "--allow-network-media",
        action="store_true",
        help="Cho phép tải media HTTP/HTTPS không có trong media map",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = generate_mock_deck(args)
    except Exception as exc:
        parser.exit(2, f"Lỗi tạo mock PPTX: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
