# Bài 11: MÔ HÌNH HỘP, BỐ CỤC TRANG WEB

Học xong bài này, em sẽ:
*   Mô tả được mô hình hộp trong trình bày phần tử HTML.
*   Trình bày được cách hiển thị phần tử theo khối, theo dòng.
*   Nhận diện được các thành phần cơ bản trong bố cục trang web.

Em hãy truy cập trang chủ của các website: https://moet.gov.vn, https://tienphong.vn. Theo em, bố cục của hai trang web này có giống nhau không?

## 1. Mô hình hộp trong trình bày phần tử HTML

Các phần tử trong văn bản HTML được trình bày trên trình duyệt web theo **mô hình hộp (box model)**. Theo đó, mỗi phần tử khi được trình bày có cấu trúc logic gồm các hộp chữ nhật xác định các vùng nội dung và vùng đường viền.

Ngăn cách nhau giữa vùng nội dung và vùng đường viền là một vùng đệm mặc định hiển thị trong suốt, giúp phân tách nội dung và đường viền khi hiển thị trên màn hình trình duyệt web. Vùng lề là một vùng mặc định hiển thị trong suốt, bao ngoài vùng đường viền để phân tách các phần tử được hiển thị cạnh nhau.

Thông thường, các trình duyệt web tự động căn chỉnh để toàn bộ các phần tử được khai báo trong văn bản HTML hiển thị đầy đủ trên màn hình trình duyệt web. Tuy vậy, hoàn toàn có thể điều chỉnh kích cỡ các vùng hiển thị này bằng cách thiết lập giá trị phù hợp cho các thuộc tính định dạng CSS. Bảng 1 liệt kê một số thuộc tính định dạng CSS cho các vùng hiển thị này.

Ví dụ 1. Trong văn bản HTML có khai báo thuộc tính định dạng kích thước vùng lề của phần tử p, kết quả hiển thị trên màn hình trình duyệt web như sau:

Đoạn mã HTML này định nghĩa một kiểu CSS để đặt lề (margin) 50 pixel cho các phần tử đoạn văn bản (`<p>`).
Kết quả hiển thị trên trình duyệt web cho thấy một đoạn văn bản được căn lề 50 pixel từ các cạnh.

Ví dụ 2. Trong văn bản HTML có khai báo thuộc tính định dạng kích thước vùng đệm và đường viền của phần tử p, kết quả hiển thị trên màn hình trình duyệt web như sau:

Đoạn mã HTML này định nghĩa một lớp CSS `custom-border` để đặt vùng đệm (padding) 30 pixel và đường viền kiểu liền nét (solid) cho phần tử đoạn văn bản (`<p>`).
Kết quả hiển thị trên trình duyệt web cho thấy một đoạn văn bản nằm trong một hộp có vùng đệm và đường viền.

## 2 Hiển thị phần tử theo khối, theo dòng

Theo em, trên một dòng của màn hình trình duyệt web có thể hiển thị nhiều phần tử HTML được không?

Theo mặc định, mỗi phần tử HTML sẽ được xác định kiểu hiển thị theo khối hoặc theo dòng. Với cách hiển thị theo khối, mỗi phần tử được hiển thị trên một dòng mới. Ngược lại, với cách hiển thị theo dòng, nhiều phần tử có thể được hiển thị trên cùng một dòng. Ví dụ: phần tử **h1**, **p** hiển thị theo khối; phần tử **img**, **a** hiển thị theo dòng.
CSS cho phép thay đổi kiểu hiển thị mặc định của các phần tử HTML trên trang web thông qua thuộc tính **CSS display**.

Thiết lập kiểu hiển thị của phần tử theo khối được khai báo như sau:
{display: block;}

Thiết lập kiểu hiển thị của phần tử theo dòng được khai báo như sau:
{display: inline;}

Ví dụ 3. Trong văn bản HTML ở Hình 4a, dòng 6 khai báo định dạng hiển thị theo khối, dòng 7 khai báo định dạng hiển thị theo dòng và kết quả hiển thị trên màn hình trình duyệt web như ở Hình 4b.

Đoạn mã HTML minh họa cách khai báo và sử dụng các lớp CSS `.bl` và `.il` để thiết lập kiểu hiển thị **`display: block;`** và **`display: inline;`**. Phần thân HTML chứa các cặp thẻ `<img>` và `<p>` được gán các lớp này.

Kết quả hiển thị trên trình duyệt web cho thấy:
*   Phần tử được gán lớp `.bl` (hiển thị theo khối) chiếm toàn bộ chiều rộng có thể, và mỗi phần tử này sẽ bắt đầu trên một dòng mới.
    *   Hiển thị theo khối: Mang tri thức vào cuộc sống
*   Phần tử được gán lớp `.il` (hiển thị theo dòng) chỉ chiếm không gian cần thiết cho nội dung của nó và có thể nằm trên cùng một dòng với các phần tử khác.
    *   Hiển thị theo dòng: Mang tri thức vào cuộc sống

### Bố cục trang web

**Bố cục trang web** là cách sắp xếp, bố trí các đối tượng nội dung trên trang web vào các khu vực hiển thị khác nhau để tạo nên một giao diện web. Tuỳ thuộc vào mục đích chuyển tải thông tin, trang web có các bố cục khác nhau. Mỗi trang web như minh hoạ ở Hình 5 thường gồm một số thành phần cơ bản sau đây:

*   ① Phần đầu trang (header): cung cấp thông tin như logo, tiêu đề trang web.

* Thanh điều hướng (navigation menu): là tập hợp các siêu liên kết đến các trang web khác trong website.
* Phần nội dung (content): cung cấp thông tin chính của trang web.
* Phần chân trang (footer): cung cấp các thông tin bổ trợ như bản quyền, các liên kết nhanh.

Một cách phổ biến để phân chia trang web thành các vùng là sử dụng phần tử **div** kết hợp với các định dạng CSS như bộ chọn lớp, bộ chọn định danh. Mỗi vùng thường trình bày một thành phần chính của trang web. Nội dung của mỗi vùng được khai báo trong cặp thẻ `<div> </div>`.

Ví dụ 4. Văn bản HTML ở Hình 6a sử dụng phần tử div, kết hợp với định dạng CSS để tạo ra bốn vùng khác nhau, kết quả bố cục trang web sẽ như ở Hình 6b.

Đoạn mã HTML này định nghĩa một cấu trúc trang web cơ bản. Trong phần `<head>`, nó có một tiêu đề, meta charset và một khối `<style>` chứa các quy tắc CSS để định dạng các vùng của trang. Các quy tắc CSS này thiết lập padding, kiểu đường viền, màu nền và chiều cao cho các lớp `.region`, `.header`, `.navigation_menu`, `.content`, và `.footer`. Trong phần `<body>`, các thẻ `<div>` được sử dụng để tạo ra bốn vùng: "Phần đầu trang" (header), "Thanh điều hướng" (navigation menu), "Phần nội dung" (content) và "Phần chân trang" (footer), mỗi vùng được gán một lớp CSS tương ứng.

## Luyện tập

Em hãy khai báo thêm các quy tắc định dạng cho trang web “**Bai10-NV1.html**” để: nội dung phần tử **body** có khoảng cách lề 30 **pixel**; phần tử **h3** có đường viền tô liền nét (**solid**), khoảng cách vùng đệm là 20 **pixel**.

Em hãy sử dụng phần tử **div** kết hợp với định dạng **CSS** để tách trang web *Bai10-NV1.html* thành hai phần: phần đầu trang và phần nội dung. Phần đầu trang là tiêu đề “Đóng góp ý kiến cho thư viện của nhà trường”, phần nội dung là các thông tin còn lại. Tạo màu nền khác nhau cho hai phần này.

**Câu 1**. Cho khai báo định dạng sau: **p{height: 50 px; padding:5px; border:2px solid; margin: 4px;}**. Khi đó chiều cao của phần tử **p** tính theo **pixel** là bao nhiêu?
A. 60px
B. 72px
C. 54px
D. 64px

**Câu 2**. Cần thiết lập hiển thị theo dòng hoặc theo khối để tạo trang web như ở một biểu mẫu nhập liệu cơ bản với các trường "Họ tên", "Địa chỉ", và hai nút "Đồng ý", "Hủy bỏ". Mỗi phát biểu dưới đây là đúng hay sai?
a) Theo mặc định, các phần tử **input** được hiển thị theo khối nên khi khai báo các phần tử **input** trong văn bản **HTML** không cần xác định thuộc tính **display** mà các điều khiển trên biểu mẫu vẫn hiển thị đúng như yêu cầu.
b) Để hiển thị như yêu cầu cần định dạng các **label** được hiển thị theo khối bằng khai báo định dạng **label {display: block;}**. Phần **body** của văn bản **HTML** khai báo như sau:
Mô tả: Đoạn mã HTML khai báo một biểu mẫu (`<form>`) trong phần thân (`<body>`) của trang. Biểu mẫu này chứa hai nhãn (`<label>`) cho "Họ tên" và "Địa chỉ", mỗi nhãn kèm theo một trường nhập liệu văn bản (`<input type="text">`).

c) Để hiển thị như yêu cầu cần định dạng các label được hiển thị theo khối bằng khai báo label {display: block;}. Phần body của văn bản HTML khai báo như sau:
Mã HTML này tạo một biểu mẫu với hai trường nhập liệu "Họ tên" và "Địa chỉ", cùng với hai nút "Đồng ý" và "Huỷ bỏ". Các nhãn (`label`) và trường nhập liệu (`input`) được hiển thị trên các dòng riêng biệt.

d) Theo mặc định, các phần tử input được hiển thị theo dòng nên cần khai báo định dạng hiển thị theo khối cho hai ô text nhập dữ liệu .bl {display: block;}. Phần body của văn bản HTML khai báo như sau:
Mã HTML này tạo một biểu mẫu, trong đó mỗi nhãn (`label`) bao gồm cả văn bản nhãn và trường nhập liệu (`input`). Các trường nhập liệu có lớp CSS "bl" để được hiển thị theo kiểu khối, đảm bảo chúng xuất hiện trên các dòng riêng biệt. Biểu mẫu cũng có hai nút "Đồng ý" và "Huỷ bỏ".

## Tóm tắt bài học

*   CSS trình bày các phần tử HTML trên trình duyệt web theo mô hình hộp. CSS định nghĩa một số thuộc tính định dạng để tuỳ chỉnh vùng lề, đường viền, vùng đệm, vùng nội dung của mô hình hộp.
*   Định dạng CSS cho phép hiển thị phần tử theo khối hoặc theo dòng thông qua thuộc tính **display**.
*   Thông thường, bố cục của một trang web gồm: phần đầu trang, thanh điều hướng, phần nội dung, phần chân trang.
