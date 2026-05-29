# Bài 32: ÔN TẬP LẬP TRÌNH PYTHON

## SAU BÀI NÀY EM SẼ:

*   Thực hành ôn tập lập trình Python.
*   Thực hành lập trình giải bài toán có tính liên môn.

## Nhiệm vụ 1.

Viết chương trình nhập họ tên đầy đủ từ bàn phím, ví dụ "Nguyễn Thị Mai Hương", sau đó tách riêng phần tên, họ, đệm và in ra màn hình.

**Hướng dẫn.** Trong Bài 25 chúng ta sẽ biết cách tách phần họ đệm và tên từ một xâu họ và tên. Bài này yêu cầu thêm tách phần đệm, tức là phần nằm giữa tên và họ ra bằng cách sử dụng lệnh `join()`. Xâu kí tự ban đầu được tách thành một danh sách dùng hàm `split()`. Sau khi lấy phần họ và tên, phần đệm sẽ lấy ra theo lệnh sau:
Mô tả: Đoạn mã này tính phần đệm bằng cách nối các từ trong danh sách từ vị trí thứ 1 đến vị trí n-2 (tức là loại bỏ từ đầu tiên và từ cuối cùng).
Trong đó slist là danh sách được tách ra từ xâu ban đầu, n là độ dài của xâu slist.

Nhập, chạy thử và kiểm tra chương trình sau:
Mô tả: Chương trình này yêu cầu người dùng nhập họ tên đầy đủ. Sau đó, nó tách họ tên thành họ (từ đầu tiên), tên (từ cuối cùng) và đệm (các từ ở giữa). Cuối cùng, nó in ra tên, họ và đệm (nếu có).

## Nhiệm vụ 2. Trọng lượng của em trên các hành tinh khác.

Chương trình yêu cầu nhập trọng lượng của em (tính theo đơn vị **N – Newton**) trên Trái Đất và tính trọng lượng của em trên một hành tinh khác (ví dụ Mặt Trăng, Hoả tinh, Kim tinh, Thổ tinh, Mộc tinh, Mặt Trời).

**Hướng dẫn.** Trọng lượng đo lực hút của Trái Đất (hay hành tinh) lên vật thể. Trọng lượng có đơn vị đo **N (Newton)**. Khối lượng vật thể tính bằng kg và giá trị này không thay đổi. Chúng ta có công thức:
P = m x g (1)

Trong đó P là trọng lượng lượng tính bằng N, m là khối lượng tính bằng kg, g là gia tốc trọng trường của Trái Đất (hay hành tinh), tính theo m/s². Trên Trái Đất, g = 9.8 m/s². Trên mỗi hành tinh các giá trị g sẽ khác nhau. Danh sách các hành tinh được lưu trong biến planet, các trọng lực tương ứng lưu trong danh sách gravities.
Biết trọng lượng của một người trên Trái Đất (ví dụ P₀) thì sẽ dễ dàng tính được trọng lượng của người này trên một hành tinh khác nếu biết giá trị g của hành tinh đó. Gọi P là trọng lượng cần tìm, khi đó ta có công thức sau, suy trực tiếp từ công thức (1).
m = P₀/9.8 = P/g, vậy suy ra P = P₀× g/9.8. (2)
Em hãy nhập chương trình sau và kiểm tra tính đúng đắn của chương trình.

weight.py

Đoạn mã Python này định nghĩa một hàm để định dạng danh sách và sau đó thực hiện tính toán trọng lượng của một vật thể trên các hành tinh khác nhau.
- Nó định nghĩa một danh sách các hành tinh (`planet`) và danh sách các gia tốc trọng trường tương ứng (`gravities`).
- Chương trình yêu cầu người dùng nhập trọng lượng của họ trên Trái Đất (tính bằng N).
- Người dùng được yêu cầu nhập số thứ tự của hành tinh muốn tính trọng lượng.
- Dựa trên đầu vào, chương trình truy xuất gia tốc trọng trường của hành tinh đã chọn.
- Cuối cùng, nó tính toán và in ra trọng lượng của người dùng trên hành tinh đã chọn, làm tròn đến 3 chữ số thập phân.

## Nhiệm vụ 3. Kiểm tra tính hợp lệ của ba tham số ngày, tháng, năm.

Chương trình sẽ yêu cầu nhập ba số tự nhiên: ngày, tháng, năm từ bàn phím theo khuôn dạng, ví dụ nhập 08-02-2021. Chương trình sẽ thông báo bộ dữ liệu đã nhập là hợp lệ hay không hợp lệ.

### Hướng dẫn
Bộ dữ liệu chính cần nhập sẽ đặt tên là **day**, **month**, **year**. Nhiệm vụ của bài toán là nhập bộ dữ liệu này và kiểm tra tính hợp lệ theo các yêu cầu về lịch của ngày, tháng, năm.
Điểm đặc biệt nhất cần chú ý là kiểm tra năm **year** có phải là nhuận không, nếu là nhuận thì tháng 2 phải có 29 ngày so với các năm không nhuận tháng 2 có 28 ngày. Chúng ta sử dụng biến danh sách số **thang** để lưu số ngày của các tháng trong năm. Sau mỗi lần nhập ba số **day**, **month**, **year** cần kiểm tra năm nhuận để cập nhật tháng 2. Khi đó, chương trình kiểm tra có thể viết đơn giản như sau:

Đoạn mã Python `date.py` định nghĩa một hàm để kiểm tra năm nhuận và một chương trình chính để nhập ngày, tháng, năm từ người dùng. Chương trình phân tích dữ liệu nhập vào, sau đó kiểm tra tính hợp lệ của ngày dựa trên số ngày của từng tháng và có tính đến năm nhuận. Kết quả sẽ thông báo ngày nhập vào là hợp lệ hay không.

## LUYỆN TẬP
Viết chương trình nhập số n, sau đó nhập danh sách tên học sinh với họ, đệm, tên. Sắp xếp tên học sinh trong lớp theo bảng chữ cái. Đưa kết quả ra màn hình.

## VẬN DỤNG
1.  Trong các phần mềm bảng tính điện tử, dữ liệu ngày tháng được coi là số ngày tính từ ngày 1-1-1990. Viết chương trình:
    *   Nhập số tự nhiên n từ bàn phím và tính xem số đó ứng với ngày, tháng, năm nào.
    *   Nhập thời gian theo khuôn dạng ngày - tháng - năm (ví dụ 8-10-2021), tính số ngày ứng với ngày này theo phần mềm bảng tính điện tử.
2.  Mở rộng bài tập trong phần luyện tập như sau:
    *   Việc sắp xếp thứ tự phải ưu tiên tính theo tên trước, rồi đến họ, rồi đến đệm.
    *   Sắp xếp theo thứ tự của bảng chữ cái tiếng Việt.

    Chú ý: Bảng chữ cái tiếng Việt (bao gồm cả dấu thanh) được sắp xếp theo thứ tự sau: AÁÀẢÃẠĂẰẮẲẴẶÂẤẦẨẪẬBCDEÉÈẺẼẸÊẾỀỂỄỆFGHIJKLMNOÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢPQRSTUVWXYZƯỨỪỬỮỰVXYYYYY.
3.  Nếu n là hợp số thì dễ thấy n phải có ước số nguyên tố nhỏ hơn hoặc bằng **√n**. Viết chương trình tối ưu hoá hơn nhiệm vụ 1, bài 31, theo cách sau: để tìm ước số nguyên tố nhỏ nhất chỉ cần tìm trong các số 2, 3, ..., **√n**. Nếu trong dãy trên không tìm thấy ước của n thì kết luận ngay n là nguyên tố.
