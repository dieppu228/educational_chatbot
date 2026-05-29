# Bài 7: HTML VÀ CẤU TRÚC TRANG WEB

## SAU BÀI HỌC NÀY EM SẼ:
*   Hiểu và giải thích được cấu trúc của một trang web dưới dạng HTML.
*   Các em đã được làm quen với khái niệm website và trang web, cũng có thể em đã biết cách sử dụng phần mềm để tạo ra các trang web với nội dung đa dạng và phong phú, hình thức trình bày đẹp.
    Tuy nhiên, có thể các em vẫn muốn biết:
*   Các trang web thực chất có cấu trúc như thế nào?
*   Có thể “lập trình” để tạo ra được các trang web hay không? Nếu lập trình được thì “mã nguồn” của trang web là gì?
*   Các trang web có quan hệ như thế nào với ngôn ngữ HTML?
*   Trang web và trình duyệt web có quan hệ hệ như thế nào?
    Em hãy tìm câu trả lời.

## 1. TRANG WEB VÀ HTML
### Hoạt động 1: Tìm hiểu ngôn ngữ HTML và trang web

Các trang web mà em vẫn thường xem được hiển thị bởi trình duyệt web (ví dụ: Cốc cốc, FireFox, Chrome). Thực chất chúng được tạo ra từ các tệp văn bản. Các tệp văn bản này được gọi là trang nguồn (hay mã nguồn) của trang web tương ứng. Quan sát và nhận xét về mã nguồn. Em thấy gì từ tệp nguồn của trang web?

a) Trang web hiển thị bởi trình duyệt
Trang web và html
Đây là dòng đầu tiên
Đây là dòng cuối cùng

b) Tệp văn bản nguồn
(Mô tả: Đoạn mã HTML cơ bản bao gồm các thẻ `<html>`, `<head>`, `<body>`. Phần `<head>` chứa thẻ `<title>` với nội dung "Tên trang Web". Phần `<body>` chứa thẻ `<h1>` với nội dung "Trang Web và HTML", hai thẻ `<p>` hiển thị "Đây là dòng đầu tiên" và "Đây là dòng cuối cùng", cùng với thẻ `<hr>` tạo đường kẻ ngang.)

**HTML** là viết tắt của cụm từ Hypertext Markup Language (ngôn ngữ đánh dấu siêu văn bản), là một bộ quy tắc dùng để thiết lập cấu trúc và hiển thị nội dung trang web.

Trang web được thiết lập từ các tệp văn bản thường có phần mở rộng là **.html** hoặc **.htm** được gọi là trang html. Trên trang html, ta có thể thấy nội dung bao gồm phần văn bản (text) và các kí tự đánh dấu đặc biệt nằm trong hai dấu "<", ">". Các kí tự này, được gọi là **thẻ đánh dấu HTML** (còn gọi là thẻ HTML hay tag). Trong ví dụ ở Hình 7.1b chúng ta thấy các thẻ HTML như `<head>`, `<title>`, `<body>`, `<h1>`, `<p>`, `<div>`,...

Các thẻ HTML được sử dụng để xác định phần tử HTML tương ứng. Các phần tử HTML định dạng thông tin trong trang web. Để hiển thị thông tin trong trang web, cần phần mềm trình duyệt web.

### a) Thẻ đánh dấu HTML

Thẻ đánh dấu HTML (**tag**) là các thành phần chính tạo thành ngôn ngữ đánh dấu siêu văn bản. Mỗi loại thẻ có một tên riêng và có ý nghĩa nhất định trong định dạng nội dung của trang web. Các thẻ được viết trong cặp dấu "<", ">". Thông thường mỗi thẻ sẽ bao gồm thẻ bắt đầu và thẻ kết thúc, chỉ ra phạm vi tác dụng của thẻ.

Dưới đây là thông tin về một số thẻ HTML cơ bản, ý nghĩa, mã và cách hiển thị của chúng trên trình duyệt:

*   Thẻ **p**:
    *   Ý nghĩa: Đoạn văn bản
    *   Mã HTML: `<p>Đây là đoạn văn bản.</p>`
    *   Hiển thị trên trình duyệt: Đây là đoạn văn bản.
*   Thẻ **h1**:
    *   Ý nghĩa: Tiêu đề 1 của văn bản
    *   Mã HTML: `<h1>Đây là tiêu đề 1</h1>`
    *   Hiển thị trên trình duyệt: Đây là tiêu đề 1.

Lưu ý:
*   Tên thẻ HTML không phân biệt chữ hoa, chữ thường nhưng mặc định tên thẻ được viết chữ thường.
*   Các thẻ có thể lồng nhau. Ví dụ sau là thẻ `<em>` được lồng bên trong thẻ `<p>`:
    *   Mã HTML: `<p> Trang này được lập bởi <em>nhóm bạn bè</em> thân thiết </p>`
    *   Chức năng: Đoạn mã này cho thấy thẻ `<em>` (dùng để in nghiêng) được đặt bên trong thẻ `<p>` (đoạn văn bản), làm cho phần "nhóm bạn bè" in nghiêng.
*   Mỗi thẻ có thể đi kèm các thông tin thuộc tính của thẻ. Ví dụ sau mô tả thuộc tính màu được gán thêm cho thẻ `<p>`, do đó toàn bộ đoạn văn bản này có màu đỏ khi hiển thị trên trình duyệt.
    *   Mã HTML: `<p style="color: red">This is a paragraph.</p>`
    *   Chức năng: Đoạn mã này sử dụng thuộc tính `style` để đặt màu chữ của văn bản trong thẻ `<p>` thành màu đỏ.
*   Phần lớn các thẻ đều là thẻ đôi, tức là có thẻ bắt đầu (opening tag) và thẻ kết thúc (closing tag). Vị trí kết thúc thẻ có thêm dấu "/" chẳng hạn `</p>`.
*   Tuy nhiên có một số loại thẻ đơn, tức là chỉ có thẻ bắt đầu. Các thẻ đơn thường có dạng `<tên thẻ>` hoặc `<tên thẻ/>`, ví dụ `<hr/>` (dòng kẻ ngang), `<br/>` (ngắt xuống dòng),...
*   HTML và trình duyệt không nhận biết được nhiều dấu cách. Nếu gõ nhiều dấu cách máy sẽ hiểu là chỉ có một dấu cách. Trình duyệt cũng không nhận biết dấu xuống dòng khi người dùng nhấn phím Enter trong quá trình soạn thảo. Cần chú ý điều này khi soạn thảo HTML.

### b) Phần tử HTML

**Phần tử HTML** (**element**) là khái niệm cơ bản của trang html. Thông thường, một phần tử được định nghĩa bởi thẻ bắt đầu, thẻ kết thúc và phần nội dung nằm giữa cặp thẻ này.

Lưu ý: Các thẻ đơn cùng với nội dung của nó cũng được gọi là phần tử HTML.

Vậy phần tử HTML có thể hiểu là toàn bộ phần thể và nội dung của thẻ. Mỗi tệp HTML là tập hợp các **phần tử HTML**. Các phần tử HTML đóng vai trò quan trọng tạo nên cấu trúc và nội dung của trang web. Các phần tử HTML có thể độc lập, rời nhau hoặc lồng nhau.

Trong ví dụ ở Hình 7.1, em thấy hai phần tử HTML rời nhau là `<head>` và `<body>`, trong khi đó phần tử `<div>` chứa bên trong bốn phần tử HTML khác.

### Lưu ý

*   Dòng đầu tiên của mỗi tệp HTML có dạng `<!DOCTYPE html>` có vai trò thông báo kiểu của tệp là html và không được xem là phần tử HTML.
*   Phần tử HTML đặc biệt có ý nghĩa chú thích trong tệp HTML có dạng: `<!-- đây là dòng chú thích -->` (cách ghi chú thích trong HTML).

Trang web được thiết lập theo một ngôn ngữ có cấu trúc đặc biệt gọi là **ngôn ngữ đánh dấu siêu văn bản HTML**. Các tệp HTML là tệp văn bản được cấu tạo từ các **phần tử HTML** gồm nội dung được đánh dấu bởi các **thẻ** (HTML tag) có tính năng điều khiển hoặc định dạng nội dung. Trình duyệt có chức năng hiển thị nội dung trang web theo đúng định dạng được thiết lập.

1.  Tệp văn bản trong Hình 7.1 có bao nhiêu phần tử HTML?
2.  Nêu sự giống và khác nhau giữa thẻ HTML và phần tử HTML.

## CẤU TRÚC CƠ BẢN CỦA MỘT TỆP HTML

### Hoạt động 2: Tìm hiểu cấu trúc cơ bản của một tệp HTML

Quan sát tệp HTML sau, em có nhận xét gì về cấu trúc chung của một trang web? newpage.html

Đoạn mã HTML này thể hiện cấu trúc cơ bản của một trang web, bao gồm khai báo `<!DOCTYPE html>`, thẻ `<html>` chứa toàn bộ nội dung, thẻ `<head>` chứa thông tin về trang (như tiêu đề và charset), và thẻ `<body>` chứa nội dung hiển thị trên trình duyệt (như tiêu đề `<h1>`, đoạn văn ` <p>`, đường kẻ ngang `<hr>`, và nhóm các phần tử trong `<div>`).

Mỗi tệp HTML bao gồm nhiều phần tử HTML, các phần tử HTML có thể lồng nhau. Ví dụ trong Hình 7.2, phần tử với thẻ `<div>` chứa phần tử với thẻ `<h1>`. Quan hệ lồng nhau giữa các phần tử HTML có thể hình dung như quan hệ cha – con hay quan hệ giữa các nút của một sơ đồ hình cây.

Đoạn mã HTML cơ bản mô tả cấu trúc của một trang web đơn giản, bao gồm các phần tử như `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`, `<meta>`, `<title>`, `<h1>`, `<p>`, `<div>`, `<hr>`, và `<em>`, thể hiện cách các thẻ này được sắp xếp và lồng vào nhau.

### Cấu trúc cơ bản của một tệp HTML

1.  Dòng đầu tiên, `<!DOCTYPE html>`, không được coi là phần tử HTML và mang ý nghĩa đặc biệt, thông báo cho trình duyệt biết đây là tệp có định dạng html. Có thể coi là dòng khai báo html của tệp văn bản.
2.  Phần tử **<html>** là bắt buộc, là phần tử gốc và chứa tất cả các phần tử HTML còn lại của trang web. Trong sơ đồ hình cây HTML, đây là phần tử gốc (root). Phần tử `<html>` thường chứa hai phần tử con `<head>` và `<body>`.
3.  Phần tử **<head>** chứa các phần tử có liên quan chung đến toàn bộ trang web. Trong `<head>` thường có phần tử `<title>`. Một số phần tử khác thường có trong `<head>` bao gồm `<meta>`, `<style>` và `<script>`.
4.  Phần tử **<body>** chứa tất cả các phần tử còn lại là thông tin của trang web. Các phần tử này sẽ được tìm hiểu trong các bài học sau.
5.  Phần tử **<meta>** được dùng để mô tả các thông tin bổ sung của trang web như cách mã hoá Unicode, từ khoá dùng để tìm kiếm trang, tên tác giả trang web. Phần tử này nằm trong phần tử `<head>`. Trong Hình 7.3, phần tử `<meta charset = "utf-8">` mô tả cách mã hoá văn bản trên trang web theo mã UTF-8.
6.  Phần tử **<title>** nằm trong `<head>`. Thẻ `<title>` mô tả tên của trang web hiện thời. Tên của trang web sẽ xuất hiện trong danh sách kết quả tìm kiếm. Phần tử `<title>` phải là văn bản thường và không được phép chứa các phần tử con.
7.  Nhóm các thẻ định dạng văn bản thường dùng là các thẻ tiêu đề theo thứ tự giảm cấp dần là `<h1>`, `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>`. Thẻ `<p>` mô tả một đoạn văn bản hoàn chỉnh.

Lưu ý: Văn bản HTML không nhận biết kí tự xuống dòng (nhấn phím Enter) để kết thúc đoạn văn bản (paragraph) như các phần mềm soạn thảo văn bản thông thường.

Như vậy, cấu trúc chung của một trang web có thể hình dung như một cây thông tin các phần tử HTML có quan hệ cha con (lồng nhau), nút gốc (root) là phần tử `<html>`. Cấu trúc cây HTML này sẽ được giới thiệu trong các phần sau. Ví dụ, trang web ở Hình 7.2 có cây thông tin như Hình 7.4.

Cấu trúc cơ bản của tệp HTML có dạng như một cây thông tin các phần tử HTML. Quan hệ cha – con của các nút trên cây được mô tả bằng sự lồng nhau của các phần tử (hay thẻ) HTML. Gốc của cây HTML chính là phần tử `<html>`.

## Luyện tập

1.  Vẽ sơ đồ cây của đoạn văn bản HTML sau:
    `<p>Thông tin này in <b>đậm</b>, in <i>nghiêng</i> in <u>gạch dưới</u>, in bình thường.</p>`
2.  Cây HTML có bao nhiêu phần tử gốc?

# Bài 3: PHẦN MỀM SOẠN THẢO HTML

## Hoạt động 3: Tìm hiểu cách soạn thảo các tệp HTML
Hãy tìm hiểu những phần mềm có thể dùng để soạn thảo tệp HTML. Thảo luận để tìm ra cách soạn thảo tệp HTML hợp lí nhất.

Có nhiều cách để tạo tệp nguồn HTML. Ví dụ sử dụng các phần mềm soạn thảo như Notepad, Notepad++ hay Sublime Text. Ta cũng có thể soạn thảo trên các trang hỗ trợ tạo tệp HTML trực tuyến.

### a) Phần mềm Notepad

Đây là phần mềm soạn thảo văn bản đơn giản không định dạng, cung cấp một số chức năng chỉnh sửa cơ bản. Notepad có sẵn trên hệ điều hành Windows. Trên MacOS cũng có phần mềm tương tự Notepad là TextEdit.

### b) Phần mềm soạn thảo HTML chuyên nghiệp nguồn mở

*   Phần mềm Notepad++

Notepad++ là phần mềm soạn thảo chương trình đa năng, hỗ trợ soạn thảo chương trình với nhiều ngôn ngữ khác nhau, trong đó có ngôn ngữ HTML. Đây là phần mềm miễn phí, mã nguồn mở và có thể tải về từ địa chỉ https://notepad-plus-plus.org/.

*Mô tả mã nguồn:* Đoạn mã HTML trong phần mềm hiển thị cấu trúc cơ bản của một trang web với các thẻ như `<!DOCTYPE html>`, `<html>`, `<head>`, `<meta>`, `<title>`, `<body>`, `<h1>`, `<p>`, `<hr>` và `<em>`.

Lưu ý: Để phần mềm hiển thị và hỗ trợ soạn thảo đúng HTML cần thực hiện lệnh Language → H → HTML để chọn ngôn ngữ HTML.

*   Phần mềm Sublime Text

Sublime Text là phần mềm soạn thảo chương trình với nhiều ngôn ngữ khác nhau, tương tự như Notepad++. Phần mềm này có phiên bản cơ bản miễn phí. Địa chỉ tải phần mềm: https://www.sublimetext.com/.
Lưu ý: Để phần mềm hiển thị và hỗ trợ soạn thảo đúng theo ngôn ngữ HTML cần thực hiện lệnh View → Syntax → HTML để chọn ngôn ngữ HTML.

### c) Sử dụng trang web hỗ trợ soạn thảo HTML trực tuyến

Một cách phổ biến để soạn thảo HTML là sử dụng các trang hỗ trợ soạn thảo HTML trực tuyến. Để thực hiện theo cách này, yêu cầu máy tính có kết nối Internet và cài đặt trình duyệt chuẩn, ví dụ như Cốc Cốc, FireFox, Chrome hay Microsoft Edge.

Ví dụ là giao diện soạn thảo HTML trực tuyến. Khi đó có thể quan sát ngay kết quả hiển thị trang web trên trình duyệt. Việc soạn thảo HTML được thực hiện tại khung bên trái, nháy nút Run để kiểm tra kết quả tại khung bên phải.

Đoạn mã HTML hiển thị một tiêu đề lớn "Trang Web và HTML", hai đoạn văn bản ("Đây là dòng đầu tiên" và "Đây là dòng cuối cùng"), và một đoạn văn bản "Trang này được lập bởi nhóm bạn bè" với từ "nhóm bạn bè" được in nghiêng.

Kết quả hiển thị trên trình duyệt:
```
Trang web và html
Đây là dòng đầu tiên
Đây là dòng cuối cùng
Trang này được lập bởi nhóm bạn bè
```

Một số trang web hỗ trợ soạn thảo HTML trực tuyến là: w3schools.com, tutorialspoint.com,...

## Em cần chú ý
*   Có thể soạn thảo tệp HTML bằng nhiều phần mềm khác nhau. Cũng có thể soạn thảo trực tuyến và kiểm tra kết quả trực tiếp trên trình duyệt.

## Luyện tập

1.  Xếp các tên sau vào hai nhóm: phần mềm soạn thảo HTML và trình duyệt web:
    a) Notepad.
    b) Opera.
    c) Sublime Text.
    d) Chrome.
    e) Cốc Cốc.
    f) Notepad++.
    g) FireFox.
    h) Microsoft Edge.
2.  Em có nhận xét gì về sự khác biệt khi soạn thảo HTML giữa các phần mềm chuyên nghiệp (ví dụ Notepad++, Sublime Text) và phần mềm soạn thảo văn bản thông thường (ví dụ Notepad)?

1.  Tìm ví dụ về phần tử HTML không thể lồng, tức là không thể có quan hệ cha – con trong cây thông tin của trang web.
2.  Chọn một văn bản đơn giản. Soạn thảo tệp HTML để hiển thị nội dung văn bản đó. Vẽ cây thông tin các phần tử HTML của trang web vừa soạn thảo.

## Vận dụng

1.  Em hãy tìm trên mạng các trang web hỗ trợ soạn thảo HTML trực tuyến.
2.  Sử dụng phần mềm soạn thảo HTML và soạn thảo trang web có nội dung như Hình 7.7. Lưu ý rằng thẻ `<img>` với tính năng thể hiện ảnh trên trang web có cú pháp: `<img src="tên tệp ảnh">`, trong đó **"tên tệp ảnh"** chính là đường dẫn của tệp hình ảnh cần đưa lên trang.

## Lịch sử phát triển HTML

Các chuẩn HTML của trang web hiện nay được nhà vật lí Tim Berners-Lee đưa ra lần đầu tiên vào những năm 1990 của thế kỉ XX tại Trung tâm Vật lí Hạt nhân CERN.
Ý tưởng ban đầu của Berners-Lee là muốn thiết lập một chuẩn chung để thể hiện và chia sẻ các văn bản có thể trao đổi bên trong cơ quan CERN.
Hình ảnh sau là sơ đồ thông tin mà Tim Berners-Lee đưa ra lần đầu tiên để minh hoạ cho ý tưởng của mình. Trong sơ đồ này, lần đầu tiên xuất hiện cụm từ “hypertext” (siêu văn bản).

Phiên bản đầu tiên của HTML được thiết lập vào cuối năm 1991 mang tên “Các thẻ HTML”. Văn bản này do chính Tim Berners-Lee biên soạn.
Từ đó, các phiên bản tiếp theo của HTML lần lượt ra đời cùng với sự phát triển của công nghệ Internet.
Phiên bản hiện tại là HTML5 ra đời năm 2014.
