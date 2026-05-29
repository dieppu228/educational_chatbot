# Bài 16: NGÔN NGỮ LẬP TRÌNH BẬC CAO VÀ PYTHON

SAU BÀI NÀY EM SẼ:
*   Biết khái niệm ngôn ngữ lập trình bậc cao và ngôn ngữ lập trình bậc cao Python.
*   Phân biệt được chế độ gõ lệnh trực tiếp và chế độ soạn thảo chương trình trong môi trường lập trình Python.
*   Biết cách tạo và thực hiện một chương trình Python.

Em hãy quan sát các đoạn chương trình được viết bằng các ngôn ngữ lập trình khác nhau và cho biết câu lệnh trong ngôn ngữ nào dễ hiểu nhất?

*   **Ngôn ngữ máy**: Một khối mã nhị phân gồm các chuỗi bit.
*   **Hợp ngữ (Assembly)**: Một khối mã hợp ngữ sử dụng các lệnh viết tắt như RESETA, CTLREG, LDA, STA, JMP.
*   **Ngôn ngữ Python**: Một đoạn mã Python cho phép nhập một dãy N số từ bàn phím và tính tổng của chúng, sau đó in kết quả ra màn hình.

## 1. NGÔN NGỮ LẬP TRÌNH BẬC CAO

### Hoạt động 1 Tìm hiểu ngôn ngữ bậc cao
1. Ngôn ngữ lập trình là gì? Có những loại ngôn ngữ lập trình nào?
2. Hãy kể tên một số ngôn ngữ lập trình bậc cao mà em biết.

Các lệnh viết bằng **ngôn ngữ máy** ở dạng mã nhị phân hay **hợp ngữ** sử dụng một số từ viết tắt (thường là tiếng Anh) không thuận tiện cho việc viết hoặc hiểu chương trình. Khó khăn đó đã được giảm bớt khi lập trình bằng **ngôn ngữ bậc cao** với các câu lệnh được viết gần với ngôn ngữ tự nhiên. Tuy nhiên, để máy tính có thể hiểu và thực hiện, các chương trình đó cần được dịch sang ngôn ngữ máy nhờ một chương trình chuyên dụng được gọi là **chương trình dịch**.

Hiện nay đã có nhiều ngôn ngữ lập trình bậc cao khác nhau, trong số đó Java, C/C++, Python,... là những ngôn ngữ lập trình thông dụng nhất.

Python là ngôn ngữ lập trình bậc cao do Guido van Rossum, người Hà Lan tạo ra và ra mắt lần đầu năm 1991. Các câu lệnh của Python có cú pháp đơn giản. Môi trường lập trình Python dễ sử dụng, không phụ thuộc vào hệ điều hành, chạy trên nhiều loại máy tính, điện thoại thông minh, robot giáo dục,... Python có mã nguồn mở nên thu hút nhiều nhà khoa học cùng phát triển. Nhờ có các thư viện chương trình phong phú về trí tuệ nhân tạo, phân tích dữ liệu, kĩ thuật robot,... Python là ngôn ngữ lập trình được dùng phổ biến trong nghiên cứu và giáo dục.

*   **Ngôn ngữ lập trình bậc cao** có các câu lệnh được viết gần với ngôn ngữ tự nhiên giúp cho việc đọc, hiểu chương trình dễ dàng hơn.
*   Python là một ngôn ngữ lập trình bậc cao phổ biến trong nghiên cứu và giáo dục.

Theo em, viết chương trình bằng loại ngôn ngữ lập trình nào dễ nhất?
A. Ngôn ngữ máy. B. Hợp ngữ. C. Ngôn ngữ lập trình bậc cao.

## 2. MÔI TRƯỜNG LẬP TRÌNH PYTHON

### Hoạt động 2 Làm quen với môi trường lập trình Python
1.  Tìm hiểu cách viết và thực hiện các lệnh trong môi trường lập trình Python.
2.  Phân biệt chế độ gõ lệnh trực tiếp và chế độ soạn thảo chương trình của Python.

Sau khi khởi động, màn hình làm việc của Python có dạng tương tự như sau:

Mô tả màn hình làm việc của Python (IDLE Shell): Màn hình hiển thị phiên bản Python đang sử dụng và các thông tin khởi động. Có dấu nhắc `>>>` là nơi người dùng có thể nhập lệnh. Sau khi nhập lệnh xong, nhấn phím Enter để thực hiện lệnh.

Phần mềm Python là một môi trường lập trình cho phép soạn thảo chương trình bằng ngôn ngữ Python, hỗ trợ gỡ lỗi, phân tích cú pháp dòng lệnh và thực hiện các chương trình Python (chương trình hoàn chỉnh hoặc từng câu lệnh). Môi trường lập trình Python có hai chế độ:
*   Chế độ gõ lệnh trực tiếp thường được dùng để tính toán và kiểm tra nhanh các lệnh.
*   Chế độ soạn thảo dùng để viết các chương trình có nhiều dòng lệnh.

### a) Chế độ gõ lệnh trực tiếp

Trong một phiên làm việc với Python, em có thể gõ lệnh trực tiếp sau dấu nhắc `>>>` và nhấn phím Enter để thực hiện lệnh như sau:
`>>> <lệnh Python>`

### b) Chế độ soạn thảo

Trong môi trường lập trình Python, chúng ta cũng có thể soạn thảo chương trình hoàn chỉnh bằng cách chọn **File/New File** để mở ra màn hình soạn thảo chương trình tương tự như sau:

Viết mỗi lệnh trên một dòng. Khi viết xong chương trình thì có thể lưu tệp và chọn **Run** để thực hiện.

Chú ý. Người ta có thể soạn thảo chương trình Python bằng phần mềm soạn thảo văn bản hoặc phần mềm lập trình Python như Wingware, PyCharm, Thonny, Visual Studio,...

Môi trường lập trình của Python có hai chế độ: **chế độ gõ lệnh trực tiếp** và **chế độ soạn thảo**.

1.  Dấu nhắc chính là con trỏ soạn thảo chương trình Python. Đúng hay sai?
2.  Việc thực hiện câu lệnh ở chế độ gõ lệnh trực tiếp và chế độ soạn thảo có điểm gì giống nhau, khác nhau?

## 3. MỘT SỐ LỆNH PYTHON ĐẦU TIÊN

### Hoạt động 3 Làm quen với câu lệnh của Python

Quan sát một số lệnh trong chế độ gõ lệnh trực tiếp để biết chức năng của các lệnh này.

### Ví dụ 1. Các lệnh đầu tiên.

*   Nhập số nguyên 5, Python trả về 5.
    *   Khi nhập 5, Python hiểu rằng đó là số nguyên 5.
*   Nhập số thực 2.6, Python trả về 2.6.
    *   Nếu nhập 2.6 thì Python tự động nhận ra đó là số thực 2.6.
*   Nhập chuỗi "hoc sinh lop 10", Python trả về chuỗi 'hoc sinh lop 10'.
    *   Còn nếu gõ các chữ giữa cặp dấu nháy kép "" thì Python hiểu là xâu kí tự.

Python tự nhận biết kiểu dữ liệu và thực hiện các phép toán ngay trên dòng lệnh.

### Ví dụ 2. Các lệnh với phép toán.

*   Nhập phép cộng 3 + 7, Python trả về 10.
    *   Các phép toán thông thường với số bao gồm phép cộng (+), trừ (-), nhân (*) và chia (/).
*   Nhập phép nhân 12*5, Python trả về 60.

### Ví dụ 3. Lệnh print().

*   `print(12)`
    *   Kết quả: `12`
    *   Mô tả: Lệnh `print(12)` trong Python hiển thị số nguyên 12.
*   `print(10,3.4 + 4.1, "hoà bình")`
    *   Kết quả: `10 7.5 hoà bình`
    *   Mô tả: Lệnh `print(10,3.4 + 4.1, "hoà bình")` trong Python hiển thị số nguyên 10, kết quả của phép toán 3.4 + 4.1, và chuỗi "hoà bình".
    *   Chú ý: Nếu lệnh print() nhiều giá trị thì các dữ liệu này sẽ được đưa ra trên một dòng, giữa các dữ liệu sẽ có dấu cách.
*   `print("Dãy ba số chẵn:",2,4,6)`
    *   Kết quả: `Dãy ba số chẵn: 2 4 6`
    *   Mô tả: Lệnh `print("Dãy ba số chẵn:",2,4,6)` trong Python hiển thị chuỗi "Dãy ba số chẵn:" theo sau là các số nguyên 2, 4, 6.
*   `print("3 + 7 =",3+7)`
    *   Kết quả: `3 + 7 = 10`
    *   Mô tả: Lệnh `print("3 + 7 =",3+7)` trong Python hiển thị chuỗi "3 + 7 =" theo sau là kết quả của phép toán 3+7.
    *   Chú ý: Lệnh print() có thể tính toán và đưa ra kết quả của biểu thức.

Trong Python, lệnh **print()** có chức năng đưa dữ liệu ra (xuất dữ liệu). Mặc định dữ liệu sẽ được in ra màn hình. Lệnh print() cho phép in một hoặc nhiều giá trị ra màn hình. Cú pháp lệnh print() như sau:

`print(v1, v2,..., vn)`

trong đó v1, v2,..., vn là các giá trị cần đưa ra màn hình.

*   Khi nhập giá trị số hoặc xâu kí tự từ dòng lệnh, Python tự nhận biết kiểu dữ liệu.
*   Python có thể thực hiện các phép toán thông thường với số, phân biệt số thực và số nguyên.
*   Lệnh print() có chức năng in dữ liệu ra màn hình, có thể in ra một hoặc nhiều giá trị đồng thời.

1.  Kết quả của mỗi lệnh sau là gì? Kết quả đó có kiểu dữ liệu nào?
    *   `>>> 5/2`
    *   `>>> 12 + 1.5`
    *   `>>> "Bạn là học sinh lớp 10"`
    *   `>>> 10 + 7/2`
2.  Lệnh sau sẽ in ra kết quả gì?
    *   `>>> print("13 + 10*3/2 – 3*2 = ", 13 + 10*3/2 – 3*2)`

## THỰC HÀNH

**Nhiệm vụ:** Sử dụng chế độ soạn thảo chương trình của Python để tạo, nhập và chạy chương trình đầu tiên có tên **Bai1.py** như sau:

**Bai1.py**
*   `# Chương trình đầu tiên`
    *   Mô tả: Dòng này là một chú thích trong Python, không ảnh hưởng đến việc thực thi chương trình.
*   `print("Xin chào!")`
    *   Mô tả: Lệnh `print("Xin chào!")` trong Python hiển thị chuỗi "Xin chào!" ra màn hình.
    *   Chú ý: Kí hiệu **#** là vị trí bắt đầu dòng chú thích lệnh của Python.

**Hướng dẫn.**

Bước 1: Nháy đúp chuột vào biểu tượng của Python để khởi động.

Bước 2: Chọn chế độ soạn thảo chương trình của môi trường lập trình Python: Trong môi trường lập trình Python, chọn File/New.
Bước 3: Nhập nội dung chương trình.
Bước 4: Chọn **File/Save** hoặc nhấn tổ hợp phím **Ctrl + S** để lưu tệp.
Bước 5: Chọn **Run/Run module** hoặc nhấn phím **F5** để thực hiện chương trình.
Bước 6: Để kết thúc một phiên làm việc, nháy nút (x) ở góc trên bên phải màn hình hoặc gõ lệnh quit() hoặc lệnh exit() rồi nhấn phím ENTER. Ví dụ:

## LUYỆN TẬP
1. Hãy viết lệnh để tính giá trị các biểu thức sau trong chế độ gõ lệnh trực tiếp của Python:
   a) 10 + 13
   b) 20 – 7
   c) 3 × 10 – 16
   d) 12/5 + 13/6
2. Các lệnh sau có lỗi không? Vì sao?
3. Viết các lệnh in ra màn hình thông tin như sau:
   a) 1 × 3 × 5 × 7 = 105.
   b) Bạn Hoa năm nay 16 tuổi.

## VẬN DỤNG
1. Ngoài cách viết xâu kí tự giữa cặp dấu nháy đơn hoặc nháy kép còn có thể viết xâu được viết giữa cặp ba dấu nháy kép. Nếu một xâu được viết giữa cặp ba dấu nháy kép thì chúng ta có thể dùng phím **Enter** để xuống dòng ở giữa xâu. Hãy thực hiện lệnh sau và quan sát kết quả:
2. Viết chương trình Python in ra màn hình bảng nhân trong phạm vi 10.
