# Step 1 (LLM) — Sinh lại benchmark retrieval: Chỉ dẫn triển khai cho Codex

## 0. Bối cảnh & lý do làm lại (đọc kỹ trước khi code)

Benchmark hiện tại (`retrieval_benchmark_final_250_v1.jsonl`) **hỏng từ khâu sinh câu hỏi**, không phải do search.
Bằng chứng (eval lesson-level, single retriever):

- 239/250 câu (95%) là **template rỗng nghĩa**. Eval Hit@1 = 0.43, Hit@10 = 0.76.
- Nhóm 11 câu **non-template** đạt Hit@1 = 0.73, **Hit@10 = 1.00** → search tốt, benchmark tệ.

Nguyên nhân gốc: `src/evaluation/generate_retrieval_benchmark_step1_v2.py` hàm `choose_question()` là
**bộ sinh template tất định** (nhét anchor vào khuôn cứng), KHÔNG dùng LLM. Step 2/Step 3 cũng thuần rule,
chỉ check token-overlap nên template lọt hết. 5 khuôn cần diệt:

```
"{anchor} được hiểu là gì?"
"{anchor} có vai trò gì trong ví dụ hoặc yêu cầu được nêu?"
"Với {anchor}, các thao tác chính cần thực hiện là gì?"
"{anchor} gồm những thành phần hoặc đặc điểm nào?"
"{anchor} được dùng để làm gì?"
```

Quyết định đã chốt:
- **Gold = single-lesson** (mỗi câu trỏ đúng 1 bài). Metric chính: Hit@k, MRR. Bỏ recall/ndcg multi-gold khỏi headline.
- Sinh câu bằng **LLM thật** đọc `seed_content`, viết câu **tự nhiên + phân biệt được bài** (discriminative).

## 1. Mục tiêu

Viết file mới `src/evaluation/generate_retrieval_benchmark_step1_v3_llm.py` thay lõi sinh câu bằng LLM.
Đầu ra: `data/eval/retrieval_benchmark_step1_raw_v3.jsonl` cùng schema cũ (để Step 2/3 dùng lại được).

## 2. GIỮ NGUYÊN (tái dùng từ v2, import lại, đừng viết lại)

Từ `generate_retrieval_benchmark_step1_v2.py`, import và dùng lại nguyên:
- `select_seeds(chunks, max_chars, target_total)` — đã phủ đủ 185 bài + cân book×grade. **Không sửa.**
- `build_seed_content`, `lesson_key`, `LessonKey`, `compact`, `normalize`.
- Toàn bộ logic chọn seed, coverage, balancing.

CHỈ thay phần (seed, seed_content) → câu hỏi: bỏ `choose_question`, `extract_anchors`, `expected_answer` tất định.

## 3. LLM client (dùng đúng pattern đã có trong repo)

Tham chiếu `src/rag/context_builder.py:14-16, 43-51` để biết cách khởi tạo client và gọi:
- Dùng `google.genai` client, `model = settings.LLM_MODEL`, key `settings.GENAI_API_KEY` (đã có sẵn, **không hardcode**).
- `temperature ≈ 0.3` (ổn định + đa dạng vừa phải), `top_p ≈ 0.9`.
- Ép JSON: ưu tiên `response_mime_type="application/json"` (+ `response_schema` nếu SDK bản này hỗ trợ).
  Nếu không, parse thủ công có strip ```` ```json ```` fence.

## 4. Luồng

```
load chunks → select_seeds(...) → (optional slice theo --limit/--offset)
for each seed:
    nếu có trong cache (key = seed_chunk_id + prompt_version) → lấy lại
    else: build prompt → gọi LLM → parse JSON → validate (mục 6) → cache
    map mỗi câu hợp lệ thành 1 row (mục 7), ghi jsonl
in report: rows, seeds_done, seeds_failed, by_group, by_type, covered_lessons
```

- **Cache** JSON tại `data/eval/_step1_v3_cache.json` (giống `data/chunk_type_cache.json`):
  key `"<seed_chunk_id>@<prompt_version>"` → list câu hỏi. Cho phép chạy lại không tốn LLM.
- **Retry**: parse/JSON lỗi → thử lại tối đa 2 lần; vẫn lỗi → skip seed, log vào `seeds_failed`, KHÔNG crash.
- **Idempotent**: chạy lại cho kết quả như cũ (nhờ cache + temperature thấp). Ghi đè output.

## 5. Bộ sinh câu hỏi — YÊU CẦU (codex tự soạn prompt LLM sao cho thỏa hết các điều kiện dưới)

> Đây là **chỉ dẫn**, không phải prompt mẫu. Codex tự viết prompt tiếng Việt, nhưng prompt đó BẮT BUỘC
> truyền vào `book, grade, topic_name, lesson_name, seed_content` và ép LLM tuân thủ A–F. Sinh `N` câu/seed (mặc định 2).

**A. Đúng & bám nguồn.** Câu hỏi phải trả lời được CHỈ bằng `seed_content`; cấm bịa thông tin ngoài đoạn.

**B. Discriminative — điều kiện cốt lõi.** Mỗi câu phải chứa ít nhất một thuật ngữ/khái niệm/cú pháp/tên riêng
**cụ thể** có trong đoạn, đủ riêng để KHÔNG trả lời được bởi bài khác.
- Ưu tiên từ khóa riêng của bài: vd "câu lệnh `while`", "hàm `math.gcd()`", "bảng mã TCVN3",
  "phép toán `//` và `%`", "khoá công khai", "kiểu dữ liệu danh sách (list)".
- Tránh từ chung chung khi đứng một mình: "máy tính", "dữ liệu", "thông tin", "file", "Python", "chương trình"
  — chỉ dùng nếu đã gắn ngữ cảnh riêng của bài.

**C. Self-contained.** Đọc câu hỏi không cần nhìn đoạn. Cấm tham chiếu mơ hồ: "bài này", "đoạn trên",
"ví dụ trên", "nội dung trên", "ở trên", "nó".

**D. Tự nhiên, không khuôn.** Kết thúc bằng "?". Cấm tuyệt đối 5 khuôn template ở mục 0 và mọi biến thể của chúng.

**E. Đa dạng.** `N` câu khác nhau về nội dung lẫn cách hỏi; trải đều các `question_type`.

**F. Few-shot.** Prompt nên nhúng ít nhất 1 ví dụ TỐT và 1 ví dụ XẤU để LLM bắt chước/né.
Gợi ý ví dụ (codex chỉnh lại cho hợp): với bài "BIẾN, PHÉP GÁN VÀ BIỂU THỨC SỐ HỌC":
- Tốt: "Trong Python, hai kí hiệu `//` và `%` thực hiện phép toán số học nào?"
- Xấu: "Trừ có vai trò gì trong ví dụ hoặc yêu cầu được nêu?" (template + anchor rác).

**Hợp đồng đầu ra (output contract).** LLM trả về JSON — mảng `N` object, mỗi object đúng các field:
`question` (str, kết thúc "?"), `question_type` ∈ {definition, process, list, application, compare, fact},
`difficulty` ∈ {easy, medium, hard}, `expected_answer` (1–3 câu lấy từ đoạn), `anchor` (thuật ngữ cụ thể câu xoáy vào),
`distinctive_terms` (list từ khóa riêng của bài). Không kèm markdown/giải thích.

## 6. Validate mỗi câu LLM trả về (rẻ, deterministic — chạy ngay sau parse)

Loại câu nếu:
- Không kết thúc bằng `?` hoặc độ dài < 18 ký tự.
- Khớp regex 5 khuôn template ở mục 0 (chuẩn hóa bỏ dấu rồi match) — phòng LLM lỡ tạo.
- Chứa từ mơ hồ: `bài này | đoạn trên | ví dụ trên | ở trên | nó | nội dung trên`.
- `anchor` rỗng, hoặc `anchor`/`distinctive_terms` KHÔNG xuất hiện trong `seed_content` (normalize rồi check substring).
- `expected_answer` overlap token với `seed_content` < 0.5.
- Trùng (normalize question) với câu đã giữ.

Seed nào sau validate còn < 1 câu → ghi `seeds_failed`, bỏ qua (bù ở quarter sau / lần chạy sau).

## 7. Schema row ghi ra (GIỮ ĐÚNG để Step 2/3 chạy được)

```json
{
  "id": "V3-0001",
  "seed_chunk_id": "<uuid>",
  "source_level": 2,
  "question": "...",
  "question_type": "definition",
  "difficulty": "easy",
  "expected_answer": "...",
  "anchor": "...",
  "distinctive_terms": ["..."],
  "seed_content": "<full seed_content>",
  "seed_content_sha1": "<sha1>",
  "gold_lesson_key": {"book","grade","topic_name","lesson","lesson_name"},
  "gen_meta": {"generator":"gemini","prompt_version":"step1_v3_llm_discriminative","stage":"raw_generation"}
}
```

## 8. CLI args

```
--chunks            data/rag_chunks_v2.json
--output            data/eval/retrieval_benchmark_step1_raw_v3.jsonl
--target-seeds      300
--questions-per-seed 2
--max-seed-chars    2500
--limit             0      # >0: chỉ xử lý N seed đầu (để chạy thử 1/4)
--offset            0      # bỏ qua N seed đầu (chạy tiếp quarter sau)
--model             (mặc định settings.LLM_MODEL)
--temperature       0.3
--cache             data/eval/_step1_v3_cache.json
```

## 9. Chạy thử 1/4 trước (quan trọng)

`select_seeds` trả 300 seed. Chạy quarter đầu để review chất lượng trước khi đốt LLM cho cả 300:

```
venv/bin/python src/evaluation/generate_retrieval_benchmark_step1_v3_llm.py --limit 75 \
    --output data/eval/retrieval_benchmark_step1_raw_v3_q1.jsonl
```

Sau khi review OK, chạy full (cache giữ lại quarter 1, chỉ gọi LLM cho phần còn lại):

```
venv/bin/python src/evaluation/generate_retrieval_benchmark_step1_v3_llm.py \
    --output data/eval/retrieval_benchmark_step1_raw_v3.jsonl
```

## 10. Tiêu chí nghiệm thu (self-check sau khi chạy quarter 1)

- 0% câu khớp 5 khuôn template (grep kiểm tra).
- ≥ 95% câu có `anchor` nằm trong `seed_content`.
- Mỗi câu kết thúc bằng `?`, ≥ 18 ký tự, không chứa từ mơ hồ.
- Đa dạng `question_type` (không dồn 1 loại > 60%).
- Đọc tay 20 câu ngẫu nhiên: phải tự nhiên + đoán được đúng bài chỉ từ câu hỏi.

## 11. Điều chỉnh Step 2 & Step 3 cho khớp (làm sau, ghi chú để không quên)

- **Step 2** (`filter_retrieval_benchmark_step2.py`): GIỮ dedup + title_leak. BỎ/nới filter `template` và
  `anchor_missing` (giờ LLM kiểm soát chất lượng; validate ở mục 6 đã lo).
- **Step 3** (`validate_retrieval_benchmark_step3.py`): THÊM **cổng discriminative bằng LLM** (khâu đang thiếu).
  Với mỗi câu, đưa cho LLM **chỉ câu hỏi** + danh sách 185 `lesson_name` (gom theo book-grade), hỏi
  "câu này trỏ đúng bài nào? mức độ duy nhất?". LOẠI nếu bài LLM đoán ≠ gold, hoặc không đủ duy nhất.
  Bản rẻ hơn: chỉ so gold với các bài cùng `topic_name`/cùng book-grade. Đây mới là filter đúng cho eval retrieval.
- Đổi đường dẫn output Step 3 sang hậu tố `_v3` để khỏi đè bản v1.
```
