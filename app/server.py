import sys
import os
from pathlib import Path
import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for p in [str(PROJECT_ROOT), str(PROJECT_ROOT / "src")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from src.utils.trace_decorator import logger, suppress_http_request_logs
from app.gradio_app import init_components, build_ui


def create_app():
    suppress_http_request_logs()
    logger.info("Initializing production Gradio components")
    init_components()
    demo = build_ui()

    # Mount Gradio as ASGI app (FastAPI-compatible)
    app = demo.app
    return demo, app


if __name__ == "__main__":
    suppress_http_request_logs()
    demo, app = create_app()

    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    logger.info("Starting Gradio server on http://127.0.0.1:%s", server_port)
    demo.launch(
        server_name="127.0.0.1",
        server_port=server_port,
        share=False,
        show_error=False,
    )
