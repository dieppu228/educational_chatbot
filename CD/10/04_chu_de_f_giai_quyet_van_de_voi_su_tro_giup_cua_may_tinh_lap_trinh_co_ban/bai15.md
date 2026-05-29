## Bài 15: THỰC HÀNH VỚI KIỂU DỮ LIỆU DANH SÁCH

### Học xong bài này, em sẽ:
*   Viết được chương trình đơn giản sử dụng kiểu dữ liệu danh sách.
*   Làm quen và khai thác được một số hàm xử lí danh sách.

### Bài 1. Cập nhật danh sách
Viết chương trình nhập vào từ bàn phím một danh sách các số nguyên, sau đó thực hiện:
*   Thay thế các phần tử âm bằng –1, phần tử dương bằng 1, giữ nguyên các phần tử giá trị 0.
*   Đưa ra màn hình danh sách nhận được.

Ví dụ:
Input: -5 0 6 8 -3 -4 -2 0 4 6
Output: -1 0 1 1 -1 -1 -1 0 1 1

Hướng dẫn:
*   Tạo danh sách a từ dữ liệu nhập vào.
*   Duyệt các phần tử a_i (với i = 0, 1, 2,..., len (a) – 1); thay a_i = 1 nếu a_i > 0 và a_i = –1 nếu a_i < 0.

Lưu ý: Lệnh **print ()** chứa tham số **end = ' '** để thêm dấu cách giữa các phần tử của danh sách.

Tham khảo chương trình:
Chương trình thực hiện việc nhập một dãy số nguyên từ bàn phím để tạo danh sách `a`. Sau đó, nó duyệt qua từng phần tử của danh sách. Nếu một phần tử lớn hơn 0, nó được thay thế bằng 1. Nếu một phần tử nhỏ hơn 0, nó được thay thế bằng -1. Các phần tử có giá trị 0 được giữ nguyên. Cuối cùng, chương trình in ra các phần tử của danh sách `a` đã được cập nhật, ngăn cách bởi dấu cách.

### Bài 2: Các số đặc biệt của dãy số

Viết chương trình nhập vào từ bàn phím danh sách số nguyên a; đếm và đưa ra màn hình số lượng các phần tử lớn hơn phần tử đứng trước và phần tử đứng sau nó.

Ví dụ:
INPUT: 5 -3 0 4 -1 2 -6 -4 -5 9 -12 15
OUTPUT: 4

Hướng dẫn:
*   Tạo danh sách a từ dữ liệu nhập vào.
*   Duyệt các phần tử a_i (với i = 1, 2,..., len(a) -1), đếm các phần tử a_i thoả mãn điều kiện a_i-1 < a_i > a_i+1.
*   Tham khảo chương trình ở Hình 2.

Đoạn mã Python này đọc một dãy số nguyên từ người dùng. Sau đó, nó duyệt qua dãy số để đếm và in ra số lượng các phần tử mà giá trị của chúng lớn hơn cả phần tử đứng ngay trước và phần tử đứng ngay sau nó.

### Bài 3. Trò chơi với các chiếc giày

Có n đôi giày cùng loại chỉ khác nhau về kích cỡ được xếp thành một hàng theo thứ tự ngẫu nhiên. Chủ trò bí mật rút một chiếc giày và giấu đi, sau đó yêu cầu người chơi cho biết chiếc giày được giấu là chiếc giày trái hay phải và có số là bao nhiêu.

Hà My muốn viết một chương trình nhập vào một dãy, mỗi số trong dãy mô tả một chiếc giày, số có giá trị âm cho biết đó là giày trái, số có giá trị dương cho biết đó là giày phải, giá trị tuyệt đối của số là kích cỡ của giày. Chương trình sẽ cho biết chiếc giày nào còn thiếu trong dãy.

Cách làm thông thường để tìm ra chiếc giày còn thiếu là đi ghép các đôi giày, tuy nhiên cách làm này sẽ mất nhiều thời gian. Một cách làm đơn giản là dựa trên nhận xét: Nếu dãy không thiếu chiếc giày nào thì tổng sẽ bằng 0, nên có thể xác định chiếc giày còn thiếu khi biết tổng các số trong dãy. Chương trình Hà My viết theo cách làm trên, tuy nhiên chương trình vẫn còn có lỗi. Em hãy giúp Hà My sửa các lỗi để nhận được chương trình chạy được và cho ra kết quả đúng.

Đoạn mã Python này thực hiện việc nhập vào một dãy các số (kích cỡ giày), tính tổng của các số đó, sau đó in ra thông báo "Chiếc giày bên trái, kích cỡ" hoặc "Chiếc giày bên phải, kích cỡ" tùy thuộc vào tổng có lớn hơn 0 hay không.

### Quản lí tiền điện
Viết chương trình nhập vào 12 số nguyên dương tương ứng là tiền điện của 12 tháng trong năm vừa rồi của nhà em, đưa ra màn hình các thông tin sau:
* Tổng số tiền điện của cả năm và tiền điện trung bình theo tháng.
* Liệt kê các tháng có số tiền điện nhiều hơn tiền điện trung bình theo tháng.

## BÀI ĐỌC THÊM
### DANH SÁCH LỒNG NHAU VÀ DANH SÁCH RỖNG
Python cho phép mỗi phần tử của một danh sách cũng có thể là một danh sách.
Ví dụ: **Danhsach1 = ["Canh dieu", 10, [2018, 2021, 2022]]**
Phần tử cuối của Danhsach1 là một danh sách, đó là [2018, 2021, 2022].
Danh sách rỗng là danh sách không có phần tử nào và được mô tả là: **[]**
Ví dụ: **Danhsach2 = []**
Nếu thực hiện câu lệnh print (Danhsach2), ta sẽ không thấy trên màn hình hiển thị gì.
