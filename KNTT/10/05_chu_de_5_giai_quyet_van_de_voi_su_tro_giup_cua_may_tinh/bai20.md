# Bài 20: CÂU LỆNH LẶP FOR

SAU BÀI NÀY EM SẼ:
*   Biết được ý nghĩa của vùng giá trị tạo bởi lệnh range().
*   Biết được chức năng của lệnh lặp for và cách dùng trong Python.

Em có thể đã gặp những trường hợp cần thực hiện một số công việc lặp đi lặp lại nhiều lần. Ví dụ, để kể tên tất cả các bạn trong lớp có 30 học sinh, em cần lần lượt đọc tên từng bạn; để đếm số lượng các số chia hết cho 3 trong khoảng từ 1 đến 50, em có thể kiểm tra lần lượt các số từ 1 đến 50 và ghi ra các số chia hết cho 3 (chẳng hạn 3, 6, 9,...), rồi đếm các số đó. Ngôn ngữ lập trình bậc cao có các câu lệnh cho phép viết một cách ngắn gọn các bước cần thực hiện lặp đi lặp lại để tạo thành một cấu trúc lập trình được gọi là cấu trúc lặp.

Em có thể xác định được trong mỗi ví dụ trên công việc nào cần phải lặp và được lặp lại bao nhiêu lần không?

## 1. LỆNH FOR

### Hoạt động 1: Làm quen với lệnh lặp for

Thực hiện đoạn chương trình sau trong chế độ gõ lệnh trực tiếp của Python để tính tổng 0 + 1 + ... + 9. Tổng này có giá trị bao nhiêu? Giải thích kết quả.

Đoạn chương trình gán S bằng 0, sau đó sử dụng vòng lặp `for` để biến `k` nhận các giá trị từ 0 đến 9. Trong mỗi lần lặp, giá trị của `k` được cộng vào `S`. Cuối cùng, in ra giá trị của `S`.
Kết quả output: 45

Trong đoạn chương trình trên, lệnh **range(10)** trả lại một **vùng giá trị** gồm 10 số 0, 1, 2, 3, 4, 5, 6, 7, 8, 9. Lệnh **for** sẽ thực hiện 10 lần lặp, mỗi lần lặp ứng với một giá trị k trong vùng giá trị trên. Sau lệnh lặp for trên, biến S sẽ có giá trị là tổng 0 + 1 + ... + 9 = 45.

Lệnh **range(n)** trả lại vùng giá trị gồm n số từ 0 đến n – 1. Cú pháp của lệnh lặp với số lần biết trước **for** trong Python như sau:

Cú pháp lệnh lặp `for` bao gồm từ khóa `for`, một biến lặp (ví dụ `<i>`), từ khóa `in`, hàm `range(n)` để xác định số lần lặp, và sau đó là một khối lệnh sẽ được thực hiện lặp lại.

Khi thực hiện, ở mỗi vòng lặp biến **i** sẽ được gán lần lượt các giá trị trong vùng giá trị của lệnh **range()** và thực hiện **\<khối lệnh>**.

Ví dụ 1. Tính tổng các số tự nhiên chẵn nhỏ hơn n, với n cho trước (n = 10).
Chương trình tính tổng các số chẵn nhỏ hơn n.
Điều kiện k là số chẵn là k%2 = 0

Ví dụ 2. Đếm số các số nguyên nhỏ hơn n (n = 20) và là bội của 3.
Chương trình đếm số các số nguyên nhỏ hơn n và là bội của 3.
Điều kiện k là bội của 3 là k%3 = 0

for là lệnh lặp với số lần biết trước. Số lần lặp thường được xác định bởi vùng giá trị của lệnh range().

Với giá trị n cho trước, so sánh giá trị S trong đoạn chương trình sau với tổng 1 + 2 + ... + n.
Chương trình tính tổng các số nguyên từ 1 đến n.

## 2. LỆNH RANGE

### Hoạt động 2 Tìm hiểu vùng giá trị xác định bởi lệnh range()

Quan sát các lệnh for sau và so sánh kết quả in ra để biết vùng giá trị được xác định bởi lệnh range(). Lưu ý, lệnh print() có thêm tham số để in bộ dữ liệu theo hàng ngang.
Vùng giá trị được tạo bởi `range(3,10)`:
3 4 5 6 7 8 9
Đây là vùng range(3,10)
Vùng giá trị được tạo bởi `range(0,15)`:
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
Đây là vùng range(0,15)

Lệnh tạo vùng giá trị **range()** có các dạng sau:
* `range(stop)` trả lại vùng giá trị từ 0 đến stop - 1.
* `range(start, stop)` trả lại vùng giá trị từ start đến stop - 1.
Ví dụ:
* `range(n)` cho vùng gồm các số 0, 1,..., n - 1.
* `range(1,n+1)` cho vùng gồm các số 1, 2,..., n.
* `range(0,99)` cho vùng giá trị gồm các số 0, 1, 2,..., 98.
* `range(100,1)` cho vùng rỗng.

Lệnh tạo vùng giá trị có cú pháp range(start, stop) trả lại vùng giá trị gồm các số nguyên liên tiếp từ start đến stop - 1.

Hãy biểu diễn các dãy sau đây bằng lệnh range().
a) 1, 2, 3,..., 50.
b) 5, 6, 7, 8, 9, 10.
c) 0, 1.
d) 10.

## THỰC HÀNH. Lệnh lặp for và lệnh range()

### Nhiệm vụ 1. Nhập số tự nhiên n từ bàn phím và in ra màn hình dãy các ước số của n theo chiều ngang màn hình. Ví dụ nếu n = 10 thì chương trình sẽ in ra dãy số 1, 2, 5, 10.

**Hướng dẫn**. Các ước số của n là các số tự nhiên k thoả mãn: n%k = 0. Muốn in các số trên một hàng ngang cần dùng thêm tham số end = " " trong lệnh print().

Chương trình có thể như sau:
Chương trình nhập một số tự nhiên n, sau đó dùng vòng lặp để duyệt qua các số từ 1 đến n và in ra các ước số của n, các số này được in trên cùng một hàng ngang và cách nhau bởi một khoảng trắng.

### Nhiệm vụ 2. Nhập số tự nhiên n từ bàn phím và đếm số các ước số thực sự của n.
**Ước số thực sự** của n là số tự nhiên k < n và là ước của n.

**Hướng dẫn**. Tương tự như chương trình ở nhiệm vụ 1, điểm khác là cần đếm số các ước số này và không tính n. Tạo một biến có tên count để đếm số các ước số thực sự của n.
Chương trình nhập một số tự nhiên n, sau đó dùng vòng lặp để duyệt qua các số từ 1 đến n-1. Nếu một số k là ước của n, biến count sẽ tăng lên 1. Cuối cùng, chương trình in ra tổng số ước số thực sự của n.

## LUYỆN TẬP

1.  Đoạn chương trình sau in ra kết quả gì?
    Chương trình nhập một số tự nhiên n, tính tổng S của các số từ 0 đến n, sau đó in ra bình phương của tổng S (S*S).

2.  Viết đoạn chương trình tính tích 1 × 2 × 3 ×...× n với n được nhập vào từ bàn phím.

## VẬN DỤNG

1.  Viết chương trình nhập từ bàn phím số tự nhiên n và in ra kết quả S = 1 + 1/2 + ... + 1/n.
2.  Viết chương trình nhập từ bàn phím số tự nhiên n và in ra kết quả là tổng sau:
    S = 1³ + 2³ + ... + n³.
