# Bài 12: KIỂU DỮ LIỆU XÂU KÍ TỰ - XỬ LÍ XÂU KÍ TỰ

Học xong bài này, em sẽ:
*   Nhận biết được dữ liệu kiểu xâu.
*   Viết được câu lệnh Python trích xâu con từ xâu cho trước.
*   Sử dụng được một số phép xử lí xâu thường dùng trong Python.

Em đã từng sử dụng phần mềm xử lí văn bản. Theo em, trong ngôn ngữ lập trình, ngoài kiểu dữ liệu số có cần một kiểu dữ liệu không phải là số dùng cho các bài toán xử lí văn bản hay không? Nếu có kiểu dữ liệu như vậy thì nên có những phép xử lí nào trên dữ liệu thuộc kiểu đó?

## 1. Kiểu dữ liệu xâu kí tự

Em hãy đọc chương trình sau đây và cho biết mỗi biến: so_hop, khoi_luong_hop, don_vi_kl chứa dữ liệu thuộc kiểu nào?

Chương trình Python này yêu cầu người dùng nhập số hộp cafe, khối lượng mỗi hộp và đơn vị tính khối lượng, sau đó tính và in ra tổng khối lượng cafe.

Gợi ý: có thể dùng hàm `type()` để kiểm tra kết quả.

Để giải quyết các bài toán trong thực tế gồm cả dữ liệu số và không phải là số, các ngôn ngữ lập trình bậc cao đều cho chúng ta dùng các biến thuộc kiểu dữ liệu **xâu kí tự** và cung cấp một số công cụ để xử lí dữ liệu kiểu xâu kí tự. Một xâu kí tự là một dãy các kí tự. Trong Python, xâu kí tự được đặt trong cặp nháy đơn (hoặc nháy kép).

Ví dụ 1 minh hoạ một chương trình sử dụng kiểu dữ liệu xâu kí tự và một biến có chứa xâu kí tự.

Các kí tự trong xâu được đánh số bắt đầu từ 0. Python cung cấp hàm **len()** để đếm số kí tự trong một xâu kể cả kí tự dấu cách. Số kí tự trong xâu được gọi là **độ dài của xâu**.

*Chương trình minh họa xử lí xâu:*
Một chương trình Python yêu cầu người dùng nhập tên (một xâu kí tự), lưu vào biến `name`, sau đó in ra lời chào và lời chúc mừng sử dụng biến `name`.
Kết quả chạy chương trình với đầu vào "Phạm Anh Thư" sẽ là:
```
Bạn tên gì? Phạm Anh Thư
Chào bạn Phạm Anh Thư
Rất vui được làm quen với bạn!
Chúc bạn Phạm Anh Thư một ngày vui!
>>>
```

*Chương trình minh họa sử dụng hàm len():*
Một chương trình Python yêu cầu người dùng nhập tên, sau đó in ra lời chào và độ dài của tên đó bằng cách sử dụng hàm `len()`.
Hàm này cho biết độ dài xâu kí tự (số kí tự) chứa trong biến `name`.
Kết quả chạy chương trình với đầu vào "Phạm Anh Thư" sẽ là:
```
Bạn tên gì? Phạm Anh Thư
Chào bạn Phạm Anh Thư
12
>>>
```
"Phạm Anh Thư" gồm 12 kí tự.

## 2. Một số hàm xử lí xâu kí tự
Python cung cấp nhiều công cụ để xử lí xâu. Một số công cụ thường dùng là:

### a) Ghép xâu bằng phép +
Viết liên tiếp các xâu cần ghép theo thứ tự và đặt giữa hai xâu kề nhau dấu “+”. Có thể dùng dấu nháy đơn hoặc kép.

*Ví dụ về ghép xâu trong Python shell:*
```
>>> x = "ABC"
>>> y = "1234"
>>> z = "cba"
>>> r = x + y + z
>>> r
'ABC1234cba'
>>> "ABC" + "1234" + "cba"
'ABC1234cba'
>>>
```

### b) Đếm số lần xuất hiện xâu con
Hàm **y.count(x)** đếm số lần xuất hiện không giao nhau của x trong y.

*Ví dụ về đếm số lần xuất hiện xâu con trong Python shell:*
```
>>> y = "abc1234abc1234abc1234"
>>> print(y.count("a"))
3
>>> x = "c12"
>>> print(y.count(x,3))
2
>>>

>>> y = "aaa"
>>> x = "aa"
>>> print(y.count(x))
1
>>>
```

Có thể nêu các tham số xác định cụ thể phạm vi tìm kiếm. Ví dụ:
*   `y.count(x, 3)` cho biết số lần xuất hiện các xâu x không giao nhau trong xâu y nhưng chỉ trong phạm vi từ kí tự thứ ba đến kí tự cuối của xâu y.
*   `y.count(x, 3, 5)` cho biết số lần xuất hiện các xâu x không giao nhau trong xâu y nhưng chỉ trong phạm vi từ kí tự thứ ba đến kí tự thứ năm của xâu y.

### c) Xác định xâu con

Xác định **xâu con** của xâu y từ vị trí m đến trước vị trí n (m < n) ta có cú pháp: `y[m:n]`

Đoạn mã gán xâu "0123456" cho biến `y` và sau đó in ra xâu con từ vị trí 2 đến trước vị trí 5.
```
234
```

Đoạn mã gán xâu "0123456" cho biến `y` và sau đó in ra kí tự tại vị trí 2.
```
2
```

Các trường hợp đặc biệt:
*   `y[:m]` là xâu con gồm m kí tự đầu tiên của xâu y.
*   `y[m:]` là xâu con nhận được bằng cách bỏ m kí tự đầu tiên của xâu y.

### d) Tìm vị trí xuất hiện lần đầu tiên của một xâu trong xâu khác

Hàm `y.find(x)` trả về số nguyên xác định vị trí đầu tiên trong xâu y mà từ đó xâu x xuất hiện như một xâu con của xâu y. Nếu xâu x không xuất hiện như một xâu con, kết quả trả về sẽ là -1.

Đoạn mã tìm vị trí xuất hiện lần đầu của xâu con "xinh" và "bé" trong xâu "Cái xắc xinh xinh".
```
8
-1
```

### e) Thay thế xâu con

Hàm `y.replace(x1, x2)` tạo xâu mới từ xâu y bằng cách thay thế xâu con x1 của y bằng xâu x2. Tất cả các xâu con bằng x1 và không giao nhau của y đều được thay bằng xâu x2.

Em hãy đọc các chương trình sau đây và cho biết kết quả nhận được khi thực hiện chương trình.

Đoạn mã thay thế xâu con "sân đình" bằng "bờ ao" trong xâu "Trúc xinh trúc mọc sân đình".

Đoạn mã in ra hai xâu `a` và `b`, sau đó thay thế xâu con "bờ ao" bằng "sân đình" trong xâu `a` và thay thế xâu con "nơi nào" bằng "một mình" trong xâu `b`.

## Luyện tập
Bài 1. Hãy dự đoán kết quả đưa ra màn hình sau mỗi câu lệnh xuất dữ liệu **print ()** trong chương trình ở hình bên và sau đó dùng cửa sổ Shell để đối chiếu, kiểm tra từng kết quả dự đoán.

Chương trình thực hiện các thao tác với xâu:
*   Định nghĩa hai xâu `xau1` và `xau2`.
*   Nối hai xâu `xau1` và `xau2` thành `xau` mới.
*   In ra xâu `xau` đã nối.
*   Đếm số lần xuất hiện của kí tự "N" trong xâu `xau` từ vị trí thứ 6.
*   Tìm vị trí xuất hiện đầu tiên của xâu con "Khánh" trong xâu `xau`.
*   Trích xuất một phần của xâu `xau` từ vị trí 25 đến 33.
*   Thay thế tất cả các lần xuất hiện của xâu con "Khánh" bằng xâu "An" trong `xau` và in ra xâu mới.

Bài 2. Em hãy viết chương trình nhập từ bàn phím xâu s ghi ngày tháng dạng dd/mm/yyyy, trong đó dd là hai kí tự chỉ ngày, mm là hai kí tự chỉ tháng, yyyy là bốn kí tự chỉ năm. Sau đó đưa ra màn hình ngày, tháng, năm dưới dạng xâu “Ngày dd tháng mm năm yyyy”.

Ví dụ:
*   INPUT: 15/12/2022
*   OUTPUT: Ngày 15 tháng 12 năm 2022

Nhập vào từ bàn phím hai xâu s1 và s2, mỗi xâu không chứa kí tự dấu cách ở đầu và cuối xâu cũng như không chứa hai hay nhiều dấu cách liên tiếp nhau. Nếu xâu không chứa dấu cách thì nó là một từ, trong trường hợp ngược lại, dấu cách là dấu phân tách các từ trong xâu. Ví dụ, xâu “Bước tới Đèo Ngang, bóng xế tà” chứa bảy từ. Em hãy viết chương trình xác định và đưa ra màn hình tổng số từ trong hai xâu s1 và s2 đã cho.

Ví dụ:
*   INPUT:
    *   Dưới trăng quyên đã gọi hè
    *   Đầu tường lửa lựu lập loè đâm bông
*   OUTPUT: 14

Trong các câu sau đây, những câu nào đúng?
*   1) Có thể ghép các xâu để được xâu mới.
*   2) Có thể tìm vị trí một xâu con trong một xâu.
*   3) Không thể xoá một xâu con trong một xâu.
*   4) Không thể đếm số lần xuất hiện một xâu con trong một xâu.

## Tóm tắt bài học

*   Trong các ngôn ngữ lập trình bậc cao có kiểu dữ liệu xâu kí tự và các chương trình con cung cấp thao tác xử lí xâu kí tự.
*   Trong Python, phép “+” dùng để ghép nối các xâu.
*   Trong Python, có một số hàm xử lí xâu thường dùng: xác định độ dài xâu, đếm số lần xuất hiện xâu con, tìm vị trí xuất hiện lần đầu tiên của một xâu trong xâu khác, thay thế xâu con và cách xác định xâu con.

## BÀI TÌM HIỂU THÊM
### THAY THẾ THIẾT BỊ VÀO – RA CHUẨN

Giống như nhiều ngôn ngữ lập trình khác, Python mặc định sử dụng bàn phím làm thiết bị cho nhập dữ liệu vào (**stdin**) và màn hình làm thiết bị xuất dữ liệu ra (**stdout**). Như vậy, bàn phím và màn hình là thiết bị vào – ra chuẩn.

Khi dữ liệu vào – ra lớn, các thiết bị này không còn phù hợp trong việc thực hiện chương trình cũng như gỡ lỗi. Python cho phép thay thiết bị chuẩn bằng file văn bản. Ví dụ, dữ liệu nhập vào được chuẩn bị trong file **input.txt** (bằng **notepad** hay bằng chính chương trình soạn thảo của Python), kết quả sẽ được đưa ra file văn bản **output.txt**, việc thay thế thiết bị chuẩn được thực hiện theo mẫu sau:

Để đưa vào và đưa ra tiếng Việt

Đoạn mã Python này minh họa cách chuyển hướng luồng nhập và xuất chuẩn. Nó import module `sys`, mở file `input.txt` ở chế độ đọc và file `output.txt` ở chế độ ghi, cả hai đều sử dụng mã hóa UTF-8 để hỗ trợ tiếng Việt. Sau đó, nó gán **sys.stdin** cho file `input.txt` và **sys.stdout** cho file `output.txt`. Đoạn mã cũng bao gồm các chú thích về vị trí bắt đầu và kết thúc của chương trình giải bài toán thực tế, và lệnh đóng file `output.txt`.

Ví dụ, chương trình giải bài toán có thể là một đoạn mã đọc hai số nguyên từ đầu vào, sau đó tính tổng và in kết quả ra đầu ra.

Chẳng hạn, nếu đưa ba dòng lệnh nhập n và m vào và sau đó in ra tổng của chúng thì với file **input.txt** ta sẽ nhận được file **output.txt**.

Input ví dụ:
```
5
3
```
Output ví dụ:
```
8
```

Lưu ý: Tên file trong các câu lệnh **open** và các tên biến **fi**, **fo** là tuỳ chọn.
