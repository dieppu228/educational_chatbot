
import re
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal


# ============================================================
# CONTENT PIPELINE INPUT — Narrow Interface DTO
# ============================================================

@dataclass
class ContentPipelineInput:
    task_type: str          # "slide" | "lesson_plan"
    query: str              # enriched query
    topic: str              # topic bài học
    grade: str              # "10" | "11" | "12"
    book: str               # "CD" | "KNTT"
    rag_chunks: list = field(default_factory=list)
    request_id: str = ""

    @classmethod
    def from_context(cls, ctx, rag_chunks: list, task_type: str = "slide") -> "ContentPipelineInput":
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
            "synthesized_context": "",
            "context_map": "",
            "chunk_map": {},
            "outline_payload": None,
            "content_payload": None,
            "media_payload": None,
            "quiz_payload": None,
            "quality_review": None,
            "reflection_attempts": 0,
            "revision_instruction": None,
            "quality_blocked": False,
            "agent_tasks": [],
            "agent_results": [],
            "artifacts": {},
            # ── Output (graph sẽ populate) ──
            "merged_slides": None,
            "final_output": None,
            "status": "pending",
            "error_message": None,
        }

    @staticmethod
    def _extract_grade(topic: str, contexts: list) -> str:
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
    url: Optional[str] = None
    type: Literal["image", "gif"] = "image"
    caption: str = ""
    for_slide_type: Optional[str] = None  # "title" | "content" | "image"


class MediaPayload(BaseModel):
    hero_media: List[MediaItem] = Field(default_factory=list)
    inline_media: List[MediaItem] = Field(default_factory=list)


# ============================================================
# AGENT 2 — OUTLINE PLANNER (critical)
# ============================================================

class OutlineSlide(BaseModel):
    slide_id: str = Field(..., description="VD: s1, s2, ...")
    slide_type: Literal["title", "content", "exercise", "summary", "image"] = "content"
    title: str
    objective: Optional[str] = None
    key_points: List[str] = Field(default_factory=list)
    source_chunk_ids: List[str] = Field(default_factory=list)


class OutlinePayload(BaseModel):
    lesson_title: str
    slides: List[OutlineSlide] = Field(..., min_length=1)


# ============================================================
# AGENT 3 — CONTENT WRITER (critical)
# ============================================================

class ContentSlide(BaseModel):
    slide_id: str
    title: str
    bullets: List[str] = Field(default_factory=list, max_length=6)
    notes: Optional[str] = Field(None, max_length=600)  # ~120 từ tiếng Việt
    source_chunk_ids: List[str] = Field(default_factory=list)


class ContentPayload(BaseModel):
    slides: List[ContentSlide]


# ============================================================
# AGENT 4 — QUIZ GENERATOR (optional)
# ============================================================

class SlideQuizItem(BaseModel):
    question: str
    options: Dict[str, str] = Field(
        ..., description="4 options: A, B, C, D"
    )
    correct_answer: Literal["A", "B", "C", "D"]
    explanation: str = ""
    source_chunk_ids: List[str] = Field(default_factory=list)


class QuizPayload(BaseModel):
    quiz_items: List[SlideQuizItem] = Field(default_factory=list)


# ============================================================
# MERGED SLIDE — Output cuối cùng sau merge
# ============================================================

class MergedSlide(BaseModel):
    slide_id: str
    slide_type: Literal["title", "content", "exercise", "summary", "image"]
    title: str
    bullets: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    media: List[MediaItem] = Field(default_factory=list)
    questions: List[SlideQuizItem] = Field(default_factory=list)
    source_chunk_ids: List[str] = Field(default_factory=list)


# ============================================================
# QUALITY REVIEW — Shared reviewer output contract
# ============================================================

class QualityIssue(BaseModel):
    case: str
    severity: Literal["minor", "major", "critical"] = "major"
    target: Optional[str] = None
    message: str
    suggestion: Optional[str] = None


class QualityReviewResult(BaseModel):
    passed: bool = False
    score: float = Field(default=0.0, ge=0.0, le=10.0)
    reason_fail: Optional[str] = None
    summary: str = ""
    issues: List[QualityIssue] = Field(default_factory=list)
    reflection_action: Literal[
        "approve",
        "revise_outline",
        "revise_content",
        "revise_quiz",
        "ask_human",
        "block",
    ] = "block"
    revision_instruction: Optional[str] = None
    requires_human_review: bool = False

    @classmethod
    def fallback_fail(cls, reason: str, message: str) -> "QualityReviewResult":
        return cls(
            passed=False,
            score=0.0,
            reason_fail=reason,
            summary=message,
            issues=[QualityIssue(
                case=reason,
                severity="critical",
                target="quality_reviewer",
                message=message,
            )],
            reflection_action="block",
            revision_instruction=message,
            requires_human_review=True,
        )




__all__ = [
    "ContentPipelineInput",
    "AgentResult",
    "MediaItem", "MediaPayload",
    "OutlineSlide", "OutlinePayload",
    "ContentSlide", "ContentPayload",
    "SlideQuizItem", "QuizPayload",
    "MergedSlide",
    "QualityIssue", "QualityReviewResult",
]
