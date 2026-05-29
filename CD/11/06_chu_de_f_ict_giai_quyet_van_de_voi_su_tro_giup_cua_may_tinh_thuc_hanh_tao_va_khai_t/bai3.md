# Bài 3: LIÊN KẾT CÁC BẢNG TRONG CƠ SỞ DỮ LIỆU

Học xong bài này, em sẽ:
*   Biết được cách thiết lập đúng đắn mối quan hệ giữa các bảng trong một CSDL để kết nối dữ liệu giữa hai bản ghi từ hai bảng.
*   Tạo được CSDL có nhiều bảng.
*   Thiết lập được quan hệ giữa các bảng.

Khi một bạn đọc mượn sách, thủ thư cần ghi lại những thông tin gì? Có một bảng nào trong CSDL chứa đầy đủ những thông tin này hay không?

## 1) Thiết lập mối quan hệ giữa hai bảng
### a) Các lựa chọn kết nối dữ liệu
Thiết lập mối quan hệ giữa hai bảng nhằm mục đích nối (join) dữ liệu giữa hai bản ghi tương ứng trong mỗi bảng. Access sẽ so khớp giá trị của hai trường được liên kết khi truy vấn dữ liệu hay kiểm tra hợp lệ khi nhập dữ liệu. Ví dụ, không thể có một người mượn mà chưa có thẻ thư viện; không thể mượn cuốn sách còn chưa có trong kho sách.

Quan hệ 1-∞ phổ biến nhất giữa hai bảng có ba lựa chọn thuộc tính của phép nối dữ liệu (**Join Properties**) như trong Hình 1. Khi truy vấn lấy dữ liệu có yêu cầu nối các bản ghi từ hai bảng thì trong số các bản ghi đã thoả mãn điều kiện cần biết cách “nối” cụ thể.

1: Chỉ nối các bản ghi nếu các giá trị trường được kết nối trùng khớp nhau. Đây là phép **nối trong** (**Inner join**).
2: Lấy tất cả các bản ghi trong bảng bên trái nhưng chỉ nối với các bản ghi của bảng bên phải khớp giá trị trong trường được kết nối. Đây là phép **nối ngoài bên trái** (**Left outer join**).

3: Ngược với tuỳ chọn 2:, lấy tất cả các bản ghi trong bảng bên phải nhưng chỉ nối với các bản ghi của bảng bên trái khớp giá trị trong trường được kết nối. Đây là phép **nối ngoại bên phải** (*Right outer join*).
Access đánh dấu lựa chọn 1: theo mặc định.
### b) Thao tác thiết lập, chỉnh sửa, xoá mối quan hệ giữa hai bảng

Chọn **Database Tools\\Relationships** để mở vùng làm việc với các mối quan hệ. Access hiển thị trực quan mối quan hệ giữa hai bảng bằng một đoạn thẳng nối hai bảng, ghi kèm các cặp số 1 – 1 hay 1 – ∞ ở hai đầu đoạn nối nếu đã được thiết lập rõ ràng. Chú ý rằng một bảng có thể liên kết với nhiều bảng khác.

Quy trình thiết lập mối quan hệ giữa hai bảng có thể chia làm 3 bước lớn.

Bước 1. Đưa hộp thể hiện mỗi bảng vào vùng làm việc với các mối quan hệ (nếu trong đó còn chưa nhìn thấy bảng ta muốn):
*   Nháy nút lệnh **Show Table**. Hộp thoại Show Table xuất hiện.
*   Nháy đúp chuột lên tên bảng: Hộp thể hiện bảng sẽ xuất hiện.

Bước 2. Tạo quan hệ giữa hai bảng:
*   Kéo thả chuột từ trường khoá ngoại trong bảng con vào trường khoá chính trong bảng mẹ; hộp thoại **Edit Relationships** xuất hiện.
*   Đánh dấu hộp kiểm **Enforce Referential Integrity** (đảm bảo toàn vẹn tham chiếu) và chọn Create hay OK.

#### Xác định các lựa chọn liên kết dữ liệu
* Bước 3. Xác định các lựa chọn liên kết dữ liệu:
  1) Nháy nút **Join Type** để mở hộp thoại Join Properties (nếu chưa xuất hiện) để chọn thuộc tính cho phép nối dữ liệu thực thi mối quan hệ này.
  2) Để nguyên như mặc định hoặc đánh dấu chọn thuộc tính kết nối đúng yêu cầu.
### Chỉnh sửa mối quan hệ
1) Chọn mối quan hệ bằng cách nháy chuột lên đường nối hai bảng.
2) Nháy nút lệnh **Edit Relationship**.
### Xoá mối quan hệ
Nháy chuột chọn mối quan hệ, nhấn phím **Delete**.
*Chú ý*: Nháy chuột phải lên đường nối hai bảng cũng xuất hiện bảng chọn nối lên có hai lệnh **Edit Relationship** và **Delete**.

## Cột dữ liệu từ tra cứu
Sử dụng cột dữ liệu từ tra cứu giúp người dùng có thể chọn mục dữ liệu từ một danh sách thay cho gõ nhập. Việc nhập dữ liệu sẽ nhanh hơn và đảm bảo toàn vẹn tham chiếu (Hình 3).
### Hướng dẫn thao tác
Access có trình tiện ích **Lookup Wizard** giúp thiết lập mối quan hệ khoá ngoài và khoá chính giữa hai bảng (quan hệ ∞ – 1) để cho phép nhập dữ liệu bằng cách chọn từ danh sách thả xuống.
Ta sẽ thiết lập cột **Số thẻ** trong bảng **Mượn-Trả** thành cột dữ liệu từ tra cứu.
1) Mở bảng **Mượn-Trả** trong khung nhìn thiết kế.
2) Thiết lập lại Data Type của trường **Số thẻ**: Nháy dấu trỏ xuống để thả xuống danh sách chọn.
3) Nháy chọn **Lookup Wizard** (ở dòng cuối cùng) sẽ làm xuất hiện một loạt hộp thoại để đánh dấu các lựa chọn.
4) Hộp thoại thứ nhất (Hình 4a): Đánh dấu chọn "I want the lookup field to get the values from another table or query"; chọn Next.

* 5) Hộp thoại thứ hai:
  Chọn bảng hay truy vấn làm nguồn để tra cứu dữ liệu. Trong ví dụ này, đánh dấu chọn bảng **Bạn Đọc**; chọn **Next**.
* 6) Hộp thoại thứ ba:
  Chọn các trường dữ liệu trong bảng (hay truy vấn) vừa chọn. Trong ví dụ này, đánh dấu chọn trường **Số thẻ** (của bảng **Bạn Đọc**); Nháy dấu mũi tên “**>**” để chuyển nó sang *Selected Fields*; chọn **Next**.
* 7) Hộp thoại thứ tư để chọn trường muốn sắp xếp để tiện tra cứu. Trong ví dụ này, đó vẫn là trường **Số thẻ** vừa chọn; chọn trường **Số thẻ** và chọn **Next**.
* 8) Hộp thoại thứ năm:
  Đặt tên cho trường lookup. Ta giữ nguyên tên là **Số thẻ**; chọn **Finish**.

Quan sát kết quả: Mở bảng trong khung nhìn bảng dữ liệu sẽ thấy có mũi tên trỏ xuống khi chọn ô để nhập dữ liệu cho trường **Số thẻ**. Từ đây thay vì gõ nhập có thể chọn từ danh sách tra cứu.

## Thiết lập đảm bảo toàn vẹn tham chiếu

* Nháy chọn **Database Tools\Relationships** sẽ thấy có đường nối giữa hai bảng **Bạn đọc** và **Mượn-Trả** hiển thị trực quan mối quan hệ tra cứu vừa thiết lập.
* Nháy chuột phải lên đường nối này; hộp thoại *Edit Relationships* xuất hiện. Đánh dấu hộp kiểm *Enforce Referential Integrity* và chọn **OK**.

## Thực hành tạo liên kết giữa các bảng trong CSDL

### Nhiệm vụ 1. Tạo bảng Mượn-Trả theo thiết kế và thử nhập dữ liệu

Các bước tạo bảng tương tự như trong bài học trước.

### Chú ý:
1.  Vẫn dùng khóa chính là **ID** như **Access** đã chọn mặc định.
2.  Các cột **Ngày mượn**, **Ngày Trả** nên chọn thuộc tính **Format** phù hợp, ví dụ **Short Date**.
3.  Nên hạn chế độ dài của các trường **Số thẻ**, **Mã sách** giống như ở các bảng **Bạn Đọc**, **Sách**.

### Nhiệm vụ 2. Thiết lập mối quan hệ và xác định thuộc tính kết nối dữ liệu giữa các bảng
1.  Thiết lập mối quan hệ **1 – ∞** từ bảng **Sách** và từ bảng **Bạn Đọc** tới bảng **Mượn-Trả** theo hướng dẫn trong mục “**Thao tác thiết lập, chỉnh sửa, xoá mối quan hệ giữa hai bảng**”.
2.  Thiết lập cột **Số thẻ** và cột **Mã sách** thành kiểu dữ liệu tra cứu.

### Chú ý:
Có thể phải xoá kết quả của yêu cầu 1 và sau đó thiết lập lại thành cột tra cứu.

Theo em, nếu như **CSDL** của trường có bảng **Học sinh** và đã thiết lập quan hệ 1 – 1 giữa hai bảng **Bạn Đọc** và **Học sinh** thì có thể thiết lập kiểu dữ liệu tra cứu để không phải gõ nhập lại dữ liệu những cột nào trong bảng **Bạn Đọc**.

## Luyện tập
Câu 1. Cần mở cửa sổ làm việc nào để thiết lập, chỉnh sửa mối quan hệ giữa các bảng **CSDL**?
Câu 2. Để thiết lập kiểu dữ liệu từ tra cứu cần thao tác như thế nào?

## Tóm tắt bài học

*   Các thao tác thiết lập, chỉnh sửa, xoá mối quan hệ giữa hai bảng trong **CSDL** bắt đầu bằng chọn **Database Tools\Relationships** để mở vùng làm việc với các mối quan hệ.
*   Thiết lập kiểu dữ liệu từ tra cứu sẽ đảm bảo **toàn vẹn tham chiếu**.
*   Kéo thả trường **khóa ngoại** của bảng con vào trường **khóa chính** của bảng mẹ để tạo quan hệ giữa hai bảng.
*   Chọn thuộc tính cho phép nối dữ liệu trong hộp thoại **Join Properties**.
