# Bài 4: TRÌNH BÀY NỘI DUNG THEO DẠNG DANH SÁCH, BẢNG BIỂU

**Học xong bài này, em sẽ:**
*   Trình bày được nội dung dạng danh sách trên trang web.
*   Tạo được bảng biểu trên trang web.

Theo em, để trình bày một văn bản, khi nào nên trình bày theo dạng liệt kê các mục và khi nào nên trình bày theo dạng bảng?

## Tạo danh sách

### Danh sách xác định thứ tự

Danh sách xác định thứ tự được dùng khi thứ tự xuất hiện các mục của nó là quan trọng. Phần tử **ol** dùng để tạo danh sách xác định thứ tự và được khai báo như sau:

Một đoạn mã HTML minh họa cấu trúc cơ bản của danh sách xác định thứ tự (ordered list) sử dụng thẻ `<ol>` và các thẻ `<li>` để định nghĩa từng mục nội dung.

Phần tử **li** được sử dụng để tạo các mục nội dung trong danh sách. Nội dung của mỗi mục được viết trong cặp thẻ `<li></li>`. Các mục trong danh sách theo mặc định được xác định thứ tự tăng dần bằng các số nguyên bắt đầu từ 1.

Ví dụ 1. Nội dung phần **body** của văn bản HTML khai báo một danh sách gồm ba mục nội dung. Khi hiển thị trên màn hình trình duyệt web, các mục đó được xác định thứ tự. Nội dung mục đầu tiên "HTML" được xác định thứ tự là 1.

Một đoạn mã HTML trong phần `<body>` hiển thị một đoạn văn bản và một danh sách xác định thứ tự bao gồm ba mục: HTML, Cascading Style Sheets (CSS), và JavaScript. Khi chạy đoạn mã này trên trình duyệt, kết quả sẽ hiển thị như sau:
```
Các công nghệ cần biết khi tạo trang web
1. HTML
2. Cascading Style Sheets (CSS)
3. JavaScript
```

Em có thể xác định thứ tự bắt đầu của danh sách bằng cách gán một số nguyên khác cho thuộc tính **start** trong khai báo phần tử **ol**.

Ví dụ 2. Khai báo `<ol start = "5">` xác định thứ tự mục đầu tiên của danh sách là 5.

Hãy nêu một số cách em đã biết để xác định thứ tự các mục được liệt kê trong một danh sách.

Muốn thay đổi cách xác định thứ tự các mục trong danh sách, em cần thiết lập giá trị cho thuộc tính *type* trong khai báo phần tử *ol*. Ví dụ 3. Khai báo `<ol type = "A">` xác định thứ tự các mục trong danh sách bằng chữ cái viết hoa.

### b) Danh sách không xác định thứ tự

Danh sách không xác định thứ tự thường được sử dụng khi thứ tự xuất hiện các mục của nó là không quan trọng. Phần tử **ul** được dùng để tạo danh sách không xác định thứ tự, các mục nội dung được khai báo thông qua phần tử **li** tương tự như với danh sách xác định thứ tự. Theo mặc định, mỗi mục nội dung khi hiển thị trên màn hình trình duyệt web được bắt đầu bằng một dấu chấm tròn màu đen.

Ví dụ 4. Nội dung trong phần *body* của văn bản HTML khai báo danh sách gồm hai mục nội dung trong cặp thẻ `<ul></ul>` và kết quả hiển thị trên màn hình trình duyệt web.

Đoạn mã HTML sau đây tạo một đoạn văn bản và một danh sách không có thứ tự.
*Nội dung đoạn mã:*
```html
<body>
    <p>HTML hỗ trợ tạo danh sách</p>
    <ul>
        <li>Danh sách xác định thứ tự</li>
        <li>Danh sách không xác định thứ tự</li>
    </ul>
</body>
```
*Kết quả khi mở văn bản HTML bằng trình duyệt web:*
HTML hỗ trợ tạo danh sách
* Danh sách xác định thứ tự
* Danh sách không xác định thứ tự

## Tạo bảng

Bảng thường được sử dụng để thể hiện thông tin có cấu trúc, dùng cho thống kê, so sánh dữ liệu.

HTML định nghĩa phần tử **table** để tạo bảng. Bảng được tạo bởi lần lượt các hàng. Mỗi hàng được khai báo bằng phần tử **tr**. Mỗi hàng chứa một hoặc nhiều ô dữ liệu, mỗi ô dữ liệu được khai báo bằng phần tử **td**. Phần tử **table** có cú pháp khai báo như sau:

*   Mô tả cú pháp cơ bản của bảng HTML:
    Mã HTML bắt đầu với thẻ `<table>`. Bên trong `<table>`, mỗi hàng được định nghĩa bằng thẻ `<tr>`. Trong mỗi `<tr>`, các ô dữ liệu được định nghĩa bằng thẻ `<td>` chứa nội dung "Dữ liệu".

Dữ liệu trong các ô thường là văn bản, hình ảnh, siêu liên kết,... Dữ liệu cũng có thể bao gồm các bảng khác.

**Ví dụ 5.** Nội dung phần **body** của văn bản HTML trình bày danh sách cán bộ lớp 12A1 dưới dạng bảng. Kết quả hiển thị trên màn hình trình duyệt web như sau:

*   Mô tả mã HTML tạo bảng:
    Đoạn mã HTML này nằm trong phần `<body>` của một trang web. Nó bắt đầu bằng một đoạn văn bản (`<p>`) hiển thị "Danh sách cán bộ lớp 12A1".
    Tiếp theo là một bảng (`<table>`) bao gồm các hàng (`<tr>`) và các ô dữ liệu (`<td>`).
    Hàng đầu tiên chứa tiêu đề cột: STT, Họ và tên, Chức vụ.
    Hàng thứ hai chứa dữ liệu của cán bộ thứ nhất: 1, Nguyễn Thảo Linh, Lớp trưởng.
    Hàng thứ ba chứa dữ liệu của cán bộ thứ hai: 2, Nguyễn Hoàng Nam, Bí thư chi đoàn.

*   Kết quả hiển thị trên trình duyệt web:
    ```
    Danh sách cán bộ lớp 12A1
    STT   Họ và tên           Chức vụ
    1     Nguyễn Thảo Linh    Lớp trưởng
    2     Nguyễn Hoàng Nam    Bí thư chi đoàn
    ```

**Lưu ý:** Để bổ sung thông tin chú thích cho bảng, em khai báo phần tử **caption**. Theo quy định, phần tử **caption** phải được khai báo ngay sau thẻ mở `<table>`.

# Bài Thực hành tạo danh sách, tạo bảng

## Nhiệm vụ 1. Tạo danh sách

**Yêu cầu:** Soạn văn bản HTML để khi mở bằng trình duyệt web sẽ có danh sách xuất hiện như sau:

*   Danh sách các trường đại học Việt Bách cân nhắc dự tuyển
    *   I. Các trường Kĩ thuật - Công nghệ
        *   a. Đại học Bách khoa Hà Nội
        *   b. Trường Đại học Công nghệ, ĐHQGHN
    *   II. Các trường Kinh tế
        *   c. Trường Đại học Kinh tế Quốc dân
        *   d. Trường Đại học Ngoại thương
    *   III. Các trường Quân đội - Công an
        *   e. Học viện Kĩ thuật Quân sự
        *   f. Học viện An ninh nhân dân

**Hướng dẫn thực hiện:**

*   **Bước 1.** Tạo tệp “Bai4-NV1.html”.
*   **Bước 2.** Tạo cấu trúc và khai báo phần tử head cho tệp “Bai4-NV1.html”.
    *   Các thao tác cụ thể thực hiện như hướng dẫn trong Bước 2, Nhiệm vụ 1 ở Bài 3.
*   **Bước 3.** Tạo danh sách xác định thứ tự.
    *   Trong nội dung phần tử body:
        *   Khai báo danh sách xác định thứ tự theo các chữ số La Mã viết hoa bằng cách sử dụng cặp thẻ `<ol type = "I"></ol>`.
        *   Với các mục con của nhóm Các trường Kĩ thuật – Công nghệ, khai báo danh sách xác định thứ tự theo chữ cái viết thường bằng cách sử dụng cặp thẻ `<ol type = "a"></ol>`.
        *   Quan sát các nhóm tiếp theo, các mục con được đánh thứ tự kế tiếp, cùng kiểu của các mục con trước đó. Danh sách các mục con này cần khai báo thuộc tính `start` để xác định giá trị thứ tự bắt đầu cho phù hợp. Ví dụ, các mục con của nhóm Các trường Kinh tế được khai báo bằng cặp thẻ `<ol type = "a" start = "3"></ol>`. Thực hiện tương tự với danh sách con của nhóm Các trường Quân đội – Công an.
*   **Bước 4.** Ghi lưu, mở tệp bằng trình duyệt web và xem xét kết quả.

## Nhiệm vụ 2. Tạo bảng

**Yêu cầu:** Soạn văn bản HTML để hiển thị trên màn hình trình duyệt web thông tin dạng bảng như sau:

*   Thống kê số lượng học sinh lớp 12A1 tham gia hoạt động thể thao của trường
| Nội dung | Nam | Nữ |
| :------- | :-- | :- |
| Bóng bàn | 10 | 5 |
| Cờ vua | 8 | 3 |
| Chạy cự li ngắn | 15 | 6 |

**Hướng dẫn thực hiện:**

*   **Bước 1.** Tạo tệp “Bai4-NV2.html”.
*   **Bước 2.** Tạo cấu trúc và khai báo phần tử head cho tệp “Bai4-NV2.html”.
*   **Bước 3.** Tạo đường viền và chú thích cho bảng.
    *   Trong nội dung phần tử body:
        *   Khai báo phần tử bảng bằng cặp thẻ `<table>`.
        *   Tạo đường viền bao quanh các ô bằng cách sử dụng cặp thẻ `<table border = "1">`.
        *   Khai báo chú thích “Thống kê số lượng học sinh lớp 12A1 tham gia hoạt động thể thao của trường” của bảng ngay sau thẻ mở `<table>` bằng cặp thẻ `<caption></caption>`.

### Bước 4. Tạo nội dung bảng.
Tạo nội dung bảng bằng cách khai báo nội dung cho từng hàng, trong mỗi hàng khai báo nội dung cho từng ô.
Trong nội dung phần tử **table**:
*   Sau phần chú thích, khai báo tạo bốn hàng bảng các cặp thẻ `<tr></tr>`.
*   Trong mỗi hàng, tạo ba ô bằng cặp thẻ `<td></td>` và viết nội dung tương ứng vào các ô như yêu cầu.

### Bước 5. Ghi lưu, mở tệp bằng trình duyệt web và xem kết quả.

## Tạo website cá nhân
Em hãy bổ sung thêm một số nội dung cho website cá nhân đã được tạo ở các bài học trước.
**Gợi ý thực hiện:**
*   Trong tệp “hobbies.html”, bổ sung tiêu đề mục `h1` “Sở thích của em” tạo danh sách xác định thứ tự hoặc không xác định thứ tự liệt kê các sở thích của em.
*   Trong tệp “index.html”, bổ sung tiêu đề mục `h2` “Kế hoạch học tập” và trình bày thời khoá biểu của em dưới dạng bảng.

## Luyện tập
## Câu 1. Mỗi phát biểu sau đây là đúng hay sai khi sử dụng các phần `ol`, `ul` để tạo danh sách trên trang web?
a) Khi khai báo thuộc tính `type = "A"` danh sách xác định thứ tự các mục theo chữ cái viết hoa.
b) Số thứ tự trong danh sách xác định thứ tự luôn là số nguyên.
c) Khi mở bằng trình duyệt web, theo mặc định mục trong danh sách không xác định thứ tự được hiển thị bắt đầu bằng dấu sao (*).
d) Có thể thay đổi số thứ tự của mục bắt đầu trong danh sách xác định thứ tự.

## Câu 2. Khai báo nào sau đây sẽ tạo một bảng có hai hàng, mỗi hàng gồm một ô dữ liệu?
A. `<table><td><tr>Hàng 1</tr><tr>Hàng 2</tr></td></table>`
B. `<table><tr>Hàng 1</tr><tr>Hàng 2</tr></table>`
C. `<table><tr><td>Hàng 1</td></tr><tr><td>Hàng 2</td></tr></table>`
D. `<table><td>Hàng 1</td><td>Hàng 2</td></table>`

## Tóm tắt bài học
Trong HTML:
*   Phần tử **ol** dùng để khai báo danh sách xác định thứ tự.
*   Phần tử **ul** dùng để khai báo danh sách không xác định thứ tự.
*   Phần tử **li** dùng để khai báo các mục nội dung trong danh sách.
*   Phần tử **table**, **tr**, **td** là các phần tử cơ bản dùng để tạo bảng biểu.
