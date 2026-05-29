# Bài 1: LÀM QUEN VỚI NGÔN NGỮ LẬP TRÌNH BẬC CAO

**Học xong bài này, em sẽ:**
*   Giải thích được vì sao chúng ta cần lập trình và cần có ngôn ngữ lập trình bậc cao.
*   Giới thiệu được sơ lược về Python – một ngôn ngữ lập trình bậc cao thông dụng.
*   Bắt đầu chạy được một vài chương trình tính toán đơn giản trong môi trường Python.

Máy tính không hiểu được ngôn ngữ tự nhiên của con người. Vậy làm thế nào để chỉ dẫn cho máy tính thực hiện một việc nào đó?

## Ngôn ngữ lập trình bậc cao

Em đã biết một ngôn ngữ lập trình nào chưa? Nếu đã từng dùng một ngôn ngữ lập trình thì em đã dùng nó để làm gì?

Để điều khiển được máy tính, con người phải viết các chỉ dẫn để máy hiểu và thực hiện. Như vậy, cần phải có ngôn ngữ chung giữa con người và máy tính để ta viết các chỉ dẫn cho máy tính thực hiện được nhiệm vụ mà con người giao cho nó. Những ngôn ngữ như vậy được gọi là **ngôn ngữ lập trình**.

Ngôn ngữ lập trình trực quan như Scratch dễ dùng và thích hợp với các bạn nhỏ tuổi. Nhưng những ngôn ngữ lập trình bậc cao như: Python, C++, Java,... mới cung cấp tính năng chuyên nghiệp cho việc lập trình. Trong những ngôn ngữ như vậy, em sẽ viết các chỉ dẫn cho máy tính bằng cách gõ các kí tự trên bàn phím.

*   **Ngôn ngữ Scratch**: Một đoạn mã Scratch thực hiện phép tính cộng 3 + 5 và hiển thị kết quả là 8.
*   **Ngôn ngữ Python**: Một đoạn mã Python nhập `3 + 5` vào dòng lệnh và sau khi gõ Enter, kết quả `8` được hiển thị.

Hai chương trình này đều yêu cầu máy tính làm cùng một việc.

Do gần với ngôn ngữ tự nhiên, có cú pháp đơn giản, ngữ nghĩa đơn trị, số lượng từ khá ít (thường không quá 50 từ), nên các ngôn ngữ lập trình bậc cao dễ hiểu, dễ học. Ngày nay, nếu sử dụng được một ngôn ngữ lập trình bậc cao, em có thể ra lệnh cho mọi loại máy tính. Việc soạn thảo các hướng dẫn để máy tính hiểu và có thể thực hiện các yêu cầu của em được gọi là **lập trình** và sản phẩm soạn thảo được gọi là **chương trình**. Mỗi hướng dẫn để máy có thể thực hiện một công việc nào đó được gọi là **câu lệnh**.

Để sử dụng ngôn ngữ lập trình bậc cao, máy tính của em cần được trang bị **môi trường lập trình** trợ giúp em soạn thảo, kiểm tra từng câu lệnh đã viết đúng chưa, chuyển các câu lệnh sang ngôn ngữ mà máy hiểu được (gọi là **ngôn ngữ máy**) và theo đó máy thực hiện được.

## 2. Làm quen với Python

Quyển sách này sẽ sử dụng Python (phiên bản 3.9.0) để minh hoạ cho việc lập trình bằng ngôn ngữ lập trình bậc cao. Hiện nay, Python là một trong số các ngôn ngữ lập trình bậc cao phổ biến rộng rãi trên thế giới.

Python được Guido van Rossum (người Hà Lan) đề xuất và công bố năm 1991. Với nhiều ưu điểm, Python được dùng để phát triển các ứng dụng web, phần mềm ứng dụng, lập trình game, điều khiển robot, xử lí ảnh, phân tích dữ liệu,...

Hệ thống công cụ lập trình Python có thể dễ dàng tìm thấy trên Internet và tải về miễn phí. Sau khi thực hiện cài đặt chương trình (ví dụ cho Python phiên bản 3.9.0), trong cửa sổ Start sẽ xuất hiện các mục cho ta chọn loại dịch vụ của Python.

Nếu chọn mục **IDLE (Python 3.9 64-bit)**, ta sẽ có cửa sổ Shell, cho phép viết và thực hiện ngay các biểu thức hoặc câu lệnh.

Cửa sổ Python Shell hiển thị thông tin phiên bản của Python và một dấu nhắc lệnh (`>>>`) để người dùng nhập và thực thi các câu lệnh Python trực tiếp.

Ví dụ 1. Để máy tính hiển thị trên màn hình dòng chữ "Python là một trong những ngôn ngữ lập trình bậc cao", ta có thể sử dụng câu lệnh **print ()** như ở Hình 4.

Gõ dòng này từ bàn phím:
Mô tả: Đoạn mã Python hiển thị chuỗi "Python là một trong những ngôn ngữ lập trình bậc cao".
Kết quả:
Python là một trong những ngôn ngữ lập trình bậc cao

Ví dụ 2. Tốc độ ánh sáng là 299 792 458 m/s và thời gian ánh sáng đi từ Mặt Trời tới Trái Đất là 8 phút 20 giây. Ta có thể dùng Python để viết chương trình tính được khoảng cách từ Mặt Trời đến Trái Đất như ở Hình 5.

Gõ dòng này từ bàn phím:
Mô tả: Đoạn mã Python tính toán tích của tốc độ ánh sáng (299792458) với thời gian (8 phút 20 giây, được chuyển đổi sang giây: 8*60 + 20).
Lưu ý: Dấu phép tính nhân được viết là `*`.
Kết quả:
149896229000

Lưu ý:
*   Python phân biệt chữ hoa và chữ thường.
*   Dãy kí tự muốn in ra màn hình bằng câu lệnh **print ()** cần được đặt trong cặp dấu nháy đơn (hoặc nháy kép).

Ai cũng có thể lập trình được
*   Hãy học một số quy tắc và các câu lệnh cơ bản.
*   Hãy thực hành và luyện tập để phát triển kĩ năng.

## Luyện tập
Bài 1. Em hãy viết câu lệnh `print()` sao cho khi thực hiện câu lệnh này trên màn hình sẽ hiển thị dòng chữ “Học lập trình với Python để ra lệnh cho máy tính”.
Bài 2. Đường cao tốc Hà Nội – Lào Cai (kí hiệu CT.05) có chiều dài 264 km. Một ô tô chạy với tốc độ trung bình toàn tuyến là 70 km/h. Em hãy dùng ngôn ngữ lập trình Python ra lệnh cho máy tính để xác định thời gian ô tô đó đi từ Lào Cai về Hà Nội.

Năm 2020 nước ta sản xuất được 247 tỉ kWh điện. Sản lượng điện của nước ta được dự báo sẽ tiếp tục tăng nhanh với tốc độ trung bình là 8,6%/năm. Em hãy dùng ngôn ngữ lập trình Python ra lệnh cho máy tính để tính sản lượng điện của nước ta sản xuất được trong năm 2021 theo dự báo.

Câu 1. Trong các câu sau đây, những câu nào đúng?
1) Chương trình là một bản chỉ dẫn cho máy tính làm việc, được viết bằng một ngôn ngữ lập trình.
2) Chỉ có một ngôn ngữ lập trình bậc cao là Python.
3) Lập trình bằng Python có thể đưa ra các thông báo bằng tiếng Việt.
4) Môi trường lập trình hỗ trợ người lập trình phát hiện ra câu lệnh viết sai ngữ pháp.

Câu 2. Trong các câu sau đây, những câu nào phù hợp với lí do nên học lập trình?
Em học lập trình để:
1) Giỏi tiếng Anh.
2) Làm phong phú kiến thức cá nhân.
3) Có thể truy cập Internet.
4) Sử dụng được các phần mềm văn phòng.
5) Điều khiển máy tính giải nhiều loại bài toán sẽ gặp trong thực tế.
6) Sau này trở thành chuyên gia trong lĩnh vực tin học.

## Tóm tắt bài học
*   **Chương trình máy tính** là một dãy các câu lệnh mà máy tính có thể “hiểu” và thực hiện được.
*   **Ngôn ngữ lập trình** là ngôn ngữ dùng để viết các chương trình máy tính.
*   **Python** là một trong những ngôn ngữ lập trình bậc cao thông dụng.
*   Trong cửa sổ Shell của Python có thể thực hiện ngay từng câu lệnh và thấy được kết quả.

# BÀI TÌM HIỂU THÊM

## CÀI ĐẶT HỆ THỐNG CÔNG CỤ LẬP TRÌNH PYTHON

Em hoàn toàn có thể tự cài đặt hệ thống công cụ lập trình Python (gọi tắt là Python) lên máy tính của mình. Để cài đặt Python lên máy tính, em cần chọn đúng phiên bản phù hợp với hệ điều hành mà máy tính đã cài đặt. Theo từng bước trong hướng dẫn ở Hình 1 sau đây, em sẽ tải về và cài đặt được Python lên máy đang sử dụng hệ điều hành Windows.

*   Bước 1. Trong trang web *http://python.org* chọn mục **Downloads**.
*   Bước 2. Chọn phiên bản cần tải về máy.
*   Bước 3. Thực hiện chương trình cài đặt Python lên máy.

Kết quả của Bước 2 là một tệp với đuôi .exe đã được tải về trong một thư mục trên máy của em (ví dụ, tệp có tên “python-3.9.0.exe”). Hãy nháy đúp chuột vào tên tệp này để thực hiện chương trình cài đặt Python lên máy.

Khi trên màn hình xuất hiện cửa sổ với thông báo “Setup was successful” tức là em đã tải về và cài đặt thành công Python cho máy tính. Em có thể gọi Python từ cửa sổ Start để bắt đầu lập trình.

Mách nhỏ: Để cài đặt Python lên máy sử dụng hệ điều hành Mac em làm như sau:

*   Bước 1. Truy cập vào địa chỉ *https://www.python.org/* và chọn **Downloads**, lựa chọn phiên bản phù hợp, tải tệp “Python.pkg” về máy.
*   Bước 2. Kích hoạt tệp “Python.pkg” trong thư mục **Downloads**, chọn **Continue** sau đó chọn **Install**.
