# Bài 21: THỰC HÀNH CẬP NHẬT VÀ TRUY XUẤT DỮ LIỆU CÁC BẢNG

SAU BÀI HỌC NÀY EM SẼ:
* Biết cách cập nhật và truy xuất CSDL.

Cập nhật và truy xuất dữ liệu là hai công việc chính khi làm việc với một CSDL. HeidiSQL hỗ trợ việc thực hiện các công việc đó như thế nào với những bảng đơn giản, không có khoá ngoại?

Nhiệm vụ. Cập nhật bảng nhacsi
Hướng dẫn:

## 1. THÊM MỚI DỮ LIỆU VÀO BẢNG NHACSI

Chọn bảng nhacsi, chọn thẻ Dữ liệu, em sẽ thấy bảng dữ liệu có hai trường idNhacsi và tenNhacsi nhưng chưa có dữ liệu.

Để thêm vào một hàng dữ liệu mới có thể nhấn phím **Insert** hoặc chọn biểu tượng + hay nháy nút phải chuột lên vùng dữ liệu của bảng và chọn **Chèn hàng**. Một hàng dữ liệu rỗng sẽ xuất hiện. Tiếp theo nháy đúp chuột vào từng ô trên hàng đó để nhập dữ liệu tương ứng cho từng trường.

Trường idNhacsi là có kiểu INT, AUTO_INCREMENT (tự động điền giá trị) nên không cần nhập dữ liệu cho trường này. Nháy đúp chuột vào ô ở cột tenNhacsi để nhập tên Nhạc sĩ, nhấn phím **Enter**, sau đó nhấn phím **Insert** để nhập hàng mới.

## 2. CHỈNH SỬA DỮ LIỆU TRONG BẢNG NHACSI

Tiếp tục thực hành nhập thêm dữ liệu để nắm vững những thao tác nhập dữ liệu.

Giả sử dữ liệu nhập có sai sót, cần sửa lại, chẳng hạn tên nhạc sĩ Hoàng Việt thiếu dấu tiếng Việt.

Em có thể nháy đúp chuột vào ô dữ liệu cần sửa và nhập lại.

## 3. XOÁ DÒNG DỮ LIỆU TRONG BẢNG NHACSI

Để xoá các dòng dữ liệu trong bảng **nhacsi**, hãy đánh dấu những dòng muốn chọn: giữ phím **Shift** và nháy chuột để chọn những dòng liền nhau hoặc nhấn giữ phím **Ctrl** và nháy chuột để chọn những dòng tách rời nhau.

Nhấn tổ hợp phím **Ctrl**+**Delete** trên bàn phím hoặc chọn biểu tượng để xoá. Phần mềm sẽ có lời nhắc yêu cầu khẳng định muốn xoá.

Nếu chắc chắn muốn xoá, nháy chuột chọn **OK**.

## 4. TRUY XUẤT DỮ LIỆU TỪ BẢNG NHACSI

### a) Truy xuất đơn giản

Để xem toàn bộ dữ liệu trong bảng nhacsi, chỉ cần chọn bảng nhacsi và thẻ Dữ liệu.
(Mô tả: Giao diện hiển thị bảng dữ liệu `nhacsi` với một câu lệnh SQL để chọn tất cả dữ liệu từ bảng `mymusic`.)

### b) Truy xuất và sắp xếp kết quả theo thứ tự

Nhìn trong danh sách dữ liệu kết xuất, có thể thấy bình thường dữ liệu được kết xuất theo thứ tự tăng dần của trường khoá chính **idNhacsi**. Nếu muốn kết xuất theo thứ tự giảm dần của **idNhacsi**, hãy nháy chuột vào ô **idNhacsi**. Hình tam giác màu đen sẽ xuất hiện và dữ liệu được kết xuất theo thứ tự giảm dần của **idNhacsi**.

### c) Tìm kiếm

Để lấy ra danh sách dữ liệu thoả mãn một yêu cầu nào đó có thể thực hiện các thao tác tạo bộ lọc: Nháy nút phải chuột vào vùng dữ liệu **tenNhacsi**, chọn **Quick Filter**, rồi chẳng hạn chọn LIKE “%...”. Nhập vào kí tự P.

Kết quả thu được như Hình 21.12 là danh sách hai nhạc sĩ và có chữ P trong tên.

– Để xoá bộ lọc chọn **Dọn dẹp** và **Lọc**.

## 5. TRUY XUẤT DỮ LIỆU VỚI CÂU TRUY VẤN SQL

Ngoài việc sử dụng các thao tác qua giao diện trực quan như đã hướng dẫn ở trên, cũng có thể nhập câu truy vấn SQL để truy xuất dữ liệu một cách linh hoạt hơn. Cấu trúc cơ bản câu truy vấn vào một bảng dữ liệu như sau:
Mô tả đoạn mã SQL: Đoạn mã này hiển thị cấu trúc cơ bản của một câu truy vấn SELECT trong SQL. Nó bao gồm việc chọn các trường (`danh_sách_các_trường`) từ một bảng (`tên_bảng`), có thể kèm theo điều kiện lọc (`biểu_thức_điều_kiện`) và sắp xếp kết quả theo một hoặc nhiều trường (`tên_trường`) theo thứ tự tăng dần (ASC) hoặc giảm dần (DESC).

Trong đó:
*   **danh_sách_các_trường**: liệt kê các tên trường ngăn cách nhau bởi dấu phẩy. Nếu muốn lấy tất cả các trường dùng kí tự `*`.
*   **tên_bảng**: khi làm việc với nhiều CSDL đồng thời, tên trường phải bao gồm cả tên CSDL, ví dụ: mymusic.bannhac.

– **biểu_thức_điều_kiện**: là biểu thức logic xác lập các điều kiện với các giá trị của các trường dữ liệu.
Ví dụ: `tenNhacsi LIKE 'P%' AND (idNhacsi=2 OR idNhacsi=6)`
Cặp dấu [ ] biểu thị nội dung bên trong nó là một lựa chọn có thể dùng hoặc không dùng.
**ASC | DESC**: nghĩa là ASC hoặc DESC. **ASC** là viết tắt của Ascending – tăng dần, **DESC** là viết tắt của Descending – giảm dần.
Ý nghĩa của câu truy vấn trên, với đủ các lựa chọn là: Lấy ra tất cả các dòng dữ liệu, mỗi dòng là giá trị của các trường trong `danh_sách_các_trường` từ bảng `tên_bảng` ở đó các giá trị thoả mãn `biểu_thức_điều_kiện`, kết quả truy vấn được sắp xếp theo thứ tự `tên_trường_1 [ASC | DESC]`, `tên_trường_2 [ASC | DESC]`.
Ví dụ:
Mã nguồn SQL này chọn ra `idNhacsi` và `tenNhacsi` từ bảng `nhacsi`, lọc những bản ghi có `tenNhacsi` bắt đầu bằng chữ 'P', và sắp xếp kết quả theo `tenNhacsi`.
```sql
SELECT idNhacsi, tenNhacsi
FROM nhacsi
WHERE tenNhacsi LIKE 'P%'
ORDER BY tenNhacsi;
```

Mở CSDL mymusic, chọn thẻ Truy vấn, nhập câu truy vấn trên và chọn Kết quả nhận được.

## LUYỆN TẬP

1.  Cập nhật dữ liệu vào bảng casi.
2.  Truy xuất dữ liệu bảng casi theo các tiêu chí khác nhau.

## VẬN DỤNG

Thực hành cập nhật và truy xuất dữ liệu bảng Tỉnh/Thành phố trong CSDL quản lí danh sách tên Quận/Huyện, Tỉnh/Thành phố.
