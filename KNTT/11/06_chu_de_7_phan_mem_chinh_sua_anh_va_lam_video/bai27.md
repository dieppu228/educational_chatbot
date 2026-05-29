# Bài 27: CÔNG CỤ VẼ VÀ MỘT SỐ ỨNG DỤNG

**SAU BÀI HỌC NÀY EM SẼ:**
*   Biết được khái niệm **lớp ảnh**.
*   Biết một số **công cụ vẽ** đơn giản.
*   Thực hiện được một số ứng dụng để tẩy, làm sạch và xoá các vết xước trên ảnh.

Khi chỉnh sửa ảnh em muốn thực hiện những việc gì? Em đã dùng những phần mềm chỉnh sửa ảnh nào?

## 1. GIỚI THIỆU VỀ LỚP ẢNH

### Hoạt động 1 Nền xanh để làm gì?
Khi làm phim, các cảnh quay thường diễn ra như
Em có biết nền màu xanh để làm gì không?

**Lớp ảnh (Layer)** đóng vai trò quan trọng trong chỉnh sửa ảnh, giúp xử lí các phần riêng biệt của bức ảnh mà không làm ảnh hưởng đến các phần khác và dễ dàng sử dụng lại từng phần nhỏ trong ảnh.

Khái niệm về **lớp ảnh** tương tự như trong Inkscape, nghĩa là mỗi lớp ảnh sẽ chứa một số đối tượng hình ảnh, thứ tự sắp xếp của các lớp và độ trong suốt của mỗi lớp sẽ ảnh hưởng đến hình ảnh tổng thể của tệp ảnh. Các thao tác quản lí các lớp ảnh được tìm thấy trong hộp thoại **Layer** ở góc dưới bên phải màn hình của GIMP.

Có thể thêm mới, xoá hay thay đổi thứ tự các lớp ảnh. Các lớp ảnh được sắp theo thứ tự hiển thị từ dưới lên trên. Có hay không hình con mắt bên cạnh biểu tượng và tên lớp cho biết lớp được hiển thị hay ẩn. Chọn một lớp để xử lí riêng (chỉnh sửa hay vẽ thêm). Có thể thay đổi thứ tự lớp bằng cách kéo thả lên trên hoặc xuống dưới.

Mỗi lớp ảnh chứa một số đối tượng của ảnh để có thể xử lí riêng. Thứ tự sắp xếp của các lớp quyết định ảnh sản phẩm.

Trong Hình 27.2, lớp nào được hiển thị, lớp nào không?

# Bài 2: GIỚI THIỆU MỘT SỐ CÔNG CỤ VẼ

## Hoạt động 2: Chỉnh sửa ảnh thời xưa

Hình 27.3 là một bức ảnh nổi tiếng của nhiếp ảnh gia Kusaikabe Kimbei được chụp từ những năm 1870. Em có thể xác định được tác giả đã phải vẽ thêm những gì để thu được tấm hình này không?

Vẽ thêm vào ảnh gốc là một phần của việc chỉnh sửa ảnh. Các công cụ vẽ trong GIMP được cung cấp trong bảng chọn Tools → Paint Tools. Công cụ vẽ gồm ba nhóm chính: vẽ thêm (ví dụ như **Paint Brush, Bucket Fill, Gradient**), tẩy (**Eraser**) và vẽ bằng vùng chọn (ví dụ như **Clone** và **Healing**) (Bảng 27.1). Để dùng một công cụ nào đó em nháy chuột vào biểu tượng tương ứng trong hộp công cụ hoặc nhấn tổ hợp phím tắt tương ứng.

Các công cụ **Clone** và **Healing** thường dùng để sửa nhược điểm trên ảnh hay lấp đầy một vùng ảnh đã cắt.

Các công cụ vẽ là phương tiện để chúng ta vẽ thêm chi tiết hoặc loại bỏ các nhược điểm trên ảnh.

* Nêu sự khác nhau giữa hai công cụ **Clone** và **Healing**.

# 3. THIẾT LẬP MÀU SẮC

## Hoạt động 3 Màu sắc

Khi viết trên bảng, các thầy cô sử dụng phấn màu trắng, còn khi viết trong vở học sinh thường dùng mực màu gì? Tại sao không dùng bút mực trắng?

Ngoài ba kênh màu cơ bản R, G và B, giá trị màu sắc của các điểm ảnh còn có một kênh nữa là **kênh alpha**. Khi lớp ảnh có kênh alpha, trên lớp có thể có những điểm ảnh trong suốt, giống như khi ta nhìn qua tấm kính. Khi không có kênh alpha, lớp ảnh giống như tờ giấy, không thể nhìn thấy các hình ảnh ở dưới. Mặc định là chỉ có lớp dưới cùng không có kênh alpha. Ta có thể thêm kênh alpha vào một lớp bằng cách nháy nút phải chuột vào lớp và chọn **Add Alpha Channel**, chọn **Remove Alpha Chanel** để xoá kênh alpha.

GIMP phân biệt màu nổi (**Foreground**) và màu nền (**Background**): màu nổi là màu của các đối tượng được vẽ khi sử dụng các công cụ như cọ vẽ, bút chì,... màu nền được coi là màu của giấy vẽ. Khi dùng công cụ **Erase** để xoá tại một điểm ảnh, nếu lớp không có kênh alpha thì điểm ảnh đó sẽ có màu nền, còn nếu có kênh alpha thì điểm ảnh đó sẽ không có màu và ta có thể nhìn thấy hình ảnh ở lớp dưới tại vị trí được xoá.

Để chọn màu cho màu nổi/màu nền, ta nháy chuột vào ô tương ứng. Trong hộp thoại chọn màu, chọn dải màu trước rồi nháy chuột vào màu muốn chọn. Có thể sử dụng công cụ **Color Picker** để lấy màu từ một điểm ảnh.

Màu nổi là màu dùng cho các công cụ vẽ, màu nền được coi là màu giấy vẽ.

Có ba lớp ảnh theo thứ tự từ dưới lên là 1, 2 và 3. Lớp 1 có một bông hoa, lớp 2 có một quả táo và lớp 3 có một chiếc bàn. Biết chỉ có lớp 2 có kênh alpha và độ mờ của cả 3 lớp là 100. Hỏi khi hiển thị cả ba lớp em thấy hình gì?

# 4. THỰC HÀNH

## Nhiệm vụ 1. Xoá đoạn chi tiết thừa bằng công cụ Clone và Healing

Hướng dẫn:

*   Xoá hình dây điện trên ảnh (Hình 27.5): Chọn công cụ **Healing**, rồi chọn loại cọ và độ lớn của cọ vẽ (sử dụng cọ đầu tròn, độ lớn 300).
*   Đưa con trỏ chuột lên vùng trời màu xanh, nhấn giữ phím **Ctrl** và nháy chuột để sao (vùng nguồn). Nhấn giữ và di chuyển chuột vào vùng dây điện để sao chép điểm ảnh ở vùng nguồn vào vùng chỉnh sửa để xoá hình dây điện.

* Xoá gạch đen: Sử dụng công cụ Clone và làm tương tự công cụ Healing.
Lưu ý: Với phần ảnh sát với lá cây, cần giảm độ lớn của cọ (10) để không làm ảnh hưởng đến phần lá cây.
Trong phần ảnh này, ta muốn nền trời phía sau xanh hoàn toàn. Khác biệt hoàn toàn so với phần ảnh bên cạnh nên không thể dùng công cụ Healing vì công cụ này kết hợp với mẫu tại điểm vẽ nên sẽ tạo ra hiện tượng lem màu do ảnh hưởng của phần lá cây tại điểm giao.

### Nhiệm vụ 2. Thay nền trời trong ảnh cảnh đồng hoa

Thay phần nền trời trong hình cảnh đồng hoa bằng một lớp màu chuyển đơn giản mô phỏng trời trong xanh.

Hướng dẫn:

* Tách phần phong cảnh
Bước 1. Sau khi mở tệp ảnh chỉ có một lớp duy nhất chứa ảnh cảnh đồng hoa. Nháy nút phải chuột vào tên lớp trong hộp thoại Layer và chọn Duplicate layer. Sửa tên lớp mới thành **phong_canh**. Sửa trên bản sao **phong_canh** để không ảnh hưởng đến ảnh gốc.

Bước 2. Nháy nút phải chuột vào lớp **phong_canh** và chọn **Add alpha Channel**.
Bước 3. Sử dụng công cụ chọn tư do để chọn phần bầu trời.
*Lưu ý: Nên phóng to ảnh để dễ thực hiện, để đơn giản, nên cắt cả phần cây phía trên.*
Bước 4. Nháy nút phải chuột vào vùng vừa chọn, chọn **Edit → Clear**. Phần lưới ô vuông xám – đen là phần trong suốt, có thể nhìn thấy lớp bên dưới.
Bước 5. Chỉnh lại cây: Sử dụng công cụ **Eraser** để tẩy các phần còn sót lại hoặc dùng cọ vẽ để thêm viền cây cho đẹp. Có thể chỉnh màu sắc của cây bằng các công cụ đã học trong Bài 26.

### Vẽ nền trời

Bước 5. Nháy nút phải chuột vào lớp dưới cùng (ảnh gốc) và chọn **New Layer**, nhập tên lớp mới là **bau_troi** trong ô **Layer Name**. Lớp **bau_troi** mới tạo sẽ nằm dưới lớp **phong_canh**.
Để tiện thao tác với lớp này, ta tắt hiển thị của tất cả các lớp còn lại (nháy chuột vào hình con mắt bên cạnh mỗi lớp).
Bước 6. Chọn màu nổi và màu nền là hai tông màu của màu xanh lam (các màu có giá trị 4b9dde và c1e6fb, nhập vào ô **HTML notation** trong hộp thoại chọn màu).
Bước 7. Chọn công cụ màu chuyển **Gradient**, trong hộp công cụ.
Bước 8. Chọn kiểu chuyển **FB to GB (RGB)** trong hộp thoại **Gradients**.
Bước 9. Nháy chuột vào điểm sát phía trên cùng của ảnh, kéo thả chuột theo phương thẳng đứng xuống phía dưới để đổ màu cho lớp.
Để xem ảnh tổng thể, em hiển thị lại lớp **phong_canh**.

## LUYỆN TẬP

1.  Trong Nhiệm vụ 2, nếu thực hiện các bước từ 5 đến 9 trước thì khi hiển thị cả ba lớp ta thu được ảnh như thế nào?
2.  Giả sử màu nổi và màu nền đang có giá trị theo hệ RGB là (100, 125, 125) và (225, 225, 0). Nếu ta thực hiện bước 3 và 4 trên lớp ảnh ban đầu (ảnh gốc sau khi mở) thì hình ảnh mới của lớp như thế nào?
3.  Nếu ta cần sử dụng công cụ **Clone** trên một vùng ảnh hình chữ nhật thì theo em ta nên dùng đầu cọ nào?

## VẬN DỤNG

Lấy một ảnh chụp chân dung có nhược điểm như nám, mụn,... Thực hiện việc xoá các vết này bằng công cụ **Clone** và **Healing**. So sánh kết quả khi chỉ dùng một trong hai loại.
