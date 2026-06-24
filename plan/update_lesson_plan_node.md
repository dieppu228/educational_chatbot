# Plan: Nâng cấp sinh GIÁO ÁN (lesson_plan) thoát khỏi tư duy slide
> **Mục tiêu**: Giáo án sinh ra phải là *kịch bản dạy học giáo viên dùng được ngay*
> (nội dung chi tiết từng đề mục, hoạt động GV/HS, câu hỏi gợi mở, dự kiến trả lời,
> ví dụ, sai lầm thường gặp, cách chốt) — KHÔNG còn là slide gắn nhãn "giáo án".
> **Trạng thái đã verify trong code** (không phải suy đoán):
> - Prompt `LESSON_PLAN_CONTENT_PROMPT` ([prompts.py:803](src/llm/prompts.py)) ép bullets/notes, cap 6 bullet / 30 từ / notes 200 từ.
> - `ContentAgent` hard cap `bullets[:6]` ([content_agent.py:124](src/llm/handlers/content/slide_agents/content_agent.py)) — KHÔNG branch theo task_type.
> - Schema cũng cap: `ContentSlide.bullets max_length=6`, `notes max_length=600` ([slide_schemas.py:149-150](src/schemas/slide_schemas.py)).
> - Formatter cắt `notes[:150]` ([slide_service.py:491](src/llm/services/slide_service.py)).
> - Outline lesson_plan vẫn dùng `slides/slide_id/slide_type/key_points` ([prompts.py:760-788](src/llm/prompts.py)).
---
## 0. Nguyên tắc thiết kế
- **Hướng (A) — Additive, KHÔNG tách pipeline.** Giữ nguyên graph, ContentAgent, SlideMerger,
  export service dùng chung; chỉ **thêm field optional** cho nhánh lesson_plan và **branch theo
  `task_type`** ở các điểm cap/parse/render. Lý do: ripple nhỏ nhất, không phá luồng slide đang chạy,
  và giữ được luận điểm "tái dùng kiến trúc qua `task_type`" của Chương 3 (task_type giờ phân hoá
  *độ sâu output thật sự*, không chỉ là nhãn).
- **Hợp đồng dùng chung là rủi ro chính.** `bullets/notes` bị tiêu thụ ở 5 nơi (xem mục 1). Mọi field
  mới phải được thread qua **ContentAgent → ContentSlide → SlideMerger → MergedSlide → export/formatter**,
  nếu không sẽ bị drop ở merge và "export chỉ ra outline".
- **Giữ grounding.** Mọi đề mục giữ `source_chunk_ids` (đừng bỏ) — đây là điểm tựa cho luận văn.
- **Regression luồng slide sau mỗi bước** vì dùng chung component.
---
## 1. Bản đồ "hợp đồng dùng chung" cần đụng tới
| File | Dòng | Vai trò với bullets/notes | Phải sửa? |
|---|---|---|---|
| `src/llm/prompts.py` | 803 (content), 760-788 (outline) | prompt ép bullets/notes/cap | ✅ |
| `src/schemas/slide_schemas.py` | 128-134 (OutlineSlide), 146-151 (ContentSlide), 180-188 (MergedSlide) | cap + thiếu field giáo án | ✅ |
| `src/llm/handlers/content/slide_agents/content_agent.py` | 124 (`[:6]`) | cap + parse | ✅ branch task_type |
| `src/llm/services/slide_merger.py` | 112-113 | map content → MergedSlide | ✅ map field mới |
| `src/llm/services/slide_export_service.py` | 62,134,146,150 | render HTML export | ✅ render field mới |
| `src/llm/services/slide_service.py` | 487-491 (`notes[:150]`) | display text | ✅ bỏ cắt |
| `src/llm/services/quality_reviewer.py` | 122-123 + `LESSON_PLAN_QUALITY_REVIEW_PROMPT` | reviewer đã có sẵn | ✅ chỉ sửa prompt |
| `src/config/config.py` | `RERANKER_TOP_N_LESSON_PLAN=10` | context cho giáo án | ✅ tăng 18-20 |
| HITL resume outline (`slide_service.resume_outline`) | — | truyền field outline mới | ⚠️  kiểm tra không strip |
---
## 2. Schema mới (additive — field optional)
### 2.1. Outline giáo án → "tiến trình dạy học" (`OutlineSlide` thêm field optional)
Giữ `slide_id/slide_type/title/key_points/source_chunk_ids`, **thêm** (optional, chỉ lesson_plan dùng):
```python
duration_minutes: Optional[int] = None      # thời lượng phần
teaching_goal: Optional[str] = None         # mục tiêu dạy học của phần
knowledge_units: List[str] = []             # các đề mục nhỏ theo SGK (chia nhỏ, KHÔNG gom)
activity_type: Optional[str] = None         # khoi_dong | hinh_thanh | luyen_tap | van_dung | danh_gia
```
> Lưu ý: yêu cầu outline chia "Hình thành kiến thức" thành **nhiều `knowledge_units`** theo SGK,
> mỗi unit về sau thành một mục `content_detail` ở bước content.
### 2.2. Content giáo án → section chi tiết (`ContentSlide` thêm field optional + nới cap)
Giữ `bullets/notes` cho tương thích slide; **thêm** field giàu cho giáo án:
```python
# nới cap: bỏ max_length=6 / 600 cho nhánh lesson_plan (xem mục 3.2)
duration_minutes: Optional[int] = None
objectives: List[str] = []
teacher_activities: List[str] = []
student_activities: List[str] = []
content_detail: List[ContentDetailItem] = []   # cốt lõi — kịch bản dạy
assessment: List[str] = []
transition: Optional[str] = None
class ContentDetailItem(BaseModel):
    heading: str                         # "1. Khái niệm thông tin"
    explanation: str                     # nội dung kiến thức chi tiết
    example: Optional[str] = None        # ví dụ minh họa
    teacher_prompt: Optional[str] = None # câu hỏi gợi mở của GV
    expected_student_response: Optional[str] = None  # dự kiến HS trả lời
    common_mistake: Optional[str] = None # sai lầm thường gặp
    wrap_up: Optional[str] = None        # cách chốt kiến thức
    source_chunk_ids: List[str] = []     # căn cứ SGK
```
### 2.3. `MergedSlide` thêm các field trên (optional) để không bị drop ở merge
Thêm vào `MergedSlide`: `duration_minutes, objectives, teacher_activities, student_activities,
content_detail, assessment, transition`. Slide không set → mặc định rỗng, không ảnh hưởng.
---
## 3. Thay đổi theo file (chi tiết)
### 3.1. `prompts.py`
- **`LESSON_PLAN_CONTENT_PROMPT`**: viết lại hoàn toàn theo schema section ở 2.2. Mỗi `content_detail`
  item bắt buộc: nội dung chi tiết, câu hỏi gợi mở GV, dự kiến trả lời HS, ví dụ, sai lầm thường gặp,
  cách chốt, `source_chunk_ids`. Bỏ luật "tối đa 6 bullet/30 từ/notes 200 từ". Trả JSON theo schema mới.
- **`LESSON_PLAN_OUTLINE_PROMPT`**: thêm yêu cầu sinh `duration_minutes/teaching_goal/knowledge_units/
  activity_type`; ép chia "Hình thành kiến thức" thành nhiều `knowledge_units` theo đề mục SGK.
- **`LESSON_PLAN_QUALITY_REVIEW_PROMPT`**: thêm tiêu chí FAIL (mục 3.5).
### 3.2. `slide_schemas.py`
- Thêm `ContentDetailItem`.
- `OutlineSlide`, `ContentSlide`, `MergedSlide`: thêm field optional (2.1-2.3).
- **Nới cap**: bỏ `max_length=6`/`max_length=600` trên `ContentSlide` (vì slide cap đã enforce ở
  ContentAgent theo task_type — xem 3.3); hoặc nâng giới hạn đủ lớn. Giữ validation nhẹ để không vỡ slide.
### 3.3. `content_agent.py`
- Dòng 124: **branch theo `task_type`** — slide vẫn `bullets[:6]`; lesson_plan KHÔNG cap, thay vào đó
  parse các field mới (`content_detail`, `teacher_activities`, ...) từ JSON trả về và đưa vào result.
- `_fallback_from_outline`: bổ sung fallback cho lesson_plan (đổ `knowledge_units` thành content_detail rỗng-có-heading) để khi 1 section fail vẫn không mất cấu trúc.
### 3.4. `slide_merger.py` (BƯỚC THEN CHỐT — đừng bỏ)
- Dòng 112-113: ngoài `bullets/notes`, **map toàn bộ field mới** từ `content_data` sang `MergedSlide`
  (`content_detail, teacher_activities, student_activities, objectives, assessment, transition,
  duration_minutes`). Nếu không làm bước này, prompt tốt mấy cũng bị drop ở đây.
### 3.5. `slide_export_service.py` + `slide_service.py` (formatter)
- `slide_export_service` (62,134,146,150): với section có `content_detail`, render khối chi tiết
  (heading → explanation → ví dụ → câu hỏi GV → dự kiến HS → sai lầm → chốt) thay vì chỉ bullets.
  Slide giữ nguyên path bullets/key_points.
- `slide_service._format_lesson_plan_display` (474-495): **bỏ `notes[:150]`**, render theo field mới
  (hoặc full notes nếu section kiểu cũ). Đây là chỗ làm "thấy được" kết quả khi test UI.
### 3.6. `quality_reviewer.py` — `LESSON_PLAN_QUALITY_REVIEW_PROMPT`
Thêm tiêu chí **FAIL** nếu: mỗi phần chỉ có bullet ngắn; thiếu hoạt động GV/HS; thiếu `content_detail`
chi tiết từng đề mục; thiếu ví dụ / câu hỏi gợi mở / đánh giá; "Hình thành kiến thức" gom thành vài bullet.
### 3.7. `config.py`
- `RERANKER_TOP_N_LESSON_PLAN`: 10 → **18-20** (không quá tay; ContentAgent vẫn viết theo
  `source_chunk_ids` của từng section). Kiểm tra token budget trong ContextBuilder không tràn.
### 3.8. HITL resume
- Kiểm tra `slide_service.resume_outline` truyền nguyên outline (gồm field mới) khi resume, không strip.
---
## 4. Lộ trình thực hiện (theo thứ tự an toàn)
1. **Schema** (`slide_schemas.py`): thêm `ContentDetailItem` + field optional + nới cap. → compile.
2. **Prompt** content + outline lesson_plan (`prompts.py`). → compile.
3. **ContentAgent**: branch task_type, parse field mới, bỏ cap cho lesson_plan. → unit test parse.
4. **🔴 SlideMerger**: map field mới vào MergedSlide. → test merge giữ field.
5. **Export + formatter**: render content_detail; bỏ `notes[:150]`. → **test export thấy nội dung chi tiết**.
6. **config**: tăng top_n lesson_plan.
7. **Quality reviewer prompt**: thêm tiêu chí FAIL.
8. **Regression luồng slide** (mục 5) + chạy thật 1 giáo án end-to-end.
> Nguyên tắc: làm 1→5 trước rồi test end-to-end một giáo án thật ngay (đừng để dồn). Bước 4-5 quyết định
> kết quả có hiển thị/export được không.
  - (A) Additive — tao nghiêng về cái này: giữ MergedSlide, thêm field optional (content_detail, teacher_activities, duration_minutes...). Slide bỏ qua, lesson_plan dùng. Ripple nhỏ nhất, không phá luồng slide đang chạy.
  - (B) Tách hẳn LessonPlanSection + merger riêng + export riêng. Sạch về mặt mô hình (đúng như mày viết "tách giáo án khỏi cấu trúc slide") nhưng đụng nhiều file, dễ vỡ luồng slide, phải regression test kỹ.

  Với mục tiêu đồ án + thời gian, tao khuyên (A): vừa đạt được "giáo án sâu hơn slide", vừa giữ luận điểm "tái dùng kiến trúc qua task_type" (điểm mạnh ở Chương 3) — task_type giờ phân hoá độ sâu output thật sự, không chỉ là nhãn.

  Vài cảnh báo nhỏ

  - RERANKER_TOP_N_LESSON_PLAN 10→18-25: hợp lý nhưng đừng quá tay — ContentAgent viết theo từng section chỉ dùng source_chunk_ids của section đó (outline đã phân bổ chunk). Tăng top_n giúp outline có nhiều chunk để chia, nhưng nhớ check
  token budget trong ContextBuilder. Tao đề xuất 18-20.
  - Outline thêm field (duration_minutes, knowledge_units...): an toàn (thêm field không phá), nhưng HITL resume phải truyền field mới qua — check resume_outline không strip chúng.
  - Sau khi sửa, bắt buộc regression test luồng slide (vì dùng chung ContentAgent/merger/export) để chắc không vỡ.

  Verdict

  Plan tốt, chẩn đoán chính xác, schema section đề xuất hợp sư phạm. Chỉ cần thêm bước 3 (MergedSlide+merger+export) và chốt hướng (A) additive là đủ chắc để làm. Đừng tin "chỉ sửa prompt là xong" — cái contract dùng chung mới là thứ
  quyết định.
