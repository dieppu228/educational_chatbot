# Bài 29: KHÁM PHÁ PHẦN MỀM LÀM PHIM

SAU BÀI HỌC NÀY EM SẼ:
*   Tạo được các đoạn phim, nhập tư liệu từ ảnh và video có sẵn, biên tập được đoạn phim phục vụ học tập và giải trí.

Bạn Nam làm một đoạn phim để kể lại những điều thú vị diễn ra trong kì nghỉ hè của mình. Tư liệu được sử dụng trong phim là các ảnh, video mà Nam đã chụp và quay trong kì nghỉ ấy. Em có mong muốn làm được một đoạn phim như vậy không?

## 1. KHÁM PHÁ PHẦN MỀM LÀM PHIM

Ngày nay, việc tạo các đoạn phim cho các mục đích khác nhau không chỉ là nhu cầu của các tổ chức, doanh nghiệp, mà đang dần trở thành nhu cầu khá phổ biến của mỗi cá nhân. Nếu như trước đây, ta chỉ biết đến các sản phẩm do các nhà làm phim chuyên nghiệp làm ra, thì ngày nay, ta có thể dễ dàng tìm thấy rất nhiều các đoạn phim được tạo ra bởi các cá nhân, đăng tải trên mạng Internet với nhiều thể loại nội dung, mục đích phong phú, hình thức cũng rất hấp dẫn và chuyên nghiệp.

Để đáp ứng nhu cầu của người dùng, nhiều hãng phần mềm đã cho ra đời các ứng dụng làm phim với những tính năng hiện đại, hữu ích. Chỉ cần vào Internet, gõ từ khoá tìm kiếm, chẳng hạn "phần mềm làm phim", ta có thể nhận về hàng ngàn gợi ý. Mỗi phần mềm làm phim đều có những ưu điểm riêng, tuy nhiên, hầu hết chúng đều cung cấp một số tính năng cơ bản như cho phép tạo ra các phân cảnh phim từ các tư liệu đầu vào như ảnh hay video clip. Mỗi phân cảnh được thiết đặt thời lượng xuất hiện trên phim, thiết lập hiệu ứng chuyển cảnh, ghép âm thanh làm nhạc nền, lồng tiếng hay phụ đề,... để tạo thành một đoạn phim hoàn chỉnh.

Giao diện chung của một phần mềm làm phim thường có bố cục với các thành phần chính như Hình 29.2.
1) **Thanh công cụ**: chứa các nút lệnh để thiết lập các tính năng hay các thao tác chỉnh sửa phim.
2) **Ngăn tư liệu**: chứa các tệp ảnh, tệp video clip, tệp âm thanh,... là đầu tư liệu vào cho phim.
3) **Ngăn xem trước** đoạn phim và các lệnh chỉnh sửa, điều khiển đối tượng đang xem trước.
4) **Con trỏ thời điểm**.

### Ngăn tiến trình
đây là khu vực giúp theo dõi, quản lí toàn bộ trình tự cũng như các thành phần của phim. Có hai chế độ hiển thị trong ngăn tiến trình:

*   Hiển thị theo **Phần cảnh** (Story board): Là chế độ hiển thị đơn giản, giúp quan sát trực quan chuỗi các phần cảnh trong phim. Mỗi phần cảnh có thể là một ảnh hoặc một video clip. Con số chỉ thời lượng dưới mỗi phần cảnh thể hiện thời gian xuất hiện trên phim của phần cảnh đó. Nút lệnh giữa các phần cảnh dùng để thiết lập hiệu ứng chuyển cảnh và thời gian diễn ra hiệu ứng.
*   Hiển thị theo **Dòng thời gian** (Timeline): Là chế độ hiển thị toàn bộ các thành phần của đoạn phim dưới dạng các lớp (track) theo đúng trình tự thời gian của phim.

Mỗi đoạn phim có thể có nhiều lớp khác nhau. Ví dụ đoạn phim có hai lớp:

*   Video track 1: **lớp Băng hình số 1**, bao gồm các ảnh và các video clip.
*   Audio track 1: **lớp Âm thanh số 1**, bao gồm đoạn âm thanh được sử dụng làm nhạc nền cho phim.

Tại mỗi thời điểm, đoạn phim sẽ thể hiện đồng thời các lớp đối tượng này. Chẳng hạn, tại thời điểm con trỏ đang đứng, phim sẽ hiển thị phần cảnh tại Video track 1 và âm thanh nhạc nền ở Audio track 1.

* Có thể tạo ra các đoạn phim bằng cách sử dụng phần mềm làm phim.
* Phần mềm làm phim có các tính năng giúp sắp xếp các tư liệu (ảnh, video clip, âm thanh) theo một trình tự, thời lượng nhất định tạo thành chuỗi các phân cảnh để làm thành một đoạn phim hoàn chỉnh.

## 2. THỰC HÀNH TẠO VÀ BIÊN TẬP MỘT ĐOẠN PHIM TỪ TƯ LIỆU ẢNH VÀ VIDEO CÓ SẴN
Hướng dẫn thực hành sau đây sử dụng phần mềm VideoPad của nhà sản xuất NCH Software, phiên bản không thương mại để minh hoạ. Các em có thể tải phần mềm này từ địa chỉ https://www.nchsoftware.com/videopad/index.html và thực hành cá nhân hoặc theo nhóm.

### Nhiệm vụ 1. Chuẩn bị tư liệu và kịch bản phim
Hướng dẫn:
* Chuẩn bị tư liệu đầu vào cho đoạn phim: khoảng 5 ảnh và 1 video clip. Nếu tải từ mạng Internet, cần lưu ý về bản quyền của chúng.
* Xây dựng ý tưởng, kịch bản phim, xác định thứ tự các phân đoạn. Nên đặt tên cho các tư liệu theo thứ tự phân đoạn dự kiến, chẳng hạn Ảnh 1, Ảnh 2,..., Video 1, Video 2,...

### Nhiệm vụ 2. Tạo đoạn phim từ tư liệu đã chuẩn bị
Hướng dẫn:
### Bước 1. Khởi động phần mềm VideoPad.
### Bước 2. Chọn lệnh Video Wizard tại màn hình khởi động của VideoPad.
Đây là tính năng hỗ trợ tạo phim đơn giản và nhanh nhất theo các mẫu có sẵn của phần mềm. Khi hộp thoại Video Wizard hiện ra, có các mẫu phim nhóm Full Video (mẫu phim có ba đoạn). Thực hiện các bước sau:
    * Chọn một mẫu bất kì (chẳng hạn Vacation).
    * Nháy chọn Select để bắt đầu.

### Bước 3: Tạo video theo mẫu đã chọn

#### Bước 3.1: Chọn tư liệu đầu vào tại hộp thoại Add Content

1.  Nháy chọn Add Files.
2.  Hộp thoại Add Files to Your Project hiện ra, mở thư mục chứa các tư liệu, chọn các ảnh và video tư liệu rồi chọn Open. Các ảnh và video được chọn sẽ được đưa vào hộp thoại Add Content. Ở bước này, có thể bổ sung hoặc xoá các tư liệu nếu cần.
3.  Tiếp tục chọn Next để sang bước tiếp theo.

#### Bước 3.2: Chọn âm thanh, nhạc nền cho phim

Sau bước chọn ảnh và video clip đầu vào là bước chọn âm thanh hoặc nhạc nền cho phim với các lựa chọn.
Ở bài thực hành này, hãy thử lựa chọn “Sử dụng nhạc nền đi kèm mẫu” (Use theme music) rồi chọn lệnh Next để chuyển sang bước tiếp theo.

#### Bước 3.3: Biên tập đoạn phim mở đầu (Intro).

Mẫu đoạn mở đầu gồm 1 ảnh và 2 dòng chữ.
1. Tích chọn ảnh muốn đưa vào đoạn mở đầu.
2. Gõ nội dung chữ xuất hiện trên đoạn mở đầu.
3. Chọn màu chữ.
4. Chọn phông chữ.
5. Nháy chọn Next để chuyển sang bước tiếp theo.

#### Bước 3.4. Biên tập đoạn phim kết thúc (Outro).
Thực hiện tương tự Bước 3.3.
#### Bước 3.5. Xem trước đoạn phim vừa tạo.
Sau khi thực hiện xong các bước trên, phần mềm cho phép ta xem lại đoạn phim vừa tạo (Hình 29.8).
Quay lại các bước trước để sửa lại nếu cần.
Các nút điều khiển để xem trước đoạn phim.
Kết thúc quá trình tạo đoạn phim.

### Bước 4. Nháy chọn **Create** để kết thúc quá trình tạo đoạn phim (Hình 29.8).
### Bước 5. Lưu lại và xuất bản phim.
* Sau bốn bước trên, phần mềm sẽ hiện ra giao diện như Hình 29.2. Em có thể xem lại đoạn phim của mình ở **ngăn xem trước**.
* Lưu lại dự án làm phim của mình, đặt tên dự án theo cấu trúc <**Tên phim**>.<**Ngày tạo**>.vpj. Ta sẽ quay lại dự án này để làm cho đoạn phim thêm hấp dẫn ở các tiết học sau.

– Nháy chọn lệnh **Export Video** trên thanh công cụ để xuất bản phim vừa tạo với các lựa chọn gợi ý như dưới đây:

*   1. Đặt tên cho đoạn phim
*   2. Chọn đường dẫn tới thư mục lưu đoạn phim
*   3. Chọn định dạng đoạn phim, chẳng hạn .mp4
*   Dung lượng đoạn phim ước tính. Dung lượng này phụ thuộc độ dài phim và định dạng tệp phim
*   4. Nháy chọn **Create** để tạo đoạn phim

Chúc mừng em đã hoàn thành đoạn phim đầu tiên của của mình.

## LUYỆN TẬP

Mở tệp dự án phim em vừa tạo được bằng phần mềm VideoPad. Tại ngăn **Tư liệu**, lần lượt mở các trang **Sequences**, **Video Files**, **Audio Files**, **Images**, quan sát danh sách tư liệu tại mỗi trang đó, lập bảng nhận xét theo mẫu dưới đây:

**Lưu trữ tư liệu gồm**
*   1. Sequences: 3 chuỗi phân cảnh chính: (1) Đoạn phim mở đầu; (2) Đoạn phim chính; (3) Đoạn phim kết thúc.
*   2. Video Files: ...
*   3. Audio Files: ...
*   4. Images: ...

## VẬN DỤNG

Tạo mới một đoạn phim với tư liệu đầu vào là các ảnh và video khác, hoặc với tệp nhạc nền khác theo ý thích của em.
