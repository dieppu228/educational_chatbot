"""
Slide Pipeline Schemas — Multi-Agent Content Generation I/O.

Định nghĩa data contract cho toàn bộ content pipeline (slide + lesson plan):
    - ContentPipelineInput (narrow interface DTO)
    - Agent envelope (kết quả mỗi agent)
    - Payload riêng cho từng agent (outline, content, media, quiz)
    - Merged slide (output cuối cùng)
"""

import re
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal


# ============================================================
# CONTENT PIPELINE INPUT — Narrow Interface DTO
# ============================================================

@dataclass
class ContentPipelineInput:
    """
    Narrow interface DTO — chỉ chứa INPUT cần thiết cho ContentSupervisor graph.

    Adapter pattern:
        RequestContext (broad, ~20 fields)
        → ContentPipelineInput (narrow, 7 fields)
        → ContentSupervisorState (graph dict)

    Usage:
        pipeline_input = ContentPipelineInput.from_context(ctx, rag_chunks, "slide")
        initial_state = pipeline_input.to_graph_state()
    """
    task_type: str          # "slide" | "lesson_plan"
    query: str              # enriched query
    topic: str              # topic bài học
    grade: str              # "10" | "11" | "12"
    book: str               # "CD" | "KNTT"
    rag_chunks: list = field(default_factory=list)
    request_id: str = ""

    @classmethod
    def from_context(cls, ctx, rag_chunks: list, task_type: str = "slide") -> "ContentPipelineInput":
        """
        Factory: extract chỉ fields cần thiết từ RequestContext.

        Args:
            ctx: RequestContext — broad context object
            rag_chunks: RAG retrieved chunks (đã qua retrieval + rerank)
            task_type: "slide" hoặc "lesson_plan"
        """
        # Extract topic
        topic = (
            (ctx.intent_result.topic if ctx.intent_result else None)
            or (ctx.session.topic if ctx.session else None)
            or "Bài học"
        )

        # Extract grade
        grade = cls._extract_grade(topic, rag_chunks)

        # Extract book
        book = ctx.effective_book or "KNTT"

        return cls(
            task_type=task_type,
            query=ctx.enriched_query,
            topic=topic,
            grade=grade,
            book=book,
            rag_chunks=rag_chunks,
            request_id=ctx.request_id or "",
        )

    def to_graph_state(self) -> dict:
        """
        Serialize thành ContentSupervisorState initial dict.

        Chỉ set INPUT fields + required defaults.
        Intermediate/output fields dùng None/empty defaults.
        """
        return {
            # ── Input (from DTO) ──
            "task_type": self.task_type,
            "request_id": self.request_id,
            "query": self.query,
            "topic": self.topic,
            "grade": self.grade,
            "book": self.book,
            "rag_chunks": self.rag_chunks,
            "messages": [],
            # ── Intermediate (graph sẽ populate) ──
            "context_map": "",
            "chunk_map": {},
            "outline_payload": None,
            "content_payload": None,
            "media_payload": None,
            "quiz_payload": None,
            # ── Output (graph sẽ populate) ──
            "merged_slides": None,
            "final_output": None,
            "status": "pending",
            "error_message": None,
        }

    @staticmethod
    def _extract_grade(topic: str, contexts: list) -> str:
        """Extract grade từ topic hoặc context metadata."""
        match = re.search(r'(?:lớp|lop|grade)\s*(10|11|12)', topic.lower())
        if match:
            return match.group(1)
        for ctx in contexts[:5]:
            meta = ctx.get("metadata", {}) if isinstance(ctx, dict) else {}
            grade = meta.get("grade")
            if grade in ("10", "11", "12"):
                return grade
        return "10"


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
    "ContentPipelineInput",
    "AgentResult",
    "MediaItem", "MediaPayload",
    "OutlineSlide", "OutlinePayload",
    "ContentSlide", "ContentPayload",
    "SlideQuizItem", "QuizPayload",
    "MergedSlide",
]
