# Bài 4: CÁC KIỂU DỮ LIỆU SỐ VÀ CÂU LỆNH VÀO – RA ĐƠN GIẢN

**Học xong bài này, em sẽ:**

*   Viết được câu lệnh đơn giản để nhập dữ liệu kiểu số nguyên, số thực trong Python.
*   Viết được câu lệnh đưa ra kết quả trong Python.
*   Nêu được ví dụ về hằng trong chương trình.

Khi yêu cầu máy tính giải quyết một bài toán, ta cần phải cung cấp dữ liệu vào cho máy tính và yêu cầu máy tính trả kết quả ra. Theo em, ngôn ngữ lập trình có cần các câu lệnh đưa dữ liệu vào và xuất dữ liệu ra không?

## 1. Kiểu dữ liệu số nguyên và số thực

Các ngôn ngữ lập trình bậc cao đều cho phép sử dụng các biến kiểu dữ liệu số nguyên và kiểu dữ liệu số thực. Trong Python khi một biến được gán bằng một biểu thức, tuỳ thuộc giá trị biểu thức đó là số nguyên hay số thực thì biến sẽ lưu trữ tương ứng là kiểu số nguyên hoặc là kiểu số thực.

Mô tả đoạn mã: Đoạn mã Python Shell thực hiện các phép gán và tính toán.
*   Biến `a` được gán giá trị `5`, là kiểu số nguyên.
*   Biến `b` được gán giá trị `5.0`, là kiểu số thực.
*   Biến `c` được gán giá trị `3.2`, cũng là kiểu số thực.
*   Khi in kết quả của phép chia `a/3`, output là `1.6666666666666667`, cho thấy phép chia trong Python luôn có kết quả là số thực, ngay cả khi chia số nguyên.

Câu lệnh **type()** của Python cho ta biết kiểu dữ liệu của biến hay biểu thức nằm trong cặp dấu ngoặc tròn.

Mô tả đoạn mã: Đoạn mã Python Shell minh họa cách sử dụng hàm `type()`.
*   Khi biến `a` được gán `5` (số nguyên), lệnh `print(type(a))` cho kết quả `<class 'int'>`.
*   Khi biến `a` được gán `5.0` (số thực), lệnh `print(type(a))` cho kết quả `<class 'float'>`.
*   Lệnh `print(type(5/3))` kiểm tra kiểu dữ liệu của biểu thức chia `5/3`, cho kết quả `<class 'float'>`, khẳng định rằng phép chia luôn trả về kiểu số thực.

Em hãy viết chương trình Python (hoặc làm việc với Python ở cửa sổ Shell), dùng câu lệnh type() để biết kiểu dữ liệu liên quan đến các phép toán: chia, chia lấy phần nguyên, chia lấy phần dư. Em có thể tham khảo dữ liệu ở Bảng 1 sau đây.

## Các câu lệnh vào – ra đơn giản

Khi thực hiện chương trình, dữ liệu sẽ được nhập vào từ bàn phím hoặc từ tệp ở thiết bị ngoài. Kết quả thực hiện phải được đưa ra màn hình hay ra tệp.

### a) Nhập dữ liệu từ bàn phím

Khi lập trình Scratch, em đã dùng câu lệnh nào trong chương trình để yêu cầu nhập dữ liệu từ bàn phím?

Với câu lệnh nhập dữ liệu ta có thể lập trình với các biến mà giá trị của nó chỉ có thể biết khi thực hiện chương trình (ở thời điểm giá trị đó được nhập vào từ bàn phím hoặc từ tệp).

Ví dụ, để tính tổng n số tự nhiên đầu tiên ta có câu lệnh:
*   Một đoạn mã tính tổng n số tự nhiên đầu tiên bằng công thức `sum = n * (n + 1) // 2`.

Câu lệnh này không thể thực hiện được nếu không biết giá trị cụ thể của n. Thay vì gán giá trị cho n trong chương trình ta có thể nhập giá trị từ bàn phím. Như vậy, ta có một chương trình cho phép tính sum với n bằng bao nhiêu cũng được mà không cần sửa chương trình.

Câu lệnh nhập giá trị cho một biến vào từ bàn phím có dạng:
*   Mô tả cú pháp câu lệnh nhập dữ liệu từ bàn phím, trong đó 'Biến' là tên biến sẽ lưu giá trị nhập vào, và 'dòng thông báo' là thông điệp hiển thị cho người dùng (ví dụ: `Biến = input (dòng thông báo)`).

Trong đó: **dòng thông báo** là để nhắc người dùng biết cần nhập gì, dòng thông báo là một xâu kí tự đặt giữa cặp dấu nháy đơn hoặc nháy kép, có thể không cần có.

Dữ liệu nhập vào có dạng xâu kí tự. Nếu muốn chuyển dữ liệu này sang kiểu số nguyên hay số thực để tính toán cần có câu lệnh **int()** hay **float()** như sau:

*   Để chuyển đổi dữ liệu nhập vào thành kiểu số nguyên và gán cho biến:
    `Biến = int (input (dòng thông báo))`
    (Với biến kiểu nguyên)
*   Để chuyển đổi dữ liệu nhập vào thành kiểu số thực và gán cho biến:
    `Biến = float (input (dòng thông báo))`
    (Với biến kiểu thực)

**Ví dụ 1**. Chương trình thực hiện tính tổng n số tự nhiên đầu tiên với giá trị n nhập vào từ bàn phím.

*   Mô tả đoạn mã nguồn:
    Đoạn mã này yêu cầu người dùng nhập một số nguyên `n` thông qua hàm `input()`, sau đó chuyển đổi giá trị nhập vào thành số nguyên bằng `int()`. Tiếp theo, nó tính tổng các số tự nhiên từ 1 đến `n` bằng công thức `n * (n + 1) // 2` và gán kết quả cho biến `sum`.
    *   **input()**: nhập dữ liệu vào
    *   **int()**: chuyển kiểu dữ liệu vừa nhập vào thành kiểu số nguyên

### b) Xuất dữ liệu ra màn hình

Ở cửa sổ Shell, nếu viết dòng lệnh chỉ chứa tên biến hoặc biểu thức số học thì kết quả tương ứng sẽ được đưa ra màn hình.

Ở cửa sổ Code để đưa thông tin ra và lưu lại trên màn hình cần dùng câu lệnh **print()**.
Dạng đơn giản của câu lệnh print () đưa giá trị các biểu thức ra màn hình là:

*   Cú pháp: `print (danh sách biểu thức)`

Trong đó **danh sách biểu thức** là các biểu thức viết cách nhau bởi dấu “,”.
Câu lệnh print () sẽ in ra màn hình giá trị các biểu thức theo đúng thứ tự và cách nhau bởi dấu cách.

**Ví dụ 2**. Viết chương trình nhập ba số thực là điểm kiểm tra cuối học kì của ba môn Ngữ văn, Vật lí và Sinh học. Tính và đưa ra màn hình tổng điểm và điểm trung bình của ba môn.

*   Mô tả đoạn mã nguồn:
    Đoạn mã này yêu cầu người dùng nhập ba điểm số (Ngữ văn, Vật lí, Sinh học) dưới dạng số thực bằng cách sử dụng `input()` và `float()`. Sau đó, nó tính tổng ba điểm và gán cho biến `t`. Cuối cùng, chương trình in ra màn hình tổng điểm và điểm trung bình của ba môn.

*   Kết quả thực hiện chương trình với số liệu cụ thể:
    ```
    Điểm Ngữ văn: 7.5
    Điểm Vật lí: 10
    Điểm Sinh học: 9.5
    Tổng ba môn: 27.0 trung bình: 9.0
    >>>
    ```

## Hằng trong Python

**Hằng** là những biến có giá trị chỉ định trước và không thể thay đổi trong quá trình thực hiện chương trình. Khác với nhiều ngôn ngữ lập trình khác, Python không cung cấp công cụ khai báo hằng. Khi lập trình bằng Python, người ta thường sử dụng hằng số như một loại biến với cách đặt tên đặc biệt, ví dụ bắt đầu bằng dấu gạch dưới và sau đó là các kí tự La tinh in hoa, gán giá trị cần thiết cho nó và tự quy ước không gán lại giá trị cho các biến đó.

Ví dụ:
*   Biến `_PI` được dùng như một hằng số có giá trị là 3.1416.
*   Biến `_MOD` được dùng như một hằng số có giá trị là 1000000007 (tức 10^9 + 7).

Nếu hai dòng nêu trên ở trong chương trình chính thì hai biến đó được coi là hằng ở trong chương trình con.

## Luyện tập
**Bài 1. Tam giác vuông**

Viết chương trình thực hiện nhập từ bàn phím hai số nguyên dương b, c là độ dài hai cạnh góc vuông của tam giác vuông ABC, tính và đưa ra màn hình:
*   Diện tích tam giác.
*   Độ dài cạnh huyền.

Có thể đưa ra dòng thông báo tuỳ chọn (bằng tiếng Việt có dấu) trước mỗi dữ liệu nhập vào và trước mỗi kết quả xuất ra.

Ví dụ:
Với dữ liệu nhập:
*   b = 3
*   c = 4
Kết quả xuất ra:
*   Diện tích tam giác: 6.0
*   Độ dài cạnh huyền: 5.0

**Bài 2. Chia mận**

Cô giáo đi du lịch ở Sa Pa mang về túi mận làm quà cho cả lớp. Túi mận có k quả, lớp có n học sinh. Mận được chia đều để em nào cũng nhận được một số lượng quả như nhau. Nếu còn thừa, những quả còn lại sẽ được dành cho các em nữ.
Viết chương trình: nhập n và k vào từ bàn phím, đưa ra màn hình số quả mận mỗi học sinh nhận được và số quả dành riêng cho các em nữ. Sử dụng dòng thông báo cho dữ liệu nhập vào và mỗi kết quả đưa ra.

Ví dụ:
Với dữ liệu nhập:
*   số học sinh: n = 31
*   số mận: k = 123
Kết quả xuất ra:
*   Mỗi học sinh được chia 3 quả mận.
*   Số mận dành riêng cho các em nữ là 30.

# Tính số bàn học

Trường mới đẹp và rộng hơn trường cũ, số phòng học cũng nhiều hơn so với trước. Nhà trường dự định tuyển thêm học sinh cho ba lớp mới với số lượng học sinh mỗi lớp tương ứng là a, b và c. Cần mua bàn cho các lớp mới này. Mỗi bàn học có không quá hai chỗ ngồi cho học sinh. Xác định số lượng bàn tối thiểu cần mua. Em hãy viết chương trình giải quyết bài toán trên. Dữ liệu được nhập vào từ bàn phím. Kết quả được đưa ra màn hình.

Ví dụ:
INPUT
a = 35
b = 42
c = 39

OUTPUT
Số bàn tối thiểu cần mua: 59

## Luyện tập
Trong các câu sau đây, những câu nào đúng?
1) Để tính toán, các ngôn ngữ lập trình bậc cao không phân biệt kiểu dữ liệu số nguyên và kiểu dữ liệu số thực.
2) Trong Python, câu lệnh **n = int(input('n = '))** cho nhập vào một số thực từ bàn phím.
3) Trong Python mỗi câu lệnh **print()** chỉ đưa ra được giá trị của một biến.
4) Trong Python, với câu lệnh **input()** có thể nhập dữ liệu cùng với thông báo hướng dẫn.

## Tóm tắt bài học

*   Trong các ngôn ngữ lập trình bậc cao có **kiểu dữ liệu số nguyên** và **kiểu dữ liệu số thực**.
*   Trong Python:
    *   Câu lệnh **type(biến)** cho biết kiểu dữ liệu hiện thời của biến.
    *   Câu lệnh nhập dữ liệu cho biến là:
        *   **Biến = input(dòng thông báo)**
        *   **Biến = int(input(dòng thông báo))** (với biến kiểu nguyên)
        *   **Biến = float(input(dòng thông báo))** (với biến kiểu thực)
    *   Câu lệnh đưa giá trị các biểu thức ra màn hình là:
        *   **print(danh sách biểu thức)**
