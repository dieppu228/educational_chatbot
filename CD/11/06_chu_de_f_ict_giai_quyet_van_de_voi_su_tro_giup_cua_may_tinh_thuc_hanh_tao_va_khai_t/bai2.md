# Bài 2: TẠO BẢNG TRONG CƠ SỞ DỮ LIỆU

Học xong bài này, em sẽ:
* Biết được cách tạo bảng theo thiết kế.
* Biết được sơ bộ cách thiết lập một số thuộc tính kiểu dữ liệu thường dùng.
* Tạo được một số bảng CSDL.

Thư viện trường em lưu trữ những gì và hàng ngày phục vụ những ai?

## 1. Các bảng trong cơ sở dữ liệu thư viện trường
### a) Các cột trong bảng

Một bảng CSDL có nhiều cột. Mỗi cột chứa dữ liệu thuộc một kiểu nhất định. Cần thiết lập kiểu dữ liệu cho mỗi cột trong bảng phù hợp với thực tế và mục đích sử dụng.

## Thiết kế các bảng

Trong tin học, **logic nghiệp vụ** (*Business Logic*) hàm ý các quy tắc nghiệp vụ trong thế giới thực và người thiết kế CSDL cần dựa vào đó xác định cách thu thập, lưu trữ và thao tác dữ liệu.

Hoạt động hằng ngày của thư viện trường liên quan đến kho sách, đến bạn đọc là các học sinh trong trường, đến các giao dịch mượn, trả sách. CSDL thư viện đơn giản nhất gồm 3 bảng tương ứng: *Sách, Bạn Đọc, Mượn-Trả sách*.

Bảng *Mượn-Trả* là bảng nối, một kiểu bảng riêng, sẽ được thiết kế sau. Dưới đây trình bày chi tiết về bảng *Sách* và bảng *Bạn Đọc*.

Bảng *Sách* gồm các cột và kiểu dữ liệu tương ứng, ví dụ như sau:

### Các trường dữ liệu trong bảng Sách
*   **Mã sách**: Kiểu dữ liệu Short Text. Chú thích: Do thư viện đặt, là khoá chính; có thể hạn chế độ dài.
*   **Tên sách**: Kiểu dữ liệu Short Text. Chú thích: Cần có.
*   **Sẵn có**: Kiểu dữ liệu Yes/No. Chú thích: Cần có.
*   **Số trang**: Kiểu dữ liệu Number. Chú thích: Tuỳ chọn.
*   **Tác giả**: Kiểu dữ liệu Short Text. Chú thích: Tuỳ chọn.
*   **Loại sách**: Kiểu dữ liệu Short Text. Chú thích: Tuỳ chọn.

Có thể thêm một số cột nữa cho bảng *Sách* tuỳ theo yêu cầu quản lí và quy mô kho sách. Ví dụ: ngày nhập kho sách; phân loại sách giáo khoa, sách hỗ trợ học tập và giảng dạy (sách bài tập, sách giáo viên,...). Với mục đích minh hoạ, ta thêm cột *Loại sách*, phân loại sách Tin học “**TH**” và còn lại là sách “**Khác**”.

Bảng Bạn Đọc gồm các cột và kiểu dữ liệu tương ứng, ví dụ như Bảng 3 sau đây:

Bảng 3. Các trường dữ liệu trong bảng Bạn Đọc
*   **1. Số thẻ**: Kiểu dữ liệu: Short Text, Chú thích: Do thư viện đặt, là khoá chính; có thể hạn chế độ dài.
*   **2. Mã Học sinh**: Kiểu dữ liệu: Short Text, Chú thích: Do phòng giáo vụ đặt; có thể hạn chế độ dài.
*   **3. Họ và đệm**: Kiểu dữ liệu: Short Text, Chú thích: Cần có; có thể hạn chế độ dài.
*   **4. Tên**: Kiểu dữ liệu: Short Text, Chú thích: Cần có; có thể hạn chế độ dài.
*   **5. Ngày sinh**: Kiểu dữ liệu: Date/Time, Chú thích: Tuỳ chọn.
*   **6. Giới tính**: Kiểu dữ liệu: Yes/No, Chú thích: Tuỳ chọn; Nữ = Yes.
*   **7. Số điện thoại**: Kiểu dữ liệu: Short Text, Chú thích: Tuỳ chọn; có thể hạn chế độ dài.
*   **8. Email**: Kiểu dữ liệu: Short Text, Chú thích: Tuỳ chọn; có thể hạn chế độ dài.
*   **9. Ảnh**: Kiểu dữ liệu: Attachement, Chú thích: Đính kèm; Tuỳ chọn.

Hình 2 minh hoạ bảng Bạn Đọc với một số bản ghi. Có thể thêm một số cột nữa cho bảng Bạn Đọc tuỳ theo yêu cầu quản lí và quy mô tập thể bạn đọc. Ví dụ: ngày bắt đầu trở thành bạn đọc; là học sinh, giáo viên hay cán bộ nhà trường,...

## Nhận xét:

Để phân biệt đối tượng bạn đọc, có thể sử dụng mã số thẻ bạn đọc. Ví dụ, số thẻ bắt đầu bằng “HS-” nghĩa là học sinh, bắt đầu bằng “GV-” nghĩa là giáo viên. Tương tự, có thể sử dụng mã số sách để phân loại sách. Cách làm này thích hợp cho thư viện quy mô nhỏ và dễ nhận biết, dễ nhớ với con người.

Với thư viện quy mô lớn, có yêu cầu quản lí nâng cao hơn và dịch vụ phong phú hơn cần xử lí bằng máy tính thì sẽ có những bất tiện. Việc trích lấy ra các thông tin

“ngầm” trong mã số để phân tích số liệu thống kê theo đối tượng bạn đọc, theo phân loại sách,... sẽ phức tạp hơn. Giải pháp thích hợp là thêm cột **Phân loại** và mã hoá rõ ràng cách phân loại.

### c) Hướng dẫn tạo bảng theo thiết kế

Xét hai trường hợp:
*   CSDL trống mới tạo sẽ có sẵn ngay một bảng tên là **Table1** theo mặc định.
*   CSDL đang làm việc: Nháy chuột chọn **Create\Table** sẽ tạo thêm một bảng mới tên là **Table1**.

Access sẽ yêu cầu đổi tên tạm **Table1** thành tên mới khi ghi lưu bảng mới tạo hoặc ta có thể gõ nhập luôn tên mới cho bảng trước khi nháy lệnh **Create**. Nên chọn tên gợi nhớ nội dung bảng chứa dữ liệu gì.

## Thiết lập kiểu dữ liệu cho mỗi trường và các thuộc tính chi tiết

### Thao tác thiết kế các cột trong bảng

Nháy chuột vào ô vuông đầu mút trái cạnh tên trường sẽ đánh dấu chọn cả hàng ngang (tức là cột có tên đó trong bảng dữ liệu). Sau khi đã chọn, có thể:

*   Xóa hay chèn thêm trường mới kế bên: Dùng nút lệnh **Delete Rows** hay **Insert Rows** trong vùng nút lệnh.
*   Đặt làm trường khóa chính của bảng hay gỡ bỏ không còn là khóa chính bằng nút lệnh **Primary Key** hình chìa khóa trong vùng nút lệnh.

Mẹo: Nháy chuột phải vào ô vuông đầu mút trái cạnh tên trường sẽ xuất hiện bảng chọn nổi lên với các lệnh tương tự.

*   Nháy chuột vào tên trường để gõ nhập tên mới nếu muốn đổi tên.

Mở bảng trong khung nhìn thiết kế và nhập lần lượt các tên trường trong cột **Field Name**. Nên giữ nguyên cột **ID** do Access tự động tạo ra. Cột **Data Type** để chọn kiểu dữ liệu của trường.

*   **Bước 1**. Nháy chuột vào ô tên kiểu dữ liệu (cột **Data Type**), nháy dấu trỏ xuống ở đầu mút phải sẽ thả xuống danh sách để chọn các kiểu dữ liệu.
*   **Bước 2**. Chọn một kiểu dữ liệu (bằng tiếng Anh) thích hợp trong danh sách.
Vùng **Field Properties** bên dưới để xác định chi tiết các thuộc tính của kiểu dữ liệu đã chọn. Cột đầu tiên là danh sách các tên thuộc tính: **Field Size, Format, Input Mask,...**. Cột kế tiếp xác định cụ thể giá trị của thuộc tính.
*   **Bước 3**. Thiết lập các chi tiết thuộc tính của trường đã chọn:
    1) Nháy chuột chọn một thuộc tính (một dòng) sẽ xuất hiện dấu trỏ xuống ở đầu mút phải.
    2) Nháy dấu trỏ xuống để thả danh sách chọn thiết lập chi tiết cho thuộc tính đó.
Các trường **Mã sách, Số thẻ** được dự kiến làm khoá chính trong các bảng tương ứng. Theo mặc định, trường khoá chính sẽ được xác định một số thuộc tính như sau: **Required: Yes; Indexed: Yes (No Duplicates)**.

Thuộc tính **Indexed** (được lập chỉ mục) giúp tìm kiếm nhanh hơn. Một việc hay làm là tìm kiếm bạn đọc theo tên. Do đó với cột **Tên** trong bảng **Bạn Đọc** nên xác định thuộc tính **Indexed**. Tuy nhiên, việc hai người trùng tên có thể xảy ra, nên ta phải chọn **Indexed: Yes (Duplicates OK)**.

Cũng cần xác định thuộc tính **Format** của trường để hiển thị dữ liệu dưới dạng quen thuộc dễ xem và dễ gõ nhập dữ liệu mới. Ví dụ, trong bảng **Bạn Đọc** có trường **Ngày sinh**, kiểu dữ liệu **Date/Time** có các lựa chọn: **General Date, Long Date, Medium Date, Short Date**. Hãy chọn sao cho phù hợp.

# Bài 6: Thực hành làm quen với Microsoft Access

## Nhiệm vụ 1. Tạo CSDL bằng khuôn mẫu
*   a) Tạo một CSDL theo mẫu **Students**. Mở bảng Students và chuyển sang khung nhìn thiết kế.
*   b) Thử ghi lưu CSDL vừa tạo ở câu a) về máy tính cá nhân với một tên tuỳ ý.

## Nhiệm vụ 2. Khám phá biểu mẫu và thử nhập dữ liệu từ biểu mẫu
*   a) Mở biểu mẫu **Student List**, chuyển sang khung nhìn **Form View** (nếu cần thiết).
*   b) Nhập dữ liệu tuỳ ý cho vài bản ghi và một vài trường:
    *   Trường với kiểu dữ liệu **Date/Time**, chú ý cách Access hỗ trợ dùng lịch để chọn ngày tháng.
    *   Trường **Level**, chú ý biểu mẫu sẽ thả xuống danh sách để chọn.
*   c) Mở bảng Students để xem kết quả nhập dữ liệu.

## Nhiệm vụ 3. Xem các thuộc tính chi tiết của một cột
*   a) Mở bảng Students trong khung nhìn thiết kế, chú ý ý vùng **Field Properties** hiển thị các thuộc tính chi tiết hơn.
*   b) Nháy chuột vào **Data Type** của trường **Student ID** và xem các thuộc tính.
*   c) Làm tương tự với trường **Data of Birth**.

## Nhiệm vụ 4. Khám phá các thao tác thiết kế cột trong khung nhìn thiết kế bảng Students
*   a) Thử xoá một trường, ví dụ **Company, Room,...**
*   b) Thử chèn thêm một trường mới vào chỗ vừa xoá bớt xong.
*   c) Thử đổi tên một vài trường, ví dụ **First Name** thành **Tên**, **Last Name** thành **Họ**; đổi tên trường có kiểu dữ liệu **Date/Time** thành **Ngày sinh**.

## Luyện tập
Theo em, khi nào nên tạo mới một CSDL Access từ khuôn mẫu có sẵn?

*   Câu 1. Vùng điều hướng trong cửa sổ làm việc của Access hiển thị những gì?
*   Câu 2. Có thể mở bảng CSDL dưới những khung nhìn nào?
*   Câu 3. Khung nhìn thiết kế bảng gồm mấy phần? Từng phần hiển thị những gì?

## Tóm tắt bài học
*   Có thể mở một bảng (biểu mẫu, truy vấn, báo cáo) dưới các khung nhìn khác nhau trong vùng làm việc của Access tuỳ theo việc ta muốn làm.
*   Khung nhìn thiết kế bảng chia làm hai phần: nửa trên là danh sách tên trường (**Field Name**) kèm kiểu dữ liệu (**Data Type**), nửa dưới hiển thị các thuộc tính chi tiết của trường ta đang thiết kế, chỉnh sửa.
```

## Gõ nhập dữ liệu vào bảng để kiểm tra thiết kế

Sau khi thiết kế xong bảng, ghi lưu và chuyển về khung nhìn bảng dữ liệu, ta có thể bắt đầu nhập dữ liệu vào bảng. Việc gõ nhập dữ liệu được thực hiện theo từng ô. Access tự động lưu kết quả nhập dữ liệu khi kết thúc một bản ghi và chuyển sang bản ghi tiếp theo, không cần nháy chuột vào biểu tượng Save.

*Chú ý*: Trong thực tế, người ta thường thiết kế để nhập dữ liệu cho CSDL qua biểu mẫu để kiểm soát một số ràng buộc dữ liệu.

## Chuyển quan hệ "nhiều – nhiều" thành quan hệ "một – nhiều"

Nhật kí giao dịch hằng ngày phản ánh mối quan hệ giữa hai (hoặc nhiều) đối tượng liên quan trong hoạt động kinh doanh hay dịch vụ. Thư viện cần ghi lại các giao dịch mượn trả sách trong một thời gian, ví dụ một năm học. Thực tế cho thấy mỗi học sinh đã từng mượn nhiều cuốn sách và mỗi cuốn sách đã từng được nhiều học sinh mượn. Đây là quan hệ nhiều – nhiều ($\infty – \infty$). Trong Access nói riêng và CSDL quan hệ nói chung giữa hai bảng chỉ có mối quan hệ một – một ($1 – 1$) hoặc một – nhiều ($1 – \infty$).

Ta tạo bảng thứ ba đặt tên là *Mượn-Trả*, là bảng nối giữa *Bạn Đọc* và *Sách* để chuyển quan hệ $\infty – \infty$ thành hai quan hệ $1 – \infty$. Trong bảng nối sẽ có hai cột ứng với hai khoá chính của bảng *Bạn Đọc* và bảng *Sách*. Đó là các **khoá ngoài**.

Bảng *Mượn-Trả* gồm các cột và kiểu dữ liệu tương ứng, ví dụ như Bảng 4 sau đây:

Tuỳ theo yêu cầu sử dụng, có thể thêm cột cho bảng *Mượn-Trả*.

## Thực hành tạo bảng trong CSDL
### Nhiệm vụ 1. Tạo bảng Sách theo thiết kế và thử nhập dữ liệu
#### a) Tạo bảng mới. Mở bảng trong khung nhìn thiết kế, giữ nguyên trường ID, thêm các trường mới và xác định kiểu dữ liệu, thiết lập thuộc tính của trường dữ liệu.

#### b) Chuyển sang khung nhìn bảng dữ liệu, nhập dữ liệu cho một vài cột, vài hàng.
#### c) Chuyển sang khung nhìn thiết kế, bỏ chọn khoá chính là *ID*; chọn *Mã sách* làm khoá chính; ghi lưu thay đổi thiết kế.
Chú ý: Kiểu dữ liệu **Number** cho cột *Số trang* nên được xác định chi tiết hơn: *Field Size* là *Integer*. Nên hạn chế độ dài một số trường kiểu **Short text**, ví dụ hạn chế độ dài *Mã sách*: 15; *Tác giả*: 127.

### Nhiệm vụ 2. Tạo bảng Bạn Đọc theo thiết kế và thử nhập dữ liệu
*   Các bước thực hành tương tự như Bài 1.
*   Chú ý:
    1.  Nên hạn chế độ dài một số trường kiểu **Short text**, ví dụ hạn chế độ dài *Số thẻ, Mã học sinh*: 15; *Họ và đệm*: 63; *Tên*: 15.
    2.  Chọn *Số thẻ* làm khoá chính của bảng thay cho trường *ID* mặc định.
    3.  Cột *Tên* nên chọn thuộc tính **Indexed** là “*Yes (Duplicates OK)*”.
    4.  Cột *Ngày sinh* nên chọn thuộc tính **Format** phù hợp, ví dụ *Short Date*.
    5.  Nhập một số bạn đọc không là học sinh, ví dụ có *Số thẻ* bắt đầu bằng “GV”.

## Luyện tập
*   Câu 1. Học sinh là trung tâm của hoạt động giáo dục trong nhà trường. Em hãy thiết kế bảng dữ liệu *Học sinh* cho CSDL của trường em.
*   Câu 2. Theo em, trong bảng *Bạn đọc*, những trường dữ liệu nào hoàn toàn giống như trong bảng *Học sinh*.

*   Câu 1. Để tạo một bảng mới cần thao tác như thế nào?
*   Câu 2. Để tạo cột và xác định kiểu dữ liệu cho cột cần thao tác như thế nào?
*   Câu 3. Để chọn một cột làm khoá chính cần làm gì?

## Tóm tắt bài học
*   Các việc cần làm sau khi tạo bảng mới:
    *   Mở khung nhìn thiết kế để nhập các tên cột, chọn kiểu dữ liệu cho cột.
    *   Xác định một số thuộc tính chi tiết quan trọng của cột trong trường hợp cần thiết: *Field Size, Required, Indexed* và *Yes/No Duplicates,...*
    *   Chọn cột làm khoá chính của bảng.
    *   Chuyển sang khung nhìn bảng dữ liệu và thử nhập dữ liệu để kiểm tra.
