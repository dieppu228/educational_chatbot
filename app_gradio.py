"""
Gradio Chatbot Application — Phase 2 Full Pipeline
===================================================
Demo hệ thống sinh câu hỏi + slide bài giảng tự động.

Pipeline:
  IntentDetector → CustomSearch (BM25 + Semantic + RRF)
  → Reranker (CrossEncoder) → Handlers → Validator → Output

Tabs:
  1. Sinh câu hỏi  — MCQ / Essay / Fill-blank / True-False
  2. Sinh slide     — Tạo bài giảng HTML từ nội dung SGK
  3. Chat tự do     — Hỏi đáp chung (chatbot.ask)
"""

import sys
import os
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
from src.llm.conversation import ChatBot
from src.llm.utils import format_contexts
from src.llm.handlers.question.mcq_handler import MCQHandler
from src.llm.handlers.question.essay_handler import EssayHandler
from src.llm.handlers.question.fill_handler import FillHandler
from src.llm.handlers.question.true_false_handler import TrueFalseHandler
from src.llm.handlers.content.slide_handler import SlideHandler
from src.llm.handlers.content.slide_template import SlideTemplate

# ── Global refs (gán trong init_components) ────────────────────
searcher = None
reranker = None
chatbot = None
question_handlers = {}
slide_handler = None


# ============================================================
# INITIALIZATION — gọi 1 lần khi app start
# ============================================================

def init_components():
    """Khởi tạo tất cả components. Gọi 1 lần trong main()."""
    global searcher, reranker, chatbot, question_handlers, slide_handler

    DATA_DIR = PROJECT_ROOT / 'data'
    CHUNKS_PATH = str(DATA_DIR / 'rag_chunks_v2.json')
    EMBEDDINGS_PATH = str(DATA_DIR / 'embeddings.npy')

    print("=" * 60)
    print("Initializing Gradio Application...")
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

    # 3. ChatBot orchestrator
    print("Initializing ChatBot...", flush=True)
    chatbot = ChatBot(retriever=searcher, reranker=reranker)
    print("   ChatBot ready", flush=True)

    # 4. Standalone handlers
    question_handlers.update({
        "mcq":        MCQHandler(),
        "essay":      EssayHandler(),
        "fill_blank": FillHandler(),
        "true_false": TrueFalseHandler(),
    })
    slide_handler = SlideHandler()
    print("   Handlers ready", flush=True)

    print("=" * 60)
    print("All components are ready!")
    print("=" * 60, flush=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def do_rag_search(query: str, top_k: int = 60, top_n: int = 10):
    """Chạy RAG pipeline: Search → Rerank, trả về contexts + debug info."""
    search_results = searcher.search(query, top_k=top_k)
    if not search_results:
        return [], "⚠️ Không tìm thấy tài liệu liên quan."

    reranked = reranker.rerank(query, search_results, top_n=top_n)

    lines = [f"🔍 **Hybrid Search:** {len(search_results)} kết quả → **Rerank:** {len(reranked)} kết quả\n"]
    for i, r in enumerate(reranked[:5], 1):
        score = r.get('rerank_score', r.get('score', 0))
        content_preview = r['content'][:120].replace('\n', ' ')
        lines.append(f"**[{i}]** score={score:.4f} · `{content_preview}…`")
    debug_text = "\n".join(lines)
    return reranked, debug_text


# ============================================================
# TAB 1: SINH CÂU HỎI
# ============================================================

def generate_questions(topic, question_type, num_questions):
    """Sinh câu hỏi: RAG → Handler → Display."""
    if not topic or not topic.strip():
        return "⚠️ Vui lòng nhập chủ đề.", "", ""

    type_map = {
        "Trắc nghiệm (MCQ)": "mcq",
        "Tự luận (Essay)":    "essay",
        "Điền khuyết (Fill)": "fill_blank",
        "Đúng/Sai (T/F)":    "true_false",
    }
    q_type = type_map.get(question_type, "mcq")
    handler = question_handlers[q_type]
    num_q = int(num_questions)

    # 1. RAG Search
    contexts, debug_text = do_rag_search(topic)
    if not contexts:
        return "⚠️ Không tìm thấy tài liệu phù hợp.", debug_text, ""

    context_text = format_contexts(contexts)

    # 2. Generate
    try:
        query_str = f"Tạo {num_q} câu {question_type.split('(')[0].strip()} về {topic}"
        output = handler.handle(query_str, context_text, num_questions=num_q)
    except Exception as e:
        return f"❌ Lỗi sinh câu hỏi: {e}", debug_text, ""

    # 3. Format display
    display = output.to_display_format()

    # 4. Answer info
    answer_lines = []
    if q_type == "mcq":
        for q in output.mcq:
            answer_lines.append(f"**Câu {q.index}:** {q.correct_answer} — {q.explanation}")
    elif q_type == "essay":
        for q in output.essays:
            answer_lines.append(
                f"**Câu {q.index} ({q.difficulty}):**\n"
                f"- Đáp án mẫu: {q.sample_answer[:200]}…\n"
                f"- Rubric: {q.rubric[:200]}…"
            )
    elif q_type == "fill_blank":
        for q in output.fill_blanks:
            answer_lines.append(f"**Câu {q.index}:** {', '.join(q.answers)} — {q.explanation}")
    elif q_type == "true_false":
        for q in output.true_false:
            tf_label = "Đúng ✅" if q.correct_answer else "Sai ❌"
            answer_lines.append(f"**Câu {q.index}:** {tf_label} — {q.explanation}")

    answer_text = "\n\n".join(answer_lines) if answer_lines else ""
    return display, debug_text, answer_text


# ============================================================
# TAB 2: SINH SLIDE
# ============================================================

def generate_slides(topic, book, grade, lesson):
    """Sinh slide bài giảng: RAG → SlideHandler → HTML render."""
    if not topic or not topic.strip():
        return "⚠️ Vui lòng nhập chủ đề.", "", "<p>Chưa có slide</p>"

    contexts, debug_text = do_rag_search(topic)
    if not contexts:
        return "⚠️ Không tìm thấy tài liệu.", debug_text, "<p>Không có dữ liệu</p>"

    context_text = format_contexts(contexts)

    try:
        slide_output = slide_handler.handle(
            book=book or "Kết nối tri thức",
            grade=grade or "10",
            lesson=lesson or topic,
            context=context_text
        )
    except Exception as e:
        return f"❌ Lỗi sinh slide: {e}", debug_text, "<p>Lỗi</p>"

    text_display = slide_output.to_display_format()
    html_display = SlideTemplate.render_to_html(slide_output)
    return text_display, debug_text, html_display


# ============================================================
# TAB 3: CHAT TỰ DO
# ============================================================

def chat_response(message, history):
    """Chat qua ChatBot.ask() generator."""
    if not message or not message.strip():
        return history

    history = history + [{"role": "user", "content": message}]

    full_response = ""
    try:
        for chunk in chatbot.ask(message):
            full_response += chunk
        history = history + [{"role": "assistant", "content": full_response}]
    except Exception as e:
        history = history + [{"role": "assistant", "content": f"❌ Lỗi: {str(e)[:200]}"}]

    return history


def clear_chat():
    """Reset chat."""
    from src.llm.memory import MemoryManager
    chatbot.memory = MemoryManager()
    return []


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

.tab-nav button {
    font-weight: 600 !important;
    font-size: 0.95em !important;
    padding: 12px 24px !important;
    border-radius: 12px 12px 0 0 !important;
}
.tab-nav button.selected {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
}

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

.app-footer {
    text-align: center;
    padding: 16px;
    opacity: 0.6;
    font-size: 0.85em;
}
"""


# ============================================================
# BUILD GRADIO UI
# ============================================================

def build_ui():
    """Tạo Gradio Blocks UI. Gọi sau khi init_components()."""
    with gr.Blocks(
        title="🤖 EduBot — Sinh câu hỏi & Slide SGK Tin Học",
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
            <p>Hệ thống sinh câu hỏi & slide bài giảng tự động · SGK Tin Học THPT</p>
        </div>
        """)

        with gr.Tabs():
            # ══════════════════════════════════════════════════
            # TAB 1: SINH CÂU HỎI
            # ══════════════════════════════════════════════════
            with gr.Tab("📝 Sinh câu hỏi"):
                gr.Markdown("### Sinh câu hỏi tự động từ SGK Tin Học")

                with gr.Row():
                    with gr.Column(scale=2):
                        q_topic = gr.Textbox(
                            label="📌 Chủ đề / Nội dung",
                            placeholder="VD: Mạng máy tính, An toàn thông tin...",
                            lines=2,
                        )
                    with gr.Column(scale=1):
                        q_type = gr.Dropdown(
                            label="📋 Loại câu hỏi",
                            choices=[
                                "Trắc nghiệm (MCQ)",
                                "Tự luận (Essay)",
                                "Điền khuyết (Fill)",
                                "Đúng/Sai (T/F)",
                            ],
                            value="Trắc nghiệm (MCQ)",
                        )
                    with gr.Column(scale=1):
                        q_num = gr.Slider(
                            label="🔢 Số câu",
                            minimum=1, maximum=10, step=1, value=3,
                        )

                q_btn = gr.Button(
                    "🚀 Sinh câu hỏi", variant="primary",
                    elem_classes=["primary-btn"]
                )

                with gr.Row():
                    with gr.Column(scale=3):
                        q_output = gr.Textbox(
                            label="📄 Câu hỏi được sinh",
                            lines=18, interactive=False,
                            show_copy_button=True,
                        )
                    with gr.Column(scale=2):
                        q_debug = gr.Markdown(
                            label="🔍 RAG Debug",
                            value="*Chờ sinh câu hỏi...*",
                        )

                with gr.Accordion("📋 Đáp án & Giải thích", open=False):
                    q_answer = gr.Markdown(value="*Chưa có đáp án*")

                q_btn.click(
                    fn=generate_questions,
                    inputs=[q_topic, q_type, q_num],
                    outputs=[q_output, q_debug, q_answer],
                )

            # ══════════════════════════════════════════════════
            # TAB 2: SINH SLIDE
            # ══════════════════════════════════════════════════
            with gr.Tab("📊 Sinh slide"):
                gr.Markdown("### Sinh bài giảng slide tự động")

                with gr.Row():
                    with gr.Column(scale=2):
                        s_topic = gr.Textbox(
                            label="📌 Chủ đề bài học",
                            placeholder="VD: Mạng máy tính...",
                            lines=2,
                        )
                    with gr.Column(scale=1):
                        s_book = gr.Dropdown(
                            label="📚 Bộ sách",
                            choices=["Kết nối tri thức", "Cánh Diều"],
                            value="Kết nối tri thức",
                        )
                    with gr.Column(scale=1):
                        s_grade = gr.Dropdown(
                            label="🎓 Khối lớp",
                            choices=["10", "11", "12"],
                            value="10",
                        )

                s_lesson = gr.Textbox(
                    label="📖 Tên bài học (tùy chọn)",
                    placeholder="VD: Bài 1 - Mạng máy tính",
                )

                s_btn = gr.Button(
                    "🚀 Sinh slide", variant="primary",
                    elem_classes=["primary-btn"]
                )

                with gr.Row():
                    with gr.Column(scale=2):
                        s_text = gr.Textbox(
                            label="📄 Cấu trúc slide (text)",
                            lines=15, interactive=False,
                            show_copy_button=True,
                        )
                    with gr.Column(scale=1):
                        s_debug = gr.Markdown(
                            label="🔍 RAG Debug",
                            value="*Chờ sinh slide...*",
                        )

                with gr.Accordion("🖥️ Xem slide (HTML Preview)", open=True):
                    s_html = gr.HTML(
                        value="<p style='text-align:center; color:#999; padding:40px;'>"
                              "Chưa có slide — nhấn Sinh slide để bắt đầu</p>"
                    )

                s_btn.click(
                    fn=generate_slides,
                    inputs=[s_topic, s_book, s_grade, s_lesson],
                    outputs=[s_text, s_debug, s_html],
                )

            # ══════════════════════════════════════════════════
            # TAB 3: CHAT TỰ DO
            # ══════════════════════════════════════════════════
            with gr.Tab("💬 Chat"):
                gr.Markdown("### Hỏi đáp tự do — Full pipeline")

                chatbot_ui = gr.Chatbot(
                    height=500,
                    show_copy_button=True,
                    show_label=False,
                    type="messages",
                )

                with gr.Row():
                    chat_input = gr.Textbox(
                        placeholder="VD: Tạo 3 câu trắc nghiệm về mạng LAN",
                        show_label=False, lines=2, scale=4,
                    )
                    chat_send = gr.Button(
                        "📤 Gửi", variant="primary", scale=1,
                        elem_classes=["primary-btn"],
                    )

                chat_clear = gr.Button("🗑️ Xóa lịch sử", variant="secondary")

                chat_send.click(
                    fn=chat_response,
                    inputs=[chat_input, chatbot_ui],
                    outputs=chatbot_ui,
                ).then(lambda: "", outputs=chat_input)

                chat_input.submit(
                    fn=chat_response,
                    inputs=[chat_input, chatbot_ui],
                    outputs=chatbot_ui,
                ).then(lambda: "", outputs=chat_input)

                chat_clear.click(fn=clear_chat, outputs=chatbot_ui)

        # ── System Info ──
        with gr.Accordion("ℹ️ Thông tin hệ thống", open=False):
            info_text = (
                f"| Thành phần | Giá trị |\n|---|---|\n"
                f"| **Chunks** | {searcher.corpus_size:,} |\n"
                f"| **Embedding dim** | {searcher.embeddings.shape[1]} |\n"
                f"| **Embedding model** | `{settings.EMBEDDING_MODEL}` |\n"
                f"| **Reranker model** | `{settings.RERANKER_MODEL}` |\n"
                f"| **LLM model** | `{settings.LLM_MODEL}` |\n"
                f"| **API Key** | {'✅ Set' if os.getenv('GENAI_API_KEY') else '❌ Not set'} |"
            )
            gr.Markdown(info_text)

        # ── Footer ──
        gr.HTML("""
        <div class="app-footer">
            <p>🎓 Đồ án tốt nghiệp — Hệ thống hỗ trợ giảng dạy Tin Học THPT bằng AI</p>
        </div>
        """)

    return demo


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # 1. Khởi tạo components
    init_components()

    # 2. Build UI
    print("\nBuilding Gradio UI...", flush=True)
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