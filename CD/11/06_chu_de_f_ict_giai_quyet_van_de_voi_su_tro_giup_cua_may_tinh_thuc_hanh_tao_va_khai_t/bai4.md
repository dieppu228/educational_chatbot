# Bài 4: TẠO VÀ SỬ DỤNG BIỂU MẪU

Học xong bài này, em sẽ:
* Phân biệt được “có kết buộc với bảng CSDL” và “không kết buộc”.
* Tạo được một số loại biểu mẫu thường dùng nhất.
* Sử dụng được biểu mẫu để nhập dữ liệu.

Em hãy kể một loại biểu mẫu điền thông tin mà em biết, nó gồm có những mục gì? Một số mục có một (hay vài) ô vuông để đánh dấu chọn, vì sao có mẫu như thế?

## 1. Tạo biểu mẫu trong Access
### a) Các loại biểu mẫu
**Biểu mẫu một bản ghi** và **biểu mẫu nhiều bản ghi**
* Biểu mẫu một bản ghi: Tại một thời điểm, nó hiển thị một hàng trong bảng CSDL. Trong ứng dụng thực tế, biểu mẫu này dùng để nhập hay hiển thị thông tin về một cá thể: một người, một mục hàng trong đơn hàng,... Thông thường, các tên trường ở bên trái và ô để nhập, hiển thị dữ liệu kể bên phải.
* Biểu mẫu nhiều bản ghi: Hiển thị nhiều bản ghi cùng một lúc, mỗi bản ghi trên một hàng ngang, các trường là các cột, nhìn tương tự như một phần của bảng dữ liệu.

**Biểu mẫu tách đôi**
Vùng hiển thị biểu mẫu được chia thành hai nửa, theo chiều dọc hoặc chiều ngang.
Ví dụ, nửa trên hiển thị các trường của một bản ghi dưới dạng biểu mẫu tờ khai quen thuộc. Nửa dưới hiển thị nội dung của nhiều bản ghi.
Một kiểu biểu mẫu khác cũng tách đôi thành hai nửa nhưng nó thể hiện quan hệ 1 – ∞ giữa hai bảng. Ví dụ, hiển thị thông tin về một bạn đọc và một số lần mượn trả sách của bạn đọc đó.

Biểu mẫu có kết buộc với bảng CSDL và biểu mẫu không kết buộc
*   **Biểu mẫu có kết buộc (bound)**: Các mục dữ liệu hiển thị trong biểu mẫu kết buộc trực tiếp với các trường trong bảng CSDL và làm thay đổi dữ liệu của trường khi gõ nhập. Phải là biểu mẫu có kết buộc thì mới có thể dùng để nhập, chỉnh sửa, xem dữ liệu,... Các mục sau chủ yếu trình bày về biểu mẫu có kết buộc.
*   **Biểu mẫu không kết buộc (unbound)**: Đối lập với biểu mẫu có kết buộc, biểu mẫu không kết buộc không dùng để nhập, chỉnh sửa dữ liệu.

### b) Tạo biểu mẫu

#### Hướng dẫn tạo nhanh một số biểu mẫu có kết buộc với một bảng

Nhóm lệnh **Forms** có các nút lệnh để tạo nhanh một biểu mẫu và sau đó sử dụng ngay được.

Sau khi đánh dấu chọn một bảng hay truy vấn trong vùng điều hướng, Access sẽ hiểu là bước tiếp theo ta cần sử dụng bảng (truy vấn) đó làm nguồn dữ liệu cho biểu mẫu.

##### Tạo biểu mẫu một bản ghi

*   Bước 1. Nháy chuột chọn `Create\Form` sẽ tạo biểu mẫu một bản ghi gồm tất cả các trường. Access tự động đặt một tên tạm dựa trên tên bảng.
*   Bước 2. Sửa lại tên biểu mẫu (nếu cần) trước khi ghi lưu. Nên đặt tên gợi nhớ nội dung biểu mẫu là gì.

Sau khi đặt tên và ghi lưu, biểu tượng biểu mẫu kèm tên sẽ xuất hiện trong vùng điều hướng. Ta có thể mở để chỉnh sửa thiết kế hay sử dụng bất kì lúc nào.

##### Tạo biểu mẫu nhiều bản ghi

*   Bước 1. Nháy chuột chọn `Create\More Forms` sẽ thả xuống một danh sách chọn. Sau đó nháy chuột.
    *   Chọn `Multiples Items` sẽ tạo ra một biểu mẫu nhiều bản ghi.
    *   Chọn `DataSheet` cũng tạo ra một biểu mẫu nhiều bản ghi nhưng có dạng như khung nhìn bảng dữ liệu.
    *   Chọn `Split Form` sẽ tạo ra biểu mẫu tách đôi.

Bước 2. Tương tự như Bước 2 khi tạo biểu mẫu một bản ghi.

## Hướng dẫn tạo biểu mẫu bằng Form Wizard

Tạo nhanh biểu mẫu bằng nút lệnh Form hay More Forms rất dễ nhưng không có các lựa chọn tuỳ biến, ví dụ chỉ chọn một số trường nào đó, chọn các bản ghi từ hai bảng,...

Cách làm tốt hơn là sử dụng tiện ích tạo biểu mẫu Form Wizard hỗ trợ làm biểu mẫu có tuỳ biến rất thuận tiện.

### Tạo biểu mẫu một bản ghi

Sau khi khởi chạy tiện ích tạo biểu mẫu bằng cách chọn Create\Form Wizard, thực hiện quy trình 3 bước chính như sau:

#### Bước 1. Chọn các trường dữ liệu.
Hộp thoại đầu tiên mở ra để chọn các trường dữ liệu sẽ hiển thị trên biểu mẫu. Các trường này có thể lấy từ các bảng hoặc truy vấn.
Thao tác tương tự như nhau:
1) Từ danh sách thả xuống **Tables\Queries** cần chọn tên bảng/truy vấn. Danh sách các trường có sẵn **Available Fields** hiển thị trong khoảng dưới.
2) Chọn tên trường, nháy dấu “>” để chuyển sang hộp thoại **Selected Fields**.
3) Có thể nháy vào dấu “>>” để di chuyển tất cả các trường cùng lúc.
4) Nháy **Next** khi đã chọn xong tất cả các trường dữ liệu muốn có.
#### Bước 2. Chọn kiểu trình bày biểu mẫu.
Hộp thoại tiếp theo của tiện ích tạo biểu mẫu sẽ yêu cầu chọn kiểu trình bày. Có 4 kiểu: **columnar** (mặc định, hay dùng nhất); **tabular, datasheet, justified**. Hãy thử chọn, xem trước và đổi sang kiểu khác nếu muốn vì có sẵn nút “**< back**” để quay lại.
#### Bước 3. Chọn **Finish** để kết thúc và ghi lưu. Có thể đổi tên nếu cần.

## Biểu mẫu phân cấp và biểu mẫu đồng bộ hoá

Nếu hai bảng có mối quan hệ 1 – ∞ (bảng mẹ – bảng con), có thể tạo biểu mẫu hiển thị một bản ghi của bảng mẹ và dữ liệu từ các hàng trong bảng con liên quan đến bản ghi của bảng mẹ. Đây là biểu mẫu phân cấp, có dạng tách đôi, hiển thị đồng bộ dữ liệu từ hai bảng khác nhau, theo mối quan hệ đã thiết lập trước.

## Hướng dẫn tạo biểu mẫu phân cấp và biểu mẫu đồng bộ hoá bằng Form Wizard

Quy trình tạo biểu mẫu kết buộc với nhiều hơn một bảng sẽ có nhiều thao tác hơn ở bước chọn các trường dữ liệu.

### Bước 1. Chọn các trường dữ liệu

Chọn các trường dữ liệu từ cả hai, bảng mẹ và bảng con, trước khi nháy chọn **Next**. Tiện ích tạo biểu mẫu sẽ nhận biết và yêu cầu lựa chọn biểu mẫu chính và biểu mẫu con lệ thuộc.

### Bước 2. Chọn biểu mẫu chính:

Nháy chuột chọn tên bảng nguồn dữ liệu chính. Khung hình sẽ đưa ra câu hỏi để chọn tạo biểu mẫu phân cấp hay biểu mẫu đồng bộ hoá.
*   1) **Form with subform(s)**: Tạo biểu mẫu đồng bộ hoá.
*   2) **Linked forms**: Tạo biểu mẫu phân cấp.

### Bước 3. Đánh dấu lựa chọn 1).

Hộp thoại tiếp theo sẽ hỏi cách trình bày biểu mẫu con. Đánh dấu chọn theo mong muốn. Tiếp theo ta trở lại với Bước 2 và Bước 3 trong quy trình thao tác làm biểu mẫu bằng **Form Wizard**.

## Sử dụng biểu mẫu để nhập hoặc xem dữ liệu

Mở biểu mẫu trong khung nhìn biểu mẫu (**Form View**) để nhập hoặc xem dữ liệu. Minh hoạ một biểu mẫu nhiều bản ghi vừa được tạo ra, chưa chỉnh sửa, nhưng đã có thể sử dụng để xem và nhập dữ liệu.

Chú ý ở góc dưới bên trái:
*   Có hộp hiển thị số thứ tự bản ghi đang xử lí, trong hình minh hoạ: “17 of 17” nghĩa là bản ghi thứ 17 trong số 17 bản ghi đã có.
*   Có các nút điều hướng quen thuộc: lùi, tiến, nhảy tới bản ghi cuối cùng, hiển thị một biểu mẫu trống để bắt đầu nhập dữ liệu cho bản ghi mới.
*   Có hộp **Search** để tìm kiếm.

## Sắp xếp các bản ghi theo giá trị một trường

Khi nhập dữ liệu, theo mặc định Access thêm bản ghi mới thành hàng cuối cùng trong bảng dữ liệu. Khi xem dữ liệu, thứ tự hiển thị các bản ghi như vốn có trong bảng nếu ta không thay đổi cách sắp xếp. Một số kiểu dữ liệu như: chữ, số, ngày tháng,... có thể sắp xếp theo thứ tự tăng dần hay giảm dần.

### Hướng dẫn thao tác sắp xếp

*   Bước 1. Chọn cột hay ô dữ liệu trong cột đó.
*   Bước 2. Chọn Home sau đó chọn nhóm **Sort & Filter**.
*   Bước 3. Chọn **Ascending** hay **Descending** rồi quan sát kết quả.
*   Bước 4. Chọn **Save** trong thanh công cụ nhanh **Quick Access Toolbar**.
    Sau khi đã ghi lưu cách sắp thứ tự thì mỗi lần mở xem sau này các bản ghi sẽ hiển thị theo cách sắp xếp đã chọn.
    Để gỡ bỏ không sắp thứ tự nữa, nháy chuột vào **Remove Sort**.
    Việc sắp thứ tự nhiều mức, lần lượt theo vài cột phức tạp hơn, cần sử dụng nút lệnh **Advanced** trong nhóm lệnh **Sort & Filter**.

### Lọc các bản ghi
Access làm sẵn nhiều lựa chọn lọc kèm các cột dữ liệu kiểu văn bản chữ, số, ngày tháng. Mở bảng dưới khung nhìn bảng dữ liệu và thao tác tương tự như trong Excel.
* Bước 1. Nháy chuột vào dấu trỏ xuống cạnh tên cột muốn lọc; xuất hiện danh sách thả xuống các hộp đánh dấu chọn.
* Bước 2. Đánh dấu chọn những gì bạn muốn xuất hiện, sau đó chọn OK.

## Thực hành tạo và sử dụng biểu mẫu

### Nhiệm vụ 1. Tạo biểu mẫu để nhập dữ liệu vào bảng Mượn-Trả sách
Tạo một biểu mẫu nhiều bản ghi lấy dữ liệu từ bảng *Mượn-Trả*, ghi lưu với tên *MượnTrả*.

### Nhiệm vụ 2. Tạo biểu mẫu để tìm mượn sách
Biểu mẫu nhiều bản ghi để tìm mượn sách lấy dữ liệu từ bảng *Sách* và cần đáp ứng các yêu cầu:
* a) Sắp xếp thứ tự theo *Tên sách*.
* b) Lọc theo cột *Sẵn có*. Ghi lưu với tên *Sách-Multi*.

### Nhiệm vụ 3. Sử dụng biểu mẫu để nhập dữ liệu
Dùng biểu mẫu vừa tạo ở Bài 1, nhập một số bản ghi vào bảng *Mượn-Trả*.
*Chú ý*: Dữ liệu nhập vào không được trái với thực tế trong hoạt động của thư viện.

## Luyện tập
Quản lí thư viện cần biết mỗi bạn đọc đã mượn những cuốn sách nào. Em hãy tạo một biểu mẫu cho phép làm việc này.

Câu 1. Mục dữ liệu “có kết buộc với bảng CSDL” và “không kết buộc” khác nhau như thế nào?
Câu 2. Dùng nút lệnh nào để tạo nhanh biểu mẫu? Trường hợp nào nên chọn cách làm này?

## Tóm tắt bài học
*   **Biểu mẫu** dùng để nhập và xem dữ liệu từ một hoặc nhiều bảng; có thể hiển thị một bản ghi hay nhiều bản ghi; có thể trình bày tách đôi thành hai phần.
*   Nút lệnh Form để tạo nhanh biểu mẫu nhưng không cho phép tùy biến.
*   Tiện ích tạo biểu mẫu Form Wizard hỗ trợ tạo các loại biểu mẫu tuỳ biến theo yêu cầu sử dụng.
