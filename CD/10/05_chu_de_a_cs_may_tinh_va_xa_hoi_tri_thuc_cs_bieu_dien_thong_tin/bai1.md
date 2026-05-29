# Bài 1: HỆ NHỊ PHÂN VÀ ỨNG DỤNG

## Học xong bài này, em sẽ:
*   Hiểu và thực hiện được các phép toán cơ bản NOT, AND, OR và XOR theo từng bit và cho các dãy bit.
*   Biết **hệ nhị phân** (hệ đếm cơ số 2) là gì.
*   Chuyển đổi được số đếm hệ nhị phân sang giá trị thập phân và ngược lại.
*   Biết được các **phép toán bit** là cơ sở để thực hiện các tính toán số học nhị phân.
*   Giải thích được ứng dụng của hệ nhị phân trong tin học.

## Luyện tập

Máy tính tính toán với các bit, các toán hạng là bit và kết quả cũng là bit.
a) Em sẽ chọn kết quả phép cộng hai bit 1+1 là 0, 1 hay 10? Tại sao?
b) Em sẽ chọn kết quả phép nhân hai bit 1*1 là 0, 1 hay 10? Tại sao?

# Bài 1: Các phép toán bit
## 1. Các phép toán bit
### a) Định nghĩa

Để đánh giá một món ăn, ta có thể dựa vào các tiêu chí ngon hay không, rẻ hay không. Em hãy phân biệt "ngon và rẻ" với "ngon hoặc rẻ" với "hoặc ngon hoặc rẻ".

Mọi dữ liệu trong máy tính đều đã số hoá tức là có dạng dãy các bit. Mọi thao tác xử lí dữ liệu cuối cùng đều dẫn đến xử lí các bit. Các phép toán bit là nền tảng hoạt động của máy tính. Bốn phép toán bit cơ sở là NOT, AND, OR và XOR. Các phép toán này cũng gọi là phép toán logic với các bit.

### Phép toán NOT
NOT là phép toán có một toán hạng. Kí hiệu toán hạng đầu vào là x. Bảng kết quả phép toán NOT cho kết quả trái ngược với đầu vào.
Ba phép toán còn lại AND, OR và XOR có hai toán hạng.

### Phép toán AND
Kí hiệu hai toán hạng đầu vào là x, y.
Phép toán AND còn gọi là phép nhân logic.
**AND** cho kết quả là 1 khi và chỉ khi cả hai bit toán hạng đều là 1; bằng 0 trong những trường hợp còn lại.

### Phép toán OR và XOR
Kí hiệu hai toán hạng đầu vào là x, y.
Phép toán OR còn gọi là phép cộng logic.
Phép toán **XOR** là viết tắt của eXclusive OR nghĩa là phép OR loại trừ hay "độc quyền" không lấy cả hai.
Phép toán **OR** cho kết quả là 0 khi và chỉ khi cả hai bit toán hạng đều là 0.
Phép toán **XOR** cho kết quả là 1 khi và chỉ khi hai bit toán hạng trái ngược nhau.

### b) Các phép toán bit với dãy bit
Mỗi phần tử dữ liệu số hoá là một dãy bit liền nhau với độ dài ấn định trước. Bốn phép toán cơ sở NOT, AND, OR và XOR được áp dụng cho các dãy bit theo cách sau:
* Phép toán một toán hạng NOT được thực hiện với từng bit trong dãy. Phép toán **NOT** cũng gọi là phép bù (*complement*). Bit chỉ nhận hai giá trị 0 hoặc 1, nên phần bù của 0 là 1, phần bù của 1 là 0.
* Các phép toán hai toán hạng AND, OR và XOR được thực hiện với từng cặp bit từ hai toán hạng đóng cột tương ứng với nhau. Các dãy bit có cùng độ dài.
Các ví dụ minh hoạ:
