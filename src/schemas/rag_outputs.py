"""
Pydantic schemas for RAG pipeline outputs.
Provides type-safe validation for retrieval and reranking results.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any


# ============================================================
# Retrieval Output Schemas
# ============================================================

class ChunkMetadata(BaseModel):
    """Metadata for a retrieved chunk"""
    grade: Optional[str] = Field(None, description="Grade level (10, 11, 12)")
    lesson: Optional[str] = Field(None, description="Lesson name/number")
    idea: Optional[str] = Field(None, description="Main idea/concept")
    level: Optional[int] = Field(None, ge=1, le=6, description="Heading level")
    title: Optional[str] = Field(None, description="Section title")
    type: str = Field(default="content", description="Content type")


class RetrievalResult(BaseModel):
    """
    Schema for a single retrieval result.
    Represents one document/chunk from hybrid search.
    """
    context: Optional[str] = Field(None, description="Parent context/breadcrumb")
    content: str = Field(..., description="Main content text")
    metadata: ChunkMetadata = Field(default_factory=ChunkMetadata, description="Chunk metadata")
    
    # Scores from different retrieval methods
    bm25_score: Optional[float] = Field(None, ge=0.0, description="BM25 keyword score")
    faiss_score: Optional[float] = Field(None, description="FAISS vector similarity score")
    rrf_score: Optional[float] = Field(None, ge=0.0, description="Combined RRF score")
    
    def get_display_content(self, max_length: int = 200) -> str:
        """Get truncated content for display"""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."


class RetrievalOutput(BaseModel):
    """
    Schema for complete retrieval output.
    Contains list of retrieved documents with scores.
    """
    results: List[RetrievalResult] = Field(default_factory=list, description="Retrieved documents")
    query: str = Field(..., description="Original search query")
    total_retrieved: int = Field(default=0, description="Total number retrieved")
    
    @field_validator('total_retrieved', mode='before')
    @classmethod
    def set_total(cls, v, info):
        """Auto-calculate total if not provided"""
        if v == 0 and 'results' in info.data:
            return len(info.data['results'])
        return v
    
    def get_top_k(self, k: int) -> List[RetrievalResult]:
        """Get top k results"""
        return self.results[:k]
    
    def get_contexts_text(self, separator: str = "\n\n---\n\n") -> str:
        """Combine all content into single text for LLM prompt"""
        return separator.join([r.content for r in self.results])


# ============================================================
# Reranking Output Schemas
# ============================================================

class RerankResult(BaseModel):
    """
    Schema for a single reranked result.
    Extends RetrievalResult with rerank score.
    """
    context: Optional[str] = Field(None, description="Parent context")
    content: str = Field(..., description="Main content text")
    metadata: ChunkMetadata = Field(default_factory=ChunkMetadata, description="Chunk metadata")
    
    # Original scores
    rrf_score: Optional[float] = Field(None, description="Original RRF score")
    
    # Reranking score
    rerank_score: float = Field(..., description="Score from reranker model")
    original_rank: Optional[int] = Field(None, ge=0, description="Rank before reranking")
    new_rank: Optional[int] = Field(None, ge=0, description="Rank after reranking")


class RerankOutput(BaseModel):
    """
    Schema for complete reranking output.
    Contains reranked list of documents.
    """
    results: List[RerankResult] = Field(default_factory=list, description="Reranked documents")
    query: str = Field(..., description="Original search query")
    top_n: int = Field(..., ge=1, description="Number of results after reranking")
    
    def get_contexts_for_prompt(self) -> str:
        """Get formatted contexts for LLM prompt"""
        parts = []
        for i, result in enumerate(self.results, 1):
            header = f"[Document {i}]"
            if result.metadata.title:
                header += f" - {result.metadata.title}"
            if result.metadata.grade:
                header += f" (Lớp {result.metadata.grade})"
            
            parts.append(f"{header}\n{result.content}")
        
        return "\n\n---\n\n".join(parts)


__all__ = [
    "ChunkMetadata",
    "RetrievalResult",
    "RetrievalOutput",
    "RerankResult",
    "RerankOutput",
]
