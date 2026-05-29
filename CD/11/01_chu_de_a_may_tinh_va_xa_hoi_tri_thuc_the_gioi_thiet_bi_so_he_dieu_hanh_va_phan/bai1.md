# Bài 1: BÊN TRONG MÁY TÍNH

Học xong bài này, em sẽ:
*   Nhận biết được sơ đồ của các mạch logic AND, OR, NOT; giải thích được vai trò của các mạch logic trong thực hiện các tính toán nhị phân.
*   Nêu được tên, nhận diện được hình dạng, mô tả được chức năng và giải thích được đơn vị đo hiệu năng của các bộ phận chính bên trong máy tính.

Em hãy cho biết CPU là gì và làm nhiệm vụ gì trong máy tính?

## 1. Các cổng logic và tính toán nhị phân

### a) Cổng logic
Trong máy tính, một bóng bán dẫn chỉ thực hiện được chức năng bật hoặc tắt mạch đơn giản, tương ứng với hai giá trị 0 và 1. Mỗi cách kết hợp các bóng bán dẫn tạo ra một **cổng logic**. Các cổng logic là thành phần cơ bản thực hiện mọi tính toán trong máy tính.

Quan sát mạch điện ở Hình 1. Mạch có hai công tắc A và B phối hợp để điều khiển đèn F. Đèn chỉ sáng khi cả hai công tắc cùng đóng.
Nếu quy ước: công tắc mở tương ứng với mức "0", công tắc đóng tương ứng với mức "1"; đèn tắt tương ứng với mức "0", đèn sáng tương ứng với mức "1". Em hãy:
1) Nêu giá trị đúng tại dấu ? cho mỗi hàng của đầu ra F.
2) Nhận xét về hoạt động của mạch điện.

Ta thấy rằng: Để đèn F sáng thì cả công tắc A và công tắc B đồng thời phải đóng, nếu một trong hai công tắc mở thì đèn F tắt. Hoạt động của mạch điện minh hoạ chức năng của cổng logic AND và bảng hoạt động tương ứng của mạch điện được gọi là bảng chân lí. Cổng AND thực hiện chức năng nhân logic.

Để thực hiện các phép toán logic khác, ta cần có thêm nhiều loại cổng logic. Dựa trên quan hệ giữa đầu ra và đầu vào, các cổng logic được đặt tên tương ứng là cổng AND, cổng OR, cổng NOT, cổng XOR,... dưới đây liệt kê một số loại cổng logic thông dụng.

*Bảng 1. Một số cổng logic thông dụng*

**Cổng logic: AND**
*   Biểu thức logic: F = A AND B = A . B
*   Bảng chân lí:
    A B F
    0 0 0
    0 1 0
    1 0 0
    1 1 1
*   Đặc điểm: Đầu ra bằng 1, khi tất cả đầu vào bằng 1.

**Cổng logic: OR**
*   Biểu thức logic: F = A OR B = A + B
*   Bảng chân lí:
    A B F
    0 0 0
    0 1 1
    1 0 1
    1 1 1
*   Đặc điểm: Đầu ra bằng 1, khi hoặc một trong các đầu vào bằng 1.

**Cổng logic: NOT**
*   Biểu thức logic: F = NOT A = Ā
*   Bảng chân lí:
    A F
    0 1
    1 0
*   Đặc điểm: Đầu ra có giá trị đảo lại giá trị đầu vào.

**Cổng logic: XOR**
*   Biểu thức logic: F = A XOR B = A ⊕ B
*   Bảng chân lí:
    A B F
    0 0 0
    0 1 1
    1 0 1
    1 1 0
*   Đặc điểm: Đầu ra bằng 1 khi hai đầu vào khác nhau.

### b) Thực hiện phép toán nhị phân với mạch logic

Các phép toán trên hệ nhị phân cũng có nguyên tắc thực hiện giống như trên hệ thập phân. Ví dụ nguyên tắc cơ bản để cộng hai số nhị phân:
0 + 0 = 0 (Bằng 0, nhớ 0)
1 + 0 = 1 (Bằng 1, nhớ 0)
0 + 1 = 1 (Bằng 1, nhớ 0)
1 + 1 = 10 (Bằng 10 (Bằng 0, nhớ 1))

*Hình 2. Phép cộng hai bit trong hệ nhị phân*

Giả sử ta cộng hai số nhị phân 1 bit là A với B được tổng là S và nhớ là C. Vì là các số nhị phân nên A và B chỉ nhận các giá trị là 0 hoặc 1, lập bảng các trường hợp có thể xảy ra với các đầu vào A, B và điền giá trị đầu ra S, C tương ứng.

*Bảng 2. Bảng chân lí mạch cộng hai số nhị phân 1 bit*

| Đầu vào | Đầu ra |
|---|---|
| A | B | S | C |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

So sánh Bảng 2 với bảng chân lí của các cổng logic trong Bảng 1, dễ thấy tổng S = A XOR B và nhớ C = A AND B. Từ đó, ta lập được sơ đồ mạch logic để thực hiện phép cộng hai số nhị phân 1 bit. Phép cộng hai số nhị phân dài nhiều bit thực hiện bằng cách cộng lần lượt từng cặp bit từ phải sang trái và có bit nhớ (C_in) mang sang cột kề bên trái.

**Mạch cộng đầy đủ (FA – Full Adder)** có ba đầu vào là A, B và bit nhớ mang sang C_in; có hai đầu ra là bit tổng S và bit nhớ C_out để phân biệt với C_in đầu vào. Mạch cộng đầy đủ là ghép nối hai mạch cộng 1 bit.

Như vậy, bằng cách kết hợp các cổng logic AND, XOR, máy tính có thể thực hiện được phép tính cộng nhị phân. Tương tự, các cổng logic cơ bản cũng có thể kết hợp để tạo thành các mạch logic thực hiện tất cả các tính toán nhị phân khác.

## 2. Những bộ phận chính bên trong máy tính

Theo em, bộ phận nào của máy tính là quan trọng nhất?

Máy tính có nhiều loại như: máy tính để bàn, máy tính xách tay, máy tính bảng. Bên trong thân máy tính được cấu thành từ các bộ phận chính gồm: **bảng mạch chính**, **CPU**, **RAM**, **ROM**, **thiết bị lưu trữ**. Tốc độ và dung lượng của chúng ảnh hưởng lớn tới hiệu năng của máy.

**Bảng mạch chính** có để cắm CPU, ROM, các khe cắm RAM, các khe cắm ổ cứng và một số khe cắm khác. Bảng mạch chính đóng vai trò làm nền giao tiếp giữa CPU, RAM và các linh kiện điện tử khác phục vụ cho việc kết nối với các thiết bị ngoại vi.

CPU (Central Processing Unit – bộ xử lí trung tâm) đóng vai trò bộ não của máy tính; đảm nhiệm công việc tìm nạp lệnh, giải mã lệnh và thực thi lệnh cho máy tính.

RAM (Random Access Memory – bộ nhớ truy cập ngẫu nhiên) lưu trữ dữ liệu tạm thời trong quá trình tính toán của máy tính. Dữ liệu sẽ bị mất khi máy tính bị mất điện hoặc khởi động lại.

ROM (Read Only Memory – bộ nhớ chỉ đọc) lưu trữ chương trình giúp khởi động các chức năng cơ bản của máy tính.

**Thiết bị lưu trữ** dùng để lưu trữ dữ liệu lâu dài và không bị mất đi khi máy tính tắt nguồn. Ngày nay, máy tính thường sử dụng ổ cứng HDD, ổ cứng SSD hoặc ổ USB để lưu trữ dữ liệu.

**Dung lượng lưu trữ dữ liệu của máy tính** là tổng dung lượng của ổ cứng HDD, ổ cứng SSD gắn sẵn bên trong máy tính, không bao gồm dung lượng lưu trữ của RAM. Hiện nay, dung lượng lưu trữ của máy tính có thể lên tới hàng TB.

## 3) Hiệu năng của máy tính

Hiệu năng của máy tính phụ thuộc vào thông số kĩ thuật của từng bộ phận và sự đồng bộ giữa chúng. Có thể đánh giá nhanh hiệu năng của máy thông qua tốc độ CPU, dung lượng bộ nhớ RAM.

Thông số kĩ thuật cần quan tâm của CPU gồm:
*   **Tốc độ của CPU**: đo bằng Hz (Hertz), biểu thị số chu kì xử lí mỗi giây mà CPU có thể thực hiện được. Tốc độ này càng cao thì máy tính chạy càng nhanh. Hiện nay, CPU có tốc độ hàng GHz (1 GHz = 10⁹ Hz).
*   **Số lượng nhân hay lõi (core)**: CPU có cấu tạo gồm một hoặc nhiều nhân (còn gọi là lõi) vật lí. Với cùng một công nghệ sản xuất, CPU có nhiều nhân hơn thì hiệu năng, khả năng đa nhiệm và tốc độ xử lí tốt hơn.

Thông số kĩ thuật cần quan tâm của RAM là dung lượng. Dung lượng của RAM được đo bằng đơn vị Byte. Hiện nay, máy tính có RAM với dung lượng hàng GB (1 GB = 2³⁰ Byte). Máy tính có RAM với dung lượng lớn hơn thì hiệu năng cao hơn.

## Luyện tập
Câu 1. Em hãy nêu giá trị thích hợp tại dấu ? cho hai cột S và C_out để hoàn thành bảng chân lí cho mạch cộng đầy đủ.

Câu 2. Hãy nêu tên một số thành phần chính bên trong máy tính và cho biết chức năng của nó.

Em hãy sắp xếp thứ tự ưu tiên khi chọn mua máy tính:
a) Ổ cứng dung lượng lớn.
b) RAM dung lượng lớn.
c) CPU tốc độ cao.

Trong các câu sau, những câu nào đúng?
a) **CPU** có tốc độ càng cao thì máy tính có hiệu năng càng cao.
b) Dung lượng **ổ cứng** đo bằng GHz.
c) Các bộ nhớ **RAM** ngày nay có dung lượng hàng TB.
d) Dung lượng **RAM** có ảnh hưởng tới hiệu năng của máy tính.

## Tóm tắt bài học
*   Bằng cách kết hợp các **cổng logic cơ bản** để tạo thành các **mạch logic**, máy tính có thể thực hiện được các **tính toán nhị phân**.
*   Các bộ phận chính bên trong thân máy tính gồm: **bảng mạch chính**, **CPU**, **RAM**, **ROM**, **thiết bị lưu trữ**.
*   **Hiệu năng** của máy tính được quyết định bởi hiệu năng của từng thành phần, trong đó **CPU**, **RAM** có vai trò quan trọng nhất. Ngày nay, **CPU** có tốc độ hàng **GHz**, bộ nhớ **RAM** có dung lượng hàng **GB**, **ổ cứng** có dung lượng hàng **TB**.
