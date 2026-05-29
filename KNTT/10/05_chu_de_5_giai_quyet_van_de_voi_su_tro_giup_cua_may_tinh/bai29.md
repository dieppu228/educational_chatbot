# Bài 29: NHẬN BIẾT LỖI CHƯƠNG TRÌNH

SAU BÀI NÀY EM SẼ:
*   Biết và phân loại được một số loại lỗi chương trình.
*   Biết được một vài lỗi ngoại lệ thường gặp.

Một chương trình hoàn chỉnh được mô tả như sau: Tiếp nhận các dữ liệu đầu vào, xử lí theo yêu cầu bài toán và đưa ra kết quả đúng theo yêu cầu. Theo em nếu chương trình có lỗi, thì các lỗi này sẽ như thế nào và có thể ở đâu?

## 1. NHẬN BIẾT LỖI CHƯƠNG TRÌNH

### Hoạt động 1: Nhận biết và phân biệt một số loại lỗi chương trình

Quan sát các trường hợp chương trình gặp lỗi như sau, từ đó nhận biết và phân biệt một số loại lỗi của chương trình.

*   **Trường hợp 1.** Người lập trình viết sai cú pháp lệnh, chương trình lập tức dừng lại và thông báo lỗi cú pháp.
    *   Đoạn mã Python cố gắng in ra chuỗi "Hello" liên tục trong một vòng lặp vô hạn nhưng có lỗi cú pháp trong cấu trúc câu lệnh `print` của vòng lặp `while`.
    *   Kết quả báo lỗi:
        ```
        SyntaxError: invalid syntax
        ```

*   **Trường hợp 2.** Người dùng nhập dữ liệu sai, chương trình thông báo lỗi nhập dữ liệu không đúng khuôn dạng.
    *   Đoạn mã Python yêu cầu người dùng nhập một số nguyên.
    *   Khi người dùng nhập: `Nhập số nguyên n: 1.5`
    *   Kết quả báo lỗi:
        ```
        Traceback (most recent call last):
          File "<pyshell#0>", line 1, in <module>
            n = int(input("Nhập số nguyên n: "))
        ValueError: invalid literal for int() with base 10: '1.5'
        ```

*   **Trường hợp 3.** Chương trình thông báo lỗi chỉ số vượt quá giới hạn cho phép.
    *   Đoạn mã Python khởi tạo một mảng `A` với 4 phần tử. Sau đó, nó cố gắng lặp qua 5 lần (`range(5)`) để in các phần tử của mảng, dẫn đến việc truy cập một chỉ số không tồn tại trong mảng.

# Bài 2: MỘT SỐ LỖI NGOẠI LỆ THƯỜNG GẶP

Chúng ta đã biết, nếu gặp **lỗi ngoại lệ**, chương trình Python sẽ dừng lại, báo lỗi. Một trong những vấn đề được đưa ra khi kiểm soát lỗi là làm thế nào để vẫn phát hiện lỗi, xử lí lỗi nhưng chương trình không bị dừng lại trong khi thực hiện.

## Hoạt động 2: Nhận biết một số lỗi ngoại lệ thường gặp

Đọc, thảo luận để nhận biết một số lỗi ngoại lệ thường gặp trong chương trình Python.

*   **ZeroDivisionError**: Lỗi này xảy ra khi lệnh thực hiện phép chia cho giá trị 0.
*   **IndexError**: Lỗi xảy ra khi lệnh cố gắng truy cập phần tử của danh sách nhưng chỉ số vượt quá giới hạn.
*   **NameError**: Lỗi xảy ra khi chương trình muốn tìm một tên nhưng không thấy. Ví dụ khi lệnh gọi một hàm nhưng không có hàm đó.
*   **TypeError**: Lỗi kiểu dữ liệu. Một số ví dụ lỗi loại này:
    *   Lệnh truy cập một phần tử của danh sách nhưng chỉ số không là số nguyên.
    *   Lệnh tính biểu thức số nhưng lại có một toán hạng không phải là số.
*   **ValueError**: Lỗi liên quan đến giá trị của đối tượng. Lỗi khi thực hiện lệnh chuyển đổi kiểu dữ liệu, đối số của hàm có giá trị mà hàm không hỗ trợ. Ví dụ khi thực hiện lệnh chuyển đổi chuỗi "1.55" sang số nguyên sẽ sinh lỗi loại này.
*   **IndentationError**: Lỗi khi các dòng lệnh thụt vào không thẳng hàng hoặc không đúng vị trí.
*   **SyntaxError**: Lỗi cú pháp.

Hãy nêu mã lỗi ngoại lệ của mỗi lệnh sau nếu xảy ra lỗi.
*   a) Lệnh truy cập phần tử danh sách A với chỉ số là 1.5.
*   b) Lệnh chuyển đổi chuỗi "abc" sang số nguyên.
*   c) Lệnh nhân chuỗi "10" với số thực 3.5.
*   d) Lệnh thực hiện phép cộng giữa số 12 và kết quả gọi hàm x với đối số 10.

## THỰC HÀNH

### Nhiệm vụ 1. Lập trình và kiểm tra khả năng sinh lỗi khi chạy chương trình.

Viết chương trình nhập các số nguyên m, n từ bàn phím, cách nhau bởi dấu cách. Chương trình đưa ra tổng, hiệu, thương của hai số đã nhập.

**Hướng dẫn**. Chương trình chính là khối các lệnh nhập từ bàn phím hai số nguyên m, n. Các số này được nhập bằng lệnh `input()` (nhập dữ liệu từ bàn phím), kết quả là một xâu kí tự. Xâu này sẽ được tách thành danh sách các xâu con bằng lệnh `split()` (tách xâu kí tự). Kết quả thu được sẽ

chuyển đổi thành hai số m, n bằng lệnh int(). Nhập chương trình sau và kiểm tra khả năng sinh lỗi khi chạy chương trình.

Chương trình này yêu cầu người dùng nhập hai số m, n cách nhau bởi dấu cách, sau đó chuyển đổi chúng thành số nguyên và in ra tổng, hiệu, thương của hai số đó.

Gợi ý. Các khả năng sinh lỗi của chương trình:
*   Các số m, n khi nhập vào không là số nguyên.
*   Giữa hai số m, n không có dấu cách.
*   Số n nhập vào là số 0.

### Nhiệm vụ 2. Viết chương trình nhập số tự nhiên n và nhập lần lượt n số nguyên đưa vào danh sách số A. Sau khi nhập xong in danh sách A ra màn hình.

Hướng dẫn. Nhập chương trình sau và kiểm tra khả năng sinh lỗi khi chạy.

Chương trình này yêu cầu người dùng nhập một số tự nhiên `n`, sau đó lặp lại `n` lần việc nhập một số nguyên và thêm số đó vào danh sách `A`. Cuối cùng, chương trình sẽ in ra danh sách `A`.

Gợi ý. Các khả năng sinh lỗi của chương trình:
*   Số n được nhập không là số nguyên.
*   Mỗi số hạng của danh sách nhập vào không là số nguyên.

## LUYỆN TẬP

1.  Các lệnh sau có sinh lỗi chương trình không? Nếu có thì mã lỗi là gì?
    *   Lệnh khởi tạo danh sách `A = [1,3,5,10,0]` và sau đó lặp qua các phần tử của `A` bằng cách in ra `A[k]` với `k` trong `range(1, len(A)+1)`.
    *   Lệnh gán `s1 = "101010"`, `s2 = 10101` và sau đó cố gắng thực hiện phép cộng `s = s1 + s2`.

2.  Để tính giá trị trung bình của một danh sách số A, người lập trình đã dùng lệnh sau để tính:
    *   Lệnh gán `gttb = sum(A)/len(A)`.
    lệnh này có thể sinh lỗi ngoại lệ không? Nếu có thì là những lỗi gì?

## VẬN DỤNG

1.  Giả sử em được yêu cầu viết một chương trình nhập số tự nhiên n từ bàn phím, kết quả đưa ra là danh sách các ước số thực sự của n, tính cả 1 và không tính n. Hãy viết chương trình và kiểm tra các khả năng sinh lỗi khi thực hiện chương trình.
2.  Em hãy viết một chương trình nhỏ để khi chạy sẽ sinh mã lỗi NameError.
