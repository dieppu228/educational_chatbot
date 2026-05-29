# Bài 7: THỰC HÀNH CÂU LỆNH RẼ NHÁNH

Học xong bài này, em sẽ:
*   Viết được chương trình đơn giản có sử dụng **câu lệnh rẽ nhánh**.

## Bài 1. Lấy ví dụ về câu lệnh if

Bảng sau đây cho một ví dụ về viết câu lệnh **if** tương ứng với mô tả điều kiện để đưa ra một thông báo trên màn hình. Trong bảng biến age là biến số nguyên chứa giá trị tuổi của một người. Em hãy cho thêm hai ví dụ nữa tương tự như ví dụ đã có trong bảng.

*   Mô tả: Nếu age lớn hơn hoặc bằng 18 đưa ra thông điệp “Bạn đã đủ tuổi bầu cử”.
    *   Mã nguồn: Chương trình kiểm tra nếu biến `age` lớn hơn hoặc bằng 18 thì in ra màn hình thông báo "Bạn đã đủ tuổi bầu cử".

## Bài 2. Chia kẹo

Có n chiếc kẹo và m em bé. Hãy viết chương trình nhập vào hai số nguyên dương n, m và kiểm tra n chiếc kẹo có chia đều được cho m em bé hay không (thông báo ra màn hình “Có” hoặc “Không”). Chạy chương trình ba lần, mỗi lần với bộ dữ liệu n, m khác nhau.

Gợi ý: Để có thể chia đều số kẹo thì n phải chia hết cho m, như vậy ở đây cần kiểm tra số dư của phép chia n cho m có bằng 0 hay không, tức là kiểm tra điều kiện **n % m == 0**.

## Bài 3. Tìm lỗi sai

Ba bạn Bình, An, Phúc thảo luận với nhau để viết chương trình Python nhập vào từ bàn phím ba số thực khác nhau và in ra màn hình số đứng giữa trong ba số (số đó không là lớn nhất và cũng không là nhỏ nhất).

Mỗi bạn soạn thảo chương trình và chạy thử trên máy tính của mình, nhưng mỗi bạn đều gặp báo lỗi của Python. Em hãy xác định lỗi ở chương trình của mỗi bạn, sửa lỗi cho từng bạn sao cho chương trình chạy được và đưa ra kết quả đúng.

*   Mã nguồn (chương trình của bạn Bình): Chương trình này được thiết kế để nhập ba số thực `a`, `b`, `c` và tìm ra số nằm giữa chúng bằng cách so sánh các giá trị.
    *   Kết quả: Chương trình báo lỗi `SyntaxError: invalid syntax` (lỗi cú pháp không hợp lệ).

Chương trình minh họa việc tìm số ở giữa của ba số nhập vào, tuy nhiên cả hai phiên bản đều có lỗi cú pháp (invalid syntax), đặc biệt phiên bản thứ hai có các dòng lệnh `if` chưa hoàn chỉnh.

## Bài 4: Tìm số lớn nhất

Viết chương trình nhập vào từ bàn phím ba số nguyên, mỗi số ghi trên một dòng và đưa ra màn hình giá trị lớn nhất trong các số đã nhập. Em hãy chạy chương trình với một số bộ dữ liệu vào khác nhau.

Ví dụ:
*   **INPUT**
    *   a = 6
    *   b = 10
    *   c = 4
*   **OUTPUT**
    *   Max = 10

Em hãy đọc hiểu sơ đồ khối và chương trình, thực hiện chương trình và cho nhận xét.

### Sơ đồ khối tìm số lớn nhất
*   Bắt đầu
*   Nhập a, b, c
*   max = a
*   Nếu max < b:
    *   Đúng: max = b
    *   Sai: tiếp tục
*   Nếu max < c:
    *   Đúng: max = c
    *   Sai: tiếp tục
*   Đưa ra max
*   Kết thúc

Chương trình giải Bài 4 là một đoạn mã Python thực hiện việc tìm số lớn nhất trong ba số nguyên được nhập từ bàn phím. Chương trình khởi tạo giá trị lớn nhất (max) bằng số đầu tiên (a), sau đó so sánh max với số thứ hai (b) và số thứ ba (c), cập nhật max nếu tìm thấy giá trị lớn hơn. Cuối cùng, chương trình in ra giá trị lớn nhất đã tìm được. Với các giá trị nhập vào là a=6, b=10, c=4, chương trình sẽ cho kết quả `Max = 10`.

## Bài 5. Tiền điện
Trong tháng người dùng tiêu thụ x (kWh) điện. Nếu x ≤ a thì số tiền phải trả là x × d₁, nếu a < x ≤ b thì số tiền phải trả là a × d₁ + (x – a) × d₂, nếu x > b thì số tiền phải trả là a × d₁ + (b – a) × d₂ + (x – b) × d₃. Em hãy viết chương trình nhập vào từ bàn phím các số nguyên dương a, b, d₁, d₂, d₃ và x, tính và đưa ra màn hình số tiền điện phải trả. Tìm hiểu bảng giá điện hiện hành và chạy chương trình một số lần sao cho có đủ các bộ dữ liệu đầu vào đại diện cho các mức tính tiền điện.

## BÀI TÌM HIỂU THÊM

### CÂU LỆNH IF VÀ NHIỀU NHÁNH RẼ

Có thể dùng câu lệnh **if** để rẽ nhiều nhánh, các nhánh lồng được bắt đầu bằng từ khoá **elif** và có khoảng cách đầu dòng giống ở dòng câu lệnh **if**.

Cấu trúc câu lệnh **if** với nhiều nhánh rẽ: nếu Điều kiện 1 đúng thì thực hiện Nhóm câu lệnh 1; ngược lại, nếu Điều kiện 2 đúng thì thực hiện Nhóm câu lệnh 2; nếu cả hai điều kiện trên đều sai thì thực hiện Nhóm câu lệnh 3.

Ví dụ: Một người cân nặng w (kg) và cao h (m) sẽ có chỉ số **BMI** = w/h². Bảng đánh giá bên dưới là bảng đánh giá sức khoẻ cho người châu Á theo chỉ số **BMI**. Trong Python, để viết chương trình đánh giá sức khoẻ theo chỉ số **BMI** ta có thể sử dụng các lệnh **if** lồng nhau.

Chương trình dưới đây yêu cầu người dùng nhập cân nặng (kg) và chiều cao (m), sau đó tính chỉ số BMI. Dựa vào giá trị BMI, chương trình sử dụng cấu trúc **if-elif-else** để in ra kết quả đánh giá sức khỏe là "Thiếu cân.", "Bình thường." hoặc "Thừa cân.".

Kết quả ví dụ
Cân nặng (kg): 55
Chiều cao (m): 1.65
Bình thường.
>>>
