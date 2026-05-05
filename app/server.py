import sys
from pathlib import Path
import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for p in [str(PROJECT_ROOT), str(PROJECT_ROOT / "src")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from app.gradio_app import init_components, build_ui


def create_app():
    init_components()
    demo = build_ui()

    # Mount Gradio as ASGI app (FastAPI-compatible)
    app = demo.app
    return demo, app


if __name__ == "__main__":
    demo, app = create_app()

    print("Starting production server on http://0.0.0.0:7860", flush=True)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=False,
        show_api=False,
    )
