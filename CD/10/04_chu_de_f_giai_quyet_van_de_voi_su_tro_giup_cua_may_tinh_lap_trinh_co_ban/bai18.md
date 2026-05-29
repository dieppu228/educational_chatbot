# Bài 18: LẬP TRÌNH GIẢI QUYẾT BÀI TOÁN TRÊN MÁY TÍNH

**Học xong bài này, em sẽ:**

*   Trình bày tóm tắt được các bước cần thực hiện khi giải một bài toán bằng lập trình trên máy tính với một ngôn ngữ lập trình bậc cao.

Theo em, cách phát biểu đề bài của một bài tập trong tin học và trong toán học thường khác nhau ra sao?

# Bài 1: NHÓM NGHỀ THIẾT KẾ VÀ LẬP TRÌNH
**CHỦ ĐỀ G : Hướng nghiệp với Tin học – Giới thiệu nhóm nghề thiết kế và lập trình**

## 1. Quá trình giải một bài toán bằng lập trình

Việc lập trình trên máy tính để giải quyết một bài toán gồm những bước nào?

Bài toán tin học thường gắn liền với các vấn đề thực tế trong cuộc sống và được phát biểu dưới dạng ngôn ngữ tự nhiên, gắn liền với bối cảnh xuất hiện bài toán. Dưới đây là một ví dụ cụ thể về một bài toán tin học và quá trình giải quyết bài toán này bằng lập trình.

Ví dụ: Bài toán **Quản lí tiền điện**

Em có dữ liệu về số tiền mà gia đình em chi trả cho tiêu thụ điện trong mỗi tháng của năm vừa rồi. Hãy tính tổng số tiền điện gia đình em phải trả cho cả năm, tính số tiền điện trung bình phải trả mỗi tháng và liệt kê các tháng dùng nhiều điện hơn trung bình cho mỗi tháng.

Dữ liệu vào từ bàn phím gồm một dòng chứa 12 số nguyên, các số cách nhau bằng dấu cách, số thứ i là tiền điện (tính theo đơn vị nghìn đồng) phải chi trả ở tháng i, (i = 1, 2,..., 12).

Kết quả đưa ra màn hình, dòng thứ nhất là tổng số tiền phải trả trong cả năm, dòng thứ hai là thông báo về số tiền trung bình hàng tháng phải trả, dòng thứ ba chứa danh sách các tháng dùng điện cao hơn mức trung bình.

Để giải một bài toán đã cho, trước hết cần xác định rõ bài toán yêu cầu tìm gì, dữ liệu cho ban đầu gồm những gì và được cho ở dạng nào. Trên cơ sở đó, ta có thể phát biểu lại bài toán dưới dạng tóm tắt, nêu các mối quan hệ toán học giữa các đại lượng đã cho. Đây là bước **Xác định bài toán**.

Bài toán Quản lí tiền điện nêu trên có thể phát biểu tóm tắt như ở Hình 1.

**Bài toán Quản lí tiền điện**
Cho dãy 12 số nguyên t₁, t₂, ..., t₁₂.
Yêu cầu:
*   Tính tổng các số trong dãy s = Σ(tᵢ từ i=1 đến 12).
*   Tính trung bình cộng: av = s/12.
*   Đưa ra các vị trí i thoả mãn điều kiện tᵢ > av.

Trên cơ sở phát biểu tóm tắt, rút gọn được bài toán như trên, tiếp đến cần Tìm **thuật toán** giải bài toán và cách tổ chức dữ liệu tương ứng để có thể viết chương trình giải bài toán. Ở Hình 2 là một mô tả thuật toán để giải bài toán đã phát biểu tóm tắt ở Hình 1.

**Thuật toán giải bài toán Quản lí tiền điện**
*   Bước 1. Nhập dãy số tiền (t₁, t₂, ..., t₁₂).
*   Bước 2. Khởi tạo giá trị ban đầu: s = 0.
*   Bước 3. Cộng dồn giá trị các số của dãy vào tổng s.
*   Bước 4. Đưa ra giá trị s.
*   Bước 5. Tính và đưa ra giá trị trung bình av = s/12.
*   Bước 6. Duyệt tuần tự từ t₁ đến t₁₂: đưa ra i nếu tᵢ > av (i = 1, 2, ..., 12).

Khi đã xác định được thuật toán cùng với cách tổ chức dữ liệu, ta có thể tiến hành **Viết chương trình**, tức là viết lại thuật toán trên một ngôn ngữ lập trình. Chương trình Python trong Hình 3 là kết quả viết chương trình thể hiện thuật toán mô tả ở Hình 2.

Đoạn mã này là một chương trình Python thực hiện việc quản lý tiền điện. Nó yêu cầu người dùng nhập 12 số tiền điện của 12 tháng, sau đó tính tổng tiền điện cả năm và số tiền điện trung bình mỗi tháng. Cuối cùng, chương trình sẽ liệt kê các tháng có số tiền điện cao hơn mức trung bình.

Với chương trình vừa viết xong cần phải chạy thử và kiểm tra xem chương trình có lỗi hay không và nếu tìm thấy thì phải sửa tất cả các lỗi tìm được. Đây là bước cuối cùng, bước **Kiểm thử, chạy và hiệu chỉnh chương trình**.

Có thể xem quá trình giải bài toán bằng lập trình trên máy tính có các bước như sau:
*   Bước 1. Xác định bài toán.
*   Bước 2. Tìm thuật toán giải bài toán và cách tổ chức dữ liệu.
*   Bước 3. Viết chương trình.
*   Bước 4. Kiểm thử, chạy và hiệu chỉnh chương trình.

Việc hiểu rõ hơn mục tiêu cũng như biết thêm một số lưu ý của từng bước nêu trên sẽ giúp việc lập trình trở nên nhẹ nhàng hơn và đạt hiệu quả cao hơn.

## Các bước giải bài toán bằng lập trình

### a) Xác định bài toán

Khi xác định bài toán có thể cần bỏ qua bối cảnh thực tế nêu trong đề bài, xác định những giá trị đã cho và các mối quan hệ giữa chúng. Điều rất quan trọng là xác định được mối quan hệ giữa các đại lượng đã cho với những giá trị cần tìm. Những mối quan hệ này không phụ thuộc vào bản chất vật lí của các đại lượng mà thường biểu diễn được bằng công thức, phương trình, bất phương trình,... Bởi vậy, bước này còn hay được gọi là bước xây dựng mô hình toán học. Nói một cách khác, mô hình toán học cô đọng, ngắn gọn, sẽ giúp ta có cái nhìn bao quát vấn đề cần giải quyết, thấy được các tình huống cần xem xét, các cách tổ chức dữ liệu có thể và từ đó tìm ra thuật toán giải bài toán.

### b) Tìm thuật toán giải bài toán và cách tổ chức dữ liệu

Đây là bước tìm thuật toán dựa trên kết quả quan trọng của bước xác định bài toán, dựa trên mối quan hệ giữa các đại lượng đã cho với những giá trị cần tìm. Cùng với việc tìm thuật toán, ta đồng thời phải xác định các cách tổ chức dữ liệu có thể sử dụng tương ứng với thuật toán đó.

Ví dụ như ở bài toán Quản lí tiền điện, thông tin về tiền điện hằng tháng được sử dụng hai lần. Lần đầu từ dữ liệu tiền điện của 12 tháng, ta tính tổng tiền điện và mức chi trung bình tháng. Lần thứ hai là xem lại tiền điện của từng tháng để đưa ra tháng nào dùng điện nhiều. Như vậy dữ liệu tiền điện hằng tháng cần phải được lưu lại và do vậy ta nhận thấy cấu trúc dữ liệu thích hợp là mảng (hay danh sách trong Python).

### c) Viết chương trình

Muốn viết chương trình cho máy tính thực hiện, ta cần nắm vững một ngôn ngữ lập trình. Có nhiều ngôn ngữ lập trình bậc cao khác nhau, tuy nhiên mỗi ngôn ngữ lập trình

bậc cao đều được xây dựng trên những yếu tố cơ bản gồm:
*   Bảng chữ cái (bộ các kí tự được phép sử dụng) của ngôn ngữ;
*   Quy định về cách viết các thành tố như: tên, câu lệnh, biểu thức;
*   Loại dữ liệu cơ sở có thể lưu trữ và xử lí;
*   Các phép tính và loại câu lệnh có thể thực hiện;
*   Các kiểu dữ liệu có cấu trúc;
*   Thư viện chương trình con cung cấp sẵn cho người lập trình.
Trong quá trình giải quyết một bài toán trên máy tính, khi đã xác định được cấu trúc dữ liệu và thuật toán, bước viết chương trình trong một ngôn ngữ lập trình bậc cao cụ thể đòi hỏi ta cần sử dụng được:
*   Các lệnh nhập dữ liệu vào và đưa kết quả ra;
*   Các kiểu dữ liệu như số nguyên, số thực, xâu kí tự, danh sách,... và cách dùng chúng;
*   Các câu lệnh tương ứng thể hiện cấu trúc rẽ nhánh, cấu trúc lặp của thuật toán;
*   Các chương trình con đã cung cấp sẵn trong các thư viện của ngôn ngữ lập trình đó và cách tự xây dựng chương trình con.

Như ta đã biết, mọi dữ liệu trong máy tính đều là dãy các bit. Máy tính chỉ có thể “hiểu” được những chỉ dẫn bằng **ngôn ngữ máy** (ngôn ngữ viết bằng dãy bit). Vì vậy, để máy tính có thể hiểu và thực hiện được chương trình viết trên ngôn ngữ lập trình bậc cao cần có công cụ dịch chương trình sang ngôn ngữ máy. Việc dịch có thể thực hiện theo nguyên tắc **biên dịch (Compiler)** hoặc **thông dịch (Interpreter)**.

Ở chế độ biên dịch, chương trình không còn lỗi cú pháp sẽ được dịch sang ngôn ngữ máy. Chương trình trên ngôn ngữ máy này sẽ được gọi ra ở mỗi lần cần thực hiện.
Ở chế độ thông dịch, khi thực hiện chương trình, gặp đến câu lệnh nào thì câu lệnh đó sẽ được dịch ra ngôn ngữ máy để thực hiện. Trong quá trình thực hiện chương trình, nếu một câu lệnh được thực hiện bao nhiêu lần thì nó sẽ được dịch lại bấy nhiêu lần.

### d) Kiểm thử, chạy và hiệu chỉnh chương trình

Một chương trình viết xong chưa chắc đã chạy được ngay trên máy tính để cho ra kết quả mong muốn. Việc tìm lỗi, sửa lỗi, điều chỉnh lại chương trình cũng một công việc quan trọng trong các giai đoạn giải bài toán bằng máy tính.
Cần lưu ý là dù việc kiểm thử có làm tốt đến mức độ nào đi nữa thì trong hầu hết các trường hợp ta chỉ có thể khẳng định là chương trình cho kết quả đúng với nhiều bộ dữ liệu vào khác nhau.

## Luyện tập
Bài 1. Có nhất thiết phải tìm được thuật toán trước khi viết chương trình để giải bài toán đó không?
Bài 2. Nếu muốn học một ngôn ngữ lập trình bậc cao, em sẽ phải tìm hiểu những gì ở ngôn ngữ lập trình đó?

Em hãy giới thiệu một bài toán thực tế mà em biết và trình bày các bước cần thực hiện để giải quyết bài toán đó bằng máy tính.

Trong các câu sau, những câu nào đúng?
1) Kết quả của bước xác định bài toán có ý nghĩa quan trọng đối với bước tìm thuật toán giải bài toán.
2) Nếu không biết thuật toán của một bài toán thì không thể viết được chương trình để máy tính giải quyết bài toán đó.
3) Việc viết chương trình không liên quan gì đến thuật toán và cách tổ chức dữ liệu.
4) Chỉ cần kiểm thử một chương trình khi không thực hiện được chương trình và gặp báo lỗi trên màn hình.

## Tóm tắt bài học
* Các bước giải bài toán trên máy tính:
    * Xác định bài toán.
    * Tìm thuật toán giải bài toán và cách tổ chức dữ liệu.
    * Viết chương trình: mô tả thuật toán bằng ngôn ngữ lập trình.
    * Kiểm thử chương trình.
* Mỗi **ngôn ngữ lập trình bậc cao** đều có các **yếu tố cơ bản**: **bảng chữ cái**; **cú pháp**, **ngữ nghĩa**; các **kiểu dữ liệu**; các **câu lệnh**, **biểu thức**, **thư viện các hàm cho sẵn**.
* Có hai **chế độ dịch chương trình** viết trên **ngôn ngữ lập trình bậc cao** sang **ngôn ngữ máy** là **biên dịch** và **thông dịch**.

## Học xong bài này, em sẽ:
* Nêu được một số thông tin cơ bản về nhóm nghề thiết kế và lập trình:
    * Sơ lược về các công việc chính.
    * Yêu cầu chính về kiến thức và kĩ năng.
    * Các ngành học có liên quan ở các bậc học tiếp theo.
    * Nhu cầu nhân lực hiện tại và tương lai.

Theo em, vì sao nghề thiết kế và lập trình đang được nhiều bạn trẻ yêu thích tin học ưu tiên lựa chọn?

Định hướng, lựa chọn nghề nghiệp cho tương lai là việc rất quan trọng đối với mỗi học sinh cấp trung học phổ thông.

Dựa trên **khả năng**, **cá tính**, **sở thích** và **nguyện vọng** của bản thân kết hợp với **đặc điểm ngành nghề**, **cơ hội được đào tạo và việc làm**, mỗi em sẽ định hướng và lựa chọn cho bản thân ngành nghề trong tương lai (Hình 1).

# Bài 1: Mô tả nhóm nghề thiết kế và lập trình

1 Em đã nghe tới cụm từ "lập trình viên" chưa? Em hãy trình bày những hiểu biết, suy nghĩ, cảm nhận của em về "lập trình viên".

## a) Vài nét sơ lược về phát triển phần mềm

Phát triển phần mềm là công việc của nhóm nghề thiết kế và lập trình, đó là quá trình tạo ra sản phẩm phần mềm máy tính để đáp ứng nhu cầu của một cộng đồng người dùng. Có thể mô tả sơ lược những công đoạn chính của quá trình đó như sau:
* **Phân tích hệ thống**: phân tích nhu cầu của cộng đồng cần phục vụ, xác định vai trò của phần mềm, xác định thông tin đầu vào, đầu ra của hệ thống phần mềm cần xây dựng.
* **Thiết kế phần mềm**: chuyển các yêu cầu về phần mềm thành bản thiết kế phần mềm. Có thể hiểu sơ lược bản thiết kế phần mềm là một tập hợp các mô tả về tổ chức dữ liệu, kiến trúc, thuật toán và giao diện (dựa trên đồ họa, bảng hay ngôn ngữ).
* **Lập trình**: chuyển những mô tả ở bản thiết kế thành các lệnh thực hiện được trên máy tính để máy tính "hiểu" và "thực hiện" đúng theo thiết kế.
* **Kiểm thử phần mềm**: thực hiện các bước thử nghiệm sản phẩm xem có khiếm khuyết gì không để khắc phục kịp thời trước khi phần mềm đến tay người sử dụng.

Khi thực hiện phát triển một phần mềm thì số lượng người và sự chuyên biệt hóa công việc phụ thuộc vào quy mô và công nghệ sử dụng của phần mềm đó. Một người được phân công làm ở vị trí nào, trong công đoạn nào sẽ phụ thuộc vào quy mô phần mềm và trình độ, kinh nghiệm làm việc của người đó. Trường hợp xây dựng một phần mềm nhỏ thì một người có thể làm tất cả các công đoạn, vừa thiết kế chương trình vừa lập trình. Nhưng khi xây dựng các hệ thống phần mềm lớn, mỗi công đoạn của phát triển phần mềm sẽ do một nhóm chuyên biệt thực hiện.

Sau đây là hai loại tình huống điển hình cần thiết phải có nguồn nhân lực phát triển phần mềm:
* Tổ chức hoặc doanh nghiệp muốn áp dụng công nghệ số để phục vụ quản lí, sản xuất hay kinh doanh, do vậy xuất hiện yêu cầu phát triển phần mềm.
* Công nghệ phát triển và thay đổi làm cho các tổ chức, doanh nghiệp phải cập nhật theo xu hướng mới để tồn tại và phát triển. Khi đó, những nhà phát triển phần mềm sẽ phải thực hiện nâng cấp, bảo trì, khai thác các chương trình máy tính theo công nghệ mới cho các tổ chức, doanh nghiệp này.

## b) Thiết kế và lập trình các sản phẩm phần mềm

### Phát triển phần mềm ứng dụng web

Ngày nay lập trình ứng dụng web đã trở thành một lĩnh vực sôi động và có tốc độ phát triển nhanh. Ban đầu nhu cầu rất phổ biến là phát triển ứng dụng dựa trên nền tảng web cho máy tính. Càng ngày nhu cầu phát triển ứng dụng trực tuyến càng tăng trưởng mạnh và tiếp đến có sự bùng nổ ở thị trường phát triển ứng dụng trên thiết bị di động. Các ứng dụng web được triển khai trên nhiều lĩnh vực: chính phủ điện tử, quản trị doanh nghiệp điện tử, thanh toán điện tử, giải trí điện tử, công dân điện tử, y tế điện tử, mạng xã hội, giáo dục trực tuyến,...

### Phát triển thương mại điện tử

Trước đây, thương mại điện tử vẫn còn là một khái niệm khá mới mẻ tại Việt Nam. Đến nay, nó đã trở thành một phần không thể thiếu trong hoạt động kinh doanh của không chỉ các doanh nghiệp mà cả nhóm nhỏ lẻ, cá nhân. Chất lượng ứng dụng thương mại điện tử vào kinh doanh đang là yếu tố quyết định giá trị cạnh tranh.

### Thiết kế và lập trình trò chơi

Lập trình trò chơi hay còn gọi là lập trình game, ngành công nghiệp này ở nước ta mới chỉ dừng lại ở mức phân phối phát hành và gia công các game nước ngoài. Trong những năm gần đây, nhiều doanh nghiệp thành lập ra studio riêng của mình nhằm phát triển sản xuất game thuần Việt, kéo theo đó là sự tăng trưởng lớn về nhu cầu nhân lực ở tất cả các khâu của quá trình sản xuất game: thiết kế đồ họa game (Game Design), lập trình game (Programming), âm thanh (Audio),...

## 2 Đặc điểm lao động, yêu cầu đối với nhóm nghề thiết kế và lập trình

Với nghề thiết kế và lập trình, người lao động có rất nhiều lựa chọn việc làm. Họ có thể làm việc cho khối cơ quan nhà nước hay khối doanh nghiệp tư nhân, làm cho các công ty chuyên về IT (Information Technology), chuyên về sản xuất phần mềm hay là thành viên trong bộ phận công nghệ thông tin phục vụ hoạt động của một đơn vị nào đó. Các đơn vị, các doanh nghiệp thuộc các lĩnh vực khác nhau như: công nghiệp, thương mại, viễn thông, xây dựng, hàng không, văn hoá, dịch vụ,... đều có nhu cầu về nguồn nhân lực này. Phát triển phần mềm không chỉ là sản xuất của những tổ chức gia công phần mềm trong nước mà còn là sản xuất, kinh doanh của nhiều tổ chức liên doanh với nước ngoài hay hoàn toàn của nước ngoài.

Vì tính chất công việc, người lao động có thể làm việc với máy tính tại văn phòng công ty hoặc làm việc độc lập tại nhà. Những công ty phần mềm lớn luôn coi trọng việc tạo không gian và môi trường làm việc mở cho các nhân viên nhằm nâng cao sự sáng tạo và hiệu quả công việc.

Nhóm nghề thiết kế và lập trình tạo ra những sản phẩm công nghệ thông tin đáp ứng nhu cầu phát triển xã hội, phục vụ sinh hoạt, giải trí của con người. Nghề thiết kế và lập trình đang thu hút nguồn nhân lực với số lượng lớn và có mức thu nhập cao. Theo thống kê từ TopDev, trang chuyên tuyển dụng nhân lực về công nghệ phần mềm, Việt Nam luôn trong tình trạng thiếu hụt ứng viên về cả số lượng và chất lượng. Cụ thể, năm 2020, ngành công nghệ thông tin cần khoảng 400 000 nhân sự, thiếu khoảng 100 000 nhân sự, năm 2021 cần 500 000 nhân sự, thiếu khoảng 190 000 nhân sự (nguồn: https://tapchicongthuong.vn ngày 8/5/2021). Dự báo nhân lực ngành công nghệ thông tin sẽ tiếp tục thiếu trong các năm tiếp theo.

### Người theo nghề thiết kế và lập trình có những đặc điểm:

*   **Kiên trì, đam mê**: Phát triển phần mềm là việc đòi hỏi sự kiên trì, tỉ mỉ. Người theo nhóm nghề này cần thực hành và trao đổi thường xuyên với đồng nghiệp để phát triển được kĩ năng đáp ứng công việc. Công nghệ ngày càng phát triển, vì vậy người đam mê với công nghệ sẽ có khả năng bắt kịp các xu thế mới, cập nhật được công nghệ tiên tiến, phát triển được sự nghiệp.
*   **Tư duy logic và chính xác**: Đây là công việc đòi hỏi nhiều mô tả có tính logic, chính xác và đầy đủ để có được sản phẩm đáp ứng đúng nhu cầu người dùng. Trong lập trình một lỗi sai nhỏ cũng có thể dẫn tới chương trình không hoạt động hoặc hoạt động không chính xác.
*   **Khả năng tự học, sáng tạo**: Đối diện với sự thay đổi nhanh chóng của công nghệ, người thiết kế và lập trình phải luôn tự học, chủ động cập nhật kiến thức và kĩ năng mới. Tính chất của công việc thiết kế luôn đòi hỏi sự sáng tạo. Thiết kế phần mềm là phải tìm tòi để xuất các giải pháp hiệu quả để giải quyết được vấn đề thực tế. Lập trình cũng cần đến sự thông minh, tinh tế và sáng tạo, vì lập trình tức là đã tạo ra một phần mềm hữu dụng.
*   **Khả năng đọc hiểu tiếng Anh**: Để đảm bảo được công việc, nghề thiết kế và lập trình đòi hỏi người thiết kế và lập trình cần đọc hiểu được tiếng Anh chuyên ngành.

## Đào tạo và việc làm

Theo em những nghề thuộc nhóm thiết kế và lập trình có thể làm ở những cơ quan, tổ chức nào?

Trong giai đoạn từ năm 2015 đến năm 2020, ngành công nghệ thông tin là một trong những ngành có số lượng tuyển sinh cao nhất hằng năm. Tính đến thời điểm năm 2020, trong cả nước có khoảng gần 200 khoa đào tạo công nghệ thông tin bậc cao đẳng

và đại học (Nguồn: Cẩm nang tuyển sinh Đại học và Cao đẳng năm 2021, NXB Phụ nữ Việt Nam phát hành tháng 5/2021). Trong đó có một số trường đại học có thương hiệu đào tạo chất lượng cao như: Trường Đại học Công nghệ – Đại học Quốc gia Hà Nội, Trường Đại học Bách khoa Hà Nội, Trường Đại học Bách khoa và Trường Đại học Khoa học Tự nhiên – Đại học Quốc gia Thành phố Hồ Chí Minh (Nguồn: Giáo dục Việt Nam có thêm 6 lĩnh vực của bảng xếp hạng Quốc tế, Báo Đại đoàn kết ngày 04/9/2021),... Nhu cầu phát triển **phần mềm** trong thời đại số hoá rất lớn, do đó đào tạo chuyên ngành **kĩ thuật phần mềm** được xem là một trong những mũi nhọn của đào tạo nhân lực **công nghệ thông tin**. Theo chương trình đào tạo của chuyên ngành này, sinh viên được trang bị các kiến thức nền tảng về khoa học cơ bản của ngành công nghệ thông tin và kiến thức chuyên sâu về quy trình phát triển phần mềm; các phương pháp, kĩ thuật, công nghệ trong phân tích, thiết kế, phát triển, kiểm thử, bảo trì phần mềm và quản lí dự án phần mềm,... Với các kiến thức cơ bản được trang bị, sinh viên tốt nghiệp có thể hoà nhập vào môi trường làm việc hiện đại với các vị trí như: **người phân tích thiết kế hệ thống phần mềm**, **lập trình viên**, **kiểm thử viên phần mềm**, **nhà quản trị hệ thống công nghệ thông tin**, **cán bộ nghiên cứu**, **cán bộ giảng dạy** về công nghệ thông tin tại các trường, viện nghiên cứu và các cơ sở đào tạo.

Để minh hoạ một phần về cơ hội việc làm rộng mở cho những người thiết kế và lập trình, một vài lĩnh vực họ có thể làm việc được giới thiệu sơ lược sau đây:

### a) Các công ty phần mềm
Có nhiều công ty phần mềm với những quy mô khác nhau, sản xuất các loại sản phẩm phần mềm khác nhau. Bên cạnh một số công ty lớn và nổi tiếng sản xuất các phần mềm thương mại, có nhiều công ty nhỏ hơn sản xuất phần mềm phục vụ cho các công ty và doanh nghiệp khác. Có những công ty cung cấp sản phẩm đa dạng nhưng cũng nhiều công ty chuyên làm phần mềm phục vụ một lĩnh vực nào đó, ví dụ như: lĩnh vực ngân hàng – tài chính, viễn thông, quản trị kinh doanh,...

### b) Các cơ quan Nhà nước
Ngày nay, **hệ thống phần mềm quản lí hành chính** cho các cấp chính quyền của mọi quốc gia đều có vai trò quan trọng. Phát triển phần mềm để thực hiện **chính quyền điện tử** rất được coi trọng và đầu tư. Các hệ thống lớn này đòi hỏi nhiều nhân lực thiết kế, phát triển, vận hành và bảo trì. Các nhà thiết kế và lập trình viên có cơ hội lớn làm việc ở nhiều vị trí trong các cấp chính quyền và cấp bộ ngành, chính phủ.

### c) Các doanh nghiệp tài chính – ngân hàng
**Hệ thống tài chính** là một trong những hệ thống thiết yếu, phức tạp, hằng ngày phải phân tích, thống kê xử lí khối lượng dữ liệu rất lớn. Các doanh nghiệp tài chính – ngân hàng

hàng của Nhà nước hay tư nhân đều phải sử dụng những hệ thống phần mềm phức tạp, có tính nghiệp vụ cao, yêu cầu bảo mật nghiêm ngặt. Tính tự động hoá của công việc ở khu vực làm việc này tạo nên áp lực cao nhưng đồng thời mở ra nhiều cơ hội lớn cho những người thiết kế và lập trình.

## Luyện tập

* Nếu giáo viên dạy môn Tin học ở trường em viết phần mềm quản lí điểm cho trường thì em có thể gọi giáo viên đó là lập trình viên được không? Vì sao?

* Em có dự định sẽ làm việc trong các lĩnh vực thiết kế và lập trình không? Vì sao?

* Trong các câu sau đây, những câu nào đúng?
    1) Công việc của lập trình viên là viết các dòng lệnh bằng một ngôn ngữ lập trình.
    2) Phần mềm ứng dụng cần nâng cấp, chỉnh sửa để đáp ứng sự thay đổi mới của công nghệ số.
    3) Để thiết kế và lập trình cần rất giỏi Toán và thành thạo tiếng Anh.
    4) Số lượng cung cầu về lập trình viên ở Việt Nam đã cân bằng. Do vậy nhiều sinh viên tốt nghiệp ngành lập trình trong những năm tới rất khó tìm kiếm được việc làm.
    5) Sinh viên tốt nghiệp ngành công nghệ thông tin không có cơ hội tìm kiếm việc làm trong lĩnh vực tài chính.

## Tóm tắt bài học

Có nhiều lĩnh vực liên quan đến thiết kế và lập trình như: phát triển ứng dụng phần mềm và web; thương mại điện tử; lập trình ứng dụng trên thiết bị di động; lập trình trò chơi. Nhu cầu nhân lực cho các lĩnh vực này rất lớn, đặc biệt là phát triển phần mềm tài chính, phần mềm chính phủ. Đào tạo nguồn nhân lực thiết kế và lập trình được coi là lĩnh vực đào tạo mũi nhọn hướng đến sự phát triển của công nghệ và khoa học kĩ thuật trong thời đại số.

DỰ ÁN NHỎ:

# Bài 2: TÌM HIỂU VỀ NGHỀ LẬP TRÌNH WEB, LẬP TRÌNH TRÒ CHƠI VÀ LẬP TRÌNH CHO THIẾT BỊ DI ĐỘNG

## 1. Mục đích của dự án
Sau khi hoàn thành xong dự án, em có khả năng:
* Tìm kiếm và khai thác được thông tin khái quát về nghề thiết kế và lập trình web, thiết kế và lập trình trò chơi, phát triển ứng dụng trên thiết bị di động và các ngành nghề khác.
* Giao lưu được với bạn bè qua các kênh truyền thông tin số để tham khảo và trao đổi thông tin hướng nghiệp.
* Trình bày, giới thiệu về một vài nghề trong nhóm nghề thiết kế và lập trình.

## 2. Yêu cầu chung
* Chia lớp thành ba nhóm, mỗi nhóm thực hiện một đề tài. Mỗi học sinh lựa chọn tham gia một nhóm.
    * Nhóm 1. Tìm hiểu nghề thiết kế và lập trình web
    * Nhóm 2. Tìm hiểu nghề thiết kế và lập trình trò chơi
    * Nhóm 3. Tìm hiểu nghề phát triển ứng dụng trên thiết bị di động
* Thời gian thực hiện dự án: 2 tuần, trong đó có 2 tiết học trên lớp. Giáo viên quy định nhiệm vụ của 2 tiết trên lớp học (bao gồm nhiệm vụ trình bày kết quả thực hiện dự án), đồng thời các nhóm học sinh chủ động thực hiện dự án ngoài giờ học trên lớp.

## 3. Một số hướng dẫn và gợi ý thực hiện dự án
* **Giai đoạn 1. Lập kế hoạch**
    * Xác định mục tiêu dự án
    * Lập danh sách công việc cụ thể
    * Dự kiến sản phẩm
    * Phân chia công việc và lên lịch triển khai
* **Giai đoạn 2. Thực hiện dự án**
    * Mỗi người thực hiện nhiệm vụ được phân công
    * Nhóm thảo luận, đề xuất, đóng góp ý kiến
    * Phối hợp chuẩn bị và hoàn thiện sản phẩm
* **Giai đoạn 3. Báo cáo kết quả**
    * Trình bày báo cáo kết quả thực hiện dự án
    * Giới thiệu sản phẩm của nhóm

Các nhóm cần thực hiện dự án theo ba giai đoạn với những nhiệm vụ chính của từng giai đoạn như trong Hình 2.

### Gợi ý về những việc cần làm

*   Tìm kiếm thông tin (qua mạng, qua phỏng vấn, qua giao lưu khách mời), tổng hợp biên tập thông tin.
*   Chuẩn bị sản phẩm và báo cáo kết quả dự án.
    Với hai mảng việc lớn trên, phối hợp với dự kiến sản phẩm để tạo ra danh sách công việc cụ thể cần làm.

### Gợi ý về sản phẩm

*   Sản phẩm thứ nhất: Bản mô tả nghề (chuẩn bị bằng tệp văn bản) có những nội dung chính như ở Bảng 1.
*   Sản phẩm thứ hai: Bài trình bày, giới thiệu về nghề được nhóm tìm hiểu: chuẩn bị bằng phần mềm trình chiếu (thời gian trình bày tuỳ theo quy định của giáo viên).

### Hai tiêu chí đánh giá

*   Nội dung: cung cấp được những thông tin cơ bản về nghề mà nhóm tìm hiểu
*   Hình thức: có tính thẩm mĩ, ngắn gọn và hấp dẫn

**Chú ý**: Chất lượng nội dung và hình thức phụ thuộc nhiều vào khả năng tìm kiếm, giao lưu và chia sẻ thông tin hướng nghiệp. Các kĩ năng ứng dụng công nghệ thông tin cần được khai thác tốt để có được sản phẩm đáp ứng yêu cầu dự án.

### Những nội dung chính của sản phẩm thứ nhất

1.  Giới thiệu khái quát nghề, công cụ, phương tiện lao động của nghề.
2.  Tên nghề nghiệp, các chuyên môn chủ yếu.
3.  Đặc điểm lao động và yêu cầu của nghề (sản phẩm chính là gì?).
4.  Đào tạo và tuyển sinh:
    *   Nơi đào tạo uy tín.
    *   Số lượng tuyển sinh hằng năm.
5.  Cơ hội, môi trường làm việc và thu nhập, phúc lợi xã hội:
    *   Tình hình tuyển dụng nhân lực.
    *   Môi trường làm việc, thu nhập, tính ổn định và cơ hội phát triển, thăng tiến.
