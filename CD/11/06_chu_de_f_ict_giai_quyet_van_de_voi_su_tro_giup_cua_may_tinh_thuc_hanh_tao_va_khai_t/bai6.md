# Bài 6: TẠO BÁO CÁO ĐƠN GIẢN

Học xong bài này, em sẽ:
* Thực hiện được việc kết xuất thông tin từ CSDL.
* Tìm hiểu được thêm một vài chức năng của hệ quản trị CSDL.

Theo em hiểu "làm báo cáo" nghĩa là gì?

## 1) Xây dựng báo cáo đơn giản
### a) Các loại báo cáo

Xây dựng báo cáo là khâu quan trọng cuối cùng hoàn tất việc kết xuất thông tin từ CSDL phục vụ người dùng. Báo cáo nhằm đáp ứng yêu cầu thông tin của cấp quản lí cơ quan, doanh nghiệp. Mỗi khi chạy thực thi báo cáo, thông tin được kết xuất từ dữ liệu cập nhật mới nhất. Khác với biểu mẫu, người xem báo cáo không sửa đổi được các mục dữ liệu.

Một báo cáo **chi tiết** hiển thị tất cả các bản ghi đã chọn, được phân nhóm và sắp xếp, có thể thêm số liệu tóm tắt mỗi nhóm ví dụ như: tổng con, số đếm, tỉ lệ phần trăm,... Cuối báo cáo thường có các số liệu tổng hợp toàn bộ.

Một báo cáo **tóm tắt** không liệt kê các bản ghi đã chọn, chỉ trình bày các số liệu tổng hợp nhóm theo một chiều nào đó. Ví dụ, tổng hợp theo tháng, theo quý, theo năm (chiều thời gian); tổng hợp theo các chi nhánh khác nhau: Hà Nội, Hải Phòng, Đà Nẵng, Thành phố Hồ Chí Minh,... (chiều địa điểm).

Một báo cáo **tóm tắt phân tích nhiều chiều** dựa trên một mẫu truy vấn riêng tạo bằng *Crosstab Query Wizard*. Ví dụ, báo cáo phân tích theo cả hai chiều, thời gian (theo tháng, theo quý, theo năm) và theo các chi nhánh ở nhiều địa phương khác nhau.

Báo cáo được xây dựng dựa trên nguồn dữ liệu là bảng hay truy vấn. Để xây dựng báo cáo, cần biết sẽ dùng đến những trường dữ liệu nào và nên chuẩn bị sắp xếp, chọn lọc sẵn từ trước bằng một truy vấn.

### b) Truy vấn chuẩn bị dữ liệu

Giả sử ta cần làm báo cáo chi tiết hoạt động mượn trả sách của thư viện theo từng tháng, cho biết mỗi tháng có bao nhiêu giao dịch mượn sách và đồng thời phân tích số liệu theo **loại sách** được mượn. Cần thiết kế truy vấn lấy dữ liệu từ các bảng **Mượn-Trả** và bảng **Sách** (để có trường **Loại sách**).

*(Mô tả truy vấn)*: Ảnh minh họa một truy vấn được thiết kế để chuẩn bị báo cáo chi tiết. Truy vấn này kết hợp dữ liệu từ hai bảng "Mượn-Trả" và "Sách" thông qua liên kết giữa chúng. Các trường được chọn bao gồm ID, Số thẻ, Mã sách, Ngày mượn, Ngày trả từ bảng "Mượn-Trả", và Mã sách, Tên sách, Sẵn có, Số trang từ bảng "Sách". Một trường tính toán mới tên "Month" được tạo để trích xuất tháng từ trường "Ngày mượn".

Chú ý các chi tiết trong truy vấn:
*   Sắp xếp theo **Ngày mượn** là để nhóm theo từng tháng.
*   Gõ nhập trực tiếp cho cột “Month: Month([Ngày mượn])” để trích ra phần “tháng” từ **Ngày mượn**.

Ghi lưu truy vấn, ví dụ với tên là “q-MượnTrả-Month”.

### c) Tạo nhanh báo cáo đơn giản

*   Bước 1. Mở truy vấn “q-MượnTrả-Month” (hoặc chỉ cần đánh dấu chọn).
*   Bước 2. Nháy chọn Create\Report sẽ tạo một báo cáo.
*   Bước 3. Ghi lưu với tên “MượnTrả-Month”.

Đây là báo cáo chi tiết, hiển thị đầy đủ các bản ghi. Sau đó có thể thêm gộp nhóm và thông tin tóm tắt theo nhóm.

## 2) Hướng dẫn sử dụng Report Wizard

Trình tiện ích **Report Wizard** hỗ trợ tạo báo cáo và cho phép lựa chọn tuỳ biến theo yêu cầu.

*   Bước 1. Nháy chuột chọn Create\Report Wizard.

Bước 2. Chọn bảng hoặc truy vấn làm nguồn dữ liệu cơ sở cho báo cáo. Ví dụ, chọn bảng Mượn-Trả.
Bước 3. Chọn các trường dữ liệu cần báo cáo. Ví dụ **Số thẻ, Mã sách, Ngày Mượn**; nháy vào dấu ">" để chuyển sang hộp Selected Fields); nháy Next khi đã chọn đủ các trường dữ liệu cần có.
Bước 4. Chọn gộp nhóm theo trường dữ liệu nào. Ví dụ, chọn nhóm theo **Số thẻ** tức là nhóm theo từng bạn đọc; nháy Next.
Bước 5. Chọn một bài trí cơ sở cho báo cáo. Lựa chọn mặc định là “Tabular” nhưng có thể thay đổi nếu muốn; nháy Next.
Bước 6. Nhập tên báo cáo trước khi chọn **Finish**. Nên đặt tên gợi nhớ nội dung báo cáo. Ví dụ, “MượnTrả-theoBạnđọc”.

Sau khi được tạo ra, biểu tượng của báo cáo sẽ xuất hiện trong vùng điều hướng. Ta có thể mở ra bất cứ lúc nào để chỉnh sửa lại thiết kế theo mong muốn hoặc cho chạy để lấy thông tin mới cập nhật.

## Gộp nhóm, sắp xếp và các tổng con

Gộp nhóm các bản ghi là để tóm tắt dữ liệu nhằm hiển thị **tổng con** (hay giá trị trung bình, giá trị cực tiểu, giá trị cực đại) cho mỗi trường dữ liệu kiểu số của từng nhóm bản ghi (nhóm hàng). Sau khi gộp nhóm thì dữ liệu từng nhóm xuất hiện trong phần Detail. Ví dụ, ta muốn tóm tắt hoạt động mượn trả theo từng tháng.

**Hướng dẫn thực hiện:**
*   **Bước 1.** Mở báo cáo chi tiết “MượnTrả-Month” trong khung nhìn thiết kế. Nháy vào lệnh **Group & Sort** trong vùng nút lệnh. Cửa sổ Group, Sort, and Total xuất hiện ở đáy màn hình.

Bước 2. Nháy nút lệnh Add a group; nháy vào mũi tên trỏ xuống cạnh selected field; tiếp tục nháy chọn Month.
Bước 3. Access gợi ý sắp xếp tăng dần “from smallest to largest”. Bỏ qua vì ta đã sắp xếp theo Ngày mượn khi truy vấn.
Bước 4. Nháy mũi tên More để thấy các lựa chọn tóm tắt dữ liệu (nếu chưa thấy). Access đưa ra gợi ý sẵn, thường là đã phù hợp. Tuy nhiên, ta có thể thay đổi nếu không đúng yêu cầu. Ví dụ, nháy mũi tên xuống và chọn Total On: Số thẻ, chọn kiểu Type: Count Values.
Bước 5. Đánh dấu chọn cách hiển thị, ví dụ Show Grand Total và Show subtotal in group header.
Bước 6. Ghi lưu với tên “MượnTrả-TheoTháng”. Chuyển sang khung nhìn báo cáo để xem kết quả.

## Thực hành tạo báo cáo đơn giản

### Nhiệm vụ 1. Theo hướng dẫn chi tiết từng bước trong bài học, thực hiện các việc sau:
*   a) Tạo truy vấn dữ liệu làm nguồn dữ liệu cho báo cáo.
*   b) Tạo báo cáo đơn giản bằng nút lệnh **Report**; ghi lưu kết quả thành báo cáo “MượnTrả-Month”.

### Nhiệm vụ 2. Sử dụng báo cáo vừa tạo ở Bài 1, thực hiện các việc sau:
*   a) Mở báo cáo “MượnTrả-Month”.
*   b) Lặp lại từng bước theo hướng dẫn để gộp nhóm theo tháng, tính các tổng con và xác định cách hiển thị. Kiểm tra kết quả. Ghi lưu.

## Luyện tập

Em hãy thiết kế truy vấn làm cơ sở để báo cáo chi tiết từng bạn đọc mượn sách trong năm học.
*Gợi ý: Lấy dữ liệu từ hai bảng Bạn Đọc và bảng Mượn-Trả, sắp xếp theo Số thẻ.*

Câu 1. Báo cáo chi tiết khác với báo cáo tóm tắt ở điểm nào?
Câu 2. Khi nào nên dùng nút lệnh tạo báo cáo nhanh? Khi nào nên dùng công cụ **Report Wizard**?

## Tóm tắt bài học

*   Lệnh **Report** giúp dễ dàng tạo báo cáo chi tiết có phân nhóm dựa trên truy vấn có sắp xếp kết quả thích hợp.
*   Trình tiện ích **Report Wizard** hỗ trợ tạo báo cáo lấy dữ liệu từ nhiều bảng hay truy vấn, có các tuỳ chọn sắp xếp và bài trí đa dạng.
*   Trong khung nhìn thiết kế báo cáo, nhóm lệnh **Group & Sort** hỗ trợ phân nhóm, sắp xếp và thêm các loại tổng con.

## BÀI TÌM HIỂU THÊM

### BÁO CÁO PHÂN TÍCH NHIỀU CHIỀU

Truy vấn **Crosstab Query Wizard** là tiện ích tạo truy vấn tóm tắt nguồn dữ liệu lớn, phức tạp, đáp ứng yêu cầu tổng hợp số liệu và phân tích theo nhiều cách. Access có sẵn nhiều hàm gộp để tổng hợp số liệu như: *Sum, Count, Min, Max, Avg* (tính trung bình), được dùng trong mẫu truy vấn đặc thù này. Báo cáo phân tích nhiều chiều dựa trên truy vấn crosstab. Đó là một báo cáo tóm tắt hoạt động của thư viện theo tháng, có phân tích theo loại sách: "TH" là Tin học, "Khác" là không phải Tin học.
