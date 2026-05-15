import sys
import os
from pathlib import Path

# ── Path setup ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
for p in [str(PROJECT_ROOT), str(PROJECT_ROOT / "src")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

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


# ── Schemas ──
class ChatRequest(BaseModel):
    message: str
    book: Optional[str] = None
    user_id: str = "anonymous"


class ChatResponse(BaseModel):
    content: str
    debug: Optional[dict] = None


# ── API Routes ──
@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    ui_book = req.book if req.book and req.book != "auto" else None

    full_response = ""
    try:
        async for chunk in orchestrator.ask_async(req.message, ui_book=ui_book, user_id=req.user_id):
            full_response += chunk
    except Exception as e:
        full_response = f"Lỗi: {str(e)[:300]}"

    debug_info = orchestrator.last_debug_info

    return ChatResponse(content=full_response, debug=debug_info)


# ── Serve Frontend ──
app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR)), name="assets")


@app.get("/")
async def root():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/{path:path}")
async def static_files(path: str):
    file_path = FRONTEND_DIR / path
    if file_path.is_file():
        return FileResponse(str(file_path))
    return FileResponse(str(FRONTEND_DIR / "index.html"))


if __name__ == "__main__":
    import uvicorn
    suppress_http_request_logs()
    host = os.getenv("EDUBOT_HOST", "127.0.0.1")
    port = int(os.getenv("EDUBOT_PORT", "8000"))
    logger.info("Starting EduBot API on http://%s:%s", host, port)
    uvicorn.run(app, host=host, port=port, access_log=False)
