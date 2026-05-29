# Bài 8: HOÀN TẤT ỨNG DỤNG

Học xong bài này, em sẽ:
* Tạo được biểu mẫu điều hướng để làm giao diện khi mở ứng dụng.
* Hoàn tất một ứng dụng đơn giản, có thể sử dụng được.

Theo em, làm thế nào để một người không học Access cũng có thể sử dụng được các công cụ quản lí thư viện ta đã tạo ra trong các bài học?

## 1. Biểu mẫu điều hướng

Vùng điều hướng trong CSDL Access hiển thị tất cả đối tượng đã được tạo ra, trong đó có nhiều đối tượng không nên cho phép truy cập trực tiếp. Ví dụ: các bảng, các truy vấn. Người dùng có thể vô tình hay cố ý gõ nhập làm hỏng dữ liệu khi mở bảng dữ liệu hay chạy truy vấn.

Biểu mẫu điều hướng đơn giản là một giao diện có chứa các nút điều khiển (**control**) giúp điều hướng để người dùng dễ dàng chuyển đổi giữa các biểu mẫu và báo cáo khác nhau trong CSDL. Báo cáo chỉ hiển thị kết quả xuất ra thông tin, không cho phép sửa đổi được dữ liệu từ các bảng nguồn bên dưới. Biểu mẫu cho phép xem và gõ nhập dữ liệu, nhưng có tính năng khoá chặt một số trường dữ liệu cần bảo vệ, không cho phép sửa đổi.

Nếu người thiết kế muốn tạo một bàn điều khiển trung tâm (**switchboard**) giúp người dùng dễ dàng tìm thấy các đối tượng cụ thể đã dành cho họ, thì biểu mẫu điều hướng là giải pháp phù hợp.

### Thao tác tạo biểu mẫu điều hướng

Bước 1. Chọn **Create\Navigation** (trong nhóm Forms). Trong danh sách thả xuống có các mục chọn kèm biểu tượng rất dễ hình dung bố cục trống sẽ như thế nào.

Bước 2. Chọn một mục, ví dụ *Horizontal Tabs*. Trong vùng làm việc hiển thị biểu mẫu có bố cục đã chọn trong khung nhìn bài trí *Layout View*.

Bước 3. Khi biểu mẫu điều hướng đang mở trong khung nhìn bài trí, kéo các báo cáo hay biểu mẫu khác từ vùng điều hướng thả vào ô *Add New*. Biểu mẫu hay báo cáo đó sẽ lập tức xuất hiện trong vùng làm việc là ô hình chữ nhật đã dành sẵn. Có thể sử dụng ngay để nhập dữ liệu hay xem thông tin giống như khi mở nó từ vùng điều hướng. Thẻ của biểu mẫu, báo cáo sẽ hiển thị thay thế nút *Add New*.

## Thiết lập biểu mẫu điều hướng làm bàn điều khiển trung tâm của ứng dụng

Để khi mở CSDL trong cửa sổ Access thì biểu mẫu điều hướng sẽ hiển thị đầu tiên, che khuất toàn bộ vùng làm việc và vùng điều hướng, ta thực hiện như sau:

Bước 1. Nháy chọn **File\\Options** (ở cuối dải lệnh thả xuống). Access hiển thị cửa sổ để thiết lập nhiều lựa chọn chung cho toàn bộ phần mềm Access trên máy cá nhân hoặc riêng cho từng CSDL đang làm việc (**Current Database**).

Bước 2. Chọn **Current Database**.

Bước 3. Tìm mục **Display Form**. Hiện đang bỏ trống (none). Nháy mũi tên trỏ xuống để thả xuống danh sách các biểu mẫu đang có trong CSDL.

Bước 4. Chọn **Navigation Form** là tên biểu mẫu dự kiến làm bàn điều khiển trung tâm.

Bước 5. Có thể chọn thiết lập che khuất vùng điều hướng để người dùng không nhìn thấy các đối tượng khác đã có trong CSDL bằng cách: tìm mục **Navigation**; bỏ đánh dấu chọn trong ô *Display Navigation Pane*.

Đóng Access và khởi chạy lại tệp CSDL thì các thiết lập trên mới có hiệu lực. Người sử dụng chỉ cần nháy chuột lên các thẻ, giống như các nút lệnh, thì biểu mẫu, báo cáo sẽ mở để làm việc.

*Chú ý:* Nếu biết lập trình, có thể làm thêm một biểu mẫu đăng nhập (**login form**) yêu cầu cung cấp tên, mật khẩu; sau đó thiết lập để mở biểu mẫu đăng nhập trước tiên thay vì mở bàn điều khiển trung tâm.

Access tích hợp sẵn môi trường lập trình **VBA (Visual Basic for Application)**. Nháy chọn **Create**, ở cuối dải lệnh sẽ thấy nhóm lệnh **Macros & Code**. Nháy các nút lệnh để bắt đầu viết các câu lệnh.

## Thiết kế giao diện của ứng dụng quản lí thư viện trường

Dưới đây tóm tắt ngắn gọn vài điểm về quy trình tác nghiệp của thư viện và các biểu mẫu, báo cáo liên quan.

### a) Các biểu mẫu

*   (1) Bạn đọc đến thư viện tìm sách để mượn. Thao tác “tìm sách”: biểu mẫu **TìmSách** cho thông tin về sách có sẵn.
*   (2) Bạn đọc yêu cầu mượn một cuốn sách. Thao tác “cho mượn”: biểu mẫu **ChoMượn** để thủ thư cập nhật gồm các trường **Số thẻ, Mã sách, Ngày mượn** trong bảng **Mượn-Trả** và **Sẵn** có trong bảng **Sách**.
    Quy tắc nghiệp vụ cần tuân thủ: Bỏ đánh dấu cuốn sách vừa cho mượn là sẵn có.
*   (3) Bạn đọc đến trả một cuốn sách. Thao tác “nhận trả”: biểu mẫu để thủ thư cập nhật gồm các trường **Số thẻ, Mã sách, Ngày mượn, Ngày trả** trong bảng **Mượn-Trả** và **Sẵn** có trong bảng **Sách**.
    Quy tắc nghiệp vụ cần tuân thủ: Đánh dấu cuốn sách vừa nhận trả là sẵn có.
    Có thể thêm các biểu mẫu để nhập dữ liệu cho bảng **Bạn đọc**, bảng **Sách**. Có thể quy ước là khi nhập một cuốn sách mới vào kho sách thì trường **Sẵn** có mặc định nhận giá trị là Yes.
    Chú ý: Nếu biết lập trình, có thể thiết lập việc thực thi các quy tắc vừa nêu trên, tránh trường hợp làm sai, dữ liệu có mâu thuẫn, không nhất quán.

### b) Các báo cáo

*   (1) Thống kê hoạt động mượn trả, ví dụ theo tháng: báo cáo **MượnTrả-TheoTháng**.
*   (2) Báo cáo phân tích mượn trả theo tháng và theo loại sách: báo cáo **MượnTrả-Tháng-LoạiSách**.
    Có thể thêm những báo cáo thống kê khác, ví dụ thống kê theo bạn đọc và số đầu sách đã mượn.

### c) Bàn điều khiển trung tâm của ứng dụng quản lí thư viện trường
Một ví dụ thiết kế biểu mẫu điều hướng như sau:
*   Nhãn tiêu đề: "Thư viện Trường THPT..."
*   Bố cục: *Horizontal Tabs*.
*   Các thẻ đầu tiên là các biểu mẫu, sau đó là các báo cáo.

## 3 Thực hành tổng hợp
### Nhiệm vụ 1. Tạo và chỉnh sửa bài trí biểu mẫu điều hướng
a) Làm theo các bước hướng dẫn thao tác tạo biểu mẫu điều hướng.
b) Kéo thả các biểu mẫu và báo cáo từ vùng điều hướng vào các ô *Add New* theo bố cục như trong ví dụ đã nêu.
c) Đổi tiêu đề biểu mẫu điều hướng.
d) Đổi tên trong thẻ của các biểu mẫu, báo cáo. Ví dụ: *Tìm Sách, Cho Mượn, Nhận trả* (có khoảng trắng, có dấu tiếng Việt, kiểu dáng chữ,...).
Chú ý quan sát thấy tên đối tượng trong vùng điều hướng không thay đổi.

### Nhiệm vụ 2. Hoàn thiện biểu mẫu một bản ghi để nhập dữ liệu cho bảng Bạn đọc;
thử nhập dữ liệu cho trường Ảnh.

### Nhiệm vụ 3. Thử xuất ra một báo cáo.
Gợi ý: Mở báo cáo trong khung nhìn *Print Preview* sẽ thấy nhiều nút lệnh để in ra giấy, chuyển thành tệp *Excel*, chuyển thành tệp “*pdf*”....

Hoàn tất ứng dụng quản lí thư viện theo yêu cầu sử dụng thực tế.

## Luyện tập
**Câu 1. Biểu mẫu điều hướng dùng để làm gì và chứa những gì?**
**Câu 2. Thao tác thiết lập biểu mẫu điều hướng làm bàn điều khiển trung tâm của ứng dụng gồm mấy bước? Bắt đầu bằng thao tác nào?**

## Tóm tắt bài học
Những công việc chính để hoàn tất ứng dụng là:
*   Thiết kế giao diện, bài trí các nút lệnh phù hợp với quy trình nghiệp vụ quản lí CSDL và cung cấp dịch vụ.
*   Tạo một biểu mẫu điều hướng và thực hiện các thiết kế giao diện như trên, chỉnh sửa lại các nhãn tiêu đề, chạy thử kiểm tra.
*   Thiết lập biểu mẫu điều hướng làm bàn điều khiển trung tâm của ứng dụng.

# MỤC LỤC

* LỜI NÓI ĐẦU (trang 3)
* BẢNG GIẢI THÍCH THUẬT NGỮ (trang 4)

## CHỦ ĐỀ A
### MÁY TÍNH VÀ XÃ HỘI TRI THỨC
### THẾ GIỚI THIẾT BỊ SỐ – HỆ ĐIỀU HÀNH VÀ PHẦN MỀM ỨNG DỤNG
* Bài 1. Bên trong máy tính (trang 5)
* Bài 2. Khám phá thế giới thiết bị số thông minh (trang 10)
* Bài 3. Khái quát về hệ điều hành (trang 13)
* Bài 4. Thực hành với các thiết bị số (trang 19)
* Bài 5. Phần mềm ứng dụng và dịch vụ phần mềm (trang 24)

## CHỦ ĐỀ C
### TỔ CHỨC LƯU TRỮ, TÌM KIẾM VÀ TRAO ĐỔI THÔNG TIN
### TÌM KIẾM VÀ TRAO ĐỔI THÔNG TIN TRÊN MẠNG
* Bài 1. Lưu trữ trực tuyến (trang 28)
* Bài 2. Thực hành một số tính năng hữu ích của máy tìm kiếm (trang 33)
* Bài 3. Thực hành một số tính năng nâng cao của mạng xã hội (trang 36)
* Bài 4. Thực hành một số tính năng hữu ích của dịch vụ thư điện tử (trang 39)

## CHỦ ĐỀ D
### ĐẠO ĐỨC, PHÁP LUẬT VÀ VĂN HOÁ TRONG MÔI TRƯỜNG SỐ
### ỨNG XỬ VĂN HOÁ VÀ AN TOÀN TRÊN MẠNG
* Phòng tránh lừa đảo và ứng xử văn hoá trên mạng (trang 42)

## CHỦ ĐỀ F
### GIẢI QUYẾT VẤN ĐỀ VỚI SỰ TRỢ GIÚP CỦA MÁY TÍNH
### GIỚI THIỆU CÁC HỆ CƠ SỞ DỮ LIỆU
* Bài 1. Bài toán quản lí và cơ sở dữ liệu (trang 47)
* Bài 2. Bảng và khoá chính trong cơ sở dữ liệu quan hệ (trang 52)
* Bài 3. Quan hệ giữa các bảng và khoá ngoại trong cơ sở dữ liệu quan hệ (trang 57)
* Bài 4. Các biểu mẫu cho xem và cập nhập dữ liệu (trang 62)
* Bài 5. Truy vấn trong cơ sở dữ liệu quan hệ (trang 67)
* Bài 6. Truy vấn trong cơ sở dữ liệu quan hệ (tiếp theo) (trang 71)
* Bài 7. Các loại kiến trúc của hệ cơ sở dữ liệu (trang 76)
* Bài 8. Bảo vệ sự an toàn của hệ CSDL và bảo mật thông tin trong CSDL (trang 81)

## CHỦ ĐỀ G
### HƯỚNG NGHIỆP VỚI TIN HỌC
### GIỚI THIỆU NGHỀ QUẢN TRỊ CƠ SỞ DỮ LIỆU
* Nghề quản trị cơ sở dữ liệu (trang 84)

## CHỦ ĐỀ E FICT
### ỨNG DỤNG TIN HỌC
### PHẦN MỀM CHỈNH SỬA ẢNH VÀ LÀM VIDEO
* Bài 1. Một số thao tác chỉnh sửa ảnh và hỗ trợ chỉnh sửa ảnh (trang 89)
* Bài 2. Tẩy xoá ảnh (trang 94)
* Bài 3. Tạo ảnh động (trang 100)
* Bài 4. Giới thiệu phần mềm làm video (trang 106)
* Bài 5. Chỉnh sửa video (trang 112)
* Bài 6. Làm phim hoạt hình (trang 118)
* Bài 7. Thực hành tổng hợp (trang 124)

## CHỦ ĐỀ F FICT
### GIẢI QUYẾT VẤN ĐỀ VỚI SỰ TRỢ GIÚP CỦA MÁY TÍNH
### THỰC HÀNH TẠO VÀ KHAI THÁC CƠ SỞ DỮ LIỆU
* Bài 1. Làm quen với Microsoft Access (trang 127)
* Bài 2. Tạo bảng trong cơ sở dữ liệu (trang 133)
* Bài 3. Liên kết các bảng trong cơ sở dữ liệu (trang 139)
* Bài 4. Tạo và sử dụng biểu mẫu (trang 144)
* Bài 5. Thiết kế truy vấn (trang 150)
* Bài 6. Tạo báo cáo đơn giản (trang 156)
* Bài 7. Chỉnh sửa các thành phần giao diện (trang 161)
* Bài 8. Hoàn tất ứng dụng (trang 167)
