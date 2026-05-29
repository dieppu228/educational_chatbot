# Bài 2: BẢNG VÀ KHOÁ CHÍNH TRONG CƠ SỞ DỮ LIỆU QUAN HỆ

**Học xong bài này, em sẽ:**
*   Diễn đạt được khái niệm quan hệ (bảng) và khoá của một quan hệ. Giải thích được các khái niệm đó qua ví dụ minh hoạ.
*   Giải thích được ràng buộc khoá là gì.
*   Biết được các phần mềm quản trị CSDL có cơ chế kiểm soát các cập nhật dữ liệu để đảm bảo ràng buộc khoá.

Hồ sơ học sinh một lớp được tổ chức theo dạng bảng: mỗi hàng chứa dữ liệu về một học sinh, mỗi cột chứa dữ liệu về một thuộc tính của học sinh như: Họ và tên, Ngày sinh,... Theo em, cách tổ chức như vậy có ưu điểm gì trong việc quản lí thông tin học sinh của lớp?

## 1. Tổ chức dữ liệu trong CSDL quan hệ và các thao tác trên dữ liệu

### a) Cơ sở dữ liệu quan hệ

**Cơ sở dữ liệu quan hệ** là một tập hợp các bảng dữ liệu có liên quan với nhau. Hình 1 cho thấy một phần bảng HỌC SINH 11 trong một CSDL quan hệ của một trường học.

Tên của mỗi cột trong bảng cho biết ý nghĩa dữ liệu ở các ô thuộc cột đó. Tên bảng cùng với tên cột giúp hiểu nghĩa của mỗi hàng trong bảng. Mỗi hàng trong bảng chứa một bộ các giá trị, ví dụ, trong Hình 1, bộ gồm 6 giá trị: “13109413”, “Phan Thuỳ Anh”, “29/10/2007”, “Nữ”, “☑”, “39 Hùng Vương” cho thông tin về một học sinh.

Mỗi một hàng trong bảng của CSDL quan hệ còn được gọi là **một bản ghi**. Mỗi cột của bảng còn được gọi là **một trường**. Trong Hình 1 bảng HỌC SINH 11 có 6 trường phản ánh 6 thuộc tính của mỗi học sinh.

## Cập nhật dữ liệu trong CSDL quan hệ
Cập nhật dữ liệu của một bảng bao gồm các thao tác thêm, sửa và xoá dữ liệu của bảng. Cấu trúc của một bảng bao gồm các mô tả cho các cột của bảng; người thiết kế CSDL sẽ định nghĩa cấu trúc của các bảng dựa vào các yêu cầu quản lí của đơn vị chủ quản. Cập nhật dữ liệu của một bảng không làm thay đổi cấu trúc của bảng.

## Truy vấn trong CSDL quan hệ
Dữ liệu được tổ chức, lưu trữ trong CSDL là để người sử dụng có thể khai thác dữ liệu, rút ra thông tin phục vụ các hoạt động hoặc giúp đưa ra các quyết định phù hợp, kịp thời. Bản chất việc khai thác một CSDL là tìm kiếm dữ liệu và kết xuất ra thông tin cần tìm, công việc này còn được gọi là **truy vấn CSDL**.

## Các ràng buộc dữ liệu trong CSDL quan hệ
Theo em, mỗi học sinh cần phải có riêng một **Mã định danh** để đưa vào hồ sơ quản lí hay không? Vì sao?

Dữ liệu trong CSDL quan hệ phải thoả mãn một số ràng buộc gọi là **ràng buộc toàn vẹn về dữ liệu** để đảm bảo tính xác định và đúng đắn của dữ liệu. Ví dụ một số ràng buộc dữ liệu:
*   Trong một bảng không có hai bản ghi giống nhau hoàn toàn.
*   Trong cùng một bảng, mỗi trường có một tên phân biệt với tất cả các trường khác.
*   Mỗi bảng có một tên phân biệt với các bảng khác trong cùng CSDL.
*   Mỗi ô của bảng chỉ chứa một giá trị.
Ngoài ra, tuỳ theo yêu cầu của bài toán quản lí cụ thể mà người thiết kế CSDL đặt thêm một số ràng buộc khác cho dữ liệu. Ví dụ: người thiết kế CSDL cho trường học có thể yêu cầu **Mã định danh** của mỗi học sinh phải là một dãy số không quá 12 kí tự, tất cả các kí tự đều là số. Với ràng buộc như thế, việc nhập “0011234567899” vào cột **Mã định danh** là không hợp lệ, đó là vì phạm ràng buộc miền giá trị.

### Khoá của một bảng
Trong một bảng, mỗi bản ghi thể hiện thông tin về một đối tượng (một cá thể hoặc một sự kiện) nên không thể có hai bản ghi giống nhau hoàn toàn. Trong bảng chứa dữ liệu học sinh, ví dụ như bảng HỌC SINH 11, hai học sinh khác nhau sẽ có hai **Mã định danh** khác nhau. Điều này giống như trường hợp số căn cước công dân của mỗi người xác định người đó là duy nhất, không nhầm lẫn với bất cứ ai.

Trong một bảng, có những tập hợp gồm một trường hay một số trường mà giá trị của chúng ở các bản ghi khác nhau là khác nhau. Ví dụ ở Hình 2: một giá trị của trường *STT* chỉ xuất hiện ở một bản ghi; một bộ giá trị của hai trường *CCCD* và *BHYT*, chẳng hạn ("001160017719", "HT3010101040124") chỉ xuất hiện ở một bản ghi. Nói cách khác, tập hợp gồm một trường *STT* và tập hợp gồm hai trường *CCCD* và *BHYT* đều có tính chất: Dùng giá trị của nó xác định được duy nhất một bản ghi trong bảng. Với ví dụ bảng trong Hình 2, có thể kể ra thêm một số tập hợp trường có tính chất như vậy:
*   Tập chỉ gồm một trường *CCCD*.
*   Tập gồm hai trường: *STT*, *Họ và tên*.
*   Tập gồm tất cả sáu trường.

Khoá của một bảng là tập hợp một số trường có tính chất: mỗi bộ giá trị của các trường đó xác định duy nhất một bản ghi trong bảng và không thể bỏ bớt bất cứ trường nào mà tập hợp gồm các trường còn lại vẫn còn tính chất đó.

**Khoá của một bảng**: tập hợp các trường (có thể chỉ là một trường) mà mỗi bộ giá trị của nó xác định duy nhất một bản ghi ở trong bảng và ta không thể bỏ đi trường nào mà tập hợp các trường còn lại vẫn còn có tính chất xác định duy nhất một bản ghi trong bảng.

Với ví dụ bảng ở Hình 2:
*   Tập hợp chỉ có một trường *CCCD* là một **khoá**.
*   Tập hợp gồm hai trường *STT*, *Họ và tên* không phải là **khoá** vì nếu bỏ trường *Họ và tên* ra khỏi tập hợp này thì chỉ riêng *STT* cũng có tính chất xác định duy nhất một bản ghi trong bảng.
*   Nếu không thể có hai nhân viên trùng nhau hoàn toàn ở *Họ và tên*, *Ngày sinh* thì tập hợp gồm hai trường *Họ và tên*, *Ngày sinh* cũng tạo thành một **khoá**. Nhưng tập gồm ba thuộc tính *STT*, *Họ và tên*, *Ngày sinh* không phải là một **khoá**.

Khi bảng có hơn một khoá, người ta thường chọn (chỉ định) một khoá làm **khoá chính** (Primary Key), ưu tiên chọn khoá gồm ít trường nhất, tốt nhất nếu chọn được khoá chỉ là một trường. Bởi vậy, với bảng ở Hình 2, thay vì chọn khoá chính là tập hợp gồm hai trường

Họ và tên và Ngày sinh, ta có thể chọn trường *STT* hay trường *CCCD* làm **khoá chính** của bảng bởi các hàng trong bảng phân biệt với nhau bởi số thứ tự (*STT*). Trên thực tế, người ta thường tạo thêm trường *MaNV* (Mã nhân viên) làm khoá chính cho bảng chứa thông tin nhân viên để phù hợp với cách tổ chức quản lí của đơn vị đó.

Việc cập nhật dữ liệu cho một bảng cũng phải thoả mãn yêu cầu không làm xuất hiện hai bản ghi có giá trị khoá giống nhau. Yêu cầu này còn được gọi là **ràng buộc khoá**.

## Hệ quản trị CSDL đảm bảo ràng buộc khoá
Bất cứ **hệ quản trị CSDL** nào cũng có cơ chế kiểm soát, ngăn chặn những vi phạm **ràng buộc khoá** đối với việc cập nhật dữ liệu. Để thực hiện điều đó, phần mềm yêu cầu người tạo lập CSDL chỉ định trường làm **khoá chính** và mỗi khi xuất hiện thao tác cập nhật dữ liệu, phần mềm sẽ tự động kiểm tra xem cập nhật đó có vi phạm ràng buộc khoá hay không.

## Thực hành với khoá của bảng trong CSDL

### Yêu cầu:
Sử dụng phần mềm **Microsoft Access 365** tạo bảng SÁCH có cấu trúc như ở Hình 3, chỉ định trường **Mã sách** làm **khoá chính** và nhập nhiều hơn 5 bản ghi cho bảng.

### Hướng dẫn thực hiện:
*   Bước 1. Khởi chạy **Microsoft Access 365** bằng cách nháy đúp chuột vào biểu tượng Access của phần mềm này.
*   Bước 2. Tạo một CSDL mới, trong CSDL mới này tạo cấu trúc cho bảng SÁCH bằng cách thực hiện tuần tự các thao tác sau:
    *   Chọn **Blank Desktop Database** rồi đặt tên cho CSDL mới (hoặc nháy đúp chuột vào biểu tượng của Blank Desktop Database, Access sẽ tự đặt tên cho CSDL mới tạo).
    *   Chọn **Create\Table Design** để xuất hiện cửa sổ khai báo cấu trúc bảng (Hình 3).

- Trên mỗi hàng nhập tên một trường (ở cột **Field Name**), chọn kiểu dữ liệu cho trường đó bằng cách đưa con trỏ chuột vào ô ở cột **Data Type** để làm xuất hiện danh sách cho chọn.
- Bước 3. Chỉ định khóa chính cho bảng bằng cách chọn hàng có trường Mã sách, sau đó chọn **Primary Key**.
- Bước 4. Chọn **Save** để lưu cấu trúc bảng và đặt tên cho bảng.
- Bước 5. Chọn **View** để xuất hiện cửa sổ cho nhập các bản ghi vào bảng.
- Chú ý: Nên thử nhập hai bản ghi giống nhau để xem phần mềm báo lỗi vì phạm ràng buộc khoá ra sao.

## Luyện tập
Để tiếp tục xây dựng CSDL quản lí một thư viện, em hãy cho biết:
* a) Dự kiến của em về cấu trúc bảng **NGƯỜI ĐỌC**, biết rằng bảng này dùng để lưu trữ dữ liệu về những người có thể thư viện.
* b) Trong các trường của bảng **NGƯỜI ĐỌC**, nên chọn trường nào làm khóa chính? Giải thích vì sao?
* c) Hãy nêu ví dụ cụ thể về nhập dữ liệu cho bảng **NGƯỜI ĐỌC** nhưng vi phạm ràng buộc khoá.

Trong các câu sau, những câu nào đúng?
* a) Trong CSDL quan hệ, mỗi bảng chỉ có một khoá.
* b) Khoá của một bảng chỉ là một trường.
* c) Nếu hai bản ghi khác nhau thì giá trị khoá của chúng phải khác nhau.
* d) Các hệ quản trị CSDL quan hệ tự động kiểm tra ràng buộc khoá để đảm bảo tính đúng đắn của dữ liệu.

## Tóm tắt bài học
* Một **CSDL quan hệ** là một tập hợp các bảng dữ liệu (quan hệ) có liên quan với nhau.
* Mỗi bảng trong CSDL đều phải có **khoá**, đó là tập hợp gồm một hay một số trường cho phép xác định duy nhất một bản ghi trong bảng.
* **Dữ liệu** trong một bảng phải thoả mãn **ràng buộc khoá**: Không có hai bản ghi giống nhau ở giá trị khoá. Mọi hệ quản trị CSDL quan hệ đều có cơ chế kiểm soát việc cập nhật dữ liệu để không xảy ra vi phạm ràng buộc khoá đối với mỗi bảng.
