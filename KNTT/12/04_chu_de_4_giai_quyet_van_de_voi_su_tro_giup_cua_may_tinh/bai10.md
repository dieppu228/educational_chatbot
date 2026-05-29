# Bài 10: TẠO LIÊN KẾT

SAU BÀI HỌC NÀY EM SẼ:
*   Sử dụng thẻ HTML tạo được các loại liên kết.

Em hãy nêu những điểm khác biệt khi em đọc thông tin trên các trang web với việc em đọc sách, báo giấy. Theo em, điểm khác biệt nào là quan trọng nhất?

## 1. Siêu văn bản và đường dẫn

### Hoạt động 1: Nhận biết siêu văn bản
Các tệp có phần mở rộng .docx được tạo bởi Microsoft Word có thể là một siêu văn bản còn tệp có phần mở rộng .txt tạo bởi Notepad thì không. Theo em siêu văn bản có những đặc điểm gì?

**Siêu văn bản** (hypertext) là loại văn bản mà nội dung của nó không chỉ chứa văn bản mà còn có thể chứa nhiều dạng dữ liệu khác như âm thanh, hình ảnh,... và đặc biệt là chứa các **siêu liên kết** (hyperlink) tới siêu văn bản khác. Khi xem siêu văn bản, không cần xem tuần tự từ đầu đến cuối mà có thể nhờ các siêu liên kết để truy cập vị trí tương ứng không theo trình tự nào.

**Siêu liên kết** (còn gọi tắt là **liên kết**), là một tham chiếu để liên kết tới siêu văn bản khác. Người dùng có thể dễ dàng truy cập đến văn bản liên kết bằng cách nháy chuột vào vị trí đặt liên kết trong văn bản ban đầu.

Trong HTML, người ta sử dụng thẻ `<a>` cho các liên kết. Cấu trúc chung của thẻ `<a>` có dạng:
Mã HTML mô tả một siêu liên kết với thuộc tính `href` chỉ định địa chỉ (URL) của liên kết và phần `Nội dung hiển thị tại vị trí đặt liên kết` là văn bản hoặc hình ảnh mà người dùng sẽ nhấp vào để điều hướng.

Trong đó URL là địa chỉ (**đường dẫn**) tham chiếu tới tài liệu được liên kết. Thuộc tính **href** dùng để cung cấp địa chỉ của trang web hay tài nguyên được liên kết (URL) tới. Đường dẫn URL phải được nằm trong cặp dấu nháy kép "". Phần lớn các liên kết trỏ tới một tài liệu HTML khác, nhưng ta cũng có thể trỏ tới một hình ảnh, một tệp âm thanh hoặc video.

Có hai loại URL chính là đường dẫn tuyệt đối và đường dẫn tương đối.
*   **Đường dẫn tuyệt đối**: Cung cấp một địa chỉ đầy đủ bao gồm cả giao thức (http:// hoặc https://), tên miền (domain name) và tên đường dẫn chi tiết nếu cần. Khi sử dụng liên kết trên mạng Internet (mà tài liệu không nằm trên máy chủ của mình), ta cần phải sử dụng đường dẫn tuyệt đối. Ví dụ: href="https://www.nxbgd.vn/". Đôi khi đường dẫn tuyệt đối rất dài và khó nhìn, ta vẫn cần để một cách chính xác.

*   **Đường dẫn tương đối**: Mô tả cách truy cập tài liệu được liên kết từ vị trí của tài liệu hiện tại. Đường dẫn tương đối được sử dụng khi liên kết tới một tài liệu khác trên cùng trang web (cùng máy chủ hoặc máy tính cài đặt trang web), nó không yêu cầu giao thức hay tên miền, mà chỉ cần tên đường dẫn. Ví dụ: Với cấu trúc website như Hình 10.1, nếu ta đang ở trang index.html thì liên kết `href="BT/bai_tap_1.html"` là đường dẫn tương đối tới tệp tin bai_tap_1.html trong thư mục BT, thư mục BT nằm trong cùng thư mục cha với index.html.

**Siêu văn bản** là văn bản chứa nhiều loại dữ liệu và các liên kết tới siêu văn bản khác. Trong HTML, liên kết được xác định bằng thẻ `<a>` và thuộc tính `href` dùng để cung cấp đường dẫn (tuyệt đối hoặc tương đối) tới địa chỉ đích.

Trong các đường dẫn sau, đường dẫn nào là tuyệt đối, đường dẫn nào là tương đối?
a) `html/cach_tao_lien_ket.html`
b) `http://google.com`
c) `mail.google.com/mail/u/0/#inbox/FMfcgzGMpKDHQFWcdfXcmMtxvZ`

## 2. CÁC CÁCH LIÊN KẾT TỚI MỘT TRANG WEB

**Hoạt động 2** Tìm hiểu các cách liên kết tới một trang web
Hãy kể tên các trường hợp liên kết mà em đã gặp khi duyệt web hoặc khi đọc văn bản.

### a) Liên kết tới một trang web khác
Liên kết từ một trang web tới một trang web khác trên Internet được gọi là liên kết ngoài. Để tạo liên kết ngoài, ta sử dụng thẻ `<a>` và truyền đường dẫn tuyệt đối cho thuộc tính `href`.
Ví dụ, để đặt liên kết tới mục **Sách điện tử** của bộ sách **Kết nối tri thức với cuộc sống** trên website của Nhà xuất bản Giáo dục Việt Nam trên trang web của mình, em sử dụng đoạn mã:
Mô tả đoạn mã: Đoạn mã HTML sử dụng thẻ `<a>` với thuộc tính `href` chứa đường dẫn `https://hanhtrangso.nxbgd.vn/sach-dien-tu?book_active=0` và nội dung hiển thị là "Sách điện tử Kết nối tri thức với cuộc sống".
Kết quả có được là đoạn văn bản đã được liên kết đến trang web **Sách điện tử** của bộ sách **Kết nối tri thức với cuộc sống**. Khi nháy chuột vào liên kết, trình duyệt sẽ gọi tới trang web **Sách điện tử** và hiển thị nội dung trang web.

### b) Liên kết đến một vị trí khác trong cùng website
Trong lập trình web, phần lớn các liên kết được sử dụng là liên kết trỏ tới các trang trong website của mình. Ví dụ, từ trang chủ đi tới các trang nội dung chi tiết. Trường hợp này gọi là liên kết trong. Ta sử dụng đường dẫn tương đối cho thuộc tính `href`. Khi đường dẫn không có giao thức ở đầu (`http://` hoặc `https://`), trình duyệt kiểm tra địa chỉ đó trên máy chủ hiện tại để tìm tài liệu và liên kết. Tên đường dẫn được sử dụng để xác định tệp được liên kết.
Để hiểu rõ về cách viết đường dẫn tương đối, xét website có cấu trúc đơn giản như Hình 10.1.

Các trường hợp liên kết trong website có thể là:

*   Liên kết tới trang web cùng thư mục
    Để liên kết tới một tệp trong cùng thư mục, ta chỉ cần cung cấp tên của tệp liên kết tới. Ví dụ tạo liên kết từ trang **index.html** tới trang **thong_tin.html** như sau:

    Mã HTML tạo hyperlink đến trang `thong_tin.html` với văn bản hiển thị là "Giới thiệu về trang web".

*   Liên kết tới trang web thuộc thư mục khác, dưới một cấp
    Đường dẫn đến trang web khác thư mục, dưới một cấp gồm tên thư mục và tên tệp được phân cách bằng dấu “/”. Ví dụ tạo liên kết từ trang **index.html** tới trang **bai_tap_1.html** như sau:

    Mã HTML tạo hyperlink đến trang `bai_tap/bai_tap_1.html` với văn bản hiển thị là "Bài tập 1".

*   Liên kết tới trang web thuộc thư mục khác, dưới hai (hay nhiều) cấp
    Tương tự, đường dẫn gồm tên các thư mục và tên tệp cần được liên kết theo thứ tự từ trên xuống. Mỗi cấp thư mục hoặc tệp tin được phân cách bởi dấu “/”. Ví dụ: tạo liên kết từ trang **index.html** tới trang **bai_tap_on_tap.html** như sau:

    Mã HTML tạo hyperlink đến trang `bai_tap/on_tap/bai_tap_on_tap.html` với văn bản hiển thị là "Bài tập ôn tập".

Trong trường hợp trang web liên kết tới nằm ở thư mục mức trên, ta sử dụng các kí tự “**../**”. Khi sử dụng “**../**” trong đường dẫn, tức là chỉ định “trở lại thư mục trên một mức” của thư mục chứa tệp có liên kết. Số cụm “**../**” trong đường dẫn tương ứng với số mức quay trở lại thư mục ở mức trên.
