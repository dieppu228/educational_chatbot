
import re
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, field_validator
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
    type: Literal["image", "gif", "animation", "diagram", "infographic"] = "image"
    caption: str = ""
    for_slide_type: Optional[str] = None  # "title" | "content" | "image"
    for_slide_id: Optional[str] = None
    query: Optional[str] = None
    required: bool = False
    media_type: Optional[Literal[
        "image", "gif", "animation", "diagram", "infographic"
    ]] = None
    source_url: str = ""
    source_title: str = ""
    relevance_score: Optional[float] = None


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
    duration_minutes: Optional[int] = None
    teaching_goal: Optional[str] = None
    knowledge_units: List[str] = Field(default_factory=list)
    activity_type: Optional[str] = None

    @field_validator("key_points", "knowledge_units", mode="before")
    @classmethod
    def normalize_text_items(cls, value):
        if not value:
            return []
        if not isinstance(value, list):
            value = [value]
        normalized = []
        for item in value:
            if isinstance(item, str):
                normalized.append(item)
            elif isinstance(item, dict):
                normalized.append(
                    str(
                        item.get("heading")
                        or item.get("sub_title")
                        or item.get("title")
                        or item.get("name")
                        or item
                    )
                )
            else:
                normalized.append(str(item))
        return normalized


class OutlinePayload(BaseModel):
    lesson_title: str
    slides: List[OutlineSlide] = Field(..., min_length=1)


# ============================================================
# AGENT 3 — CONTENT WRITER (critical)
# ============================================================

class ContentDetailItem(BaseModel):
    heading: str
    explanation: str
    example: Optional[str] = None
    teacher_prompt: Optional[str] = None
    expected_student_response: Optional[str] = None
    common_mistake: Optional[str] = None
    wrap_up: Optional[str] = None
    source_chunk_ids: List[str] = Field(default_factory=list)


class ContentSlide(BaseModel):
    slide_id: str
    title: str
    bullets: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    source_chunk_ids: List[str] = Field(default_factory=list)
    duration_minutes: Optional[int] = None
    objectives: List[str] = Field(default_factory=list)
    teacher_activities: List[str] = Field(default_factory=list)
    student_activities: List[str] = Field(default_factory=list)
    content_detail: List[ContentDetailItem] = Field(default_factory=list)
    assessment: List[str] = Field(default_factory=list)
    transition: Optional[str] = None


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
    layout: Optional[str] = None
    title: str
    bullets: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    media: List[MediaItem] = Field(default_factory=list)
    questions: List[SlideQuizItem] = Field(default_factory=list)
    source_chunk_ids: List[str] = Field(default_factory=list)
    duration_minutes: Optional[int] = None
    objectives: List[str] = Field(default_factory=list)
    teacher_activities: List[str] = Field(default_factory=list)
    student_activities: List[str] = Field(default_factory=list)
    content_detail: List[ContentDetailItem] = Field(default_factory=list)
    assessment: List[str] = Field(default_factory=list)
    transition: Optional[str] = None


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

_HARD_REASONS = {"UNSAFE", "UNGROUNDED", "HALLUCINATION", "UNSAFE_CONTENT"}


def _is_media_issue(issue: dict) -> bool:
    target = str((issue or {}).get("target") or "").lower()
    case = str((issue or {}).get("case") or "").lower()
    message = str((issue or {}).get("message") or "").lower()
    return (
        "media" in target
        or "image" in target
        or "gif" in target
        or "media" in case
        or "image" in case
        or "gif" in case
        or "hình ảnh" in message
        or "ảnh" in message
        or "gif" in message
    )


def classify_quality(review: Optional[dict], has_deck: bool, *, hard_floor: float) -> str:
    """Return approve, warn, or block for a quality review result."""
    if not has_deck:
        return "block"
    if not isinstance(review, dict):
        return "warn"
    if review.get("passed") and review.get("reflection_action") == "approve":
        return "approve"

    reason = (review.get("reason_fail") or "").upper()
    if reason == "FORMAT_INVALID":
        return "warn"

    issues = review.get("issues") or []
    critical_issues = [
        issue for issue in issues
        if (issue or {}).get("severity") == "critical"
    ]
    if any(not _is_media_issue(issue) for issue in critical_issues):
        return "block"

    if reason in _HARD_REASONS:
        return "block"

    try:
        if float(review.get("score") or 0.0) < hard_floor:
            return "block"
    except (TypeError, ValueError):
        pass
    return "warn"


def build_quality_warnings(review: Optional[dict]) -> list[str]:
    if not isinstance(review, dict):
        return ["Chưa kiểm định được chất lượng tự động, bạn nên rà soát lại nội dung trước khi dùng."]

    warnings = []
    for issue in review.get("issues") or []:
        if not isinstance(issue, dict):
            continue
        message = str(issue.get("message") or "").strip()
        suggestion = str(issue.get("suggestion") or "").strip()
        if not message:
            continue
        warnings.append(f"{message} Gợi ý: {suggestion}" if suggestion else message)
        if len(warnings) >= 3:
            break

    if warnings:
        return warnings

    for key in ("summary", "revision_instruction", "reason_fail"):
        value = str(review.get(key) or "").strip()
        if value:
            return [value]
    return ["Có một số điểm nên rà soát và chỉnh sửa thêm trước khi sử dụng."]


__all__ = [
    "ContentPipelineInput",
    "AgentResult",
    "MediaItem", "MediaPayload",
    "OutlineSlide", "OutlinePayload",
    "ContentDetailItem", "ContentSlide", "ContentPayload",
    "SlideQuizItem", "QuizPayload",
    "MergedSlide",
    "QualityIssue", "QualityReviewResult",
    "classify_quality", "build_quality_warnings",
]
