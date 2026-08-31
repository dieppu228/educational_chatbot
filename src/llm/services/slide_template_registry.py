from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


REQUIRED_LAYOUTS = {
    "EDU_TITLE",
    "EDU_SECTION",
    "EDU_CONTENT",
    "EDU_CONTENT_MEDIA",
    "EDU_CODE",
    "EDU_TABLE",
    "EDU_CHART",
    "EDU_PROCESS",
    "EDU_COMPARISON",
    "EDU_EXERCISE",
    "EDU_ANSWER_KEY",
    "EDU_SUMMARY",
}


class TemplateContractError(ValueError):
    pass


@dataclass(frozen=True)
class TemplateInfo:
    template_id: str
    version: str
    theme: Dict[str, str]


class TemplateRegistry:
    """Resolve semantic layouts and placeholders from a versioned manifest."""

    def __init__(self, manifest_path: Path):
        self.manifest_path = Path(manifest_path)
        self.manifest = self._load_manifest()
        self.layouts = self.manifest["layouts"]
        self.info = TemplateInfo(
            template_id=str(self.manifest["template_id"]),
            version=str(self.manifest["version"]),
            theme=dict(self.manifest.get("theme") or {}),
        )

    def _load_manifest(self) -> dict:
        try:
            manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TemplateContractError(f"Không đọc được template manifest: {exc}") from exc
        if str(manifest.get("version")) != "1.0":
            raise TemplateContractError("Template manifest version không được hỗ trợ")
        layouts = manifest.get("layouts")
        if not isinstance(layouts, dict):
            raise TemplateContractError("Template manifest thiếu layouts")
        missing = sorted(REQUIRED_LAYOUTS - set(layouts))
        if missing:
            raise TemplateContractError(f"Template manifest thiếu layouts: {', '.join(missing)}")
        return manifest

    def validate_presentation(self, prs) -> None:
        ratio = float(prs.slide_width) / float(prs.slide_height)
        if abs(ratio - (16 / 9)) > 0.02:
            raise TemplateContractError("Template phải có tỉ lệ 16:9")
        available = {layout.name: layout for layout in prs.slide_layouts}
        for layout_id, contract in self.layouts.items():
            layout = available.get(contract.get("name"))
            if layout is None:
                raise TemplateContractError(
                    f"Template thiếu layout {layout_id}: {contract.get('name')}"
                )
            placeholders = {
                ph.placeholder_format.idx: ph for ph in layout.placeholders
            }
            for role, spec in (contract.get("roles") or {}).items():
                if spec.get("idx") not in placeholders:
                    raise TemplateContractError(
                        f"Layout {layout_id} thiếu placeholder {role} idx={spec.get('idx')}"
                    )
                expected_types = set(spec.get("types") or [])
                actual_type = placeholders[spec["idx"]].placeholder_format.type.name
                if expected_types and actual_type not in expected_types:
                    raise TemplateContractError(
                        f"Layout {layout_id} placeholder {role} phải có type "
                        f"{sorted(expected_types)}, nhận {actual_type}"
                    )

    def layout(self, prs, layout_id: str):
        contract = self.layouts.get(layout_id)
        if contract is None:
            raise TemplateContractError(f"Layout ID không hợp lệ: {layout_id}")
        for layout in prs.slide_layouts:
            if layout.name == contract["name"]:
                return layout
        raise TemplateContractError(f"Không tìm thấy layout: {contract['name']}")

    def placeholder(self, slide, layout_id: str, role: str):
        spec = self._role(layout_id, role)
        try:
            return slide.placeholders[spec["idx"]]
        except (KeyError, IndexError) as exc:
            raise TemplateContractError(
                f"Slide {layout_id} thiếu placeholder role={role} idx={spec['idx']}"
            ) from exc

    def region(self, slide, layout_id: str, role: str) -> tuple[Any, Any, Any, Any]:
        placeholder = self.placeholder(slide, layout_id, role)
        return placeholder.left, placeholder.top, placeholder.width, placeholder.height

    def _role(self, layout_id: str, role: str) -> dict:
        layout = self.layouts.get(layout_id) or {}
        roles = layout.get("roles") or {}
        if role not in roles:
            raise TemplateContractError(f"Layout {layout_id} không khai báo role={role}")
        return roles[role]


__all__ = ["TemplateContractError", "TemplateInfo", "TemplateRegistry"]
