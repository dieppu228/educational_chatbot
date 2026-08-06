# Tài liệu kỹ thuật dự án Educational Chatbot

Tài liệu này mô tả hiện trạng triển khai của dự án ở mức đủ chi tiết để dùng làm nguồn tham chiếu khi viết báo cáo/LaTeX. Nội dung ưu tiên khớp với source code hiện tại, đặc biệt là các phần Orchestrator, RAG, quiz, slide/lesson plan, multi-agent content pipeline, session, trace và evaluation.

Khi chuyển nội dung kỹ thuật trong tài liệu này sang LaTeX, cần đối chiếu thêm quy tắc hành văn và bố cục trong `docs/latex_writing_guidelines_vi.md`.

## 1. Mục tiêu hệ thống

Dự án xây dựng một trợ lý giáo dục thông minh cho môn Tin học THPT lớp 10-12. Hệ thống hỗ trợ học sinh và giáo viên tương tác bằng ngôn ngữ tự nhiên, đồng thời bám sát nội dung sách giáo khoa để giảm hiện tượng sinh thông tin sai lệch.

Các năng lực chính:

- Hỏi đáp và giải thích kiến thức Tin học dựa trên SGK.
- Sinh câu hỏi luyện tập độc lập theo nhiều dạng: trắc nghiệm, tự luận, điền khuyết, đúng/sai.
- Chấm câu trả lời, giải thích câu hỏi, ôn tập câu sai và thống kê tiến độ.
- Sinh slide bài giảng và giáo án bằng một pipeline content multi-agent chung.
- Gợi ý media minh họa cho slide/giáo án ở mức metadata; MCP-backed media search hiện là extension point.
- Lưu session, trace, debug metadata để hỗ trợ nối tiếp hội thoại và kiểm thử.

## 2. Phạm vi dữ liệu và mô hình

### 2.1. Nguồn dữ liệu

Dữ liệu đầu vào chính là nội dung SGK Tin học THPT thuộc các bộ sách Cánh Diều và Kết Nối Tri Thức. Repo hiện có các nguồn thô trong `RawData/`, dữ liệu map trong `data/`, và dữ liệu chunk phục vụ RAG trong `data/rag_chunks_v2.json`.

Các file dữ liệu đáng chú ý:

- `RawData/SGK_Tin10_CD_clean.md`, `RawData/SGK_Tin11_CD_clean.md`, `RawData/SGK_Tin12_CD_clean.md`: dữ liệu đã làm sạch của bộ Cánh Diều.
- `RawData/SGK_Tin10_KNTT_clean.md`, `RawData/SGK_Tin11_KNTT_clean.md`, `RawData/SGK_Tin12_KNTT_clean.md`: dữ liệu đã làm sạch của bộ Kết Nối Tri Thức.
- `data/rag_chunks_v2.json`: chunk chính dùng cho retrieval.
- `data/table_of_contents.md`: mục lục/chương trình học.
- `CD/*.pdf`: PDF sách tham khảo.

### 2.2. Mô hình và cấu hình

Cấu hình tập trung trong `src/config/config.py`.

Các cấu hình chính:

- LLM chính: `gemini-2.5-flash-lite`.
- Provider gọi LLM: Google Generative AI thông qua `langchain_google_genai` và `google-genai`/Gemini API key.
- Embedding model: `dangvantuan/vietnamese-document-embedding`.
- Reranker model: `AITeamVN/Vietnamese_Reranker`.
- Retriever top-k mặc định: `RETRIEVER_TOP_K = 25`.
- Reranker top-n mặc định: `RERANKER_TOP_N = 5`.
- Reranker top-n cho slide: `RERANKER_TOP_N_SLIDE = 15`.
- Reranker top-n cho lesson plan: `RERANKER_TOP_N_LESSON_PLAN = 10`.
- Evaluation LLM: `gemini-2.5-flash-lite`.

Ý nghĩa khi viết luận văn: hệ thống không chỉ là một chatbot gọi LLM trực tiếp. LLM được đặt sau các lớp điều phối, truy xuất tri thức, kiểm định chất lượng và quản lý trạng thái.

## 3. Kiến trúc tổng quan

Hệ thống hiện có kiến trúc dạng pipeline điều phối mỏng. `Orchestrator` không chứa logic nghiệp vụ chi tiết mà chủ yếu tạo `RequestContext`, phân tích intent, lập action plan, sau đó giao cho `ExecutionDispatcher` gọi đúng domain service hoặc handler.

Luồng tổng quát:

```text
User / Frontend
  -> FastAPI /api/chat
  -> Orchestrator.ask_async()
  -> RequestContext
  -> ContextAnalyzer
  -> QueryRewriter nếu cần
  -> IntentRouter.detect_multi()
  -> SessionManager
  -> ActionPlanner.plan_all()
  -> ExecutionDispatcher
  -> Domain Services / Handlers
  -> RAGService / AdaptiveRAGAgent
  -> LLM generation / validation / quality review
  -> Streamed response
  -> SessionStore + TraceService
```

Các lớp chính:

- Presentation/API layer: `app/api.py`, `app/frontend/`.
- Pipeline orchestration layer: `src/llm/orchestrator.py`.
- Context/session/action layer: `RequestContext`, `SessionManager`, `ActionPlanner`, `ExecutionDispatcher`.
- Domain service layer: `QuizService`, `SlideService`, explain/chat/fallback handlers.
- Retrieval layer: `RAGService`, `AdaptiveRAGAgent`, retriever, reranker, `ContextBuilder`, `ContextCombiner`.
- Content multi-agent layer: `ContentSupervisor`, specialist agents, A2A-lite protocol.
- Tool/MCP layer: `src/tools/`.
- Persistence/observability layer: `SessionStore`, `TraceService`, `debug_steps`.

## 4. RequestContext và state xuyên suốt pipeline

`RequestContext` trong `src/schemas/context.py` là state object chính đi xuyên qua toàn bộ request. Đây là điểm thay thế cho cách truyền nhiều biến rời rạc hoặc global state.

Các nhóm trường chính:

- Input: `query`, `ui_book`, `ui_grade`, `user_id`.
- Enrichment: `enriched_query`, `queries_for_rag`, `context_enriched`, `rewrite_info`.
- Intent: `intent_result`, `intent_results`.
- Session: `session`.
- Action: `action_plan`, `action_plans`.
- Scope resolution: `effective_book`, `effective_grade`, `scope_source`, `scope_is_soft`, `requested_scope`, `actual_scope`, `scope_fallback_notice`.
- Debug/trace: `request_id`, `timestamp`, `debug_steps`, `t0`, `auto_approve_outline`, `graph_debug_stream`.

State mẫu đầy đủ có thể mô tả trong luận văn:

```json
{
  "request_id": "a1b2c3d4",
  "user_id": "student_01",
  "query": "Tạo 5 câu trắc nghiệm về cơ sở dữ liệu lớp 12 Cánh Diều",
  "ui_book": "CD",
  "ui_grade": "12",
  "enriched_query": "Tạo 5 câu trắc nghiệm về cơ sở dữ liệu lớp 12 Cánh Diều",
  "queries_for_rag": [
    "cơ sở dữ liệu lớp 12 Cánh Diều",
    "khái niệm cơ sở dữ liệu hệ quản trị cơ sở dữ liệu"
  ],
  "context_enriched": false,
  "intent_results": [
    {
      "primary_intent": "generate",
      "task_type": "mcq",
      "topic": "Cơ sở dữ liệu",
      "grade": "12",
      "book": "CD",
      "is_new_topic": true,
      "confidence": 0.92
    }
  ],
  "session": {
    "session_id": "student_01:co-so-du-lieu",
    "topic": "Cơ sở dữ liệu",
    "book": "CD",
    "metadata": {
      "grade": "12"
    }
  },
  "action_plans": [
    {
      "action": "generate_quiz",
      "reason": "task_type=mcq"
    }
  ],
  "effective_book": "CD",
  "effective_grade": "12",
  "scope_source": "mixed",
  "scope_is_soft": false,
  "requested_scope": {
    "book": "CD",
    "grade": "12",
    "source": "mixed"
  },
  "actual_scope": {
    "book": "CD",
    "grade": "12",
    "source": "requested"
  },
  "debug_steps": [
    {
      "node": "IntentRouter",
      "intents": 1,
      "primary_intent": "generate",
      "task_type": "mcq"
    },
    {
      "node": "RAG",
      "strategy": "hierarchical",
      "chunks_returned": 5,
      "filter": {
        "grade": "12",
        "topic": "Cơ sở dữ liệu",
        "book": "CD"
      }
    }
  ]
}
```

Lưu ý: JSON trên là mock minh họa. Trong runtime thật, `session`, `intent_result` và `action_plan` là object/dataclass nội bộ, còn debug output được serialize qua `RequestContext.to_debug_dict()`.

## 5. Pipeline điều phối request

### 5.1. Entry point API

`app/api.py` cung cấp endpoint chính:

```text
POST /api/chat
```

Request gồm:

- `message`: câu hỏi/yêu cầu của người dùng.
- `book`: tùy chọn, chỉ nhận `CD` hoặc `KNTT`.
- `grade`: tùy chọn, chỉ nhận `10`, `11`, `12`.
- `user_id`: định danh người dùng, mặc định `anonymous`.

API khởi tạo `CustomSearch`, `Reranker`, `Orchestrator`, sau đó gọi `orchestrator.ask_async(...)`. Response trả về:

- `content`: toàn bộ câu trả lời đã ghép từ stream chunks.
- `debug`: debug info mới nhất của user.

### 5.2. Orchestrator

`src/llm/orchestrator.py` là controller trung tâm. Trách nhiệm chính:

1. Tạo `RequestContext`.
2. Kiểm tra có HITL resume đang chờ hay không.
3. Enrich context và rewrite query khi cần.
4. Gọi `IntentRouter.detect_multi()` để phát hiện tối đa 3 intent.
5. Resolve session bằng `SessionManager`.
6. Lập danh sách action bằng `ActionPlanner.plan_all()`.
7. Resolve phạm vi sách/lớp.
8. Chạy vòng lặp multi-action qua `ExecutionDispatcher`.
9. Lưu session bằng `SessionStore`.
10. Ghi trace/debug bằng `TraceService`.

Thiết kế này giúp Orchestrator giữ vai trò mỏng, còn nghiệp vụ chi tiết nằm ở domain services.

### 5.3. ContextAnalyzer và QueryRewriter

`ContextAnalyzer` xác định query hiện tại có phụ thuộc lịch sử hội thoại hay không. Nếu có, hệ thống lấy context từ session trước đó. `QueryRewriter` dùng LLM để sinh 2-3 query phụ giàu ngữ nghĩa hơn, phục vụ retrieval sâu hơn.

Điểm quan trọng:

- Query rewrite không nhằm trả lời user trực tiếp.
- Query rewrite chỉ tối ưu truy xuất RAG.
- Nếu không cần context, `queries_for_rag` mặc định chỉ chứa query gốc.

### 5.4. IntentRouter.detect_multi

`IntentRouter` dùng LLM để phân tích ý định người dùng. Kết quả là danh sách `IntentResult`, tối đa 3 intent. Mỗi intent thường gồm:

- `primary_intent`: `generate`, `interact`, `analyze`, `explain`, hoặc chat.
- `task_type`: ví dụ `mcq`, `essay`, `fill_blank`, `true_false`, `slide`, `lesson_plan`.
- `topic`: chủ đề học tập.
- `grade`: lớp nếu phát hiện được.
- `book`: bộ sách nếu phát hiện được.
- `is_new_topic`: có phải chủ đề mới không.

Ý nghĩa kiến trúc: một câu hỏi của user có thể tạo nhiều hành động. Ví dụ: "Tạo slide rồi cho thêm vài câu hỏi luyện tập" có thể sinh nhiều action plan.

### 5.5. SessionManager

`SessionManager` quyết định request hiện tại nối tiếp session cũ hay tạo session mới. Session lưu:

- Lịch sử hội thoại.
- Chủ đề và bộ sách hiện hành.
- Quiz state.
- Slide state.
- Metadata như lớp học.

Session được lưu lâu dài bởi `SessionStore` dưới dạng JSON trong `data/sessions`.

### 5.6. ActionPlanner

`src/llm/action_planner.py` map intent sang action bằng rule-based logic. Không gọi LLM ở bước này.

Các action hiện có:

- `GENERATE_QUIZ`
- `GENERATE_SLIDE`
- `GENERATE_LESSON_PLAN`
- `CHECK_ANSWER`
- `REVIEW_WRONG`
- `EXPLAIN_QUESTION`
- `ANSWER_EXERCISE`
- `GET_STATS`
- `EXPLAIN_CONCEPT`
- `CHAT`

`plan_all()` nhận danh sách intent và trả danh sách `ActionPlan`, đồng thời deduplicate action liền kề giống nhau.

### 5.7. ExecutionDispatcher

`src/llm/execution_dispatcher.py` là registry dispatch action sang module xử lý tương ứng.

Mapping chính:

- `GENERATE_QUIZ` -> `QuizService.generate_quiz`.
- `CHECK_ANSWER` -> `QuizService.check_answer`.
- `REVIEW_WRONG` -> `QuizService.review_wrong`.
- `GET_STATS` -> `QuizService.get_stats`.
- `GENERATE_SLIDE` -> `SlideService.generate_slide`.
- `GENERATE_LESSON_PLAN` -> `SlideService.generate_lesson_plan`.
- `ANSWER_EXERCISE` -> `SlideService.answer_exercise`.
- `EXPLAIN_CONCEPT` -> `ExplainHandler` với RAG context.
- `CHAT` -> `ChatHandler`.

Dispatcher có cả sync và async path để tương thích các entrypoint cũ và API hiện tại.

## 6. RAG và Knowledge Layer

### 6.1. RAGService

`src/rag/rag_service.py` là interface retrieval chính cho domain services. Nó nhận `RequestContext`, lấy topic/grade/book đã resolve, sau đó gọi `AdaptiveRAGAgent`.

RAGService xử lý:

- Single-query retrieval.
- Multi-query retrieval khi `queries_for_rag` có nhiều query.
- Rerank và filter context theo `RERANKER_MIN_SCORE`.
- Fallback scope khi user chọn scope mềm từ UI nhưng không đủ chunk.
- Ghi debug step vào `RequestContext.debug_steps`.

### 6.2. AdaptiveRAGAgent

`src/rag/adaptive_rag.py` chọn strategy truy xuất dựa trên `QueryClassifier`. Classifier là heuristic code, không dùng LLM.

Bốn strategy chính:

| Strategy | Khi dùng | Cách hoạt động |
| --- | --- | --- |
| `STANDARD` | Query cụ thể, thiếu grade/topic context | Hybrid search toàn cục rồi rerank |
| `BROAD` | Query tổng quan, hỏi khái quát | Lấy metadata/objective chunk, mỗi bài một chunk, fallback sang standard nếu quá ít |
| `CURRICULUM` | Hỏi cấu trúc chương trình/danh sách bài/chủ đề | Tổng hợp metadata bài học, không ưu tiên vector search |
| `HIERARCHICAL` | Query cụ thể có grade/topic | Truy xuất theo cấp: chọn bài liên quan rồi tìm chunk con chi tiết |

### 6.3. Hybrid Search và reranking

Repo dùng `CustomSearch` trong `src/rag/retrieve_rebuild.py` làm retriever. Theo README và code, search kết hợp:

- Lexical/BM25-like search.
- Semantic vector search bằng embedding tiếng Việt.
- RRF normalization để hợp nhất điểm.
- Cross-encoder reranking bằng `AITeamVN/Vietnamese_Reranker`.

Sau rerank, số chunk cuối phụ thuộc task:

- Task thường: top-n mặc định.
- Slide: nhiều chunk hơn để phủ bài học.
- Lesson plan: nhiều chunk hơn task hỏi đáp nhưng ít hơn slide nếu cấu hình như hiện tại.

### 6.4. ContextBuilder và ContextCombiner

`ContextBuilder` và `ContextCombiner` chuẩn hóa context trước khi đưa vào LLM.

`ContextCombiner` có hai mode:

- Flat mode: sort chunk theo score, phù hợp quiz/explain/chat.
- Grouped mode: group theo chủ đề và bài học, phù hợp slide/lesson plan/essay.

Điểm này quan trọng khi viết luận văn: cùng một retriever nhưng context format được điều chỉnh theo nhiệm vụ, giúp long-form generation giữ cấu trúc SGK tốt hơn.

### 6.5. Scope resolution và fallback

`RequestContext.resolve_book()` và `resolve_grade()` xác định phạm vi cuối cùng từ:

1. Query trực tiếp của user.
2. Kết quả IntentRouter.
3. UI dropdown.
4. Session cũ.

Nếu scope chỉ đến từ UI và không tìm đủ chunk, RAGService có thể mở rộng tìm kiếm ra toàn bộ SGK. Khi fallback xảy ra, hệ thống ghi:

- `scope_fallback_used = true`
- `actual_scope`
- `scope_fallback_notice`
- Debug step `ScopeFallback`

## 7. Quiz standalone pipeline

Quiz standalone nằm trong `src/llm/services/quiz_service.py`. Đây là pipeline riêng, không đưa vào content multi-agent pipeline để giữ ổn định các chức năng tương tác như chấm điểm, review câu sai và thống kê.

### 7.1. Generate quiz

Luồng sinh quiz:

```text
QuizService.generate_quiz
  -> RAGService.get_context(intent_hint="generate")
  -> ContextBuilder.build(action="generate_quiz")
  -> Question handler theo task_type
  -> QualityReviewer
  -> optional revise
  -> QuestionValidator
  -> persist QuizRound / QuestionRecord
  -> display format
```

Các handler câu hỏi:

- `MCQHandler`
- `EssayHandler`
- `FillHandler`
- `TrueFalseHandler`

Quality path của quiz:

- `QualityReviewer` kiểm tra chất lượng output ở cấp bộ câu hỏi.
- Nếu reviewer yêu cầu `revise_quiz`, handler được gọi lại một lần với revision instruction.
- `QuestionValidator` kiểm tra câu hỏi với context trước khi lưu vào session.

### 7.2. Quiz state

State chính nằm trong `src/llm/memory.py`.

Các model quan trọng:

- `QuizSessionState`: chứa nhiều `QuizRound`.
- `QuizRound`: một lượt sinh câu hỏi.
- `QuestionRecord`: một câu hỏi cụ thể, kèm trạng thái trả lời.

Một `QuestionRecord` lưu:

- `question_id`
- `question_type`
- `content`
- `user_answer`
- `is_correct`
- `score`
- `answered_at`
- `attempt_count`
- `source`

### 7.3. Check answer

Khi user trả lời, `QuizService.check_answer()`:

1. Lấy tất cả câu hỏi trong session.
2. Chuyển thành `TaskItem`.
3. Gọi `QuestionScorer`.
4. Cập nhật `QuestionRecord`.
5. Ghi attempt vào `StudentTracker`.
6. Trả feedback cho user.

### 7.4. Review wrong và stats

`review_wrong()` tạo hoặc hiển thị các câu sai để ôn tập. `get_stats()` trả thống kê tổng số câu, số câu đã trả lời, số câu đúng và accuracy. Đây là lý do quiz standalone không nên bị trộn vào ContentAssessmentAgent của slide/lesson plan.

## 8. Slide và Lesson Plan pipeline

Slide và giáo án dùng chung `SlideService` trong `src/llm/services/slide_service.py`.

Hai entrypoint:

- `generate_slide(ctx)`
- `generate_lesson_plan(ctx)`

Cả hai gọi `_run_content_pipeline(ctx, task_type=...)`, chỉ khác `task_type` là `slide` hoặc `lesson_plan`.

Luồng tổng quát:

```text
SlideService._run_content_pipeline
  -> RAGService.get_context(task_type="slide" hoặc "lesson_plan")
  -> ContentPipelineInput.from_context()
  -> build graph state
  -> ContentSupervisor LangGraph
  -> HITL outline review
  -> specialist agents
  -> merge results
  -> quality review
  -> persist slide_state
  -> streamed formatted output
```

### 8.1. HITL outline review

Sau khi `generate_outline` tạo dàn ý, graph interrupt để user duyệt hoặc chỉnh sửa. `SlideService` lưu các trường resume vào `slide_state.slide_output`:

- `_graph_thread_id`
- `_graph_config`
- `_interrupt`
- `_task_type`

Nếu user gửi `ok`, `duyệt`, `đồng ý`, `approve`, pipeline resume với `True`. Nếu user gửi nội dung khác, nội dung đó được coi là feedback chỉnh sửa.

### 8.2. Xử lý kết quả hoàn thành

Khi graph hoàn tất, `_process_completed_result()`:

- Kiểm tra quality blocked.
- Lấy `merged_slides`.
- Lấy `outline_payload`.
- Lấy `quality_review`.
- Tóm tắt `agent_results`.
- Lưu vào `slide_state.slide_output`.
- Ghi debug step.
- Trả output cho user.

Slide state cũng có `exercise_questions` để hỗ trợ trả lời bài tập nhúng trong slide.

## 9. Content Multi-Agent System

### 9.1. Ranh giới áp dụng multi-agent

Hiện tại multi-agent rõ nhất nằm ở pipeline sinh slide và lesson plan. Toàn bộ hệ thống không phải là LangGraph multi-agent end-to-end. Orchestrator cấp cao vẫn là controller code; LangGraph chỉ điều phối content pipeline.

Thiết kế này hợp lý vì:

- Slide và lesson plan là tác vụ dài, cần chia nhỏ thành outline, content, media, assessment và review.
- Quiz standalone có nhiều state tương tác riêng, nên giữ ở service để maintain tracker/scoring/review.
- Các agent content có artifact rõ ràng để merge và review.

### 9.2. ContentSupervisor

`src/llm/graphs/content_supervisor.py` xây LangGraph supervisor. Supervisor dùng LLM để quyết định gọi agent adapters theo thứ tự, nhưng không tự viết nội dung trực tiếp.

Các node chính:

- `preprocess_node`: tạo `context_map`, `chunk_map`, `synthesized_context`, system message.
- `supervisor_node`: gọi LLM supervisor có bind tools.
- `tools`: `ToolNode` thực thi adapter tools.
- `post_tool_processor`: parse kết quả tool và cập nhật state.
- `reflection_decision_node`: xử lý quality review và route revision/block/approve.

### 9.3. A2A-lite protocol

`src/schemas/agent_protocol.py` định nghĩa contract giao tiếp nội bộ giữa supervisor và specialist agent.

Luồng contract chuẩn:

```text
ContentSupervisor
  -> build AgentTask
  -> SpecialistAgent.run_task(task)
  -> BaseAgent._run(task)
  -> AgentTaskResult
  -> post_tool_processor/direct node
  -> ContentSupervisorState.agent_tasks / agent_results / artifacts
```

Contract này được gọi là **A2A-lite** vì nó dùng message envelope rõ ràng nhưng vẫn chạy in-process, chưa phải distributed agent runtime.

#### 9.3.1. `AgentTask` — input contract từ supervisor sang specialist

`AgentTask` là yêu cầu công việc mà supervisor giao cho một agent cụ thể. Các field:

| Field | Vai trò |
| --- | --- |
| `task_id` | ID ổn định cho một tác vụ, thường là `{request_id}:{suffix}` như `abc:outline`, `abc:content`, `abc:quiz`. Dùng để dedup log và trace. |
| `from_agent` | Nguồn giao việc, hiện là `content_supervisor`. |
| `to_agent` | Agent nhận việc, ví dụ `pedagogy_planner_agent`, `content_drafting_agent`. |
| `task_type` | Loại nghiệp vụ agent phải làm, ví dụ `plan_content_outline`, `draft_learning_content`, `research_media`. |
| `objective` | Mô tả mục tiêu bằng ngôn ngữ tự nhiên để log/debug và có thể mở rộng cho planner. |
| `inputs` | Payload nghiệp vụ chính: `context_map`, `outline_payload`, `chunk_map`, `topic`, `grade`, `book`, `task_type`, output đã merge... |
| `constraints` | Ràng buộc thực thi: số câu hỏi, ngôn ngữ, media type, yêu cầu bám nguồn, rule chặn unsafe/ungrounded output. |
| `context_refs` | Danh sách ID nguồn context agent được phép/được kỳ vọng dùng, ví dụ các key trong `chunk_map`. |
| `expected_artifact` | Tên artifact mà agent phải trả, ví dụ `outline_payload`, `content_payload`, `media_payload`, `quiz_payload`, `quality_review`. |
| `revision_instruction` | Chỉ dẫn sửa đổi khi quality reflection yêu cầu regenerate outline/content/quiz. |

Ý nghĩa: supervisor không truyền tham số rời rạc trực tiếp vào worker cũ, mà đóng gói thành task envelope. Nhờ vậy mỗi agent có thể được trace, retry, audit hoặc sau này chuyển sang external tool mà ít đổi contract.

#### 9.3.2. `AgentTaskResult` — output contract từ specialist về supervisor

`AgentTaskResult` là kết quả chuẩn hóa mà mọi specialist agent trả về. Các field:

| Field | Vai trò |
| --- | --- |
| `task_id` | Khớp với task đầu vào để nối request/result. |
| `agent_id` | Agent thực thi thật sự. |
| `status` | Một trong `success`, `partial`, `failed`, `blocked`. |
| `task` | Bản sao `AgentTask` dạng dict; `BaseAgent.run_task()` tự gắn nếu agent chưa set. |
| `artifact_type` | Loại artifact được sinh ra; thường trùng `expected_artifact`. |
| `artifact` | Payload nghiệp vụ chính: outline/content/media/quiz/review. |
| `confidence` | Điểm tin cậy tương đối do adapter gán, dùng để debug/metadata, không phải metric học máy chính thức. |
| `warnings` | Cảnh báo mềm, ví dụ outline bị user chỉnh qua HITL. |
| `used_tools` | Danh sách năng lực đã dùng như `llm_generation`, `chunk_lookup`, `web_search`, `llm_review`. |
| `latency_ms` | Thời gian chạy agent. Nếu agent không tự set, `BaseAgent` đo tự động. |
| `error_code` | Mã lỗi chuẩn hóa như `INVALID_AGENT_INPUT`, `FORMAT_INVALID`, `QUALITY_AGENT_ERROR`. |
| `error_message` | Thông điệp lỗi rút gọn, không lưu full prompt/context. |

`is_agent_task_result()` nhận diện output mới bằng các key bắt buộc `task_id`, `agent_id`, `status`, `artifact`. Điều này giúp `post_tool_processor()` phân biệt format mới với payload legacy.

#### 9.3.3. Error contract

`BaseAgent.run_task()` là lớp bảo vệ chung:

- Gọi `_run(task)` của specialist.
- Tự đo `latency_ms` nếu result chưa có.
- Tự gắn `task=task.to_dict()` nếu result chưa chứa task.
- Bắt exception và trả `AgentTaskResult(status="failed")`, không để exception phá graph.

Điều này làm contract giữa các agent ổn định: graph luôn nhận một result object có schema chuẩn, kể cả khi worker bên trong lỗi.

#### 9.3.4. Artifact ownership

Mỗi agent sở hữu đúng một artifact chính:

| Artifact | Agent sở hữu | State field |
| --- | --- | --- |
| `outline_payload` | `PedagogyPlannerAgent` | `outline_payload` |
| `content_payload` | `ContentDraftingAgent` | `content_payload` |
| `media_payload` | `MediaResearchAgent` | `media_payload` |
| `quiz_payload` | `ContentAssessmentAgent` | `quiz_payload` |
| `quality_review` | `QualityReviewerAgent` | `quality_review` |
| `merged_slides` | `SlideMerger` service | `merged_slides` |

`merged_slides` không thuộc sở hữu agent nào vì merge là deterministic service, không phải specialist agent.

### 9.4. Specialist agents

Các adapter nằm trong `src/llm/agents/`.

| Agent | File | Input chính | Output/artifact | Tool/worker bên dưới |
| --- | --- | --- | --- | --- |
| `PedagogyPlannerAgent` | `slide_planner.py` | `context_map`, `topic`, `grade`, `book`, `task_type`, `revision_instruction` | `outline_payload` | `OutlineAgent` |
| `ContentDraftingAgent` | `content_drafting.py` | `outline_payload.slides`, `chunk_map`, `task_type`, `revision_instruction` | `content_payload` | `ContentAgent` |
| `MediaResearchAgent` | `media_research.py` | `topic`, `grade`, `book`, `outline_payload`, `content_payload` | `media_payload` | `MediaAgent` + optional MCP media search |
| `ContentAssessmentAgent` | `content_assessment.py` | `topic`, `context_map` | `quiz_payload` | `QuizAgent` |
| `QualityReviewerAgent` | `quality.py` | `task_type`, `query`, `context`, `output` | `quality_review` | `get_quality_reviewer(task_type)` |

Các agent này wrap các worker cũ trong `src/llm/handlers/content/slide_agents/`. Vì vậy code vẫn giữ backward compatibility, nhưng kiến trúc bên ngoài đã rõ contract hơn.

Lưu ý thuật ngữ: `AgentResult` trong `src/schemas/slide_schemas.py` là envelope legacy cho worker/merger cũ (`agent`, `status`, `payload`, `latency_ms`). `AgentTaskResult` trong `src/schemas/agent_protocol.py` mới là contract inter-agent hiện tại. Khi viết luận văn, nên gọi `AgentTaskResult` là A2A-lite result; không nên lẫn với `AgentResult`.

### 9.5. Tool adapters trong graph

`src/llm/graphs/tools.py` expose các tool cho LangGraph supervisor:

- `generate_outline`
- `generate_content`
- `generate_media`
- `generate_quiz`
- `merge_results`
- `check_quality`

Tên `generate_quiz` trong content graph có nghĩa là sinh embedded assessment cho slide/giáo án, không phải quiz standalone trong `QuizService`.

`merge_results` là deterministic service, không phải agent. Nó dùng `SlideMerger` để ghép outline, content, media và quiz payload thành `MergedSlide`.

Các tool agent adapter hoạt động theo cùng một mẫu:

```text
Tool function
  -> đọc ContentSupervisorState qua InjectedState
  -> validate prerequisite
  -> build AgentTask
  -> Agent.run_task(task)
  -> json.dumps(AgentTaskResult)
  -> ToolMessage
  -> post_tool_processor parse và cập nhật state
```

Prerequisite contract:

| Tool | Điều kiện trước khi chạy | Nếu thiếu điều kiện |
| --- | --- | --- |
| `generate_outline` | Có `context_map` từ `preprocess_node` | Trả `AgentTaskResult(status="failed", error_code="INVALID_AGENT_INPUT")` |
| `generate_content` | Có `outline_payload.slides` | Trả failed result, yêu cầu gọi `generate_outline` trước |
| `generate_media` | Có thể chạy optional, dùng outline/content nếu có | Nếu agent fail thì degrade thành `partial` với media rỗng |
| `generate_quiz` | Có `context_map`; chỉ là assessment nhúng | Nếu agent fail thì degrade thành `partial` với `quiz_items=[]` |
| `merge_results` | Có `outline_payload` và `content_payload` | Trả legacy JSON `status="failed"` |
| `check_quality` | Có `merged_slides` | Trả `blocked` quality result nếu chưa có output |

Ngoài đường LLM supervisor gọi tool qua `ToolNode`, graph còn có các node deterministic/direct:

- `quiz_direct_node`: tự sinh quiz cho `task_type="slide"` nếu đã có content mà chưa có quiz.
- `media_direct_node`: tự gọi media agent nếu query có tín hiệu media/ảnh/gif/diagram.
- `merge_direct_node`: tự merge khi đã có content mà chưa có deck.
- `quality_direct_node`: tự review khi đã merge nhưng chưa có quality review.

Vì vậy mô tả chính xác là: LLM supervisor điều phối chính, còn graph có guardrail deterministic để đảm bảo các bước bắt buộc/optional hợp lý không bị bỏ sót.

### 9.6. Post-tool processing và registry artifact

`post_tool_processor()` là điểm chuyển đổi từ ToolMessage sang graph state.

Quy tắc xử lý:

1. Duyệt các `ToolMessage` mới nhất từ cuối về đầu.
2. Map `tool_name` sang state field bằng `TOOL_STATE_MAPPING`.
3. Parse JSON từ tool output.
4. Nếu output là `AgentTaskResult`:
   - Append vào `agent_results` nếu cặp `(task_id, agent_id)` chưa tồn tại.
   - Extract `task` và append vào `agent_tasks` nếu `task_id` chưa tồn tại.
   - Lấy `artifact_type` hoặc fallback về state field.
   - Nếu result không failed, hoặc failed nhưng vẫn có artifact, ghi vào `artifacts[artifact_type]` và state field tương ứng.
5. Nếu output là legacy JSON không failed, ghi trực tiếp vào `artifacts[state_key]` và state field.

State vì vậy có 4 lớp lưu trữ song song:

| Lớp | Mục đích |
| --- | --- |
| Legacy state fields (`outline_payload`, `content_payload`,...) | Giữ compatibility với merger/service/display cũ. |
| `agent_tasks` | Audit trail của task đã giao cho agent. |
| `agent_results` | Audit trail của result, status, latency, tool usage, error code. |
| `artifacts` | Registry artifact theo `artifact_type`, thuận tiện cho graph/debug và mở rộng sau này. |

### 9.7. ContentSupervisorState

`src/llm/graphs/state.py` mô tả state của graph.

Các nhóm field:

- Input: `task_type`, `request_id`, `query`, `topic`, `grade`, `book`, `rag_chunks`.
- Context: `synthesized_context`, `context_map`, `chunk_map`.
- Artifacts legacy fields: `outline_payload`, `content_payload`, `media_payload`, `quiz_payload`, `quality_review`.
- A2A-lite fields: `agent_tasks`, `agent_results`, `artifacts`.
- Quality/reflection: `reflection_attempts`, `revision_instruction`, `quality_blocked`.
- Output: `merged_slides`, `final_output`, `status`, `error_message`.

### 9.8. Quality reflection contract

`QualityReviewerAgent` trả `quality_review` với các field nghiệp vụ như `passed`, `score`, `reason_fail`, `issues`, `reflection_action`, `revision_instruction`, `requires_human_review`.

`reflection_decision_node()` đọc `quality_review` và quyết định:

| `reflection_action` | Hành vi |
| --- | --- |
| `approve` + `passed=True` | Kết thúc thành công. |
| `revise_outline` | Xóa `outline_payload`, `content_payload`, `merged_slides`; tăng `reflection_attempts`; đưa `revision_instruction` về supervisor. |
| `revise_content` | Xóa `content_payload`, `merged_slides`; regenerate content rồi merge/review lại. |
| `revise_quiz` | Xóa `quiz_payload`, `merged_slides`; regenerate quiz rồi merge/review lại. |
| `block` hoặc vượt quá `MAX_REFLECTION_ATTEMPTS` | Set `quality_blocked=True` hoặc `status="failed"` tùy verdict. |

Giới hạn hiện tại: `MAX_REFLECTION_ATTEMPTS = 2`. Reflection không tạo agent mới; nó tạo lại task cho đúng specialist thông qua `revision_instruction`.

### 9.9. Persistence contract trong `SlideService`

Khi graph hoàn tất, `SlideService._process_completed_result()` chỉ lưu **summary** của `agent_results` vào `slide_state.slide_output`, gồm:

- `task_id`
- `agent_id`
- `status`
- `artifact_type`
- `confidence`
- `used_tools`
- `latency_ms`
- `error_code`

Service không lưu full `task.inputs`, `context_map`, prompt hay raw context vào session output. Đây là chủ đích để metadata đủ debug nhưng không phình state và không lộ context dài.

## 10. MCP và Tool Layer

Repo có một MCP-like in-process tool layer trong `src/tools/`.

Các thành phần:

- `mcp_protocol.py`: định nghĩa `MCPRequest`, `MCPResponse`, method `tools/list` và `tools/call`.
- `mcp_client.py`: client gọi tool.
- `mcp_server.py`: server xử lý tool call.
- `base_tool.py`: interface chung cho tools.
- `implementations/tool_registry.py`: registry tool.
- `knowledge_retrieval_tool.py`: wrapper cho RAGService.
- `content_formatter_tool.py`: tool format context.
- `web_search_tool.py`: extension point cho web/media search.

Trạng thái hiện tại:

- MCP chưa phải remote/distributed MCP production.
- MCP đóng vai trò chuẩn hóa tool call nội bộ và extension point.
- Media search là ứng viên phù hợp nhất để MCP-backed trong tương lai.
- Không nên mô tả mọi specialist agent là MCP tool bên ngoài, vì phần lớn task hiện còn nhỏ và chạy tốt in-process.

## 11. Quality, validation và reflection

Hệ thống có hai quality path riêng.

### 11.1. Quiz standalone quality path

```text
Question handler
  -> QualityReviewer
  -> optional revise_quiz
  -> QuestionValidator
  -> persist QuizRound / QuestionRecord
```

Vai trò:

- `QualityReviewer`: đánh giá tổng thể bộ câu hỏi.
- `QuestionValidator`: kiểm tra từng câu hỏi với context và schema.
- `QuizService`: quyết định retry, block hoặc lưu câu hỏi.

### 11.2. Slide/Lesson Plan quality path

```text
Specialist agents
  -> SlideMerger
  -> QualityReviewerAgent
  -> approve / revise_outline / revise_content / revise_quiz / block
```

`reflection_decision_node` xử lý kết quả review:

- `approve`: đánh dấu success.
- `revise_outline`: clear outline/content/merged và regenerate.
- `revise_content`: clear content/merged và regenerate.
- `revise_quiz`: clear quiz/merged và regenerate.
- `block` hoặc `ask_human`: dừng pipeline.

Hiện `MAX_REFLECTION_ATTEMPTS = 2`, tức cho phép tối đa hai vòng sửa tự động trước khi dừng hoặc trả kết quả theo verdict của quality gate.

## 12. Session, memory và trace

### 12.1. Memory/session model

`src/llm/memory.py` chứa các dataclass:

- `Message`
- `QuestionRecord`
- `QuizRound`
- `QuizSessionState`
- `SlideSessionState`
- `Session`
- `MemoryManager`

Session giữ cả trạng thái hội thoại và trạng thái học tập. Đây là nền tảng cho các tác vụ follow-up như:

- "Giải thích câu 2"
- "Ôn lại câu sai"
- "Chấm đáp án của em"
- "Ok, duyệt dàn ý"

### 12.2. Persistent session store

`SessionStore` trong `src/llm/session_store.py` serialize session thành JSON. Orchestrator gọi `auto_save_async(ctx.session)` sau khi hoàn tất response.

### 12.3. Trace và debug

`RequestContext.add_debug_step()` ghi metadata từng node. Sau request, Orchestrator gọi:

- `_set_debug_info(ctx, full_response)`
- `trace_service.write_trace(ctx, full_response)`

Debug info trả về API giúp frontend hoặc người phát triển biết request đã đi qua các bước nào, strategy RAG nào, lấy bao nhiêu chunk, mất bao lâu và action nào được dispatch.

## 13. Frontend và API runtime

Frontend tĩnh nằm trong `app/frontend/`:

- `index.html`
- `style.css`
- `app.js`

FastAPI mount frontend tại `/` và assets tại `/assets`. Endpoint phụ:

```text
GET /api/frontend-info
```

trả thông tin version UI, đường dẫn frontend và kiểm tra dropdown book/grade.

Lệnh chạy thường dùng:

```bash
uvicorn app.api:app --reload
```

Hoặc chạy trực tiếp:

```bash
python app/api.py
```

Yêu cầu môi trường:

- `.env` có `GENAI_API_KEY`.
- Dữ liệu chunk và embedding tồn tại trong `data/`.
- Dependencies trong `requirements.txt` đã được cài.

## 14. Evaluation

Evaluation nằm trong `src/evaluation/` và output hiện tại nằm trong `data/eval/`.

Các file chính:

- `src/evaluation/run_eval.py`
- `src/evaluation/ragas_eval.py`
- `src/evaluation/report.py`
- `src/evaluation/data_collector.py`
- `data/eval/ragas/eval_report.md`
- `data/eval/ragas/eval_results.json`
- `data/eval/ragas/eval_metrics.json`
- `data/eval/ragas/eval_metrics.csv`

Kết quả hiện tại trong `data/eval/ragas/eval_report.md`:

| Metric | Giá trị trung bình |
| --- | ---: |
| Faithfulness | 0.9757 |
| Answer Relevancy | 0.8571 |
| LLM Context Precision With Reference | 0.8555 |
| Context Recall | 0.9593 |

Thống kê thời gian:

| Thành phần | Thời gian trung bình |
| --- | ---: |
| Retriever | 4.579 s |
| Generator | 1.979 s |
| Tổng pipeline | 6.558 s |

Số mẫu đánh giá: 246.

Khi viết luận văn, không nên tự thay số liệu này nếu chưa chạy lại evaluation.

## 15. Mapping nội dung sang LaTeX

### 15.1. Chương 3 - Công nghệ và cơ sở lý thuyết

Nên đưa các phần:

- RAG và adaptive retrieval.
- Hybrid search, embedding, reranker, RRF.
- Multi-intent routing.
- Multi-agent với LangGraph.
- A2A-lite in-process contract.
- MCP/tool layer như extension point.
- Session memory và HITL.

Điểm cần tránh: không mô tả toàn bộ hệ thống là LangGraph multi-agent. LangGraph chỉ áp dụng rõ cho content pipeline slide/lesson_plan.

### 15.2. Chương 4 - Kết quả triển khai và thực nghiệm

Nên đưa các phần:

- Kiến trúc request lifecycle thực tế.
- `RequestContext` là state xuyên suốt.
- Orchestrator mỏng + dispatcher + domain services.
- RAGService và 4 retrieval strategies.
- Quiz standalone service.
- Slide/Lesson Plan content multi-agent pipeline.
- Quality paths tách riêng cho quiz và content.
- SessionStore, TraceService, debug steps.
- RAGAS metrics và latency hiện có.

### 15.3. Chương 5 - Giải pháp và đóng góp

Nên nhấn mạnh:

- Thiết kế thin orchestrator giúp dễ mở rộng action.
- Multi-intent planning xử lý nhiều yêu cầu trong một query.
- Adaptive RAG cải thiện lựa chọn retrieval theo loại câu hỏi.
- Tách quiz standalone khỏi content assessment giúp maintain tracker/scoring.
- A2A-lite làm rõ vai trò sub-agent mà chưa cần distributed runtime.
- HITL outline review tăng kiểm soát cho slide/lesson plan.

### 15.4. Chương 6 - Kết luận và hướng phát triển

Hướng phát triển hợp lý:

- MCP-backed media search thật với URL validation và source attribution.
- Export slide sang PPTX/PDF/HTML.
- Test suite chính thức cho agent protocol, graph post-processing và slide pipeline.
- Theo dõi chất lượng theo từng user bằng student profile đầy đủ hơn.
- Evaluation riêng cho slide/lesson plan ngoài RAGAS QA.
- Cải thiện frontend streaming thật thay vì gom full response nếu cần.

## 16. Các quyết định kiến trúc quan trọng

### 16.1. Vì sao không đưa quiz standalone vào multi-agent content pipeline

Quiz standalone không chỉ là sinh câu hỏi. Nó còn gồm:

- Lưu `QuizRound`.
- Lưu từng `QuestionRecord`.
- Chấm câu trả lời.
- Theo dõi attempt.
- Ôn tập câu sai.
- Thống kê accuracy.
- Cập nhật `StudentTracker`.

Nếu đưa vào ContentSupervisor, các state tương tác này sẽ bị trộn với artifact generation và khó maintain. Vì vậy `ContentAssessmentAgent` chỉ sinh assessment nhúng trong slide/giáo án.

### 16.2. Vì sao slide và lesson plan dùng chung pipeline

Về nghiệp vụ, slide và giáo án đều cần:

- Xác định mục tiêu học tập.
- Lập outline.
- Viết nội dung theo SGK.
- Có thể kèm media.
- Có thể kèm assessment.
- Merge artifact.
- Review chất lượng.

Khác biệt nằm ở `task_type`, prompt/template và format đầu ra, không cần tách supervisor.

### 16.3. Vì sao dùng A2A-lite thay vì full A2A/MCP distributed

Hiện các sub-agent chạy in-process, task nhỏ và phụ thuộc nhiều vào context nội bộ. Full distributed A2A/MCP sẽ tăng độ phức tạp vận hành mà chưa đem lại nhiều lợi ích. A2A-lite đủ để:

- Chuẩn hóa task envelope.
- Ghi agent execution metadata.
- Tách artifact ownership.
- Chuẩn bị đường nâng cấp sang external agents/tools sau này.

### 16.4. Vì sao MCP hiện là extension point

MCP hữu ích nhất khi tool cần năng lực ngoài process, ví dụ:

- Web/image search.
- URL validation.
- Source attribution.
- Export/render artifact.

Các task như outline/content drafting hiện vẫn phù hợp hơn với in-process agent adapters.

## 17. Cây thư mục kỹ thuật rút gọn

```text
app/
  api.py                         FastAPI entrypoint
  frontend/                      Static frontend

src/
  config/                        Cấu hình model, retrieval, eval
  rag/                           RAG service, adaptive RAG, retriever, reranker
  schemas/                       RequestContext, agent protocol, output schemas
  tools/                         MCP-like in-process tool layer
  evaluation/                    RAGAS evaluation
  utils/                         Logging, trace, error handling
  llm/
    orchestrator.py              Thin pipeline controller
    intent_router.py             Multi-intent detection
    action_planner.py            Rule-based action planning
    execution_dispatcher.py      Action -> service/handler registry
    session_manager.py           Resolve conversational session
    session_store.py             Persist JSON sessions
    memory.py                    Session/quiz/slide state dataclasses
    services/
      quiz_service.py            Quiz standalone lifecycle
      slide_service.py           Slide/lesson_plan facade + HITL
      slide_merger.py            Deterministic artifact merge
      quality_reviewer.py        Shared quality review wrapper
    graphs/
      content_supervisor.py      LangGraph content supervisor
      tools.py                   Agent dispatch adapters + merge tool
      state.py                   ContentSupervisorState
      stream_wrapper.py          Graph invoke/resume helpers
    agents/
      base.py                    BaseAgent
      slide_planner.py           PedagogyPlannerAgent
      content_drafting.py        ContentDraftingAgent
      media_research.py          MediaResearchAgent
      content_assessment.py      ContentAssessmentAgent
      quality.py                 QualityReviewerAgent
    handlers/
      question/                  MCQ/essay/fill/true_false/scorer
      content/                   Legacy content worker implementations
      explain_handler.py
      chat_handler.py
      fallback_handler.py
    validators/
      question_validator.py

data/                            Chunks, mappings, sessions, embeddings, evaluation artifacts
data/eval/                       Evaluation results
docs/                            Technical docs and refactor notes
latex/                           Thesis LaTeX source
```

## 18. Các điểm cần nói cẩn thận trong báo cáo

- Không gọi `merge_results` là agent; nó là deterministic service/tool.
- Không gọi `ContentAssessmentAgent` là quiz standalone; nó chỉ tạo assessment nhúng.
- Không nói MCP-backed media search đã production-ready; hiện là extension point.
- Không nói toàn bộ project dùng LangGraph; LangGraph nằm ở content supervisor.
- Không nói `QueryClassifier` dùng LLM; nó là heuristic code.
- Không gom `QualityReviewerAgent`, `QuestionValidator` và `QualityReviewer` thành một "Validator Agent" chung.
- Không cập nhật số liệu RAGAS nếu chưa chạy lại evaluation.

## 19. Checklist kiểm tra khi cập nhật LaTeX

Khi sửa các chương LaTeX theo docs này, nên kiểm tra:

```bash
rg -n "Validator Agent|MergeAgent|QuizAgent|Google Gemini 2.5 Flash|Generation Layer \\(Tổng hợp Toàn bộ" latex/Chuong
```

Build root:

```bash
cd latex
latexmk -pdf DoAn.tex
```

Build riêng Chương 4:

```bash
cd latex/Chuong
latexmk -pdf 4_Ket_qua_thuc_nghiem.tex
```

Không nên build riêng chương từ thư mục `latex` bằng đường dẫn `Chuong/4_Ket_qua_thuc_nghiem.tex` vì `subfiles` có thể resolve sai preamble `../DoAn.tex`.
