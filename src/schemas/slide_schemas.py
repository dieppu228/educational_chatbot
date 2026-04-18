"""
Slide Pipeline Schemas — Multi-Agent Slide Generation I/O.

Định nghĩa data contract cho toàn bộ slide pipeline:
    - Pipeline input/output
    - Agent envelope (kết quả mỗi agent)
    - Payload riêng cho từng agent (outline, content, media, quiz)
    - Merged slide (output cuối cùng)
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal


# ============================================================
# AGENT ENVELOPE — Kết quả chung cho mọi agent
# ============================================================

class AgentResult(BaseModel):
    """
    Envelope thống nhất cho kết quả mỗi agent.
    Mọi agent đều trả về format này.
    """
    agent: str = Field(..., description="Agent name: media|outline|content|quiz")
    status: Literal["success", "partial", "failed"] = "failed"
    latency_ms: int = Field(default=0, ge=0)
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)




# ============================================================
# AGENT 1 — MEDIA SEARCH (optional)
# ============================================================

class MediaItem(BaseModel):
    """Một item media (image/gif)."""
    url: Optional[str] = None
    type: Literal["image", "gif"] = "image"
    caption: str = ""
    for_slide_type: Optional[str] = None  # "title" | "content" | "image"


class MediaPayload(BaseModel):
    """Output payload của Media Agent."""
    hero_media: List[MediaItem] = Field(default_factory=list)
    inline_media: List[MediaItem] = Field(default_factory=list)


# ============================================================
# AGENT 2 — OUTLINE PLANNER (critical)
# ============================================================

class OutlineSlide(BaseModel):
    """Một slide trong outline."""
    slide_id: str = Field(..., description="VD: s1, s2, ...")
    slide_type: Literal["title", "content", "exercise", "summary", "image"] = "content"
    title: str
    objective: Optional[str] = None
    key_points: List[str] = Field(default_factory=list)
    source_chunk_ids: List[str] = Field(default_factory=list)


class OutlinePayload(BaseModel):
    """Output payload của Outline Planner."""
    lesson_title: str
    slides: List[OutlineSlide] = Field(..., min_length=1)


# ============================================================
# AGENT 3 — CONTENT WRITER (critical)
# ============================================================

class ContentSlide(BaseModel):
    """Nội dung chi tiết cho 1 slide."""
    slide_id: str
    title: str
    bullets: List[str] = Field(default_factory=list, max_length=6)
    notes: Optional[str] = Field(None, max_length=600)  # ~120 từ tiếng Việt
    source_chunk_ids: List[str] = Field(default_factory=list)


class ContentPayload(BaseModel):
    """Output payload của Content Writer."""
    slides: List[ContentSlide]


# ============================================================
# AGENT 4 — QUIZ GENERATOR (optional)
# ============================================================

class SlideQuizItem(BaseModel):
    """Một câu hỏi quiz cho slide."""
    question: str
    options: Dict[str, str] = Field(
        ..., description="4 options: A, B, C, D"
    )
    correct_answer: Literal["A", "B", "C", "D"]
    explanation: str = ""
    source_chunk_ids: List[str] = Field(default_factory=list)


class QuizPayload(BaseModel):
    """Output payload của Quiz Generator."""
    quiz_items: List[SlideQuizItem] = Field(default_factory=list)


# ============================================================
# MERGED SLIDE — Output cuối cùng sau merge
# ============================================================

class MergedSlide(BaseModel):
    """Slide hoàn chỉnh sau khi merge tất cả agents."""
    slide_id: str
    slide_type: Literal["title", "content", "exercise", "summary", "image"]
    title: str
    bullets: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    media: List[MediaItem] = Field(default_factory=list)
    questions: List[SlideQuizItem] = Field(default_factory=list)
    source_chunk_ids: List[str] = Field(default_factory=list)




__all__ = [
    "AgentResult",
    "MediaItem", "MediaPayload",
    "OutlineSlide", "OutlinePayload",
    "ContentSlide", "ContentPayload",
    "SlideQuizItem", "QuizPayload",
    "MergedSlide",
]
