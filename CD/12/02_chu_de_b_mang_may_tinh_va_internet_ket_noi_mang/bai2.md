# Bài 2: CÁC GIAO THỨC MẠNG

Học xong bài này, em sẽ:
* Mô tả sơ lược được vai trò và chức năng của giao thức mạng nói chung và giao thức TCP/IP nói riêng.

Em hãy liệt kê những yêu cầu cần thiết để em và bạn em có thể trao đổi tin nhắn được với nhau.

## 1. Giao thức mạng
### a) Khái niệm cơ bản

Em hãy liên tưởng đến quá trình gửi thư qua bưu điện và đưa ra các bước cần thiết để gửi một tệp dữ liệu từ máy tính thứ nhất đến máy tính thứ hai trong một mạng máy tính.

**Giao thức mạng** là một tập hợp các quy tắc được sử dụng để điều khiển truyền thông và trao đổi dữ liệu giữa các thiết bị trong mạng máy tính nhằm đáp ứng các yêu cầu về:
1.  **Định dạng và chuẩn hoá**: định nghĩa các quy tắc và định dạng cho việc đóng gói, trao đổi dữ liệu trong mạng; đảm bảo rằng dữ liệu được truyền đi và nhận về đúng cách, giúp đảm bảo tính tương thích giữa các thiết bị và ứng dụng khác nhau.
2.  **Định tuyến và chuyển tiếp**: cung cấp các thuật toán và quy trình để định tuyến và chuyển tiếp gói tin từ nguồn đến đích; giúp xác định đường truyền tối ưu cho dữ liệu trong mạng, đảm bảo rằng dữ liệu được truyền đi và nhận về một cách đầy đủ mà không bị lạc mất hoặc bị trùng lặp.
3.  **Quản lí lưu lượng mạng**: cho phép quản lí lưu lượng mạng bằng cách kiểm soát việc gửi và nhận dữ liệu trong mạng; giúp hạn chế lưu lượng không cần thiết, phân phối công bằng tài nguyên mạng, đảm bảo rằng mạng hoạt động hiệu quả và ổn định.
4.  **Đảm bảo tính bảo mật và độ tin cậy**: cung cấp các cơ chế bảo mật để bảo vệ dữ liệu trong mạng khỏi các mối đe doạ như tin tặc, tấn công mạng và lừa đảo. Nó bao gồm các giao thức mã hoá, xác thực và kiểm soát truy cập để đảm bảo tính riêng tư và an toàn của thông tin truyền qua mạng. Đảm bảo tính toàn vẹn cho dữ liệu được truyền thông trong mạng.

5. Tích hợp các dịch vụ và ứng dụng khác nhau trong mạng; định nghĩa cách các ứng dụng giao tiếp và trao đổi dữ liệu với nhau, cho phép người dùng truy cập vào các dịch vụ như truyền tải tệp, truyền thông đa phương tiện, truy cập web và gửi email.
Các giao thức mạng phân tách các quy trình lớn hơn thành các chức năng và nhiệm vụ nhỏ hơn, riêng biệt, trên tất cả các cấp độ mạng. Một tập hợp các giao thức mạng kết nối với nhau thành một bộ giao thức. Ví dụ, bộ giao thức **TCP/IP** được sử dụng phổ biến nhất trong mạng máy tính hiện nay.

## b) Một số giao thức mạng

Một số giao thức mạng quan trọng hiện nay bao gồm:
*   **Giao thức Internet (IP – Internet Protocol)** là một giao thức quan trọng trong mạng máy tính và là một trong những giao thức cốt lõi trong bộ giao thức TCP/IP.
*   **Giao thức vận chuyển** bao gồm các giao thức quy định cách dữ liệu được chia thành các gói tin, đánh số, gửi và nhận giữa các thiết bị mạng. Ví dụ: **TCP – Transmission Control Protocol** và **UDP – User Datagram Protocol**. Giao thức TCP là giao thức vận chuyển đáng tin cậy hơn giao thức UDP trong mạng Internet. UDP truyền dữ liệu mà không yêu cầu việc thiết lập kết nối trước và không đảm bảo việc truyền dữ liệu đúng thứ tự hoặc toàn vẹn.
*   **Giao thức truyền tải siêu văn bản (HTTP – HyperText Transfer Protocol)** là một trong những giao thức phổ biến hiện nay và được sử dụng trong việc truyền tải dữ liệu các trang web. HTTP quy định cách các máy khách và máy chủ giao tiếp và trao đổi thông tin.
*   **Giao thức truyền tải tệp (FTP – File Transfer Protocol)** là giao thức được sử dụng để truyền tải tệp giữa các máy tính. FTP cho phép người dùng truy cập, tải lên, tải xuống và quản lí các tệp trên một máy chủ từ xa.
*   **Giao thức truyền tải thư đơn giản (SMTP – Simple Mail Transfer Protocol)** là giao thức được sử dụng để gửi và nhận thư điện tử trong mạng máy tính. SMTP quy định quy trình trao đổi thư, bao gồm việc xác thực, mã hoá và chuyển tiếp thư.

## 2) Giao thức TCP

**Giao thức điều khiển truyền tải (TCP)** đảm bảo việc truyền dữ liệu ổn định và đúng thứ tự giữa các ứng dụng trên mạng. TCP có cơ chế kiểm tra lỗi, khôi phục và điều chỉnh tốc độ truyền dữ liệu. Ví dụ, khi một máy tính gửi đi một gói tin và không nhận được thông báo từ máy nhận là đã nhận được gói tin đó thì nó sẽ gửi lại. Do đó, TCP trở thành giao thức để truyền thông tin như: hình ảnh tĩnh, tệp dữ liệu và trang web.

Ví dụ, trong quá trình trao đổi dữ liệu giữa hai máy tính theo giao thức TCP bao gồm các bước sau:
* 1. **Quá trình thiết lập kết nối**: Thiết lập kết nối giữa hai máy tính gửi và nhận.
* 2. **Quá trình trao đổi dữ liệu**: Bao gồm
    * Truyền dữ liệu: Dữ liệu được chia nhỏ thành các gói tin và được gắn thêm các thông tin khác (như: số thứ tự và số xác nhận). Gói tin được gửi đi qua mạng và máy nhận xác thực đã nhận được gói tin.
    * Kiểm tra lỗi và khôi phục: TCP sử dụng số thứ tự và số xác nhận để đảm bảo dữ liệu được truyền tải một cách đáng tin cậy. Trong trường hợp gói tin bị mất hoặc bị lỗi, thiết bị gửi sẽ thực hiện gửi lại gói tin.
* 3. **Quá trình kết thúc kết nối**: Sau khi quá trình trao đổi dữ liệu hoàn tất, quá trình kết thúc kết nối được thực hiện giữa hai thiết bị gửi và nhận.

## Giao thức IP
### a) Giao thức và địa chỉ IP
Giao thức Internet (IP) là một giao thức định tuyến và định danh các gói tin để có thể chuyển tiếp các gói tin qua các mạng đến đúng địa chỉ máy nhận. Các gói tin sẽ được gắn thêm các địa chỉ IP của máy gửi và máy nhận trước khi được gửi đi. Giao thức IP có chức năng phân phối các gói tin từ máy gửi đến máy nhận dựa trên địa chỉ IP được gắn với gói tin tương ứng. Dựa theo thông tin được đính kèm trong mỗi gói tin mà bộ định tuyến có thể chuyển tiếp gói tin đến đúng máy nhận.

**Địa chỉ IP** là một địa chỉ số được gán cho mỗi thiết bị khi kết nối vào mạng máy tính. Trong một mạng cục bộ, mỗi thiết bị bị kết nối vào mạng đều được gán một địa chỉ IP duy nhất. Hiện nay, địa chỉ IP có hai phiên bản chính: IPv4 và IPv6.

**IPv4** là phiên bản phổ biến và được sử dụng rộng rãi hiện nay. Địa chỉ IPv4 là một chuỗi số 32 bit nhị phân chia thành 4 cụm 8 bit hay 1 byte và được gọi là octet. Mỗi octet được biểu diễn dưới dạng thập phân và được ngăn cách nhau bằng dấu chấm. Ví dụ một địa chỉ IPv4 ở hệ nhị phân là: 10000010.00111001.00011110.00111000 tương ứng ở dạng thập phân là 130.57.30.56. Với một dãy dài 32 bit, có thể tạo được khoảng 2^32

xấp xỉ 4,3 tỉ địa chỉ IPv4 khác nhau. Do đó, số lượng địa chỉ IPv4 là không đủ cho tất cả thiết bị kết nối Internet trên thế giới hiện nay.
IPv6 là phiên bản mới hơn và được phát triển để đảm bảo nhu cầu lớn hơn về địa chỉ IP. IPv6 là một chuỗi 128 bit nhị phân, thường được biểu diễn dưới dạng thập lục phân, gồm 8 phần ngăn cách nhau bằng dấu hai chấm, ví dụ: 2620:0AB2:0D01:2042:0100:8C4D:D370:72B4. Với một dãy dài 128 bit, có thể tạo được 2<sup>128</sup> địa chỉ IPv6 khác nhau, lớn hơn rất nhiều so với IPv4 và cho phép tạo được hàng tỉ tỉ địa chỉ khác nhau.

Em hãy tìm địa chỉ IPv4 của máy tính em đang được sử dụng với sự hướng dẫn của giáo viên.

Một địa chỉ IPv4 bao gồm hai phần là địa chỉ mạng (Network ID) và địa chỉ máy (Host ID). Địa chỉ mạng xác định mạng mà thiết bị đang kết nối. Các máy tính trong một mạng LAN sẽ có cùng một địa chỉ mạng. Địa chỉ máy xác định thiết bị cụ thể trong một mạng.

### b) Hệ thống tên miền

Mỗi trang web tương ứng với một địa chỉ IP trong mạng Internet. Ví dụ: Trang web https://google.com.vn có địa chỉ IP tương ứng là 142.251.220.3. Do đó, có thể truy cập Google theo tên miền hay theo địa chỉ IP đều được.
Dễ thấy rằng người dùng mạng khó có thể nhớ được địa chỉ IP của những trang web mà họ muốn truy cập. Hệ thống tên miền DNS (Domain Name System) là cách định danh các máy tính trong mạng bằng những chữ gợi nhớ, tạo thuận lợi cho người dùng Internet.
Tên miền được phân thành các cấp, viết cách nhau một dấu chấm:
*   **Tên miền cấp cao nhất** là phần đuôi sau cùng của tên miền. Đây có thể là viết tắt tên một quốc gia (ví dụ: vn, us, uk,...) hay một tổ chức kinh tế – xã hội (ví dụ: com, org, net, edu, gov, info, biz, xyz, io, ai,...).
*   **Tên miền cấp hai** là phần ngay trước tên miền cấp cao nhất, ví dụ: google.com, facebook.com, youtube.com, amazon.com,...

* Tên miền cấp ba là phần trước của tên miền cấp hai, ví dụ: mail.google.com, news.google.com, drive.google.com,...
* Tên miền phụ là một phần thông tin mở rộng được thêm vào đầu tên miền của mỗi trang web. Tên miền phụ cho phép phân tách nội dung cho một chức năng cụ thể của trang web. Tên miền phụ phổ biến nhất là www, viết tắt của World Wide Web. Tên miền phụ này chứa trang chủ của trang web và các trang quan trọng nhất của nó.

## Luyện tập
Câu 1. **Giao thức mạng** là gì?
Câu 2. Em hãy mô tả chức năng của giao thức TCP và IP.
Câu 3. Theo em, giao thức TCP có được sử dụng cho vận chuyển dữ liệu thư điện tử hay không?

## Vận dụng
Em hãy xác định và ghi lại địa chỉ IP của 5 máy tính được kết nối mạng trong lớp học. Sau đó, em hãy cho biết điểm giống nhau và khác nhau của 5 địa chỉ này.

## Luyện tập
Em hãy cho biết mỗi câu sau là đúng hay sai:
a) Giao thức TCP thường được sử dụng cho các ứng dụng truyền tải dữ liệu thời gian thực.
b) Máy tính khi kết nối tới AP sẽ được cung cấp một địa chỉ IP.
c) Địa chỉ IPv4 bao gồm 48 bit.
d) Địa chỉ IPv6 bao gồm 128 bit.

## Tóm tắt bài học
* **Giao thức mạng** là một tập hợp các quy tắc được sử dụng để điều khiển truyền thông và trao đổi dữ liệu giữa các thiết bị trong mạng máy tính.
* Một số giao thức mạng Internet quan trọng hiện nay: IP, TCP, UDP, HTTP, FTP, SMTP.
* **Giao thức TCP** là giao thức đồng bộ, đảm bảo độ tin cậy cho quá trình kết nối và truyền nhận dữ liệu giữa hai thiết bị.
* **Giao thức IP** có chức năng định dạng và định danh các gói tin thông qua địa chỉ IP để đảm bảo các gói tin có thể gửi đi qua các mạng khác nhau và tới đúng địa chỉ máy nhận.
* **Địa chỉ IP** bao gồm IPv4 và IPv6 là một định danh duy nhất được sử dụng để xác định các thiết bị kết nối trong mạng máy tính.
