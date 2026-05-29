# Bài 28: TẠO ẢNH ĐỘNG

SAU BÀI HỌC NÀY EM SẼ:
*   Thực hiện được các thao tác tạo ảnh động từ mô hình lớp ảnh.

Em đã từng nhìn thấy hình ảnh chuyển động nhưng không phải một đoạn phim chưa? Nếu đã từng thấy, em gặp ở đâu?

## 1. CÁC THAO TÁC XỬ LÍ TRÊN LỚP ẢNH

GIMP hỗ trợ tạo ảnh gif từ các lớp ảnh mà ta đưa vào. Các lớp ảnh được hiển thị lần lượt từ lớp dưới cùng, mỗi lớp ảnh tương ứng với một khung hình. Do vậy để làm một tệp tin ảnh động ta cần nhiều lớp ảnh và cần thực hiện nhiều thao tác xử lí trên các lớp khác nhau. Những thao tác thường được thực hiện là:

*   **Mở một hay nhiều tệp làm lớp ảnh mới:** chọn lệnh File → Open as Layers. Chọn đường dẫn đến thư mục chứa ảnh, chọn các ảnh muốn mở rồi nháy nút Open. Ta cũng có thể mở thư mục chứa ảnh, chọn và kéo vào màn hình làm việc của GIMP.

*   **Khoá lớp:** Khi một lớp đã sửa xong và muốn đảm bảo không bị sửa nhầm khi sửa các lớp khác, em thực hiện khoá lớp lại bằng cách: nháy chuột vào lớp muốn khoá trong hộp thoại Layer rồi nháy chuột vào thuộc tính mà em muốn khoá.

*   **Gom cụm:** Khi muốn thực hiện một thao tác nào đó cùng lúc trên nhiều lớp ta nháy chuột vào ô vuông thứ hai (hình sợi dây xích) bên tay trái của các lớp muốn cùng thực hiện.

*   **Gộp lớp:** Trong khi thực hiện việc chỉnh sửa ta có thể tạo ra nhiều lớp để xử lí từng phần nhỏ, các lớp sau đó có thể gộp lại để tránh phải quản lí quá nhiều lớp bằng cách nháy nút phải chuột vào tên lớp và chọn Merge Down. Lớp được chọn sẽ được gộp với lớp ngay bên dưới.

Giả sử em đang làm việc với bốn lớp ảnh. Lớp nào có thể thực hiện được lệnh Merge Down? Vì sao các lớp còn lại không thực hiện được?

# Bài 2: THIẾT LẬP ẢNH ĐỘNG TỪ LỚP ẢNH

## Hoạt động 1 Ảnh và video

Mỗi khi phải cài đặt một phần mềm mới trên điện thoại hay máy tính, trong thời gian chờ đợi em sẽ thấy có hình vòng tròn quay, đồng hồ cát hoặc một thanh chạy tăng dần. Hãy phân tích một trong các biểu tượng để xem trong mỗi ảnh ta cần những ảnh thành phần nào?

Để bắt đầu tạo ảnh động, em mở ảnh bằng lệnh **File → Open as Layers**. Ta có thể tạo ảnh động đơn giản như trong phần 1 đã đề cập bằng cách chọn lệnh **Filters → Animation → Playback**. Ảnh động được tạo gồm các ảnh đã mở, mỗi khung hình là một lớp ảnh, hiện lần lượt theo thứ tự từ dưới lên trên.

Em có thể thiết lập thời gian xuất hiện cho mỗi khung hình bằng cách thêm vào phía sau tên lớp tương ứng cụm “(Xms)” trong đó X là số mili-giây mà ta muốn hiển thị khung hình trước khi chuyển sang lớp tiếp theo. Lưu ý rằng, thời gian của các khung hình khác nhau có thể được đặt khác nhau. Ví dụ: Lớp có tên là **Frame 1 (1000ms)** sẽ được hiển thị 1 giây (1000 mili-giây) trước khi chuyển sang hình tiếp theo.

Để xuất ra tệp ảnh động, em chọn **File → Export As** và gõ tên tệp với phần mở rộng là gif (loại tệp trong **Select File Type** là **By Extension**) rồi nháy nút **Export**. Hộp thoại xuất tệp hiện ra, trong đó có ba nội dung cần chú ý:
* Nháy vào ô **As Animation** để tạo ảnh động.
* Nháy vào ô **Loop forever** nếu muốn ảnh lặp lại sau khi hiển thị một lượt từ đầu đến cuối. Nếu không nháy vào ô này, ảnh chỉ chạy một lần rồi dừng.
* Nhập giá trị vào ô màu xanh để xác định số mili-giây dừng giữa các khung hình chưa được đặt thời gian.

Sau khi kiểm tra thông tin, em nháy vào nút **Export** để lưu tệp tin.

Lưu ý: Nếu trong các ảnh đã tải có ảnh mà kích thước lớn hơn khung của hình động, khi thực hiện lệnh xuất sẽ có thông báo: "The image you are trying to export as a GIF contains layers which extend beyond the actual borders of the image.", nháy nút **Crop** để cắt các lớp này cho vừa với khung hình.

Ngoài ra, GIMP còn cung cấp một số hiệu ứng để làm ảnh sinh động hơn.

Để thêm hiệu ứng cho ảnh, em chọn **Filters → Animation** và chọn trong các hiệu ứng có sẵn, ví dụ hiệu ứng Bend:

Blend (Hiệu ứng chuyển động mờ dần giữa các layer): Hiệu ứng này cần ít nhất 3 lớp, lớp dưới cùng là lớp nền, hình ảnh sẽ được chuyển dần dần từ lớp 2 lên lớp trên cùng. Giữa 2 khung hình tương ứng với 2 lớp ảnh gốc có một số khung hình trung gian (số lượng trong ô Intermediate frames) được tạo ra bằng cách hoà trộn lớp nguồn, lớp đích và lớp nền.

Nếu em tạo ảnh động với các lớp như Hình 28.4 và giá trị Delay between frames where unspecified là 2000 thì thời gian xuất hiện của mỗi khung hình bao lâu?

## 3. THỰC HÀNH
### Nhiệm vụ 1. Tạo hình tròn bằng các nét như Hình 28.5
Hướng dẫn:
* Bước 1. Chọn File → New rồi nhập 500 vào hai ô Width và Height rồi nháy OK.
* Bước 2. Chọn màu trắng cho màu nền, chọn công cụ tô màu, hoặc nhấn tổ hợp phím Shift+B rồi tô màu cho lớp vừa tạo.
* Bước 3. Nháy nút phải chuột vào lớp vừa tạo rồi chọn New Layer, đặt tên lớp là **Layer 1**.
* Bước 4. Chọn màu xám nhạt cho màu nền (ví dụ dcdcdc) và màu xám đậm cho màu nền (ví dụ 7f7f7f).
* Bước 5. Nháy chuột vào công cụ Rectangle Select Tool và vẽ một vùng chọn. Trong phần tuỳ chọn công cụ: nháy chọn vào ô Rounded corners, đặt Radius bằng 30 và xác định vị trí vùng chọn: Position 235, 0; Size 30, 90.
* Bước 6. Nhấn tổ hợp phím Shift + B rồi tô màu cho vùng chọn vừa tạo (Hình 28.6a).
* Bước 7. Chọn Duplicate layer trên **Layer 1**.
* Bước 8. Nháy chuột vào lớp ảnh mới (**Layer 1 copy**) rồi chọn công cụ Flip , chọn Vertical trong tuỳ chọn công cụ rồi nháy chuột vào lớp ảnh **Layer 1 copy** (Hình 28.6b).
* Bước 9. Nháy nút phải chuột vào lớp **Layer 1 copy** và chọn Merge Down.
* Bước 10. Chọn Duplicate layer trên **Layer 1**.
* Bước 11. Chọn lệnh **Unified Transform Tool** trong hộp công cụ (nhấn tổ hợp Shift + T); giữ chuột bên ngoài khung hình và quay sao cho hình quay 3 bước (tương ứng với góc quay 45°) rồi nháy vào nút Transform (Hình 28.6c).
* Bước 12. Nháy nút phải chuột vào lớp **Layer 1 copy** và chọn Merge Down.
* Bước 13. Thực hiện lại các bước 10, 11, 12 với góc quay 90° để thu được phần còn thiếu (Hình 28.6d).

### Nhiệm vụ 2. Tạo ảnh động biểu tượng chờ dùng hình trong Nhiệm vụ 1
Hướng dẫn:
*   **Bước 1.** Chọn **Duplicate layer** trên Layer 1.
*   **Bước 2.** Chọn công cụ tạo vùng chọn có màu tương tự **Fuzzy Select Tool** (hoặc nhấn phím U) trên hộp công cụ rồi nháy vào nét gạch ở vị trí 12 giờ. Toàn bộ nét gạch này sẽ được chọn.
*   **Bước 3.** Nhấn tổ hợp phím **Shift + B** để tô màu, nháy chuột vào ô **BG color fill** để tô bằng màu nền màu xám nhạt. Rồi đưa con trỏ chuột lên vùng đã chọn và nháy chuột để tô.
*   **Bước 4.** Chọn **Duplicate layer** trên Layer 1.
*   **Bước 5.** Nháy chuột vào lớp vừa tạo và kéo lên trên cùng.
*   **Bước 6.** Nhấn phím U và nháy chuột vào nét gạch ở vị trí 1 giờ.
*   **Bước 7.** Nhấn tổ hợp phím **Shift+B** rồi di chuột lên vùng vừa chọn và nháy chuột.
*   **Bước 8.** Lặp lại các bước 4, 5, 6, 7 thêm 6 lần, mỗi lần tô một gạch lần lượt theo thứ tự trên vòng tròn. Ta thu được 8 ảnh lần lượt theo thứ tự từ dưới lên trên.
*   **Bước 9.** Xoá lớp Layer 1.
*   **Bước 10.** Chọn lệnh **File → Export As**, nhập tên cho tệp ảnh là **Waiting.gif**, kiểm tra các thông số và nháy chọn **Export** để xuất ra tệp ảnh động **Waiting.gif**.
*   **Lưu ý**: Ta có thể vào xem ảnh tại vị trí đã lưu hoặc xem trước bằng GIMP bằng lệnh **Filter → Animation → Play back** và nháy chọn nút hình tam giác để xem.

## LUYỆN TẬP
1.  Để thay đổi thời gian xuất hiện của khung hình trong một tệp ảnh động em làm thế nào?
2.  Một tệp ảnh mở trong GIMP có 5 lớp ảnh. Nếu dùng hiệu ứng **Blend** với số khung hình trung gian là 5 thì số lượng khung hình do GIMP tạo ra để làm trung gian là bao nhiêu?

## VẬN DỤNG
*   Vẽ và tạo ảnh động hình quả bóng đang nảy trên mặt đất.
