# Intelligent Educational Assistant System (Educational Chatbot)

Graduation Thesis project to design and build an Intelligent Virtual Assistant supporting teaching and learning of Computer Science at the High School level (Grades 10-12). The system is developed based on the RAG (Retrieval-Augmented Generation) architecture combined with a Multi-Agent LLM approach to overcome information hallucination and enhance accuracy by closely following textbooks.

## 1. General Introduction

The system aims to provide a tool that automates complex academic tasks, serving both students and teachers.

**Core Functions:**

- **Knowledge Query (QA):** Answer questions based on a standardized textbook corpus (Canh Dieu and Ket Noi Tri Thuc).
- **Extraction and Question Generation (Quiz Generation):** Automatically initialize exercise systems in various formats (Multiple choice, Fill-in-the-blank, True/False, Essay) with customizable quantity and difficulty.
- **Evaluation and Scoring (Answer Scoring):** Automatically score answers and provide reasoning for corrections based on actual context instead of just keyword matching.
- **Lecture Structure Generation (Slide/Lesson Plan Generation):** Convert text content into summary structures for creating presentations or lesson plans.

---

## 2. Detailed System Pipeline

The system is designed with a Multi-Agent processing flow combined with an advanced RAG mechanism. The End-to-End Workflow goes through independent stages:

```text
┌────────────────────────────────────────────────────────┐
│                   User Message / Query                 │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│               1. Intent Detector Agent                 │
│  (Extracts: Intent, Task Type, Topic, Specific Info)   │
└───────────────────────────┬────────────────────────────┘
                            ▼
                    [ Dispatcher ] ────────────┐
                            │                  │
                      (Match Task)             │
                            ▼                  ▼
┌──────────────────────────────────┐   ┌───────────────┐
│        Specialist Handlers       │   │ General Chat  │
│  (Question / Explain / Slide...) │   │   Handler     │
└─────────────────┬────────────────┘   └───────────────┘
                  │
                  ▼
┌────────────────────────────────────────────────────────┐
│            2. Advanced RAG Pipeline Core               │
│                                                        │
│  a. Query Rewriting (Expands query context)            │
│          │                                             │
│  b. Hybrid Search ──▶ Lexical (Custom BM25)            │
│                   ──▶ Semantic (Vector Embedding)      │
│          │                                             │
│  c. RRF (Reciprocal Rank Fusion - Score merging)       │
│          │                                             │
│  d. Reranking (Cross-Encoder threshold filtering)      │
└─────────────────────────┬──────────────────────────────┘
                          │      ┌───────────────────────┐
                          ├──────┤  Document Datastore   │
                          │      │  (Text Chunks / JSON) │
                          ▼      └───────────────────────┘
┌────────────────────────────────────────────────────────┐
│          3. Generation & Validator (Reflection)        │
│                                                        │
│   ┌───────────────────┐        ┌───────────────────┐   │
│   │   Generator LLM   │───────▶│  Validator Agent  │   │
│   │ (Drafts Content)  │◀───────│ (Check & Reflect) │   │
│   └───────────────────┘        └───────────────────┘   │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                 Final Response / UI Output             │
└────────────────────────────────────────────────────────┘
```

### 2.1. Intent Detection

When the system receives a natural language query from the user, the `IntentDetector Agent` performs semantic analysis to extract 3 entities (Entities):

- `intent`: The actual purpose of the command (Chat, Generate Question, Explain, etc.).
- `task_type`: Desired output format (e.g., `mcq`, `essay`).
- `topic`: The knowledge topic the user is targeting.

The extraction command is then routed by the Dispatcher to the corresponding Specialist Handler.

### 2.2. Advanced RAG Pipeline

To ensure the LLM receives the most accurate context (Context), the system implements a Retrieval pipeline with 4 steps optimized for latency and precision:

1. **Query Rewriting:** The LLM Agent breaks down and rewrites the original question into variants (queries) to cover the semantic space, increasing the Recall metric.
2. **Hybrid Search:** Performs parallel searching in Vector space:
   - **Lexical Search:** Uses an independent `Custom BM25` module (enhanced TF-IDF) to accurately trace industry-specific keywords.
   - **Semantic Search:** Uses Cosine Similarity on an Embedding model to find semantic similarities.
3. **Reciprocal Rank Fusion (RRF):** An algorithm to normalize and merge ranking results from the two search engines in step 2.
4. **Cross-Encoder Reranking:** Uses the `Vietnamese_Reranker` model to calculate linear vector distances between the Query and Top N Documents. Filters out noisy chunks caused by duplication or those with relevance scores (`rerank_score`) below a certain threshold.

### 2.3. Generation & Self-Reflection

Filtered documents are packaged with the Query and fed into the LLM to generate results (JSON Formatting).
In this phase, the system applies a Self-Reflection mechanism through a `Validator Agent`. The generated results are reversely extracted by this Agent to cross-check with the original Context to ensure structural requirements and logical conditions are met. If validation fails, the Generation process is called recursively to re-execute until it meets the standards.

### 2.4. RAGAS Evaluation Pipeline

To quantitatively evaluate the RAG system's performance, the project integrates an independent automated evaluation pipeline:

- **Testset Generator:** Automatically synthesizes 50-100 random samples (Query, Ground Truth Answer) from the textbook JSON chunks.
- **RAGAS Evaluator:** Uses a standard framework to measure 4 coefficients: _Answer Relevancy_, _Faithfulness_, _Context Precision_, and _Context Recall_.

---

## 3. Tech Stack

The system is developed in separate modules to ensure high scalability.

**1. Core LLM & Orchestration:**

- **Language Model:** Google Gemini (`gemini-2.5-pro` & `gemini-2.5-flash`) via `google-genai` SDK.
- **Agent Management:** Object-Oriented Python (OOP) builds an internal State Machine architecture instead of heavy frameworks.

**2. Retrieval & Vector Core:**

- **Embedding Model:** `dangvantuan/vietnamese-document-embedding` (Based on `HuggingFaceEmbeddings` / `SentenceTransformer` architecture, 768 dimensions).
- **Reranker Model:** `AITeamVN/Vietnamese_Reranker` (Cross-Encoder architecture running on torch/CUDA).
- **Search Engine:** Vector space is mathematicalized using pure `Numpy` + a self-programmed `BM25 TF-IDF Analyzer` algorithm to avoid resource waste and native library dependencies (like FAISS).

**3. Infrastructure & UI:**

- **User Interface:** `Gradio` Web Framework.
- **Evaluation System:** `ragas==0.4.3` running via CLI Argument Parser (`run_eval.py`).
- **Data Engineering:** Regular Expression (Regex) combined with Hierarchical Document Splitting handles unstructured text (Markdown).

---

## 4. Local Setup Guide

The local deployment process requires a Python environment >= 3.12:

```bash
# 1. Clone Source Code
git clone https://github.com/KhacDiep08/Educational-Chatbot.git
cd Educational-Chatbot

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Assign API Keys
echo GENAI_API_KEY=your_key_here > .env

# 4. Launch UI Server Application
python app_gradio.py
```

Run the RAGAS Metric Report evaluation script (Optional):

```bash
python -m src.evaluation.run_eval --step all
```

---

_Student Information: Khac Diep (Hanoi University of Science and Technology)._
