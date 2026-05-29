# Bài 8: LÀM QUEN VỚI CSS

**Học xong bài này, em sẽ:**
* Nêu được mục đích sử dụng CSS.
* Mô tả được bộ chọn phần tử và cách áp dụng CSS.
* Trình bày được một số thuộc tính định dạng CSS.

Theo em, làm thế nào để trình bày các đoạn văn, tiêu đề, nhãn trong trang web có cùng màu chữ?

## 1. Bảng định dạng CSS

**Bảng định dạng** (Cascading Style Sheets – CSS) là ngôn ngữ được sử dụng để khai báo kiểu trình bày các phần tử HTML trong trang web. CSS thường gồm một số quy tắc định dạng. Mỗi quy tắc định dạng như minh hoạ gồm bộ chọn (**selector**) và các khai báo thuộc tính CSS (**css properties**) để xác định kiểu trình bày cho phần tử, ví dụ: màu sắc, phông chữ, kích cỡ, đường viền,...

**Mô tả đoạn mã:**
Đoạn mã CSS này định nghĩa hai quy tắc định dạng:
*   Quy tắc thứ nhất áp dụng cho phần tử `p` (đoạn văn bản), đặt màu chữ là đỏ và kiểu chữ in đậm.
*   Quy tắc thứ hai áp dụng cho phần tử `h1` (tiêu đề cấp 1), đặt màu nền là vàng.

Sử dụng CSS giúp tách biệt khai báo nội dung với định dạng và trang trí trang web. Với sự tách biệt như vậy, khai báo CSS dễ dàng được chỉnh sửa, tái sử dụng. Sử dụng CSS còn cho phép nhiều trang web hay toàn bộ website cùng dùng chung quy tắc định dạng nhằm tạo sự thống nhất trong trình bày.

Trình duyệt web áp dụng CSS bằng cách chọn các phần tử trong văn bản HTML khớp với bộ chọn trong CSS và sử dụng các quy tắc định dạng tương ứng để trình bày phần tử.

Phiên bản đầu tiên CSS1 được công bố vào năm 1996. Cho đến nay, CSS đã cập nhật và hoàn thiện thêm một số phiên bản. Trong quyển sách này, phiên bản CSS3 được sử dụng để minh hoạ khai báo CSS.

## 2. Khai báo bộ chọn phần tử và áp dụng CSS

Bộ chọn phần tử thường được dùng để áp dụng CSS cho một hoặc nhiều phần tử cụ thể trong văn bản HTML nhằm tạo sự thống nhất trong trình bày, ví dụ: trình bày chữ in nghiêng cho các đoạn văn bản trên trang web. Với mỗi phần tử HTML, CSS định nghĩa một bộ chọn tương ứng và đặt tên theo tên phần tử đó.

Bộ chọn phần tử được khai báo như sau:
`Tên_bộ_chọn_phần_tử {thuộc tính 1 : giá trị;...; thuộc tính n : giá trị;}`

Ví dụ 1. Quy tắc định dạng sau xác định kiểu trình bày nội dung của phần tử p trong văn bản HTML có chữ màu đỏ và in đậm: `p {color: red; font-weight: bold;}`

Có hai cách khai báo để áp dụng CSS trong văn bản HTML được sử dụng phổ biến là: **CSS trong (internal CSS)**, **CSS ngoài (external CSS)**.

Khai báo **internal CSS** thường được sử dụng khi muốn áp dụng CSS trong phạm vi một văn bản HTML. Các quy tắc định dạng internal CSS được viết trong cặp thẻ `<style></style>` và thường được đặt trong nội dung của phần tử **head**.

Ví dụ 2. Trong văn bản HTML, có một phần khai báo CSS sử dụng bộ chọn phần tử để đặt màu chữ cho đoạn văn `p` là màu xanh và tiêu đề `h1` là màu đỏ. Cụ thể, trong phần `<head>` có các quy tắc CSS: `p {color: blue;}` và `h1 {color: red;}`. Khi mở văn bản bằng trình duyệt web, các tiêu đề mục `h1` sẽ có chữ màu đỏ và các đoạn văn `p` có chữ màu xanh. Kết quả hiển thị bao gồm: "Tiêu đề mục 1" (màu đỏ), "Đoạn văn 1" (màu xanh), "Tiêu đề mục 2" (màu đỏ), "Đoạn văn 2" (màu xanh).

Khai báo **external CSS** thường được sử dụng khi cần áp dụng chung bảng định dạng CSS cho nhiều văn bản HTML. Các quy tắc định dạng được ghi lưu dưới dạng tệp có phần mở rộng `*.css`. Để áp dụng external CSS, trong nội dung phần **head** của văn bản HTML, cần khai báo tham chiếu đến tệp CSS có dạng `Tên_tệp.css`, được viết dưới dạng `<link rel = “stylesheet” href = “Tên_tệp.css”>`.

Ví dụ 3. Văn bản HTML ở Hình 4a áp dụng các quy tắc định dạng được khai báo trong tệp external CSS có tên “default.css” (Hình 4b), kết quả hiển thị trên màn hình trình duyệt web như ở Hình 4c.

* Đoạn mã HTML này liên kết đến một tệp CSS bên ngoài (`default.css`) để áp dụng các quy tắc định dạng. Trong nội dung trang, có một tiêu đề cấp 1 và một đoạn văn bản.

* Đoạn mã CSS từ tệp `default.css` này định nghĩa rằng các đoạn văn bản (`p`) sẽ có màu chữ đỏ và in đậm, còn tiêu đề cấp 1 (`h1`) sẽ có màu nền vàng.

*Kết quả khi mở văn bản HTML trên trình duyệt web (Hình 4c):*
Màu nền của Heading 1 tô màu vàng
Nội dung đoạn văn có màu đỏ, in đậm

Trong trường hợp một số phần tử có các khai báo CSS giống nhau, có thể viết gộp nhiều bộ chọn để không phải khai báo lặp lại thuộc tính CSS nhiều lần cho từng phần tử. Khi đó, bộ chọn gồm danh sách các phần tử, ngăn cách nhau bởi dấu “,”.
Ví dụ 4. Các bộ chọn p, h1 và h2, h3 cùng có chung quy tắc định dạng nên được viết gộp như ở Hình 5.

* Đoạn mã CSS này minh họa việc gộp các bộ chọn: các phần tử `p` và `h1` sẽ có màu chữ xanh dương và cỡ chữ 20px; các phần tử `h2` và `h3` sẽ có màu nền vàng và phông chữ Verdana.

## 3. Một số thuộc tính định dạng CSS

Em hãy nêu một số thuộc tính định dạng cho đoạn văn bản mà em đã dùng trong hệ soạn thảo văn bản Microsoft Word.

### a) Thuộc tính định dạng màu sắc

Thuộc tính **color** định dạng màu chữ, được khai báo như sau:

`color: Màu;`

Trong đó, giá trị **Màu** thường được xác định bởi tên màu phổ biến như red, green, blue, yellow, brown,...

Ví dụ 5. Văn bản HTML này định dạng màu chữ cho các phần tử HTML: các phần tử `h1`, `h2` có màu xanh nước biển, phần tử `p` có màu đỏ.

Đoạn mã HTML tương ứng:
```html
<!DOCTYPE html>
<html>
<head>
<title>CSS</title>
<meta charset="utf-8">
<style>
p {color: red;}
h1, h2 {color: blue;}
</style>
</head>
<body>
<h1> Heading 1 có màu xanh</h1>
<h2> Heading 2 có màu xanh</h2>
<p>Đoạn văn có màu đỏ</p>
</body>
</html>
```

Kết quả hiển thị trên trình duyệt web:
* Heading 1 có màu xanh
* Heading 2 có màu xanh
* Đoạn văn có màu đỏ

Thuộc tính **background-color** định dạng màu nền, áp dụng được cho tất cả phần tử, được khai báo như sau:

`background-color: Màu;`

Ví dụ 6. Văn bản HTML này định dạng màu nền cho trang web là màu xanh lơ.

Đoạn mã HTML tương ứng:
```html
<!DOCTYPE html>
<html>
<head>
<title>CSS</title>
<meta charset="utf-8">
<style>
body {background-color: cyan;}
</style>
</head>
<body>
</body>
</html>
```

Kết quả hiển thị trên trình duyệt web:
(Trang web có nền màu xanh lơ)

### b) Thuộc tính định dạng phông chữ

Thuộc tính **font-family** xác định tên phông chữ, áp dụng được cho tất cả phần tử HTML, được khai báo như sau:

`font-family: Tên phông chữ;`

Trong đó, **Tên phông chữ** là một hoặc nhiều tên phông chữ được ngăn cách nhau bởi dấu “,”. Chú ý, nếu tên phông chữ có dấu cách thì phải được đặt trong cặp dấu nháy kép (“ ”).

Thuộc tính **font-size** xác định kích cỡ chữ, áp dụng được cho tất cả các phần tử, được khai báo như sau:

`font-size: Kích cỡ;`

Trong đó, giá trị **Kích cỡ** thường được tính theo đơn vị điểm ảnh (**pixel**) hoặc tỉ lệ phần trăm.

Ví dụ 7. Văn bản HTML trong Hình 8a sẽ trình bày phần tử p có phông chữ *Times New Roman*, cỡ chữ 20 *pixel* khi hiển thị trên màn hình trình duyệt web (Hình 8b).

Đoạn mã HTML sau minh họa cách khai báo CSS để định dạng phông chữ và kích cỡ cho đoạn văn bản:
Nội dung HTML là một trang web đơn giản với tiêu đề "CSS". Trong phần `<style>`, nó định nghĩa rằng tất cả các thẻ `<p>` sẽ có font là "Times New Roman" và kích thước là 20px. Trong phần `<body>` có một đoạn văn bản `<p>` với nội dung "Định dạng phông và kích cỡ chữ".

Kết quả hiển thị trên trình duyệt web là dòng chữ: Định dạng phông và kích cỡ chữ.

## c) Thuộc tính định dạng đường viền

Thuộc tính **border-style** xác định kiểu trình bày đường viền của phần tử, được khai báo như sau:

`border-style: Kiểu trình bày;`

CSS quy định cụ thể các **Kiểu trình bày**. Một số kiểu trình bày thông dụng gồm:
* **dotted** – đường viền là những dấu chấm liền nhau, **solid** – đường viền là một đường đậm liền nét.

Thuộc tính **border-color** xác định màu đường viền của phần tử, được khai báo như sau:

`border-color: Màu;`

Lưu ý: Định dạng thuộc tính **border-color** chỉ được áp dụng khi thuộc tính **border-style** được khai báo.

Ví dụ 8. Văn bản HTML trong Hình 9a trình bày đường viền màu đỏ, nét liền đậm bao quanh phần tử p khi hiển thị trên màn hình trình duyệt web (Hình 9b).

Đoạn mã HTML này định nghĩa một tài liệu HTML với một kiểu CSS nội bộ. Kiểu CSS này áp dụng một đường viền **solid** màu đỏ cho tất cả các phần tử `<p>`. Trong phần `<body>`, có một đoạn văn bản "Đường viền màu đỏ nét đậm" được đặt trong thẻ `<p>`.

Kết quả hiển thị: Đường viền màu đỏ nét đậm

## Luyện tập

* Em hãy soạn văn bản HTML có hai đoạn văn bản được tạo bởi phần tử p. Khai báo và áp dụng **internal CSS** để trình bày trang web có nền màu xanh lơ (**cyan**); đoạn văn bản có chữ màu đỏ, phông chữ Arial, cỡ chữ 15 pixel.

* Em hãy chuyển các khai báo **internal CSS** trong mục Luyện tập thành khai báo **external CSS** ghi lưu với tên tệp “styles.css”, tạo mới văn bản HTML để áp dụng bảng định dạng *styles.css* này.

* Mỗi phát biểu sau đây về CSS là đúng hay sai?
  * a) Sử dụng CSS giúp tách biệt khai báo nội dung với định dạng và trang trí trang web.
  * b) Để áp dụng CSS, trong văn bản HTML phải khai báo tham chiếu đến tệp CSS.
  * c) Sử dụng **external CSS** giúp cho nhiều trang web trong một **website** có thể dùng chung kiểu định dạng và trang trí.
  * d) Khai báo CSS sử dụng bộ chọn phần tử: `p{color=red; font-size:20px;}` là đúng cú pháp.

## Tóm tắt bài học

* **CSS** dùng để khai báo quy tắc định dạng trình bày các phần tử HTML trên trình duyệt web.
* **Bộ chọn phần tử** thường được dùng để áp dụng CSS cho tất cả các phần tử cùng loại trong văn bản HTML nhằm tạo sự thống nhất trong trình bày.
* Hai cách khai báo CSS thường được sử dụng là **internal CSS** và **external CSS**.
* CSS định nghĩa một số thuộc tính để định dạng trình bày: màu sắc, phông chữ, cỡ chữ, đường viền.
