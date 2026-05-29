# Bài 10: BỘ CHỌN LỚP, BỘ CHỌN ĐỊNH DANH

Học xong bài này, em sẽ:
* Sử dụng được bộ chọn lớp, bộ chọn định danh.

Trong một trang web có 5 đoạn văn bản, em có biết khai báo CSS như thế nào để trình bày đoạn văn bản đầu tiên và cuối cùng chữ màu đỏ, còn các đoạn văn bản còn lại chữ màu xanh không?

## 1. Bộ chọn lớp

Mỗi **bộ chọn lớp** (class selector) được đặt tên, thường được dùng để khai báo các quy tắc định dạng được áp dụng chung cho nhiều phần tử trong văn bản HTML thay vì phải viết lặp lại các quy tắc này cho từng phần tử.
Bộ chọn lớp được khai báo như sau:
Mô tả cú pháp khai báo bộ chọn lớp: `Tên_bộ_chọn_lớp {thuộc tính 1: giá trị;...; thuộc tính n: giá trị;}`.

Trong đó, *Tên_bộ_chọn_lớp* do người tạo CSS tự định nghĩa và bắt đầu bằng dấu chấm.

Ví dụ 1. Bảng định dạng CSS khai báo bộ chọn lớp được đặt tên là “red” và khai báo giá trị thuộc tính màu đỏ:
Mô tả đoạn mã khai báo bộ chọn lớp `red` trong CSS: `.red {color: red;}`.

Để áp dụng bộ chọn lớp có tên “*Tên_bộ_chọn_lớp*” cho phần tử cụ thể của văn bản HTML, cần khai báo giá trị thuộc tính `class` của phần tử đó là “*Tên_bộ_chọn_lớp*”.

Ví dụ 2. Văn bản HTML minh họa việc áp dụng bộ chọn lớp, kết quả hiển thị trên màn hình trình duyệt web như mô tả dưới đây. Các phần tử có thuộc tính `class = “red”` đều được trình bày bằng chữ màu đỏ.
Mô tả đoạn mã HTML sử dụng bộ chọn lớp:
Đoạn mã HTML định nghĩa style CSS cho lớp `red` với màu chữ đỏ, sau đó áp dụng lớp `red` này cho thẻ `h1`, thẻ `p` và thẻ `label` trong phần `<body>`.

Kết quả khi mở văn bản HTML bằng trình duyệt web:
Tiêu đề có chữ màu đỏ
Đoạn văn có chữ màu đỏ
Nhân có chữ màu đỏ

Sử dụng bộ chọn lớp còn giúp tùy biến các định dạng trình bày cho các nội dung được tạo bởi cùng loại phần tử HTML. Ví dụ, một số đoạn văn bản được trình bày chữ màu xanh, một số đoạn văn bản được trình bày chữ màu đỏ trong cùng một trang web. Bộ chọn lớp sử dụng cho một phần tử được khai báo như sau:

`Phần tử.Tên_bộ_chọn_lớp {thuộc tính 1: giá trị;...; thuộc tính n: giá trị;}`

Ví dụ 3. Văn bản HTML minh hoạ việc áp dụng các bộ chọn lớp khác nhau cho cùng một kiểu phần tử, kết quả hiển thị trên màn hình trình duyệt web. Các phần tử `p` có thuộc tính `class = “red”` được trình bày chữ màu đỏ. Các phần tử `p` có thuộc tính `class = “blue”` được trình bày chữ màu xanh. Phần tử `p` nếu không có khai báo thuộc tính `class`, mặc định chữ có màu đen.

Đoạn mã HTML và CSS minh họa việc sử dụng bộ chọn lớp (`class selector`) để định dạng các đoạn văn bản. Các đoạn văn bản có `class="red"` được định dạng màu đỏ, các đoạn có `class="blue"` được định dạng màu xanh. Đoạn văn bản không có lớp sẽ hiển thị màu mặc định.

Kết quả hiển thị trong trình duyệt web cho thấy các dòng chữ được tô màu đỏ, màu xanh và màu đen tương ứng với định dạng đã khai báo.

## 2. Bộ chọn định danh

Em có biết cách khai báo định dạng CSS để chỉ áp dụng cho một phần tử cụ thể trên trang web không?

CSS có thể sử dụng **bộ chọn định danh (ID selector)** để áp dụng quy tắc định dạng cho một phần tử đã được định danh trong văn bản HTML. Khi đó, bộ chọn định danh được xác định thông qua *Tên_định_danh* của phần tử này và được khai báo như sau:

`#Tên_định_danh {thuộc tính 1: giá trị;...; thuộc tính n: giá trị;}`

Ví dụ 4. Văn bản HTML khai báo và áp dụng quy tắc định dạng dùng bộ chọn định danh, kết quả hiển thị trên trình duyệt web, phần tử `h1` với định danh là “tieu-de-muc-chinh” sẽ được trình bày chữ màu đỏ.

Đoạn mã HTML minh họa việc sử dụng bộ chọn định danh để định dạng tiêu đề. Nó định nghĩa một kiểu CSS cho phần tử có `id="tieu_de_muc_chinh"` là màu đỏ và áp dụng kiểu này cho tiêu đề "Chương 1", trong khi tiêu đề "Chương 2" không được áp dụng kiểu đặc biệt.

## Luyện tập
### Nhiệm vụ 1. Khai báo và áp dụng bộ chọn lớp
Soạn văn bản HTML có khai báo CSS sử dụng bộ chọn lớp để được trang web hiển thị trên màn hình trình duyệt web như ở Hình 5.

#### Yêu cầu 1:
Em hãy sử dụng external CSS tạo bảng định dạng gồm các quy tắc sau:
*   Bộ chọn lớp có tên **blue** khai báo định dạng màu **steelblue**.
*   Bộ chọn lớp có tên **red** khai báo định dạng màu **darkred**.
*   Bộ chọn lớp có tên **orangered** để khai báo các thuộc tính định dạng CSS: tên phông chữ “**Verdana**”, cỡ chữ **25 pixel**, màu chữ **orangered**.
*   Bộ chọn lớp có tên **yellow** cho phần tử **input** để khai báo thuộc tính CSS: màu nền **yellow**.
*   Bộ chọn lớp có tên **blue** cho phần tử **input** để khai báo thuộc tính CSS: màu nền **blue**, màu chữ **white**.

#### Hướng dẫn thực hiện:
*   Bước 1. Tạo tệp “Bai10-NV1.css”.
    *   Mở phần mềm Sublime Text.
    *   Tạo tệp mới và ghi lưu với tên “Bai10-NV1.css”.
*   Bước 2. Khai báo các quy tắc định dạng CSS như sau:

Các khai báo CSS định nghĩa các lớp `.blue` (màu chữ `steelblue`), `.red` (màu chữ `darkred`), `.orangered` (phông chữ `Verdana`, cỡ chữ `25px`, màu chữ `orangered`), và các kiểu cho thẻ `<input>` có lớp `.yellow` (nền `yellow`) và thẻ `<input>` có lớp `.blue` (nền `blue`, chữ `white`).

Bước 3. Ghi lưu tệp.

#### Yêu cầu 2:
Áp dụng khai báo external CSS đã hoàn thành ở Yêu cầu 1 để định dạng trình bày trang web.

#### Hướng dẫn thực hiện:
*   Bước 1. Mở tệp "Bai9-NV2.html" đã soạn ở Bài 9, ghi lưu với tên tệp mới là “Bai10-NV1.html”. Lưu ý, cần lưu cùng thư mục với tệp “Bai10-NV1.css”.
*   Bước 2. Khai báo áp dụng định dạng external CSS.
    *   Trong nội dung phần tử `head`, sửa khai báo liên kết đến external CSS: Sử dụng thẻ `<link>` để liên kết đến tệp CSS ngoại vi `Bai10-NV1.css`.
*   Bước 3. Khai báo các thuộc tính **class** cho các phần tử.
    *   Trong nội dung phần tử `body`:
        *   Thêm khai báo thuộc tính **class** cho phần tử `h2` như sau: Áp dụng lớp `red` cho phần tử `h2`.
        *   Thêm khai báo thuộc tính **class** cho phần tử `h3` của tiêu đề mục “1. Thông tin về người góp ý” như sau: Áp dụng các lớp `blue` và `orangered` cho phần tử `h3`. Chú ý, giá trị của thuộc tính **class** có thể gồm nhiều bộ chọn lớp được viết phân tách bởi dấu cách. Khi đó, các khai báo định dạng CSS thuộc bộ chọn lớp `blue` và `orangered` đều được áp dụng.
        *   Thêm khai báo thuộc tính **class = "blue"** cho các phần tử `h3` khác.
        *   Thêm khai báo thuộc tính **class = "yellow"** cho các phần tử `input` nhập liệu ô text.
        *   Thêm khai báo thuộc tính **class = "blue"** cho phần tử `input` gửi dữ liệu.
*   Bước 4. Ghi lưu, mở tệp bằng trình duyệt web và xem kết quả.

### Nhiệm vụ 2. Khai báo và áp dụng bộ chọn định danh

#### Yêu cầu:
Em hãy chỉnh sửa văn bản HTML đã hoàn thành ở Nhiệm vụ 1 để khai báo định dạng CSS theo bộ chọn định danh cho tiêu đề “Đóng góp ý kiến cho thư viện của nhà trường” có phông chữ “Courier New”, cỡ chữ 30 pixel, màu chữ `lightsalmon`.

#### Hướng dẫn thực hiện:
*   Bước 1. Mở tệp “Bai10-NV1.html” đã hoàn thành ở Nhiệm vụ 1, ghi lưu với tên mới là “Bai10-NV2.html”.
*   Thêm khai báo CSS định nghĩa một bộ chọn định danh (`id`) tên `tieu-de` với phông chữ `Courier New`, cỡ `30px` và màu chữ `lightsalmon` vào trong phần khai báo `<style></style>`.

a) Khai báo CSS sử dụng bộ chọn phần tử cho phần tử *h1* vì nội dung văn bản HTML chỉ gồm các phần tử tiêu đề mục *h1*.

b) Thực hiện các bước sau:
Bước 1. Khai báo CSS sử dụng **bộ chọn lớp** để định dạng màu chữ khác với màu mặc định.
Đoạn mã CSS khai báo hai bộ chọn lớp `.tieude1` (màu đỏ) và `.tieude2` (màu xanh).
Bước 2. Khai báo thuộc tính *class="tieude1"* cho các tiêu đề mục chữ có màu đỏ, khai báo thuộc tính *class="tieude2"* cho các tiêu đề đề mục chữ có màu xanh.

c) Thực hiện các bước sau:
Bước 1. Khai báo CSS sử dụng **bộ chọn định danh** để định dạng tiêu đề mục chữ có màu xanh, các tiêu đề khác sử dụng **bộ chọn phần tử** *h1*.
Đoạn mã CSS khai báo bộ chọn định danh `#tieude1` (màu xanh) và bộ chọn phần tử `h1` (màu đỏ).
Bước 2. Khai báo thuộc tính *class = "tieude1"* cho tiêu đề mục chữ có màu xanh.

d) Thực hiện các bước sau:
Bước 1. Kết hợp khai báo CSS sử dụng **bộ chọn lớp**, **bộ chọn định danh**:
Đoạn mã CSS kết hợp khai báo bộ chọn lớp `.tieude1` (màu đỏ) và bộ chọn định danh `#tieude2` (màu xanh).
Bước 2. Khai báo thuộc tính *class = "tieude1"* cho các tiêu đề đề mục chữ màu đỏ, khai báo thuộc tính *id= "tieude2"* cho các tiêu đề đề mục chữ có màu xanh.

## Tóm tắt bài học
*   **Bộ chọn lớp** thường dùng để khai báo các quy tắc định dạng được áp dụng chung cho nhiều phần tử trong văn bản HTML.
*   **Bộ chọn định danh** được dùng để khai báo các quy tắc định dạng chỉ áp dụng cho một phần tử cụ thể trong văn bản HTML.
