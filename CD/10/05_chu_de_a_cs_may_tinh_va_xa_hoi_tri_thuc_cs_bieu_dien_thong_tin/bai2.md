# Bài 2: Hệ nhị phân và ứng dụng

## a) Hệ nhị phân

### Cơ số trong một hệ đếm

Số tự nhiên quen thuộc là cách biểu diễn số trong hệ thập phân (hệ đếm cơ số 10). Một dãy kí số biểu diễn một giá trị số lượng. Quy ước từ phải sang trái là cột hàng đơn vị, cột hàng chục, cột hàng trăm, cột hàng nghìn,... Cứ dịch thêm một vị trí cột, từ phải sang trái, thì giá trị của kí số được tăng thêm 10 lần, 10 là cơ số của hệ đếm thập phân.

Số nhị phân là cách biểu diễn số trong hệ nhị phân (hệ đếm cơ số 2). Hệ nhị phân quy ước từ phải sang trái, cứ dịch thêm một vị trí cột thì giá trị của kí số được tăng thêm 2 lần. Hệ nhị phân chỉ dùng hai kí số 0 và 1. Mỗi số nhị phân đều là một dãy bit.

Hệ nhị phân (**hệ đếm cơ số 2**): chỉ dùng hai kí số 0 và 1, giá trị của kí số tăng gấp 2 lần khi dịch sang trái một vị trí cột.

Ví dụ minh họa: Chuyển đổi biểu diễn số ở hệ nhị phân sang hệ thập phân.

101101 (cơ số 2) → 1 × 2⁵ + 0 × 2⁴ + 1 × 2³ + 1 × 2² + 0 × 2¹ + 1 × 2⁰ = 45 (cơ số 10).

## b) Chuyển đổi một số nguyên dương ở hệ thập phân sang hệ nhị phân

Dãy bit 1101 biểu diễn số nào ở hệ thập phân? Em hãy quan sát hình sau và nêu nhận xét.

**Chuyển đổi 13 (hệ thập phân) sang hệ nhị phân:**

*   13 chia 2, được 6 dư 1
*   6 chia 2, được 3 dư 0
*   3 chia 2, được 1 dư 1
*   1 chia 2, được 0 dư 1

Vậy 13 (cơ số 10) = 1101 (cơ số 2).

**Kiểm tra lại 1101 (hệ nhị phân) sang hệ thập phân:**

*   1 × 2⁰ = 1
*   0 × 2¹ = 0
*   1 × 2² = 4
*   1 × 2³ = 8
*   Tổng = 13

Chú ý:
*   Khi phần nguyên của kết quả là 0 thì kết thúc. Dãy các kí số 0 và 1 ghi lại phần dư các phép chia sẽ tạo thành số nhị phân cần tìm.
*   Để chuyển số nguyên dương n bất kì ở hệ thập phân sang hệ nhị phân, ta làm tương tự.

## c) Phép cộng và phép nhân hai số nguyên trong hệ nhị phân

Các phép toán số học với các số trong hệ nhị phân được thực hiện theo quy tắc (thuật toán) tương tự như trong hệ thập phân.

### Phép cộng

Phép cộng hai số trong hệ nhị phân thực hiện với hai dãy bit (biểu diễn hai toán hạng) theo quy tắc như cộng hai số trong hệ thập phân và “viết 0, ghi nhớ 1, nếu có” trước khi cộng tiếp cho cột kế bên trái. Bảng cộng cơ sở giống với phép toán XOR, nhưng trường hợp cả hai toán hạng đều bằng 1 thì kết quả là “viết 0 nhớ 1”.

#### Ví dụ minh họa

Bảng cộng cơ sở giống với phép toán XOR, nhưng trường hợp cả hai toán hạng đều bằng 1 thì kết quả là “viết 0 nhớ 1”.

### Phép nhân

Phép nhân hai số trong hệ nhị phân thực hiện với hai dãy bit biểu diễn hai toán hạng và theo quy tắc tương tự như trong hệ thập phân.

Bảng nhân cơ sở giống với phép toán AND.

Ví dụ sau đây minh họa từng bước làm phép tính nhân x = 100101 với y = 101:

*   Bước 1: x = 100101, y = 101
*   Bước 2: Tính tích riêng thứ nhất bằng cách nhân 1 (bit cuối của y) với x, cho ra 100101.
*   Bước 3: Tính tích riêng thứ hai bằng cách nhân 0 (bit giữa của y) với x, cho ra 000000, dịch trái một vị trí.
*   Bước 4: Tính tích riêng thứ ba bằng cách nhân 1 (bit đầu của y) với x, cho ra 100101, dịch trái hai vị trí.
*   Bước 5: Cộng các tích riêng (100101, 0000000, 10010100) theo cột dọc, cho kết quả x * y = 10111001.

## d) Vai trò của hệ nhị phân trong tin học

Hệ nhị phân chỉ dùng hai kí số là 0 và 1. Các số trong hệ nhị phân đều biểu diễn được bằng dãy bit. Ban đầu, máy tính điện tử ra đời là để tính toán số học với tốc độ rất nhanh. Máy tính biểu diễn các số trong hệ nhị phân, thực hiện các phép tính số học nhị phân dựa trên cơ sở các phép toán bit và các quy tắc tương tự như của hệ thập phân.

Nhờ có **hệ nhị phân** mà **máy tính** có thể **tính toán**, **xử lí thông tin định lượng**, tương tự như con người dùng **hệ thập phân**.

Việc dễ dàng thể hiện một **dãy bit** về mặt vật lí là làm nên sức mạnh của **hệ nhị phân**. Cách thể hiện **bit** bởi hai **mức điện áp** khác nhau trong các **mạch điện tử** bằng các **cổng logic** cho phép thực hiện tính toán rất nhanh và thuận tiện. Có thể thể hiện **dãy bit** bằng cách phân biệt giữa điểm bằng phẳng với điểm lồi lên hay lõm xuống như trong **đĩa CD**. Thể hiện **dãy bit** nhờ phân biệt hai cực của **nam châm** như trong **băng từ**,...

**Hệ nhị phân** đặt cơ sở cho sự ra đời của **máy tính điện tử**, là cơ sở của các **thiết bị xử lí thông tin kĩ thuật số**.

## Luyện tập
Bài 1. Số 11111111 trong hệ nhị phân có giá trị là bao nhiêu trong hệ thập phân?

Bài 2. Chuyển hai số sau sang hệ nhị phân rồi thực hiện phép toán cộng (hoặc nhân) số nhị phân, kiểm tra lại kết quả qua số trong hệ thập phân.
1) 125 + 12
2) 125 × 6

Một máy tính kết nối với Internet phải được gán một **địa chỉ IP** (viết tắt của Internet Protocol). Địa chỉ **IP** là một số nhị phân dài 32 bit (tức là 4 byte) còn gọi là **IPv4** để phân biệt với **IPv6** dài 6 byte. Để cho con người dễ đọc, người ta viết địa chỉ **IP** dưới dạng 4 số trong hệ thập phân, cách nhau bởi dấu chấm, mỗi số trong hệ thập phân ứng với 1 byte. Các dãy sau đây có thể là địa chỉ **IP** không? Tại sao?
(Gợi ý: Số nhị phân dài 1 byte biểu diễn được các giá trị trong khoảng nào?)
1) 345.123.011.201
2) 123.110.256.101

Câu 1. Trong hệ nhị phân khi nào thì phép toán AND có kết quả là 1? Khi nào thì phép toán OR có kết quả là 0?
Câu 2. Điểm khác nhau giữa hai phép toán OR và XOR là gì?
Câu 3. Tại sao phép toán NOT cũng được gọi là phép bù?

## Tóm tắt bài học
*   Các tên gọi **phép toán bit NOT, AND, OR và XOR** nói lên kết quả thực hiện phép toán.
*   **Hệ nhị phân** biểu diễn các số bằng dãy bit và tính toán bằng các **phép toán bit**.
*   **Hệ nhị phân** là cơ sở để máy tính thực hiện tính toán.

# Bài 2: THỰC HÀNH VỀ CÁC PHÉP TOÁN BIT VÀ HỆ NHỊ PHÂN

Học xong bài này, em sẽ:
*   Thực hiện được các phép toán bit NOT, AND, OR và XOR theo từng bit và cho dãy bit.
*   Thực hiện được các phép toán cộng và nhân hai số nhị phân.
*   Viết được số bù 1, số bù 2 của một số nguyên nhị phân và biết được số bù 2 là số đối của số nguyên nhị phân.

## Luyện tập
Bài 1. Chuyển đổi biểu diễn số ở hệ thập phân sang hệ nhị phân

Chuyển số 44 ở hệ thập phân thành số ở hệ nhị phân bằng cách thực hiện theo hướng dẫn từng bước trong bảng sau:

*   Bước 1: Chuyển số 4 sang dạng nhị phân. Gợi ý: 4 = 2²
*   Bước 2: Chuyển số 8 sang dạng nhị phân. Gợi ý: 8 = 2³
*   Bước 3: Chuyển số 32 sang dạng nhị phân. Gợi ý: 32 = 2⁵
*   Bước 4: Cộng ba số cùng cột ở trên trong hệ nhị phân.

Bài 2. Cộng và nhân hai số nhị phân

Thực hiện phép cộng và phép nhân hai số nhị phân
Tạo bảng (ít nhất 3 hàng) theo mẫu bên:
x
y
x + y
x * y

Ghi chú: Ở cột 2, hàng 1, hàng 2 là các số nhị phân tuỳ chọn, tương ứng với x và y mỗi số có độ dài không ít hơn 3 bit.

Trong bảng em vừa tạo ra, hãy tính và điền kết quả vào hàng 3 và hàng 4 kết quả tương ứng với phép cộng và phép nhân.

Bài 3. Tính số bù của một số nhị phân

a) Cho số nhị phân x. Kết quả của phép toán NOT x kí hiệu là x̄. Ta gọi x̄ là **số bù 1** của x. Em hãy viết số bù 1 của số 44 ở hệ nhị phân.
b) Cho số nhị phân x. Kết quả của phép toán x̄ + 1 gọi là **số bù 2** của x. Em hãy viết số bù 2 của số 44 ở hệ nhị phân.

# Bài 4: Khám phá ý nghĩa của số bù của một số nhị phân

Em hãy thực hiện phép cộng số nhị phân x có giá trị thập phân là 44 với số bù 2 của x và cho biết kết quả nếu quy ước độ dài dãy bit biểu diễn số nguyên trong máy là 1 byte.

*Chú ý:* Với quy ước độ dài dãy bit biểu diễn số nguyên cố định trước, kết quả phép cộng x với số bù 2 của x luôn bằng 0. Số bù 2 của x cũng là số đối của x. Trong máy tính, để biểu diễn số nguyên âm, người ta không viết thêm dấu trừ mà dùng cách chuyển số nguyên nhị phân thành số bù 2.

Một bài kiểm tra môn Tin học gồm 10 câu hỏi trắc nghiệm đúng – sai. Đáp án được biểu diễn bằng dãy 10 bit, kí hiệu là *DapAn*. Trả lời của thí sinh được biểu diễn bằng dãy 10 bit, kí hiệu là *TraLoi*.

* Em hãy dùng phép toán bit để tạo ra *KetQua* là dãy 10 bit, biểu diễn kết quả chấm từng câu hỏi, đúng là 1, sai là 0.
* Em hãy tính điểm cho thí sinh theo thang điểm 10.

## BÀI TÌM HIỂU THÊM

### HỆ ĐẾM CƠ SỐ 8 VÀ HỆ ĐẾM CƠ SỐ 16

Một dãy dài nhiều kí số 0 và 1 tiện cho máy tính nhưng sẽ rất khó đọc với con người. Trong tin học, người ta còn định nghĩa hai hệ đếm khác là hệ đếm cơ số 8 và hệ đếm cơ số 16.

* Hệ đếm cơ số 8 hay **hệ bát phân** quy ước từ phải sang trái, cứ dịch thêm một vị trí sang trái thì giá trị của kí số được tăng thêm 8 lần. Để viết một số hệ bát phân ta dùng tám kí số 0, 1, 2, 3, 4, 5, 6, 7.

Ví dụ minh họa:
16 453 (cơ số 8) → 1 × 8⁴ + 6 × 8³ + 4 × 8² + 5 × 8¹ + 3 × 8⁰ = 7 467 (cơ số 10).

* Hệ đếm cơ số 16 hay **hệ thập lục phân** quy ước từ phải sang trái, cứ dịch thêm một vị trí sang trái thì giá trị của kí số được tăng thêm 16 lần. Để viết một số hệ thập lục phân, sẽ cần 16 kí hiệu khác nhau. Ta mới có 10 kí số quen thuộc trong hệ thập phân. Người ta dùng thêm các chữ cái và quy ước giá trị của chúng trong hệ thập phân như sau: A → 10, B → 11, C → 12, D → 13, E → 14, F → 15.

Ví dụ minh họa:
1D2B (cơ số 16) → 1 × 16³ + 13 × 16² + 2 × 16¹ + 11 × 16⁰ = 7 467 (cơ số 10).
