# Bài 16: ĐỊNH DẠNG KHUNG

SAU BÀI HỌC NÀY EM SẼ:
*   Sử dụng được CSS để định dạng khung văn bản, kích thước khung, kiểu đường viền,...
*   Biết sử dụng CSS cho các bộ chọn khác nhau (id, class,...).

Trên một trang web thường có rất nhiều phần tử cùng loại (cùng tên thẻ). Ví dụ thẻ `p` sẽ tương ứng với rất nhiều phần tử của trang web. Một định dạng với bộ chọn `p` sẽ áp dụng cho tất cả các thẻ `p`. Nếu muốn phân biệt các thẻ `p` với nhau và muốn tạo ra các CSS để phân biệt các thẻ `p` thì có thể thực hiện được không?

## 1. PHÂN LOẠI PHẦN TỬ KHỐI VÀ NỘI TUYẾN

**Hoạt động 1: Tìm hiểu và phân biệt phần tử khối và phần tử nội tuyến**

Quan sát cách tô màu nền của hai phần tử trên trang web trong Hình 16.1, em có nhận xét gì?

Thư Bác Hồ gửi học sinh

Non sông **Việt Nam** có trở nên tươi đẹp hay không, dân tộc Việt Nam có bước tới đài vinh quang để sánh vai với các cường quốc năm châu được hay không, chính là nhờ một phần lớn ở công học tập của các cháu.

Các thẻ (hay phần tử) html được chia làm hai loại, **khối** (block level) và **nội tuyến** (inline level).

Các phần tử **khối** thường bắt đầu từ đầu hàng và kéo dài suốt chiều rộng của trang web. Trong ví dụ ở Hình 16.1, dòng chữ *Thư Bác Hồ gửi học sinh* được thể hiện ở dạng khối.

Các phần tử **nội tuyến** là các phần tử nhúng bên trong một phần tử khác. Trong ví dụ ở Hình 16.1, cụm từ *Việt Nam* là một phần tử nội tuyến, được nhúng trong phần tử `p`.

Mặc định các phần tử HTML sẽ thuộc một trong hai loại khối hoặc nội tuyến (Bảng 16.1).

**Bảng 16.1. Phân loại phần tử CSS**

**Phần tử loại khối**
h1 – h6, p, div, address, nav, article, section, aside, form, header, footer, table, hr, ol, ul, li, canvas

**Phần tử loại nội tuyến**
b, span, a, img, em, strong, sub, sup, var, samp, cite, dfn, kbd, pre, code, q, i, u, del, ins, mark, br, label, textarea, input, script

Chúng ta có thể thay đổi loại phần tử HTML bằng thuộc tính **display**. Các giá trị của thuộc tính này bao gồm **block**, **inline**, **none**. Giá trị **none** sẽ làm ẩn (không hiển thị) phần tử này trên trang web. Ví dụ CSS sau sẽ đổi loại phần tử `span` từ dạng mặc định là inline sang block.

Kết quả áp dụng mẫu CSS trên được minh họa.

Đây là đoạn mã CSS định nghĩa kiểu hiển thị cho các phần tử `<span>` (hiển thị dạng khối, thụt lề 2em, màu đỏ) và phần tử `<p>` (màu xanh).

Đây là đoạn mã HTML tạo một trang với tiêu đề `<h1>`, một đoạn văn `<p>` và nhiều phần tử `<span>` bên trong.

*   Các phần tử HTML đều thuộc một trong hai loại **khối (block)** hoặc **nội tuyến (inline)**. Có thể dùng thuộc tính **display** để thay đổi loại phần tử.

1.  Chiều rộng của các phần tử nội tuyến phụ thuộc vào những yếu tố nào? Có phụ thuộc vào chiều rộng của của sổ trình duyệt không?
2.  Khẳng định "Chiều rộng của các phần tử khối chỉ phụ thuộc vào kích thước của cửa sổ trình duyệt" là đúng hay sai?

## 2. THIẾT LẬP ĐỊNH DẠNG KHUNG BẰNG CSS

Trong hoạt động tiếp theo các em sẽ được làm quen với cách định dạng khung, viền cho các phần tử HTML của trang web. Cần phân biệt hai loại phần tử HTML, phần tử khối và phần tử nội tuyến. Với phần tử dạng khối, các khung được xác định với đầy đủ tính chất, còn với các phần tử nội tuyến thì khung chỉ có thể thiết lập mà không có các thông số chiều cao, chiều rộng.

### Hoạt động 2 Tìm hiểu cách thiết lập định dạng khung cho các phần tử

Quan sát Hình 16.3 để biết các thông số chính của khung của phần tử HTML để có thể hiểu được cách thiết lập khung, viền bằng CSS.

Các thuộc tính liên quan đến khung của một phần tử HTML được mô tả. Lưu ý các thuộc tính này đều không có tính kế thừa.

Các thuộc tính liên quan đến khung:

*   **width**: Chiều rộng của khung. Thuộc tính này chỉ áp dụng cho phần tử dạng khối.
*   **height**: Chiều cao khung. Thuộc tính này chỉ áp dụng cho phần tử dạng khối.
*   **padding**: Vùng đệm, khoảng cách từ vùng text đến đường viền ngoài của khung.
*   **margin**: Lề khung, khoảng cách từ đường viền ngoài của khung đến văn bản xung quanh (nếu có).
*   **border-color**: Màu của viền khung.
*   **border-width**: Độ dày của đường viền khung.
*   **border-style**: Kiểu đường viền khung. Các giá trị có thể là: none, solid, dotted, dashed, double, inset, outset, ridge, groove.
*   **border**: Thuộc tính này có thể gán giá trị là đồng thời các thuộc tính border-width, border-style và border-color, ví dụ: `{border: 2px solid red;}`.

Cho một đoạn mã HTML như sau:
Đoạn mã HTML định nghĩa một trang với tiêu đề cấp 1 "Lịch sử CSS" và một đoạn văn bản mô tả ý tưởng của CSS do Håkon Wium Lie thiết lập, trong đó tên Håkon Wium Lie được in nghiêng.

Nếu thiết lập mẫu định dạng CSS như sau cho đoạn mã HTML ở trên thì kết quả nhận được là tiêu đề "Lịch sử CSS" có viền xanh dương dạng "ridge", kích thước 5px, lề và chiều rộng được đặt, cùng với khoảng đệm. Tên Håkon Wium Lie được in nghiêng có viền đỏ dạng "double", kích thước 2px.

Có thể thiết lập định dạng khung cho các phần tử bằng CSS. Cần phân biệt hai loại **phần tử khối** và **phần tử nội tuyến** với các thông số khác nhau.

1. Trong các thuộc tính khung của một phần tử HTML, khoảng cách từ vùng văn bản đến đường viền khung được gọi là gì?
2. Lề khung khác gì với vùng đệm?

# 3. MỘT SỐ BỘ CHỌN ĐẶC BIỆT CỦA CSS

### Hoạt động 3: Tìm hiểu một số cách thiết lập các bộ chọn đặc biệt khác
Thảo luận, tìm hiểu thêm cách thiết lập bộ chọn đặc biệt của CSS và trả lời các câu hỏi sau:
1. Có thể đặt mẫu định dạng cho các thẻ với thuộc tính cho trước được không?
2. Có thể thiết lập các mẫu định dạng khác nhau cho cùng một loại phần tử giống nhau được không? Nếu có thì thực hiện bằng cách nào?

### a) Thiết lập bộ chọn là một lớp các phần tử có ý nghĩa gần giống nhau
Trong thực tế, có thể có nhu cầu định dạng cho một nhóm phần tử có cùng ý nghĩa, ví dụ các đoạn văn bản có liên quan đến một sự kiện nào đó hoặc một số đoạn văn bản quan trọng cần nhấn mạnh. Trong các trường hợp này, thiết lập bộ chọn lớp **class** cho các phần tử đó để có thể thiết lập định dạng chung. Cấu trúc chung của định dạng CSS liên quan đến lớp:

```
.class {thuộc tính : giá trị;}
```

Ví dụ một số bộ chọn lớp CSS như sau:

Đoạn mã CSS định nghĩa kiểu cho các lớp `warning` (chữ màu đỏ) và `test` (chữ màu xanh, in đậm).

Ví dụ đoạn mã HTML sau được áp dụng mẫu CSS ở ví dụ trên thì đoạn văn bản thứ nhất có chữ màu xanh và in đậm, đoạn văn bản thứ hai có chữ màu đỏ.

Đoạn mã HTML sử dụng các lớp `test` và `warning` cho hai đoạn văn bản.

### b) Thiết lập bộ chọn riêng cho từng phần tử riêng biệt có mã định danh id

Chúng ta đã biết cách thiết lập và gán mã định danh id cho từng phần tử trong tệp HTML. Mỗi phần tử chỉ có một mã định danh id duy nhất trong một trang web.

CSS cho phép thiết lập các mẫu định dạng với các phần tử có id tương ứng như sau:

Đoạn mã CSS sau định nghĩa quy tắc định dạng cho phần tử có id là `idname`.

Ví dụ một số mẫu định dạng ID như sau:

Đoạn mã CSS sau định nghĩa màu chữ đỏ cho phần tử có id là "home".
Đoạn mã CSS sau định nghĩa cỡ chữ 150% cho phần tử `p` có id là "home".

### c) Thiết lập bộ chọn thuộc tính CSS

Một tính chất quan trọng khác của CSS là có thể thiết lập bộ chọn là thuộc tính. Các định dạng này sẽ được thiết lập và áp dụng cho các phần tử nếu được gán với thuộc tính cụ thể nào đó. Sau đây là ví dụ định dạng CSS loại này:

Đoạn mã CSS sau áp dụng viền màu xanh dương 1px liền nét cho tất cả các phần tử có thuộc tính `href`.

Đoạn mã CSS sau áp dụng chữ màu đỏ và in đậm cho tất cả các thẻ `a` với thuộc tính `target` có giá trị `"_blank"`.

Lưu ý: Khi đặt tên cho id và class:
*   Tên của id và class phân biệt chữ in hoa, in thường.
*   Tên bắt buộc phải có ít nhất một kí tự không là số, không bắt đầu bằng số, không chứa dấu cách và các kí tự đặc biệt khác.
*   Một phần tử có thể thuộc nhiều lớp khác nhau. Để khai báo, chúng ta đặt các tên lớp cách nhau bởi dấu cách. Trong ví dụ sau phần tử `p` thuộc đồng thời ba lớp là "test", "more" và "once".

Đoạn mã HTML sau có một thẻ `p` với các lớp "test", "more" và "once".

Có thể thiết lập các mẫu định dạng với bộ chọn là class, ID hoặc thuộc tính.

## Luyện tập
1.  Nêu sự khác biệt cơ bản giữa thuộc tính id và class của các phần tử HTML.
2.  Mỗi bộ chọn sau có ý nghĩa gì?
    a) `div#bat_dau > p.`
    b) `p.test em#p123.`

## 4. THỰC HÀNH

**Nhiệm vụ:** Tạo trang web

**Yêu cầu:** Tạo trang web mô tả bảng 16 tên màu cơ bản CSS.

**Gợi ý:** Bài thực hành có thể thực hiện theo hai bước:
*   Bước 1. Thiết lập bảng với nội dung nhưng chưa định dạng.
*   Bước 2. Viết bổ sung các mẫu CSS để định dạng khung đúng.

### Hướng dẫn:

*   **Bước 1.** Thiết lập trang web theo nội dung như Hình 16.5. Sử dụng các thẻ `<table>`...`</table>` để thiết lập bảng. Tên bảng được thiết lập bằng thẻ `<caption>`...`<caption>`. Các hàng thiết lập bảng thẻ `<tr>`...`</tr>` và ô của bảng thiết lập bằng thẻ `<td>`...`<td>`.
*   Riêng các ô tiêu đề (hàng thứ nhất) sẽ sử dụng thẻ `<th>`. Lưu ý các ô cuối của mỗi hàng cần được thiết lập màu nền theo đúng thông số màu đã ghi tại cột 1 hoặc cột 2.
*   Ví dụ mã nguồn của bảng với 2 hàng đầu tiên như sau, các hàng khác sẽ được thiết lập tương tự:

Mã nguồn HTML minh họa cấu trúc bảng. Đoạn mã này bao gồm thẻ `<table>` để tạo bảng, thẻ `<caption>` để đặt tên bảng là "Bảng tên màu CSS". Tiếp theo là một hàng tiêu đề (`<tr>`) chứa các ô tiêu đề (`<th>`) là "Tên màu", "#hex", "#rgb(r,g,b)", và "Thể hiện". Sau đó là một hàng dữ liệu (`<tr>`) đầu tiên chứa các ô dữ liệu (`<td>`) cho màu "black", mã hex "#000000", giá trị rgb "rgb(0,0,0)", và một ô `<td>` được định dạng màu nền (`background-color`) là "rgb(0,0,0)".

Bước 2. Thiết lập mẫu CSS để tạo khuôn khung, viền cho bảng.
Ví dụ các mẫu định dạng sau:
* Đoạn mã này thiết lập các thuộc tính kiểu dáng CSS cho một bảng, bao gồm viền ngoài của bảng, đệm bên trong các ô, viền và chiều rộng cho các ô dữ liệu (td), viền và màu nền cho ô tiêu đề (th), viền cho hàng (tr) và màu sắc, kích thước chữ, độ đậm, viền và lề cho chú thích (caption).

## LUYỆN TẬP
1. Phần tử html có thể ẩn đi trên trang web được không? Nếu có thì dùng lệnh CSS gì?
2. Hãy giải thích ý nghĩa định dạng sau:
* Đoạn mã này áp dụng màu nền đỏ cho các phần tử có cả hai lớp `.test` và `.test_more`.

## VẬN DỤNG
1. Giả sử nội dung trang web của em có rất nhiều thẻ p, trong đó có ba đoạn mà em thấy quan trọng nhất, kí hiệu các đoạn này là P1, P2, P3. Có cách nào thiết lập định dạng CSS để có thể định dạng P1 khác biệt, P2 và P3 có cùng kiểu và cùng khác biệt không? Tất cả các đoạn còn lại có định dạng giống nhau. Hãy nêu cách giải quyết vấn đề của em.
2. Có thể thiết lập định dạng cho các khung với thông số khung, viền trên, dưới, trái, phải khác nhau được không? Em hãy tìm hiểu và trình bày cách thiết lập định dạng CSS cho các khung, viền như vậy.
