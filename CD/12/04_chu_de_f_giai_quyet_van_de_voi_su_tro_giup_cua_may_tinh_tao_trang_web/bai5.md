# Bài 5: CHÈN HÌNH ẢNH, ÂM THANH, VIDEO VÀ SỬ DỤNG KHUNG

Học xong bài này, em sẽ:
*   Chèn được hình ảnh, tệp âm thanh, video vào trang web.
*   Nhúng được nội dung trang web khác vào trang web.

Em có biết làm thế nào để trang web Bai3-NV1.html em tạo ở bài học trước trở nên đẹp và sinh động hơn không?

## 1. Chèn hình ảnh

Trong số các định dạng ảnh sau: PNG, RAW, BMP, JPG, GIF, theo em, những định dạng ảnh nào được sử dụng phổ biến trên trang web? Vì sao?

Khi tạo trang web, em cần có thêm các nội dung đa phương tiện như hình ảnh, âm thanh, video để việc truyền tải thông tin hiệu quả, trực quan và sinh động hơn. Phần tử **img** khai báo việc chèn hình ảnh vào trang web theo cú pháp sau:
`<img src = “Tên tệp ảnh” alt = “Nội dung” width = “Chiều rộng” height = “Chiều cao”>`

Thuộc tính **src** xác định **Tên tệp ảnh** được chèn vào trang web. Lưu ý, **Tên tệp ảnh** có thể bao gồm cả đường dẫn đến tệp ảnh. Thuộc tính **alt** xác định **Nội dung** thay thế sẽ hiển thị vào vùng của hình ảnh trên trình duyệt web trong trường hợp việc hiển thị hình ảnh gặp lỗi. Thuộc tính **width**, **height** xác định cụ thể kích thước **Chiều rộng** và **Chiều cao** của ảnh, thường được dùng để tăng giảm kích thước của ảnh gốc và tuỳ biến kích thước ảnh khi hiển thị trên trình duyệt web. Theo mặc định, giá trị **Chiều rộng**, **Chiều cao** được tính theo đơn vị điểm ảnh pixel. Ảnh được sử dụng trên trình duyệt web thường ở các định dạng JPG, PNG, GIF. Lưu ý: Ảnh sẽ được hiển thị theo kích thước ảnh gốc nếu không khai báo thuộc tính **width**, **height**.

Ví dụ 1. Nội dung phần **body** của văn bản HTML chèn tệp ảnh “canhdieu.jpg” vào trang web, kết quả hiển thị trên màn hình trình duyệt web.

Đoạn mã HTML này chèn một hình ảnh có tên "canhdieu.jpg" vào trang web, với văn bản thay thế là "Cánh Diều" và thiết lập chiều rộng là 800 pixel, chiều cao là 300 pixel.

Lưu ý: Phải lưu trữ tệp ảnh trong cùng thư mục với văn bản HTML nếu thuộc tính **src** chỉ xác định tên tệp ảnh mà không bao gồm đường dẫn đến tệp ảnh.

## Chèn âm thanh
Phần tử `audio` khai báo việc chèn âm thanh vào trang web theo cú pháp sau:
Mã HTML để chèn tệp âm thanh, với `src` là tên tệp âm thanh và `controls` để hiển thị điều khiển.

Thuộc tính **src** xác định Tên tệp âm thanh được chèn vào trang web. Lưu ý, Tên tệp âm thanh có thể bao gồm đường dẫn đến tệp âm thanh. Định dạng tệp âm thanh thường được sử dụng trên trang web là MP3, OGG. Thuộc tính **controls** được khai báo để hiển thị bảng điều khiển tệp âm thanh trên trình duyệt web. Bảng điều khiển cung cấp một số nút lệnh có chức năng: **Phát, Tạm dừng, Tắt, Tăng/Giảm âm lượng,...**

Ví dụ 2. Nội dung phần `body` của văn bản HTML ở Hình 2a chèn tệp âm thanh “QueHuong.mp3” vào trang web, kết quả hiển thị trên màn hình trình duyệt web như Hình 2b.
Mã HTML trong phần `body` để nhúng tệp âm thanh "QueHuong.mp3" với các điều khiển phát.
Kết quả khi mở văn bản HTML trong trình duyệt web là một giao diện trình phát âm thanh, hiển thị thời lượng 0:00/4:35 và các nút điều khiển.

## Chèn video
Phần tử `video` khai báo việc chèn video vào trang web theo cú pháp sau:
Mã HTML để chèn tệp video, với `src` là tên tệp video và `controls` để hiển thị điều khiển.

Thuộc tính **src** xác định Tên tệp video được chèn vào trang web. Lưu ý, Tên tệp video có thể bao gồm đường dẫn đến tệp video. Định dạng tệp video thường được sử dụng trên trang web là MP4, OGG. Thuộc tính **controls** được khai báo để hiển thị bảng điều khiển tệp video trên màn hình trình duyệt web. Bảng điều khiển cung cấp một số nút lệnh có chức năng **Chạy, Tạm dừng, Tắt, Tăng/Giảm âm lượng, Phóng to/Thu nhỏ màn hình,...**

Ví dụ 3. Nội dung phần `body` của văn bản HTML ở Hình 3a chèn tệp video “monguockyniemxua.mp4” vào trang web, kết quả hiển thị trên màn hình trình duyệt web như Hình 3b.
Mã HTML trong phần `body` để nhúng tệp video "monguockyniemxua.mp4" với các điều khiển phát.
Kết quả khi mở văn bản HTML trong trình duyệt web là một giao diện trình phát video, hiển thị hình ảnh từ video, thời lượng 0:53/4:45 và các nút điều khiển.

## 4. Sử dụng khung

Phần tử `iframe` khai báo việc nhúng một tệp HTML hoặc tài nguyên web khác vào văn bản HTML theo cú pháp sau:

Mã HTML `<iframe src="url" width="Chiều rộng" height="Chiều cao"></iframe>` được dùng để nhúng nội dung.

Trong đó, **url** là đường dẫn đến tệp HTML hoặc tài nguyên web khác. Thuộc tính **width**, **height** xác định cụ thể kích thước chiều rộng và chiều cao của vùng được nhúng trên trang web. Theo mặc định, giá trị Chiều rộng, Chiều cao được tính theo đơn vị **điểm ảnh pixel**.

Ví dụ 4. Nội dung phần `body` của văn bản HTML nhúng trang web `Bai4-NV2.html`, kết quả hiển thị trên màn hình trình duyệt web.

Mã HTML nhúng một tệp HTML khác (Bai4-NV2.html) vào trong phần body của trang web, với chiều rộng và chiều cao là 200 pixel.

Kết quả hiển thị khung trên màn hình trình duyệt web là một bảng thống kê số lượng học sinh lớp 12A1 tham gia hoạt động thể thao của trường, với các nội dung như Bóng bàn (10 nam, 5 nữ), Cờ vua (8 nam, 3 nữ), Chạy cự li ngắn (15 nam, 6 nữ).

Lưu ý: Khi chèn hình ảnh, âm thanh, video, có thể xác định vị trí tuỳ ý trên trang web để hiển thị thành phần được chèn vào. Nhưng khi nhúng nội dung trang web khác vào trang web hiện thời, không thể điều chỉnh vị trí hiển thị các thành phần trong trang web được nhúng.

## 5. Thực hành chèn hình ảnh, âm thanh và sử dụng khung

### Nhiệm vụ 1. Chèn hình ảnh

**Yêu cầu**: Soạn văn bản HTML để tạo trang web có một hình ảnh giới thiệu Văn Miếu Quốc Tử Giám.

**Hướng dẫn thực hiện**:
*   **Bước 1**. Tạo tệp "Bai5-NV1.html".
*   **Bước 2**. Tạo cấu trúc và khai báo phần tử `head` cho tệp "Bai5-NV1.html".
*   **Bước 3**. Chuẩn bị tệp hình ảnh.
    *   Sử dụng công cụ tìm kiếm Google, chọn chế độ tìm kiếm hình ảnh để tìm một hình ảnh về Văn Miếu Quốc Tử Giám và lưu hình ảnh về máy tính.

*   Lưu ảnh với tên "vanmieu.jpg" trong cùng thư mục lưu tệp "Bai5-NV1.html".
*   **Lưu ý**: Có thể chèn hình ảnh từ nguồn khác trên Internet mà không phải lưu ảnh về máy tính. Thực hiện bằng cách sao chép đường link ảnh và gán cho thuộc tính src trong khai báo phần tử img. Tuy nhiên, khi mất kết nối Internet hay nguồn ảnh bị thay đổi thì việc hiển thị hình ảnh có thể gặp lỗi.
*   Bước 4. Chèn hình ảnh vào trang web.
    *   Trong nội dung phần tử body: Thực hiện khai báo để chèn hình ảnh `vanmieu.jpg` và cung cấp văn bản thay thế `Văn Miếu Quốc Tử Giám`.
*   Bước 5. Ghi lưu, mở tệp bằng trình duyệt web và xem kết quả.

### Nhiệm vụ 2. Chèn âm thanh

Yêu cầu: Soạn văn bản HTML giúp Khánh Nam tạo một trang web để nghe bài hát “Nhớ về Hà Nội”.

Hướng dẫn thực hiện:
*   Bước 1. Tạo tệp “Bai5-NV2.html”.
*   Bước 2. Tạo cấu trúc và khai báo phần tử **head** cho tệp “Bai5-NV2.html”.
*   Bước 3. Chuẩn bị tệp âm thanh.
    *   Có thể truy cập một số website như chiasenhac.vn, zingmp3.vn, nhaccuatui.com để tìm kiếm tệp âm thanh định dạng MP3.
    *   Tải và lưu tệp nhạc với tên mới là “nhovehanoi.mp3” trong cùng thư mục lưu tệp “Bai5-NV2.html”.
*   Bước 4. Chèn âm thanh vào trang web.
    *   Trong nội dung phần tử **body**: Thực hiện khai báo để chèn tệp âm thanh `nhovehanoi.mp3`.
*   Bước 5. Ghi lưu, mở tệp trên trình duyệt web và xem kết quả.

### Nhiệm vụ 3. Nhúng tệp HTML đã có vào văn bản HTML

Yêu cầu: Sử dụng phần tử **iframe** để tạo trang web mới có nội dung là hai trang web đã tạo ở Nhiệm vụ 1 và Nhiệm vụ 2.

Hướng dẫn thực hiện:
*   Bước 1. Tạo tệp “Bai5-NV3.html”.
*   Bước 2. Tạo cấu trúc và khai báo phần tử **head** cho tệp “Bai5-NV3.html”.
*   Bước 3. Soạn nội dung phần tử **body** cho tệp “Bai5-NV3.html”.
    *   Trong nội dung phần tử **body**:
        *   Thực hiện khai báo để nhúng tệp `Bai5-NV1.html` bằng **iframe**.

- Khai báo phần tử *iframe* với thuộc tính *src = “Bai5-NV2.html”*.
Lưu ý: Các tệp “Bai5-NV1.html”, “Bai5-NV2.html”, “Bai5-NV3.html” cần được lưu trong cùng một thư mục.
Bước 4. Ghi lưu, mở tệp “Bai5-NV3.html” bằng trình duyệt web và xem kết quả.

### Tạo website cá nhân
Em hãy chèn thêm hình ảnh, âm thanh, video để hoàn thiện tiếp website cá nhân đã tạo ở các bài học trước.

#### Gợi ý thực hiện
* Mở tệp “album.html”, thêm một số hình ảnh của em hoặc em thích (nên lưu tệp ảnh vào thư mục *images*).
* Mở tệp “hobbies.html”, bổ sung tiêu đề mục *h2* là “Bài hát tôi thích” và thêm một tệp âm thanh/video cho bài hát đó.

## Luyện tập
Câu 1. Thuộc tính nào của phần tử *img* được dùng để hiển thị thông báo khi hình ảnh chèn vào trang web gặp lỗi trong quá trình hiển thị trên màn hình trình duyệt web?
A. *link*
B. *title*
C. *src*
D. *alt*

Câu 2. Thuộc tính nào dùng để xác định tài nguyên được nhúng vào trang web khi khai báo *iframe*?
A. *source*
B. *src*
C. *link*
D. *target*

## Tóm tắt bài học
* Các phần tử **img**, **audio**, **video** được dùng để thêm nội dung đa phương tiện (hình ảnh, âm thanh, video) vào trang web.
* Phần tử **iframe** dùng để khai báo nhúng tệp HTML hoặc tài nguyên web khác vào văn bản HTML đang soạn.
