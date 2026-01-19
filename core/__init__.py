"""Core Pydantic models for the application"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class MCQOption(BaseModel):
    """Multiple choice options"""
    A: str
    B: str
    C: str
    D: str


class MCQQuestion(BaseModel):
    """Single MCQ question"""
    index: int = Field(ge=1, description="Question number (1-indexed)")
    question: str = Field(..., description="Question text")
    options: MCQOption = Field(..., description="Answer options")
    correct_answer: str = Field(pattern="^[A-D]$", description="Correct answer letter")
    explanation: str = Field(..., description="Explanation for the answer")


class MCQResponse(BaseModel):
    """Complete MCQ response with multiple questions"""
    mcq: List[MCQQuestion] = Field(..., min_items=1, description="List of questions")


class ChunkMetadata(BaseModel):
    """Metadata for a chunk"""
    grade: str = Field(..., description="Grade level (10, 11, or 12)")
    lesson: Optional[str] = Field(default=None, description="Lesson number")
    idea: Optional[str] = Field(default=None, description="Idea/concept identifier")
    level: int = Field(..., ge=1, le=6, description="Markdown heading level")
    title: str = Field(..., description="Section title")
    type: str = Field(default="content", description="Content type")


class Chunk(BaseModel):
    """A text chunk with metadata"""
    context: str = Field(..., description="Context/parent reference")
    content: str = Field(..., description="Main content")
    metadata: ChunkMetadata = Field(..., description="Metadata")


class ScoringResult(BaseModel):
    """Result of answer scoring"""
    status: str = Field(..., description="Status: 'found', 'not_found', 'ambiguous'")
    question_index: Optional[int] = Field(default=None, description="Question index (1-indexed)")
    question_text: Optional[str] = Field(default=None, description="Original question")
    user_answer: Optional[str] = Field(default=None, description="User's answer (A/B/C/D)")
    correct_answer: Optional[str] = Field(default=None, description="Correct answer (A/B/C/D)")
    is_correct: Optional[bool] = Field(default=None, description="Whether answer is correct")
    explanation: Optional[str] = Field(default=None, description="Feedback/explanation")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Confidence score")


class Query(BaseModel):
    """User query input"""
    text: str = Field(..., description="Query text")
    grade: Optional[str] = Field(default=None, description="Target grade")
    num_questions: Optional[int] = Field(default=None, ge=1, le=10, description="Number of questions")


class RetrievedDocument(BaseModel):
    """Retrieved document from search"""
    content: str = Field(..., description="Document content")
    metadata: ChunkMetadata = Field(..., description="Document metadata")
    score: float = Field(..., ge=0.0, description="Relevance score")


class ConversationContext(BaseModel):
    """Conversation history and context"""
    session_id: str = Field(..., description="Session ID")
    history: List[Dict[str, str]] = Field(default_factory=list, description="Message history")
    current_questions: Optional[MCQResponse] = Field(default=None, description="Current set of questions")
    grade_context: Optional[str] = Field(default=None, description="Selected grade")
