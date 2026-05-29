# Bài 3: THỰC HÀNH ĐỊNH DẠNG VĂN BẢN VÀ TẠO SIÊU LIÊN KẾT

## Học xong bài này, em sẽ:
* Tạo được trang web đơn giản với các đoạn văn bản và các tiêu đề mục.
* Làm nổi bật được nội dung văn bản trên màn hình trình duyệt web.
* Tạo được siêu liên kết.

## Nhiệm vụ 1. Tạo tiêu đề mục cho trang web giới thiệu về bản thân
**Yêu cầu:** Soạn thảo nội dung trang web giới thiệu bản thân và lưu tệp văn bản HTML với tên "Bai3-NV1.html". Màn hình trình duyệt web cần hiển thị:
* Tiêu đề trang web là: Trang web cá nhân.
* Dòng đầu tiên viết nội dung: Trang web cá nhân của <Tên của em> được trình bày với tiêu đề mục **Heading 1**. Ví dụ: Trang web cá nhân của Thanh Uyên.
* Các dòng tiếp theo là tiêu đề mục **Heading 2** với các mục Thông tin cá nhân, Sở thích, mỗi mục viết trên một dòng.

## Hướng dẫn thực hiện:
### Bước 1. Tạo tệp "Bai3-NV1.html".
* Mở phần mềm Sublime Text.
* Mở tệp mới bằng cách chọn File\New File.
* Lưu tệp với tên là "Bai3-NV1.html", thực hiện soạn thảo.

### Bước 2. Tạo cấu trúc và khai báo phần tử head cho tệp "Bai3-NV1.html".
* Dòng đầu tiên soạn Khai báo DOCTYPE để sử dụng phiên bản HTML5.
* Khai báo phần tử **html** bằng cặp thẻ đại diện cho phần tử gốc HTML.
* Trong nội dung phần tử **html**:
    * Khai báo phần tử **head** bằng cặp thẻ đại diện cho phần tử head.
    * Khai báo phần tử **body** bằng cặp thẻ đại diện cho phần tử body.

* Trong nội dung phần tử **head**:
    *   Khai báo tiêu đề trang web bằng phần tử `title`.
    *   Thiết lập thuộc tính **charset** của phần tử `meta` để hiển thị đúng tiếng Việt trên trình duyệt bằng khai báo `<meta charset="utf-8">`.
### Bước 3. Soạn nội dung phần tử **body** cho tệp “Bai3-NV1.html”.
    *   Sử dụng phần tử `h1` để trình bày tiêu đề mục Heading 1.
    *   Sử dụng phần tử `h2` để trình bày tiêu đề mục Heading 2.
### Bước 4. Ghi lưu, mở tệp bằng trình duyệt web và xem kết quả.
*   *Lưu ý:* Để thêm **chú thích** vào văn bản HTML, em viết chú thích trong cặp thẻ `<!--` và `-->`. Các chú thích sẽ không hiển thị trên trình duyệt web.

## Nhiệm vụ 2. Làm nổi bật nội dung cho trang web giới thiệu về bản thân

**Yêu cầu:**

1.  Soạn nội dung chi tiết cho mỗi mục đã có tiêu đề trong trang web giới thiệu bản thân ở tệp “Bai3-NV1.html”.
    *   Mục Thông tin cá nhân cần có các thông tin: Họ và tên, Sinh năm, Quê quán.
    *   Mục Sở thích, nêu các sở thích của mình (ví dụ, Đọc sách: Các tác phẩm của nhà văn Nguyễn Nhật Ánh; Thể thao: Chơi bóng chuyền, Chơi cầu lông).
2.  Trình bày trang web như sau:
    *   Các nội dung trong từng mục được trình bày dưới dạng các đoạn văn bản.
    *   Nội dung trong mục Sở thích được in nghiêng.

**Hướng dẫn thực hiện:**

*   **Bước 1**. Mở tệp “Bai3-NV1.html”, ghi lưu tệp với tên mới là “Bai3-NV2.html”.
*   **Bước 2**. Cập nhật nội dung phần tử **body** cho tệp “Bai3-NV2.html”.
    *   Chèn dòng mới vào sau dòng khai báo tiêu đề mục “Thông tin cá nhân”, sử dụng phần tử `p` để tạo đoạn văn ghi nội dung “Họ và tên: <Tên của em>”, “Sinh năm: <Năm sinh của em>”, “Quê quán: <Quê quán của em >”.
    *   Chèn dòng mới vào sau dòng khai báo tiêu đề mục “Sở thích” tương tự như trên.
*   **Bước 3**. Làm nổi bật nội dung trang web.
    Trong nội dung phần tử **body**: Kết hợp sử dụng phần tử `p` và phần tử `em` để in nghiêng các nội dung cụ thể như minh hoạ.
*   **Bước 4**. Ghi lưu, mở tệp bằng trình duyệt web và xem kết quả.

## Nhiệm vụ 3. Tạo siêu liên kết

**Yêu cầu:** Trong trang web giới thiệu cá nhân vừa tạo được ở Nhiệm vụ 2, em hãy tạo siêu liên kết để cung cấp thêm thông tin về Quê quán. Kết quả cần có là khi nháy chuột vào tên tỉnh/thành phố trong mục Quê quán, trang web cổng thông tin điện tử của quê hương em sẽ được mở ra.

### Hướng dẫn thực hiện:

*   **Bước 1.** Mở tệp “Bai3-NV2.html”, ghi lưu với tên mới là “Bai3-NV3.html”.
*   **Bước 2.** Sửa nội dung dòng thông tin Quê quán để tạo siêu liên kết bằng cách sử dụng phần tử **a**.

    **Ví dụ**, khai báo sau sẽ tạo siêu liên kết đến trang web cổng thông tin điện tử thành phố Hà Nội:
    *Mô tả mã:* Đoạn mã HTML này tạo một đoạn văn bản có nội dung "Quê quán: Hà Nội". Trong đó, chữ "Hà Nội" được biến thành một siêu liên kết dẫn đến địa chỉ `https://www.hanoi.gov.vn/`.

    **Lưu ý:** Các tỉnh, thành phố đều có trang web cổng thông tin điện tử với tên dạng `<tentinh>.gov.vn`. (Ví dụ: `thanhphohaiphong.gov.vn`, `hochiminhcity.gov.vn`,...).
*   **Bước 3.** Ghi lưu, mở tệp bằng trình duyệt web và xem kết quả.

### Tạo website cá nhân:

Em hãy hoàn thành một website cá nhân của riêng mình theo ý muốn.

**Gợi ý:**

*   Tạo thư mục `myHomepage` để lưu trữ website cá nhân.
*   Tạo trang chủ của website bằng cách mở tệp mới, ghi và lưu trong thư mục `myHomepage` với tên tệp là “index.html”.
*   Tạo hai văn bản HTML bằng cách mở tệp mới, ghi và lưu trong thư mục `myHomepage` với tên tệp là “hobbies.html” và “album.html”.
*   Sử dụng phần tử **h1** để soạn tiêu đề cho văn bản `index.html` (Ví dụ: “Website của tôi”).
*   Tạo các siêu liên kết sau: liên kết “Sở thích” đến tệp “hobbies.html”, liên kết “Ảnh của tôi” đến tệp “album.html”.
*   Sử dụng phần tử **p** để viết đoạn văn ngắn giới thiệu về bản thân em.
