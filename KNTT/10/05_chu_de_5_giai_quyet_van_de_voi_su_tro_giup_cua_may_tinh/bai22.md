# Bài 22: KIỂU DỮ LIỆU DANH SÁCH

SAU BÀI NÀY EM SẼ:
*   Biết được kiểu dữ liệu **danh sách** (list), cách khởi tạo và truy cập từng phần tử của danh sách.
*   Biết và thực hiện được cách duyệt các phần tử của danh sách bằng lệnh for.
*   Thực hành được một số phương thức đơn giản trên dữ liệu danh sách.

Em đã được học những kiểu dữ liệu cơ bản của Python như số nguyên, số thực, xâu kí tự, kiểu dữ liệu logic. Tuy nhiên, khi em cần lưu một dãy các số hay một danh sách học sinh thì cần kiểu dữ liệu dạng **danh sách** (còn gọi là dãy hay **mảng**). Kiểu dữ liệu danh sách được dùng nhiều nhất trong Python là kiểu list.

Em hãy tìm một số dữ liệu kiểu danh sách thường gặp trên thực tế.

## 1. KIỂU DỮ LIỆU DANH SÁCH

### Hoạt động 1 Khởi tạo và tìm hiểu dữ liệu kiểu danh sách

Khởi tạo dữ liệu danh sách như thế nào? Cách truy cập, thay đổi giá trị và xoá một phần tử trong danh sách như thế nào?

#### Ví dụ 1. Quan sát các lệnh sau để tìm hiểu kiểu dữ liệu danh sách.
Đoạn mã khởi tạo một danh sách A với các số nguyên, và một danh sách B với các kiểu dữ liệu hỗn hợp (số thực, số nguyên, xâu kí tự). Sau đó, truy cập phần tử đầu tiên của danh sách A và phần tử thứ ba của danh sách B.
Output:
```
1
'Python'
```
Có thể truy cập từng phần tử của danh sách thông qua chỉ số. Chỉ số của list đánh số từ 0.

Kiểu dữ liệu danh sách trong Python được khởi tạo như sau:
`<tên list> = [<v1>, <v2>, ..., <vn>]`

Trong đó các giá trị `<vk>` có thể có kiểu dữ liệu khác nhau (số nguyên, số thực, xâu kí tự...). Ta có thể truy cập từng phần tử của danh sách thông qua chỉ số. Chỉ số bắt đầu từ 0.

Việc chỉ số hoá từng phần tử của danh sách cho thấy, có thể dùng danh sách để biểu diễn dữ liệu tương tự như kiểu mảng trong nhiều ngôn ngữ lập trình bậc cao khác. Tuy nhiên, **danh sách** của Python có một khác biệt quan trọng, đó là nó có thể gồm các phần tử có kiểu dữ liệu khác nhau.

#### Ví dụ 2. Quan sát các lệnh sau để biết cách thay đổi hoặc xoá phần tử của danh sách.
Đoạn mã khởi tạo một danh sách A với các số nguyên, sau đó sử dụng hàm `len()` để tính độ dài của danh sách đó.
Output:
```
5
```
Lệnh `len()` tính độ dài của danh sách.

Sau khi đã khởi tạo danh sách, chúng ta có thể thay đổi các giá trị của từng phần tử bằng lệnh gán hoặc xoá phần tử bằng lệnh `del`.
*Mô tả mã Python:*
Lệnh gán giá trị mới cho phần tử ở chỉ số 1 của danh sách A.
```
A[1] = "One"
```
Kết quả hiển thị danh sách A:
```
[1, 'One', 3, 4, 5]
```
Lệnh xóa phần tử ở chỉ số 4 của danh sách A.
```
del A[4]
```
Kết quả hiển thị danh sách A sau khi xóa:
```
[1, 'One', 3, 4]
```

#### Ví dụ 3. Quan sát các lệnh sau để biết cách tạo danh sách rỗng (có độ dài 0) và các phép toán ghép danh sách (phép +).
*Mô tả mã Python:*
Lệnh tạo một danh sách rỗng có độ dài bằng 0.
```
a = []
```
Kết quả hiển thị độ dài của danh sách a:
```
0
```
Các phép ghép hai danh sách.
```
[1,2] + [3,4,5,6]
```
Kết quả hiển thị danh sách sau khi ghép:
```
[1, 2, 3, 4, 5, 6]
```

*   **List** là kiểu dữ liệu danh sách (dãy, mảng) trong Python. Tạo list bằng lệnh gán với các phần tử trong cặp dấu ngoặc `[]`. Các phần tử của danh sách có thể có các kiểu dữ liệu khác nhau. Truy cập hoặc thay đổi giá trị của từng phần tử thông qua chỉ số: `<danh sách>[<chỉ số>]`
*   Chỉ số của danh sách bắt đầu từ 0 đến `len()` – 1, trong đó `len()` là lệnh tính độ dài danh sách.

1.  Cho danh sách A = [1, 0, "One", 9, 15, "Two", True, False]. Hãy cho biết giá trị các phần tử:
    a) A[0]
    b) A[2]
    c) A[7]
    d) A[len(A)]
2.  Giả sử A là một danh sách các số, mỗi lệnh sau thực hiện gì? (Giả sử ban đầu A = [1, 2, 3, 4, 5, 6])
    a) A = A + [10]
    b) del A[0]
    c) A = [100] + A
    d) A = A[1]*25

## 2. DUYỆT CÁC PHẦN TỬ CỦA DANH SÁCH

### Hoạt động 2: Dùng lệnh for để duyệt danh sách

Quan sát các lệnh sau để biết cách dùng lệnh `for` duyệt lần lượt các phần tử của một danh sách.

#### Ví dụ 1. Duyệt và in ra từng phần tử của danh sách.

*Mô tả mã Python:*
Tạo danh sách A và sử dụng vòng lặp `for` để duyệt qua các chỉ số của danh sách A, sau đó in từng phần tử ra màn hình, cách nhau bởi dấu cách. Biến i chạy trên vùng chỉ số từ 0 đến `len(A)` – 1.
```
A = [1,2,3,4,5]
for i in range(len(A)):
    print(A[i],end = " ")
```
Kết quả hiển thị:
```
1 2 3 4 5
```

#### Ví dụ 2. Duyệt và in một phần của danh sách.

Đoạn mã Python khởi tạo một danh sách A và sau đó duyệt qua các phần tử từ chỉ số 2 đến chỉ số 4 (không bao gồm 5), in từng phần tử ra màn hình, cách nhau bởi một khoảng trắng.
Kết quả:
1 5 6

Hai ví dụ trên cho thấy dùng lệnh for kết hợp với lệnh range() để duyệt từng phần tử của danh sách.

Có thể duyệt lần lượt các phần tử của danh sách bằng lệnh for kết hợp với vùng giá trị của lệnh range().

1. Giải thích các lệnh ở mỗi câu sau thực hiện công việc gì?
   a) Đoạn mã Python khởi tạo biến S bằng 0. Sau đó, nó duyệt qua tất cả các phần tử trong danh sách A. Nếu phần tử đó lớn hơn 0, nó sẽ được cộng vào S. Cuối cùng, giá trị của S được in ra. Đoạn mã này tính tổng các số dương trong danh sách A.
   b) Đoạn mã Python khởi tạo biến C bằng 0. Sau đó, nó duyệt qua tất cả các phần tử trong danh sách A. Nếu phần tử đó lớn hơn 0, biến C sẽ tăng lên 1. Cuối cùng, giá trị của C được in ra. Đoạn mã này đếm số lượng các số dương trong danh sách A.
2. Cho dãy các số nguyên A, viết chương trình in ra các số chẵn của A.

## 3. THÊM PHẦN TỬ VÀO DANH SÁCH

Python có những lệnh đặc biệt để thêm phần tử vào một danh sách. Các lệnh này được thiết kế riêng cho kiểu dữ liệu danh sách và còn được gọi là phương thức (method) của danh sách.

### Hoạt động 3 Tìm hiểu lệnh thêm phần tử cho danh sách

Quan sát các lệnh sau đây để biết cách thêm phần tử vào một danh sách bằng phương thức append().

Ví dụ. Thêm phần tử vào cuối danh sách.

Đoạn mã Python khởi tạo một danh sách A với hai phần tử. Sau đó, nó sử dụng phương thức `append()` để thêm giá trị 10 vào cuối danh sách A. Cuối cùng, nó in ra danh sách A.
Chú ý cách dùng phương thức append(): gõ tên biến danh sách, dấu ".", sau đó gõ append.
Kết quả:
[1, 2, 10]

*   Python có một số lệnh dành riêng (phương thức) cho dữ liệu kiểu danh sách. Cú pháp các lệnh đó như sau: **<danh sách>.<phương thức>**
*   Lệnh thêm phần tử vào cuối danh sách là **<danh sách>.append()**.

1. Sau khi thêm một phần tử vào danh sách A bằng lệnh append() thì độ dài danh sách A thay đổi như thế nào?
2. Danh sách A sẽ như thế nào sau các lệnh sau?
   Đoạn mã Python khởi tạo một danh sách A. Sau đó, nó thêm giá trị 100 vào cuối danh sách A bằng phương thức `append()`. Cuối cùng, nó xóa phần tử ở chỉ số 1 khỏi danh sách A bằng lệnh `del`.

# THỰC HÀNH

## Khởi tạo, nhập dữ liệu, thêm phần tử cho danh sách

### Nhiệm vụ 1. Nhập số n từ bàn phím, sau đó nhập danh sách n tên các bạn lớp em và in ra danh sách các tên đó, mỗi tên trên một dòng.
**Hướng dẫn**. Chương trình yêu cầu nhập số tự nhiên n, sau đó nhập từng tên trong danh sách, dùng phương thức append() để đưa dần vào danh sách.
**Chú ý**: Vì vùng giá trị của lệnh range(n) bắt đầu từ 0 nên trong thông báo nhập cần viết là str(i+1) để bắt đầu từ 1.
Chương trình có thể như sau:
*   Mã nguồn khởi tạo một danh sách rỗng `dsLop`.
*   Nhập số lượng học sinh `n` từ người dùng.
*   Sử dụng vòng lặp `for` để lặp `n` lần:
    *   Nhập tên học sinh, có hiển thị số thứ tự (bắt đầu từ 1).
    *   Thêm tên đã nhập vào danh sách `dsLop` bằng phương thức `append()` ہو۔
*   In ra dòng chữ "Danh sách học sinh đã nhập:".
*   Sử dụng vòng lặp `for` để duyệt qua danh sách `dsLop` và in từng tên học sinh trên một dòng riêng biệt.

### Nhiệm vụ 2. Nhập một dãy số từ bàn phím. Tính tổng, trung bình của dãy và in dãy số trên một hàng ngang.
**Hướng dẫn**. Tương tự nhiệm vụ 1, chỉ khác là nhập số nguyên nên dùng lệnh int() để chuyển đổi dữ liệu.
*   Mã nguồn khởi tạo một danh sách rỗng `A` và một biến `T` (tổng) bằng 0.
*   Nhập số lượng phần tử `n` (số tự nhiên) từ người dùng.
*   Sử dụng vòng lặp `for` để lặp `n` lần:
    *   Nhập một số nguyên `num` từ người dùng, có hiển thị số thứ tự (bắt đầu từ 1).
    *   Thêm số `num` vào danh sách `A` bằng phương thức `append()`.
    *   Cộng `num` vào biến `T`.
*   In ra dòng chữ "Dãy số đã nhập:".
*   Sử dụng vòng lặp `for` để duyệt qua danh sách `A` và in từng phần tử trên cùng một hàng ngang, cách nhau bởi dấu cách.
*   In ra tổng `T` với nhãn "Tổng:".
*   In ra giá trị trung bình `T/n` với nhãn "Trung bình:".

## LUYỆN TẬP
1.  Viết lệnh xóa phần tử cuối cùng của danh sách A bằng lệnh **del**.
2.  Có thể thêm một phần tử vào đầu danh sách được không? Nếu có thì nêu cách thực hiện.

## VẬN DỤNG
Cho dãy số A. Viết chương trình tính giá trị và chỉ số của phần tử lớn nhất của A. Tương tự với bài toán tìm phần tử nhỏ nhất.
