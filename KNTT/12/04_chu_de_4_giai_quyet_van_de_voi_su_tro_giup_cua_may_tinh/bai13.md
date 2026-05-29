# Bài 13: KHÁI NIỆM, VAI TRÒ CỦA CSS

SAU BÀI HỌC NÀY EM SẼ:
*   Hiểu được vai trò và ý nghĩa của mẫu định dạng CSS (Cascading Style Sheets) trong việc trình bày trang web.

Quan sát trang web trong Hình 13.1, trả lời các câu hỏi sau:
*   Mã nguồn trang web có những phần tử HTML nào?
*   Định dạng các phần tử HTML này có đặc điểm chung nào?
*   Có thể định dạng mẫu một lần để áp dụng mẫu đó cho nhiều phần tử HTML được không?

Lịch sử phát triển HTML
Các chuẩn HTML của trang web hiện nay được nhà vật lí Tim Berners-Lee đưa ra lần đầu tiên vào những năm 1990 của thế kỉ XX tại trung tâm vật lí hạt nhân CERN.
Ý tưởng ban đầu của Berners-Lee là muốn thiết lập một chuẩn chung để thể hiện và chia sẻ các văn bản có thể trao đổi bên trong cơ quan CERN.

### Hình 13.1. Trang web

## 1. KHÁI NIỆM MẪU ĐỊNH DẠNG CSS

## Hoạt động 1 Tìm hiểu khái niệm và ý nghĩa của CSS

1.  Hình 13.2 là mã nguồn của trang web trong Hình 13.1. Em có nhận xét gì về cách thiết lập định dạng của trang này?

Đoạn mã này là một trang HTML cơ bản. Phần `<head>` chứa siêu dữ liệu và một khối `<style>` định nghĩa các quy tắc CSS:
*   Tiêu đề `h1` sẽ có màu chữ đỏ và viền liền 2px màu xanh dương.
*   Đoạn văn `p` sẽ có thụt đầu dòng 15px.
Phần `<body>` chứa một tiêu đề `h1` và hai đoạn văn `p` với nội dung về lịch sử phát triển HTML.

### Hình 13.2. Mã nguồn của trang web

2.  Em thấy gì từ đoạn mã nguồn trên?

Trong đoạn mã nguồn ở Hình 13.2, các dòng từ 6 đến 10 là một loại ngôn ngữ đặc biệt dùng để thiết lập các mẫu định dạng cho trang web. Các mẫu định dạng này được gọi là **Cascading Style Sheet** và viết tắt là **CSS**.

Mô tả các quy tắc định dạng CSS cho tiêu đề cấp 1 (h1) và đoạn văn (p). Cụ thể: thiết lập màu chữ đỏ và viền xanh dày 2px cho h1; thiết lập lề thụt đầu dòng 15px cho p.

CSS là định dạng độc lập với chuẩn HTML, được dùng để thiết lập các mẫu định dạng dùng trong trang web.

Trong Hình 13.3, ba mẫu định dạng tương ứng với ba dòng được ghi trong thẻ `<style>....</style>` (trong phần tử head): Mẫu thứ nhất thiết lập màu chữ đỏ cho các phần tử `<h1>`. Mẫu thứ hai thiết lập khung viền màu xanh có độ dày 2 pixel (mỗi pixel = 2,54/96 cm) cũng được áp dụng cho các phần tử `<h1>`. Mẫu thứ ba thiết lập dòng đầu thụt vào 15 pixel cho tất cả các phần tử `<p>`.

Như vậy CSS có thể hiểu là tập hợp các mẫu định dạng viết độc lập với mã nguồn html của trang web và dùng để định dạng cho các phần tử HTML tương ứng. CSS có cách viết riêng (ngôn ngữ CSS), độc lập với ngôn ngữ HTML. Chỉ cần viết mẫu định dạng một lần và được áp dụng đồng thời cho tất cả các phần tử, ví dụ `<h1>` và `<p>` trong trang web trên.

Mẫu định dạng CSS là một công cụ hỗ trợ giúp định dạng nội dung trang web nhanh hơn, thuận tiện hơn bằng cách định nghĩa một lần và sử dụng nhiều lần. CSS sử dụng ngôn ngữ mô tả riêng, độc lập với HTML.

## Em cần chú ý
1. Ngôn ngữ CSS có phải là HTML không?
2. Các mẫu định dạng CSS thường được mô tả như thế nào?
*   A. Trong một bảng.
*   B. Phải viết trên một hàng.
*   C. Có thể viết trên nhiều hàng.

## 2. CẤU TRÚC CSS
### Hoạt động 2 Tìm hiểu cấu trúc tổng quát của CSS
Quan sát, tìm hiểu và thảo luận về cấu trúc tổng quát của các mẫu định dạng CSS.

Cấu trúc tổng quát của một mẫu định dạng CSS có hai phần: **bộ chọn** (selector) và **vùng mô tả** (declaration block). Vùng mô tả bao gồm một hay nhiều quy định có dạng {thuộc tính : giá trị ; }, các quy định được viết cách nhau bởi dấu “;”. Bộ chọn sẽ quy định những thẻ HTML nào được chọn để áp dụng định dạng này.
Cấu trúc CSS có thể ở dạng đơn giản, trong đó vùng mô tả chỉ có một quy định:
```
bộ chọn {thuộc tính: giá trị;}
```

hoặc nhiều quy định ở vùng mô tả như sau:

Cấu trúc khai báo CSS với bộ chọn, thuộc tính và giá trị:
```
bộ chọn {
    thuộc tính 1: giá trị 1;
    thuộc tính 2: giá trị 2;
    ...
    thuộc tính n: giá trị n;
}
```

Ví dụ 1: Mẫu CSS thiết lập màu chữ đỏ cho bộ chọn là tất cả các thẻ h1.
Đoạn mã CSS này định nghĩa màu chữ (color) của thẻ `h1` là màu đỏ (red).

Ví dụ 2: Mẫu CSS gồm hai quy định, thụt lề dòng đầu và chữ màu xanh áp dụng cho bộ chọn là tất cả các thẻ p.
Đoạn mã CSS này định nghĩa thụt lề dòng đầu (text-indent) của thẻ `p` là 15 pixel và màu chữ (color) là màu xanh (blue).

Bộ chọn có thể là một thẻ để áp dụng các quy định như hai ví dụ trên hoặc đồng thời nhiều thẻ. Cách viết này giúp cho CSS dễ thiết lập và áp dụng.

Ví dụ 3: Mẫu CSS sau thiết lập định dạng chữ đỏ cho đồng thời các thẻ h1, h2, h3. Các thẻ này được viết cách nhau bởi dấu phẩy.
Đoạn mã CSS này định nghĩa màu chữ (color) của các thẻ `h1`, `h2`, `h3` là màu đỏ (red).

Có ba cách thiết lập CSS là **CSS trong** (internal CSS), **CSS ngoài** (external CSS) và **CSS nội tuyến** (inline CSS).

### a) Cách thiết lập CSS trong

Cách thiết lập này đưa toàn bộ các mẫu định dạng vào bên trong thẻ **<style>** và đặt trong phần tử **head** của tệp HTML. Với cách thiết lập này các định dạng sẽ áp dụng cho tất cả các phần tử HTML của trang web phù hợp với mô tả bộ chọn của CSS. Với cách thiết lập CSS trong, các mẫu định dạng CSS chỉ được áp dụng cho tệp HTML hiện thời. Cách thiết lập CSS trong ví dụ ở Hoạt động 1 là thiết lập CSS trong.

### b) Cách thiết lập CSS ngoài

Các mẫu định dạng CSS được viết trong một tệp css, bên ngoài tệp HTML. Tệp css này sẽ bao gồm các mẫu định dạng như đã mô tả ở trên, theo ngôn ngữ CSS. Sau đó, cần thực hiện thao tác kết nối, liên kết tệp HTML với tệp định dạng css.

Tệp **styles.css** sau là ví dụ cách thiết lập tệp css ngoài. Các dòng chú thích dưới dạng `/* ...... */` và có thể trên nhiều dòng.

Nội dung tệp `styles.css` mô tả các quy tắc CSS:
*   Bắt đầu bằng một chú thích: "tệp thông tin CSS".
*   Định nghĩa màu chữ cho thẻ `h1` là màu đỏ.
*   Định nghĩa viền cho thẻ `h1` là 2 pixel, kiểu solid và màu xanh.
*   Định nghĩa thụt lề dòng đầu cho thẻ `p` là 15 pixel.

Cách kết nối tệp HTML với CSS như sau:

**Cách 1:** Sử dụng thẻ **link** đặt trong vùng **head** của trang web, ví dụ:
Đoạn mã HTML này đặt trong phần `<head>` của trang, sử dụng thẻ `<link>` để liên kết đến tệp `styles.css`. Thuộc tính `rel="stylesheet"` chỉ định đây là một bảng kiểu, và `type="text/css"` chỉ định loại là CSS.

Cách 2: Sử dụng lệnh `@import` đặt trong phần tử `style` và nằm trong phần `head` của trang web, ví dụ:
Mã này minh họa cách sử dụng lệnh `@import` để nhúng một tệp CSS bên ngoài có tên "styles.css" vào trong phần `<style>` của trang web.
Một tệp CSS có thể được thiết lập để đồng thời áp dụng cho nhiều trang web, giúp cho việc định dạng nhiều trang web thống nhất và khi cần chỉnh sửa định dạng thì chỉ cần sửa một lần trong tệp định dạng css.

### c) Cách thiết lập CSS nội tuyến
Có thể định dạng CSS trực tiếp bên trong thẻ của các phần tử HTML bằng cách chỉ ra các thuộc tính và giá trị cho thuộc tính `style`. Cách làm này mất thời gian nhưng thời gian thực hiện sẽ nhanh. Các lợi ích khác của cách thiết lập CSS nội tuyến sẽ được trình bày trong phần sau.

Cấu trúc tổng quát của CSS bao gồm các mẫu định dạng dùng để tạo khuôn cho các phần tử HTML của trang web. Mỗi mẫu này bao gồm hai phần: **bộ chọn** và **vùng mô tả**. Có thể thiết lập CSS trong, ngoài thông qua tệp CSS hoặc đặt **nội tuyến** trực tiếp bên trong các phần tử HTML thông qua thuộc tính **style**.

1. Nếu muốn thiết lập CSS để áp dụng cho toàn bộ tệp HTML thì làm cách nào?
2. Nếu muốn thiết lập CSS để có thể áp dụng đồng thời cho nhiều trang web thì làm cách nào?

## 3. VAI TRÒ, Ý NGHĨA CỦA CSS
### Hoạt động 3 Tìm hiểu ý nghĩa, vai trò của CSS
Tìm hiểu, thảo luận và trả lời các câu hỏi sau:
1. Nếu không dùng CSS thì các định dạng của trang web phải thực hiện theo cách nào?
2. Sử dụng CSS có những ưu điểm gì trong việc định dạng trang web?

Nếu không dùng CSS thì khi định dạng nội dung trang web ta phải thực hiện thông qua việc thiết lập các thuộc tính cho từng phần tử HTML. Nếu có nhiều trang web và có nhiều phần tử HTML thì công việc này mất nhiều thời gian và có thể không thống nhất. CSS ra đời để phục vụ việc định dạng nội dung trang web một cách thống nhất, nhanh chóng và thuận tiện.
* CSS sẽ giúp tách việc nhập nội dung trang web bằng thẻ HTML và việc định dạng thành hai công việc độc lập với nhau. Điều này sẽ làm giảm nhẹ công việc nhập nội dung, tăng tính chuyên nghiệp của việc định dạng.
* Các mẫu định dạng của CSS có thể được viết ngay trong phần **head** của trang html, chỉ cần viết một lần và áp dụng cho tất cả các phần tử trong bộ chọn. Như vậy, các định dạng này được thiết lập một lần và được dùng nhiều lần.

* Các mẫu định dạng có thể viết trong tệp CSS ngoài và kết nối vào bất kì trang web nào. Tính năng này cho phép định dạng một lần và áp dụng cho nhiều trang web, thậm chí cả một website. Một ý nghĩa khác là nếu một website (hay trang web) cần thay đổi định dạng thì có thể chỉ cần chỉnh sửa một lần.

CSS được thiết lập với mục đích làm cho công việc định dạng nội dung trang web trở nên khoa học hơn, nhanh hơn, thuận tiện hơn. Với CSS, các mẫu định dạng được thiết kế độc lập, có thể viết ra một lần nhưng được áp dụng nhiều lần.

1.  Nếu muốn tất cả các đoạn văn bản của trang web có màu xanh (blue) thì cần thiết lập định dạng CSS như thế nào?
2.  Giả sử có một mẫu định dạng CSS như sau:
    Mã CSS này định nghĩa một đường viền liền màu đỏ, dày 2 pixel cho các thẻ tiêu đề h1, h2 và h3.
    Hãy giải thích ý nghĩa của mẫu định dạng CSS trên.

## LUYỆN TẬP
1.  Ngôn ngữ định dạng CSS chính là ngôn ngữ HTML, đúng hay sai?
2.  Khẳng định sau là đúng hay sai: Có thể chỉ cần thay đổi thông tin của một tệp CSS sẽ làm thay đổi định dạng của nhiều trang web, thậm chí cả một website.
