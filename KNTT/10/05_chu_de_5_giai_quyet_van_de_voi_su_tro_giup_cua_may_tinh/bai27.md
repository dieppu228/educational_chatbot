# Bài 27: THAM SỐ CỦA HÀM

SAU BÀI NÀY EM SẼ:
*   Biết cách thiết lập các tham số của hàm. Hiểu được cách truyền giá trị thông qua đối số hàm.
*   Biết viết chương trình có sử dụng chương trình con.

Quan sát các lệnh sau và cho biết sự khác nhau giữa **tham số** (parameter) và **đối số** (argument).

### Tham số
Mô tả đoạn mã định nghĩa hàm `f_sum` nhận ba tham số `a, b, c` và trả về tổng của chúng.

### Đối số
Mô tả đoạn mã gán giá trị `5` cho `x` và `3` cho `y`. Sau đó, gọi hàm `f_sum` với các đối số `10`, `x`, `y`. Kết quả trả về là `18`.

## 1. THAM SỐ VÀ ĐỐI SỐ CỦA HÀM

### Hoạt động 1 Phân biệt tham số và đối số

Quan sát ví dụ sau, tìm hiểu cách dữ liệu được truyền qua tham số vào hàm. Thảo luận để giải thích kết quả.

**Ví dụ**. Cách truyền dữ liệu qua tham số.

Mô tả đoạn mã định nghĩa hàm `f` nhận ba tham số `a, b, c` và trả về tổng của chúng.
*   Hàm `f()` có ba tham số **a, b, c**.

Mô tả đoạn mã gọi hàm `f` với các đối số `1, 2, 3`. Kết quả trả về là `6`.
*   Hàm `f()` được gọi với ba giá trị cụ thể.

Mô tả đoạn mã gán giá trị `10, 20, 5` lần lượt cho các biến `x, y, z`. Sau đó, gọi hàm `f` với các đối số `x, y, z`. Kết quả trả về là `35`.
*   Hàm `f()` được gọi với ba biến đã có giá trị.

Mô tả đoạn mã gọi hàm `f` với các đối số `a, b, c` mà các biến này chưa được định nghĩa, dẫn đến lỗi `NameError`.
*   Lời gọi hàm bị lỗi nếu các tham số được truyền vào chưa có giá trị.

Giải thích:
*   Dòng 1: Hàm f() đã được định nghĩa với ba tham số a, b, c. Chú ý trong định nghĩa hàm, các tham số được coi như biến.
*   Dòng 3: Hàm f() được gọi với ba giá trị cụ thể là 1, 2, 3. Các giá trị được truyền qua tham số được gọi là đối số. Đối số tại dòng 3 là các số cụ thể.
*   Dòng 6: Hàm f() được gọi với ba biến x, y, z, đã được gán giá trị (dòng 5). Các biến được truyền qua tham số được gọi là đối số, kết quả trả lại là x + y + z.
*   Dòng 10: Hàm f() được gọi với ba biến a, b, c không xác định giá trị nên lời gọi hàm f(a, b, c) báo lỗi do không xác định được giá trị của a, b, c.

**Tham số** của hàm được định nghĩa khi khai báo hàm và được dùng như biến trong định nghĩa hàm. **Đối số** là giá trị được truyền vào khi gọi hàm. Khi gọi hàm, các **tham số (parameter)** sẽ được truyền bằng giá trị thông qua **đối số (argument)** của hàm, số lượng giá trị được truyền vào hàm bằng với số tham số trong khai báo hàm.

1.  Một hàm khi khai báo có một tham số, nhưng khi gọi hàm có thể có hai đối số được không?
2.  Giả sử hàm f có hai tham số x, y khi khai báo, hàm sẽ trả lại giá trị x + 2y. Lời gọi hàm f(10,a) có lỗi hay không?

## 2. CÁCH SỬ DỤNG CHƯƠNG TRÌNH CON

### Hoạt động 2 Khi nào nên sử dụng chương trình con?
Bài toán đưa ra là viết chương trình chính yêu cầu nhập số tự nhiên n từ bàn phím và in các số nguyên tố nhỏ hơn hoặc bằng n ra màn hình. Trong phần thực hành của Bài 26 em đã biết hàm prime(n) kiểm tra số n có là số nguyên tố.

Em sẽ viết chương trình giải bài toán này như thế nào?

### Ví dụ 1.
Việc kiểm tra một số có là số nguyên tố được lặp đi lặp lại từ 1 đến n và do đó nên sử dụng hàm prime(n) để kiểm tra sẽ giúp chương trình cấu trúc rõ ràng và dễ hiểu hơn.

Chương trình hoàn chỉnh giải bài toán trên có thể được viết như sau:

Đoạn mã định nghĩa hàm `prime(n)` để đếm số ước số của n (không bao gồm chính n) bằng cách lặp từ 1 đến n-1. Biến C lưu trữ số lượng ước số tìm được và k là biến đếm.

### Ví dụ 2. Chương trình sử dụng chương trình con.

Cho trước hai dãy số B, C, chương trình chính cần tính tổng các số hạng dương của mỗi dãy này. Chúng ta sẽ thiết lập hàm tongduong(A) để tính tổng các số hạng lớn hơn 0 của một dãy A. Chương trình chính sẽ gọi hàm tongduong(A).

Chương trình có thể như sau:

Đoạn mã Python định nghĩa một hàm để kiểm tra một số có phải là số nguyên tố hay không, trả về True nếu là số nguyên tố, False nếu không phải. Sau đó, chương trình chính yêu cầu người dùng nhập một số tự nhiên n và in ra tất cả các số nguyên tố trong khoảng từ 1 đến n (bao gồm cả n).

Đoạn mã Python định nghĩa hàm `tongduong(A)` để tính tổng các phần tử dương trong danh sách A.

Chương trình chính sử dụng hàm `tongduong`.

*   Sử dụng hàm `tongduong` tính tổng các số dương của dãy A
*   Kết quả `tongduong(A)` là 17.
*   Sử dụng hàm `tongduong` tính tổng các số dương của dãy B
*   Kết quả `tongduong(B)` là 11.
*   In ra dãy B.

Sử dụng chương trình con có thể giúp phân chia việc giải một bài toán lớn thành giải quyết các bài toán nhỏ và phát huy được tinh thần làm việc nhóm; Chương trình chính có cấu trúc rõ ràng, dễ hiểu hơn; Nếu cần hiệu chỉnh, phát triển và nâng cấp cũng thuận tiện hơn.

1.  Sử dụng hàm prime, em hãy viết chương trình in ra các số nguyên tố trong khoảng từ m đến n, với m, n là hai số tự nhiên và 1 < m < n.
2.  Em hãy nêu một công việc/bài toán nào đó mà có thể sử dụng hàm để giải.

# THỰC HÀNH
Truyền giá trị cho đối số của hàm.

## Nhiệm vụ 1. Thiết lập hàm f_sum(A, b)
có chức năng tính tổng các số của danh sách A theo quy định sau:
*   Nếu **b = 0** thì tính tổng các số của danh sách A.
*   Nếu **b khác 0** thì chỉ tính tổng các số dương của A.

### Hướng dẫn.
Chương trình luôn kiểm tra giá trị của đối số **b** khi tính tổng các số của danh sách A.

Chương trình có thể như sau:
Đoạn mã này định nghĩa hàm `f_sum(A, b)`. Hàm khởi tạo biến tổng `S` bằng 0. Nó lặp qua từng phần tử `x` trong danh sách `A`.
*   Nếu `b` bằng 0, nó cộng `x` vào `S`.
*   Nếu `b` không bằng 0, nó kiểm tra nếu `x` lớn hơn 0 thì cộng `x` vào `S`.
Cuối cùng, hàm trả về giá trị của `S`.

## Nhiệm vụ 2. Thiết lập hàm f_dem(msg, sep)
có chức năng đếm số các từ của một xâu **msg** với kí tự tách từ là **sep**.

Ví dụ:
*   `f_dem("Mùa thu lịch sử", " ")` Trả lại giá trị 4.
*   `f_dem("Mùa thu lịch sử", "-")` Trả lại giá trị 1.

### Hướng dẫn.
Để tách xâu **msg** thành các từ, chúng ta dùng lệnh **split()**. Tham số **sep** chính là tham số của lệnh **split()**.

Chương trình có thể như sau:
Đoạn mã này định nghĩa hàm `f_dem(msg, sep)`. Hàm sử dụng phương thức `split(sep)` để tách xâu `msg` thành một danh sách các từ dựa trên kí tự phân tách `sep`. Sau đó, nó trả về độ dài của danh sách các từ này, tức là số lượng từ.

## Nhiệm vụ 3. Thiết lập hàm merge_str(s1,s2)
với **s1**, **s2** là hai xâu cần gộp.
Hàm này sẽ gộp hai xâu **s1**, **s2** theo cách, lấy lần lượt từng kí tự của **s1**, **s2** đưa vào xâu kết quả. Nếu có một xâu hết kí tự thì đưa phần còn lại của xâu dài hơn vào xâu kết quả. Ví dụ nếu s1 = "1111", s2 = "0000", c = 1 thì xâu kết quả là "10101010".

### Hướng dẫn.
Gọi S là xâu kết quả sau khi gộp hai xâu s1 và s2, chương trình có thể như sau:
Hàm `merge_str(s1, s2)` nhận vào hai xâu `s1` và `s2`, sau đó ghép các kí tự của chúng vào một xâu `S` mới. Hàm này thực hiện ghép xen kẽ các kí tự từ `s1` và `s2` cho đến hết phần chung, sau đó tiếp tục ghép các kí tự còn lại của xâu dài hơn vào `S`.

## LUYỆN TẬP
1.  Thiết lập hàm **power(a,b,c)** với a, b, c là số nguyên. Hàm trả lại giá trị (a+b)c.
2.  Viết chương trình thực hiện: Nhập n số tự nhiên từ bàn phím, hai số cách nhau bởi dấu cách. Tính và in ra tổng của các số này.

## VẬN DỤNG
1.  Viết chương trình thực hiện: Nhập hai số tự nhiên từ bàn phím, hai số cách nhau bởi dấu phẩy, in ra **ước chung lớn nhất (ƯCLN)** của hai số.
2.  Thiết lập hàm **change()** có hai tham số là xâu **ho_ten** và số **c**. Hàm sẽ trả lại xâu kí tự **ho_ten** là chữ in hoa nếu c = 0. Nếu tham số c khác 0 thì hàm trả lại xâu **ho_ten** là chữ in thường.
    Gợi ý: Sử dụng các phương thức **s.upper()** và **s.lower()** để chuyển đổi các kí tự của xâu s sang chữ in hoa và in thường.
