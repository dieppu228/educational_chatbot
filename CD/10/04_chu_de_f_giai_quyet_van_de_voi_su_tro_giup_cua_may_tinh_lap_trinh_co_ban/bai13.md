# Bài 13: THỰC HÀNH DỮ LIỆU KIỂU XÂU

**Học xong bài này, em sẽ:**
*   Tìm và xoá được kí tự trong xâu.
*   Tách được xâu con, thay thế được xâu con.
*   Đếm được số lần xuất hiện kí tự cho trước trong xâu.

## Luyện tập
Bài 1. Xoá kí tự trong xâu

a) Em hãy viết chương trình tạo một xâu mới từ xâu s đã cho bằng việc xoá những kí tự được chỉ định trước.
Hướng dẫn: Xoá kí tự tương đương với việc thay kí tự đó bằng kí tự rỗng.
b) Em hãy chạy thử chương trình và kiểm tra kết quả.

Ví dụ:

Chương trình này nhận vào một xâu `s` và một kí tự `c` từ người dùng. Sau đó, nó tạo một xâu mới `w` bằng cách thay thế tất cả các lần xuất hiện của kí tự `c` trong `s` bằng một xâu rỗng, tức là xoá kí tự `c`. Cuối cùng, nó in ra xâu `w`.
Nếu nhập xâu `s` là `123a45a6a78` và kí tự `c` là `a`, kết quả in ra sẽ là `12345678`.

# Bài 2. Giúp bạn tìm và sửa lỗi chương trình

Tên tệp thường gồm hai phần: phần tên và phần mở rộng được ngăn cách nhau bởi dấu chấm. Ví dụ, các tệp chương trình Python có phần mở rộng là “py”, các tệp văn bản có phần mở rộng là “doc” hoặc “docx”. Trong hệ điều hành Windows, tên tệp không phân biệt chữ hoa và chữ thường. Bạn Khánh Linh muốn viết chương trình nhập vào một xâu là tên của một tệp và kiểm tra xem tên tệp đó có phải là tên của tệp chương trình Python trong hệ điều hành Windows không.

Chương trình này yêu cầu người dùng nhập vào một tên tệp. Nó sau đó tính độ dài của tên tệp, và cố gắng lấy 20 kí tự cuối cùng của tên tệp để gán vào biến `extensionName`. Cuối cùng, nó kiểm tra xem `extensionName` có bằng "py" hay không để thông báo tên tệp đã nhập là tệp mã nguồn Python hay không.

Khánh Linh đã nghĩ ra thuật toán, bằng cách lấy ra hai kí tự cuối cùng của xâu rồi so sánh với xâu "py". Tuy nhiên, chương trình do Khánh Linh viết vẫn còn có lỗi. Em hãy giúp bạn Khánh Linh tìm và sửa lỗi để chương trình chạy được và đưa ra kết quả đúng.

*Gợi ý:* Nếu Python báo lỗi cú pháp, em hãy sửa hết lỗi cú pháp để chương trình chạy được. Sau đó hãy chạy thử với một số dữ liệu vào khác nhau, ví dụ "Hello.py", "introPython.doc", "Hello.PY" và kiểm tra xem kết quả nhận được có đúng không.

# Bài 3. Xác định toạ độ

### a) Tìm hiểu bài toán:
Robot thám hiểm Sao Hoả đang ở điểm có toạ độ (0; 0) nhận được dòng lệnh điều khiển từ Trái Đất. Dòng lệnh chỉ chứa các kí tự từ tập kí tự {E, S, W, N}, mỗi kí tự là một lệnh di chuyển với quãng đường bằng một đơn vị độ dài. Lệnh E – đi về hướng đông, lệnh S – đi về hướng nam, lệnh W – đi về hướng tây và lệnh N – đi về hướng bắc. Trục Ox của hệ toạ độ chạy từ tây sang đông, trục Oy – chạy từ nam lên bắc. Em hãy xác định toạ độ của robot sau khi thực hiện lệnh di chuyển nhận được.

**Ví dụ:** Với dòng lệnh "ENENWWWS", sau khi thực hiện robot sẽ tới vị trí (–1; 1).

*Gợi ý:* Toạ độ x của đích tới bằng số lượng kí tự 'E' trừ số lượng kí tự 'W'.
Toạ độ y của đích tới bằng số lượng kí tự 'N' trừ số lượng kí tự 'S'.

### b) Em hãy đọc hiểu và chạy thử chương trình sau và cho biết chương trình đó có giải quyết được bài toán ở mục a) hay không.

Chương trình tính toán toạ độ của robot:
Chương trình yêu cầu người dùng nhập một chuỗi các lệnh di chuyển. Sau đó, nó đếm số lần xuất hiện của các kí tự 'E', 'W', 'N', 'S' trong chuỗi lệnh. Cuối cùng, nó tính toán toạ độ x và y của robot dựa trên các số lượng này và in ra kết quả.

Kết quả thực hiện:
Dòng lệnh: ENENWWWS
Toạ độ hiện tại của robot: (-1, 1)

## Luyện tập

**Tên gọi chữ số bằng tiếng Anh**

Em hãy viết chương trình nhập vào từ bàn phím một chữ số trong hệ thập phân, đưa ra màn hình tên gọi của chữ số đó bằng tiếng Anh.

**Ví dụ:**
INPUT
5
OUTPUT
five
