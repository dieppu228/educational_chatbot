# Bài 5: THỰC HÀNH VIẾT CHƯƠNG TRÌNH ĐƠN GIẢN

Học xong bài này, em sẽ:
*   Viết và thực hiện được một vài chương trình Python đơn giản với dữ liệu nhập vào từ bàn phím.
*   Sử dụng được một vài hàm toán học do Python cung cấp.
*   Nhận biết được chú thích trong một chương trình Python.

## Bài 1. Giải phương trình bậc nhất

Chương trình ở Hình 1a được viết để giải phương trình bậc nhất ax + b = 0, với a, b là hai số thực nhập từ bàn phím (a ≠ 0) và nghiệm được thông báo ra màn hình. Tuy nhiên, chương trình đó còn viết thiếu ở những vị trí “…”. Em hãy hoàn thiện chương trình và kiểm thử xem với dữ liệu vào a = 1 và b = 2, chương trình em vừa hoàn thiện có cho kết quả giống như Hình 1b không?

**Chương trình:**
Một đoạn mã Python cho phép người dùng nhập vào hai số thực `a` và `b` từ bàn phím để giải phương trình bậc nhất `ax + b = 0`. Đoạn mã còn thiếu một phần tính toán giá trị `b` và hiển thị nghiệm của phương trình.

**Ví dụ chạy chương trình với a = 1, b = 2:**
Kết quả của chương trình giải phương trình bậc nhất khi `a = 1` và `b = 2` là:
```
Nghiệm của phương trình là -2.0
```

Chương trình sẽ đưa ra màn hình thông tin gì nếu nhập vào giá trị a = 0?

## Bài 2. An ninh lương thực

Trung bình mỗi người dân cần có a kg gạo để ăn, chế biến và phục vụ chăn nuôi trong một năm. Để đảm bảo an ninh lương thực, tổng số gạo dự trữ trong các kho của nhà nước chia cho đầu người phải lớn hơn hoặc bằng a kg.

Một nước có số dân là b thì cần dự trữ tối thiểu bao nhiêu ki-lô-gam gạo? Em hãy viết chương trình nhập từ bàn phím hai số a, b và đưa ra màn hình khối lượng gạo tối thiểu cần dự trữ.

Yêu cầu: Cần đưa ra màn hình hướng dẫn nhập dữ liệu và thông báo kết quả bằng tiếng Việt có dấu.

Ví dụ:
INPUT: a = 365, b = 91086294
OUTPUT: Số gạo cần dự trữ: 33246497310

# Bài 3. Tìm ước chung lớn nhất
Em hãy viết chương trình nhập vào từ bàn phím hai số nguyên a và b, tính và đưa ra màn hình ước chung lớn nhất của hai số đó.

Gợi ý: Hãy tìm hiểu một số hàm toán học thường dùng trong Python.

Ví dụ:
INPUT: a = 9855, b = 11556
OUTPUT: Ước chung lớn nhất: 27

## Một số hàm toán học thường dùng
Để hỗ trợ cho người dùng trong các chương trình tính toán, mỗi ngôn ngữ lập trình bậc cao đều cung cấp sẵn nhiều hàm toán học. Các hàm tính toán có sẵn như vậy thường được lưu trữ trong một thư viện thuộc hệ thống lập trình của ngôn ngữ bậc cao đó.

Trong Python, các hàm toán học lưu trữ trong thư viện **math**. Một số hàm toán học thường dùng bao gồm:
*   Hàm **abs(x)**: Tính giá trị tuyệt đối của x (|x|)
*   Hàm **ceil(x)**: Trả về số nguyên nhỏ nhất, lớn hơn hoặc bằng giá trị x
*   Hàm **gcd(x, y)**: Tính ước chung lớn nhất của số nguyên x và y
*   Hàm **sqrt(x)**: Tính căn bậc hai của x
*   Hàm **log(x)**: Tính lôgarit tự nhiên của x (lnx)
*   Hàm **exp(x)**: Tính lũy thừa e mũ x (eˣ)

Có thể biết chi tiết về các hàm qua trang web chính thức của Python: https://www.python.org/

Hàm **abs()** có thể sử dụng trực tiếp. Với các hàm còn lại như **ceil()**, **gcd()**, ... ta cần đưa vào chương trình câu lệnh **import math** trước khi gọi hàm lần đầu tiên. Thông thường câu lệnh này được viết ngay ở đầu chương trình.

Lời gọi tới hàm có dạng: **math.<tên_hàm>**

Mô tả đoạn mã Python 1:
- Lệnh sử dụng thư viện hàm toán học.
- Lời gọi hàm tính căn bậc hai của 5.
- Kết quả tính căn bậc hai của 5: 2.236079774979
- Kết quả tính 16/3: 5.333333333333333
- Lời gọi hàm trả về số nguyên nhỏ nhất lớn hơn hoặc bằng giá trị của 16/3.
- Kết quả làm tròn 16/3 bằng hàm **ceil**: 6

# Bài 4: Làm quen với ghi chú thích trong chương trình

Em hãy soạn thảo rồi chạy thử chương trình ở Hình 3 sau đây trong hai trường hợp là có chú thích và không có chú thích. Em có nhận xét gì khi so sánh kết quả thực hiện chương trình trong hai trường hợp nêu trên.

## Tìm hiểu về ghi chú thích trong chương trình

Khi soạn thảo chương trình, ngoài các câu lệnh, người lập trình có thể viết thêm các dòng chú thích. Các dòng chú thích không ảnh hưởng đến nội dung chương trình mà chỉ giúp cho người đọc nhanh chóng biết được mục đích của các câu lệnh và ý nghĩa của chương trình. Trong Python, thông tin chú thích viết trên một dòng, bắt đầu bằng kí tự **#**. Nhờ kí tự đánh dấu đó mà máy tính nhận biết được dòng chú thích.

Mô tả đoạn mã Python 2:
- Chú thích cho biết mục đích của chương trình: Giải phương trình bậc hai.
- Lệnh sử dụng thư viện hàm toán học.
- Khai báo và gán giá trị cho các biến a, b, c.
- Tính toán giá trị x1.
- Tính toán giá trị x2, kèm chú thích cho biết kiến thức câu lệnh sử dụng: Định lí Viet.
- In ra giá trị của x1 và x2.

## Luyện tập
*   Viết chương trình tính và đưa ra màn hình vận tốc v (m/s) khi chạm mặt đất của một vật rơi tự do từ độ cao h, biết rằng v = √(2gh), trong đó g là gia tốc trọng trường (g ≈ 9.8 m/s²). Độ cao h tính theo mét được nhập từ bàn phím.
