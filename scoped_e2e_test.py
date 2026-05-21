import logging
from pathlib import Path

from src.llm.intent_router import IntentResult
from src.rag.rag_service import RAGService
from src.rag.reranker import Reranker
from src.rag.retrieve_rebuild import CustomSearch
from src.schemas.context import RequestContext


QUERY = "cho 3 câu hỏi trắc nghiệm SQL và hệ quản trị cơ sở dữ liệu"


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )

    root = Path(__file__).resolve().parent
    retriever = CustomSearch(
        chunks_path=str(root / "data" / "rag_chunks_v2.json"),
        embeddings_path=str(root / "data" / "embeddings.npy"),
    )
    service = RAGService(retriever=retriever, reranker=Reranker())

    ctx = RequestContext(
        query=QUERY,
        ui_book="KNTT",
        ui_grade="12",
        user_id="scoped-e2e-test",
    )
    ctx.intent_result = IntentResult(
        primary_intent="generate",
        task_type="mcq",
        topic="SQL và hệ quản trị cơ sở dữ liệu",
    )
    ctx.resolve_book()
    ctx.resolve_grade()

    chunks = service.get_context(ctx, intent_hint="generate", task_type="mcq")

    print("\n--- RESULT ---")
    print("chunks:", len(chunks))
    print("requested_scope:", ctx.requested_scope)
    print("actual_scope:", ctx.actual_scope)
    print("scope_fallback_used:", ctx.scope_fallback_used)

    assert ctx.scope_fallback_used is True, "Expected soft UI scope fallback to be used"
    assert len(chunks) > 0, "Expected fallback search to return chunks"
    print("OK: scoped_e2e_test passed")


if __name__ == "__main__":
    main()
