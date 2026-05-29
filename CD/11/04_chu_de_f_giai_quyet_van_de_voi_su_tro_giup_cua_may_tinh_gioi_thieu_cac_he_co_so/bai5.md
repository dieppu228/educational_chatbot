# Bài 5: TRUY VẤN TRONG CƠ SỞ DỮ LIỆU QUAN HỆ

## Học xong bài này, em sẽ:

*   Diễn đạt được **khái niệm truy vấn CSDL**.
*   Giải thích được cấu trúc cơ bản SELECT...FROM...WHERE... của câu lệnh SQL.
*   Nêu được một vài ví dụ minh họa việc dùng truy vấn để tổng hợp, tìm kiếm dữ liệu trên một bảng.

Em hãy nêu một vài ví dụ cụ thể về khai thác thông tin trong một CSDL mà em biết.

## 1. Khái niệm truy vấn CSDL

**Truy vấn CSDL (Query)** là một phát biểu thể hiện yêu cầu của người dùng đối với CSDL. Đó có thể là yêu cầu thao tác trên dữ liệu như: thêm, sửa, xoá bản ghi,... Đó cũng có thể là yêu cầu khai thác CSDL. Dù đơn giản hay phức tạp thì bản chất việc **khai thác một CSDL** là tìm kiếm dữ liệu đã lưu giữ trong đó và hiển thị kết quả theo khuôn dạng thuận lợi cho người khai thác.

Để máy tính có thể hiểu và thực thi được yêu cầu của người dùng, truy vấn phải được viết theo một số quy tắc của hệ quản trị CSDL. Nói cách khác, mỗi hệ quản trị CSDL có ngôn ngữ truy vấn của nó. Đối với các hệ quản trị CSDL quan hệ, ngôn ngữ truy vấn phổ biến nhất và nổi tiếng nhất cho đến nay là **SQL (Structured Query Language)**. Hầu hết các hệ quản trị CSDL quan hệ, ngay cả những hệ thống có ngôn ngữ của riêng chúng, đều hỗ trợ một số phiên bản SQL. Bài học này tập trung vào việc dùng SQL thể hiện yêu cầu tìm và trích rút dữ liệu trong CSDL.

Chẳng hạn, giáo viên chủ nhiệm cần danh sách những học sinh của lớp có điểm tổng kết môn Tin học từ 8,0 trở lên. Tuỳ theo hệ quản trị CSDL, có thể có những truy vấn tóm tắt dữ liệu và thực hiện một số phép tính trên dữ liệu để đưa ra kết quả. Với những truy vấn như vậy, kết quả trả ra có thể là hình ảnh, đồ thị, ví dụ như kết quả của yêu cầu phân tích xu hướng mua/bán một mặt hàng trong 6 tháng đầu năm của một công ty thương mại.

## Khai thác CSDL bằng câu truy vấn SQL đơn giản

Em hãy quan sát mẫu câu truy vấn ở Hình 1a dùng để tìm dữ liệu trong CSDL và một ví dụ truy vấn ở Hình 1b. Muốn tìm Họ và tên, Ngày sinh, điểm môn Toán và điểm môn Ngữ văn của những học sinh có điểm môn Toán trên 7.0 thì em sẽ dùng câu truy vấn SQL như thế nào?

Cấu trúc cơ bản của một câu truy vấn viết bằng ngôn ngữ SQL như ở Hình 1a:

*   **SELECT**: Dùng để chỉ ra **tên các trường dữ liệu** cần được hiển thị trong kết quả.
*   **FROM**: Dùng để chỉ ra **tên bảng** trong CSDL mà từ đó dữ liệu được truy cập.
*   **WHERE**: Dùng để chỉ ra **biểu thức logic** để chọn lọc các bản ghi phù hợp đưa ra kết quả.

Một ví dụ về câu truy vấn SQL (tương tự Hình 1b):
*   Chọn các trường **Mã định danh**, **Họ và tên**, **Toán**, **Ngữ văn**.
*   Từ bảng **HỌC SINH 11**.
*   Với điều kiện **Ngữ văn** >= 7.0.

Để có kết quả của câu truy vấn, hệ quản trị CSDL sẽ truy cập vào các bảng dữ liệu có tên được chỉ ra sau **FROM**. Các bản ghi thoả mãn điều kiện tìm kiếm đứng sau **WHERE** sẽ được lựa chọn. Kết quả câu truy vấn là những bản ghi đã được lựa chọn và chỉ giá trị của những trường có tên đứng sau **SELECT** mới được hiển thị.

Chú ý: Khi thực hiện các câu truy vấn, hệ quản trị CSDL sẽ coi tên trường là biến trong chương trình xử lí, do vậy, nếu tên trường có chứa dấu cách thì cần phải dùng các dấu **[]** để đánh dấu bắt đầu và kết thúc tên trường.

Để dễ theo dõi các ví dụ về câu truy vấn trong mục này, CSDL nói đến ở các ví dụ có bảng **HỌC SINH 11** với dữ liệu như ở Hình 2.

Ví dụ 1. Để tìm Mã định danh, Họ và tên, điểm môn Toán và điểm môn Ngữ văn của những học sinh có điểm môn Ngữ văn từ 7.0 trở lên thì cần dùng truy vấn SQL như trong Hình 1b. Kết quả nhận được từ truy vấn đó sẽ như trong Hình 3.

Kết quả của câu truy vấn hiển thị thông tin về Mã định danh, Họ và tên, điểm Toán và điểm Ngữ văn của các học sinh có điểm Ngữ văn từ 7.0 trở lên. Ví dụ, học sinh Phan Thuỷ Anh có điểm Toán 7.3, Ngữ văn 7.4; Lê Minh Đức có Toán 6.4, Ngữ văn 7.2; Hoàng Giang có Toán 7.7, Ngữ văn 7.6; và Nguyễn Minh Trí có Toán 9.0, Ngữ văn 7.0.

### Ngôn ngữ truy vấn QBE

Có những hệ quản trị CSDL cho phép truy vấn bằng cách điền vào chỗ trống trong một bảng, như thế hiện một ví dụ về kết quả cần nhận được (nên ngôn ngữ truy vấn này là **Query By Example – QBE**). Access là một hệ quản trị CSDL cho truy vấn bằng cả SQL và QBE.

Ví dụ 2. Tương ứng với câu truy vấn SQL ở Hình 1b, ta có thể điền vào bảng thiết kế QBE của Access như ở Hình 4 dưới đây:

Bảng thiết kế QBE (Query By Example) trong Access cho phép người dùng xây dựng truy vấn bằng cách điền thông tin vào một lưới. Trong ví dụ này, truy vấn được thiết lập để chọn các trường `Mã định danh`, `Họ và tên`, `Toán` và `Ngữ Văn` từ bảng `HỌC SINH 11`. Trường `Ngày sinh` cũng được liệt kê nhưng không được chọn hiển thị trong kết quả. Điều kiện được áp dụng là `Ngữ Văn >= 7.0`, nghĩa là chỉ những bản ghi có giá trị trường `Ngữ Văn` từ 7.0 trở lên mới được đưa vào kết quả của truy vấn. Điều này cho biết trường Mã định danh xuất hiện trong kết quả truy vấn, còn trường Ngày sinh không xuất hiện trong kết quả truy vấn.

## Luyện tập

*   Câu 1. Hãy viết câu truy vấn SQL để tìm điểm môn Ngữ văn của những học sinh là Đoàn viên trong bảng HỌC SINH 11 (Hình 2). Kết quả của câu truy vấn là gì?
*   Câu 2. Hình bên là một câu truy vấn SQL được viết để tìm dữ liệu trong CSDL Thư viện (Hình 2 Bài 3). Theo em, người viết truy vấn đó muốn tìm biết gì?

Đoạn mã SQL này có chức năng chọn các trường `Mã sách`, `Tên sách`, và `Số trang` từ bảng `SÁCH` với điều kiện trường `Tác giả` phải là "Nguyễn Nhật Ánh".

Hãy nêu một yêu cầu tìm thông tin trong bảng HỌC SINH 11 và viết câu truy vấn SQL để có được thông tin cần tìm.

Trong các câu sau, những câu nào đúng?
a) Truy vấn CSDL là một biểu mẫu.
b) Có thể dùng các câu truy vấn để tìm kiếm dữ liệu trong CSDL.
c) SQL là ngôn ngữ truy vấn thường được dùng trong các hệ CSDL quan hệ.
d) Trong câu truy vấn SQL, sau từ khoá FROM là tên của bảng dữ liệu nguồn cho các trích xuất dữ liệu.

## Tóm tắt bài học

*   Đối với các hệ CSDL quan hệ, có hai loại truy vấn dữ liệu: **truy vấn cập nhật dữ liệu** và **truy vấn khai thác dữ liệu**.
*   Ngôn ngữ truy vấn phổ biến nhất trong các hệ quản trị CSDL quan hệ là **SQL**. Câu truy vấn khai thác dữ liệu của SQL có cấu trúc cơ bản là **SELECT...FROM...WHERE...**.
*   Mệnh đề **SELECT** xác định thông tin ta muốn hiển thị; mệnh đề **FROM** xác định dữ liệu được lấy từ đâu; mệnh đề **WHERE** xác định điều kiện lọc dữ liệu.
*   Trong một số hệ quản trị CSDL, truy vấn còn có thể được thể hiện bằng ngôn ngữ **QBE**.

## BÀI ĐỌC THÊM
### VÀI NÉT VỀ CSDL NoSQL
Vào cuối những năm 2000 xuất hiện các **CSDL NoSQL**. Một số người quen dùng truy vấn SQL trong các hệ CSDL quan hệ có thể suy đoán rằng CSDL NoSQL là CSDL không dùng truy vấn **SQL**. Thực ra "NoSQL" trong tên gọi đó nên được hiểu là “Không chỉ SQL” (**Not Only SQL**). Các hệ **CSDL NoSQL** ra đời là để lưu trữ và xử lí lượng dữ liệu tăng rất nhanh trong nhiều ứng dụng, đặc biệt là các ứng dụng web. Khác với các CSDL quan hệ truyền thống, **CSDL NoSQL** hỗ trợ nhiều kiểu lưu trữ dữ liệu khác nhau tuỳ thuộc vào ứng dụng cụ thể thay vì sử dụng cấu trúc chặt chẽ dạng bảng. Một số hệ **CSDL NoSQL** có thể sử dụng cú pháp giống **SQL** để làm việc với dữ liệu nhưng chỉ ở một mức độ hạn chế. **CSDL NoSQL** nới lỏng ràng buộc và tính nhất quán dữ liệu để đạt tốc độ nhanh trong phục vụ, tính linh hoạt cũng như khả năng mở rộng quy mô phục vụ. CSDL quan hệ và CSDL NoSQL, mỗi loại có cách lưu trữ và truy xuất dữ liệu khác nhau, được thiết kế để giải quyết các loại nhu cầu khác nhau do các ứng dụng CSDL đòi hỏi.
