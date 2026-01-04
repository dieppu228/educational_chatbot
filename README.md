# 📚 Educational Chatbot - Vietnamese RAG System

Một hệ thống chatbot giáo dục thông minh sử dụng **Retrieval-Augmented Generation (RAG)** để tạo và chấm điểm câu hỏi trắc nghiệm từ tài liệu giáo dục Vietnamese.

## ✨ Tính năng chính

- 🎯 **Tạo câu hỏi trắc nghiệm tự động** từ tài liệu sử dụng RAG
- ✅ **Chấm điểm câu trả lời** của học sinh với giải thích chi tiết
- 💬 **Chat interactice** với Gradio interface
- 🔍 **Hybrid search** kết hợp BM25 (keyword) + FAISS (semantic)
- 📊 **Tối ưu số lượng câu hỏi** dựa trên context khả dụng
- 🌐 **Hỗ trợ tiếng Việt** đầy đủ với embedding model chuyên dụng

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────┐
│                   User Input (Gradio)               │
└────────────────────────┬────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
    ╔═══▼═════╗                    ╔═════▼════╗
    ║  Router ║                    ║   Query  ║
    ║(Classify)║                    ║  Intent  ║
    ╚═╤═════╤═╝                    ╚═════╤════╝
      │     │                            │
      │     └─────────────────┬──────────┘
      │                       │
  ╔═══▼═══════════╗    ╔══════▼═════════╗
  ║  ChatBot Mode ║    ║ Question Mode  ║
  ║  (Fallback)   ║    ║  (Generate)    ║
  ╚═══════════════╝    ╚══════╤═════════╝
                              │
                    ┌─────────▼──────────┐
                    │  RAG Pipeline      │
                    ├────────────────────┤
                    │ 1. Retriever       │
                    │ 2. Reranker        │
                    │ 3. LLM Generator   │
                    └────────────────────┘
                              │
    ┌─────────────────────────┼──────────────────────────┐
    │                         │                          │
╔═══▼════════════╗    ╔═══════▼═══════╗       ╔═════════▼══════╗
║   Utility Node ║    ║ Answer Checker║       ║  Format Output ║
║  (Score)       ║    ║  (Feedback)   ║       ║  (Display)     ║
╚════════════════╝    ╚═══════════════╝       ╚════════════════╝
```

## 📦 Cấu trúc project

```
ĐATN/
├── LLM/                          # LLM & Response Processing
│   ├── handle_query.py           # Core query handlers
│   ├── conversation.py           # ChatBot & Session management
│   ├── response.py               # Response generation with context
│   ├── router.py                 # Query routing & classification
│   ├── format_context.py         # Context formatting
│   ├── build_context.py          # Context building utilities
│   └── test.ipynb                # Testing & demo notebook
│
├── RAG/                          # Retrieval-Augmented Generation
│   ├── embedding.py              # Embedding generation
│   ├── retriever.py              # Hybrid search (BM25 + FAISS)
│   ├── reranker.py               # Result reranking
│   └── classification_query.py   # Query classification
│
├── RawData/                      # Raw educational materials
│   ├── SGK_Tin10_CD.md           # Grade 10 IT Textbook
│   ├── SGK_Tin11_CD.md           # Grade 11 IT Textbook
│   └── SGK_Tin12_CD.md           # Grade 12 IT Textbook
│
├── data/                         # Processed data
│   ├── final_chunks_clean.json   # Cleaned chunks
│   ├── embeddings.npy            # Precomputed embeddings
│   ├── query_label.csv           # Query labels for training
│   └── du_lieu_mapped.csv        # Mapped data
│
├── Notebook/                     # Analysis & preprocessing notebooks
│   ├── preprocess_chunking.ipynb
│   ├── finetune_embedding.ipynb
│   ├── classification_model.ipynb
│   ├── rag.ipynb
│   └── scan_text.ipynb
│
├── requirements.txt              # Project dependencies
├── rag_chunks.json               # RAG document chunks
└── README.md                     # This file
```

## 🚀 Cài đặt & Setup

### 1. Prerequisites
- Python 3.9+
- pip hoặc conda

### 2. Clone & Navigate
```bash
cd "ĐATN"
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API Keys
Tạo file `.env` trong thư mục root:
```env
GENAI_API_KEY=your_gemini_api_key_here
```

### 5. Download/Prepare Data
- Embeddings: `data/embeddings.npy` (precomputed)
- RAG chunks: `rag_chunks.json`

## 💻 Sử dụng

### Option 1: Gradio Web Interface (Recommended)

```bash
# Chạy notebook cell cuối cùng trong test.ipynb
# Hoặc chạy command:
python -m jupyter notebook LLM/test.ipynb
```

Mở trình duyệt tại: `http://127.0.0.1:7860`

**Các lệnh có thể dùng:**

| Yêu cầu | Ví dụ |
|---------|-------|
| Tạo 3 câu hỏi | "Cho 3 câu hỏi về HTML" |
| Tạo với số lượng tự động | "Các câu hỏi về CSS" |
| Trả lời câu hỏi | "Đáp án câu 1 là C" |
| Hỏi về nội dung | "HTML là gì?" |
| Chào hỏi | "Xin chào" |

### Option 2: Python API

```python
from LLM.conversation import ChatBot
from RAG.retriever import Retriever
from RAG.reranker import RerankerModule
import numpy as np

# Initialize components
model = SentenceTransformer('dangvantuan/vietnamese-document-embedding')
retriever = Retriever(model)
reranker = RerankerModule()
bot = ChatBot(retriever, reranker)

# Start session & generate questions
bot._start_new_session()
response = bot.ask("Cho 3 câu hỏi về HTML", stream=True)
print("".join(response))

# Answer question
result = bot.ask("Đáp án câu 1 là B", stream=True)
print("".join(result))
```

## 🔧 Core Modules

### 1. **Retriever** (RAG/retriever.py)
- Hybrid search using BM25 (keyword) + FAISS (semantic)
- Reciprocal Rank Fusion (RRF) để combine results
- Trả về top-k most relevant documents

### 2. **Reranker** (RAG/reranker.py)
- Sử dụng FlagEmbedding để rerank kết quả
- Filtering based on relevance score & domain keywords

### 3. **Question Generator** (LLM/handle_query.py)
- `generate_question()`: Tạo MCQ từ context
- Adaptive number of questions (2-5) dựa trên context
- Temperature 0.5 để balance creativity & accuracy

### 4. **Answer Checker** (LLM/handle_query.py)
- `utility_node()`: Xác định câu hỏi & chấm điểm
- Support fuzzy matching cho cách nói khác nhau
- Trả về JSON với explanation & confidence score

### 5. **Response Generator** (LLM/handle_query.py)
- `generate_answer()`: Tạo feedback từ kết quả chấm
- Feedback tích cực & hữu ích cho học sinh

## ⚙️ Cấu hình

### Environment Variables (.env)
```
GENAI_API_KEY=<Google Generative AI API Key>
```

### Model Settings (trong code)
```python
# Embedding model
model = SentenceTransformer('dangvantuan/vietnamese-document-embedding')

# LLM model
model="gemini-2.5-flash-lite"

# Temperature (creativity level)
temperature=0.5  # Cho generate_question
temperature=0.0  # Cho utility_node (deterministic)
temperature=0.7  # Cho generate_answer (varied feedback)
```

## 📊 Performance Tips

1. **Increase Context**: Nâng `top_n` ở reranker từ 10 → 15
2. **Adjust Temperature**: 
   - Tăng lên 0.7 nếu muốn câu hỏi đa dạng hơn
   - Giảm xuống 0.3 nếu muốn focus hơn
3. **Cache Embeddings**: Embeddings đã được tính sẵn ở `data/embeddings.npy`
4. **Batch Processing**: Process multiple queries cùng lúc để optimize API calls

## 🧪 Testing

```bash
# Run test notebook
jupyter notebook LLM/test.ipynb

# Key test cases:
# 1. Generate questions với số lượng specify
# 2. Generate questions mà không specify (adaptive)
# 3. Answer questions & receive feedback
# 4. Out-of-domain questions (fallback)
```

## 🔐 API Keys & Security

- ⚠️ **KHÔNG** commit `.env` vào git
- ⚠️ **KHÔNG** share API keys công khai
- Sử dụng environment variables cho sensitive data

## 📋 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| sentence-transformers | 5.1.2+ | Vietnamese embeddings |
| transformers | 4.56.2+ | Model inference |
| torch | 2.6.0+ | Deep learning framework |
| faiss-cpu | 1.12.0+ | Vector search |
| langchain | 0.3.27+ | LLM pipeline |
| rank-bm25 | 0.2.2+ | Keyword-based search |
| gradio | 5.46.1+ | Web interface |
| google-generativeai | 2.3.0+ | Gemini API |

## 🎓 Dữ liệu đầu vào

**Textbooks sử dụng:**
- SGK Tin 10 (Information Technology Grade 10)
- SGK Tin 11 (Information Technology Grade 11)
- SGK Tin 12 (Information Technology Grade 12)

Các sách được xử lý thành chunks & embedding thành vectors để RAG có thể retrieve.

## 📈 Improvements & TODOs

- [ ] Support multiple languages beyond Vietnamese
- [ ] Fine-tune embedding model trên domain-specific data
- [ ] Add multi-turn conversation history persistence
- [ ] Implement caching để reduce API calls
- [ ] Add analytics dashboard
- [ ] Support image-based questions
- [ ] Deploy lên cloud (Hugging Face Spaces, Streamlit Cloud)

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open pull request

## 📝 License

Đây là project học tập cho **ĐATN (Đồ án tốt nghiệp)** tại Đại học Khoa học Tự nhiên Hà Nội.

## 👨‍💼 Authors

- **Student**: [Your Name]
- **Institution**: Hanoi University of Science and Technology
- **Academic Year**: 2025-2026

## 📞 Support & Contact

- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues Link]
- 💬 Discussions: [GitHub Discussions Link]

---

**Last Updated**: January 4, 2026

**Version**: 1.0.0

Made with ❤️ for Vietnamese Education
