# Bài 4: SỐ HOÁ HÌNH ẢNH VÀ SỐ HOÁ ÂM THANH

## Học xong bài này, em sẽ:
* Giải thích được sơ lược cách số hoá hình ảnh.
* Giải thích được sơ lược cách số hoá âm thanh.

Em hãy tìm trên Internet các hình minh hoạ ảnh độ phân giải thấp bằng cách sử dụng từ khoá tìm kiếm _low resolution images_, rồi đoán xem điều gì xảy ra nếu mở xem một hình ảnh và cứ phóng to lên mãi.

## 1. Số hoá hình ảnh
### a) Rời rạc hoá hình ảnh và các điểm ảnh
Người ta dùng lưới ô vuông để chia một hình ảnh thành nhiều ô vuông rất nhỏ, mỗi ô vuông gọi là một phần tử ảnh. Hình ảnh gồm nhiều phần tử ảnh là các ô vuông rất nhỏ, xếp lần lượt từ trái sang phải, từ trên xuống dưới. Có thể coi một phần tử ảnh là một ô vuông đồng màu duy nhất, thuật ngữ tin học là **pixel**, cũng là **điểm ảnh** theo cách nói thông dụng hằng ngày.

#### Điểm ảnh và độ phân giải
Một bức ảnh kĩ thuật số có thể được tạo nên từ hàng triệu **điểm ảnh**. Độ phân giải điểm ảnh thể hiện bằng cặp hai số đếm điểm ảnh theo chiều ngang và theo chiều cao. Tích hai số này là tổng số điểm ảnh làm nên hình ảnh. Cùng một kích thước, số điểm ảnh càng cao thì ảnh càng mịn, số điểm ảnh càng thấp thì ảnh càng thô. Tương ứng, ta nói ảnh có độ phân giải cao hay độ phân giải thấp. Khi phóng to ảnh quá mức so với kích thước ban đầu của nó, nhất là ảnh có độ phân giải thấp, có thể xảy ra hiện tượng “vỡ” ảnh. Ta nhìn thấy rõ rệt các ô vuông nhỏ, màu sắc hơi khác nhau.

Mở thư mục và trỏ chuột vào một tệp ảnh, sẽ thấy hiển thị thông tin về kích thước của nó theo số điểm ảnh, tính theo chiều ngang và chiều cao ảnh. Ví dụ, một ảnh chụp toàn bộ màn hình máy tính bằng phím in màn hình (**Print Screen**) có thông tin kích thước “Dimensions: 1920 × 1080; size 723 KB”, nghĩa là ảnh có 2 073 600 điểm ảnh.

### b) Hệ màu và rời rạc hoá màu
#### Hệ màu RGB
Kiến thức vật lí cho biết rằng ba màu cơ sở: đỏ, xanh lục, xanh lam trộn chung với nhau theo những tỉ lệ khác nhau sẽ tạo ra đủ các màu sắc. Hệ màu **RGB**, R là Red (màu đỏ), G là Green (màu xanh lục), B là Blue (màu xanh lam) dựa trên nguyên lí này.

Hệ màu RGB dành một byte để thể hiện cường độ của mỗi màu trong tổ hợp. Như vậy giá trị cường độ của mỗi màu biến thiên từ 0 đến 255. Một bộ ba byte sẽ thể hiện một cách tổ hợp ba màu cơ sở để nhận được một màu sắc cụ thể. Hệ màu RGB có số lượng màu là $2^8 \times 2^8 \times 2^8 = 2^{24} = 16\ 777\ 216$.

#### Rời rạc hoá màu:
cho tương ứng mỗi màu với một dãy bit nhất định gọi là mã nhị phân của màu. màu khác nhau thì mã nhị phân khác nhau.

#### Độ sâu màu:
độ dài dãy bit để rời rạc hoá màu.

Em hãy khám phá những màu sắc có thể dùng trong một văn bản được tạo ra bởi một phần mềm soạn thảo văn bản và trả lời các câu hỏi sau:
1) Bảng **Theme Colors** hay hộp thoại **Colors** (xuất hiện khi chọn **More Colors**) hiển thị nhiều màu hơn cho người dùng chọn?
2) Mã màu RGB của một màu em đã chọn được tìm như thế nào?

### c) Số hoá hình ảnh
Theo định nghĩa, mỗi điểm ảnh có diện tích rất nhỏ. Do đó, có thể coi mỗi điểm ảnh là một ô vuông đồng màu (một màu đồng nhất). Sau khi rời rạc hoá hình ảnh, sắp xếp mã nhị phân màu của các điểm ảnh nối tiếp nhau từ trái sang phải, từ trên xuống dưới, ta sẽ nhận được dãy bit biểu diễn ảnh số.

## 2) Số hoá âm thanh
### a) Tín hiệu âm thanh
Quan sát Hình 2 và cho biết hình đó muốn minh hoạ điều gì.

Tai người nghe được âm thanh là do sóng âm truyền qua môi trường làm rung màng nhĩ. Đồ thị biểu diễn của sóng âm có dạng một đường cong liên tục, lên xuống nhấp nhô. Đồ thị này là dữ liệu dạng tương tự (analog) mang thông tin âm thanh.

### b) Lấy mẫu tín hiệu âm thanh theo thời gian

Các điểm ảnh biến đổi về màu sắc trên mặt phẳng hai chiều. Một đoạn âm thanh biến đổi cao độ (trầm hay bổng), cường độ (mạnh hoặc yếu) theo thời gian. Đồ thị liên tục dạng hình sóng thể hiện những biến đổi này theo thời gian.

Người ta rời rạc hoá đồ thị liên tục dạng hình sóng thành nhiều mẫu (đoạn) rất ngắn nối tiếp nhau theo trục thời gian (trục hoành). Vì mỗi mẫu rất ngắn nên có thể coi là có biên độ không đổi, tức là một đoạn thẳng nằm ngang trên đồ thị minh hoạ. Các vạch nằm ngang xấp xỉ đường hình sin. Việc lấy mẫu được thực hiện theo những khoảng thời gian cách đều. Số mẫu lấy được trong một giây gọi là **tốc độ lấy mẫu**, đo bằng hertz hoặc số mẫu/giây. Giá trị biên độ tại thời điểm lấy mẫu áp dụng cho cả khoảng thời gian.

### c) Lượng tử hoá

Quá trình chuyển đổi giá trị mẫu liên tục thành các giá trị rời rạc được gọi là **lượng tử hoá**. Có nhiều kĩ thuật lượng tử hoá, trong đó có thể là chia giải biên độ tín hiệu thành khoảng cố định bằng nhau và được gán một con số được gọi là **số hiệu khoảng**. Mỗi mẫu âm thanh thu được ở bước trên sẽ thuộc một trong những khoảng biên độ này và nó được gán số hiệu khoảng.

### d) Biểu diễn nhị phân

Biểu diễn số hiệu khoảng thành số nhị phân, xếp các dãy bit liên tục theo thời gian, ta sẽ nhận được dãy bit là dữ liệu âm thanh số.

## Luyện tập
Bài 1. Ảnh số là một dãy bit rất dài trong máy tính. Hãy cho biết sẽ nhận được hình ảnh như thế nào nếu:
1) Cắt đi đúng một nửa cuối dãy, chỉ giữ lại nửa đầu dãy.
2) Nối thêm một bản sao của dãy bit vào cuối thành dãy bit dài gấp đôi.

Bài 2. Đơn vị đo tốc độ lấy mẫu để rời rạc hoá tín hiệu âm thanh theo thời gian là gì? Tại sao có thể coi biên độ tín hiệu âm thanh không đổi trong một mẫu?

Em hãy cho biết hình ảnh HD (high definition) có liên quan gì đến lưới chia để rời rạc hoá hình ảnh và độ dài dãy bit để rời rạc hoá màu.

Câu 1. Làm thế nào để chia hình ảnh thành nhiều điểm ảnh? Tại sao có thể coi một điểm ảnh hình vuông là đồng màu?

Câu 2. Trong hệ màu RGB, một điểm ảnh dài bao nhiêu bit? Tỉ lệ trộn ba màu cơ sở thể hiện bằng cách nào?

Câu 3. Rời rạc hoá biên độ tín hiệu âm thanh là gì?

## Tóm tắt bài học
*   Số hoá hình ảnh bằng cách chia thành nhiều ô vuông rất nhỏ và cho tương ứng mỗi ô với mã nhị phân của màu trong ô đó.
*   Số hoá tín hiệu âm thanh bằng cách chia thành nhiều mẫu thời gian rất ngắn và cho tương ứng mỗi mẫu với dãy bit biểu diễn biên độ.

## BÀI TÌM HIỂU THÊM
### HỆ MÀU
Hệ màu được tạo ra để số hoá các màu sắc, cho tương ứng mỗi màu với một mẫu bit (bit pattern). Hệ màu **RGB** định nghĩa mã màu RGB.

# Bài 1: TẠO VĂN BẢN TÔ MÀU VÀ GHÉP ẢNH

## Học xong bài này, em sẽ:
*   Bước đầu quen được với một số thành phần chính trong màn hình làm việc của GIMP.
*   Tạo được tệp ảnh mới, lưu được tệp ảnh và xuất tệp ảnh với định dạng chuẩn.
*   Bước đầu nhận diện được các lớp ảnh, chọn và đổi được tên lớp ảnh.
*   Bước đầu sử dụng được các công cụ: tạo văn bản, tô màu, ghép ảnh đơn giản để tạo được các sản phẩm đồ hoạ như thiệp chúc mừng, thiệp mời, bưu thiếp.

Em đã bao giờ dùng phần mềm để tạo ra những sản phẩm như thiệp chúc mừng, bưu thiếp hay một áp phích (poster) chưa? Em hãy giới thiệu sơ lược về một phần mềm như vậy.

## 1. Phần mềm thiết kế đồ hoạ và GIMP

Theo em, để tạo được các bưu thiếp đẹp bằng một phần mềm thì phần mềm đó cần cung cấp những khả năng gì?

### a) Sản phẩm đồ hoạ và phần mềm thiết kế đồ hoạ

Phần mềm thiết kế đồ hoạ là phần mềm cung cấp các công cụ giúp tạo ra sản phẩm đồ hoạ như: logo, banner, topic quảng cáo, băng rôn, áp phích, poster và thiệp chúc mừng.

### b) Giới thiệu phần mềm GIMP

Một phần mềm thiết kế, chỉnh sửa đồ hoạ sẽ hỗ trợ tạo ra sản phẩm số dựa trên đồ hoạ vector hay đồ hoạ raster.

Đồ họa vector sử dụng các tọa độ trong mặt phẳng và mối quan hệ vector để tạo ra các đường giữa chúng với các thuộc tính như màu nét, hình dạng, độ dày để biểu diễn hình ảnh. Ảnh được tạo theo cách này được gọi là **ảnh vector**. Đồ họa raster sử dụng ma trận các điểm ảnh với màu sắc và sắc thái khác nhau để biểu diễn hình ảnh. Ảnh được tạo theo cách này được gọi là **ảnh raster** (hay **ảnh bitmap**).

GIMP (viết tắt của "GNU Image Manipulation Program" – phần mềm xử lí ảnh) là phần mềm mã nguồn mở, miễn phí, trợ giúp một cách hiệu quả cả hai công việc chỉnh sửa ảnh và thiết kế đồ họa dựa trên đồ họa raster. Hơn nữa, mặc dù GIMP xử lí đồ họa raster nhưng cũng hỗ trợ đồ họa vector. Do vậy có thể khai thác GIMP cho các chủ đề về chỉnh sửa ảnh, làm video, phim hoạt hình,... Có thể tải phần mềm GIMP từ trang https://gimp.org phiên bản GIMP được sử dụng trong sách giáo khoa là 2.10.x.

### c) Màn hình làm việc của GIMP

Màn hình làm việc của một phần mềm thiết kế đồ họa thường có các thành phần như giao diện của GIMP. Sau đây là một số thành phần chính:
*   Hệ thống bảng chọn chứa các lệnh của phần mềm.
*   **Hộp công cụ** (Toolbox) chứa các công cụ thiết kế và chỉnh sửa như: tạo văn bản, chọn, cắt, xoá, vẽ, tô màu và biến đổi hình. Các thuộc tính của công cụ được chọn ở bảng tuỳ chọn.
*   Các bảng quản lí lớp ảnh, kênh màu và đường dẫn chứa các lệnh làm việc với các lớp ảnh (thường gọi tắt là lớp), các kênh màu và các đường dẫn.

## Tạo tệp ảnh mới

Chọn File\New, GIMP đưa ra hộp thoại hỏi về các tham số để tạo tệp ảnh mới.

Đơn vị đo kích thước và độ phân giải ảnh được chọn tuỳ theo đặc điểm của sản phẩm đồ hoạ cần tạo và cách chọn đơn vị thông dụng của người thiết kế.

Ví dụ: Thiệp chúc mừng sinh nhật có thể được tạo trên tệp ảnh mới với kích thước 15 × 8 (cm), không gian màu là **RGB**. Tệp ảnh mới sẽ có “ảnh trống” trong cửa sổ ảnh. Lớp ảnh nền có tên mặc định là **Background** được hiển thị trong bảng quản lí lớp ảnh.

## Tô màu

Khi thực hiện công việc “tô màu”, đối tượng được tô hay phủ màu có thể là **hậu cảnh** (nền ảnh) hoặc **tiền cảnh** (văn bản, hình vẽ, vùng chọn trên ảnh).
Để thay đổi màu tiền cảnh (hoặc hậu cảnh), nháy chuột vào biểu tượng FG hoặc BG rồi chọn màu trong hộp thoại chọn màu xuất hiện ngay sau đó.

Có hai cách tô màu: tô màu thuần nhất và tô màu gradient.
Tô màu thuần nhất là phủ một màu duy nhất lên bề mặt đối tượng. Để tô màu, nháy chuột vào công cụ **Bucket Fill** chọn thuộc tính cho công cụ (chẳng hạn, chọn màu tô mặc định là màu FG) rồi nháy chuột vào một vị trí nào đó trên đối tượng cần tô màu. minh hoạ kết quả tô màu mặc định cho lớp nền ảnh.

Tô màu **gradient** là phủ lên bề mặt đối tượng một dải màu chuyển dần từ màu thứ nhất sang màu thứ hai. Để tô màu, nháy chuột vào công cụ **Gradient**, sau đó chọn các thuộc tính của công cụ rồi kéo thả chuột để xác định một đoạn thẳng (gọi là đường cơ sở) tại vị trí nào đó bên cạnh hoặc bên trên đối tượng cần tô màu. Dải màu gradient thể hiện quá trình chuyển dần từ màu FG (xanh dương) sang BG (trắng).

## 4) Tạo văn bản

Văn bản được tạo bằng công cụ **Text** với các thuộc tính định dạng. Để tạo một đoạn văn bản, nháy chuột vào công cụ **Text**, chọn các thuộc tính định dạng rồi nháy chuột vào vị trí cần chèn văn bản trong cửa sổ ảnh để nhập văn bản. Để kết thúc, nháy chuột vào công cụ khác (thường là công cụ di chuyển **Move**). Khi tạo xong, một lớp mới được tự động tạo ra để chứa văn bản. Tên lớp trùng với phần đầu nội dung văn bản.

*   Chọn kiểu chữ
*   Chọn cỡ chữ
*   Chọn màu chữ
*   Chọn kiểu căn biên
*   Chọn độ giãn dòng
*   Chọn độ giãn chữ
*   Nhập văn bản: Chúc mừng sinh nhật Trung Anh

Khi công cụ **Text** không được chọn, văn bản được xem như một đối tượng đồ họa và lớp văn bản cũng là một lớp ảnh.

## Mở tệp ảnh và ghép ảnh

Ảnh nguồn để ghép thường được xử lí trước khi ghép bằng các phép biến đổi ảnh. Em hãy tìm hiểu và cho biết các cách biến đổi ảnh như: thay đổi kích thước, xoay, lật và biến dạng ảnh.

Có thể mở một hoặc nhiều tệp ảnh trong GIMP bằng lệnh **File\Open**, nhưng tại một thời điểm, cửa sổ ảnh chỉ hiển thị ảnh của một tệp. Danh sách các biểu tượng tệp ảnh đang mở nằm ở phía trên của sổ ảnh. Nếu muốn đóng một tệp ảnh, nháy dấu X ở bên phải biểu tượng tệp ảnh.

Có thể ghép một phần hoặc toàn bộ ảnh nguồn vào trong ảnh đích bằng cách:
* Chọn ảnh nguồn và thực hiện các xử lí cần thiết (biến đổi ảnh).
* Sao chép ảnh nguồn vào ảnh đích điều chỉnh kích thước và vị trí ảnh mới ghép vào cho phù hợp.

Em hãy thực hiện ghép ảnh để thiết kế một thiệp chúc mừng sinh nhật.

### Hướng dẫn thực hiện:

*   **Bước 1.** Chọn ảnh nguồn từ một tệp ảnh đã mở và thực hiện các xử lí cần thiết.
    Có thể dùng công cụ **Crop** để cắt, phần cần lấy ở ảnh nguồn, sau đó chọn lớp ảnh nguồn rồi thực hiện lệnh **Edit\Copy**.

*   **Bước 2.** Sao chép ảnh nguồn thành một lớp mới của ảnh đích và thực hiện các điều chỉnh cần thiết cho lớp ảnh mới.
    *   Chọn tệp ảnh đích, chọn một lớp ảnh ví dụ lớp **Background**, thực hiện lệnh **Edit\Paste**. Một lớp động được tự động tạo ra ở phía trên lớp đã chọn để chứa ảnh được sao chép và có tên tạm thời là **Floating Selection**.

* Nháy chuột vào nút lệnh New Layer để tạo lớp mới. Tên lớp mới mặc định là tên tệp ảnh nguồn. Nên đổi lại tên lớp mới này bằng cách nháy đúp chuột vào tên lớp rồi gõ tên mới.
* Ảnh mới được ghép thường có kích thước và vị trí không phù hợp. Dùng công cụ **Scale** để thay đổi kích thước ảnh và công cụ **Move** để di chuyển ảnh đến vị trí phù hợp.

Em hãy tạo một thiệp chúc mừng sinh nhật bạn hoặc người thân. Lưu sản phẩm với tên tệp là “Chúc mừng sinh nhật.cxf” và xuất sang định dạng JPG bằng cách thực hiện lệnh **File\Export As**.

## Luyện tập

Em đồng ý với những phát biểu nào sau đây?
Trong phần mềm thiết kế đồ hoạ, ví dụ như phần mềm GIMP:
* 1) Có bảng các công cụ thiết kế đồ hoạ như: tạo văn bản, tô màu, biến đổi hình.
* 2) Có thể tô nền bằng một màu duy nhất hoặc tô bằng hai màu chuyển dần cho nhau.
* 3) Văn bản được tạo cũng có các thuộc tính định dạng cơ bản như: kiểu chữ, cỡ chữ, màu sắc.
* 4) Không thể mở nhiều tệp ảnh để lựa chọn và sao chép sang tệp ảnh đích.

## Tóm tắt bài học

* Màn hình làm việc của một **phần mềm thiết kế đồ hoạ** thường có các thành phần chính là: hệ thống bảng chọn, hộp công cụ, các bảng tuỳ chọn và các bảng (quản lí lớp, kênh màu và đường dẫn).
* Có thể chỉnh sửa ảnh có sẵn, có thể ghép vào ảnh khác tạo thành sản phẩm đồ hoạ mới. Phần mềm thiết kế đồ hoạ cung cấp các công cụ tạo văn bản, tô màu và biến đổi hình.

**CHỦ ĐỀ E (ICT): Ứng dụng Tin học – ICT: Phần mềm thiết kế đồ họa**

# Bài 2: MỘT SỐ KĨ THUẬT THIẾT KẾ SỬ DỤNG VÙNG CHỌN, ĐƯỜNG DẪN VÀ CÁC LỚP ẢNH

Học xong bài này, em sẽ:
*   Thực hiện được các thao tác cơ bản đối với lớp, vùng chọn và đường dẫn.
*   Biết và thực hiện được một số kĩ thuật thiết kế dựa trên lớp, vùng chọn và đường dẫn.

Khi thiết kế một sản phẩm đồ họa có nên đưa tất cả các đối tượng vào cùng một lớp ảnh không? Tại sao?

## 1. Khám phá các lớp ảnh

Trong logo "Cờ cổ động", một bạn vô tình thay đổi thứ tự một lớp ảnh của logo làm lá cờ trên logo bị biến mất. Thứ tự mới của các lớp ảnh như. Em hãy đoán xem bạn đó thay đổi thứ tự lớp ảnh nào. Thứ tự ban đầu của nó là gì?

Khi thiết kế một đối tượng đồ họa mới, ví dụ như lá cờ, ngôi sao, cán cờ, chúng mặc định được tạo trên lớp đang chọn. Cùng với lớp, chúng tạo thành một đối tượng hợp nhất nên khó chỉnh sửa từng đối tượng. Do đó, mỗi đối tượng nên được tạo trên một lớp riêng. Ví dụ, nếu lá cờ và ngôi sao cùng được tạo trong một lớp ảnh thì chúng tạo thành một đối tượng duy nhất, không thuận lợi cho việc chỉnh sửa riêng lá cờ hay ngôi sao. GIMP cung cấp các lệnh làm việc với lớp như: thêm, xoá, nhân đôi lớp, ẩn hoặc hiện và thay đổi thứ tự các lớp.

* Thêm một lớp mới bên trên lớp được chọn
* Di chuyển lớp đang chọn lên trên hoặc xuống dưới
* Nhân đôi lớp được chọn
* Xoá lớp được chọn

## Một số kĩ thuật thiết kế làm việc với các lớp ảnh

### a) Thiết kế trên lớp bản sao
Nhiều khi cần thực hiện lệnh nhân đôi lớp vì lớp bản sao được sử dụng trong nhiều trường hợp khác nhau. Ví dụ, ở Hình 3a, đường viền màu trắng trên dải nơ của hộp quà được tạo trên lớp riêng, việc nhân đôi nó nhiều lần rồi di chuyển các lớp mới đến vị trí phù hợp sẽ nhận được kết quả như Hình 3b. Đôi khi, bản sao của đối tượng được chỉnh sửa lại để kết hợp với đối tượng ban đầu. Ví dụ, sau khi nhân đôi lớp văn bản màu đen (Hình 3c), lớp bản sao được tô lại thành màu xám rồi di chuyển sang phải và xuống dưới văn bản màu đen sẽ nhận được kết quả như Hình 3d.

### b) Hướng tập trung vào một lớp
Bên trái tên lớp có biểu tượng hình con mắt. Nháy chuột vào đó sẽ tắt (hoặc bật) con mắt để ẩn (hoặc hiện) lớp. Ví dụ, sau khi nhân đôi lớp văn bản chữ màu đen, lớp bản sao sẽ trùng khít với lớp cũ, không thể phân biệt được lớp mới và lớp cũ. Do vậy phải tạm ẩn lớp ban đầu trước khi tô màu xám cho lớp bản sao (Hình 4).

### c) Sắp xếp lại các lớp

Việc thay đổi thứ tự các lớp sẽ tạo ra sự thay đổi của ảnh hợp thành của chúng ở cửa sổ ảnh. Chẳng hạn, sau khi nhân đôi một lớp, lớp bản sao mặc định được tạo ở bên trên nó. Sau khi tô màu xám cho lớp bản sao để thể hiện bóng (**shadow**) của văn bản, kết quả không hợp lí vì đáng lẽ phần bóng phải chìm dưới văn bản. Do vậy chuyển lớp bản sao xuống dưới lớp gốc thì kết quả nhận được sẽ hợp lí hơn.

## 3 Sử dụng vùng chọn

### a) Vùng chọn và các công cụ tạo vùng chọn

**Vùng chọn** giúp xử lí riêng biệt một vùng nào đó trên ảnh, ví dụ như: tô màu, vẽ hình. Hai công cụ phổ biến để tạo vùng chọn hình chữ nhật và hình elip tương ứng là **Rectangle Select** và **Ellipse Select**. Để tạo một vùng chọn, nháy chuột vào công cụ tạo vùng chọn, chọn các thuộc tính của công cụ rồi kéo thả chuột để xác định vùng chọn trên ảnh. Nếu giữ kèm phím **Shift** trong thao tác kéo thả chuột thì vùng chọn sẽ là hình vuông hoặc hình tròn. Nếu giữ kèm thêm phím **Ctrl** thì vùng chọn sẽ nhận tâm là điểm đầu tiên nhấn chuột trong thao tác kéo thả chuột.

### b) Một số thao tác cơ bản với vùng chọn

*   Đảo ngược vùng chọn bằng lệnh **Select\Invert**. Khi đó một vùng chọn mới thay thế vùng chọn cũ, chứa tất cả các đối tượng ngoại trừ đối tượng thuộc vùng chọn cũ.
*   Co hoặc giãn vùng chọn bằng lệnh **Shrink** hoặc **Grow** trong bảng chọn **Edit**. Đơn vị co hoặc giãn là số pixel được xác định trong hộp thoại xuất hiện sau đó.

* Xoá vùng chọn bằng cách nhấn phím **Delete**. Ảnh trong vùng chọn bị xoá nhưng vùng chọn vẫn đang hoạt động.
* Bỏ vùng chọn bằng lệnh **Select\None**. Khi đó không có bất kì vùng ảnh hay đối tượng nào được chọn.

**Chú ý**: Vùng chọn không thuộc bất kì lớp ảnh nào. Các thao tác với vùng chọn tác động vào lớp ảnh đang được chọn nhưng trong phạm vi được xác định bởi vùng chọn.

## 4. Một số kĩ thuật thiết kế sử dụng vùng chọn

### a) Tạo đường viền

Với kĩ thuật tạo đường viền, dấu chữ thập có thể được bao quanh bởi một đường tròn. Thực hiện các bước sau đây để tạo một đường viền.

*   Bước 1. Thêm một lớp mới, chọn lớp này và xác định một vùng chọn hình tròn.
*   Bước 2. Trên lớp vừa tạo, tô màu cho vùng chọn.
*   Bước 3. Co vùng chọn với số pixel bằng độ dày của đường viền cần tạo.
*   Bước 4. Xoá vùng chọn sau khi co rồi bỏ vùng chọn.

### b) Lồng hình

Tại một số điểm giao cắt giữa hai đối tượng lồng nhau, đối tượng này phải ở trên (hoặc ở dưới) đối tượng kia. Ví dụ, lớp Vòng 2 nằm bên trên lớp Vòng 1 nên ảnh hợp thành của chúng không thể hiện sự lồng nhau.

Sau đây là cách thực hiện thao tác lồng hình tại một điểm giao cắt giữa hai hình.
*   Bước 1. Chọn lớp cần đưa hình ảnh của nó lên trên hình ảnh của lớp kia tại điểm giao cắt. Ví dụ, chọn lớp Vòng 1.
*   Bước 2. Tạo một vùng chọn tại điểm giao cắt sao cho nó bao quanh phần hình ảnh đối tượng cần đưa nó lên trên đối tượng kia, ví dụ như ở Hình 8a.
*   Bước 3. Nhấn liên tiếp hai tổ hợp phím **Ctrl+C** và **Ctrl+V** để thực hiện sao chép hình ảnh của lớp đang chọn tại vùng chọn. Một lớp động (Floating Selection) xuất hiện như Hình 8b. Nháy đúp chuột vào lớp này và đổi tên lớp để tạo một lớp mới thay thế lớp động. Di chuyển lớp mới lên trên lớp đối tượng cần đưa nó xuống dưới (Hình 8c). Ví dụ, sau khi đưa lớp Mảnh vòng 1 lên ta được kết quả mong đợi như Hình 7c.

## 5 SỬ DỤNG ĐƯỜNG DẪN (Paths)
### a) Đường dẫn và cách tạo đường dẫn
Để vẽ hình có hình dạng tuỳ ý cần sử dụng **đường dẫn (Paths)**. Đường dẫn được tạo trong GIMP như sau:
*   Bước 1. Nháy chuột vào công cụ **Paths**.
*   Bước 2. Lần lượt nháy chuột tại các điểm (gọi là các **điểm mốc**), theo thứ tự đó chúng tạo thành đường dẫn cần vẽ. Nếu kéo thả điểm mốc cuối cùng trùng với điểm mốc đầu tiên thì sẽ nhận được đường dẫn khép kín (xem Hình 9a).
*   Bước 3. Khi một đường dẫn được tạo ra, biểu tượng của nó sẽ xuất hiện trong bảng quản lí đường dẫn **Paths** (Hình 9b). Nháy đúp chuột vào tên đường dẫn để gõ tên mới cho nó (Hình 9c).

### b) Thiết kế và chỉnh sửa đường dẫn

Bảng tùy chọn của công cụ **Paths** cho phép chuyển đổi giữa chế độ thiết kế (**Design**) và chế độ chỉnh sửa (**Edit**) đường dẫn. Chế độ thiết kế hỗ trợ các thao tác được mô tả. Chế độ chỉnh sửa hỗ trợ các thao tác.

*   **Uốn cong đoạn nối**: Kéo thả một điểm nào đó trên đoạn nối giữa hai điểm mốc để làm cong đoạn nối (xuất hiện hai tiếp tuyến với đường cong tại hai đầu mút của nó).
*   **Điều chỉnh tiếp tuyến của đường cong**: Kéo thả chuột tại điểm đầu tiếp tuyến của đường cong sẽ thay đổi hướng và độ dài của chúng, làm thay đổi hình dạng đường cong.
*   **Di chuyển điểm mốc**: Kéo thả chuột từ điểm mốc đến vị trí khác để thay đổi hình dạng của các đường nối với điểm này.
*   **Thêm điểm mốc**: Nháy chuột vào một vị trí trên đường cong để thêm điểm mốc, xuất hiện hai tiếp tuyến tại đó. Các tiếp tuyến dùng để điều chỉnh hình dạng của đường cong.

Muốn hiện lại một đường dẫn đã tạo trước đó để chỉnh sửa lại, trong bảng quản lí đường dẫn, nháy chuột phải vào biểu tượng đường dẫn và chọn lệnh **Edit Path**.

### c) Các thao tác cơ bản đối với đường dẫn

Hãy tìm hiểu về các thao tác cơ bản đối với đường dẫn. Từ đó cho biết: Trong các hình bên, em vẽ được những hình nào? Hãy trình bày cách vẽ chúng.

*   Chuyển đổi giữa đường dẫn và vùng chọn bằng lệnh **Select\From Path** (hoặc nháy chuột vào nút lệnh **Selection From Path** trong bảng tuỳ chọn). Để chuyển một vùng chọn thành một đường dẫn, thực hiện lệnh **Select\To Path**.
*   Tạo nét vẽ theo đường dẫn bằng cách nháy chuột vào nút lệnh **Stroke Path** ở bảng tuỳ chọn và nhập số pixel biểu thị độ dày của nét vẽ. Màu của nét vẽ là màu FG.
*   Tô màu vùng đường dẫn bằng cách nháy chuột vào nút lệnh **Fill Path** trong bảng tuỳ chọn. Màu được tô mặc định là màu FG.

## ⑥ Kĩ thuật thiết kế "Cắt xén chi tiết thừa"

**Cắt xén chi tiết thừa** là kĩ thuật thiết kế sử dụng kết hợp đường dẫn và vùng chọn. Mỗi chi tiết thừa của một hình ảnh nào đó được cắt xén theo ba bước sau:
*   *Bước 1*. Xác định vùng chọn để khoanh vùng chỗ cần cắt xén.
*   *Bước 2*. Chọn lớp chứa hình ảnh và xoá vùng chọn.
*   *Bước 3*. Bỏ vùng chọn.

Ví dụ với hình ảnh như Hình 11a, cần cắt xén hình này để nó giống như phần đầu của một dải nơ. Vùng cần cắt được xác định bởi một đường dẫn (Hình 11b). Sau đó, đường dẫn này được chuyển thành vùng chọn để xoá vùng chọn. Sau khi bỏ vùng chọn, nhận được kết quả như Hình 11c.

## Luyện tập

### Bài 1. Thiết kế các hình tròn đồng tâm

Em hãy thiết kế ba hình tròn đồng tâm như Hình 12.
Hướng dẫn thực hiện
Dùng kĩ thuật tạo đường viền để tạo các hình tròn theo thứ tự từ ngoài vào trong. Mỗi hình tròn được tạo trên một lớp riêng. Quá trình thiết kế được gợi ý ở Hình 13.

### Bài 2: Thiết kế hình tròn và hình vuông lồng nhau

Em hãy thiết kế hình tròn và hình vuông lồng nhau.

### Hướng dẫn thực hiện

Trước hết sử dụng kĩ thuật tạo đường viền để tạo hình tròn và hình vuông (đồng tâm). Giả sử lớp **Hình vuông** ở trên lớp **Hình tròn**. Quay hình vuông để được kết quả.

Sử dụng kĩ thuật lồng hình để đưa hình vuông xuống dưới hình tròn tại 4 điểm giao cắt. Quá trình thực hiện lồng hình tại điểm giao cắt thứ nhất. Các điểm giao cắt còn lại thực hiện tương tự.

Em hãy thiết kế logo “10A5 ICT GROUP” như Hình 17.

## Gợi ý thực hiện

Trước hết thực hiện theo hướng dẫn của Bài 2 để tạo khung logo gồm hình vuông và hình tròn lồng nhau. Tô màu gradient cho nền logo và chèn các văn bản vào trong khung logo theo yêu cầu để nhận được kết quả như Hình 18.

Dải nơ bên trái logo được thiết kế bắt đầu từ việc tạo một vùng chọn hình elip trên một lớp mới và tô màu như Hình 19a. Từ hình elip này, tiến hành cắt xén thành dải nơ theo kĩ thuật cắt xén.

Các vùng chọn được xác định trong quá trình cắt xén hình elip được gợi ý như trong Hình 19. Trong đó Hình 19c và Hình 19d minh hoạ các đường dẫn khoanh vùng chi tiết thừa trước khi chuyển nó thành vùng chọn để xoá.

## Luyện tập
Em đồng ý với những phát biểu nào sau đây?
Trong phần mềm thiết kế đồ hoạ, ví dụ như phần mềm GIMP:
1) Để cho đơn giản, nên thiết kế các đối tượng đồ hoạ trên cùng một lớp ảnh.
2) Một số chi tiết của một lớp ảnh có thể không nhìn thấy trong ảnh hợp thành.
3) Không cần có lệnh chuyển đổi giữa đường dẫn và vùng chọn.
4) Các kĩ thuật thiết kế với sự hỗ trợ của các lệnh làm việc với lớp ảnh có thể giúp giảm thời gian thiết kế hoặc thay đổi sự hiển thị của ảnh hợp thành.

## Tóm tắt bài học

Trong các phần mềm thiết kế đồ hoạ, ví dụ như GIMP:
*   **Khái niệm**:
    *   Cửa sổ ảnh hiển thị ảnh hợp thành của các lớp ảnh.
    *   Vùng chọn dùng để xử lí một vùng nào đó trên ảnh.
    *   Đường dẫn dùng để vẽ hình và có thể chuyển đổi đối với vùng chọn.
*   **Các kĩ thuật thiết kế cơ bản**:
    *   Sử dụng các lệnh làm việc với lớp ảnh: thiết kế trên lớp bản sao, hướng tập trung vào một lớp, sắp xếp lại các lớp.
    *   Sử dụng vùng chọn: tạo đường viền, lồng hình.
    *   Sử dụng kết hợp đường dẫn và vùng chọn để cắt xén chi tiết thừa.

# Bài 3: TÁCH ẢNH VÀ THIẾT KẾ ĐỒ HOẠ VỚI KÊNH ALPHA

Học xong bài này, em sẽ:
*   Hiểu được khái niệm độ **"trong suốt"**.
*   Sử dụng được kênh alpha và các kĩ thuật thiết kế dựa trên vùng chọn, đường dẫn để thiết kế được banner hoặc bảng rôn.

Khi ghép hai ảnh với nhau để tạo thành một ảnh mới, em thường gặp điều gì không như mong đợi và muốn khắc phục để được kết quả đẹp hơn?

## 1 Kênh alpha và kĩ thuật tách ảnh nhờ kênh alpha

### 1
Hình 1 minh hoạ hai ảnh đích (thiệp chúc mừng sinh nhật) được tạo thành sau khi ghép hai ảnh nguồn (hộp quà và bó hoa) từ hai tệp ảnh có sẵn. Ở Ảnh đích 1, các ảnh nguồn có nền không "trong suốt". Ngược lại, ở Ảnh đích 2, chúng có nền "trong suốt".

1) Em hãy nêu tác dụng của ảnh có nền trong suốt.
2) Mức độ nhìn rõ ảnh phụ thuộc thế nào vào độ "trong suốt" của nó?

a) Ảnh đích 1
b) Ảnh đích 2

### a) Ảnh có nền trong suốt
Trong các phần mềm thiết kế, chỉnh sửa đồ hoạ, nếu ảnh có nền trong suốt thì có thể nhìn xuyên qua ảnh đến tận “vô cùng”. GIMP sử dụng mẫu ca rô đen xám xen kẽ để biểu thị giới hạn vô cùng hay nền trong suốt này (Hình 2a). Nếu dùng công cụ Eraser để tẩy một số chỗ trên ảnh thì sẽ phát hiện ra ảnh có nền trong suốt hay không. Hình 2b minh hoạ ảnh có nền trong suốt (đôi khi còn gọi là “ảnh không có nền”), còn Hình 2c minh hoạ ảnh có nền màu trắng vì nó lộ ra ở chỗ bị tẩy xoá.

## Kênh alpha và kĩ thuật tách ảnh

Mỗi điểm ảnh sẽ không được nhìn thấy nếu nó có độ trong suốt hoàn toàn hoặc nhìn thấy mờ mờ nếu nó có độ trong suốt nào đó. Nói cách khác, sự hiện diện của mỗi điểm ảnh được thể hiện thông qua màu sắc cùng với độ trong suốt của nó. Vì vậy, nhiều phần mềm thiết kế, chỉnh sửa đồ hoạ lưu trữ và biểu thị các điểm ảnh thông qua các kênh màu và kênh trong suốt của chúng. GIMP lưu trữ ba kênh màu R, B, G và có thể được thêm một kênh lưu độ trong suốt của tất cả các điểm ảnh, gọi là **kênh alpha**.

Tấm thiệp ở *Hình 1a* thể hiện sự ghép ảnh một cách thô sơ là sản phẩm đồ hoạ thiếu tính tự nhiên. Do đó, trước khi ghép vào ảnh đích, các ảnh nguồn cần được tách ra khỏi nền của nó. Tuỳ theo đặc điểm của ảnh cần tách khỏi nền mà sử dụng công cụ tách ảnh phù hợp. Sau đây là cách tách ảnh phổ biến bằng công cụ **Free Select** (công cụ chọn tự do).

### Bước 1. Chọn ảnh nguồn và thêm kênh alpha vào lớp ảnh

*   Chọn lớp ảnh cần xử lí, ví dụ chọn lớp ảnh *Hộp quà*.
*   Thêm kênh alpha vào lớp ảnh bằng cách thực hiện lệnh **Add Alpha Channel** từ bảng chọn **Layer\Transparency** hoặc từ bảng chọn được mở ra khi nháy chuột phải vào tên lớp ở bảng quản lí lớp. Ảnh bây giờ có nền trong suốt nên có thể chọn và tách các đối tượng ra khỏi nền.

### Bước 2. Chọn đối tượng cần tách ra khỏi nền ảnh

*   Nháy chuột chọn công cụ **Free Select** rồi bắt đầu từ một điểm bất kì trên biên đối tượng, lần lượt nháy chuột vào xung quanh đối tượng cần tách, ví dụ như *Hình 3a*.
*   Khi chọn đến chi tiết nhỏ, khó nhìn rõ, nhấn giữ phím **Ctrl** và lăn nút cuộn chuột để phóng to hay thu nhỏ ảnh cho phù hợp. Khi phóng to ảnh, vị trí đang thao tác có thể chạy ra xa, nhấn giữ phím **Space** và di chuyển chuột để di chuyển khung ảnh sao cho nhìn thấy vị trí này, ví dụ như *Hình 3b*.
*   Điểm chọn cuối cùng được xác định bằng cách nháy chuột trùng với điểm xuất phát. Khi đó, một vùng chọn bao quanh đối tượng xuất hiện, nó biểu thị đối tượng đã được chọn, ví dụ như *Hình 3c*.

### Bước 3. Tách ảnh khỏi nền
*   Đảo ngược vùng chọn đối tượng. Toàn bộ phần ảnh xung quanh hộp quà sẽ được chọn.
*   Xoá vùng chọn rồi bỏ chọn. Theo ví dụ trên, toàn bộ phần ảnh xung quanh hộp quà bị xoá. Lớp ảnh **Hộp quà** bây giờ có nền trong suốt.

## Xác định vùng chọn đối tượng từ kênh alpha trong thiết kế đồ hoạ
Trong Hình 4a và Hình 4b, lớp Tam giác chứa duy nhất hoạ tiết màu đen. Hãy nêu cách thức hiện tạo thêm một hoạ tiết giống như vậy và chỉnh sửa để được kết quả như Hình 4c.

Vùng chọn đối tượng được sử dụng để thiết kế, chỉnh sửa cho chính đối tượng đó hoặc cho đối tượng thuộc lớp ảnh khác.

Ví dụ, sau khi thiết kế xong hoạ tiết ở Hình 4c, ta muốn tô lại màu cho hoạ tiết tam giác thành màu xanh như Hình 5. Để làm điều này, chọn lớp Tam giác, chuyển kênh alpha của lớp sang vùng chọn bằng lệnh **Layer\Transparency\Alpha to Selection** hoặc nháy chuột phải vào tên lớp ở bảng điều khiển lớp và chọn lệnh **Alpha to Selection**. Sau đó tiến hành tô màu xanh cho vùng chọn và bỏ vùng chọn.

## Thực hành

### Bài 1. Tạo thiệp chúc mừng với ảnh được tách khỏi nền
Em hãy tạo một thiệp chúc mừng sinh nhật như Hình 1b, trong đó các ảnh nguồn (hộp quà và bó hoa) được tách khỏi nền. Có thể thay đổi nội dung các lời chúc mừng và thay các ảnh nguồn bằng ảnh khác.
Gợi ý thực hiện: Sử dụng kĩ thuật tách ảnh để tách các ảnh nguồn ra khỏi nền trước khi sao chép vào ảnh đích.

### Bài 2. Tạo banner “ICT GROUP 10A5”
Em hãy tạo banner “ICT GROUP 10A5” như Hình 6 sau đây.
Gợi ý thực hiện:
* Sử dụng lại sản phẩm của bài tập Vận dụng thuộc Bài học 2 để làm logo cho banner.
* Tạo thêm một dải nơ cho logo này.
* Tách ảnh logo khỏi nền nếu cần thiết.
* Tạo tệp ảnh mới để thiết kế banner.
* Tạo nền banner và tô màu gradient cho nền.
* Sao chép ảnh logo vào banner.
* Tạo các hoạ tiết đường cong cho banner bằng kĩ thuật cắt xén.
* Trong quá trình thiết kế, các chi tiết có thể tô lại màu sắc bằng cách chuyển lớp chứa nó thành vùng chọn và tô màu cho vùng chọn.

## Vận dụng
Em hãy thiết kế một trong các sản phẩm đồ hoạ như: áp phích, banner, bảng rôn, logo theo nhu cầu và sở thích của em. Lưu sản phẩm và xuất ra một tệp ảnh với định dạng chuẩn. Sau đây là một số ví dụ về logo và áp phích:

Em đồng ý với những phát biểu nào sau đây? Trong phần mềm thiết kế đồ hoạ, ví dụ như phần mềm GIMP:
1) Độ trong suốt của ảnh tỉ lệ thuận với mức độ nhìn rõ ảnh.
2) Tách ảnh khỏi nền là loại bỏ lớp nền hay nói cách khác là tạo ra một lớp nền trong suốt.
3) Việc chuyển kênh alpha của một lớp ảnh vào vùng chọn sẽ giúp chọn được các đối tượng trên lớp đó.
4) Cho dù đối tượng được thiết kế phức tạp thế nào thì luôn chọn được nó nhờ chuyển kênh alpha của lớp chứa nó vào vùng chọn.
5) Sử dụng các kĩ thuật thiết kế và kênh alpha có thể tạo ra các sản phẩm đồ hoạ đơn giản như logo, áp phích hay poster, banner hoặc băng rôn.

## Tóm tắt bài học

Trong các phần mềm thiết kế đồ hoạ, ví dụ như GIMP:

### Khái niệm

*   **Độ trong suốt** của điểm ảnh thể hiện mức độ rõ nét của nó: Điểm ảnh càng trong suốt thì càng không nhìn thấy rõ nó. Ảnh không có nền (còn gọi là nền không màu) là ảnh có lớp nền trong suốt.
*   Các điểm ảnh trên lớp ảnh được thể hiện và lưu trữ trên các kênh màu và **kênh alpha**. Trong đó, **kênh alpha** thể hiện **độ trong suốt** (hay độ không nhìn rõ) của các điểm ảnh.
*   Có hai thao tác cơ bản với **kênh alpha** đó là: thêm **kênh alpha** vào một lớp ảnh và chuyển **kênh alpha** của một lớp ảnh vào vùng chọn.

### Các kĩ thuật thiết kế cơ bản

*   **Tách ảnh** (sau khi thêm kênh alpha vào lớp chứa ảnh cần tách).
*   **Xử lí một vùng chọn** trên ảnh (với vùng chọn được xác định từ kênh alpha của một lớp ảnh nào đó).

# Bài 4: THỰC HÀNH TỔNG HỢP

Học xong bài này, em sẽ:
* Sử dụng được các lớp ảnh, kênh alpha và ôn luyện các kĩ thuật thiết kế.
* Làm quen với các lệnh tạo hiệu ứng.
* Tạo được các sản phẩm đồ hoạ đơn giản như logo, poster.

## Bài 1. Thiết kế logo Olympic Việt Nam

### Yêu cầu
Em hãy tạo tệp ảnh mới và thiết kế logo “Olympic Việt Nam” trong đó các vòng tròn Olympic lồng nhau. Lưu tệp ảnh với tên tệp là “Olympic VN.cxf” và xuất ảnh với tên tệp là “Olympic VN.png”.

### Hướng dẫn thực hiện

#### Bước 1. Mở tệp ảnh mới và xác định các tham số của ảnh
Tạo một tệp ảnh mới với các tham số được lựa chọn phù hợp, chẳng hạn như sau:
Kích thước = 300 × 250 mm; Độ phân giải = 7 pixels/mm; Không gian màu = RBG; Nền trắng.

#### Bước 2. Thiết kế các vòng tròn Olympic
Các vòng tròn Olympic được tạo bằng kĩ thuật thiết kế trên lớp bản sao.

##### a) Tạo vòng tròn Olympic thứ nhất
Thêm một lớp mới trong suốt, đặt tên lớp là **Xanh đậm** để chứa vòng tròn Olympic thứ nhất màu xanh da trời. Chọn lớp **Xanh đậm**, sử dụng kĩ thuật tạo đường viền để tạo trên lớp này một hình tròn màu xanh da trời.

##### b) Tạo các vòng tròn Olympic còn lại

Các vòng tròn Olympic còn lại (Đen, Đỏ, Vàng sẫm, Xanh lá) được tạo bằng kĩ thuật thiết kế trên lớp bản sao. Ví dụ, tạo vòng tròn Olympic thứ hai như sau: nhân đôi lớp **Xanh đậm**, đổi tên lớp thành **Đen** rồi di chuyển nó đến vị trí phù hợp, cuối cùng tô màu đen cho vòng tròn.

*Lưu ý:* Khi di chuyển lớp, nó lệch ra khỏi vị trí của ảnh ban đầu. Thực hiện lệnh **Layer\Layer to Image Size** để khớp lớp ảnh mới với lớp ảnh ban đầu.

#### Bước 3. Tạo các điểm lồng nhau của các vòng tròn Olympic

Các điểm lồng nhau giữa các vòng tròn Olympic được thiết kế dựa trên kĩ thuật lồng hình. Ví dụ, tại một điểm giao, cần đưa vòng tròn xanh đậm lên trên vòng tròn vàng sẫm. Thực hiện điều này như sau:

*   Chọn lớp **Xanh đậm** rồi tạo một vùng chọn hình chữ nhật tại điểm giao của hai vòng tròn. Thực hiện liên tiếp hai lệnh **Edit\Copy** và **Edit\Paste** để sao chép một mảnh của đường tròn xanh đậm tại điểm giao. Một lớp động được tự động tạo ra chứa kết quả sao chép. Nháy chuột vào nút lệnh (biểu tượng thêm lớp mới) để thêm vào một lớp mới thay thế lớp động. Đổi tên lớp mới thành **Mảnh xanh đậm**.
*   Di chuyển lớp **Mảnh xanh đậm** lên trên lớp **Vàng sẫm** để che đường tròn màu vàng sẫm tại điểm giao. Kết quả nhận được là vòng tròn xanh đậm đè lên trên vòng tròn vàng sẫm.

#### Bước 4. Tạo lá cờ của logo
* Dùng công cụ đường dẫn và vùng chọn để tạo lá cờ màu đỏ và ngôi sao màu vàng.
* Dùng kĩ thuật cắt xén để cắt phần dưới lá cờ, trong đó vùng chọn để cắt là vùng chọn hình elip.

#### Bước 5. Lưu và xuất tệp ảnh
* Lưu tệp ảnh với tên tệp là "Olympic VN.cxf".
* Xuất ảnh với tên tệp là "Olympic VN.jpg".

## Bài 2. Thiết kế banner "Câu lạc bộ Tin học ứng dụng"

### Yêu cầu
Hãy thiết kế banner "Câu lạc bộ Tin học ứng dụng" của lớp 10A5 như Hình 5. Lưu tệp ảnh và xuất tệp sang định dạng chuẩn png, tên tệp là "Banner CLB ICT".

### Hướng dẫn thực hiện
#### Bước 1. Tạo tệp ảnh mới và thêm các lớp ảnh mới
* Tệp ảnh mới nền trắng với một trong các kích thước phù hợp của banner, chẳng hạn là: 2 500 × 1 500 pixel, độ phân giải 200 ppi.
* Mỗi đối tượng nên được tạo trên một lớp riêng biệt và tất cả các lớp được thêm mới đều có nền trong suốt.

#### Bước 2. Thiết kế khu vực nền banner: nền, khung và màu nền
* Thêm lớp mới để tạo nền banner. Nền banner được tạo bằng vùng chọn hình chữ nhật và được tô màu gradient với các thuộc tính gradient: FG/BG = Đen/Trắng, gradient = **Rounded edge**, hoà màu = **Perceptual RGB**, hình dạng = **Linear**, đường cơ sở đi từ góc trái dưới lên góc phải trên, xem Hình 6.

* Thêm lớp mới bên trên lớp nền để tạo khung banner. Khung banner được thiết kế bằng kĩ thuật tạo đường viền.
* Thêm lớp mới bên trên lớp khung để tạo màu nền cho banner. Màu nền của banner được tạo bằng cách hoà màu xanh dương với dải gradient đen, xám của lớp nền bên dưới. Để hoà màu, trước hết tô màu thuần nhất (xanh dương) cho lớp **Màu nền** (Hình 7a, 7b), sau đó đặt chế độ hoà màu (**Mode**) là **Soft Light**. Kết quả như Hình 7c.

#### Bước 3. Thiết kế hoạ tiết “Tam giác”

* Thêm lớp **Tam giác** bên trên lớp **Màu nền** để chứa hoạ tiết tam giác màu đen. Hoạ tiết này bắt đầu được tạo bằng một vùng chọn hình vuông, được tô màu đen. Sau đó quay, di chuyển hình và dùng kĩ thuật cắt xén để nhận được kết quả như mong muốn. Quá trình thiết kế này được gợi ý qua Hình 8.
* Nhân đôi lớp **Tam giác** để nhận được lớp **Tam giác copy**. Chuyển kênh alpha của lớp **Tam giác copy** vào vùng chọn. Tô màu gradient cho vùng chọn với các thuộc tính gradient đã chọn trước đó (Hình 9a). Bỏ vùng chọn rồi di chuyển lớp **Tam giác copy** sang phải một chút để hở lớp bên dưới, tạo thành một đường viền đen bên trái nó (Hình 9b).

Hình 9. Nhân đôi hoạ tiết để thiết kế hoạ tiết mới

#### Bước 4. Thiết kế hoạ tiết các hình tròn đồng tâm

Sử dụng kĩ thuật tạo đường viền để tạo các hình tròn đồng tâm màu đen, tương ứng ở trên các lớp HT1, HT2, HT3 (Hình 10a, 10b). Sử dụng kĩ thuật cắt xén chi tiết thừa để nhận được kết quả như Hình 11c. Cuối cùng tô màu hai hình tròn trong cùng và thu được kết quả như Hình 10d.

Hình 10. Tóm tắt quá trình thiết kế hoạ tiết các hình tròn đồng tâm

#### Bước 5. Tạo hoạ tiết các đường cong cách điệu

Hai đường cong cách điệu ở trên và dưới được tạo trên các lớp mới bằng các vùng chọn hình elip, sau đó sử dụng kĩ thuật cắt xén để nhận được kết quả mong muốn. Hình 11 gợi ý quá trình tạo vùng chọn, tô màu rồi thực hiện cắt xén.
