# Bài 31: THỰC HÀNH VIẾT CHƯƠNG TRÌNH ĐƠN GIẢN

SAU BÀI NÀY EM SẼ:
*   Thực hành viết chương trình đơn giản bằng ngôn ngữ Python.
*   Thực hành được các bước gỡ rối chương trình bằng công cụ debug – thiết lập điểm dừng và chạy theo từng lệnh.

## Nhiệm vụ 1.

Viết chương trình nhập từ bàn phím số tự nhiên n, kiểm tra n có phải là **số nguyên tố** hay không. Nếu n là **hợp số** thì in ra kết quả phân tích n thành tích các thừa số nguyên tố. Chú ý số 1 không là nguyên tố và cũng không là hợp số.

### Hướng dẫn.

Sử dụng biến danh sách NT để lưu các **thừa số nguyên tố** của n. Chương trình sẽ thiết lập danh sách NT chỉ khi n > 1. Kết quả của chương trình sẽ như sau:
*   Nếu n = 1 thì danh sách NT sẽ rỗng.
*   Nếu n > 1 thì danh sách NT không rỗng. Độ dài danh sách len(NT) sẽ bằng 1 khi và chỉ khi n là số nguyên tố.
*   Nếu len(NT) > 1 thì chương trình sẽ in ra khai triển n thành tích các thừa số nguyên tố, khai triển này sẽ có dạng: n = p₁×p₂×...×pₖ.

phantichnt.py

Chương trình này thực hiện các bước sau:
1.  Nhập một số tự nhiên `n` từ bàn phím.
2.  Khởi tạo biến `m` bằng `n` và một danh sách rỗng `NT` để lưu trữ các thừa số nguyên tố.
3.  Sử dụng một vòng lặp `while` để tìm các thừa số nguyên tố:
    *   Bắt đầu với `k = 2`.
    *   Trong vòng lặp `while m > 1`, tiếp tục tìm ước số `k` cho `m`.
    *   Nếu `m` chia hết cho `k`, `k` được thêm vào danh sách `NT` và `m` được chia cho `k`.
    *   Nếu `m` không chia hết cho `k`, `k` được tăng lên 1.
4.  Sau khi phân tích xong, chương trình kiểm tra độ dài của danh sách `NT` để đưa ra kết luận:
    *   Nếu danh sách `NT` rỗng (nghĩa là `n=1`), thông báo `n` không là số nguyên tố.
    *   Nếu độ dài danh sách `NT` bằng 1 (nghĩa là `n` là số nguyên tố), thông báo `n` là số nguyên tố.
    *   Nếu độ dài danh sách `NT` lớn hơn 1 (nghĩa là `n` là hợp số), in ra `n` dưới dạng tích các thừa số nguyên tố đã tìm được.

Chạy chương trình với công cụ gỡ lỗi của phần mềm lập trình. Thiết lập một điểm dừng tại dòng 20 của chương trình như sau:

Đoạn mã Python thực hiện việc phân tích một số nguyên `n` (được gán cho `m`) thành các thừa số nguyên tố. Biến `k` bắt đầu từ 2 và tăng dần để tìm ước số. Mỗi khi tìm thấy một ước số nguyên tố `k` của `m`, `k` được thêm vào danh sách `NT` và `m` được cập nhật bằng `m // k`.

Điểm dừng của chương trình được đặt trước lệnh `m = m//k`, sau khi `k` là ước số nguyên tố tiếp theo được phát hiện và đưa vào danh sách `NT`. Quá trình gỡ lỗi được tiến hành để kiểm tra sự thay đổi các biến `n, m, k` có đúng theo thuật toán hay không.

Đoạn mã Python tiếp theo của chương trình thực hiện việc kiểm tra số lượng thừa số nguyên tố đã tìm được (`count = len(NT)`) để xác định tính chất của số `n`.
*   Nếu `count` bằng 0, chương trình in ra thông báo rằng `n` không là số nguyên tố.
*   Nếu `count` bằng 1, chương trình in ra thông báo rằng `n` là số nguyên tố.
*   Phần `else` (không hiển thị đầy đủ) sẽ xử lý trường hợp `n` có nhiều hơn một thừa số nguyên tố.

Khi chạy, chương trình sẽ chạy và dừng lại trước điểm dừng (trên màn hình dòng dừng lại được đánh dấu). Nháy nút để chạy tiếp chương trình.

Mỗi lần chương trình dừng lại có thể quan sát các biến `n, m, k` để kiểm tra tính đúng đắn của chương trình.

Thiết lập bảng theo dõi các giá trị trung gian k, m, n, NT sẽ như sau, giả sử giá trị nhập ban đầu của n = 100:

## Nhiệm vụ 2.

Viết chương trình nhập từ bàn phím ba số thực a, b, c và tìm nghiệm của phương trình bậc hai: ax² + bx + c = 0. Chương trình cần xét đầy đủ các trường hợp xảy ra.

### Hướng dẫn.

Với bộ dữ liệu a, b, c đã nhập (là các số thực), chúng ta cần xét đầy đủ các trường hợp sau:

*   Nếu a = b = c = 0 phương trình có vô số nghiệm.
*   Nếu a = b = 0; c ≠ 0, phương trình vô nghiệm.
*   Nếu a = 0; b ≠ 0 phương trình là bậc nhất và có nghiệm duy nhất.
*   Nếu a ≠ 0, giải phương trình bậc hai. Nghiệm sẽ phụ thuộc vào giá trị delta = b² – 4ac. Phương trình vô nghiệm, có một nghiệm kép hoặc hai nghiệm phân biệt phụ thuộc vào giá trị delta là nhỏ hơn 0, bằng 0 hay lớn hơn 0.

Chương trình được thiết kế thông qua các hàm sau:
*   NhapDL(): hàm nhập ba số a, b, c từ bàn phím.
*   GiaiPT1(b, c): hàm giải phương trình bậc nhất: bx + c = 0.
*   GiaiPT2(a, b, c): hàm giải phương trình bậc hai: ax² + bx + c = 0.

Trong bài thực hành chúng ta sử dụng cấu trúc mở rộng của lệnh rẽ nhánh **if ... else** trong Python khi các lệnh này lồng nhau. Khi đó các lệnh rẽ nhánh lồng nhau trong mô hình bên trái sẽ được viết gọn hơn như mô hình bên phải.

Mô hình lệnh rẽ nhánh lồng nhau:
*   if <điều kiện 1>:
    <nhóm lệnh 1>
*   else:
    if <điều kiện 2>:
        <nhóm lệnh 2>
    else:
        <nhóm lệnh 3>

Mô hình lệnh rẽ nhánh sử dụng elif:
*   if <điều kiện 1>:
    <nhóm lệnh 1>
*   elif <điều kiện 2>:
    <nhóm lệnh 2>
*   else:
    <nhóm lệnh 3>

**Chú ý**: Cấu trúc **if ... elif .... else** có thể lồng nhau nhiều lần.
Chương trình đầy đủ như sau:

giaipt.py

Đoạn mã Python định nghĩa một hàm tính căn bậc hai.
```python

# Nhập từ bàn phím ba số thực a, b, c và tìm nghiệm của phương trình ax2 + bx + c = 0.

# Hàm sqrt(x): tính căn bậc hai của x.

# return x**0.5
```

Đoạn mã Python định nghĩa hàm NhapDL() để nhập ba số thực.
```python

# Hàm NhapDL():

# Yêu cầu người dùng nhập ba số a, b, c cách nhau bởi dấu cách.

# Chuyển chuỗi nhập thành danh sách các chuỗi số.

# Chuyển đổi và trả về ba số dưới dạng số thực.
```

Đoạn mã Python định nghĩa hàm GiaiPT1(b, c) để giải phương trình bậc nhất bx + c = 0.
```python

# Hàm GiaiPT1(b,c):

# Nếu b khác 0, in ra thông báo "Phương trình có một nghiệm duy nhất" và giá trị nghiệm.

# Ngược lại (nếu b bằng 0):

#   Nếu c bằng 0, in ra thông báo "Phương trình có vô số nghiệm".

#   Ngược lại (nếu b bằng 0 và c khác 0), in ra thông báo "Phương trình vô nghiệm".
```

Mô tả chức năng của đoạn mã trên:

Đoạn mã Python này định nghĩa hàm `GiaiPT2(a,b,c)` để giải phương trình bậc hai `ax^2 + bx + c = 0`.
*   Nếu `a` bằng 0, nó sẽ gọi một hàm khác là `GiaiPT1(b,c)` (để giải phương trình bậc nhất).
*   Nếu `a` khác 0, nó tính biệt thức `delta`.
    *   Nếu `delta` dương, phương trình có hai nghiệm thực phân biệt.
    *   Nếu `delta` bằng 0, phương trình có nghiệm kép.
    *   Nếu `delta` âm, phương trình vô nghiệm.
Phần chương trình chính sẽ nhập dữ liệu `a, b, c` và gọi hàm `GiaiPT2` để giải.

## LUYỆN TẬP

1.  Viết chương trình yêu cầu nhập số thực dương `a`. Chương trình cần kiểm tra dữ liệu nhập như sau: Nếu số đã nhập nhỏ hơn hoặc bằng 0 thì thông báo: "Nhập sai, số `a` phải lớn hơn 0. Hãy nhập lại". Chương trình chỉ dừng sau khi người dùng nhập đúng.
2.  Viết chương trình in bảng cửu chương ra màn hình như sau:
    *   Hàng thứ nhất in ra bảng nhân 1, 2, 3, 4, 5.
    *   Hàng thứ hai in ra bảng nhân 6, 7, 8, 9, 10.

## VẬN DỤNG

1.  Viết chương trình nhập hai số tự nhiên `Y1`, `Y2` là số năm, `Y2 > Y1`. Tính xem trong khoảng thời gian từ năm `Y1` đến năm `Y2` có bao nhiêu năm nhuận. Áp dụng tính xem trong thế kỉ XXI có bao nhiêu năm nhuận.
2.  Gọi **ƯCLN(a, b)** là hàm ƯCLN của hai số tự nhiên `a`, `b`. Dễ thấy ta có **ƯCLN(a, b) = ƯCLN(b, a%b)** nếu `b > 0` và **ƯCLN(a, 0) = a**. Từ đó hãy viết chương trình nhập hai số `a`, `b` và tính ƯCLN của `a` và `b`.
