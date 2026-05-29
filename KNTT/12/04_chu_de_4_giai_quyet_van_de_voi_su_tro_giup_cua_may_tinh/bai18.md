# Bài 18: THỰC HÀNH TỔNG HỢP THIẾT KẾ TRANG WEB

## SAU BÀI HỌC NÀY EM SẼ:
* Tạo được trang web bằng html và định dạng bằng CSS.

Giả sử website của em có nhiều tệp html. Có thể hay không chỉ dùng một tệp CSS duy nhất để định dạng cho toàn bộ các trang web? Nếu có thể hãy nêu các bước cần thực hiện.

## 1. DỰ ÁN: XÂY DỰNG WEBSITE GIỚI THIỆU CÁC CÂU LẠC BỘ NGOẠI KHOÁ CỦA TRƯỜNG

### Hoạt động
### Thảo luận theo nhóm
Thảo luận theo nhóm để trả lời các câu hỏi sau:
1. Tổ chức cấu trúc website như thế nào cho phù hợp?
2. Với mỗi câu lạc bộ sẽ đưa những thông tin gì?
3. Trình bày các trang web như thế nào cho đẹp và thống nhất với nhau?
4. Làm thế nào để website sinh động và đẹp mắt?

Website cần một trang chủ và các trang riêng cho từng nhóm hoặc từng câu lạc bộ tuỳ theo số lượng và thông tin hoạt động chi tiết của các câu lạc bộ. Ở mức đơn giản, em có thể thiết kế website với ba thành viên: trang giới thiệu chung về trường, trang giới thiệu các câu lạc bộ thể thao và các câu lạc bộ nghệ thuật.

Trang chủ sẽ chứa các thông tin chung nhất về các câu lạc bộ và liên kết tới các trang thành viên. Minh hoạ có thể tuỳ chọn vào các tài nguyên sẵn có - thường là ảnh và video. Các trang thành viên đăng thông tin chi tiết, lịch hoạt động, thành tích,... tuỳ nhu cầu. Ngoài ra, em có thể tạo thêm một trang chứa biểu mẫu để các bạn đăng kí tham gia.

Các trang nên tuân theo phong cách trình bày chung bằng cách sử dụng liên kết tới cùng một tệp tin CSS.

Để thực hiện ý tưởng này, trước hết ta cần lên ý tưởng về bố cục của từng phần trong một trang web rồi sử dụng CSS để định dạng (kích thước, vị trí, màu sắc, cỡ chữ,...) của mỗi phần.

## 2. THỰC HÀNH:
### Nhiệm vụ 1: Tạo tệp CSS
Yêu cầu: Tạo tệp CSS để trình bày website như Hình 18.2.

#### Hướng dẫn:
Với bố cục như Hình 18.2, mỗi thành phần (**đầu trang**, **nội dung chính**, **cuối trang**, **banner**, **slogan**, **ảnh/nội dung**) được định nghĩa bằng một lớp riêng hoặc sử dụng chung lớp nếu cùng định dạng.

Phần đầu trang gồm hai phần nhỏ:
#### Banner: Có thể sử dụng một ảnh làm nền và tiêu đề là tiêu đề trang web, cỡ chữ to, màu sắc nổi bật. Ví dụ, CSS để trang web hiển thị như Hình 18.1 được thiết lập như sau:
    Đoạn mã CSS này định nghĩa kiểu cho một phần tử có lớp `.banner`. Nó đặt ảnh nền, kích thước ảnh nền bao phủ toàn bộ phần tử, thêm khoảng đệm trên và dưới, căn chỉnh văn bản ở giữa, và thiết lập màu văn bản là đỏ sẫm.

#### Slogan: Trong Hình 18.1, slogan gồm 3 ô trên hàng ngang có định dạng giống nhau, mỗi ô có độ rộng bằng 1/3 độ rộng trang. Vì các ô giống nhau nên ta chỉ cần tạo một lớp CSS (đặt tên là block_3). Tuy nhiên khi sử dụng thẻ div, các ô này sẽ được xếp theo chiều dọc. Để hiển thị theo phương ngang, ta sẽ tạo ra một lớp Row có độ rộng bằng độ rộng trang, lớp Row chứa 3 ô trên.

Cách trình bày nhiều ô trong cùng một hàng được sử dụng phổ biến trong các trang web, tạo sự cân đối và hài hoà khi hiển thị. Trong phần nội dung, cách thiết lập hoàn toàn tương tự, áp dụng cho việc chia hai cột bằng nhau trên mỗi hàng. Do vậy, ta sẽ định nghĩa thêm lớp slogan và lớp nội dung chính (content) để bao phía ngoài lớp Row. Mỗi lớp có thể có thêm các đặc tính trình bày riêng.

Ví dụ, CSS cho slogan được thiết lập như sau:

*   Mã CSS cho lớp `.slogan` để thiết lập màu nền, căn chỉnh văn bản, chiều rộng và khoảng đệm (padding) cho phần slogan.
*   Mã CSS cho lớp `.row` để thiết lập hiển thị flexbox, cách bao dòng, lề trên, chiều rộng tối đa và khoảng đệm (padding) hai bên.
*   Mã CSS cho lớp `.block_3` để thiết lập các thuộc tính flex và chiều rộng là 33.33333333%.

Với phần nội dung chính và cuối trang, ta thực hiện việc phân tích bố cục và thiết lập CSS hoàn toàn tương tự.

Sau khi hoàn thành, lưu tệp tin dưới tên **style.css**.

### Nhiệm vụ 2: Tạo các tệp html

Yêu cầu: Tạo các tệp html **index.html**, **thethao.html** và **nghethuat.html** để tạo trang web theo phân tích ở Nhiệm vụ 1.

#### Hướng dẫn:

Để sử dụng các thiết lập CSS từ Nhiệm vụ 1, ta cần tạo các khối bằng thẻ **div** với các lớp CSS đã tạo. Ví dụ, để tạo khối banner cho trang chủ, ta làm như sau:

Đoạn mã HTML này mô tả cấu trúc một phần trang web. Nó bắt đầu với một div có class "banner", chứa tiêu đề "CLB ngoại khoá trường THPT Nguyễn Bình Khiêm". Tiếp theo là một div có class "slogan", bên trong chứa ba div con với class "block_3". Mỗi div "block_3" này lại bao gồm một tiêu đề cấp 3 (h3) và một đoạn văn bản (p), mô tả các đặc điểm như "Năng động", "Đam mê", và "Toả sáng" với nội dung chi tiết tương ứng.

Thực hiện tương tự cho cả ba tệp tin.

Chuẩn bị một số hình ảnh và video của các hoạt động tại lớp/trường em để sử dụng trong mỗi trang web.

Tạo các liên kết từ trang chủ đến hai trang còn lại và đặt liên kết tới các trang khác ở phần cuối trang.

## Luyện tập
1.  Tạo trang **dang_ki.html** chứa biểu mẫu đăng kí câu lạc bộ và bổ sung liên kết tới trang **dang_ki** trong phần cuối trang của tất cả các trang.
2.  Thay đổi định dạng và màu sắc của phông chữ trong các vùng khi di chuyển chuột qua.

## Vận dụng
Hãy đưa ra một thiết kế khác cho website đã tạo ở phần Thực hành. Viết định dạng theo thiết kế mới và chuyển toàn bộ website sang định dạng mới.
