# Bài 14: KIỂU DỮ LIỆU DANH SÁCH - XỬ LÍ DANH SÁCH

Học xong bài này, em sẽ:
* Nhận biết được sơ lược cấu trúc của kiểu dữ liệu mảng trong các ngôn ngữ lập trình bậc cao.
* Mô tả được kiểu danh sách trong Python có cấu trúc giống như kiểu mảng.
* Viết được câu lệnh trong Python để khởi tạo và truy cập tới các phần tử của danh sách.
* Sử dụng được một số hàm xử lí danh sách thường dùng.

Có nhiều bài toán thực tế cần giải quyết mà trong đó dữ liệu có được ở dạng một bản liệt kê tuần tự (thường gọi là danh sách). Ví dụ: Từ danh sách kết quả một cuộc thi, hãy đưa ra danh sách những người đỗ trong kì thi đó. Em hãy đưa thêm ví dụ.

## 1. Kiểu dữ liệu danh sách

Nhiều khi chúng ta cần lưu trữ nhiều phần tử dữ liệu cùng với nhau thành một dãy mà trong dãy đó thứ tự của mỗi phần tử dữ liệu là quan trọng. Với những dãy dữ liệu như thế ta có thể truy cập, xem hoặc thay đổi được một phần tử của dãy khi biết vị trí của nó trong dãy.

Nhiều ngôn ngữ lập trình bậc cao cho phép sử dụng kiểu dữ liệu theo cấu trúc như vậy, gọi là **kiểu mảng**. Thay vì dùng nhiều biến riêng lẻ chứa các đại lượng cùng một kiểu dữ liệu, ta có thể dùng một biến kiểu mảng chứa cả dãy các đại lượng đó.

Trong Python có **kiểu dữ liệu danh sách (list)** để lưu trữ dãy các đại lượng có thể ở các kiểu dữ liệu khác nhau và cho phép truy cập tới mỗi phần tử của dãy theo vị trí (chỉ số) của phần tử đó. Khi tất cả các phần tử trong danh sách đều có cùng một kiểu dữ liệu thì danh sách đó tương ứng với mảng ở nhiều ngôn ngữ lập trình bậc cao khác. Các phần tử trong danh sách của Python được đánh chỉ số bắt đầu từ 0.

Ví dụ 1. Thay vì dùng sáu biến kiểu kí tự để lưu trữ tên sáu bạn, có thể dùng một biến kiểu danh sách.

Trong ví dụ về sáu người bạn:
*   Để lưu trữ riêng lẻ tên của sáu người bạn, có thể khai báo sáu biến độc lập, mỗi biến lưu một tên.
*   Để lưu trữ tên của sáu người bạn trong một **danh sách**, có thể khai báo một biến danh sách và gán cho nó một tập hợp các tên. Kiểu dữ liệu của biến này là `list`.
    *   Các phần tử trong danh sách phải cách nhau bởi dấu “,”

1.  Với gợi ý từ Ví dụ 1, em hãy viết câu lệnh Python để tạo ra một biến kiểu danh sách lưu trữ được dữ liệu cho ở Bảng 1.
2.  Viết câu lệnh in ra phần tử thứ ba của danh sách được tạo ở yêu cầu 1.
3.  Dùng hàm `type()` kiểm tra lại kiểu dữ liệu của biến vừa tạo ra.
4.  Dùng hàm `len()` để biết kích thước của danh sách (độ dài hay số phần tử của danh sách).

## Khởi tạo danh sách

Có nhiều cách **khởi tạo danh sách**, ba cách trong số các cách đó là:

*   Dùng phép gán, ví dụ: `ds = [1, 1, 2, 3, 5, 8]`
*   Dùng câu lệnh lặp `for` gán giá trị trong khoảng cho trước, ví dụ: `ds = [i for i in range(6)]`
*   Kết quả của ví dụ trên: `ds = [0, 1, 2, 3, 4, 5]`
*   Khởi tạo danh sách số nguyên hay thực từ dữ liệu nhập vào:
    *   Sử dụng câu lệnh cho phép nhập một dãy số nguyên trên cùng một dòng: `a = [int(i) for i in input().split()]`

Một chương trình Python để nhập danh sách các số nguyên và in ra danh sách đó có thể được viết như sau:

*   Chương trình nhập danh sách số nguyên:
    ```
    print ("Nhập một danh sách gồm các số nguyên")
    a = [int(i) for i in input().split()]
    print (a)
    ```
*   Kết quả chạy chương trình khi nhập năm số nguyên (các số cách nhau một hay một số dấu cách):
    ```
    Nhập một danh sách gồm các số nguyên
    12 24 9 11 7
    [12, 24, 9, 11, 7]
    >>>
    ```

## Truy cập đến phần tử trong danh sách

Nêu tên danh sách và chỉ số của phần tử, chỉ số cần đặt trong cặp dấu ngoặc vuông. Chỉ số có thể là một biểu thức số học.

Trong Ví dụ 1, với danh sách friends, friends[5] là phần tử thứ ba trong danh sách và có giá trị là 'Thuý Anh'.

Đoạn mã Python sau minh họa cách truy cập phần tử trong danh sách:
*   `>>> friends[0]` trả về 'Ảnh Hồng', yêu cầu cho biết phần tử đầu tiên của danh sách `friends`.
*   `>>> friends[5]` trả về 'Thuý Anh', yêu cầu cho biết phần tử ở vị trí thứ sáu của danh sách `friends`.

## Một số hàm và thao tác xử lí danh sách

Hãy hình dung, nhóm em dùng một danh sách trong Python để lưu trữ và quản lí danh sách các bạn trong Câu lạc bộ Lập trình của lớp em. Trong tình huống ấy, nhóm em mong muốn Python cung cấp sẵn những công cụ nào ở dạng hàm để dễ thực hiện được việc quản lí danh sách câu lạc bộ?

Bảng 2 sau đây giới thiệu một số hàm Python cung cấp để người lập trình xử lí danh sách nhanh chóng, thuận lợi. Ngoài ra, còn có nhiều hàm khác nữa có thể dùng trong xử lí danh sách mà người lập trình có thể dễ dàng tra cứu và tìm hiểu.

Một số hàm xử lí danh sách trong Python và ý nghĩa của chúng:
*   **a.append(x)**: Bổ sung phần tử x vào cuối danh sách a.
*   **a.pop(i)**: Xoá phần tử đứng ở vị trí i trong danh sách a và đưa ra phần tử này.
*   **a.insert(i,x)**: Bổ sung phần tử x vào trước phần tử đứng ở vị trí i trong danh sách a. `a.insert(0,x)` sẽ bổ sung x vào đầu danh sách.
*   **a.sort()**: Sắp xếp các phần tử của danh sách a theo thứ tự không giảm.

Ví dụ 2. Hình 3 minh họa chương trình Python sử dụng một số hàm để xử lí danh sách.

Đoạn mã Python này minh họa các thao tác cơ bản với danh sách:
*   Khởi tạo một danh sách `friends`.
*   Thêm một phần tử vào cuối danh sách bằng `append()`.
*   Truy cập phần tử tại một chỉ mục nhất định.
*   Xóa một phần tử tại một chỉ mục và trả về giá trị của nó bằng `pop()`.
*   Chèn một phần tử vào vị trí chỉ định bằng `insert()`.
*   Truy cập phần tử tại một chỉ mục nhất định sau khi chèn.
*   Sắp xếp danh sách theo thứ tự bảng chữ cái bằng `sort()`.
*   In danh sách đã được sắp xếp.
Kết quả in ra của danh sách `friends` sau các thao tác là: `['Anh', 'Giang', 'Hoa', 'Lan', 'Mai', 'Minh', 'Phan']`

## Ghép các danh sách thành một danh sách
Phép “+” được dùng để ghép nối hai danh sách.
Ví dụ 3. Chương trình ở Hình 4 thực hiện ghép hai danh sách.

Đoạn mã Python này minh họa việc ghép nối hai danh sách bằng toán tử `+`:
*   Khởi tạo danh sách `a` với các số nguyên.
*   Khởi tạo danh sách `b` với các chuỗi ký tự.
*   Ghép nối `a` và `b` để tạo ra danh sách `c`.
*   In danh sách `c`.
Kết quả in ra của danh sách `c` là: `[1, 2, 3, 'Hồng', 'Cúc', 'Lan', 'Mai']`

## Duyệt các phần tử trong danh sách theo thứ tự lưu trữ
Gọi `a` là một danh sách, câu lệnh duyệt danh sách có dạng:
```
for i in a:
    Các câu lệnh xử lí
```

Ví dụ 4. Hình 5 minh họa chương trình và kết quả duyệt danh sách bằng câu lệnh `for`.

Đoạn mã Python này minh họa cách duyệt qua từng phần tử trong danh sách và thực hiện một thao tác trên mỗi phần tử:
*   Khởi tạo danh sách `a` chứa các số nguyên.
*   Dùng vòng lặp `for` để duyệt qua từng phần tử `i` trong danh sách `a`.
*   Trong mỗi lần lặp, in ra bình phương của phần tử `i`.
Kết quả in ra là:
```
16
1
16
4
4
25
```

## Luyện tập
# Bài 1: Đọc chương trình sau đây và cho biết kết quả in ra màn hình. Em hãy soạn thảo và chạy chương trình để kiểm tra dự đoán của em.

Chương trình đọc một chuỗi các số từ đầu vào, chuyển đổi chúng thành số nguyên và lưu vào một danh sách. Sau đó, chương trình duyệt qua danh sách, đếm số lượng các số nhỏ hơn hoặc bằng 100 và lưu vào biến `sonho`. Cuối cùng, chương trình in ra giá trị của `sonho`.

# Bài 2: Bạn Thanh muốn tính trung bình cộng của nhiệt độ trung bình các ngày trong tuần. Thanh đã viết được đoạn chương trình nhập từ bàn phím nhiệt độ trung bình của bảy ngày trong tuần vào một danh sách. Em hãy giúp bạn Thanh viết tiếp những câu lệnh còn thiếu vào chỗ trống để máy tính đưa ra màn hình kết quả cần có.

Chương trình đọc một chuỗi các số từ đầu vào (biểu thị nhiệt độ), chuyển đổi chúng thành số thực và lưu vào một danh sách `nh_d`. Biến `tb` được khởi tạo bằng 0. Đoạn mã còn thiếu cần thực hiện việc tính tổng các giá trị nhiệt độ trong danh sách `nh_d` và lưu vào `tb`. Cuối cùng, chương trình in ra "Nhiệt độ trung bình:" kèm theo giá trị trung bình (tổng `tb` chia cho 7).

Camera đặt cạnh trạm thu phí đường cao tốc ghi nhận nhiều thông tin, trong đó có mã số nhận dạng loại ô tô đi qua. Mỗi loại ô tô được mã hoá thành một số nguyên dương. Cho dãy số, mỗi số là mã hoá về loại của một ô tô đi qua trạm thu phí. Em hãy viết chương trình nhập dãy số mã hoá xe vào từ bàn phím và đưa ra màn hình số loại xe khác nhau đã được nhận dạng.

Ví dụ:

Trong các câu sau đây, những câu nào đúng?
* Trong các ngôn ngữ lập trình bậc cao đều có kiểu dữ liệu để lưu trữ một dãy hữu hạn các phần tử.

1) Trong ngôn ngữ lập trình Python, dữ liệu kiểu danh sách là một dãy hữu hạn các phần tử cho phép truy cập đến từng phần tử của nó.
2) Python bắt buộc các phần tử của một danh sách phải có cùng một kiểu dữ liệu.
3) Phải khởi tạo một danh sách trong Python bằng phép gán trong chương trình, không thể nhập các phần tử của danh sách từ bàn phím.
4) Python chỉ cung cấp những hàm sau đây để xử lí danh sách: append(), pop(), insert(), sort(), clear().

## Tóm tắt bài học

*   Các ngôn ngữ lập trình bậc cao đều cung cấp kiểu dữ liệu cho phép lưu trữ một dãy hữu hạn các phần tử và các chương trình con có sẵn để xử lí dữ liệu thuộc kiểu này.
*   Trong Python, **list** là kiểu dữ liệu có cấu trúc dùng để nhóm một tập dữ liệu thành một dãy giá trị được đánh số và có thể truy cập đến từng giá trị.
*   Có thể khởi tạo cho list trong Python bằng cách gán trực tiếp hoặc nhập giá trị các phần tử vào từ thiết bị vào chuẩn.
*   Python cung cấp nhiều thao tác hữu dụng trên list, một số hàm thông dụng là: **len()**, **append()**, **pop()**, **insert()**, **sort()**.

## BÀI TÌM HIỂU THÊM

### NHẬP DANH SÁCH TỪ FILE

Có thể nhập một danh sách từ file như chương trình. Nếu danh sách cần xử lí rất dài thì chúng ta sẽ thấy được rõ tính ưu việt của việc nhập dữ liệu từ file. Ví dụ chương trình dưới đây nhập danh sách các số nguyên từ file input.txt và ghi tổng các số nguyên đó ra file output.txt.

Đoạn mã Python thực hiện việc đọc các số nguyên từ file `input.txt`, tính tổng của chúng và sau đó ghi tổng này vào file `output.txt`. Chương trình cũng sử dụng `sys.stdin` và `sys.stdout` để chuyển hướng đầu vào và đầu ra chuẩn đến các file.
