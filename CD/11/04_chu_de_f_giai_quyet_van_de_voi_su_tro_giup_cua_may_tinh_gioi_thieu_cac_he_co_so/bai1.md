## Bài 1: BÀI TOÁN QUẢN LÍ VÀ CƠ SỞ DỮ LIỆU

Học xong bài này, em sẽ:
*   Nhận biết được nhu cầu lưu trữ dữ liệu và khai thác thông tin cho bài toán quản lí.
*   Diễn đạt được khái niệm hệ cơ sở dữ liệu, nếu nêu được ví dụ minh họa.

Có một số cụm từ mà em đã từng nghe và có thể em đã từng dùng, ví dụ: "Quản lí học sinh", "Quản lí nhân sự", "Quản lí chi tiêu cá nhân",... Theo em, việc quản lí có liên quan đến việc lưu trữ và xử lí dữ liệu không? Hãy nêu một việc em đã làm để quản lí một hoạt động nào đó của mình.

### 1. Bài toán quản lí

Có rất nhiều bài toán quản lí cho các tổ chức lớn, nhỏ khác nhau với mức độ phức tạp khác nhau và ngay cả mỗi cá nhân cũng có những nhu cầu quản lí của riêng mình. Quản lí là công việc rất phổ biến. Xã hội càng phát triển, càng văn minh thì nhu cầu và chất lượng quản lí các hoạt động càng cao.

Việc quản lí một tổ chức gắn liền với những dữ liệu phản ánh thông tin về hoạt động của tổ chức đó. Ví dụ: Dựa trên kết quả học tập của lớp mà giáo viên có thể đề xuất với nhà trường danh sách những em tham gia bồi dưỡng học sinh giỏi môn Tin học; để khách sạn quyết định có nhận cho khách thuê phòng hay không tuỳ thuộc vào thông tin về số phòng còn trống chưa ai thuê trong thời gian cụ thể đó. Trong hai ví dụ trên đây, dễ thấy rằng nếu thông tin không chính xác sẽ dẫn đến những hậu quả đáng tiếc.

Thông tin dùng trong bài toán quản lí phải chính xác, kết quả xử lí thông tin phải đáng tin cậy để giúp có được quyết định đúng đắn, hợp lí.

### 2. Xử lí thông tin trong bài toán quản lí

Các bài toán quản lí đều có chung đặc điểm là lưu trữ và xử lí dữ liệu về hoạt động của một tổ chức. Thông thường, từ "**hồ sơ**" được dùng để chỉ một tập hợp dữ liệu được tổ chức và thể hiện theo những khuôn mẫu nào đó. Xử lí thông tin trong bài toán quản lí bao gồm: **tạo lập hồ sơ, cập nhật và khai thác thông tin.**

#### Tạo lập hồ sơ

Ví dụ, để quản lí việc học tập của một lớp, hồ sơ của lớp thường có cấu trúc dạng bảng để dễ theo dõi.

Để phản ánh đúng thực tế, dữ liệu trong bảng phải đầy đủ và chính xác.
*   Dữ liệu phải đầy đủ so với yêu cầu quản lí. Ví dụ, muốn quản lí thông tin mỗi học sinh đã là đoàn viên hay chưa, bảng hồ sơ của lớp cần có thêm cột ghi nhận thông tin này, nếu sĩ số lớp là 45 thì bảng phải có 45 hàng dữ liệu.
*   Dữ liệu phải chính xác. Ví dụ, không thể có hai hàng trong bảng hoàn toàn giống nhau ở họ tên, ngày sinh và địa chỉ, vì hoặc đó là dư thừa dữ liệu hoặc không phân biệt được chính xác điểm của mỗi bạn trong hai bạn trùng tên đó.

Khi tạo lập hồ sơ cho mỗi bài toán quản lí, phải xác định đầy đủ những dữ liệu cần được lưu trữ, đồng thời dữ liệu nhập vào phải đúng đắn.

#### Cập nhật dữ liệu

Dữ liệu được lưu trữ cần được cập nhật để phản ánh kịp thời những thay đổi diễn ra trên thực tế. Ví dụ, trong quản lí học tập của một lớp, những việc làm sau đây là cập nhật dữ liệu:
*   Học sinh Hoàng Giang vừa chuyển nhà về địa chỉ “20 Chùa Bộc”, cần sửa đổi dữ liệu tương ứng, dữ liệu “27 Lò Sũ” không còn đúng nữa.
*   Cần bổ sung một hàng mới ghi dữ liệu cho học sinh Trần Anh Tuấn mới chuyển đến lớp.
*   Cần xoá dữ liệu của học sinh Nguyễn Thị Hà vì học sinh này đã chuyển trường do bố mẹ chuyển công tác về tỉnh khác.

Cập nhật dữ liệu gồm các thao tác: thêm, sửa, xoá dữ liệu. Toàn bộ dữ liệu sau mỗi lần cập nhật cũng phải thoả mãn tính đầy đủ và đúng đắn.

#### Khai thác thông tin

Mục đích của việc lưu trữ và cập nhật dữ liệu là để khai thác thông tin, phục vụ cho việc điều hành công việc và ra quyết định của người quản lí. Một số việc khai thác thông tin thường gặp là: *tìm kiếm dữ liệu, thống kê, lập báo cáo*.

*   **Tìm kiếm dữ liệu** là việc rút ra được các dữ liệu thoả mãn một số điều kiện nào đó từ dữ liệu đã lưu trữ. Ví dụ: tìm họ và tên học sinh có điểm môn Tin học cao nhất.
*   **Thống kê** là khai thác hồ sơ dựa trên tính toán để đưa ra các thông tin không có sẵn trong hồ sơ. Ví dụ: xác định điểm cao nhất và điểm thấp nhất của môn Tin học; xác định số học sinh là đoàn viên.
*   **Lập báo cáo** là sử dụng các kết quả tìm kiếm, thống kê, sắp xếp dữ liệu được rút ra để tạo lập một bộ hồ sơ mới có nội dung và cấu trúc theo một số yêu cầu cụ thể trong quản lí. Ví dụ: Hết mỗi học kì, giáo viên chủ nhiệm cần có một danh sách học sinh đề nghị nhà trường khen thưởng, cuối năm học cần báo cáo phân loại học tập để lên kế hoạch ôn tập hè cho lớp và trao đổi với phụ huynh về hướng nghiệp cho các em.

Khai thác thông tin là để phục vụ kịp thời cho công tác quản lí. Do vậy, việc xử lí dữ liệu trong hồ sơ phải nhanh chóng, chính xác và thông tin kết xuất ra phải ở dạng dễ hiểu cho người quản lí.

### Cơ sở dữ liệu và phần mềm hệ quản trị cơ sở dữ liệu

Theo em, có nên dùng phần mềm soạn thảo văn bản hay phần mềm bảng tính để tạo lập hồ sơ, cập nhật và khai thác thông tin trong hồ sơ phục vụ công tác quản lí của một tổ chức hay không? Vì sao?

Ngày nay, với khả năng lưu trữ dữ liệu khổng lồ, tốc độ truy xuất và xử lí dữ liệu vô cùng nhanh, máy tính là công cụ hỗ trợ đắc lực cho con người trong mọi hoạt động thông tin. Tập hợp hồ sơ dữ liệu làm cơ sở cho việc quản lí các hoạt động của một tổ chức, được số hoá để máy tính truy cập, cập nhật và xử lí, được gọi là một cơ sở dữ liệu (CSDL).

**Cơ sở dữ liệu**: tập hợp dữ liệu được tổ chức sao cho máy tính có thể lưu trữ, truy cập, cập nhật và xử lí để phục vụ cho hoạt động của một đơn vị nào đó.

Để giúp tạo lập, cập nhật CSDL và khai thác thông tin trong CSDL có loại phần mềm được gọi là **hệ quản trị CSDL** (Database Management System – DBMS).

**Hệ quản trị CSDL** là một hệ thống chương trình giúp người dùng tương tác với CSDL qua các giao diện dễ hiểu, dễ dùng (như hệ thống bảng chọn, hộp thoại, các biểu mẫu, báo cáo,...). Với CSDL, hệ quản trị CSDL là hệ thống chương trình truy cập được dữ liệu nhưng tuân theo những ràng buộc để đảm bảo tính đúng đắn cho mỗi thao tác cập nhật dữ liệu và khai thác dữ liệu.

Mỗi đơn vị, mỗi tổ chức có những yêu cầu riêng và cụ thể trong khai thác CSDL thể hiện qua các mẫu (giao diện) cập nhật dữ liệu, các mẫu tìm kiếm dữ liệu và báo cáo thường dùng. **Hệ cơ sở dữ liệu** của một đơn vị là cách gọi chung một tập hợp gồm: CSDL của đơn vị, hệ quản trị CSDL và các phần mềm ứng dụng có các giao diện tương tác với CSDL đáp ứng được nhu cầu quản lí của đơn vị đó.

Các phần mềm ứng dụng khác muốn sử dụng dữ liệu trong CSDL đều phải thông qua hệ quản trị CSDL giống như mọi chương trình máy tính đều phải chạy dưới sự kiểm soát, điều phối của hệ điều hành.

**Hệ quản trị CSDL**: phần mềm cung cấp môi trường thuận lợi và hiệu quả để tạo lập, lưu trữ và khai thác dữ liệu của CSDL.

## 4. Thực hành tìm hiểu các yêu cầu của một bài toán quản lí và CSDL phục vụ bài toán đó

Em hãy hình dung việc quản lí thư viện của một trường học, thảo luận với bạn và thực hiện các yêu cầu sau đây.

### a) Mô tả hoạt động của thư viện
Gợi ý: Cho mượn sách hoặc trả sách như thế nào? Căn cứ vào đâu để biết ai đã mượn, trả sách gì? Căn cứ vào đâu để biết một quyển sách cụ thể đã được cho mượn và chưa được trả lại?...

### b) Liệt kê những dữ liệu cần có trong CSDL
Gợi ý: Những đối tượng cần quản lí là người đọc, sách cho mượn,...
*   Với người đọc, cần quản lí thông tin gì? (Thông tin trên thẻ thư viện gồm: Số thẻ TV, Họ và tên,...).
*   Với sách cho mượn, cần quản lí thông tin gì? (Thông tin về quyển sách gồm: Mã sách, Tên sách, Tác giả,...).

### c) Nêu ví dụ
Nêu thêm ít nhất hai ví dụ cho mỗi công việc sau đây:
*   Cập nhật dữ liệu (cho CSDL):
    *   Ví dụ 1. Khi có thêm một học sinh làm thẻ thư viện, cần bổ sung một số thông tin của học sinh này vào CSDL.

- Tìm kiếm dữ liệu:
*   Ví dụ 2. Tìm xem trong thư viện có quyển “Tôi tài giỏi, Bạn cũng thế” không?
- Thống kê và báo cáo:
*   Ví dụ 3. Xác định trong thư viện có bao nhiêu quyển sách về Tin học (giả sử sách về Tin học sẽ có hai chữ cái đầu trong mã sách là “TH”).

Giả sử dùng một bảng để chứa dữ liệu thể hiện thông tin về những người được mượn sách ở thư viện (những người có thể thư viện), em hãy chỉ ra một vài điều kiện cho dữ liệu trong bảng đó nhằm đảm bảo tính chính xác của thông tin. Theo em, nếu dùng một phần mềm bảng tính để tạo lập, lưu trữ bảng dữ liệu đó thì phần mềm bảng tính có tự động kiểm soát các cập nhật dữ liệu để đảm bảo được các điều kiện đã đặt ra hay không?

## Luyện tập
Câu 1. Trong các câu sau, những câu nào đúng?
a) CSDL là tập hợp dữ liệu được lưu trữ trên thiết bị nhớ phục vụ cho hoạt động của một cơ quan, đơn vị nào đó.
b) Hệ CSDL của một đơn vị là phần mềm quản trị CSDL của đơn vị đó.
c) Các giá trị dữ liệu được lưu trữ trong CSDL phải thoả mãn một số ràng buộc để góp phần đảm bảo được tính đúng đắn của thông tin.
d) Hệ quản trị CSDL là chương trình kiểm soát được các cập nhật dữ liệu.

Câu 2. Theo em, những ứng dụng nào dưới đây cần có CSDL?
a) Quản lí bán vé máy bay.
b) Quản lí chi tiêu cá nhân.
c) Quản lí cước phí điện thoại.
d) Quản lí một mạng xã hội.

## Tóm tắt bài học

*   Các tổ chức hoạt động trong xã hội đều có nhu cầu lưu trữ dữ liệu và khai thác thông tin cho bài toán quản lí.
*   Muốn máy tính hỗ trợ đắc lực được cho công tác quản lí, dữ liệu của một đơn vị phải được tổ chức trong một CSDL với tính đầy đủ và đúng đắn.
*   Phần mềm quản trị CSDL là loại phần mềm tạo ra môi trường thuận lợi để tạo lập CSDL, cập nhật cho CSDL theo cách đúng đắn, đồng thời kiểm soát được các truy cập đến dữ liệu, đảm bảo tính chính xác và sự an toàn của dữ liệu.
