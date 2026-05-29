## Nhiệm vụ 1. Trích xuất thông tin về ước tính kì hạn vay từ dữ liệu cho trước

### Yêu cầu:
Khi quyết định vay một số tiền lớn và trả góp hằng tháng trong một thời gian dài, người vay cần lựa chọn phương án phù hợp với khả năng trả góp hằng tháng của mình. Kì hạn vay phụ thuộc vào số tiền trả góp hằng tháng và mặt bằng lãi suất lúc đi vay. Hãy xác định kì hạn vay dựa trên dữ liệu về mặt bằng lãi suất cho trước và số tiền trả góp hằng tháng.

### Hướng dẫn thực hiện:
#### 1. Xác định vấn đề
Xác định kì hạn vay dựa trên dữ liệu về mặt bằng lãi suất cho trước.
#### 2. Thu thập dữ liệu
Các dữ liệu đầu vào cần có:
*   Số tiền cần vay;
*   Số tiền có thể trả góp hằng tháng;
*   Lãi suất theo năm của một số ngân hàng khi đi vay.
#### 3. Phân tích dữ liệu, trích xuất thông tin bằng công cụ phân tích dữ liệu nâng cao của Excel
Từ dữ liệu đầu vào có thể trích xuất thông tin về thời hạn vay phù hợp với khả năng trả góp bằng cách dùng hàm **PMT** kết hợp với công cụ phân tích **What-If Analysis** có sẵn trong Excel.

**PMT** (viết tắt của “payment”) là một hàm tài chính của Excel có thể dùng để tính khoản thanh toán định kì cho một khoản vay. Khi nhân **PMT** với số tháng sẽ là tổng số tiền phải trả trong suốt kì hạn của khoản vay. Excel gợi ý cú pháp hàm **PMT** với các tham số: **rate** (lãi suất), **nper** (số kì hạn), **pv** (giá trị hiện tại), cùng với các tham số tùy chọn **fv** (giá trị tương lai) và **type** (thời điểm thanh toán).

Trong đó, **rate** là lãi suất (không đổi trong suốt kì hạn), **nper** là kì hạn (số tháng), **pv** là giá trị hiện tại của khoản đầu tư, [**fv**] và [**type**] là các tham số không bắt buộc phải có.

Công cụ phân tích **What-If Analysis** cho phép người dùng thử các giá trị khác nhau cho các công thức. **What-If Analysis** bao gồm ba công cụ chính:
*   **Scenario Manager**: cho phép tạo và quản lí các kịch bản khác nhau, mỗi kịch bản có các giá trị đầu vào riêng.

*   **Data Table**: cho phép xem cách các giá trị đầu vào của một công thức thay đổi khi thay đổi một hoặc nhiều giá trị đầu vào.
*   **Goal Seek**: cho phép tìm giá trị đầu vào cần thiết để đạt được một mục tiêu cụ thể.
Với yêu cầu của nhiệm vụ này, ta sử dụng công cụ Data Table để thấy số tiền phải trả mỗi tháng thay đổi như thế nào khi thay đổi lãi suất hoặc vừa thay đổi lãi suất vừa thay đổi kì hạn vay. Căn cứ vào dữ liệu sau khi phân tích, người vay có thể ước tính kì hạn vay theo khả năng trả góp hằng tháng.
#### 4. Ví dụ minh họa
##### a) Các dữ liệu đầu vào thu thập được:
*   Số tiền cần vay: 500 triệu VNĐ;
*   Số tiền có thể trả góp hằng tháng: khoảng 10 triệu VNĐ;
*   Lãi suất theo năm khi đi vay dao động tuỳ ngân hàng, ví dụ có các mức là 6,5%; 7,0; 7,5%; 8,0%.
##### b) Các bước thao tác:
###### Bước 1. Lập khối ô tính PMT.
*   Nhập số tiền vay vào ô C4.
*   Nhập mức lãi suất vay vào ô C5.
*   Nhập kì hạn vay vào ô C6.
*   Nhập vào ô C7 hàm **=PMT(C5/12, C6, -C4)**.
    Vay tiền là đầu tư với giá trị âm nên để kết quả của hàm PMT ra một số dương ta dùng dấu trừ “-” trước tham số *pv* (C4).
###### Bước 2. Phân tích dự báo What-If Analysis theo một biến lãi suất.
*   Nhập dãy giá trị biến thiên của mức lãi suất trong một cột (hoặc hàng); ví dụ: khối ô B13:B16.
*   Nhập vào ô C12 hàm **=PMT(C5/12, C6, -C4)**.
*   Đánh dấu chọn khối ô B12:C16.
*   Chọn Data, chọn What-If Analysis trong nhóm lệnh Forecast. Trong bảng chọn thả xuống, chọn **Data Table**.

- Hộp thoại **Data Table** xuất hiện nhập $C$5 vào ô Column input cell và chọn OK. Kết quả nhận được như khối ô B12:C16.

###### Bước 3. Phân tích dự báo **What-If Analysis** theo hai biến lãi suất và kì hạn vay.
*   Để dễ theo dõi, nhập dữ liệu cho khối ô E13:E16 tương tự như B13:B16.
*   Bổ sung thêm dãy giá trị biến thiên của kì hạn vay vào khối ô F12: I12 để tạo thành khối ô hình chữ nhật.
*   Nhập vào ô E12 hàm dùng để tính toán khoản thanh toán định kì (PMT) dựa trên lãi suất, số kì và giá trị hiện tại.
*   Lặp lại các thao tác để xuất hiện hộp thoại Data Table như ở Bước 2.
*   Nhập $C$5 vào ô Column input cell.
*   Nhập $C$6 vào ô Row input cell.
*   Chọn OK. Kết quả nhận được khối ô E12:I16.

###### Bước 4. Trích xuất thông tin về ước tính kì hạn vay theo khả năng trả góp hằng tháng căn cứ vào kết quả nhận được. Giá trị trong khối ô I13:I16 xấp xỉ 10 triệu VND. Kết luận: Thời hạn vay sẽ vào khoảng 60 tháng.

## Nhiệm vụ 2. Đưa ra dự báo dựa trên chuỗi thời gian

### Yêu cầu:
Xét ví dụ minh hoạ trình bày ở Bài 2 (trang 134). Để tìm ra mối quan hệ phụ thuộc của số lượng hành khách qua sân bay theo các chu kì thời gian, tổ dự án đã thu thập số liệu thống kê lượng hành khách hằng tháng trong quá khứ.
Giả sử tệp Excel chứa chuỗi thời gian gồm hai cột, cột A kiểu Date ghi lại chu kì thời gian (theo tháng) và cột B kiểu Number ghi lại số hành khách trong tháng đó.
Dựa trên chuỗi thời gian đó, sử dụng công cụ dự báo của Excel để:
a) Xem kết quả dự báo và các tham số được thiết lập theo mặc định.
b) Thay đổi một số tham số để hiểu và giải thích ý nghĩa của chúng trong kết quả dự báo nhận được.
c) Rút ngắn chuỗi thời gian đầu vào, ví dụ bỏ bớt các tháng của năm 2013. Dùng chuỗi thời gian đã rút ngắn để dự báo, so sánh với số liệu thực tế đã có và cho nhận xét.

### Hướng dẫn thực hiện:
#### a) Thực hiện các bước sau (cho yêu cầu a và c):
##### Bước 1. Chọn khối ô chứa dữ liệu chuỗi thời gian rồi chọn **Data**.
##### Bước 2. Chọn **Forecast Sheet** trong nhóm lệnh **Forecast**. Hộp thoại *Create Forecast Worksheet* xuất hiện.
##### Bước 3. Chọn **Create**, kết quả dự báo được tạo ra theo các thiết lập mặc định và lưu thành một trang mới.
##### Bước 4. Chọn **Options** để mở rộng hộp thoại *Create Forecast Worksheet* (Hình 6) và xem thiết lập mặc định cho các tham số: *Forecast Start*, *Forecast End*, *Confidence Interval*.
##### Bước 5. Kết quả thông tin được khai phá từ dữ liệu là dự báo cho một số tháng tiếp theo. Hình 6 là kết quả dự báo dựa trên tệp dữ liệu đã có dưới dạng biểu đồ đường. Đường màu xanh là biểu diễn dữ liệu hiện có (số lượng hành khách từ 01/01/2009 đến 01/09/2013), đường màu cam là biểu diễn dự đoán dữ liệu trong tương lai (số lượng hành khách từ 01/09/2013 đến 01/09/2015). Hình 7 là kết quả dự báo được trình bày trong khối ô **C59:C82**.

#### b) Lặp lại các thao tác như trên cho đến Bước 2. Tiếp theo, chọn **Options** để thay đổi một số tham số trước khi chọn Create xem kết quả và giải thích ý nghĩa.

Bỏ đánh dấu chọn **Confidence Interval** trước khi chọn Create, rút ra kết luận về tác dụng của lựa chọn này. Đánh dấu lựa chọn **Confidence Interval**, thay đổi tăng/giảm giá trị của **Confidence Interval**, chọn Create, cho biết tác động của sự thay đổi này tới đồ thị biểu diễn.

## Vận dụng
Nước ta xuất khẩu nhiều mặt hàng, trong đó có hải sản, rau quả là các mặt hàng có tính mùa vụ trong một năm. Hãy sưu tầm một chuỗi thời gian về xuất khẩu hải sản (hoặc rau quả) làm dữ liệu đầu vào và phân tích dự báo dựa trên chuỗi thời gian này để ước tính kim ngạch xuất khẩu trong năm tiếp theo.

Gợi ý về nguồn dữ liệu:
*   Tìm kiếm với cụm từ “số liệu xuất nhập khẩu các tháng năm 2023” để truy cập trang “https://www.gso.gov.vn/du-lieu-va-so-lieu-thong-ke/2023/03/so-lieu-xuat-nhap-khau-cac-thang-nam-2023/...”.
*   Tìm mục “Tệp đính kèm”; nháy chọn, ví dụ “Trị giá và mặt hàng xuất khẩu chủ yếu sơ bộ các tháng của năm 2023 (.xls)” hoặc “Trị giá và mặt hàng nhập khẩu chủ yếu
sơ bộ các tháng năm 2023 (.xls)”. Tệp Excel chứa số liệu xuất khẩu (nhập khẩu) nhiều mặt hàng sẽ xuất hiện.
– Thao tác tương tự như trên, nhưng trong cụm từ tìm kiếm thay 2023 thành 2022 sẽ nhận được số liệu xuất nhập khẩu các tháng của năm 2022. Bằng cách lùi dần như vậy, có thể nhận được chuỗi thời gian dài hơn.

## BÀI TÌM HIỂU THÊM

### PHẦN BỔ SUNG DATA MINING TRONG EXCEL

Excel có các phần bổ sung (Add-ins) giúp thực hiện phân tích dữ liệu nâng cao, bao gồm cả loại miễn phí và loại phải trả phí để có thể sử dụng. **Data Mining** là một Add-ins thực hiện khai phá dữ liệu có thể bổ sung miễn phí với Office 365. Các công cụ khai phá dữ liệu có sẵn sau khi bổ sung sẽ xuất hiện trong nhóm lệnh **Data Mining** gồm: phân loại (Classify), dự báo (Predict) và phát hiện luật kết hợp hay sự tương quan trong tập dữ liệu (Association).

Để thêm phần bổ sung **Data Mining** vào Excel, ta thực hiện theo các bước sau:
#### Bước 1. Trong cửa sổ làm việc của Excel, nháy chuột chọn **Insert\Get Add-ins**.
#### Bước 2. Hộp thoại *Office Add-ins* xuất hiện, tìm và chọn phần bổ sung muốn có.
#### Bước 3. Đọc qua các thông tin cần biết. Sau đó, chọn **Add** (với các phiên bản phải trả phí, chọn **Try** để dùng thử, chọn **Buy** để thanh toán tiền mua).
#### Bước 4. Cần đăng nhập (sign in) bằng tài khoản Office 365 và chọn **Continue** để có thể sử dụng.
#### Bước 5. Mở dải lệnh **Data Mining** mới xuất hiện để xem kết quả.

# Bài 1: MÔ PHỎNG ĐƯỢC SỬ DỤNG TRONG NHIỀU LĨNH VỰC

Học xong bài này, em sẽ:
*   Nêu được một số lĩnh vực trong đời sống có sử dụng kĩ thuật mô phỏng.
*   Nêu được một số vấn đề thực tế mà ở đó có thể cần dùng kĩ thuật mô phỏng để giải quyết.
*   Sử dụng được phần mềm Mô phỏng 3D Hệ Mặt Trời (Solar System 3D Simulator).

Theo em, vì sao mô phỏng được dùng trong nhiều lĩnh vực?
Gợi ý: Em có thể giải thích bằng ví dụ minh họa.

## Mô phỏng và phần mềm mô phỏng

Kĩ thuật mô phỏng (thường được gọi ngắn gọn là **mô phỏng**) là kĩ thuật tái tạo, bắt chước hoạt động của một quá trình hoặc hệ thống, thể hiện hoạt động của nó theo thời gian. Mục tiêu thực hiện mô phỏng là để hiểu rõ hơn về một hiện tượng hoặc một hệ thống cụ thể. Vì vậy, mô phỏng được sử dụng trong các điều kiện thử nghiệm nhằm phục vụ nghiên cứu hoặc giảng dạy. Hệ thống được mô phỏng có thể là: hệ thống tự nhiên trong vật lí, hoá học, sinh học,...; hệ thống khoa học xã hội; hệ thống do con người xây dựng;...

Để khảo sát, nghiên cứu một hiện tượng hay một hệ thống, con người mô hình hoá hệ thống đó bằng cách sử dụng các mô hình như: biểu đồ, công thức toán học hay các hình thức khác. Mô hình làm nổi bật những yếu tố quan trọng của hệ thống và mối quan hệ giữa chúng. Trong phạm vi môn Tin học, ta sẽ chỉ đề cập tới việc sử dụng các công cụ tin học (bao gồm cả phần cứng và phần mềm) để tạo ra các mô hình mô phỏng dưới dạng các phần mềm mô phỏng.

Có những phần mềm mô phỏng không yêu cầu cung cấp dữ liệu đầu vào. Ví dụ: Phần mềm Solar System 3D Simulator, mô phỏng chuyển động của các hành tinh trong Hệ Mặt Trời. Có những phần mềm mô phỏng cần được cung cấp dữ liệu đầu vào, các điều kiện khởi đầu của hệ thống. Thực hiện phần mềm mô phỏng với các tham số đầu vào khác nhau sẽ cho ta thử nghiệm các tình huống và kịch bản khác nhau. Ví dụ: phần mềm mô phỏng hoạt động của con lắc lò xo (trang https://phet.colorado.edu) cho ta thay đổi dữ liệu đầu vào (chẳng hạn, khối lượng vật treo) để quan sát sự thay đổi tương ứng trong chuyển động của con lắc đó.

Những năm gần đây, công nghệ **thực tế ảo – Virtual Reality (VR)** đang ngày một phát triển mạnh mẽ. Công nghệ thực tế ảo mô tả một môi trường được mô phỏng bằng phần mềm chuyên dụng. Khi sử dụng kính 3D, ta sẽ nhìn thấy một không gian như thật, tương tác với môi trường này như với không gian thật.

Những mô phỏng khác nhau có độ chính xác khác nhau, nói cách khác đó là độ giống với quá trình hay hệ thống trong đời thực, nguyên gốc của sự mô tả. Tuỳ theo trường hợp cụ thể và mục tiêu mô phỏng mà một độ chính xác nào đó được chấp nhận. Nói chung, người làm mô phỏng muốn người dùng có cảm giác hệ thống ảo càng giống với hệ thống thực càng tốt.

## Phần mềm mô phỏng trong một số lĩnh vực

Hãy kể một số phần mềm mô phỏng mà em đã từng sử dụng trong học tập cùng với kiến thức hay kĩ năng mà em thu nhận được từ đó.

### a) Phần mềm mô phỏng trong lĩnh vực giáo dục và đào tạo

Thực hiện thí nghiệm là điều không thể thiếu được trong giáo dục và đào tạo. Có thể dùng phần mềm mô phỏng để làm thí nghiệm ảo thay cho thực hiện thí nghiệm thật. Ví dụ: Những thí nghiệm ảo ở trang web PhET Interactive Simulations (https://phet.colorado.edu) thay thế được cho nhiều thí nghiệm thật ở các môn Toán, Vật lí, Hoá học, Khoa học Trái đất và Sinh học.

Trang web Labster (https://labster.com) cung cấp môi trường thực tế ảo để người học có thể thực hiện các thí nghiệm về Vật lí, Hoá học và Sinh học mà không cần đến phòng thí nghiệm thực tế. Thí nghiệm ảo đã được dùng nhiều trong những trường hợp thiết bị thí nghiệm thật đòi hỏi chi phí cao hoặc có nguy cơ gây hại cho người làm thí nghiệm. Dùng phần mềm mô phỏng làm thí nghiệm giúp giảm chi phí, an toàn mà người học vẫn tiếp nhận bài học một cách hiệu quả. Đặc biệt, người học có thể mắc lỗi khi thực hiện thí nghiệm nhưng không phải gánh chịu hậu quả nghiêm trọng như khi làm thí nghiệm thực tế. Ví dụ: Thí nghiệm về hiện tượng chập mạch điện, nếu làm thí nghiệm trên hệ thống thật có thể gây cháy nổ, hoả hoạn rất nghiêm trọng, thí nghiệm ảo sẽ giúp tránh được điều đó.

Có những phần mềm mô phỏng dưới dạng trò chơi, giúp người chơi học được những kiến thức về Lịch sử, Địa lí. Chẳng hạn, Sphinx là một trò chơi mô phỏng trực tuyến giúp người chơi tìm hiểu văn hoá và lịch sử Ai Cập cổ đại. Một ví dụ khác, phần mềm Microsoft Flight Simulator cho người chơi khám phá một bản đồ số hoá của thế giới với cảnh quan và địa hình được mô tả tinh xảo.

### b) Phần mềm mô phỏng trong lĩnh vực y tế

Nhiều phần mềm mô phỏng được sử dụng rộng rãi trong lĩnh vực y tế. Có loại mô phỏng giúp bác sĩ luyện tập các kĩ năng trong môi trường ảo an toàn và được kiểm soát. Có loại được sử dụng để giả lập các kịch bản điều trị và hướng dẫn bệnh nhân sử dụng thuốc, thiết bị y tế hoặc thực hiện các công việc tự chăm sóc. Phần mềm mô phỏng không chỉ được sử dụng để đào tạo nhân viên y tế hay hướng dẫn bệnh nhân mà còn được dùng để hỗ trợ nghiên cứu và phát triển sản phẩm y tế. Ví dụ: Phần mềm SimSurgery mô phỏng chính xác các cơ quan nội tạng người, được dùng để huấn luyện phẫu thuật nội soi; phần mềm ANSYS Medical Simulation mô hình hoá quá trình sinh học, mô tả tương tác giữa cơ thể người với thiết bị y tế, được dùng để nghiên cứu và phát triển các sản phẩm y tế;...

### c) Phần mềm mô phỏng trong lĩnh vực quân sự

Phần mềm mô phỏng là một công cụ hữu ích phục vụ đào tạo trong lĩnh vực quân sự. Các phần mềm mô phỏng tạo ra môi trường ảo huấn luyện binh sĩ trong nhiều tình huống khác nhau như huấn luyện sử dụng vũ khí, huấn luyện lái máy bay, lái ô tô (Hình 3),... Có những phần mềm giúp mô phỏng vũ khí và kĩ thuật quân sự, chúng được dùng để kiểm tra hiệu quả và tính năng của các loại vũ khí, hệ thống ra-đa, hệ thống liên lạc hay các công nghệ quân sự khác. Để phân tích, đánh giá các tình huống, các chiến lược quân sự khác nhau, phần mềm mô phỏng cũng có thể được sử dụng để tìm phương án tối ưu.

### d) Phần mềm mô phỏng trong lĩnh vực sản xuất

Trong sản xuất, các phần mềm mô phỏng đem lại nhiều lợi ích quan trọng như: tối ưu hoá quy trình sản xuất, giúp thiết kế sản phẩm, đào tạo nhân viên,... Việc thử nghiệm bằng mô phỏng cho ta kết quả nhanh hơn so với thử nghiệm trên hệ thống thực, đây là một trong những lợi ích lớn mà mô phỏng đem lại. Chẳng hạn, phần mềm **SolidWorks** mô phỏng kĩ thuật cơ học, được sử dụng rộng rãi để đánh giá các thiết kế sản phẩm, cải thiện chất lượng và tính năng sản phẩm trước khi sản xuất hàng loạt. Để đào tạo người sản xuất, nhiều phần mềm mô phỏng đã được sử dụng để giúp họ làm quen với các thiết bị và quy trình làm việc. Ví dụ: Có thể sử dụng phần mềm mô phỏng **Simufact Welding** để đào tạo nhân viên về quy trình hàn kim loại.

### e) Phần mềm mô phỏng trong lĩnh vực giải trí

Theo em, các phần mềm trò chơi có sử dụng kĩ thuật mô phỏng hay không? Giải thích ý kiến của em.

Mô phỏng trong giải trí xuất hiện ở nhiều ngành công nghiệp lớn và phổ biến như: phim ảnh, truyền hình, trò chơi điện tử và một số trò chơi trong công viên giải trí.
Trò chơi mô phỏng đầu tiên được tạo ra vào năm 1947, chỉ đơn giản là mô phỏng một tên lửa bắn vào mục tiêu. Đường cong và tốc độ của tên lửa có thể được điều chỉnh bằng một số nút bấm. Ngày nay, hàng triệu người trên khắp thế giới chơi các trò chơi mô phỏng trên máy tính như **World of Warcraft**.
Năm 1993, bộ phim **Công viên kỉ Jura** là bộ phim nổi tiếng đầu tiên sử dụng đồ hoạ do máy tính tạo ra và tích hợp những con khủng long mô phỏng gần như hài hoà vào các cảnh hành động trực tiếp. Sự kiện này đã làm thay đổi ngành công nghiệp điện ảnh. Kĩ thuật mô phỏng đã dần đến sự ra đời của kĩ xảo điện ảnh vào đầu những năm 2000, kết quả là sự ra đời những bộ phim bom tấn với các cảnh phim mà những máy quay vật lí không thể đạt được như vậy. Ví dụ kinh điển là những hình ảnh trong các bộ phim như: Ma trận, Chúa tể của những chiếc nhẫn, Avatar,... được tạo ra từ kĩ xảo điện ảnh nhờ mô phỏng bằng máy tính.

## Thực hành sử dụng phần mềm mô phỏng 3D Hệ Mặt Trời (Solar System 3D Simulator)

### Yêu cầu:

Phần mềm mô phỏng Solar System 3D Simulator giúp người dùng quan sát các hành tinh trong Hệ Mặt Trời và khám phá thêm thông tin về Hệ Mặt Trời.

Em hãy tìm hiểu phần mềm Solar System 3D Simulator để trả lời cho các câu hỏi và yêu cầu sau:

1.  Hệ Mặt Trời gồm bao nhiêu hành tinh và đó là những hành tinh nào (tên tiếng Anh và tên tiếng Việt)?
2.  Hãy chọn ba hành tinh và cho biết một số thông tin về mỗi hành tinh đó (đường kính, quỹ đạo, thời gian quay một vòng quỹ đạo, vận tốc trung bình, thời gian một ngày của hành tinh, khối lượng, nhiệt độ).
3.  Hành tinh nào gần Mặt Trời nhất? Hành tinh nào xa Mặt Trời nhất?
4.  Quỹ đạo của hành tinh nào dài nhất?
5.  Hành tinh nào có nhiều vệ tinh quay xung quanh nhất?
6.  Hãy dùng phần mềm để giải thích hiện tượng nguyệt thực.
7.  Hãy dùng phần mềm để giải thích hiện tượng nhật thực.
8.  Làm thế nào để xác định một vùng trên Trái Đất đang là ban ngày hay ban đêm?
9.  Theo em, phần mềm mô phỏng này đem lại lợi ích gì và có thể dùng trong những lĩnh vực nào?

### Hướng dẫn thực hiện:

Bước 1. Kích hoạt biểu tượng phần mềm Solar System 3D Simulator. Nếu chưa có phần mềm này trên máy tính thì cần tải từ trên Internet xuống và cài đặt (đây là phần mềm miễn phí).

Bước 2. Khám phá bảng điều khiển.

## Bảng điều khiển
*   Dịch chuyển khung nhìn
*   Nâng lên/ hạ xuống vị trí quan sát
*   Phóng to/ thu nhỏ khung nhìn
*   Hiện/ ẩn quỹ đạo
*   Đặt lại vị trí mặc định
*   Thay đổi tốc độ quay
*   Thay đổi vị trí quan sát
*   Hiện thông tin chi tiết về các hành tinh

## Luyện tập
Em hãy chọn thực hiện một mô phỏng thuộc chủ đề hoá học trong trang web https://phet.colorado.edu/vi/ và cho biết mục đích của mô phỏng đó.

Câu 1. Giải thích sơ lược vì sao mô phỏng được sử dụng trong nhiều lĩnh vực.
Câu 2. Em hãy lấy ví dụ kèm theo lập luận để minh hoạ cho các phát biểu sau:
a) Trong lĩnh vực sản xuất, sử dụng phần mềm mô phỏng có thể tiết kiệm được chi phí và thời gian.
b) Trong lĩnh vực y tế và quân sự, sử dụng phần mềm mô phỏng có thể tránh được những rủi ro.

## Tóm tắt bài học
*   Mô phỏng bằng máy tính là dùng công cụ phần cứng và phần mềm để tái tạo, biểu diễn hoặc bắt chước một hiện tượng, một quá trình hay một hệ thống.
*   Mô phỏng được sử dụng trong nhiều lĩnh vực như: giáo dục và đào tạo, y tế, sản xuất, quân sự, giải trí.
*   Một số lợi ích chính mà việc sử dụng phần mềm mô phỏng có thể đem lại là: hiệu quả về chi phí, hiệu quả về thời gian thử nghiệm một hệ thống, giảm thiểu rủi ro, quan sát được hệ thống trong các điều kiện khác nhau.
