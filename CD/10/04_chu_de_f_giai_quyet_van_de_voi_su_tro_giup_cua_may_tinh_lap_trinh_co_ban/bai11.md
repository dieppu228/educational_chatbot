# Bài 11: THỰC HÀNH LẬP TRÌNH VỚI HÀM VÀ THƯ VIỆN

Học xong bài này, em sẽ:
* Chạy và kiểm thử được chương trình.
* Rèn luyện được kĩ năng viết chương trình có khai báo và gọi hàm.
* Tìm hiểu và sử dụng được hàm time có trong thư viện.

## Luyện tập
Bài 1. Giải phương trình

Chương trình cho trong Hình 1 nhằm tạo một bảng chọn việc, để người chạy chương trình chọn cho máy tính giúp giải phương trình bậc nhất hay giải phương trình bậc hai. Em hãy đưa khai báo của các hàm thực hiện hai việc nói trên và các lời gọi chúng vào đúng chỗ trong chương trình. Sau đó hãy chạy thử chương trình với một số dữ liệu đầu vào khác nhau để kiểm thử chương trình.

*Mô tả mã nguồn:*
Đoạn mã này hiển thị một bảng chọn việc cho người dùng trong một vòng lặp vô hạn. Các tùy chọn bao gồm:
1. Giải phương trình bậc nhất.
2. Giải phương trình bậc hai.
3. Thoát khỏi công việc.
Người dùng được yêu cầu nhập lựa chọn của mình (1, 2, hoặc 3). Dựa trên lựa chọn, chương trình sẽ in ra thông báo tương ứng và bao gồm các chú thích để gọi hàm giải phương trình bậc nhất (**GPTB1**) hoặc giải phương trình bậc hai (**GPTB2**). Nếu người dùng chọn '3', chương trình sẽ in "Tạm biệt" và kết thúc.

Bài 2. Thời gian gặp nhau

Hiện tại, anh trai Khánh Nam đang ở thành phố A còn em gái Sương Mai đang ở thành phố B. Khoảng cách giữa hai thành phố đó là d km. Hai anh em đi ô tô xuất phát cùng một thời điểm từ hai thành phố, ô tô khởi hành từ A đi về B với tốc độ không đổi v1 km/h, ô tô khởi hành từ B đi đến A với tốc độ không đổi v2 km/h; trong đó d, v1, v2 là các số thực. Chương trình ở Hình 2 khai báo hàm mtime với các tham số d, v1, v2 để xác định thời gian hai ô tô gặp nhau tính từ lúc xuất phát. Em hãy:
a) Hoàn thiện chương trình ở Hình 2 bằng cách bổ sung cho chương trình lời gọi hàm mtime với dữ liệu nhập từ bàn phím.
b) Chạy chương trình và chạy thử chương trình với ít nhất hai bộ dữ liệu vào khác nhau.

**Hướng dẫn:** Viết hàm **mtime** với tham số **d**, **v1**, **v2** và trả về thời gian gặp nhau d/(v1+v2).

### a) Chương trình
Ví dụ một chương trình cho bài toán thời gian gặp nhau
### b) Kết quả thực hiện
Kết quả thực hiện của chương trình trên với các giá trị đầu vào d=300, v1=70, v2=80, cho ra thời gian 2 xe gặp nhau là 2.0 giờ.

Bài 3. Thời gian thực hiện chương trình

Hàm **time** (với lời gọi time ( ) ) trong thư viện **time** cho biết thời gian tại thời điểm hiện tại (tính theo giây). Để biết thời gian thực hiện chương trình, người ta ghi nhận thời điểm lúc bắt đầu thực hiện chương trình, thời điểm lúc kết thúc chương trình và đưa ra hiệu các thời điểm đã xác định. Em hãy gắn hàm time từ thư viện time vào một số chương trình đã có của em và đưa ra thời gian thực hiện chương trình.
Hướng dẫn:
*   Gắn thư viện time vào chương trình: `import time`
*   Để ghi nhận thời điểm bắt đầu viết câu lệnh đầu tiên là: `tb = time.time()`
*   Cuối chương trình, đưa ra thời gian thực hiện: `time.time() - tb`
*   Để cho đẹp: Nên dùng quy cách `%.4f` để đưa ra ra thời gian thực hiện chương trình với bốn chữ số ở phần thập phân.

Đoạn mã Python này sử dụng thư viện `time` để đo thời gian thực hiện một chương trình. Chương trình nhập các số nguyên dương từ người dùng cho đến khi nhập số 0 hoặc số âm, sau đó tính và in ra trung bình cộng của các số dương đã nhập và thời gian thực hiện chương trình với độ chính xác 4 chữ số thập phân.
Kết quả thực hiện của chương trình trên với các giá trị đầu vào 5, 6, 4, 0. Chương trình in ra trung bình cộng là 5.0 và thời gian thực hiện là 9.9937 giây.

#### Minh hoạ cách sử dụng hàm time

Viết chương trình vẽ một hình chữ nhật bằng các dấu # với một cạnh có độ dài bằng 10, một cạnh có độ dài bằng a. Ví dụ với a = 4, hình chữ nhật cần vẽ như hình bên:
Yêu cầu xây dựng một hàm Drawbox với tham số (a), hàm này đưa ra màn hình các dòng, mỗi dòng chứa 10 dấu # liên tiếp và tham số a quyết định số dòng sẽ được đưa ra. Chương trình gọi hàm Drawbox(a) với a nhập vào từ bàn phím.
