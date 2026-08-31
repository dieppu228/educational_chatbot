from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageStat


def _run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _contact_sheet(images: list[Path], output_path: Path) -> None:
    opened = [Image.open(path).convert("RGB") for path in images]
    try:
        thumb_width = 480
        thumbs = []
        for image in opened:
            height = max(1, int(image.height * thumb_width / image.width))
            thumbs.append(image.resize((thumb_width, height)))
        gap = 24
        sheet = Image.new(
            "RGB",
            (thumb_width + gap * 2, sum(image.height for image in thumbs) + gap * (len(thumbs) + 1)),
            "white",
        )
        y = gap
        for image in thumbs:
            sheet.paste(image, (gap, y))
            y += image.height + gap
        sheet.save(output_path)
    finally:
        for image in opened:
            image.close()


def inspect_deck(deck_path: Path, output_dir: Path) -> dict:
    soffice = shutil.which("soffice")
    pdfinfo = shutil.which("pdfinfo")
    pdftoppm = shutil.which("pdftoppm")
    if not soffice or not pdfinfo or not pdftoppm:
        missing = [
            name for name, value in {
                "soffice": soffice,
                "pdfinfo": pdfinfo,
                "pdftoppm": pdftoppm,
            }.items() if not value
        ]
        raise RuntimeError("Thiếu visual QA tools: " + ", ".join(missing))

    output_dir.mkdir(parents=True, exist_ok=True)
    _run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(deck_path)])
    pdf_path = output_dir / f"{deck_path.stem}.pdf"
    if not pdf_path.exists():
        raise RuntimeError("LibreOffice không tạo được PDF")
    info = _run([pdfinfo, str(pdf_path)])
    pages_line = next((line for line in info.splitlines() if line.startswith("Pages:")), "")
    page_count = int(pages_line.split(":", 1)[1].strip()) if pages_line else 0
    if page_count < 1:
        raise RuntimeError("PDF không có trang")

    prefix = output_dir / "slide"
    _run([pdftoppm, "-png", "-r", "120", str(pdf_path), str(prefix)])
    images = sorted(output_dir.glob("slide-*.png"))
    if len(images) != page_count:
        raise RuntimeError("Số ảnh render không khớp số trang PDF")
    blank_pages = []
    for index, image_path in enumerate(images, start=1):
        with Image.open(image_path) as image:
            grayscale = image.convert("L")
            if ImageStat.Stat(grayscale).stddev[0] < 1.0:
                blank_pages.append(index)
    if blank_pages:
        raise RuntimeError(
            "PDF có trang trắng hoàn toàn: " + ", ".join(map(str, blank_pages))
        )
    contact_sheet = output_dir / "contact-sheet.png"
    _contact_sheet(images, contact_sheet)
    return {"pdf": pdf_path, "pages": page_count, "contact_sheet": contact_sheet}


def main() -> None:
    parser = argparse.ArgumentParser(description="Render PPTX thành PDF/PNG để visual QA")
    parser.add_argument("deck", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = inspect_deck(args.deck.resolve(), args.output_dir.resolve())
    print(f"Rendered {result['pages']} pages: {result['contact_sheet']}")


if __name__ == "__main__":
    main()
