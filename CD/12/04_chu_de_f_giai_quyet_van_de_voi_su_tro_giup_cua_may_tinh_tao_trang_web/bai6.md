# Bài 6: TẠO BIỂU MẪU

**Học xong bài này, em sẽ:**
*   Phát biểu được khái niệm biểu mẫu.
*   Mô tả được một số điều khiển hỗ trợ nhập dữ liệu trên trang web.
*   Nêu được một số quy định trong thiết kế biểu mẫu.

Trên màn hình soạn thảo email có một số ô điều khiển nhập dữ liệu, em hãy cho biết tên và chức năng của các điều khiển đó.

## 1. Nhập dữ liệu thông qua biểu mẫu

Biểu mẫu trên trang web là một giao diện để thu nhận thông tin từ người dùng.

Biểu mẫu bao gồm các điều khiển nhập dữ liệu như ô văn bản, nút chọn, hộp kiểm,... được thiết kế phù hợp với nhiều kiểu dữ liệu khác nhau, giúp người dùng dễ dàng nhập dữ liệu và giảm sai sót.

Ngoài ra, biểu mẫu còn có các nút lệnh cho phép người dùng xác nhận kết thúc nhập dữ liệu để gửi yêu cầu và dữ liệu về máy chủ web.

Ví dụ, biểu mẫu có ô văn bản để nhập địa chỉ email hoặc số điện thoại. Kết thúc việc nhập dữ liệu và gửi yêu cầu, người dùng nháy chuột vào nút lệnh **Tiếp theo**.

HTML định nghĩa phần tử **form** để tạo biểu mẫu theo cú pháp sau:

Cú pháp HTML định nghĩa một biểu mẫu. Thuộc tính `action` chỉ định URL để gửi dữ liệu, và `method` chỉ định phương thức HTTP (GET/POST) được sử dụng để gửi dữ liệu. Bên trong thẻ `form` là nơi chứa các điều khiển nhập dữ liệu.

Thuộc tính *action* xác định tài nguyên web sẽ tiếp nhận và xử lí dữ liệu mà người dùng vừa gửi đến máy chủ. Tài nguyên web thường là các chương trình được viết bằng các ngôn ngữ lập trình, ví dụ như: Java, PHP, Python,...
Thuộc tính *method* xác định phương thức gửi dữ liệu đến máy chủ để xử lí, thường có giá trị là GET hoặc POST. Nếu không khai báo, phương thức GET được sử dụng. Sử dụng GET, dữ liệu gửi đến máy chủ xuất hiện trong ô địa chỉ của trình duyệt và bị hạn chế về dung lượng. Ngược lại, sử dụng POST, dữ liệu gửi đến máy chủ không xuất hiện trong ô địa chỉ của trình duyệt và không bị hạn chế về dung lượng nên POST thường được dùng để gửi dữ liệu có dung lượng lớn.
Thông thường, kết thúc quá trình nhập dữ liệu, người dùng cần nháy chuột vào nút lệnh có chức năng gửi dữ liệu trên biểu mẫu để dữ liệu nhập vào được gửi đến máy chủ web. Sau khi tiếp nhận, xử lí dữ liệu, máy chủ web gửi trả kết quả và kết quả thường là một trang web khác.

## Một số điều khiển hỗ trợ nhập dữ liệu thông dụng và nút lệnh

Em hãy phân biệt sự khác nhau giữa việc nhập dữ liệu cho ô "Địa chỉ người nhận" và ô "Nội dung" khi soạn thảo email.

### a) Nhập kí tự

Điều khiển nhập xâu kí tự (ô text) được khai báo bằng phần tử *input* như sau:

Một đoạn mã HTML khai báo một trường nhập liệu dạng văn bản (text input) với tên điều khiển và giá trị mặc định.

Trong đó:
*   **Tên_điều_khiển** được gán cho thuộc tính **name**. Thuộc tính **name** không phải là thuộc tính bắt buộc khai báo, nhưng tất cả các điều khiển thường được đặt tên để thuận lợi cho việc xử lí dữ liệu gửi từ biểu mẫu về máy chủ web.
*   Thuộc tính **value** nếu được khai báo thì **Giá trị** được gán là giá trị mặc định của ô text khi hiển thị trên màn hình trình duyệt web.

Ví dụ 1. Văn bản HTML ở Hình 2a tạo biểu mẫu có hai ô text nhập dữ liệu, trong đó một ô text có giá trị mặc định. Kết quả hiển thị trên màn hình trình duyệt web sẽ như ở Hình 2b.

Mô tả chức năng của đoạn mã: Khai báo một biểu mẫu (form) HTML để đăng nhập. Biểu mẫu này chứa hai trường nhập liệu kiểu văn bản: một cho tên đăng nhập với giá trị mặc định là "VietBach" và một cho email.

Ngoài ô text, HTML còn cung cấp một số điều khiển hỗ trợ nhập dữ liệu thông dụng như sau:

*   **textarea**: Tạo ô nhập đoạn văn bản.
    *   Ví dụ: Một trường nhập liệu nhiều dòng cho phép người dùng nhập các bình luận.
*   **label**: Tạo nhãn mô tả ý nghĩa của điều khiển nhập dữ liệu.
    *   Ví dụ: Nhãn "Địa chỉ email:" để mô tả trường nhập liệu email.
*   **password**: Tạo ô text nhập định dạng mật khẩu, mỗi kí tự nhập trong ô text thường được thay thế bằng dấu chấm đen trên màn hình trình duyệt web giúp bảo mật thông tin.
    *   Ví dụ: Một trường nhập liệu kiểu mật khẩu có tên "MatKhau".

### b) Nhập dữ liệu bằng cách lựa chọn

Trong một số trường hợp, dữ liệu nhập vào được xác định trước bằng cách cung cấp một số phương án để người dùng lựa chọn.

Danh sách các nút chọn (**radio button**) được sử dụng trong trường hợp cho người dùng chọn lựa một mục trong danh sách mục gợi ý. HTML định nghĩa **radio button** thông qua phần tử *input* có thuộc tính *type = "radio"*. Mỗi nút chọn trong danh sách được khai báo bởi một phần tử *input*.

Chú ý: Thuộc tính *name* của các nút chọn phải được khai báo như nhau để khi nhập liệu người dùng chỉ tích (chọn) được một mục trong danh sách.

Ví dụ 2. Nội dung trong phần *body* của văn bản HTML ở *Hình 3a* khai báo danh sách các mục chọn và kết quả hiển thị trên màn hình trình duyệt web sẽ như ở *Hình 3b*.

Đoạn mã HTML này tạo một biểu mẫu thăm dò ý kiến với câu hỏi "Thời gian tham gia ngoại khoá ngày Chủ nhật?". Người dùng có thể chọn một trong ba lựa chọn: "Sáng", "Chiều" hoặc "Tối" thông qua các nút **radio**.

HTML còn hỗ trợ tạo danh sách chọn hộp kiểm (**checkbox**) cho phép người nhập dữ liệu có thể chọn nhiều hoặc tất cả các mục trong danh sách các mục chọn. Hộp kiểm được định nghĩa thông qua phần tử **input** có thuộc tính **type = "checkbox"**.

Ví dụ 3. Nội dung trong phần **body** của văn bản HTML ở Hình 4a khai báo danh sách các hộp kiểm và kết quả hiển thị trên màn hình trình duyệt web sẽ như ở Hình 4b.

Đoạn mã HTML này tạo một biểu mẫu thăm dò ý kiến với câu hỏi "Bạn sẽ tham gia các câu lạc bộ thể thao nào?". Người dùng có thể chọn nhiều câu lạc bộ từ danh sách "Bóng đá", "Cầu lông" hoặc "Cờ vua" bằng cách sử dụng các hộp **kiểm (checkbox)**.

### c) Nút lệnh gửi dữ liệu

HTML cho phép tạo nút lệnh (thường được gọi là nút **submit**) để gửi dữ liệu được nhập trên biểu mẫu về máy chủ web. Nút submit được khai báo như sau:

Đoạn mã HTML này định nghĩa một thẻ `input` với `type="submit"`. Thẻ này có thể có thuộc tính `name` để đặt tên cho điều khiển và thuộc tính `value` tùy chọn để đặt nhãn hiển thị trên nút.

Thuộc tính **value** nếu được khai báo sẽ cung cấp nhãn của nút, trong trường hợp không khai báo, nút trên biểu mẫu có nhãn mặc định là “Submit”.

Ví dụ 4. Nội dung trong phần **body** của văn bản HTML khai báo nút lệnh gửi dữ liệu có nhãn là “Đồng ý” và kết quả hiển thị trên màn hình trình duyệt web như sau:

Đoạn mã HTML này tạo một biểu mẫu (`form`) sử dụng phương thức `POST`. Bên trong biểu mẫu có một nút `input` kiểu `submit` với thuộc tính `name` là `cmd` và thuộc tính `value` là “Đồng ý”.

Kết quả khi mở văn bản HTML trong trình duyệt web là một nút có nhãn "Đồng ý".

## Em cần chú ý

Khi khai báo các điều khiển trên biểu mẫu, cần lưu ý:
*   Chọn điều khiển nhập dữ liệu phù hợp với loại thông tin cần thu thập. Ví dụ, để người dùng chọn được nhiều mục thì nên sử dụng **checkbox**.
*   Thứ tự các điều khiển nên sắp xếp từ trái sang phải, từ trên xuống dưới, góp nhóm phù hợp với thứ tự dữ liệu người dùng cần nhập. Ví dụ, nên đặt các nút lệnh ở cuối biểu mẫu vì thao tác gửi dữ liệu thường được thực hiện sau khi nhập xong dữ liệu.
*   Nếu biểu mẫu có nhiều nút lệnh, nên sắp xếp nút lệnh theo hàng ngang, ưu tiên nút lệnh có tần suất sử dụng nhiều ở bên trái.

## Luyện tập

* Em hãy soạn văn bản HTML để tạo biểu mẫu với các điều khiển nhập liệu như ở Hình 6.
* Em hãy hiệu chỉnh văn bản HTML trong bài Luyện tập để chỉ cho phép chọn một môn thể thao trong danh sách các môn thể thao được gợi ý.

**Câu 1. Khai báo nào được dùng để tạo điều khiển nhập dữ liệu ô text trong biểu mẫu?**
A. `<input type = "text" name = "txt">`
B. `<textfield name= "txt">`
C. `<textinput name = "txt">`
D. `<input type = "txtfield" name = "txt">`

**Câu 2. Mỗi phát biểu sau đây về các điều khiển nhập dữ liệu trên biểu mẫu là đúng hay sai?**
a) Phần tử **textarea** được dùng để khai báo điều khiển nhập dữ liệu kí tự trên nhiều dòng trong biểu mẫu.
b) Phần tử **input** có thuộc tính **type = "radio"** được dùng để khai báo các mục lựa chọn cho phép người dùng có thể chọn nhiều mục chọn.
c) Phần tử **input** có thuộc tính **type = "submit"** được dùng để khai báo nút lệnh gửi dữ liệu.
d) Muốn xuống dòng khi nhập dữ liệu vào ô nhập liệu tạo bằng khai báo phần tử **input** có thuộc tính **type = "text"** sử dụng phím Enter.

## Tóm tắt bài học

* Phần tử **form** được sử dụng để khai báo biểu mẫu.
* Các điều khiển nhập dữ liệu thông dụng trong biểu mẫu gồm: ô **text**, tích chọn **radio button**, hộp kiểm **checkbox**, nút lệnh **submit**.
* Khi thiết kế biểu mẫu, em cần lựa chọn điều khiển phù hợp với thông tin cần thu thập.
