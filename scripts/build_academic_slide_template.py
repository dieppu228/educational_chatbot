#!/usr/bin/env python3
"""Build the bundled academic template from the legacy PowerPoint template.

The source template supplies PowerPoint-compatible masters and placeholders. This
script adds named semantic layouts and replaces its theme with EduBot's palette,
without relying on private python-pptx APIs.
"""

from __future__ import annotations

import argparse
import io
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

SEMANTIC_LAYOUTS = {
    "EDU_TITLE": "Title Slide",
    "EDU_SECTION": "Section Header",
    "EDU_CONTENT": "Title and Content",
    "EDU_CONTENT_MEDIA": "Two Content",
    "EDU_CODE": "Title and Content",
    "EDU_TABLE": "Title and Content",
    "EDU_CHART": "Title and Content",
    "EDU_PROCESS": "Title and Content",
    "EDU_COMPARISON": "Comparison",
    "EDU_EXERCISE": "Title and Content",
    "EDU_ANSWER_KEY": "Title and Content",
    "EDU_SUMMARY": "Section Header",
}

THEME_COLORS = {
    "dk1": "1F2937",
    "lt1": "F7FAFC",
    "dk2": "17324D",
    "lt2": "DDF4F1",
    "accent1": "17324D",
    "accent2": "0F766E",
    "accent3": "DDF4F1",
    "accent4": "F59E0B",
    "accent5": "5B8DEF",
    "accent6": "A7D8D4",
    "hlink": "0F766E",
    "folHlink": "17324D",
}


def _parse(data: bytes) -> ET.Element:
    return ET.fromstring(data)


def _serialize(root: ET.Element) -> bytes:
    stream = io.BytesIO()
    ET.ElementTree(root).write(stream, encoding="UTF-8", xml_declaration=True)
    return stream.getvalue()


def _layout_sources(files: dict[str, bytes]) -> dict[str, str]:
    result: dict[str, str] = {}
    for name, data in files.items():
        if not re.fullmatch(r"ppt/slideLayouts/slideLayout\d+\.xml", name):
            continue
        root = _parse(data)
        common = root.find(f"{{{P_NS}}}cSld")
        if common is not None and common.get("name"):
            result[common.get("name", "")] = name
    missing = sorted(set(SEMANTIC_LAYOUTS.values()) - set(result))
    if missing:
        raise ValueError(f"Source template thiếu layout: {', '.join(missing)}")
    return result


def _apply_theme(files: dict[str, bytes]) -> None:
    root = _parse(files["ppt/theme/theme1.xml"])
    root.set("name", "EduBot Academic VI")
    color_scheme = root.find(f".//{{{A_NS}}}clrScheme")
    if color_scheme is None:
        raise ValueError("Source template thiếu color scheme")
    color_scheme.set("name", "EduBot Academic VI")
    for role, value in THEME_COLORS.items():
        container = color_scheme.find(f"{{{A_NS}}}{role}")
        if container is None:
            continue
        container.clear()
        ET.SubElement(container, f"{{{A_NS}}}srgbClr", {"val": value})

    font_scheme = root.find(f".//{{{A_NS}}}fontScheme")
    if font_scheme is not None:
        font_scheme.set("name", "EduBot Academic VI")
        for family in ("majorFont", "minorFont"):
            latin = font_scheme.find(f"{{{A_NS}}}{family}/{{{A_NS}}}latin")
            if latin is not None:
                latin.set("typeface", "Arial")
    files["ppt/theme/theme1.xml"] = _serialize(root)


def _add_semantic_layouts(files: dict[str, bytes]) -> None:
    sources = _layout_sources(files)
    content_types = _parse(files["[Content_Types].xml"])
    master = _parse(files["ppt/slideMasters/slideMaster1.xml"])
    master_rels = _parse(files["ppt/slideMasters/_rels/slideMaster1.xml.rels"])
    layout_list = master.find(f"{{{P_NS}}}sldLayoutIdLst")
    if layout_list is None:
        raise ValueError("Source template thiếu slide layout list")

    layout_numbers = [
        int(match.group(1))
        for name in files
        if (match := re.fullmatch(r"ppt/slideLayouts/slideLayout(\d+)\.xml", name))
    ]
    relationship_numbers = [
        int(match.group(1))
        for rel in master_rels
        if (match := re.fullmatch(r"rId(\d+)", rel.get("Id", "")))
    ]
    layout_ids = [int(item.get("id", "0")) for item in layout_list]
    next_layout_number = max(layout_numbers) + 1
    next_relationship_number = max(relationship_numbers) + 1
    next_layout_id = max(layout_ids) + 1
    layout_content_type = (
        "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"
    )

    for semantic_name, source_name in SEMANTIC_LAYOUTS.items():
        source_path = sources[source_name]
        target_path = f"ppt/slideLayouts/slideLayout{next_layout_number}.xml"
        target_rels_path = (
            f"ppt/slideLayouts/_rels/slideLayout{next_layout_number}.xml.rels"
        )
        layout = _parse(files[source_path])
        common = layout.find(f"{{{P_NS}}}cSld")
        if common is None:
            raise ValueError(f"Layout {source_name} thiếu cSld")
        common.set("name", semantic_name)
        files[target_path] = _serialize(layout)

        source_rels = source_path.replace("ppt/slideLayouts/", "ppt/slideLayouts/_rels/") + ".rels"
        files[target_rels_path] = files[source_rels]
        ET.SubElement(
            content_types,
            f"{{{CT_NS}}}Override",
            {"PartName": f"/{target_path}", "ContentType": layout_content_type},
        )

        relationship_id = f"rId{next_relationship_number}"
        ET.SubElement(
            master_rels,
            f"{{{REL_NS}}}Relationship",
            {
                "Id": relationship_id,
                "Type": (
                    "http://schemas.openxmlformats.org/officeDocument/2006/"
                    "relationships/slideLayout"
                ),
                "Target": f"../slideLayouts/slideLayout{next_layout_number}.xml",
            },
        )
        ET.SubElement(
            layout_list,
            f"{{{P_NS}}}sldLayoutId",
            {"id": str(next_layout_id), f"{{{R_NS}}}id": relationship_id},
        )
        next_layout_number += 1
        next_relationship_number += 1
        next_layout_id += 1

    files["[Content_Types].xml"] = _serialize(content_types)
    files["ppt/slideMasters/slideMaster1.xml"] = _serialize(master)
    files["ppt/slideMasters/_rels/slideMaster1.xml.rels"] = _serialize(master_rels)


def build_template(source: Path, output: Path) -> None:
    with zipfile.ZipFile(source) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    _apply_theme(files)
    _add_semantic_layouts(files)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 8, 31, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=project_root / "app/templates/default_slide_template.pptx",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "app/templates/academic_vi_slide_template.pptx",
    )
    args = parser.parse_args()
    build_template(args.source.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
