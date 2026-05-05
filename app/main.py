import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for p in [str(PROJECT_ROOT), str(PROJECT_ROOT / "src")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from app.gradio_app import init_components, build_ui


if __name__ == "__main__":
    init_components()

    print("\nBuilding Gradio UI...", flush=True)
    demo = build_ui()

    print("Starting server on http://127.0.0.1:7860", flush=True)
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        show_api=False,
    )
