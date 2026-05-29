# Bài 1: LÀM QUEN VỚI MICROSOFT ACCESS

Học xong bài này, em sẽ:
* Biết được một số đặc điểm của phần mềm hệ quản trị cơ sở dữ liệu quan hệ **Microsoft Access** và một số thành phần chính trong cửa sổ làm việc của nó.
* Biết được một số kiểu dữ liệu trường của các bản ghi trong **Microsoft Access** và cách thiết lập kiểu dữ liệu trường.
* Tạo lập được một cơ sở dữ liệu đơn giản từ khuôn mẫu **Microsoft Access** cho trước và biết cách nhập dữ liệu vào một bảng.

Một doanh nghiệp nhỏ cần quản lí kho hàng bằng máy tính. Theo em, nên chọn dùng phần mềm ứng dụng nào? Tại sao?

## 1. Giới thiệu Microsoft Access

**Microsoft Access** (gọi tắt là Access), là phần mềm hệ quản trị CSDL phù hợp với các cơ quan, doanh nghiệp nhỏ hay người dùng cá nhân. Cửa sổ làm việc của Access có giao diện tương tự như Word, Excel và cũng áp dụng các khái niệm, cách tổ chức cũng những thao tác tương tự như các ứng dụng trong bộ phận mềm văn phòng Microsoft Office.

### a) Vùng nút lệnh

Ở phía trên cùng là **vùng nút lệnh** gồm nhiều dải lệnh nằm đè lên nhau. Các thẻ (tab) để mở các dải lệnh **File, Home, Create, External Data, Database Tools**,... là dải lệnh **Home** hay dùng nhất với các nhóm lệnh **Views, Clipboard, Sort & Filter, Records**.

Access làm thay đổi các thành phần trong vùng nút lệnh tuỳ theo ta đang làm việc với đối tượng cụ thể nào ở trong vùng làm việc. Vùng nút lệnh hiển thị sẵn sàng các nút lệnh thường dùng vào lúc ấy.

### Vùng điều hướng

Vùng điều hướng hiển thị các đối tượng trong một CSDL. Mỗi đối tượng được thể hiện dưới dạng một biểu tượng kèm với tên của nó, ví dụ: là bảng, là truy vấn, là biểu mẫu, là báo cáo.

### Vùng làm việc

Nháy đúp chuột vào biểu tượng của đối tượng trong vùng điều hướng sẽ làm hiển thị nội dung của đối tượng đó trong vùng làm việc. Có thể mở đồng thời nhiều đối tượng trong vùng làm việc. Mỗi đối tượng sẽ có một thẻ ở bên trên cho thấy tên của nó. Nháy chuột chọn thẻ sẽ làm hiển thị nội dung của đối tượng đã chọn. Để đóng đối tượng, nháy chuột vào dấu X ở góc trên bên phải màn hình.

### Nhận xét và quy ước chung:

*   Thường có vài cách thao tác khác nhau để đạt được cùng một kết quả. Cách được coi là **“chính thống”** khi mới làm quen với phần mềm là bắt đầu từ một nút lệnh trong một dải lệnh ở vùng làm việc.
*   Quy ước: Trong hướng dẫn thao tác sẽ viết ngắn gọn cho dễ nhớ. Ví dụ, viết `Create\Table...` nghĩa là “nháy chuột vào thẻ **Create** sẽ thấy nút lệnh **Table** và tiếp tục nháy chuột chọn **Table**...”.
*   Thao tác nhanh: Khi đã quen dùng, nên ưu tiên nháy chuột phải và sử dụng bảng chọn nổi lên (context menu). Ở đây có các lựa chọn thích hợp với bối cảnh lúc đó, rất tiện chọn lệnh tiếp theo.

### d) Thay đổi khung nhìn

Một đối tượng trong CSDL Access có thể mở dưới các khung nhìn (View) khác nhau. Mỗi khung nhìn phục vụ tốt nhất cho một loại công việc. Để thay đổi khung nhìn cho một đối tượng, có thể thực hiện một trong các cách sau đây:
*   **Cách 1**: Nháy chuột vào nút lệnh View để hiển thị danh sách chọn khung nhìn, sau đó chọn khung nhìn thích hợp.
*   **Cách 2**: Nháy chuột vào các nút lệnh chọn khung nhìn có sẵn ở góc phải dưới của cửa sổ Access.
*   **Cách 3**: (Dùng bảng chọn nổi lên) Nháy chuột phải lên thẻ của đối tượng đang mở và chọn khung nhìn thích hợp.

## 2) Cơ sở dữ liệu trong Access

Một CSDL Access được lưu trong máy tính thành một tệp có đuôi tên tệp là “.accdb”. Mỗi cửa sổ Access làm việc với một CSDL.

Có thể tạo một CSDL mới trong Access bằng hai cách khác nhau: từ khuôn mẫu cho trước hoặc từ CSDL trống (Blank Database). Đối với CSDL trống, ta phải tự làm tất cả các công việc như: tạo từng bảng theo thiết kế, nhập dữ liệu và xây dựng các biểu mẫu, báo cáo, truy vấn,...

Nếu sử dụng khuôn mẫu, Access giúp ta rất nhiều vì đã làm sẵn một số khung bảng, biểu mẫu, báo cáo,... Nói “khung” hàm ý chưa có dữ liệu. Chỉ cần nhập dữ liệu là CSDL đã sẵn sàng để sử dụng. Nếu thấy những điểm chưa hoàn toàn phù hợp với nhu cầu sử dụng, có thể chỉnh sửa thiết kế các khung bảng, biểu mẫu, báo cáo,... theo ý muốn. Access đã làm sẵn khá nhiều khuôn mẫu để lựa chọn.

## 3) Tạo mới cơ sở dữ liệu

### a) Tạo cơ sở dữ liệu mới từ Blank database

*   **Bước 1**. Khởi chạy Access, chọn New hoặc từ cửa sổ làm việc của Access, chọn **File\New**.
*   **Bước 2**. Nháy chuột chọn **Blank desktop database**, một cửa sổ Access mở ra.
*   **Bước 3**. Đổi tên tệp thay cho tên mặc định ở ô File Name và xác định thư mục nơi chứa tệp CSDL. Sau đó nhấn **Create**.

### Tạo CSDL từ khuôn mẫu

Tạo mới một CSDL từ khuôn mẫu chỉ khác tạo CSDL trống ở Bước 2. Thay vì chọn **Blank desktop database**, cần tìm và chọn khuôn mẫu mong muốn trước khi thực hiện Bước 3. Chi tiết Bước 2 như sau:

*   Nếu thấy khuôn mẫu mong muốn, nháy chọn nó; một cửa sổ Access sẽ mở, thực hiện tiếp Bước 3 như Mục a.
*   Nếu chưa nhìn thấy khuôn mẫu mong muốn trên máy tính của mình, cần tìm kiếm nó bằng cách sử dụng ô tìm kiếm (Search for online templates). Sau đó chọn tải về và mở ra.

## Bảng và các kiểu dữ liệu cột

Có hai khung nhìn bảng là khung nhìn thiết kế (Design View) và khung nhìn bảng dữ liệu (Datasheet View).

Trong khung nhìn bảng dữ liệu, mỗi bản ghi là một hàng trong bảng, mỗi cột trong bảng là một trường của bản ghi, chứa dữ liệu thuộc một kiểu nào đó. Mỗi kiểu dữ liệu có các thuộc tính nhất định. Cần thiết lập kiểu dữ liệu cho mỗi cột trong bảng phù hợp với thực tế và mục đích sử dụng.

### Hướng dẫn thao tác khám phá trong khung nhìn thiết kế bảng

#### Các cột trong bảng

Access luôn mặc định thiết kế trường dữ liệu đầu tiên tên là ID và có kiểu dữ liệu là **AutoNumber**. Access mặc định chọn trường ID là khoá chính của bảng và hiển thị biểu tượng chìa khoá tại đầu mút trái cạnh tên trường. Sau này, ta có thể chọn trường khác làm khoá chính, theo đúng thiết kế thay cho trường ID mặc định.

Mở bảng *Students* trong khung nhìn thiết kế để thao tác khám phá. Khung nhìn thiết kế bảng chia làm hai phần. Nửa trên là danh sách tên trường (Field Name) kèm kiểu dữ liệu (Data Type). Nháy chuột chọn Data Type cụ thể cho một trường thì nửa dưới hiển thị các thuộc tính chi tiết hơn của kiểu dữ liệu trong trường đó, gọi là thuộc tính trường (Field Properties). Minh hoạ các thuộc tính chi tiết của trường *Date of Birth*.

```markdown
