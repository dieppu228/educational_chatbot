# Bài 25: MỘT SỐ LỆNH LÀM VIỆC VỚI XÂU KÍ TỰ

SAU BÀI NÀY EM SẼ:
*   Biết và thực hiện được một số lệnh thường dùng với xâu kí tự.

Bài toán tìm kiếm xâu con trong một xâu là một trong những bài toán tin học được ứng dụng nhiều trong thực tế. Công cụ tìm kiếm thông tin trên Internet hay lệnh tìm kiếm trong soạn thảo văn bản được xây dựng trên cơ sở bài toán tìm xâu con.
Cho xâu c = "Trường Sơn" và xâu m = "Bước chân trên dải Trường Sơn". Em hãy cho biết xâu c có là xâu con của xâu m không? Nếu có thì tìm vị trí của xâu c trong xâu m.

## 1. XÂU CON VÀ LỆNH TÌM VỊ TRÍ XÂU CON

**Hoạt động 1** Một số lệnh tìm kiếm xâu con trong xâu kí tự

Quan sát các ví dụ sau để tìm hiểu cách kiểm tra xâu con và tìm kiếm vị trí xâu con trong xâu kí tự.

**Ví dụ 1.** Dùng toán tử **in** để kiểm tra một xâu có là xâu con của xâu khác không.
*   Kiểm tra xem "abc" có trong "123abc" không.
    `True`
*   Kiểm tra xem "010" có trong "1101" không.
    `False`

Biểu thức kiểm tra `<xâu 1> in <xâu 2>`
Nếu đúng thì trả lại giá trị True, nếu sai trả lại giá trị False.

**Ví dụ 2.** Lệnh **find()** tìm vị trí xuất hiện của một xâu trong xâu khác.
*   Khởi tạo xâu `s = "ab bc cd 123 456 00"`.
*   Tìm vị trí xuất hiện đầu tiên của "b" trong xâu `s`.
    `1` (Vị trí xuất hiện đầu tiên của "b" trong xâu `s` là chỉ số 1.)
*   Tìm vị trí xuất hiện đầu tiên của "12" trong xâu `s`.
    `9` (Vị trí tìm thấy đầu tiên của "12" trong xâu `s` là chỉ số 9.)
*   Tìm vị trí xuất hiện đầu tiên của "AB" trong xâu `s`.
    `-1` (Không tìm thấy xâu "AB" trong xâu `s` nên trả về -1.)

Tương tự danh sách, Python cũng có một số lệnh đặc biệt dành riêng cho xâu kí tự (phương thức). Cách thức hiện phương thức là:
Cú pháp chung để gọi phương thức trên xâu kí tự.

Cú pháp đơn của lệnh find():
Cú pháp lệnh `find()` tìm xâu con đơn giản.
Lệnh sẽ tìm vị trí đầu tiên của xâu con trong xâu mẹ và trả về vị trí đó. Nếu không tìm thấy thì trả về -1.

Cú pháp đầy đủ của lệnh find():
Cú pháp lệnh `find()` tìm xâu con từ vị trí `start`.
Lệnh sẽ tìm vị trí xâu con bắt đầu từ vị trí start.

Ví dụ 3
Ví dụ minh họa lệnh `find()` tìm vị trí của xâu con `sub` trong xâu `s`.
Khi tìm `sub` trong `s`, kết quả là `9`.
Khi tìm `sub` trong `s` bắt đầu từ vị trí `10`, kết quả là `-1` (không tìm thấy).

Để tìm một xâu trong một xâu khác có thể dùng toán tử `in` hoặc lệnh `find()`. Lệnh `find()` trả về vị trí của xâu con trong xâu mẹ.

1.  Biểu thức logic sau là đúng hay sai?
    Kiểm tra sự tồn tại của xâu "010" trong "001100".
2.  Lệnh sau trả lại giá trị gì?
    Tìm xâu "ab" trong "ababababab" bắt đầu từ vị trí 4.

## 2. MỘT SỐ LỆNH THƯỜNG DÙNG VỚI XÂU KÍ TỰ

### Hoạt động 2: Một số lệnh thường dùng với xâu kí tự
Quan sát các ví dụ sau để biết cách sử dụng một số lệnh thường dùng với xâu kí tự như: `split()`, `join()`.

Ví dụ 1. Lệnh **split()** tách một xâu thành danh sách các từ.
Ví dụ minh họa lệnh `split()` không có đối số, tách xâu `s` dùng dấu cách.
Kết quả là một danh sách các từ: `['Tiên', 'học', 'lễ', 'hậu', 'học', 'văn']`

Ví dụ minh họa lệnh `split()` với đối số là dấu phẩy, tách xâu `st` dùng dấu phẩy.
Kết quả là một danh sách các chuỗi số: `['0', '1', '2', '3', '4', '5', '6', '10']`

**Lệnh split()** tách một xâu thành các từ và đưa vào một danh sách. Kí tự tách dùng để phân tách các từ mặc định là dấu cách, tuy nhiên có thể thay thế kí tự tách bằng kí tự khác.
Cú pháp của lệnh split().
Mô tả: Phương thức `split()` được gọi trên một đối tượng xâu mẹ (`<xâu mẹ>`) và nhận một đối số tùy chọn là kí tự dùng để tách (`<kí tự tách>`).

### Ví dụ 2. Lệnh join() nối danh sách gồm các từ thành một xâu.

Mô tả: Định nghĩa danh sách A chứa các xâu.
Mô tả: Lệnh `join()` này sẽ nối các phần tử của danh sách A bởi dấu cách.
Kết quả: `'Tiên học lễ hậu học văn'`

Mô tả: Định nghĩa danh sách B chứa các xâu số.
Mô tả: Lệnh `join()` này sẽ nối các phần tử của danh sách B bởi dấu ",".
Kết quả: `'0,1,2,3,4,5,6,10'`

**Lệnh join()** có tác dụng ngược với lệnh split(), có chức năng nối các phần tử (là xâu) của một danh sách thành một xâu. Cú pháp của lệnh join() là:
Mô tả: Phương thức `join()` được gọi trên một xâu kí tự dùng để nối (`"kí tự nối"`) và nhận một đối số là danh sách các xâu cần nối (`<danh sách>`).

Python có các lệnh đặc biệt để xử lí xâu là split() dùng để tách xâu thành danh sách và lệnh join() dùng để nối danh sách các xâu thành một xâu.

Cho xâu kí tự: "gà,vịt,chó,lợn,ngựa,cá". Em hãy trình bày cách làm để xoá các dấu "," và thay thế bằng dấu " " trong xâu này.

## THỰC HÀNH
### Một số bài toán liên quan đến xâu kí tự.

**Nhiệm vụ 1.** Viết chương trình nhập nhiều số nguyên từ bàn phím, các số cách nhau bởi dấu cách. Khi nhập xong thông báo số lượng các số đã nhập và in các số này thành hàng ngang.

**Hướng dẫn.** Dữ liệu nhập vào là một xâu. Dùng lệnh split() để tách thành danh sách. Chuyển các phần tử của danh sách này thành số và in ra màn hình.

Mô tả: Đoạn mã Python này yêu cầu người dùng nhập các số nguyên cách nhau bởi dấu cách. Sau đó, nó sử dụng `split()` để tách xâu nhập thành danh sách các xâu số, chuyển đổi từng phần tử thành số nguyên, lưu vào một danh sách mới. Cuối cùng, chương trình in ra số lượng số đã nhập và tất cả các số đó trên cùng một dòng.

Nhiệm vụ 2. Viết chương trình nhập một xâu kí tự có thể có nhiều dấu cách giữa các từ. Sau đó chỉnh sửa xâu kí tự đó sao cho giữa các từ chỉ có một dấu cách. In xâu kết quả ra màn hình.

**Hướng dẫn**. Chuyển xâu kí tự ban đầu thành danh sách các từ đơn bằng lệnh `split()`, sau đó nối các từ đơn này bằng lệnh `join()`.

Đoạn mã Python thực hiện việc nhập một đoạn văn bản, sau đó tách nó thành các từ riêng lẻ, và nối lại các từ đó bằng một dấu cách duy nhất giữa chúng. Cuối cùng, nó in ra xâu đã được chỉnh sửa.

Nhiệm vụ 3. Viết chương trình nhập số tự nhiên n, rồi nhập họ tên của n học sinh. Sau đó in ra danh sách tên học sinh theo hai cột, cột 1 là tên, cột 2 là họ đệm.

**Hướng dẫn**. Họ tên ban đầu tách ra thành tên và họ đệm bằng lệnh `split()`. Các tên được đưa vào danh sách `ten`, các họ đệm được đưa vào danh sách `hodem`. Sau đó in ra danh sách theo yêu cầu.

Đoạn mã Python này yêu cầu người dùng nhập số lượng học sinh (n). Sau đó, nó lặp lại n lần để nhập họ và tên đầy đủ của từng học sinh. Với mỗi họ tên, nó tách thành tên (từ cuối cùng) và họ đệm (các từ còn lại), lưu vào hai danh sách riêng biệt (`ten` và `hodem`). Cuối cùng, chương trình in ra danh sách học sinh với tên và họ đệm được trình bày trong hai cột.

## LUYỆN TẬP

1.  Viết chương trình nhập nhiều số (số nguyên hoặc số thực) từ bàn phím, các số cách nhau bởi dấu cách. Sau đó in ra màn hình tổng các số đã nhập.
2.  Viết chương trình nhập họ tên đầy đủ của người dùng, sau đó in thông báo tên và họ đệm của người đó.

## VẬN DỤNG

1.  Viết chương trình nhập hai số tự nhiên từ bàn phím, cách nhau bởi dấu cách và đưa ra kết quả là ƯCLN của hai số này.
2.  Viết chương trình nhập số tự nhiên n rồi nhập n họ tên học sinh. Sau đó yêu cầu nhập một tên và thông báo số bạn có cùng tên đó trong lớp.
