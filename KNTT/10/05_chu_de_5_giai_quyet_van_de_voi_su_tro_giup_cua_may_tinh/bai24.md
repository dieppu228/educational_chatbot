# Bài 24: XÂU KÍ TỰ

## SAU BÀI NÀY EM SẼ:
* Hiểu được xâu kí tự là kiểu dữ liệu cơ bản của Python.
* Biết và thực hiện được lệnh for để xử lí xâu kí tự.

Em đã biết dữ liệu xâu kí tự (gọi tắt là **xâu**) từ Bài 16 và chúng ta có thể tạo các biến kiểu xâu kí tự theo nhiều cách như sau:
* Tạo biến `s` với giá trị "Thời khoá biểu".
* Tạo biến `xau` với giá trị 'Hoa học trò'.
* Tạo biến `Cau_tho` với giá trị chuỗi nhiều dòng: "Mình về mình có nhớ ta Mười lăm năm ấy thiết tha mặn nồng".

Liệu có lệnh nào trích ra từng kí tự của một xâu kí tự? Đếm số kí tự của một xâu?

## 1. XÂU LÀ MỘT DÃY CÁC KÍ TỰ

### Hoạt động 1: Tìm hiểu cấu trúc của xâu kí tự

Quan sát các ví dụ sau để biết cấu trúc xâu kí tự, so sánh với danh sách để biết sự khác nhau giữa xâu (string) và danh sách (list).

**Ví dụ 1:** Xâu kí tự và cách truy cập đến từng kí tự của xâu.

* Tạo biến `s` có giá trị là "Thời khoá biểu".
* Lệnh `len(s)` trả về độ dài của xâu hay số lượng các kí tự có trong xâu.
  Kết quả: `14`
* Lệnh `s[0]` truy cập kí tự đầu tiên của xâu (chỉ số 0).
  Kết quả: `'T'`
* Lệnh `s[10]` truy cập kí tự ở vị trí chỉ số 10 của xâu.
  Kết quả: `'b'`

Một **xâu kí tự** được hiểu là một dãy các kí tự. Tương tự danh sách, ta có thể truy cập từng kí tự của xâu thông qua **chỉ số**, chỉ số bắt đầu từ 0.

**Ví dụ 2:** Quan sát các lệnh sau để thấy sự khác nhau giữa xâu và danh sách.

* Tạo danh sách `d` với các phần tử `["a","b","c"]`.
* Gán giá trị "A" cho phần tử đầu tiên của danh sách `d[0]`. (Việc này thành công, danh sách có thể thay đổi được phần tử)
* Tạo biến `s` với giá trị "abc".
* Khi cố gắng gán giá trị "A" cho kí tự đầu tiên của xâu `s[0]`, chương trình báo lỗi.
  Kết quả:
  `Traceback (most recent call last):`
  `File "<pyshell#15>", line 1, in <module>`
  `s[0] = "A"`
  `TypeError: 'str' object does not support item assignment`

Python không cho phép thay đổi từng kí tự của một xâu. Điều này khác với danh sách.
Python không có kiểu dữ liệu kí tự. Kí tự chính là xâu có độ dài 1. Xâu rỗng được định nghĩa như sau:
Xâu rỗng được định nghĩa bằng cách gán biến `empty` với cặp dấu nháy kép rỗng.

Xâu kí tự trong Python là dãy các kí tự Unicode. Xâu có thể được coi là danh sách các kí tự nhưng không thay đổi từng kí tự của xâu. Truy cập từng kí tự của xâu qua chỉ số, chỉ số từ 0 đến độ dài len() – 1.

1. Các xâu kí tự sau có hợp lệ không?
   a) "123&*()+–ABC"
   b) "1010110&0101001"
   c) "Tây Nguyễn"
   d) 11111111 = 256
2. Mỗi xâu hợp lệ ở Câu 1 có độ dài bằng bao nhiêu?

## 2. LỆNH DUYỆT KÍ TỰ CỦA XÂU

### Hoạt động 2 Tìm hiểu lệnh duyệt từng kí tự của xâu

Quan sát các lệnh sau để biết cách duyệt từng kí tự của xâu kí tự bằng lệnh for. Có hai cách duyệt, theo chỉ số và theo phần tử của xâu kí tự.

Duyệt theo chỉ số với lệnh `range()`:
```
>>> s = "Thời khoá biểu"
>>> for i in range(len(s)):
>>>     print(s[i],end = " ")
```
Kết quả output:
`T h ờ i k h o á b i ể u`

Duyệt theo kí tự của xâu kí tự:
```
>>> for ch in s:
>>>     print(ch, end = " ")
```
Kết quả output:
`T h ờ i k h o á b i ể u`

*   Cách thứ nhất, biến i lần lượt chạy theo chỉ số của xâu kí tự s, từ 0 đến len(s) – 1. Kí tự tại chỉ số i là s[i].
*   Cách thứ hai duyệt theo từng kí tự của xâu s. Biến ch sẽ được gán lần lượt các kí tự của xâu s từ đầu đến cuối.

**Chú ý**: Từ khoá **in**, tuỳ trường hợp cụ thể, hoặc là toán tử lôgic dùng để kiểm tra một giá trị có mặt hay không trong một vùng giá trị/danh sách/xâu, hoặc để chọn lần lượt từng phần tử trong một vùng giá trị/danh sách/xâu.

Kiểm tra xem kí tự "a" có trong xâu "abcd" không:
```
>>> "a" in "abcd"
```
Kết quả output:
`True`

Kiểm tra xem xâu con "abc" có trong xâu "abcd" không:
```
>>> "abc" in "abcd"
```
Kết quả output:
`True`

Có thể duyệt các kí tự của xâu bằng lệnh **for** tương tự như với danh sách. **s1 in s2** trả lại giá trị **True** nếu **s1** là xâu con của **s2**.

1. Sau khi thực hiện các lệnh sau, biến skq sẽ có giá trị bao nhiêu?
Đoạn mã Python này duyệt qua từng kí tự trong xâu "81723". Nếu kí tự đó (sau khi chuyển sang số nguyên) là số lẻ (chia 2 dư khác 0), thì kí tự đó được nối vào biến `skq`.

2. Cho s1 = "abc", s2 = "ababcabca". Các biểu thức logic sau cho kết quả là đúng hay sai?
a) s1 in s2
b) s1 + s1 in s2
c) "abcabca" in s2
d) "abc123" in s2

## THỰC HÀNH
### Các lệnh cơ bản làm việc với xâu kí tự

Nhiệm vụ 1. Viết chương trình nhập số tự nhiên n là số học sinh, sau đó nhập họ và tên học sinh. Lưu họ và tên học sinh vào một danh sách. In danh sách ra màn hình, mỗi họ tên trên một dòng.

**Hướng dẫn.** Chương trình có thể như sau:
Đoạn mã Python này yêu cầu người dùng nhập số lượng học sinh (`n`), sau đó lặp `n` lần để nhập họ tên từng học sinh và lưu vào danh sách `ds_lop`. Cuối cùng, nó in ra danh sách các họ tên học sinh, mỗi họ tên trên một dòng.

Nhiệm vụ 2. Nhập một xâu kí tự S từ bàn phím rồi kiểm tra xem xâu S có chứa xâu con "10" không.

**Hướng dẫn.** Cách 1. Nếu xâu S chứa xâu con "10" thì sẽ có chỉ số k mà S[k] = "1" và S[k+1] = "0". Cách 2. Dùng toán tử **in** để kiểm tra xâu "10" có là xâu con của S.

### Cách 1: Duyệt kí tự của xâu theo chỉ số.
Đoạn mã Python này yêu cầu người dùng nhập một xâu kí tự bất kì và khởi tạo biến `kq` (kết quả) là `False`.

Đoạn mã này thực hiện kiểm tra xem một xâu S có chứa xâu con "10" hay không bằng cách duyệt qua từng cặp kí tự liên tiếp trong xâu. Nếu tìm thấy "1" và "0" liền kề, nó sẽ báo "Xâu gốc có chứa xâu '10'". Ngược lại, nếu duyệt hết mà không tìm thấy, nó sẽ báo "Xâu gốc không chứa xâu '10'".

### Cách 2: Sử dụng toán tử **in**.

Đoạn mã này yêu cầu người dùng nhập một xâu kí tự bất kì. Sau đó, nó kiểm tra xem xâu con "10" có tồn tại trong xâu vừa nhập hay không bằng cách sử dụng toán tử `in`. Kết quả sẽ được in ra màn hình là "Xâu gốc có chứa xâu '10'" hoặc "Xâu gốc không chứa xâu '10'".

## LUYỆN TẬP

1.  Cho xâu S, viết đoạn lệnh trích ra xâu con của S bao gồm ba kí tự đầu tiên của S.
2.  Viết chương trình kiểm tra xâu S có chứa chữ số không. Thông báo "S có chứa chữ số" hoặc "S không chứa chữ số nào".

## VẬN DỤNG

1.  Cho hai xâu s1, s2. Viết đoạn chương trình chèn xâu s1 vào giữa s2, tại vị trí len(s2)//2. In kết quả ra màn hình.
2.  Viết chương trình nhập số học sinh và họ tên học sinh. Sau đó đếm xem trong danh sách có bao nhiêu bạn tên là "Hương".
    Gợi ý: Sử dụng toán tử **in** để kiểm tra một xâu có là xâu con của một xâu khác.
