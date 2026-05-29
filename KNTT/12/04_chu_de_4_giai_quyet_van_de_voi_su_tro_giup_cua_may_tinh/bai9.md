# Bài 9: TẠO DANH SÁCH, BẢNG

## SAU BÀI HỌC NÀY EM SẼ:
*   Sử dụng thẻ HTML tạo được danh sách, bảng.

Theo em, khi trang web chỉ toàn các đoạn văn bản thì cần trình bày thế nào cho dễ nhìn?

## 1. TẠO DANH SÁCH
### Hoạt động 1 Nhận biết phần tử danh sách
Em hãy quan sát và nhận xét xem có điểm nào có thể cải tiến về mặt trình bày không.

Danh sách trong html cho phép nhóm và liệt kê tập hợp các mục tương tự nhau thành một danh sách để hiển thị. Các dạng danh sách trong html cơ bản gồm: **danh sách không có thứ tự**, **danh sách có thứ tự** và **danh sách mô tả**. Có thể tạo danh sách lồng nhau.

### a) Danh sách có hoặc không có thứ tự
Trong danh sách, các mục được hiển thị tuần tự, kí tự đầu dòng có thể là một số, chữ, dấu, kí hiệu hoặc hình ảnh. Cấu trúc của đoạn mã html tạo danh sách như sau:

Mô tả cấu trúc cơ bản của một danh sách trong HTML, bao gồm thẻ mở, các mục danh sách (`<li>`) và thẻ đóng.

*   Để tạo danh sách có thứ tự, dùng cặp thẻ `ol` và `ol`. Để chọn kiểu đánh thứ tự và giá trị bắt đầu, dùng thuộc tính `type` và `start`.
    *   `type`: xác định kiểu đánh số. Các kiểu đánh số là: "1", "A", "a", "I" và "i".
    *   `start`: xác định giá trị bắt đầu đánh số, nhận giá trị là các số thực.

Mô tả đoạn mã HTML sử dụng thẻ `ol` với thuộc tính `type="i"` để tạo danh sách có thứ tự La Mã nhỏ, chứa các mục `li` mô tả điều kiện của `delta`.
Kết quả:
*   i. Nếu **delta** < 0: ...
*   ii. Nếu **delta** = 0: ...
*   iii. Nếu **delta** > 0: ...

*   Để tạo danh sách không có thứ tự, dùng cặp thẻ `ul` và `ul`. Để chọn kí tự đầu dòng, ta thiết lập giá trị của đặc tính `list-style-type` trong thuộc tính `style` bằng một trong 4 giá trị `disc`, `circle`, `square` và `none`.

Mô tả đoạn mã HTML sử dụng thẻ `ul` với thuộc tính `style="list-style-type:square"` để tạo danh sách không có thứ tự với kí hiệu đầu dòng là hình vuông, chứa các mục `li` mô tả điều kiện của `delta`.
Kết quả:
*   Nếu **delta** < 0: ...
*   Nếu **delta** = 0: ...
*   Nếu **delta** > 0: ...

### b) Danh sách mô tả

Danh sách mô tả dùng để liệt kê các mục kèm với mô tả cho từng mục. Cấu trúc của đoạn mã tạo danh sách mô tả khác cấu trúc của đoạn mã tạo danh sách có hoặc không có thứ tự. Để tạo danh sách mô tả, em dùng ba thẻ **&lt;dl&gt;**, **&lt;dt&gt;** và **&lt;dd&gt;**:

Mô tả cú pháp cơ bản của danh sách mô tả, bao gồm thẻ `<dl>` để định nghĩa danh sách, thẻ `<dt>` cho thuật ngữ (tên mục) và thẻ `<dd>` cho mô tả của thuật ngữ đó.

**Ví dụ**:

Mô tả một danh sách mô tả với hai mục là 'Kem' và 'Trà sữa', cùng với mô tả tương ứng cho mỗi mục.

**Kết quả**
Kem
Món ăn ngọt, ở dạng đông lạnh.
Trà sữa
Đồ uống làm từ hai nguyên liệu trà và sữa.

**Lưu ý**: Ta có thể tạo ra các danh sách lồng nhau bằng cách để một danh sách là một mục của một danh sách khác (bằng cách đặt danh sách đó bên trong cụm thẻ **&lt;li&gt;&lt;/li&gt;** của mục tương ứng).

Trong HTML, ta có thể định nghĩa các kiểu danh sách có thứ tự, không có thứ tự và danh sách mô tả bằng các thẻ **&lt;ol&gt;**, **&lt;ul&gt;** và **&lt;dl&gt;**.

Làm thế nào để tạo một danh sách lồng nhau, danh sách mức 1 đánh số dạng 1, 2, 3,... và danh sách mức 2 đánh số dạng a, b, c?

## 2. THIẾT LẬP BẢNG

### Hoạt động 2 Lựa chọn định dạng phù hợp nhất

Trong Hội chợ ẩm thực ở trường, lớp 12E dự định bán một số món, các bạn muốn đăng trên trang web của lớp các thông tin: món ăn, đơn giá, số lượng và tổng số tiền. Theo em, các bạn nên dùng dạng biểu diễn nào: danh sách, danh sách mô tả hay bảng. Tại sao?

Phần tử bảng được dùng khi ta cần thêm dữ liệu có thể sắp xếp dưới dạng hàng và cột vào trang web. Dữ liệu trong bảng có thể là bất kì loại thông tin nào, không nhất thiết là dạng số. Bảng là công cụ để tạo ra các bố cục nhiều cột hoặc phân bổ nội dung và các khoảng trắng. Chính vì vậy, độ phức tạp của bảng từng là thước đo giá trị thiết kế trang web. Tuy nhiên, sử dụng bảng tạo bố cục tương đối phức tạp nên người ta thường sử dụng CSS để tạo bố cục, nội dung này được trình bày ở các bài sau.

Bảng được tạo từ các hàng, mỗi hàng gồm các ô dữ liệu. Hàng đầu tiên có thể là hàng tiêu đề. Ngôn ngữ HTML xây dựng bảng từ các thành phần tương ứng như trên. Các thành phần lần lượt được định nghĩa bởi các thẻ **&lt;table&gt;** – tạo bảng, **&lt;tr&gt;** – tạo hàng, **&lt;td&gt;** – tạo các ô dữ liệu và **&lt;th&gt;** – tạo ô tiêu đề.

Mã HTML tạo một bảng đơn giản với các hàng tiêu đề (Món ăn, Đơn giá, SL, Thành tiền) và hai hàng dữ liệu (Thịt xiên 10K 3 30, Cá viên 5k 6 30).
Kết quả:

| Món ăn   | Đơn giá | SL | Thành tiền |
| :------- | :------ | :- | :--------- |
| Thịt xiên | 10K     | 3  | 30         |
| Cá viên  | 5k      | 6  | 30         |

### Cấu trúc html của bảng

Bảng trong Hình 9.4 có thể được định dạng thêm để đẹp và dễ đọc hơn bằng cách chỉnh các thuộc tính của bảng. Các định dạng cơ bản bao gồm: thêm tiêu đề cho bảng, tạo khung bảng, điều chỉnh kích thước hàng/cột/ô và gộp ô.

*   Thêm tiêu đề: sử dụng thẻ `<caption>`, ngay sau thẻ `<table>` và trước thẻ `<tr>` đầu tiên.

### Ví dụ:

Mã HTML: Mã HTML dùng thẻ `<caption>` để định nghĩa tiêu đề của bảng.
Kết quả: Bảng có tiêu đề là "Hoá đơn"

*   Tạo khung bảng: Trong HTML5, độ dày khung được thiết lập cho viền khung bảng hoặc khung của từng ô bảng thông qua thuộc tính con **border** của thuộc tính **style** có giá trị là một bộ ba thuộc tính nhỏ hơn sau: "độ_dày_theo_px kiểu_viền [màu_viền]"
    trong đó, ba thuộc tính cách nhau bởi dấu cách, hai thuộc tính đầu là bắt buộc; thuộc tính **kiểu_viền** có thể nhận một trong bốn giá trị (**solid**, **dotted**, **double**, **none**), còn thuộc tính **màu_viền** mặc định là màu đen và có thể bỏ qua.
*   Điều chỉnh kích thước: Sử dụng đặc tính con **width** và **height** của thuộc tính **style**. Kích thước được đặt có thể là theo tỉ lệ với khối bao ngoài đối tượng (%) hoặc theo số điểm ảnh (px).

Lưu ý: Không nên sử dụng kích thước theo px do các thiết bị hiển thị có sự khác nhau về kích thước và số điểm ảnh có thể dẫn đến bảng không hiển thị đúng như mong đợi.

### Ví dụ:

Mã HTML:
*   Mã HTML thiết lập **chiều rộng** của bảng là 80% và **chiều cao** là 400px.
*   Mã HTML thiết lập **chiều cao** của một hàng là 15%.
*   Mã HTML thiết lập **chiều rộng** của một ô/cột là 10%.
Kết quả:
*   Bảng có chiều rộng bằng 80% phần hiển thị, cao 400px.
*   Hàng này có chiều cao bằng 15% độ cao bảng.
*   Ô/cột này có độ rộng bằng 10% độ rộng bảng.

*   Gộp ô: Sử dụng thuộc tính **rowspan** (cho hàng) và **colspan** (cho cột). Bản chất của việc gộp ô là mở rộng một ô bảng cách thêm một số hàng hoặc một số cột lân cận có cùng nội dung. Việc này giúp tạo ra được bảng có cấu trúc phức tạp nhưng cũng làm cho việc đánh dấu, theo dõi và kiểm soát số lượng ô trở nên khó khăn hơn. Việc gộp ô trên hàng được thực hiện như sau (tương tự đối với cột, sử dụng thuộc tính **colspan**):

- Thêm `rowspan="số_hàng_muốn_ghép"` cho phần tử `<th>` hoặc `<td>` thuộc hàng đầu tiên cần ghép.
- Đối với các hàng tiếp theo: Bỏ qua cặp thẻ `<th>` hoặc `<td>` tại vị trí tương ứng (nếu bước trên đặt `rowspan="3"` thì bỏ qua hai hàng tiếp theo).
Ví dụ như Hình 9.6.

Đoạn mã HTML này tạo một bảng với đường viền. Nó sử dụng `rowspan` để gộp hàng và `colspan` để gộp cột cho các tiêu đề bảng. Cụ thể, 'Họ và tên' gộp 2 hàng, và 'Điểm thi' gộp 3 cột ('Toán', 'Vật lí', 'Hoá học').

Kết quả hiển thị:
| Họ và tên | Điểm thi |
|---|---|
| | Toán | Vật lí | Hoá học |

**Phần tử bảng** dùng để biểu diễn dữ liệu có cấu trúc dạng bảng. Phần tử bảng được tạo bởi các thẻ chính là `<table>`, `<tr>`, `<td>` và `<th>`; trình bày bảng bằng thuộc tính `style`.

Bảng trong ví dụ trên Hình 9.6 có nhược điểm gì? Cần làm thế nào để giải quyết nhược điểm đó?

## 3. THỰC HÀNH TẠO DANH SÁCH VÀ BẢNG

### Nhiệm vụ 1: Tạo danh sách

Yêu cầu: Viết đoạn mã html để tạo danh sách các câu lạc bộ của trường như Hình 9.7.

**Hướng dẫn:**
Bước 1. Xác định thành phần của văn bản:
Văn bản gồm hai phần tử: một phần tử tiêu đề và một phần tử danh sách lồng nhau.
Bước 2. Tạo tiêu đều bằng cặp thẻ `<h2>`...`</h2>`.
Bước 3. Tạo danh sách không có thứ tự:
Đoạn mã HTML này tạo một danh sách không có thứ tự rỗng.

Bước 4. Tạo mục **THỂ THAO**, với phần mã được thêm vào giữa cặp thẻ ở dòng 2 là định nghĩa của một danh sách có thứ tự:
Đoạn mã HTML này tạo một mục danh sách không có thứ tự có tên 'THỂ THAO', bên trong nó là một danh sách có thứ tự gồm các môn thể thao như 'Bóng đá', 'Bơi', v.v.

Danh sách Câu lạc bộ
*   THỂ THAO
    1.  Bóng đá
    2.  Bóng chuyền
    3.  Bóng rổ
    4.  Võ
        a. Karatedo
        b. Taekwondo
        c. Vovinam
    5.  Bơi
*   NGHỆ THUẬT
    1.  Mĩ thuật
    2.  Nhiếp ảnh
    3.  Âm nhạc
        a. Thanh nhạc
        b. Piano
        c. Violin
    4.  Khiêu vũ

Lưu ý: Mục thứ tự của danh sách này là một danh sách có thứ tự, kiểu đánh số **type="a"**.

Bước 5. Làm tương tự với mục NGHỆ THUẬT để hoàn thiện danh sách.

### Nhiệm vụ 2: Tạo bảng

Yêu cầu: Lập bảng lịch hoạt động của các câu lạc bộ.

Hướng dẫn:

Bước 1. Xác định các thông số của bảng:
* Bảng có 7 hàng, 7 cột.
* Thuộc tính Caption của bảng là “Lịch hoạt động CLB Thể thao”.
* Hai ô 1, 2 của cột 1 và hai ô 1, 2 của cột 2 được gộp (**rowspan="2"**).
* Các ô 3, 4, 5, 6, 7 của hàng 1 được gộp (**colspan="5"**).

Khung viền được đặt **border="1"** trong thẻ `<table>` hoặc sử dụng **style="border:1px solid"** cho thẻ `<table>` và từng thẻ `<td>` trong bảng.

Bước 2. Tạo bảng kèm caption:
Mô tả: Đoạn mã HTML này khởi tạo một bảng với viền `border="1"` và đặt tiêu đề (caption) là "Lịch hoạt động CLB Thể thao".

Bước 3. Tạo hai hàng đầu như phần tích phía trên.
Mô tả: Đoạn mã HTML này định nghĩa hai hàng đầu của bảng. Hàng đầu tiên có hai ô tiêu đề "Bộ môn" và "GV phụ trách" gộp 2 hàng (`rowspan="2"`), và một ô tiêu đề "Ngày" gộp 5 cột (`colspan="5"`). Hàng thứ hai chứa các tiêu đề con cho các ngày trong tuần (Thứ 2 đến Thứ 6).

Bước 4. Tạo các hàng còn lại, mỗi hàng là một cặp `<tr/></tr`> bao bẩy cặp `<td/></td`> ở giữa chứa dữ liệu.

Lưu lại tệp với tên **CLB.html**.

## LUYỆN TẬP

Sửa lại chương trình trong Hình 9.5a, sử dụng thuộc tính **style** thay vì thuộc tính **border** để tạo viền cho bảng. Sử dụng màu xanh cho viền của ô hai dòng đầu bảng và sử dụng ba màu đỏ, vàng, xanh cho ba chữ Toán, Vật lí và Hoá học.

## VẬN DỤNG

Cho trước một bảng dữ liệu cỡ n x 4, mỗi hàng tương ứng với một bộ (họ tên, điểm Toán, điểm Vật lí, điểm Hoá học). Viết chương trình Python để tạo ra tệp HTML thực hiện việc vẽ bảng tương tự như Hình 9.5 và bổ sung dữ liệu vào các hàng phía dưới.
