# Bài 3: THỰC HÀNH LÀM QUEN VÀ KHÁM PHÁ PYTHON

Học xong bài này, em sẽ:
*   Viết và thực hiện được một vài chương trình Python đơn giản có sử dụng biểu thức số học.
*   Bước đầu nhận thấy được cách báo lỗi của Python.
*   Biết được Python dùng màu sắc để hỗ trợ người dùng.
*   Viết được câu lệnh nhập dữ liệu là một dòng chữ.

## Bài 1. Tổng bình phương ba số

Em hãy gán giá trị số nguyên cho ba biến tương ứng a, b, c, mỗi giá trị có thể là số dương, số âm hoặc bằng 0 và có số chữ số tuỳ ý. Viết chương trình đưa ra màn hình tổng và tổng bình phương ba số đó.

Ví dụ:
*   INPUT: a = 2, b = 5, c = 3
*   OUTPUT: Tổng ba số: 10, Tổng bình phương ba số: 38

Gợi ý: Có thể giải bài toán trên theo chế độ đối thoại (ở cửa sổ Shell) hoặc chế độ soạn thảo (ở cửa sổ Code).

Chế độ đối thoại: Trong cửa sổ Shell, soạn thảo các câu lệnh như ở Hình 1.

Mô tả đoạn mã Python trong cửa sổ Shell:
Đoạn mã thực hiện gán giá trị cho ba biến `a`, `b`, `c` và sau đó tính toán, in ra tổng của ba số và tổng bình phương của ba số đó.

Các bước thực hiện:
1.  Gán giá trị cho biến `a`: `a = 2`
2.  Gán giá trị cho biến `b`: `b = 5`
3.  Gán giá trị cho biến `c`: `c = 3`
4.  Tính và in ra tổng ba số: `print('Tổng ba số:', a + b + c)`
    *   Kết quả output: `Tổng ba số: 10`
5.  Tính và in ra tổng bình phương ba số: `print('Tổng bình phương ba số:', a*a + b*b + c*c)`
    *   Kết quả output: `Tổng bình phương ba số: 38`

Lưu ý:
*   Mỗi lần chạy khác, có thể gõ lại các câu lệnh với các giá trị mới cho `a`, `b`, `c`.
*   Có thể có hoặc không có dấu cách trước và sau dấu phẩy, trước và sau dấu phép tính trong các câu lệnh `print`.

Chế độ soạn thảo Vào mục **File**, chọn **New File** và soạn thảo chương trình lưu lại với tệp có đuôi **.py**, vào mục **Run**, chọn **Run module** để thực hiện chương trình.

*Mô tả mã nguồn hiển thị trong cửa sổ Code:*
Chương trình này yêu cầu người dùng nhập ba số nguyên (a, b, c). Sau đó, nó tính toán và in ra tổng của ba số đó, và tổng bình phương của ba số đó.

*Kết quả chạy chương trình hiển thị trong cửa sổ Shell với các giá trị đầu vào:*
Nếu a = 2, b = 5, c = 3 thì:
Tổng ba số: 10
Tổng bình phương ba số: 38

Em hãy thực hiện chương trình với một số bộ dữ liệu khác nhau.

## Bài 2: Làm quen với hai cửa sổ lập trình của Python

Lần lượt theo các yêu cầu a, b và c sau đây, em hãy viết chương trình để trả lời được câu hỏi trong bài toán Tìm số lượng bi.

### Tìm số lượng bi

Có hai hộp đựng các viên bi. Hộp thứ nhất được dán nhãn bên ngoài là A, trong hộp có 20 viên bi. Hộp thứ hai được dán nhãn bên ngoài là B, trong hộp có 100 viên bi. Thực hiện thao tác sau: Bỏ 5 viên bi ra khỏi hộp A, sau đó bỏ khỏi hộp B số bi bằng số bi còn lại trong hộp A.

Hãy cho biết số bi trong hộp B sau khi thực hiện thao tác trên.

* **Yêu cầu a:**
  Trong cửa sổ Shell, viết chương trình để máy thực hiện mỗi câu lệnh ngay sau khi gõ câu lệnh đó vào.

* **Yêu cầu b:**
  Trong cửa sổ Code viết chương trình và lưu tệp chương trình với tên là “Tim-so-bi.py”. Chạy chương trình đó để so sánh với kết quả ở yêu cầu a.

* **Yêu cầu c:**
  Sửa chương trình trong tệp “Tim-so-bi.py” với dữ liệu ban đầu là: hộp A có 30 viên bi, hộp B có 50 viên bi. Chạy lại chương trình để nhận kết quả với dữ liệu đầu vào mới.

## Bài 3. Làm quen với thông báo lỗi của Python

Python phân biệt chữ hoa và chữ thường, nên chương trình sau có lỗi.

Một đoạn mã Python gán giá trị 20 cho biến `N` (chữ hoa) nhưng sau đó cố gắng in giá trị của biến `n` (chữ thường), dẫn đến lỗi `NameError` vì biến `n` chưa được định nghĩa.

Em hãy thực hiện chương trình này xem Python phản hồi như thế nào.

## Bài 4. Tìm hiểu Python sử dụng màu sắc trong chương trình

Em hãy tìm hiểu và cho biết màu sắc của những thành phần sau đây trong chương trình:

*   Câu lệnh **print** ().
*   Thông báo lỗi Python đưa ra.
*   Đoạn chữ nằm giữa cặp dấu nháy đơn (hoặc nháy kép).
*   Kết quả đưa ra ra màn hình.

Em có thích Python dùng các màu khác nhau như thế không? Theo em, điều đó giúp gì cho người lập trình?

## Bài 5. Làm quen với nhập dữ liệu là một dòng chữ

Hai đoạn chương trình (viết bằng hai ngôn ngữ lập trình khác nhau) ở đây có cùng mục đích: nhập vào từ bàn phím tên của một người và in ra màn hình lời chào dành cho người đó.

a) Chương trình Scratch: Một đoạn mã Scratch thực hiện việc hỏi người dùng tên của họ, lưu câu trả lời vào biến `Name` và sau đó hiển thị lời chào "Chào bạn" kèm theo tên đã nhập.

b) Chương trình Python: Một đoạn mã Python nhập tên từ bàn phím bằng hàm `input()` và lưu vào biến `Name`, sau đó in ra màn hình lời chào "Chào bạn" cùng với tên đã nhập bằng hàm `print()`.

Em hãy viết thêm vào chương trình Python ở Hình 5a để khi chạy chương trình đó ta được đọc dòng chữ hướng dẫn nhập dữ liệu và sau khi nhập dữ liệu vào, máy tính sẽ hiển thị giá trị vừa nhập (minh hoạ ở Hình 5b).

Đoạn mã trên minh họa cách **nhập dữ liệu từ bàn phím** và **in kết quả ra màn hình** trong Python. Cụ thể, nó yêu cầu người dùng nhập vào ngày tháng năm sinh và sau đó hiển thị thông tin đã nhập.

Viết thêm vào

Khi chạy, chương trình sẽ hiển thị lời nhắc `Gõ vào ngày tháng năm sinh: ` và sau khi người dùng nhập `05/09/2010`, nó sẽ in ra `Ngày sinh: 05/09/2010`.

## Luyện tập
Du lịch Phan Xi Păng
Để lên đỉnh Phan Xi Păng cần mua vé cáp treo a nghìn đồng/1 người lớn và b nghìn đồng/1 trẻ em, vé xe lửa là u nghìn đồng/1 người lớn và v nghìn đồng/1 trẻ em. Đoàn du lịch có x người, trong số đó có y trẻ em. Hãy xác định số tiền cần chuẩn bị để mua vé cho cả đoàn và đưa kết quả ra màn hình.

Các dữ liệu a, b, u, v, x, y là các số nguyên không âm (y ≤ x).
Gợi ý: Số tiền cần chuẩn bị được tính theo công thức sau đây:
Số_tiền = a × (x – y) + u × (x – y) + b × y + v × y
= (a + u) × (x – y) + (b + v) × y

Lưu ý: Có thể đưa ra dòng thông báo tuỳ chọn trước mỗi phép nhập dữ liệu và trước mỗi kết quả, Python cho phép đưa ra dòng thông báo dưới dạng tiếng Việt có dấu.

Ví dụ:
Input:
* a = 60
* b = 30
* u = 50
* v = 25
* x = 40
* y = 10

Output:
* Tổng số tiền vé: 3850 nghìn đồng.
