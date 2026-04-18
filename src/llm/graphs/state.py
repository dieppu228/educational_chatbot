"""
ContentSupervisorState — State schema cho LangGraph supervisor.

LangGraph yêu cầu TypedDict với Annotated reducers.
State này được chia sẻ giữa tất cả graph nodes.
"""

from typing import TypedDict, Annotated, Optional
from langgraph.graph import add_messages


class ContentSupervisorState(TypedDict):
    """
    State cho ContentSupervisor graph.

    Các field chia thành 4 nhóm:
        - Input: từ caller (SlideService)
        - Intermediate: populated bởi preprocess + agents
        - Output: kết quả cuối
        - Messages: conversation history cho supervisor LLM
    """

    # ── Messages (supervisor LLM conversation) ──
    messages: Annotated[list, add_messages]

    # ── Input (set bởi caller) ──
    task_type: str              # "slide" | "lesson_plan"
    request_id: str
    query: str
    topic: str
    grade: str
    book: str
    rag_chunks: list            # Raw RAG chunks from retrieval

    # ── Intermediate (populated bởi nodes/tools) ──
    context_map: str            # Preprocessed grouped context text
    chunk_map: dict             # Dict[chunk_id → content]
    outline_payload: Optional[dict]     # OutlinePayload
    content_payload: Optional[dict]     # ContentPayload
    media_payload: Optional[dict]       # MediaPayload
    quiz_payload: Optional[dict]        # QuizPayload

    # ── Output ──
    merged_slides: Optional[list]       # List[MergedSlide dicts]
    final_output: Optional[dict]        # Final formatted output
    status: str                         # "pending" | "success" | "partial" | "failed"
    error_message: Optional[str]


__all__ = ["ContentSupervisorState"]
