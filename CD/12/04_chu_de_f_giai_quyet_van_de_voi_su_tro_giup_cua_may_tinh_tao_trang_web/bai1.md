# Bài 1: LÀM QUEN VỚI NGÔN NGỮ ĐÁNH DẤU SIÊU VĂN BẢN

**Học xong bài này, em sẽ:**
*   Nhận biết được một số khái niệm chính của ngôn ngữ đánh dấu siêu văn bản: phần tử, thẻ mở, thẻ đóng.
*   Trình bày được cấu trúc của văn bản HTML.
*   Tạo được một trang web đơn giản bằng ngôn ngữ đánh dấu siêu văn bản.

Theo em, có ngôn ngữ chuyên dụng dùng để tạo trang web không?

## 1. Ngôn ngữ đánh dấu siêu văn bản

Thông thường, một **website** gồm một số **trang web tĩnh** và một số **trang web động**. **Trang web tĩnh** có nội dung không thay đổi mỗi khi người dùng truy cập. Ngược lại, nội dung **trang web động** có thể thay đổi tuỳ theo yêu cầu của người dùng. Tìm hiểu xong chủ đề này, em sẽ tạo được các trang web tĩnh.

Có nhiều cách để tạo trang web. Bên cạnh cách sử dụng phần mềm có sẵn như: Dreamweaver, Mobirise,..., em có thể tạo trang web bằng **ngôn ngữ chuyên dụng**. **Ngôn ngữ đánh dấu siêu văn bản** (**HyperText Markup Language – HTML**) là ngôn ngữ chuyên dụng dùng để tạo trang web.

Em hãy cho biết các thành phần trong trang chủ của website minh hoạ ở Hình 1.

Thông qua các phần tử của mình, HTML cho phép khai báo các thành phần của trang web như tiêu đề mục, đoạn văn, bảng biểu, hình ảnh, âm thanh và các siêu liên kết,...

# CHUYÊN ĐỀ 2 ỨNG DỤNG VẬT LÍ TRONG CHẨN ĐOÁN HÌNH ẢNH

## Tia X
* Tia X là những bức xạ điện từ có bước sóng trong khoảng từ 10⁻¹¹ m đến 10⁻⁸ m.
* Tia X được tạo ra bằng ống tia X.
* Có thể tăng cường độ tia X phát ra từ ống tia X bằng cách tăng cường độ dòng điện nung nóng cathode.
* Có thể điều khiển độ cứng của chùm tia X phát ra nhờ thay đổi hiệu điện thế giữa anode và cathode của ống tia X.
* Cường độ của chùm tia X song song giảm đi theo cùng một tỉ lệ mỗi khi chùm đi qua các độ dày bằng nhau của một chất:
  I = I₀ e⁻μx
* Tia X có nhiều ứng dụng trong khoa học kĩ thuật và đời sống.

## Tạo ảnh bằng tia X
* Để chụp ảnh bằng tia X, người ta chiếu chùm tia X vào phần cơ thể cần chụp, chùm tia xuyên qua được cho tác dụng lên phim ảnh, màn hình hoặc máy dò tia X.
* Để tạo được ảnh tia X có chất lượng cao và an toàn cho người, cần cải thiện độ sắc nét và độ tương phản của ảnh đồng thời cần giảm liều chiếu.
* Để tăng độ sắc nét của hình ảnh tia X, người ta điều chỉnh độ rộng của đối cathode, kích thước cửa sổ, độ song song của chùm tia X và dùng thiết bị hấp thụ những tia X phân tán.
* Để tăng độ tương phản ảnh các mô mềm chụp bằng tia X, người ta dùng các chất tương phản.

## Chụp cắt lớp
* Người ta khắc phục hạn chế của ảnh chụp bằng tia X – là một loại ảnh hai chiều, bằng máy chụp cắt lớp tạo ra ảnh ba chiều.
* Nguyên lí chụp cắt lớp: chùm tia X quay xung quanh phần cơ thể cần chụp, máy dò thu nhận thông tin và máy tính dùng thông tin này tạo thành ảnh ba chiều của đối tượng được chụp.

# Bài 1: Cấu trúc trang web

## 1. Phần tử head
Phần đầu của văn bản được xác định thông qua phần tử **head**. Nội dung phần tử **head** được viết trong cặp thẻ mở `<head>` và thẻ đóng `</head>`, dùng để khai báo tiêu đề trang web, các siêu dữ liệu mô tả thông tin về trang web. Siêu dữ liệu có thể gồm bảng mã kí tự, từ khoá tìm kiếm và các liên kết đến tài nguyên khác nhằm chỉ dẫn trình duyệt web trong việc phân tích và hiển thị kết quả. Tiêu đề trang web được viết trong cặp thẻ mở `<title>` và thẻ đóng `</title>` và sẽ được hiển thị trên tiêu đề của cửa sổ trình duyệt web. Các thông tin khác không hiển thị trong màn hình của sổ trình duyệt web.

## 2. Phần tử body
Phần thân của văn bản được xác định thông qua phần tử **body**. Nội dung của phần tử **body** được viết trong cặp thẻ mở `<body>` và thẻ đóng `</body>` sẽ được hiển thị trong màn hình của cửa sổ trình duyệt web như minh hoạ.

Thông thường, dòng đầu tiên của văn bản HTML là một chỉ dẫn cung cấp thông tin phiên bản HTML được sử dụng.

## 3. Ví dụ cấu trúc trang web cơ bản
Đoạn mã HTML minh họa một cấu trúc trang web cơ bản:
*   Dòng `<!DOCTYPE html>` chỉ dẫn đây là văn bản sử dụng phiên bản HTML5.
*   Toàn bộ nội dung văn bản nằm trong cặp thẻ `<html>` và `</html>`.
*   Phần đầu của văn bản HTML nằm trong cặp thẻ `<head>` và `</head>`.
    *   Trong đó, cặp thẻ `<title> Trang web đầu tiên </title>` khai báo tiêu đề của trang, và nội dung này sẽ hiển thị trong thanh tiêu đề của cửa sổ trình duyệt web.
    *   Thẻ `<meta charset="utf-8">` khai báo rằng văn bản sử dụng bảng mã kí tự utf-8.
*   Phần thân của văn bản HTML nằm trong cặp thẻ `<body>` và `</body>`.
    *   Trong phần thân có một đoạn văn bản `<p>Chủ đề F: Tạo trang web</p>`, là nội dung chính sẽ hiển thị trên trang web.

Kết quả khi mở văn bản HTML này bằng trình duyệt web:
*   Tiêu đề trang web hiển thị trên thanh tiêu đề của trình duyệt là: "Trang web đầu tiên".
*   Nội dung chính hiển thị trong cửa sổ trình duyệt là: "Chủ đề F: Tạo trang web".

# Thực hành tạo trang web đơn giản

Sử dụng phần mềm **Sublime Text** soạn văn bản HTML thuận tiện hơn so với việc dùng các phần mềm soạn văn bản được cài sẵn trên máy tính. Phần mềm Sublime Text cung cấp một số tính năng như: sử dụng màu sắc để phân biệt các phần tử, tự động điền thẻ đóng cho phần tử được khai báo, đánh số dòng văn bản HTML,...

## Yêu cầu 1: Cài đặt phần mềm Sublime Text.

### Hướng dẫn thực hiện:

*   Bước 1. Truy cập trang web `https://sublimetext.com`, chọn mục **Download**.
*   Bước 2. Chọn phiên bản phù hợp với hệ điều hành đang sử dụng và tải về máy tính.
*   Bước 3. Nháy đúp chuột vào tên tệp đã được tải về ở Bước 2. Khi trên màn hình xuất hiện cửa sổ với thông báo “Completing the Sublime Text Setup Wizard”, việc cài đặt Sublime Text đã kết thúc thành công.

## Yêu cầu 2: Sử dụng phần mềm Sublime Text để soạn một văn bản HTML sao cho khi mở văn bản bằng trình duyệt web, trên màn hình hiển thị dòng chữ: “Chủ đề F: Tạo trang web”.

### Hướng dẫn thực hiện:

*   Bước 1. Khởi động Sublime Text bằng cách nháy đúp chuột vào biểu tượng phần mềm.
*   Bước 2. Trong màn hình làm việc, soạn thảo nội dung văn bản HTML. Đoạn mã này là một cấu trúc HTML cơ bản, bao gồm thẻ khai báo `<!DOCTYPE html>`, thẻ `<html>` chứa toàn bộ nội dung trang. Bên trong thẻ `<head>` có tiêu đề trang `<title>` là "Trang web đầu tiên" và thiết lập bộ mã kí tự `<meta charset="utf-8">`. Phần nội dung hiển thị trên trình duyệt được đặt trong thẻ `<body>`, với một đoạn văn bản `<p>` chứa dòng chữ "Chủ đề F: Tạo trang web".
*   Bước 3. Chọn **File\Save**, ghi lưu tệp với tên “trangwebdautien.html”.
*   Bước 4. Mở tệp bằng trình duyệt web, xem kết quả.

## Luyện tập
Hãy truy cập website trường em và cho biết cấu trúc văn bản HTML của trang chủ website này.

Câu 1. Trong các khai báo cấu trúc văn bản HTML sau, khai báo nào đúng cú pháp?
A. `<html><head><title></title></head><body></body></html>`
B. `<html><head></head><body><title></title></body></html>`
C. `<html><head><title><body></body></title></head></html>`
D. `<html><body><title></title><head></head></body></html>`

Câu 2. Mỗi phát biểu sau đây về mục đích sử dụng của các phần tử là đúng hay sai?
a) Phần tử `body` dùng để khai báo phần nội dung sẽ hiển thị trên màn hình cửa sổ trình duyệt web.
b) Phần tử `head` dùng để khai báo thông tin về cấu trúc của trang web.
c) Phần tử `title` dùng để khai báo tiêu đề và thông tin tác giả soạn trang web.
d) Phần tử `html` để khai báo cấu trúc và nội dung của trang web.

Câu 3. Dưới đây là văn bản HTML do bạn Thiên Phúc soạn để tạo trang web nhưng có một số thẻ bị viết sai cú pháp. Em hãy tìm các lỗi cú pháp giúp Thiên Phúc.
Đoạn mã HTML dùng để tạo một trang web đơn giản với tiêu đề và nội dung, nhưng có một số lỗi cú pháp.

## Tóm tắt bài học
*   Văn bản HTML định nghĩa các phần tử để xác định nội dung và cấu trúc của trang web. Phần tử thường được khai báo bắt đầu bằng thẻ mở và kết thúc bằng thẻ đóng.
*   Các phần tử **html, head, body** là các thành phần cơ bản của văn bản HTML.
*   Văn bản HTML dễ dàng được tạo bằng các phần mềm hỗ trợ soạn thảo văn bản.
