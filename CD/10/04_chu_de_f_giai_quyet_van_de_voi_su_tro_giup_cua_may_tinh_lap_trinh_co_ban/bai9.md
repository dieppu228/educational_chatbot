# Bài 9: THỰC HÀNH CÂU LỆNH LẶP

Học xong bài này, em sẽ:
*   Viết được chương trình đơn giản có sử dụng câu lệnh lặp.
*   Viết được chương trình đơn giản có sử dụng câu lệnh rẽ nhánh kết hợp với câu lệnh lặp.

## Bài 1. Làm quen với câu lệnh lặp trong Python
Em hãy dự đoán xem chương trình ở Hình 1 sau đây sẽ đưa ra màn hình những gì. Chạy chương trình để kiểm tra kết quả.
Mô tả chương trình ở Hình 1: Đoạn mã Python này khởi tạo `total` bằng 0. Sau đó, nó sử dụng một vòng lặp `for` để lặp qua các số nguyên từ 1 đến 100 (không bao gồm 101). Trong mỗi lần lặp, nó cộng giá trị của biến lặp `i` vào `total` và in ra giá trị hiện tại của `i` cùng với `total`.

## Bài 2. Đếm các ước thực sự của một số nguyên
Bạn Hà viết chương trình ở Hình 2 để đếm xem số nguyên n nhập vào từ bàn phím có bao nhiêu ước số thực sự (ước khác 1 và n). Tuy nhiên, chương trình chạy ra kết quả sai. Em hãy sửa lỗi giúp bạn Hà.
Mô tả chương trình ở Hình 2: Đoạn mã Python này yêu cầu người dùng nhập một số nguyên `n`. Nó khởi tạo biến `i` bằng 2 và `so_uoc` bằng 0. Vòng lặp `while` tiếp tục chừng nào `i` còn nhỏ hơn hoặc bằng `n/2`. Trong vòng lặp, nếu `n` chia hết cho `i` (tức là `i` là một ước của `n`), thì `so_uoc` được tăng lên 1. Sau đó, `i` được tăng lên 1. Cuối cùng, nó in ra `n` và số lượng ước thực sự tìm được (`so_uoc`).

## Bài 3. Nhập dữ liệu có kiểm tra
Tham khảo chương trình ở Ví dụ 5 trong Bài 8, em hãy viết chương trình yêu cầu người dùng nhập một số nguyên lớn hơn 1 000 000. Chừng nào người dùng nhập chưa đúng yêu cầu thì có thông báo yêu cầu nhập lại, chương trình chỉ kết thúc với thông báo “Cảm ơn, bạn đã nhập dữ liệu đúng yêu cầu.” khi số người dùng gõ vào thoả điều kiện đặt ra.

Em hãy lập trình giải bài toán cổ ở hình bên một cách tổng quát bằng cách nhập hai số nguyên dương n, m tương ứng là tổng số con và tổng số chân sau đó đưa ra màn hình số lượng gà và số lượng chó. Kiểm thử chương trình với n = 36 và m = 100.

Vừa gà vừa chó
Bó lại cho tròn
Ba mươi sáu con
Một trăm chân chẵn
Hỏi có mấy con gà, mấy con chó?

BÀI TÌM HIỂU THÊM

# CÁC CÂU LỆNH BREAK VÀ CONTINUE

Trong Python câu lệnh **break** dùng để thoát ra khỏi vòng lặp ngay kể cả khi điều kiện lặp còn đúng. Bất cứ những lệnh nào trong vòng lặp đứng sau **break** đều bị bỏ qua. Câu lệnh **continue** trong Python được dùng để bỏ qua các câu lệnh còn lại chưa được thực hiện trong vòng lặp, chuyển đến vòng lặp tiếp theo.

## Ví dụ 1. Chương trình ở hình bên sử dụng **break** và **continue** trong câu lệnh **for** giải quyết bài toán sau:

Bài toán: Hãy viết chương trình nêu những câu hỏi để kiểm tra xem người ngồi trước máy tính có thuộc bảng nhân 6 hay không. Chương trình cho phép người trả lời bỏ qua một câu hỏi nào đó hoặc dừng kiểm tra.

Chương trình Python thực hiện một bài kiểm tra bảng nhân 6.
- Nó lặp qua các số từ 1 đến 10.
- Với mỗi số, nó in ra một câu hỏi (ví dụ: "6 x 1 = ?") và chờ người dùng nhập câu trả lời.
- Nếu người dùng nhập "dừng", câu lệnh **break** sẽ thoát khỏi vòng lặp, kết thúc bài kiểm tra.
- Nếu người dùng nhập "bỏ qua", câu lệnh **continue** sẽ bỏ qua phần còn lại của vòng lặp hiện tại và chuyển sang câu hỏi tiếp theo.
- Nếu người dùng nhập một số, chương trình sẽ kiểm tra xem câu trả lời có đúng hay không.
- Nếu đúng, in "Đúng!". Nếu sai, in "Sai! đáp án: " cùng với đáp án đúng.
- Cuối cùng, in "Kết thúc" sau khi vòng lặp kết thúc hoặc bị ngắt.

## Ví dụ 2. Chương trình ở hình sau đây sử dụng **break** và **continue** trong câu lệnh **while** để giải quyết bài toán sau:

Bài toán: Để thử nghiệm lâm sàng vacxin mới ở giai đoạn 1, người ta cần những người trong độ tuổi từ 18 đến 64 tuổi và thoả mãn điều kiện 18.5 <= cân nặng/(chiều cao)² <= 22.9. Theo tập hồ sơ nhận được từ những người tình nguyện, hãy đưa ra màn hình số người sẽ được xét để tham gia thử nghiệm. Số liệu về tuổi, cân nặng (kg) và chiều cao (m) của mỗi hồ sơ nhập vào từ bàn phím, mỗi số trên một dòng. Nhập tuổi bằng 0 để kết thúc tập hồ sơ.

Chương trình Python này đếm số người đủ điều kiện tham gia thử nghiệm lâm sàng vacxin.
- Nó bắt đầu với một biến đếm `p` bằng 0 và chạy trong một vòng lặp vô hạn (**while True**).
- Trong mỗi vòng lặp, nó yêu cầu người dùng nhập tuổi.
- Nếu tuổi nhập vào là 0, câu lệnh **break** sẽ thoát khỏi vòng lặp, kết thúc quá trình nhập liệu.
- Sau đó, chương trình yêu cầu nhập chiều cao (m) và cân nặng (kg).
- Nó kiểm tra hai điều kiện:
    *   Tuổi phải nằm trong khoảng từ 18 đến dưới 65 (18 <= tuổi < 65).
    *   Chỉ số BMI (cân nặng / (chiều cao)²) phải nằm ngoài khoảng từ 18.5 đến 22.9 (nghĩa là BMI < 18.5 hoặc BMI > 22.9).
- Nếu một trong hai điều kiện trên đúng (tức là người đó KHÔNG đủ điều kiện), câu lệnh **continue** sẽ bỏ qua phần còn lại của vòng lặp và chuyển sang người tiếp theo.
- Nếu người đó đủ điều kiện (tuổi trong khoảng và BMI trong khoảng), biến đếm `p` sẽ được tăng lên 1.
- Cuối cùng, sau khi vòng lặp kết thúc, chương trình in ra tổng số người được xét ("Số người được xét: ") cùng với giá trị của `p`.
