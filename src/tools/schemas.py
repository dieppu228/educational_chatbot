"""schemas.py — Pydantic models validate dữ liệu giữa Agent ↔ Tool.

Tại sao cần schemas?
  - Agent gửi params cho tool → cần validate đúng format
  - Tool trả kết quả → cần structure rõ ràng để Agent xử lý
  - Tránh lỗi runtime do dữ liệu sai kiểu/thiếu field

Mỗi tool có cặp Input/Output schema riêng:
  - KnowledgeRetrievalInput  → KnowledgeRetrievalOutput
  - ContentFormatterInput    → ContentFormatterOutput
  - WebSearchInput           → WebSearchOutput (placeholder)

Metadata fields mapping:
  Nguồn gốc: src/rag/chunking.py::ChunkMetadata dataclass
  ┌──────────────┬───────────────────────────────────────────────┐
  │ Field        │ Ý nghĩa                                      │
  ├──────────────┼───────────────────────────────────────────────┤
  │ book         │ Bộ sách: CD (Cánh Diều), KNTT (Kết Nối TT)  │
  │ grade        │ Lớp: "10", "11", "12"                        │
  │ topic        │ Mã chủ đề: "A", "B", "C", ...                │
  │ topic_name   │ Tên chủ đề đầy đủ                            │
  │ lesson       │ Mã bài: "Bài 1", "Bài 2", ...               │
  │ lesson_name  │ Tên bài học đầy đủ                           │
  │ section      │ Section con trong bài                        │
  │ title        │ Tiêu đề section/heading                      │
  │ level        │ Cấp heading: 1-6 (1=Bài, 2=Mục, 3+=Chi tiết)│
  │ type         │ Loại nội dung: theory, exercise, objective...│
  └──────────────┴───────────────────────────────────────────────┘
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ============================================================
# CHUNG — Dùng cho mọi tool
# ============================================================

class ToolCallRequest(BaseModel):
    """Request gọi một tool — Agent gửi tới MCP Server.

    Ví dụ:
        {
            "tool_name": "knowledge_retrieval",
            "params": {"query": "biến trong Python", "book": "CD"}
        }
    """
    tool_name: str = Field(..., description="Tên tool cần gọi")
    params: Dict[str, Any] = Field(default_factory=dict, description="Params đầu vào cho tool")


class ToolCallResponse(BaseModel):
    """Response từ tool — MCP Server trả về cho Agent.

    Ví dụ:
        {
            "tool_name": "knowledge_retrieval",
            "success": true,
            "data": [...chunks...],
            "error": null,
            "metadata": {"execution_time_s": 0.45, "strategy": "HIERARCHICAL"}
        }
    """
    tool_name: str = Field(..., description="Tên tool đã gọi")
    success: bool = Field(..., description="True nếu thành công")
    data: Any = Field(None, description="Kết quả trả về")
    error: Optional[str] = Field(None, description="Thông báo lỗi nếu fail")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Thông tin bổ sung")


# ============================================================
# KNOWLEDGE RETRIEVAL TOOL — Tra cứu SGK qua RAG
# ============================================================

class KnowledgeRetrievalInput(BaseModel):
    """Input cho KnowledgeRetrievalTool.

    Agent truyền query + optional metadata hints.
    Mỗi field đều ảnh hưởng tới RAG strategy selection:
      - grade + topic → HIERARCHICAL (2-phase retrieval)
      - broad keywords → BROAD (metadata-only filter)
      - curriculum keywords → CURRICULUM (lesson list)
      - không có hints → STANDARD (hybrid BM25+semantic)
    """
    # ── Required ──────────────────────────────────────────────
    query: str = Field(..., description="Câu hỏi / nội dung cần tra cứu")

    # ── Intent & Task hints ───────────────────────────────────
    # Ảnh hưởng tới strategy: explain → có thể HIERARCHICAL, generate → BROAD/HRAG
    intent_hint: Optional[str] = Field(
        None,
        description="Gợi ý intent: 'explain' (giải thích) hoặc 'generate' (tạo nội dung)"
    )
    # Ảnh hưởng tới rerank top_n: slide→15, lesson_plan→20, default→5
    task_type: Optional[str] = Field(
        None,
        description=(
            "Loại task quyết định số chunks giữ lại sau rerank: "
            "'slide' | 'slide_generate' (top 15), "
            "'lesson_plan' | 'giao_an' (top 20), "
            "'mcq' | 'essay' | 'fill_blank' | 'true_false' | 'explain' (top 5)"
        )
    )

    # ── Chunk Metadata filters ────────────────────────────────
    # Mapping 1:1 với ChunkMetadata trong src/rag/chunking.py
    book: Optional[str] = Field(
        None,
        description="Bộ sách SGK: 'CD' (Cánh Diều) hoặc 'KNTT' (Kết Nối Tri Thức)"
    )
    grade: Optional[str] = Field(
        None,
        description="Lớp học: '10', '11', '12'. Ảnh hưởng tới scope tìm kiếm"
    )
    topic: Optional[str] = Field(
        None,
        description="Mã chủ đề: 'A', 'B', 'C', ... Dùng cho metadata filter"
    )
    topic_name: Optional[str] = Field(
        None,
        description="Tên chủ đề đầy đủ. Ảnh hưởng tới BROAD/CURRICULUM strategy"
    )
    lesson: Optional[str] = Field(
        None,
        description="Mã bài học: 'Bài 1', 'Bài 2', ... Dùng cho scoped search"
    )
    lesson_name: Optional[str] = Field(
        None,
        description="Tên bài học đầy đủ. Dùng cho metadata filter"
    )
    section: Optional[str] = Field(
        None,
        description="Section con trong bài. Dùng cho fine-grained search"
    )
    title: Optional[str] = Field(
        None,
        description="Tiêu đề heading cụ thể cần tìm"
    )
    level: Optional[int] = Field(
        None, ge=1, le=6,
        description=(
            "Cấp heading filter: "
            "1=Bài học, 2=Mục chính, 3=Mục con, 4+=Chi tiết. "
            "HRAG Phase 1 dùng level 1-2, Phase 2 dùng level 3+"
        )
    )
    chunk_type: Optional[str] = Field(
        None,
        description=(
            "Loại nội dung chunk: "
            "'theory' (lý thuyết), 'exercise' (bài tập), "
            "'objective' (mục tiêu), 'summary' (tóm tắt), "
            "'application' (vận dụng), 'note' (chú ý)"
        )
    )


# ── Chunk Metadata schema (output) ───────────────────────────

class ChunkMetadataSchema(BaseModel):
    """Schema đầy đủ cho metadata của một chunk.

    Mapping 1:1 với dataclass ChunkMetadata trong src/rag/chunking.py.
    Mỗi field đều ảnh hưởng tới cách RAG pipeline xử lý:
      - book/grade: scope tìm kiếm (book_indices)
      - topic/topic_name: BROAD + CURRICULUM strategy
      - lesson/lesson_name: HRAG parent-child matching
      - level: HRAG Phase 1 (≤2) vs Phase 2 (≥3)
      - type: metadata filter (objective cho BROAD/CURRICULUM)
    """
    book: str = Field("", description="Bộ sách: 'CD' hoặc 'KNTT'")
    grade: str = Field("", description="Lớp: '10', '11', '12'")
    topic: str = Field("", description="Mã chủ đề: 'A', 'B', ...")
    topic_name: str = Field("", description="Tên chủ đề đầy đủ")
    lesson: str = Field("", description="Mã bài: 'Bài 1', 'Bài 2', ...")
    lesson_name: str = Field("", description="Tên bài học đầy đủ")
    section: str = Field("", description="Section con trong bài")
    title: str = Field("", description="Tiêu đề section/heading")
    level: int = Field(0, ge=0, le=6, description="Cấp heading: 1-6")
    type: str = Field(
        "theory",
        description="Loại: 'theory'|'exercise'|'objective'|'summary'|'application'|'note'"
    )


class RetrievedChunk(BaseModel):
    """Một chunk kết quả từ RAG pipeline — đầy đủ mọi field.

    Bao gồm:
      - doc_id: vị trí trong corpus (dùng cho scoped search)
      - content: nội dung text chính
      - context: breadcrumb path (topic > lesson > section)
      - metadata: ChunkMetadataSchema đầy đủ
      - Các điểm score từ retrieval pipeline
    """
    doc_id: int = Field(..., description="Index trong corpus (0-based)")
    content: str = Field(..., description="Nội dung text chính của chunk")
    context: str = Field("", description="Breadcrumb: 'Topic > Lesson > Section'")
    metadata: ChunkMetadataSchema = Field(
        default_factory=ChunkMetadataSchema,
        description="Metadata đầy đủ của chunk"
    )

    # ── Scores từ retrieval pipeline ──────────────────────────
    # Mỗi bước trong pipeline gắn thêm score riêng
    score: Optional[float] = Field(
        None,
        description="RRF score (sau khi combine BM25 + Semantic)"
    )
    bm25_score: Optional[float] = Field(
        None,
        description="BM25 keyword matching score (TF-IDF based)"
    )
    semantic_score: Optional[float] = Field(
        None,
        description="Cosine similarity score (embedding-based)"
    )
    rerank_score: Optional[float] = Field(
        None,
        description="Cross-Encoder reranking score (final relevance)"
    )


class KnowledgeRetrievalOutput(BaseModel):
    """Output của KnowledgeRetrievalTool — đầy đủ thông tin retrieval.

    Bao gồm:
      - chunks: danh sách kết quả với metadata đầy đủ
      - strategy_used: strategy mà AdaptiveRAGAgent đã chọn
      - metadata_filter: các filter đã áp dụng
      - retrieval timing
    """
    chunks: List[RetrievedChunk] = Field(
        default_factory=list,
        description="Danh sách chunks kết quả"
    )
    strategy_used: Optional[str] = Field(
        None,
        description="RAG strategy: 'standard'|'broad'|'curriculum'|'hierarchical'"
    )
    total_chunks: int = Field(0, description="Tổng số chunks trả về")
    query: str = Field("", description="Query gốc đã dùng")
    reason: str = Field(
        "",
        description="Lý do chọn strategy (từ QueryClassifier)"
    )
    metadata_filter: Dict[str, Any] = Field(
        default_factory=dict,
        description="Các metadata filter đã áp dụng: {grade, topic, book}"
    )
    retrieval_time_s: Optional[float] = Field(
        None,
        description="Thời gian retrieval (giây)"
    )


# ============================================================
# CONTENT FORMATTER TOOL — Format context cho LLM
# ============================================================

class ContentFormatterInput(BaseModel):
    """Input cho ContentFormatterTool."""
    chunks: List[Dict[str, Any]] = Field(
        ..., description="Danh sách chunks cần format (raw dict từ RAG)"
    )
    action: Optional[str] = Field(
        None,
        description=(
            "Loại action quyết định cách format: "
            "'generate_slide' | 'generate_lesson_plan' → grouped by topic/lesson, "
            "'generate_quiz' | 'explain_concept' → flat sorted by score"
        )
    )


class ContentFormatterOutput(BaseModel):
    """Output của ContentFormatterTool."""
    formatted_text: str = Field(..., description="Text đã format, sẵn sàng đưa vào LLM prompt")
    total_chunks: int = Field(0, description="Số chunks đã format")
    format_mode: str = Field(
        "flat",
        description="Chế độ format đã dùng: 'flat' (sort by score) hoặc 'grouped' (by topic/lesson)"
    )


# ============================================================
# WEB SEARCH TOOL — Placeholder (chưa implement)
# ============================================================

class WebSearchInput(BaseModel):
    """Input cho WebSearchTool (placeholder)."""
    query: str = Field(..., description="Từ khoá tìm kiếm")
    top_k: int = Field(5, ge=1, le=20, description="Số kết quả trả về")


class WebSearchResult(BaseModel):
    """Một kết quả tìm kiếm web."""
    title: str = Field("", description="Tiêu đề trang")
    link: str = Field("", description="URL")
    snippet: str = Field("", description="Đoạn trích")


class WebSearchOutput(BaseModel):
    """Output của WebSearchTool (placeholder)."""
    results: List[WebSearchResult] = Field(
        default_factory=list,
        description="Danh sách kết quả tìm kiếm"
    )
    total_results: int = Field(0, description="Tổng số kết quả")


__all__ = [
    "ToolCallRequest",
    "ToolCallResponse",
    "KnowledgeRetrievalInput",
    "KnowledgeRetrievalOutput",
    "ChunkMetadataSchema",
    "RetrievedChunk",
    "ContentFormatterInput",
    "ContentFormatterOutput",
    "WebSearchInput",
    "WebSearchOutput",
    "WebSearchResult",
]
