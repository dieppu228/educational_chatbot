# Chương 3: Cơ sở lý thuyết

Chương này tập trung trình bày các nền tảng kiến thức cốt lõi về Trí tuệ Nhân tạo (AI) và các kỹ thuật tiên tiến được áp dụng để xây dựng hệ thống Trợ lý ảo giáo dục. Các khái niệm được triển khai từ mức cơ bản đến chuyên sâu, bám sát vào những công nghệ thực tế đang được sử dụng trong dự án.

## 3.1. Kiến thức nền tảng về Trí tuệ Nhân tạo và Xử lý ngôn ngữ tự nhiên
Khái quát về kiến trúc cốt lõi định hình nên các mô hình ngôn ngữ hiện đại.

### 3.1.1. Mã hóa từ vựng (Tokenization)
Quá trình chuyển đổi văn bản thô thành các đơn vị cơ sở (token) để máy tính hiểu được. Một trong những thuật toán phổ biến nhất hiện nay là **Byte-Pair Encoding (BPE)**. BPE bắt đầu bằng việc coi mỗi ký tự riêng lẻ là một token, sau đó lặp lại nhiều lần quá trình tìm cặp token xuất hiện cạnh nhau nhiều nhất và gộp chúng thành một token mới.
Nguyên lý tần suất của BPE có thể biểu diễn như sau:
$$ freq(t_a, t_b) = \sum_{w \in D} C(w) \cdot count((t_a, t_b), w) $$
Trong đó:
- $D$: Tập dữ liệu văn bản đào tạo.
- $C(w)$: Số lần xuất hiện của từ $w$ trong $D$.
- $count((t_a, t_b), w)$: Số lượng cặp token $(t_a, t_b)$ liền kề nhau bên trong từ $w$.
Cặp $(t_a, t_b)$ có $freq$ lớn nhất sẽ được ghép lại thành một token mới. Quy trình này giúp cân bằng giữa từ vựng kích thước cố định và khả năng biểu diễn từ chưa biết (Out-Of-Vocabulary).

### 3.1.2. Biểu diễn trong không gian vector (Word/Document Embeddings)
Embeddings là cách máy tính biểu diễn token hoặc toàn bộ văn bản dưới dạng vector số học dày đặc (Dense Vector) gồm các số thực liên tục nhằm lưu giữ đặc trưng ngữ nghĩa. Các từ có nghĩa tương đồng sẽ nằm gần nhau hơn trong một không gian vector đa chiều (ví dụ 512, 768 chiều).
Để đo mức độ tương đồng giữa hai vector mô tả ngữ nghĩa, ta sử dụng công thức **Cosine Similarity (Độ tương đồng Cosin)**:
$$ \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{ \sum_{i=1}^{n} A_i B_i }{ \sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2} } $$
Trong đó:
- $\mathbf{A}$, $\mathbf{B}$: Là hai vector đặc trưng nhiều chiều (n-chiều) biểu diễn cho hai văn bản.
- $A_i, B_i$: Thành phần thứ $i$ của vector $\mathbf{A}$ và $\mathbf{B}$.
- $\|\mathbf{A}\|, \|\mathbf{B}\|$: Độ dài (norm L2) của mỗi vector.
Giá trị cosin nằm trong khoảng $[-1, 1]$, trong đó $1$ chỉ ra hai vector cùng hướng (ý nghĩa giống nhau hoàn toàn), $0$ là trực giao (không liên quan), và $-1$ là ngược hướng.

### 3.1.3. Kiến trúc Transformer và Cơ chế Attention
Kể từ khi ra mắt vào năm 2017, kiến trúc Transformer đã trở thành sợi chỉ đỏ của NLP hiện đại. Thay vì xử lý tuần tự (như RNN/LSTM), Transformer xử lý văn bản song song thông qua cơ chế Tự chú ý (Self-Attention). 
Cơ chế **Scaled Dot-Product Attention** cho phép mô hình đánh giá tầm quan trọng của các từ trong câu khi đang xét một từ bất kỳ. Công thức lõi của cơ chế này là:
$$ Attention(Q, K, V) = \text{softmax} \left( \frac{Q K^T}{\sqrt{d_k}} \right) V $$
Trong đó:
- $Q$ (Query - Truy vấn): Vector biểu diễn từ đang cần tìm độ tương quan phân tích (thứ ta đi tìm).
- $K$ (Key - Khóa): Vector biểu diễn để đối chiếu độ tương hợp với Query cho mọi từ trong câu (thứ ta kiểm tra).
- $V$ (Value - Giá trị): Vector mang nội dung ngữ nghĩa thực sự của từ đó sẽ được giữ lại.
- $d_k$: Chiều không gian của vector Key, việc chia cho $\sqrt{d_k}$ giúp thu nhỏ phương sai của Tích vô hướng (dot product) tránh việc hàm softmax rơi vào vùng bão hòa gradient (gradient vanishing).
- Hàm $\text{softmax}$ đảm bảo ma trận trọng số luôn có phạm vi $[0, 1]$ và tổng phân bố là $1$.

## 3.2. Mô hình ngôn ngữ lớn (Large Language Models - LLM)
Khái quát về thành phần tạo nên "bộ não" suy luận của hệ thống.

### 3.2.1. Tổng quan và Bản chất dự đoán
Sự tiến hóa từ các mô hình biểu diễn ngữ nghĩa thành các LLM có khả năng suy luận mạnh mẽ là kết quả của việc gia tăng kích thước mạng nơ-ron và dữ liệu sinh văn bản (Causal Language Modeling). Bài toán cốt lõi của LLM là **Dự đoán token tiếp theo (Next-token Prediction)** dựa trên chuỗi từ đã có.
Xác suất tạo ra một câu chữ chiều dài $T$ được định nghĩa theo chuỗi phân phối xác suất có điều kiện:
$$ P(w_1, w_2, ..., w_T) = \prod_{t=1}^{T} P(w_t \mid w_1, ..., w_{t-1}) $$
Trong đó:
- $w_t$: Token mục tiêu tại vị trí $t$.
- $w_1, ..., w_{t-1}$: Các token tiền cảnh (context) đã được cung cấp (từ prompt sinh ra phía trước).
Mô hình sẽ chọn token tiếp theo thông qua việc lấy mẫu (Sampling) theo hàm phân phối xác suất này.

### 3.2.2. Kỹ thuật Prompt Engineering
Là quá trình thiết kế, điều chỉnh các chỉ thị đầu vào (prompt) nhằm định hướng LLM sinh ra câu trả lời theo ý muốn mà không phải đào tạo lại trọng số. Một số kỹ thuật cốt lõi:
- **Zero-shot**: Yêu cầu trả lời trực tiếp mà không cung cấp mẫu trước.
- **Few-shot learning**: Cung cấp một vài ví dụ input-output để mô hình nội suy quy luật.
- **Chain-of-Thought (CoT)**: Chỉ thị mô hình suy luận từng bước thay vì nhảy ngay ra kết quả cuối cùng (giúp giảm thiểu sai sót toán học/logic).

### 3.2.3. Khả năng gọi hàm (Function Calling / Tool Use)
Đây là đặc tính quan trọng giúp LLM kết nối với thế giới bên ngoài thay vì chỉ sinh text bị cô lập. Khi cấu hình một prompt đi kèm danh sách các "Tool", mô hình khi cần dữ liệu hoặc thực hiện thao tác sẽ tự động trả về chuỗi văn bản dạng cấu trúc (JSON) mô tả tên hàm và danh sách tham số (Arguments) thay vì sinh chuỗi text tự do.

### 3.2.4. Hạn chế "Ảo giác" (Hallucination) trong LLM
Bản chất của LLM là dự đoán chuỗi từ mang ý nghĩa tự nhiên nhất, chúng không "nhớ" thông tin theo các bản ghi chính xác. Vì thế, khi đối diện với thông tin chuyên ngành mới hoặc tự suy đoán sự kiện, LLM gặp ảo giác — sinh ra thông tin thoạt nhìn rất đáng tin cậy nhưng sai hoàn toàn sự thật. Nguyên nhân cốt lõi do dữ liệu đào tạo (out-of-date) và sự thiếu vắng nền tảng bám trụ kiến thức thực tế (lack of grounding). Điều này là căn cứ mạnh mẽ để đưa công nghệ RAG vào hệ thống.

## 3.3. Tăng cường sinh văn bản bằng truy xuất (Retrieval-Augmented Generation - RAG)
Thành phần quan trọng nhất giúp hệ thống trả lời chính xác dựa trên Sách giáo khoa trực tiếp.

### 3.3.1. Kiến trúc RAG cơ bản
Nguyên lý hoạt động cơ bản của RAG gồm 3 bước tuần tự: Truy xuất (Retrieval) - Bổ sung (Augmented) - Sinh văn bản (Generation). 
- **Pha Offline (Chuẩn bị dữ liệu)**: Tập hợp tải nội dung tài liệu, phân mảnh nhỏ (chunking), sau đó quy đổi mảnh bằng Embedding Model và lưu trữ vào Vector Database.
- **Pha Online (Truy vấn)**: Nhận câu hỏi thực, mã hóa vector câu hỏi đưa đi tìm kiếm chuỗi nội dung giống nhất (Retrieval), đưa đoạn văn bản kết quả thu được bổ sung vào Prompt hiện tại (Augmented) rồi đưa vào tính toán trả kết quả bởi LLM (Generation).

### 3.3.2. Tiền xử lý dữ liệu và Phân mảnh (Data Chunking)
Do các LLM có hạn chế về kích cỡ cửa sổ khung ngữ cảnh (Context Window), nguyên văn tài liệu bắt buộc phải được chia nhỏ (Chunking). Các chiến lược chia nhỏ thường gặp:
- **Fixed-size Chunking**: Cắt nội dung theo chuỗi số lượng token nhất định liên tiếp, có dải đè (overlap) để nối mạch văn.
- **Recursive Character Chunking**: Cắt theo phân cấp ngắt đoạn lô-gic như đoạn văn (\`\\n\\n\`), câu xuống dòng (\`\\n\`), khoảng trắng.
- **Hierarchical Chunking (Phân mảnh phân cấp)**: Rạch ròi dựa trên cấu trúc chương/mục nhằm gắn kết Metadata để duy trì cây tri thức vững chắc mà không làm đứt gãy luồng thông tin văn bản.

### 3.3.3. Cơ sở dữ liệu Vector (Vector Database)
Nơi lưu trữ Embeddings và ứng dụng các thuật toán tìm kiếm láng giềng gần nhất xấp xỉ (Approximate Nearest Neighbor - ANN) như độ thị **HNSW (Hierarchical Navigable Small World)** nhằm rà quét hàng triệu vector để tìm mảnh thông tin đối sánh chỉ trong vài mili-giây thay vì tìm toàn phần tĩnh.

## 3.4. Các kỹ thuật truy xuất thông tin nâng cao (Advanced Retrieval)
Đi sâu vào các thuật toán tối ưu hóa việc tìm kiếm tài liệu từ kho Sách giáo khoa (Corpus).

### 3.4.1. Tìm kiếm từ khóa (Lexical Search)
Thuật toán cơ sở dùng để tra cứu sự tương đồng phần chữ cái đối với từ khóa hiếm/chuyên ngành. Nổi bật là cơ chế **TF-IDF** (Term Frequency - Inverse Document Frequency).
**Công thức TF-IDF cơ bản**:
$$ TF\_IDF(t, d, D) = TF(t,d) \times IDF(t, D) $$
Trong đó:
- $TF(t, d) = \frac{f_{t,d}}{\sum_{t' \in d} f_{t', d}}$: Tần suất (mật độ) từ t xuất hiện trong văn bản d.
- $IDF(t, D) = \log \frac{N}{|\{d \in D : t \in d\}|}$: Cơ chế đo lường mức độ đặc trưng chuyên biệt với việc nghịch đảo số tài liệu liên quan ($N$ là tổng số văn bản).

Tuy nhiên, TF-IDF không có điểm trần và dễ bị thiên lệch chiều dài văn bản. Hiện tại phiên bản tiến tiến hơn được sử dụng là **BM25 (Best Matching 25)** với giới hạn tần suất:
$$ Score_{BM25}(Q, d) = \sum_{q_i \in Q} IDF(q_i) \cdot \frac{f(q_i, d) \cdot (k_1 + 1)}{f(q_i, d) + k_1 \cdot \left(1 - b + b \cdot \frac{|d|}{avgdl}\right)} $$
Trong đó:
- $Q$: Câu truy vấn bao gồm các từ khóa $q_i$.
- $f(q_i, d)$: Số lần xuất hiện từ khóa $q_i$ trong văn bản $d$.
- $|d|$ và $avgdl$: Chiều dài độ dài văn bản $d$ và trung bình cộng độ dài hệ thống.
- $k_1$ và $b$: Các siêu tham số tinh chỉnh độ dốc phạt do độ dài văn bản và trần bão hòa của tần suất điểm BM25.

### 3.4.2. Tìm kiếm theo ngữ nghĩa (Semantic Search)
Thay vì tìm từ khóa đúng chính tả xác khớp dạng rải rác, mô hình Bi-Encoder lưu cả Query lẫn Document dưới dạng một Vector Embedding duy nhất tách rẽ. Việc tìm kiếm dùng Tích vô hướng (Dot-Product) giúp nhặt tài liệu tương đồng nghĩa toàn cục dẫu không lặp chữ nào của gốc câu hỏi ban đầu.

### 3.4.3. Tìm kiếm lai (Hybrid Search) và RRF
Mục đích kết hợp sự chính xác ngữ pháp vựng từ BM25 và sự nhận thức khái niệm từ Vector Search (Semantic). **Reciprocal Rank Fusion (RRF)** là một thuật toán tích hợp ưu điểm của bảng xếp thứ hạng của hai chiến lược tìm kiếm.
Cách tính điểm RRF bù trừ của một đoạn tìm kiếm kết quả $d$:
$$ Score_{RRF}(d) = \frac{1}{k + rank_{BM25}(d)} + \frac{1}{k + rank_{Vector}(d)} $$
Trong đó:
- $rank_{BM25}(d)$, $rank_{Vector}(d)$: Trật tự xếp hạng của văn bản $d$ truy được dựa theo từng cơ chế.
- $k$: Hằng số giảm xóc (thường từ 60).

### 3.4.4. Cải thiện truy vấn (Query Optimization)
Tiền xử lý dùng nội tính của LLM nâng cao khả năng câu hỏi:
- **Query Rewriting (Viết lại truy vấn)**: Chuyển câu hỏi thô thành các keywords chuyên biệt bám bản thông tin tài liệu.
- **HyDE (Hypothetical Document Embeddings)**: Yêu cầu mô hình tưởng tượng (hallucinate) nội suy nhanh giả câu trả lời, sử dụng đoạn đó làm khung Vector đi tìm phần tham chiếu sát thực tiễn để tăng phần cover (độ phủ tìm kiếm).

### 3.4.5. Đánh giá xếp hạng lại (Reranking)
Thay Bi-Encoder bằng việc dùng **Cross-Encoder** đánh bảng điểm Top 10-20 về lại. Bi-Encoder Embedding lưu rẽ hai chuỗi làm chậm chạp thiếu nhạy bén trong ngữ cảnh. Khối Cross-Encoder cho trượt luôn cặp chuỗi ký tự Text gốc vào một lớp Self-Attention làm cho sự đánh giá trở nên cực kỳ tinh xác (tất nhiên chi phí truy vấn thời gian nhỉnh hơn bởi đối sánh chéo đôi). 

## 3.5. Hệ thống Đa tác tử (Multi-Agent Systems)
Lý thuyết phục vụ cho tính năng thiết kế Bài giảng, Slide hoặc cấu trúc Giáo án tự động.

### 3.5.1. Khái niệm hệ thống AI Agent
Triển khai môi trường nơi mà Agent lấy tư duy từ lõi LLM kèm hệ Tools (Công cụ tương tác được ra API hay code bên ngoài – ví dụ đọc code, gọi python tính, trích xuất wiki).

### 3.5.2. Khung lý thuyết ReAct (Reasoning and Acting)
Một vòng lặp giải bài toán chia tuần tự:
- **Thought (Tư duy)**: Nhận xét phương hướng tương ứng tiếp diễn.
- **Action (Hành động)**: Điều động chạy tham số gọi Tool cung cấp.
- **Observation (Quan sát)**: Kịch bản quan sát phản hồi kết xuất rồi chạy vòng nghĩ Thought để ra trả lời kết.

### 3.5.3. Mô hình điều phối Supervisor (Router)
Cho một Supervisor Agent đóng vai giám soát, nhận tin đầu vào và ra quyết định gửi yêu cầu chia nhiệm vụ trạm tuyến dưới.

### 3.5.4. Cơ chế thực thi song song (Fan-out / Fan-in)
Cách chia song song. (Phơi cử sub-agent tìm Mở Đầu độc lập với sub-agent tìm Bài Tập) và sau đó tổng kết dồn thông tin (Fan-in) quy tụ làm tiết kiệm mạnh chi phí chờ.

## 3.6. Framework Đánh giá hệ thống RAG (RAG Evaluation)
Cách đo lường và định lượng bằng số (Metrics) độ chính xác của hệ thống AI bằng các framework chuẩn (ví dụ RAGAS).

### 3.6.1. Mô hình LLM-as-a-Judge
Sử dụng LLM đóng vai giám khảo cho việc tính hệ số chính xác không can thiệp sức người.

### 3.6.2. Bộ khung đo lường RAG Triad
Khảo sát các thành phần chính để RAG không bị ảo giác:
- **Độ trung thực (Faithfulness / Groundedness):** Đảm bảo câu sinh từ Model bao nằm đủ bằng chứng trên text đã retrieve. 
  Công thức tính xấp xỉ tỉ lệ:
  $$ Faithfulness = \frac{| \text{số suy ý claims được support từ document} |}{| \text{tổng số claims có bên trong kết quả} |} $$
- **Chất lượng truy xuất (Context Precision & Recall):** Recall đánh giá đã mang đủ thông tin lấy về không còn Precision coi hạng giá trị cần để trích dẫn trên dòng đầu.
- **Mức độ liên quan (Answer Relevance):** Điểm cosin đối soát lại xem người trả lời có đúng không đi vòng trọng tâm người hỏi không.

