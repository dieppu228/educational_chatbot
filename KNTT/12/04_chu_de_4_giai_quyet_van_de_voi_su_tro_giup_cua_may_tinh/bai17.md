# Bài 17: CÁC MỨC ƯU TIÊN CỦA BỘ CHỌN

SAU BÀI HỌC NÀY EM SẼ:
*   Biết cách dùng CSS cho các kiểu bộ chọn khác nhau (id, class, pseudo-class, pseudo-element).
*   Biết cách sử dụng CSS thực hiện các mẫu định dạng theo thứ tự ưu tiên của mình.

Chúng ta đã biết nhiều cách thiết lập mẫu định dạng cho các phần tử HTML. Tuy nhiên, các lệnh định dạng CSS đã biết đều chỉ áp dụng cho các phần tử tĩnh, tức là không phụ thuộc vào tương tác với người dùng. Vậy có cách nào thiết lập CSS để định dạng cho các trạng thái tương tác với người dùng, ví dụ như trạng thái khi người dùng di chuyển hay nháy chuột lên phần tử đó không?

## 1. KIỂU BỘ CHỌN DẠNG PSEUDO-CLASS VÀ PSEUDO-ELEMENT

### Hoạt động 1: Tìm hiểu một số kiểu lớp và bộ chọn pseudo-class, pseudo-element

Thảo luận và trả lời các câu hỏi sau:
1.  Thể nào là **pseudo-class** của bộ chọn? Cách áp dụng.
2.  Thể nào là **pseudo-element** của bộ chọn? Nêu ý nghĩa của khái niệm này trong định dạng CSS.

### a) Bộ chọn pseudo-class

**Pseudo-class** (lớp giả) là khái niệm chỉ các trạng thái đặc biệt của phần tử HTML. Các trạng thái này không cần định nghĩa và mặc định được coi như các lớp có sẵn của CSS. Trong CSS, các lớp giả quy định viết sau dấu ":" theo cú pháp:

`:pseudo-class {thuộc tính : giá trị ;}`

Dưới đây là một số lớp giả thường dùng:

*   **Bộ chọn**: `:link`
    *   **Ý nghĩa**: Tất cả các liên kết khi chưa được kích hoạt.
    *   **Ví dụ**: Các liên kết (khi chưa kích hoạt) sẽ có màu xanh dương.
        Đoạn mã CSS này thiết lập màu xanh dương cho tất cả các liên kết chưa được kích hoạt.
*   **Bộ chọn**: `:visited`
    *   **Ý nghĩa**: Tất cả các liên kết sau khi đã được kích hoạt một lần.
    *   **Ví dụ**: Các liên kết sau khi kích hoạt chuyển màu xám.
        Đoạn mã CSS này thiết lập màu xám cho tất cả các liên kết đã được kích hoạt một lần.
*   **Bộ chọn**: `:hover`
    *   **Ý nghĩa**: Tất cả các phần tử, khi người dùng di chuyển con trỏ chuột lên đối tượng.
    *   **Ví dụ**: Khi di chuyển con trỏ chuột lên đối tượng có id = "home" sẽ hiển thị với cỡ chữ tăng lên 150%.
        Đoạn mã CSS này làm tăng kích thước phông chữ lên 150% cho đối tượng có id là 'home' khi con trỏ chuột di chuyển lên nó.

Ví dụ trong Hình 17.1 mô tả CSS thiết lập định dạng cho các trạng thái đặc biệt của phần tử a chứa liên kết. Các trạng thái này gọi là **"lớp giả"**. Liên kết "Tự học nhanh CSS" sẽ được thiết lập màu đỏ mặc định. Nếu đã được kích hoạt, liên kết sẽ tự động chuyển màu xanh lá cây. Khi di chuyển con trỏ chuột lên liên kết thì dòng chữ liên kết đổi màu hồng.

Đoạn mã HTML/CSS này định nghĩa các kiểu cho một liên kết và một tiêu đề. Cụ thể, nó thiết lập màu đỏ cho liên kết chưa được truy cập, màu xanh lá cây cho liên kết đã truy cập và màu hồng khi di chuột qua liên kết. Tiêu đề `h1` được đặt màu xanh dương.

CSS là gì
CSS (Cascading Style Sheets) là ngôn ngữ dùng để mô tả cách thiết lập định dạng đặc biệt được dùng để mô tả cách thể hiện của văn bản HTML trong trang web.

Kết quả hiển thị trên trình duyệt cho thấy một tiêu đề "CSS là gì" và một liên kết "Tự học nhanh CSS".

### b) Bộ chọn kiểu pseudo-element

**Pseudo-element** (phần tử giả) là khái niệm chỉ một phần (hoặc một thành phần) của các phần tử bình thường. Các phần này có thể coi là một phần tử giả và có thể thiết lập mẫu định dạng CSS. Quy định phần tử giả viết sau dấu "::" theo cú pháp:
`::pseudo-element {thuộc tính : giá trị ;}`

*   Bộ chọn `::first-line`: Dòng đầu tiên của đối tượng.
    *   Ví dụ: Dòng đầu tiên của các đoạn thuộc lớp test chuyển phông monospace. `p.test::first-line {font-family: monospace;}`
*   Bộ chọn `::first-letter`: Kí tự đầu tiên của đối tượng.
    *   Ví dụ: Kí tự đầu tiên của đoạn có id = "first" có màu đỏ và kích thước gấp đôi bình thường. `p#first::first-letter {font-size: 200%;}`
*   Bộ chọn `::selection`: Phần được chọn (bằng cách kéo thả chuột trên màn hình) của đối tượng.
    *   Ví dụ: Vùng đang chọn bất kì sẽ chuyển màu nền xanh lá mạ. `::selection {background-color: lime;}`

Ví dụ trong Hình 17.2 mô tả CSS thiết lập định dạng cho một phần hoặc một thành phần của phần tử p (được gọi là phần tử giả). CSS sẽ tự động tạo khuôn cho dòng đầu tiên của tất cả các phần tử p của trang web với màu đỏ, phông chữ có độ rộng đều nhau và có kích thước lớn hơn 1,2 lần so với bình thường. Chú ý dòng đầu tiên này không phụ thuộc vào văn bản mà chỉ phụ thuộc vào độ rộng của cửa sổ trình duyệt.

Đoạn mã HTML này định nghĩa một trang web cơ bản với một khối kiểu dáng (style) và phần nội dung (body).
Trong khối kiểu dáng, CSS được sử dụng để định dạng dòng đầu tiên của các đoạn văn bản (paragraph `p`) với màu đỏ, font monospace và kích thước 120%.
Phần nội dung chứa hai đoạn văn bản mô tả về HTML và CSS.

**Kết quả hiển thị trên trình duyệt:**
Dòng đầu tiên của mỗi đoạn văn bản sẽ được hiển thị với màu đỏ, font monospace và kích thước 120%.

**HTML** là ngôn ngữ đánh dấu siêu văn bản, là ngôn ngữ đặc biệt dùng để thiết kế nội dung các trang web và được thể hiện bằng trình duyệt.
**CSS** là ngôn ngữ định dạng đặc biệt được dùng để mô tả cách thể hiện của văn bản HTML trong trang web.

CSS hỗ trợ thiết lập định dạng cho các **lớp giả (pseudo-class)** và **phần tử giả (pseudo-element)**. Lớp giả mô tả các trạng thái được định nghĩa trước của phần tử. Phần tử giả mô tả các thành phần (nhỏ hơn) của phần tử.

## Luyện tập
1.  Muốn áp dụng đổi màu chữ một vùng trên màn hình khi nháy chuột tại vùng đó thì cần phải dùng định dạng CSS nào?
2.  Muốn tăng kích thước một đoạn văn bản khi di chuyển chuột qua đoạn văn bản đó thì cần dùng định dạng CSS nào?

## 2. MỨC ĐỘ ƯU TIÊN KHI ÁP DỤNG CSS

**Hoạt động 2 Tìm hiểu ý nghĩa và ứng dụng của mức độ ưu tiên trong CSS**

Giả sử có định dạng CSS như sau:
Đoạn mã CSS này định nghĩa hai quy tắc: một quy tắc cho các phần tử có lớp `.test` sẽ có màu xanh lá cây, và một quy tắc cho tất cả các đoạn văn bản `p` sẽ có màu đỏ.

CSS trên áp dụng cho phần tử HTML sau:
Đoạn mã HTML này là một đoạn văn bản `<p>` có thuộc tính `class` là "test" với nội dung "Tin học 12".

Khi đó cụm từ “Tin học 12” sẽ có màu gì?

Khi có nhiều mẫu định dạng có thể áp dụng cho một phần tử HTML nào đó trên trang web, CSS sẽ áp dụng định dạng theo thứ tự ưu tiên. Trong các bài học trước, em đã biết hai quy tắc ưu tiên là **tính kế thừa** và quy định về **thứ tự cuối cùng (cascading)**. Trên thực tế quy định về chọn mẫu định dạng ưu tiên từ cao xuống thấp của CSS được mô tả trong Bảng 17.3.

Bảng 17.3. Thứ tự (mức) ưu tiên của CSS

*   **!important**: Các thuộc tính trong CSS với từ khoá **!important** sẽ có mức ưu tiên cao nhất.
*   **CSS trực tiếp (inline CSS)**: Các định dạng nằm ngay trong phần tử HTML với thuộc tính **style**.
*   **CSS liên quan đến kích thước thiết bị (Media type)**: Các định dạng loại này thường dùng để điều khiển cách hiển thị thông tin phụ thuộc vào kích thước màn hình của thiết bị. Ví dụ mẫu định dạng sau sẽ tăng kích thước chữ lên 150% nếu chiều ngang màn hình nhỏ hơn 600 px. (Đoạn mã CSS này tăng kích thước chữ lên 150% cho phần tử `body` khi màn hình có chiều rộng tối đa là 600px.)
*   **Trọng số CSS**: Mỗi định dạng CSS sẽ có trọng số (**specificity**) riêng của mình. Tại mức ưu tiên này, định dạng CSS có trọng số cao nhất sẽ được áp dụng.
*   **Nguyên tắc thứ tự cuối cùng (Rule order)**: Nếu có nhiều mẫu định dạng với cùng trọng số thì định dạng ở vị trí cuối cùng sẽ được áp dụng.
*   **Kế thừa từ CSS cha**: Nếu không tìm thấy mẫu định dạng tương ứng thì sẽ lấy thông số định dạng CSS kế thừa từ phần tử cha.
*   **Mặc định theo trình duyệt**: Nếu không có bất cứ định dạng CSS nào thì trình duyệt quyết định thể hiện nội dung mặc định.

Như vậy theo nguyên tắc trên, nếu có một dãy các mẫu định dạng CSS cùng có thể áp dụng cho một phần tử HTML thì tính kế thừa CSS và nguyên tắc thứ tự cuối cùng được xếp dưới trọng số CSS, tức là khi đó CSS sẽ tính trọng số các mẫu định dạng, cái nào có trọng số lớn hơn sẽ được ưu tiên áp dụng.

Cách tính trọng số của CSS rất đơn giản dựa trên giá trị trọng số của từng thành phần của bộ chọn (**selector**) trong mẫu định dạng. Trọng số của mẫu định dạng sẽ được tính bằng tổng của các giá trị thành phần đó. Giá trị của các thành phần của bộ chọn theo quy định trong Bảng 17.4.

Bảng 17.4. Giá trị của các thành phần của bộ chọn

*   **Mã định danh (ID)**: Giá trị đóng góp trọng số: 100
*   **Lớp, lớp giả, bộ chọn kiểu thuộc tính (Class, pseudo-class, attribute selector)**: Giá trị đóng góp trọng số: 10
*   **Phần tử, phần tử giả (element, pseudo-element)**: Giá trị đóng góp trọng số: 1
*   **\***: Giá trị đóng góp trọng số: 0

Bảng 17.5. Một số ví dụ tính trọng số

*   **Bộ chọn: p > em**. Trọng số: 2. Giải thích: Bộ chọn có hai phần tử là **p** và **em**, vậy trọng số bằng 1 + 1 = 2.
*   **Bộ chọn: .test #p11**. Trọng số: 110. Giải thích: Bộ chọn bao gồm 1 **class** và 1 **id**, vậy trọng số bằng 10 + 100 = 110.
*   **Bộ chọn: p.test em.more**. Trọng số: 22. Giải thích: Bộ chọn có hai phần tử (**p, em**) và hai **class (test, more)**, vậy trọng số bằng 2 + 20 = 22.
*   **Bộ chọn: p > em#p123**. Trọng số: 102. Giải thích: Bộ chọn có hai phần tử (**p, em**) và một **id**, vậy trọng số bằng 2 + 100 = 102.

Trở lại với ví dụ của Hoạt động 2, cụm từ "Tin học 12" là nội dung của phần tử p. Có hai định dạng CSS có thể áp dụng cho phần tử: Định dạng phía trên có trọng số 10 (vì là pseudo-class), định dạng phía dưới có trọng số 1 (vì là element). Do đó định dạng phía trên sẽ được áp dụng và cụm từ đó sẽ có màu xanh lá cây.

Nếu có nhiều mẫu định dạng CSS cùng mức ưu tiên áp dụng cho một phần tử HTML thì mẫu CSS nào có trọng số cao nhất sẽ được áp dụng.

## Luyện tập
1.  Tính trọng số của các mẫu định dạng sau:
    a) `#n12 > .test.`
    b) `h1, h2, h3, h4 > #new.`
    c) `p + em.test.`
2.  Khi nào nguyên tắc cascading (thứ tự cuối cùng) được áp dụng cho một dãy các định dạng CSS?

## 3. THỰC HÀNH

### Nhiệm vụ 1: Nhập tệp html

**Yêu cầu**: Nhập tệp html với nội dung như sau:

Giới thiệu HTML và CSS
Giới thiệu HTML
Giới thiệu CSS
HTML là gì
HTML - tên viết tắt của HyperText Markup Language, ngôn ngữ đánh dấu siêu văn bản, là ngôn ngữ đặc biệt dùng để thiết kế nội dung các trang web và được thể hiện bằng trình duyệt.
Cấu trúc mỗi tệp HTML là một cấu trúc dạng cây của các phần tử HTML.
Xem logo của HTML.

Link xem thêm chi tiết về HTML tại đây (https://en.wikipedia.org/wiki/HTML).
Link xem và tự học HTML tại đây (https://www.w3schools.com/html/default.asp).
CSS là gì
CSS (Cascading Style Sheets) là ngôn ngữ định dạng đặc biệt được dùng để mô tả cách thể hiện của văn bản HTML trong trang web.
Mỗi định dạng CSS đều có dạng chuẩn là bộ chọn {thuộc tính : giá trị; }.
Xem logo của CSS.

Link xem thêm chi tiết về CSS tại đây (https://en.wikipedia.org/wiki/CSS).
Link xem và tự học CSS tại đây (https://www.w3schools.com/css/default.asp).

### Nhiệm vụ 2: Thiết lập định dạng bằng CSS

**Yêu cầu**: Thiết lập định dạng cho tệp html ở Nhiệm vụ 1 bằng CSS theo các yêu cầu sau:
*   Tiêu đề chính của bài màu đỏ, căn giữa.
*   Các tiêu đề nhỏ màu xanh, đậm.
*   Phần kết nối liên kết phía trên định dạng trên một hàng ngang, căn phải, các liên kết có màu nền xanh lá cây. Khi di chuột lên thì chuyển chữ màu đỏ.
*   Các đoạn đầu tiên bên dưới các tiêu đề có màu đỏ, các đoạn khác vẫn màu mặc định.
*   Các hình ảnh logo ban đầu ẩn đi. Khi nháy chuột lên dòng "Xem logo của HTML." và "Xem logo của CSS." thì các hình ảnh tương ứng được hiện ra.

Hình ảnh trang web sau khi định dạng cần được thể hiện như Hình 17.3.

# Giới thiệu HTML và CSS

## HTML là gì

**HTML** (tên viết tắt của HyperText Markup Language, ngôn ngữ đánh dấu siêu văn bản), là ngôn ngữ đặc biệt dùng để thiết kế nội dung các trang web và được thể hiện bằng trình duyệt.

HTML do nhà khoa học Tim Berners-Lee thiết lập vào những năm 1990 của thế kỉ trước. HTML được thiết lập gắn liền một số công nghệ khác như CSS (mẫu định dạng CSS) và ngôn ngữ lập trình Javascript.

## Hướng dẫn:

*   Phần liên kết đầu trang có thể thiết lập bằng các thẻ `<nav>` và `<ul></ul><li></li>` như sau:
    *Đoạn mã HTML này tạo một thanh điều hướng (`<nav>`) chứa một danh sách không thứ tự (`<ul>`) với hai mục danh sách (`<li>`). Mỗi mục là một liên kết (`<a>`) đến các phần khác nhau của trang (ví dụ: "#P1" và "#P2") với văn bản hiển thị là "Giới thiệu HTML" và "Giới thiệu CSS".*

*   CSS được thiết lập như sau:
    *Đoạn mã CSS này định dạng các phần tử trên trang web. Nó căn giữa và đặt màu đỏ cho tiêu đề `h1`, đặt màu xanh dương cho `h2`. Thanh điều hướng (`nav`) được căn phải. Các mục danh sách (`li`) được hiển thị cùng dòng, có viền xanh dương, đệm 5px và nền màu xanh lá cây chanh. Khi di chuột qua liên kết (`a:hover`), văn bản sẽ có màu đỏ và nền màu xanh lơ. Đoạn mã cũng đặt màu đỏ cho đoạn văn bản (`p`) ngay sau một tiêu đề `h2`. Cuối cùng, nó ẩn các phần tử `img` và hiển thị phần tử `img` khi có lớp `.img` đang hoạt động (`.img:active + img`).*

## Luyện tập

1.  Giải thích sự khác nhau giữa hai định dạng sau:
    `#p123 + p {color : red ;}`
    `h2#p123 + p {color : red ;}`
2.  Trong phần Thực hành, các tên riêng (tên người, tên tổ chức) cần được bổ sung định dạng đóng khung và in nghiêng. Em sẽ thực hiện các yêu cầu này như thế nào?

## Vận dụng

1.  Tìm hiểu thêm các dạng **pseudo-class** khác, nêu ý nghĩa và tìm ví dụ ứng dụng thực tế cho các kiểu bộ chọn này.
2.  Tìm hiểu thêm các dạng **pseudo-element** khác, nêu ý nghĩa và tìm ví dụ ứng dụng thực tế cho các kiểu bộ chọn này.
