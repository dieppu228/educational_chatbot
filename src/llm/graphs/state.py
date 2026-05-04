
from typing import TypedDict, Annotated, Optional
from langgraph.graph import add_messages


class ContentSupervisorState(TypedDict):

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
    synthesized_context: str     # LLM-synthesized context (cho Supervisor planning)
    context_map: str            # Preprocessed grouped context text (cho sub-agents)
    chunk_map: dict             # Dict[chunk_id → content] (cho sub-agents)
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
