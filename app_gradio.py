"""
Gradio Chatbot Application — Orchestrator v2
=============================================
Giao dien 1 khung chat duy nhat.
Moi thu di qua Orchestrator: sinh quiz, slide, cham diem, on tap, giai thich, chat.

Pipeline:
  IntentRouter -> SessionManager -> ActionPlanner -> Handler -> SessionStore

Debug panel hien thi ket qua tung node.
"""

import sys
import os
import json
import gradio as gr
from pathlib import Path

# ── Project root setup ─────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
for p in [str(PROJECT_ROOT), str(PROJECT_ROOT / 'src')]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / '.env')

# ── Imports ────────────────────────────────────────────────────
from src.config.config import settings
from src.rag.retrieve_rebuild import CustomSearch
from src.rag.reranker import Reranker
from src.llm.orchestrator import Orchestrator
from src.llm.memory import MemoryManager

# ── Global refs ────────────────────────────────────────────────
searcher = None
reranker = None
orchestrator = None


# ============================================================
# INITIALIZATION
# ============================================================

def init_components():
    """Khoi tao tat ca components. Goi 1 lan trong main()."""
    global searcher, reranker, orchestrator

    DATA_DIR = PROJECT_ROOT / 'data'
    CHUNKS_PATH = str(DATA_DIR / 'rag_chunks_v2.json')
    EMBEDDINGS_PATH = str(DATA_DIR / 'embeddings.npy')

    print("=" * 60)
    print("Initializing Gradio Application (Orchestrator v2)...")
    print("=" * 60, flush=True)

    # 1. CustomSearch (BM25 + Semantic + RRF)
    print("Loading CustomSearch (BM25 + Semantic)...", flush=True)
    searcher = CustomSearch(
        chunks_path=CHUNKS_PATH,
        embeddings_path=EMBEDDINGS_PATH
    )
    print(f"   CustomSearch: {searcher.corpus_size} chunks, dim={searcher.embeddings.shape[1]}", flush=True)

    # 2. Reranker (CrossEncoder — lazy load)
    print("Initializing Reranker...", flush=True)
    reranker = Reranker()
    print("   Reranker ready (lazy load)", flush=True)

    # 3. Orchestrator v2
    print("Initializing Orchestrator v2...", flush=True)
    orchestrator = Orchestrator(retriever=searcher, reranker=reranker)
    print("   Orchestrator ready", flush=True)

    print("=" * 60)
    print("All components are ready!")
    print("=" * 60, flush=True)


# ============================================================
# CHAT HANDLER
# ============================================================

def chat_response(message, history):
    """Process message through Orchestrator pipeline."""
    if not message or not message.strip():
        return history, ""

    history = history + [{"role": "user", "content": message}]

    full_response = ""
    try:
        for chunk in orchestrator.ask(message):
            full_response += chunk
        history = history + [{"role": "assistant", "content": full_response}]
    except Exception as e:
        history = history + [{"role": "assistant", "content": f"Loi: {str(e)[:300]}"}]

    # Build debug text from orchestrator.last_debug_info
    debug_text = format_debug_info(orchestrator.last_debug_info)

    return history, debug_text


def format_debug_info(debug_info: dict) -> str:
    """Format debug info dict into readable markdown."""
    if not debug_info:
        return "*Chua co debug info*"

    lines = []
    lines.append(f"**Query:** `{debug_info.get('query', '?')[:80]}`\n")

    for step in debug_info.get("steps", []):
        node = step.get("node", "?")

        if node == "ContextAnalyzer":
            enriched = "Co" if step.get("enriched") else "Khong"
            lines.append(f"**[1] ContextAnalyzer** — Enriched: {enriched}")

        elif node == "IntentRouter":
            lines.append(
                f"**[2] IntentRouter** ({step.get('time_s', '?')}s)\n"
                f"  - Intent: `{step.get('primary_intent')}`\n"
                f"  - Task type: `{step.get('task_type')}`\n"
                f"  - Topic: `{step.get('topic')}`\n"
                f"  - New topic: `{step.get('is_new_topic')}`"
            )

        elif node == "SessionManager":
            lines.append(
                f"**[3] SessionManager**\n"
                f"  - Session ID: `{step.get('session_id')}`\n"
                f"  - Topic: `{step.get('topic')}`\n"
                f"  - Messages: {step.get('total_messages')}\n"
                f"  - Quiz state: {step.get('has_quiz_state')}\n"
                f"  - Slide state: {step.get('has_slide_state')}"
            )

        elif node == "ActionPlanner":
            lines.append(
                f"**[4] ActionPlanner**\n"
                f"  - Action: `{step.get('action')}`\n"
                f"  - Reason: {step.get('reason')}"
            )
            if step.get("round_id") is not None:
                lines.append(f"  - Round ID: {step.get('round_id')}")

        elif node == "RAG":
            if step.get("error"):
                lines.append(f"**[5] RAG** — Error: {step.get('error')}")
            else:
                lines.append(
                    f"**[5] RAG Search** ({step.get('time_s', '?')}s)\n"
                    f"  - Search results: {step.get('search_results')}\n"
                    f"  - After rerank: {step.get('reranked')}"
                )
                for preview in step.get("top_chunks", []):
                    lines.append(f"  - `{preview[:100]}`")

        lines.append("")

    total = debug_info.get("total_time_s")
    if total:
        lines.append(f"**Total time: {total}s**")

    return "\n".join(lines)


def clear_chat():
    """Reset orchestrator memory."""
    orchestrator.memory = MemoryManager()
    return [], "*Reset — chua co debug info*"


# ============================================================
# CUSTOM CSS
# ============================================================

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }

.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 28px 32px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
}
.app-header h1 { margin: 0 0 6px 0; font-size: 1.8em; font-weight: 700; }
.app-header p  { margin: 0; opacity: 0.9; font-size: 0.95em; }

.primary-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-size: 1em !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
}
.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.45) !important;
}

.debug-panel {
    background: #1a1a2e !important;
    border: 1px solid #333 !important;
    border-radius: 12px !important;
    font-size: 0.85em !important;
}

.app-footer {
    text-align: center;
    padding: 16px;
    opacity: 0.6;
    font-size: 0.85em;
}
"""


# ============================================================
# BUILD GRADIO UI — Single Chat Interface
# ============================================================

def build_ui():
    """Tao Gradio UI — 1 khung chat duy nhat + debug panel."""
    with gr.Blocks(
        title="EduBot — Tro ly Giao duc Tin Hoc",
        theme=gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="purple",
            neutral_hue="slate",
            font=gr.themes.GoogleFont("Inter"),
        ),
        css=CUSTOM_CSS,
    ) as demo:

        # ── Header ──
        gr.HTML("""
        <div class="app-header">
            <h1>🤖 EduBot — Trợ lý Giáo dục Tin Học</h1>
            <p>Sinh câu hỏi · Chấm điểm · Ôn tập · Sinh slide · Giải thích kiến thức · Chat tự do</p>
        </div>
        """)

        # ── Main Chat ──
        chatbot_ui = gr.Chatbot(
            height=520,
            show_copy_button=True,
            show_label=False,
            type="messages",
            placeholder="Hãy hỏi bất cứ điều gì: tạo câu hỏi, sinh slide, giải thích kiến thức...",
        )

        with gr.Row():
            chat_input = gr.Textbox(
                placeholder="VD: Tạo 3 câu trắc nghiệm về mạng LAN | Sinh slide bài An toàn thông tin | Mạng máy tính là gì?",
                show_label=False,
                lines=2,
                scale=5,
            )
            chat_send = gr.Button(
                "📤 Gửi", variant="primary", scale=1,
                elem_classes=["primary-btn"],
            )

        with gr.Row():
            chat_clear = gr.Button("🗑️ Xóa lịch sử", variant="secondary", scale=1)
            gr.HTML("<div style='flex:4'></div>")  # spacer

        # ── Debug Panel ──
        with gr.Accordion("🔍 Pipeline Debug — Kết quả từng Node", open=False):
            debug_output = gr.Markdown(
                value="*Chờ xử lý tin nhắn đầu tiên...*",
                elem_classes=["debug-panel"],
            )

        # ── Quick Actions (gợi ý nhanh) ──
        with gr.Accordion("💡 Gợi ý nhanh", open=False):
            gr.Markdown("""
| Chức năng | Ví dụ câu lệnh |
|-----------|----------------|
| **Sinh câu hỏi** | "Tạo 5 câu trắc nghiệm về mạng LAN" |
| **Tự luận** | "Cho tôi 3 câu tự luận về hệ điều hành" |
| **Đúng/Sai** | "Sinh 4 câu đúng sai về an toàn thông tin" |
| **Điền khuyết** | "Tạo 3 câu điền khuyết về thuật toán" |
| **Chấm điểm** | "Câu 1 là A, câu 2 là C" |
| **Ôn tập** | "Ôn lại câu sai lần 1" |
| **Sinh slide** | "Tạo slide bài mạng máy tính" |
| **Giải thích** | "Giải thích mạng WAN là gì" |
| **Xem điểm** | "Xem thống kê điểm số" |
| **Chat** | "Xin chào" |
""")

        # ── System Info ──
        with gr.Accordion("ℹ️ Thông tin hệ thống", open=False):
            info_text = (
                f"| Thành phần | Giá trị |\n|---|---|\n"
                f"| **Chunks** | {searcher.corpus_size:,} |\n"
                f"| **Embedding dim** | {searcher.embeddings.shape[1]} |\n"
                f"| **Embedding model** | `{settings.EMBEDDING_MODEL}` |\n"
                f"| **Reranker model** | `{settings.RERANKER_MODEL}` |\n"
                f"| **LLM model** | `{settings.LLM_MODEL}` |\n"
                f"| **Orchestrator** | v2 (code-level) |\n"
                f"| **API Key** | {'Set' if os.getenv('GENAI_API_KEY') else 'Not set'} |"
            )
            gr.Markdown(info_text)

        # ── Footer ──
        gr.HTML("""
        <div class="app-footer">
            <p>🎓 Đồ án tốt nghiệp — Hệ thống hỗ trợ giảng dạy Tin Học THPT bằng AI</p>
        </div>
        """)

        # ── Event Handlers ──
        chat_send.click(
            fn=chat_response,
            inputs=[chat_input, chatbot_ui],
            outputs=[chatbot_ui, debug_output],
        ).then(lambda: "", outputs=chat_input)

        chat_input.submit(
            fn=chat_response,
            inputs=[chat_input, chatbot_ui],
            outputs=[chatbot_ui, debug_output],
        ).then(lambda: "", outputs=chat_input)

        chat_clear.click(
            fn=clear_chat,
            outputs=[chatbot_ui, debug_output],
        )

    return demo


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # 1. Init
    init_components()

    # 2. Build UI
    print("\nBuilding Gradio UI (Single Chat + Debug)...", flush=True)
    demo = build_ui()

    # 3. Launch
    print("Starting server on http://127.0.0.1:7860", flush=True)
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        show_api=False,
    )