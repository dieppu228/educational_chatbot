# Phân tích Usecase - Chương 2: Phân tích và Thiết kế hệ thống

Dựa trên các chức năng cốt lõi của Hệ thống Trợ lý Ảo hỗ trợ dạy và học môn Tin học, dưới đây là danh sách phân tích các Use case tổng quan, Use case phân rã và đề xuất các Use case quan trọng cần đặc tả chi tiết trong báo cáo đồ án.

## 1. Các Actor (Tác nhân) trong hệ thống
- **Học sinh (Student):** Người dùng sử dụng hệ thống để học tập, tra cứu kiến thức, làm bài tập và nhận đánh giá.
- **Giáo viên (Teacher):** Người dùng sử dụng hệ thống để hỗ trợ giảng dạy, tạo câu hỏi/bài tập, tạo dàn ý bài giảng.

*(Hệ thống tập trung phục vụ tối đa cho việc học và giảng dạy, mọi quy trình tác vụ bảo trì dữ liệu cốt lõi đã được xử lý ngầm, do đó **không có tác nhân Quản trị viên (Admin)**).*

---

## 2. Các Use case tổng quan và Phân quyền Tác nhân
Đây là các Use case mức cao (High-level Use cases) thể hiện các tính năng chức năng của hệ thống. Chúng được phân loại theo quyền truy cập của các Tác nhân và thể hiện các mối quan hệ bổ sung (`<<include>>`, `<<extend>>`):

### Tác nhân: Học sinh (Student)
Học sinh có thể truy cập các Use case phục vụ trực tiếp cho việc theo dõi, ôn tập và tự đánh giá kiến thức:
1. **UC01 - Quản lý phiên trò chuyện (Session Management):** Tạo mới, xem lại lịch sử hoặc xóa các phiên hội thoại.
2. **UC02 - Hỏi đáp kiến thức Giáo khoa (Knowledge Query):** Truy vấn thông tin trong cơ sở dữ liệu Sách giáo khoa (RAG).
   - *`<<include>>`*: **Truy xuất tài liệu (Retrieval):** Bắt buộc hệ thống phải tìm kiếm nội dung từ Vector DB trước khi trả lời.
   - *`<<extend>>`*: **Sinh đa truy vấn (Multi-Query/Question Rewriting):** Kích hoạt nếu câu hỏi phức tạp và hệ thống cần tối ưu ngữ nghĩa truy vấn.
3. **UC04 - Chấm điểm và chữa bài (Answer Scoring):** Gửi đáp án cho hệ thống và nhận lại điểm đánh giá cũng như diễn giải lỗi sai.

### Tác nhân: Giáo viên (Teacher)
Giáo viên có quyền thực hiện **toàn bộ các Use case của Học sinh**, đồng thời được cấp quyền các chức năng thiết kế nội dung hỗ trợ giảng dạy:
4. **UC03 - Khởi tạo bộ câu hỏi/bài tập (Quiz Generation):** Tự động sinh danh sách bài tập đa định dạng (Trắc nghiệm, tự luận, điền khuyết...).
   - *`<<include>>`*: **Truy xuất kiến thức (Retrieval):** Bắt buộc phải trích xuất kiến thức chuẩn từ SGK để tạo nội dung tránh ảo giác (Hallucination).
   - *`<<extend>>`*: **Xuất tập tin (Export Quiz):** Mở rộng tính năng cho phép Giáo viên tải câu hỏi về máy (file Text/Markdown).
5. **UC05 - Sinh cấu trúc bài giảng (Slide/Lesson Plan Generation):** Tạo dàn ý, phân rã cấu trúc slide giảng dạy dựa trên chủ đề yêu cầu.
   - *`<<extend>>`*: **Tùy chỉnh thông số đầu ra:** Mở rộng cho phép giáo viên chỉnh sửa độ chi tiết của cấu trúc bài giảng sinh ra.

---

## 3. Các Use case phân rã chi tiết
### Từ UC01 - Quản lý phiên trò chuyện
- UC01.1: Tạo phiên trò chuyện mới.
- UC01.2: Xem lại lịch sử các phiên trò chuyện cũ.
- UC01.3: Xóa phiên trò chuyện.
- UC01.4: Tải hội thoại xuống (Export chat).

### Từ UC02 - Hỏi đáp kiến thức Giáo khoa
- UC02.1: Nhập câu hỏi truy vấn kiến thức.
- UC02.2: Hệ thống truy xuất tài liệu (Retrieval) (Use case Extend/Include ẩn dươí hệ thống).
- UC02.3: Nhận câu trả lời kèm theo trích dẫn (Citation) từ SGK.

### Từ UC03 - Khởi tạo bộ câu hỏi/bài tập
- UC03.1: Chọn bộ sách, lớp và bài học cụ thể.
- UC03.2: Chọn mức độ khó (Nhận biết, Thông hiểu, Vận dụng).
- UC03.3: Chọn định dạng câu hỏi (Trắc nghiệm, Tự luận, Điền khuyết, Đúng/Sai).
- UC03.4: Chỉnh sửa hoặc xuất file danh sách câu hỏi.

### Từ UC04 - Chấm điểm và chữa bài
- UC04.1: Cung cấp câu trả lời hoặc file bài làm.
- UC04.2: Nhận kết quả đánh giá (Điểm số, Phân tích lỗi sai, Gợi ý sửa).

### Từ UC05 - Sinh cấu trúc bài giảng
- UC05.1: Nhập yêu cầu, chủ đề bài học cần tạo slide.
- UC05.2: Tùy chỉnh độ dài và chi tiết của cấu trúc bài giảng.
- UC05.3: Xuất dàn ý ra định dạng Markdown hoặc text.

---

## 4. Các Use case đặc tả chi tiết (Đề xuất)
Trong báo cáo Đồ án, không cần đặc tả toàn bộ tất cả các use case nhỏ. Bạn nên chọn các Use case thể hiện rõ nhất **độ phức tạp của hệ thống AI / RAG** để làm nổi bật tính học thuật của đồ án. Dưới đây là 3 Use case nên được chọn để vẽ luồng hoạt động (Activity Diagram), Sequence Diagram và viết đặc tả chi tiết:

### Ưu tiên 1 (Bắt buộc): Đặc tả Use case "Hỏi đáp kiến thức Giáo khoa (Từ yêu cầu đến câu trả lời)"
- **Lý do:** Đây là xương sống của đồ án, liên kết trực tiếp với kiến trúc RAG, Multi-Intent Agent, và quá trình Intent Routing. 
- **Các bước chính cần nêu trong đặc tả:** 
    1. Người dùng nhập câu hỏi.
    2. Hệ thống phân tích lịch sử, phân tích ý định (Intent Routing).
    3. Sinh truy vấn tối ưu (Query Rewriting).
    4. Tìm kiếm vector trong ChromaDB/VectorDB.
    5. Cung cấp bối cảnh (Context) cho LLM để tạo câu trả lời.
    6. Trả kết quả về cho người dùng.

### Ưu tiên 2: Đặc tả Use case "Khởi tạo bộ câu hỏi/bài tập tự động"
- **Lý do:** Thể hiện khả năng ứng dụng AI vào giáo dục tạo ra giá trị thiết thực. Chức năng này yêu cầu LLM phải tuân thủ Format (JSON, Markdown) và mức độ khó (Bloom's Taxonomy).
- **Các bước chính:** Người dùng nhập yêu cầu (Số câu, độ khó, dạng báo) -> Hệ thống lấy nội dung sách giáo khoa tương ứng -> LLM tạo câu hỏi theo prompt kỹ thuật chặt chẽ (Prompt Engineering, Few-shot) -> Hiển thị list bài tập.

### Ưu tiên 3: Đặc tả Use case "Chấm điểm và chữa bài chi tiết"
- **Lý do:** Thể hiện việc sử dụng AI không chỉ để sinh văn bản mà để đánh giá Logic. 
- **Các bước chính:** Người dùng gửi đáp án -> Hệ thống phân tích đáp án gốc trong nội dung bài học -> LLM thực hiện đóng vai trò Giám khảo (Evaluator) chấm chéo và chỉ ra lỗi sai.

---
*Ghi chú: Nếu hệ thống của bạn có tích hợp thêm chức năng của Admin như (Upload PDF/Markdown SGK mới, chunking, và embedding lại dữ liệu) thì hãy bổ sung thêm **Use case Quản trị Tri thức (Knowledge Base Management)** vào danh sách đặc tả.*