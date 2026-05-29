# Bài 5: THIẾT KẾ TRUY VẤN

Học xong bài này, em sẽ:
*   Tạo và sử dụng được các truy vấn để tìm kiếm và kết xuất thông tin từ CSDL.
*   Góp phần giải thích tính ưu việt của việc quản lí dữ liệu một cách khoa học nhờ ứng dụng CSDL.

Theo em để lấy ra một thông tin cụ thể từ CSDL thì cần công cụ gì?

## 1. Thiết kế truy vấn đơn giản
### a) Truy vấn SELECT
Truy vấn là một mẫu câu hỏi. Nó cho phép chọn từ các bảng đúng những gì ta cần xem. Sau khi thiết kế và ghi lưu, mỗi khi mở lại truy vấn, ta có câu trả lời dựa trên dữ liệu mới nhất. Đây là tính ưu việt của việc quản lí dữ liệu một cách khoa học nhờ ứng dụng CSDL.

Access hỗ trợ rất tốt việc thiết kế và thực thi truy vấn. Thiết kế truy vấn bắt đầu từ yêu cầu thao tác dữ liệu của một ứng dụng quản lí cụ thể. Bài học sẽ bám sát chức năng cung ứng dịch vụ “cho mượn – nhận trả” sách. Dưới đây nêu vài điểm thuộc logic nghiệp vụ của thư viện và dự kiến truy vấn tương ứng:
*   (1) Bạn đọc đến tìm sách để mượn: Cần truy vấn tìm “Sách có **sẵn** để mượn”.
*   (2) Thủ thư cần thao tác “Cho mượn - Nhận trả”: Ngoài việc nhập dữ liệu vào bảng Mượn-Trả còn phải sửa giá trị trường **Sẵn có** trong bảng để đánh dấu **Yes/No** phù hợp.

### b) Thiết kế truy vấn SELECT đơn giản
*   **Bước 1**. Nháy chuột chọn **Create\Query Design**.
*   **Bước 2**. Hộp thoại *Show Table* xuất hiện. Truy vấn lấy thông tin từ các bảng của CSDL. Nháy chuột chọn tên bảng và nháy nút **Add**. Nháy **Close** khi chọn xong.
*   **Bước 3**. Vùng làm việc thiết kế truy vấn sẽ mở ra và được chia thành hai phần. Phần trên có các hộp thể hiện các bảng vừa được chọn. Trong mỗi hộp hiển thị tên tất cả các trường của bảng đó. Nếu có trường bị che khuất, dùng chuột kéo đường viền đáy hộp để mở rộng thêm.

Access cũng hiển thị đường nối thể hiện liên kết giữa các bảng.

Bước 4. Phần dưới hiển thị một lưới ô, thường gọi là lưới QBE (Query by Example). Muốn chọn lấy dữ liệu từ trường nào chỉ cần nháy đúp chuột lên tên trường trong hộp thể hiện bảng. Tên trường sẽ xuất hiện trong cột ở lưới ô bên dưới, tuần tự từ trái sang phải theo trình tự thao tác chọn.
Hàng **Field** ở trên cùng của lưới ô hiển thị các tên trường đã chọn. Hàng thứ hai bên dưới **Field** là **Table**, hiển thị tên bảng chứa trường đó.

Bước 5. Nháy chọn **Run**, kết quả truy vấn hiển thị trong khung nhìn bảng dữ liệu.

Bước 6. Ghi lưu truy vấn. Nên đặt tên gợi nhớ kết quả truy vấn. Tên truy vấn sẽ xuất hiện trong vùng điều hướng. Sau đó, ta có thể mở ra bất cứ lúc nào để chỉnh sửa lại thiết kế theo mong muốn hoặc cho chạy để xem thông tin mới cập nhật từ CSDL. Ví dụ, ta đặt tên truy vấn vừa làm xong là “q-BanDoc-MuonTra”.
**Mẹo**: Một thói quen thực hành tốt là thêm tiền tố “q-” (**query**) vào trước tên để dễ nhận biết đó là một truy vấn. Trong vùng điều hướng có biểu tượng đi kèm nên ta không nhầm lẫn, nhưng trong các hộp thoại để chọn nguồn dữ liệu tạo biểu mẫu, báo cáo,... sẽ chỉ có tên xuất hiện nên khó phân biệt bảng với truy vấn.

## Sắp xếp kết quả truy vấn

Trong khung nhìn bảng dữ liệu, chú ý quan sát ta sẽ nhận thấy:

*   Thứ tự hiển thị các trường (cột) giống như trong lưới ô. Muốn thay đổi thứ tự này, ta sửa lại lưới ô trong khung nhìn thiết kế.
*   Nếu hai bảng đã được thiết lập mối quan hệ kết nối với nhau, sẽ chỉ thấy những bản ghi khớp đúng. Access đã tự động thực hiện phép nối trong.
*   Trình tự hiển thị các bản ghi là trình tự vốn có ở trong bảng dữ liệu cơ sở.

### Sắp xếp các bản ghi theo giá trị trường dữ liệu
Chuyển sang khung nhìn thiết kế truy vấn **Design View**. Trong vùng lưới ô, ở bên dưới hàng Table có hàng tên là **Sort**. Hàng này dùng để sắp xếp kết quả truy vấn theo một hoặc nhiều trường (lồng nhau).
(1) Sắp xếp theo một trường: chọn trường; chọn **Ascending** hoặc **Descending** để sắp xếp tăng dần hoặc giảm dần.
(2) Sắp xếp lồng nhau theo một vài trường, từ ngoài vào trong: thao tác lần lượt tuần tự từng trường, trình tự lồng nhau từ ngoài vào trong sẽ tương ứng lần lượt từ trái sang phải.
Ví dụ, trong truy vấn ở trên, nếu ta muốn sắp xếp theo “**Tên**” bạn đọc thì trong lưới ô, tại ô giao cắt cột **Tên** với hàng **Sort** cần chọn **Ascending**.

## 3. Chọn bản ghi cho truy vấn SELECT
### a) Tiêu chí lựa chọn bản ghi
Tiêu chí lựa chọn được thể hiện bằng một biểu thức logic gồm các biến trường và các phép toán. Chỉ các bản ghi với các giá trị trường dữ liệu làm biểu thức logic có giá trị là “Đúng” (**True**) mới được chọn lấy ra.
Hàng **Criteria** (tiêu chí) trong phần lưới ô là nơi viết biểu thức logic thể hiện tiêu chí lựa chọn.

## b) Một số thành phần trong biểu thức logic làm tiêu chí lựa chọn dữ liệu

Trong Bảng 1 là một số ví dụ đơn giản để minh hoạ cách viết một số biểu thức cơ sở.

*Bảng 1. Một số ví dụ về tiêu chí lựa chọn dữ liệu*
*   **Kiểu dữ liệu: Số** (ví dụ trường Số trang)
    *   Biểu thức logic: `>100 AND <=200`
    *   Diễn giải ý nghĩa: `100 < Số trang <= 200`
*   **Kiểu dữ liệu: Ngày tháng**
    *   Biểu thức logic: `>#14/09/2022# AND <=#20/09/2022#`
    *   Diễn giải ý nghĩa: `Từ sau 14/09/2022 đến hết ngày 20/09/2022`
*   **Kiểu dữ liệu: Xâu kí tự**
    *   Biểu thức logic: `="An"`
    *   Diễn giải ý nghĩa: `Đúng bằng "An"`
*   **Kiểu dữ liệu: Xâu kí tự**
    *   Biểu thức logic: `>"An"`
    *   Diễn giải ý nghĩa: `Xếp sau "An" theo từ điển`
*   **Kiểu dữ liệu: Logic** (ví dụ trường Sẵn có)
    *   Biểu thức logic: `Is Not Null`
    *   Diễn giải ý nghĩa: `Sẵn có (để mượn)`

Các phép toán:
*   (1) Các phép so sánh (kiểu số, xâu kí tự, ngày tháng): `=`, `<>` (không bằng), `>`, `>=`, `<`, `<=`.
*   (2) Kiểm tra thuộc miền giá trị: *In*, *Not In*, *Between*, *Not Between*, *Is Null*, *Is Not Null*.

Có thể phối hợp vài biểu thức logic để tạo ra tiêu chí lựa chọn phức tạp hơn.
*   Liên kết **AND**: Thể hiện bằng cách đặt hai tiêu chí lựa chọn ở hai trường khác nhau nhưng trên cùng hàng. Access sẽ chỉ lấy ra các bản ghi mà đáp ứng cả hai tiêu chí.
*   Liên kết **OR**: Thể hiện bằng cách đặt tiêu chí lựa chọn thứ hai ở hàng *Or*. Access sẽ lấy ra các bản ghi đáp ứng một trong hai tiêu chí.

Bảng 2 là ví dụ đơn giản để minh hoạ cách viết cho hai trường *Ngày Mượn* trong bảng *Mượn-Trả* và *Số trang* trong bảng *Sách*.

*Bảng 2. Một ví dụ về minh hoạ cách viết cho hai trường*
*   **Ví dụ 1 (kết hợp AND)**
    *   Ngày mượn: `<#05/09/2022#`
    *   Số trang: `>100`
    *   Diễn giải ý nghĩa: `Sách mượn từ trước ngày 05/9/2022 VÀ hơn 100 trang`
*   **Ví dụ 2 (kết hợp OR)**
    *   Ngày mượn: `>=#05/09/2022#`
    *   Số trang: `<200`
    *   Diễn giải ý nghĩa: `Sách mượn bắt đầu từ ngày 05/9/2022 HOẶC dưới 200 trang`

Em hãy làm theo các bước như hướng dẫn trong mục 1 và ghi lưu truy vấn “q-BanDoc-MuonTra”.
1) Thử thêm một số tiêu chí lựa chọn áp dụng cho trường *Tên*; chạy thử; kiểm tra kết quả; không ghi lưu.
2) Thử thêm một số tiêu chí lựa chọn áp dụng cho trường *Ngày mượn*; chạy thử; kiểm tra kết quả; không ghi lưu.

## 4. Truy vấn có tham số

Thay vì viết sẵn đầy đủ biểu thức logic thể hiện tiêu chí truy vấn, ta có thể muốn mời người sử dụng gõ nhập thêm yêu cầu lựa chọn trong khi chạy một truy vấn. Đó là một truy vấn có tham số (**Parameter Query**). Truy vấn có tham số làm tăng tính linh hoạt khi khai thác dữ liệu từ CSDL.

### Cách viết một truy vấn tham số đơn giản:

*   Trong cặp ngoặc vuông ([]) viết lời nhắc sao cho người sử dụng hiểu và điền vào đúng tham số ta muốn có trong câu lệnh truy vấn. Cặp dấu ngoặc vuông chứa lời nhắc ở đúng vị trí thay thế cho dữ liệu điền trước.
*   Tiếp nối việc thiết kế truy vấn đã xét ở mục trước, thay thế cho “VH-01” ta cần viết, ví dụ [Mã sách?]. Khi chạy truy vấn, một hộp thoại sẽ hiển thị chờ cung cấp tham số. (Hộp thoại này có trường nhập liệu cho "Mã sách ?" và các nút "OK", "Cancel".) Sau khi điền tham số ví dụ “VH-01” và nháy OK sẽ nhận được kết quả giống như có dữ liệu trực tiếp.

### Một số mẫu lời nhắc linh hoạt:

*   Thay cho dấu bằng “=” có thể sử dụng các phép so sánh khác khi thể hiện tham số truy vấn: <, <=, >, >=, <>,...

## 5. Truy vấn hành động

Ngoài truy vấn SELECT, có các loại truy vấn khác để tạo bảng, nối thêm dữ liệu vào một bảng, cập nhật hay xoá hàng loạt nhiều bản ghi trong bảng (**Make Table**, **Append**, **Update**, **Delete**).

Truy vấn hành động làm thay đổi bảng, thay đổi một loạt nhiều bản ghi. Kết quả của truy vấn hành động là không thể đảo ngược, nghĩa là không thể hồi lại trạng thái trước đó (**undo**). Do đó, cần rất thận trọng. Như một quy tắc chung, nên sao lưu dự phòng các bảng liên quan trước khi thực hiện truy vấn hành động.

## Thực hành thiết kế truy vấn

### Nhiệm vụ 1. Thiết kế truy vấn dựa trên bảng **Sách**, lấy ra các thông tin phục vụ bạn đọc tìm sách để mượn sao cho thuận tiện nhất:

*   a) Sắp xếp theo trường tên sách.
*   b) Lựa chọn chỉ hiển thị khi sẵn có để mượn.
    *   Gợi ý: `<>IsEmpty([Sẵn có])`. Ghi lưu với tên “q-TìmSách”.
*   c) Tạo biểu mẫu nhiều bảng ghi dựa trên truy vấn “q-TìmSách”; ghi lưu với tên *TìmSách*.
*   d) So sánh với biểu mẫu *Sách-Multi* đã làm sau bài học về biểu mẫu.

### Nhiệm vụ 2. Để chuẩn bị thông tin cho thao tác “Cho mượn” hay “Nhận trả” một cuốn sách cụ thể cần truy vấn nối hai bảng *Mượn-Trả* và *Sách*.

*   a) Thao tác từng bước thiết kế truy vấn nối hai bảng nói trên, chạy thử; kiểm tra kết quả; ghi lưu với tên “q-Sách-MượnTrả”.
*   b) Thêm tiêu chí lựa chọn theo **Mã sách**, ví dụ chọn mã sách là “VH-01”.
    *   Gợi ý: Trong lưới ô, tại ô giao cắt cột *Mã sách* với hàng *Criteria*, cần viết rõ mã sách này là “VH-01” giống như ở Hình 4; chạy thử để kiểm tra.
*   c) Chuyển thành truy vấn có tham số; chạy thử; kiểm tra kết quả và ghi lưu với tên “q-NhậnTrả”.

Giả sử thư viện có quy định một bạn đọc không được mượn và giữ quá 5 cuốn sách. Hãy thiết kế truy vấn giúp thủ thư kiểm tra điều kiện này khi có một bạn đọc muốn mượn sách.

*   Câu 1. Thao tác nào sẽ mở vùng làm việc thiết kế truy vấn?
*   Câu 2. Truy vấn có tham số là gì? Lời nhắc điền tham số viết ở đâu?
*   Câu 3. Truy vấn hành động là gì? Tại sao cần rất thận trọng khi thực hiện nó?

## Tóm tắt bài học

*   Trình tiện ích **Query Design** cho phép chọn các bảng (hay truy vấn khác) và lấy ra các trường dữ liệu cần có; mỗi cột trong lưới **QBE** ứng với một trường dữ liệu (cột trong bảng) được chọn.
*   Hàng **Sort** trong lưới **QBE** để sắp xếp thứ tự theo giá trị dữ liệu trường.
*   Hàng **Criteria** để viết biểu thức logic chọn các bản ghi mong muốn; dùng phép toán **AND** kết hợp điều kiện cho các trường khác nhau.
*   Hàng **Or** để viết biểu thức dùng phép toán **OR** kết hợp điều kiện cho các trường khác nhau.
