# Plan viết lại đồ án theo hướng nghiên cứu giải pháp

## 0. Trạng thái hiện tại của bản thảo

Cập nhật theo nội dung LaTeX hiện tại:

| Phần | Trạng thái | Ghi chú |
|---|---|---|
| Chương 2 | Đã viết lại xong bản đầu | Đã theo đúng bốn mục: Phạm vi nghiên cứu, Tổng quan về bài toán, Khảo sát các giải pháp liên quan, Cơ sở lý thuyết và hướng tiếp cận. |
| Chương 3.1 | Đã viết | Tổng quan kiến trúc hệ thống, bài toán/yêu cầu, kiến trúc tổng thể và công nghệ nền. |
| Chương 3.2 | Đã viết | Nền tảng tri thức: nguồn SGK, metadata, chunking theo tiêu đề, embedding và Qdrant. |
| Chương 3.3 | Đã viết | RAG core: BM25/dense retrieval, RRF, reranking bằng cross-encoder và Adaptive RAG. |
| Chương 3.4 | Đã viết | Tầng điều phối tác tử: intent routing, context analysis, query rewriting, action planning và execution loop. |
| Chương 3.5 | Chưa viết xong | Đang là skeleton cho tầng sinh nội dung đa tác tử. |
| Chương 3.6 | Chưa viết xong | Đang là skeleton cho phương pháp đánh giá retrieval/generation. |
| Chương 4 trở đi | Chưa cập nhật theo bản research mới | Giữ plan hiện tại, sẽ chỉnh sau khi chốt Chương 3 và kết quả rerank. |

## 1. Mục tiêu tái tổ chức nội dung

Đồ án cần được viết theo hướng nghiên cứu và đánh giá giải pháp chatbot giáo dục dựa trên RAG, thay vì trình bày như một tài liệu thiết kế web app. Trục nội dung chính của báo cáo là:

```text
Bài toán hỏi đáp trên tài liệu giáo dục
  -> Khó khăn trong truy xuất ngữ cảnh và sinh câu trả lời có căn cứ
  -> Cơ sở lý thuyết và khảo sát giải pháp liên quan
  -> Đề xuất pipeline RAG/adaptive retrieval cho dữ liệu SGK Tin học
  -> Thiết kế chi tiết từng node và phương pháp đánh giá
  -> Cài đặt, kiểm thử, thực nghiệm và phân tích lỗi
  -> Kết luận và hướng phát triển
```

Các phần về package, API, frontend, backend, session, trace và deployment vẫn cần xuất hiện, nhưng chỉ giữ vai trò chứng minh giải pháp đã được cài đặt và có thể kiểm thử. Không để phần thiết kế phần mềm lấn át phần nghiên cứu retrieval, generation và evaluation.

## 2. Nguyên tắc viết lại

- Chương 2 trả lời câu hỏi: vì sao cần hướng RAG/adaptive retrieval cho chatbot giáo dục.
- Chương 3 trả lời câu hỏi: giải pháp được thiết kế như thế nào và các node trọng tâm được đánh giá ra sao.
- Chương 4 trả lời câu hỏi: giải pháp đã được cài đặt, kiểm thử và cho kết quả thực nghiệm như thế nào.
- Chương 5 tổng kết đóng góp, kết quả đạt được và hạn chế.
- Chương 6 trình bày hướng phát triển tiếp theo.
- Không viết chương 3 như tài liệu mô tả package thuần túy.
- Không biến chương 4 thành hướng dẫn chạy app.
- Mỗi chương cần có phần Tổng quan và Kết chương.
- Mỗi mục nên có vai trò rõ ràng trong lập luận chung của đồ án.

## 3. Narrative nghiên cứu đề xuất

Đoạn định hướng có thể dùng xuyên suốt báo cáo:

```text
Đồ án nghiên cứu và xây dựng một trợ lý giáo dục thông minh cho môn Tin học THPT dựa trên kiến trúc Retrieval-Augmented Generation. Trọng tâm của đồ án là thiết kế pipeline truy xuất ngữ cảnh từ SGK, sinh câu trả lời dựa trên tài liệu, và đánh giá chất lượng của từng thành phần trong pipeline, đặc biệt là các bước retrieval và generation.
```

Các đóng góp chính nên được nhấn mạnh:

- Xây dựng pipeline hỏi đáp trên dữ liệu SGK Tin học THPT.
- Thiết kế cơ chế xử lý tài liệu, chunking, embedding, retrieval, reranking và generation.
- Tổ chức đánh giá riêng cho retrieval và generation, trong đó retrieval ưu tiên đánh giá tự động còn generation ưu tiên đánh giá thủ công bằng rubric.
- So sánh chất lượng giữa các cấu hình truy xuất hoặc các service liên quan nếu có dữ liệu thực nghiệm.
- Phân tích lỗi để chỉ ra nguyên nhân ảnh hưởng đến chất lượng câu trả lời.

## 4. Chương 2: Tổng quan và cơ sở nghiên cứu

Trạng thái: **đã viết lại xong bản đầu trong `latex/Chuong/2_Khao_sat.tex`**. Nội dung hiện tại đã theo đúng bốn đầu mục chính dưới đây. Các ghi chú trong mục này được giữ lại để phục vụ rà soát văn phong, bổ sung citation nếu cần và kiểm tra sự liên kết với Chương 3.

### 4.1. Mục tiêu chương

Chương 2 cần đặt nền tảng cho hướng nghiên cứu. Sau chương này, người đọc phải hiểu:

- Phạm vi và trọng tâm nghiên cứu của đồ án là gì.
- Bài toán chatbot giáo dục có đặc thù gì.
- Các hướng giải pháp hiện có trên thị trường và trong kỹ thuật có ưu nhược điểm gì.
- Vì sao LLM trực tiếp chưa đủ cho dữ liệu SGK và RAG giải quyết vấn đề nào.
- Đồ án đề xuất giải pháp nào và giải pháp đó lấp khoảng trống nào.

### 4.2. Cấu trúc chương: 4 đầu mục chính

Chương 2 được tổ chức theo **4 đầu mục chính**, đánh số 2.1 đến 2.4:

| Đầu mục | Tên | Vai trò |
|---|---|---|
| 2.1 | Phạm vi nghiên cứu | Khoanh vùng đối tượng, ranh giới và trọng tâm nghiên cứu |
| 2.2 | Tổng quan về bài toán | Bối cảnh, đặc thù dữ liệu và yêu cầu của bài toán hỏi đáp giáo dục |
| 2.3 | Khảo sát các giải pháp liên quan | Phân tích đối thủ, thị trường và các hướng kỹ thuật hiện có |
| 2.4 | Cơ sở lý thuyết và hướng tiếp cận | Nền tảng kỹ thuật (LLM, embedding, RAG, adaptive retrieval, evaluation) và khoảng trống đồ án giải quyết |

---

### 2.1. Phạm vi nghiên cứu

Trạng thái: **đã viết**.

Mục này khoanh vùng rõ đồ án nghiên cứu cái gì và không nghiên cứu cái gì, để định hướng toàn bộ các chương sau.

Nội dung cần viết:

- **Đối tượng nghiên cứu:** hệ thống hỏi đáp (document-grounded QA) trên dữ liệu SGK Tin học THPT, dựa trên kiến trúc Retrieval-Augmented Generation.
- **Phạm vi dữ liệu:** SGK Tin học lớp 10-12, bộ Cánh Diều (CD) và Kết Nối Tri Thức (KNTT).
- **Đối tượng sử dụng:** học sinh, giáo viên và người tự học môn Tin học THPT.
- **Trọng tâm nghiên cứu:** thiết kế và đánh giá pipeline retrieval và generation; trong đó retrieval là phần đánh giá định lượng chính, generation đánh giá bằng rubric thủ công.
- **Ngoài phạm vi (giới hạn rõ):**
  - không đi sâu thiết kế UI/frontend như một sản phẩm thương mại;
  - không tập trung tối ưu hạ tầng triển khai/DevOps;
  - các tác vụ phụ (quiz, slide, giáo án) chỉ trình bày ở mức điều phối, không phải trọng tâm đánh giá;
  - graph/hybrid retrieval chỉ coi là hướng mở rộng nếu chưa có thực nghiệm đầy đủ.
- **Câu hỏi nghiên cứu chính:** làm sao truy xuất đúng ngữ cảnh từ SGK và sinh câu trả lời bám tài liệu, đồng thời đánh giá được chất lượng của từng bước.

Điểm cần tránh: không mô tả frontend, API, login hoặc các tính năng web app ở phần này.

---

### 2.2. Tổng quan về bài toán

Trạng thái: **đã viết**.

Mục này trình bày bối cảnh và đặc thù của bài toán hỏi đáp trên tài liệu giáo dục, làm rõ vì sao đây là một bài toán đáng nghiên cứu.

#### 2.2.1. Bài toán chatbot giáo dục

Nội dung cần viết:

- Bối cảnh ứng dụng chatbot trong giáo dục.
- Nhu cầu hỏi đáp tự nhiên trên tài liệu học tập.
- Đặc điểm dữ liệu SGK Tin học THPT: phân theo lớp, bộ sách, chủ đề, bài học.
- Đối tượng sử dụng: học sinh, giáo viên, người tự học.
- Các yêu cầu của hệ thống:
  - trả lời đúng theo tài liệu;
  - truy xuất được ngữ cảnh liên quan;
  - giảm câu trả lời không có căn cứ;
  - hỗ trợ nhiều dạng yêu cầu học tập;
  - có thể mở rộng khi bổ sung tài liệu.

Điểm cần tránh: không mô tả frontend, API, login hoặc các tính năng web app ở phần này.

#### 2.2.2. Hệ thống hỏi đáp dựa trên tài liệu

Nội dung cần viết:

- Khái niệm Question Answering.
- Phân biệt closed-book QA và open-book/document-grounded QA.
- Luồng cơ bản của hệ thống hỏi đáp dựa trên tài liệu:
  - nhận câu hỏi;
  - phân tích ý định hoặc phạm vi;
  - truy xuất tài liệu/ngữ cảnh;
  - tổng hợp câu trả lời;
  - trả câu trả lời kèm nguồn nếu có.
- Lý do đồ án thuộc nhóm document-grounded QA.

#### 2.2.3. Thách thức đặc thù của dữ liệu SGK Tin học

Nội dung cần viết:

- Nội dung dài, phân cấp nhiều tầng (bộ sách > lớp > chủ đề > bài > mục).
- Cùng một chủ đề xuất hiện ở nhiều lớp/bộ sách, dễ gây nhầm phạm vi.
- Thuật ngữ tiếng Việt chuyên ngành Tin học, cần embedding tiếng Việt phù hợp.
- Một bài học gồm cả lý thuyết, ví dụ và bài tập với vai trò khác nhau.
- Hệ quả: cần cơ chế truy xuất có xét phạm vi và đánh giá tách bạch retrieval/generation.

---

### 2.3. Khảo sát các giải pháp liên quan

Trạng thái: **đã viết**.

Mục này phân tích các hướng giải pháp hiện có trên thị trường và trong kỹ thuật, chỉ ra ưu/nhược điểm của từng nhóm để định vị giải pháp của đồ án.

#### 2.3.1. Các nhóm giải pháp hiện có

Nội dung cần viết:

- Nhóm chatbot rule-based.
- Nhóm FAQ/keyword search.
- Nhóm semantic search.
- Nhóm chatbot gọi LLM trực tiếp.
- Nhóm RAG chatbot.
- Nhóm hybrid/adaptive RAG nếu có khảo sát.

#### 2.3.2. Bảng so sánh các nhóm giải pháp

Bảng so sánh nên có các tiêu chí:

| Nhóm giải pháp | Hiểu câu hỏi tự nhiên | Dùng dữ liệu riêng | Giảm hallucination | Khả năng mở rộng | Phù hợp với SGK |
|---|---|---|---|---|---|
| Rule-based | Thấp | Trung bình | Cao nếu luật đủ | Thấp | Thấp |
| FAQ/keyword search | Thấp-Trung bình | Có | Trung bình | Trung bình | Trung bình |
| LLM trực tiếp | Cao | Thấp nếu không nạp context | Thấp | Cao | Thấp-Trung bình |
| RAG | Cao | Cao | Trung bình-Cao | Cao | Cao |
| Adaptive/hybrid RAG | Cao | Cao | Cao hơn nếu retrieval tốt | Trung bình-Cao | Cao |

#### 2.3.3. Nhận xét và định vị giải pháp đồ án

Nội dung cần viết:

- Các giải pháp đơn giản (rule-based, FAQ) không hiểu câu hỏi tự nhiên và khó mở rộng.
- LLM trực tiếp mạnh về ngôn ngữ nhưng yếu về dữ liệu riêng và dễ hallucination.
- RAG là hướng phù hợp nhất với dữ liệu SGK, nhưng các triển khai hiện có thường chưa đánh giá tách bạch retrieval/generation.
- Đồ án định vị ở nhóm **adaptive/hybrid RAG** có xét phạm vi sách/lớp/chủ đề và có quy trình đánh giá riêng cho từng bước.

---

### 2.4. Cơ sở lý thuyết và hướng tiếp cận

Trạng thái: **đã viết**.

Đây là phần *tự do*, trình bày các nền tảng kỹ thuật cần thiết để hiểu giải pháp, kết thúc bằng khoảng trống và đề xuất của đồ án. Các kiến thức ở đây được rút ngược từ thiết kế chương 3.

#### 2.4.1. Large Language Model và hạn chế khi dùng trực tiếp

Nội dung cần viết:

- Khái niệm LLM và khả năng sinh ngôn ngữ tự nhiên.
- Vai trò của prompt trong sinh câu trả lời.
- Các hạn chế khi dùng LLM trực tiếp:
  - không biết dữ liệu SGK nội bộ nếu không được cung cấp;
  - dễ sinh thông tin sai hoặc không có căn cứ;
  - khó cập nhật tri thức theo tài liệu mới;
  - bị giới hạn bởi context window;
  - khó kiểm chứng nguồn câu trả lời.

Kết luận cần đạt: cần một cơ chế cung cấp ngữ cảnh đáng tin cậy trước khi sinh câu trả lời.

#### 2.4.2. Embedding và tìm kiếm ngữ nghĩa

Nội dung cần viết:

- Khái niệm embedding.
- Cách biểu diễn câu hỏi và đoạn tài liệu thành vector.
- Similarity search và vai trò của vector database/index.
- Các độ đo tương đồng thường gặp: cosine similarity, dot product, Euclidean distance.
- Ý nghĩa trong đồ án: truy xuất các chunk SGK có nội dung gần với câu hỏi.

Nếu muốn gắn với hiện trạng dự án, có thể nhắc ở mức tổng quan rằng hệ thống dùng embedding tiếng Việt phù hợp hơn với dữ liệu SGK tiếng Việt. Chi tiết model cụ thể nên để chương 4.

#### 2.4.3. Retrieval-Augmented Generation

Nội dung cần viết:

- Khái niệm RAG.
- Pipeline RAG cơ bản:
  - document ingestion;
  - preprocessing;
  - chunking;
  - embedding;
  - indexing;
  - retrieval;
  - reranking nếu có;
  - generation.
- Ưu điểm của RAG:
  - cập nhật tri thức dễ hơn fine-tuning;
  - giảm phụ thuộc vào tri thức tham số của LLM;
  - tăng khả năng trả lời dựa trên tài liệu;
  - hỗ trợ kiểm tra nguồn.
- Hạn chế:
  - retrieval sai dẫn tới generation sai;
  - chunking kém làm mất ngữ cảnh;
  - context nhiễu làm câu trả lời thiếu chính xác;
  - việc đánh giá cần tách riêng retrieval và generation.

#### 2.4.4. Adaptive retrieval, reranking và query rewriting

Nội dung cần viết:

- Lý do một truy vấn người dùng có thể mơ hồ hoặc thiếu ngữ cảnh.
- Query rewriting giúp mở rộng hoặc chuẩn hóa truy vấn như thế nào.
- Adaptive retrieval chọn chiến lược truy xuất theo phạm vi sách, lớp, chủ đề hoặc loại intent.
- Reranking giúp sắp xếp lại các đoạn candidate theo mức độ liên quan.
- Trade-off giữa chất lượng, latency và chi phí.

Phần này cần chuẩn bị nền cho các thành phần đang có trong dự án như ContextAnalyzer, QueryRewriter, AdaptiveRAGAgent, Reranker.

#### 2.4.5. Multi-intent và điều phối yêu cầu học tập

Nội dung cần viết vừa đủ:

- Người dùng không chỉ hỏi đáp mà còn có thể yêu cầu tạo quiz, giải thích, sinh slide hoặc giáo án.
- Cần có bước phân tích intent để định tuyến yêu cầu.
- Phân biệt rõ: đây là lớp điều phối hệ thống, không phải đóng góp nghiên cứu chính về retrieval.
- Liên hệ với hệ thống hiện tại: Orchestrator, IntentRouter, ActionPlanner và ExecutionDispatcher có vai trò điều phối pipeline.

#### 2.4.6. Đánh giá hệ thống RAG

Nội dung cần viết:

- Vì sao cần đánh giá riêng retrieval và generation.
- Vì sao không nên chỉ đánh giá câu trả lời cuối cùng: nếu câu trả lời sai thì cần biết lỗi đến từ truy xuất sai context hay từ LLM sinh sai trên context đúng.
- Retrieval metrics:
  - Hit Rate@k;
  - Recall@k;
  - Precision@k;
  - MRR;
  - nDCG nếu có nhãn mức độ liên quan.
- Generation metrics/rubric:
  - correctness;
  - relevance;
  - completeness;
  - faithfulness/groundedness;
  - clarity;
  - hallucination.
- Với generation, hướng đánh giá chính của đồ án là đánh giá thủ công bằng con người theo rubric. Không mặc định dùng LLM-as-judge vì làm tăng chi phí và có thể trùng vai trò với node validate đã có trong pipeline.
- System-level metrics:
  - latency;
  - cost nếu có;
  - tỷ lệ câu hỏi ngoài phạm vi được xử lý đúng;
  - khả năng truy vết lỗi qua log/debug.

#### 2.4.7. Khoảng trống và đề xuất giải pháp của đồ án

Nội dung cần viết:

- Các giải pháp hiện có thường chưa đánh giá rõ từng bước retrieval/generation.
- Với dữ liệu giáo dục, việc trả lời đúng chưa đủ; câu trả lời cần bám sát tài liệu.
- Cần một pipeline có khả năng:
  - truy xuất theo phạm vi sách/lớp/chủ đề;
  - kết hợp query rewriting hoặc adaptive retrieval;
  - rerank context trước khi sinh câu trả lời;
  - ghi log để phân tích lỗi;
  - đánh giá retrieval và generation bằng bộ câu hỏi kiểm thử.

Kết chương 2 cần dẫn sang chương 3: chương sau sẽ thiết kế chi tiết pipeline và phương pháp đánh giá.

## 5. Chương 3: Thiết kế giải pháp và phương pháp đánh giá

### 5.1. Mục tiêu chương

Chương 3 là chương trọng tâm về phương pháp đề xuất. Chương này cần trả lời câu hỏi hệ thống được thiết kế như thế nào để giải quyết bài toán hỏi đáp và sinh nội dung dựa trên SGK Tin học THPT. Nội dung chương không trình bày theo hướng liệt kê package phần mềm, mà tổ chức theo các tầng xử lý chính của giải pháp: kiến trúc tổng quan, nền tảng tri thức, RAG core, tầng điều phối tác tử, tầng sinh nội dung đa tác tử và phương pháp đánh giá.

Trạng thái hiện tại: các mục 3.1 đến 3.4 đã được viết vào LaTeX ở mức bản thảo đầu. Mục 3.5 và 3.6 hiện mới có skeleton, cần viết tiếp sau khi chốt nội dung multi-agent và kết quả đánh giá retrieval/generation.

Phạm vi đánh giá chính trong chương 3:

| Node | Vai trò trong evaluation | Cách đánh giá chính | Trạng thái |
|---|---|---|---|
| Retrieve | Node đánh giá định lượng chính | Chạy benchmark retrieval và so sánh metric | Đã có benchmark/script, cần viết mô tả vào 3.6 |
| Rerank | Node phụ nhưng quan trọng trong RAG core | So sánh trước/sau rerank | Chờ kết quả chạy đầy đủ với rerank |
| LLM generate | Node đánh giá chất lượng câu trả lời | Dùng kết quả RAGAS đã có và/hoặc rubric thủ công | Chưa viết vào 3.6 |
| Validate | Node hỗ trợ kiểm soát runtime | Mô tả cơ chế, không dùng làm evaluator chính | Chưa viết sâu |

### 5.2. Cấu trúc chương 3 hiện tại

Chương 3 trong LaTeX hiện được tổ chức theo 7 mục chính, đánh số 3.1 đến 3.7 nếu tính cả Kết chương:

| Mục | Tên trong LaTeX | Trạng thái | Vai trò |
|---|---|---|---|
| 3.1 | Tổng quan kiến trúc hệ thống | Đã viết | Giới thiệu bài toán, kiến trúc tổng thể, luồng xử lý và công nghệ nền. |
| 3.2 | Nền tảng tri thức: tiền xử lý, chunking và lập chỉ mục | Đã viết | Mô tả cách biến SGK thành kho chunk có metadata, embedding và chỉ mục Qdrant. |
| 3.3 | Cơ chế truy hồi ngữ cảnh (RAG core) | Đã viết | Trình bày keyword search/BM25, vector search, RRF, reranking và Adaptive RAG. |
| 3.4 | Tầng điều phối tác tử | Đã viết | Trình bày Orchestration Agent, intent routing, context analysis, query rewriting, action planning và execution loop. |
| 3.5 | Tầng sinh nội dung đa tác tử | Chưa viết xong | Cần mô tả content multi-agent cho slide/giáo án, supervisor-specialist, artifact và quality loop. |
| 3.6 | Phương pháp đánh giá | Chưa viết xong | Cần mô tả benchmark retrieval, metric, before/after rerank và đánh giá generation. |
| 3.7 | Kết chương | Chưa viết xong | Tổng kết các thành phần đã thiết kế và dẫn sang Chương 4. |

### 5.3. Nội dung đã viết xong trong Chương 3

#### 3.1. Tổng quan kiến trúc hệ thống

Trạng thái: **đã viết bản đầu**.

Nội dung đã khớp với bản thảo hiện tại:

- Bài toán và yêu cầu của hệ thống: chatbot Tin học THPT trên dữ liệu SGK CD/KNTT lớp 10-12, hỗ trợ hỏi đáp, sinh slide và soạn giáo án.
- Kiến trúc tổng thể theo hướng hai tầng: tầng điều phối tác tử và tầng sinh nội dung đa tác tử, vận hành trên nền RAG.
- Luồng xử lý một yêu cầu từ input người dùng đến phân tích context/intent, lập kế hoạch, gọi service, truy xuất tri thức, sinh nội dung, kiểm soát chất lượng và trả kết quả.
- Công nghệ nền được nêu ở mức phương pháp: LangGraph, Gemini, Qdrant, embedding model và reranker. Chi tiết cài đặt cụ thể sẽ để Chương 4.
- Đã có sơ đồ tổng quan kiến trúc hệ thống và phần mô tả sau hình.

Việc cần rà soát sau: cân chỉnh bố cục trang và bảo đảm mọi hình trong mục 3.1 đều được tham chiếu, mô tả bằng đoạn văn ngay trước/sau hình.

#### 3.2. Nền tảng tri thức: tiền xử lý, chunking và lập chỉ mục

Trạng thái: **đã viết bản đầu**.

Nội dung đã khớp với bản thảo hiện tại:

- Nguồn SGK, cấu trúc phân cấp và lược đồ metadata.
- Bảng phân bố chunk theo loại nội dung và bảng mô tả metadata.
- Quy trình tiền xử lý tài liệu và chunking theo heading.
- Ví dụ prototype về một document có nhiều mức heading và cách sinh chunk tương ứng.
- Biểu diễn vector tiếng Việt và lưu trữ Qdrant.
- Đã loại bỏ các mô tả về quan hệ cha-con nếu hệ thống không lưu tường minh, tránh viết những phần không triển khai.

Việc cần rà soát sau: nếu có số liệu chunk mới sau khi embedding lại full corpus, cần cập nhật bảng thống kê để khớp dữ liệu thực tế.

#### 3.3. Cơ chế truy hồi ngữ cảnh (RAG core)

Trạng thái: **đã viết bản đầu**.

Nội dung đã khớp với bản thảo hiện tại:

- Giải thích tìm kiếm từ khóa (keyword search) và tìm kiếm ngữ nghĩa theo vector (vector search), sau đó dùng thuật ngữ chuyên ngành BM25, dense retrieval và cosine similarity.
- Trình bày công thức TF, IDF, BM25, cosine similarity, RRF và score rerank.
- Mỗi công thức có nhãn tham chiếu và giải thích tham số theo dạng "Trong đó:".
- Trình bày cơ chế hợp nhất BM25 + dense bằng Reciprocal Rank Fusion.
- Trình bày reranking bằng cross-encoder và vai trò đưa breadcrumb vào cặp query-document.
- Mục Adaptive RAG đã đặt sơ đồ đúng vị trí và mô tả các strategy ở phần sau hình, tránh duplicate với phần tổng quan.

Việc cần rà soát sau: khi có kết quả rerank cuối cùng, phần này có thể thêm một câu dẫn rằng hiệu quả thực nghiệm được báo cáo ở Chương 4, không đưa số liệu vào Chương 3 nếu chưa cần.

#### 3.4. Tầng điều phối tác tử

Trạng thái: **đã viết bản đầu**.

Nội dung đã khớp với bản thảo hiện tại:

- Lý do cần orchestration agent thay vì pipeline tuyến tính.
- Intent routing bằng LLM, xử lý multi-intent và trích xuất scope như book/grade/topic.
- ContextAnalyzer và QueryRewriter để xử lý câu hỏi phụ thuộc hội thoại, query mơ hồ và scope thiếu.
- State management như nền của tầng điều phối: mô hình `Session`, `QuizState`, `SlideState`, luật vòng đời session trong `SessionManager.resolve_session()` và cách `get_context_messages()` được inject vào intent detection cùng query rewriting.
- ActionPlanner, Dispatcher và execution loop kiểu OBSERVE--DECIDE--ACT.
- Đã có các sơ đồ về intent routing, action planning và execution loop.

Việc cần rà soát sau: cân bằng lại thuật ngữ tiếng Anh/tiếng Việt nếu đọc quá nặng tiếng Anh, nhưng vẫn nên giữ các thuật ngữ chuyên ngành như intent routing, query rewriting, action planning, dispatcher và execution loop.

### 5.4. Phần Chương 3 chưa viết xong

#### 3.5. Tầng sinh nội dung đa tác tử

Trạng thái: **chưa viết xong, đang là skeleton trong LaTeX**.

Nội dung cần viết tiếp:

- Mô hình Supervisor--Specialist và lý do lựa chọn so với single-agent.
- Giao thức giao tiếp giữa các agent: `AgentTask`, `AgentTaskResult`, artifact, confidence, constraint và source grounding.
- Content Supervisor và thứ tự delegate: outline -> content -> media/quiz -> merge -> quality.
- Các specialist agent chính:
  - PedagogyPlannerAgent: lập dàn ý sư phạm;
  - ContentDraftingAgent: sinh nội dung bám nguồn;
  - MediaResearchAgent: gợi ý học liệu minh họa;
  - ContentAssessmentAgent: sinh câu hỏi hoặc hoạt động đánh giá nhúng.
- Tổng hợp kết quả bằng service tất định như SlideMerger/SlideExportService, không mô tả merger như một agent tự trị nếu code không triển khai như agent.
- QualityReviewerAgent, reflection loop và quality gate.
- Human-in-the-loop (HITL) tại bước duyệt outline, cơ chế interrupt-resume.
- Tái sử dụng kiến trúc cho slide và giáo án thông qua `task_type`, artifact schema và ContextBuilder/token budgeting.

Các sơ đồ nên có hoặc tận dụng:

- Sơ đồ Supervisor--Specialist cho content multi-agent.
- Sơ đồ giao thức `AgentTask -> Specialist -> AgentTaskResult -> Artifact store/workflow state` nếu cần làm rõ communication protocol.
- Sơ đồ quality loop và HITL nếu phần text dài.

#### 3.6. Phương pháp đánh giá

Trạng thái: **chưa viết xong, đang là skeleton trong LaTeX**.

Nội dung cần viết tiếp:

- Tách rõ đánh giá retrieval và đánh giá generation.
- Retrieval là đánh giá định lượng chính, có benchmark single-gold theo lesson key và có thể tính Hit@k, Recall@k, Precision@k, MRR@k, nDCG@k.
- Cần trình bày vì sao benchmark dùng single-gold lesson key trong bộ câu hỏi hiện tại, và cách tính metric dựa trên lesson key của retrieved chunk.
- Cần mô tả hai cấu hình chính:
  - no rerank: đo chất lượng retriever trước reranking;
  - with rerank: đo chất lượng sau khi reranker sắp xếp lại candidate.
- Cần báo cáo rằng benchmark hiện đã có khoảng 600 query, phân bố theo book/grade và có kết quả no-rerank sơ bộ tốt; số liệu với rerank sẽ cập nhật sau khi chạy xong.
- Generation dùng kết quả RAGAS đã có hoặc rubric thủ công, không gọi lại LLM để đánh giá nếu chi phí không phù hợp.
- Node validate bằng LLM trong pipeline chỉ là cơ chế kiểm soát runtime, không thay thế ground truth đánh giá generation.

Logic benchmark retrieval cần giữ trong Chương 3/4:

- Mỗi query gắn với một bài học gold thông qua `gold_lesson_key`.
- Một retrieved chunk được xem là đúng nếu có cùng `(book, grade, topic_name, lesson_name)` với gold.
- Metrics tính với k ∈ {1, 3, 5, 10}:
  - Hit@k;
  - Recall@k;
  - Precision@k;
  - MRR@k;
  - nDCG@k.
- Kết quả cần tách theo overall và theo nhóm book-grade, ví dụ CD-10, CD-11, CD-12, KNTT-10, KNTT-11, KNTT-12.
- Output evaluation nên lưu raw per-query để phân tích lỗi.

Kết quả no-rerank hiện có thể dùng làm mốc sơ bộ cho Chương 4 sau này:

| Nhóm | Hit@1 | Hit@10 | MRR@10 |
|---|---:|---:|---:|
| CD-10 | 0.700 | 0.970 | 0.809 |
| CD-11 | 0.900 | 0.990 | 0.937 |
| CD-12 | 0.770 | 0.980 | 0.843 |
| KNTT-10 | 0.740 | 0.980 | 0.842 |
| KNTT-11 | 0.700 | 1.000 | 0.813 |
| KNTT-12 | 0.760 | 0.970 | 0.848 |

Các số liệu trên là kết quả no-rerank trên 600 query, chưa dùng để kết luận cuối cùng cho reranker. Khi có kết quả with-rerank, cần cập nhật bảng so sánh trước/sau rerank ở Chương 4.

#### 3.7. Kết chương

Trạng thái: **chưa viết xong**.

Kết chương cần tóm tắt:

- Đã trình bày kiến trúc tổng thể và luồng xử lý chính.
- Đã mô tả nền tảng tri thức và RAG core.
- Đã mô tả tầng điều phối tác tử và tầng sinh nội dung đa tác tử.
- Đã xác định phương pháp đánh giá retrieval/generation.
- Chương 4 sẽ trình bày cài đặt, kiểm thử và kết quả thực nghiệm.

## 6. Chương 4: Cài đặt, kiểm thử và kết quả thực nghiệm

### 6.1. Mục tiêu chương

Chương 4 chứng minh thiết kế ở chương 3 đã được hiện thực hóa và đánh giá. Chương này nên ngắn gọn về kiến trúc phần mềm, tập trung nhiều hơn vào kiểm thử, kết quả retrieval/generation và phân tích lỗi.

### 6.2. Cấu trúc đề xuất

#### 4.1. Môi trường cài đặt

Nội dung cần viết:

- Ngôn ngữ lập trình.
- Backend framework.
- LLM provider/model.
- Embedding model.
- Reranker model.
- Vector database/index hoặc cơ chế search đang dùng.
- Các thư viện chính.
- Môi trường phần cứng/phần mềm nếu cần.

Thông tin hiện trạng có thể lấy từ `docs/project_technical_reference_vi.md` và `src/config/config.py`.

#### 4.2. Cấu trúc cài đặt hệ thống

Nội dung cần viết:

- Trình bày các module chính ở mức đủ hiểu:
  - app/API;
  - orchestrator;
  - schemas/context;
  - RAG service;
  - retriever/reranker;
  - quiz/slide/lesson services;
  - evaluation scripts;
  - logs/trace.
- Không cần liệt kê toàn bộ package hoặc từng file nhỏ.

#### 4.3. Cài đặt pipeline xử lý tài liệu

Nội dung cần viết:

- Dữ liệu nguồn được đặt ở đâu.
- Cách dữ liệu được làm sạch.
- Cách sinh chunk.
- Cách gắn metadata.
- Cách tạo hoặc nạp index.
- Cách kiểm tra số lượng chunk và metadata.

#### 4.4. Cài đặt pipeline hỏi đáp

Nội dung cần viết:

- User gửi câu hỏi qua API/frontend.
- Orchestrator tạo RequestContext.
- ContextAnalyzer/QueryRewriter xử lý ngữ cảnh nếu cần.
- IntentRouter xác định intent.
- ActionPlanner tạo action.
- ExecutionDispatcher gọi service tương ứng.
- RAGService truy xuất context.
- LLM sinh câu trả lời.
- Response được trả về và ghi debug/trace.

#### 4.5. Cài đặt retrieval và reranking

Nội dung cần viết:

- Top-k retrieval mặc định.
- Top-n sau reranking.
- Cách filter theo book/grade/topic.
- Ví dụ một kết quả retrieval gồm:
  - chunk text rút gọn;
  - score;
  - metadata;
  - source.
- Nếu có nhiều chiến lược retrieval, mô tả từng chiến lược và cách chọn.

#### 4.6. Cài đặt generation

Nội dung cần viết:

- Prompt template chính.
- Cách đưa context vào prompt.
- Quy tắc trả lời khi context không đủ.
- Cách format câu trả lời cho học sinh.
- Cách giữ nguồn hoặc debug context.

#### 4.7. Cài đặt evaluation

Nội dung cần viết:

- Định dạng file test.
- Cách sinh benchmark bằng LLM từ dữ liệu SGK/chunk.
- Cách rà soát benchmark sau khi sinh:
  - loại câu hỏi không có đáp án trong tài liệu;
  - chuẩn hóa metadata sách/lớp/chủ đề/bài;
  - gắn expected chunk/source nếu có;
  - kiểm tra expected keywords.
- Cách chạy evaluation.
- Output sinh ra:
  - bảng kết quả;
  - report markdown;
  - log hoặc file raw output.
- Cách đọc các metric.
- Cần tách hai luồng evaluation:
  - retrieval evaluation chạy tự động trên bộ câu hỏi có expected context/source;
  - generation evaluation xuất bảng câu hỏi, context, answer và rubric để người đánh giá chấm thủ công.
- Không dùng node validate hoặc LLM-as-judge làm nguồn điểm chính cho generation trong chương 4.

#### 4.8. Kiểm thử chức năng

Bảng test case gợi ý:

| Mã | Chức năng | Input | Kết quả mong đợi | Kết quả |
|---|---|---|---|---|
| TC01 | Đọc dữ liệu SGK | File markdown/PDF đã làm sạch | Nội dung được parse | Đạt/Không đạt |
| TC02 | Chunking | Nội dung bài học | Sinh chunk có metadata | Đạt/Không đạt |
| TC03 | Embedding/indexing | Danh sách chunk | Sinh vector/index | Đạt/Không đạt |
| TC04 | Scope filtering | Câu hỏi có sách/lớp | Chỉ lấy context đúng phạm vi | Đạt/Không đạt |
| TC05 | Retrieval | Câu hỏi kiến thức | Trả về top-k context liên quan | Đạt/Không đạt |
| TC06 | Reranking | Candidate chunks | Chunk đúng được đưa lên cao | Đạt/Không đạt |
| TC07 | Generation | Question + context | Trả lời đúng theo SGK | Đạt/Không đạt |
| TC08 | Out-of-scope | Câu hỏi ngoài tài liệu | Không bịa, báo thiếu thông tin | Đạt/Không đạt |
| TC09 | Multi-intent | Yêu cầu gồm nhiều tác vụ | Tạo nhiều action phù hợp | Đạt/Không đạt |
| TC10 | Logging/debug | Một request bất kỳ | Có trace/debug phục vụ phân tích | Đạt/Không đạt |

#### 4.9. Kết quả đánh giá retrieval

Bảng kết quả gợi ý (k ∈ {1,3,5,10}, benchmark single-gold theo lesson key như mô tả ở mục 3.6):

| Cấu hình | Hit@5 | Recall@5 | Precision@5 | MRR | nDCG@5 | Latency(s) | Nhận xét |
|---|---:|---:|---:|---:|---:|---:|---|
| Vector top-k | ... | ... | ... | ... | ... | ... | ... |
| Vector + filter scope | ... | ... | ... | ... | ... | ... | ... |
| Vector + rerank | ... | ... | ... | ... | ... | ... | ... |
| Hierarchical (HRAG) | ... | ... | ... | ... | ... | ... | ... |
| Adaptive end-to-end | ... | ... | ... | ... | ... | ... | ... |

Phân tích cần có:

- Cấu hình nào tốt nhất tổng thể.
- Cấu hình nào tốt với câu hỏi định nghĩa.
- Cấu hình nào tốt với câu hỏi vận dụng hoặc nhiều bước.
- Lỗi retrieval phổ biến là gì.
- Tác động của reranking.
- Tác động của filter theo sách/lớp/chủ đề.

#### 4.10. Kết quả đánh giá generation

Bảng kết quả gợi ý:

| Cấu hình | Correctness | Faithfulness | Completeness | Clarity | Điểm TB | Lỗi chính |
|---|---:|---:|---:|---:|---:|---|
| Vector only | ... | ... | ... | ... | ... | ... |
| Vector + rerank | ... | ... | ... | ... | ... | ... |
| Adaptive retrieval | ... | ... | ... | ... | ... | ... |

Phân tích cần có:

- Context tốt có cải thiện answer không.
- Các lỗi answer đến từ retrieval hay từ LLM.
- Các mẫu hallucination hoặc suy diễn ngoài context xuất hiện ở cấu hình nào.
- Câu trả lời có phù hợp với học sinh THPT không.
- Việc chấm generation được thực hiện thủ công theo rubric đã mô tả ở chương 3; node validate nếu có chỉ dùng làm thông tin tham khảo.

#### 4.11. Phân tích lỗi

Chia lỗi theo nhóm:

- Lỗi dữ liệu:
  - tài liệu thiếu hoặc chưa làm sạch;
  - metadata sai;
  - nội dung cùng chủ đề ở nhiều nơi gây nhầm.
- Lỗi chunking:
  - cắt mất ý;
  - chunk quá dài;
  - chunk quá ngắn;
  - overlap tạo nhiều chunk trùng.
- Lỗi retrieval:
  - query mơ hồ;
  - embedding không bắt đúng thuật ngữ;
  - filter quá chặt;
  - top-k chứa context nhiễu.
- Lỗi reranking:
  - reranker đánh giá sai relevance;
  - chunk đúng bị đẩy xuống dưới.
- Lỗi generation:
  - LLM suy diễn ngoài context;
  - trả lời thiếu ý;
  - không nhận biết câu hỏi ngoài phạm vi;
  - diễn đạt không phù hợp cấp học.
- Lỗi evaluation:
  - ground truth chưa đầy đủ;
  - câu hỏi có nhiều cách trả lời đúng;
  - rubric chưa đủ chi tiết.

#### 4.12. Nhận xét kết quả thực nghiệm

Nội dung cần viết:

- Tóm tắt 3-5 kết quả quan trọng nhất.
- Nhận xét cấu hình tốt nhất và lý do.
- Những phần hệ thống làm tốt.
- Những hạn chế còn lại.
- Mối quan hệ giữa retrieval score và generation score.

## 7. Chương 5: Kết luận

### 7.1. Kết quả đạt được

Nội dung cần viết:

- Đã xây dựng pipeline chatbot giáo dục dựa trên RAG.
- Đã xử lý dữ liệu SGK Tin học THPT thành dạng phục vụ retrieval.
- Đã cài đặt các thành phần hỏi đáp: context analysis, retrieval, reranking, generation.
- Đã hỗ trợ các tác vụ học tập liên quan như giải thích, quiz, slide hoặc giáo án nếu nằm trong phạm vi.
- Đã thiết kế và chạy evaluation cho retrieval/generation.
- Đã phân tích lỗi để xác định hướng cải thiện.

### 7.2. Đóng góp của đồ án

Nội dung cần viết:

- Đề xuất kiến trúc pipeline phù hợp với hỏi đáp trên SGK tiếng Việt.
- Thiết kế cơ chế truy xuất có xét phạm vi sách/lớp/chủ đề.
- Kết hợp query rewriting, adaptive retrieval hoặc reranking nếu có cài đặt.
- Đề xuất quy trình đánh giá riêng retrieval và generation.
- Tạo nền tảng để mở rộng sang các tác vụ giáo dục khác.

### 7.3. Hạn chế

Nội dung cần viết:

- Dữ liệu đánh giá còn giới hạn.
- Ground truth có thể chưa bao phủ hết các cách hỏi.
- Chất lượng phụ thuộc embedding, reranker và LLM.
- Chưa tối ưu sâu latency/cost nếu chưa đo đầy đủ.
- Một số tác vụ như slide/giáo án có thể khó đánh giá tự động.
- Nếu graph retrieval chưa hoàn thiện thì cần ghi rõ là hướng mở rộng, không trình bày như kết quả chính.

## 8. Chương 6: Hướng phát triển

Nội dung nên tổ chức theo các nhóm:

### 8.1. Mở rộng dữ liệu và bộ đánh giá

- Bổ sung thêm tài liệu, bài tập, đề kiểm tra.
- Tạo bộ benchmark lớn hơn theo lớp, bộ sách, chủ đề.
- Gắn nhãn expected context/chunk kỹ hơn.
- Tăng số lượng câu hỏi ngoài phạm vi.

### 8.2. Cải thiện retrieval

- Thử nhiều embedding model tiếng Việt.
- Tối ưu chunking theo cấu trúc bài học.
- Tối ưu top-k/top-n.
- Cải thiện query rewriting.
- Kết hợp lexical search và vector search.
- Nghiên cứu graph/hybrid retrieval nếu phù hợp.

### 8.3. Cải thiện generation

- Tối ưu prompt theo từng loại câu hỏi.
- Thêm bước kiểm tra faithfulness sau generation.
- Tự động từ chối khi context không đủ.
- Cải thiện citation/source attribution.
- Cá nhân hóa mức diễn giải theo học sinh.

### 8.4. Cải thiện evaluation và observability

- Xây dựng dashboard theo dõi kết quả evaluation.
- Lưu lịch sử lỗi theo từng service.
- Mở rộng human feedback để tăng độ tin cậy của đánh giá generation.
- Có thể nghiên cứu LLM-as-judge ở giai đoạn sau nếu cần tự động hóa và kiểm soát được chi phí.
- Đánh giá latency và cost ở quy mô lớn hơn.

### 8.5. Mở rộng tác vụ giáo dục

- Nâng cấp sinh quiz theo mức độ nhận thức.
- Đánh giá chất lượng slide/giáo án bằng rubric riêng.
- Hỗ trợ học tập cá nhân hóa theo tiến độ.
- Tích hợp phản hồi giáo viên vào vòng cải thiện nội dung.

## 9. Thứ tự triển khai tiếp theo

Thứ tự triển khai hiện tại được cập nhật theo trạng thái đã viết của bản thảo:

1. Rà soát nhanh Chương 2 sau khi compile PDF: văn phong, độ dài, bảng so sánh và liên kết dẫn sang Chương 3.
2. Hoàn thiện Chương 3.5 về tầng sinh nội dung đa tác tử, ưu tiên Supervisor--Specialist, giao thức agent, artifact, quality loop và HITL.
3. Hoàn thiện Chương 3.6 về phương pháp đánh giá, bao gồm retrieval benchmark, metric, no-rerank/with-rerank và generation evaluation.
4. Cập nhật kết chương 3 để tóm tắt đúng các phần đã viết và dẫn sang Chương 4.
5. Khi có kết quả rerank đầy đủ, viết Chương 4 theo kết quả thực nghiệm thực tế.
6. Sau Chương 4, chỉnh lại Chương 5 và Chương 6 để tổng kết đúng đóng góp, hạn chế và hướng phát triển.
7. Quay lại rà soát toàn bộ văn phong theo guideline: không bullet tùy tiện, mọi bảng/hình/công thức đều được tham chiếu và giải thích.

## 10. Checklist rà soát hiện tại

| Mục kiểm tra | Trạng thái | Ghi chú |
|---|---|---|
| Chương 2 đã giải thích đủ vì sao cần RAG/adaptive retrieval | Đã xong bản đầu | Cần rà văn phong và citation nếu muốn bổ sung sau. |
| Chương 2 có khảo sát và khoảng trống rõ ràng | Đã xong bản đầu | Đã có bảng so sánh và định vị giải pháp. |
| Chương 3.1-3.4 đã có nội dung | Đã xong bản đầu | Cần rà bố cục hình và mức độ thuật ngữ. |
| Chương 3.5 đã mô tả content multi-agent | Chưa xong | Đây là phần cần viết tiếp. |
| Chương 3.6 đã mô tả phương pháp đánh giá | Chưa xong | Cần viết retrieval/generation evaluation. |
| Chương 4 có kết quả thực nghiệm thật | Chưa cập nhật | Đang chờ kết quả rerank đầy đủ. |
| Các phần web app/package/API không lấn át phần nghiên cứu | Đang kiểm soát | Tiếp tục giữ ở mức cài đặt/chứng minh hệ thống chạy được. |
| Thuật ngữ RAG, embedding, reranking, hallucination, faithfulness được giải thích trước khi dùng | Đã có nền ở Chương 2 | Cần giữ nhất quán ở Chương 3-4. |
| Các bảng metric có định nghĩa rõ cách tính | Chưa xong | Sẽ viết trong Chương 3.6 và Chương 4. |
| Văn phong tránh quảng bá/cảm tính | Đang rà soát | Ưu tiên văn phong khoa học, mô tả dựa trên thiết kế và kết quả. |

## 11. Deliverable cần có

| Deliverable | Mục đích | Dùng ở chương |
|---|---|---|
| Sơ đồ pipeline tổng thể | Giải thích kiến trúc giải pháp | Chương 3 |
| Bảng node input/output | Làm rõ thiết kế từng thành phần | Chương 3 |
| Bảng dataset/evaluation samples | Mô tả bộ câu hỏi đánh giá | Chương 3, 4 |
| Bảng retrieval metrics | So sánh chất lượng truy xuất | Chương 4 |
| Bảng generation metrics | So sánh chất lượng câu trả lời | Chương 4 |
| Bảng test case chức năng | Chứng minh hệ thống chạy đúng chức năng | Chương 4 |
| Bảng phân tích lỗi | Chỉ ra giới hạn và nguyên nhân | Chương 4, 5 |
| Danh sách hạn chế | Làm cơ sở cho hướng phát triển | Chương 5, 6 |

## 12. Ranh giới nội dung cần giữ

Những phần nên viết sâu:

- Bài toán hỏi đáp trên tài liệu giáo dục.
- RAG pipeline.
- Chunking, embedding, retrieval, reranking, generation.
- Evaluation retrieval/generation.
- Phân tích lỗi.

Những phần chỉ viết vừa đủ:

- Cấu trúc package.
- API endpoint.
- Frontend.
- Session store.
- Trace/debug implementation.
- Deployment.

Những phần không nên đưa thành trọng tâm:

- Mô tả UI như một sản phẩm thương mại.
- Liệt kê toàn bộ file source code.
- Trình bày quá nhiều về framework web.
- Viết graph/hybrid retrieval như đóng góp chính nếu chưa có thực nghiệm tương ứng.
