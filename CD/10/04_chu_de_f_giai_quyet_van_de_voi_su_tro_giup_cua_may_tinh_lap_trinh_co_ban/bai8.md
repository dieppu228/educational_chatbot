# Bài 8: CÂU LỆNH LẶP

Học xong bài này, em sẽ:
*   Biết được có hai loại cấu trúc lặp để mô tả thuật toán: lặp với số lần biết trước và lặp với số lần không biết trước.
*   Viết được câu lệnh lặp dạng `for` và dạng `while` trong Python.

Nếu em kiểm tra tuần tự từng dòng trong bảng điểm thi môn Tin học của lớp để biết tên các bạn đã được điểm 10 thì hành động nào được lặp lại và số lần lặp là bao nhiêu? Nếu chỉ cần tìm được tên của một bạn được điểm 10 thì số lần lặp là bao nhiêu?

## 1. Cấu trúc lặp trong mô tả thuật toán

Em đã biết, khi có một (hay nhiều) thao tác cần được thực hiện lặp lại một số lần liên tiếp trong quá trình thực hiện thuật toán thì cần dùng **cấu trúc lặp**. Có những thuật toán ta biết trước được số lần lặp của những thao tác cần lặp lại. Nhưng cũng có những thuật toán ta không biết trước được số lần lặp mà chỉ đến khi thực hiện thuật toán với những dữ liệu đầu vào cụ thể mới biết được.
*   **Ví dụ 1.** Thuật toán của việc in ra màn hình máy tính 10 dòng “Xin chào Python” là thuật toán có cấu trúc lặp với số lần biết trước.
*   **Ví dụ 2.** Khi mô tả thuật toán cho máy tính hỏi và kiểm tra mật khẩu thì ta không tính trước được số lần máy tính yêu cầu nhập lại mật khẩu, bởi vì chừng nào mật khẩu nhập vào chưa đúng thì máy tính còn hỏi lại. Đây là thuật toán có cấu trúc lặp với số lần không biết trước.

Với hai mẫu mô tả cấu trúc lặp, em hãy mô tả hai thuật toán ở Ví dụ 1 và Ví dụ 2.

**Mẫu mô tả cấu trúc lặp có số lần biết trước**
*   **Lặp với đếm từ** số đếm đầu **đến** số đếm cuối:
    *   Câu lệnh hay nhóm câu lệnh
*   **Hết lặp**

**Mẫu mô tả cấu trúc lặp không biết trước số lần lặp**
*   **Lặp khi** điều kiện lặp được thoả mãn:
    *   Câu lệnh hay nhóm câu lệnh
*   **Hết lặp**

Các ngôn ngữ lập trình bậc cao đều cung cấp các câu lệnh để người lập trình mô tả được hai loại cấu trúc lặp nêu trên. Cũng như ở các mẫu mô tả cấu trúc lặp trong thuật toán, câu lệnh lặp với số lần lặp biết trước trong ngôn ngữ lập trình bậc cao cần dùng một biến để đếm số lần lặp. Trong khi đó ở câu lệnh lặp với số lần lặp không biết trước phải có biểu thức lôgic thể hiện điều kiện lặp.

## Câu lệnh lặp với số lần lặp biết trước trong Python
Trong Python, câu lệnh lặp với số lần lặp biết trước có dạng:
*   `for biến_chạy in range (m,n):`
    *   Biến phục vụ quản lí số lần lặp
    *   Khối lệnh cần lặp
    *   Danh sách giá trị lặp

Trong câu lệnh `for`, hàm **range(m,n)** dùng để khởi tạo dãy số nguyên từ m đến n-1 (với m < n). Trường hợp m = 0, hàm **range (m,n)** có thể viết gọn là **range (n)**.
Ví dụ 3 minh hoạ một câu lệnh `for` trong Python và kết quả thực hiện.
*   Chương trình Python sử dụng vòng lặp `for` để in chuỗi "Xin chao Python" 10 lần.
*   Kết quả thực hiện:
    ```
    Xin chao Python
    Xin chao Python
    Xin chao Python
    Xin chao Python
    Xin chao Python
    Xin chao Python
    Xin chao Python
    Xin chao Python
    Xin chao Python
    Xin chao Python
    >>>
    ```

Ví dụ 4. Viết chương trình nhập n từ bàn phím và tính tổng các số tự nhiên chia hết cho 3 nhỏ hơn n.
*   Chương trình Python nhận một số nguyên `n` từ người dùng, sau đó tính tổng các số tự nhiên nhỏ hơn `n` và chia hết cho 3.
*   Ví dụ: Nếu `n` là 10, các số tự nhiên nhỏ hơn 10 chia hết cho 3 là 3, 6, 9. Tổng của chúng là 18.

## Câu lệnh lặp với số lần lặp không biết trước trong Python

Trong Python, câu lệnh lặp với số lần lặp không biết trước có dạng:
```
while <điều kiện>:
    Câu lệnh hay nhóm câu lệnh
```

Ví dụ 5. Các phần mềm ứng dụng mang tính cá nhân thường dùng mật khẩu để xác nhận quyền sử dụng. Chương trình yêu cầu người dùng nhập mật khẩu. Người dùng sẽ được yêu cầu nhập lại cho đến khi nhập đúng mật khẩu (là HN123). Khi dữ liệu nhập vào đúng là “HN123” thì thông điệp “Bạn đã nhập đúng mật khẩu” xuất hiện trên màn hình.

Mô tả mã nguồn:
Đoạn mã này yêu cầu người dùng nhập mật khẩu. Nó sẽ tiếp tục hỏi nhập mật khẩu trong một vòng lặp `while` chừng nào mật khẩu nhập vào chưa phải là "HN123". Khi mật khẩu đúng được nhập, vòng lặp kết thúc và in ra thông báo "Bạn đã nhập đúng mật khẩu".

Ví dụ 6. Chương trình khi thực hiện sẽ in ra màn hình các số từ 1 đến 6. Điều kiện lặp là `sodem <= 6`. Khi điều kiện lặp đúng thì `sodem` được in ra màn hình và được tăng lên 1 đơn vị, rồi điều kiện lặp được kiểm tra lại. Quá trình trên được lặp lại cho đến khi `sodem > 6` thì vòng lặp kết thúc.

Mô tả mã nguồn:
Đoạn mã này khởi tạo biến `sodem` bằng 1. Nó sử dụng một vòng lặp `while` để kiểm tra nếu `sodem` nhỏ hơn hoặc bằng 6. Trong mỗi lần lặp, giá trị của `sodem` được in ra, sau đó `sodem` được tăng lên 1.
Kết quả đầu ra của đoạn mã này sẽ là các số 1, 2, 3, 4, 5, 6, mỗi số trên một dòng.

Trong chương trình ở Ví dụ 6, em có thể dùng câu lệnh `for` thay cho câu lệnh `while` để chương trình khi chạy vẫn cho cùng kết quả được không?

Để thuận lợi cho việc lập trình, các ngôn ngữ lập trình bậc cao thường cung cấp cả hai câu lệnh lặp **for** và **while** tương ứng thể hiện lặp với số lần biết trước và lặp với số lần không biết trước. Tuy nhiên, dùng câu lệnh **while** ta cũng thể hiện được cấu trúc lặp với số lần biết trước.

## Luyện tập
Bài 1. Em hãy dự đoán chương trình thực hiện vòng lặp `for` để in ra giá trị của biến đếm và tổng của biến đếm với chính nó, với biến đếm chạy từ 1 đến 10.

Bài 2. Trong các chương trình trò chơi truyền hình, người dẫn chương trình thường đếm ngược để bắt đầu trò chơi. Em hãy viết chương trình nhập một số nguyên n, sau đó in ra các giá trị từ n về 1 để mô phỏng quá trình đếm ngược.

Mẹ em dự định gửi tiết kiệm một khoản tiền tại một ngân hàng có lãi suất 5% một năm, nghĩa là sau mỗi năm tiền lãi nhận được là 5% số tiền gửi. Hết một năm, nếu mẹ không rút tiền thì cả vốn lẫn lãi sẽ tự động được gửi tính cho năm tiếp theo. Em hãy viết chương trình nhập vào số tiền T (đơn vị triệu đồng) sau đó tính và đưa ra 10 dòng, mỗi dòng ghi số tiền sau mỗi năm trong 10 năm gửi liên tiếp cả gốc lẫn lãi để mẹ tham khảo.

Trong các câu sau đây, những câu nào đúng?
*   1) Trong các ngôn ngữ lập trình bậc cao đều có câu lệnh thể hiện cấu trúc lặp.
*   2) Trong Python chỉ có câu lệnh lặp **while** để thể hiện cấu trúc lặp.
*   3) Trong Python chỉ có câu lệnh lặp **for** để thể hiện cấu trúc lặp.
*   4) Có thể sử dụng câu lệnh **while** để thể hiện cấu trúc lặp với số lần lặp biết trước.
*   5) Có thể sử dụng câu lệnh **for** để thể hiện cấu trúc lặp với số lần lặp chưa biết trước.

## Tóm tắt bài học

*   Các ngôn ngữ lập trình bậc cao đều có câu lệnh thể hiện cấu trúc lặp của thuật toán.
*   Câu lệnh thể hiện lặp với số lần biết trước cần phải sử dụng một biến để kiểm soát được số lần lặp.
*   Câu lệnh thể hiện lặp với số lần không biết trước phải sử dụng một biểu thức logic làm điều kiện lặp.
*   Câu lệnh lặp trong Python có hai dạng cơ bản là:
    `for biến_chạy in danh_sách_giá_trị:`
    `Câu lệnh hay nhóm câu lệnh`

    `while <điều kiện>:`
    `Câu lệnh hay nhóm câu lệnh`
