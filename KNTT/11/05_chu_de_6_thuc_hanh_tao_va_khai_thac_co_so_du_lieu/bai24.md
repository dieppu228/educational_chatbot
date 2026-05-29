# Bài 24: THỰC HÀNH SAO LƯU DỮ LIỆU

SAU BÀI HỌC NÀY EM SẼ:
* Nắm được các thao tác sao lưu và phục hồi dữ liệu.

Như đã biết, để tổ chức đảm bảo an toàn CSDL phục vụ công tác quản lí của một tổ chức, cần xây dựng chính sách an toàn dữ liệu với những kế hoạch về tất cả các phương án sự cố có thể xảy ra và giải pháp hạn chế, khắc phục. Chính sách an toàn dữ liệu cũng phải bao gồm những quy định về ý thức, trách nhiệm đối với những người vận hành hệ thống. Về giải pháp phần mềm, các hệ QTCSDL đều có chức năng hỗ trợ sao lưu dữ liệu dự phòng một cách thường xuyên theo quy định và phục hồi dữ liệu khi có sự cố. Có thể khai thác sử dụng nhóm chức năng này như thế nào?

## Nhiệm vụ 1. Thực hành sao lưu CSDL
Hướng dẫn:
* Nháy chuột chọn thẻ Các công cụ, chọn Xuất cơ sở dữ liệu dưới dạng SQL.
* Nháy chuột để đánh dấu vào CSDL mymusic ở phía trái và đánh dấu vào các ô Drop, có nghĩa là khi phục hồi CSDL thì xoá đối tượng cũ (nếu có) trước khi tạo đối tượng mới (Create).
* Ở dòng Data chọn Delete + Insert để khi phục phục hồi thì xoá dữ liệu cũ đi (nếu có) trước khi chèn vào dữ liệu đã sao lưu.

Tiếp theo, chọn kiểu output là 1 tệp các câu truy vấn SQL: Single.sql file. Nhập vào tên tệp sao lưu, ví dụ là C:\Temp\_mymusic.sql.
Chọn Export để thực hiện việc sao lưu.

- Cuối cùng là sao chép và lưu lại tệp _mymusic.sql.
Lưu ý: Cũng có thể thực hiện sao lưu một phần CSDL (một số bảng), bằng cách chỉ chọn những bảng muốn sao lưu.

## Nhiệm vụ 2. Thực hành phục hồi (restore) CSDL
Hướng dẫn:
Sau đây là một ví dụ phục hồi mymusic trên một máy mới, chưa có CSDL mymusic. Cũng có thể xoá CSDL mymusic đang có đi để thực hành khôi phục CSDL mymusic từ tệp sao lưu _mymusic.sql.

(Đoạn mã SQL minh họa việc xóa một cơ sở dữ liệu có tên `mymusic`)

*   Nháy chuột chọn thẻ **Tập tin**, chọn **Load SQL file**... (hoặc nhấn Ctrl+O).

*   Chọn tệp đã sao lưu là **_mymusic.sql**. Nháy chuột chọn Open. Nội dung tệp mymusic_data sẽ được tải vào cửa sổ truy vấn.
    Đoạn mã SQL hiển thị một tập hợp các lệnh để xóa (nếu tồn tại) và tạo lại cơ sở dữ liệu `mymusic` cùng với các bảng dữ liệu bên trong.

*   Nháy chuột chọn để thực hiện truy vấn. Sau đó nhấn **F5** để làm tươi lại danh sách CSDL. Khi đó CSDL `mymusic` đã được khởi tạo với đầy đủ các bảng.
    Đoạn mã hiển thị lệnh truy vấn danh sách các trigger trong CSDL `mymusic`.
    Đoạn mã hiển thị lệnh truy vấn các ràng buộc kiểm tra (CHECK CONSTRAINTS) của CSDL `mymusic`.

## LUYỆN TẬP
*   Thực hành sao lưu và phục hồi bảng **banthuam** của CSDL **mymusic**.

## VẬN DỤNG
*   Giả sử cần di chuyển một CSDL từ máy tính này sang máy tính khác, em sẽ làm thế nào?
