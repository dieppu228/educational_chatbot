from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RenderSlideModel:
    slide_id: str
    slide_type: str
    layout_id: str
    title: str
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    media: Optional[Dict[str, Any]] = None
    questions: List[Dict[str, Any]] = field(default_factory=list)
    answer_entries: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""
    source_chunk_ids: List[str] = field(default_factory=list)
    logical_slide_id: str = ""


@dataclass
class RenderPlan:
    slides: List[RenderSlideModel]
    source_slide_count: int
    warnings: List[str] = field(default_factory=list)


__all__ = ["RenderPlan", "RenderSlideModel"]
