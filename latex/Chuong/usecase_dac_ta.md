# Bảng đặc tả Use Case (UC02-UC06)

## UC02 - Hỏi đáp kiến thức SGK

| Mục | Đặc tả |
|---|---|
| **Tên use case** | UC02 - Hỏi đáp kiến thức SGK |
| **Tác nhân** | User |
| **Tiền điều kiện** | (1) Hệ thống hoạt động bình thường; (2) Kho tri thức SGK đã được nạp; (3) User đang ở giao diện chat |
| **Luồng sự kiện chính** | 1) User nhập câu hỏi kiến thức. <br>2) Hệ thống phân tích ngữ cảnh hội thoại và nhận diện intent. <br>3) Hệ thống truy xuất tri thức (RAG) theo chủ đề/lớp/bộ sách. <br>4) Hệ thống sinh câu trả lời dựa trên ngữ cảnh truy xuất. <br>5) Hiển thị câu trả lời cho User. |
| **Luồng sự kiện phát sinh** | **A1:** Câu hỏi mơ hồ/phụ thuộc ngữ cảnh -> hệ thống sinh đa truy vấn để tăng chất lượng truy xuất. <br>**A2:** User chưa chọn bộ sách -> hệ thống yêu cầu bổ sung thông tin bộ sách trước khi trả lời. <br>**A3:** Không tìm thấy ngữ cảnh phù hợp -> hệ thống trả thông báo và gợi ý cách hỏi lại. |
| **Hậu điều kiện** | (1) Câu trả lời được trả về cho User; (2) Lịch sử hội thoại được cập nhật vào session; (3) Thông tin debug/trace được lưu |

## UC03 - Sinh câu hỏi/bài tập

| Mục | Đặc tả |
|---|---|
| **Tên use case** | UC03 - Khởi tạo bộ câu hỏi/bài tập |
| **Tác nhân** | User |
| **Tiền điều kiện** | (1) Hệ thống sẵn sàng; (2) Kho SGK khả dụng; (3) User cung cấp yêu cầu sinh câu hỏi |
| **Luồng sự kiện chính** | 1) User nhập yêu cầu tạo câu hỏi (chủ đề, dạng câu hỏi, số lượng). <br>2) Hệ thống nhận diện intent sinh câu hỏi. <br>3) Hệ thống truy xuất tri thức liên quan từ SGK. <br>4) Hệ thống sinh bộ câu hỏi theo định dạng yêu cầu. <br>5) Hiển thị danh sách câu hỏi cho User. |
| **Luồng sự kiện phát sinh** | **A1:** User không nêu rõ loại câu hỏi -> hệ thống dùng mặc định (ví dụ MCQ). <br>**A2:** User yêu cầu mức độ khó (planned) -> hệ thống điều chỉnh prompt sinh câu hỏi theo mức độ. <br>**A3:** User muốn chỉnh sửa/xuất file -> hệ thống mở rộng thao tác sau khi sinh. |
| **Hậu điều kiện** | (1) Bộ câu hỏi được tạo thành công hoặc trả lỗi có hướng dẫn; (2) Trạng thái quiz được lưu vào session để phục vụ chấm điểm/ôn tập tiếp theo |

## UC05 - Sinh slide bài giảng

| Mục | Đặc tả |
|---|---|
| **Tên use case** | UC05 - Sinh slide bài giảng |
| **Tác nhân** | User |
| **Tiền điều kiện** | (1) Hệ thống AI và RAG hoạt động; (2) User cung cấp chủ đề bài giảng; (3) Có thông tin lớp/bộ sách (hoặc xác định được tự động) |
| **Luồng sự kiện chính** | 1) User nhập yêu cầu sinh slide. <br>2) Hệ thống nhận diện intent tạo slide. <br>3) Hệ thống truy xuất tri thức SGK liên quan. <br>4) Supervisor gọi agent tạo outline. <br>5) Hệ thống sinh nội dung chi tiết từng slide. <br>6) (Tùy chọn) sinh media và câu hỏi luyện tập. <br>7) Hệ thống merge kết quả và kiểm tra chất lượng. <br>8) Trả bộ slide hoàn chỉnh cho User. |
| **Luồng sự kiện phát sinh** | **A1:** User duyệt/chỉnh sửa outline (HITL) trước khi tiếp tục sinh nội dung. <br>**A2:** Một agent phụ (media/quiz) lỗi -> hệ thống tiếp tục với output một phần (partial) nếu lõi vẫn đạt. <br>**A3:** Chưa có bộ sách -> hệ thống yêu cầu User bổ sung. |
| **Hậu điều kiện** | (1) Slide được tạo và hiển thị; (2) Dữ liệu slide lưu vào session; (3) Có thể tiếp tục chỉnh sửa/resume trong phiên hiện tại |

## UC06 - Sinh giáo án

| Mục | Đặc tả |
|---|---|
| **Tên use case** | UC06 - Sinh giáo án |
| **Tác nhân** | User |
| **Tiền điều kiện** | (1) Hệ thống hoạt động ổn định; (2) User cung cấp yêu cầu giáo án (chủ đề/lớp/mục tiêu) |
| **Luồng sự kiện chính** | 1) User nhập yêu cầu sinh giáo án. <br>2) Hệ thống nhận diện intent sinh giáo án. <br>3) Hệ thống truy xuất tri thức từ SGK. <br>4) Hệ thống tạo cấu trúc giáo án. <br>5) Hệ thống sinh nội dung chi tiết theo cấu trúc. <br>6) Trả giáo án cho User. |
| **Luồng sự kiện phát sinh** | **A1:** User yêu cầu tùy chỉnh độ dài/mức chi tiết -> hệ thống tái sinh nội dung theo tham số mới. <br>**A2:** User yêu cầu xuất định dạng Markdown/Text -> hệ thống thực hiện xuất file. <br>**A3:** Ngữ cảnh truy xuất chưa đủ -> hệ thống yêu cầu làm rõ chủ đề. |
| **Hậu điều kiện** | (1) Giáo án được sinh và trả về; (2) Nội dung được lưu vào session; (3) Sẵn sàng cho chỉnh sửa/xuất bản |
