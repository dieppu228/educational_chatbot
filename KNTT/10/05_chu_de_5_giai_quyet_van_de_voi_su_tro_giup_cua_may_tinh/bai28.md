# Bài 28: PHẠM VI CỦA BIẾN

SAU BÀI NÀY EM SẼ:
*   Biết và trình bày được ý nghĩa của phạm vi hoạt động của biến trong chương trình và hàm.

1. Một biến được định nghĩa trong chương trình chính (bên ngoài các hàm) thì sẽ được sử dụng như thế nào bên trong các hàm?
2. Một biến được khai báo bên trong một hàm thì có sử dụng được ở bên ngoài hàm đó hay không?

Bài này sẽ giúp em tìm câu trả lời cho các câu hỏi trên.

## 1. PHẠM VI CỦA BIẾN KHAI BÁO TRONG HÀM

### Hoạt động 1 Phạm vi của biến khi khai báo trong hàm

Quan sát các lệnh sau để tìm hiểu phạm vi có hiệu lực của biến khi khai báo bên trong một hàm.

Các biến được khai báo bên trong một hàm chỉ được sử dụng bên trong hàm đó. Chương trình chính không sử dụng được.

Đoạn mã Python sau định nghĩa một hàm `func(a, b)`.
Bên trong hàm này, có các biến `n`, `a`, `b` đang hoạt động. Biến `n` được gán giá trị 10, và các biến `a`, `b` được thay đổi giá trị. Hàm trả về một giá trị tính toán.

Tiếp theo, đoạn mã gán giá trị 1 cho biến `a` và giá trị 2 cho biến `b` bên ngoài hàm. Đây là các biến bên ngoài hàm.
Khi gọi hàm `func(a, b)` với các biến này, kết quả trả về là `16`.
Sau khi chạy hàm, các biến `a`, `b` (bên ngoài hàm) vẫn giữ nguyên giá trị ban đầu là `(1, 2)`.
Khi cố gắng truy cập biến `n` bên ngoài hàm, chương trình sẽ báo lỗi `NameError: name 'n' is not defined`. Điều này chứng tỏ biến `n` chỉ có tác dụng bên trong hàm `func`, và việc gọi nó bên ngoài hàm sẽ gây ra lỗi.

Trong Python tất cả các biến khai báo bên trong hàm đều có tính địa phương (cục bộ), không có hiệu lực ở bên ngoài hàm.

1. Giả sử có các lệnh sau:
   Đoạn mã khởi tạo biến `a` và `b` với giá trị `1` và `2`, sau đó định nghĩa một hàm `f(a,b)` thực hiện các phép tính `a = a + b`, `b = b * a`, và trả về `a + b`.
   Giá trị của a, b bằng bao nhiêu sau khi thực hiện lệnh sau?
   a) f(1, 2)
   b) f(10, 20)
2. Ta có thể khai báo một biến bên trong hàm trùng tên với biến đã khai báo trước đó bên ngoài hàm không?

## 2. PHẠM VI CỦA BIẾN KHAI BÁO NGOÀI HÀM

### Hoạt động 2 Phạm vi của biến khi khai báo bên ngoài hàm

Quan sát các lệnh sau, tìm hiểu phạm vi có hiệu lực của biến khi khai báo bên ngoài một hàm.

### Ví dụ 1. Biến khai báo bên ngoài hàm không có tác dụng bên trong hàm.

Đoạn mã định nghĩa một hàm `f(n)` tính `n + 1` và trả về kết quả.
Sau đó, một biến `t` được gán giá trị 10.
Hàm `f` được gọi với đối số 5.
Kết quả của `f(5)` là:
6
Khi in giá trị của `t` sau khi gọi hàm:
10

Trong chương trình chính, **biến t** được khai báo bên ngoài hàm và gán giá trị 10. Khi gọi `f(5)`, t sẽ được gán 6 (là giá trị của biến cục bộ `t` trong hàm). Hàm trả lại giá trị 6. Nhưng khi thoát khỏi `f()`, t vẫn có giá trị 10 (là giá trị của biến toàn cục `t`). Do vậy **biến t** không có tác dụng bên trong hàm `f()`.

### Ví dụ 2. Bên trong hàm có thể truy cập để sử dụng giá trị của biến đã khai báo trước đó ở bên ngoài hàm.

Đoạn mã định nghĩa một hàm `f(a,b)` trả về tổng của `a + b + N`.
Sau đó, một biến `N` được khai báo và gán giá trị 10.
Hàm `f` được gọi với đối số 1 và 2.
Kết quả của `f(1,2)` là:
13

Trong chương trình chính, **biến N** được khai báo và gán giá trị 10. Khi gọi hàm `f(1,2)`, giá trị trả lại là biểu thức có N tham gia. Vậy trong hàm `f()` được phép truy cập giá trị của **biến N**.

Lưu ý: Nếu muốn biến biến bên ngoài vẫn có tác dụng bên trong hàm thì cần khai báo lại biến này bên trong hàm với từ khoá **global**.

Đoạn mã Python định nghĩa một hàm `f(n)`. Bên trong hàm, biến `t` được khai báo là biến toàn cục (`global t`), sau đó `t` được gán giá trị `2*n + 1`, và cuối cùng giá trị của `t` được trả về. Bên ngoài hàm, `t` ban đầu được gán giá trị `10`. Khi hàm `f(1)` được gọi, biến toàn cục `t` được cập nhật thành `3`. Cuối cùng, giá trị của `t` được hiển thị là `3`.

Biến đã khai báo bên ngoài sẽ không có tác dụng bên trong hàm như một biến. Nếu muốn có tác dụng thì cần khai báo lại biến này trong hàm với từ khoá **global**.

Giả sử hàm f(x,y) được định nghĩa như sau:

Đoạn mã Python định nghĩa một hàm `f(x,y)`. Trong hàm, một biến `a` được tính bằng `2*(x+y)`, sau đó giá trị của `a+n` được in ra.
Bên ngoài hàm, biến `n` được gán giá trị `10`, sau đó hàm `f(1,2)` được gọi.

Kết quả nào được in ra khi thực hiện các lệnh sau?

## THỰC HÀNH
### Phạm vi của biến

#### Nhiệm vụ 1. Viết hàm với đầu vào là danh sách A chứa các số và số thực x. Hàm trả lại một danh sách kết quả B từ danh sách A bằng cách chỉ giữ lại các phần tử lớn hơn hoặc bằng x.

Hướng dẫn. Biến B kiểu danh sách cần được định nghĩa trong hàm và được bổ sung thêm các phần tử từ A nếu thoả mãn điều kiện lớn hơn hoặc bằng x.

Đoạn mã Python định nghĩa hàm `Select(A,x)`. Hàm này khởi tạo một danh sách rỗng `B`. Nó lặp qua các chỉ số của danh sách `A`. Nếu phần tử `A[k]` lớn hơn hoặc bằng `x`, thì phần tử đó được thêm vào danh sách `B`. Cuối cùng, hàm trả về danh sách `B`.

#### Nhiệm vụ 2. Viết hàm với đầu vào là xâu kí tự Str và số c, đầu ra là danh sách các từ được tách ra từ xâu Str nhưng đã được chuyển thành chữ in hoa hoặc chữ in thường, hoặc chỉ chuyển kí tự đầu các từ thành chữ in hoa tuỳ thuộc vào tham số đầu vào c như sau:

*   Nếu c = 0, danh sách B là các từ được chuyển thành chữ in hoa.
*   Nếu c = 1, danh sách B là các từ được chuyển thành chữ in thường.
*   Nếu c = 2, danh sách B là các từ được chuyển viết chữ hoa kí tự đầu của mỗi từ.

##### Hướng dẫn.
Chúng ta cần sử dụng các lệnh sau:
*   Str.upper() – chuyển kí tự của xâu thành chữ in hoa.
*   Str.lower() – chuyển kí tự của xâu thành chữ in thường.
*   Str.title() – chuyển kí tự đầu mỗi từ của xâu thành chữ in hoa, các kí tự khác chuyển về chữ thường.

Hàm được định nghĩa có dạng **Tach_tu(Str,c)**. Đầu tiên xâu Str cần được tách từ bằng lệnh split(). Sau đó danh sách kết quả sẽ được chuyển đổi chữ in hoa, in thường sử dụng một trong các lệnh trên tùy thuộc vào giá trị của đối số c.

Đoạn mã này định nghĩa hàm `Tach_tu` nhận một chuỗi `Str` và một số nguyên `c`. Hàm này sẽ tách chuỗi `Str` thành các từ, sau đó duyệt qua từng từ. Dựa vào giá trị của `c`: nếu `c=0` thì chuyển từ đó thành chữ in hoa, nếu `c=1` thì chuyển thành chữ in thường, và nếu `c=2` thì chuyển thành dạng chữ hoa chữ cái đầu và các chữ cái còn lại là chữ thường. Cuối cùng, hàm trả về danh sách các từ đã được chuyển đổi.

### Nhiệm vụ 3.
Viết chương trình yêu cầu thực hiện lần lượt các việc sau, mỗi việc cần được thực hiện bởi một hàm:
1.  Nhập từ bàn phím một dãy các số nguyên, mỗi số cách nhau bởi dấu cách. Chuyển các số này vào danh sách A và in danh sách A ra màn hình.
2.  Trích từ danh sách A ra một danh sách B gồm các phần tử lớn hơn 0. In danh sách B ra màn hình.
3.  Trích từ danh sách A ra một danh sách C gồm các phần tử nhỏ hơn 0. In danh sách C ra màn hình.

#### Hướng dẫn.
Với mỗi việc trên được viết thành một hàm. Toàn bộ chương trình có thể như sau:

Đoạn mã này định nghĩa hàm `Nhap_DuLieu`. Hàm này yêu cầu người dùng nhập một dãy các số nguyên cách nhau bởi dấu cách, sau đó chuyển chuỗi nhập vào thành danh sách các số nguyên và trả về danh sách đó.

Đoạn mã này định nghĩa hàm `getB` nhận vào một danh sách `A`. Hàm này khởi tạo một danh sách rỗng `B`.

Mô tả chức năng của đoạn mã:
Đoạn mã bao gồm hai hàm và một chương trình chính.
Hàm `getB(A)`: Nhận vào một danh sách `A`, tạo một danh sách `B` rỗng. Duyệt qua từng phần tử `x` trong `A`. Nếu `x` lớn hơn 0, thêm `x` vào danh sách `B`. Cuối cùng, trả về danh sách `B`.
Hàm `getC(A)`: Nhận vào một danh sách `A`, tạo một danh sách `C` rỗng. Duyệt qua từng phần tử `x` trong `A`. Nếu `x` nhỏ hơn 0, thêm `x` vào danh sách `C`. Cuối cùng, trả về danh sách `C`.
Chương trình chính:
*   Gọi hàm `Nhap_DuLieu()` để lấy dữ liệu ban đầu và gán vào biến `A`.
*   In ra màn hình chuỗi "Danh sách A:" và nội dung của danh sách `A`.
*   Gọi hàm `getB(A)` để tạo danh sách `B` từ `A`, chứa các phần tử dương.
*   Gọi hàm `getC(A)` để tạo danh sách `C` từ `A`, chứa các phần tử âm.
*   In ra màn hình chuỗi "Danh sách B:" và nội dung của danh sách `B`.
*   In ra màn hình chuỗi "Danh sách C:" và nội dung của danh sách `C`.

## LUYỆN TẬP

1.  Viết hàm với đầu vào, đầu ra như sau:
    *   Đầu vào là danh sách sList, các phần tử là xâu kí tự.
    *   Đầu ra là danh sách cList, các phần tử là kí tự đầu tiên của các xâu kí tự tương ứng trong danh sách sList.
2.  Viết hàm Tach_day() với đầu vào là danh sách A, đầu ra là hai danh sách B, C được mô tả như sau:
    *   Danh sách B thu được từ A bằng cách lấy ra các phần tử có chỉ số chẵn.
    *   Danh sách B thu được từ A bằng cách lấy ra các phần tử có chỉ số lẻ.

## VẬN DỤNG

1.  Viết hàm có hai tham số đầu vào là m, n. Đầu ra trả lại hai giá trị là:
    *   **ƯCLN** của m, n.
    *   **Bội chung nhỏ nhất** (**BCNN**) của m, n.
    Gợi ý: Sử dụng công thức ƯCLN(m, n) × BCNN(m, n) = m × n.
2.  Viết chương trình nhập ba số tự nhiên từ bàn phím day, month, year, các số cách nhau bởi dấu cách. Các số này biểu diễn giá trị của ngày, tháng, năm nào đó. Chương trình cần kiểm tra và in ra thông báo số liệu đã nhập vào đó có hợp lệ hay không.
