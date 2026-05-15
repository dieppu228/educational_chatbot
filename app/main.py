import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for p in [str(PROJECT_ROOT), str(PROJECT_ROOT / "src")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from src.utils.trace_decorator import logger, suppress_http_request_logs
from app.gradio_app import init_components, build_ui


if __name__ == "__main__":
    suppress_http_request_logs()
    logger.info("Starting Gradio application bootstrap")
    init_components()

    logger.info("Building Gradio UI")
    demo = build_ui()

    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    logger.info("Starting server on http://127.0.0.1:%s", server_port)
    demo.launch(
        server_name="127.0.0.1",
        server_port=server_port,
        share=False,
        show_error=True,
    )
