# Bài 26: HÀM TRONG PYTHON

SAU BÀI NÀY EM SẼ:
*   Biết được chương trình con là hàm.
*   Biết cách tạo hàm.

Các chương trình giải những bài toán thực tế phức tạp thường có rất nhiều dòng lệnh, trong đó có không ít những khối lệnh tương ứng với một số thao tác được lặp đi lặp lại nhiều lần ở những vị trí khác nhau. Để đỡ công viết đi viết lại các khối lệnh đó, trong tổ chức chương trình viết bằng ngôn ngữ lập trình bậc cao, người ta thường gom các khối lệnh như vậy thành những chương trình con. Khi đó, trong chương trình người ta chỉ cần thay cả khối lệnh bằng một lệnh gọi chương trình con tương ứng. Trong Python, các hàm chính là các chương trình con.

Em có thể kể tên một số hàm trong số các lệnh đã học hay không? Các hàm đó có những đặc điểm chung gì?

## 1. MỘT SỐ HÀM THIẾT KẾ SẴN CỦA PYTHON

### Hoạt động 1: Tìm hiểu một số hàm của Python

Quan sát một số câu lệnh trong Bảng 26.1 và cho biết những câu lệnh này có điểm chung gì.

Trước tiên, về hình thức, em có thể thấy các lệnh trên đều có các dấu mở đóng ngoặc đi sau tên lệnh. Tiếp đó, khi viết trong chương trình, bên trong các dấu ngoặc, nói chung, em có thể cần ghi thêm các tham số là các đại lượng, các biến hoặc thậm chí, trong một số trường hợp, cả các biểu thức. Ví dụ:

*   Lệnh in một xâu kí tự ra màn hình.
*   Lệnh gán `x` bằng cách chuyển xâu `"52"` thành số nguyên 52.
*   Lệnh trả lại kiểu dữ liệu của biến `y`.

Trong một số trường hợp bên trong dấu ngoặc có thể bỏ trống. Ví dụ, lệnh yêu cầu nhập vào một xâu kí tự bất kì và gán cho biến `x`.

Các lệnh trong Bảng 26.1 chính là các chương trình con được thiết kế sẵn của Python, cho phép người dùng tuỳ ý sử dụng trong các chương trình của riêng mình.
Trong các ví dụ trên, xâu kí tự bên trong ngoặc của các hàm `int()` và `print()` là **tham số của hàm**. Cú pháp câu lệnh gọi hàm trong Python có dạng chung như sau:
`<tên hàm>(<danh sách tham số hàm>)`

Python cung cấp sẵn nhiều hàm thực hiện những công việc khác nhau cho phép người dùng được tuỳ ý sử dụng khi viết chương trình bằng các câu lệnh gọi hàm tương ứng.

Mô tả tham số và giá trị trả lại của mỗi hàm sau: `float()`, `str()`, `len()`, `list()`.

## 2. THIẾT LẬP CÁC HÀM TỰ ĐỊNH NGHĨA

Ngoài các hàm thiết kế sẵn, Python còn cho phép người dùng tự thiết lập các hàm của riêng mình (còn gọi là các hàm tự định nghĩa).

### Hoạt động 2: Cách thiết lập hàm trong Python

Quan sát các ví dụ sau để biết cách viết hàm.

### Ví dụ 1. Cách viết hàm có trả lại giá trị.

*   Đoạn mã định nghĩa hàm `inc` nhận một tham số `n` và trả về `n+1`.
    *   Tên hàm: inc.
    *   Tham số hàm: số n.
    *   Giá trị trả lại: số n + 1.
*   Lời gọi hàm `inc` với tham số là `3`.
    *   Kết quả: `4`

### Ví dụ 2. Cách viết hàm không trả lại giá trị.

*   Đoạn mã định nghĩa hàm `thong_bao` nhận một tham số `msg`, in ra chuỗi "Xin chào bạn" kèm theo giá trị của `msg` và không trả về giá trị nào.
    *   Tên hàm: thong_bao.
    *   Tham số hàm: xâu kí tự msg.
    *   Giá trị trả lại: không có.
*   Lời gọi hàm `thong_bao` với tham số là `"Trần Quang Minh"`.
    *   Kết quả: `Xin chào bạn Trần Quang Minh`

**Hàm** trong Python được định nghĩa bằng từ khoá **def**, theo sau là tên hàm (tên hàm sẽ theo quy tắc đặt tên định danh). Hàm có thể có hoặc không có tham số. **Khối lệnh** mô tả hàm được viết sau dấu ":" và viết lùi vào, thẳng hàng. Hàm có thể có hoặc không có **giá trị trả lại** sau từ khoá **return**.

Cú pháp thiết lập hàm có trả lại giá trị.

Mô tả: Định nghĩa một hàm với tên hàm và các tham số. Khối lệnh của hàm thực hiện các tác vụ và cuối cùng sử dụng lệnh `return` để trả về một giá trị.
Cần có lệnh **return <giá trị>**. Hàm sẽ kết thúc khi gặp lệnh **return** và trả lại **<giá trị>**.

Cú pháp thiết lập hàm không trả lại giá trị.

Mô tả: Định nghĩa một hàm với tên hàm và các tham số. Khối lệnh của hàm thực hiện các tác vụ và có thể kết thúc bằng lệnh `return` mà không kèm giá trị nào.
Lệnh **return** không có giá trị trả lại. Hàm kết thúc khi gặp lệnh **return**. Nếu hàm không trả lại giá trị thì có thể không cần lệnh **return**.

Để thiết lập hàm trả lại giá trị, câu lệnh **return** trong khai báo hàm cần có **<giá trị>** đi kèm. Để thiết lập hàm không trả lại giá trị có thể dùng lệnh **return** không có **<giá trị>** hoặc không cần có **return**.

Quan sát các hàm sau, giải thích cách thiết lập và chức năng của mỗi hàm.

a)
Mô tả: Hàm `Nhap_xau()` không có tham số. Hàm này yêu cầu người dùng nhập một chuỗi thông qua hàm `input()` và lưu vào biến `msg`. Sau đó, hàm trả về giá trị của biến `msg`.

b)
Mô tả: Hàm `Inday(n)` nhận một tham số `n`. Hàm này sử dụng một vòng lặp `for` để lặp từ `k = 0` đến `n-1`, và trong mỗi lần lặp, in giá trị của `k` ra màn hình, các giá trị được ngăn cách bởi dấu cách và nằm trên cùng một dòng.

## THỰC HÀNH
Thiết lập hàm trong Python.

Nhiệm vụ 1. Viết hàm yêu cầu người dùng nhập họ tên rồi đưa lời chào ra màn hình.

**Hướng dẫn.** Chương trình có thể như sau:
Mô tả: Hàm `meeting()` không có tham số. Hàm này yêu cầu người dùng nhập họ tên vào biến `ten` bằng hàm `input()`, sau đó in ra lời chào "Xin chào " cùng với tên đã nhập. Cuối cùng, hàm được gọi để thực thi.

Nhiệm vụ 2. Viết hàm **prime(n)** với tham số là số tự nhiên n và trả lại True nếu n là số nguyên tố, trả lại False nếu n không phải là số nguyên tố.

**Hướng dẫn.** Số nguyên tố là số tự nhiên lớn hơn 1, không có ước nào ngoài 1 và chính nó. Để thiết lập hàm **prime(n)** chúng ta cần tính số ước thực sự của n (từ 1 đến n – 1). Biến C dùng để đếm số các ước thực sự của n. Khi đó, n sẽ là số nguyên tố khi và chỉ khi C = 1.
Hàm **prime(n)** và chương trình có thể được thiết lập như sau:
Mô tả: Hàm `prime(n)` khởi tạo biến `C = 0` (để đếm ước) và `k = 1`.
Ban đầu đặt k = 1. Vòng lặp sẽ tăng k lên 1 đơn vị cho đến khi k = n thì dừng. Với mỗi k, kiểm tra nếu k là ước của n thì tăng C lên 1.

Mô tả chức năng của đoạn mã trên:
Đoạn mã này là một phần của thuật toán kiểm tra tính nguyên tố. Nó lặp qua các số `k` nhỏ hơn `n`. Nếu `n` chia hết cho `k`, nó tăng biến đếm `C`. Sau khi vòng lặp kết thúc, nếu `C` bằng 1, hàm trả về `True`, nếu không thì trả về `False`.

## LUYỆN TẬP

1.  Viết hàm với tham số là số tự nhiên n in ra các số là **ước nguyên tố** của n.
    Gợi ý: Sử dụng hàm `prime()` trong phần thực hành.
2.  Viết hàm `numbers(s)` đếm số các chữ số có trong xâu s.
    Ví dụ `numbers("0101abc")` = 4.

## VẬN DỤNG

1.  Trong khi viết hàm có thể có nhiều lệnh **return**. Quan sát hàm sau và giải thích ý nghĩa của những lệnh return. Hàm này có điểm gì khác so với hàm `prime()` đã được mô tả trong phần thực hành.

    Mô tả chức năng của đoạn mã trên:
    Hàm `prime(n)` kiểm tra xem số `n` có phải là số nguyên tố hay không.
    *   Nếu `n` nhỏ hơn 2, hàm trả về `False` (vì số nguyên tố phải lớn hơn hoặc bằng 2).
    *   Hàm khởi tạo biến đếm `C` bằng 0 và `k` bằng 2.
    *   Vòng lặp `while` kiểm tra các số `k` từ 2 đến `n-1`. Nếu `n` chia hết cho bất kỳ `k` nào trong khoảng này, hàm ngay lập tức trả về `False` (vì `n` có ước ngoài 1 và chính nó, không phải số nguyên tố).
    *   Nếu vòng lặp kết thúc mà không tìm thấy ước nào, hàm trả về `True` (vì `n` không chia hết cho bất kỳ số nào từ 2 đến `n-1`, tức là nó là số nguyên tố).

2.  Viết chương trình yêu cầu nhập từ bàn phím một xâu kí tự, sau đó thông báo:
    *   Tổng số các kí tự là chữ số của xâu.
    *   Tổng số các kí tự là chữ cái tiếng Anh trong xâu.
    Viết hàm cho mỗi yêu cầu trên.
