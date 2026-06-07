import sys
import os
import re
from pathlib import Path

# ── Path setup ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
for p in [str(PROJECT_ROOT), str(PROJECT_ROOT / "src")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, Literal

from src.config.config import settings
from src.rag.retrieve_rebuild import CustomSearch
from src.rag.reranker import Reranker
from src.llm.orchestrator import Orchestrator
from src.utils.trace_decorator import logger, suppress_http_request_logs

suppress_http_request_logs()

# ── Init components ──
DATA_DIR = PROJECT_ROOT / "data"

logger.info("Loading API components")
searcher = CustomSearch(
    chunks_path=str(DATA_DIR / "rag_chunks_v2.json"),
    embeddings_path=str(DATA_DIR / "embeddings.npy"),
)
reranker = Reranker()
orchestrator = Orchestrator(retriever=searcher, reranker=reranker)
logger.info("All API components ready")

# ── FastAPI app ──
app = FastAPI(title="EduBot API")

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"

NO_CACHE_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0",
}


# ── Schemas ──
class ChatRequest(BaseModel):
    message: str
    book: Optional[str] = None
    grade: Optional[str] = None
    user_id: str = "anonymous"
    hitl_type: Optional[Literal["outline_review"]] = None
    hitl_approved: Optional[bool] = None
    edited_outline: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    content: str
    debug: Optional[dict] = None
    hitl: Optional[dict] = None
    export: Optional[dict] = None


# ── API Routes ──
@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    ui_book = req.book if req.book in {"CD", "KNTT"} else None
    ui_grade = req.grade if req.grade in {"10", "11", "12"} else None

    full_response = ""
    debug_info = None
    previous_export = orchestrator.get_last_export(req.user_id)
    previous_export_id = previous_export.get("file_id") if previous_export else None
    try:
        async for chunk in orchestrator.ask_async(
            req.message,
            ui_book=ui_book,
            ui_grade=ui_grade,
            user_id=req.user_id,
            hitl_type=req.hitl_type,
            hitl_approved=req.hitl_approved,
            edited_outline=req.edited_outline,
        ):
            full_response += chunk
    except Exception as e:
        full_response = f"Lỗi: {str(e)[:300]}"
        debug_info = {
            "user_id": req.user_id,
            "query": req.message,
            "error": str(e)[:300],
        }

    if debug_info is None:
        debug_info = orchestrator.get_debug_info(req.user_id)

    current_export = orchestrator.get_last_export(req.user_id)
    response_export = (
        current_export
        if current_export and current_export.get("file_id") != previous_export_id
        else None
    )

    return ChatResponse(
        content=full_response,
        debug=debug_info,
        hitl=orchestrator.get_pending_hitl(req.user_id),
        export=response_export,
    )


@app.get("/api/frontend-info")
async def frontend_info():
    index_path = FRONTEND_DIR / "index.html"
    index_html = index_path.read_text(encoding="utf-8")
    return {
        "frontend_dir": str(FRONTEND_DIR),
        "index_path": str(index_path),
        "index_mtime": index_path.stat().st_mtime,
        "ui_version": "export-pptx-1",
        "has_book_select": 'id="bookSelect"' in index_html,
        "has_grade_select": 'id="gradeSelect"' in index_html,
    }


EXPORT_DIR = PROJECT_ROOT / "app" / "data" / "exports"


@app.get("/api/exports/{file_id}")
async def download_export(file_id: str):
    if not re.fullmatch(r"[a-f0-9]{32}\.pptx", file_id):
        raise HTTPException(status_code=400, detail="Invalid export file id")
    path = (EXPORT_DIR / file_id).resolve()
    if path.parent != EXPORT_DIR.resolve() or not path.is_file():
        raise HTTPException(status_code=404, detail="Export file not found")
    return FileResponse(
        str(path),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=file_id,
    )


# ── Serve Frontend ──
app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR)), name="assets")


@app.get("/")
async def root():
    return FileResponse(str(FRONTEND_DIR / "index.html"), headers=NO_CACHE_HEADERS)


@app.get("/{path:path}")
async def static_files(path: str):
    file_path = FRONTEND_DIR / path
    if file_path.is_file():
        return FileResponse(str(file_path), headers=NO_CACHE_HEADERS)
    return FileResponse(str(FRONTEND_DIR / "index.html"), headers=NO_CACHE_HEADERS)


if __name__ == "__main__":
    import uvicorn
    suppress_http_request_logs()
    host = os.getenv("EDUBOT_HOST", "127.0.0.1")
    port = int(os.getenv("EDUBOT_PORT", "8000"))
    logger.info("Starting EduBot API on http://%s:%s", host, port)
    uvicorn.run(app, host=host, port=port, access_log=False)
