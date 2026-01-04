# CHỦ ĐỀ A: MÁY TÍNH VÀ XÃ HỘI TRI THỨC, THẾ GIỚI THIẾT BỊ SỐ, HỆ ĐIỀU HÀNH VÀ PHẦN MỀM ỨNG DỤNG
# BÀI 1: BÊN TRONG MÁY TÍNH
*   Học xong bài này, em sẽ:
    *   Nhận biết được sơ đồ của các mạch logic AND, OR, NOT; giải thích được vai trò của các mạch logic trong thực hiện các tính toán nhị phân.
    *   Nêu được tên, nhận diện được hình dạng, mô tả được chức năng và giải thích được đơn vị đo hiệu năng của các bộ phận chính bên trong máy tính.
    *   Em hãy cho biết CPU là gì và làm nhiệm vụ gì trong máy tính?
## Các cổng logic và tính toán nhị phân
### a) Cổng logic
*   Trong máy tính, một bóng bán dẫn chỉ thực hiện được chức năng bật hoặc tắt mạch đơn giản, tương ứng với hai giá trị 0 và 1. Mỗi cách kết hợp các bóng bán dẫn tạo ra một cổng logic. Các cổng logic là thành phần cơ bản thực hiện mọi tính toán trong máy tính.
*   Các hướng dẫn liên quan đến mạch điện:
    *   Quan sát mạch điện ở Hình 1. Mạch có hai công tắc A và B phối hợp để điều khiển đèn F. Đèn chỉ sáng khi cả hai công tắc cùng đóng.
    *   Nếu quy ước: công tắc mở tương ứng với mức “0”, công tắc đóng tương ứng với mức “1”; đèn tắt tương ứng với mức “0”, đèn sáng tương ứng với mức “1”. Em hãy:
        *   1) Nêu giá trị đúng tại dấu ? cho mỗi hàng của đầu ra F.
        *   2) Nhận xét về hoạt động của mạch điện.
*   Ta thấy rằng: Để đèn F sáng thì cả công tắc A và công tắc B đồng thời phải đóng, nếu một trong hai công tắc mở thì đèn F tắt. Hoạt động của mạch điện minh hoạ chức năng của cổng logic AND và bảng hoạt động tương ứng của mạch điện được gọi là bảng chân lí. Cổng AND thực hiện chức năng nhân logic.
*   Để thực hiện các phép toán logic khác, ta cần có thêm nhiều loại cổng logic. Dựa trên quan hệ giữa đầu ra và đầu vào, các cổng logic được đặt tên tương ứng là cổng AND, cổng OR, cổng NOT, cổng XOR,... Bảng 1 dưới đây liệt kê một số loại cổng logic thông dụng.
*   Thực hiện phép toán nhị phân với mạch logic: Các phép toán trên hệ nhị phân cũng có nguyên tắc thực hiện giống như trên hệ thập phân. Ví dụ nguyên tắc cơ bản để cộng hai số nhị phân như ở Hình 2.
*   Các ví dụ về phép cộng nhị phân:
    *   0 + 0 = 0 (Bằng 0, nhớ 0)
    *   1 + 0 = 1 (Bằng 1, nhớ 0)
    *   0 + 1 = 1 (Bằng 1, nhớ 0)
    *   1 + 1 = 10 (Bằng 10 (Bằng 0, nhớ 1))
*   Giả sử ta cộng hai số nhị phân 1 bit là A với B được tổng là S và nhớ là C. Vì là các số nhị phân nên A và B chỉ nhận các giá trị là 0 hoặc 1, lập bảng các trường hợp có thể xảy ra với các đầu vào A, B và điền giá trị đầu ra S, C tương ứng, ta có bảng chân lí mạch cộng hai số nhị phân 1 bit (Bảng 2).
*   So sánh Bảng 2 với bảng chân lí của các cổng logic trong Bảng 1 để thấy tổng S = A XOR B và nhớ C = A AND B.
*   Từ đó, lập được sơ đồ mạch logic để thực hiện phép cộng hai số nhị phân 1 bit.
*   Phép cộng hai số nhị phân dài nhiều bit thực hiện bằng cách cộng lần lượt từng cặp bit từ phải sang trái và có bit nhớ (C_in) mang sang cột kề bên trái.
*   Mạch cộng đầy đủ (FA – Full Adder) có ba đầu vào là A, B và bit nhớ mang sang C_in, có hai đầu ra là bit tổng S và bit nhớ C_out để phân biệt với C_in đầu vào.
*   Mạch cộng đầy đủ là ghép nối hai mạch cộng 1 bit.
*   Bằng cách kết hợp các cổng logic AND, XOR, máy tính có thể thực hiện được phép tính cộng nhị phân.
*   Các cổng logic cơ bản cũng có thể kết hợp để tạo thành các mạch logic thực hiện tất cả các tính toán nhị phân khác.
## Những bộ phận chính bên trong máy tính
*   Theo em, bộ phận nào của máy tính là quan trọng nhất?
*   Máy tính có nhiều loại như: máy tính để bàn, máy tính xách tay, máy tính bảng.
*   Bên trong thân máy tính được cấu thành từ các bộ phận chính gồm: bảng mạch chính, CPU, RAM, ROM, thiết bị lưu trữ.
*   Tốc độ và dung lượng của chúng ảnh hưởng lớn tới hiệu năng của máy.
### Bảng mạch chính
*   Bảng mạch chính có để cắm CPU, ROM, các khe cắm RAM, các khe cắm ổ cứng và một số khe cắm khác.
*   Bảng mạch chính đóng vai trò làm nền giao tiếp giữa CPU, RAM và các linh kiện điện tử khác.
*   Bảng mạch chính phục vụ cho việc kết nối với các thiết bị ngoại vi.
### CPU (Central Processing Unit – bộ xử lí trung tâm)
*   Đóng vai trò bộ não của máy tính.
*   Đảm nhiệm công việc tìm nạp lệnh, giải mã lệnh và thực thi lệnh cho máy tính.
### RAM (Random Access Memory – bộ nhớ truy cập ngẫu nhiên)
*   Lưu trữ dữ liệu tạm thời trong quá trình tính toán của máy tính.
*   Dữ liệu sẽ bị mất khi máy tính bị mất điện hoặc khởi động lại.
### ROM (Read Only Memory – bộ nhớ chỉ đọc)
*   Lưu trữ chương trình giúp khởi động các chức năng cơ bản của máy tính.
### Thiết bị lưu trữ
*   Dùng để lưu trữ dữ liệu lâu dài và không bị mất đi khi máy tính tắt nguồn.
*   Ngày nay, máy tính thường sử dụng ổ cứng HDD, ổ cứng SSD hoặc ổ USB để lưu trữ dữ liệu.
*   Dung lượng lưu trữ dữ liệu của máy tính là tổng dung lượng của ổ cứng HDD, ổ cứng SSD gắn sẵn bên trong máy tính, không bao gồm dung lượng lưu trữ của RAM.
*   Hiện nay, dung lượng lưu trữ của máy tính có thể lên tới hàng TB.
### Hiệu năng của máy tính
*   Hiệu năng của máy tính phụ thuộc vào thông số kĩ thuật của từng bộ phận và sự đồng bộ giữa chúng.
*   Có thể đánh giá nhanh hiệu năng của máy thông qua tốc độ CPU, dung lượng bộ nhớ RAM.
#### Thông số kĩ thuật cần quan tâm của CPU gồm:
*   Tốc độ của CPU: đo bằng Hz (Hertz), biểu thị số chu kì xử lí mỗi giây mà CPU có thể thực hiện được. Tốc độ này càng cao thì máy tính chạy càng nhanh. Hiện nay, CPU có tốc độ hàng GHz (1 GHz = 10^9 Hz).
*   Số lượng nhân hay lõi (core): CPU có cấu tạo gồm một hoặc nhiều nhân (còn gọi là lõi) vật lí. Với cùng một công nghệ sản xuất, CPU có nhiều nhân hơn thì hiệu năng, khả năng đa nhiệm và tốc độ xử lí tốt hơn.
#### Thông số kĩ thuật cần quan tâm của RAM là dung lượng.
*   Dung lượng của RAM được đo bằng đơn vị Byte.
*   Hiện nay, máy tính có RAM với dung lượng hàng GB (1 GB = 2^30 Byte).
*   Máy tính có RAM với dung lượng lớn hơn thì hiệu năng cao hơn.
*   **Câu 1. Em hãy nêu giá trị thích hợp tại dấu ? cho hai cột S và Cout để hoàn thành bảng chân lí cho mạch cộng đầy đủ (Bảng 4).**
*   **Câu 2. Hãy nêu tên một số thành phần chính bên trong máy tính và cho biết chức năng của nó.**
    *   Em hãy sắp xếp thứ tự ưu tiên khi chọn mua máy tính:
        *   a) Ổ cứng dung lượng lớn.
        *   b) RAM dung lượng lớn.
        *   c) CPU tốc độ cao.
    *   Trong các câu sau, những câu nào đúng?
        *   a) CPU có tốc độ càng cao thì máy tính có hiệu năng càng cao.
        *   b) Dung lượng ổ cứng đo bằng GHz.
        *   c) Các bộ nhớ RAM ngày nay có dung lượng hàng TB.
        *   d) Dung lượng RAM có ảnh hưởng tới hiệu năng của máy tính.
### Tóm tắt bài học
*   Bằng cách kết hợp các cổng logic cơ bản để tạo thành các mạch logic, máy tính có thể thực hiện được các tính toán nhị phân.
*   Các bộ phận chính bên trong thân máy tính gồm: bảng mạch chính, CPU, RAM, ROM, thiết bị lưu trữ.
*   Hiệu năng của máy tính được quyết định bởi hiệu năng của từng thành phần, trong đó CPU, RAM có vai trò quan trọng nhất. Ngày nay, CPU có tốc độ hàng GHz, bộ nhớ RAM có dung lượng hàng GB, ổ cứng có dung lượng hàng TB.
## Thiết kế giao diện của ứng dụng quản lí thư viện trường
*   Dưới đây tóm tắt ngắn gọn vài điểm về quy trình tác nghiệp của thư viện và các biểu mẫu, báo cáo liên quan.
### a) Các biểu mẫu
*   Khi bạn đọc đến thư viện tìm sách để mượn, thao tác “tìm sách” sử dụng biểu mẫu TìmSách để hiển thị thông tin về sách có sẵn.
*   Khi bạn đọc yêu cầu mượn một cuốn sách, thao tác “cho mượn” sử dụng biểu mẫu ChoMượn để thủ thư cập nhật các trường Số thẻ, Mã sách, Ngày mượn trong bảng Mượn-Trả và trường Sẵn có trong bảng Sách.
*   Quy tắc nghiệp vụ cần tuân thủ khi cho mượn: Bỏ đánh dấu cuốn sách vừa cho mượn là sẵn có.
*   Khi bạn đọc đến trả một cuốn sách, thao tác “nhận trả” sử dụng biểu mẫu để thủ thư cập nhật các trường Số thẻ, Mã sách, Ngày mượn, Ngày trả trong bảng Mượn-Trả và trường Sẵn có trong bảng Sách.
*   Quy tắc nghiệp vụ cần tuân thủ khi nhận trả: Đánh dấu cuốn sách vừa nhận trả là sẵn có.
*   Có thể thêm các biểu mẫu để nhập dữ liệu cho bảng Bạn đọc, bảng Sách.
*   Quy ước khi nhập một cuốn sách mới vào kho sách thì trường Sẵn có mặc định nhận giá trị là Yes.
*   Lưu ý: Nếu biết lập trình, có thể thiết lập việc thực thi các quy tắc trên để tránh trường hợp làm sai, gây ra dữ liệu có mâu thuẫn, không nhất quán.
### b) Các báo cáo
*   Báo cáo thống kê hoạt động mượn trả, ví dụ theo tháng, được gọi là báo cáo MượnTrả-TheoTháng.
*   Báo cáo phân tích mượn trả theo tháng và theo loại sách, được gọi là báo cáo MượnTrả-Tháng-LoạiSách.
*   Có thể thêm những báo cáo thống kê khác, ví dụ thống kê theo bạn đọc và số đầu sách đã mượn.
## Bảng điều khiển trung tâm của ứng dụng quản lí thư viện trường
*   Ví dụ thiết kế biểu mẫu điều hướng:
    *   Nhãn tiêu đề: “Thư viện Trường THPT...”
    *   Bố cục: *Horizontal Tabs*.
    *   Các thẻ đầu tiên là các biểu mẫu, sau đó là các báo cáo.
## Thực hành tổng hợp
### Nhiệm vụ 1.
# Tạo và chỉnh sửa bài trí biểu mẫu điều hướng
*   Làm theo các bước hướng dẫn thao tác tạo biểu mẫu điều hướng.
*   Kéo thả các biểu mẫu và báo cáo từ vùng điều hướng vào các ô *Add New* theo bố cục như trong ví dụ đã nêu.
*   Đổi tiêu đề biểu mẫu điều hướng.
*   Đổi tên trong thẻ của các biểu mẫu, báo cáo. Ví dụ: *Tìm Sách, Cho Mượn, Nhận trả* (có khoảng trắng, có dấu tiếng Việt, kiểu dáng chữ,...).
*   Chú ý quan sát thấy tên đối tượng trong vùng điều hướng không thay đổi.
## Nhiệm vụ 2. Hoàn thiện biểu mẫu một bản ghi để nhập dữ liệu cho bảng *Bạn đọc*; thử nhập dữ liệu cho trường *Ảnh*.
## Nhiệm vụ 3. Thử xuất ra một báo cáo.
*   Gợi ý: Mở báo cáo trong khung nhìn *Print Preview* sẽ thấy nhiều nút lệnh để in ra giấy, chuyển thành tệp Excel, chuyển thành tệp “pdf”,...
*   Hoàn tất ứng dụng quản lí thư viện theo yêu cầu sử dụng thực tế.
## Câu hỏi
*   Câu 1. Biểu mẫu điều hướng dùng để làm gì và chứa những gì?
*   Câu 2. Thao tác thiết lập biểu mẫu điều hướng làm bàn điều khiển trung tâm của ứng dụng gồm mấy bước? Bắt đầu bằng thao tác nào?
## Tóm tắt bài học
*   Những công việc chính để hoàn tất ứng dụng là:
    *   Thiết kế giao diện, bài trí các nút lệnh phù hợp với quy trình nghiệp vụ quản lí CSDL và cung cấp dịch vụ.
    *   Tạo một biểu mẫu điều hướng và thực hiện các thiết kế giao diện như trên, chỉnh sửa lại các nhãn tiêu đề, chạy thử kiểm tra.
    *   Thiết lập biểu mẫu điều hướng làm bàn điều khiển trung tâm của ứng dụng.
*   **Câu 1:** Em hãy nêu giá trị thích hợp tại dấu ? cho hai cột S và C_out để hoàn thành bảng chân lí cho mạch cộng đầy đủ (Bảng 4).
*   (Phần Bảng 4. Bảng chân lí mạch cộng đầy đủ đã được bỏ qua theo yêu cầu xử lý.)
*   **Câu 2:** Hãy nêu tên một số thành phần chính bên trong máy tính và cho biết chức năng của nó.
*   Em hãy sắp xếp thứ tự ưu tiên khi chọn mua máy tính:
    *   a) Ổ cứng dung lượng lớn.
    *   b) RAM dung lượng lớn.
    *   c) CPU tốc độ cao.
*   Trong các câu sau, những câu nào đúng?
    *   a) CPU có tốc độ càng cao thì máy tính có hiệu năng càng cao.
    *   b) Dung lượng ổ cứng đo bằng GHz.
    *   c) Các bộ nhớ RAM ngày nay có dung lượng hàng TB.
    *   d) Dung lượng RAM có ảnh hưởng tới hiệu năng của máy tính.
## Tóm tắt bài học
*   Bằng cách kết hợp các cổng logic cơ bản để tạo thành các mạch logic, máy tính có thể thực hiện được các tính toán nhị phân.
*   Các bộ phận chính bên trong thân máy tính gồm: bảng mạch chính, CPU, RAM, ROM, thiết bị lưu trữ.
*   Hiệu năng của máy tính được quyết định bởi hiệu năng của từng thành phần, trong đó CPU, RAM có vai trò quan trọng nhất. Ngày nay, CPU có tốc độ hàng GHz, bộ nhớ RAM có dung lượng hàng GB, ổ cứng có dung lượng hàng TB.
# BÀI 2 KHÁM PHÁ THẾ GIỚI THIẾT BỊ SỐ THÔNG MINH
## Học xong bài này, em sẽ:
*   Đọc hiểu được một số điểm chính trong tài liệu hướng dẫn về thiết bị số thông dụng.
*   Thực hiện được một số chỉ dẫn trong tài liệu đó.
*   Đọc hiểu và giải thích được một vài thông số cơ bản của các thiết bị số thông dụng.
*   Em đã sử dụng các thiết bị số của mình như thế nào? Theo em, sử dụng như thế đã đúng cách chưa?
## Sử dụng đúng cách các thiết bị số
*   Hiện nay các loại thiết bị kĩ thuật số mới xuất hiện thêm mỗi ngày.
*   Các thiết bị đã phổ biến cũng liên tục được đổi mới, thế hệ sau có nhiều tính năng hiện đại hơn thế hệ trước.
*   Để biết sử dụng thiết bị số kiểu mới, thế hệ mới đúng cách, không làm hỏng và khai thác tốt nhất các tính năng thiết bị, cần đọc kĩ và thực hiện theo đúng hướng dẫn sử dụng ngay từ bước lắp đặt, thiết lập ban đầu và tiếp tục trong quá trình sử dụng sau này.
## Quan sát, em hãy:
*   Phân biệt mục đích của thông điệp CẢNH BÁO và THẬN TRỌNG.
*   Thực hiện theo các bước của hướng dẫn.
## Quy trình vệ sinh
*   Thực hiện theo các quy trình trong phần này để vệ sinh máy tính của bạn một cách an toàn.
### CẢNH BÁO!
Để ngăn ngừa điện giật hoặc hư hỏng cho các linh kiện, không cố gắng làm sạch máy tính của bạn khi máy đang bật.
1. Tắt máy tính.
2. Ngắt kết nối nguồn AC.
3. Ngắt kết nối với tất cả các thiết bị đang chạy bằng điện bên ngoài.
### THẬN TRỌNG:
Để tránh gây hư hỏng cho các cấu phần bên trong, không phun chất tẩy rửa hoặc chất lỏng trực tiếp lên bất kỳ bề mặt nào của máy tính. Chất lỏng nhỏ giọt trên bề mặt có thể gây tổn hại vĩnh viễn cho các cấu phần bên trong.
## Làm sạch màn hình
*   Nhẹ nhàng lau sạch màn hình bằng vải mềm không có xơ vải và được làm ẩm bằng nước lau kính không chứa cồn.
*   Đảm bảo rằng màn hình đã khô trước khi đóng máy tính lại.
*   **Hình 1. Một nội dung trong hướng dẫn sử dụng máy tính**
*   Tài liệu hướng dẫn sử dụng thiết bị số thường có các mục sau:
    *   Hướng dẫn an toàn (Safety): nhằm mục đích ngăn chặn các rủi ro hoặc hư hỏng không thể lường trước khi vận hành sản phẩm không đúng cách.
    *   Lắp đặt/thiết đặt (Setup): hướng dẫn lắp ráp hoặc thiết đặt thông số ban đầu cho thiết bị.
    *   Vận hành (Operation): hướng dẫn sử dụng các tính năng chính của thiết bị.
    *   Bảo trì (Maintenance): hướng dẫn vệ sinh, chăm sóc kĩ thuật,... nhằm đảm bảo sự hoạt động bình thường của thiết bị.
    *   Xử lí sự cố (Troubleshooting): hướng dẫn chẩn đoán và xử lí sơ bộ các lỗi thường gặp của thiết bị.
    *   Thông tin về nơi để tìm thêm sự trợ giúp và chi tiết liên hệ (Support).
## Thông số kĩ thuật của thiết bị số
*   Quan sát các thiết bị, em thấy chúng có các bộ phận nào giống nhau?
*   Các thiết bị số rất đa dạng, các bộ phận xử lí dữ liệu số của chúng cũng tương tự như của máy tính. Các thông số kĩ thuật quan trọng là tốc độ bộ vi xử lí CPU, dung lượng RAM, dung lượng lưu trữ. Các thông số kĩ thuật khác nhau tuỳ vào chức năng của thiết bị.
*   Ngoài bộ phận xử lí dữ liệu số tích hợp sẵn (nếu có), các thiết bị số để nhập dữ liệu hay xuất thông tin cho con người sử dụng như: máy in, máy chiếu, màn hình, loa, micro, camera,... có những thông số kĩ thuật quan trọng khác tuỳ theo chức năng.
## Kích thước màn hình
*   Màn hình hiển thị hình ảnh hình chữ nhật thường được quy định tiêu chuẩn hoá tỉ lệ giữa chiều dài và chiều rộng, ví dụ 4:3, 16:9, 21:9.
*   Kích thước màn hình thường được thể hiện bằng độ dài đường chéo của nó, đơn vị đo là inch (1 inch tương đương 2.54 cm).
*   Hiện nay, màn hình điện thoại thường có kích thước 4 inch – 6.5 inch, màn hình laptop thường có kích thước 13.3 inch – 17 inch, còn ti vi thường có kích thước 40 inch – 65 inch.
## Độ phân giải hình ảnh
*   Hình ảnh số hoá được tạo nên từ các điểm ảnh rất nhỏ gọi là pixel (picture element).
*   Độ phân giải điểm ảnh thể hiện bằng cặp hai số đếm điểm ảnh theo chiều ngang và theo chiều cao.
*   Tích hai số này là số điểm ảnh của hình ảnh.
*   Một triệu điểm ảnh là một megapixel.
*   Hình ảnh càng nhiều điểm ảnh thì càng rõ nét.
*   Điện thoại thông minh hiện nay có camera với độ phân giải lên đến vài chục megapixel.
## Các câu hỏi và bài tập
*   Em hãy tính số đo bằng centimet theo chiều dài và chiều rộng của màn hình máy tính có kích thước 24", 27", 32" tương ứng với tỉ lệ 16:9 và 21:9.
*   Tìm hiểu cấu hình của một điện thoại thông minh. Em hãy cho biết kích thước màn hình, tốc độ CPU, dung lượng RAM, dung lượng lưu trữ, độ phân giải camera của điện thoại đó.
## Câu 1. Trong tài liệu hướng dẫn sử dụng thiết bị số:
*   a) Mục “Hướng dẫn an toàn” nhằm mục đích gì?
*   b) Mục “Xử lí sự cố” thường hướng dẫn những gì?
## Câu 2.
Tại sao kích thước màn hình của các thiết bị điện tử thường được thể hiện bằng số đo độ dài đường chéo?
## Câu 3.
Nói “Camera có độ phân giải 12 megapixel” nghĩa là gì?
## Tóm tắt bài học
*   Tài liệu hướng dẫn sử dụng thiết bị số giúp ta sử dụng an toàn và đúng cách thường có nội dung gồm các mục: hướng dẫn an toàn, lắp đặt/thiết đặt, vận hành, bảo trì, xử lí sự cố, thông tin hỗ trợ khách hàng.
*   Các thông số kĩ thuật quan trọng về xử lí dữ liệu số: tốc độ CPU, dung lượng RAM, dung lượng lưu trữ.
*   Các thông số kĩ thuật quan trọng về hình ảnh kĩ thuật số: độ dài đường chéo màn hình, độ phân giải hình ảnh.
# Chủ đề bài học: BÀI 3. KHÁI QUÁT VỀ HỆ ĐIỀU HÀNH
## Học xong bài này, em sẽ:
*   Trình bày được một cách khái quát mối quan hệ giữa phần cứng, hệ điều hành và phần mềm ứng dụng.
*   Nêu được sơ lược lịch sử phát triển, vai trò và chức năng cơ bản của hai hệ điều hành thông dụng.
*   Trình bày được sơ lược về một số hệ điều hành tiêu biểu.
*   Sử dụng được một số tiện ích có sẵn của hệ điều hành để nâng cao hiệu suất sử dụng máy tính.
## Câu hỏi thảo luận:
*   Khi mua một máy tính mới, máy tính bảng hay điện thoại thông minh, trước khi bắt đầu sử dụng cần kích hoạt chế độ cài đặt. Tại sao cần làm việc này và những gì sẽ được cài đặt vào máy?
## Mục: ① Hệ điều hành, vai trò và chức năng của hệ điều hành
### Câu hỏi mở đầu mục:
*   Khi bật máy tính, ta phải chờ một lúc rồi mới có thể bắt đầu công việc. Với điện thoại thông minh có khác biệt gì không?
# Hệ điều hành (Operating System)
## 1. Định nghĩa Hệ điều hành (OS)
### 1.1. Khái niệm
Là tập các chương trình điều khiển và xử lí tạo giao diện trung gian giữa các thiết bị của hệ thống với phần mềm ứng dụng, đồng thời quản lí các thiết bị của hệ thống, phân phối tài nguyên và điều khiển các quá trình xử lí trong hệ thống.
## 2. Phân loại phần mềm
### 2.1. Phần mềm ứng dụng
Các phần mềm để soạn thảo văn bản, duyệt web, xử lí hình ảnh, viết chương trình bằng ngôn ngữ Python,... Đây là các phần mềm ứng dụng.
*   Các phần mềm ứng dụng chạy trên nền tảng OS nào cần phù hợp với OS đó. Ví dụ, phần mềm xử lí ảnh trên nền tảng Windows khác với phần mềm cùng chức năng trên nền tảng Android hay iOS.
### 2.2. Phần mềm hệ thống
Các phần mềm thiết kế cho việc vận hành và điều khiển phần cứng máy tính là các phần mềm hệ thống, ví dụ như các trình điều khiển thiết bị.
## 3. Vai trò của hệ điều hành
*   Hệ điều hành (OS) điều phối tất cả các thiết bị, làm trung gian giữa phần mềm ứng dụng và phần cứng.
*   Hệ điều hành cũng là trung gian giữa người dùng máy tính và thiết bị phần cứng, giúp dễ dàng sử dụng thiết bị mà không cần biết sâu về kĩ thuật công nghệ.
*   Hệ điều hành giúp người dùng dễ dàng cài đặt, gỡ bỏ phần mềm ứng dụng theo nhu cầu.
## 4. Các chức năng cơ bản của hệ điều hành
### 4.1. Quản lí tệp
Tạo và tổ chức lưu trữ các tệp trên bộ nhớ ngoài, cung cấp các công cụ để tìm kiếm và truy cập các tệp, chia sẻ và bảo vệ tệp.
### 4.2. Quản lí, khai thác các thiết bị của hệ thống
Hệ điều hành tự nhận biết có thiết bị ngoại vi mới được kết nối với máy tính qua các cổng vào – ra như: USB, HDMI, Datamini Port, Bluetooth,... và tự động bổ sung các chương trình điều khiển vào hệ thống. Người dùng có thể sử dụng các thiết bị đó ngay sau khi thiết bị kết nối với hệ thống. Hệ điều hành sẽ tự động ngắt kết nối khi tháo thiết bị khỏi hệ thống.
### 4.3. Quản lí tiến trình
Các phần mềm ứng dụng xử lí dữ liệu thông qua nhiều tiến trình, mỗi tiến trình làm một việc nhất định. Hệ điều hành tạo ra các tiến trình, điều khiển giao tiếp giữa các tiến trình để phối hợp nhịp nhàng hoàn thành nhiệm vụ. Hệ điều hành hủy bỏ tiến trình khi nó kết thúc công việc.
### 4.4. Cung cấp phương thức giao tiếp
Để người dùng điều khiển máy tính bằng câu lệnh hoặc qua giao diện đồ họa hay dùng tiếng nói.
### 4.5. Bảo vệ hệ thống
Hệ điều hành có cơ chế nhằm bảo vệ hệ thống và thông tin lưu trữ, hạn chế tối đa ảnh hưởng của các sai lầm do vô tình hay cố ý.
## ② Sơ lược lịch sử phát triển của hệ điều hành qua các thế hệ máy tính
### 2.1. Máy tính thế hệ thứ nhất
Máy tính thế hệ thứ nhất không có hệ điều hành: Ở giai đoạn này, các chương trình viết bằng ngôn ngữ máy. Việc điều khiển máy tính được thực hiện bằng cách nối dây trên các bảng cắm nối. Phần mềm hỗ trợ người dùng chỉ là thư viện các chương trình mẫu và một số chương trình phục vụ.
### 2.2. Máy tính thế hệ thứ hai
Hệ điều hành của các máy tính thế hệ thứ hai: Máy tính thế hệ này bắt đầu có hệ điều hành, tại mỗi thời điểm chỉ cho phép thực hiện một chương trình.
## 3. Hệ điều hành của máy tính thế hệ thứ ba
### 3.1. Đặc điểm
*   Hệ điều hành của máy tính thứ ba theo chế độ đa nhiệm, cho phép tại mỗi thời điểm có nhiều chương trình được thực hiện.
*   Ví dụ, trong khi một chương trình đang sử dụng CPU thì chương trình thứ hai có thể sử dụng máy in để in kết quả ra.
*   Máy tính chỉ có một CPU nhưng mỗi chương trình được OS cấp thời gian để CPU xử lí theo cách luân phiên.
*   Đó là cơ chế phân chia thời gian.
*   OS IBM 360/370 là tiêu biểu cho giai đoạn này.
*   Ngoài ra, OS cũng có khả năng quản lí giao tiếp với nhiều người dùng.
*   Vào những năm 70 của thế kỉ XX, OS bắt đầu có thêm khả năng điều hành mạng để khai thác hiệu quả mạng cục bộ và mạng diện rộng.
## 4. Hệ điều hành của máy tính thế hệ thứ tư
### 4.1. Xu hướng phát triển
Ở giai đoạn này, có hai khuynh hướng phát triển máy tính: máy tính cá nhân và siêu máy tính, với mỗi loại máy tính có loại OS tương ứng.
## 5. Một số hệ điều hành tiêu biểu
*   Ngoài hệ điều hành Windows, em có biết hệ điều hành nào khác không?
### 5.1. Hệ điều hành cho máy tính cá nhân
#### 5.1.1. Các hệ điều hành thương mại
Một số OS thương mại tiêu biểu là: MS DOS, Windows cho dòng máy tính với CPU Intel.
*   MS DOS là OS đơn chương trình, tổ chức thông tin theo đơn vị quản lí là file, theo cấu trúc thư mục phân cấp dạng cây.
*   Giao tiếp giữa người và máy tính thông qua lệnh.
*   Năm 1981, công ty Microsoft đã đưa ra thị trường MS DOS 2.0. Nhiều năm liên tiếp phát triển thành phiên bản MS DOS 5.0 và được bình chọn là OS tốt nhất cho máy tính cá nhân.
*   Windows các phiên bản đầu tiên chạy trên nền tảng của MS DOS sử dụng giao diện đồ hoạ rất đẹp, thân thiện.
*   Cho đến nay, kiểu giao tiếp với các biểu tượng (icon) và cơ chế chỉ định bằng chuột đã trở thành chuẩn.
*   Từ năm 1995, với sự phổ biến rộng rãi của máy tính cá nhân có cấu hình mạnh, hai loại OS được sử dụng chủ yếu, rộng rãi là Windows cho các máy tính của hãng IBM và MacOS cho các máy tính của hãng Apple (ra đời sớm hơn, từ năm 1985).
*   Cuối thập kỉ XX, có các OS tiêu biểu như Windows 95/98/NT.
*   Windows 95 là một cột mốc phát triển OS với giao diện đẹp, có nhiều công cụ tiện ích như menu Start, thanh trạng thái Taskbar, biểu tượng lối tắt Shortcut.
*   Windows 2000 Server có nhiều công cụ để quản trị mạng, cung cấp nhiều dịch vụ cho mạng cục bộ kết nối với Internet.
*   Năm 2001, Windows XP được phát hành với nâng cấp để chạy trên các bộ xử lí tiên tiến 64 bit thế hệ mới.
*   Sau đó là các phiên bản Windows 7 (năm 2009), Windows 8 (năm 2012).
*   Windows 10 (năm 2015) đang được sử dụng phổ biến vì tính hiệu quả, có sẵn các hỗ trợ phòng chống virus, an toàn dữ liệu,... và hoạt động ổn định, đáng tin cậy.
*   Windows 11 (năm 2021) là thế hệ mới nhất sẽ dần dần thay thế các phiên bản Windows trước đó.
#### 5.1.2. Hệ điều hành cho máy tính bảng và điện thoại thông minh
Có các công cụ quản lí thông tin cá nhân, xử lí âm thanh và đồ họa được đặc biệt chú ý nhiều hơn cả để đảm bảo chất lượng cao trong vai trò của công cụ giải trí, thư giãn.
#### 5.1.3. Hệ điều hành UNIX
*   OS UNIX xuất hiện từ thế hệ máy tính thứ ba, do Ken Thompson xây dựng, được sử dụng chủ đạo cho các máy tính lớn, siêu máy tính.
*   UNIX là OS đa nhiệm, nhiều người dùng dựa trên cơ chế phân chia thời gian, kiểm soát người dùng rất nghiêm ngặt, đảm bảo an toàn cho các chương trình cùng thực hiện đồng thời trên một máy tính.
*   UNIX được viết bằng ngôn ngữ lập trình C, cung cấp các lệnh thao tác với file, thư mục, các phương tiện lập trình, quản trị hệ thống.
*   UNIX sử dụng giao thức mạng TCP/IP phục vụ truyền thông tốt.
*   Nhờ có chế độ vận hành bộ nhớ ảo nên UNIX cho phép máy tính thực hiện các chương trình lớn hơn bộ nhớ của nó.
#### 5.1.4. Hệ điều hành LINUX
*   Năm 1991, Linus Benedict Torvalds, một sinh viên ngành khoa học máy tính tại Đại học Helsinki (Phần Lan), bắt đầu một dự án mà kết quả sau đó là hạt nhân (phần cốt lõi) của OS LINUX.
*   LINUX là OS nguồn mở, theo kiểu UNIX, viết trên ngôn ngữ C và được cung cấp miễn phí toàn bộ mã nguồn các chương trình hệ thống.
*   Đầu tiên, LINUX được phát hành với giấy phép riêng, hạn chế sử dụng cho hoạt động thương mại.
*   Năm 1992, Torvalds đề nghị phát hành hạt nhân LINUX theo giấy phép công cộng.
*   GNU đã tạo cơ sở để các nhà phát triển LINUX tạo ra một hệ điều hành miễn phí có đầy đủ chức năng.
*   Mọi người đều có thể sửa đổi, nâng cấp hệ điều hành LINUX mà không vi phạm bản quyền, tạo thuận lợi cho việc bản địa hóa LINUX, tạo giao diện theo tiếng địa phương, ví dụ bằng tiếng Việt.
#### 5.1.5. Các mốc phát triển của hệ điều hành LINUX
*   Năm 1994: Torvalds đánh giá tất cả các thành phần của hạt nhân đã được hoàn thiện và phiên bản 1.0 của LINUX được phát hành.
*   Năm 1996: Phiên bản 2.0 của hệ điều hành LINUX ra đời, có thể phục vụ nhiều bộ vi xử lí cùng lúc.
*   Những năm tiếp theo nhiều công ty lớn như IBM, Compaq và Oracle tuyên bố hỗ trợ LINUX.
*   Năm 1998: LINUX lần đầu tiên xuất hiện trong danh sách Top 500 siêu máy tính nhanh nhất và đến năm 2017 tất cả Top 500 siêu máy tính đều chạy LINUX.
*   Các phiên bản 3.0 (năm 2011), 4.0 (năm 2015) và 5.0 (năm 2019) của nhân LINUX lần lượt được phát hành.
### 5.2. Hệ điều hành Android
*   Android là hệ điều hành nguồn mở, dựa trên nền tảng của LINUX dành cho các thiết bị di động có màn hình cảm ứng như điện thoại thông minh, máy tính bảng.
*   Năm 2003, hệ điều hành Android được bắt đầu phát triển. Cuối năm 2008, hơn một năm sau khi iPhone của Apple xuất hiện, điện thoại thông minh HTC Dream (T-Mobile G1) chạy hệ điều hành Android 1.0 ra đời, được coi là điện thoại dùng hệ điều hành Android đầu tiên.
*   Từ năm 2015, Google đã đưa ra phiên bản hệ điều hành Android cài đặt cho ô tô và ti vi.
*   Tháng 8 năm 2019, Google quyết định không dùng các icon bánh kẹo nữa mà chuyển sang đánh số thứ tự.
*   Android 10, được phát hành vào tháng 9 năm 2019.
*   Android 11 ra mắt vào tháng 6 năm 2020.
*   Android 12 được công bố lần đầu tiên vào tháng 2 năm 2021.
*   Android 13 được phát hành cho công chúng vào ngày 15 tháng 8 năm 2022.
# Thực hành tìm hiểu về hệ điều hành
*   Tìm hiểu các khả năng của máy tính và sử dụng một số tiện ích có sẵn của hệ điều hành để nâng cao hiệu suất sử dụng máy tính.
# Nhiệm vụ 1: Tìm hiểu các khả năng của máy tính hay điện thoại (ưu tiên tìm hiểu OS Android hay iOS).
*   Khả năng phát âm thanh và video.
*   Thử nghiệm chụp ảnh ở chế độ chụp ảnh toàn cảnh, ghi ảnh, xem lại và chia sẻ cho người khác.
# Nhiệm vụ 2: Một số tổ hợp phím tắt của OS Windows cho phép người dùng thao tác nhanh hơn khi dùng chuột. Hãy khám phá tác dụng của một số phím tắt dưới đây và mô tả các bước thao tác bằng chuột để có kết quả tương tự.
*   Ctrl + Win + O: bật/tắt bàn phím ảo trên màn hình.
*   Alt + Tab: chuyển cửa sổ đang hoạt động.
*   Win + D: chuyển sang màn hình nền.
*   Ctrl + Shift: chuyển chế độ gõ bàn phím.
*   Win + H: bật/tắt micro.
*   Win + . (hoặc ;): bật/tắt cửa sổ chứa các biểu tượng cảm xúc.
*   Tìm hiểu xem điện thoại thông minh của em dùng hệ điều hành gì? Nó có phải là hệ điều hành nguồn mở hay không?
# Câu hỏi
## Câu 1. Hệ điều hành có phải là phần mềm duy nhất trong máy tính, máy tính bảng hoặc điện thoại thông minh hay không? Vì sao?
## Câu 2. Nêu tên một số hệ điều hành thương mại thường gặp.
## Câu 3. Nêu tên một số hệ điều hành nguồn mở thường gặp.
# Tóm tắt bài học
*   Hệ điều hành tạo môi trường để người dùng khai thác máy tính và các thiết bị ngoại vi một cách tối ưu và đơn giản.
*   Hệ điều hành cung cấp các dịch vụ để tổ chức và quản lí tệp, thực hiện các chương trình ứng dụng.
*   Hệ điều hành có nhiều loại: thương mại và nguồn mở; dành cho máy tính và dành cho điện thoại thông minh.
*   Hệ điều hành có lịch sử phát triển gắn với các thế hệ máy tính và ngày càng tiện lợi hơn, hỗ trợ tốt hơn cho người dùng.
# BÀI 4 THỰC HÀNH VỚI CÁC THIẾT BỊ SỐ
*   Học xong bài này, em sẽ:
    *   Kết nối được các bộ phận thân máy, bàn phím, chuột, màn hình của máy tính với nhau.
    *   Kết nối được PC với các thiết bị số thông dụng như máy in, điện thoại thông minh, máy ảnh số,...
    *   Tùy chỉnh được một vài chức năng cơ bản của máy tính và các thiết bị vào – ra thông dụng để phù hợp với nhu cầu sử dụng và đạt hiệu quả tốt hơn.
## Nhiệm vụ 1. Lắp ráp các bộ phận của máy tính
*   **Yêu cầu:** Kết nối thân máy, bàn phím, chuột, màn hình.
### Hướng dẫn thực hiện:
#### Bước 1. Chuẩn bị
*   Chuẩn bị các bộ phận cần thiết: thân máy tính, màn hình, bàn phím, chuột.
*   Xác định các cổng kết nối có trên máy tính và các thiết bị.
*   **Bảng 1. Một số cổng giao tiếp của máy tính và cáp kết nối tương ứng**
#### Bước 2. Xếp đặt vị trí thiết bị
*   Lựa chọn vị trí đặt các thiết bị sao cho:
    *   Đảm bảo thiết bị có thể cắm được vào nguồn điện.
    *   Đặt bàn phím, chuột và màn hình trên bàn nơi phù hợp với vị trí lựa chọn.
    *   Lựa chọn vị trí đặt thân máy tính để dễ dàng kết nối với các thiết bị ngoại vi.
#### Bước 3. Kết nối các bộ phận với nhau
*   Kết nối màn hình với thân máy.
*   Kết nối chuột, bàn phím với thân máy.
*   Kết nối cáp VGA (thường là màu xanh lam) với màn hình, vặn chặt các vít.
*   Kết nối dây nguồn của màn hình và thân máy với ổ điện.
#### Bước 4. Kiểm tra kết quả
*   Bật nguồn màn hình, bật nguồn máy tính.
*   Kiểm tra màn hình đã hiển thị bình thường chưa.
*   Di chuyển chuột và quan sát màn hình để kiểm tra hoạt động của chuột.
*   Gõ phím và quan sát màn hình để kiểm tra hoạt động của bàn phím.
## Nhiệm vụ 2. Kết nối máy tính với các thiết bị số thông dụng
*   Nhiều thiết bị số có thể kết nối với máy tính, trở thành thiết bị ngoại vi trong một phiên làm việc và ngắt kết nối khi xong việc.
*   Điện thoại thông minh, máy in, máy chiếu,... là các ví dụ.
*   Có thể kết nối thiết bị ngoại vi với máy tính qua cáp nối (kết nối có dây) hoặc qua Bluetooth, qua Wi-Fi (kết nối không dây).
### Bước 2. Chọn chế độ kết nối.
*   Thông thường sẽ có các chế độ: sạc pin, truyền tệp, truyền ảnh.
*   Ta chọn chế độ truyền tệp trao đổi dữ liệu giữa máy tính và điện thoại.
### Bước 3. Truy cập ổ đĩa bộ nhớ điện thoại và thực hiện việc chuyển/sao chép dữ liệu qua lại giữa máy tính và điện thoại.
#### Yêu cầu 2:
*   Kết nối máy tính dùng Windows 10 với điện thoại thông minh dùng Android thông qua Bluetooth và sao chép một số dữ liệu từ điện thoại sang máy tính và ngược lại.
#### Hướng dẫn thực hiện:
##### Bước 1. Bật Bluetooth trên điện thoại.
*   Vào **Settings** (Cài đặt), chọn **Bluetooth** và gạt công tắc sang chế độ **ON**.
##### Bước 2. Bật Bluetooth trên máy tính.
*   Chọn **Windows Settings**, sau đó chọn **Devices**.
*   Tại mục Bluetooth, kéo chuột để gạt thanh công tắc sang phải bật kết nối.
##### Bước 3. Dò tìm và kết nối máy tính với điện thoại.
*   **Yêu cầu kết nối:** Để thực hiện yêu cầu kết nối từ điện thoại, trên điện thoại ta chọn vào thiết bị muốn kết nối (máy tính).
*   Khi đó trên máy tính nhận được yêu cầu kết nối hiện ở góc thông báo của Windows.
*   Chọn **Connect\OK** trên cả hai thiết bị.
##### Bước 4. Gửi/nhận file.
*   Tại thanh công cụ, nháy chuột phải vào biểu tượng Bluetooth.
*   Chọn **Send a file** để gửi file đi hoặc **Receive a file** để nhận file.
## Nhiệm vụ 3. Cá nhân hoá máy tính
*   Có thể tuỳ chỉnh máy tính theo nhu cầu sử dụng hoặc sở thích cá nhân. OS thường có sẵn một số công cụ tiện ích hỗ trợ việc này.
### Yêu cầu:
*   Với sự hướng dẫn của giáo viên, em hãy thực hiện các tuỳ chỉnh sau:
1) Lựa chọn ảnh nền, chỉnh độ sáng, độ phân giải cho màn hình.
2) Thay đổi kích thước, màu sắc, lựa chọn nút nhấn chính của chuột.
3) Chỉnh sửa thời gian cho đồng hồ về đúng thời gian hiện tại.
### Hướng dẫn thực hiện:
*   Máy tính sử dụng OS Windows: vào mục Control Panel.
*   Máy tính sử dụng OS iOS: nháy vào biểu tượng Apple, sau đó chọn System Preferences.
*   Dưới đây là một số mục tuỳ chỉnh (của OS Windows). Hãy nháy chuột để mở các lựa chọn chi tiết hơn.
*   Appearance and Personalization: cách hiển thị các mục trên màn hình và cá nhân hoá.
*   Easy of Access: cho phép thay đổi cách hoạt động của chuột, của bàn phím,...
*   Clock and Region: thay đổi cách hiển thị ngày, tháng và các số.
*   Kết nối điện thoại với máy tính bằng phần mềm để gửi tệp tin từ điện thoại tới máy tính và ngược lại.
*   Gợi ý: Sử dụng AirDroid cho điện thoại Android và AirDrop cho điện thoại iPhone.
# BÀI 5: PHẦN MỀM ỨNG DỤNG VÀ DỊCH VỤ PHẦN MỀM
*   Học xong bài này, em sẽ:
    *   Biết vấn đề bản quyền trong sử dụng phần mềm nguồn mở.
    *   Biết cách khai thác các mặt mạnh của phần mềm trực tuyến, sử dụng các phần mềm này trong học tập và công việc.
    *   Hiểu được vai trò của phần mềm nguồn mở và phần mềm thương mại đối với sự phát triển của ICT.
    *   Nêu được tên một số phần mềm soạn thảo văn bản, phần mềm trình chiếu và phần mềm bảng tính nguồn mở trong bộ OpenOffice.
*   Câu hỏi: Những phần mềm đang có trong máy tính đã đáp ứng đầy đủ mọi nhu cầu làm việc của em hay chưa?
## 1 Một số loại phần mềm
*   Câu hỏi: Lần gần đây nhất, em đã tải về và cài thêm phần mềm mới nào trên điện thoại thông minh của em? Tại sao em cần thêm phần mềm đó?
*   Có thể phân loại phần mềm ứng dụng theo nhiều góc độ khác nhau. Dưới đây là một số cách phân biệt thường thấy:
    *   Phần mềm thương mại và phần mềm miễn phí.
    *   Phần mềm nguồn mở và phần mềm nguồn đóng.
    *   Phần mềm khai thác trực tuyến (online) và phần mềm cài trên máy tính cá nhân.
    *   Phần mềm thương mại là phần mềm phải trả tiền mua để sử dụng dù đó là phần mềm ứng dụng hay OS. Phần lớn phần mềm ứng dụng là phần mềm thương mại.
    *   Đối lập với phần mềm thương mại là phần mềm miễn phí. Người dùng không phải trả chi phí và có thể cài đặt trên máy để sử dụng. Các phần mềm phục vụ học tập thường được cung cấp miễn phí và có chất lượng cao (ví dụ: phần mềm nguồn mở Codeblocks, Dev C++ cho hệ thống lập trình C++, Python, Java,...).
*   **Phần mềm nguồn đóng**: Được cung cấp dưới dạng các mô đun chương trình viết trên ngôn ngữ máy. Phần mềm thương mại thường được cung cấp dưới dạng nguồn đóng.
*   **Phần mềm nguồn mở**: Được cung cấp dưới dạng các mô đun chương trình viết trên một ngôn ngữ lập trình bậc cao. Ví dụ, bộ phận mềm OpenOffice là phần mềm nguồn mở, có các khả năng như một bộ phận mềm văn phòng điển hình. Nó gồm Writer (tương tự với Microsoft Word), Calc (tương tự với Microsoft Excel), Impress (tương tự với Microsoft PowerPoint),...
*   **Phần mềm khai thác trực tuyến**: Chỉ có thể sử dụng trên môi trường web, có thể miễn phí hoặc phải trả tiền cho từng phiên sử dụng.
*   Các phần mềm khai thác trực tuyến đóng vai trò quan trọng trong cuộc sống ngày nay. Các phần mềm tra cứu bản đồ và chỉ dẫn đường đi (maps.google.com), dịch văn bản (translate.google.com), hệ thống văn phòng trực tuyến (docs.google.com), hệ thống phục vụ dạy và học trực tuyến (meet.google.com),...
Dưới đây là đoạn văn bản  đã được phân cấp lại theo cấu trúc rõ ràng:
# Ứng dụng của phần mềm
Ngày nay, phần mềm khai thác trực tuyến ngày càng trở nên quen thuộc với người dùng. Các phần mềm này được cung cấp dưới hai dạng: miễn phí (bị hạn chế một số tính năng) và có trả phí, nếu không muốn bị hạn chế sử dụng những tính năng phong phú khác. Phần mềm khai thác trực tuyến có trả phí được cung cấp theo cách linh hoạt, như một dịch vụ, tuỳ theo nhu cầu của người dùng.
*   **Giấy phép phần mềm công cộng**: Viết tắt là GNU GPL hay ngắn gọn hơn là GPL (General Public License). GPL là giấy phép phần mềm phổ biến nhất trong lĩnh vực phần mềm tự do nguồn mở. Nó đảm bảo cho người dùng được tự do khai thác, nghiên cứu, sửa đổi và chia sẻ phần mềm.
*   Để có thể tự do nghiên cứu và sửa đổi phần mềm thì mã nguồn phải mở. Tính mở và tính tự do gắn liền với nhau. Hiện nay thuật ngữ “phần mềm tự do nguồn mở”, viết tắt tiếng Anh là FOSS (Free Open Source Software) hay được dùng hơn.
*   Giấy phép phần mềm công cộng đã mở rộng cánh cửa để mọi người tiếp cận những sản phẩm trí tuệ của xã hội và đóng góp phần mình vào vốn kiến thức chung của nhân loại.
## Thực hành với phần mềm khai thác trực tuyến miễn phí
*   **Yêu cầu:** Làm quen với soạn thảo văn bản, làm bài trình chiếu và sử dụng bảng tính qua các phần mềm trực tuyến của Google.
*   **Hướng dẫn thực hiện:** Mở trang web www.google.com, mở bảng chọn các ứng dụng của Google, chọn ứng dụng muốn dùng thử.
### Thử nghiệm nhập nội dung soạn thảo vào Google Docs bằng giọng nói
*   **a) Thử nghiệm nhập nội dung soạn thảo vào Google Docs bằng giọng nói theo các bước ở Hình 1:**
    1.  Kích hoạt (trên menu "Tools")
    2.  Chọn (mục "Voice typing")
    3.  Kích hoạt (biểu tượng micro)
    4.  Đọc nội dung: Trâu ơi ta bảo trâu này, Trâu ra ngoài ruộng trâu cày với ta. Cây cày vun nghiệp nông gia. Ta đây trâu đấy ai mà quản công. Bao giờ lúa chín trĩu bông. Thì còn ngon cỏ ngoài đồng trâu ăn!
*   Thông báo kết quả lưu vào www.google.com
*   Hình 1. Soạn thảo văn bản với Google Docs
### Thử mở Google Sheets và tạo một bảng tính
*   **b) Thử mở Google Sheets và tạo một bảng tính ghi thông tin các bạn trong tổ theo mẫu như ở Hình 2.**
*   Hình 2. Một mẫu soạn thảo bảng tính với Google Sheets
### Thử nghiệm mở Google Slides và thiết kế một trang trình chiếu
*   Thử nghiệm mở Google Slides và thiết kế một trang trình chiếu.
## Câu hỏi và bài tập
*   **Câu 1:** Hãy sử dụng công cụ dịch trực tuyến, ví dụ như translate.google.com.vn để dịch một đoạn văn bản từ tiếng Việt sang tiếng Anh và ngược lại.
*   **Câu 2:** Hãy tìm trên mạng phần mềm chuyển định dạng, chạy trực tuyến miễn phí. Sử dụng phần mềm tìm được để chuyển một số file “.docx” sang tương ứng thành file “.pdf” và ghép nối các file kết quả thành một file “.pdf”.
### Câu hỏi trắc nghiệm
*   Trong các câu sau, những câu nào đúng?
    *   a) Trong hệ thống luôn cần có các chương trình ứng dụng.
    *   b) Phần mềm nguồn mở được cung cấp dưới dạng các mô đun phần mềm viết bằng ngôn ngữ máy.
    *   c) Phần mềm là một sản phẩm thương mại nên luôn phải có bản quyền mới sử dụng được.
    *   d) Không phải tất cả các phần mềm nguồn mở đều miễn phí.
## Tóm tắt bài học
*   Tùy thuộc vào nhu cầu sử dụng, người dùng cài đặt thêm vào hệ thống của mình các phần mềm ứng dụng khác nhau.
*   Có các loại phần mềm: nguồn đóng và nguồn mở, phần mềm khai thác trực tuyến và phần mềm cài trên máy tính cá nhân, phần mềm thương mại và phần mềm miễn phí.
*   Không phải mọi phần mềm nguồn mở đều miễn phí.
*   Việc sử dụng phần mềm nguồn mở sẽ giúp người dùng dễ dàng cải tiến, nâng cấp khi giải quyết vấn đề của mình.
# Chủ đề C: Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin
## Bài 1: Lưu trữ trực tuyến
**Học xong bài này, em sẽ:**
*   Biết được ưu, nhược điểm cơ bản của việc lưu trữ trực tuyến.
*   Sử dụng được một số công cụ trực tuyến như: Google Driver, Dropbox,... để lưu trữ và chia sẻ tệp tin.
**Câu hỏi gợi mở:**
*   Em đã từng dùng USB để sao lưu các tệp dữ liệu, chuyển dữ liệu từ máy tính này sang máy tính khác chưa? Em có biết cách nào khác để thực hiện việc đó không?
## 1. Dịch vụ lưu trữ trực tuyến
*   Việc lưu trữ dữ liệu số được xử lí bởi máy tính bằng các thiết bị có dung lượng lớn như ổ đĩa cứng (HDD), ổ đĩa cứng thể rắn (SSD) và ổ đĩa USB flash đã rất phổ biến. Cách lưu trữ này gọi là lưu trữ tại chỗ hay lưu trữ vật lí.
*   Ngày nay, việc lưu trữ dữ liệu cần đáp ứng nhu cầu tính toán như trong các dự án dữ liệu lớn (Big Data), trí tuệ nhân tạo (AI), máy học và Internet vạn vật (IoT).
*   Các yêu cầu đặt ra là bảo vệ chống mất mát dữ liệu do thảm họa, lỗi hoặc gian lận. Đặc biệt, để dữ liệu lưu trữ được chia sẻ cho nhiều người ở các vị trí địa lí khác nhau và đảm bảo dữ liệu lưu trữ được đồng bộ hoá trên nhiều thiết bị, cách lưu trữ trực tuyến đang tỏ ra rất hiệu quả.
*   Lưu trữ trực tuyến là một cách tiếp cận lưu trữ cho phép người dùng sử dụng Internet lưu trữ, quản lí, sao lưu và chia sẻ dữ liệu.
*   Việc lưu trữ trực tuyến thường liên quan đến hợp đồng với dịch vụ của một công ty gọi là bên thứ ba và chấp nhận dữ liệu được định tuyến thông qua giao thức Internet (IP).
*   Hầu hết các nhà cung cấp dịch vụ lưu trữ trực tuyến đều miễn phí một lượng nhỏ dung lượng lưu trữ và trả phí (theo tháng hoặc năm) với dung lượng lưu trữ lớn hơn.
*   Một số dịch vụ lưu trữ trực tuyến rất phổ biến như: Google Drive (www.drive.google.com) là dịch vụ lưu trữ dữ liệu dựa trên đám mây của Google, OneDrive (www.onedrive.live.com) là dịch vụ đám mây của Microsoft, Fshare (www.fshare.vn) là một dịch vụ lưu trữ trực tuyến lớn của Việt Nam hiện nay.
## Thực hành lưu trữ và chia sẻ dữ liệu trên Google Drive
### Nhiệm vụ 1. Tải và chia sẻ dữ liệu trên Google Drive
#### Yêu cầu:
*   Lớp được chia thành các nhóm, mỗi nhóm thực hiện những công việc sau:
    *   Tìm hiểu một trong những dịch vụ lưu trữ trực tuyến: Dropbox, OneDrive, Mega, Box, Mediafire. Tóm tắt các nội dung tìm hiểu được bằng một tệp văn bản và một tệp trình chiếu để thuyết trình trong khoảng 5 phút.
    *   Tạo một thư mục trên Google Drive có tên là tên của nhóm em (ví dụ: Nhóm 1, Nhóm 2,...). Tải các tệp ở câu a) lên thư mục, chia sẻ cho giáo viên và các bạn trong lớp với các bình luận (nếu có) được ghi kèm vào các tệp dữ liệu.
#### Hướng dẫn thực hiện:
##### Tìm kiếm và tạo các tệp tóm tắt nội dung tìm kiếm
*   Bước 1: Sử dụng máy tìm kiếm (chẳng hạn Google) để tìm thông tin về một trong các dịch vụ Dropbox, OneDrive, Mega, Box, Mediafire.
*   Bước 2: Tạo tệp văn bản và nhập nội dung về dịch vụ lưu trữ trực tuyến đã tìm ở Bước 1 gồm: giới thiệu, cách lưu trữ và chia sẻ dữ liệu, ưu và nhược điểm.
*   Bước 3: Tạo tệp trình chiếu giới thiệu tóm tắt nội dung có được ở Bước 2.
##### Lưu và chia sẻ dữ liệu trên Google Drive
*   Để sử dụng được dịch vụ Google Drive, người dùng phải có tài khoản Gmail (nếu chưa có thì đăng kí tài khoản Gmail tại www.gmail.com).
###### Bước 1. Đăng nhập Google Drive.
*   Cách 1: Truy cập địa chỉ www.drive.google.com, đăng nhập tài khoản Gmail.
*   Cách 2: Đăng nhập tài khoản Gmail, chọn Google apps (các ứng dụng của Google) để mở cửa sổ các ứng dụng của Google và chọn Drive.
###### Bước 2. Tải dữ liệu lên Google Drive:
*   Người dùng có thể tải thư mục hoặc tệp từ máy tính lên Google Drive.
*   Để dễ quản lí, người dùng nên tạo các thư mục để lưu các tệp theo cấu trúc cây như trên Windows.
####### Tạo thư mục mới:
Chọn mục New trên cửa sổ Google Drive, chọn Folder, đặt tên thư mục tại ô New folder và chọn Create.
####### Tải dữ liệu:
*   Mở thư mục muốn tải dữ liệu lên, chọn New (hoặc nháy chuột phải).
*   Chọn File upload (tải tệp) hoặc Folder upload (tải thư mục).
*   Chọn tệp hoặc thư mục trong máy tính muốn tải, chọn Open.
###### Bước 3. Chia sẻ dữ liệu:
*   Google Drive cho phép chia sẻ các tệp hoặc thư mục cho nhiều người dùng qua email hoặc đường liên kết.
####### Chia sẻ tệp/thư mục qua email:
*   Chọn tệp hoặc thư mục muốn chia sẻ, nháy chuột phải.
*   Chọn Share.
*   Nhập địa chỉ email của người hoặc nhóm người nhận dữ liệu được chia sẻ, chọn Send.
####### Gửi đường liên kết:
*   Chọn Copy link của tệp hoặc thư mục dữ liệu muốn chia sẻ.
*   Gửi link này cho người nhận.
####### Chọn quyền chia sẻ:
*   Viewer (chỉ xem dữ liệu).
*   Commenter (được bình luận).
*   Editor (được sửa dữ liệu).
*   Người được chia sẻ tệp hoặc thư mục có thể mở trực tiếp tệp hoặc thư mục trên Google Drive để xem và sửa dữ liệu (nếu được cấp quyền) mà không cần phải tải về.
###### Bước 4. Tải xuống các tệp hoặc thư mục từ Google Drive.
*   Chọn tệp hoặc thư mục cần tải xuống, nháy chuột phải, chọn Download.
### Nhiệm vụ 2. Tìm kiếm, truy cập và cập nhật dữ liệu
#### Yêu cầu:
*   Các nhóm hãy chỉnh sửa nội dung tệp theo bình luận của giáo viên (được lưu ở thư mục chung có tên *Bài 1*) và di chuyển tệp vào thư mục của nhóm mình.
#### Hướng dẫn thực hiện:
##### Bước 1. Tìm kiếm và truy cập dữ liệu trên Google Drive.
*   Truy cập Google Drive, chọn Search in Drive, xuất hiện danh sách các loại tệp ngay bên dưới bao gồm: Documents, SpreadSheets, Presentations, Forms,...
# Quản Lý và Chia Sẻ Tệp trên Google Drive
## Các Bước Cơ Bản
### Bước 1. Truy cập Tệp
*   Chọn loại tệp Documents, xuất hiện danh sách các tệp tài liệu (nếu muốn tìm chi tiết thì chọn More search tools), chọn và mở tệp cần truy cập.
### Bước 2. Cập nhật Dữ liệu
*   **Cách 1:** Mở tệp trực tiếp trên Google Drive và sửa nội dung tệp.
*   **Cách 2:** Cập nhật và lưu cả phiên bản cũ và mới của tệp dữ liệu trên Google Drive.
    *   Cập nhật nội dung tệp và lưu trên máy tính.
    *   Mở Google Drive, chọn tệp cần cập nhật, nháy chuột phải và chọn Manage versions.
    *   Chọn Upload new version, chọn tệp cập nhật từ máy tính, chọn Close sau khi tệp mới được tải xong.
### Bước 3. Di chuyển Tệp
*   Chọn tệp cần di chuyển, nháy chuột phải, chọn Move to, chọn thư mục cần di chuyển đến, chọn Move here.
## Xoá Tệp hoặc Thư Mục
*   Chọn tệp hoặc thư mục cần xoá, nháy chuột phải, chọn Remove.
# Lợi Ích và Lưu Ý Khi Sử Dụng Lưu Trữ Trực Tuyến
## Lợi Ích của Lưu Trữ Trực Tuyến
*   Lưu trữ trực tuyến mang lại rất nhiều lợi ích:
    *   Truy cập được dữ liệu từ mọi nơi và mọi lúc, truyền dữ liệu và đồng bộ hoá dữ liệu giữa các thiết bị. Điều này làm tăng tính sẵn có của dữ liệu.
    *   Chia sẻ tập tin với nhiều người dùng ở các vị trí địa lí khác nhau.
    *   Sao lưu và khôi phục tệp dữ liệu sau thảm hoạ vì nó nằm ngoài địa điểm của các thiết bị vật lí.
    *   Tránh được các sự cố như mất điện, thảm hoạ,...và khả năng sao lưu tự động để đảm bảo rằng dữ liệu không bị mất. Cần phải có tài khoản mới truy cập được dữ liệu.
## Lưu Ý Khi Sử Dụng Lưu Trữ Trực Tuyến
*   Tuy nhiên, lưu trữ trực tuyến có một số mặt trái tiềm ẩn như:
    *   Các dịch vụ lưu trữ đám mây có thể có những lỗ hổng bảo mật.
    *   Một số nhà cung cấp đôi khi gặp tình trạng ngừng hoạt động, dẫn đến lo ngại về độ tin cậy.
    *   Sử dụng bộ nhớ tại chỗ nhanh hơn so với sử dụng bộ nhớ Internet, vì thời gian đợi tệp tải lên hoặc tải xuống phụ thuộc vào tốc độ đường truyền.
    *   Nhiều cá nhân và tổ chức sử dụng kết hợp lưu trữ tại chỗ và trực tuyến. Chẳng hạn, sử dụng bộ nhớ cục bộ cho các tệp được sử dụng thường xuyên và bộ nhớ trực tuyến để sao lưu hoặc lưu trữ dữ liệu. Hoặc có thể sử dụng bộ nhớ cục bộ cho dữ liệu cá nhân và bộ nhớ trực tuyến cho các tệp muốn chia sẻ với người khác.
    *   Em hãy mở tệp của một nhóm đã được chia sẻ trên Google Drive ở bài thực hành, bình luận hoặc sửa nội dung tệp và chia sẻ lại tệp này.
    *   Theo em, những trường hợp nào sau đây nên sử dụng lưu trữ trực tuyến?
        *   a) Chia sẻ tệp dữ liệu cho nhiều người ở nhiều nơi và sao lưu dữ liệu tự động.
        *   b) Giải phóng bộ nhớ cho máy tính.
        *   c) Thiết bị lưu trữ dữ liệu không có kết nối Internet.
        *   d) Truy cập tệp dữ liệu từ nhiều thiết bị.
## Tóm Tắt Bài Học
*   Lợi ích chính của lưu trữ trực tuyến là khả năng bảo mật dữ liệu, sao lưu tự động, tăng tính an toàn cho dữ liệu, truyền và chia sẻ dữ liệu cho nhiều người dùng một cách thuận lợi.
*   Phần lớn các dịch vụ lưu trữ trực tuyến đều cung cấp tính năng đồng bộ hoá dữ liệu trên các thiết bị, bảo vệ dữ liệu bằng mật khẩu, tìm kiếm, truy cập tệp dữ liệu và chỉnh sửa tệp dữ liệu trực tuyến.
# BÀI 2: THỰC HÀNH MỘT SỐ TÍNH NĂNG HỮU ÍCH CỦA MÁY TÌM KIẾM
## Mục Tiêu Bài Học
*   **Học xong bài này, em sẽ:**
    *   Xác định được các lựa chọn theo tiêu chí tìm kiếm để nâng cao hiệu quả tìm kiếm thông tin.
    *   Thực hành tìm kiếm thông tin bằng cách nhập từ khoá hoặc giọng nói với Google.
## 1. Sử Dụng Biểu Thức Tìm Kiếm
*   Khi tìm kiếm thông tin trên Internet bằng máy tìm kiếm, có thể sử dụng một số toán tử và các kí hiệu đặc biệt, kết hợp với các từ khoá tìm kiếm. Điều này nhằm tăng hiệu quả tìm kiếm như: tìm kiếm nhanh hơn, trả về kết quả phù hợp với mong đợi hơn.
### Nhiệm Vụ 1. Kết Hợp Các Từ Khoá Tìm Kiếm Thành Biểu Thức Tìm Kiếm
*   **Yêu cầu:**
    *   Em hãy sử dụng máy tìm kiếm Google để thực hiện tìm kiếm với các biểu thức sau và so sánh kết quả nhận được về: thời gian tìm kiếm, số lượng trang web trả về, nội dung một số trang web kết quả.
    *   a) Cá heo xanh.
    *   b) “Cá heo xanh” + “cửa hàng”.
    *   c) Cửa hàng cá heo xanh.
*   **Hướng dẫn thực hiện:**
    *   Truy cập trang web www.google.com, tại ô tìm kiếm nhập lần lượt các biểu thức tìm kiếm ở trên, quan sát và nhận xét các kết quả nhận được.
*   Google hỗ trợ các kí hiệu đặc biệt và toán tử nhằm tăng hiệu quả tìm kiếm, một số kí hiệu đó như sau (kí hiệu A, B là các từ khoá tìm kiếm):
    *   “A”: Tìm trang chứa chính xác từ khoá A.
    *   A-B: Tìm trang chứa từ khoá A nhưng không chứa từ khoá B.
    *   A+B: Tìm trang kết quả chứa cả từ khoá A và B nhưng không cần theo thứ tự.
    *   A\*: Tìm trang chứa từ khoá A và một số từ khác mà Google xem là có liên quan. Ví dụ: Từ khoá “tin học\*” tìm các trang có chứa từ “tin học ứng dụng”, “tin học văn phòng”,...
    *   A AND B: Tìm trang chứa cả từ khoá A và B.
    *   A OR B (hoặc A | B): Tìm trang chứa từ khoá A hoặc B. Toán tử này hữu ích khi tìm từ đồng nghĩa hoặc một từ có nhiều cách viết.
    *   A + filetype (loại tệp): Tìm thông tin chính xác theo loại tệp như “.txt”, “.doc”, “.pdf”,... Sử dụng từ khoá này thuận lợi trong tìm kiếm tài liệu, sách điện tử.
## Nhiệm Vụ 2: Điều Chỉnh Biểu Thức Tìm Kiếm
*   **Yêu cầu:** Dựa trên kết quả Bài 1, điều chỉnh biểu thức tìm kiếm để nhận được kết quả phù hợp với mong đợi hơn. Ví dụ tìm kiếm "Đặc điểm sinh thái của cá heo xanh".
*   **Hướng dẫn thực hiện:**
    *   Sử dụng toán tử trừ (-) để loại bỏ các trang web về các cửa hàng có tên cá heo xanh.
    *   Nhập từ khoá "cá heo xanh" - "cửa hàng" vào ô tìm kiếm.
### Thu Hẹp Kết Quả Tìm Kiếm
*   Một cách khác để thu hẹp kết quả tìm kiếm là sử dụng bộ lọc trên một hoặc nhiều thuộc tính dữ liệu bằng cách truy cập trang tìm kiếm nâng cao tại địa chỉ www.google.com/advanced_search.
## Tìm Kiếm Thông Tin Bằng Giọng Nói
### Nhiệm Vụ 3. Tìm Kiếm Thông Tin Bằng Giọng Nói Trên Google
*   **Yêu cầu:** Em hãy tìm những trường học ở quận/huyện nơi em ở bằng giọng nói trên máy tìm kiếm Google.
*   **Hướng dẫn thực hiện:** Chẳng hạn, nếu muốn tìm trường học ở quận Cầu Giấy thì em thực hiện như sau:
    *   **Bước 1.** Truy cập trang web www.google.com và chọn ngôn ngữ tiếng Việt.
    *   **Bước 2.** Chọn biểu tượng (Tìm kiếm bằng giọng nói), bật micro của máy tính và nói “trường học ở quận Cầu Giấy”. Kết quả tìm kiếm là các trang web của các trường học ở Cầu Giấy.
*   Tìm kiếm bằng giọng nói rất thuận lợi khi sử dụng tìm kiếm trên các thiết bị di động, thiết bị điều khiển trên ô tô.
*   Ngoài ra, Google còn cung cấp tính năng tìm kiếm bằng hình ảnh. Kết quả tìm kiếm là các trang web có hình ảnh cần tìm kiếm, thông tin về vật thể trong hình và các hình ảnh tương tự khác.
*   Em hãy sử dụng một máy tìm kiếm để tìm thông tin về lĩnh vực ngành nghề mà mình quan tâm. Trong đó, có sử dụng tìm kiếm theo từ khoá được nhập vào ô tìm kiếm, tìm một vài địa điểm của đơn vị hoạt động về lĩnh vực ngành nghề này bằng giọng nói, tìm kiếm dựa vào hình ảnh nhân vật hoặc sự kiện nổi bật trong lĩnh vực đó.
# BÀI 3: THỰC HÀNH MỘT SỐ TÍNH NĂNG NÂNG CAO CỦA MẠNG XÃ HỘI
## Mục Tiêu Bài Học
*   **Học xong bài này, em sẽ:**
    *   Sử dụng được một số chức năng nâng cao của dịch vụ mạng xã hội.
    *   Thực hành các chức năng nâng cao trên mạng xã hội Facebook.
## 1. Cài Đặt Bảo Mật và Quyền Riêng Tư Trên Mạng Xã Hội
*   Các mạng xã hội cung cấp các cơ chế bảo vệ tài khoản bằng cách sử dụng mật khẩu mạnh và thay đổi mật khẩu thường xuyên hoặc thiết lập bảo mật hai lớp.
*   Bảo mật hai lớp là thêm một bước xác thực, ví dụ: Người dùng phải nhập một dãy số được gửi đến số điện thoại đã đăng kí kèm theo tài khoản.
### Nhiệm Vụ 1. Bảo Mật Hai Lớp Tài Khoản Facebook
*   **Yêu cầu:** Kích hoạt bảo mật hai lớp cho tài khoản Facebook của mình.
*   **Hướng dẫn thực hiện:**
    *   **Bước 1:** Đăng nhập tài khoản Facebook, chọn Your Profile, chọn Settings & privacy, chọn Settings tại cửa sổ Settings & privacy.
    *   **Bước 2:** Chọn Security and login, chọn Use two-factor authentication trong mục Two-factor authentication và chọn Edit.
### Bước 3. Lựa Chọn Các Phương Án:
*   (1) Use Authentication App: Sử dụng một ứng dụng như Google Authenticator hoặc Duo Mobile để tạo mã xác minh nhằm bảo vệ tốt hơn.
*   (2) Use Text Message (SMS): Sử dụng tin nhắn văn bản để nhận mã xác minh.
*   (3) Use security key: Sử dụng khoá bảo mật đăng nhập qua USB hoặc NFC.
*   Chẳng hạn, lựa chọn (2), nhập số điện thoại và chọn Continue, nhập mã xác nhận 6 số được gửi vào điện thoại, chọn Done.
### Nhiệm Vụ 2. Cài Đặt Quyền Riêng Tư Với Các Thông Tin Chia Sẻ Trên Facebook
*   **Yêu cầu:** Em đăng một bức ảnh chụp với bạn trên Facebook và chỉ chia sẻ bức ảnh với người bạn này.
*   **Hướng dẫn thực hiện:**
    *   Bước 1. Đăng nhập tài khoản Facebook trên máy tính.
    *   Bước 2. Tạo bài đăng, tại cửa sổ Create Post chọn Photo/Video, chọn Add photos/videos, chọn ảnh cần đăng.
    *   Bước 3. Chọn Friends, chọn Specific friends, nhập tài khoản Facebook của người mà em muốn chia sẻ ảnh, chọn Save changes, chọn Post.
# Trao đổi và chia sẻ thông tin trên Facebook
## Nhiệm vụ 3: Tạo phòng họp nhóm để trao đổi thông tin trên Facebook
### Yêu cầu:
Tạo phòng họp trên Facebook để trao đổi về làm bài tập nhóm.
### Hướng dẫn thực hiện:
#### Bước 1:
Đăng nhập tài khoản Facebook, chọn "Create room" hoặc chọn (biểu tượng Menu), rồi chọn "Room" trong cửa sổ "Create".
#### Bước 2: Đặt tên phòng họp và thời gian cuộc họp:
*   Tại cửa sổ "Create your room": chọn "Room name", chọn "New" và nhập tên phòng họp, chọn thời điểm bắt đầu cuộc họp tại "Start time", sau đó chọn "Save".
*   Chọn "Create Room".
#### Bước 3: Gửi lời mời tham gia phòng họp.
*   Chọn nút "Send" bên cạnh tài khoản muốn mời, chọn "Join Room" để tham gia và bắt đầu cuộc họp.
### Lời khuyên:
Nên tạo phòng họp nhóm và hẹn mời các bạn cùng nhóm học tập thảo luận để lựa chọn thiết lập quyền riêng tư khi chia sẻ thông tin trên Facebook sao cho thuận tiện. Đồng thời, tạo sự kiện thông báo với các bạn trong nhóm về buổi thảo luận này.
### Gợi ý:
Để tạo sự kiện, chọn "Event" trong cửa sổ "Create".
# THỰC HÀNH MỘT SỐ TÍNH NĂNG HỮU ÍCH CỦA DỊCH VỤ THƯ ĐIỆN TỬ
## Học xong bài này, em sẽ:
*   Biết cách phân loại và đánh dấu thư điện tử.
*   Thực hành phân loại và đánh dấu thư điện tử Gmail.
## Phân loại thư điện tử
*   Ở lớp 6, em đã biết sử dụng các chức năng cơ bản của dịch vụ thư điện tử (như: tạo tài khoản, đăng nhập tài khoản, soạn thư, gửi thư và đăng xuất khỏi hộp thư) để trao đổi thông tin với thầy cô, bạn bè, người thân. Sau một thời gian sử dụng, hộp thư đến sẽ chứa rất nhiều email và khi cần tìm kiếm có thể phải thực hiện mất nhiều thời gian. Để thuận tiện, các dịch vụ thư điện tử đều hỗ trợ tính năng quản lí bằng cách phân loại và gắn nhãn các thư đến.
*   Việc phân loại cho phép người dùng dễ dàng gắn thẻ, gắn nhãn vào nhóm các thư cũng như sự kiện lịch trong các dịch vụ thư điện tử. Gmail có sẵn các nhóm được gắn nhãn như: Inbox (các thư được gửi đến), Sent (các thư đã được gửi đi), Drafts (các thư nháp),...
## Nhiệm vụ 1. Phân loại và đánh dấu email trong Gmail
### Yêu cầu:
Em hãy tạo nhãn “Học tập” cho các email về học tập, gồm các email được gửi từ giáo viên và các bạn trong lớp. Đánh dấu ⭐ cho những email được gửi đến từ giáo viên.
### Hướng dẫn thực hiện:
#### Bước 1.
Đăng nhập tài khoản Gmail của em.
#### Bước 2.
Chọn ⚙️ (Settings) ở góc phải trên màn hình, xuất hiện cửa sổ Settings như ở Hình 2, chọn mục Labels, chọn Create new label.
#### Bước 3.
Tại cửa sổ New label nhập tên nhãn “Học tập” và chọn Create.
### Lưu ý:
Có thể tạo nhãn con của một nhãn khác giống như tạo thư mục con, bằng cách chọn Nest label under và chọn tên nhãn cha (Cửa sổ New label ở Hình 2).
## Cài đặt nhãn (Labels) trong Gmail:
*   Trong phần cài đặt, có các mục như General, Labels, Inbox, Accounts and Import, Filters and blocked addresses, Forwarding and POP/IMAP, Add-ons, Chat and Meet, Advanced, Offline, Themes.
*   Các mục con trong Labels bao gồm All Mail, Spam, Bin, Categories (Categories, Social, Updates, Forums, Promotions). Đối với mỗi mục, có tùy chọn "show" (hiển thị) hoặc "hide" (ẩn).
*   Cũng có tùy chọn "Show in label list" (hiển thị trong danh sách nhãn) và "Show in message list" (hiển thị trong danh sách tin nhắn) cho các nhãn.
*   Để tạo nhãn mới, chọn "Create new label". Khi tạo nhãn mới, cần nhập tên nhãn và có thể chọn "Nest label under" (lồng nhãn dưới) một nhãn khác.
*   Lưu ý: Việc xóa một nhãn sẽ không xóa các tin nhắn có nhãn đó.
## Hướng dẫn gán nhãn cho email:
*   Nếu muốn gán thêm nhãn khác cho email: chọn email cần gán thêm nhãn, sau đó chọn tùy chọn "Labels", và chọn nhãn muốn gán thêm.
## Hướng dẫn di chuyển email sang nhãn khác:
*   Nếu muốn di chuyển email sang nhãn khác: chọn email muốn di chuyển, sau đó chọn tùy chọn "Move to", và chọn nhãn muốn email di chuyển đến.
## Hướng dẫn đánh dấu email quan trọng:
*   Bước 4: Chọn dấu ⭐ ở cạnh email cần đánh dấu (ví dụ: email do giáo viên gửi).
*   Lưu ý: Em nên đánh dấu những email quan trọng để dễ tìm kiếm.
## Quản lí email bằng bộ lọc và tìm kiếm email:
## Nhiệm vụ 2. Tìm kiếm và tạo bộ lọc email trong Gmail
### Yêu cầu:
Em hãy tìm kiếm các email do giáo viên dạy môn Tin học gửi đến và có tệp đính kèm.
### Hướng dẫn thực hiện:
#### Bước 1.
Đăng nhập tài khoản Gmail của em.
#### Bước 2.
Tại ô Search in mail chọn biểu tượng bộ lọc, xuất hiện cửa sổ tìm kiếm như ở Hình 4.
#### Bước 3.
Chọn tiêu chí tìm kiếm: chọn mục From và nhập địa chỉ email của giáo viên môn Tin học, tích chọn Has attachment (chứa tệp đính kèm), chọn Search.
*   Khi muốn tìm các email đã được gắn sao, chọn Starred ở cột bên trái của sổ màn hình tài khoản email (Hình 1).
*   Lưu ý: Có thể chọn nhiều tiêu chí tìm kiếm trong cửa sổ tìm kiếm (Hình 4) để thu hẹp kết quả tìm kiếm.
*   Để thuận lợi cho việc tìm kiếm và quản lí email, có thể tạo bộ lọc email. Muốn tạo bộ lọc email, chọn Create filter biểu tượng bộ lọc, chọn các tiêu chí cho bộ lọc, chọn Create filter.
*   Em hãy tạo nhãn “Tin học” là nhãn con của nhãn “Học tập” (đã được tạo trong bài thực hành). Nhãn “Tin học” dành cho các email được gửi từ giáo viên môn Tin học và các bạn trong nhóm làm bài tập môn Tin học cùng với em. Sau đó, hãy tìm kiếm và tạo bộ lọc những email mà em cho là quan trọng.
# Chủ đề D: Đạo đức, pháp luật và văn hoá trong môi trường số – Ứng xử văn hoá và an toàn trên mạng – Phòng tránh lừa đảo và ứng xử văn hoá trên mạng.
## Học xong bài này, em sẽ:
*   Nêu được một số dạng lừa đảo phổ biến trên mạng và những biện pháp phòng tránh.
*   Giao tiếp được trên mạng qua email, chat, mạng xã hội,... và trong môi trường số một cách văn minh, phù hợp với văn hoá ứng xử.
## Câu hỏi gợi mở:
Theo em, lừa đảo trên không gian mạng dễ gặp hay hiếm thấy? Dễ tránh hay khó tránh? Vì sao?
## 1) Lừa đảo qua mạng
### a) Một số dạng lừa đảo
#### Hoạt động khám phá:
Em hãy sử dụng máy tìm kiếm tìm cụm từ "dạng lừa đảo phổ biến trên mạng" và cho biết:
*   1) Số kết quả trả về là nhiều hay ít?
*   2) Có thể tính được có bao nhiêu dạng lừa đảo hay không?
*   Không thể tin tưởng mọi điều nhìn thấy, nghe thấy trên mạng.
*   Biết cách phát hiện nội dung giả mạo, lừa đảo là một kĩ năng quan trọng khi sử dụng Internet.
*   Bọn lừa đảo trên mạng dùng nhiều thủ đoạn tinh vi, nhằm những mục đích khác nhau.
*   Có nhiều ví dụ về lừa đảo, từ lừa “nhấn chuột là được tiền”, lừa nạp thẻ điện thoại, đến lừa tiền đặt cọc, tiền chuyển hàng hay đánh cắp thông tin cá nhân qua trang web giả mạo.
*   Dưới đây nêu ví dụ một số thủ đoạn lừa đảo qua mạng:
##### Lừa đảo trúng thưởng, tặng quà để lấy tiền phí vận chuyển:
*   Gửi email hay tin nhắn qua mạng xã hội và thông báo, ví dụ: “Bạn thật may mắn đã trúng thưởng...” hoặc “Nhân ngày lễ lớn, ngày kỉ niệm của công ty, để tri ân khách hàng, công ty xin tặng món quà... Cần trả phí vận chuyển (từ 100 đến 200 nghìn đồng) để nhận quà”.
*   Kèm theo thông báo là ảnh món quà rất bắt mắt, ghi giá bán tới vài triệu đồng.
*   Nạn nhân mất tiền phí vận chuyển, không nhận được gì hoặc món quà chỉ đáng giá 10 đến 20 nghìn đồng.
##### Lừa đảo chiếm tiền đặt cọc hoặc bán hàng giả:
*   Lập tài khoản mạo danh các gian hàng trực tuyến uy tín để lừa khách hàng đặt mua, sau đó yêu cầu chuyển tiền đặt cọc để chiếm đoạt hay yêu cầu thanh toán và trả hàng giả, chất lượng khác xa với hình ảnh quảng cáo.
##### Lừa đảo để lấy cắp thông tin cá nhân:
*   Cũng dùng thủ đoạn giống như hai trường hợp ở trên, nhưng thay vì lừa lấy tiền, bọn lừa đảo yêu cầu nhấn vào link để xác nhận sớm, nếu chậm sẽ mất cơ hội.
*   Đường link gửi kèm sẽ dẫn tới một trang web (giả mạo) yêu cầu cung cấp thông tin cá nhân (ví dụ số tài khoản, mật khẩu,...) để có thể thực hiện giao dịch và chúng sẽ lấy cắp những thông tin ấy.
*   Các đối tượng lừa đảo có thể mạo danh các cơ quan, doanh nghiệp, người có uy tín, bạn bè hoặc người quen, thậm chí là đối tác nước ngoài, mời chào hợp tác kinh doanh, mua hàng giá rẻ,... kèm link lừa đảo.
##### Dấu hiệu lừa đảo và lời khuyên phòng ngừa:
*   Trong tin học, việc lừa đảo để lấy cắp thông tin cá nhân bằng các trang web giả gọi là phishing. Cần nhận biết các dấu hiệu lừa đảo và luôn có ý thức đề phòng để tự bảo vệ, tránh bị lừa.
# An Toàn Trên Mạng và Ứng Xử Văn Minh
*   Các cơ quan, tổ chức, doanh nghiệp uy tín phải đảm bảo giao tiếp quan hệ công chúng với chất lượng cao, có tính chuyên nghiệp.
*   Nếu email, trang web có lỗi chính tả, lỗi hành văn thì đó có thể là lừa đảo.
*   Những lỗi này có thể là do sự thiếu chuyên nghiệp của kẻ lừa đảo, do cố gắng tránh các bộ lọc thông minh, phát hiện kiểu lừa đảo đã biết, do được dịch từ một ngoại ngữ, từ kẻ lừa đảo xuyên biên giới, nhằm đến nạn nhân thích mới lạ.
*   Tên miền gồm vài phần cách nhau dấu chấm. Phần đầu viết tắt tên cơ quan, tổ chức, doanh nghiệp dễ nhớ nhưng các phần đuôi như: “com”, “net”, “org”,... ít được chú ý hơn. Các đuôi tên miền khác với tên miền chính thức mà cơ quan, tổ chức, doanh nghiệp vẫn dùng là dấu hiệu lừa đảo.
*   Cần chú ý nhận biết những cách viết sai chính tả trong tên miền để đánh lừa người đọc. Ví dụ, thay chữ “o” bằng số 0; thay “m” bằng “r” và “n”. Đây là những thủ đoạn phổ biến.
*   Trỏ chuột vào một liên kết nhưng không nháy chuột, ta sẽ nhìn thấy địa chỉ đích thực sự mà liên kết sẽ mở ra. Nếu nó không khớp với địa chỉ hiển thị mời nháy chuột thì đó là dấu hiệu lừa đảo.
*   Cảnh giác với email, tin nhắn từ người lạ, với cách xưng hô chung chung hoặc đột xuất bất ngờ từ người quen cũ lâu nay ít liên hệ.
*   Tạo ra tình huống khẩn cấp là một thủ đoạn phổ biến của kẻ lừa đảo. Nạn nhân sẽ không kịp suy nghĩ về hậu quả.
*   Hãy tìm cách kiểm tra lại thông tin bằng con đường khác, chẳng hạn như gọi điện thoại trực tiếp, truy cập địa chỉ trang web in trên các tài liệu chính thức.
*   Khi nghi ngờ email, tin nhắn là lừa đảo, đừng mở bất kì liên kết hoặc tệp đính kèm nào mà hãy kiểm tra địa chỉ đích thực sự để phát hiện liên kết lừa đảo.
*   **Nguyên tắc để hạn chế thiệt hại**
    *   Nếu nghi ngờ rằng mình đã có thể vô tình bị lừa qua mạng, hãy làm ngay một vài việc sau:
        *   Lập tức thay đổi mật khẩu cho những tài khoản giao tiếp qua mạng bị ảnh hưởng.
        *   Cần thiết lập xác minh hai bước cho những tài khoản quan trọng.
        *   Nếu tài khoản bị ảnh hưởng có liên quan đến nhà trường hay một cơ quan, tổ chức, cần thông báo ngay cho người có trách nhiệm.
        *   Nếu đã lỡ chia sẻ thông tin về thẻ tín dụng, tài khoản cá nhân, hãy báo ngay cho ngân hàng biết.
        *   Nếu đã bị thiệt hại, hãy báo ngay cho cơ quan chức năng.
*   **Văn hoá ứng xử trên mạng**
    *   Theo em cụm từ “anh hùng bàn phím” có hàm ý gì? Hãy nêu vài ví dụ cụ thể về “anh hùng bàn phím”.
    *   Nếu em là người có nhiều fan hâm mộ trên mạng xã hội, em nên làm gì và tránh những gì?
*   **Quy tắc nền tảng: Thế giới ảo, cuộc sống thực**
    *   Trên không gian mạng, các tiêu chuẩn về hành xử có đạo đức, có văn hoá, tuân thủ pháp luật cũng như trong cuộc sống thực.
    *   Hãy ý thức rằng khi lên mạng là đang ở giữa cộng đồng.
    *   Trong cuộc sống thực, hầu hết mọi người đều tuân thủ luật pháp, hành xử lịch sự, có văn hoá.
    *   Một số người hành xử trên mạng theo cách khác hẳn với khi đối mặt trực tiếp vì họ cho rằng, trên không gian mạng thì yêu cầu thấp hơn về đạo đức, văn hoá trong hành xử.
*   **b) Một số nguyên tắc về ứng xử trên mạng**
    *   Hãy đặt mình vào vị trí người khác. Cha mẹ, thầy cô vẫn dạy: “Ta đối xử với người khác thế nào thì họ đối xử với ta như thế”. Trên không gian mạng, lời khuyên này được cụ thể hoá là: “Hãy nhớ ở đâu kia của mạng là những người khác, cũng có cảm xúc giống ta!”. Vì không nhìn thấy, ta dễ dàng quên rằng họ đang có mặt; không thấy các phản ứng tức thì, người ta dễ hiểu lầm nhau và khi biết thì đã muộn.
    *   Rộng lượng với người khác, không gây chiến trên mạng. Khi ai đó mắc lỗi với bạn, hãy rộng lượng. Cần phản ứng lịch sự và tốt nhất là theo cách riêng tư hơn là to tiếng công khai.
    *   Có người thích “thể hiện”, dù sự việc không liên quan trực tiếp đến mình cũng phản ứng theo cách cực đoan. Phản xử người khác bằng ngôn từ bất lịch sự, hành vi thiếu văn hoá chỉ dẫn đến có thêm kẻ thù mà thôi. Những gì bạn nói ra, viết ra trên mạng có thể được lưu trữ ở một nơi nào đó, được chuyển tiếp đi bất cứ đâu mà bạn không còn quyền kiểm soát nữa.
    *   Tôn trọng “văn hoá nhóm”. Khi tham gia một nhóm mạng mới, hãy tìm hiểu xem “văn hoá nhóm” có phù hợp với bạn. Có những điều chấp nhận được ở một nơi này lại thành thô lỗ, bất lịch sự ở nơi khác. Một số câu chuyện cười kể trong nhóm nhỏ là bình thường nhưng không nên mang kể trong nhóm chat của cả lớp.
    *   Bạn không phải là trung tâm của không gian mạng. Đừng cố lấn át, nói hết phần người khác khi tham gia một nhóm mạng. Đừng mong đợi tất cả bài đăng, câu hỏi của bạn được phản hồi ngay; đừng cho rằng tất cả người đọc sẽ đồng ý hoặc quan tâm đến những bài viết đầy tâm huyết của bạn.
    *   Tôn trọng thời gian và công sức của người khác. Thật dễ nhấn nút “đăng” hay “gửi” bản sao cho nhiều người. Nhưng đăng bài nhiều lần, đăng tin rác, gửi thư rác,... sẽ làm phiền người khác và chiếm dụng đường truyền, chiếm dụng dung lượng lưu trữ trên máy chủ. Người có trách nhiệm luôn ý thức rằng “Không lãng phí thời gian và công sức của người khác”.
*   Tôn trọng quyền riêng tư của người khác. Không tìm cách đọc email, tin nhắn của người khác. Không chuyển tiếp email, tin nhắn riêng tư mà mình được chia sẻ cho người tiếp theo nếu không chắc đó là việc nên làm.
*   Một số người thích thu thập thông tin về những người nổi tiếng hay bất kì ai có các vụ bê bối rồi chia sẻ cho nhau. Đó là xâm phạm quyền riêng tư, có thể gây ra áp lực lớn cho người “được quan tâm”; nạn nhân có thể bị stress thậm chí tự tử.
*   Không lợi dụng vị thế của mình để làm việc xấu. Một số người trong không gian mạng có nhiều ảnh hưởng hơn, dễ điều khiển luồng dư luận theo hướng ủng hộ ý kiến của họ. Đó là các KOL (Key Opinion Leader) trong một lĩnh vực, các quản trị viên hệ thống, các quản trị diễn đàn, nhóm tin trên mạng.
*   Đạo đức trên mạng không cho phép bạn, với tư cách là một KOL, lợi dụng vị thế của mình vì mục đích xấu.
*   **Câu 1. Hãy cho biết những dấu hiệu để phát hiện lừa đảo qua mạng.**
*   **Câu 2. Hãy cho biết quy tắc nền tảng về văn hoá, đạo đức trên mạng.**
*   **Câu 1. Em sẽ làm gì khi nhận được email báo được thưởng một phần quà vì là khách hàng trung thành và phải gửi ngay một khoản tiền để nhận thưởng?**
*   **Câu 2. Ngày 17/6/2021, Bộ Thông tin và Truyền thông ban hành Bộ Quy tắc ứng xử trên mạng xã hội, trong đó có quy định chung về Quy tắc Lành mạnh: hành vi, ứng xử trên mạng xã hội phù hợp với các giá trị đạo đức, văn hoá, truyền thống tốt đẹp của dân tộc Việt Nam. Em hãy trích ra một số quy tắc ứng xử cho cá nhân về điều này.**
*   **Câu 1. Cần làm gì trước khi nhảy vào một liên kết trong email từ người gửi chưa chắc chắn đáng tin?**
*   **Câu 2. Quy tắc ứng xử văn minh và có đạo đức trên mạng có gì khác với trong cuộc sống thực?**
**Tóm tắt bài học**
*   Cảnh giác để phòng lừa đảo trên mạng: thận trọng với email, tin nhắn khác thường; không vội vã, cần kiểm tra để tránh trang web giả mạo trước khi nhập thông tin cá nhân hay chuyển tiền; hành động ngay để hạn chế thiệt hại khi cần thiết.
*   Ứng xử văn hoá và có đạo đức trên mạng: rộng lượng với người khác, không gây chiến trên mạng; tôn trọng “văn hoá nhóm”; tôn trọng quyền riêng tư, thời gian và công sức của người khác; không lợi dụng vị thế của mình để làm việc xấu.
*   **CHỦ ĐỀ F**
*   **GIẢI QUYẾT VẤN ĐỀ VỚI SỰ TRỢ GIÚP CỦA MÁY TÍNH**
*   **GIỚI THIỆU CÁC HỆ CƠ SỞ DỮ LIỆU**
*   **BÀI 1: BÀI TOÁN QUẢN LÝ VÀ CƠ SỞ DỮ LIỆU**
*   **Học xong bài này, em sẽ:**
    *   Nhận biết được nhu cầu lưu trữ dữ liệu và khai thác thông tin cho bài toán quản lí.
    *   Diễn đạt được khái niệm hệ cơ sở dữ liệu, nếu được ví dụ minh họa.
*   **Có một số cụm từ mà em đã từng nghe và có thể em đã từng dùng, ví dụ:** "Quản lí học sinh", "Quản lí nhân sự", "Quản lí chi tiêu cá nhân",... Theo em, việc quản lí có liên quan đến việc lưu trữ và xử lí dữ liệu không? Hãy nêu một việc em đã làm để quản lí một hoạt động nào đó của mình.
*   **1. Bài toán quản lí**
    *   Có rất nhiều bài toán quản lí cho các tổ chức lớn, nhỏ khác nhau với mức độ phức tạp khác nhau và ngay cả mỗi cá nhân cũng có những nhu cầu quản lí của riêng mình. Quản lí là công việc rất phổ biến. Xã hội càng phát triển, càng văn minh thì nhu cầu và chất lượng quản lí các hoạt động càng cao.
    *   Việc quản lí một tổ chức gắn liền với những dữ liệu phản ánh thông tin về hoạt động của tổ chức đó. Ví dụ: Dựa trên kết quả học tập của lớp mà giáo viên có thể đề xuất với nhà trường danh sách những em tham gia bồi dưỡng học sinh giỏi môn Tin học; để khách sạn quyết định có nhận cho khách thuê phòng hay không tuỳ thuộc vào thông tin về số phòng còn trống chưa ai thuê trong thời gian cụ thể đó. Trong hai ví dụ trên đây, dễ thấy rằng nếu thông tin không chính xác sẽ dẫn đến những hậu quả đáng tiếc.
    *   Thông tin dùng trong bài toán quản lí phải chính xác, kết quả xử lí thông tin phải đáng tin cậy để giúp có được quyết định đúng đắn, hợp lí.
*   **2. Xử lí thông tin trong bài toán quản lí**
    *   Các bài toán quản lí đều có chung đặc điểm là lưu trữ và xử lí dữ liệu về hoạt động của một tổ chức.
# Xử lí thông tin trong bài toán quản lí
Thông thường, từ “hồ sơ” được dùng để chỉ một tập hợp dữ liệu được tổ chức và thể hiện theo những khuôn mẫu nào đó. Xử lí thông tin trong bài toán quản lí bao gồm: tạo lập hồ sơ, cập nhật và khai thác thông tin.
## a) Tạo lập hồ sơ
Để quản lí việc học tập của một lớp, hồ sơ của lớp thường có cấu trúc dạng bảng để dễ theo dõi.
*   Để phản ánh đúng thực tế, dữ liệu trong bảng phải đầy đủ và chính xác.
*   Dữ liệu phải đầy đủ so với yêu cầu quản lí. Ví dụ, muốn quản lí thông tin mỗi học sinh đã là đoàn viên hay chưa, bảng hồ sơ của lớp cần có thêm cột ghi nhận thông tin này, nếu sĩ số lớp là 45 thì bảng phải có 45 hàng dữ liệu.
*   Dữ liệu phải chính xác. Ví dụ, không thể có hai hàng trong bảng hoàn toàn giống nhau ở họ tên, ngày sinh và địa chỉ, vì hoặc đó là dư thừa dữ liệu hoặc không phân biệt được chính xác điểm của mỗi bạn trong hai bạn trùng tên đó.
*   Khi tạo lập hồ sơ cho mỗi bài toán quản lí, phải xác định đầy đủ những dữ liệu cần được lưu trữ, đồng thời dữ liệu nhập vào phải đúng đắn.
## b) Cập nhật dữ liệu
Dữ liệu được lưu trữ cần được cập nhật để phản ánh kịp thời những thay đổi diễn ra trên thực tế.
*   Ví dụ về cập nhật dữ liệu trong quản lí học tập của một lớp:
    *   Học sinh Hoàng Giang vừa chuyển nhà về địa chỉ “20 Chùa Bộc”, cần sửa đổi dữ liệu tương ứng, dữ liệu “27 Lò Sũ” không còn đúng nữa.
    *   Cần bổ sung một hàng mới ghi dữ liệu cho học sinh Trần Anh Tuấn mới chuyển đến lớp.
    *   Cần xoá dữ liệu của học sinh Nguyễn Thị Hà vì học sinh này đã chuyển trường do bố mẹ chuyển công tác về tỉnh khác.
*   Cập nhật dữ liệu gồm các thao tác: thêm, sửa, xoá dữ liệu. Toàn bộ dữ liệu sau mỗi lần cập nhật cũng phải thoả mãn tính đầy đủ và đúng đắn.
## c) Khai thác thông tin
Mục đích của việc lưu trữ và cập nhật dữ liệu là để khai thác thông tin, phục vụ cho việc điều hành công việc và ra quyết định của người quản lí.
*   Một số việc khai thác thông tin thường gặp là: tìm kiếm dữ liệu, thống kê, lập báo cáo.
*   Tìm kiếm dữ liệu là việc rút ra được các dữ liệu thoả mãn một số điều kiện nào đó từ dữ liệu đã lưu trữ. Ví dụ: tìm họ và tên học sinh có điểm môn Tin học cao nhất.
*   Thống kê là khai thác hồ sơ dựa trên tính toán để đưa ra các thông tin không có sẵn trong hồ sơ. Ví dụ: xác định điểm cao nhất và điểm thấp nhất của môn Tin học; xác định số học sinh là đoàn viên.
*   Lập báo cáo là sử dụng các kết quả tìm kiếm, thống kê, sắp xếp dữ liệu được rút ra để tạo lập một bộ hồ sơ mới có nội dung và cấu trúc theo một số yêu cầu cụ thể trong quản lí. Ví dụ: Hết mỗi học kì, giáo viên chủ nhiệm cần có một danh sách học sinh để nghị nhà trường khen thưởng, cuối năm học cần báo cáo phân loại học tập để lên kế hoạch ôn tập hè cho lớp và trao đổi với phụ huynh về hướng nghiệp cho các em.
*   Khai thác thông tin là để phục vụ kịp thời cho công tác quản lí. Do vậy, việc xử lí dữ liệu trong hồ sơ phải nhanh chóng, chính xác và thông tin kết xuất ra phải ở dạng dễ hiểu cho người quản lí.
## 3) Cơ sở dữ liệu và phần mềm hệ quản trị cơ sở dữ liệu
Theo em, có nên dùng phần mềm soạn thảo văn bản hay phần mềm bảng tính để tạo lập hồ sơ, cập nhật và khai thác thông tin trong hồ sơ phục vụ công tác quản lí của một tổ chức hay không? Vì sao?
*   Ngày nay, với khả năng lưu trữ dữ liệu khổng lồ, tốc độ truy xuất và xử lí dữ liệu vô cùng nhanh, máy tính là công cụ hỗ trợ đắc lực cho con người trong mọi hoạt động thông tin.
*   Tập hợp hồ sơ dữ liệu làm cơ sở cho việc quản lí các hoạt động của một tổ chức, được số hoá để máy tính truy cập, cập nhật và xử lí, được gọi là một cơ sở dữ liệu (CSDL).
*   Để giúp tạo lập, cập nhật CSDL và khai thác thông tin trong CSDL có loại phần mềm được gọi là hệ quản trị CSDL (Database Management System – DBMS).
### Cơ sở dữ liệu:
tập hợp dữ liệu được tổ chức sao cho máy tính có thể lưu trữ, truy cập, cập nhật và xử lí để phục vụ cho hoạt động của một đơn vị nào đó.
Hệ quản trị CSDL là một hệ thống chương trình giúp người dùng tương tác với CSDL qua các giao diện dễ hiểu, dễ dùng (như hệ thống bảng chọn, hộp thoại, các biểu mẫu, báo cáo,...).
*   Với CSDL, hệ quản trị CSDL là hệ thống chương trình truy cập dữ liệu nhưng tuân theo những ràng buộc để đảm bảo tính đúng đắn cho mỗi thao tác cập nhật dữ liệu và khai thác dữ liệu.
*   Mỗi đơn vị, mỗi tổ chức có những yêu cầu riêng và cụ thể trong khai thác CSDL thể hiện qua các mẫu (giao diện) cập nhật dữ liệu, các mẫu tìm kiếm dữ liệu và báo cáo thường dùng.
*   Hệ cơ sở dữ liệu của một đơn vị là cách gọi chung một tập hợp gồm: CSDL của đơn vị, hệ quản trị CSDL và các phần mềm ứng dụng có các giao diện tương tác với CSDL đáp ứng được nhu cầu quản lí của đơn vị đó.
*   Các phần mềm ứng dụng khác muốn sử dụng dữ liệu trong CSDL đều phải thông qua hệ quản trị CSDL giống như mọi chương trình máy tính đều phải chạy dưới sự kiểm soát, điều phối của hệ điều hành.
### Hệ quản trị CSDL:
phần mềm cung cấp môi trường thuận lợi và hiệu quả để tạo lập, lưu trữ và khai thác dữ liệu của CSDL.
## 4 Thực hành tìm hiểu các yêu cầu của một bài toán quản lí và CSDL phục vụ bài toán đó
Em hãy hình dung việc quản lí thư viện của một trường học, thảo luận với bạn và thực hiện các yêu cầu sau đây.
### a) Mô tả hoạt động của thư viện
**Gợi ý:** Cho mượn sách hoặc trả sách như thế nào? Căn cứ vào đâu để biết ai đã mượn, trả sách gì? Căn cứ vào đâu để biết một quyển sách cụ thể đã được cho mượn và chưa được trả lại?...
### b) Liệt kê những dữ liệu cần có trong CSDL
**Gợi ý:** Những đối tượng cần quản lí là người đọc, sách cho mượn,...
*   – Với người đọc, cần quản lí thông tin gì? (Thông tin trên thẻ thư viện gồm: Số thẻ TV, Họ và tên,...).
*   – Với sách cho mượn, cần quản lí thông tin gì? (Thông tin về quyển sách gồm: Mã sách, Tên sách, Tác giả,...).
### c) Nêu ví dụ
Nêu thêm ít nhất hai ví dụ cho mỗi công việc sau đây:
*   – Cập nhật dữ liệu (cho CSDL):
**Ví dụ 1.** Khi có thêm một học sinh làm thẻ thư viện, cần bổ sung một số thông tin của học sinh này vào CSDL.
### Tìm kiếm dữ liệu:
Ví dụ 2. Tìm xem trong thư viện có quyển “Tôi tài giỏi, Bạn cũng thế” không?
### Thống kê và báo cáo:
Ví dụ 3. Xác định trong thư viện có bao nhiêu quyển sách về Tin học (giả sử sách về Tin học sẽ có hai chữ cái đầu trong mã sách là “TH”).
Giả sử dùng một bảng để chứa dữ liệu thể hiện thông tin về những người được mượn sách ở thư viện (những người có thể thư viện), em hãy chỉ ra một vài điều kiện cho dữ liệu trong bảng đó nhằm đảm bảo tính chính xác của thông tin. Theo em, nếu dùng một phần mềm bảng tính để tạo lập, lưu trữ bảng dữ liệu đó thì phần mềm bảng tính có tự động kiểm soát các cập nhật dữ liệu để đảm bảo được các điều kiện đã đặt ra hay không?
### Câu 1. Trong các câu sau, những câu nào đúng?
a) CSDL là tập hợp dữ liệu được lưu trữ trên thiết bị nhớ phục vụ cho hoạt động của một cơ quan, đơn vị nào đó.
*   b) Hệ CSDL của một đơn vị là phần mềm quản trị CSDL của đơn vị đó.
*   c) Các giá trị dữ liệu được lưu trữ trong CSDL phải thoả mãn một số ràng buộc để góp phần đảm bảo được tính đúng đắn của thông tin.
*   d) Hệ quản trị CSDL là chương trình kiểm soát được các cấp nhật dữ liệu.
### Câu 2. Theo em, những ứng dụng nào dưới đây cần có CSDL?
a) Quản lí bán vé máy bay.
*   b) Quản lí chi tiêu cá nhân.
*   c) Quản lí cước phí điện thoại.
*   d) Quản lí một mạng xã hội.
### Tóm tắt bài học
Các tổ chức hoạt động trong xã hội đều có nhu cầu lưu trữ dữ liệu và khai thác thông tin cho bài toán quản lí.
*   Muốn máy tính hỗ trợ đắc lực cho công tác quản lí, dữ liệu của một đơn vị phải được tổ chức trong một CSDL với tính đầy đủ và đúng đắn.
*   Phần mềm quản trị CSDL là loại phần mềm tạo ra môi trường thuận lợi để tạo lập CSDL, cập nhật cho CSDL theo cách đúng đắn, đồng thời kiểm soát được các truy cập đến dữ liệu, đảm bảo tính chính xác và sự an toàn của dữ liệu.
# BÀI 2: BẢNG VÀ KHOÁ CHÍNH TRONG CƠ SỞ DỮ LIỆU QUAN HỆ
### Học xong bài này, em sẽ:
Diễn đạt được khái niệm quan hệ (bảng) và khoá của một quan hệ. Giải thích được các khái niệm đó qua ví dụ minh hoạ.
*   Giải thích được ràng buộc khoá là gì.
*   Biết được các phần mềm quản trị CSDL có cơ chế kiểm soát các cập nhật dữ liệu để đảm bảo ràng buộc khoá.
Hồ sơ học sinh một lớp được tổ chức theo dạng bảng: mỗi hàng chứa dữ liệu về một học sinh, mỗi cột chứa dữ liệu về một thuộc tính của học sinh như: Họ và tên, Ngày sinh,... Theo em, cách tổ chức như vậy có ưu điểm gì trong việc quản lí thông tin học sinh của lớp?
## 1) Tổ chức dữ liệu trong CSDL quan hệ và các thao tác trên dữ liệu
### a) Cơ sở dữ liệu quan hệ
Cơ sở dữ liệu quan hệ là một tập hợp các bảng dữ liệu có liên quan với nhau.
*   Hình 1. Một phần bảng HỌC SINH 11 của một cơ sở dữ liệu quan hệ.
*   Tên của mỗi cột trong bảng cho biết ý nghĩa dữ liệu ở các ô thuộc cột đó.
# 1) Giới thiệu về CSDL quan hệ
Tên bảng cùng với tên cột giúp hiểu nghĩa của mỗi hàng trong bảng. Mỗi hàng trong bảng chứa một bộ các giá trị, ví dụ, trong Hình 1, bộ gồm 6 giá trị: “13109413”, “Phan Thuỳ Anh”, “29/10/2007”, “Nữ”, “☑”, “39 Hùng Vương” cho thông tin về một học sinh.
*   Mỗi một hàng trong bảng của CSDL quan hệ còn được gọi là một bản ghi. Mỗi cột của bảng còn được gọi là một trường. trong Hình 1 bảng HỌC SINH 11 có 6 trường phản ánh 6 thuộc tính của mỗi học sinh.
## a) Cập nhật dữ liệu trong CSDL quan hệ
*   Cập nhật dữ liệu của một bảng bao gồm các thao tác thêm, sửa và xoá dữ liệu của bảng.
*   Cấu trúc của một bảng bao gồm các mô tả cho các cột của bảng; người thiết kế CSDL sẽ định nghĩa cấu trúc của các bảng dựa vào các yêu cầu quản lí của đơn vị chủ quản.
*   Cập nhật dữ liệu của một bảng không làm thay đổi cấu trúc của bảng.
## b) Truy vấn trong CSDL quan hệ
*   Dữ liệu được tổ chức, lưu trữ trong CSDL là để người sử dụng có thể khai thác dữ liệu, rút ra thông tin phục vụ các hoạt động hoặc giúp đưa ra các quyết định phù hợp, kịp thời.
*   Bản chất việc khai thác một CSDL là tìm kiếm dữ liệu và kết xuất ra thông tin cần tìm, công việc này còn được gọi là truy vấn CSDL.
## c) Các ràng buộc dữ liệu trong CSDL quan hệ
*   Theo em, mỗi học sinh cần phải có riêng một Mã định danh để đưa vào hồ sơ quản lí hay không? Vì sao?
*   Dữ liệu trong CSDL quan hệ phải thoả mãn một số ràng buộc gọi là ràng buộc toàn vẹn về dữ liệu để đảm bảo tính xác định và đúng đắn của dữ liệu.
*   Ví dụ một số ràng buộc dữ liệu:
    *   Trong một bảng không có hai bản ghi giống nhau hoàn toàn.
    *   Trong cùng một bảng, mỗi trường có một tên phân biệt với tất cả các trường khác.
    *   Mỗi bảng có một tên phân biệt với các bảng khác trong cùng CSDL.
    *   Mỗi ô của bảng chỉ chứa một giá trị.
    *   Ngoài ra, tuỳ theo yêu cầu của bài toán quản lí cụ thể mà người thiết kế CSDL đặt thêm một số ràng buộc khác cho dữ liệu.
    *   Ví dụ: Người thiết kế CSDL cho trường học có thể yêu cầu Mã định danh của mỗi học sinh phải là một dãy số không quá 12 kí tự, tất cả các kí tự đều là số.
    *   Với ràng buộc như thế, việc nhập “0011234567899” vào cột Mã định danh là không hợp lệ, đó là vi phạm ràng buộc miền giá trị.
## 2) Khoá của một bảng
*   Trong một bảng, mỗi bản ghi thể hiện thông tin về một đối tượng (một cá thể hoặc một sự kiện) nên không thể có hai bản ghi giống nhau hoàn toàn.
*   Trong bảng chứa dữ liệu học sinh, ví dụ như bảng HỌC SINH 11, hai học sinh khác nhau sẽ có hai Mã định danh khác nhau.
*   Điều này giống như trường hợp số căn cước công dân của mỗi người xác định người đó là duy nhất, không nhầm lẫn với bất cứ ai.
*   Trong một bảng, có những tập hợp gồm một trường hay một số trường mà giá trị của chúng ở các bản ghi khác nhau là khác nhau.
*   Ví dụ ở Hình 2: một giá trị của trường STT chỉ xuất hiện ở một bản ghi; một bộ giá trị của hai trường CCCD và BHYT, chẳng hạn (“001160017719”, “HT3010101040124”) chỉ xuất hiện ở một bản ghi.
*   Tập hợp gồm một trường STT và tập hợp gồm hai trường CCCD và BHYT đều có tính chất: Dùng giá trị của nó xác định được duy nhất một bản ghi trong bảng.
*   Với ví dụ bảng trong Hình 2, có thể kể ra thêm một số tập hợp trường có tính chất như vậy:
    *   Tập chỉ gồm một trường CCCD.
    *   Tập gồm hai trường: STT, Họ và tên.
    *   Tập gồm tất cả sáu trường.
*   Khoá của một bảng là tập hợp một số trường có tính chất: mỗi bộ giá trị của các trường đó xác định duy nhất một bản ghi trong bảng và không thể bỏ bớt bất cứ trường nào mà tập hợp gồm các trường còn lại vẫn còn tính chất đó.
*   Ví dụ với bảng ở Hình 2:
    *   Tập hợp chỉ có một trường CCCD là một khoá.
    *   Tập hợp gồm hai trường STT, Họ và tên không phải là khoá vì nếu bỏ trường Họ và tên ra khỏi tập hợp này thì chỉ riêng STT cũng có tính chất xác định duy nhất một bản ghi trong bảng.
    *   Nếu không thể có hai nhân viên trùng nhau hoàn toàn ở Họ và tên, Ngày sinh thì tập hợp gồm hai trường Họ và tên, Ngày sinh cũng tạo thành một khoá.
    *   Nhưng tập gồm ba thuộc tính STT, Họ và tên, Ngày sinh không phải là một khoá.
*   Khoá của một bảng là tập hợp các trường (có thể chỉ là một trường) mà mỗi bộ giá trị của nó xác định duy nhất một bản ghi ở trong bảng và ta không thể bỏ đi trường nào mà tập hợp các trường còn lại vẫn còn có tính chất xác định duy nhất một bản ghi trong bảng.
*   Khi bảng có hơn một khoá, người ta thường chọn (chỉ định) một khoá làm khoá chính (Primary Key), ưu tiên chọn khoá gồm ít trường nhất, tốt nhất nếu chọn được khoá chỉ là một trường.
*   Bởi vậy, với bảng ở Hình 2, thay vì chọn khoá chính là tập hợp gồm hai trường...
*   Để phân biệt các hàng trong bảng, có thể chọn trường "STT" hay "CCCD" làm khoá chính, hoặc tạo thêm trường "MaNV" (Mã nhân viên) làm khoá chính cho bảng chứa thông tin nhân viên, phù hợp với cách tổ chức quản lí của đơn vị.
*   Việc cập nhật dữ liệu cho một bảng phải thoả mãn yêu cầu không làm xuất hiện hai bản ghi có giá trị khoá giống nhau. Yêu cầu này còn được gọi là ràng buộc khoá. **Hệ quản trị CSDL đảm bảo ràng buộc khoá**
*   Bất cứ hệ quản trị CSDL nào cũng có cơ chế kiểm soát, ngăn chặn những vi phạm ràng buộc khoá đối với việc cập nhật dữ liệu.
*   Để thực hiện điều đó, phần mềm yêu cầu người tạo lập CSDL chỉ định trường làm khoá chính và mỗi khi xuất hiện thao tác cập nhật dữ liệu, phần mềm sẽ tự động kiểm tra xem cập nhật đó có vi phạm ràng buộc khoá hay không. **Thực hành với khoá của bảng trong CSDL**
*   **Yêu cầu**: Sử dụng phần mềm Microsoft Access 365 tạo bảng SÁCH có cấu trúc như ở Hình 3, chỉ định trường "Mã sách" làm khoá chính và nhập nhiều hơn 5 bản ghi cho bảng.
*   **Hướng dẫn thực hiện**:
    *   **Bước 1**: Khởi chạy Microsoft Access 365 bằng cách nháy đúp chuột vào biểu tượng Access của phần mềm này.
    *   **Bước 2**: Tạo một CSDL mới, trong CSDL mới này tạo cấu trúc cho bảng SÁCH bằng cách thực hiện tuần tự các thao tác sau:
        *   Chọn "Blank Desktop Database" rồi đặt tên cho CSDL mới (hoặc nháy đúp chuột vào biểu tượng của "Blank Desktop Database", Access sẽ tự đặt tên cho CSDL mới tạo).
        *   Chọn "Create\Table Design" để xuất hiện cửa sổ khai báo cấu trúc bảng (Hình 3).
*   Trên mỗi hàng, nhập tên một trường (ở cột Field Name), chọn kiểu dữ liệu cho trường đó bằng cách đưa con trỏ chuột vào ô ở cột Data Type để làm xuất hiện danh sách cho chọn.
*   Bước 3. Chỉ định khoá chính cho bảng bằng cách chọn hàng có trường Mã sách (3.1), sau đó chọn Primary Key (3.2).
*   Bước 4. Chọn Save để lưu cấu trúc bảng và đặt tên cho bảng.
*   Bước 5. Chọn View để xuất hiện cửa sổ cho nhập các bản ghi vào bảng.
*   Chú ý: Nên thử nhập hai bản ghi giống nhau để xem phần mềm báo lỗi vì phạm ràng buộc khoá ra sao.
*   Để tiếp tục xây dựng CSDL quản lí một thư viện, em hãy cho biết:
    *   a) Dự kiến của em về cấu trúc bảng NGƯỜI ĐỌC, biết rằng bảng này dùng để lưu trữ dữ liệu về những người có thể thư viện.
    *   b) Trong các trường của bảng NGƯỜI ĐỌC, nên chọn trường nào làm khoá chính? Giải thích vì sao?
    *   c) Hãy nêu ví dụ cụ thể về nhập dữ liệu cho bảng NGƯỜI ĐỌC nhưng vi phạm ràng buộc khoá.
*   Trong các câu sau, những câu nào đúng?
    *   a) Trong CSDL quan hệ, mỗi bảng chỉ có một khoá.
    *   b) Khoá của một bảng chỉ là một trường.
    *   c) Nếu hai bản ghi khác nhau thì giá trị khoá của chúng phải khác nhau.
    *   d) Các hệ quản trị CSDL quan hệ tự động kiểm tra ràng buộc khoá để đảm bảo tính đúng đắn của dữ liệu.
**Tóm tắt bài học**
*   Một CSDL quan hệ là một tập hợp các bảng dữ liệu (quan hệ) có liên quan với nhau.
*   Mỗi bảng trong CSDL đều phải có khoá, đó là tập hợp gồm một hay một số trường cho phép xác định duy nhất một bản ghi trong bảng.
*   Dữ liệu trong một bảng phải thoả mãn ràng buộc khoá: Không có hai bản ghi giống nhau ở giá trị khoá. Mọi hệ quản trị CSDL quan hệ đều có cơ chế kiểm soát việc cập nhật dữ liệu để không xảy ra vi phạm ràng buộc khoá đối với mỗi bảng.
# BÀI 3: QUAN HỆ GIỮA CÁC BẢNG VÀ KHOÁ NGOÀI TRONG CƠ SỞ DỮ LIỆU QUAN HỆ
*   **Học xong bài này, em sẽ:**
    *   Diễn đạt được khái niệm khoá ngoài của một bảng và mối liên kết giữa các bảng.
    *   Giải thích được các khái niệm đó qua ví dụ minh họa.
    *   Giải thích được ràng buộc khoá ngoài là gì.
    *   Biết được các phần mềm quản trị CSDL có cơ chế kiểm soát các cập nhật dữ liệu để đảm bảo ràng buộc khoá ngoài.
*   **Để quản lí sách, người đọc và việc mượn/trả sách của một thư viện (TV) trường học, bạn Anh Thư dự định chỉ dùng một bảng. Theo em, trong trường hợp cụ thể này, việc đưa tất cả dữ liệu cần quản lí vào trong một bảng như Anh Thư thực hiện có ưu điểm và nhược điểm gì?**
*   **Gợi ý: Xét một số trường hợp sau:**
    *   1) Một học sinh mượn sách nhiều lần, mỗi lần mượn nhiều quyển sách.
    *   2) Cần bổ sung dữ liệu về số sách mới mua của thư viện.
*   **1.**
# Tính dư thừa dữ liệu
*   **a) Dư thừa dữ liệu có thể dẫn đến dữ liệu không nhất quán khi cập nhật**
    *   Có thể một số người nghĩ rằng nên đưa tất cả dữ liệu cần lưu trữ vào trong một bảng vì khi cần tìm thông tin nào đó thì chỉ phải tìm trong một bảng.
    *   Thực tế cho thấy đa số bài toán quản lí cần dùng nhiều hơn một bảng dữ liệu.
    *   Nếu chỉ dùng một bảng thì rất có thể dẫn đến tình trạng dư thừa dữ liệu.
    *   Ví dụ: trường hợp nếu ở phần khởi động, giả sử học sinh có số thẻ TV “HS-002” tên là “Lê Bình” sinh ngày “02/3/2007”, học lớp “11A1” đã có 68 lần mượn sách.
    *   Như vậy, bộ giá trị (“HS-002”, “Lê Bình”, “02/3/2007”, “11A1”) phải xuất hiện 68 lần (trên 68 bản ghi của bảng).
    *   Tình trạng dư thừa dữ liệu có thể dẫn đến sai nhầm, không nhất quán về dữ liệu.
    *   Việc gõ nhập 68 lần.
    *   bộ dữ liệu về Lê Bình sẽ dễ xuất hiện sai nhầm hơn so với 68 lần chỉ gõ Số thẻ TV của Lê Bình vào bảng.
    *   Giải pháp tránh dư thừa là có thể dùng một bảng khác chỉ chứa dữ liệu về người đọc và có khoá chính là trường Số thẻ TV.
*   **b) CSDL cần được thiết kế để tránh dư thừa dữ liệu**
    *   Dư thừa dữ liệu do trùng lặp dữ liệu có các nhược điểm là tốn nhiều vùng nhớ lưu trữ không cần thiết và dữ liệu có thể không nhất quán (dữ liệu bị mâu thuẫn) khi cập nhật dữ liệu.
    *   Để tránh những nhược điểm do dư thừa dữ liệu gây ra, CSDL quan hệ thường được thiết kế gồm một số bảng, có bảng chứa dữ liệu về riêng một đối tượng (cá thể) cần quản lí, có bảng chứa dữ liệu về những sự kiện liên quan đến các đối tượng được quản lí.
    *   Ví dụ, ở một thư viện nhỏ, CSDL có thể gồm 3 bảng:
        *   Bảng SÁCH chứa dữ liệu về các quyển sách của thư viện.
        *   Bảng NGƯỜI ĐỌC chứa dữ liệu về những người đọc (có thể thư viện).
        *   Bảng MƯỢN-TRẢ chứa dữ liệu về sự việc một người mượn/trả một quyển sách, sự việc này liên quan đến hai đối tượng quản lí (một người đọc và một quyển sách).
    *   Với cách tổ chức CSDL như trong ví dụ vừa nêu, mỗi bảng sẽ giảm được dữ liệu lặp lại, tránh thông tin dư thừa và việc cập nhật dữ liệu sẽ bớt được nhiều rủi ro sai nhầm.
*   2. Liên kết giữa các bảng và khoá ngoại
    *   Để trích xuất thông tin từ CSDL quan hệ, ta có thể cần dữ liệu trong hơn một bảng và phải ghép nối đúng được dữ liệu giữa các bảng với nhau.
# Ví dụ về CSDL Thư viện và các mối liên kết:
*   CSDL Thư viện gồm ba bảng và để trả lời yêu cầu về Họ và tên, Lớp của học sinh mượn sách mã TH-01, cần dữ liệu từ hai bảng MƯỢN-TRẢ và NGƯỜI ĐỌC.
*   Giá trị "HS-002" của Số thẻ TV trong bảng MƯỢN-TRẢ dẫn đến một bản ghi trong bảng NGƯỜI ĐỌC chứa thông tin cần tìm.
*   Thuộc tính Số thẻ TV tạo mối liên kết giữa bảng MƯỢN-TRẢ và NGƯỜI ĐỌC, với mỗi giá trị Số thẻ TV trong MƯỢN-TRẢ được giải thích chi tiết hơn trong NGƯỜI ĐỌC.
*   Trong mối liên kết này, bảng MƯỢN-TRẢ là bảng tham chiếu, và NGƯỜI ĐỌC là bảng được tham chiếu.
*   Tương tự, bảng MƯỢN-TRẢ và SÁCH cũng liên kết qua thuộc tính Mã sách, với MƯỢN-TRẢ là bảng tham chiếu và SÁCH là bảng được tham chiếu.
*   **Xác định thuộc tính liên kết và khoá:**
    *   Để xác định tham chiếu, thuộc tính liên kết giữa hai bảng phải là khoá của bảng được tham chiếu.
    *   Trong ví dụ, Số thẻ TV phải là khoá chính của bảng NGƯỜI ĐỌC và là khoá ngoài của bảng MƯỢN-TRẢ.
    *   Liên kết giữa hai bảng trong CSDL được thực hiện thông qua cặp khoá chính – khoá ngoài.
*   **Hệ quản trị CSDL đảm bảo ràng buộc khoá ngoài:**
    *   **Tình huống kiểm tra ràng buộc khoá ngoài:** CSDL Thư viện có bảng MƯỢN-TRẢ liên kết với bảng NGƯỜI ĐỌC qua khoá ngoài Số thẻ TV. Bảng NGƯỜI ĐỌC hiện có bốn bản ghi (ghi nhận dữ liệu về bốn học sinh đã làm thẻ thư viện).
    *   Câu hỏi đặt ra là việc thêm một bản ghi mới vào bảng MƯỢN-TRẢ có hợp lí không, và cần giải thích vì sao.
*   **Ràng buộc khoá ngoài:**
    *   Khi hai bảng trong một CSDL có liên kết với nhau, mỗi giá trị khoá ngoài ở bảng tham chiếu sẽ được giải thích chi tiết hơn ở bảng được tham chiếu. Ví dụ, “HS-001”.
    *   Được giải thích bằng thông tin “Họ và tên: Trần Văn An; Ngày sinh: 14/9/2006; Lớp: 12A2”.
    *   Nếu có giá trị khoá ngoài nào không xuất hiện trong giá trị khoá ở bảng được tham chiếu thì xảy ra hiện tượng mất tham chiếu.
    *   “HS-007” không xuất hiện trong Số thẻ TV của bảng NGƯỜI ĐỌC.
    *   Do vậy, việc bổ sung cho bảng MƯỢN-TRẢ một bản ghi mới có giá trị khoá ngoài là “HS-007” sẽ làm cho dữ liệu trong CSDL không còn đúng đắn nữa, không giải thích được “HS-007” là số thẻ thư viện của ai.
    *   Muốn cập nhật đó hợp lệ, phải bổ sung bản ghi có giá trị khoá là “HS-007” vào bảng NGƯỜI ĐỌC trước.
    *   Đảm bảo tính tham chiếu đầy đủ giữa các bảng có liên kết với nhau cũng là một phần của việc đảm bảo tính toàn vẹn của dữ liệu.
    *   Ràng buộc này áp dụng cho khoá ngoài nên được gọi là ràng buộc khoá ngoài.
    *   Nói một cách cụ thể hơn, ràng buộc khoá ngoài là yêu cầu mọi giá trị của khoá ngoài trong bảng tham chiếu phải xuất hiện trong giá trị khoá ở bảng được tham chiếu.
*   **b) Khai báo liên kết giữa các bảng**
    *   Các hệ quản trị CSDL đều cho người tạo lập CSDL được khai báo liên kết giữa các bảng.
    *   Phần mềm quản trị CSDL sẽ căn cứ vào các liên kết đó để kiểm soát tất cả thao tác cập nhật, không để xảy ra những vi phạm ràng buộc khoá ngoài.
*   **④ Thực hành về bảng với khoá ngoài**
    *   **Yêu cầu:** Khám phá cách khai báo liên kết giữa các bảng trong môi trường Access và nhận biết các cập nhật vi phạm ràng buộc khoá ngoài.
    *   **Hướng dẫn thực hiện:**
        *   **Bước 1.** Mở CSDL Thư viện đã có bảng SÁCH (kết quả mục thực hành ở Bài 2).
        *   Tạo cấu trúc cho bảng NGƯỜI ĐỌC và bảng MƯỢN-TRẢ.
        *   Chọn Số thẻ TV làm khoá chính cho bảng NGƯỜI ĐỌC.
        *   Chọn khoá chính của bảng MƯỢN-TRẢ gồm ba thuộc tính: Số thẻ TV, Mã sách và Ngày mượn.
*   **Bước 2. Khám phá cách khai báo liên kết giữa các bảng.**
    *   Trong dải Database Tools, chọn Relationships.
    *   Dùng chuột kéo thả các bảng vào cửa sổ khai báo liên kết (vùng trống ở giữa).
    *   Dùng chuột kéo thả khoá ngoài của bảng tham chiếu thả vào khoá chính của bảng được tham chiếu, làm xuất hiện hộp thoại Edit Relationships.
    *   Đánh dấu hộp kiểm Enforce Referential Integrity và chọn Create.
*   **Bước 3. Khám phá báo lỗi của phần mềm quản trị CSDL khi cập nhật vi phạm ràng buộc khoá ngoài.**
    *   Thêm một vài bản ghi trong đó có bản ghi vi phạm lỗi ràng buộc khoá ngoài, quan sát báo lỗi của phần mềm.
    *   Chọn xoá một bản ghi trong bảng NGƯỜI ĐỌC nếu giá trị Số thẻ TV trong bản ghi này xuất hiện trong bảng MƯỢN-TRẢ, quan sát báo lỗi của phần mềm.
*   **Câu hỏi:** Trong việc tạo lập CSDL, sau khi tạo xong cấu trúc cho hai bảng mà ta dự kiến có liên kết với nhau bằng khoá ngoài, ta nên khai báo liên kết trước hay nên nhập dữ liệu cho hai bảng trước? Hãy giải thích vì sao.
*   **Câu hỏi:** Trong các câu sau, những câu nào đúng?
    *   a) Một trường là khoá ngoài của một bảng nếu nó là khoá của bảng đó và đồng thời xuất hiện trong một bảng khác.
    *   b) Khoá ngoài của một bảng là tập hợp một số trường của bảng đó và đồng thời là khoá của một bảng khác.
    *   c) Khi hai bảng có liên kết với nhau qua khoá chính – khoá ngoài, chỉ khi bổ sung bản ghi vào các bảng mới cần thoả mãn ràng buộc khoá ngoài.
    *   d) Các hệ quản trị CSDL quan hệ tự động kiểm tra và chỉ chấp nhận các cặp nhật thoả mãn ràng buộc khoá ngoài.
*   **Tóm tắt bài học**
    *   CSDL quan hệ có thể gồm một số bảng, trong đó có những bảng có mối liên kết với nhau. Những liên kết này giúp tìm được những thông tin đúng đắn và đầy đủ.
    *   Nếu hai bảng có chung một trường và trường này là khoá của một trong hai bảng thì trường đó là khoá ngoài của bảng còn lại. Hai bảng có thể liên kết với nhau thông qua khoá ngoài.
    *   Dữ liệu trong hai bảng liên kết với nhau qua khoá ngoài cần phải thoả mãn ràng buộc khoá ngoài: Mọi giá trị khoá ngoài đều phải xuất hiện trong trường khoá ở bảng được tham chiếu. Mọi hệ quản trị CSDL quan hệ đều có cơ chế đảm bảo cập nhật dữ liệu không vi phạm ràng buộc khoá ngoài đối với các liên kết giữa các bảng.
# BÀI 4: CÁC BIỂU MẪU CHO XEM VÀ CẬP NHẬT DỮ LIỆU
*   **Học xong bài này, em sẽ:**
    *   Diễn đạt được khái niệm biểu mẫu trong các CSDL và ứng dụng CSDL.
    *   Giải thích được những ưu điểm khi người dùng xem và cập nhật dữ liệu cho CSDL thông qua biểu mẫu.
*   **Khi nhập dữ liệu vào một bảng của CSDL quan hệ, theo em có thể gặp những lỗi nào? Em hãy cho ví dụ.**
# 1. Khái niệm và chức năng của biểu mẫu
*   **a) Chức năng của biểu mẫu**
    *   Phục vụ cho hoạt động của một tổ chức nên một CSDL có thể được nhiều người cùng sử dụng. Thay vì cho phép người dùng tương tác trực tiếp với CSDL, các giao diện người dùng đã được thiết kế phù hợp với mỗi nhóm người làm việc với CSDL. Biểu mẫu là giao diện thuận tiện để người dùng tương tác với CSDL khi xem dữ liệu, hạn chế bớt lỗi, tránh vi phạm ràng buộc về dữ liệu khi cập nhật CSDL.
    *   **Biểu mẫu được thiết kế nhằm các mục đích sau:**
        *   Hiển thị dữ liệu trong bảng dưới dạng phù hợp để xem.
        *   Cung cấp một khuôn dạng thuận tiện để nhập và sửa dữ liệu.
# Biểu Mẫu và Truy Vấn Cơ Sở Dữ Liệu
## 1. Biểu Mẫu
### a) Giới Thiệu
*   Cung cấp các nút lệnh để người dùng có thể sử dụng, thông qua đó thực hiện một số thao tác với dữ liệu.
*   Phổ biến nhất là các biểu mẫu hiển thị dữ liệu cho từng nhóm người dùng và biểu mẫu cho người nhập dữ liệu.
### b) Tạo biểu mẫu
*   Các hệ quản trị CSDL thường cung cấp các công cụ để tạo được biểu mẫu cho người dùng CSDL.
*   Muốn nhanh chóng có được biểu mẫu theo ý mình, ta có thể dùng công cụ thiết kế biểu mẫu tự động, sau đó điều chỉnh thêm để có một biểu mẫu thân thiện hơn, thuận tiện hơn trong sử dụng.
*   Những ứng dụng CSDL đơn giản sử dụng các biểu mẫu được tạo ra theo cách này.
*   Trong khi đó, ở những ứng dụng CSDL lớn và phức tạp, (thường là những phần mềm được xây dựng trên nền hệ quản trị CSDL), các biểu mẫu như một thành phần của phần mềm ứng dụng được tạo ra nhờ một ngôn ngữ lập trình.
## 2. Biểu Mẫu Cho Xem Dữ Liệu
*   Các hệ quản trị CSDL thường cung cấp công cụ tạo lập nhanh chóng những biểu mẫu cho xem dữ liệu.
*   Những biểu mẫu loại này không cho người xem sửa đổi dữ liệu.
*   Việc thiết kế những biểu mẫu như vậy là để hỗ trợ cho những nhóm người dùng tra cứu thông tin của CSDL trong phạm vi được phép:
    *   Biểu mẫu chỉ hiển thị dữ liệu người dùng cần hoặc phần dữ liệu được phép xem. Có thể thiết kế biểu mẫu hiển thị chỉ một phần của dữ liệu trong bảng.
    *   Biểu mẫu hiển thị các bản ghi theo thứ tự sắp xếp của một trường nào đó.
    *   Biểu mẫu cho xem dữ liệu được lọc theo một tiêu chí nào đó và có thể lọc dần nhiều bước.
    *   Các biểu mẫu minh họa trong bài đều được tạo ra bởi hệ quản trị CSDL Microsoft Access 365.
    *   Biểu mẫu như ở Hình 1 chỉ hiển thị một số trường của bảng dữ liệu nguồn THÔNG TIN HỌC SINH LỚP 11 (không hiển thị điểm các môn học).
    *   Các thanh trượt dọc và ngang được dùng để xem những dữ liệu bị khuất trong cửa sổ biểu mẫu.
    *   Các nút **► ◄** được dùng để chuyển đến xem bản ghi đứng trước hoặc đứng sau bản ghi hiện thời.
    *   Có thể chỉ hiển thị danh sách các bản ghi thoả mãn điều kiện nào đó (ví dụ xem danh sách học sinh là Đoàn viên) bằng cách sử dụng chức năng lọc bản ghi theo điều kiện.
    *   Người dùng biểu mẫu có thể thay đổi các điều kiện lọc, điều kiện sắp xếp ngay trên biểu mẫu để xem được dữ liệu tương ứng.
    *   Biểu mẫu cũng có thể hiển thị các trường từ nhiều bảng khác nhau.
    *   Hình 2 cho thấy dữ liệu trong biểu mẫu lấy từ 3 bảng SÁCH, NGƯỜI ĐỌC và MƯỢN-TRẢ của CSDL Thư viện trong ví dụ đã nêu.
## 3. Biểu Mẫu Cho Cập Nhật Dữ Liệu
*   Theo em, có những bất lợi nào trong việc mở một bảng của CSDL quan hệ rồi trực tiếp cập nhật dữ liệu (thêm bản ghi, sửa các bản ghi trong đó)?
*   Các hệ quản trị CSDL quan hệ cũng thường cung cấp công cụ cho phép tạo lập nhanh chóng những biểu mẫu cập nhật dữ liệu. Những biểu mẫu loại này có các ô nhập dữ liệu còn để trống hoặc chứa dữ liệu đã có nhưng cho phép sửa đổi. Các ô và nhãn đi kèm được bố trí hợp lí cho việc xem và thực hiện thao tác cập nhật.
*   Việc thiết kế những biểu mẫu như vậy giúp việc cập nhật dữ liệu được tiện lợi hơn, hạn chế được những sai nhằm khi cập nhật:
    *   Tránh được các cập nhật vi phạm ràng buộc toàn vẹn như ràng buộc khoá, ràng buộc khoá ngoài.
    *   Tránh được các cập nhật vi phạm ràng buộc miền giá trị, tức là không đưa vào giá trị nằm ngoài tập giá trị được chấp nhận.
    *   Ví dụ 1. Biểu mẫu ở Hình 3 dùng để nhập dữ liệu. Dữ liệu của các trường ở nửa bên trên biểu mẫu đó (Mã định danh,... Giới tính) được hiển thị và bị khoá lại không cho thay đổi.
*   Có thể thiết kế biểu mẫu dùng để cập nhật dữ liệu cho bảng MƯỢN-TRẢ và tránh được vi phạm ràng buộc khoá ngoại.
*   Thiết kế để Số thẻ TV của người mượn (hay người trả) không thể gõ nhập vào mà chỉ lựa chọn trong một danh sách thả xuống.
*   Biểu mẫu cho phép nhập dữ liệu Ngày mượn, Ngày trả theo cách mở lịch và chọn ngày trên đó.
*   Một số CSDL trực tuyến cũng có các biểu mẫu cho sẵn phục vụ người dùng, như biểu mẫu khai báo y tế mà người dân có thể điền thông tin trên điện thoại di động.
## 4. Thực Hành Tạo Biểu Mẫu và Cập Nhật Dữ Liệu
### Nhiệm vụ 1:
Thầy, cô giáo đã dựng sẵn 3 bảng: SÁCH, NGƯỜI ĐỌC, MƯỢN-TRẢ cùng một vài biểu mẫu trong CSDL Thư viện (tạo bằng Access). Em hãy sử dụng biểu mẫu NHẬP DỮ LIỆU MƯỢN-TRẢ SÁCH đã có để nhập 3 bản ghi mới cho bảng MƯỢN-TRẢ.
#### Hướng dẫn thực hiện:
*   Bước 1. Kích hoạt Microsoft Access.
*   Bước 2. Mở CSDL Thư viện, chọn biểu mẫu NHẬP DỮ LIỆU MƯỢN-TRẢ SÁCH.
*   Bước 3. Trên biểu mẫu vừa mở, hãy nhập ít nhất 3 bản ghi.
*   Bước 4. Tìm và mở biểu mẫu XEM THÔNG TIN MƯỢN-TRẢ SÁCH để kiểm tra xem những bản ghi nhập vào ở Bước 3 đã xuất hiện trong bảng MƯỢN-TRẢ chưa.
*   Bước 5. Kết thúc phiên làm việc với CSDL Thư viện, trong bảng chọn File chọn nút lệnh Close để đóng CSDL này.
### Nhiệm vụ 2:
Khám phá cách dùng công cụ tạo biểu mẫu trong Access.
#### Hướng dẫn thực hiện:
*   Bước 1. Chọn mở CSDL HỌC SINH 11. Mở bảng HỌC SINH 11.
*   **Bước 2:** Nháy chuột vào Create để xuất hiện các công cụ tạo lập biểu mẫu.
*   **Bước 3:** Chọn và khám phá công cụ Form Wizard. Cần chọn các trường cho biểu mẫu, đặt tên biểu mẫu, sau đó chọn Finish.
*   **Bước 4:** Đóng CSDL HỌC SINH 11 để kết thúc phiên làm việc với CSDL này.
## 5. Câu Hỏi Thảo Luận
*   Nếu là người xây dựng một CSDL quản lí học sinh khối 11 của trường mình, em sẽ xây dựng những biểu mẫu nào? Mỗi biểu mẫu em định thiết kế sẽ có chức năng nào và đem lại thuận lợi gì, cho ai?
## 6. Câu Hỏi Trắc Nghiệm
*   Trong các câu sau, những câu nào đúng?
    *   a) Mỗi biểu mẫu đều được dùng chung cho tất cả mọi người sử dụng CSDL.
    *   b) Mỗi biểu mẫu là một cửa sổ cho người dùng xem toàn bộ thông tin trong một bảng của CSDL.
    *   c) Khi cập nhật dữ liệu, cần sử dụng biểu mẫu vì có thể đảm bảo được rằng buộc khoá và khoá ngoài, tránh được nhiều sai nhầm về dữ liệu.
    *   d) Biểu mẫu là một giao diện được thiết kế để kiểm soát các truy cập của người dùng đến dữ liệu trong CSDL.
## 7. Tóm Tắt Bài Học
*   Biểu mẫu là một loại giao diện cho người dùng CSDL tương tác với dữ liệu nguồn trong việc xem và cập nhật dữ liệu.
*   Biểu mẫu đem lại sự thuận tiện cho các nhóm người dùng làm việc với CSDL và giúp hạn chế những vi phạm trong cập nhật nhằm tăng cường sự đảm bảo tính đúng đắn của dữ liệu.
## 8. Mục Tiêu Học Tập
*   **Học xong bài này, em sẽ:**
    *   Diễn đạt được khái niệm truy vấn CSDL.
    *   Giải thích được cấu trúc cơ bản SELECT...FROM...WHERE... của câu lệnh SQL.
    *   Nêu được một vài ví dụ minh họa việc dùng truy vấn để tổng hợp, tìm kiếm dữ liệu trên một bảng.
## 9. Hoạt Động
*   Em hãy nêu một vài ví dụ cụ thể về khai thác thông tin trong một CSDL mà em biết.
## 10. Khái Niệm Truy Vấn CSDL
*   Truy vấn CSDL (Query) là một phát biểu thể hiện yêu cầu của người dùng đối với CSDL.
*   Đó có thể là yêu cầu thao tác trên dữ liệu như: thêm, sửa, xoá bản ghi,...
*   Đó cũng có thể là yêu cầu khai thác CSDL.
*   Dù đơn giản hay phức tạp thì bản chất việc khai thác một CSDL là tìm kiếm dữ liệu đã lưu giữ trong đó và hiển thị kết quả theo khuôn dạng thuận lợi cho người khai thác.
*   Để máy tính có thể hiểu và thực thi được yêu cầu của người dùng, truy vấn phải được viết theo một số quy tắc của hệ quản trị CSDL.
*   Nói cách khác, mỗi hệ quản trị CSDL có ngôn ngữ truy vấn của nó.
*   Đối với các hệ quản trị CSDL quan hệ, ngôn ngữ truy vấn phổ biến nhất và nổi tiếng nhất cho đến nay là SQL (Structured Query Language).
*   Hầu hết các hệ quản trị CSDL quan hệ, ngay cả những hệ thống có ngôn ngữ của riêng chúng, đều hỗ trợ một số phiên bản SQL.
*   Bài học này tập trung vào việc dùng SQL thể hiện yêu cầu tìm và trích rút dữ liệu trong CSDL.
*   Chẳng hạn, giáo viên chủ nhiệm cần danh sách những học sinh của lớp có điểm tổng kết môn Tin học từ 8,0 trở lên.
*   Tùy theo hệ quản trị CSDL, có thể có những truy vấn tóm tắt dữ liệu và thực hiện một số phép tính trên dữ liệu để đưa ra kết quả.
*   Với những truy vấn như vậy, kết quả trả ra có thể là hình ảnh, đồ thị, ví dụ như kết quả của yêu cầu phân tích xu hướng mua/bán một mặt hàng trong 6 tháng đầu năm của một công ty thương mại.
## 11. Khai Thác CSDL Bằng Câu Truy Vấn SQL Đơn Giản
*   Em hãy quan sát mẫu câu truy vấn ở Hình 1a dùng để tìm dữ liệu trong CSDL và một ví dụ truy vấn ở Hình 1b. Muốn tìm Họ và tên, Ngày sinh, điểm môn Toán và điểm môn Ngữ văn của những học sinh có điểm môn Toán trên 7.0 thì em sẽ dùng câu truy vấn SQL như thế nào?
*   Cấu trúc cơ bản của một câu truy vấn viết bằng ngôn ngữ SQL như ở Hình 1a:
    *   `SELECT`: Tên các trường dữ liệu cần đưa ra kết quả.
    *   `FROM`: Tên bảng trong CSDL được truy cập để lấy dữ liệu.
    *   `WHERE`: Biểu thức logic chọn các bản ghi đưa ra kết quả.
*   Để có kết quả của một câu truy vấn, hệ quản trị CSDL sẽ truy cập vào các bảng dữ liệu có tên được chỉ ra sau FROM. Các bản ghi thoả mãn điều kiện tìm kiếm đứng sau WHERE sẽ được lựa chọn. Kết quả câu truy vấn là những bản ghi đã được lựa chọn và chỉ giá trị của những trường có tên đứng sau SELECT mới được hiển thị.
# BÀI 6: TRUY VẤN TRONG CƠ SỞ DỮ LIỆU QUAN HỆ (tiếp theo)
*   **Học xong bài này, em sẽ:**
    *   Đưa ra được một vài ví dụ minh hoạ cho việc dùng truy vấn để tổng hợp, tìm kiếm dữ liệu trên hơn một bảng.
## Câu hỏi
*   Theo em, việc khai báo liên kết giữa một số bảng trong một CSDL quan hệ có ý nghĩa gì?
## Câu lệnh truy vấn SQL với liên kết các bảng
### Nội dung
*   Xét CSDL được mô tả như ở Hình 1. Nếu cần biết tên quyển sách mà người có thể thư viện HS-001 đã mượn vào ngày 02/10/2022, ta có thể dùng câu truy vấn trên một bảng được không? Nếu tìm thông tin này bằng cách tra cứu thủ công (không dùng máy tính) thì em sẽ làm như thế nào?
*   **Khi khai thác CSDL quan hệ, nhiều tình huống cần phải kết hợp dữ liệu ở hai hoặc nhiều bảng để đưa ra được dữ liệu cần tìm.**
    *   Kiểu kết hợp thường gặp là ghép nối một bản ghi của bảng này với một hay nhiều bản ghi của bảng khác, tạo nên một hay nhiều bản ghi mới đầy đủ thông tin hơn.
    *   Kết quả của các ghép nối là các bản ghi mới được đưa vào một bảng tạm thời.
    *   Hệ quản trị CSDL sẽ chọn lựa trong bảng tạm thời này những dữ liệu thoả mãn điều kiện tìm để đưa ra kết quả.
    *   Ví dụ, để tìm Mã sách của những quyển sách mà học sinh Trần Văn An đã mượn, hệ quản trị CSDL cần kết hợp dữ liệu ở bảng NGƯỜI ĐỌC với dữ liệu ở bảng MƯỢN-TRẢ.
    *   Mục đích kết hợp dữ liệu của hai bảng này là để có một bảng dữ liệu tạm thời mà mỗi bản ghi của nó cho ta dữ liệu đúng đắn và đầy đủ gồm Họ và tên, Số thẻ TV,... của một người đọc cùng với Mã sách của quyển sách họ mượn và ngày mượn.
*   **Khi kết hợp dữ liệu, hai bản ghi thuộc hai bảng khác nhau trong CSDL chỉ được ghép lại nếu chúng thoả mãn một điều kiện mà ta gọi là điều kiện kết nối.**
    *   Trong tình huống nêu trên (kết nối dữ liệu từ bảng NGƯỜI ĐỌC và bảng MƯỢN-TRẢ), điều kiện kết nối là giá trị ở trường Số thẻ TV của hai bản ghi đó phải trùng nhau.
*   **Việc trích rút dữ liệu từ nhiều bảng khác nhau được thực hiện như những truy vấn trên một bảng dữ liệu, đó là bảng dữ liệu tạm thời chứa kết quả kết nối các bản ghi.**
    *   Hệ quản trị CSDL chỉ việc lựa chọn dữ liệu trong bảng kết quả kết nối đó để đưa ra ví dụ như “Trần Văn An” đã mượn quyển sách có mã sách “AN-01” và quyển sách có mã sách “TH-02”.
*   **Để kết hợp dữ liệu từ các bảng có trường chung theo cách ghép nối các bản ghi thoả mãn một điều kiện nào đó, SQL sử dụng từ khoá JOIN trong mệnh đề FROM.**
    *   Có một số kiểu JOIN khác nhau, trong đó INNER JOIN được dùng phổ biến nhất.
    *   Phần dưới giải thích mẫu viết mệnh đề FROM (trong câu truy vấn) sử dụng INNER JOIN.
*   Trong mẫu nêu trên, kí hiệu Ø dùng để chỉ bất kỳ toán tử so sánh nào, bao gồm: `=`, `<`, `<=`, `<>`, `>`, `>=`. Kí hiệu `<>` thể hiện toán tử so sánh khác.
*   Trên thực tế, từ khóa `INNER JOIN` thường được dùng với điều kiện kết nối là sự trùng khớp giá trị trên một trường chung của hai bảng.
*   Mệnh đề `FROM` trong một câu truy vấn có thể yêu cầu kết nối hai bản ghi từ các bảng khác nhau, ví dụ: bảng `NGƯỜI ĐỌC` và bảng `MƯỢN-TRẢ`.
*   Điều kiện để kết nối hai bản ghi thường là khi giá trị của một trường chung (ví dụ: `Số thẻ TV`) bằng nhau.
*   Mục đích của một câu truy vấn SQL cụ thể là để tìm mã sách của các cuốn sách mà một học sinh cụ thể (ví dụ: “Trần Văn An”) đã mượn, đồng thời hiển thị thông tin về học sinh đó (Họ và tên, Số thẻ TV) và Mã sách.
*   Từ khóa `DISTINCT` được dùng để quy định rằng nếu kết quả có nhiều dòng giống nhau, chỉ một dòng duy nhất sẽ được đưa vào kết quả.
*   Quan hệ giữa bảng `NGƯỜI ĐỌC` và `MƯỢN-TRẢ` là quan hệ một – nhiều, nghĩa là một bản ghi ở bảng thứ nhất (NGƯỜI ĐỌC) có thể tương ứng với nhiều bản ghi ở bảng thứ hai (MƯỢN-TRẢ), nhưng một bản ghi ở bảng thứ hai chỉ tương ứng với một bản ghi ở bảng thứ nhất.
*   **Chú ý:** Từ khoá `INNER JOIN` được đặt giữa tên hai bảng nguồn cần kết nối, và từ khoá `ON` đứng ngay trước điều kiện kết nối.
## Kết xuất thông tin bằng báo cáo
*   Bạn đã biết có thể truy vấn CSDL Quản lí học tập 11 để có được thông tin về kết quả học tập của học sinh lớp 11 ở một số môn học.
*   Có thể sử dụng công cụ truy vấn để có được dữ liệu trình bày theo một định dạng cụ thể (tham chiếu Hình 4).
### Mô tả chức năng của đoạn mã nguồn
Đoạn mã đầu tiên `FROM bảng1 INNER JOIN bảng2 ON bảng1.TrườngA Ø bảng2.TrườngB` minh họa cấu trúc cơ bản của một phép kết nối trong SQL, cho biết cách hai bảng (`bảng1`, `bảng2`) được kết nối bằng từ khóa `INNER JOIN` dựa trên một điều kiện so sánh (`Ø`) giữa các trường (`TrườngA`, `TrườngB`) của chúng. Đoạn mã truy vấn SQL thứ hai:
Mã này thực hiện việc chọn lọc các bản ghi duy nhất, hiển thị Họ và tên, Số thẻ TV của người đọc và Mã sách. Dữ liệu được lấy từ việc kết nối bảng `NGƯỜI ĐỌC` và bảng `MƯỢN-TRẢ` thông qua từ khóa `INNER JOIN`. Điều kiện kết nối là giá trị Số thẻ TV phải giống nhau giữa hai bảng. Sau đó, kết quả được lọc để chỉ hiển thị các bản ghi mà Họ và tên của người đọc là "Trần Văn An". Mục đích chính là liệt kê các cuốn sách mà "Trần Văn An" đã mượn cùng với thông tin nhận dạng của anh/cô ấy.
*   Báo cáo CSDL là một văn bản trình bày thông tin được kết xuất từ cơ sở dữ liệu, có thể xem trực tiếp trên màn hình hoặc in ra.
*   Dữ liệu được sử dụng để tạo báo cáo được lấy từ một hoặc nhiều bảng và truy vấn trong CSDL.
*   Báo cáo có chức năng trình bày dữ liệu một cách trực quan, làm nổi bật các mục quan trọng và thường tuân theo mẫu quy định.
*   Nhu cầu sử dụng báo cáo trong công tác quản lý là rất lớn.
*   Báo cáo này có được từ CSDL của một trường trung học phổ thông, như đã nêu trong các ví dụ trước.
*   Để hiển thị kết quả học tập của học sinh đối với một số môn học, có thể sử dụng truy vấn CSDL.
*   Tuy nhiên, việc sử dụng hình thức báo cáo để trình bày thông tin kết xuất sẽ đạt hiệu quả cao hơn và phù hợp hơn với nhu cầu của người dùng.
*   Người xem dễ dàng so sánh thực tế mua bán giữa các mặt hàng khi quan sát một báo cáo, vì dữ liệu về mỗi mặt hàng được tổng hợp (tính tổng) theo số lượng đã bán và tổng tiền thu được.
*   Việc sắp xếp các mặt hàng trong báo cáo theo thứ tự giảm dần của tổng tiền thu được rất hữu ích cho người làm kinh doanh.
*   Bên cạnh các công cụ tạo biểu mẫu và tạo truy vấn, các hệ quản trị CSDL quan hệ đều cung cấp công cụ tạo báo cáo tự động.
*   Người phát triển ứng dụng CSDL có thể sử dụng công cụ tạo báo cáo tự động, sau đó chỉnh sửa bố cục và định dạng dữ liệu của báo cáo.
*   Với những ứng dụng CSDL, người phát triển ứng dụng có thể dùng ngôn ngữ lập trình để thiết kế các báo cáo phù hợp với nhu cầu người dùng.
## Thực hành truy vấn trong CSDL quan hệ
*   Trong CSDL Thư viện được tạo bởi hệ quản trị CSDL Access, giáo viên đã chuẩn bị sẵn một số truy vấn.
*   Em hãy mở xem một truy vấn và chạy thử để biết kết quả.
*   Trong các truy vấn được thiết kế sẵn, em hãy cho biết câu truy vấn nào trả lời cho câu hỏi: Các quyển sách “AI-Trí tuệ nhân tạo” đã được những người nào mượn đọc?
*   Hãy cho biết truy vấn đó kết nối những bảng nào của cơ sở dữ liệu và vì sao em biết điều đó?
*   Nếu cần biết tên cuốn sách đã được mượn với ID = 1 trong bảng MƯỢN-TRẢ, em sẽ viết câu truy vấn.
## Các nội dung khác (Có thể thêm vào các bài khác hoặc nhóm lại nếu phù hợp)
### Chú ý về tên trường trong truy vấn SQL
*   **Chú ý:** Khi thực hiện các câu truy vấn, hệ quản trị CSDL sẽ coi tên trường là biến trong chương trình xử lí, do vậy, nếu tên trường có chứa dấu cách thì cần phải dùng các dấu [ ] để đánh dấu bắt đầu và kết thúc tên trường.
### Ví dụ về CSDL và bảng HỌC SINH 11
*   Để dễ theo dõi các ví dụ về câu truy vấn trong mục này, CSDL nói đến ở các ví dụ có bảng HỌC SINH 11 với dữ liệu như ở Hình 2.
### Mô tả chức năng đoạn mã (Ví dụ 1)
**Mô tả chức năng đoạn mã:**
Đoạn mã này là một câu truy vấn SQL đơn giản. Chức năng của nó là chọn ra các thông tin bao gồm mã định danh, họ và tên, điểm môn Toán, và điểm môn Ngữ văn từ bảng `HỌC SINH 11`. Các bản ghi được chọn sẽ chỉ bao gồm những học sinh có điểm môn Ngữ văn lớn hơn hoặc bằng 7.0.
### Ví dụ 1 về truy vấn SQL
*   **Ví dụ 1. Để tìm Mã định danh, Họ và tên, điểm môn Toán và điểm môn Ngữ văn của những học sinh có điểm môn Ngữ văn từ 7.0 trở lên thì cần dùng truy vấn SQL như trong Hình 1b. Kết quả nhận được từ truy vấn đó sẽ như trong Hình 3.**
### Ngôn ngữ truy vấn QBE
*   **3) Ngôn ngữ truy vấn QBE**
*   **Có những hệ quản trị CSDL cho phép truy vấn bằng cách điền vào chỗ trống trong một bảng, như thể hiện một ví dụ về kết quả cần nhận được (nên ngôn ngữ truy vấn này là Query By Example – QBE). Access là một hệ quản trị CSDL cho truy vấn bằng cả SQL và QBE.**
### Ví dụ 2 về truy vấn QBE
*   **Ví dụ 2. Tương ứng với câu truy vấn SQL ở Hình 1b, ta có thể điền vào bảng thiết kế QBE của Access như ở Hình 4 dưới đây:**
### Câu hỏi về truy vấn SQL (Câu 1 & 2)
*   **Câu 1. Hãy viết câu truy vấn SQL để tìm điểm môn Ngữ văn của những học sinh là Đoàn viên trong bảng HỌC SINH 11 (Hình 2). Kết quả của câu truy vấn là gì?**
*   **Câu 2. Hình bên là một câu truy vấn SQL được viết để tìm dữ liệu trong CSDL Thư viện (Hình 2 Bài 3). Theo em, người viết truy vấn đó muốn tìm biết gì?**
### Mô tả code (Ví dụ về bảng SÁCH)
**Mô tả code:**
Đoạn mã này truy xuất các thông tin gồm mã sách, tên sách và số trang từ bảng SÁCH. Dữ liệu được lọc để chỉ lấy những cuốn sách có tác giả là "Nguyễn Nhật Ánh".
# BÀI 7 CÁC LOẠI KIẾN TRÚC CỦA HỆ CƠ SỞ DỮ LIỆU
## Học xong bài này, em sẽ:
* Phân biệt được CSDL tập trung và CSDL phân tán.
* Biết được một số kiến trúc thường gặp của hai loại hệ CSDL tập trung và hệ CSDL phân tán.
* Theo em, CSDL của trường em được đặt trong một máy tính hay trong tất cả các máy tính có sử dụng CSDL đó? CSDL của một ngân hàng được đặt trong một máy tính hay nhiều máy tính?
## ① Cơ sở dữ liệu tập trung và cơ sở dữ liệu phân tán
### a) Cơ sở dữ liệu tập trung
* Một CSDL tập trung được lưu trữ trên một máy tính.
* Việc quản lí, cập nhật được thực hiện tại chính vị trí này.
* Tuỳ trường hợp cụ thể, người dùng có thể truy cập và khai thác thông tin bằng chính máy tính chứa CSDL hay thông qua kết nối mạng (Internet, LAN, WAN,...).
* Vì tất cả dữ liệu được lưu trữ tại một máy tính duy nhất nên việc truy cập và điều phối dữ liệu dễ dàng hơn, đây là một ưu điểm lớn.
* Phần lớn các cơ quan, doanh nghiệp, tổ chức dùng hệ CSDL tập trung.
* Hệ thống quản lí học sinh của trường em là một hệ CSDL tập trung cỡ nhỏ. Hệ thống bán vé tàu hoả của Tổng công ty Đường sắt Việt Nam cũng là một ví dụ về hệ CSDL tập trung.
* Tuy nhiên, hệ CSDL tập trung cũng có những hạn chế.
* Trong quá trình khai thác, nếu CSDL tập trung gặp sự cố thì các chương trình ứng dụng CSDL không thể chạy được.
### b) Cơ sở dữ liệu phân tán
* Theo em, các hệ thống thư điện tử trên Internet có thể sử dụng hệ CSDL tập trung không? Vì sao?
* Một CSDL phân tán là một tập hợp dữ liệu được lưu trữ phân tán trên các máy tính khác nhau của một mạng máy tính (mỗi máy tính như vậy được gọi là một *site* hay một trạm của mạng) cùng với những đặc điểm sau đây:
    * Mỗi trạm có một CSDL được gọi là CSDL cục bộ của trạm này. Mỗi trạm thực hiện ít nhất một ứng dụng cục bộ, tức là chỉ sử dụng CSDL cục bộ để cho ra kết quả. Khả năng thực hiện ứng dụng cục bộ được gọi là xử lí độc lập.
    * Mỗi trạm phải tham gia thực hiện ít nhất một ứng dụng toàn cục. Ứng dụng toàn cục là ứng dụng chạy tại một trạm và phải sử dụng CSDL của ít nhất hai trạm.
* **Cơ sở dữ liệu phân tán:** tập hợp dữ liệu được phân tán trên các máy tính khác nhau của một mạng máy tính. Mỗi nơi (site) của mạng máy tính có khả năng xử lí độc lập và thực hiện các ứng dụng cục bộ. Mỗi nơi cũng tham gia thực hiện ít nhất một ứng dụng toàn cục, yêu cầu truy xuất dữ liệu tại nhiều nơi bằng cách dùng hệ thống truyền thông con.
* **Ví dụ 1.** Một ngân hàng có nhiều chi nhánh, ở mỗi thành phố có một chi nhánh, ở mỗi chi nhánh có dữ liệu quản lí các tài khoản của dân cư và đơn vị đăng kí kinh doanh tại thành phố đó. Thông qua mạng truyền thông, tập hợp dữ liệu của ngân hàng này tại các chi nhánh tạo thành một hệ CSDL phân tán. Người chủ của một tài khoản có thể thực hiện các giao dịch (chẳng hạn rút một khoản tiền trong tài khoản) ở một chi nhánh nào đó (ví dụ ở Hà Nội), nhưng cũng có thể thực hiện giao dịch ở một chi nhánh đặt tại một thành phố khác (ví dụ ở Đà Nẵng).
* **Ví dụ 2.** Hệ thống tìm kiếm Google có hệ CSDL phân tán. Mối yêu cầu có thể được thực hiện bởi hàng trăm máy tính thu thập dữ liệu web và trả về các kết quả có liên quan.
* Đối với người dùng, Google là một hệ thống gồm nhiều máy tính làm việc cùng nhau và truy xuất dữ liệu tại nhiều trạm để hoàn thành một nhiệm vụ duy nhất (trả lại kết quả cho truy vấn tìm kiếm).
* **So với hệ CSDL tập trung, hệ CSDL phân tán có một số ưu điểm chính:**
    * Sự phân tán dữ liệu về mặt vật lí phù hợp với các tổ chức, doanh nghiệp lớn hoạt động trải rộng về mặt địa lí, phù hợp với các dịch vụ phổ rộng trên toàn cầu, ví dụ như: các hệ thống dịch vụ dựa trên web, hệ thống thương mại điện tử.
    * Tính sẵn sàng và tính tin cậy của dữ liệu cao hơn. Tính sẵn sàng phục vụ cao là do những dữ liệu được đơn vị nào sử dụng nhiều nhất sẽ được lưu trữ và quản lí tại đơn vị đó. Khi có sự cố không truy cập được dữ liệu tại một trạm thì vẫn có thể khai thác bản sao của dữ liệu đặt tại một trạm khác. Về tính tin cậy, khi một trạm gặp sự cố, có thể khôi phục được dữ liệu do có bản sao của nó được lưu trữ và vận hành tại một hay vài trạm khác nữa.
    * Mở rộng các tổ chức một cách linh hoạt, có thể thêm trạm mới vào mạng máy tính mà không ảnh hưởng đến hoạt động của các trạm sẵn có.
* **Tuy nhiên, hệ CSDL phân tán có một số hạn chế so với hệ CSDL tập trung:**
    * Chi phí cao hơn do hệ thống phức tạp hơn, hệ thống phải làm ẩn đi sự phân tán dữ liệu đối với người dùng.
    * Khó khăn hơn trong đảm bảo tính nhất quán dữ liệu và tính an ninh, đồng thời rất khó cung cấp một cái nhìn thống nhất cho người dùng vì dữ liệu đặt tại nhiều địa điểm khác nhau.
## Các loại kiến trúc của các hệ cơ sở dữ liệu
* Mỗi hệ CSDL bao gồm 3 lớp: Lớp CSDL, Lớp hệ quản trị CSDL, Lớp các ứng dụng CSDL.
* Kiến trúc của một hệ CSDL là cách phân chia hệ thống thành các thành phần chức năng để có thể hiểu, chỉnh sửa, thay thế mỗi thành phần một cách độc lập.
* Giới thiệu sơ lược một số kiến trúc phổ biến của hai loại hệ CSDL tập trung và hệ CSDL phân tán.
### a) Kiến trúc phổ biến của hệ CSDL tập trung
* Các hệ CSDL tập trung thường theo kiến trúc khách – chủ (Client – Server).
* Các thành phần của hệ quản trị CSDL gồm thành phần yêu cầu tài nguyên (dữ liệu).
* Thành phần cung cấp tài nguyên (dữ liệu) không nhất thiết phải cài đặt trên cùng một máy tính.
* Thành phần cung cấp tài nguyên thường đặt tại một máy chủ (server).
* Thành phần yêu cầu tài nguyên có thể cài đặt tại nhiều máy khác trên mạng, ta gọi là máy khách (client).
* **Kiến trúc 1 tầng (1-Tier Architecture):** Là kiến trúc đơn giản nhất, toàn bộ CSDL được lưu trữ tại một máy tính và cũng chỉ được khai thác tại máy tính này. Máy tính như vậy vừa là máy chủ CSDL vừa là máy khách duy nhất khai thác CSDL. Tuy nhiên, kiến trúc đơn giản này không phù hợp cho các ứng dụng phức tạp.
* **Kiến trúc 2 tầng (2-Tier Architecture):** Là kiến trúc có CSDL được lưu trữ ở một máy chủ trên mạng (được xem là tầng 2), thành phần trình bày dữ liệu cho người khai thác được cài đặt trên máy khách kết nối được với mạng (được xem là tầng 1). Máy khách có thể là PC, máy tính bảng hay điện thoại di động. Tuy nhiên, hiệu suất hoạt động của hệ thống này sẽ kém trong trường hợp có nhiều máy khách cùng khai thác CSDL.
* **Kiến trúc 3 tầng (3-Tier Architecture):** Là kiến trúc mở rộng của kiến trúc 2 tầng. Tầng 1 vẫn là thành phần trình bày dữ liệu. Tầng 3 là máy chủ chứa CSDL. Tầng 2 nằm giữa gọi là tầng ứng dụng, hoạt động như một phương tiện để trao đổi dữ liệu đã được xử lí một phần giữa máy chủ và máy khách. Tầng trung gian này chứa các chương trình ứng dụng thường xử lí các vấn đề nghiệp vụ trước khi chuyển dữ liệu qua lại giữa tầng 1 và tầng 3. Loại kiến trúc này thường được sử dụng trong trường hợp các ứng dụng web lớn.
### Các kiến trúc phổ biến của hệ CSDL phân tán:
Hệ CSDL phân tán có một số mô hình kiến trúc phổ biến: mô hình ngang hàng (peer to peer), mô hình khách – chủ cho hệ CSDL phân tán.
* **Kiến trúc ngang hàng cho hệ CSDL phân tán:** Có mỗi máy tính hoạt động như một máy khách và máy chủ để truyền tải các dịch vụ CSDL. Các máy tính ngang hàng với nhau trong khả năng chia sẻ nguồn tài nguyên dữ liệu của nó với các máy khác và cùng ngang hàng trong khả năng điều phối các hoạt động.
* Kiến trúc khách – chủ cho hệ CSDL cũng là kiến trúc khách – chủ như đã biết, nhưng khác với ở hệ CSDL tập trung, hệ CSDL phân tán có nhiều máy chủ CSDL.
## Câu hỏi và bài tập
* Hãy nêu đặc điểm quan trọng nhất để phân biệt một hệ CSDL tập trung với một hệ CSDL phân tán.
* Dựa vào quy mô và đặc điểm tổ chức của mình mà các doanh nghiệp lựa chọn xây dựng cho mình loại hệ CSDL (tập trung hay phân tán) và mô hình kiến trúc phù hợp. Em hãy giải thích và lấy vài ví dụ để minh họa.
* Trong các câu sau đây, những câu nào đúng?
    * a) CSDL luôn chỉ được lưu trữ và khai thác tại một máy tính.
    * b) Trong hệ CSDL tập trung, việc quản lí và cập nhật dữ liệu dễ dàng hơn so với hệ CSDL phân tán.
    * c) Trong tất cả các hệ CSDL, hễ có sự cố không truy cập được một máy chủ CSDL thì toàn bộ hệ thống CSDL đó ngừng hoạt động.
## **Trong các câu sau, những câu nào đúng?**
* Chỉ có thể viết câu truy vấn SQL trên một bảng của CSDL.
* Các từ khoá kết nối phải viết trong mệnh đề FROM của câu truy vấn SQL.
* Chỉ có thể kết nối với điều kiện giá trị ở trường chung giữa hai bảng là bằng nhau.
* Dữ liệu để đưa vào báo cáo được lấy từ một hay nhiều bảng và truy vấn.
## **Tóm tắt bài học**
* Để trích rút dữ liệu trong một CSDL quan hệ, có những truy vấn phải thực hiện kết nối dữ liệu của các bảng.
* Mệnh đề FROM có thể chứa từ khoá chỉ định kiểu JOIN để thực hiện kết nối các bản ghi ở các bảng khác nhau. INNER JOIN là một kiểu kết nối phổ biến.
* Các hệ quản trị CSDL đều cung cấp công cụ tạo báo cáo tự động và người dùng cũng có thể điều chỉnh bố cục, định dạng báo cáo để nâng cao chất lượng trình bày thông tin.
# BÀI 7: CƠ SỞ DỮ LIỆU PHÂN TÁN
*   d) Một hệ CSDL phân tán đắt hơn so với một hệ CSDL tập trung vì nó phức tạp hơn nhiều.
*   **Tóm tắt bài học**
    *   Điểm khác biệt quan trọng giữa CSDL tập trung và CSDL phân tán là: CSDL tập trung có toàn bộ dữ liệu được lưu trữ trên một máy tính, trong khi đó CSDL phân tán có dữ liệu phân tán trên các máy tính khác nhau của một mạng máy tính và mỗi máy tính khai thác CSDL đều tham gia ít nhất một ứng dụng toàn cục.
    *   Kiến trúc khách – chủ là kiến trúc phổ biến của các hệ CSDL tập trung, tuỳ theo ứng dụng mà có kiến trúc theo mô hình 1 tầng, 2 tầng hay nhiều tầng hơn.
    *   Có vài loại mô hình kiến trúc phổ biến của các hệ CSDL phân tán: khách – chủ (cho CSDL phân tán), ngang hàng,...
# BÀI 8: BẢO VỆ SỰ AN TOÀN CỦA HỆ CSDL VÀ BẢO MẬT THÔNG TIN TRONG CSDL
*   **Học xong bài này, em sẽ:**
    *   Nêu được tầm quan trọng của an toàn và bảo mật hệ CSDL.
    *   Nêu được một số biện pháp bảo vệ sự an toàn và bảo mật hệ CSDL.
    *   Hệ CSDL của một tổ chức thường có nhiều người dùng truy cập, do vậy có những nguy cơ đe dọa sự an toàn của hệ CSDL. Em hãy cho một vài ví dụ về những nguy cơ đó và hậu quả có thể xảy ra.
*   **Tầm quan trọng của việc bảo vệ sự an toàn của hệ CSDL và bảo mật thông tin trong CSDL**
    ## Bảo vệ sự an toàn của hệ CSDL và tầm quan trọng của an toàn hệ CSDL
        *   Bảo vệ sự an toàn hệ CSDL là bảo vệ hệ CSDL khỏi các mối đe dọa cố ý hoặc vô tình.
        *   Nguy cơ phá vỡ sự an toàn của hệ CSDL có thể đến từ những sự cố, tai hoạ ngẫu nhiên. Ví dụ, do thao tác vô tình hoặc do lỗi bất chợt ở phần cứng làm hỏng các ổ đĩa lưu trữ dữ liệu hay sự cố cháy nổ,...
        *   Sự cố tình phá hoại hoạt động của hệ CSDL, sử dụng hệ CSDL một cách bất hợp pháp hay đánh cắp dữ liệu cũng là nguy cơ làm mất đi sự an toàn của hệ CSDL.
        *   Bảo vệ sự an toàn của hệ CSDL là rất quan trọng đối với bất cứ tổ chức nào vì bất kì một hỏng hóc hay mất mát nào cũng sẽ ảnh hưởng đến hoạt động hằng ngày của tổ chức và hiệu suất làm việc của mọi người.
    ## Bảo mật thông tin trong CSDL và tầm quan trọng của bảo mật thông tin
        *   Một CSDL có thể có những dữ liệu cần được bảo mật. Điều này có nghĩa là cần kiểm soát được việc xem dữ liệu, mỗi cá nhân chỉ được phép xem dữ liệu mà họ được quyền xem.
        *   Bảo mật được thông tin trong CSDL là bảo vệ được tính bí mật của những thông tin có tính riêng tư của cá nhân hay tổ chức.
        *   Ví dụ, để lộ những thông tin cá nhân bí mật như hồ sơ sức khoẻ, số tài khoản cũng như mật khẩu thẻ tín dụng là vi phạm tính bảo mật thông tin.
        *   Những thông tin như bí mật thương mại, phân tích cạnh tranh, kế hoạch tiếp thị và bán hàng cũng là những ví dụ về thông tin cần bảo mật của một công ty thương mại, không phải ai trong công ty đó cũng được quyền biết.
        *   Bảo mật thông tin trong CSDL cũng rất quan trọng. Các tổ chức không thực hiện được bảo mật thông tin sẽ phải gánh chịu nhiều hậu quả khó giải quyết hoặc tổn thất.
*   Một ví dụ khác, nếu thông tin bí mật của khách hàng bị lộ, đơn vị kinh doanh chủ quản hệ CSDL lưu trữ thông tin đó có thể phải đối mặt với pháp luật, bồi thường cho khách hàng, mất uy tín trong kinh doanh.
*   Bảo vệ tính an toàn của hệ CSDL và bảo mật thông tin trong CSDL là vô cùng cần thiết. Đó không chỉ là bảo vệ dữ liệu bên trong CSDL, bảo vệ tính bí mật của thông tin, mà còn gồm cả bảo vệ hệ quản trị CSDL và tất cả các ứng dụng CSDL sao cho không có truy cập sử dụng dữ liệu sai mục đích và làm hư hỏng dữ liệu.
*   **2. Một số biện pháp bảo vệ sự an toàn của hệ CSDL và bảo mật thông tin trong CSDL**
    *   Theo em, sự an toàn của hệ CSDL và bảo mật thông tin trong CSDL có liên quan đến nhau không? Em hãy giải thích ý kiến của mình về điều đó.
    ## a) Bảo vệ sự an toàn của hệ CSDL
        *   Có nhiều biện pháp và cách thức khác nhau mà các tổ chức, doanh nghiệp thực hiện để hệ CSDL của họ được an toàn. Dưới đây là một số biện pháp thường được sử dụng.
        *   *Xác thực người truy cập:* Hai loại xác thực thường được thực hiện đồng thời là xác thực bằng thẻ vào cửa và xác thực bằng kiểm tra quyền truy cập tài khoản. Hệ thống bảo vệ (người bảo vệ và camera an ninh) được các tổ chức thiết lập nhằm ngăn chặn người xâm nhập trái phép các thành phần vật lí của hệ thống như: khu vực, toà nhà, phòng chứa máy chủ. Đồng thời với điều đó, các hình thức thẻ vào cửa (thẻ nhân viên và mã truy cập vào cửa,...) là một biện pháp không thể bỏ qua. Để kiểm tra quyền truy cập tài khoản, xác thực qua mật khẩu là biện pháp phổ biến. Nhiều hệ thống sử dụng thêm các hình thức xác thực khác nữa như: chữ kí điện tử, nhận dạng vân tay, nhận dạng giọng nói, nhận dạng khuôn mặt,... Cơ chế xác thực mạnh sẽ bảo vệ quyền truy cập hiệu quả hơn.
        *   *Sử dụng tường lửa:* Sử dụng một kĩ thuật được cài vào hệ thống mạng để thiết lập một rào cản giữa một mạng nội bộ đáng tin cậy và mạng bên ngoài không tin cậy.
        *   *Sao lưu dự phòng và duy trì biên bản hệ thống:* Tạo các bản sao lưu của CSDL và các tệp biên bản (nhật kí) theo định kì, đồng thời đảm bảo rằng các bản sao ở một vị trí an toàn. Trong trường hợp xảy ra lỗi khiến CSDL không thể sử dụng được, bản sao lưu và các chi tiết được ghi lại trong tệp nhật kí được sử dụng để khôi phục CSDL về trạng thái nhất quán mới nhất có thể.
    ## b) Bảo mật thông tin trong CSDL
        *   Nhiều trường hợp cố tình truy cập trái phép, tấn công vào hệ CSDL là để nhằm lấy cắp dữ liệu, đặc biệt là dữ liệu bí mật. Bởi vậy, tất cả các biện pháp nhằm bảo vệ sự an toàn của hệ thống CSDL cũng có vai trò thiết yếu để tăng cường bảo mật thông tin trong CSDL.
*   Mã hóa dữ liệu là biện pháp bảo mật dữ liệu trong CSDL, là lớp bảo vệ trong trường hợp các biện pháp kiểm soát truy cập đã bị vượt qua.
*   Mã hóa dữ liệu là quá trình chuyển đổi dữ liệu sang một định dạng khác gọi là bản mã.
*   Chỉ những người dùng được ủy quyền có khóa giải mã mới có thể truy cập được thông tin đó.
*   Mục tiêu của mã hóa dữ liệu là để bảo vệ tính bí mật của dữ liệu kĩ thuật số trong quá trình lưu trữ hoặc trong quá trình truyền trên mạng.
*   Nén dữ liệu cũng góp phần tăng cường tính bảo mật dữ liệu ngoài mục đích giảm dung lượng lưu trữ.
*   Khi có dữ liệu dạng nén, cần biết quy tắc nén, giải nén mới có dữ liệu gốc được.
*   Việc áp dụng các biện pháp an toàn và bảo mật hệ CSDL có ý nghĩa rất quan trọng nhằm bảo vệ hệ CSDL.
*   Em hãy nêu một trường hợp cụ thể về hệ CSDL không được an toàn hoặc lộ bí mật thông tin. Với trường hợp đó, cần áp dụng biện pháp nào để tăng cường khả năng bảo vệ sự an toàn của hệ CSDL và bảo mật thông tin trong CSDL.
*   Em hãy tìm hiểu các giải pháp đảm bảo an toàn cho hệ CSDL của trường em và đề xuất bổ sung giải pháp cụ thể để nâng cao tính an toàn cho hệ thống đó.
*   Câu 1. Vì sao cần đảm bảo sự an toàn của hệ CSDL và bảo mật thông tin trong CSDL?
*   Câu 2. Hãy nêu một vài biện pháp thông dụng bảo vệ sự an toàn cho hệ CSDL và giải thích mục đích của việc mã hóa dữ liệu.
**Tóm tắt bài học**
*   Cần thiết phải bảo vệ hệ CSDL và bảo mật thông tin trong CSDL khỏi những mối đe dọa: phá hoại hoạt động của hệ thống, thay đổi dữ liệu, lấy cắp dữ liệu, làm lộ bí mật thông tin.
*   Một số biện pháp bảo vệ sự an toàn của hệ CSDL được dùng rất phổ biến là: xác thực người truy cập kiểm soát các truy cập, sử dụng tường lửa, sao lưu dự phòng và duy trì biên bản hệ thống.
*   Mã hoá và nén dữ liệu là những biện pháp thường dùng để bảo mật thông tin trong CSDL, ngoài ra các biện pháp bảo vệ sự an toàn của hệ CSDL cũng giúp ngăn chặn nguy cơ xâm nhập lấy cắp thông tin bí mật.
# HƯỚNG NGHIỆP VỚI TIN HỌC
# GIỚI THIỆU NGHỀ QUẢN TRỊ CƠ SỞ DỮ LIỆU
# NGHỀ QUẢN TRỊ CƠ SỞ DỮ LIỆU
**Học xong bài này, em sẽ:**
*   Biết được một số thông tin cơ bản về nghề quản trị CSDL: các công việc chính; yêu cầu về kiến thức, kĩ năng; các ngành học có liên quan ở các bậc học tiếp theo; nhu cầu nhân lực hiện tại và tương lai.
*   Tự tìm kiếm và khai thác được thông tin hướng nghiệp (qua các chương trình đào tạo, thông báo tuyển dụng nhân lực,...) về một vài ngành nghề liên quan khác trong lĩnh vực tin học.
*   Giao lưu được với bạn bè qua các kênh truyền thông số để tham khảo và trao đổi ý kiến về những thông tin trên.
**Thảo luận:**
*   Em đã được giới thiệu về hệ quản trị CSDL, đã thực hành tạo lập CSDL và khai thác thông tin trong CSDL cho một bài toán quản lí nhỏ. Hãy thảo luận nhóm và trả lời các câu hỏi sau:
    1. Quản trị CSDL là gì và nhằm mục đích gì?
    2. Em có muốn trở thành nhà quản trị CSDL hay không?
## 1 Công việc chính của nhà quản trị CSDL
*   Quản trị CSDL là để đảm bảo việc khai thác thông tin trong CSDL phục vụ mọi hoạt động thường ngày của tổ chức, doanh nghiệp và chuẩn bị để ứng phó tốt nhất với các sự cố có thể xảy ra đối với CSDL.
# Quản trị Cơ Sở Dữ Liệu (CSDL)
## Người làm việc quản trị CSDL (Database Administrator)
Người làm việc quản trị CSDL (Database Administrator) gọi là nhà quản trị CSDL và có các nhiệm vụ chính sau đây:
### a) Đảm bảo an toàn dữ liệu và xác thực quyền truy cập
*   Nhà quản trị CSDL cần kiểm soát và đảm bảo tính toàn vẹn an toàn cho dữ liệu.
*   Cụ thể, nhà quản trị CSDL thực hiện cấp quyền và kiểm soát truy cập CSDL cho các đối tượng người dùng, đồng thời phát triển các biện pháp bảo mật CSDL và đảm bảo dữ liệu đến từ các nguồn đáng tin cậy.
*   Đặc biệt, vấn đề bảo mật dữ liệu càng cần được coi trọng đối với các hệ thống trực tuyến, doanh nghiệp thương mại điện tử, các công ty và tổ chức có lưu giữ thông tin cá nhân và tài chính của khách hàng.
### b) Giám sát hiệu suất và điều chỉnh CSDL
*   Giám sát hiệu suất CSDL là một phần của quá trình bảo trì hệ thống do nhà quản trị CSDL thực hiện.
*   Nhà quản trị CSDL cần xác định nguyên nhân làm giảm hiệu suất xử lí của hệ thống để khắc phục, ví dụ: thay đổi các thông số thiết lập trong phần mềm, thay phần cứng có cấu hình mạnh hơn hoặc điều chỉnh các tham số CSDL.
*   Các tham số CSDL ví dụ: số lượng dữ liệu tối đa, số lượng khoá tối đa.
### c) Lập kế hoạch phát triển CSDL
*   Nhà quản trị cần cập nhật định kì nhu cầu mới về khai thác dữ liệu của CSDL để đề xuất mở rộng, nâng cấp các khả năng đáp ứng của CSDL.
*   Nhà quản trị CSDL cần thường xuyên cập nhật xu thế phát triển CSDL để có những dự báo tương lai về: không gian lưu trữ của CSDL, công suất sử dụng CSDL.
*   Từ đó, nhà quản trị CSDL sẽ phải chuẩn bị tăng khả năng xử lí khối lượng công việc khi cần.
### d) Sao lưu, phục hồi và khắc phục sự cố
*   Nhà quản trị CSDL cần có khả năng phán đoán sự cố, nhanh chóng khắc phục các sự cố, khôi phục dữ liệu để giảm thiểu thiệt hại cho tổ chức, đưa các hoạt động với CSDL sớm trở lại bình thường.
*   Nhà quản trị CSDL có trách nhiệm thực hiện sao lưu hệ thống thường xuyên để không có dữ liệu nào bị mất khi ngắt điện đột ngột hoặc các loại thảm họa khác.
### e) Cài đặt và bảo trì phần mềm CSDL
*   Nhà quản trị CSDL cài đặt phần mềm CSDL, thực hiện bảo trì, cập nhật và vá lỗi.
*   Điều này góp phần quan trọng đảm bảo tính toàn vẹn dữ liệu của tổ chức.
### Yêu cầu của nghề quản trị CSDL
*   Để trở thành nhà quản trị CSDL, có thể học các chuyên ngành về quản trị CSDL, khoa học máy tính, hệ thống thông tin quản lí hoặc một chuyên ngành về công nghệ thông tin.
*   Ngoài ra, tùy thuộc vào quy mô của tổ chức và mức độ phức tạp của công việc, nhà quản trị CSDL có thể cần thêm các chứng chỉ của nhà cung cấp phần mềm hệ quản trị CSDL và kinh nghiệm làm việc.
*   Các kĩ năng cụ thể để quản trị CSDL thường khác nhau tùy theo tổ chức, vị trí công việc và dự án. Tuy nhiên, nhà quản trị CSDL cần có những kiến thức và kĩ năng cơ bản sau:
    *   Kiến thức vững chắc về CSDL, ngôn ngữ truy vấn CSDL.
    *   Nhà quản trị CSDL nên nắm được một số ngôn ngữ truy vấn CSDL phổ biến như: SQL, Oracle SQL và DB2 của IBM.
*   Kiến thức về hệ điều hành (các hệ điều hành thông dụng như: Unix, Linux, Windows), phần cứng và mạng.
*   Hiểu biết về các ứng dụng liên quan đến CSDL mà mình quản trị.
*   Kĩ năng phân tích dữ liệu: Nhà quản trị CSDL phân tích các tập dữ liệu, trích xuất ra thông tin hữu ích cho tổ chức và khách hàng, đồng thời cung cấp thông tin chi tiết về các cải tiến hệ thống, ra quyết định.
*   Kĩ năng giao tiếp: Nhà quản trị CSDL thường phải giám sát và làm việc nhóm với các nhân viên công nghệ thông tin. Ngoài ra họ cũng giao tiếp với người quản lí điều hành, nhà cung cấp và các chuyên gia công nghệ tại các tổ chức khác.
*   Kĩ năng giải quyết vấn đề: Năng lực xác định, kiểm tra và phát hiện các vấn đề tiềm ẩn, nguyên nhân và giải pháp khắc phục các sự cố là rất có giá trị đối với nhà quản trị CSDL. Nhà quản trị CSDL cũng cần sáng tạo trong việc đưa ra giải pháp cho các vấn đề mới.
*   Kĩ năng tổ chức: Tổ chức dữ liệu để đưa ra các quyết định về CSDL. Nhà quản trị CSDL cũng tổ chức các nhiệm vụ cho nhân viên của bộ phận công nghệ thông tin.
*   Cẩn trọng và tỉ mỉ: Vì phải làm việc với khối lượng dữ liệu lớn, nên sai sót nhỏ cũng có thể dẫn đến những lỗi nghiêm trọng. Điều đó đòi hỏi nhà quản trị CSDL phải làm việc cẩn trọng, tỉ mỉ.
## 3 Nhu cầu nhân lực và triển vọng phát triển
*   Hiện nay, ở Việt Nam có rất nhiều trường đại học đào tạo cử nhân hoặc kĩ sư công nghệ thông tin.
*   Các trường đại học có uy tín về đào tạo công nghệ thông tin như: Trường Đại học Bách Khoa Hà Nội, Trường Đại học Bách Khoa – Đại học Quốc gia Thành phố Hồ Chí Minh, Trường Đại học Công nghệ – Đại học Quốc gia Hà Nội, Trường Đại học Khoa học tự nhiên – Đại học Quốc gia Hà Nội, Trường Đại học Công nghệ thông tin – Đại học Quốc gia Thành phố Hồ Chí Minh,...
*   Các chương trình đào tạo công nghệ thông tin trong các trường đại học ở Việt Nam đều trang bị cho sinh viên cơ sở lí thuyết về hệ CSDL, thực hành với hệ quản trị cơ sở dữ liệu, an toàn hệ thống thông tin, lập trình web và phần mềm ứng dụng.
*   Ngoài ra, sinh viên có thể học thêm các khoá học về các hệ CSDL hoặc về các phần mềm cụ thể của Microsoft, IBM, Oracle, Altibase,...
*   Cơ hội việc làm và mức lương cũng khác nhau đáng kể theo vị trí công việc, quy mô và địa điểm của tổ chức.
*   Dữ liệu của Cục Thống kê Lao động Hoa Kỳ (BLS) năm 2018 cho thấy rằng các nhà quản trị CSDL có mức lương trung bình hàng năm là 90 070 USD.
*   BLS dự đoán rằng các công việc quản trị CSDL sẽ tăng 9% từ năm 2018 đến năm 2028, các vị trí phân tích thông tin y tế dự kiến sẽ tăng 13% vào năm 2026 (www.bls.gov/ooh/healthcare).
*   Các vị trí nhà quản trị CSDL, chuyên gia phân tích thông tin sức khoẻ được tuyển dụng trong nhiều tổ chức như: bệnh viện, các cơ sở y tế, các tổ chức khác.
*   Chức năng quản trị cơ sở dữ liệu (CSDL) là cần thiết trong nhiều ngành nghề và lĩnh vực khác nhau như chăm sóc sức khỏe, bảo hiểm, công ty dược phẩm, công ty sản xuất thiết bị y tế, giáo dục, viễn thông, ngân hàng, xuất bản và phát triển phần mềm.
*   Nhiều công việc khác cũng cần đến kỹ năng quản trị CSDL bao gồm tư vấn công nghệ thông tin, quản lý dự án công nghệ thông tin, tư vấn ứng dụng và quản trị mạng.
*   Tại Việt Nam, nhu cầu nhân lực ngành công nghệ thông tin được dự báo sẽ tiếp tục tăng cao trong những năm tới do sự phát triển của thương mại điện tử, chính phủ điện tử, kinh tế số và xã hội số.
*   Vị trí nhà quản trị CSDL ngày càng trở nên quan trọng, cần thiết cho các tổ chức chính quyền và các cơ quan doanh nghiệp.
*   Nhà quản trị CSDL có thể theo đuổi con đường học vấn cao hơn (thạc sĩ, tiến sĩ về công nghệ thông tin) hoặc thông qua các chứng chỉ chuyên môn thuộc lĩnh vực CSDL, hoặc mở rộng sang các lĩnh vực liên quan như an ninh mạng.
## Thực hành tìm hiểu một số ngành nghề liên quan
### Yêu cầu:
Học sinh được chia thành các nhóm, mỗi nhóm lựa chọn tìm hiểu một trong các ngành nghề như nhà phân tích CSDL, kiến trúc sư CSDL, nhà quản trị dữ liệu. Sau đó, mỗi nhóm phải mô tả nghề nghiệp tìm hiểu được bằng một tệp văn bản và giới thiệu nghề nghiệp đó bằng một tệp trình chiếu.
### Hướng dẫn thực hiện:
*   Bước 1: Phân công nhiệm vụ cho các thành viên trong nhóm.
*   Bước 2: Tìm kiếm thông tin về ngành nghề lựa chọn (qua Internet, phỏng vấn và giao lưu với khách mời qua mạng xã hội, email,...), tổng hợp thông tin.
*   Bước 3: Trao đổi, thảo luận trong nhóm về các nội dung tìm hiểu được.
*   Bước 4: Soạn nội dung báo cáo (tệp văn bản và trình chiếu).
#### Gợi ý chuẩn bị tệp văn bản:
##### Về nội dung, nên gồm những phần chính sau:
1. Giới thiệu về nghề
2. Kiến thức, kĩ năng cần thiết cho nghề
3. Đặc điểm lao động và yêu cầu của nghề (sản phẩm chính là gì?)
4. Đào tạo và tuyển sinh
5. Tình hình tuyển dụng, môi trường làm việc, thu nhập và phúc lợi xã hội
##### Về hình thức, cần định dạng văn bản và trình bày khoa học.
#### Gợi ý chuẩn bị tệp trình chiếu:
*   **Về nội dung:** Tùy vào thời lượng trình bày (do giáo viên quy định) để chọn lọc các nội dung (trong tệp văn bản) đưa vào bài trình chiếu. Có thể đưa thêm các hình ảnh, video minh hoạ cho các phần nội dung để bài trình bày sinh động hơn.
*   **Về hình thức:** Thiết kế, định dạng bài trình bày và lựa chọn hiệu ứng phù hợp.
*   **Bước 5. Trình bày báo cáo.**
## Bài tập
### Bài 1.
Nếu thầy, cô giáo môn Tin học ở trường em được giao quản lí điểm của học sinh trong trường. Theo em, có thể gọi thầy, cô giáo môn Tin học này là nhà quản trị CSDL được không? Vì sao?
### Bài 2.
Nếu muốn trở thành nhà quản trị CSDL thì em sẽ chuẩn bị những gì?
### Trong các câu sau, những câu nào đúng?
*   a) Công việc của nhà quản trị CSDL là đảm bảo CSDL luôn sẵn sàng trong trạng thái tốt nhất và được bảo mật.
*   b) Nhà quản trị CSDL chỉ cần cho các doanh nghiệp lớn.
*   c) Nhà quản trị CSDL nên có hiểu biết về các ứng dụng liên quan đến CSDL mà mình quản trị.
# Chủ đề D: TỔ CHỨC VÀ QUẢN LÍ DỮ LIỆU
## Bài 3: HỆ QUẢN TRỊ CƠ SỞ DỮ LIỆU
### 4.  NHÀ QUẢN TRỊ CƠ SỞ DỮ LIỆU
*   d) Nhà quản trị CSDL cần thành thạo các ngôn ngữ lập trình thông dụng hiện nay.
*   e) Nhà quản trị CSDL có hiểu biết sâu về tất cả các ứng dụng liên quan đến CSDL.
*   g) Nhà quản trị CSDL cần sử dụng thành thạo ngôn ngữ truy vấn CSDL như SQL.
*   h) Nhà quản trị CSDL cần có kĩ năng phân tích và giải quyết vấn đề.
*   **Tóm tắt bài học**
    *   Nhà quản trị CSDL có vai trò rất quan trọng trong các tổ chức, doanh nghiệp vì họ chịu trách nhiệm duy trì và quản lí CSDL của tổ chức, đảm bảo sự vận hành thông suốt của hệ thống. Nhu cầu nhân lực cho ngành nghề này rất lớn, đặc biệt là trong các tổ chức sử dụng lượng dữ liệu lớn như: bảo hiểm, tài chính, y tế, thương mại điện tử, giáo dục.
# Chủ đề E: ỨNG DỤNG TIN HỌC - PHẦN MỀM CHỈNH SỬA ẢNH VÀ LÀM VIDEO
## Bài 1: MỘT SỐ THAO TÁC CHỈNH SỬA ẢNH VÀ HỖ TRỢ CHỈNH SỬA ẢNH
### Học xong bài này, em sẽ:
*   Thực hiện được các thao tác: thu nhỏ, phóng to và di chuyển ảnh.
*   Thực hiện được một số thao tác chỉnh sửa ảnh: cắt ảnh, hiệu chỉnh màu sắc cho ảnh và biến đổi ảnh đơn giản (thay đổi kích thước, xoay, lật, làm nghiêng).
*   Hãy cho biết tương ứng với mỗi nhu cầu sau đây, cần thực hiện thao tác nào:
    *   1) Muốn nhìn bao quát toàn bộ ảnh trong khi màn hình không hiển thị hết bức ảnh.
    *   2) Muốn nhìn gần và rõ một chi tiết trong ảnh để xử lí.
    *   3) Muốn quan sát rõ hai vùng ảnh đã được phóng to và ở vị trí xa nhau, không nhìn thấy cả hai cùng một lúc.
### 1. Thu nhỏ, phóng to và di chuyển ảnh
*   Hãy mở một tệp ảnh trong GIMP, sau đó quan sát bằng công cụ và các thành phần xung quanh cửa sổ ảnh. Từ đó, hãy dự đoán xem những công cụ nào giúp thu nhỏ, phóng to và di chuyển ảnh.
*   Quá trình quan sát, thiết kế, chỉnh sửa ảnh thường cần đến các thao tác hỗ trợ như: thu nhỏ, phóng to và di chuyển ảnh.
*   Ví dụ, xét tình huống cần đổi màu quần của nhân vật chuột Mickey trong ảnh. Trước hết, sử dụng công cụ Free Select (chọn tự do) để tạo một vùng chọn xung quanh chiếc quần. Trong quá trình chọn, cần phóng to và di chuyển ảnh sao cho quan sát rõ chỗ tiếp giáp giữa quần với cánh nền để xác định chính xác đường biên của vùng chọn. Khi chọn xong, thu nhỏ ảnh như ban đầu để nhìn được toàn bộ vùng chọn.
### a) Thu nhỏ, phóng to ảnh
*   Có ba cách thu nhỏ, phóng to ảnh:
    *   Cách 1: Giữ phím Ctrl rồi lăn nút cuộn chuột theo chiều tiến hoặc lùi.
    *   Cách 2: Gõ trực tiếp giá trị vào ô tỉ lệ thu/phóng ở góc dưới bên trái thanh trạng thái, ví dụ 50%.
    *   Cách 3: Sử dụng công cụ Zoom (thu/phóng).
        *   Bước 1. Nháy chuột vào công cụ Zoom (thu/phóng).
        *   Bước 2. Đưa chuột vào cửa sổ ảnh và nháy chuột để phóng to ảnh hoặc giữ phím Ctrl khi nháy chuột để thu nhỏ ảnh.
### b) Di chuyển ảnh
*   Để di chuyển đồng thời cả ảnh và khung ảnh (canvas), thực hiện một trong hai cách sau:
    *   Cách 1: Giữ phím Space rồi di chuyển chuột.
    *   Cách 2: Sử dụng thanh trượt dọc và thanh trượt ngang để cuộn nội dung trong cửa sổ sao cho hiển thị được vùng ảnh cần xem.
*   Để di chuyển ảnh nhưng không di chuyển khung ảnh, sử dụng công cụ Move (di chuyển) như sau:
    *   Bước 1. Nháy chuột vào công cụ Move.
    *   Bước 2. Kéo thả chuột trên đối tượng để di chuyển nó trên khung ảnh.
*   Ví dụ minh hoạ một kết quả di chuyển ảnh nhân vật hoạt hình bằng công cụ Move, khi đó ảnh lệch ra khỏi khung ảnh do khung ảnh được giữ cố định.
### 2 Cắt ảnh
*   Cắt ảnh là chọn, giữ lại một phần bức ảnh và loại bỏ phần còn lại. Nhu cầu cắt ảnh thường nảy sinh trong quá trình chỉnh sửa ảnh.
*   Ví dụ, sau khi hình nhân vật được chọn rồi tách ra khỏi nền ảnh, thao tác cắt ảnh sẽ giúp xác định một vùng hình chữ nhật đủ để chứa hình nhân vật cần lấy.
*   Thực hiện cắt ảnh như sau:
    *   Bước 1. Nháy chuột chọn công cụ Crop (cắt ảnh) rồi đưa chuột vào cửa sổ ảnh để xác định một vùng ảnh hình chữ nhật cần lấy.
    *   Bước 2. Kéo thả chuột trên các ô hình chữ nhật tại các đường biên vùng chọn để điều chỉnh kích thước vùng ảnh cần cắt.
### Bước 3. Nhấn phím Enter để xoá toàn bộ vùng ảnh bên ngoài vùng đã chọn.
*   Các cách cắt ảnh khác sử dụng công cụ chọn hoặc công cụ tạo đường dẫn để chọn vùng ảnh cần lấy.
*   Bản chất của những cách này là thực hiện “kĩ thuật cắt xén chi tiết thừa” đã được giới thiệu trong Chủ đề E ở lớp 10.
*   Sau khi cắt ảnh, thường phải thực hiện lệnh Layer\Layer to Image Size hoặc Image\Fit Canvas to Layers để điều chỉnh khung ảnh vừa với ảnh sau khi cắt.
## Biến đổi ảnh
*   Các thao tác hỗ trợ chỉnh sửa ảnh cũng thường phát sinh khi thực hiện các phép biến đổi ảnh, đặc biệt là thao tác cắt ảnh.
*   Ví dụ, một bức ảnh biểu tượng mũi Sa Vĩ (tỉnh Quảng Ninh) bị chụp nghiêng có thể được chỉnh cho thẳng lại bằng công cụ Perspective, sau đó ảnh được cắt để loại bỏ các phần thừa hai bên.
*   Lưu ý, quá trình biến đổi ảnh sau đó cắt ảnh có thể làm mất đi một phần bức ảnh.
*   Hãy khám phá một số công cụ biến đổi ảnh bằng cách thử biến đổi một ảnh nào đó: Scale (thay đổi kích thước), Rotate (xoay ảnh), Flip (lật ảnh), Perspective (biến đổi phối cảnh).
## Các bước biến đổi ảnh
*   **Bước 1.** Nháy chuột chọn công cụ biến đổi ảnh trong hộp công cụ.
*   **Bước 2.** Nháy chuột vào ảnh cần biến đổi. Một lưới hoặc khung bao quanh ảnh xuất hiện với các ô vuông nhỏ ở các góc, trên các cạnh và ở trung tâm. Các ô này được gọi là “mốc điều khiển”. Ngoài ra còn có một hộp thoại để nhập các tham số biến đổi ảnh.
*   **Bước 3.** Tiến hành biến đổi ảnh bằng cách kéo thả chuột từ các mốc điều khiển hoặc nhập các tham số vào hộp thoại.
*   Xác nhận kết quả biến đổi ảnh bằng cách nhấn phím Enter hoặc chọn một công cụ bất kì khác (thường chọn công cụ Move).
*   Nếu muốn huỷ bỏ kết quả biến đổi ảnh, thay vì nhấn Enter hãy nhấn phím ESC hoặc lệnh Reset trong hộp thoại.
## Thực hành chỉnh sửa ảnh
### Nhiệm vụ 1. Hiệu chỉnh màu sắc cho ảnh
*   **Yêu cầu:** Cho ảnh nhân vật chuột Mickey với đôi giày màu vàng như ở Hình 1a. Hãy đổi màu đôi giày của nhân vật để màu vàng sẫm hơn như ở Hình 5. Em có thể chọn ảnh khác và hiệu chỉnh lại màu sắc cho toàn bộ ảnh hoặc cho một đối tượng nào đó trong ảnh.
### Hướng dẫn thực hiện:
*   Cách hiệu chỉnh màu sắc cho một vùng ảnh như sau:
    *   Bước 1. Dùng công cụ Free Select kết hợp với các thao tác hỗ trợ để chọn chính xác đối tượng cần hiệu chỉnh màu sắc.
    *   Bước 2. Thực hiện lệnh Colors\Curves để mở hộp thoại Curves như ở Hình 6a. Đường chéo trong hộp thoại là dãy cung điều khiển màu sắc của ảnh.
    *   Bước 3. Nháy chuột vào danh sách Channel (kênh màu) để chọn màu cần hiệu chỉnh. Kéo thả chuột tại một vị trí thích hợp trên dãy cung để uốn nó hướng lên trên hoặc xuống dưới tuỳ theo ý định tăng hay giảm cường độ của màu đã chọn. Trong lúc kéo thả chuột, quan sát thấy nếu màu thay đổi như mong đợi thì dừng lại. Ví dụ, sau khi chọn từng màu Green, Blue và Red từ danh sách Channel rồi kéo thả các dãy cung màu để được các hình dạng tương tự như trong Hình 6b, giày của nhân vật sẽ đổi thành màu vàng sẫm như ở Hình 5.
### Nhiệm vụ 2. Sửa chữa ảnh bị nghiêng và lật đối xứng ảnh
*   **Yêu cầu:** Hãy sưu tầm một bức ảnh bị chụp nghiêng, sau đó sửa cho bức ảnh khỏi nghiêng và lật đối xứng nó để thay đổi hướng nhìn. Ví dụ, Hình 7a minh hoạ bức ảnh cầu Cần Thơ bị chụp nghiêng và được chỉnh lại như ở Hình 7b, sau đó được lật đối xứng để thay đổi góc nhìn thuận chiều từ trái sang phải như ở Hình 7c.
### Hướng dẫn thực hiện:
*   Bước 1: Chọn công cụ Perspective rồi nháy chuột vào ảnh cầu Cần Thơ.
*   Bước 2: Kéo thả chuột tại các điểm mốc phù hợp để chỉnh cho ảnh hết nghiêng. Dùng công cụ Crop để cắt ảnh và nhận được kết quả. Dùng công cụ Flip để lật ảnh và thu được kết quả.
### Hoạt động:
*   Em hãy sưu tầm một bức ảnh bị chụp nghiêng, sau đó sửa cho bức ảnh khỏi nghiêng và hiệu chỉnh lại màu sắc của một đối tượng nào đó trong ảnh.
### Bài tập điền từ:
*   Trong các câu khẳng định dưới đây, mỗi số thứ tự biểu thị một chỗ trống cần điền. Từng số thứ tự này cần thay bằng từ nào trong các từ sau: Space, Move, Zoom, Fit Canvas to Layers?
    *   a) Dùng phím (1) hoặc dùng các thanh trượt dọc/ngang để di chuyển ảnh.
    *   b) Dùng công cụ (2) để di chuyển ảnh trên khung ảnh (canvas).
    *   c) Sau khi cắt ảnh thường dùng lệnh (3) để khung ảnh khớp với kích thước của ảnh sau khi cắt.
    *   d) Dùng công cụ (4) kết hợp với phím Ctrl để thu nhỏ hoặc phóng to ảnh.
### Tóm tắt bài học:
*   Thu nhỏ, phóng to ảnh bằng cách nhấn, giữ phím Ctrl và lăn nút cuộn chuột. Hai cách khác là dùng công cụ Zoom hoặc ô tỉ lệ thu/phóng ảnh.
*   Di chuyển toàn bộ ảnh (ảnh và khung ảnh) bằng cách nhấn, giữ phím Space và di chuyển chuột. Di chuyển ảnh (nhưng giữ cố định khung ảnh) bằng công cụ Move.
*   Một số công cụ biến đổi ảnh thường sử dụng là: Scale, Rotate, Flip, Perspective.
## BÀI 2 TẨY XOÁ ẢNH
### Học xong bài này, em sẽ:
*   Thực hiện được cách tẩy xoá ảnh bằng các công cụ Clone và Healing.
# Thực hiện được cách sao chép ảnh theo phép phối cảnh bằng công cụ Perspective Clone.
*   Thực hiện được cách sao chép ảnh theo phép phối cảnh bằng công cụ Perspective Clone.
*   Hiện trạng của khu du lịch thác Dray Nur như ở Hình 1a. Để chuẩn bị cho việc chỉnh trang khu du lịch, người quản lí đã nhờ người thiết kế cảnh quan như Hình 1b. Em hãy chỉ ra các điểm khác biệt giữa hai hình này. Theo em, bằng cách nào ta có thể nhận được bức ảnh ở Hình 1b?
*   **① Tẩy xoá ảnh bằng công cụ Clone**
## Tẩy xoá ảnh bằng công cụ Clone
    *   Tẩy xoá ảnh là loại bỏ những chi tiết nào đó trong ảnh, đồng thời thay chúng bằng những chi tiết khác phù hợp sao cho ảnh không để lại dấu vết đã tẩy xoá.
    *   Ví dụ, ở vị trí 1 trong Hình 2, sau khi loại bỏ cái cây bị cắt cụt cành và thay bằng một thảm cỏ sẽ nhận được kết quả như ở Hình 1b. Các chi tiết ở vị trí 2 và 3 cũng được chỉnh sửa tương tự.
    *   Để tẩy xoá và phục hồi ảnh trong GIMP, sử dụng các công cụ: Clone, Perspective Clone và Healing. Dưới đây là cách sử dụng công cụ Clone.
### Bước 1. Chọn công cụ Clone
        *   Phóng to ảnh và di chuyển ảnh để tập trung vào vùng ảnh cần xử lí (Hình 3a). Nháy chuột chọn công cụ Clone. Nó được xem như một cái bút lông. Ở bảng tuỳ chọn của công cụ, mở danh sách Brush (bút lông) và chọn kiểu của bút lông tuỳ theo độ phóng to và màu sắc của vùng ảnh được xử lí (Hình 3b).
### Bước 2. Lấy mẫu
    *   Nhấn, giữ phím Ctrl khi nháy chuột vào một điểm ảnh cần lấy mẫu để áp dụng vào vùng ảnh cần tẩy xoá.
    *   Ví dụ, nháy chuột vào một điểm trên mặt nước, gần chỗ cành cây.
### Bước 3. Thực hiện tẩy xoá ảnh dựa trên mẫu
    *   Nháy chuột vào những điểm ảnh cần tẩy xoá.
    *   Sau mỗi lần nháy chuột, điểm ảnh tại chỗ vừa nháy chuột sẽ có màu sắc như điểm ảnh mẫu.
    *   Theo ví dụ, nháy chuột vào những chỗ thuộc cành cây để biến nó thành mặt nước.
    *   Khi thấy thích hợp, có thể kéo thả chuột lên vùng ảnh cần xoá để tốc độ tẩy xoá nhanh hơn và tăng độ tương đồng với vùng ảnh mẫu.
#### Chú ý:
    *   Lặp lại Bước 2 và Bước 3 ở đây nếu cần thay đổi điểm ảnh mẫu.
    *   Sau khi xóa xong phần cành cây chỗ mặt nước, để xóa phần thân cây trên nền cỏ xanh, cần lấy lại mẫu mới là một điểm nào đó trên đám cỏ xanh.
    *   Công cụ Clone lấy mẫu của một vùng ảnh (gọi là vùng mẫu) để áp dụng vào vùng cần tẩy xóa trong ảnh (gọi là vùng đích).
## Tẩy xoá ảnh bằng công cụ Healing
    *   Khi sử dụng công cụ Clone để chỉnh sửa ảnh ở các vị trí được chỉ ra trong Hình 2, trên ảnh lộ ra khá rõ chỗ tẩy xoá. Theo em, tại sao công cụ Clone có hạn chế này?
    *   Công cụ Healing cũng có cách sử dụng tương tự như công cụ Clone.
    *   Công cụ Healing không chỉ có tác dụng như công cụ Clone mà còn hòa trộn độ sáng và sắc thái của các điểm ảnh giữa vùng mẫu và vùng đích để làm cho những điểm ảnh được chỉnh sửa không có sự khác biệt với những điểm ảnh còn lại.
    *   Việc loại bỏ một chi tiết trên ảnh bằng công cụ Clone làm lộ ra dấu vết tẩy xoá tại đường biên của vùng ảnh bị tẩy xoá.
    *   Cần sử dụng công cụ Healing tô lên đường biên này để làm mờ vết tẩy xoá.
    *   Ví dụ, dấu vết tẩy xoá ở Hình 5a được xử lí bằng công cụ Healing và nhận được vùng ảnh nhìn tự nhiên hơn như ở Hình 5b.
## Sao chép ảnh theo phép biến đổi phối cảnh bằng công cụ Perspective Clone
    *   Hình 6a và Hình 6b đều thể hiện kết quả sao chép hai cái cây từ vị trí 1 đến vị trí 2 của cùng một ảnh. Theo em, nếu sử dụng công cụ Clone thì sẽ tạo ra được kết quả nào (Hình 6a hay Hình 6b)? Tại sao?
    *   Công cụ Clone hoạt động như một công cụ sao chép các đối tượng mẫu.
    *   Đối tượng đích (kết quả sao chép) giống hệt đối tượng mẫu.
    *   Trong nhiều trường hợp, đối tượng đích được mong đợi là kết quả của một phép biến đổi phối cảnh của đối tượng mẫu.
    *   Công cụ Perspective Clone giúp thực hiện phép biến đổi này.
### Cách sử dụng công cụ Perspective Clone:
#### Bước 1. Chọn công cụ Perspective Clone
    *   Nháy chuột chọn công cụ Perspective Clone.
    *   Ở bảng tùy chọn của công cụ, chọn chế độ Modify Perspective để làm xuất hiện một khung mờ xung quanh ảnh, gọi là khung phối cảnh.
    *   Trên khung có các điểm điều khiển là các ô vuông nhỏ ở các góc và trên các cạnh.
    *   Để nhìn thấy khung này cần thu nhỏ ảnh.
#### Bước 2. Xác định hình dạng khung phối cảnh
    *   Kéo thả chuột tại các điểm điều khiển trên khung phối cảnh để xác định hình dạng mà nó biểu thị phép đồng dạng phối cảnh của đối tượng mẫu.
    *   Phép biến đổi này sẽ được áp dụng để tạo đối tượng đích.
#### Bước 3. Sao chép phối cảnh
    *   Ở bảng tùy chọn của công cụ, chọn chế độ **Perspective Clone**. Khung phối cảnh tạm ẩn.
    *   Nhấn phím **Ctrl** và nháy chuột vào một điểm trên đối tượng mẫu, ở vị trí 1.
    *   Nháy chuột vào một điểm nào đó được chọn là vị trí xuất phát để tạo đối tượng đích, ví dụ đó là vị trí 2.
    *   Nháy chuột hoặc kéo thả chuột trên vùng ảnh cần tạo đối tượng đích. Nháy hoặc kéo thả chuột đến đâu, đối tượng đích hiện ra đến đó và thể hiện kết quả sao chép đối tượng mẫu theo phép đồng dạng phối cảnh đã xác định.
    *   Tiếp tục quá trình này cho đến khi đối tượng đích được tạo đầy đủ.
#### Bước 4. Hoàn thiện
    *   Đối tượng đích có thể có những chi tiết thừa hoặc bất hợp lí khi được sao chép từ đối tượng mẫu.
    *   Sau khi đối tượng đích được tạo xong, cần sử dụng công cụ **Clone** và có thể kết hợp với công cụ **Healing** để loại bỏ các chi tiết này.
    *   Cuối cùng thu được sản phẩm mong đợi.
## Thực hành tẩy xoá ảnh
    *   **Yêu cầu:**
        *   Một cảnh của thị xã Cửa Lò được chụp.
        *   Khu đất ở vị trí 1 chưa được xây dựng, có sỏi, đá, cát rất bừa bộn, làm cho bức ảnh bị xấu đi.
        *   Theo quy hoạch, mảnh đất này sẽ được làm sân bóng chuyền với cây cối xung quanh tương tự như mảnh đất ở vị trí 2.
        *   Sử dụng GIMP để tạo ra bức ảnh như mô tả để xem trước kết quả quy hoạch mảnh đất nói trên.
### Hướng dẫn thực hiện:
        *   *Bước 1. Chọn công cụ Perspective Clone:*
            *   Thu nhỏ ảnh và nháy chuột chọn công cụ Perspective Clone.
            *   Chọn chế độ Modify Perspective để làm xuất hiện khung phối cảnh.
#### Bước 2. Xác định hình dạng khung phối cảnh:
Kéo thả chuột tại các điểm điều khiển ở cạnh và các góc trên khung phối cảnh để có hình dạng khu đất cần quy hoạch.
    *   **Bước 3. Sao chép phối cảnh:** Chọn chế độ Perspective Clone rồi thực hiện quá trình nhấn phím Ctrl và nháy chuột lấy mẫu ảnh từ khu đất ở vị trí 2, sau đó nhấn hoặc kéo thả chuột trên ảnh khu đất ở vị trí 1 để sao chép mẫu theo phép phối cảnh.
    *   **Bước 4. Hoàn thiện:** Sử dụng công cụ Clone để tẩy xoá chỗ đất và rác bừa bộn ở xung quanh và thay bằng tán lá cây ở khu vực ảnh lấy mẫu.
    *   **Hướng dẫn tương tác:** Em hãy lựa chọn một ảnh chứa đối tượng cần loại bỏ. Sau đó, tiến hành tẩy xoá đối tượng này đồng thời khôi phục vùng ảnh chỗ tẩy xoá một cách hợp lí.
## Tóm tắt bài học:
    *   Công cụ Clone dùng để sao chép y nguyên hình dạng, kích thước vùng mẫu sang vùng đích.
    *   Công cụ Perspective Clone dùng để sao chép từ vùng mẫu sang vùng đích theo một phép biến đổi đồng dạng phối cảnh.
    *   Công cụ Healing dùng để sao chép, hoà trộn màu sắc và ánh sáng giữa vùng mẫu với vùng đích.
    *   Các công cụ Clone, Perspective Clone và Healing giúp tẩy xoá các dấu vết trên ảnh, giúp thay thế một chi tiết trên ảnh bằng một chi tiết khác có trên ảnh đó.
# BÀI 3: TẠO ẢNH ĐỘNG
    *   **Học xong bài này, em sẽ:**
        *   Tạo được ảnh động với hiệu ứng tự thiết kế.
        *   Tạo được ảnh động từ các hiệu ứng có sẵn trong phần mềm.
    *   **Hình 1 minh họa một dãy các lớp ảnh tĩnh trong GIMP.**
        *   Ảnh thứ nhất là hình con bướm đang dang cánh rộng nhất.
        *   Ảnh thứ ba là hình con bướm đó với cánh được gập hẹp lại.
        *   Ảnh thứ hai và thứ tư là hình nền màu vàng.
        *   Câu hỏi: Ta sẽ nhìn thấy điều gì nếu dãy ảnh này xuất hiện liên tục, từ ảnh thứ nhất đến ảnh thứ tư rồi quay về ảnh thứ nhất?
        *   Câu hỏi: Tại sao lại cần lớp ảnh nền vàng xen giữa các lớp ảnh hình con bướm?
## Ảnh động, kịch bản và hiệu ứng của ảnh động
    *   Ảnh động được tạo từ các ảnh tĩnh.
    *   Các ảnh tĩnh này được gọi là các khung hình của ảnh động.
    *   Khi ảnh động được kích hoạt, các khung hình xuất hiện trong những khoảng thời gian xác định, làm cho nội dung bên trong ảnh thay đổi liên tục và tạo ra cảm giác đối tượng trong ảnh cử động hoặc chuyển động.
    *   Dãy 4 khung hình có thể tạo được một ảnh động mà đối tượng cử động là con bướm vỗ cánh.
    *   Thứ tự các lớp ảnh cho thấy con bướm xuất hiện rồi bị che mất ngay bởi nền màu vàng hiện ra ngay sau đó.
    *   Cách thức xuất hiện của từng khung hình là nó hiện ra rồi biến mất rất nhanh, thời gian xuất hiện của từng khung hình là không đáng kể.
    *   Khi xem ảnh động sẽ thấy con bướm này vỗ cánh liên tục.
*   Để xem được con bướm vỗ cánh chậm hơn, cần chỉ rõ thời gian xuất hiện của từng khung hình trong các ngoặc đơn và sau tên lớp ảnh, đúng như mẫu mô tả.
*   Với mẫu mô tả này, cách thức và thời gian xuất hiện của các khung hình là: từng hình con bướm xuất hiện 500 ms, thời gian để mỗi mô hình này xuất hiện trở lại là 50 ms.
# Bài 3: Thiết kế Ảnh Động
*   Trong ví dụ trên, “vỗ cánh” được xem là hiệu ứng của ảnh động.
*   Để tạo được hiệu ứng này cần xây dựng các lớp ảnh tĩnh và mô tả kịch bản.
*   Kịch bản hoạt động của đối tượng trong ảnh động được thể hiện qua các khung hình.
*   Hai khung hình liên tiếp biểu thị sự thay đổi (động tác, cử chỉ, trạng thái, vị trí...) trong cùng một hành động của đối tượng.
*   Nếu sự thay đổi này sai khác quá nhiều thì chuyển động của ảnh động sẽ bị giật, ngược lại thì chuyển động đó sẽ mềm mại hơn.
*   Do đó, càng nhiều khung hình biểu thị một hành động của đối tượng thì chuyển động của ảnh động càng mềm mại.
*   Ví dụ, xét ảnh động biểu thị hiệu ứng “trượt dốc”: Nếu ảnh chỉ có hai khung hình đầu và cuối thì chuyển động của ảnh động sẽ bị giật, nếu ảnh có đủ 4 khung hình thì chuyển động sẽ mềm mại hơn.
*   Tương tự như kịch bản cho hiệu ứng “vỗ cánh” được giới thiệu trên đây, có thể đề xuất ý tưởng kịch bản cho một hiệu ứng khác, ví dụ hiệu ứng “chữ chạy”, “lá rơi”, “tải dữ liệu”.
*   Các bước chung để tạo ảnh động với hiệu ứng tự thiết kế trong GIMP như sau:
## Bước 1: Chuẩn bị các ảnh tĩnh cho ảnh động
*   Với vai trò là các khung hình của ảnh động, các ảnh tĩnh đã chọn phải giúp xây dựng được kịch bản cho việc tạo hiệu ứng.
*   Ví dụ, từ dãy ảnh tĩnh, có thể tạo kịch bản cho hiệu ứng vỗ cánh.
*   Với ảnh tĩnh có sẵn, thường phải chỉnh sửa lại.
*   Ví dụ, sau khi sưu tầm được ảnh con bướm, nó được tách khỏi nền và đổi lại nền ảnh màu vàng.
*   Ảnh này được sao chép và dùng công cụ Perspective để co ảnh.
Trang 102
*   Có thể tự thiết kế hoặc sưu tầm các ảnh tĩnh. Với ảnh có sẵn, thường phải chỉnh sửa lại, chẳng hạn như: tách ảnh khỏi nền, cắt ảnh, biến đổi ảnh, tẩy xóa các chi tiết thừa.
*   Ví dụ, ảnh con bướm có thể tự thiết kế như ở Hình 4a hoặc sưu tầm được như ở Hình 4b. Sau đó, tách ảnh khỏi nền trắng và đổi lại nền ảnh như ở Hình 1a, dùng công cụ Perspective để co ảnh như ở Hình 1c.
## Bước 2: Xây dựng kịch bản cho hiệu ứng của ảnh động
*   Ở bước này, cần tưởng tượng ra hoạt động của đối tượng, từ đó tạo nội dung cho từng khung hình cùng với thứ tự và thời gian xuất hiện của chúng.
*   Ví dụ, hiệu ứng vỗ cánh được thể hiện bởi hai trạng thái dang rộng và thu nhỏ của đôi cánh. Mặt khác, do có hiện tượng lưu ảnh trong võng mạc của mắt người nên khi hình thứ hai của con bướm xuất hiện, mắt người vẫn đồng thời nhìn thấy cả hình thứ nhất của con bướm đó trong 0,04 giây đầu tiên. Để tránh hiện tượng này cần có một “ảnh che” (có màu nền trùng với màu nền ảnh trước đó) xuất hiện trước khi ảnh tiếp theo của con bướm hiện ra. Từ đó, cần tạo dãy 4 khung hình và thứ tự của chúng như ở Hình 1. Hơn nữa, quy định lại thời gian xuất hiện cho từng khung hình như mẫu mô tả ở Hình 2. Trong trường hợp có nhiều khung hình, ví dụ như ở Hình 3, có thể không cần các ảnh che.
*   Nếu các ảnh tĩnh được chuẩn bị là các tệp ảnh độc lập. Nên mở ảnh tĩnh ứng với khung hình thứ nhất, sau đó mở các ảnh còn lại như một lớp ảnh mới bằng lệnh **File\ Open As Layers**.
## Bước 3: Xuất ảnh động
*   Bật từng lớp ảnh để kiểm tra lại từng khung hình, chẳng hạn kiểm tra xem ảnh có trùng khít với khung ảnh không và các lớp ảnh có kích thước giống nhau không.
*   Thực hiện lệnh **File\Export As** để mở hộp thoại Export Image (Hình 5), nhập tên tệp ảnh động với đuôi tệp là “.gif” và nhấn phím Enter.
*   Hộp thoại Export Image as GIF xuất hiện. Nháy chuột chọn ô As animation rồi nhấn phím Enter hoặc lệnh Export để xuất dãy khung hình ra một tệp ảnh động (định dạng GIF). Bây giờ có thể mở tệp ảnh động này để xem kết quả.
*   **Chú ý:** Trước khi thực hiện Bước 3, có thể xem trước ảnh động bằng lệnh Filters\Animation\Playback. Hộp thoại Animation Playback xuất hiện. Có thể sử dụng các lệnh điều hướng như Step back, Step để xem ảnh động, từ đó cân nhắc điều chỉnh thời gian cho từng khung hình.
## Tạo ảnh động từ hiệu ứng có sẵn trong GIMP:
*   Lệnh Filters\Animation của GIMP cung cấp một số hiệu ứng để tạo ảnh động. Hãy khám phá các hiệu ứng có sẵn này trong GIMP để tạo ảnh động.
*   Trong trường hợp nội dung hai khung hình liên tiếp không biểu thị hành động của đối tượng thì nên tạo ảnh động dựa trên hiệu ứng có sẵn trong GIMP. Ví dụ, từ ba ảnh về một cảnh ở Mộc Châu, Sơn La có thể tạo ảnh động với hiệu ứng Blend (hiệu ứng mờ dần).
### Cách tạo ảnh động từ một hiệu ứng có sẵn có thể khái quát qua các bước sau:
#### Bước 1: Chuẩn bị ảnh tĩnh cho ảnh động
*   Tạo tệp ảnh mới và thực hiện lệnh File\Open As Layers để mở các ảnh tĩnh dưới dạng các lớp ảnh. Ví dụ, mở ba ảnh.
#### Bước 2: Tạo dãy khung hình cho ảnh động và gán thời gian (nếu cần)
*   Thực hiện lệnh Filters\Animation để mở ra danh sách các hiệu ứng, chọn tên một hiệu ứng để tạo ảnh động. Theo ví dụ, chọn hiệu ứng Blend.
*   Nếu cần, thực hiện lệnh Filters\Animation\Optimize (for GIF) để GIMP tạo dãy khung hình gắn với thời gian. Nháy đúp chuột vào các tên các khung hình có ảnh rõ nhất và tăng thời gian hiển thị các chúng.
#### Bước 3: Xuất ảnh động
*   Với dãy khung hình đã tạo, có thể xem trước ảnh động và thực hiện lệnh `File\ExportAs` để xuất ảnh động sang định dạng GIF.
## 4 Thực hành tạo hiệu ứng cho ảnh động
### Yêu cầu:
*   Hình 9 cho thấy trong nửa đầu chu kì dao động của con lắc, con lắc chuyển động từ A qua O đến B. Trong nửa sau chu kì dao động, con lắc chuyển động ngược lại: từ B qua O về A. Hãy tạo ảnh động biểu thị dao động của một con lắc đơn.
### Hướng dẫn thực hiện:
#### Bước 1: Chuẩn bị các ảnh tĩnh cho ảnh động
*   Nửa đầu chu kì dao động của con lắc được thể hiện trong Hình 10, gồm các khung hình từ Hình 10a đến Hình 10e. Nửa sau chu kì dao động của con lắc cũng được thể hiện trong Hình 10 nhưng từ khung hình Hình 10e ngược trở về khung hình Hình 10a.
*   Như vậy, cần thiết kế 5 ảnh tĩnh như trong Hình 10, chúng tương ứng có vai trò là 5 khung hình của ảnh động. Tuy nhiên, chỉ cần thiết kế một ảnh tĩnh. Các ảnh còn lại có thể được tạo bằng ba thao tác chính áp dụng cho ảnh con lắc, đó là: nhân đôi lớp ảnh bằng lệnh, quay ảnh bằng công cụ `Rotate` và lật đối xứng ảnh bằng công cụ `Flip`.
*   Ảnh tĩnh cần thiết kế bao gồm cảnh nền (thanh gỗ treo và trục đứng màu đỏ) và con lắc (quả lắc và dây lắc). Những đối tượng này có thể được tạo bằng các công cụ chọn `Rectangle Select`, `Ellipse Select` và công cụ tô màu thuần nhất `Bucket Fill`.
#### Bước 2: Xây dựng kịch bản cho hiệu ứng của ảnh động
*   Giả sử các khung hình trong Hình 10 được thiết kế và lần lượt xuất ra các tệp ảnh (đuôi PNG) với tên tệp là “Con lac 1”, “Con lac 2”, “Con lac 3”, “Con lac 4”, “Con lac 5”.
*   Mở tệp ảnh thứ nhất. Từ tệp ảnh này, mở các tệp ảnh còn lại dưới dạng các lớp ảnh mới bằng lệnh `File\Open as Layers` rồi sắp xếp lại các lớp ảnh như ở Hình 11. Đây là dãy khung hình thể hiện nửa đầu chu kì dao động của con lắc.
*   Để thể hiện nốt nửa sau chu kì dao động của con lắc, nhân đôi từng lớp ảnh và sắp xếp lại các lớp ảnh.
#### Bước 3: Xuất ảnh động
*   Chọn tệp ảnh với dãy 10 khung hình rồi thực hiện lệnh File\Export As để xuất ảnh động với định dạng GIF.
*   Hãy tạo một ảnh động với hiệu ứng tự thiết kế để mô phỏng hoạt động của một đối tượng hay hiện tượng nào đó. Hiệu ứng của ảnh động do em tự chọn hoặc sáng tạo, ví dụ hiệu ứng lắc lư của con lật đật.
*   Em đồng ý với những phát biểu nào dưới đây? Trong phần mềm thiết kế đồ họa GIMP:
    *   Nguồn ảnh tĩnh của ảnh động luôn phải tự thiết kế.
    *   Có thể thiết kế ảnh động từ các hiệu ứng có sẵn hoặc tự tạo.
    *   Có thể xem trước và chỉnh sửa ảnh động khi xuất ảnh động với định dạng GIF.
    *   Thứ tự các khung hình của ảnh động được sắp xếp tuỳ ý.
    *   Thời gian xuất hiện của từng khung hình của ảnh động ảnh hưởng đến tốc độ chuyển động của ảnh động.
## Tóm tắt bài học
*   Ảnh động gồm một dãy các khung hình. Thứ tự các khung hình cùng với thời gian xuất hiện của chúng thể hiện kịch bản tạo ra hiệu ứng của ảnh động.
*   GIMP cung cấp một số hiệu ứng để tạo ảnh động, các hiệu ứng khác có thể tự thiết kế theo trí tưởng tượng và sự sáng tạo.
*   Khi thiết kế ảnh động với hiệu ứng tự tạo, nguồn ảnh tĩnh cho ảnh động phải được chuẩn bị và sắp xếp theo kịch bản của hiệu ứng cần tạo.
*   Nếu tự tạo nguồn ảnh tĩnh, cần đến các kĩ thuật thiết kế đồ hoạ và các thao tác chỉnh sửa ảnh như cắt, biến đổi ảnh, tẩy xoá chi tiết trong ảnh.
# BÀI 4 GIỚI THIỆU PHẦN MỀM LÀM VIDEO
*   **Học xong bài này, em sẽ:**
    *   Bước đầu biết sử dụng một số chức năng chính của phần mềm làm video.
    *   Tạo được một số đoạn video từ ảnh và video có sẵn.
*   **Câu hỏi gợi mở:** Em đã từng sử dụng các video để hỗ trợ trong quá trình học tập và giải trí chưa? Em hãy kể những lợi ích khi sử dụng các video này. Em có biết cách tạo ra các video đó không?
# Video phục vụ học tập và giải trí
*   Các video có khả năng truyền tải thông điệp rất mạnh mẽ, do sự kết hợp giữa âm thanh và hình ảnh làm cho não bộ con người tiếp nhận thông tin tốt hơn.
*   Có thể chủ động học bài qua các video bài giảng của thầy, cô giáo.
*   Video từ các phương tiện truyền thông khác nhau như ti vi, Internet, phim ở rạp, giúp không chỉ trong học tập mà còn giải trí cũng như mở rộng hiểu biết về thế giới.
*   Ví dụ, qua đoạn video giới thiệu những điểm du lịch ở Hà Giang, em biết được nơi đây có ruộng bậc thang Hoàng Su Phì tuyệt đẹp.
*   Để làm những đoạn video chuyên nghiệp đòi hỏi phải có đội ngũ làm video, quay video và các thiết bị chuyên dụng.
*   Chủ đề này giới thiệu cách làm video đơn giản, sử dụng máy chụp ảnh kĩ thuật số và phần mềm làm video.
## Các bước làm video được hỗ trợ bởi phần mềm gồm:
*   Bước 1. Gợi ý cho ý tưởng chủ đề video và kịch bản video.
*   Bước 2. Chuẩn bị tư liệu cho video: bao gồm các đối tượng (hình ảnh, âm thanh, video) được đưa vào video.
*   Bước 3. Tạo dự án video và đưa tư liệu vào dự án video.
*   Bước 4. Chỉnh sửa video: chỉnh sửa các đối tượng trong video, cắt và ghép các đoạn video, tách hoặc thay đổi âm thanh, thêm hiệu ứng, hội thoại, làm tiêu đề, phụ đề, lời thuyết minh.
*   Bước 5. Lưu trữ và xuất video (với nhiều định dạng tệp, chia sẻ video qua Internet).
# Khám phá phần mềm Animiz Animation Maker
*   Phần mềm Animiz (tên đầy đủ là Animiz Animation Maker) cung cấp các tính năng như: tạo đoạn video, chỉnh sửa video, tạo ảnh động.
*   Animiz cung cấp nhiều mẫu đối tượng với nhiều chủ đề phong phú sẽ tạo thuận lợi cho việc làm video vừa đơn giản nhưng cũng rất hấp dẫn.
*   Bản miễn phí sẽ chỉ hạn chế một số mẫu đối tượng, muốn sử dụng nhiều mẫu hơn sẽ phải trả phí.
*   Để sử dụng Animiz cần cài đặt phần mềm trên máy tính, đăng kí tài khoản sử dụng qua một tài khoản email.
*   Chủ đề này sử dụng phần mềm Animiz Animation Maker phiên bản 2.5.6 miễn phí.
*   Hãy khởi động Animiz bằng cách nháy đúp chuột vào biểu tượng phần mềm.
*   Tại giao diện bắt đầu, hãy quan sát và tìm hiểu các thành phần trên cửa sổ giao diện này.
## a) Giao diện bắt đầu
*   Giao diện bắt đầu gồm ba thành phần chính:
### ① Các mẫu video trực tuyến
### ② Bảng chọn (cho biết thông tin phiên bản phần mềm, những dự án gần đây, các mẫu video đã sử dụng, các dự án đám mây và danh mục các chủ đề video mẫu)
### ③ Thanh công cụ (gồm các lệnh làm việc với tệp dự án như mở tệp mới, mở tệp đã có).
## b) Giao diện chỉnh sửa video
*   Khi tạo mới hoặc mở một dự án, giao diện chỉnh sửa video xuất hiện, gồm các thành phần chính sau:
    *   Thanh bảng chọn: gồm các dải lệnh File, Edit, Action, Timeline, Help.
    *   Thanh công cụ điều hướng: gồm các lệnh thông dụng như Home (trở về giao diện bắt đầu của Animiz), Preview (xem trước dự án video), Save (lưu dự án video), Publish (xuất bản dự án video).
    *   Thanh công cụ tiện ích: gồm các lệnh căn chỉnh đối tượng (sao chép, xoá,...).
    *   Vùng thiết đặt cảnh: gồm các lệnh thêm, xoá, di chuyển các cảnh.
    *   Khung Canvas: là nơi xem trước toàn bộ những gì diễn ra trong video. Đây cũng là nơi đưa các đối tượng vào dự án video và thực hiện căn chỉnh.
    *   Thanh đối tượng: gồm các lệnh chọn đối tượng như hình (Shape), ảnh (Image), văn bản (Text), mẫu nhân vật (Roles), hoạt hình mẫu (Animation Widget), hiệu ứng (Effect), âm thanh (Sound), video.
    *   Khung Timeline: là nơi biểu thị khung thời gian xuất hiện của các đối tượng trong video, mỗi đối tượng xuất hiện trên một dòng và có thể tuỳ chỉnh.
## 3) Thực hành tạo video
### Yêu cầu:
*   Ở lớp 10, em đã học sử dụng GIMP để thiết kế một số sản phẩm đồ hoạ. Em hãy tạo một đoạn video hướng dẫn thiết kế logo đơn giản cho lớp em. Đoạn video gồm khoảng
*   10 ảnh sẽ xuất hiện lần lượt. Đây là các ảnh chụp các bước hướng dẫn thiết kế logo bằng GIMP và có nhạc nền.
### Hướng dẫn thực hiện:
#### Bước 1. Gợi ý cho ý tưởng chủ đề video và kịch bản video
*   Chủ đề: Giới thiệu cách tạo logo của lớp bằng GIMP.
*   Kịch bản: Hình ảnh các bước tạo logo trong GIMP xuất hiện liên tiếp với thời lượng 30 giây.
#### Bước 2. Chuẩn bị tư liệu cho video
*   Chụp ảnh các bước thực hiện: Mở GIMP, vẽ logo, xuất file.
*   Lựa chọn và lưu về máy tệp nhạc yêu thích từ Internet.
*   **Chú ý:** Nên lưu các tệp ảnh và nhạc vào một thư mục để dễ tìm kiếm.
#### Bước 3. Tạo dự án video và đưa tư liệu vào dự án video
*   Khởi động Animiz: Chọn New Empty Project để tạo dự án trống mới.
*   Đặt thời lượng: Tại ô thời gian trong khung Timeline tăng thời gian thành 30 giây.
*   Nhập hình ảnh: Chọn đối tượng Image trên thanh đối tượng, chọn Add local image. Mở thư mục ảnh đã tạo ở Bước 2, chọn các ảnh đưa vào video, chọn Open.
*   Animiz hỗ trợ mở được nhiều loại tệp ảnh như: gif, png, jpg, jpeg, svg, psd,...
*   Các ảnh được nhập sẽ xuất hiện ở khung Timeline, mỗi ảnh trên một dòng và mặc định xuất hiện cùng khung thời gian.
*   Mỗi đối tượng trên khung Timeline gồm tên đối tượng (Anh1, Anh2,...), hiệu ứng xuất hiện và hiệu ứng biến mất. Thời gian xuất hiện của đối tượng được tính từ điểm thời gian bắt đầu của hiệu ứng xuất hiện đến điểm thời gian kết thúc của hiệu ứng biến mất.
Trang 112
#### Bước 4. Chỉnh sửa video
*   Muốn các đối tượng xuất hiện lần lượt thì cần thay đổi khung thời gian của mỗi đối tượng bằng cách nháy chuột vào hiệu ứng xuất hiện và biến mất tương ứng, kéo và thả đến vị trí khung thời gian mong muốn.
*   Thay đổi vị trí, kích thước ảnh: chọn ảnh trên khung Canvas, xuất hiện khung chữ nhật bao quanh, kéo thả ảnh đến vị trí và kích thước mong muốn.
*   Nhập âm thanh: Chọn Sound trên thanh đối tượng, chọn Add Sound. Mở thư mục chứa tệp nhạc (ở Bước 2) và chọn tệp nhạc. Tệp âm thanh sẽ xuất hiện ở khung Timeline. Animiz hỗ trợ các loại tệp âm thanh như: mp3, wav, wma, flac, ape, acc.
*   Ngoài ra ở thanh đối tượng còn rất nhiều loại đối tượng có thể đưa vào video như video, văn bản, hình vẽ,… Cách nhập các đối tượng này tương tự như nhập ảnh.
*   Các đối tượng được nhập sẽ cùng xuất hiện trong một cảnh video (scene). Nếu muốn tạo cảnh khác, chọn New Scene tại vùng thiết đặt cảnh và nhập các đối tượng cho cảnh video mới.
*   Một video có thể có một hoặc nhiều cảnh. Với phiên bản miễn phí, Animiz cho phép tạo tối đa 5 cảnh video.
#### Bước 5. Xem và lưu dự án video
*   Để xem trước video, sử dụng các nút như ở Hình 4:
##### Chọn Preview (nút ①) hoặc nhấn tổ hợp phím Ctrl + Shift + Space để xem toàn bộ video (tất cả các cảnh video).
##### Chọn Play the current scene (nút ②) hoặc phím Space: xem cảnh video đang được chọn từ vị trí con trỏ trên khung Timeline.
##### Chọn Play the current scene from start (nút ③) hoặc nhấn tổ hợp phím Shift + Space: xem cảnh video đang được chọn từ đầu.
*   Lưu dự án video với tệp có đuôi “.am”: chọn Save ở thanh công cụ điều hướng, nhập tên tệp là “tao_logo”.
*   Xuất video: chọn Publish, chọn định dạng tệp muốn lưu và đặt tên tệp.
*   Em hãy tạo video giới thiệu một lễ hội ở quê em hoặc em biết.
### Trong các câu sau, những câu nào đúng?
*   1) Các đối tượng trong video chỉ có ảnh và âm thanh.
*   2) Tất cả các ảnh trong video nên xuất hiện trong cùng một khung thời gian.
*   3) Các ảnh trong video nên xuất hiện trong các khung thời gian liên tiếp nhau.
*   4) Các đối tượng khi đưa vào video sẽ có trong cùng một cảnh nếu không tạo cảnh mới.
### Tóm tắt bài học
*   Các phần mềm làm video đều có chức năng dựng video, gồm tạo dự án video mới và nhập các đối tượng cho video.
*   Animiz Animation Maker cung cấp các chức năng dựng video cơ bản và hỗ trợ nhiều mẫu video, mẫu đối tượng trực tuyến.
# BÀI 5 CHỈNH SỬA VIDEO
# Học xong bài này, em sẽ:
*   Sử dụng được một số công cụ cơ bản chỉnh sửa video: chỉnh sửa hình ảnh, âm thanh, tạo phụ đề, tạo các hiệu ứng chuyển cảnh, căn chỉnh thời gian.
*   Biên tập được đoạn video phục vụ học tập, giải trí.
*   Sau khi xem đoạn video đã tạo ở phần thực hành của Bài 4, em hãy liệt kê những thay đổi mà mình muốn và giải thích vì sao.
## (1) Công việc chỉnh sửa video
*   Việc điều chỉnh và sắp xếp lại các cảnh, các đối tượng trong video được gọi là biên tập hay chỉnh sửa video. Chỉnh sửa video được xem là một phần quan trọng trong quy trình làm video. Trước khi bắt đầu, cần xác định rõ mục tiêu của việc chỉnh sửa video. Điều này sẽ giúp chúng ta có cách tiếp cận chỉnh sửa nhanh chóng và hiệu quả.
*   Các mục tiêu chỉnh sửa video thường như sau:
### Xoá hình ảnh hoặc âm thanh: là công việc đơn giản và phổ biến nhất trong chỉnh sửa video. Nếu có hình ảnh, đoạn âm thanh không mong muốn thì nên xoá bỏ.
### Chọn hình ảnh, âm thanh tốt nhất: Thông thường, ta luôn chụp hoặc quay nhiều cảnh hơn, ghi âm nhiều lần cùng một đoạn âm thanh và chỉ chọn cái tốt nhất khi chỉnh sửa.
# Tạo Video
*   Tạo câu chuyện: Việc sắp xếp các đối tượng là một bước quan trọng để đảm bảo video thể hiện được đúng nội dung và kịch bản câu chuyện.
*   Tạo sự hấp dẫn và cảm xúc: thêm hiệu ứng; lựa chọn và căn chỉnh màu sắc, thời gian, âm nhạc phù hợp sẽ hấp dẫn và dễ truyền được cảm xúc cho người xem. Thêm hội thoại, thuyết minh, phụ đề và tiêu đề sẽ làm nội dung video được chuyển tải rõ hơn.
## (2) Chỉnh sửa hình ảnh
*   Các thao tác chỉnh sửa hình ảnh bao gồm: chèn, xoá, thay đổi thứ tự, thay đổi khung thời gian xuất hiện ảnh. Các hiệu chỉnh này đều được thực hiện ở khung Timeline:
    *   Thêm ảnh: thực hiện như bước nhập ảnh. Khi nhập một ảnh mới thì ảnh này sẽ xuất hiện ở dòng đầu tiên trong khung Timeline.
    *   Xoá ảnh: chọn ảnh cần xoá, nháy chuột phải và chọn Delete object (hoặc chọn biểu tượng thùng rác ở cuối khung Timeline).
## Thay đổi thứ tự ảnh:
*   Chọn ảnh cần di chuyển.
*   Nhấn nút mũi tên xuống hoặc lên ở cuối khung Timeline để di chuyển ảnh đến vị trí mong muốn (Hình 1).
*   Khi các đối tượng có cùng khung thời gian thì chỉ có một đối tượng ở dòng trên cùng xuất hiện trên khung Canvas.
## Thay đổi thời gian xuất hiện ảnh:
*   **Thay đổi cả khung thời gian của ảnh:** Nháy chuột vào vùng giữa hiệu ứng xuất hiện và hiệu ứng biến mất, kéo và thả đến vị trí mong muốn.
*   **Thay đổi khung thời gian cho hiệu ứng của ảnh:** Chọn hiệu ứng của ảnh và kéo thả đến vị trí thời gian mong muốn (Hình 1).
*   Để tăng hay giảm khoảng thời gian của các hiệu ứng, trỏ chuột vào cạnh phải hoặc cạnh trái, khi chuột có hình mũi tên hai chiều thì kéo thả đến điểm thời gian mong muốn.
## Thay đổi hiệu ứng của ảnh:
*   Chọn hiệu ứng muốn thay đổi.
*   Nháy chuột phải và chọn Replace animation.
*   Chọn hiệu ứng thay thế, chọn OK.
*   Ví dụ, Ảnh10 ở Hình 1 đã thay hiệu ứng None bằng Fade In.
## Thông tin về hiệu ứng mặc định:
*   Một đối tượng khi được đưa vào dự án video sẽ có hiệu ứng xuất hiện mặc định là None và hiệu ứng biến mất là hiệu ứng biến mất của đối tượng đã được chọn trước đó.
*   Animiz cung cấp rất nhiều hiệu ứng như ở Hình 2.
## Thêm hiệu ứng xuất hiện:
*   Chọn nút (Hình 1).
*   Chọn hiệu ứng (Hình 2), chọn OK.
*   Ví dụ ở Hình 1 đã thêm hiệu ứng Aperture cho Ảnh10.
## Xoá hiệu ứng:
*   Nháy chuột phải vào hiệu ứng muốn xoá.
*   Chọn Delete animation.
## Lưu ý về hiệu ứng ảnh:
*   Với mỗi ảnh có thể thêm nhiều hiệu ứng xuất hiện.
*   Hiệu ứng được thêm sẽ xuất hiện ở bên phải hiệu ứng trước đó.
*   Chỉ có một hiệu ứng biến mất với mỗi ảnh.
## Chỉnh sửa âm thanh:
*   Biên tập âm thanh thường gồm: cắt bỏ một phần âm thanh, cắt tệp âm thanh thành nhiều đoạn rồi ghép các đoạn với nhau, căn chỉnh thời gian sao cho âm thanh khớp với hình ảnh khi hiển thị.
*   Để thực hiện biên tập âm thanh, nháy đúp chuột vào tệp âm thanh.
## Các thao tác chỉnh sửa tệp âm thanh:
*   **Chia tệp âm thanh thành nhiều đoạn:** Nháy chuột tại vị trí cần cắt (vị trí đầu đoạn và cuối đoạn) và chọn Split.
*   **Cắt bỏ một phần tệp âm thanh:** Chọn đoạn muốn xoá, chọn Delete hoặc nháy chuột tại vị trí bắt đầu xoá, kéo thả chuột đến vị trí cuối cần xoá, sau đó chọn Delete.
*   Nếu muốn khôi phục lại trạng thái trước đó, chọn Undo.
*   Sau khi chỉnh sửa xong, chọn OK.
*   **Ghép các đoạn âm thanh:** Sau khi xoá một đoạn ở giữa tệp, nếu muốn ghép các đoạn, thực hiện kéo thả các đoạn sang trái hoặc sang phải sao cho các đoạn được xếp liền với nhau.
## 4. Thêm hiệu ứng chuyển cảnh
*   Khi tạo một dự án video trong Animiz, một cảnh (scene) sẽ được tạo, các đối tượng được nhập sẽ cùng xuất hiện trong cảnh này.
*   Để thêm cảnh mới, chọn New Scene tại vùng thiết đặt cảnh và nhập các đối tượng cho cảnh video mới.
*   Một video có thể có một hoặc nhiều cảnh.
*   Mỗi cảnh gồm một chuỗi các ảnh được sắp xếp theo thứ tự để diễn tả một phần câu chuyện.
*   Các phần mềm làm video đều cho phép tạo các hiệu ứng chuyển giữa hai cảnh để các cảnh được xuất hiện một cách lôi cuốn.
*   **Cách thực hiện:** Tại vùng thiết đặt cảnh, chọn nút Add Transition giữa hai cảnh. Cửa sổ các hiệu ứng Transition Effects xuất hiện, chọn một hiệu ứng chuyển cảnh và khoảng thời gian ở ô Duration, sau đó chọn OK.
*   **Lưu ý:** Giữa hai cảnh chỉ có duy nhất một hiệu ứng chuyển cảnh. Nếu chọn hiệu ứng khác thì nó sẽ thay thế hiệu ứng cũ.
## 5. Thêm phụ đề
*   Văn bản là đối tượng được đưa vào video dưới dạng tiêu đề video, giới thiệu mở đầu hoặc kết thúc video, phụ đề hoặc các đoạn dẫn chuyển tiếp chủ đề video.
### Đưa văn bản vào video:
*   Chọn Text trên thanh đối tượng, chọn Add text.
*   Trên khung Canvas, nháy chuột vào vị trí muốn chèn văn bản, xuất hiện khung soạn thảo văn bản.
*   Nhập nội dung văn bản và định dạng văn bản với thanh công cụ ngay phía trên khung soạn thảo.
*   Chọn khung thời gian xuất hiện, các hiệu ứng cho văn bản ở khung Timeline tương tự như với hình ảnh.
## Tạo tiêu đề video:
*   Đưa văn bản vào video.
*   Chọn khung thời gian phù hợp (tại thời điểm bắt đầu của video, khoảng xuất hiện giữa các ảnh, hoặc cuối video).
## Tạo phụ đề video:
*   Chọn nút Subtitle trên khung Timeline (Hình 5), đối tượng Subtitle xuất hiện trên một dòng Timeline như ở Hình 6, chọn để thêm phụ đề.
*   Tại cửa sổ như ở Hình 7, nhập phụ đề, chọn phông chữ, cỡ chữ và màu chữ.
*   Chọn Entrance Effect và chọn hiệu ứng xuất hiện, chọn Exit Effect và chọn hiệu ứng biến mất cho phụ đề, sau đó chọn Save.
*   **Lưu ý:** Có thể tạo phụ đề bằng cách nhập văn bản như với tiêu đề video. Sau đó, chọn khung thời gian xuất hiện của phụ đề cùng với khung thời gian của hình ảnh.
## ⑥ Thực hành chỉnh sửa video
## Yêu cầu:
*   Hãy chỉnh sửa đoạn video giới thiệu cách tạo logo ở Bài 4, cụ thể như sau:
    *   Điều chỉnh khung thời gian để mỗi ảnh xuất hiện trong khoảng 20s, thời gian của bài nhạc khớp với thời gian xuất hiện của các ảnh (bài nhạc kết thúc khi ảnh cuối cùng xuất hiện xong).
    *   Tạo hiệu ứng cho các ảnh.
    *   Tạo phụ đề cho các ảnh giới thiệu bước thực hiện trong bức ảnh.
## Hướng dẫn thực hiện:
*   **Bước 1.** Mở dự án video “tao_logo.am” trong phần mềm Animiz.
*   **Bước 2.** Tại khung Timeline, chọn ảnh thứ nhất và điều chỉnh khung thời gian là 0s – 20s trên khung Timeline. Tương tự với các ảnh tiếp theo là 20s – 40s, 40s – 60s,...
*   **Bước 3.** Điều chỉnh khung thời gian cho tệp nhạc từ 0s đến 200s. Nháy đúp chuột vào tệp âm thanh ở khung Timeline để mở cửa sổ hiệu chỉnh. Nếu bài nhạc dài hơn 200s thì cắt một đoạn nào đó và xoá đi. Nếu xoá đoạn nhạc ở giữa thì sau khi xoá phải ghép liền hai đoạn nhạc lại. Ngược lại, thời gian của bài nhạc ngắn hơn 200s, cắt một đoạn nhạc và ghép thêm vào cuối bài. Thực hiện như hướng dẫn ở mục 3.
*   **Bước 4.** Thêm hiệu ứng cho ảnh: Thực hiện như hướng dẫn ở mục 2.
*   **Bước 5.** Thêm phụ đề cho ảnh: Thực hiện như hướng dẫn ở mục 5.
*   Em hãy bổ sung thêm một cảnh giới thiệu về GIMP vào dự án video trong bài thực hành. Tạo hiệu ứng chuyển cảnh cho các cảnh trong video.
*   Trong các câu sau, những câu nào đúng?
    *   a) Có thể tạo hiệu ứng xuất hiện cho âm thanh.
    *   b) Không thể thay đổi được thứ tự xuất hiện của các ảnh trong một cảnh video.
    *   c) Vị trí của các phụ đề mặc định ở phía dưới của ảnh và không thể thay đổi.
    *   d) Tiêu đề của video cũng có hiệu ứng xuất hiện giống như các hình ảnh.
## Tóm tắt bài học
*   Các phần mềm làm video ngoài chức năng dựng video còn có chức năng chỉnh sửa video.
*   Chỉnh sửa các đối tượng, tạo hiệu ứng, đưa tiêu đề và phụ đề vào video sẽ làm cho video hấp dẫn, truyền tải đầy đủ nội dung video và gây được cảm xúc cho người xem.
# BÀI 6 LÀM PHIM HOẠT HÌNH
*   **Học xong bài này, em sẽ:**
    *   Bước đầu biết cách làm phim hoạt hình đơn giản bằng phần mềm làm video.
    *   Tạo được phim hoạt hình từ ảnh, có hội thoại giữa các nhân vật và có phụ đề.
*   Em hãy quan sát một đoạn phim hoạt hình trên máy tính và cho biết nội dung cùng những đối tượng có trong đoạn phim hoạt hình đó.
## 1 Giới thiệu phim hoạt hình
*   Với phần mềm Animiz, em hãy dự đoán những bước nào trong làm phim hoạt hình sẽ được hỗ trợ bởi phần mềm.
*   Hoạt hình cho phép kể câu chuyện theo những cách độc đáo. Thế giới tưởng tượng trong các phim hoạt hình có thể tạo ra nguồn cảm hứng và sự kì diệu của những câu chuyện dù ở thời đại nào. Mỗi câu chuyện được kể khác nhau thông qua các nhân vật, đối tượng và bối cảnh được xây dựng. Các đối tượng trong phim hoạt hình là các nhân vật được vẽ và có các hoạt động (như di chuyển, hành động), bối cảnh là cảnh vật xung quanh.
*   Việc mô phỏng chuyển động bằng cách chụp ảnh các bản vẽ, mô hình liên tiếp để tạo ra ảo giác chuyển động theo một trình tự được gọi là hoạt hình. Trong hoạt hình truyền thống, hình ảnh được vẽ trên các tấm giấy celluloid trong suốt để chụp ảnh. Ngày nay, hầu hết các phim hoạt hình được làm bằng hình ảnh do máy tính tạo ra.
# Tạo Phim Hoạt Hình và Chỉnh Sửa Ảnh Động
Việc tạo phim hoạt hình bằng sử dụng phần mềm cũng tương tự như tạo video đã được trình bày ở các bài trước. Điểm khác ở phim hoạt hình là các nhân vật và bối cảnh trong phim hoạt hình không có thật, mà được tưởng tượng và vẽ ra. Diễn biến phim hoạt hình được thể hiện qua các cảnh phim, mỗi cảnh gồm các phân cảnh.
Animiz cũng là phần mềm làm phim hoạt hình 2D, hỗ trợ tạo dự án phim hoạt hình và các cảnh phim. Ngoài ra, Animiz còn có sẵn các công cụ để thiết kế và vẽ nhân vật, cảnh nền, cung cấp các mẫu video và mẫu đối tượng theo nhiều chủ đề gợi ý về ý tưởng và kịch bản cho phim hoạt hình.
# 2 Thực hành tạo phim hoạt hình
## Yêu cầu:
Sử dụng phần mềm Animiz tạo đoạn phim hoạt hình kể về một buổi lễ khai giảng năm học của trường em.
## Hướng dẫn thực hiện:
### Bước 1. Xây dựng kịch bản phim hoạt hình
Thời lượng: 30s. Kịch bản gồm các phân cảnh sau:
*   Phân cảnh 1: Hình ảnh học sinh và giáo viên chào đón năm học mới.
*   Phân cảnh 2: Phát biểu khai mạc của thầy Hiệu trưởng.
*   Phân cảnh 3: Chương trình văn nghệ chào mừng.
*   Phân cảnh 4: Kết thúc lễ khai giảng.
### Bước 2. Chuẩn bị tư liệu cho phim hoạt hình
Nhiều đối tượng trong phim hoạt hình được lấy trong video mẫu Opening Ceremony thuộc chủ đề Education.
### Phân cảnh 1:
Nhân vật các giáo viên và học sinh cầm bóng bay và khẩu hiệu chào mừng: Tại giao diện bắt đầu của Animiz, chọn chủ đề video mẫu Education, chọn video mẫu Opening Ceremony. Tại cảnh 2, chọn ảnh học sinh và giáo viên (tệp SVG), nháy chuột phải và chọn Add to My Library, điền tiêu đề và mô tả thông tin cho ảnh (nếu muốn) và chọn OK.
Nhân vật thầy chủ nhiệm lớp: Chọn mẫu nhân vật trong Roles.
Cảnh nền: Vẽ hình nền và dòng văn bản “Chào mừng năm học mới” trên Animiz.
### Phân cảnh 2:
Nhân vật thầy Hiệu trưởng được chọn là tệp ảnh SVG trong cảnh 3 của video mẫu Opening Ceremony, được lưu vào thư viện tương tự như trên.
Cảnh nền: Hình nền cảnh hội trường là tệp ảnh chọn trong cảnh 3 của video mẫu Opening Ceremony, được lưu vào thư viện tương tự như trên.
Phụ đề lời phát biểu là văn bản được tạo trong Animiz.
### Phân cảnh 3:
Nhân vật các diễn viên được chọn là các tệp ảnh động dạng SWF trong cảnh 4 của video mẫu.
Cảnh nền sân khấu được chọn là tệp ảnh ở cảnh 4 của video mẫu.
### Phân cảnh 4:
Nhân vật học sinh, giáo viên được lấy ở video mẫu, người dẫn chương trình là một mẫu nhân vật trong Roles.
Cảnh nền là cảnh nền của phân cảnh 3.
Phim hoạt hình có thể chia thành hai cảnh. Cảnh 1 gồm phân cảnh 1 và 2, cảnh 2 gồm phân cảnh 3 và 4.
### Bước 3. Tạo dự án phim hoạt hình và đưa các đối tượng vào phim hoạt hình
#### Tạo dự án phim hoạt hình:
Tại giao diện bắt đầu của Animiz, chọn New Empty Project để tạo dự án phim hoạt hình mới.
#### Đưa các đối tượng vào phim hoạt hình
##### a) Tạo cảnh 1
Đặt thời gian: Điều chỉnh khung thời gian cho cảnh 1 là 20s.
Tạo phân cảnh 1: Khung thời gian 0s – 10s.
Tạo hình nền: Tại khung Timeline chọn nút Background, tại dòng Background chọn biểu tượng tương ứng, chọn BG Color, chọn màu nền vàng như ở Hình 1.
Tạo văn bản: Chọn Text trên thanh đối tượng, chọn vị trí văn bản trên khung Canvas, nhập văn bản và căn chỉnh cỡ chữ, phông chữ, màu chữ như ở Hình 1.
Tạo nhân vật: Trên thanh đối tượng chọn My Library, chọn ảnh nhân vật và căn chỉnh vị trí và kích thước ảnh như ở Hình 1.
Tạo nhân vật thầy chủ nhiệm lớp: Trên thanh đối tượng chọn Roles, chọn Male Teacher, chọn hiệu ứng hành động Welcome, căn chỉnh vị trí và kích thước đối tượng trên khung Canvas như ở Hình 1.
Điều chỉnh khung thời gian cho các đối tượng trong khoảng thời gian 0s – 10s
Tạo phân cảnh 2: Khung thời gian 10s – 20s.
Đặt con trỏ Timeline tại vị trí điểm thời gian 10s.
Tạo hình nền: Trên thanh đối tượng, chọn My Library, chọn ảnh hội trường.
Tạo dòng văn bản “LỄ KHAI GIẢNG NĂM HỌC 2023 – 2024” trên hình nền tương tự như ở phân cảnh 1.
Tạo nhân vật thầy hiệu trưởng: Chọn hình ảnh thầy hiệu trưởng là tệp SVG trong My Library, căn chỉnh vị trí và kích thước.
Tạo phụ đề: Trên thanh đối tượng, chọn Text, nhập lần lượt nội dung các câu phát biểu. Mỗi câu phát biểu là một đối tượng trên khung Timeline.
Điều chỉnh khung thời gian cho các đối tượng trong khoảng thời gian 10s – 20s.
##### b) Tạo cảnh 2
Thêm cảnh: Tại vùng thiết đặt cảnh, chọn New Scene, chọn Blank Scene.
Đặt thời gian: Điều chỉnh khung thời gian cho cảnh 2 là 20s.
Tạo phân cảnh 3: Thực hiện tương tự như với phân cảnh 1 ở trên.
Tạo phân cảnh 4: Thực hiện tương tự như với phân cảnh 2 ở trên.
### Bước 4. Căn chỉnh thời gian xuất hiện của các nhân vật và đối tượng
Tại khung Timeline, điều chỉnh thứ tự và khung thời gian xuất hiện cho từng nhân vật, đối tượng trong mỗi phân cảnh.
Điều chỉnh hình ảnh nhóm học sinh và giáo viên (tệp SVG1 ở khung Timeline) xuất hiện từ giây thứ 12.
### Bước 5. Thêm hiệu ứng
Tại khung Timeline, chọn hiệu ứng xuất hiện và biến mất cho từng đối tượng.
Thêm hiệu ứng chuyển cảnh cho các cảnh.
### Bước 6. Tạo hành động và di chuyển cho các nhân vật
Animiz hỗ trợ cách tạo hành động cho các nhân vật như sau:
*   Đưa vào các tệp ảnh động, video dạng SWF, GIF,...
*   Cung cấp các mẫu nhân vật Roles với nhiều hiệu ứng hành động (nói, cười, lắc đầu,...).
Ví dụ ở phân cảnh 4, nhân vật ở giữa chính là một Roles với tên Female Teacher và hiệu ứng Spawl Hands.
Animiz cũng cung cấp hiệu ứng di chuyển cho các đối tượng: Chọn đối tượng cần di chuyển, nháy chuột phải và chọn Add emphasis effect, chọn Move, chọn dạng đường di chuyển, chọn OK. Trên khung Canvas, chọn vị trí xuất phát của đối tượng và hướng di chuyển theo chiều mũi tên và kéo đến vị trí đích.
### Bước 7. Thêm hội thoại và phụ đề
#### Thêm hội thoại
Thêm hội thoại cho các nhân vật bằng cách ghi âm trực tiếp trên Animiz.
Chọn phân cảnh 4, đưa con trỏ Timeline về vị trí bắt đầu hội thoại.
Chọn nút Record, chọn Start Record ① và bắt đầu ghi âm, chọn Stop Record để kết thúc ghi âm.
Chọn nút Play ① để nghe thử, có thể chọn Re-record ② để ghi âm lại, sau khi hoàn tất chọn Apply ③ để lưu thành tệp âm thanh.
#### Thêm phụ đề:
Thực hiện như hướng dẫn ở Bài 5.
### Bước 8. Lưu và xuất bản dự án phim hoạt hình
Chọn Save trên thanh công cụ, đặt tên tệp trong thư mục mong muốn, chọn Save.
Chọn Publish trên thanh công cụ để xuất bản phim hoạt hình và lựa chọn một trong các phương án sau:
*   Publish to cloud: Xuất bản video và lưu trên đám mây.
*   Video: Xuất bản video và lưu trên máy tính.
*   Gif: Lưu dự án phim hoạt hình với định dạng ảnh động GIF.
Nếu chọn Video, tiếp tục chọn nơi lưu trữ tệp, chọn định dạng tệp, chọn Publish.
Em hãy bổ sung thêm một cảnh giới thiệu về lớp học của em vào dự án phim hoạt hình trong bài thực hành. Tạo hiệu ứng chuyển cảnh cho các cảnh trong phim hoạt hình.
**Trong các câu sau, những câu nào đúng?**
a) Nên sắp xếp các phân cảnh trong phim hoạt hình theo thứ tự tuỳ ý.
b) Để tạo hành động cho các nhân vật hoạt hình trong Animiz, có thể sử dụng các hiệu ứng và các ảnh động.
c) Animiz hỗ trợ đưa ra ý tưởng kịch bản phim hoạt hình từ các video mẫu có sẵn.
d) Thiết kế các nhân vật, đối tượng cho phim hoạt hình là bước cuối cùng trong quy trình làm phim hoạt hình.
## Tóm tắt bài học
Animiz Animation Maker là phần mềm hỗ trợ làm phim hoạt hình 2D đơn giản và hấp dẫn dựa vào các mẫu video với nội dung phong phú, các mẫu nhân vật và ảnh động đa dạng.
Animiz cũng cung cấp nhiều loại đối tượng như các dạng hình học, văn bản, hình ảnh, video, ảnh động, ảnh vector, roles,... và các hiệu ứng sinh động.
## Học xong bài này, em sẽ:
Chỉnh sửa được ảnh và tạo được ảnh động bằng GIMP.
Tạo được phim hoạt hình ngắn bằng phần mềm Animz Animation Maker.
## Nhiệm vụ 1. Thực hành chỉnh sửa ảnh và tạo ảnh động
### Yêu cầu:
Hãy chọn một số bức ảnh về một chủ đề nào đó, ví dụ các ảnh chụp từ cáp treo lên đỉnh Phan Xi Păng. Sau đó, hiệu chỉnh màu sắc để có màu sắc tương đồng và tẩy xoá các chi tiết không mong đợi.
### Hướng dẫn thực hiện:
#### Công việc 1. Chỉnh sửa ảnh
##### Bước 1. Tẩy xoá chi tiết không mong đợi
Mở ảnh rồi sử dụng công cụ Clone để xoá dây cáp treo, sử dụng công cụ Healing để làm mờ vết xoá nếu có.
Xuất ảnh sang một tệp ảnh với định dạng chuẩn.
##### Bước 2. Điều chỉnh lại màu sắc cho ảnh
Thực hiện điều chỉnh màu sắc cho ảnh như sau:
Mở ảnh rồi thực hiện lệnh Colors\Curves để mở hộp thoại Curves.
Trong hộp thoại Curves, lần lượt chọn các kênh màu từ danh sách Channel rồi kéo dây cung màu đến các vị trí để giảm các màu đỏ và tăng các màu xanh.
# Thực hiện các điều chỉnh tương tự cho ảnh ở Hình 1c bằng cách giảm màu xanh và tăng màu đỏ để có kết quả như Hình 2c.
# Xuất các ảnh đã được điều chỉnh màu sang các tệp ảnh với định dạng chuẩn để sử dụng.
# Công việc 2. Tạo ảnh động
## Tạo ảnh động với hiệu ứng mờ dần từ ba ảnh đã được chỉnh sửa.
## Bước 1. Tạo tệp ảnh mới và mở các ảnh tĩnh dưới dạng các lớp ảnh
### Tạo một tệp ảnh mới với lớp nền trắng.
### Mở các tệp ảnh đã chỉnh sửa dưới dạng các lớp ảnh bằng lệnh `File\Open as Layers`.
## Bước 2. Tạo dãy khung hình cho ảnh động
### Thực hiện lệnh `Filters\Animation` và chọn `Blend` để tạo ảnh động với hiệu ứng mờ dần.
### Nhập các tham số vào hộp thoại `Script-Fu: Blend`.
#### `Intermediate frames`: Số lượng khung hình trung gian cho mỗi ảnh tĩnh.
#### `Max. blur radius`: Độ mờ tối đa giữa hai khung hình.
#### `Looped`: Chỉ định nội dung ảnh động có lặp lại hay không.
### Sau khi nháy lệnh OK, một tệp ảnh mới với các lớp ảnh biểu thị các khung hình của ảnh động được tạo ra.
### Tên các lớp ảnh có dạng "Frame n" trong đó n là số thứ tự khung hình.
### Theo ví dụ, tổng số khung hình là 12, bao gồm 3 khung hình gốc (1, 5, 9) và 9 khung hình trung gian (3 cho mỗi ảnh tĩnh).
## Bước 3. Gắn thời gian cho các khung hình
### Thực hiện lệnh `Filters\Animation\Optimize (for GIF)` để GIMP tự động tạo dãy khung hình gắn với thời gian.
### Nháy đúp chuột vào tên các khung hình 1, 5 và 9 (là các ảnh rõ nhất) để tăng thời gian hiển thị của chúng, ví dụ 500 ms.
## Bước 4. Xem trước và xuất ảnh động
### Xem trước ảnh động theo hướng dẫn ở phần tạo ảnh động với hiệu ứng tự thiết kế.
### Xuất ảnh động sang định dạng GIF để sử dụng.
# Mô tả chức năng Script-Fu: Blend
Chức năng `Script-Fu: Blend` được sử dụng để tạo hiệu ứng chuyển động mờ dần giữa các khung hình trong một ảnh động. Nó cho phép người dùng kiểm soát số lượng khung hình bổ sung được tạo ra giữa các ảnh tĩnh, mức độ mờ tối đa giữa các khung hình, và liệu ảnh động có được lặp lại hay không, từ đó tạo ra một chuyển động mượt mà và liền mạch.
# Nhiệm vụ 2. Thực hành tạo phim hoạt hình
## Yêu cầu:
### Tạo một đoạn phim hoạt hình với thời lượng khoảng 3 phút kể về một chuyến tham quan dã ngoại mà em ấn tượng nhất.
### Đoạn phim hoạt hình gồm 3 cảnh: cảnh 1 gồm một số hình ảnh về phong cảnh buổi dã ngoại, cảnh 2 có hoạt động dã ngoại của học sinh, cảnh 3 là cảnh học sinh báo cáo, thảo luận kết quả thu được sau buổi dã ngoại.
### Có chuyển cảnh giữa các cảnh.
### Cảnh 1 và 2 có nhạc nền.
### Cảnh 1 lấy một số hình ảnh được chỉnh sửa hoặc ảnh động đã tạo trong bài thực hành số 1 ở trên.
### Phần báo cáo và thảo luận ở cảnh 3 có cả hội thoại âm thanh và văn bản.
### Phim có tiêu đề, giới thiệu phần mở đầu phim và kết thúc phim.
## Hướng dẫn thực hiện:
### Bước 1. Xây dựng kịch bản phim hoạt hình:
#### Thiết kế chi tiết từng phân cảnh cho mỗi cảnh phim.
#### Trong mỗi cảnh, phác thảo chi tiết cảnh nền và các nhân vật.
### Bước 2. Chuẩn bị tư liệu cho phim hoạt hình:
#### Thiết kế nhân vật cho mỗi phân cảnh: Có thể lựa chọn các nhân vật mẫu, trong các video mẫu của Animiz. Ngoài ra, có thể vẽ các nhân vật bằng các phần mềm đồ họa như GIMP, hoặc vẽ các hình đơn giản bằng Animiz.
#### Thiết kế cảnh nền: Tạo cảnh nền trực tiếp trên Animiz hoặc trên các phần mềm đồ họa khác. Ảnh nền cũng có thể sưu tập trên Internet.
### Các bước 3, 4, 5, 6 thực hiện như hướng dẫn ở Bài 6.
### Bước 7. Thêm hội thoại và phụ đề:
#### Thêm hội thoại: Trên thanh đối tượng, đầu tiên chọn Callout, chọn hình hộp thoại rồi chỉnh vị trí, kích thước và xoay hướng phù hợp với vị trí nhân vật. Tiếp theo chọn Text, nhập văn bản hội thoại, căn chỉnh cỡ chữ và màu chữ, kéo thả đoạn văn bản vào hình hộp thoại và căn chỉnh.
#### Thêm phụ đề: Thực hiện như hướng dẫn ở Bài 5.
### Bước 8. Lưu và xuất bản dự án phim hoạt hình: Thực hiện như hướng dẫn ở Bài 6.
### Mỗi nhóm (gồm 5 bạn) hãy tạo một đoạn video về một trong các chủ đề sau:
#### a) Lễ hội Trung thu.
#### b) Hội diễn văn nghệ chào mừng ngày Nhà giáo Việt Nam.
#### c) Giới thiệu một nhân vật lịch sử được yêu thích.
#### d) Học tập trong đại dịch COVID-19.
#### e) Bảo vệ môi trường và chống biến đổi khí hậu.
# CHỦ ĐỀ FICT: GIẢI QUYẾT VẤN ĐỀ VỚI SỰ TRỢ GIÚP CỦA MÁY TÍNH THỰC HÀNH TẠO VÀ KHAI THÁC CƠ SỞ DỮ LIỆU
# BÀI 1: LÀM QUEN VỚI MICROSOFT ACCESS
# Học xong bài này, em sẽ:
## Biết được một số đặc điểm của phần mềm hệ quản trị cơ sở dữ liệu quan hệ Microsoft Access và một số thành phần chính trong cửa sổ làm việc của nó.
## Biết được một số kiểu dữ liệu trường của các bản ghi trong Microsoft Access và cách thiết lập kiểu dữ liệu trường.
## Tạo lập được một cơ sở dữ liệu đơn giản từ khuôn mẫu Microsoft Access cho trước và biết cách nhập dữ liệu vào một bảng.
# Một doanh nghiệp nhỏ cần quản lí kho hàng bằng máy tính. Theo em, nên chọn dùng phần mềm ứng dụng nào? Tại sao?
# 1 Giới thiệu Microsoft Access
## Microsoft Access (gọi tắt là Access), là phần mềm hệ quản trị CSDL phù hợp với các cơ quan, doanh nghiệp nhỏ hay người dùng cá nhân. Cửa sổ làm việc của Access có giao diện tương tự như Word, Excel và cũng áp dụng các khái niệm, cách tổ chức cùng những thao tác tương tự như các ứng dụng trong bộ phần mềm văn phòng Microsoft Office.
### a) Vùng nút lệnh
#### Ở phía trên cùng là vùng nút lệnh gồm nhiều dải lệnh nằm đè lên nhau. Các thẻ (tab) để mở các dải lệnh File, Home, Create, External Data, Database Tools,... là dải lệnh Home hay dùng nhất với các nhóm lệnh Views, Clipboard, Sort & Filter, Records.
#### Access làm thay đổi các thành phần trong vùng nút lệnh tuỳ theo ta đang làm việc với đối tượng cụ thể nào ở trong vùng làm việc. Vùng nút lệnh hiển thị sẵn sàng các nút lệnh thường dùng vào lúc ấy.
# b) Vùng điều hướng
## Vùng điều hướng hiển thị các đối tượng trong một CSDL.
## Mỗi đối tượng được thể hiện dưới dạng một biểu tượng kèm với tên của nó.
## Các ví dụ về biểu tượng đối tượng bao gồm: biểu tượng bảng, biểu tượng truy vấn, biểu tượng biểu mẫu, và biểu tượng báo cáo.
### c) Vùng làm việc
#### Nháy đúp chuột vào biểu tượng của một đối tượng trong vùng điều hướng sẽ hiển thị nội dung của đối tượng đó trong vùng làm việc.
#### Có thể mở đồng thời nhiều đối tượng trong vùng làm việc.
#### Mỗi đối tượng sẽ có một thẻ ở bên trên để hiển thị tên của nó.
#### Nháy chuột chọn thẻ sẽ làm hiển thị nội dung của đối tượng đã chọn.
#### Để đóng một đối tượng, nháy chuột vào dấu 'X' ở góc trên bên phải màn hình.
### Nhận xét và quy ước chung:
#### Thường có vài cách thao tác khác nhau để đạt được cùng một kết quả: Cách được coi là “chính thống” khi mới làm quen với phần mềm là bắt đầu từ một nút lệnh trong một dải lệnh ở vùng làm việc.
#### Quy ước trong hướng dẫn thao tác: Sẽ viết ngắn gọn cho dễ nhớ. Ví dụ, viết Create\Table... nghĩa là “nháy chuột vào thẻ Create sẽ thấy nút lệnh Table và tiếp tục nháy chuột chọn Table...”.
#### Thao tác nhanh: Khi đã quen dùng, nên ưu tiên nháy chuột phải để sử dụng bảng chọn nổi lên (context menu). Bảng chọn này cung cấp các lựa chọn thích hợp với bối cảnh lúc đó, rất tiện lợi để chọn lệnh tiếp theo.
# d) Thay đổi khung nhìn
## Một đối tượng trong CSDL Access có thể mở dưới các khung nhìn (View) khác nhau.
## Mỗi khung nhìn phục vụ tốt nhất cho một loại công việc.
## Để thay đổi khung nhìn cho một đối tượng, có thể thực hiện một trong các cách sau đây:
### Cách 1: Nháy chuột vào nút lệnh View để hiển thị danh sách chọn khung nhìn, sau đó chọn khung nhìn thích hợp.
### Cách 2: Nháy chuột vào các nút lệnh chọn khung nhìn có sẵn ở góc phải dưới của cửa sổ Access.
### Cách 3: (Dùng bảng chọn nổi lên) Nháy chuột phải lên thẻ của đối tượng đang mở và chọn khung nhìn thích hợp.
# 2) Cơ sở dữ liệu trong Access
## Một CSDL Access được lưu trong máy tính thành một tệp có đuôi tên tệp là “.accdb”.
## Mỗi cửa sổ Access làm việc với một CSDL.
## Có thể tạo một CSDL mới trong Access bằng hai cách khác nhau: từ khuôn mẫu cho trước hoặc từ CSDL trống (Blank Database).
## Đối với CSDL trống, ta phải tự làm tất cả các công việc như: tạo từng bảng theo thiết kế, nhập dữ liệu và xây dựng các biểu mẫu, báo cáo, truy vấn,...
## Nếu sử dụng khuôn mẫu, Access giúp ta rất nhiều vì đã làm sẵn một số khung bảng, biểu mẫu, báo cáo,...
## Nói “khung” hàm ý chưa có dữ liệu. Chỉ cần nhập dữ liệu là CSDL đã sẵn sàng để sử dụng.
## Nếu thấy những điểm chưa hoàn toàn phù hợp với nhu cầu sử dụng, có thể chỉnh sửa thiết kế các khung bảng, biểu mẫu, báo cáo,... theo ý muốn.
## Access đã làm sẵn khá nhiều khuôn mẫu để lựa chọn.
# 3) Tạo mới cơ sở dữ liệu
## a) Tạo cơ sở dữ liệu mới từ Blank database
### Bước 1. Khởi chạy Access, chọn New hoặc từ cửa sổ làm việc của Access, chọn File\New.
# Bước 2. Nháy chuột chọn Blank desktop database, một cửa sổ Access mở ra.
# Bước 3. Đổi tên tệp thay cho tên mặc định ở ô File Name và xác định thư mục nơi chứa tệp CSDL. Sau đó nhấn Create.
# b) Tạo CSDL từ khuôn mẫu
## Tạo mới một CSDL từ khuôn mẫu chỉ khác tạo CSDL trống ở Bước 2. Thay vì chọn Blank desktop database, cần tìm và chọn khuôn mẫu mong muốn trước khi thực hiện Bước 3. Chi tiết Bước 2 như sau:
### Nếu thấy khuôn mẫu mong muốn, nháy chọn nó; một cửa sổ Access sẽ mở, thực hiện tiếp Bước 3 như Mục a.
### Nếu chưa nhìn thấy khuôn mẫu mong muốn trên máy tính của mình, cần tìm kiếm nó bằng cách sử dụng ô tìm kiếm (Search for online templates). Sau đó chọn tải về và mở ra.
# ④ Bảng và các kiểu dữ liệu cột
## Có hai khung nhìn bảng là khung nhìn thiết kế (Design View) và khung nhìn bảng dữ liệu (Datasheet View).
## Trong khung nhìn bảng dữ liệu, mỗi bản ghi là một hàng trong bảng, mỗi cột trong bảng là một trường của bản ghi, chứa dữ liệu thuộc một kiểu nào đó. Mỗi kiểu dữ liệu có các thuộc tính nhất định. Cần thiết lập kiểu dữ liệu cho mỗi cột trong bảng phù hợp với thực tế và mục đích sử dụng.
# ⑤ Hướng dẫn thao tác khám phá trong khung nhìn thiết kế bảng
## a) Các cột trong bảng
### Access luôn mặc định thiết kế trường dữ liệu đầu tiên tên là ID và có kiểu dữ liệu là AutoNumber. Access mặc định chọn trường ID là khoá chính của bảng và hiển thị biểu tượng chìa khoá tại đầu mút trái cạnh tên trường. Sau này, ta có thể chọn trường khác làm khoá chính, theo đúng thiết kế thay cho trường ID mặc định.
### Mở bảng Students trong khung nhìn thiết kế để thao tác khám phá. Khung nhìn thiết kế bảng chia làm hai phần. Nữa trên là danh sách tên trường (Field Name) kèm kiểu dữ liệu (Data Type). Nháy chuột chọn Data Type cụ thể cho một trường thì nữa dưới hiển thị các thuộc tính chi tiết hơn của kiểu dữ liệu trong trường đó, gọi là thuộc tính trường (Field Properties). minh họa các thuộc tính chi tiết của trường Date of Birth.
# Thao tác thiết kế các cột trong bảng
## Nháy chuột vào ô vuông đầu mút trái cạnh tên trường sẽ đánh dấu chọn cả hàng ngang (tức là cột có tên đó trong bảng dữ liệu).
## Sau khi đã chọn, có thể:
### Xóa hay chèn thêm trường mới kế bên: Dùng nút lệnh Delete Rows hay Insert Rows trong vùng nút lệnh.
### Đặt làm trường khóa chính của bảng hay gỡ bỏ không còn là khóa chính bằng nút lệnh Primary Key hình chìa khóa trong vùng nút lệnh.
### Mẹo: Nháy chuột phải vào ô vuông đầu mút trái cạnh tên trường sẽ xuất hiện bảng chọn nổi lên với các lệnh tương tự.
## Nháy chuột vào tên trường để gõ nhập tên mới nếu muốn đổi tên.
# Thực hành làm quen với Microsoft Access
## Nhiệm vụ 1. Tạo CSDL bằng khuôn mẫu
### Tạo một CSDL theo mẫu *Students*. Mở bảng *Students* và chuyển sang khung nhìn thiết kế.
### Thử ghi lưu CSDL vừa tạo ở câu a) về máy tính cá nhân với một tên tùy ý.
## Nhiệm vụ 2. Khám phá biểu mẫu và thử nhập dữ liệu từ biểu mẫu
### Mở biểu mẫu *Student List*, chuyển sang khung nhìn **Form View** (nếu cần thiết).
### Nhập dữ liệu tuỳ ý cho vài bản ghi và một vài trường:
#### Trường với kiểu dữ liệu *Date/Time*, chú ý cách Access hỗ trợ dùng lịch để chọn ngày tháng.
#### Trường *Level*, chú ý biểu mẫu sẽ thả xuống danh sách để chọn.
### Mở bảng *Students* để xem kết quả nhập dữ liệu.
## Nhiệm vụ 3. Xem các thuộc tính chi tiết của một cột
### Mở bảng *Students* trong khung nhìn thiết kế, chú ý vùng *Field Properties* hiển thị các thuộc tính chi tiết hơn.
### Nháy chuột vào *Data Type* của trường *Student ID* và xem các thuộc tính.
### Làm tương tự với trường *Data of Birth*.
## Nhiệm vụ 4. Khám phá các thao tác thiết kế cột trong khung nhìn thiết kế bảng *Students*
### Thử xoá một trường, ví dụ *Company, Room,...*
### Thử chèn thêm một trường mới vào chỗ vừa xoá bớt xong.
### Thử đổi tên một vài trường, ví dụ *First Name* thành *Tên*, *Last Name* thành *Họ*; đổi tên trường có kiểu dữ liệu *Date/Time* thành *Ngày sinh*.
## Theo em, khi nào nên tạo mới một CSDL Access từ khuôn mẫu có sẵn?
## Câu 1. Vùng điều hướng trong cửa sổ làm việc của Access hiển thị những gì?
## Câu 2. Có thể mở bảng CSDL dưới những khung nhìn nào?
## Câu 3. Khung nhìn thiết kế bảng gồm mấy phần? Từng phần hiển thị những gì?
# Tóm tắt bài học
## Có thể mở một bảng (biểu mẫu, truy vấn, báo cáo) dưới các khung nhìn khác nhau trong vùng làm việc của Access tuỳ theo việc ta muốn làm.
## Khung nhìn thiết kế bảng chia làm hai phần: nửa trên là danh sách tên trường (*Field Name*) kèm kiểu dữ liệu (*Data Type*), nửa dưới hiển thị các thuộc tính chi tiết của trường ta đang thiết kế, chỉnh sửa.
# BÀI 2 TẠO BẢNG TRONG CƠ SỞ DỮ LIỆU
# Học xong bài này, em sẽ:
## Biết được cách tạo bảng theo thiết kế.
## Biết được sơ bộ cách thiết lập một số thuộc tính kiểu dữ liệu thường dùng.
## Tạo được một số bảng CSDL.
# Thư viện trường em lưu trữ những gì và hàng ngày phục vụ những ai?
# Các bảng trong cơ sở dữ liệu thư viện trường
## Các cột trong bảng
## Một bảng CSDL có nhiều cột. Mỗi cột chứa dữ liệu thuộc một kiểu nhất định. Cần thiết lập kiểu dữ liệu cho mỗi cột trong bảng phù hợp với thực tế và mục đích sử dụng. *(Bảng 1. Một số kiểu dữ liệu thường dùng trong Access đã được bỏ qua theo quy tắc xử lý)*
# Thiết kế các bảng
## Trong tin học, logic nghiệp vụ (Business Logic) hàm ý các quy tắc nghiệp vụ trong thế giới thực và người thiết kế CSDL cần dựa vào đó xác định cách thu thập, lưu trữ và thao tác dữ liệu.
## Hoạt động hằng ngày của thư viện trường liên quan đến kho sách, đến bạn đọc là các học sinh trong trường, đến các giao dịch mượn, trả sách. CSDL thư viện đơn giản nhất gồm 3 bảng tương ứng: Sách, Bạn Đọc, Mượn-Trả sách.
## Bảng Mượn-Trả là bảng nối, một kiểu bảng riêng, sẽ được thiết kế sau. Dưới đây trình bày chi tiết về bảng Sách và bảng Bạn Đọc.
## Bảng Sách gồm các cột và kiểu dữ liệu tương ứng, ví dụ như Bảng 2 sau đây:
## Có thể thêm một số cột nữa cho bảng Sách tuỳ theo yêu cầu quản lí và quy mô kho sách. Ví dụ: ngày nhập kho sách; phân loại sách giáo khoa, sách hỗ trợ học tập và giảng dạy (sách bài tập, sách giáo viên,...). Với mục đích minh hoạ, ta thêm cột Loại sách, phân loại sách Tin học “TH” và còn lại là sách “Khác” (Hình 1).
## Bảng Bạn Đọc gồm các cột và kiểu dữ liệu tương ứng, ví dụ như Bảng 3.
## Hình 2 minh hoạ bảng Bạn Đọc với một số bản ghi.
## Có thể thêm một số cột nữa cho bảng Bạn Đọc tuỳ theo yêu cầu quản lí và quy mô tập thể bạn đọc.
### Ví dụ (về các cột có thể thêm): ngày bắt đầu trở thành bạn đọc; là học sinh, giáo viên hay cán bộ nhà trường;...
## Để phân biệt đối tượng bạn đọc, có thể sử dụng mã số thẻ bạn đọc.
### Ví dụ (về mã số thẻ): số thẻ bắt đầu bằng “HS-” nghĩa là học sinh, bắt đầu bằng “GV-” nghĩa là giáo viên.
## Tương tự, có thể sử dụng mã số sách để phân loại sách.
## Cách làm này thích hợp cho thư viện quy mô nhỏ và dễ nhận biết, dễ nhớ với con người.
## Với thư viện quy mô lớn, có yêu cầu quản lí nâng cao hơn và dịch vụ phong phú hơn cần xử lí bằng máy tính thì sẽ có những bất tiện.
## Việc trích lấy ra các thông tin
## Phân tích dữ liệu phức tạp: Khi phân tích số liệu thống kê theo đối tượng bạn đọc và phân loại sách bằng mã số "ngầm", việc này trở nên phức tạp. Giải pháp là thêm cột "Phân loại" và mã hóa rõ ràng cách phân loại.
## Hướng dẫn tạo bảng theo thiết kế:
### CSDL trống mới tạo: Sẽ có sẵn một bảng tên là `Table1` theo mặc định.
### CSDL đang làm việc: Nháy chuột chọn `Create\Table` để tạo thêm một bảng mới cũng tên là `Table1`.
### Đổi tên bảng: Access sẽ yêu cầu đổi tên `Table1` thành tên mới khi lưu, hoặc có thể gõ tên mới trước khi nháy lệnh `Create`. Nên chọn tên gợi nhớ nội dung bảng.
## Thiết lập kiểu dữ liệu cho mỗi trường và các thuộc tính chi tiết:
### Mở bảng trong khung nhìn thiết kế và nhập lần lượt các tên trường vào cột `Field Name`.
### Giữ nguyên cột `ID` do Access tự động tạo.
### Cột `Data Type` dùng để chọn kiểu dữ liệu của trường.
#### Bước 1: Nháy chuột vào ô tên kiểu dữ liệu (cột `Data Type`), nháy dấu trỏ xuống ở đầu mút phải để thả xuống danh sách các kiểu dữ liệu.
#### Bước 2: Chọn một kiểu dữ liệu (bằng tiếng Anh) thích hợp trong danh sách.
### Vùng Field Properties: Nằm bên dưới để xác định chi tiết các thuộc tính của kiểu dữ liệu đã chọn. Cột đầu tiên là danh sách tên thuộc tính như: `Field Size`, `Format`, `Input Mask`,... Cột kế tiếp xác định giá trị cụ thể của thuộc tính.
#### Bước 3: Thiết lập các chi tiết thuộc tính của trường đã chọn:
##### Nháy chuột chọn một thuộc tính (một dòng), sẽ xuất hiện dấu trỏ xuống ở đầu mút phải.
##### Nháy dấu trỏ xuống để thả danh sách chọn thiết lập chi tiết cho thuộc tính đó.
# Thuộc tính cho trường khóa chính
*   Các trường `Mã sách`, `Số thẻ` dự kiến làm khóa chính trong các bảng tương ứng.
*   Theo mặc định, trường khóa chính sẽ có các thuộc tính: `Required: Yes; Indexed: Yes (No Duplicates)`.
## Thuộc tính Indexed
*   Thuộc tính `Indexed` (được lập chỉ mục) giúp tìm kiếm nhanh hơn.
*   Khi tìm kiếm bạn đọc theo tên, với cột `Tên` trong bảng `Bạn Đọc`, nên xác định thuộc tính `Indexed`.
*   Nếu có thể xảy ra việc hai người trùng tên, phải chọn `Indexed: Yes (Duplicates OK)`.
## Thuộc tính Format
*   Cần xác định thuộc tính `Format` của trường để hiển thị dữ liệu dưới dạng quen thuộc, dễ xem và dễ gõ nhập dữ liệu mới.
*   Ví dụ, trường `Ngày sinh` trong bảng `Bạn Đọc` với kiểu dữ liệu `Date/Time` có các lựa chọn: `General Date`, `Long Date`, `Medium Date`, `Short Date`. Hãy chọn định dạng phù hợp.
# Gõ nhập dữ liệu vào bảng để kiểm tra thiết kế
*   Sau khi thiết kế xong bảng, ghi lưu và chuyển về khung nhìn bảng dữ liệu, ta có thể bắt đầu nhập dữ liệu vào bảng.
*   Việc gõ nhập dữ liệu được thực hiện theo từng ô. Access tự động lưu kết quả nhập dữ liệu khi kết thúc một bản ghi và chuyển sang bản ghi tiếp theo, không cần nháy chuột vào biểu tượng Save.
*   **Chú ý:** Trong thực tế, người ta thường thiết kế để nhập dữ liệu cho CSDL qua biểu mẫu để kiểm soát một số ràng buộc dữ liệu.
# Chuyển quan hệ “nhiều – nhiều” thành quan hệ “một – nhiều”
*   Nhật kí giao dịch hằng ngày phản ánh mối quan hệ giữa hai (hoặc nhiều) đối tượng liên quan trong hoạt động kinh doanh hay dịch vụ.
*   Thư viện cần ghi lại các giao dịch mượn trả sách trong một thời gian, ví dụ một năm học. Thực tế cho thấy mỗi học sinh đã từng mượn nhiều cuốn sách và mỗi cuốn sách đã từng được nhiều học sinh mượn. Đây là quan hệ nhiều – nhiều (∞ – ∞).
*   Trong Access nói riêng và CSDL quan hệ nói chung giữa hai bảng chỉ có mối quan hệ một – một (1 – 1) hoặc một – nhiều (1 – ∞).
*   Ta tạo bảng thứ ba đặt tên là *Mượn-Trả*, là bảng nối giữa *Bạn Đọc* và *Sách* để chuyển quan hệ ∞ – ∞ thành hai quan hệ 1 – ∞.
*   Trong bảng nối sẽ có hai cột ứng với hai khoá chính của bảng *Bạn Đọc* và bảng *Sách*. Đó là các khoá ngoại.
*   Tuỳ theo yêu cầu sử dụng, có thể thêm cột cho bảng *Mượn-Trả*.
# Thực hành tạo bảng trong CSDL
## Nhiệm vụ 1. Tạo bảng Sách theo thiết kế và thử nhập dữ liệu
*   Tạo bảng mới. Mở bảng trong khung nhìn thiết kế, giữ nguyên trường *ID*, thêm các trường mới và xác định kiểu dữ liệu, thiết lập thuộc tính của trường dữ liệu.
*   b) Chuyển sang khung nhìn bảng dữ liệu, nhập dữ liệu cho một vài cột, vài hàng.
*   c) Chuyển sang khung nhìn thiết kế; bỏ chọn khoá chính là ID; chọn Mã sách làm khoá chính; ghi lưu thay đổi thiết kế.
*   **Chú ý:** Kiểu dữ liệu Number cho cột Số trang nên được xác định chi tiết hơn: Field Size là Integer. Nên hạn chế độ dài một số trường kiểu Short text, ví dụ hạn chế độ dài Mã sách: 15; Tác giả: 127.
## Nhiệm vụ 2. Tạo bảng Bạn Đọc theo thiết kế và thử nhập dữ liệu
*   Các bước thực hành tương tự như Bài 1.
*   **Chú ý:**
    1) Nên hạn chế độ dài một số trường kiểu Short text, ví dụ hạn chế độ dài Số thẻ, Mã học sinh: 15; Họ và đệm: 63; Tên: 15.
    2) Chọn Số thẻ làm khoá chính của bảng thay cho trường ID mặc định.
    3) Cột Tên nên chọn thuộc tính Indexed là “Yes (Duplicates OK)”.
    4) Cột Ngày sinh nên chọn thuộc tính Format phù hợp, ví dụ Short Date.
    5) Nhập một số bạn đọc không là học sinh, ví dụ có Số thẻ bắt đầu bằng “GV”.
# Câu hỏi
## Câu 1.
Học sinh là trung tâm của hoạt động giáo dục trong nhà trường. Em hãy thiết kế bảng dữ liệu Học sinh cho CSDL của trường em.
## Câu 2.
Theo em, trong bảng Bạn đọc, những trường dữ liệu nào hoàn toàn giống như trong bảng Học sinh.
# Bài tập
## Câu 1.
Để tạo một bảng mới cần thao tác như thế nào?
## Câu 2.
Để tạo cột và xác định kiểu dữ liệu cho cột cần thao tác như thế nào?
## Câu 3.
Để chọn một cột làm khoá chính cần làm gì?
# Tóm tắt bài học
*   Các việc cần làm sau khi tạo bảng mới:
    *   Mở khung nhìn thiết kế để nhập các tên cột, chọn kiểu dữ liệu cho cột.
    *   Xác định một số thuộc tính chi tiết quan trọng của cột trong trường hợp cần thiết: Field Size, Required, Indexed và Yes/No Duplicates,...
    *   Chọn cột làm khoá chính của bảng.
    *   Chuyển sang khung nhìn bảng dữ liệu và thử nhập dữ liệu để kiểm tra.
# BÀI 3 LIÊN KẾT CÁC BẢNG TRONG CƠ SỞ DỮ LIỆU
# Mục tiêu
*   **Học xong bài này, em sẽ:**
    *   Biết được cách thiết lập đúng đắn mối quan hệ giữa các bảng trong một CSDL để kết nối dữ liệu giữa hai bản ghi từ hai bảng.
    *   Tạo được CSDL có nhiều bảng.
    *   Thiết lập được quan hệ giữa các bảng.
    *   Khi một bạn đọc mượn sách, thủ thư cần ghi lại những thông tin gì? Có một bảng nào trong CSDL chứa đầy đủ những thông tin này hay không?
# Thiết lập mối quan hệ giữa hai bảng
## Các lựa chọn kết nối dữ liệu
*   **a) Các lựa chọn kết nối dữ liệu**
    *   Thiết lập mối quan hệ giữa hai bảng nhằm mục đích nối (join) dữ liệu giữa hai bản ghi tương ứng trong mỗi bảng. Access sẽ so khớp giá trị của hai trường được liên kết khi truy vấn dữ liệu hay kiểm tra hợp lệ khi nhập dữ liệu. Ví dụ, không thể có một người mượn mà chưa có thẻ thư viện; không thể mượn cuốn sách còn chưa có trong kho sách.
    *   Quan hệ 1 – ∞ phổ biến nhất giữa hai bảng có ba lựa chọn thuộc tính của phép nối dữ liệu (Join Properties). Khi truy vấn lấy dữ liệu có yêu cầu nối các bản ghi từ hai bảng thì trong số các bản ghi đã thoả mãn điều kiện cần biết cách “nối” cụ thể.
    *   1: Chỉ nối các bản ghi nếu các giá trị trường được kết nối trùng khớp nhau. Đây là phép nối trong (Inner join).
    *   2: Lấy tất cả các bản ghi trong bảng bên trái nhưng chỉ nối với các bản ghi của bảng bên phải khớp giá trị trong trường được kết nối. Đây là phép nối ngoài bên trái (Left outer join).
*   **Phép nối ngoại bên phải (Right outer join):** Lấy tất cả các bản ghi trong bảng bên phải nhưng chỉ nối với các bản ghi của bảng bên trái khớp giá trị trong trường được kết nối.
*   Access đánh dấu lựa chọn 1 theo mặc định.
## Thao tác thiết lập, chỉnh sửa, xoá mối quan hệ giữa hai bảng:
*   Chọn `Database Tools\Relationships` để mở vùng làm việc với các mối quan hệ.
*   Access hiển thị trực quan mối quan hệ giữa hai bảng bằng một đoạn thẳng nối hai bảng, ghi kèm các cặp số 1 – 1 hay 1 – ∞ ở hai đầu đoạn nối nếu đã được thiết lập rõ ràng.
*   Chú ý rằng một bảng có thể liên kết với nhiều bảng khác.
## Quy trình thiết lập mối quan hệ giữa hai bảng:
### Bước 1. Đưa hộp thể hiện mỗi bảng vào vùng làm việc với các mối quan hệ (nếu trong đó còn chưa nhìn thấy bảng ta muốn):
*   Nháy nút lệnh `Show Table`. Hộp thoại `Show Table` xuất hiện.
*   Nháy đúp chuột lên tên bảng: Hộp thể hiện bảng sẽ xuất hiện.
### Bước 2. Tạo quan hệ giữa hai bảng:
*   Kéo thả chuột từ trường khoá ngoại trong bảng con vào trường khoá chính trong bảng mẹ; hộp thoại `Edit Relationships` xuất hiện.
*   Đánh dấu hộp kiểm `Enforce Referential Integrity` (đảm bảo toàn vẹn tham chiếu) và chọn `Create` hay `OK`.
### Bước 3. Xác định các lựa chọn liên kết dữ liệu:
*   Nháy nút Join Type để mở hộp thoại Join Properties (nếu chưa xuất hiện) để chọn thuộc tính cho phép nối dữ liệu thực thi mối quan hệ này.
*   Để nguyên như mặc định hoặc đánh dấu chọn thuộc tính kết nối đúng yêu cầu.
## Chỉnh sửa mối quan hệ:
*   Chọn mối quan hệ bằng cách nháy chuột lên đường nối hai bảng.
*   Nháy nút lệnh Edit Relationship.
## Xóa mối quan hệ:
*   Nháy chuột chọn mối quan hệ, nhấn phím Delete.
*   Chú ý: Nháy chuột phải lên đường nối hai bảng cũng xuất hiện bảng chọn nối lên có hai lệnh Edit Relationship và Delete.
## Cột dữ liệu từ tra cứu:
*   Sử dụng cột dữ liệu từ tra cứu giúp người dùng có thể chọn mục dữ liệu từ một danh sách thay cho gõ nhập.
*   Việc nhập dữ liệu sẽ nhanh hơn và đảm bảo toàn vẹn tham chiếu.
## Hướng dẫn thao tác:
*   Access có trình tiện ích Lookup Wizard giúp thiết lập mối quan hệ khoá ngoài và khoá chính giữa hai bảng (quan hệ ∞ – 1) để cho phép nhập dữ liệu bằng cách chọn từ danh sách thả xuống.
*   Ta sẽ thiết lập cột Số thẻ trong bảng Mượn-Trả thành cột dữ liệu từ tra cứu.
*   Mở bảng Mượn-Trả trong khung nhìn thiết kế.
*   Thiết lập lại Data Type của trường Số thẻ: Nháy dấu trỏ xuống để thả xuống danh sách chọn.
*   Nháy chọn Lookup Wizard (ở dòng cuối cùng) sẽ làm xuất hiện một loạt hộp thoại để đánh dấu các lựa chọn.
*   Hộp thoại thứ nhất: Đánh dấu chọn “I want the lookup field to get the values from another table or query”; chọn Next.
## Hộp thoại thứ hai (Hình 4b):
*   Chọn bảng hay truy vấn làm nguồn để tra cứu dữ liệu.
*   Trong ví dụ này, đánh dấu chọn bảng Bạn Đọc; chọn Next.
## Hộp thoại thứ ba (Hình 4c):
*   Chọn các trường dữ liệu trong bảng (hay truy vấn) vừa chọn.
*   Trong ví dụ này, đánh dấu chọn trường Số thẻ (của bảng Bạn Đọc).
*   Nháy dấu mũi tên “>” để chuyển nó sang Selected Fields; chọn Next.
# Hộp thoại thứ tư:
*   Chọn trường muốn sắp xếp để tiện tra cứu.
*   Trong ví dụ này, đó vẫn là trường Số thẻ vừa chọn; chọn trường Số thẻ và chọn Next.
# Hộp thoại thứ năm (Hình 4d):
*   Đặt tên cho trường lookup.
*   Giữ nguyên tên là Số thẻ; chọn Finish.
# Quan sát kết quả:
*   Mở bảng trong khung nhìn bảng dữ liệu sẽ thấy có mũi tên trỏ xuống khi chọn ô để nhập dữ liệu cho trường Số thẻ.
*   Từ đây thay vì gõ nhập có thể chọn từ danh sách tra cứu.
# Thiết lập đảm bảo toàn vẹn tham chiếu:
*   Nháy chọn Database Tools\Relationships sẽ thấy có đường nối giữa hai bảng Bạn đọc và Mượn-Trả hiển thị trực quan mối quan hệ tra cứu vừa thiết lập.
*   Nháy chuột phải lên đường nối này; hộp thoại Edit Relationships xuất hiện.
*   Đánh dấu hộp kiểm Enforce Referential Integrity và chọn OK.
# Thực hành tạo liên kết giữa các bảng trong CSDL
## Nhiệm vụ 1. Tạo bảng Mượn-Trả theo thiết kế và thử nhập dữ liệu
*   Các bước tạo bảng tương tự như trong bài học trước.
    *Chú ý:*
    *   Vẫn dùng khoá chính là ID như Access đã chọn mặc định.
    *   Các cột *Ngày mượn, Ngày Trả* nên chọn thuộc tính *Format* phù hợp, ví dụ *Short Date*.
    *   Nên hạn chế độ dài của các trường *Số thẻ, Mã sách* giống như ở các bảng *Bạn Đọc, bảng Sách*.
## Nhiệm vụ 2. Thiết lập mối quan hệ và xác định thuộc tính kết nối dữ liệu giữa các bảng
*   1) Thiết lập mối quan hệ 1 – ∞ từ bảng *Sách* và từ bảng *Bạn Đọc* tới bảng *Mượn-Trả* theo hướng dẫn trong mục “Thao tác thiết lập, chỉnh sửa, xoá mối quan hệ giữa hai bảng”.
*   2) Thiết lập cột *Số thẻ* và cột *Mã sách* thành kiểu dữ liệu tra cứu.
    *Chú ý:* Có thể phải xoá kết quả của yêu cầu 1 và sau đó thiết lập lại thành cột tra cứu.
*   **Theo em, nếu như CSDL của trường có bảng Học sinh và đã thiết lập quan hệ 1 – 1 giữa hai bảng Bạn Đọc và Học sinh thì có thể thiết lập kiểu dữ liệu tra cứu để không phải gõ nhập lại dữ liệu những cột nào trong bảng Bạn Đọc.**
## Câu hỏi:
*   Câu 1. Cần mở cửa sổ làm việc nào để thiết lập, chỉnh sửa mối quan hệ giữa các bảng CSDL?
*   Câu 2. Để thiết lập kiểu dữ liệu từ tra cứu cần thao tác như thế nào?
## Tóm tắt bài học
*   Các thao tác thiết lập, chỉnh sửa, xoá mối quan hệ giữa hai bảng trong CSDL bắt đầu bằng chọn Database Tools\Relationships để mở vùng làm việc với các mối quan hệ.
*   Thiết lập kiểu dữ liệu từ tra cứu sẽ đảm bảo toàn vẹn tham chiếu.
*   Kéo thả trường khoá ngoài của bảng con vào trường khoá chính của bảng mẹ để tạo quan hệ giữa hai bảng.
*   Chọn thuộc tính cho phép nối dữ liệu trong hộp thoại Join Properties.
# BÀI 4: TẠO VÀ SỬ DỤNG BIỂU MẪU
*   **Học xong bài này, em sẽ:**
    *   Phân biệt được “có kết buộc với bảng CSDL” và “không kết buộc”.
    *   Tạo được một số loại biểu mẫu thường dùng nhất.
    *   Sử dụng được biểu mẫu để nhập dữ liệu.
*   **Thảo luận:** Em hãy kể một loại biểu mẫu điền thông tin mà em biết, nó gồm có những mục gì? Một số mục có một (hay vài) ô vuông để đánh dấu chọn, vì sao có mẫu như thế?
## 1. Tạo biểu mẫu trong Access
### a) Các loại biểu mẫu
#### Biểu mẫu một bản ghi và biểu mẫu nhiều bản ghi
*   **Biểu mẫu một bản ghi:** Tại một thời điểm, nó hiển thị một bản ghi, tức là một hàng trong bảng CSDL. Trong ứng dụng thực tế, biểu mẫu này dùng để nhập hay hiển thị thông tin về một cá thể: một người, một mục hàng trong đơn hàng,... Thông thường, các tên trường ở bên trái và ô để nhập, hiển thị dữ liệu kế bên phải.
*   **Biểu mẫu nhiều bản ghi:** Hiển thị nhiều bản ghi cùng một lúc, mỗi bản ghi trên một hàng ngang, các trường là các cột, nhìn tương tự như một phần của bảng dữ liệu.
#### Biểu mẫu tách đôi
*   Vùng hiển thị biểu mẫu được chia thành hai nửa, theo chiều dọc hoặc chiều ngang.
*   Ví dụ, nửa trên hiển thị các trường của một bản ghi dưới dạng biểu mẫu tờ khai quen thuộc. Nửa dưới hiển thị nội dung của nhiều bản ghi.
*   Một kiểu biểu mẫu khác cũng tách đôi thành hai nửa nhưng nó thể hiện quan hệ 1 – ∞ giữa hai bảng. Ví dụ, hiển thị thông tin về một bạn đọc và một số lần mượn trả sách của bạn đọc đó.
*   **Biểu mẫu có kết buộc với bảng CSDL và biểu mẫu không kết buộc**
    *   **Biểu mẫu có kết buộc (bound):** Các mục dữ liệu hiển thị trong biểu mẫu kết buộc trực tiếp với các trường trong bảng CSDL và làm thay đổi dữ liệu của trường khi gõ nhập. Phải là biểu mẫu có kết buộc thì mới có thể dùng để nhập, chỉnh sửa, xem dữ liệu,... Các mục sau chủ yếu trình bày về biểu mẫu có kết buộc.
    *   **Biểu mẫu không kết buộc (unbound):** Đối lập với biểu mẫu có kết buộc, biểu mẫu không kết buộc không dùng để nhập, chỉnh sửa dữ liệu.
    *   **Tạo biểu mẫu**
    *   **Hướng dẫn tạo nhanh một số biểu mẫu có kết buộc với một bảng**
        *   Nhóm lệnh Forms có các nút lệnh để tạo nhanh một biểu mẫu và sau đó sử dụng ngay được.
        *   Sau khi đánh dấu chọn một bảng hay truy vấn trong vùng điều hướng, Access sẽ hiểu là bước tiếp theo ta cần sử dụng bảng (truy vấn) đó làm nguồn dữ liệu cho biểu mẫu.
        *   **Tạo biểu mẫu một bản ghi**
            *   **Bước 1:** Nháy chuột chọn Create\Form sẽ tạo biểu mẫu một bản ghi gồm tất cả các trường. Access tự động đặt một tên tạm dựa trên tên bảng.
            *   **Bước 2:** Sửa lại tên biểu mẫu (nếu cần) trước khi ghi lưu. Nên đặt tên gợi nhớ nội dung biểu mẫu là gì.
            *   Sau khi đặt tên và ghi lưu, biểu tượng biểu mẫu kèm tên sẽ xuất hiện trong vùng điều hướng. Ta có thể mở để chỉnh sửa thiết kế hay sử dụng bất kì lúc nào.
        *   **Tạo biểu mẫu nhiều bản ghi**
            *   **Bước 1:** Nháy chuột chọn Create\More Forms sẽ thả xuống một danh sách chọn.
            *   Chọn **Multiples Items** sẽ tạo ra một biểu mẫu nhiều bản ghi.
            *   Chọn **DataSheet** cũng tạo ra một biểu mẫu nhiều bản ghi nhưng có dạng như khung nhìn bảng dữ liệu.
            *   Chọn **Split Form** sẽ tạo ra biểu mẫu tách đôi.
*   **Bước 2. Tương tự như Bước 2 khi tạo biểu mẫu một bản ghi.**
*   **Hướng dẫn tạo biểu mẫu bằng Form Wizard**
    *   Tạo nhanh biểu mẫu bằng nút lệnh Form hay More Forms rất dễ nhưng không có các lựa chọn tuỳ biến, ví dụ chỉ chọn một số trường nào đó, chọn các bản ghi từ hai bảng,...
    *   Cách làm tốt hơn là sử dụng tiện ích tạo biểu mẫu Form Wizard hỗ trợ làm biểu mẫu có tuỳ biến rất thuận tiện.
    *   **Tạo biểu mẫu một bản ghi**
    *   Sau khi khởi chạy tiện ích tạo biểu mẫu bằng cách chọn Create\Form Wizard, thực hiện quy trình 3 bước chính như sau:
        *   **Bước 1. Chọn các trường dữ liệu.** Hộp thoại đầu tiên mở ra để chọn các trường dữ liệu sẽ hiển thị trên biểu mẫu. Các trường này có thể lấy từ các bảng hoặc truy vấn. Thao tác tương tự như nhau:
            1. Từ danh sách thả xuống Tables\Queries cần chọn tên bảng/truy vấn. Danh sách các trường có sẵn Available Fields hiển thị trong khoang dưới.
            2. Chọn tên trường, nháy dấu ">" để chuyển sang hộp thoại Selected Fields.
            3. Có thể nháy vào dấu ">>" để di chuyển tất cả các trường cùng lúc.
            4. Nháy Next khi đã chọn xong tất cả các trường dữ liệu muốn có.
        *   **Bước 2. Chọn kiểu trình bày biểu mẫu.** Hộp thoại tiếp theo của tiện ích tạo biểu mẫu sẽ yêu cầu chọn kiểu trình bày. Có 4 kiểu: columnar (mặc định, hay dùng nhất); tabular, datasheet, justified. Hãy thử chọn, xem trước và đổi sang kiểu khác nếu muốn vì có sẵn nút "< back" để quay lại.
        *   **Bước 3. Chọn Finish** để kết thúc và ghi lưu. Có thể đổi tên nếu cần.
    *   **② Biểu mẫu phân cấp và biểu mẫu đồng bộ hoá**
    *   Nếu hai bảng có mối quan hệ 1-∞ (bảng mẹ – bảng con), có thể tạo biểu mẫu hiển thị một bản ghi của bảng mẹ và dữ liệu từ các hàng trong bảng con liên quan đến bản ghi của bảng mẹ. Đây là biểu mẫu phân cấp, có dạng tách đôi, hiển thị đồng bộ dữ liệu từ hai bảng khác nhau, theo mối quan hệ đã thiết lập trước.
*   **Hướng dẫn tạo biểu mẫu phân cấp và biểu mẫu đồng bộ hoá bằng Form Wizard**
    *   Quy trình tạo biểu mẫu kết buộc với nhiều hơn một bảng sẽ có nhiều thao tác hơn ở bước chọn các trường dữ liệu.
    *   **Bước 1. Chọn các trường dữ liệu:**
    *   Chọn các trường dữ liệu từ cả hai, bảng mẹ và bảng con, trước khi nháy chọn Next.
    *   Tiện ích tạo biểu mẫu sẽ nhận biết và yêu cầu lựa chọn biểu mẫu chính và biểu mẫu con lệ thuộc.
    *   **Bước 2. Chọn biểu mẫu chính:**
    *   Nháy chuột chọn tên bảng nguồn dữ liệu chính.
    *   Khung hình sẽ đưa ra câu hỏi để chọn tạo biểu mẫu phân cấp hay biểu mẫu đồng bộ hoá.
    *   1) Form with subform(s): Tạo biểu mẫu đồng bộ hoá.
    *   2) Linked forms: Tạo biểu mẫu phân cấp.
    *   **Bước 3. Đánh dấu lựa chọn 1):**
    *   Hộp thoại tiếp theo sẽ hỏi cách trình bày biểu mẫu con.
    *   Đánh dấu chọn theo mong muốn.
    *   Tiếp theo ta trở lại với Bước 2 và Bước 3 trong quy trình thao tác làm biểu mẫu bằng Form Wizard.
    *   **3) Sử dụng biểu mẫu để nhập hoặc xem dữ liệu:**
    *   Mở biểu mẫu trong khung nhìn biểu mẫu (Form View) để nhập hoặc xem dữ liệu.
    *   Một biểu mẫu nhiều bản ghi vừa được tạo ra, chưa chỉnh sửa, nhưng đã có thể sử dụng để xem và nhập dữ liệu.
# Hướng Dẫn Sử Dụng và Thiết Kế Truy Vấn trong Access
*   **Chú ý ở góc dưới bên trái:**
    *   Có hộp hiển thị số thứ tự bản ghi đang xử lí, trong hình minh hoạ: “17 of 17” nghĩa là bản ghi thứ 17 trong số 17 bản ghi đã có.
    *   Có các nút điều hướng quen thuộc: lùi, tiến, nhảy tới bản ghi cuối cùng, hiển thị một biểu mẫu trống để bắt đầu nhập dữ liệu cho bản ghi mới.
    *   Có hộp Search để tìm kiếm.
## Sắp xếp các bản ghi theo giá trị một trường
*   Khi nhập dữ liệu, theo mặc định Access thêm bản ghi mới thành hàng cuối cùng trong bảng dữ liệu.
*   Khi xem dữ liệu, thứ tự hiển thị các bản ghi như vốn có trong bảng nếu ta không thay đổi cách sắp xếp.
*   Một số kiểu dữ liệu như: chữ, số, ngày tháng,... có thể sắp xếp theo thứ tự tăng dần hay giảm dần.
*   **Hướng dẫn thao tác sắp xếp:**
### Bước 1: Chọn cột hay ô dữ liệu trong cột đó.
### Bước 2: Chọn Home sau đó chọn nhóm Sort & Filter.
### Bước 3: Chọn Ascending hay Descending rồi quan sát kết quả.
### Bước 4: Chọn Save trong thanh công cụ nhanh Quick Access Toolbar.
*   Sau khi đã ghi lưu cách sắp thứ tự thì mỗi lần mở xem sau này các bản ghi sẽ hiển thị theo cách sắp xếp đã chọn.
*   Để gỡ bỏ không sắp thứ tự nữa, nháy chuột vào Remove Sort.
*   Việc sắp thứ tự nhiều mức, lần lượt theo vài cột phức tạp hơn, cần sử dụng nút lệnh Advanced trong nhóm lệnh Sort & Filter.
## Lọc các bản ghi
*   Access làm sẵn nhiều lựa chọn lọc kèm các cột dữ liệu kiểu văn bản chữ, số, ngày tháng. Mở bảng dưới khung nhìn bảng dữ liệu và thao tác tương tự như trong Excel.
*   Bước 1. Nháy chuột vào dấu trỏ xuống cạnh tên cột muốn lọc; xuất hiện danh sách thả xuống các hộp đánh dấu chọn.
*   Bước 2. Đánh dấu chọn những gì bạn muốn xuất hiện, sau đó chọn OK.
*   **Thực hành tạo và sử dụng biểu mẫu**
### Nhiệm vụ 1. Tạo biểu mẫu để nhập dữ liệu vào bảng Mượn-Trả sách
*   Tạo một biểu mẫu nhiều bản ghi lấy dữ liệu từ bảng *Mượn-Trả*, ghi lưu với tên *MượnTrả*.
### Nhiệm vụ 2. Tạo biểu mẫu để tìm mượn sách
*   Biểu mẫu nhiều bản ghi để tìm mượn sách lấy dữ liệu từ bảng *Sách* và cần đáp ứng các yêu cầu:
    *   a) Sắp xếp thứ tự theo *Tên sách*.
    *   b) Lọc theo cột *Sẵn có*. Ghi lưu với tên *Sách-Multi*.
### Nhiệm vụ 3. Sử dụng biểu mẫu để nhập dữ liệu
*   Dùng biểu mẫu vừa tạo ở Bài 1, nhập một số bản ghi vào bảng *Mượn-Trả*.
*   *Chú ý*: Dữ liệu nhập vào không được trái với thực tế trong hoạt động của thư viện.
*   Quản lí thư viện cần biết mỗi bạn đọc đã mượn những cuốn sách nào. Em hãy tạo một biểu mẫu cho phép làm việc này.
*   Câu 1. Mục dữ liệu “có kết buộc với bảng CSDL” và “không kết buộc” khác nhau như thế nào?
*   Câu 2. Dùng nút lệnh nào để tạo nhanh biểu mẫu? Trường hợp nào nên chọn cách làm này?
*   **Tóm tắt bài học**
    *   Biểu mẫu dùng để nhập và xem dữ liệu từ một hoặc nhiều bảng; có thể hiển thị một bản ghi hay nhiều bản ghi; có thể trình bày tách đôi thành hai phần.
    *   Nút lệnh Form để tạo nhanh biểu mẫu nhưng không cho phép tùy biến.
    *   Tiện ích tạo biểu mẫu Form Wizard hỗ trợ tạo các loại biểu mẫu tùy biến theo yêu cầu sử dụng.
# Mục tiêu bài học "Thiết kế truy vấn":
*   Tạo và sử dụng được các truy vấn để tìm kiếm và kết xuất thông tin từ Cơ sở dữ liệu (CSDL).
*   Góp phần giải thích tính ưu việt của việc quản lí dữ liệu một cách khoa học nhờ ứng dụng CSDL.
*   **Để lấy ra một thông tin cụ thể từ CSDL thì cần công cụ gì?**
## Thiết kế truy vấn đơn giản:
### Truy vấn SELECT:
*   Truy vấn là một mẫu câu hỏi, cho phép chọn từ các bảng đúng những gì cần xem.
*   Sau khi thiết kế và ghi lưu, mỗi khi mở lại truy vấn sẽ có câu trả lời dựa trên dữ liệu mới nhất, thể hiện tính ưu việt của quản lí dữ liệu khoa học nhờ ứng dụng CSDL.
*   Access hỗ trợ tốt việc thiết kế và thực thi truy vấn, bắt đầu từ yêu cầu thao tác dữ liệu của một ứng dụng quản lí cụ thể.
*   Bài học sẽ tập trung vào chức năng cung ứng dịch vụ “cho mượn – nhận trả” sách.
*   **Điểm thuộc logic nghiệp vụ thư viện và dự kiến truy vấn tương ứng:**
    *   Bạn đọc đến tìm sách để mượn: Cần truy vấn tìm “Sách có sẵn để mượn”.
    *   Thủ thư cần thao tác “Cho mượn - Nhận trả”: Ngoài việc nhập dữ liệu vào bảng Mượn-Trả còn phải sửa giá trị trường Sẵn có trong bảng để đánh dấu Yes/No phù hợp.
*   **Thiết kế truy vấn SELECT đơn giản:**
#### Bước 1: Nháy chuột chọn Create\Query Design.
#### Bước 2: Hộp thoại Show Table xuất hiện. Truy vấn lấy thông tin từ các bảng của CSDL. Nháy chuột chọn tên bảng và nháy nút Add, sau đó nháy Close khi chọn xong.
#### Bước 3: Vùng làm việc thiết kế truy vấn sẽ mở ra và được chia thành hai phần. Phần trên chứa các hộp thể hiện các bảng vừa được chọn, mỗi hộp hiển thị tên tất cả các trường của bảng đó. Nếu có trường bị che khuất, dùng chuột kéo đường viền đáy hộp để mở rộng thêm.
*   Access cũng hiển thị đường nối thể hiện liên kết giữa các bảng.
*   Bước 4. Phân dưới hiển thị một lưới ô, thường gọi là lưới QBE (Query by Example).
*   Muốn chọn lấy dữ liệu từ trường nào chỉ cần nháy đúp chuột lên tên trường trong hộp thể hiện bảng. Tên trường sẽ xuất hiện trong cột ở lưới ô bên dưới, tuần tự từ trái sang phải theo trình tự thao tác chọn.
*   Hàng Field ở trên cùng của lưới ô hiển thị các tên trường đã chọn. Hàng thứ hai bên dưới Field là Table, hiển thị tên bảng chứa trường đó.
*   Bước 5. Nháy chọn Run, kết quả truy vấn hiển thị trong khung nhìn bảng dữ liệu.
*   Bước 6. Ghi lưu truy vấn. Nên đặt tên gọi nhớ kết quả truy vấn. Tên truy vấn sẽ xuất hiện trong vùng điều hướng. Sau đó, ta có thể mở ra bất cứ lúc nào để chỉnh sửa lại thiết kế theo mong muốn hoặc cho chạy để xem thông tin mới cập nhật từ CSDL. Ví dụ, ta đặt tên truy vấn vừa làm xong là “q-BanDoc-MuonTra”.
*   Mẹo: Một thói quen thực hành tốt là thêm tiền tố “q-” (query) vào trước tên để dễ nhận biết đó là một truy vấn. Trong vùng điều hướng có biểu tượng đi kèm nên ta không nhầm lẫn, nhưng trong các hộp thoại để chọn nguồn dữ liệu tạo biểu mẫu, báo cáo,... sẽ chỉ có tên xuất hiện nên khó phân biệt bảng với truy vấn.
*   Sắp xếp kết quả truy vấn
## Thứ tự hiển thị các trường:
*   Thứ tự hiển thị các trường (cột) giống như trong lưới ô. Muốn thay đổi thứ tự này, ta sửa lại lưới ô trong khung nhìn thiết kế.
*   Nếu hai bảng đã được thiết lập mối quan hệ kết nối với nhau, sẽ chỉ thấy những bản ghi khớp đúng. Access đã tự động thực hiện phép nối trong.
*   Trình tự hiển thị các bản ghi là trình tự vốn có ở trong bảng dữ liệu cơ sở.
*   **Sắp xếp các bản ghi theo giá trị trường dữ liệu:**
    *   Chuyển sang khung nhìn thiết kế truy vấn Design View. Trong vùng lưới ô, ở bên dưới hàng Table có hàng tên là Sort. Hàng này dùng để sắp xếp kết quả truy vấn theo một hoặc nhiều trường (lồng nhau).
    *   Sắp xếp theo một trường: chọn trường; chọn **Ascending** hoặc **Descending** để sắp xếp tăng dần hoặc giảm dần.
    *   Sắp xếp lồng nhau theo một vài trường, từ ngoài vào trong: thao tác lần lượt tuần tự từng trường, trình tự lồng nhau từ ngoài vào trong sẽ tương ứng lần lượt từ trái sang phải.
    *   Ví dụ, trong truy vấn ở trên, nếu ta muốn sắp xếp theo “Tên” bạn đọc thì trong lưới ô, tại ô giao cắt cột Tên với hàng Sort cần chọn **Ascending**.
*   **3 Chọn bản ghi cho truy vấn SELECT:**
### a) Tiêu chí lựa chọn bản ghi
*   Tiêu chí lựa chọn được thể hiện bằng một biểu thức logic gồm các biến trường và các phép toán. Chỉ các bản ghi với các giá trị trường dữ liệu làm biểu thức logic có giá trị là “Đúng” (True) mới được chọn lấy ra.
*   Hàng *Criteria* (tiêu chí) trong phần lưới ô là nơi viết biểu thức logic thể hiện tiêu chí lựa chọn. **Mô tả chức năng truy vấn:**
Các đoạn văn bản này mô tả cách người dùng thiết lập các thuộc tính sắp xếp (Sort) và tiêu chí lựa chọn (Criteria) trong môi trường thiết kế truy vấn cơ sở dữ liệu (ví dụ như trong Microsoft Access). Chức năng sắp xếp cho phép người dùng định nghĩa thứ tự xuất hiện của các bản ghi kết quả (tăng dần hoặc giảm dần), có thể áp dụng cho một hoặc nhiều trường. Chức năng tiêu chí lựa chọn cho phép lọc các bản ghi dựa trên một biểu thức logic, đảm bảo rằng chỉ những bản ghi thỏa mãn điều kiện đã cho mới được hiển thị trong kết quả truy vấn. Ví dụ, để lấy ra các bản ghi có "Mã sách" là "VH-01", người dùng sẽ nhập giá trị này vào hàng Criteria tương ứng với trường "Mã sách".
### b) Một số thành phần trong biểu thức logic làm tiêu chí lựa chọn dữ liệu
*   Trong Bảng 1 là một số ví dụ đơn giản để minh họa cách viết một số biểu thức cơ sở.
*   Các phép toán:
    *   (1) Các phép so sánh (kiểu số, xâu kí tự, ngày tháng): =, <> (không bằng), >, >=, <, <=.
    *   (2) Kiểm tra thuộc miền giá trị: In, Not In, Between, Not Between, Is Null, Is Not Null.
*   Có thể phối hợp vài biểu thức logic để tạo ra tiêu chí lựa chọn phức tạp hơn.
*   Liên kết AND: Thể hiện bằng cách đặt hai tiêu chí lựa chọn ở hai trường khác nhau nhưng trên cùng hàng. Access sẽ chỉ lấy ra các bản ghi mà đáp ứng cả hai tiêu chí.
# Liên kết OR
*   Thể hiện bằng cách đặt tiêu chí lựa chọn thứ hai ở hàng Or. Access sẽ lấy ra các bản ghi đáp ứng một trong hai tiêu chí.
*   Bảng 2 là ví dụ đơn giản để minh họa cách viết cho hai trường *Ngày Mượn* trong bảng *Mượn-Trả* và *Số trang* trong bảng *Sách*.
# Hướng dẫn thực hiện truy vấn "q-BanDoc-MuonTra"
*   Thử thêm một số tiêu chí lựa chọn áp dụng cho trường Tên; chạy thử; kiểm tra kết quả; không ghi lưu.
*   Thử thêm một số tiêu chí lựa chọn áp dụng cho trường Ngày mượn; chạy thử; kiểm tra kết quả; không ghi lưu.
# Truy vấn có tham số
*   Có thể mời người sử dụng nhập thêm yêu cầu lựa chọn khi chạy một truy vấn thay vì viết sẵn biểu thức logic đầy đủ.
*   Đây là một truy vấn có tham số (Parameter Query).
*   Truy vấn có tham số giúp tăng tính linh hoạt khi khai thác dữ liệu từ CSDL.
## Cách viết một truy vấn tham số đơn giản
*   Viết lời nhắc trong cặp ngoặc vuông ([]) để người sử dụng hiểu và điền đúng tham số vào câu lệnh truy vấn.
*   Cặp dấu ngoặc vuông chứa lời nhắc phải đặt ở đúng vị trí thay thế cho dữ liệu điền trước.
*   Ví dụ, thay thế cho “VH-01” bằng [Mã sách?].
*   Khi chạy truy vấn, một hộp thoại sẽ xuất hiện để chờ cung cấp tham số.
*   Sau khi điền tham số (ví dụ “VH-01”) và nhấn OK, kết quả nhận được sẽ giống như có dữ liệu trực tiếp.
## Một số mẫu lời nhắc linh hoạt
*   Ngoài dấu bằng “=”, có thể sử dụng các phép so sánh khác như <, <=, >, >=, <> khi thể hiện tham số truy vấn.
# Truy vấn hành động
*   Ngoài truy vấn SELECT, còn có các loại truy vấn khác như Make Table (tạo bảng), Append (nối thêm dữ liệu), Update (cập nhật), Delete (xoá hàng loạt nhiều bản ghi trong bảng).
*   Truy vấn hành động thực hiện thay đổi bảng và một loạt nhiều bản ghi.
*   Kết quả của truy vấn hành động không thể đảo ngược (không thể hoàn tác - undo).
*   Cần rất thận trọng khi sử dụng truy vấn hành động.
*   Nên sao lưu dự phòng các bảng liên quan trước khi thực hiện truy vấn hành động.
# Thực hành thiết kế truy vấn
## Nhiệm vụ 1. Thiết kế truy vấn dựa trên bảng Sách, lấy ra các thông tin phục vụ bạn đọc tìm sách để mượn sao cho thuận tiện nhất
*   a) Sắp xếp theo trường tên sách.
*   b) Lựa chọn chỉ hiển thị khi sẵn có để mượn.
*   Ghi lưu truy vấn với tên “q-TìmSách”.
*   c) Tạo biểu mẫu nhiều bảng ghi dựa trên truy vấn “q-TìmSách”; ghi lưu với tên TìmSách.
*   d) So sánh với biểu mẫu Sách-Multi đã làm sau bài học về biểu mẫu.
## Nhiệm vụ 2. Để chuẩn bị thông tin cho thao tác “Cho mượn” hay “Nhận trả” một cuốn sách cụ thể cần truy vấn nối hai bảng Mượn-Trả và Sách
*   a) Thao tác từng bước thiết kế truy vấn nối hai bảng nói trên, chạy thử; kiểm tra kết quả; ghi lưu với tên “q-Sách-MượnTrả”.
*   b) Thêm tiêu chí lựa chọn theo Mã sách, ví dụ chọn mã sách là “VH-01”.
*   Trong lưới ô, tại ô giao cắt cột Mã sách với hàng Criteria, cần viết rõ mã sách này là “VH-01”; chạy thử để kiểm tra.
*   c) Chuyển thành truy vấn có tham số; chạy thử; kiểm tra kết quả và ghi lưu với tên “q-NhậnTrả”.
*   Giả sử thư viện có quy định một bạn đọc không được mượn và giữ quá 5 cuốn sách. Hãy thiết kế truy vấn giúp thủ thư kiểm tra điều kiện này khi có một bạn đọc muốn mượn sách.
*   Câu 1. Thao tác nào sẽ mở vùng làm việc thiết kế truy vấn?
*   Câu 2. Truy vấn có tham số là gì? Lời nhắc điền tham số viết ở đâu?
*   Câu 3. Truy vấn hành động là gì? Tại sao cần rất thận trọng khi thực hiện nó?
# Tóm tắt bài học
*   Trình tiện ích Query Design cho phép chọn các bảng (hay truy vấn khác) và lấy ra các trường dữ liệu cần có; mỗi cột trong lưới QBE ứng với một trường dữ liệu (cột trong bảng) được chọn.
*   Hàng Sort trong lưới QBE để sắp xếp thứ tự theo giá trị dữ liệu trường.
*   Hàng Criteria để viết biểu thức logic chọn các bản ghi mong muốn; dùng phép toán AND kết hợp điều kiện cho các trường khác nhau.
*   Hàng Or để viết biểu thức dùng phép toán OR kết hợp điều kiện cho các trường khác nhau.
# Mô tả chức năng của đoạn mã hoặc biểu thức
Đoạn mã "Gợi ý: <>IsEmpty([Sẵn có])." mô tả một điều kiện được sử dụng trong truy vấn. Chức năng của nó là kiểm tra xem trường dữ liệu có tên "Sẵn có" có giá trị hay không, và chỉ chọn những bản ghi mà trường này không rỗng (có nghĩa là có dữ liệu).
# BÀI 6 TẠO BÁO CÁO ĐƠN GIẢN
*   **Học xong bài này, em sẽ:**
    *   Thực hiện được việc kết xuất thông tin từ CSDL.
    *   Tìm hiểu được thêm một vài chức năng của hệ quản trị CSDL.
*   **Theo em hiểu "làm báo cáo" nghĩa là gì?**
# 1) Xây dựng báo cáo đơn giản
## a) Các loại báo cáo
*   Xây dựng báo cáo là khâu quan trọng cuối cùng hoàn tất việc kết xuất thông tin từ CSDL phục vụ người dùng. Báo cáo nhằm đáp ứng yêu cầu thông tin của cấp quản lí cơ quan, doanh nghiệp. Mỗi khi chạy thực thi báo cáo, thông tin được kết xuất từ dữ liệu cập nhật mới nhất. Khác với biểu mẫu, người xem báo cáo không sửa đổi được các mục dữ liệu.
*   Một báo cáo chi tiết hiển thị tất cả các bản ghi đã chọn, được phân nhóm và sắp xếp, có thể thêm số liệu tóm tắt mỗi nhóm ví dụ như: tổng con, số đếm, tỉ lệ phần trăm,... Cuối báo cáo thường có các số liệu tổng hợp toàn bộ.
*   Một báo cáo tóm tắt không liệt kê các bản ghi đã chọn, chỉ trình bày các số liệu tổng hợp nhóm theo một chiều nào đó. Ví dụ, tổng hợp theo tháng, theo quý, theo năm (chiều thời gian); tổng hợp theo các chi nhánh khác nhau: Hà Nội, Hải Phòng, Đà Nẵng, Thành phố Hồ Chí Minh,... (chiều địa điểm).
*   Một báo cáo tóm tắt phân tích nhiều chiều dựa trên một mẫu truy vấn riêng tạo bằng *Crosstab Query Wizard*. Ví dụ, báo cáo phân tích theo cả hai chiều, thời gian (theo tháng, theo quý, theo năm) và theo các chi nhánh ở nhiều địa phương khác nhau.
*   Báo cáo được xây dựng dựa trên nguồn dữ liệu là bảng hay truy vấn. Để xây dựng báo cáo, cần biết sẽ dùng đến những trường dữ liệu nào và nên chuẩn bị sắp xếp, chọn lọc sẵn từ trước bằng một truy vấn.
# Truy vấn chuẩn bị dữ liệu
*   Giả sử ta cần làm báo cáo chi tiết hoạt động mượn trả sách của thư viện theo từng tháng, cho biết mỗi tháng có bao nhiêu giao dịch mượn sách và đồng thời phân tích số liệu theo Loại sách được mượn.
*   Cần thiết kế truy vấn lấy dữ liệu từ các bảng *Mượn-Trả* và bảng *Sách* (để có trường *Loại sách*).
## Chú ý các chi tiết trong truy vấn chuẩn bị báo cáo chi tiết
*   Sắp xếp theo *Ngày mượn* là để nhóm theo từng tháng.
*   Gõ nhập trực tiếp cho cột “Month: Month([Ngày mượn])” để trích ra phần “tháng” từ *Ngày mượn*.
*   Ghi lưu truy vấn, ví dụ với tên là “q-MượnTrả-Month”.
## Tạo nhanh báo cáo đơn giản
*   **Bước 1:** Mở truy vấn “q-MượnTrả-Month” (hoặc chỉ cần đánh dấu chọn).
*   **Bước 2:** Nháy chọn Create\Report sẽ tạo một báo cáo.
*   **Bước 3:** Ghi lưu với tên “MượnTrả-Month”.
*   Đây là báo cáo chi tiết, hiển thị đầy đủ các bản ghi. Sau đó có thể thêm gộp nhóm và thông tin tóm tắt theo nhóm.
## Hướng dẫn sử dụng Report Wizard
*   Trình tiện ích Report Wizard hỗ trợ tạo báo cáo và cho phép lựa chọn tuỳ biến theo yêu cầu.
*   **Bước 1:** Nháy chuột chọn Create\Report Wizard.
*   **Bước 2:** Chọn bảng hoặc truy vấn làm nguồn dữ liệu cơ sở cho báo cáo.
*   Ví dụ: chọn bảng Mượn-Trả.
*   **Bước 3:** Chọn các trường dữ liệu cần báo cáo.
*   Ví dụ: Số thẻ, Mã sách, Ngày Mượn.
*   Nháy vào dấu ">" để chuyển các trường đã chọn sang hộp Selected Fields.
*   Nháy Next khi đã chọn đủ các trường dữ liệu cần có.
*   **Bước 4:** Chọn gộp nhóm theo trường dữ liệu nào.
*   Ví dụ: chọn nhóm theo Số thẻ (tức là nhóm theo từng bạn đọc).
*   Nháy Next.
*   **Bước 5:** Chọn một bài trí cơ sở cho báo cáo.
*   Lựa chọn mặc định là "Tabular" nhưng có thể thay đổi nếu muốn.
*   Nháy Next.
*   **Bước 6:** Nhập tên báo cáo trước khi chọn Finish.
*   Nên đặt tên gợi nhớ nội dung báo cáo.
*   Ví dụ: "MượnTrả-theoBạnđọc".
*   Sau khi báo cáo được tạo ra, biểu tượng của báo cáo sẽ xuất hiện trong vùng điều hướng.
*   Có thể mở báo cáo ra bất cứ lúc nào để chỉnh sửa lại thiết kế theo mong muốn hoặc cho chạy để lấy thông tin mới cập nhật.
## Gộp nhóm, sắp xếp và các tổng con
*   Gộp nhóm các bản ghi là để tóm tắt dữ liệu nhằm hiển thị tổng con (hay giá trị trung bình, giá trị cực tiểu, giá trị cực đại) cho mỗi trường dữ liệu kiểu số của từng nhóm bản ghi (nhóm hàng).
*   Sau khi gộp nhóm thì dữ liệu từng nhóm xuất hiện trong phần Detail.
*   Ví dụ: muốn tóm tắt hoạt động mượn trả theo từng tháng.
## Hướng dẫn thực hiện gộp nhóm
*   **Bước 1:** Mở báo cáo chi tiết “MượnTrả-Month” trong khung nhìn thiết kế.
*   Nháy vào lệnh Group & Sort trong vùng nút lệnh.
*   Cửa sổ Group, Sort, and Total xuất hiện ở đáy màn hình.
*   **Bước 2.** Nháy nút lệnh Add a group; nháy vào mũi tên trỏ xuống cạnh selected field; tiếp tục nháy chọn Month.
*   **Bước 3.** Access gợi ý sắp xếp tăng dần “from smallest to largest”. Bỏ qua vì ta đã sắp xếp theo Ngày mượn khi truy vấn.
# BÁO CÁO VÀ CHỈNH SỬA GIAO DIỆN
## Thực hành tạo báo cáo đơn giản
*   **Nhiệm vụ 1.** Theo hướng dẫn chi tiết từng bước trong bài học, thực hiện các việc sau:
    *   a) Tạo truy vấn dữ liệu làm nguồn dữ liệu cho báo cáo.
    *   b) Tạo báo cáo đơn giản bằng nút lệnh Report; ghi lưu kết quả thành báo cáo “MượnTrả-Month”.
*   **Nhiệm vụ 2.** Sử dụng báo cáo vừa tạo ở Bài 1, thực hiện các việc sau:
    *   a) Mở báo cáo “MượnTrả-Month”.
    *   b) Lặp lại từng bước theo hướng dẫn để gộp nhóm theo tháng, tính các tổng con và xác định cách hiển thị. Kiểm tra kết quả. Ghi lưu.
*   Em hãy thiết kế truy vấn làm cơ sở để báo cáo chi tiết từng bạn đọc mượn sách trong năm học.
*   **Gợi ý:** Lấy dữ liệu từ hai bảng Bạn Đọc và bảng Mượn-Trả, sắp xếp theo Số thẻ.
*   **Câu 1.** Báo cáo chi tiết khác với báo cáo tóm tắt ở điểm nào?
*   **Câu 2.** Khi nào nên dùng nút lệnh tạo báo cáo nhanh? Khi nào nên dùng công cụ Report Wizard?
### Tóm tắt bài học
*   Lệnh Report giúp dễ dàng tạo báo cáo chi tiết có phân nhóm dựa trên truy vấn có sắp xếp kết quả thích hợp.
*   Trình tiện ích Report Wizard hỗ trợ tạo báo cáo lấy dữ liệu từ nhiều bảng hay truy vấn, có các tuỳ chọn sắp xếp và bài trí đa dạng.
*   Trong khung nhìn thiết kế báo cáo, nhóm lệnh Group & Sort hỗ trợ phân nhóm, sắp xếp và thêm các loại tổng con.
### BÀI TÌM HIỂU THÊM
### BÁO CÁO PHÂN TÍCH NHIỀU CHIỀU
*   Truy vấn Crosstab Query Wizard là tiện ích tạo truy vấn tóm tắt nguồn dữ liệu lớn, phức tạp, đáp ứng yêu cầu tổng hợp số liệu và phân tích theo nhiều cách.
*   Access có sẵn nhiều hàm gộp để tổng hợp số liệu như: Sum, Count, Min, Max, Avg (tính trung bình), được dùng trong mẫu truy vấn đặc thù này.
*   Báo cáo phân tích nhiều chiều dựa trên truy vấn crosstab.
*   Đó là một báo cáo tóm tắt hoạt động của thư viện theo tháng, có phân tích theo loại sách: “TH” là Tin học, “Khác” là không phải Tin học.
# BÀI 7 CHỈNH SỬA CÁC THÀNH PHẦN GIAO DIỆN
*   **Học xong bài này, em sẽ:**
    *   Chỉnh sửa được bài trí các thành phần trong biểu mẫu, báo cáo.
    *   Thiết lập được chủ đề màu sắc, phong cách văn bản của giao diện ứng dụng.
*   Em hãy cho biết dải lệnh Layout có chức năng gì.
## 1) Các thành phần và các phần tử trong báo cáo
### a) Các thành phần trong báo cáo
*   Có 4 khung nhìn báo cáo. Theo mặc định, báo cáo mở ra trong khung nhìn báo cáo Report View. Để xem cấu trúc các thành phần của báo cáo, cần chuyển sang khung nhìn thiết kế (Design View). Dưới đây minh họa bằng báo cáo “MượnTrả-TheoTháng”.
*   Trong khung nhìn thiết kế sẽ thấy rõ các phần:
    *   *Report Header*: Nhãn tiêu đề báo cáo ở phần trên cùng của trang đầu tiên. Khi mới tạo ra, theo mặc định Access lấy tên truy vấn (hay bảng) là nguồn dữ liệu của báo cáo làm tên cho báo cáo.
    *   *Page Header*: Nhãn văn bản ở trên đỉnh mọi trang của báo cáo. Đây là các tên trường dữ liệu ở đỉnh mỗi cột.
## Mô tả code:
*   Một đoạn mã có chức năng đếm tổng số bản ghi.
*   Một đoạn mã khác có chức năng hiển thị số trang hiện tại và tổng số trang của báo cáo, thường được định dạng là "Trang [số trang hiện tại] của [tổng số trang]".
*   Một đoạn mã khác có chức năng tính tổng các giá trị trong một trường dữ liệu có tên là "Montl".
Trang 164
## Phân loại các phần trong báo cáo:
*   `Detail:` Nằm giữa phần đầu trang và chân trang, xác định chi tiết việc hiển thị dữ liệu từ các bản ghi.
*   `Page Footer:` Xuất hiện ở đáy mọi trang của báo cáo; hiển thị số thứ tự trang trên tổng số trang và ngày tháng.
*   `Report Footer:` Xuất hiện trong trang cuối của báo cáo và hiển thị thông tin tóm tắt ví dụ như tổng toàn bộ (grand totals).
## Các phần tử trong thân báo cáo:
*   Mỗi phần `Report Header`, `Page Header`, `Detail`, `Page Footer`, `Report Footer` gồm nhiều phần tử nhỏ hơn, mỗi phần tử là một hộp hình chữ nhật, còn gọi là một điều khiển (control).
*   Cần phân biệt hai loại phần tử khác nhau về bản chất mặc dù nhìn giống nhau: hộp dữ liệu và nhãn tên trường.
*   `Hộp dữ liệu` được kết buộc với các trường dữ liệu từ bảng hay truy vấn cơ sở và được cập nhật bằng dữ liệu mới nhất khi chạy báo cáo.
*   `Hộp dữ liệu` nằm trong phần `Detail` của báo cáo, lấy dữ liệu từ trường nào thì tên của trường đó hiển thị bên trong hộp và không được thay đổi tên này.
*   `Nhãn tên trường` chỉ là nhãn tên, không kết buộc với dữ liệu.
*   Theo mặc định, các nhãn tên trường được gán theo tên cột dữ liệu, nên chọn đặt tên phù hợp, dễ hiểu khi thiết kế bảng.
*   Có thể sửa đổi nhãn tên, đặt tên mới nếu muốn.
*   `Thao tác sửa đổi nhãn tên:` Nháy đúp chuột vào nhãn tên; con trỏ soạn thảo xuất hiện; gõ nhập tên mới. Ví dụ, có thể sửa tiêu đề báo cáo trong hình thành “Báo cáo chi tiết hoạt động mượn trả sách từng tháng”.
## Các thành phần trong biểu mẫu:
*   Dưới khung nhìn thiết kế, biểu mẫu chia thành ba phần:
    *   `Đầu biểu mẫu (Form Header):` Hiển thị tiêu đề của biểu mẫu. Có thể thêm logo của tổ chức, hình trang trí tiêu đề ở đây.
    *   `Chân biểu mẫu (Form Footer):` Phần tùy chọn ở cuối trang biểu mẫu, thường có nội dung để in ra, ví dụ là ngày tháng, người thực hiện,...
    *   `Phần chi tiết (Detail)` là thân biểu mẫu.
## Các phần tử trong thân biểu mẫu
*   Các phần của biểu mẫu chứa nhiều phần tử nhỏ hơn là các điều khiển (control).
*   Có hai loại phần tử: hộp dữ liệu và nhãn tên trường.
*   Thân biểu mẫu chứa nội dung chính của nó.
*   Một trường trong bản ghi sẽ ứng với một cặp hai phần tử: nhãn tên trường và hộp dữ liệu.
*   Dữ liệu nhập vào hộp sẽ được cập nhật vào CSDL và hiển thị trở lại khi xem dữ liệu.
*   Có thể thay đổi nhãn tên trường mà không ảnh hưởng đến chức năng của biểu mẫu.
## Chỉnh sửa bài trí
*   Biểu mẫu hay báo cáo được tạo tự động theo mặc định có thể sử dụng ngay để xem thông tin.
*   Đây là sản phẩm thô, kích cỡ các phần tử có thể chưa hợp lí, cách bài trí tổng thể các thành phần chưa hài hoà, chưa tiện dụng.
*   Có những hộp văn bản quá rộng hoặc quá cao so với dữ liệu chứa trong nó.
*   Cũng có những hộp lại quá ngắn hoặc quá thấp.
## Có ba nhóm việc chính khi chỉnh sửa bài trí:
*   Đổi lại tên cho các tiêu đề biểu mẫu, báo cáo; sửa lại các nhãn tên cột ở đầu mỗi trang biểu mẫu hay báo cáo.
*   Có thể giữ nguyên các tên đối tượng đã ghi lưu khi vừa tạo ra và hiển thị kèm biểu tượng trong vùng điều hướng.
*   Tiêu đề của biểu mẫu hay báo cáo hiển thị cho người sử dụng thường phải sửa đổi thành tên mới phù hợp với yêu cầu nghiệp vụ của ứng dụng.
*   Có thể kết hợp chọn kiểu dáng, màu sắc văn bản đẹp mắt.
*   Thao tác hoàn toàn giống như soạn thảo văn bản.
*   Chỉnh sửa kích thước các phần tử cho hợp lí.
*   Di chuyển sắp xếp lại để trông quen thuộc, tiện sử dụng hơn.
*   Ví dụ, trên các biểu mẫu khai thông tin cá nhân, thường thấy hình ảnh ở góc trên bên phải của biểu mẫu.
*   Các trường Họ và tên, Ngày sinh và Giới tính được xếp cùng hàng ngang vì dữ liệu rất ngắn.
## Chỉnh sửa kích thước các phần tử:
*   Khung nhìn bài trí (Layout View) cho phép co giãn kích thước các phần tử theo cách quen thuộc.
*   Thao tác với biểu mẫu hay báo cáo tương tự nhau.
*   **Bước 1.** Chuyển sang khung nhìn bài trí: Chọn View\Layout View hoặc nháy nút khung nhìn tương ứng ở góc dưới bên phải cửa sổ Access.
*   **Bước 2.** Trỏ chuột vào đúng cạnh chiều rộng hay chiều cao, con trỏ chuột sẽ có hình mũi tên hai chiều.
*   **Bước 3.** Nhấn giữ và kéo thả để thay đổi kích thước.
*   Thao tác chỉnh sửa tác động lên cả ô, mọi phần tử khác cùng cột hay cùng hàng cũng được căn chỉnh theo.
*   Hình dung như đang thao tác với bảng trong Word.
*   Chuyển sang khung nhìn biểu mẫu (hay khung nhìn báo cáo) để kiểm tra kết quả sau mỗi thao tác chỉnh sửa.
## Di chuyển các phần tử trong biểu mẫu:
*   Hình dung các phần tử biểu mẫu là các ô trong một bảng nhiều hàng nhiều cột.
*   Để di chuyển sắp xếp lại vị trí, có thể phải chỉnh sửa lưới ô, tạo sẵn chỗ trống làm đích đến.
*   Dải lệnh Arrange có nhiều nút lệnh để chèn thêm cột, thêm hàng, chia tách, hoà nhập các ô.
*   Thao tác này tương tự thao tác với bảng trong Word.
*   Biểu tượng nút lệnh kèm tên gọi tiếng Anh rất dễ hiểu.
*   **Bước 1.** Nháy chọn Arrange.
*   **Bước 2.** Tạo khoảng trống làm đích đến để chứa phần tử muốn chuyển tới.
*   **Bước 3.** Kéo thả để đưa phần tử đã chọn vào đích.
## Di chuyển các phần tử trong báo cáo
*   Khung nhìn thiết kế (Design View) cho phép xử lí riêng lẻ từng phần tử.
*   Nháy chuột chọn và di chuyển bằng kéo thả chuột hoặc nhấn các phím mũi tên trên bàn phím.
# Chủ đề, màu sắc và kiểu dáng phông chữ
*   Trong một CSDL Access, chủ đề (Themes) là tập hợp một số thiết lập cơ bản áp dụng chung cho mọi đối tượng.
*   Ta có thể chọn một chủ đề, màu sắc, kiểu dáng có sẵn để áp dụng tổng thể cho mọi đối tượng trong CSDL.
*   Chỉ cần nháy chuột chọn áp dụng sẽ thấy ngay kết quả hiển thị.
## Em hãy thực hiện các công việc sau:
*   1) Mở biểu mẫu trong khung nhìn bài trí.
*   2) Chọn thẻ Design (Form Layout Tools) sẽ thấy nhóm lệnh Themes (các chủ đề).
*   Chủ đề gồm màu sắc (Colors) và phông chữ (Fonts) có thể chọn riêng hoặc mẫu chung đã tích hợp cả hai.
*   3) Nháy mũi tên xuống dưới nhóm lệnh Themes sẽ hiển thị khoang trưng bày nhiều chủ đề được tạo sẵn để dùng thử.
*   Di chuột qua một biểu tượng bất kì, Access cho xem trước kết quả thay đổi màu sắc, kích cỡ chữ và kiểu dáng sẽ được áp dụng.
*   Chú ý: Thông báo nhỏ “In This Database” cho biết phạm vi áp dụng.
*   4) Nháy mũi tên xuống cạnh lệnh Colors hay lệnh Fonts để thử áp dụng các thiết lập phối màu và phông chữ khác nhau.
## Áp dụng định dạng riêng cho một phần tử
*   Có trường hợp ta muốn chỉnh sửa định dạng riêng cho chỉ một phần tử cụ thể, khác với phong cách chung đã thiết lập cho các phần tử khác.
### Bước 1.
*   Nháy thẻ Format. Dải lệnh Format có các nút lệnh định dạng quen thuộc như trong Word.
### Bước 2.
*   Nháy chọn phần tử đó, thao tác áp dụng định dạng mong muốn.
## Trang trí và bổ sung thêm
*   Thêm logo, hình ảnh trang trí cho biểu mẫu.
*   Nếu có kĩ năng lập trình, có thể thêm một số nút lệnh để người dùng không thành thạo Access tiện sử dụng.
## Thực hành chỉnh sửa giao diện ứng dụng
### Nhiệm vụ 1.
*   Mở biểu mẫu nhiều bản ghi dùng để nhập dữ liệu cho bảng Sách trong khung nhìn bài trí và chỉnh sửa kích thước đồng thời nhiều phần tử cùng cột.
### Nhiệm vụ 2.
*   Mở biểu mẫu một bản ghi dùng để nhập dữ liệu cho bảng Bạn đọc trong khung nhìn thiết kế; bài trí lại hộp dữ liệu của trường Ảnh: co giãn kích thước, di chuyển lên góc trên bên phải.
### Nhiệm vụ 3.
*   Chọn áp dụng Themes và Colors cho toàn bộ giao diện.
*   Sửa lại tiêu đề của các biểu mẫu và báo cáo đã tạo ra, bổ sung thêm tên trường của em.
## Câu hỏi
### Câu 1.
*   Mở khung nhìn nào để chỉnh sửa kích thước các thành phần giao diện? Mở khung nhìn nào để di chuyển một thành phần giao diện?
### Câu 2.
*   Chủ đề là gì? Mở nhóm lệnh nào để chọn áp dụng một chủ đề?
### Câu 3.
*   Để chỉnh sửa định dạng riêng cho chỉ một phần tử cụ thể phải làm gì?
## Tóm tắt bài học
*   Những nhóm việc chính về chỉnh sửa các phần tử biểu mẫu, báo cáo là:
    *   (1) Đổi lại tên mới cho các tiêu đề, nhãn tên.
    *   (2) Chỉnh sửa kích thước các phần tử cho hợp lí.
    *   (3) Di chuyển sắp xếp lại.
*   Sử dụng luân phiên ba khung nhìn: Layout View, Design View, Form View để sắp xếp lại cách bài trí và chỉnh sửa kích thước các thành phần biểu mẫu, báo cáo.
# BÀI 8 HOÀN TẤT ỨNG DỤNG
## Học xong bài này, em sẽ:
*   Tạo được biểu mẫu điều hướng để làm giao diện khi mở ứng dụng.
*   Hoàn tất một ứng dụng đơn giản, có thể sử dụng được.
## Câu hỏi gợi mở:
*   Theo em, làm thế nào để một người không học Access cũng có thể sử dụng được các công cụ quản lí thư viện ta đã tạo ra trong các bài học?
## Biểu mẫu điều hướng
*   Vùng điều hướng trong CSDL Access hiển thị tất cả đối tượng đã được tạo ra, trong đó có nhiều đối tượng không nên cho phép truy cập trực tiếp. Ví dụ: các bảng, các truy vấn.
*   Người dùng có thể vô tình hay cố ý gõ nhập làm hỏng dữ liệu khi mở bảng dữ liệu hay chạy truy vấn.
*   Biểu mẫu điều hướng đơn giản là một giao diện có chứa các nút điều khiển (control) giúp điều hướng để người dùng dễ dàng chuyển đổi giữa các biểu mẫu và báo cáo khác nhau trong CSDL.
*   Báo cáo chỉ hiển thị kết quả xuất ra thông tin, không cho phép sửa đổi được dữ liệu từ các bảng nguồn bên dưới.
*   Biểu mẫu cho phép xem và gõ nhập dữ liệu, nhưng có tính năng khoá chặt một số trường dữ liệu cần bảo vệ, không cho phép sửa đổi.
*   Nếu người thiết kế muốn tạo một bản điều khiển trung tâm (switchboard) giúp người dùng dễ dàng tìm thấy các đối tượng cụ thể đã dành cho họ, thì biểu mẫu điều hướng là giải pháp phù hợp.
## Thao tác tạo biểu mẫu điều hướng
### Bước 1.
*   Chọn Create\Navigation (trong nhóm Forms).
*   Trong danh sách thả xuống có các mục chọn kèm biểu tượng rất dễ hình dung bố cục trống sẽ như thế nào.
### Bước 2:
*   Chọn một mục, ví dụ Horizontal Tabs. Trong vùng làm việc hiển thị biểu mẫu có bố cục đã chọn trong khung nhìn bài trí Layout View.
### Bước 3:
*   Khi biểu mẫu điều hướng đang mở trong khung nhìn bài trí, kéo các báo cáo hay biểu mẫu khác từ vùng điều hướng thả vào ô Add New. Biểu mẫu hay báo cáo đó sẽ lập tức xuất hiện trong vùng làm việc là ô hình chữ nhật đã dành sẵn. Có thể sử dụng ngay để nhập dữ liệu hay xem thông tin giống như khi mở nó từ vùng điều hướng. Thẻ của biểu mẫu, báo cáo sẽ hiển thị thay thế nút Add New.
## Thiết lập biểu mẫu điều hướng làm bàn điều khiển trung tâm của ứng dụng:
*   Để khi mở CSDL trong cửa sổ Access thì biểu mẫu điều hướng sẽ hiển thị đầu tiên, che khuất toàn bộ vùng làm việc và vùng điều hướng, ta thực hiện các bước sau:
### Bước 1:
*   Nháy chọn File\Options (ở cuối dải lệnh thả xuống). Access hiển thị cửa sổ để thiết lập nhiều lựa chọn chung cho toàn bộ phần mềm Access trên máy cá nhân hoặc riêng cho từng CSDL đang làm việc (Current Database).
### Bước 2:
*   Chọn Current Database.
### Bước 3:
*   Tìm mục Display Form. Hiện đang bỏ trống (none). Nháy mũi tên trỏ xuống để thả xuống danh sách các biểu mẫu đang có trong CSDL.
### Bước 4:
*   Chọn Navigation Form là tên biểu mẫu dự kiến làm bàn điều khiển trung tâm.
### Bước 5:
*   Có thể chọn thiết lập che khuất vùng điều hướng để người dùng không nhìn thấy các đối tượng khác đã có trong CSDL bằng cách: tìm mục Navigation; bỏ đánh dấu chọn trong ô Display Navigation Pane.
*   Đóng Access và khởi chạy lại tệp CSDL thì các thiết lập trên mới có hiệu lực. Người sử dụng chỉ cần nháy chuột lên các thẻ, giống như các nút lệnh, thì biểu mẫu, báo cáo sẽ mở để làm việc.
*   **Chú ý:** Nếu biết lập trình, có thể làm thêm một biểu mẫu đăng nhập (login form) yêu cầu cung cấp tên, mật khẩu; sau đó thiết lập để mở biểu mẫu đăng nhập trước tiên thay vì mở bàn điều khiển trung tâm.
*   Access tích hợp sẵn môi trường lập trình VBA (Visual Basic for Application). Nháy chọn Create, ở cuối dải lệnh sẽ thấy nhóm lệnh Macros & Code. Nháy các nút lệnh để bắt đầu viết các câu lệnh.
## Thiết kế giao diện của ứng dụng quản lí thư viện trường:
*   Tóm tắt ngắn gọn vài điểm về quy trình tác nghiệp của thư viện và các biểu mẫu, báo cáo liên quan.
### a) Các biểu mẫu
*   Bạn đọc đến thư viện tìm sách để mượn. Thao tác “tìm sách”: biểu mẫu TìmSách cho thông tin về sách có sẵn.
*   Bạn đọc yêu cầu mượn một cuốn sách. Thao tác “cho mượn”: biểu mẫu ChoMượn để thủ thư cập nhật gồm các trường Số thẻ, Mã sách, Ngày mượn trong bảng Mượn-Trả và Sẵn có trong bảng Sách.
*   Quy tắc nghiệp vụ cần tuân thủ khi cho mượn: Bỏ đánh dấu cuốn sách vừa cho mượn là sẵn có.
*   Bạn đọc đến trả một cuốn sách. Thao tác “nhận trả”: biểu mẫu để thủ thư cập nhật gồm các trường Số thẻ, Mã sách, Ngày mượn, Ngày trả trong bảng Mượn-Trả và Sẵn có trong bảng Sách.
*   Quy tắc nghiệp vụ cần tuân thủ khi nhận trả: Đánh dấu cuốn sách vừa nhận trả là sẵn có.
*   Có thể thêm các biểu mẫu để nhập dữ liệu cho bảng Bạn đọc, bảng Sách.
*   Có thể quy ước là khi nhập một cuốn sách mới vào kho sách thì trường Sẵn có mặc định nhận giá trị là Yes.
*   **Chú ý:** Nếu biết lập trình, có thể thiết lập việc thực thi các quy tắc vừa nêu trên, tránh trường hợp làm sai, dữ liệu có mâu thuẫn, không nhất quán.
### b) Các báo cáo
*   Thống kê hoạt động mượn trả, ví dụ theo tháng: báo cáo MượnTrả-TheoTháng.
*   Báo cáo phân tích mượn trả theo tháng và theo loại sách: báo cáo MượnTrả-Tháng-LoạiSách.
*   Có thể thêm những báo cáo thống kê khác, ví dụ thống kê theo bạn đọc và số đầu sách đã mượn.
## Bảng điều khiển trung tâm của ứng dụng quản lí thư viện trường
*   Một ví dụ thiết kế biểu mẫu điều hướng như sau:
    *   Nhân tiêu đề: "Thư viện Trường THPT..."
    *   Bố cục: Horizontal Tabs.
*   Các thẻ đầu tiên là các biểu mẫu, sau đó là các báo cáo.
## Thực hành tổng hợp
### Nhiệm vụ 1. Tạo và chỉnh sửa bài trí biểu mẫu điều hướng
*   Làm theo các bước hướng dẫn thao tác tạo biểu mẫu điều hướng.
*   Kéo thả các biểu mẫu và báo cáo từ vùng điều hướng vào các ô *Add New* theo bố cục như trong ví dụ đã nêu.
*   Đổi tiêu đề biểu mẫu điều hướng.
*   Đổi tên trong thẻ của các biểu mẫu, báo cáo. Ví dụ: *Tìm Sách, Cho Mượn, Nhận trả* (có khoảng trắng, có dấu tiếng Việt, kiểu dáng chữ,...).
*   Chú ý quan sát thấy tên đối tượng trong vùng điều hướng không thay đổi.
### Nhiệm vụ 2. Hoàn thiện biểu mẫu một bản ghi để nhập dữ liệu cho bảng Bạn đọc;
*   thử nhập dữ liệu cho trường *Ảnh*.
# Nhiệm vụ 3. Thử xuất ra một báo cáo.
## Gợi ý: Mở báo cáo trong khung nhìn *Print Preview* sẽ thấy nhiều nút lệnh để in ra giấy, chuyển thành tệp Excel, chuyển thành tệp “pdf”,....
## Hoàn tất ứng dụng quản lí thư viện theo yêu cầu sử dụng thực tế.
# Câu hỏi ôn tập
## Câu 1. Biểu mẫu điều hướng dùng để làm gì và chứa những gì?
## Câu 2. Thao tác thiết lập biểu mẫu điều hướng làm bàn điều khiển trung tâm của ứng dụng gồm mấy bước? Bắt đầu bằng thao tác nào?
# Tóm tắt bài học
## Những công việc chính để hoàn tất ứng dụng là:
### Thiết kế giao diện, bài trí các nút lệnh phù hợp với quy trình nghiệp vụ quản lí CSDL và cung cấp dịch vụ.
### Tạo một biểu mẫu điều hướng và thực hiện các thiết kế giao diện như trên, chỉnh sửa lại các nhãn tiêu đề, chạy thử kiểm tra.
### Thiết lập biểu mẫu điều hướng làm bàn điều khiển trung tâm của ứng dụng.
