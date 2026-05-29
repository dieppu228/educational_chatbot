# Bài 2: ĐỊNH DẠNG VĂN BẢN VÀ TẠO SIÊU LIÊN KẾT

Học xong bài này, em sẽ:
*   Trình bày được cách tạo nội dung trang web theo đoạn văn bản và cách tạo tiêu đề mục.
*   Liệt kê được một số cách làm nổi bật văn bản trên trình duyệt web.
*   Mô tả được cách tạo siêu liên kết.

Em hãy nêu một số cách để nhận biết siêu liên kết trên trang web.

## 1. Tổ chức các đoạn văn bản trong trang web

Nội dung văn bản trên trang web thường được chia thành các đoạn văn bản. Điều này làm các ý được phân tách rõ ràng, giúp văn bản dễ hiểu, dễ đọc hơn đối với người dùng. **Phần tử p** dùng để tạo đoạn văn bản trên trang web và được khai báo như sau:

Cú pháp để khai báo phần tử p là `<p> Văn bản </p>`.

Trên màn hình trình duyệt web, **Văn bản** hiển thị trên một đoạn mới và phân tách với các thành phần khác bằng một khoảng trống giữa hai đoạn văn bản. Văn bản có thể chứa một số phần tử HTML khác.

Ví dụ 1. Văn bản HTML ở Hình 1a gồm hai đoạn văn bản được tạo bằng phần tử p. Kết quả hiển thị hai đoạn văn bản trên màn hình trình duyệt web như ở Hình 1b.

Đoạn mã HTML trong Hình 1a trình bày cách sử dụng phần tử `<p>` để tạo đoạn văn bản.
Đoạn mã này khai báo một trang HTML cơ bản với tiêu đề "Sử dụng thẻ p" và mã hóa ký tự UTF-8.
Trong phần thân của trang (`<body>`), có hai đoạn văn bản được định nghĩa bằng thẻ `<p>`:
*   Đoạn thứ nhất có nội dung: "Thông thường, trang web tĩnh được tạo thành từ các văn bản HTML. Muốn thay đổi nội dung trang web tĩnh, người tạo trang web phải chỉnh sửa nội dung văn bản HTML."
*   Đoạn thứ hai có nội dung: "Các trang web động thường được tạo thành từ các kịch bản của một số ngôn ngữ lập trình PHP, Java, Python."

Thông thường, trang web tĩnh được tạo thành từ các văn bản HTML. Muốn thay đổi nội dung trang web tĩnh, người tạo trang web phải chỉnh sửa nội dung văn bản **HTML**.
Các trang web động thường được tạo thành từ các kịch bản của một số ngôn ngữ lập trình PHP, Java, Python.

## 2. Tạo tiêu đề mục

Em thường định dạng cho tiêu đề mục của các mục lớn và nhỏ trong một văn bản như thế nào?

HTML hỗ trợ khai báo sáu tiêu đề mục được phân cấp, định nghĩa bởi các phần tử **h1, h2, h3, h4, h5** và **h6** tương ứng (h là viết tắt của heading và các chữ số cho biết cấp của tiêu đề mục). Các phần tử tạo tiêu đề mục được khai báo như sau:
`<Cấp của tiêu đề mục> Tiêu đề mục </Cấp của tiêu đề mục>`
Trong đó, Cấp của tiêu đề mục là một trong các phần tử *h1, h2, h3, h4, h5, h6*. Theo mặc định, trình duyệt web sẽ hiển thị tiêu đề mục với kiểu chữ in đậm và cỡ chữ khác nhau. Phần tử **h1** tạo tiêu đề mục có cỡ chữ lớn nhất, cỡ chữ sẽ giảm dần theo các cấp từ **h2** đến **h6**.
Ví dụ 2. Văn bản HTML ở Hình 2a khai báo các phần tử *h1, h2, h3, h4, h5, h6* để tạo các tiêu đề mục tương ứng. Kết quả hiển thị trên trình duyệt web như ở Hình 2b.

Đoạn mã HTML này khai báo cấu trúc cơ bản của một trang web bao gồm phần `head` (chứa meta-data và tiêu đề trang) và phần `body`. Trong phần `body`, nó sử dụng sáu cấp độ tiêu đề từ `h1` đến `h6`. Cụ thể:
*   `<h1>` được dùng cho tên Chương.
*   `<h2>` được dùng cho tên Mục.
*   `<h3>` được dùng cho tên Tiểu mục.
*   `<h4>`, `<h5>`, `<h6>` được dùng cho các mức tiêu đề tiếp theo.

Tiêu đề mục mức 1 thường được dùng cho tên Chương
Tiêu đề mục mức 2 thường được dùng cho tên Mục
Tiêu đề mục mức 3 thường được dùng cho tên Tiểu mục
Tiêu đề mục mức 4
Tiêu đề mục mức 5
Tiêu đề mục mức 6

## 3. Làm nổi bật nội dung văn bản

Hãy nêu một số cách làm nổi bật nội dung văn bản ở các hệ soạn thảo văn bản mà em đã sử dụng.

HTML làm nổi bật nội dung trong văn bản bằng cách thay đổi định dạng của phần nội dung đó khi hiển thị trên màn hình trình duyệt web. Bảng 1 liệt kê một số phần tử dùng để làm nổi bật nội dung văn bản.

*   Phần tử `strong`: Cú pháp là cặp thẻ `<strong >` và `</strong>` bao quanh nội dung. Mục đích là in đậm **Nội dung**, thường dùng để nhấn mạnh các nội dung quan trọng trong văn bản.
*   Phần tử `em`: Cú pháp là cặp thẻ `<em >` và `</em>` bao quanh nội dung. Mục đích là in nghiêng *Nội dung*, thường dùng để nhấn mạnh các danh từ riêng hay thuật ngữ trong văn bản.
*   Phần tử `mark`: Cú pháp là cặp thẻ `<mark >` và `</mark >` bao quanh nội dung. Mục đích là tô màu vàng cho nền của **Nội dung**, thường dùng để làm nổi bật các nội dung cần chú ý trong văn bản.

Ví dụ 3. Nội dung trong phần `body` của văn bản HTML ở Hình 3a có sử dụng các phần tử `strong`, `em`, `mark` để làm nổi bật nội dung văn bản. Hình 3b là kết quả hiển thị văn bản HTML ở Hình 3a trên màn hình trình duyệt web.

Nội dung này minh họa cách sử dụng các phần tử `<strong>`, `<em>`, `mark` trong HTML để làm nổi bật nội dung văn bản.
Kết quả khi mở văn bản HTML trên bằng trình duyệt web: Nội dung được in đậm Nội dung được in nghiêng Nội dung có nền vàng

Lưu ý: HTML định nghĩa thêm phần tử `b` để in đậm văn bản và phần tử `i` để in nghiêng văn bản.

Các định dạng về phông chữ, cỡ chữ từ phiên bản HTML5 (phiên bản đang sử dụng thông dụng) không còn hỗ trợ nên để định dạng phông chữ, cỡ chữ ta sẽ sử dụng CSS. Nội dung về CSS được đề cập trong Bài 8.

## Tạo siêu liên kết

HTML định nghĩa phần tử `a` để tạo các **siêu liên kết**, giúp kết nối trang web hiện thời với các tài nguyên web khác như trang web, hình ảnh, âm thanh, đoạn phim,... Phần tử `a` được khai báo như sau:

Cấu trúc của thẻ `a` dùng để tạo một liên kết web, trong đó `href` chỉ định địa chỉ của tài nguyên được liên kết và "Liên kết web" là văn bản hiển thị cho liên kết đó.

Trong đó, thuộc tính `href` xác định địa chỉ của tài nguyên web trên Internet. **URL** (Uniform Resource Locator) có cấu trúc cơ bản như sau:

*Giao thức://Tên miền/Đường dẫn*

**Giao thức** thường là `http` hoặc `https`.
**Tên miền** là địa chỉ máy chủ chứa tài nguyên web muốn liên kết, ví dụ: `https://www.w3schools.com`
**Đường dẫn** thường là sự kết hợp giữa tên các thư mục và tên tệp để xác định vị trí cụ thể của tài nguyên web muốn liên kết, ví dụ: `/reference/tags.html`.
**Liên kết web** thường là dãy kí tự được hiển thị trên trình duyệt web cho phép người dùng nháy chuột vào để đến tài nguyên liên kết.

Ví dụ 4. Nội dung phần `body` trong văn bản HTML ở Hình 4a khai báo siêu liên kết “Trang web tìm hiểu về html”. Khi mở bằng trình duyệt web, nháy chuột vào siêu liên kết, nội dung trang web `https://www.w3schools.com/html/default.asp` sẽ hiển thị như ở Hình 4b.

Mô tả: Mã HTML tạo một siêu liên kết với văn bản hiển thị "Trang web tìm hiểu về html" dẫn đến địa chỉ `https://www.w3schools.com/html/default.asp`.

Lưu ý: Nếu URL chỉ khai báo địa chỉ website và được viết dưới dạng Giao thức: //Tên miền thì khi nháy chuột vào siêu liên kết, trình duyệt web sẽ hiển thị nội dung trang chủ của website được khai báo trong Tên miền.
Để tạo siêu liên kết giữa các trang web trong cùng thư mục, chỉ cần khai báo thành phần Đường dẫn trong URL là tên tệp của trang web cần kết nối.
Ví dụ 5. Nội dung phần body trong tệp "index.html" khai báo siêu liên kết “Sở thích” đến trang web hobbies.html được lưu trong cùng thư mục “webcanhan”.

Mô tả: Mã HTML tạo một siêu liên kết với văn bản hiển thị "Sở thích" dẫn đến tệp `hobbies.html` trong cùng thư mục.

HTML còn hỗ trợ tạo **siêu liên kết** đến một phần tử khác trên cùng một trang web dựa vào định danh của nó, nhằm tạo các dấu trang giúp người đọc chuyển nhanh đến phần nội dung mong muốn thay vì phải di chuyển thanh trượt màn hình. Các dấu trang thường được tạo khi trang web có nội dung dài hơn chiều dọc màn hình máy tính.
Mỗi phần tử trong một văn bản HTML có thể được định danh duy nhất bằng cách gán **Tên_định_danh** cho thuộc tính id theo cú pháp: id = “Tên_định_danh”.
Để tạo siêu liên kết đến một phần tử trong trang web, **Tên_định_danh** của phần tử đó được gán cho URL và được viết theo cú pháp: “#Tên_định_danh”.

Vị dụ 6. Nội dung phần **body** trong tệp “index.html” khai báo siêu liên kết “Chủ đề 1” liên kết đến phần tử **h2** thông qua định danh “Topic1”.
Đoạn mã HTML mô tả một siêu liên kết (`<a>`) trỏ đến một phần tử tiêu đề cấp 2 (`<h2>`) có id là `Topic1`.

## Luyện tập
*   **Câu 1.** Em hãy sử dụng các phần tử tạo tiêu đề mục để tạo một trang web hiển thị các tiêu đề mục của nội dung bài học này.
*   **Câu 2.** Em hãy sử dụng các phần tử **strong, em, mark** để làm nổi bật các mục đã tạo ở Câu 1.

Em hãy kết hợp sử dụng các phần tử tạo tiêu đề mục từ **h1** đến **h6** với phần tử tạo đoạn văn bản **p** và phần tử tạo siêu liên kết **a** để soạn văn bản HTML có nội dung giới thiệu về trường em. Lưu văn bản và mở bằng trình duyệt web.

*   **Câu 1.** Trong các khai báo tạo siêu liên kết sau, khai báo nào đúng?
    *   **A.** <a href= “trangnhat.html”>Trang chủ </a>
    *   **B.** <a href= “trang nhat.html”>Trang chủ </a>
    *   **C.** <a link= “trangnhat.html”>Trang chủ </a>
    *   **D.** <a link= “trang nhat.html”>Trang chủ </a>
*   **Câu 2.** Mỗi phát biểu sau đây là đúng hay sai khi sử dụng các phần tử để định dạng văn bản trên trang web?
    *   **a)** Nội dung các tiêu đề mục tạo bởi các phần tử **h1, h2, h3, h4, h5, h6** khi hiển thị trên màn hình trình duyệt web đều được in đậm.
    *   **b)** Nội dung của phần tử **strong** không thể chứa phần tử **h1**.
    *   **c)** Nội dung của phần tử **mark** khi hiển thị trên màn hình trình duyệt web được tô nền màu xanh.
    *   **d)** Đoạn văn bản tạo phần tử **p** được hiển thị trên một đoạn mới khi mở bằng trình duyệt web.

## Tóm tắt bài học

*   Phần tử **p** dùng để khai báo đoạn văn bản.
*   Các phần tử **h1, h2, h3, h4, h5, h6** khai báo cỡ chữ tạo các tiêu đề mục trong trình bày văn bản trên trang web.
*   Các phần tử **strong, em, mark** dùng để khai báo việc làm nổi bật nội dung văn bản.
*   Phần tử **a** dùng để khai báo siêu liên kết. Thuộc tính **href** trong khai báo thẻ mở `<a`> xác định địa chỉ trang web được liên kết.
