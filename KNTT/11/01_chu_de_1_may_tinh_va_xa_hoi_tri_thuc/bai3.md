# Bài 3: QUAN HỆ GIỮA HỆ ĐIỀU HÀNH, PHẦN CỨNG VÀ PHẦN MỀM ỨNG DỤNG

## Hoạt động 3: Vai trò của hệ điều hành

Có hay không trường hợp phần mềm chạy trên một thiết bị không có hệ điều hành? Khi nào cần phải có hệ điều hành?

Thời kì mới có máy tính, chưa có hệ điều hành, người sử dụng phải nạp thủ công chương trình vào bộ nhớ như gõ lệnh hay nhập chương trình được mã hoá trên băng giấy hoặc bìa đục lỗ, sau đó nhấn một phím trên bàn điều khiển và đợi kết quả.

Ngày nay, có nhiều thiết bị được điều khiển bởi các bộ vi xử lí, cài sẵn chương trình ghi trong bộ nhớ ROM, bật lên là chạy không cần hệ điều hành. Ví dụ hệ thống điều khiển lò vi sóng cho phép người dùng chọn lựa các chế độ nấu ăn.

Tuy nhiên cách này chỉ phù hợp với những thiết bị chuyên dụng, chỉ làm một việc, không thích hợp với các thiết bị đa năng như máy tính có khả năng thực hiện nhiều công việc. Với thiết bị đa năng, người dùng có nhu cầu nạp nhiều phần mềm ứng dụng và dữ liệu vào bộ nhớ ngoài (cần tổ chức dữ liệu, cần quản lí việc chạy, cần giao diện làm việc). Khi chạy, cần điều phối tài nguyên cho các ứng dụng như bộ nhớ, công suất CPU, các thiết bị ngoại vi. Cần có **hệ điều hành** để đáp ứng các nhu cầu trên. Hệ điều hành cung cấp các dịch vụ điều khiển máy tính để thực hiện các công việc cơ bản mà nhiều chương trình ứng dụng cần đến: Ví dụ, hệ điều hành có các dịch vụ tìm kiếm tệp trong bộ nhớ ngoài, mở tệp, ghi dữ liệu vào tệp và đóng tệp. Các ứng dụng muốn ghi dữ liệu vào tệp không tự điều khiển máy tính làm những công việc trên mà chỉ gọi các dịch vụ do hệ điều hành cung cấp để thực hiện.

Như vậy, **phần cứng** là thiết bị xử lí thông tin, hệ điều hành là môi trường trung gian giúp phần mềm ứng dụng khai thác phần cứng. Quan hệ giữa hệ điều hành, phần cứng và phần mềm ứng dụng được minh hoạ.

Hệ điều hành là môi trường để phần mềm ứng dụng khai thác hiệu quả phần cứng.

1.  Nêu lí do thiết bị xử lí đa năng cần có hệ điều hành.
2.  Nêu mối quan hệ giữa phần cứng, phần mềm ứng dụng và hệ điều hành.

## LUYỆN TẬP

1.  Em hiểu thế nào về tính thân thiện của hệ điều hành?
2.  Hệ điều hành cung cấp môi trường giao tiếp với người sử dụng như thế nào? Môi trường giao tiếp đó thể hiện như thế nào trên hệ điều hành Windows?

## VẬN DỤNG

1.  Em hãy tìm hiểu xem ngoài máy tính còn có thiết bị điện gia dụng nào sử dụng hệ điều hành không.
2.  Thực ra, Linux là hệ điều hành có nguồn gốc từ hệ điều hành UNIX. Hãy tìm hiểu lịch sử của hệ điều hành Linux để biết thêm về hệ điều hành UNIX.

# Bài 2: THỰC HÀNH SỬ DỤNG HỆ ĐIỀU HÀNH

SAU BÀI HỌC NÀY EM SẼ:
*   Sử dụng được một số chức năng cơ bản của hệ điều hành cho máy tính cá nhân.
*   Sử dụng được một vài tiện ích của hệ điều hành nâng cao hiệu quả của máy tính cá nhân.
*   Sử dụng được một vài tiện ích cơ bản của hệ điều hành trên thiết bị di động.

Các thiết bị di động thực tế cũng là máy tính cá nhân. Hệ điều hành của các loại máy tính cá nhân có nhiều tiện ích khác nhau nhưng giao diện người dùng có nhiều điểm tương đồng. Em hãy chỉ ra một vài điểm tương đồng đó.

## Nhiệm vụ 1. Sử dụng một số chức năng cơ bản của hệ điều hành cho máy tính cá nhân

Ở Bài 1, em đã biết hệ điều hành cho máy tính cá nhân như Windows, macOS và Linux. Em hãy thực hành sử dụng các chức năng sau (với hệ điều hành Windows hoặc hệ điều hành mã nguồn mở Ubuntu):
*   Cung cấp môi trường giao tiếp với người sử dụng.
*   Quản lí tệp và thư mục.

### Hướng dẫn:
*   Cung cấp môi trường giao tiếp với người sử dụng.
*   Quan sát giao diện đồ hoạ với các **cửa sổ**, các **biểu tượng** và **con trỏ**. Mỗi cửa sổ hay biểu tượng đều có tên. **Con trỏ** dùng để chọn đối tượng làm việc.
*   Nhận biết các biểu tượng trên màn hình như: tệp, thư mục, nút lệnh,...

Cửa sổ ứng dụng
Biểu tượng của các đối tượng
Thanh công việc (Taskbar)
Thanh trạng thái (Status bar)

*   Truy cập nhanh các phần mềm ứng dụng nhờ thanh công việc hay nút Start.
*   Quan sát thanh trạng thái hiển thị các biểu tượng và cho biết trạng thái làm việc của máy tính như kết nối mạng, dung lượng pin, mức loa, chế độ bàn phím,...
*   Thực hành các thao tác làm việc với biểu tượng như nháy chuột, nháy đúp chuột, nháy nút phải chuột, kéo thả chuột.
    *   Quản lí tệp và thư mục.
    *   Sử dụng tiện ích **File Explorer** của Windows để quản lí tệp và thư mục.
*   Trong cửa sổ **File Explorer**, nháy chuột (nháy đúp chuột) vào biểu tượng thư mục để xem nội dung bên trong (các tệp và thư mục con).
*   Thực hành quản lí thư mục gồm: tạo mới, đổi tên, xoá, di chuyển thư mục.

* Thực hành quản lí tệp trên Ubuntu gồm: đổi tên, xoá, di chuyển tệp và chạy ứng dụng với tệp chương trình.
* Nháy đúp chuột vào biểu tượng của tệp ứng dụng hoặc tệp dữ liệu để kích hoạt ứng dụng tương ứng.
* Nháy nút phải chuột vào một đối tượng để làm xuất hiện bảng chọn gồm các lệnh có thể thực hiện được với đối tượng đó như minh hoạ trong Hình 2.5.

## Nhiệm vụ 2. Sử dụng một số tiện ích trên hệ điều hành máy tính cá nhân nhằm nâng cao hiệu quả sử dụng máy

**Tiện ích** là những phần mềm công cụ hỗ trợ nhiều công việc khác nhau như ứng dụng tính toán, chụp ảnh màn hình, gõ tiếng Việt hoặc các phần mềm nâng cao hiệu quả làm việc với máy tính như nén tệp, diệt virus. Có một số tiện ích được cài đặt cùng với hệ điều hành như tiện ích kiểm tra đĩa cứng hay kiểm tra kết nối mạng nhưng cũng có những tiện ích không có sẵn, được cài đặt sau. Một khi được cài đặt chúng được tích hợp như một dịch vụ trên hệ điều hành, ví dụ các tiện ích nén dữ liệu zip hay bộ gõ bàn phím Unikey.

Em hãy thực hành sử dụng tiện ích kiểm tra đĩa và hợp mảnh trên đĩa cứng.

## Hướng dẫn:

Đĩa cứng ghi dữ liệu theo các đường tròn đồng tâm gọi là **đường ghi (track)**, mỗi đường gồm nhiều **cung (sector)**, mỗi cung ghi 512 byte dữ liệu. Việc đọc, ghi được thực hiện theo đơn vị **liên cung (cluster)**, thường gồm 8 cung.

Khi ghi tệp, hệ điều hành sẽ tìm các vùng trống trên đĩa để ghi, những vùng này có thể nằm trên các đường ghi khác nhau làm tệp bị **phân mảnh**. Khi đó, thời gian đọc, ghi tệp tăng lên nhiều lần vì đầu từ phải dịch chuyển (một cách cơ học) từ đường ghi này sang đường ghi khác. Việc tổ chức lại tệp sao cho các liên cung của một tệp được ghi liên tục, giảm hoạt động di chuyển đầu từ sẽ giúp tăng tốc độ truy cập đĩa cứng. Tiện ích tối ưu hoá (**Optimize**), còn có tên là **hợp mảnh (Defragment)** cho phép thực hiện công việc này.

Do nhiều nguyên nhân, có thể xảy ra các lỗi tệp như một liên cung mất liên kết với tệp, tạo thành các đoạn dữ liệu "**mồ côi**", có trên đĩa nhưng không khai thác được hoặc tình trạng chồng chéo, khi có vài tệp liên kết đến cùng một liên cung. Ngoài ra, còn có tình trạng một số cung bị hỏng về vật lí (**bad sector**), đọc ghi không được, cần phải loại khỏi danh sách sử dụng. Tiện ích **kiểm tra đĩa (Check disk)** dùng để khử các lỗi trên để việc đọc, ghi đĩa trở lại bình thường.

Các bước để sửa lỗi đĩa và hợp mảnh:

*   Bước 1. Sử dụng File Explorer và tìm danh sách các ổ đĩa. Nháy nút phải chuột vào ổ đĩa muốn xử lí rồi chọn Properties.
*   Bước 2. Trong cửa sổ Properties của đĩa cứng, chọn Tools.
*   Bước 3. Chọn Check để kiểm tra và khắc phục lỗi đĩa; Chọn Optimize để tối ưu hoá, hợp mảnh.

Lưu ý: Chức năng hợp mảnh chỉ có tác dụng đối với đĩa từ. Việc hợp mảnh có thể mất nhiều thời gian nếu đĩa có dung lượng lớn.

## Nhiệm vụ 3. Sử dụng một số tiện ích của hệ điều hành cho thiết bị di động

1.  Em hãy kể tên một số các tiện ích của hệ điều hành Android hoặc iOS cho thiết bị di động mà em biết.

Thiết bị di động như điện thoại thông minh và máy tính bảng cung cấp cho người dùng nhiều tiện ích cá nhân như quản lí danh bạ, nhắn tin, hẹn giờ, lịch, quản lí ảnh, quản lí tệp,...

### Giao diện quản lí danh bạ

Hãy tìm hiểu trên điện thoại em đang sử dụng để thực hiện các chức năng sau:

*   Hiển thị danh bạ.
*   Thêm một người vào danh bạ với các thông tin về số điện thoại, địa chỉ, nhóm; sửa thông tin của một người trong danh bạ; chia sẻ thông tin danh bạ.
*   Xoá một người khỏi danh bạ.
*   Truy cập danh bạ để gọi điện thoại nhanh.

### Đặt lịch, hẹn giờ, nhắc việc

*   Mở giao diện đồng hồ, sau đó đặt một công việc được nhắc hẹn vào một giờ định trước, một ngày định trước.
*   Đặt hẹn một công việc hằng ngày để được nhắc hằng ngày.

### Quản lí ứng dụng

*   Xem các ứng dụng được tải và cài trên máy.
*   Xoá ứng dụng không cần thiết.

## Luyện tập
1. Tiện ích danh bạ còn có chức năng **quản lí nhóm**. Mỗi nhóm có thể gồm nhiều số điện thoại, mỗi số điện thoại có thể thuộc nhiều nhóm. Hãy thực hiện việc tạo nhóm, xoá nhóm, đăng kí vào danh bạ.
2. **Đồng hồ** là một tiện ích cơ bản của hệ điều hành di động. Ứng dụng này, không chỉ cho phép đặt nhắc hẹn (một lần hay định kì) mà còn có khả năng đếm thời gian chính xác đến 1% giây, rất cần cho các hoạt động cần độ chính xác cao như đo các kỉ lục thể thao. Hãy sử dụng các chức năng đếm thời gian tiến hay lùi của tiện ích này.

## Vận dụng
1. Hình 2.7 là cửa sổ Properties mở theo Tab Tools. Nếu mở theo Tab General em sẽ thấy có nút lệnh của tiện ích dọn đĩa (Disk Cleanup). Hãy tìm hiểu chức năng và cách sử dụng tiện ích này.
2. Ngoài cách đăng nhập dùng mật khẩu, các thiết bị di động còn cung cấp nhiều phương pháp đăng nhập khác như nhận dạng vân tay, nhận dạng khuôn mặt hay dùng khẩu hình. Hãy tìm hiểu các phương pháp đó và so sánh các điểm mạnh, điểm yếu của chúng.

# Bài 3: PHẦN MỀM NGUỒN MỞ VÀ PHẦN MỀM CHẠY TRÊN INTERNET

## Sau bài học này em sẽ:

*   Trình bày được một số khái niệm và so sánh phần mềm nguồn mở với phần mềm thương mại; nêu được vai trò của phần mềm nguồn mở và phần mềm thương mại đối với sự phát triển của công nghệ thông tin.
*   Làm quen với phần mềm chạy trên Internet.

Với ngôn ngữ lập trình bậc cao, chương trình được viết dưới dạng văn bản gần với ngôn ngữ tự nhiên. Văn bản này gọi là mã nguồn. Để máy tính có thể chạy được trực tiếp, chương trình được dịch thành dãy lệnh máy gọi là mã máy. Mã máy rất khó đọc hiểu nên việc dịch sang mã máy còn giúp bảo vệ chống đánh cắp ý tưởng hay sửa đổi phần mềm. Phần mềm chuyển giao dưới dạng mã máy thường được gọi là phần mềm nguồn đóng.

Vào những năm 1970, trong một số trường đại học ở Mỹ đã xuất hiện việc chia sẻ mã nguồn để cùng phát triển phần mềm, dần tới sự ra đời của **phần mềm nguồn mở** – một xu hướng có ảnh hưởng lớn tới sự phát triển của công nghệ phần mềm sau này.

Theo em, lợi ích đối với cộng đồng trong việc chia sẻ mã nguồn là gì?

## 1. Phần mềm nguồn mở

### Hoạt động 1: Tìm hiểu các cách chuyển giao phần mềm

Cách thức chuyển giao phần mềm cho người sử dụng theo chiều hướng “mở dần” như sau:
1.  Bán phần mềm dưới dạng mã máy.
2.  Cho sử dụng phần mềm miễn phí có điều kiện hoặc không điều kiện, không cung cấp mã nguồn.
3.  Cho sử dụng phần mềm tự do, cung cấp cả mã nguồn để có thể sửa, nâng cấp, phát triển và chuyển giao (phân phối) lại phần mềm.

Hãy thảo luận xem lợi ích của người dùng được tăng dần như thế nào theo hướng mở nói trên.

### a) Phân loại phần mềm theo các cách chuyển giao sử dụng

Các loại phần mềm tương ứng với ba cách thức chuyển giao trong Hoạt động 1 được gọi lần lượt là:

*   **Phần mềm thương mại** (commercial software) là phần mềm để bán. Hầu hết các phần mềm thương mại là loại nguồn đóng để bảo vệ ý tưởng và chống sửa đổi. Phần mềm soạn thảo văn bản Microsoft Word và phần mềm chỉnh sửa ảnh Photoshop,... là các ví dụ phần mềm thương mại.

*   **Phần mềm tự do (free software)** là phần mềm không chỉ miễn phí mà còn được tự do sử dụng mà không phải xin phép. Phần mềm tự do có thể ở dạng mã máy hoặc mã nguồn.

Hình 3.1 cho thấy một phần của trang web cho phép tải phần mềm làm việc với các tệp pdf. Bản Acrobat Reader là phần mềm tự do ở dạng mã máy, chỉ có thể đọc, ghi chú và in văn bản. Nếu người dùng muốn có các tính năng cao hơn như soạn thảo, quét một ảnh thành một bản pdf, kí, theo dõi vết chỉnh sửa, chuyển định dạng,... thì phải mua bản thương mại Acrobat Pro DC.

*   **Phần mềm nguồn mở (open-source software)** là phần mềm được cung cấp cả mã nguồn để người dùng có thể tự sửa đổi, cải tiến, phát triển, phân phối lại theo một quy định gọi là giấy phép được nêu dưới đây. Thông thường, phần mềm nguồn mở là tự do và không được bảo hành.
*   Một số phần mềm mã nguồn mở được giới thiệu trong bộ sách giáo khoa này có thể kể tới đó là Inkscape, GIMP, môi trường lập trình cho ngôn ngữ Python,...

### b) Giấy phép đối với phần mềm nguồn mở

Khi sử dụng mỗi loại phần mềm nói trên, người dùng cần tuân thủ các điều kiện được phép sử dụng, thường được gọi là "giấy phép" với nghĩa của từ "license" trong tiếng Anh. Ví dụ, khi trả tiền cho mỗi giấy phép, phần mềm thương mại chỉ được phép cài trên một số lượng máy tính nhất định.

## Hoạt động 2: Giấy phép đối với phần mềm nguồn mở

*   Theo quy định về bản quyền, các tác giả của phần mềm có quyền bảo vệ chống phần mềm bị sửa đổi gây phương hại đến uy tín và danh dự của tác giả. Nếu là người đầu tư, các tác giả còn giữ cả quyền tạo bản sao, sửa đổi, nâng cấp phần mềm, quyền chuyển giao sử dụng,...
*   Em hãy so sánh quyền sử dụng phần mềm nguồn mở với quy định về bản quyền và cho biết một số điểm mâu thuẫn.

Chính vì sự mâu thuẫn giữa quy định về bản quyền và quyền sử dụng phần mềm nguồn mở mà cần có giấy phép cho phần mềm nguồn mở. Giấy phép sẽ cung cấp cho người dùng các quyền vốn bị cấm bởi các quy định bản quyền.

Giấy phép không chỉ đề cập đến quyền sử dụng mà còn liên quan đến nhiều vấn đề khác như:
* Các tác giả có được miễn trừ bảo hành hay không, có bị kiện vì những sai sót của phần mềm hay không.
* Người sửa đổi phần mềm có bắt buộc phải công bố rõ các tác giả trước đó hay không, bản sửa đổi có phải công khai dưới dạng nguồn mở hay không.

Có nhiều loại giấy phép phần mềm nguồn mở, trong đó giấy phép công cộng **GNU GPL** (GNU General Public License) được áp dụng rộng rãi nhất. Nó có những quy định không chỉ đảm bảo quyền tiếp cận của mọi người đối với các phần mềm nguồn mở mà còn đảm bảo sự phát triển bền vững của phần mềm nguồn mở. Giấy phép GNU GPL 3.0 phát hành năm 2007 (xem www.gnu.org/licenses/gpl.html) có một số nội dung đáng chú ý sau:
* Được sao chép và phân phối phần mềm; có quyền yêu cầu trả phí cho việc chuyển giao đó nhưng phải thông báo rõ ràng về bản quyền gốc và thông báo miễn trừ trách nhiệm bảo hành.
* Được sửa đổi và phân phối bản sửa đổi với điều kiện phải công bố mã nguồn phần sửa đổi, nêu rõ đó là bản đã được thay đổi, chỉ rõ các thành phần được thay đổi; đồng thời phải áp dụng giấy phép GNU GPL cho chính phần thay đổi đó. Nói cách khác, phần mềm có nguồn gốc từ việc sửa đổi một phần mềm nguồn mở theo GPL cũng phải là phần mềm nguồn mở theo GPL.

* Phần mềm thương mại dùng để bán, người dùng phải mua mới được quyền sử dụng. Hầu hết phần mềm thương mại được bán ở dạng mã máy, gọi là phần mềm nguồn đóng.
* Phần mềm nguồn mở là phần mềm được cung cấp cả mã nguồn mà người dùng có quyền sử dụng, thay đổi và phân phối lại theo các “giấy phép” thích hợp.
* Giấy phép công cộng GNU GPL là giấy phép điển hình đối với phần mềm nguồn mở. Nó đảm bảo quyền tiếp cận của người sử dụng đối với mã nguồn để dùng, thay đổi hoặc phân phối lại; bảo đảm quyền miễn trừ của các tác giả về hậu quả sử dụng phần mềm; bảo đảm quyền đứng tên của các tác giả tham gia phát triển, đảm bảo sự phát triển bền vững của phần mềm nguồn mở bằng cách công bố rõ ràng các thay đổi của các phiên bản và buộc phân phát triển dựa trên phần mềm nguồn mở theo giấy phép GPL cũng phải mở theo GPL.

## Luyện tập

1. Em hãy cho biết ý nghĩa của yêu cầu "người sửa đổi, nâng cấp phần mềm nguồn mở phải công bố rõ ràng phần nào đã sửa, sửa thế nào so với bản gốc".
2. Ý nghĩa của yêu cầu "phần mềm sửa đổi một phần mềm nguồn mở theo GPL cũng phải mở theo giấy phép của GPL" là gì?

# Bài 2: VAI TRÒ CỦA PHẦN MỀM THƯƠNG MẠI VÀ PHẦN MỀM NGUỒN MỞ

Phần mềm nguồn mở đã trở thành cơ hội cho những ai muốn có những giải pháp phần mềm tốt với đầu tư thấp. Đến nay, hầu như lĩnh vực nào của tin học cũng có các phần mềm nguồn mở có thể thay thế được các phần mềm nguồn đóng.

## Hoạt động 3 Vai trò của phần mềm thương mại và phần mềm nguồn mở

Hãy thảo luận xem phần mềm nguồn mở có thay thế hoàn toàn được phần mềm thương mại hay không? Tại sao?

Phần mềm thương mại có hai loại:
*   Phần mềm **“đặt hàng”** (phần mềm “may-đo”) được thiết kế theo yêu cầu của từng khách hàng. Ví dụ phần mềm điều khiển một dây chuyền lắp ráp hay phần mềm đặt xe trên thiết bị di động của các hãng taxi là các ví dụ về phần mềm đặt hàng. Điều quan trọng là phần mềm đặt hàng không những được thiết kế chính xác theo yêu cầu, mà còn được bảo hành theo hợp đồng.
*   Phần mềm **“đóng gói”** được thiết kế dựa trên những yêu cầu chung của nhiều người. Chúng được viết rất hoàn chỉnh và kèm theo công cụ cài đặt tự động giúp người dùng dễ sử dụng. Người bán không có trách nhiệm sửa chữa nâng cấp theo yêu cầu của từng người dùng nhưng có thể nâng cấp định kì. Phần mềm xử lí ảnh Photoshop, phần mềm soạn thảo văn bản Microsoft Word là các ví dụ về phần mềm thương mại đóng gói.

Rõ ràng là phần mềm nguồn mở không thể thay thế được cho phần mềm thương mại trong thực tế. Mỗi phần mềm nguồn mở đáp ứng nhu cầu chung của nhiều người, trong khi đó những nhu cầu riêng, vốn phong phú hơn rất nhiều so với những nhu cầu chung thì phần mềm “đặt hàng” mới có thể đáp ứng được.

Một điều quan trọng là chính các phần mềm thương mại mới đem lại nguồn tài chính chủ yếu để duy trì các tổ chức làm phần mềm.

Cần lưu ý, **phần mềm thương mại** liên quan đến những giải pháp riêng của người cung cấp, nên người dùng dễ bị lệ thuộc vào nhà cung cấp cả về giải pháp cũng như hỗ trợ kĩ thuật.

1.  Ưu điểm của **phần mềm thương mại**:
    *   **Phần mềm** dạng “**đặt hàng**” đáp ứng nhu cầu riêng và người dùng được hỗ trợ kĩ thuật.
    *   **Phần mềm** “**đóng gói**” có tính hoàn chỉnh cao, đáp ứng nhu cầu rộng rãi.
2.  Ưu điểm của **phần mềm nguồn mở**: chi phí thấp, minh bạch, không bị phụ thuộc nhiều vào nhà cung cấp.
3.  Vai trò của hai loại **phần mềm**:
    *   **Phần mềm thương mại** là nguồn thu nhập chính của các tổ chức, cá nhân làm phần mềm chuyên nghiệp, góp phần tạo ra thị trường phần mềm phong phú, đáp ứng các nhu cầu riêng của cá nhân, tổ chức và các nhu cầu chung của xã hội.
    *   **Phần mềm nguồn mở** giúp những người có nhu cầu được sử dụng phần mềm dùng chung chất lượng tốt, ổn định với chi phí thấp.

## Luyện tập

1.  Cho ví dụ về **phần mềm đóng gói** và **phần mềm đặt hàng**. Ưu điểm của **phần mềm thương mại** là gì?
2.  Cho ví dụ về một **phần mềm thương mại** và một **phần mềm nguồn mở** có thể thay thế. Ưu điểm của **phần mềm nguồn mở** là gì?

## 3. PHẦN MỀM CHẠY TRÊN INTERNET

### Hoạt động 4 Phần mềm chạy trên Internet

**Phần mềm chạy trên Internet** là gì? Em hãy cho một ví dụ về phần mềm như vậy. Hãy nêu ưu điểm của **phần mềm chạy trên Internet**.

Phần mềm chạy trên Internet được hiểu là phần mềm cho phép sử dụng qua Internet mà không cần phải cài đặt vào máy.

Phần mềm chạy trên Internet (**phần mềm trực tuyến**) rất phổ biến, chẳng hạn phần mềm mạng xã hội, thư điện tử và các ứng dụng mua sắm trên mạng,... Lợi ích của các phần mềm này là có thể sử dụng ở bất cứ đâu, bất cứ nơi nào, bất cứ máy tính nào miễn là có kết nối Internet, chi phí rẻ hoặc không mất phí.

Ví dụ: Google cung cấp nhiều phần mềm trực tuyến, trong đó phần mềm Google Docs giúp soạn thảo văn bản, Google Sheets giúp tạo lập các bảng tính, Google Slides giúp trình chiếu trực tuyến có thể thay thế cho Word, Excel hay PowerPoint của Microsoft.

Lưu ý: Để sử dụng được các phần mềm trực tuyến của Google, cần có tài khoản Google và truy cập trang docs.google.com, sheets.google.com, slides.google.com.

Ví dụ khi truy cập trang docs.google.com để soạn thảo văn bản, em sẽ nhận được trang màn hình, phía trên là các mẫu văn bản, phía dưới là các văn bản của em đã soạn từ trước, nếu có. Nếu muốn sửa văn bản đã có thì chỉ cần nháy chuột chọn văn bản đó, còn nếu muốn tạo mới thì nháy chuột chọn biểu tượng +. Em có thể soạn thảo tương tự như Word. Văn bản được lưu tự động trên không gian lưu trữ của em trên đám mây của Google.

## KẾT NỐI TRI THỨC

1. Em hãy nêu những ưu điểm của phần mềm chạy trên Internet.
2. Em hãy nêu tên một phần mềm trực tuyến khác với các phần mềm đã nêu trong bài.

## LUYỆN TẬP

1. Có thể nói "Phần mềm nguồn mở ngày càng phát triển thì thị trường phần mềm thương mại càng suy giảm" hay không? Tại sao?
2. Phần mềm ở các trạm ATM (rút tiền tự động) có phải là phần mềm trực tuyến không?

## VẬN DỤNG

1. Em hãy tìm trên Internet và cho biết tên một số phần mềm đồ hoạ nguồn mở và một số phần mềm đồ hoạ thương mại.
2. Nói chung, các môi trường lập trình trên ngôn ngữ Python đều không có chức năng biên dịch để chuyển mã nguồn thành mã máy. Các chương trình Python đều ở dạng mã nguồn. Liệu có thể coi mọi phần mềm viết bằng Python đều là phần mềm nguồn mở hay không?
