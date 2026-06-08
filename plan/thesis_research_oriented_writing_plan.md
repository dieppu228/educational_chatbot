# Plan viết lại đồ án theo hướng nghiên cứu giải pháp

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

## 4. Chương 2: Cơ sở lý thuyết, khảo sát và đề xuất giải pháp

### 4.1. Mục tiêu chương

Chương 2 cần đặt nền tảng cho hướng nghiên cứu. Sau chương này, người đọc phải hiểu:

- Bài toán chatbot giáo dục có đặc thù gì.
- Vì sao LLM trực tiếp chưa đủ cho dữ liệu SGK.
- RAG giải quyết vấn đề nào trong hỏi đáp dựa trên tài liệu.
- Các hướng hiện có trên thị trường hoặc trong kỹ thuật có ưu nhược điểm gì.
- Đồ án đề xuất giải pháp nào và giải pháp đó giải quyết khoảng trống nào.

### 4.2. Cấu trúc đề xuất

#### 2.1. Tổng quan bài toán chatbot giáo dục

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

#### 2.2. Hệ thống hỏi đáp dựa trên tài liệu

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

#### 2.3. Large Language Model và hạn chế khi dùng trực tiếp

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

#### 2.4. Embedding và tìm kiếm ngữ nghĩa

Nội dung cần viết:

- Khái niệm embedding.
- Cách biểu diễn câu hỏi và đoạn tài liệu thành vector.
- Similarity search và vai trò của vector database/index.
- Các độ đo tương đồng thường gặp: cosine similarity, dot product, Euclidean distance.
- Ý nghĩa trong đồ án: truy xuất các chunk SGK có nội dung gần với câu hỏi.

Nếu muốn gắn với hiện trạng dự án, có thể nhắc ở mức tổng quan rằng hệ thống dùng embedding tiếng Việt phù hợp hơn với dữ liệu SGK tiếng Việt. Chi tiết model cụ thể nên để chương 4.

#### 2.5. Retrieval-Augmented Generation

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

#### 2.6. Adaptive retrieval, reranking và query rewriting

Nội dung cần viết:

- Lý do một truy vấn người dùng có thể mơ hồ hoặc thiếu ngữ cảnh.
- Query rewriting giúp mở rộng hoặc chuẩn hóa truy vấn như thế nào.
- Adaptive retrieval chọn chiến lược truy xuất theo phạm vi sách, lớp, chủ đề hoặc loại intent.
- Reranking giúp sắp xếp lại các đoạn candidate theo mức độ liên quan.
- Trade-off giữa chất lượng, latency và chi phí.

Phần này cần chuẩn bị nền cho các thành phần đang có trong dự án như ContextAnalyzer, QueryRewriter, AdaptiveRAGAgent, Reranker.

#### 2.7. Multi-intent và điều phối yêu cầu học tập

Nội dung cần viết vừa đủ:

- Người dùng không chỉ hỏi đáp mà còn có thể yêu cầu tạo quiz, giải thích, sinh slide hoặc giáo án.
- Cần có bước phân tích intent để định tuyến yêu cầu.
- Phân biệt rõ: đây là lớp điều phối hệ thống, không phải đóng góp nghiên cứu chính về retrieval.
- Liên hệ với hệ thống hiện tại: Orchestrator, IntentRouter, ActionPlanner và ExecutionDispatcher có vai trò điều phối pipeline.

#### 2.8. Đánh giá hệ thống RAG

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

#### 2.9. Khảo sát giải pháp liên quan và thị trường

Nội dung cần viết:

- Nhóm chatbot rule-based.
- Nhóm FAQ/keyword search.
- Nhóm semantic search.
- Nhóm chatbot gọi LLM trực tiếp.
- Nhóm RAG chatbot.
- Nhóm hybrid/adaptive RAG nếu có khảo sát.

Bảng so sánh nên có các tiêu chí:

| Nhóm giải pháp | Hiểu câu hỏi tự nhiên | Dùng dữ liệu riêng | Giảm hallucination | Khả năng mở rộng | Phù hợp với SGK |
|---|---|---|---|---|---|
| Rule-based | Thấp | Trung bình | Cao nếu luật đủ | Thấp | Thấp |
| FAQ/keyword search | Thấp-Trung bình | Có | Trung bình | Trung bình | Trung bình |
| LLM trực tiếp | Cao | Thấp nếu không nạp context | Thấp | Cao | Thấp-Trung bình |
| RAG | Cao | Cao | Trung bình-Cao | Cao | Cao |
| Adaptive/hybrid RAG | Cao | Cao | Cao hơn nếu retrieval tốt | Trung bình-Cao | Cao |

#### 2.10. Khoảng trống và đề xuất giải pháp của đồ án

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

Chương 3 là chương trọng tâm về nghiên cứu/giải pháp. Chương này cần mô tả:

- Kiến trúc pipeline được đề xuất.
- Thiết kế chi tiết từng node.
- Input/output của từng node.
- Tham số hoặc quyết định kỹ thuật quan trọng.
- Cách đánh giá các node trọng tâm, đặc biệt là retrieval và generation.
- Các node còn lại như intent routing, query rewriting, context building và validate được mô tả về vai trò, input/output và kiểm thử chức năng. Không bắt buộc phải đánh giá định lượng sâu nếu không phải trọng tâm nghiên cứu.

Phạm vi đánh giá chính trong chương 3:

| Node | Vai trò trong evaluation | Cách đánh giá chính |
|---|---|---|
| Retrieve | Node đánh giá định lượng chính | Chạy test nhiều chiến lược search và so sánh metric |
| Rerank | Node phụ nhưng có thể đánh giá cùng retrieve | So sánh trước/sau rerank |
| LLM generate | Node đánh giá chất lượng câu trả lời | Con người chấm theo rubric |
| Validate | Node hỗ trợ kiểm soát runtime | Mô tả cơ chế và test chức năng, không dùng làm evaluator chính |

### 5.2. Cấu trúc đề xuất

#### 3.1. Mục tiêu thiết kế

Nội dung cần viết:

- Hệ thống cần trả lời câu hỏi dựa trên SGK Tin học.
- Câu trả lời cần đúng, đủ, dễ hiểu và có căn cứ từ context.
- Pipeline cần hỗ trợ nhiều loại yêu cầu học tập.
- Thiết kế phải phục vụ cả vận hành và đánh giá thực nghiệm.

#### 3.2. Kiến trúc tổng thể

Nội dung cần viết:

- Sơ đồ tổng quan hệ thống.
- Chia thành hai pipeline:
  - offline/indexing pipeline;
  - online/question-answering pipeline.
- Các khối chính:
  - API/frontend;
  - Orchestrator;
  - ContextAnalyzer/QueryRewriter;
  - IntentRouter;
  - ActionPlanner;
  - ExecutionDispatcher;
  - RAGService/AdaptiveRAGAgent;
  - Retriever;
  - Reranker;
  - LLM generation;
  - Evaluation/logging.

Chú ý: phần API/frontend chỉ mô tả như lớp giao tiếp, không đi sâu thiết kế UI.

#### 3.3. Thiết kế dữ liệu đầu vào

Nội dung cần viết:

- Nguồn dữ liệu: SGK Tin học THPT lớp 10-12, bộ Cánh Diều và Kết Nối Tri Thức.
- Cấu trúc phân cấp: bộ sách, lớp, chủ đề, bài học, mục.
- Metadata cần lưu:
  - book;
  - grade;
  - topic;
  - lesson;
  - section;
  - chunk_id;
  - source file;
  - page nếu có.
- Các vấn đề dữ liệu:
  - nội dung dài;
  - cùng chủ đề xuất hiện ở nhiều lớp/bộ sách;
  - thuật ngữ tiếng Việt chuyên ngành Tin học;
  - nội dung bài học có cả lý thuyết, ví dụ và bài tập.

#### 3.4. Thiết kế tiền xử lý tài liệu

Viết theo format:

- Mục đích.
- Input.
- Output.
- Cách xử lý.
- Lỗi có thể gặp.
- Cách kiểm tra.

Các bước nên trình bày:

- đọc dữ liệu nguồn;
- chuẩn hóa ký tự và encoding;
- loại bỏ đoạn rỗng hoặc nhiễu;
- giữ lại heading/section;
- gắn metadata theo bộ sách, lớp, chủ đề, bài;
- chuẩn hóa cấu trúc để phục vụ chunking.

#### 3.5. Thiết kế chunking

Nội dung cần viết:

- Vì sao không đưa toàn bộ tài liệu vào LLM.
- Vì sao cần chia chunk cho retrieval.
- Chiến lược chunking:
  - chunk theo cấu trúc bài học nếu có;
  - chunk theo độ dài;
  - overlap để giảm mất ngữ cảnh;
  - loại bỏ chunk quá ngắn hoặc không có nội dung.
- Tham số cần báo cáo:
  - chunk size;
  - overlap;
  - min/max length;
  - separator.
- Ảnh hưởng của chunking:
  - chunk quá ngắn có thể thiếu ý;
  - chunk quá dài có thể gây nhiễu;
  - overlap quá lớn làm tăng trùng lặp.
- Cách đánh giá:
  - kiểm tra phân phối độ dài chunk;
  - kiểm tra metadata;
  - kiểm tra một số câu hỏi mẫu có truy xuất đúng chunk chứa đáp án không.

#### 3.6. Thiết kế embedding và indexing

Nội dung cần viết:

- Input: nội dung chunk.
- Output: vector embedding và payload metadata.
- Lý do dùng embedding tiếng Việt.
- Cách lưu index phục vụ similarity search.
- Các payload quan trọng:
  - text;
  - book;
  - grade;
  - topic;
  - lesson;
  - source;
  - chunk_id.
- Rủi ro:
  - embedding không bắt tốt thuật ngữ chuyên ngành;
  - metadata sai làm filter sai;
  - index không đồng bộ khi dữ liệu thay đổi.

#### 3.7. Thiết kế phân tích ngữ cảnh và rewrite query

Nội dung cần viết:

- Mục đích: xử lý câu hỏi phụ thuộc hội thoại hoặc thiếu thông tin.
- Input: câu hỏi hiện tại, session/context trước đó.
- Output:
  - enriched query;
  - danh sách query phụ cho retrieval;
  - thông tin debug.
- Các trường hợp cần rewrite:
  - câu hỏi dùng đại từ hoặc tham chiếu như "phần này", "bài đó";
  - câu hỏi thiếu chủ đề;
  - câu hỏi cần mở rộng từ khóa.
- Cách đánh giá:
  - kiểm tra query rewrite có giữ đúng ý định không;
  - so sánh retrieval trước và sau rewrite.

#### 3.8. Thiết kế intent routing và action planning

Nội dung cần viết:

- Mục đích: xác định yêu cầu của người dùng để gọi đúng service.
- Intent chính:
  - hỏi đáp/giải thích;
  - tạo quiz;
  - chấm câu trả lời;
  - sinh slide;
  - sinh giáo án;
  - fallback/out-of-scope.
- Input: query đã enrich.
- Output: intent result, task type, book/grade/topic nếu có.
- Action planning:
  - chuyển intent thành hành động cụ thể;
  - hỗ trợ multi-intent nếu một câu có nhiều yêu cầu.
- Vai trò trong nghiên cứu: bảo đảm request được đưa vào đúng pipeline, không phải trọng tâm đánh giá retrieval.

#### 3.9. Thiết kế retrieval service

Viết từng retriever theo format:

- Mục đích.
- Input.
- Output.
- Cách hoạt động.
- Tham số.
- Ưu điểm.
- Hạn chế.
- Cách đánh giá.

Các service/nút cần mô tả:

##### 3.9.1. Vector Retriever

- Nhận query hoặc rewritten queries.
- Tạo embedding cho query.
- Search top-k chunk gần nhất.
- Áp dụng filter theo book/grade/topic nếu có.
- Trả về danh sách candidate context.

##### 3.9.2. Adaptive Retriever

- Xác định chiến lược truy xuất dựa trên query, intent và scope.
- Có thể điều chỉnh filter theo sách/lớp/chủ đề.
- Có thể mở rộng query hoặc lấy nhiều nhóm context.
- Trả về context có debug strategy.

##### 3.9.3. Hybrid/graph retriever nếu có

- Chỉ viết nếu hệ thống có cài đặt hoặc có kết quả thực nghiệm.
- Trình bày rõ vai trò của graph hoặc hybrid retrieval.
- Không phóng đại nếu graph chỉ là extension point hoặc chưa hoàn thiện.

#### 3.10. Thiết kế reranking

Nội dung cần viết:

- Vì sao top-k ban đầu cần được rerank.
- Input: query và danh sách candidate chunks.
- Output: top-n context đã sắp xếp lại.
- Tham số:
  - số candidate trước rerank;
  - số context sau rerank;
  - model reranker.
- Đánh đổi:
  - tăng chất lượng context;
  - tăng latency;
  - tăng chi phí tính toán.
- Cách đánh giá:
  - so sánh Hit@k/MRR trước và sau rerank;
  - kiểm tra các case rerank đưa chunk đúng lên vị trí cao hơn.

#### 3.11. Thiết kế context building và context combining

Nội dung cần viết:

- Mục đích: biến retrieved chunks thành context đưa vào prompt.
- Cách loại trùng hoặc ghép context.
- Cách giữ metadata/source.
- Cách kiểm soát độ dài context.
- Rủi ro:
  - context quá dài;
  - context nhiễu;
  - mất nguồn sau khi ghép.

#### 3.12. Thiết kế generation service

Nội dung cần viết:

- Input:
  - câu hỏi;
  - context;
  - prompt;
  - metadata/source;
  - lịch sử hội thoại nếu cần.
- Output:
  - câu trả lời cuối cùng;
  - nguồn hoặc ngữ cảnh liên quan nếu có;
  - thông tin debug.
- Yêu cầu prompt:
  - trả lời dựa trên context;
  - không bịa khi context không đủ;
  - diễn giải phù hợp với học sinh THPT;
  - giữ thuật ngữ đúng.
- Các lỗi cần dự phòng:
  - context đúng nhưng trả lời sai;
  - context thiếu dẫn tới trả lời thiếu;
  - model suy diễn ngoài tài liệu;
  - câu trả lời không phù hợp cấp học.

#### 3.13. Thiết kế evaluation service

Đây là phần cần làm nổi bật.

Nội dung cần viết:

- Mục tiêu:
  - đánh giá retrieval bằng các metric tự động;
  - đánh giá generation bằng rubric do con người chấm;
  - so sánh cấu hình;
  - phân tích lỗi pipeline.
- Input:
  - bộ câu hỏi đánh giá;
  - expected answer;
  - expected source/context;
  - output của từng service;
  - retrieved chunks;
  - generated answer.
- Output:
  - file kết quả;
  - bảng metric;
  - log chi tiết;
  - nhận xét lỗi.
- Phạm vi:
  - retrieval là phần evaluation định lượng chính;
  - generation là phần evaluation định tính/bán định lượng do người đánh giá chấm;
  - validate node chỉ được xem là bước kiểm soát chất lượng trong pipeline, không thay thế đánh giá thủ công của generation.

#### 3.14. Thiết kế bộ câu hỏi đánh giá

Nội dung cần viết:

- Cách tạo tập câu hỏi từ SGK. Riêng benchmark cho **node Retrieve** dùng logic sinh từ chunk Level 1-2 và định nghĩa relevance đa nhãn mô tả ở mục 3.15bis.
- Benchmark được sinh bằng LLM từ nội dung SGK/chunk đã có, sau đó cần kiểm tra thủ công một phần hoặc toàn bộ để bảo đảm câu hỏi, expected answer và expected context không lệch tài liệu.
- Vai trò của LLM trong bước này là hỗ trợ tạo dữ liệu đánh giá ban đầu, không phải chấm điểm generation cuối cùng.
- Quy trình tạo benchmark đề xuất:
  - chọn phạm vi dữ liệu theo sách, lớp, chủ đề, bài;
  - đưa nội dung chunk/bài học vào prompt sinh câu hỏi;
  - yêu cầu LLM trả về question, expected answer, expected keywords, expected source metadata và question type;
  - lọc bỏ câu hỏi trùng, quá mơ hồ hoặc không trả lời được từ tài liệu;
  - kiểm tra thủ công các mẫu benchmark trước khi dùng để tính metric.
- Các nhóm câu hỏi:
  - định nghĩa;
  - liệt kê;
  - so sánh;
  - quy trình;
  - vận dụng;
  - multi-hop nếu có;
  - ngoài phạm vi tài liệu.
- Mỗi sample nên có:
  - question;
  - expected_answer;
  - expected_book;
  - expected_grade;
  - expected_topic;
  - expected_lesson/section;
  - expected_chunk_id nếu có;
  - expected_keywords;
  - source_chunk_text hoặc source_preview nếu cần kiểm tra lại;
  - difficulty;
  - question_type.

#### 3.15. Thiết kế đánh giá retrieval

Nội dung cần viết:

- Định nghĩa retrieval đúng: retrieved context chứa thông tin cần thiết để trả lời câu hỏi.
- Metrics:
  - Hit@k;
  - Recall@k;
  - Precision@k;
  - MRR;
  - nDCG nếu có nhãn relevance.
- Các cấu hình cần so sánh:
  - top-k khác nhau;
  - có/không query rewriting;
  - có/không filter scope;
  - trước/sau reranking;
  - các retriever khác nếu có.
- Các cách search có thể đưa vào thí nghiệm:
  - vector search cơ bản;
  - vector search có filter theo sách/lớp/chủ đề;
  - vector search với rewritten query;
  - vector search nhiều query rồi merge kết quả;
  - vector search + rerank;
  - adaptive retrieval nếu có chiến lược khác với vector search thường.
- Cách phân tích:
  - theo loại câu hỏi;
  - theo lớp/bộ sách;
  - theo chủ đề;
  - theo lỗi thường gặp.

> Lưu ý về metric: với mỗi câu hỏi chỉ có **một** đơn vị gold thì Hit@k và Recall@k cho ra cùng một giá trị, còn Precision@k bị chặn trần ở 1/k. Để bốn metric ở trên đều có ý nghĩa độc lập, đồ án dùng định nghĩa gold **đa nhãn ở mức chunk-trong-bài** mô tả ở mục 3.15bis.

#### 3.15bis. Đánh giá node Retrieve bằng benchmark sinh từ chunk Level 1-2 (chi tiết triển khai)

Đây là phương án triển khai cụ thể cho việc đánh giá định lượng node Retrieve của đồ án. Mục này chốt rõ logic sinh benchmark, định nghĩa relevance và cách tính metric để dùng trực tiếp cho chương 4.

**a. Đối tượng và phạm vi đánh giá**

- Đánh giá **chất lượng truy xuất** của hệ thống RAG (Vector Retriever, Adaptive/Hierarchical Retriever, có/không rerank), không đánh giá generation.
- Đơn vị "document" được chốt là **một bài học (lesson)**, khóa định danh: `(book, grade, topic_name, lesson_name)`, tương đương một file `bai*.md` trong dữ liệu nguồn.

**b. Logic sinh benchmark từ chunk Level 1-2**

- Dùng các **chunk Level 1 (Bài) và Level 2 (mục/section/objective)** trong `data/rag_chunks_v2.json` làm seed sinh câu hỏi, vì hai mức này bao quát nội dung của cả bài.
- Field `level` (độ sâu heading) đã được export thật vào `rag_chunks_v2.json` (không còn suy ra từ breadcrumb). Quy mô seed thực tế: **Level 1 = 32 chunk, Level 2 = 1229 chunk → 1261 seed**, phủ 185 bài học. Phân bố level toàn bộ: `{1:32, 2:1229, 3:921, 4:137, 5:26, 6:3}`.
- Với mỗi seed, LLM sinh câu hỏi tự nhiên kiểu **học sinh hỏi**, có thể trả lời được bằng nội dung của bài chứa seed đó.
- Yêu cầu sinh query để **tránh data leakage**:
  - cấm chép lại nguyên cụm từ tiêu đề/breadcrumb của chunk (vì `full_content` có nhúng breadcrumb, dễ làm BM25 match trivial);
  - đa dạng cách diễn đạt và độ khó;
  - câu hỏi phải trả lời được bằng **nội dung bài**, không chỉ bằng tên bài.

**c. Định nghĩa relevance (đa nhãn ở mức chunk-trong-bài)**

- Gold của một câu hỏi = **tập tất cả chunk cùng `(book, grade, topic_name, lesson_name)`** với chunk seed (gồm cả L1/L2 lẫn các chunk con Level 3+ của bài đó).
- Lý do dùng đa nhãn:
  - HRAG trả về chunk Level 3+ (không bao giờ trả đúng chunk L1/L2 seed) nên **không được so khớp theo `chunk_id`** của seed; phải so khớp theo lesson key.
  - Đa nhãn làm Recall@k và Precision@k trở thành tín hiệu độc lập, thay vì trùng với Hit@k.
- Một chunk được retrieve coi là **đúng** nếu lesson key của nó trùng lesson key của gold.

**d. Tách hai trục đánh giá**

- **(A) Pure retrieval**: ép chạy đúng một chiến lược (`_standard_retrieval`, `_hierarchical_retrieval`...) để đo chất lượng truy xuất thuần, loại trừ ảnh hưởng của routing.
- **(B) Adaptive end-to-end**: chạy full `AdaptiveRAGAgent.retrieve()` và **breakdown metric theo `strategy_used`**, đồng thời báo cáo tỉ lệ mỗi strategy được chọn (để tách lỗi routing khỏi lỗi retrieval).

**e. Metrics**

- Tính với **k ∈ {1, 3, 5, 10}** (canh k theo `RETRIEVER_TOP_K`/`RERANKER_TOP_N` thực tế):
  - Hit@k;
  - Recall@k;
  - Precision@k;
  - MRR;
  - nDCG@k (chuẩn cho ranking đa nhãn).
- Báo cáo kèm **latency/query** (lấy từ `RAGResult.total_time_s`).

**f. Lấy mẫu phân tầng (stratified)**

- Phân bố câu hỏi đều theo **grade (10/11/12) × book (CD/KNTT) × topic × type (theory/exercise/application/objective)**.
- In bảng phân bố tập benchmark vào báo cáo để chứng minh tính đại diện.

**g. Quy trình kiểm tra chất lượng benchmark**

- Validate tự động: dùng một LLM khác (hoặc chính retriever + spot-check tay ~10-20%) xác nhận bài gold thực sự trả lời được câu hỏi; loại câu hỏi rác/mơ hồ/không trả lời được.
- Loại câu hỏi trùng và câu hỏi leak từ vựng quá nặng.

**h. Schema file benchmark**

```json
{
  "query_id": "...",
  "query": "câu hỏi học sinh (đã validate, không leak)",
  "gold_lesson_key": {"book": "KNTT", "grade": "10", "topic": "...", "lesson": "Bài 3"},
  "gold_chunk_ids": ["...", "..."],
  "source_level": 1,
  "question_type": "definition | list | compare | process | application",
  "gen_meta": {"model": "gemini-...", "validated_by": "..."}
}
```

**i. Output cho chương 4**

- Bảng metric theo từng cấu hình retrieval (xem mục 4.9).
- Bảng breakdown theo grade/book/topic/question_type.
- File raw kết quả từng query để phân tích lỗi.

#### 3.16. Thiết kế đánh giá generation

Nội dung cần viết:

- Định nghĩa câu trả lời tốt:
  - đúng;
  - đủ;
  - bám context;
  - dễ hiểu;
  - không hallucination.
- Rubric gợi ý thang 1-5:
  - 5: đúng, đủ, bám context rõ ràng;
  - 4: đúng ý chính, thiếu chi tiết nhỏ;
  - 3: đúng một phần hoặc thiếu căn cứ;
  - 2: nhiều lỗi, thiếu hoặc lệch context;
  - 1: sai hoặc bịa.
- Có thể chấm theo các tiêu chí:
  - correctness;
  - faithfulness;
  - completeness;
  - clarity;
  - citation/source use nếu có.
- Phương pháp chấm:
  - người đánh giá đọc câu hỏi, expected answer, retrieved context và generated answer;
  - chấm theo rubric cố định để giảm tính chủ quan;
  - mỗi câu trả lời nên ghi thêm lỗi chính nếu điểm thấp;
  - nếu có nhiều người chấm, lấy trung bình hoặc thảo luận lại các mẫu lệch điểm lớn.
- Không dùng LLM-as-judge làm phương pháp chính ở giai đoạn này để tránh tăng chi phí. Node validate bằng LLM nếu đã có trong pipeline chỉ dùng như cơ chế kiểm tra nội bộ, không được xem là ground truth đánh giá chất lượng generation.
- Cần phân biệt lỗi do retrieval và lỗi do generation.

#### 3.17. Thiết kế logging, trace và debug

Nội dung cần viết:

- Mục tiêu: hỗ trợ tái lập thí nghiệm và phân tích lỗi.
- Mỗi request nên ghi:
  - request id;
  - user query;
  - enriched query;
  - intent;
  - action plan;
  - scope;
  - retrieved chunks;
  - rerank scores;
  - prompt hoặc prompt metadata;
  - generated answer;
  - evaluation score nếu có.
- Liên hệ với SessionStore, TraceService và debug_steps.

#### 3.18. Kết chương 3

Kết chương cần tóm tắt:

- Đã thiết kế pipeline RAG/adaptive retrieval.
- Đã xác định vai trò từng node.
- Đã đề xuất phương pháp đánh giá retrieval và generation.
- Chương 4 sẽ trình bày cài đặt và kết quả thực nghiệm.

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

Bảng kết quả gợi ý (k ∈ {1,3,5,10}, gold đa nhãn mức lesson theo mục 3.15bis):

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

## 9. Thứ tự triển khai viết báo cáo

Nên viết theo thứ tự sau để tránh bị loạn:

1. Chốt mục tiêu nghiên cứu và phạm vi đóng góp.
2. Chốt pipeline ở chương 3 bằng sơ đồ và danh sách node.
3. Viết chương 3 trước ở dạng skeleton kỹ thuật.
4. Từ chương 3 rút ngược lại các kiến thức cần đưa vào chương 2.
5. Viết chương 2 theo hướng: lý thuyết -> khảo sát -> khoảng trống -> đề xuất.
6. Chạy hoặc tổng hợp evaluation để có số liệu cho chương 4.
7. Viết chương 4 theo kết quả thực nghiệm thực tế.
8. Viết chương 5 và 6 sau cùng.
9. Quay lại chỉnh phần Tổng quan/Kết chương để các chương liên kết mạch lạc.
10. Đối chiếu guideline trong `docs/latex_writing_guidelines_vi.md`.

## 10. Checklist trước khi chuyển sang LaTeX

- Chương 2 đã giải thích đủ vì sao cần RAG chưa.
- Chương 2 có khảo sát và khoảng trống rõ ràng chưa.
- Chương 3 đã mô tả input/output của từng node chưa.
- Chương 3 có phương pháp đánh giá retrieval và generation chưa.
- Chương 4 có kết quả thực nghiệm thật hoặc bảng dự kiến cần điền số liệu chưa.
- Chương 4 có phân tích lỗi thay vì chỉ liệt kê test case chưa.
- Chương 5 có nêu đóng góp đúng mức, không phóng đại chưa.
- Chương 6 có hướng phát triển bám theo hạn chế chưa.
- Các phần web app/package/API có bị viết quá dài so với phần nghiên cứu không.
- Các thuật ngữ như RAG, embedding, reranking, hallucination, faithfulness được giải thích trước khi dùng chưa.
- Các bảng metric có định nghĩa rõ cách tính chưa.
- Có câu nào mang tính quảng bá hoặc cảm tính cần bỏ không.

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
