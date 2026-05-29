# Bài 1: MỘT SỐ THAO TÁC CHỈNH SỬA ẢNH VÀ HỖ TRỢ CHỈNH SỬA ẢNH

**Học xong bài này, em sẽ:**
*   Thực hiện được các thao tác: **thu nhỏ**, **phóng to** và **di chuyển ảnh**.
*   Thực hiện được một số thao tác chỉnh sửa ảnh: **cắt ảnh**, **hiệu chỉnh màu sắc** cho ảnh và **biến đổi ảnh đơn giản** (thay đổi kích thước, xoay, lật, làm nghiêng).

Hãy cho biết tương ứng với mỗi nhu cầu sau đây, cần thực hiện thao tác nào:
1.  Muốn nhìn bao quát toàn bộ ảnh trong khi màn hình không hiển thị hết bức ảnh.
2.  Muốn nhìn gần và rõ một chi tiết trong ảnh để xử lí.
3.  Muốn quan sát rõ hai vùng ảnh đã được phóng to và ở vị trí xa nhau, không nhìn thấy cả hai cùng một lúc.

## Thu nhỏ, phóng to và di chuyển ảnh

1.  Hãy mở một tệp ảnh trong GIMP, sau đó quan sát bằng công cụ và các thành phần xung quanh cửa sổ ảnh. Từ đó, hãy dự đoán xem những công cụ nào giúp thu nhỏ, phóng to và di chuyển ảnh.

Quá trình quan sát, thiết kế, chỉnh sửa ảnh thường cần đến các thao tác hỗ trợ như: **thu nhỏ**, **phóng to** và **di chuyển ảnh**.

Ví dụ, xét tình huống cần đổi màu quần của nhân vật chuột Mickey. Trước hết, sử dụng công cụ Free Select (chọn tự do) để tạo một vùng chọn xung quanh chiếc quần. Trong quá trình chọn, cần phóng to và di chuyển ảnh sao cho quan sát rõ chỗ tiếp giáp giữa quần với cảnh nền. Để xác định chính xác đường biên của vùng chọn. Khi chọn xong, thu nhỏ ảnh như ban đầu để nhìn được toàn bộ vùng chọn.

### a) Thu nhỏ, phóng to ảnh
Có ba cách thu nhỏ, phóng to ảnh:
*   Cách 1: Giữ phím **Ctrl** rồi lăn nút cuộn chuột theo chiều tiến hoặc lùi.
*   Cách 2: Gõ trực tiếp giá trị vào ô tỉ lệ thu/phóng ở góc dưới bên trái thanh trạng thái.
*   Cách 3: Sử dụng công cụ **Zoom** (thu/phóng).
    *   Bước 1. Nháy chuột vào công cụ **Zoom** (thu/phóng).
    *   Bước 2. Đưa chuột vào cửa sổ ảnh và nháy chuột để phóng to ảnh hoặc giữ phím **Ctrl** khi nháy chuột để thu nhỏ ảnh.

### b) Di chuyển ảnh
Để di chuyển đồng thời cả ảnh và khung ảnh (**canvas**), thực hiện một trong hai cách sau:
*   Cách 1: Giữ phím **Space** rồi di chuyển chuột.
*   Cách 2: Sử dụng thanh trượt dọc và thanh trượt ngang để cuộn nội dung trong cửa sổ sao cho hiển thị được vùng ảnh cần xem.
Để di chuyển ảnh nhưng không di chuyển khung ảnh, sử dụng công cụ **Move** (di chuyển) như sau:
*   Bước 1. Nháy chuột vào công cụ **Move**.
*   Bước 2. Kéo thả chuột trên đối tượng để di chuyển nó trên khung ảnh.
Ví dụ minh họa một kết quả di chuyển ảnh nhân vật hoạt hình bằng công cụ **Move**, khi đó ảnh lệch ra khỏi khung ảnh do khung ảnh được giữ cố định.

## 2) Cắt ảnh
**Cắt ảnh** là chọn, giữ lại một phần bức ảnh và loại bỏ phần còn lại. Nhu cầu cắt ảnh thường này sinh trong quá trình chỉnh sửa ảnh. Ví dụ, sau khi hình nhân vật được chọn rồi tách ra khỏi nền ảnh như trong ảnh minh họa, thao tác cắt ảnh sẽ giúp xác định một vùng hình chữ nhật đủ để chứa hình nhân vật cần lấy.
Thực hiện cắt ảnh như sau:
*   Bước 1. Nháy chuột chọn công cụ **Crop** (cắt ảnh) rồi đưa chuột vào cửa sổ ảnh để xác định một vùng ảnh hình chữ nhật cần lấy.
*   Bước 2. Kéo thả chuột trên các ô hình chữ nhật tại các đường biên vùng chọn để điều chỉnh kích thước vùng ảnh cần cắt.

Bước 3. Nhấn phím Enter để xoá toàn bộ vùng ảnh bên ngoài vùng đã chọn.
Các cách cắt ảnh khác sử dụng công cụ chọn hoặc công cụ tạo đường dẫn để chọn vùng ảnh cần lấy. Bản chất của những cách này là thực hiện “kĩ thuật cắt xén chi tiết thừa” đã được giới thiệu trong Chủ đề E ở lớp 10. Sau khi cắt ảnh, thường phải thực hiện lệnh Layer\Layer to Image Size hoặc Image\Fit Canvas to Layers để điều chỉnh khung ảnh vừa với ảnh sau khi cắt.

## Biến đổi ảnh
Các thao tác hỗ trợ chỉnh sửa ảnh cũng thường phát sinh khi thực hiện các phép **biến đổi ảnh**, đặc biệt là thao tác cắt ảnh. Ví dụ, Hình 4a cho thấy bức ảnh biểu tượng mũi Sa Vĩ (tỉnh Quảng Ninh) bị chụp nghiêng. Nó được chỉnh cho thẳng lại như ở Hình 4b bằng công cụ **Perspective**, sau đó ảnh được cắt để loại bỏ các phần thừa hai bên để có ảnh như ở Hình 4c. Lưu ý, quá trình biến đổi ảnh sau đó cắt ảnh có thể làm mất đi một phần bức ảnh.

Hãy khám phá một số công cụ **biến đổi ảnh** sau đây bằng cách thử biến đổi một ảnh nào đó theo các bước cho bên dưới: **Scale** (thay đổi kích thước), **Rotate** (xoay ảnh), **Flip** (lật ảnh), **Perspective** (biến đổi phối cảnh).

### Các bước biến đổi ảnh
*   Bước 1. Nháy chuột chọn công cụ biến đổi ảnh trong hộp công cụ.
*   Bước 2. Nháy chuột vào ảnh cần biến đổi. Một lưới hoặc khung bao quanh ảnh xuất hiện với các ô vuông nhỏ ở các góc, trên các cạnh và ở trung tâm, ví dụ như ở Hình 4b. Các ô này được gọi là “mốc điều khiển”. Ngoài ra còn có một hộp thoại để nhập các tham số biến đổi ảnh.
*   Bước 3. Tiến hành biến đổi ảnh bằng cách kéo thả chuột từ các mốc điều khiển hoặc nhập các tham số vào hộp thoại trên đây. Xác nhận kết quả biến đổi ảnh bằng cách nhấn phím **Enter** hoặc chọn một công cụ bất kì khác (thường chọn công cụ **Move**). Nếu muốn huỷ bỏ kết quả biến đổi ảnh, thay vì nhấn **Enter** hãy nhấn phím **ESC** hoặc lệnh **Reset** trong hộp thoại.

## Thực hành chỉnh sửa ảnh

### Nhiệm vụ 1. Hiệu chỉnh màu sắc cho ảnh

**Yêu cầu:**

Cho ảnh nhân vật chuột Mickey với đôi giày màu vàng như ở Hình 1a. Hãy đổi màu đôi giày của nhân vật để màu vàng sẫm hơn như ở Hình 5. Em có thể chọn ảnh khác và hiệu chỉnh lại màu sắc cho toàn bộ ảnh hoặc cho một đối tượng nào đó trong ảnh.

**Hướng dẫn thực hiện:**

Cách hiệu chỉnh màu sắc cho một vùng ảnh như sau:

*   **Bước 1.** Dùng công cụ **Free Select** kết hợp với các thao tác hỗ trợ để chọn chính xác đối tượng cần hiệu chỉnh màu sắc.
*   **Bước 2.** Thực hiện lệnh **Colors\Curves** để mở hộp thoại Curves như ở Hình 6a. Đường chéo trong hộp thoại là dãy cung điều khiển màu sắc của ảnh.
*   **Bước 3.** Nháy chuột vào danh sách **Channel** (kênh màu) để chọn màu cần hiệu chỉnh. Kéo thả chuột tại một vị trí thích hợp trên dãy cung để uốn nó hướng lên trên hoặc xuống dưới tuỳ theo ý định tăng hay giảm cường độ của màu đã chọn. Trong lúc kéo thả chuột, quan sát thấy nếu màu thay đổi như mong đợi thì dừng lại. Ví dụ, sau khi chọn từng màu Green, Blue và Red từ danh sách **Channel** rồi kéo thả các dãy cung màu để được các hình dạng tương tự như trong Hình 6b, giày của nhân vật sẽ đổi thành màu vàng sẫm như ở Hình 5.

### Nhiệm vụ 2. Sửa chữa ảnh bị nghiêng và lật đối xứng ảnh

**Yêu cầu:**

Hãy sưu tầm một bức ảnh bị chụp nghiêng, sau đó sửa cho bức ảnh khỏi nghiêng và lật đối xứng nó để thay đổi hướng nhìn. Ví dụ, Hình 7a minh hoạ bức ảnh cầu Cần Thơ bị chụp nghiêng và được chỉnh lại như ở Hình 7b, sau đó được lật đối xứng để thay đổi góc nhìn thuận chiều từ trái sang phải như ở Hình 7c.

### Hướng dẫn thực hiện:
*   **Bước 1**. Chọn công cụ **Perspective** rồi nháy chuột vào ảnh cầu Cần Thơ.
*   **Bước 2**. Kéo thả chuột tại các điểm mốc phù hợp để chỉnh cho ảnh hết nghiêng. Dùng công cụ **Crop** để cắt ảnh và nhận được kết quả. Dùng công cụ **Flip** để lật ảnh và thu được kết quả.

## Luyện tập
Em hãy sưu tầm một bức ảnh bị chụp nghiêng, sau đó sửa cho bức ảnh khỏi nghiêng và hiệu chỉnh lại màu sắc của một đối tượng nào đó trong ảnh.

Trong các câu khẳng định dưới đây, mỗi số thứ tự biểu thị một chỗ trống cần điền. Từng số thứ tự này cần thay bằng từ nào trong các từ sau: Space, Move, Zoom, Fit Canvas to Layers?
*   a) Dùng phím (1) hoặc dùng các thanh trượt dọc/ngang để di chuyển ảnh.
*   b) Dùng công cụ (2) để di chuyển ảnh trên khung ảnh (canvas).
*   c) Sau khi cắt ảnh thường dùng lệnh (3) để khung ảnh khớp với kích thước của ảnh sau khi cắt.
*   d) Dùng công cụ (4) kết hợp với phím **Ctrl** để thu nhỏ hoặc phóng to ảnh.

## Tóm tắt bài học
*   Thu nhỏ, phóng to ảnh bằng cách nhấn, giữ phím **Ctrl** và lăn nút cuộn chuột. Hai cách khác là dùng công cụ **Zoom** hoặc ô tỉ lệ thu/phóng ảnh.
*   Di chuyển toàn bộ ảnh (ảnh và khung ảnh) bằng cách nhấn, giữ phím **Space** và di chuyển chuột. Di chuyển ảnh (nhưng giữ cố định khung ảnh) bằng công cụ **Move**.
*   Một số công cụ biến đổi ảnh thường sử dụng là: **Scale, Rotate, Flip, Perspective**.
