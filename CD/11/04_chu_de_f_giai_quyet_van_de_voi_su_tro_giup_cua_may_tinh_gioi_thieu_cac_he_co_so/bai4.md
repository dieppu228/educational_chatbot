# Bài 4: CÁC BIỂU MẪU CHO XEM VÀ CẬP NHẬT DỮ LIỆU

**Học xong bài này, em sẽ:**
*   Diễn đạt được khái niệm biểu mẫu trong các CSDL và ứng dụng CSDL.
*   Giải thích được những ưu điểm khi người dùng xem và cập nhật dữ liệu cho CSDL thông qua biểu mẫu.

Khi nhập dữ liệu vào một bảng của CSDL quan hệ, theo em có thể gặp những lỗi nào? Em hãy cho ví dụ.

## Khái niệm và chức năng của biểu mẫu

### a) Chức năng của biểu mẫu

Phục vụ cho hoạt động của một tổ chức nên một CSDL có thể được nhiều người cùng sử dụng. Thay vì cho phép người dùng tương tác trực tiếp với CSDL, các giao diện người dùng đã được thiết kế phù hợp với mỗi nhóm người làm việc với CSDL. Biểu mẫu là giao diện thuận tiện để người dùng tương tác với CSDL khi xem dữ liệu, hạn chế bớt lỗi, tránh vi phạm ràng buộc về dữ liệu khi cập nhật CSDL. Biểu mẫu được thiết kế nhằm các mục đích sau:
*   Hiển thị dữ liệu trong bảng dưới dạng phù hợp để xem.
*   Cung cấp một khuôn dạng thuận tiện để nhập và sửa dữ liệu.
*   Cung cấp các nút lệnh để người dùng có thể sử dụng, thông qua đó thực hiện một số thao tác với dữ liệu.

Phổ biến nhất là các biểu mẫu hiển thị dữ liệu cho từng nhóm người dùng và biểu mẫu cho người nhập dữ liệu.

### b) Tạo biểu mẫu

Các hệ quản trị CSDL thường cung cấp các công cụ để tạo được biểu mẫu cho người dùng CSDL. Muốn nhanh chóng có được biểu mẫu theo ý mình, ta có thể dùng công cụ thiết kế biểu mẫu tự động, sau đó điều chỉnh thêm để có một biểu mẫu thân thiện hơn, thuận tiện hơn trong sử dụng. Những ứng dụng CSDL đơn giản sử dụng các biểu mẫu được tạo ra theo cách này. Trong khi đó, ở những ứng dụng CSDL lớn và phức tạp, (thường là những phần mềm được xây dựng trên nền hệ quản trị CSDL), các biểu mẫu như một thành phần của phần mềm ứng dụng được tạo ra nhờ một ngôn ngữ lập trình.

## 2 Biểu mẫu cho xem dữ liệu

Các hệ quản trị CSDL quan hệ thường cung cấp công cụ tạo lập nhanh chóng những **biểu mẫu cho xem dữ liệu**. Những biểu mẫu loại này không cho người xem sửa đổi dữ liệu. Việc thiết kế những biểu mẫu như vậy là để hỗ trợ cho những nhóm người dùng tra cứu thông tin của CSDL trong phạm vi được phép:

*   Biểu mẫu chỉ hiển thị dữ liệu người dùng cần hoặc phần dữ liệu được phép xem. Có thể thiết kế biểu mẫu hiển thị chỉ một phần của dữ liệu trong bảng.
*   Biểu mẫu hiển thị các bản ghi theo thứ tự sắp xếp của một trường nào đó.
*   Biểu mẫu cho xem dữ liệu được lọc theo một tiêu chí nào đó và có thể lọc dần nhiều bước.

### Mô tả về một biểu mẫu hiển thị dữ liệu:

Biểu mẫu hiển thị tiêu đề "ĐỊA CHỈ LIÊN LẠC CỦA HỌC SINH LỚP 11". Nó có các trường thông tin cơ bản như Mã định danh, Họ và tên, Giới tính, Địa chỉ. Bên dưới có các nút điều hướng bản ghi (ví dụ: mũi tên trái/phải, số bản ghi hiện tại trên tổng số bản ghi) và các thanh cuộn dọc, ngang để xem các phần dữ liệu bị khuất.

Các biểu mẫu minh họa trong bài đều được tạo ra bởi hệ quản trị CSDL Microsoft Access 365.

Biểu mẫu mô tả ở trên chỉ hiển thị một số trường của bảng dữ liệu nguồn THÔNG TIN HỌC SINH LỚP 11 (không hiển thị điểm các môn học). Các thanh trượt dọc và ngang được dùng để xem những dữ liệu bị khuất trong cửa sổ biểu mẫu. Các nút **◀ ▶** được dùng để chuyển đến xem bản ghi đứng trước hoặc đứng sau bản ghi hiện thời. Có thể chỉ hiển thị danh sách các bản ghi thoả mãn điều kiện nào đó (ví dụ xem danh sách học sinh là Đoàn viên) bằng cách sử dụng chức năng lọc bản ghi theo điều kiện. Người dùng biểu mẫu có thể thay đổi các điều kiện lọc, điều kiện sắp xếp ngay trên biểu mẫu để xem được dữ liệu tương ứng.

Biểu mẫu cũng có thể hiển thị các trường từ nhiều bảng khác nhau. Một ví dụ khác cho thấy dữ liệu trong biểu mẫu lấy từ 3 bảng SÁCH, NGƯỜI ĐỌC và MƯỢN-TRẢ của CSDL Thư viện trong ví dụ đã nêu.

## Biểu mẫu cho cập nhật dữ liệu

Theo em, có những bất lợi nào trong việc mở một bảng của CSDL quan hệ rồi trực tiếp cập nhật dữ liệu (thêm bản ghi, sửa các bản ghi trong đó)?

Các hệ quản trị CSDL quan hệ cũng thường cung cấp công cụ cho phép tạo lập nhanh chóng những biểu mẫu cập nhật dữ liệu. Những biểu mẫu loại này có các ô nhập dữ liệu còn để trống hoặc chứa dữ liệu đã có nhưng cho phép sửa đổi. Các ô và nhãn đi kèm được bố trí hợp lí cho việc xem và thực hiện thao tác cập nhật.
Việc thiết kế những biểu mẫu như vậy giúp việc cập nhật dữ liệu được tiện lợi hơn, hạn chế được những sai nhầm khi cập nhật:
* Tránh được các cập nhật vi phạm ràng buộc toàn vẹn như ràng buộc khoá, ràng buộc khoá ngoài.
* Tránh được các cập nhật vi phạm ràng buộc miền giá trị, tức là không đưa vào giá trị nằm ngoài tập giá trị được chấp nhận.

Ví dụ 1. Biểu mẫu dùng để nhập dữ liệu. Dữ liệu của các trường ở nửa bên trên biểu mẫu đó (Mã định danh,..., Giới tính) được hiển thị và bị khoá lại không cho thay đổi.

Có thể thiết kế biểu mẫu dùng để cập nhật dữ liệu cho bảng **MƯỢN-TRẢ** và tránh được vi phạm ràng buộc khoá ngoài. Biểu mẫu cho thấy biểu mẫu cập nhật được thiết kế để **Số thẻ TV** của người mượn (hay người trả) không thể gõ nhập vào mà chỉ lựa chọn trong một danh sách thả xuống. Biểu mẫu cho phép nhập dữ liệu *Ngày mượn, Ngày trả* theo cách mở lịch và chọn ngày trên đó.

**Ví dụ 2.** Một số CSDL trực tuyến cũng có các biểu mẫu cho sẵn phục vụ người dùng, như biểu mẫu khai báo y tế mà người dân có thể điền thông tin trên điện thoại di động.

## 4 Thực hành tạo biểu mẫu và cập nhật dữ liệu

### Nhiệm vụ 1. Thầy, cô giáo đã dựng sẵn 3 bảng: **SÁCH, NGƯỜI ĐỌC, MƯỢN-TRẢ** cùng một vài biểu mẫu trong CSDL Thư viện (tạo bằng Access). Em hãy sử dụng biểu mẫu **NHẬP DỮ LIỆU MƯỢN-TRẢ SÁCH** đã có để nhập 3 bản ghi mới cho bảng **MƯỢN-TRẢ**.

#### Hướng dẫn thực hiện:
*   **Bước 1.** Kích hoạt Microsoft Access.
*   **Bước 2.** Mở CSDL Thư viện, chọn biểu mẫu **NHẬP DỮ LIỆU MƯỢN-TRẢ SÁCH**.
*   **Bước 3.** Trên biểu mẫu vừa mở, hãy nhập ít nhất 3 bản ghi.
*   **Bước 4.** Tìm và mở biểu mẫu **XEM THÔNG TIN MƯỢN-TRẢ SÁCH** để kiểm tra xem những bản ghi nhập vào ở Bước 3 đã xuất hiện trong bảng **MƯỢN-TRẢ** chưa.
*   **Bước 5.** Kết thúc phiên làm việc với CSDL Thư viện, trong bảng chọn **File** chọn nút lệnh **Close** để đóng CSDL này.

### Nhiệm vụ 2. Khám phá cách dùng công cụ tạo biểu mẫu trong Access.

#### Hướng dẫn thực hiện:
*   **Bước 1.** Chọn mở CSDL HỌC SINH 11. Mở bảng HỌC SINH 11.

Bước 2. Nháy chuột vào Create để xuất hiện các công cụ tạo lập biểu mẫu.
Bước 3. Chọn và khám phá công cụ Form Wizard: Chọn các trường cho biểu mẫu, kiểu cho biểu mẫu, đặt tên biểu mẫu, chọn Finish.
Bước 4. Đóng CSDL HỌC SINH 11 để kết thúc phiên làm việc với CSDL này.

## Luyện tập

Nếu là người xây dựng một CSDL quản lí học sinh khối 11 của trường mình, em sẽ xây dựng những biểu mẫu nào? Mỗi biểu mẫu em định thiết kế sẽ có chức năng nào và đem lại thuận lợi gì, cho ai?

Trong các câu sau, những câu nào đúng?
a) Mỗi biểu mẫu đều được dùng chung cho tất cả mọi người sử dụng CSDL.
b) Mỗi biểu mẫu là một cửa sổ cho người dùng xem toàn bộ thông tin trong một bảng của CSDL.
c) Khi cập nhật dữ liệu, cần sử dụng biểu mẫu vì có thể đảm bảo được rằng buộc khoá và khoá ngoài, tránh được nhiều sai nhầm về dữ liệu.
d) Biểu mẫu là một giao diện được thiết kế để kiểm soát các truy cập của người dùng đến dữ liệu trong CSDL.

## Tóm tắt bài học

*   **Biểu mẫu** là một loại giao diện cho người dùng CSDL tương tác với dữ liệu nguồn trong việc xem và cập nhật dữ liệu.
*   **Biểu mẫu** đem lại sự thuận tiện cho các nhóm người dùng làm việc với CSDL và giúp hạn chế những vi phạm trong cập nhật nhằm tăng cường sự đảm bảo tính đúng đắn của dữ liệu.
