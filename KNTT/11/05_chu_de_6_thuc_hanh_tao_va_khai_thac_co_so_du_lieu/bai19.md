# Bài 19: THỰC HÀNH TẠO LẬP CƠ SỞ DỮ LIỆU VÀ CÁC BẢNG

SAU BÀI HỌC NÀY EM SẼ:
*   Biết tạo mới một CSDL, thực hiện thông qua giao diện của phần mềm khách quản trị CSDL HeidiSQL.
*   Tạo được các bảng không có khoá ngoại, chỉ định được khoá chính cho mỗi bảng, khoá cấm trùng lặp cho những trường không được có giá trị trùng lặp.

Việc đầu tiên để làm việc với một CSDL là tạo lập. Với HeidiSQL, việc tạo lập CSDL và các bảng đơn giản được thực hiện như thế nào?

Nhiệm vụ. Tạo lập CSDL mới tên là **mymusic**, khởi tạo bảng **nhacsi**, khai báo các khoá cho các bảng này như thiết kế ở Bài 18.
Hướng dẫn:

## 1. TẠO LẬP CSDL MYMUSIC
Nháy nút phải chuột ở vùng danh sách các CSDL đã có, chọn thẻ Tạo mới, chọn Cơ sở dữ liệu. Nhập mymusic, chọn OK.
Bộ mã kí tự mặc định là **Unicode 4 byte: utf8mb4**, đối chiếu so sánh xâu theo **utf8mb4_general_ci**.
Ở vùng mã lệnh phía dưới sẽ thấy xuất hiện câu truy vấn SQL tương ứng:
Đoạn mã SQL tạo cơ sở dữ liệu có tên mymusic với bộ mã kí tự và đối chiếu quy định.

## 2. TẠO LẬP BẢNG
### a) Khai báo tạo lập bảng, các trường và kiểu dữ liệu
Tạo lập bảng **nhacsi** (**idNhacsi**, **tenNhacsi**), **idNhacsi** kiểu INT **tenNhacsi** kiểu VARCHAR (255).
Nháy nút phải chuột ở vùng danh sách các CSDL đã có, chọn thẻ Tạo mới, chọn Bảng. Nhập tên: nhacsi, chọn Thêm mới để thêm trường. Một trường với tên mặc định Column1 sẽ xuất hiện phía dưới.

Nhập Tên: **idNhacsi**, chọn kiểu dữ liệu **INT**, bỏ đánh dấu ô Allow NULL.

Chọn **AUTO_INCREMENT**, dưới nhãn Mặc định và chọn **OK**, để có kết quả như Hình 19.4.

Để thêm khai báo trường tiếp theo, nhấn **Ctrl+Insert** hoặc nháy nút phải chuột vào phần dưới dòng idNhacsi và chọn **Add column**.
Nhập: **tenNhacsi**, chọn kiểu **VARCHAR**, độ dài 255, giá trị mặc định là kí tự rỗng "".

### b) Khai báo khoá chính

Ấn định **idNhacsi** là khoá chính: Nháy nút phải chuột vào dòng khai báo **idNhacsi** và chọn **Create new index** → **PRIMARY**.

Cần phải làm gì trong trường hợp chọn nhầm trường làm khoá chính, chẳng hạn chọn nhầm trường **tenNhacsi** như Hình 19.7?

Để sửa khoá chính đã khai báo nhầm này, hãy nháy đúp chuột vào ô tenNhacsi ở dưới ô PRIMARY KEY ở phần trên và chọn lại idNhacsi:

Sau đó nháy chuột vào ô bên cạnh dưới ô PRIMARY.

### c) Lưu kết quả

Cuối cùng chọn **Lưu** để lưu lại khai báo bảng nhacsi. Ở vùng hiển thị phía trái sẽ xuất hiện tên bảng nhacsi dưới dòng tên CSDL mymusic.

## LUYỆN TẬP

Khai báo tạo lập bảng casi như thiết kế ở Bài 18.

## VẬN DỤNG

Hãy lập CSDL quản lí tên các Quận/Huyện, Tỉnh/Thành phố của Việt Nam. Tạo bảng Tỉnh/Thành phố.
