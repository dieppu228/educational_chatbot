# Bài 20: THỰC HÀNH TẠO LẬP CÁC BẢNG CÓ KHOÁ NGOÀI

SAU BÀI HỌC NÀY EM SẼ:
*   Biết cách tạo mới các bảng có khoá ngoài.

Các em đã biết, khoá ngoài có tác dụng liên kết dữ liệu giữa các bảng. Khi tạo bảng có khoá ngoài, việc thiết lập khoá ngoài được thực hiện như thế nào?

Nhiệm vụ. Tạo lập bảng bannhac với cấu trúc:
*   bannhac (idBannhac, tenBannhac, idNhacsi),
*   Các trường idBannhac, idNhacsi kiểu INT,
*   Trường tenBannhac kiểu VARCHAR (255).
Hướng dẫn:

## 1. KHAI BÁO BẢNG BANNHAC VỚI CÁC TRƯỜNG IDBANNHAC, TENBANNHAC

Chọn thẻ **Tạo mới**, chọn **Bảng**. Nhập tên: **bannhac**, chọn **Thêm mới** để thêm trường dữ liệu, một trường với tên mặc định Column1 sẽ xuất hiện phía dưới.

Phần mã nguồn hiển thị thông tin về các ràng buộc và sử dụng khóa trong cơ sở dữ liệu 'mymusic'.

Nhập tên: **idBannhac**, chọn kiểu dữ liệu **INT**, bỏ đánh dấu ô **Allow NULL**, nháy chuột vào ô **No default** để chọn giá trị mặc định là **AUTO_INCREMENT**.

(Giao diện hiển thị quá trình khai báo trường `idBannhac` với kiểu dữ liệu `INT` và thuộc tính `AUTO_INCREMENT` được bật.)

Để khai báo thêm trường tiếp theo, nhấn **Ctrl+Insert** hoặc nháy nút phải chuột vào phần dưới dòng `idBannhac` và chọn **Add column**.

Nhập: **tenBannhac**, chọn kiểu **VARCHAR**, độ dài **255**, giá trị mặc định là "kí tự rỗng".

(Giao diện hiển thị quá trình khai báo trường `tenBannhac` với kiểu dữ liệu `VARCHAR` có độ dài 255 và giá trị mặc định là chuỗi rỗng.)

## 2. KHAI BÁO CÁC TRƯỜNG LÀ KHOÁ NGOÀI

Các trường là **khoá ngoài** của bảng là các trường tham chiếu đến một trường khoá chính (k) của một bảng khác vì vậy cần được khai báo giá trị mặc định phù hợp với giá trị tương ứng của k.

Ví dụ, bảng **bannhac**, trường **idNhacsi** tham chiếu đến trường **idNhacsi** (kiểu INT) của bảng **nhacsi** nên giá trị của trường này cũng là **INT** và giá trị mặc định là một số nguyên, chẳng hạn là 0.

(Giao diện hiển thị cấu trúc bảng `bannhac` với các trường `idBannhac`, `tenBannhac` và `idNhacsi` đã được khai báo, trong đó `idNhacsi` là trường sẽ là khoá ngoài.)

## 3. KHAI BÁO CÁC TRƯỜNG KHOÁ

### a) Khai báo khoá chính: idBannhac

Nháy nút phải chuột vào ô idBannhac, chọn Creat new index, chọn **PRIMARY**.

### b) Khai báo khoá chống trùng lặp

Cặp (tenBannhac, idNhacsi) không được trùng lặp giá trị nên phải khai báo khoá cấm trùng lặp. Đánh dấu hai trường này, nháy nút phải chuột vào vùng đánh dấu và chọn Create new index, chọn **UNIQUE**.

### c) Khai báo các khoá ngoài

Để khai báo khoá ngoài idNhacsi, chọn thẻ Foreign Key.

Hình 20.7. Khai báo khoá ngoài

Nháy chuột vào ô dưới dòng Columns và chọn trường khoá ngoài là idNhacsi rồi chọn OK.

Hình 20.8. Chọn trường là khoá ngoài

Nháy chuột vào ô phía dưới Reference table để chọn bảng tham chiếu là nhacsi và chọn OK.

Tiếp theo chọn trường tham chiếu trong bảng nhacsi.
Cuối cùng nháy chuột chọn Lưu để kết thúc khai báo và khởi tạo bảng bannhac.

## LUYỆN TẬP
Hãy tạo lập bảng banthuam.

## VẬN DỤNG
Hãy tạo lập bảng Quận/Huyện trong CSDL quản lí tên Quận/Huyện, Tỉnh/Thành phố.
