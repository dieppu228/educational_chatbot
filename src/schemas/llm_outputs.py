"""
Pydantic schemas for LLM node outputs.
Provides type-safe validation and parsing for all LLM responses.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal, Dict, Any
import json


# ============================================================
# MCQ Generation Output Schemas
# ============================================================

class MCQOption(BaseModel):
    """Schema for multiple choice options A, B, C, D"""
    A: str = Field(..., description="Option A text")
    B: str = Field(..., description="Option B text")
    C: str = Field(..., description="Option C text")
    D: str = Field(..., description="Option D text")


class MCQQuestion(BaseModel):
    """Schema for a single MCQ question"""
    index: int = Field(..., ge=1, description="Question number (1-indexed)")
    question: str = Field(..., min_length=10, description="Question text")
    options: MCQOption = Field(..., description="Answer options A-D")
    correct_answer: Literal["A", "B", "C", "D"] = Field(..., description="Correct answer letter")
    explanation: str = Field(..., min_length=5, description="Explanation for the answer")
    
    @field_validator('question')
    @classmethod
    def question_must_end_with_question_mark_or_colon(cls, v: str) -> str:
        """Validate question ends appropriately"""
        v = v.strip()
        # Allow questions ending with ? : or .
        if not v[-1] in ['?', ':', '.', '。']:
            v = v + '?'
        return v


class MCQGenerationOutput(BaseModel):
    """
    Schema for Question Generator output.
    Validates the complete MCQ response from LLM.
    """
    mcq: List[MCQQuestion] = Field(..., min_length=1, description="List of MCQ questions")
    
    @field_validator('mcq')
    @classmethod
    def validate_unique_indices(cls, v: List[MCQQuestion]) -> List[MCQQuestion]:
        """Ensure all question indices are unique"""
        indices = [q.index for q in v]
        if len(indices) != len(set(indices)):
            raise ValueError("Question indices must be unique")
        return v
    
    @classmethod
    def from_json_string(cls, json_str: str) -> "MCQGenerationOutput":
        """Parse from raw JSON string returned by LLM"""
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    def get_question_by_index(self, index: int) -> Optional[MCQQuestion]:
        """Get question by its index (1-indexed)"""
        for q in self.mcq:
            if q.index == index:
                return q
        return None
    
    def to_display_format(self) -> str:
        """Convert to human-readable display format"""
        lines = []
        for q in self.mcq:
            lines.append(f"Câu hỏi {q.index}:")
            lines.append(q.question)
            lines.append("")
            lines.append(f"A. {q.options.A}")
            lines.append(f"B. {q.options.B}")
            lines.append(f"C. {q.options.C}")
            lines.append(f"D. {q.options.D}")
            lines.append("")
            lines.append("_" * 40)
            lines.append("")
        return "\n".join(lines)


# ============================================================
# Answer Scoring Output Schema
# ============================================================

class ScoringOutput(BaseModel):
    """
    Schema for Answer Scorer output.
    Validates the scoring result from LLM.
    """
    status: Literal["found", "not_found", "ambiguous"] = Field(
        ..., 
        description="Status of answer detection"
    )
    question_index: Optional[int] = Field(
        None, 
        ge=0, 
        description="Question index (0-indexed in array)"
    )
    question_text: Optional[str] = Field(
        None, 
        description="Original question text"
    )
    user_answer: Optional[Any] = Field(
        None, 
        description="Normalized user answer (can be A/B/C/D, bool, or string)"
    )
    correct_answer: Optional[Any] = Field(
        None, 
        description="Correct answer from session"
    )
    is_correct: Optional[bool] = Field(
        None, 
        description="Whether user's answer is correct"
    )
    score: Optional[float] = Field(
        None,
        ge=0.0,
        le=10.0,
        description="Score for essay (0-10)"
    )
    explanation: Optional[str] = Field(
        None, 
        description="Feedback/explanation for the answer"
    )
    confidence: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=1.0, 
        description="Confidence score (0.0 to 1.0)"
    )
    
    @classmethod
    def from_json_string(cls, json_str: str) -> "ScoringOutput":
        """Parse from raw JSON string returned by LLM"""
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    def to_feedback_message(self) -> str:
        """Generate user-friendly feedback message"""
        if self.status == "not_found":
            return "Không tìm thấy câu hỏi hoặc đáp án trong tin nhắn của bạn."
        
        if self.status == "ambiguous":
            return "Tin nhắn của bạn không rõ ràng. Vui lòng nói rõ câu số mấy và đáp án (A/B/C/D)."
        
        # status == "found"
        if self.is_correct:
            result = "✅ **Chính xác!**"
        else:
            result = f"❌ **Sai rồi!** Đáp án đúng là **{self.correct_answer}**"
        
        if self.explanation:
            result += f"\n\n💡 {self.explanation}"
        
        return result


# ============================================================
# Fallback Handler Output Schema
# ============================================================

class FallbackOutput(BaseModel):
    """
    Schema for Fallback Handler output.
    Simple text response for off-topic queries.
    """
    response: str = Field(..., min_length=1, description="Fallback response text")
    is_redirect: bool = Field(
        default=False, 
        description="Whether response redirects user back to main function"
    )
    
    @classmethod
    def from_text(cls, text: str) -> "FallbackOutput":
        """Create from raw text response"""
        return cls(response=text.strip())


# ============================================================
# Feedback Generation Output Schema
# ============================================================

class FeedbackOutput(BaseModel):
    """
    Schema for educational feedback generation.
    """
    feedback: str = Field(..., description="Educational feedback text")
    encouragement: Optional[str] = Field(None, description="Encouraging message")
    next_steps: Optional[str] = Field(None, description="Suggested next steps")


# ============================================================
# Metadata Extraction Output Schema
# ============================================================

class ExtractMetadataOutput(BaseModel):
    """
    Schema for metadata extraction from user query.
    Used for filtering RAG results.
    """
    lesson: Optional[str] = Field(None, description="Extracted lesson name")
    grade: Optional[Literal["10", "11", "12"]] = Field(None, description="Grade level")
    topic: Optional[str] = Field(None, description="Topic/subject area")
    
    @classmethod
    def from_json_string(cls, json_str: str) -> "ExtractMetadataOutput":
        """Parse from raw JSON string returned by LLM"""
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")



# ============================================================
# Essay Generation Output Schemas
# ============================================================

class EssayQuestion(BaseModel):
    """Schema for a single essay question."""
    index: int = Field(..., ge=1, description="Question number (1-indexed)")
    question: str = Field(..., min_length=10, description="Essay question text")
    sample_answer: str = Field(..., min_length=10, description="Sample answer for reference")
    rubric: str = Field(..., description="Scoring rubric / evaluation criteria")
    difficulty: Literal["easy", "medium", "hard"] = Field(
        default="medium", description="Difficulty level"
    )


class EssayGenerationOutput(BaseModel):
    """Schema for Essay Generator output."""
    essays: List[EssayQuestion] = Field(..., min_length=1, description="List of essay questions")

    @classmethod
    def from_json_string(cls, json_str: str) -> "EssayGenerationOutput":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def to_display_format(self) -> str:
        lines = []
        for q in self.essays:
            lines.append(f"📝 Câu hỏi {q.index} ({q.difficulty}):")
            lines.append(q.question)
            lines.append("")
            lines.append("_" * 40)
            lines.append("")
        return "\n".join(lines)


# ============================================================
# Fill-in-the-Blank Generation Output Schemas
# ============================================================

class FillBlankQuestion(BaseModel):
    """Schema for a single fill-in-the-blank question."""
    index: int = Field(..., ge=1, description="Question number (1-indexed)")
    text_with_blanks: str = Field(
        ..., min_length=10,
        description="Text with ___ marking blanks"
    )
    answers: List[str] = Field(
        ..., min_length=1,
        description="Correct answers for each blank, in order"
    )
    explanation: str = Field(default="", description="Explanation for the answers")


class FillBlankGenerationOutput(BaseModel):
    """Schema for Fill-in-the-Blank Generator output."""
    fill_blanks: List[FillBlankQuestion] = Field(
        ..., min_length=1, description="List of fill-blank questions"
    )

    @classmethod
    def from_json_string(cls, json_str: str) -> "FillBlankGenerationOutput":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def to_display_format(self) -> str:
        lines = []
        for q in self.fill_blanks:
            lines.append(f"✏️ Câu {q.index}:")
            lines.append(q.text_with_blanks)
            lines.append("")
            lines.append("_" * 40)
            lines.append("")
        return "\n".join(lines)


# ============================================================
# True/False Generation Output Schemas
# ============================================================

class TrueFalseQuestion(BaseModel):
    """Schema for a single true/false question."""
    index: int = Field(..., ge=1, description="Question number (1-indexed)")
    statement: str = Field(..., min_length=10, description="Statement to evaluate")
    correct_answer: bool = Field(..., description="True or False")
    explanation: str = Field(..., min_length=5, description="Why the statement is true/false")


class TrueFalseGenerationOutput(BaseModel):
    """Schema for True/False Generator output."""
    true_false: List[TrueFalseQuestion] = Field(
        ..., min_length=1, description="List of true/false questions"
    )

    @classmethod
    def from_json_string(cls, json_str: str) -> "TrueFalseGenerationOutput":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def to_display_format(self) -> str:
        lines = []
        for q in self.true_false:
            lines.append(f"❓ Câu {q.index}:")
            lines.append(f"   {q.statement}")
            lines.append("   → Đúng hay Sai?")
            lines.append("")
            lines.append("_" * 40)
            lines.append("")
        return "\n".join(lines)


# ============================================================
# Question Validation Schemas (LLM #2 — Kiểm tra chất lượng)
# ============================================================

class QuestionValidation(BaseModel):
    """Kết quả validate 1 câu hỏi."""
    index: int = Field(..., description="Question index being validated")
    is_valid: bool = Field(..., description="Whether this question passes validation")
    issues: List[str] = Field(
        default_factory=list,
        description="List of issues found, e.g. ['Đáp án sai', 'Kiến thức không có trong context']"
    )
    fixed_question: Optional[Dict[str, Any]] = Field(
        None, description="Auto-fixed question if validator could fix it"
    )


class ValidationResult(BaseModel):
    """Kết quả validate toàn bộ batch câu hỏi."""
    all_valid: bool = Field(..., description="True if all questions passed")
    validations: List[QuestionValidation] = Field(
        ..., description="Validation result per question"
    )
    approved_questions: List[Dict[str, Any]] = Field(
        default_factory=list, description="Questions that passed validation"
    )

    @classmethod
    def from_json_string(cls, json_str: str) -> "ValidationResult":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")


# ============================================================
# Slide Generation Output Schemas
# ============================================================

class SlideItem(BaseModel):
    """Schema for a single slide."""
    slide_type: Literal["title", "content", "exercise", "image", "summary"] = Field(
        ..., description="Type of slide"
    )
    title: str = Field(..., description="Slide title")
    bullets: List[str] = Field(default_factory=list, description="Content bullet points")
    notes: Optional[str] = Field(None, description="Speaker notes")
    questions: Optional[List[Dict[str, Any]]] = Field(
        None, description="Exercise questions (for exercise slides)"
    )
    related_lessons: Optional[List[str]] = Field(
        None, description="Related lesson references (for summary slides)"
    )


class SlideGenerationOutput(BaseModel):
    """Schema for Slide Generator output."""
    lesson_title: str = Field(..., description="Lesson title")
    lesson_metadata: Dict[str, str] = Field(
        ..., description="Metadata: {book, grade, lesson}"
    )
    slides: List[SlideItem] = Field(..., min_length=1, description="List of slides")
    total_slides: int = Field(..., ge=1, description="Total number of slides")

    @classmethod
    def from_json_string(cls, json_str: str) -> "SlideGenerationOutput":
        try:
            data = json.loads(json_str)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def to_display_format(self) -> str:
        lines = [f"📊 {self.lesson_title} ({self.total_slides} slides)", "=" * 50, ""]
        for i, slide in enumerate(self.slides, 1):
            icon = {"title": "🎯", "content": "📖", "exercise": "✏️",
                    "image": "🖼️", "summary": "📋"}.get(slide.slide_type, "📄")
            lines.append(f"--- Slide {i} [{icon} {slide.slide_type}] ---")
            lines.append(f"  {slide.title}")
            for b in slide.bullets:
                lines.append(f"  • {b}")
            if slide.questions:
                lines.append(f"  📝 {len(slide.questions)} câu hỏi bài tập")
            lines.append("")
        return "\n".join(lines)


__all__ = [
    "MCQOption",
    "MCQQuestion",
    "MCQGenerationOutput",
    "ScoringOutput",
    "FallbackOutput",
    "FeedbackOutput",
    "ExtractMetadataOutput",
    # Phase 2 — Question types
    "EssayQuestion",
    "EssayGenerationOutput",
    "FillBlankQuestion",
    "FillBlankGenerationOutput",
    "TrueFalseQuestion",
    "TrueFalseGenerationOutput",
    # Phase 2 — Validation
    "QuestionValidation",
    "ValidationResult",
    # Phase 2 — Slide
    "SlideItem",
    "SlideGenerationOutput",
]
