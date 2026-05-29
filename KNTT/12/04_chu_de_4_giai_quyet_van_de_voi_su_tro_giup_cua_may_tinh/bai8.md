# Bài 8: ĐỊNH DẠNG VĂN BẢN

## SAU BÀI HỌC NÀY EM SẼ:
* Sử dụng được thẻ HTML để định dạng văn bản, phông chữ.

Cho hai đoạn văn bản như Hình 8.1. Cách trình bày đoạn văn bản nào có định dạng đẹp hơn? Tại sao?

**Vội vàng**
Tôi muốn tắt nắng đi cho màu đừng nhạt mất; Tôi muốn buộc gió lại cho hương đừng bay đi.

**Vội vàng**
Tôi muốn tắt nắng đi Cho màu đừng nhạt mất; Tôi muốn buộc gió lại Cho hương đừng bay đi.

## 1. THUỘC TÍNH THẺ

### Hoạt động 1: Nhận biết thuộc tính thẻ
Hãy quan sát các thẻ trong tệp newpage.html ở Hoạt động 2, Bài 7. Trong các thẻ đó có một thẻ có thêm thuộc tính. Theo em đó là thẻ nào? Em hãy đưa ra dự đoán về tác dụng của các thuộc tính thẻ.

Mọi phần tử HTML đều có thể có thuộc tính. **Thuộc tính** của thẻ có tác dụng bổ sung thông tin, làm rõ các điều khiển được thẻ chỉ định.
Cú pháp để xác định thuộc tính: **tên_thuộc_tính**="**giá_trị**", trừ các trường hợp đặc biệt chỉ cần tên thuộc tính để xác định giá trị Có hoặc Không.
Thuộc tính nằm trong thẻ bắt đầu (không nằm trong thẻ kết thúc), sau tên thẻ. Trong trường hợp thẻ có nhiều hơn một thuộc tính thì các thuộc tính được ngăn cách bởi dấu cách.
Ví dụ: Với thẻ có hai thuộc tính là **thuộc_tính_1** nhận **giá_trị_1** và **thuộc_tính_2** nhận **giá_trị_2**, ta viết câu lệnh như sau:
Ví dụ này minh họa cách viết một thẻ HTML với tên thẻ đã cho, có hai thuộc tính `thuộc_tính_1` và `thuộc_tính_2`, nhận các giá trị tương ứng là `giá_trị_1` và `giá_trị_2`, bao quanh một phần "Nội dung".

Một trong những thuộc tính được sử dụng thường xuyên nhất là thuộc tính **style**, dùng để thiết lập định dạng văn bản như chọn màu sắc, phông chữ, cỡ chữ, kiểu chữ, căn lề, tạo khung,... cho một phần tử HTML ngay tại vị trí được viết.

Thẻ có thể có hoặc không có thuộc tính. Thuộc tính của thẻ có tác dụng bổ sung thông tin, làm rõ cách xử lí cho thẻ chứa nó.

Xác định các tên thuộc tính và thẻ chứa thuộc tính tương ứng xuất hiện trong Bài 7.

## 2. CÁC THẺ ĐỊNH DẠNG TRÌNH BÀY VĂN BẢN

### Hoạt động 2: Xác định thành phần cấu thành một văn bản

Thảo luận: Khi trình bày một văn bản (bài thơ, đoạn văn, trang web,...) có thể có những thành phần nào? Hãy kể tên các thành phần đó.

### a) Định dạng tiêu đề

Để định dạng tiêu đề và các tiêu đề con xuất hiện trong văn bản, ta sử dụng các thẻ dạng **<hx>** trong đó x nhận một trong các giá trị từ 1 đến 6, thể hiện độ quan trọng giảm dần của nội dung. Thẻ **<h1>** nên được sử dụng cho tiêu đề chính hay tiêu đề chung của cả văn bản. Các tiêu đề ở mức thấp hơn dùng thẻ **<h2>** và tiếp tục với các mức tiếp theo,...

Khi sử dụng thẻ **<hx>**, trình duyệt sẽ sử dụng chúng để hiển thị trang web và định dạng văn bản giúp người dùng đọc lướt trang web theo tiêu đề. Ngoài ra, các công cụ tìm kiếm sử dụng thẻ này để xác định cấu trúc và nội dung trang web.

Ví dụ 1: Đoạn mã html dưới đây minh hoạ một văn bản có bốn mức tiêu đề:

Đoạn mã HTML này sử dụng các thẻ tiêu đề từ `<h1>` đến `<h4>` để định nghĩa cấu trúc phân cấp của một tài liệu về "Tin học 12".

Kết quả khi dùng thẻ tiêu đề trong Ví dụ 1:
*   Tin học 12
*   Phần chung
*   Chủ đề 1. Máy tính và xã hội tri thức
    *   1. Trí tuệ nhân tạo và ứng dụng
    *   2. Trí tuệ nhân tạo trong khoa học và đời sống
*   Chủ đề 2. Mạng máy tính và Internet
    *   3. Một số thiết bị mạng thông dụng
*   Chủ đề 2. Mạng máy tính và Internet
    *   3. Thiết bị mạng

### b) Định dạng đoạn văn bản

Một văn bản thường gồm nhiều đoạn văn bản tách rời nhau. Các đoạn có thể được định dạng giống hoặc khác nhau tuỳ vào vị trí, nội dung và cách trang trí.

Cách đơn giản nhất để xác định đoạn là đặt nội dung đoạn trong cặp thẻ `<p>Nội dung</p>`. Khi gặp cặp thẻ `<p>...</p>` trình duyệt sẽ hiển thị nội dung đoạn trên dòng mới kèm với khoảng trống nhỏ trước và sau đoạn. Nội dung đoạn có thể chứa văn bản, hình ảnh và cả các phần tử khác nhưng không được chứa tiêu đề, danh sách, phần tử phân đoạn hoặc các phần tử dạng khối khác. Các đoạn được định dạng bằng thẻ `<p>` phù hợp với văn bản chứa nhiều chữ.

Khi cần thao tác với nhiều loại nội dung, ta có thể sử dụng phần tử `<div>` và thẻ `<span>`. Cặp thẻ `<div>...</div>` hay `<span>...</span>` tạo một khối chứa nội dung bất kì đặt ở giữa hai thẻ. Phần tử `<div>` là một khối, bắt đầu trên dòng mới, trong khi phần tử `<span>` có tác dụng tương tự nhưng sử dụng cho quy mô nhỏ hơn; nội dung khối hiển thị trên cùng dòng đang viết.

Để thêm các định dạng như khung, lề,... cho đoạn ta sử dụng thuộc tính **style**. Thuộc tính này sẽ được giới thiệu chi tiết trong các bài sau.

Lưu ý: Ngoài các thẻ định dạng đoạn và khối kể trên, còn có hai thẻ `<br>` và `<hr>` để xuống dòng hoặc tạo ra một đường kẻ ngang trên trang web.

Một văn bản thông thường được tạo bởi hai thành phần cơ bản là tiêu đề và các đoạn văn bản. Tiêu đề được định dạng bởi thẻ `<h1>` có 6 mức tiêu đề từ `<h1>` đến `<h6>`. Đoạn văn bản được định dạng bởi thẻ `<p>`. Khối là một phần tử chứa nhiều loại dữ liệu, được định nghĩa bởi thẻ `<div>` và `<span>`.

## Luyện tập
1.  Trình duyệt hiển thị đoạn mã html sau thành mấy dòng? Em có nhận xét gì về khoảng cách giữa các dòng?
    Đoạn mã HTML này minh họa cách các thẻ `<p>`, `<div>` và `<br>` được sử dụng để tạo đoạn văn bản, khối dữ liệu và ngắt dòng, cũng như khả năng định dạng bằng thuộc tính `style`.
2.  Chỉnh sửa đoạn mã html trong Ví dụ 1 để hiển thị thêm một đường kẻ ngang phân tách giữa dòng tiêu đề "Tin học 12" và nội dung phía dưới.

## 3. CÁC THẺ ĐỊNH DẠNG PHÔNG CHỮ

**Hoạt động 3** Xác định các dạng đặc biệt của chữ khi trình bày một văn bản

Thảo luận: Khi muốn nhấn mạnh vào một nội dung trong văn bản, em thường thấy nội dung đó được viết như thế nào?

### a) Định dạng kiểu chữ

Một số kiểu chữ thường dùng bao gồm: đậm, nghiêng, gạch chân, đánh dấu (highlight),... Các đoạn chữ cần được thiết lập kiểu chữ và được đặt trong cặp thẻ tương ứng, cụ thể như trong Bảng 8.1.

Bảng 8.1. Một số thẻ định dạng kiểu chữ

*   **Kiểu chữ:** Chữ thường
    *   **Thẻ sử dụng:** `<p>`
    *   **Chức năng:** Thẻ `<p>` được sử dụng để định dạng văn bản là một đoạn văn bản thông thường.
    *   **Hiển thị trên trình duyệt:** Đây là câu chuẩn

*   **Kiểu chữ:** Chữ đậm
    *   **Thẻ sử dụng:** `<strong>`; `<b>`
    *   **Chức năng:** Các thẻ `<strong>` hoặc `<b>` được sử dụng để định dạng văn bản thành chữ đậm.
    *   **Hiển thị trên trình duyệt:** Đây là câu **chuẩn**

*   **Kiểu chữ:** Chữ nghiêng
    *   **Thẻ sử dụng:** `<em>`; `<i>`
    *   **Chức năng:** Các thẻ `<em>` hoặc `<i>` được sử dụng để định dạng văn bản thành chữ nghiêng.
    *   **Hiển thị trên trình duyệt:** Đây là câu *chuẩn*

*   **Kiểu chữ:** Gạch chân
    *   **Thẻ sử dụng:** `<u>`
    *   **Chức năng:** Thẻ `<u>` được sử dụng để định dạng văn bản thành chữ gạch chân.
    *   **Hiển thị trên trình duyệt:** Đây là câu <u>chuẩn</u>

*   **Kiểu chữ:** Đánh dấu
    *   **Thẻ sử dụng:** `<mark>`
    *   **Chức năng:** Thẻ `<mark>` được sử dụng để đánh dấu (highlight) văn bản.
    *   **Hiển thị trên trình duyệt:** Đây là câu chuẩn (với từ "chuẩn" được đánh dấu)

*   **Kiểu chữ:** Giảm cỡ chữ
    *   **Thẻ sử dụng:** `<small>`
    *   **Chức năng:** Thẻ `<small>` được sử dụng để làm giảm kích thước chữ của văn bản.
    *   **Hiển thị trên trình duyệt:** Đây là câu chuẩn (với từ "chuẩn" có kích thước nhỏ hơn)

*   **Kiểu chữ:** Chỉ số trên hoặc dưới
    *   **Thẻ sử dụng:** `<sup>`; `<sub>`
    *   **Chức năng:** Thẻ `<sup>` được sử dụng để định dạng văn bản thành chỉ số trên, thẻ `<sub>` để định dạng thành chỉ số dưới.
    *   **Hiển thị trên trình duyệt:** Đây là câu chuẩn (với từ "chuẩn" là chỉ số trên hoặc dưới)

*   **Kiểu chữ:** Đánh dấu xoá (bằng nét gạch giữa chữ)
    *   **Thẻ sử dụng:** `<del>`
    *   **Chức năng:** Thẻ `<del>` được sử dụng để định dạng văn bản thành chữ bị gạch ngang.
    *   **Hiển thị trên trình duyệt:** Đây là câu chuẩn (với từ "chuẩn" bị gạch ngang)

## Em cần chú ý
*   HTML5 không hỗ trợ thẻ **`big`** và **`<u>`**, để điều khiển em nên thay bằng giá trị **`font-size`** và **`text-decoration`** trong thuộc tính **`style`**.
*   Các thẻ **`<strong>`**, **`<em>`** có cùng tác dụng định dạng chữ đậm, nghiêng giống các thẻ **`<b>`**, **`<i>`** nhưng các thẻ này có ý nghĩa nhấn mạnh vào ngữ nghĩa của nội dung và được khuyến khích sử dụng nhiều hơn trong định dạng văn bản.

**Ví dụ 2:** Trong đoạn mã html sau, đoạn thứ nhất nhấn mạnh vào môn học hay là "Tin học", đoạn thứ hai nhấn mạnh vào mức độ "rất" hay của môn Tin học.
*   **Đoạn mã:** Thẻ `<p>` bao quanh đoạn văn bản, trong đó thẻ `<em>` được dùng để nhấn mạnh từ "Tin học".
*   **Kết quả hiển thị:** Môn *Tin học* rất hay.
*   **Đoạn mã:** Thẻ `<p>` bao quanh đoạn văn bản, trong đó thẻ `<em>` được dùng để nhấn mạnh từ "rất".
*   **Kết quả hiển thị:** Môn Tin học *rất* hay.

### b) Định dạng phông chữ
Để định dạng phông chữ ta sử dụng thuộc tính **`style`**. Các thuộc tính màu sắc, phông chữ, cỡ chữ được xác định như sau:
*   Màu sắc: Thẻ `<p>` với thuộc tính `style="color:màu"` để định nghĩa màu cho nội dung.
*   Phông chữ: Thẻ `<p>` với thuộc tính `style="font-family:tên phông"` để định nghĩa loại phông cho nội dung.
*   Cỡ chữ: Thẻ `<p>` với thuộc tính `style="font-size:cỡ"` để định nghĩa cỡ chữ cho nội dung.

Có nhiều cách xác định cỡ chữ, phổ biến là dùng số kèm đơn vị (px-pixel, mm, cm,...) hoặc cỡ chữ thông dụng (small, medium, large,...).

Lưu ý:
*   Giá trị màu sắc được sử dụng theo tiếng Anh: red, green, blue, grey, yellow, black, brown,... hoặc giá trị màu trong hệ **RGB**.
*   Khi muốn thực hiện nhiều định dạng đồng thời, ta đặt các cặp **tên:giá trị** trong phần giá trị của thuộc tính, ngăn cách nhau bởi dấu “;”.

*   Mỗi kiểu chữ khác nhau như **in đậm**, **in nghiêng**, **chỉ số trên/dưới**,... đều có thẻ tương ứng để điều khiển.
*   Để định dạng phông chữ ta sử dụng thuộc tính **style** trong **HTML5**.

## Luyện tập
Với cùng một đoạn văn bản, kết quả khi định dạng trong các trường hợp sau giống và khác nhau như thế nào?

Kiểu 1: Đoạn mã này sử dụng thẻ `<p>` với thuộc tính `style` để đặt màu chữ là đỏ, phông chữ Tahoma, kích thước 15px và gạch chân văn bản.
Kiểu 2: Đoạn mã này sử dụng thẻ `<p>` với thuộc tính `style` để đặt màu chữ là đỏ (RGB 255,0,0), phông chữ Tahoma và kích thước 10px.

# Bài 4: THỰC HÀNH ĐỊNH DẠNG VĂN BẢN VÀ PHÔNG CHỮ

Nhiệm vụ: Viết đoạn mã HTML để trình bày đoạn văn bản trong Hình 8.3

1 **Biện luận số nghiệm của phương trình bậc 2**
2 **Bài toán**: Xác định số nghiệm của phương trình ax² + bx + c = 0 (a != 0)
3 **Cách làm**:
4 B₁: Xác định hệ số a, b và c
5 B₂: Tính delta = b² – 4ac
6 B₃: Kết luận
7 + Nếu **delta** < 0: Phương trình vô nghiệm
8 + Nếu **delta** = 0: Phương trình có nghiệm duy nhất
9 + Nếu **delta** > 0: Phương trình có hai nghiệm phân biệt

### Hướng dẫn
*   #### Bước 1. Phân tích thành phần của đoạn văn bản:
    *   Tiêu đề: Dòng 1, dòng 2, dòng 3. Trong đó dòng 1 ở mức tiêu đề đề cao hơn.
    *   Đoạn: 3 đoạn, tương ứng với 3 bước làm.
*   Lưu ý: Các dòng 7, 8, 9 đều bắt đầu viết trên dòng mới nhưng không là đoạn vì ta không thấy cách trước và sau như những dòng trên.

*   #### Bước 2. Dùng thẻ **<h1>** để viết 3 dòng đầu:
    Ta có thể sử dụng thẻ **<h1>** cho dòng 1 và **<h2>** cho dòng 2, 3 (hoặc **<h2>** cho dòng 1 và **<h3>** cho dòng 2, 3).
    Để thay đổi màu sắc, dùng thuộc tính **style**; dùng thẻ **<sup>** để viết số mũ ở câu lệnh của dòng 2:
    Mô tả đoạn mã: Đoạn mã HTML này định dạng một tiêu đề cấp 3 (**<h3>**) với nội dung "Bài toán: Xác định số nghiệm của phương trình ax<sup>2</sup> + bx - c = 0 (a != 0)". Phần "Bài toán:" được định dạng màu đỏ bằng thẻ **<span>** với thuộc tính **style**, và số '2' trong ax<sup>2</sup> được hiển thị dưới dạng số mũ bằng thẻ **<sup>**.

*   #### Bước 3. Dùng thẻ **<p>** để viết 3 đoạn bên dưới:
    *   Viết mỗi đoạn bằng một thẻ **<p>**.
    *   Viết chỉ số dưới, số mũ bằng thẻ **<sub>**, **<sup>**.
    *   In đậm, in nghiêng chữ bằng thẻ **<strong>**/**<b>**, **<em>**/**<i>**.
    *   Xuống dòng bằng thẻ **<br>**.

## LUYỆN TẬP
1.  Hãy sửa lại phần tử sau để làm nổi bật ý chính của câu:
    `<p> Thẻ strong và thẻ em được sử dụng để nhấn mạnh vào nội dung trong phần tử. Thẻ b chỉ có tác dụng in đậm văn bản <p>`
2.  Trình bày đoạn văn bản sau bằng mã HTML:
    **INTERNET TỐC ĐỘ CAO**
    *Dịch vụ Internet tốc độ cao là dịch vụ Internet cáp quang chất lượng cao, ổn định, giá cả hợp lí.*
    **Các tính năng nổi bật:**
    *   Tốc độ siêu cao từ 150 MBps trở lên
    *   Lắp đặt nhanh chóng trong 24 h
    *   Phù hợp với cá nhân/Hộ gia đình
    *   Tặng Modem 2 băng tần
    *   Miễn phí lắp đặt
    *   Hỗ trợ 24/7

## VẬN DỤNG
1.  Hãy chỉ ra các bước cần thực hiện để sử dụng một màu cụ thể trong bức ảnh làm màu cho tiêu đề một bài thơ.
2.  Hãy đưa ra cách định dạng một đoạn văn bản để được kết quả như sau:
    Dãy số "00000%00000%00000%00000" với ký hiệu phần trăm (%) được đặt ở vị trí số mũ phía trên các nhóm số 0.
