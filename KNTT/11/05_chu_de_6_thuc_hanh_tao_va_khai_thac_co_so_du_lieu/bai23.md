# Bài 23: THỰC HÀNH TRUY XUẤT DỮ LIỆU QUA LIÊN KẾT CÁC BẢNG

## SAU BÀI HỌC NÀY EM SẼ:
* Hiểu được cách thức truy xuất dữ liệu qua liên kết các bảng.

Các bảng có thể có quan hệ với nhau, thể hiện qua **khoá ngoại**. Nhờ vậy có thể truy xuất dữ liệu từ các bảng khác theo mối quan hệ. Việc này sẽ được thực hiện cụ thể như thế nào trong giao diện của một hệ **QTCSDL**?

## Nhiệm vụ 1. Lập danh sách các bản nhạc với tên bản nhạc và tên tác giả

Hướng dẫn:
* Bảng bannhac có cấu trúc:
  `bannhac (idBannhac, tenBannhac, idNhacsi, idTheloai)`
  Trong số các trường này không có trường tenNhacsi. Làm thế nào lập được danh sách các bản nhạc cùng với tên nhạc sĩ sáng tác bản nhạc ấy?
  Tên nhạc sĩ nằm trong bảng nhacsi, lưu trữ ở trường **tenNhacsi**
  `nhacsi (idNhacsi, tenNhacsi)`
  Bảng bannhac có khoá ngoại là idNhacsi tham chiếu đến trường khoá chính idNhacsi của bảng nhacsi.

Để truy vấn hai bảng qua liên kết khoá, câu truy vấn SQL với mệnh đề JOIN có cấu trúc như sau:

Mô tả cấu trúc truy vấn SQL sử dụng mệnh đề JOIN:
`SELECT danh_sách_tên_trường_của_2_bảng`
`FROM tên_bảng_a INNER JOIN tên_bảng_b`
`ON tên_bảng_a.tên_trường_a = tên_bảng_b.tên_trường_b`
`[WHERE ...] `
`[ORDER BY ... ];`

Ví dụ: Để lấy ra danh sách các bản nhạc gồm **tenBannhac**, **tenNhacsi**, dùng câu truy vấn:

Mô tả câu truy vấn SQL để lấy danh sách bản nhạc và tên nhạc sĩ:
`SELECT bannhac.tenBannhac, nhacsi.tenNhacsi`
`FROM bannhac INNER JOIN nhacsi`
`ON bannhac.idNhacsi = nhacsi.idNhacsi;`

* Vào **HeidiSQL**, chọn CSDL mymusic, chọn thẻ **Truy vấn** và nhập vào câu truy vấn trên. Nhấn **F9** trên bàn phím hoặc nháy chuột vào biểu tượng ▶ hoặc nháy nút phải chuột, chọn **Chạy**.

*   Nếu muốn ở dữ liệu kết xuất có cả trường idNhacsi của bảng nhacsi nhằm có thể đối chiếu một cách tường minh cùng không khó, chỉ cần đổi tên hai trường (cùng tên) ở hai bảng để phân biệt.

Mã nguồn SQL thực hiện việc lựa chọn tên bài hát từ bảng `bannhac`, mã số nhạc sĩ từ bảng `bannhac` (đặt biệt danh là `idNS_BN`), mã số nhạc sĩ từ bảng `nhacsi` (đặt biệt danh là `idNS_NS`) và tên nhạc sĩ từ bảng `nhacsi`. Hai bảng này được liên kết bên trong (`INNER JOIN`) với nhau thông qua trường `idNhacsi`.

Lưu ý: HeidiSQL có hỗ trợ người dùng khi nhập các câu truy vấn theo các phương thức:
*   Dùng màu sắc để trợ giúp quan sát cú pháp của câu truy vấn (**syntax coloring**).
*   Mỗi khi người dùng nhập một tên bảng và dấu chấm (.), HeidiSQL sẽ hiển thị ngay danh sách các tên trường của bảng để người dùng lựa chọn.

## Hãy thực hành
* Lập danh sách bao gồm **idBannhac**, **tenBannhac**, **tenNhacsi** từ tất cả các bản nhạc có trong bảng **bannhac**.
* Lập danh sách bao gồm **idBannhac**, **tenBannhac** từ tất cả các bản nhạc của nhạc sĩ Đỗ Nhuận có trong bảng **bannhac**.

## Nhiệm vụ 2. Lập danh sách các bản thu âm với đủ các thông tin **idBanthuam**, **tenBannhac**, **tenCasi**
### Hướng dẫn:
Để truy vấn được nhiều hơn hai bảng theo liên kết khoá ngoài, hãy lặp lại mệnh đề **JOIN** trong câu truy vấn SQL theo cấu trúc như sau:
*Mô tả cấu trúc câu lệnh SQL sử dụng mệnh đề JOIN để truy vấn dữ liệu từ nhiều bảng theo liên kết khoá ngoài, bao gồm các thành phần SELECT, FROM, INNER JOIN với điều kiện ON, WHERE và ORDER BY.*
Trong đó **tên_bảng_x.tên_trường_x** là tên trường của bảng a hay bảng b.

## Nhiệm vụ 3. Tìm hiểu một chức năng của ứng dụng Quản lý dữ liệu âm nhạc
Qua giao diện trong Hình 23.4, em hãy tìm hiểu một chức năng của ứng dụng Quản lý dữ liệu âm nhạc, so sánh với những kiến thức vừa được học và cho nhận xét so sánh.

Cách tương tác với giao diện này tương tự như với giao diện Quản lý Bản nhạc ở Bài 22 (Hình 22.7), chỉ khác ở chỗ khi nhập bản thu âm, chỉ có thể chọn tên bản nhạc, tên ca sĩ từ hộp danh sách với những tên đã có trong CSDL. Danh sách các bản thu âm có đầy đủ các thông tin tường minh tên bản nhạc, tên nhạc sĩ và tên ca sĩ thể hiện.

Theo các em:
* Người sử dụng có cần biết, nhớ cấu trúc của bảng trong CSDL không?
* Giao diện trên có dễ hiểu, dễ sử dụng không?
* Hình thức nhập dữ liệu như vậy có hỗ trợ tính nhất quán dữ liệu không?

## LUYỆN TẬP
1. Lấy danh sách các bản thu âm với đầy đủ các thông tin, idBanthuam, tenBannhac, tenTheloai, tenNhacsi, tenCasi.
2. Lấy danh sách các bản thu âm với các thông tin idBanthuam, tenBannhac, tenTheloai, tenCasi các bản nhạc của nhạc sĩ Văn Cao.
3. Lấy danh sách các bản thu âm với các thông tin idBanthuam, tenBannhac, tenTacgia, tenTheloai các bản nhạc do ca sĩ Lê Dung thể hiện.
4. Lấy danh sách các bản thu âm với các thông tin idBanthuam, tenBannhac, tenTacgia, tenCasi các bản nhạc do ca sĩ Lê Dung thể hiện thuộc thể loại Nhạc trữ tình.

## VẬN DỤNG
* Thực hành truy xuất bảng Quận/Huyện qua liên kết với bảng Tỉnh/Thành phố.
