# Plan chi tiết Chương 4: Cài đặt, kiểm thử và đánh giá hệ thống

> Plan riêng cho Chương 4, tách khỏi `thesis_research_oriented_writing_plan.md`.
> Chương 4 quan trọng ngang Chương 3: Chương 3 trả lời "thiết kế thế nào", Chương 4 trả lời
> "đã hiện thực hóa và đo được kết quả gì". Trọng tâm là **đánh giá hai node lõi**:
> retrieve node và generate node, kèm việc **xây dựng hai bộ dữ liệu kiểm thử** tương ứng.

---

## 0. Nguyên tắc và phạm vi chương

- Chương 4 KHÔNG mô tả lại kiến trúc (đã làm ở Chương 3). Phần cài đặt chỉ viết ở mức
  đủ để tái lập thí nghiệm: môi trường, cấu hình, tham số, không liệt kê package.
- Trọng tâm gồm ba khối:
  1. Cài đặt (environment + cấu hình các node trọng tâm).
  2. **Xây dựng dữ liệu kiểm thử** cho retrieve node và generate node.
  3. **Kết quả đánh giá** retrieval + generation + phân tích lỗi.
- Hai node được đánh giá độc lập bằng hai phương pháp khác nhau:
  - Retrieve node: định lượng tự động bằng benchmark single-gold (Hit@k, Recall@k, MRR@k, nDCG@k).
  - Generate node: đánh giá định lượng bằng **RAGAS** (LLM-as-judge), 4 metric.

### Phương pháp đánh giá generation (đã chốt)
- Generation được đánh giá bằng **RAGAS / LLM-as-judge** làm phương pháp định lượng **chính thức
  và duy nhất** cho generate node. Không dùng rubric chấm tay.
- Kết quả hiện có là **246 mẫu** trong `data/eval/ragas/eval_metrics.json` + báo cáo tổng hợp
  `eval_report.md`. Đây là **kết quả chính thức** của chương, trình bày như số liệu thực nghiệm
  hợp lệ.
- Khi viết Chương 4: chỉ trình bày phương pháp + kết quả, KHÔNG mô tả bộ kết quả này như tạm thời,
  sơ bộ, hay cần chạy lại. Cỡ mẫu 246 là cỡ mẫu báo cáo.
- Lưu ý văn phong khi bàn LLM-as-judge: nêu đây là phương pháp đánh giá tự động phổ biến cho RAG,
  giải thích cơ chế từng metric để người đọc hiểu vì sao điểm đáng tin, thay vì phải dựa vào
  một lớp chấm tay bổ sung.

---

## 1. Hiện trạng tài sản đánh giá (asset inventory)

Bảng này quyết định phần nào "viết là xong" và phần nào "phải làm thêm".

| Hạng mục | Trạng thái | Vị trí | Ghi chú |
|---|---|---|---|
| Benchmark retrieval (600 query) | ✅ Xong | `data/eval/retrieval/benchmark_eval.jsonl` | single-gold theo `gold_lesson_key` |
| Kết quả retrieval no-rerank | ✅ Xong | `data/eval/retrieval/no_rerank/` | summary.json + per_query.jsonl |
| Kết quả retrieval with-rerank | ✅ Xong | `data/eval/retrieval/with_rerank/` | đã có, so sánh được trước/sau rerank |
| Script tính metric retrieval | ✅ Xong | `src/evaluation/eval_retrieval.py` | `ranking_metrics()` |
| Script lọc/validate benchmark | ✅ Xong | `filter_benchmark.py`, `validate_benchmark.py` | dedup + stratified sampling |
| RAGAS evaluator | ✅ Xong | `src/evaluation/ragas_eval.py` | ragas 0.4.x, 4 metric |
| Data collector (retrieve→generate) | ✅ Xong | `src/evaluation/data_collector.py` | sinh (Q, contexts, answer, reference) |
| Kết quả RAGAS (246 mẫu) | ✅ Xong (chính thức) | `data/eval/ragas/eval_metrics.json` + `eval_report.md` | cỡ mẫu báo cáo = 246 |
| Report generator | ✅ Xong | `src/evaluation/report.py` | `eval_report.md` |

### Lưu ý cho phần viết 4.7/4.10
- Bộ kết quả generation (246 mẫu, có đủ `user_input / retrieved_contexts / response / reference`
  + 4 metric + `timing`) đã hoàn chỉnh trong `eval_results.json` và `eval_metrics.json`.
  KHÔNG cần chạy lại; viết chương dựa thẳng trên các file này.
- Khi mô tả "xây dựng testset" (mục 4.7) cho generate node: mô tả pipeline đã dùng để tạo bộ này
  (testset → collect → evaluate → report) ở mức phương pháp, dựa trên các trường thực tế còn lưu
  trong `eval_results.json`. Không cần dựng lại `TestsetGenerator` để viết — chỉ trình bày quy trình
  đã sinh ra dữ liệu.
- `reference` trong bộ dữ liệu là đáp án tham chiếu đi kèm mỗi câu hỏi; mô tả đúng vai trò của nó
  với các metric (đặc biệt Context Recall và Context Precision dựa trên reference). Không suy diễn
  thêm về nguồn nếu không chắc; bám trường dữ liệu thật.

---

## 2. Cấu trúc chương đề xuất (skeleton LaTeX)

Giữ đánh số 4.1–4.12 như plan gốc nhưng gom lại cho mạch hơn. Mỗi mục ghi rõ "viết gì" + "nguồn".

### 4.1. Môi trường và cấu hình cài đặt
- Ngôn ngữ, backend, LLM provider/model, embedding model, reranker model, vector index.
- Bảng tham số chạy thực nghiệm (lấy từ `src/config/config.py`):
  `RETRIEVER_TOP_K`, `RERANKER_TOP_N`, `search_pool`, `EVAL_LLM_MODEL`, `EVAL_EMBEDDING_MODEL`,
  temperature generation (0.1) và temperature eval (0).
- Môi trường chạy (máy/Colab, vì with-rerank chạy ~1895s cho 600 query → nêu phần cứng). phần cứng của tôi là CPU : i512450H, ram 16gb, gpu rtx3050
- Nguồn: `config.py`, `docs/project_technical_reference_vi.md`.

### 4.2. Cấu trúc cài đặt hệ thống (ngắn)
- Sơ đồ module mức cao: app/API → orchestrator → RAG service → retriever/reranker →
  generate → services (quiz/slide). Thêm nhánh `src/evaluation/` như một subsystem riêng.
- KHÔNG liệt kê file lẻ. Một sơ đồ + một đoạn mô tả.

### 4.3. Cài đặt pipeline xử lý tài liệu (tóm tắt)
- Nguồn SGK → làm sạch → chunk theo tiêu đề → metadata → index Qdrant.
- Báo số liệu thực: tổng số chunk, phân bố theo book-grade (đã có hình ở Chương 3, ở đây chỉ
  trích số tổng để chứng minh đã index thật).

### 4.4. Cài đặt pipeline hỏi đáp (luồng generate node)
- Mô tả luồng từ câu hỏi → orchestrator → retrieve → generate → response.
- Trích **prompt template generation thật** (`ANSWER_PROMPT` trong `data_collector.py`):
  vai trò trợ lý Tin học THPT, đưa context vào, quy tắc "nếu tài liệu không đủ thì nói rõ".
- Nhấn: generate node bám nguồn (grounding), temperature thấp (0.1).

### 4.5. Cài đặt retrieve node và rerank
- Hybrid search top-k (`RETRIEVER_TOP_K`) → rerank cross-encoder top-n (`RERANKER_TOP_N`).
- Filter scope theo book/grade/topic.
- Một ví dụ kết quả retrieval thật: chunk rút gọn + score + metadata + source.

### 4.6. Cài đặt generate node
- Cách ghép context (`"\n\n---\n\n".join(contexts)`).
- Quy tắc trả lời khi thiếu context, format cho học sinh, giữ nguồn để debug.

### 4.7. Xây dựng dữ liệu kiểm thử (MỤC TRỌNG TÂM — xem chi tiết mục 3 dưới)
- Tách rõ hai bộ: benchmark retrieval và testset generation.
- Với benchmark retrieval: viết **kỹ phần chứng thực nguồn gốc** (mục 3.1) — câu chuyện làm lại v3,
  instruction từng bước, phân định code vs LLM, và bộ trường truy vết (seed_chunk_id + sha1 + gen_meta)
  để chứng minh data thật, không bịa, kiểm chứng độc lập được.
- Phải nói rõ phần nào deterministic-code (mô tả qua), phần nào LLM sinh (mô tả kỹ ràng buộc + kiểm soát).

### 4.8. Kiểm thử chức năng
- Giữ bảng TC01–TC10 như plan gốc (đọc SGK, chunking, indexing, scope filter, retrieval,
  rerank, generation, out-of-scope, multi-intent, logging). Mỗi TC: input + kết quả mong đợi + đạt/không.
- Đây là kiểm thử chức năng (đúng/sai), khác với đánh giá định lượng ở 4.9/4.10.

### 4.9. Kết quả đánh giá retrieve node (xem mục 4 dưới — đã có số thật)
### 4.10. Kết quả đánh giá generate node bằng RAGAS (xem mục 5 dưới)
### 4.11. Phân tích lỗi (giữ phân nhóm lỗi của plan gốc: dữ liệu/chunking/retrieval/rerank/generation/eval)
### 4.12. Nhận xét tổng hợp kết quả thực nghiệm

---

## 3. TRỌNG TÂM: Xây dựng hai bộ dữ liệu kiểm thử

### 3.1. Bộ benchmark cho retrieve node — XÂY DỰNG & CHỨNG THỰC NGUỒN GỐC (mục trọng tâm nhất)

> Đây là phần dễ bị hội đồng soi nhất: "câu hỏi ở đâu ra, có bịa không, sao biết nhãn gold đúng".
> Phải viết để chứng minh được TỪNG câu hỏi truy ngược về một đoạn SGK thật, có chữ ký nội dung,
> và quy trình có instruction từng bước rõ ràng (file `plan/step1_llm_regen_instruction.md`).

**Mục tiêu**: đo khả năng truy hồi đúng bài học chứa câu trả lời.

#### (i) Vì sao có bản v3 — câu chuyện làm lại (nên kể ngắn trong báo cáo để tăng độ tin cậy)
Bản benchmark đầu (v1, 250 câu) **bị hỏng từ khâu sinh câu hỏi**: ~95% câu là template tất định
(nhét anchor vào 5 khuôn cứng, KHÔNG dùng LLM), khiến eval ra Hit@1=0.43 nhưng đó là lỗi dữ liệu,
không phải lỗi search — nhóm 11 câu không-template đạt Hit@10=1.00 chứng minh search vốn tốt.
→ Quyết định làm lại hoàn toàn (v3): sinh câu bằng **LLM thật đọc nội dung đoạn**, ràng buộc câu hỏi
phải *phân biệt được bài* (discriminative). Việc trình bày bước sửa sai này cho thấy data được kiểm
soát chất lượng có phương pháp, không phải sinh bừa.

#### (ii) Có instruction từng bước (truy vết được quy trình)
Toàn bộ quy trình sinh được đặc tả trong `plan/step1_llm_regen_instruction.md` — gồm: lý do làm lại,
phần tái dùng nguyên (chọn seed/coverage/balancing), hợp đồng đầu ra JSON, bộ điều kiện A–F cho câu hỏi,
luật validate, schema row, CLI, và tiêu chí nghiệm thu. Trong báo cáo: trích lại đặc tả này theo từng
bước để chứng minh pipeline có thiết kế rõ ràng, lặp lại được, không phải thao tác thủ công ngẫu hứng.
> **Lưu ý hành động:** đưa nguyên file `step1_llm_regen_instruction.md` cho một LLM mạnh để nó reason
> lại từng bước, viết thành đoạn văn học thuật mạch lạc cho 4.7. Phần nào implement bằng code
> (deterministic) thì chỉ cần mô tả qua chức năng + input/output; phần nào do LLM sinh thì mô tả kỹ
> ràng buộc và cơ chế kiểm soát.

#### (iii) Quy trình 3 bước + cái gì là CODE, cái gì là LLM
**Bước 1 — Sinh câu (LLM, có kiểm soát)** → `benchmark_raw.jsonl`:
- Chọn seed bằng **code tất định** (`select_seeds`): phủ đủ 185 bài, cân bằng book×grade. Mô tả qua.
- Với mỗi seed, **LLM (Gemini, temp 0.3)** đọc `seed_content` thật của đoạn và sinh N=2 câu, ép JSON,
  bắt buộc tuân thủ điều kiện A–F: (A) trả lời được CHỈ bằng đoạn, cấm bịa; (B) **discriminative** —
  chứa thuật ngữ/cú pháp riêng của bài (vd `//` và `%`, `math.gcd()`, TCVN3) để không bài khác trả lời
  được; (C) self-contained, cấm "đoạn trên/bài này/nó"; (D) tự nhiên, cấm 5 khuôn template; (E) đa dạng
  question_type; (F) few-shot 1 ví dụ tốt + 1 ví dụ xấu.
- **Validate ngay sau khi LLM trả (code deterministic):** loại câu nếu không kết thúc "?", <18 ký tự,
  khớp regex 5 khuôn template, chứa từ mơ hồ, `anchor`/`distinctive_terms` KHÔNG nằm trong `seed_content`
  (chuẩn hóa + check substring), `expected_answer` overlap token với đoạn < 0.5, hoặc trùng câu đã giữ.
- **Cache + idempotent:** kết quả LLM cache theo `seed_chunk_id@prompt_version`; chạy lại ra như cũ,
  không gọi lại LLM. → chứng minh tái lập được.

**Bước 2 — Lọc (code, `filter_benchmark.py`)** → `benchmark_filtered.jsonl`:
- Dedup (trùng chuẩn hóa) + chống rò rỉ tiêu đề (title leak: n-gram ≥5 trùng breadcrumb/lesson_name →
  loại, tránh câu "ăn gian" bằng cách lặp tên bài).

**Bước 3 — Validate cuối + chọn mẫu (code thuần deterministic, `validate_benchmark.py`)**
→ `benchmark_eval.jsonl`:
- ⚠️ **ĐÃ VERIFY CODE:** Step 3 KHÔNG gọi LLM (docstring file ghi rõ "does not call any LLM",
  validator tag = `codex_light_rules_v1`). Cổng discriminative-bằng-LLM nêu ở mục 11 của file
  instruction **chỉ là đề xuất, KHÔNG được hiện thực**. → Khi viết luận văn KHÔNG được khẳng định
  có lớp LLM kiểm bài ở Step 3.
- Các kiểm tra thực tế (đều deterministic): `is_self_contained` (≥18 ký tự, kết thúc "?", không từ
  mơ hồ/khuôn), `anchor_valid` (anchor ≤10 từ và nằm trong `seed_content`),
  `answerable` (anchor trong seed + `expected_answer` overlap token ≥ 0.6 với seed), dedup câu trùng.
- Stratified sampling theo book_grade × lesson × question_type (cân coverage 185 bài).
- **Điểm cần nêu đúng:** tính discriminative (câu phân biệt được bài) được kiểm soát ở **Bước 1**
  qua ràng buộc A–F khi LLM sinh + validate ngay sau sinh — KHÔNG phải ở Bước 3. Đừng dồn công lao
  cho Step 3.

#### (iv) Schema một câu — các trường là BẰNG CHỨNG truy vết
```json
{
  "query_id": "V3A-0001",
  "query": "Sau khi mở IDLE (Python 3.9 64-bit), cửa sổ Shell cho phép ... thao tác gì ...?",
  "question_type": "fact",                 // fact|application|process|definition|list|compare
  "difficulty": "easy",                    // easy|medium|hard
  "anchor": "IDLE (Python 3.9 64-bit)",    // cụm khóa câu xoáy vào, PHẢI có trong seed
  "seed_chunk_id": "59e9899d-...",         // ID đoạn SGK gốc sinh ra câu → truy ngược được
  "gold_chunk_id": "59e9899d-...",         // đoạn chứa đáp án
  "source_level": 2,
  "gold_lesson_key": {                     // nhãn vàng mức bài học
    "book": "CD", "grade": "10",
    "topic_name": "...", "lesson": "Bài 1", "lesson_name": "..."
  }
}
```
Trong file raw còn có (nên nêu để chứng thực, dù bản eval đã rút gọn):
`seed_content` (toàn văn đoạn gốc), `seed_content_sha1` (**chữ ký nội dung** — chứng minh câu sinh từ
đúng đoạn đó, đoạn không bị sửa), `distinctive_terms`, và
`gen_meta = {generator: "gemini", prompt_version: "step1_v3_llm_discriminative", stage: "raw_generation"}`.
→ Bộ ba (seed_chunk_id + seed_content_sha1 + gen_meta) cho phép **kiểm chứng độc lập**: mở đúng chunk,
đối chiếu hash, đọc đoạn, xác nhận câu hỏi trả lời được bằng đoạn. Đây là luận điểm chống "bịa data".

> **Hai lệch nhỏ code-vs-file cần biết trước khi trích code:**
> 1. `validate_benchmark.py` default `--sample-size 250`, nhưng `benchmark_eval.jsonl` thật có **600 câu**
>    (đã chạy với sample-size=600, và do accepted=600 nên giữ toàn bộ). Nêu con số 600, đừng nêu 250.
> 2. Hàm `final_row()` trong code hiện KHÔNG xuất `gold_chunk_id`/`gold_chunk_ids`, nhưng file eval thật
>    LẠI CÓ các trường đó → file được sinh bởi một phiên bản script nhỉnh hơn bản đang đọc. Nếu trích
>    `final_row()` làm minh họa, phải đối chiếu lại với file, hoặc mô tả trường ở mức dữ liệu thật thay vì
>    dán nguyên hàm.

#### (v) Số liệu thật của bộ benchmark (từ `benchmark_raw_report.json` / `benchmark_filtered_report.json`)
- 600 câu, từ 300 seed, **phủ 185 bài học**.
- Cân bằng tuyệt đối theo nhóm: mỗi book-grade đúng 100 câu (CD/KNTT × 10/11/12).
- Phân bố loại câu: definition 153, fact 150, application 141, compare 81, list 42, process 33.
- Độ khó: easy 326, medium 274.
- Bước lọc: input 600 → kept 600, dropped 0 (vì chất lượng đã kiểm soát ở bước 1) — nêu rõ con số này.

#### (vi) Định nghĩa "đúng" (relevance) và giới hạn
Một chunk được tính đúng nếu cùng `(book, grade, topic_name, lesson_name)` với `gold_lesson_key`
(single-gold mức bài học, mỗi câu một bài gold). Phải giải thích lựa chọn này và hệ quả: recall/nDCG
thấp về tuyệt đối vì nhiều chunk cùng bài đều tính đúng → headline dùng Hit@k và MRR.

### 3.2. Bộ testset cho generate node (✅ đã có 246 mẫu — mô tả lại quy trình)

**Mục tiêu**: đo chất lượng câu trả lời sinh ra (đúng, bám nguồn, đủ ý, liên quan).

**Schema một mẫu (đầu vào testset)**:
```json
{ "user_input": "câu hỏi", "reference": "đáp án tham chiếu (ground truth)" }
```

**Schema một mẫu (sau khi collect — đầu vào RAGAS)**:
```json
{
  "user_input": "...",
  "retrieved_contexts": ["chunk1", "chunk2", ...],   // context generate node thực sự dùng
  "response": "...",                                  // câu trả lời LLM sinh
  "reference": "...",                                 // đáp án tham chiếu
  "timing": {"retrieve_s": ..., "generate_s": ..., "total_s": ...}
}
```

**Quy trình xây dựng (mô tả trong 4.7, 4 bước = pipeline `run_eval.py`)**:
1. `testset` — sinh danh sách `(user_input, reference)` làm đầu vào.
2. `collect` — với mỗi câu: retrieve+rerank → generate → ghi `(Q, contexts, answer, reference)`
   vào `eval_results.json` (`data_collector.py`).
3. `evaluate` — chạy RAGAS, ghi `eval_metrics.json` (`ragas_eval.py`).
4. `report` — sinh `eval_report.md` + bảng tổng hợp (`report.py`).

**Lưu ý khi viết**:
- Mô tả quy trình 4 bước ở mức phương pháp, dựa trên dữ liệu thực còn lưu (246 mẫu đầy đủ field).
- Giải thích vai trò `reference` với các metric dựa-trên-reference (Context Recall, Context Precision).
- Phân biệt rõ với benchmark retrieval ở 3.1: đây là bộ phục vụ đánh giá chất lượng câu trả lời,
  khác mục tiêu với bộ đo thứ hạng truy hồi.

---

## 4. Kết quả đánh giá retrieve node (số thật đã có)

So sánh no-rerank vs with-rerank trên cùng 600 query (đọc cột `after_rerank`).

### Bảng overall
| Metric | No-rerank | With-rerank | Δ |
|---|---:|---:|---:|
| Hit@1 | 0.762 | 0.818 | +5.7pp |
| Hit@3 | 0.937 | 0.950 | +1.3pp |
| Hit@5 | 0.968 | 0.975 | +0.7pp |
| Hit@10 | 0.982 | 0.983 | +0.2pp |
| MRR@10 | 0.848 | 0.886 | +3.7pp |
| nDCG@10 | 0.427 | 0.417 | −1.0pp |
| Precision@10 | 0.337 | 0.313 | −2.4pp |
| Thời gian (600 query) | 59.7s | 1895.5s | ×31.8 |

### Bảng theo nhóm book-grade (Hit@1 / MRR@10)
| Nhóm | Hit@1 no→with | MRR@10 no→with |
|---|---|---|
| CD-10 | 0.70 → 0.80 | 0.809 → 0.882 |
| CD-11 | 0.90 → 0.91 | 0.937 → 0.946 |
| CD-12 | 0.77 → 0.80 | 0.843 → 0.860 |
| KNTT-10 | 0.74 → 0.79 | 0.842 → 0.869 |
| KNTT-11 | 0.70 → 0.82 | 0.813 → 0.882 |
| KNTT-12 | 0.76 → 0.79 | 0.848 → 0.875 |

### Phân tích cần viết
- Reranker cải thiện rõ ở top-1 (Hit@1 +5.7pp, MRR@10 +3.7pp); lợi ích lớn nhất ở nhóm vốn yếu
  (KNTT-11 +12pp, CD-10 +10pp), nhóm đã mạnh (CD-11) gần bão hòa.
- Hit@10 gần như không đổi → reranker sắp xếp lại thứ hạng, KHÔNG mở rộng độ phủ.
- nDCG@10/Precision@10 giảm nhẹ: do benchmark single-gold, nhiều chunk cùng bài đều tính đúng;
  retriever thô nhồi nhiều chunk cùng bài vào top-10 nên precision/nDCG cao "ảo". → phải nói rõ
  Hit@1 và MRR là metric chính ở đây, nDCG@10/Precision@10 ít phù hợp với setup single-gold.
- Trade-off chi phí: ×31.8 latency (~3.16s/query cho rerank). Bàn hướng giảm: batch, cache,
  chỉ rerank khi Adaptive RAG thấy cần.

---

## 5. Kết quả đánh giá generate node bằng RAGAS

### 5.1. RAGAS là gì và 4 metric đang dùng (mô tả để viết 4.10)
Hệ thống dùng **ragas 0.4.x**, metric dạng class, chấm bằng LLM (Gemini) + embedding tiếng Việt.
Bốn metric (trong `ragas_eval.py`):

| Metric (class) | Đo cái gì | Cần trường nào | Ý nghĩa khi cao |
|---|---|---|---|
| `Faithfulness` | Câu trả lời có bám context không (chống bịa) | response, retrieved_contexts | ít hallucination |
| `ResponseRelevancy` | Câu trả lời có đúng trọng tâm câu hỏi không | user_input, response (+embedding) | trả lời đúng ý hỏi |
| `LLMContextPrecisionWithReference` | Context lấy về có hữu ích/đúng thứ hạng không | user_input, retrieved_contexts, reference | retrieve sạch |
| `LLMContextRecall` | Context có phủ đủ thông tin của reference không | retrieved_contexts, reference | retrieve đủ |

Lưu ý: hai metric context (precision/recall) thực chất phản ánh chất lượng retrieve dưới góc nhìn
generation — nên trong báo cáo phải phân biệt với metric retrieval ở 4.9 (single-gold mức bài),
tránh người đọc nhầm là đo trùng.

### 5.2. Cách cấu hình và chạy (mô tả trong 4.7, code đã có)
- LLM chấm: `ChatGoogleGenerativeAI(model=EVAL_LLM_MODEL, temperature=0)`.
- Embedding: `HuggingFaceEmbeddings("dangvantuan/vietnamese-document-embedding", trust_remote_code=True)`
  bọc bằng `LangchainEmbeddingsWrapper` (để có `embed_query` cho ResponseRelevancy).
- Gán thủ công `metric.llm`/`metric.embeddings` cho từng metric (tránh lỗi "LLM is not set").
- `RunConfig(max_workers=2, max_retries=10, max_wait=30)` để chịu rate-limit free-tier Gemini.
- Lệnh chạy:
  ```
  python src/evaluation/run_eval.py --step all --num_samples 300
  # hoặc từng bước: --step testset | collect | evaluate | report
  ```

### 5.3. Kết quả (246 mẫu — số chính thức, nguồn `eval_report.md`)
| Metric | Giá trị TB (246 mẫu) |
|---|---:|
| Faithfulness | 0.9757 |
| Answer Relevancy | 0.8571 |
| Context Precision (LLM, with reference) | 0.8555 |
| Context Recall | 0.9593 |
| Latency retrieve TB | 4.579s |
| Latency generate TB | 1.979s |
| Tổng pipeline TB | 6.558s |

(Số khớp `data/eval/ragas/eval_report.md`. Trình bày như kết quả thực nghiệm chính thức của chương.)

### 5.4. Phân tích cần viết
- Faithfulness rất cao (0.976) → generate node bám nguồn tốt, ít bịa (đúng mục tiêu grounding).
- Answer Relevancy thấp hơn (0.857) → đôi khi trả lời lan man/thừa; phân tích ví dụ từ `eval_metrics.json`.
- Context Recall cao (0.959) nhưng Precision thấp hơn (0.856) → retrieve lấy đủ nhưng còn lẫn nhiễu,
  liên hệ với nhận xét reranker ở 4.9.
- Có thể trích vài mẫu điểm thấp nhất từ `eval_metrics.json` làm ví dụ định tính minh họa lỗi.

### 5.5. Báo cáo một cấu hình production
Bộ kết quả 246 mẫu được tạo trên cấu hình production (hybrid retrieve + rerank + generate).
Báo cáo theo đúng cấu hình này. Nếu bảng 4.10 trong plan gốc liệt kê nhiều dòng cấu hình
(vector-only / +rerank / adaptive), rút gọn lại còn cấu hình đã chạy thật để không tạo ô trống
hoặc số không có nguồn.

---

## 6. Thứ tự thực hiện viết Chương 4

Dữ liệu cho cả hai node đã có sẵn, không cần chạy lại evaluation. Trọng tâm là viết.

1. Trích số từ các file đã có: `data/eval/retrieval/{no_rerank,with_rerank}/summary.json`
   và `data/eval/ragas/eval_report.md` + `eval_metrics.json`.
2. Viết 4.7 (xây dựng hai bộ dữ liệu) — mô tả quy trình đã sinh ra benchmark retrieval và
   testset generation, bám trường dữ liệu thật.
3. Viết 4.9 (kết quả retrieval) — bảng no/with rerank + phân tích trade-off.
4. Viết 4.10 (kết quả generation RAGAS) — bảng 4 metric + giải thích từng metric.
5. Viết 4.11 (phân tích lỗi) — trích ví dụ thật từ `per_query.jsonl` và `eval_metrics.json`.
6. Viết nhanh 4.1–4.6 (cài đặt) + 4.8 (test case chức năng) + 4.12 (nhận xét tổng hợp).

## 7. Checklist hoàn thành Chương 4
- [ ] Đã mô tả rõ quy trình xây dựng CẢ HAI bộ dữ liệu (retrieval + generation) ở 4.7.
- [ ] Benchmark retrieval: đã chứng thực nguồn gốc (v3 làm lại, instruction từng bước, code vs LLM,
      trường truy vết seed_chunk_id/sha1/gen_meta, số liệu phủ 185 bài + cân bằng 100 câu/nhóm).
- [ ] Đã chỉ rõ phần deterministic-code (mô tả qua) vs phần LLM sinh (mô tả kỹ ràng buộc A–F).
- [ ] Bảng retrieval no/with rerank đã có (4.9) + phân tích trade-off.
- [ ] Bảng RAGAS 246 mẫu đã có (4.10) + giải thích 4 metric, trình bày như số liệu chính thức.
- [ ] Đã nêu RAGAS/LLM-as-judge là phương pháp đánh giá generation chính thức (không cần rubric tay).
- [ ] Phân tích lỗi (4.11) bám ví dụ thật từ `per_query.jsonl` và `eval_metrics.json`.
- [ ] Đã nêu giới hạn ở mức phù hợp: single-gold benchmark cho retrieval, free-tier latency.
- [ ] Số liệu trong chương khớp với file trong `data/eval/` (không bịa số).
- [ ] Không có chỗ nào mô tả bộ kết quả generation là tạm/sơ bộ/cần chạy lại.
