"""
Gradio Chatbot Application - Full Pipeline
Demonstrates: Data Loading → Retrieval → Reranking → Question Generation
"""

import sys
import io
import gradio as gr
from pathlib import Path

# UTF-8 encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Setup imports
from config import settings
from RAG.retriever import Retriever
from RAG.reranker import RerankerModule
from LLM.conversation import ChatBot
from sentence_transformers import SentenceTransformer
import json
import numpy as np

# ============================================================
# INITIALIZATION - Load all components
# ============================================================
print("Initializing Chatbot Application...")

try:
    # Load chunks data
    print("Loading chunks...")
    with open("data/rag_chunks.json", "r", encoding="utf-8") as f:
        chunks_data = json.load(f)
    print(f"✓ Loaded {len(chunks_data)} chunks")

    # Initialize embedding model
    print("Loading embedding model...")
    embedding_model = SentenceTransformer(
        "dangvantuan/vietnamese-document-embedding",
        device="cpu",
        trust_remote_code=True
    )
    print("✓ Embedding model loaded")

    # Initialize retriever
    print("Initializing retriever...")
    retriever = Retriever(embedding_model)
    retriever.set_data(chunks_data)

    # Build BM25 index
    corpus_texts = [chunk["content"] for chunk in chunks_data]
    retriever.build_bm25(corpus_texts)
    print("✓ BM25 index built")

    # Load embeddings and build FAISS
    embeddings = np.load("data/embeddings.npy")
    retriever.build_faiss_index(embeddings, metric="IP")
    print("✓ FAISS index built")

    # Initialize reranker
    print("Initializing reranker...")
    reranker = RerankerModule()
    print("✓ Reranker initialized")

    # Initialize chatbot
    print("Initializing chatbot...")
    chatbot = ChatBot(retriever, reranker)
    print("✓ Chatbot initialized")

    print("=" * 60)
    print("✅ All components initialized successfully!")
    print("=" * 60)

except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    raise


# ============================================================
# GRADIO INTERFACE
# ============================================================

def chat_response(message, history):
    """
    Process user message and generate response with Gradio streaming.
    """
    if not message.strip():
        yield history
        return

    try:
        # Get response from chatbot (generator)
        full_response = ""
        for chunk in chatbot.ask(message, stream=True):
            full_response += chunk
            yield history + [[message, full_response]]
        
    except Exception as e:
        error_msg = f"❌ Lỗi: {str(e)[:100]}"
        yield history + [[message, error_msg]]


def clear_chat():
    """Clear chat history"""
    chatbot.sessions = []
    chatbot.current_session = None
    return []


# Create Gradio interface
with gr.Blocks(title="🤖 Tin Học Q&A Chatbot", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🤖 Tin Học Q&A Chatbot
    
    **Hệ thống hỏi đáp trắc nghiệm các môn Tin Học (Khối 10, 11, 12)**
    
    - 📚 Dữ liệu: 702 chunks từ SGK Tin Học Cánh Diều
    - 🔍 Tìm kiếm: Hybrid Search (BM25 + FAISS)
    - ⭐ Xếp hạng: FlagReranker
    - 🤖 Tạo câu hỏi: Gemini 2.5 Flash Lite
    """)

    with gr.Row():
        with gr.Column(scale=4):
            chatbot_ui = gr.Chatbot(
                height=600,
                show_copy_button=True,
                show_label=False,
                label="Chat History"
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Hướng dẫn")
            gr.Markdown("""
            **Các lệnh:**
            
            1️⃣ **Tạo câu hỏi**
               - "Cho 3 câu hỏi về mã hóa"
               - "Hỏi về bảo mật khối 10"
               
            2️⃣ **Trả lời**
               - "A là đúng"
               - "Đáp án là C"
               
            3️⃣ **Giải thích**
               - "Giải thích câu 1"
               - "Tại sao là D?"
            """)

    with gr.Row():
        msg_input = gr.Textbox(
            placeholder="Nhập câu hỏi... (VD: Cho 3 câu hỏi về lập trình Python)",
            show_label=False,
            lines=2,
            scale=4
        )
        send_btn = gr.Button("📤 Gửi", variant="primary", scale=1)

    with gr.Row():
        clear_btn = gr.Button("🗑️ Xóa lịch sử", variant="secondary")
        info_btn = gr.Button("ℹ️ Thông tin", variant="secondary")

    # Event handlers
    send_btn.click(
        fn=chat_response,
        inputs=[msg_input, chatbot_ui],
        outputs=chatbot_ui
    ).then(
        lambda: "",
        outputs=msg_input
    )

    msg_input.submit(
        fn=chat_response,
        inputs=[msg_input, chatbot_ui],
        outputs=chatbot_ui
    ).then(
        lambda: "",
        outputs=msg_input
    )

    clear_btn.click(
        fn=clear_chat,
        outputs=chatbot_ui
    )

    # Info button
    def show_info():
        return f"""
        **📊 Thông tin hệ thống:**
        
        - Chunks: {len(chunks_data)}
        - Embedding dim: {embeddings.shape[1]}
        - API Key: {'✅ Set' if settings.GENAI_API_KEY else '❌ Not set'}
        - Embedding Model: dangvantuan/vietnamese-document-embedding
        - LLM Model: {settings.LLM_MODEL}
        """

    info_btn.click(
        fn=show_info,
        outputs=gr.Textbox(label="System Info", interactive=False)
    )

    gr.Markdown("""
    ---
    **Lưu ý:**
    - Hệ thống sử dụng AI để tạo câu hỏi, kết quả có thể không hoàn toàn chính xác
    - Vui lòng kiểm tra lại trước khi sử dụng
    - Mỗi câu hỏi mới sẽ tạo một session riêng
    """)


if __name__ == "__main__":
    print("Starting Gradio server...")
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        show_api=False
    )
