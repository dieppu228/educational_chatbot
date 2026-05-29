# Bài 1: HỆ ĐIỀU HÀNH

## Sau bài học này em sẽ

*   Trình bày được sơ lược lịch sử phát triển của các hệ điều hành thông dụng cho PC.
*   Chỉ ra được một số đặc điểm của hệ điều hành cho thiết bị di động.
*   Trình bày được một cách khái quát mối quan hệ giữa phần cứng, hệ điều hành và phần mềm ứng dụng cũng như vai trò của mỗi thành phần trong hoạt động chung của cả hệ thống.

Khi chưa có hệ điều hành, con người phải can thiệp vào hầu hết quá trình hoạt động của máy tính nên hiệu quả khai thác sử dụng máy tính rất thấp. Sự ra đời của hệ điều hành đã giúp khắc phục được tình trạng đó. Việc sử dụng máy tính về cơ bản được thực hiện thông qua hệ điều hành. Em hãy chỉ ra một số công việc mà hệ điều hành thực hiện.

## 1. LỊCH SỬ PHÁT TRIỂN CỦA HỆ ĐIỀU HÀNH MÁY TÍNH CÁ NHÂN

### Hoạt động 1 Tìm hiểu các chức năng của hệ điều hành

Hệ điều hành của các loại máy tính nói chung có năm nhóm chức năng sau:
*   Quản lí thiết bị (**CPU**, bộ nhớ hay **thiết bị ngoại vi**).
*   Quản lí việc lưu trữ dữ liệu (quản lí tệp và thư mục).
*   Tổ chức thực hiện các chương trình, điều phối tài nguyên cho các tiến trình xử lí trên máy tính. Nói cách khác, hệ điều hành là môi trường để chạy các ứng dụng.
*   Cung cấp môi trường giao tiếp với người sử dụng.
*   Cung cấp một số tiện ích giúp nâng cao hiệu quả sử dụng máy tính như định dạng đĩa, nén tệp, kiểm tra lỗi đĩa cứng, cấu hình kết nối mạng,...

Theo em, nhóm chức năng nào thể hiện rõ nhất đặc thù của hệ điều hành máy tính cá nhân?

Khác với các máy chủ, siêu máy tính do kĩ sư vận hành, máy tính cá nhân dành cho người dùng phổ thông nên sự thân thiện, dễ sử dụng là tiêu chí quan trọng nhất. Quá trình hình thành và phát triển của hệ điều hành máy tính cá nhân có liên quan chặt chẽ tới tiêu chí này và được thể hiện ở hai điểm chính sau:

*   Giao diện đồ họa.
*   Cơ chế "**plug & play**" để tự động nhận biết thiết bị ngoại vi khi khởi động máy tính.

Có thể nói cơ chế **plug & play** ("cắm và chạy", còn được hiểu là "cắm vào là chạy") là bước phát triển hết sức quan trọng của hệ điều hành máy tính cá nhân. Thời kì đầu, thiết bị ngoại vi khi kết nối gặp nhiều khó khăn cho người sử dụng, bởi lẽ mỗi thiết bị ngoại vi của một hãng đòi hỏi phải có một phần mềm điều khiển riêng, việc cài đặt không phải luôn dễ dàng với những người ít hiểu biết về tính năng của thiết bị ngoại vi và hoạt động của nó. Cơ chế plug & play giúp hệ điều hành nhận biết các thiết bị ngoại vi ngay khi khởi động máy và có thể hỗ trợ cài đặt các chương trình điều khiển một cách tự động.

Về giao diện, ban đầu hệ điều hành máy tính cá nhân sử dụng giao diện dòng lệnh, người dùng phải gõ các lệnh, chẳng hạn trong hệ điều hành DOS, lệnh:

`erase C:\dulieu\danhsach.txt`

sẽ xóa tệp `danhsach.txt` nằm trong thư mục `dulieu` của ổ đĩa C. Mặc dù đơn giản, nhưng DOS thiếu tính trực quan, đòi hỏi người dùng phải nhớ cú pháp của từng câu lệnh.

Bước phát triển tiếp theo của hệ điều hành là sử dụng giao diện đồ họa với các đối tượng thể hiện bằng hình ảnh. Một số thành phần cơ bản của giao diện đồ họa bao gồm:

*   **Cửa sổ** là một vùng hình chữ nhật trên màn hình dành cho một ứng dụng. Cửa sổ có thể phóng to, thu nhỏ, ẩn đi hoặc đóng lại.
*   **Biểu tượng** dễ gợi nhớ, cho phép quan sát đối tượng dưới dạng đồ họa.
*   **Chuột** là phương tiện chỉ định điểm làm việc trên màn hình thể hiện bởi một con trỏ màn hình.

Giao diện đồ họa có tính trực quan, giúp người sử dụng giao tiếp với máy dễ dàng hơn. Các hệ điều hành cho máy tính cá nhân ngày càng càng thân thiện, một số hệ điều hành đã hỗ trợ giao tiếp bằng giọng nói.

Hai dòng máy tính cá nhân chủ đạo là dòng Mac (MacBook, iMac) sử dụng hệ điều hành đồ họa macOS của Apple và dòng PC sử dụng hệ điều hành đồ họa Windows của Microsoft. Sau đây chúng ta sẽ tìm hiểu kĩ hơn lịch sử phát triển của một hệ điều hành thương mại và một hệ điều hành nguồn mở phổ biến nhất.

### a) Hệ điều hành Windows

Windows đã trải qua nhiều phiên bản. Sau đây là một số phiên bản quan trọng, đánh dấu các mốc phát triển của Windows:

*   Phiên bản 1 của Windows phát hành vào năm 1985 với giao diện đồ họa.
*   Phiên bản 3, phát hành năm 1990 bắt đầu có khả năng đa nhiệm, cho phép chạy nhiều chương trình đồng thời, giúp nâng cao hiệu quả máy tính. Chức năng kéo thả tiện lợi bắt đầu có từ phiên bản 3.1. Các tính năng làm việc với mạng bắt đầu có từ phiên bản 3.11.

*   Trong vòng 10 năm đầu, về cơ bản Windows chỉ là một vỏ bọc đồ hoạ và từ đó gọi các dịch vụ của DOS. Chỉ từ phiên bản Windows 95 (1995) nhiều tính năng cơ bản của hệ điều hành mới được tích hợp trực tiếp vào Windows. Không những thế Windows 95 còn có giao diện đẹp, giao tiếp tiện lợi. Nhiều công cụ bắt đầu có từ phiên bản này hiện nay vẫn được dùng như bảng chọn Start, thanh trạng thái Taskbar và biểu tượng shortcut. Cơ chế plug & play lần đầu tiên được sử dụng.
*   Năm 2001, Microsoft phát hành Windows XP với nhiều cải tiến đáng kể về giao diện và hiệu suất làm việc với một nâng cấp quan trọng để chạy trên các bộ xử lí tiên tiến thế hệ 64 bit. Đây là một trong các phiên bản hệ điều hành thành công nhất của Microsoft với số người sử dụng rất lớn.
*   Các phiên bản Windows 7 (2009), Windows 8 (2012) Windows 10 (2015) và Windows 11 (2021) là một thế hệ hệ điều với những thay đổi lớn so với Windows XP về độ an toàn, ổn định và hiệu quả sử dụng tài nguyên. Chúng dễ dùng hơn và hầu như không còn lỗi bất thường như các phiên bản trước.

Windows gần như thống trị thị trường hệ điều hành máy tính cá nhân. Một thống kê vào năm 2018 cho thấy hơn 86% người dùng máy tính sử dụng Windows.

### b) Hệ điều hành LINUX và các phiên bản

LINUX có nguồn gốc từ hệ điều hành UNIX – một hệ điều hành đa nhiệm (có thể chạy đồng thời nhiều chương trình) và đa người dùng (nhiều người có thể làm việc đồng thời) được phát triển từ 1969. UNIX đã chứng tỏ được tính hiệu quả, ổn định và an toàn cao. Phần lớn các phiên bản UNIX thương mại đều có giá thành khá cao.

Ý tưởng xây dựng một hệ điều hành kiểu UNIX chạy trên các máy tính cá nhân được quan tâm từ giữa những năm 1980 nhưng chỉ thực sự thành công với hệ điều hành LINUX, do Linus Torvalds viết vào năm 1991. Phiên bản LINUX 1.0 được công bố chính thức năm 1994 dưới dạng mã nguồn mở cho phép bất cứ ai cũng có thể sử dụng và phát triển thêm. LINUX đã khởi đầu trào lưu phần mềm nguồn mở, có ảnh hưởng rất lớn đến sự phát triển của công nghệ thông tin sau này.

LINUX được cộng đồng người dùng đánh giá cao và sử dụng rộng rãi. LINUX không chỉ dùng cho máy tính cá nhân mà còn dùng cho cả máy chủ và các thiết bị nhúng – các thiết bị có phần mềm được tích hợp vào phần cứng và được thiết kế riêng như ti vi, xe ô tô tự lái,...

Đối với máy tính cá nhân, đã có nhiều biến thể khác nhau ra đời từ LINUX như RedHat (viết năm 1994 và phát hành rộng rãi năm 1999), Suse (1996), Ubuntu (2004), thậm chí hệ điều hành Android của phần lớn điện thoại di động cũng được xây dựng trên lõi của LINUX.

## Tóm tắt bài học
Các hệ điều hành máy tính cá nhân phát triển theo hướng ngày càng dễ sử dụng, thể hiện ở các điểm sau:
*   Giao diện thân thiện, từ giao diện dòng lệnh chuyển sang giao diện đồ hoạ và tích hợp với nhận dạng tiếng nói.
*   Khả năng nhận biết các thiết bị ngoại vi với cơ chế plug & play giúp người sử dụng không cần quan tâm tới trình điều khiển của thiết bị ngoại vi.

Các hệ điều hành thông dụng nhất trên máy tính cá nhân là MacOS trên dòng máy MAC và Windows trên dòng máy PC. Đặc biệt Linux và các biến thể của nó như RedHat, Suse hay Ubuntu là hệ điều hành nguồn mở, mang đến cho người dùng các hệ điều hành mạnh mẽ, tin cậy và chi phí thấp.

## Luyện tập
1. Nêu các nhóm chức năng chính của hệ điều hành.
2. Nêu các đặc điểm cơ bản của hệ điều hành máy tính cá nhân.

## 2. HỆ ĐIỀU HÀNH CHO THIẾT BỊ DI ĐỘNG

### Hoạt động 2 Một số đặc điểm của hệ điều hành cho thiết bị di động

Điện thoại thông minh, máy tính bảng (gọi chung là thiết bị di động) thực chất là các máy tính cá nhân. Sự khác nhau giữa hệ điều hành cho thiết bị di động và hệ điều hành của máy tính có nguồn gốc từ sự khác biệt về tính năng, tác dụng của hai loại thiết bị này. Hãy cùng thảo luận để chỉ ra những điểm khác nhau đó.

Ra đời sau máy tính nhưng điện thoại thông minh và máy tính bảng được phổ cập nhanh, thúc đẩy mạnh mẽ tiến trình tin học hoá xã hội.
Điện thoại thông minh không chỉ dùng để nghe, gọi mà còn được trang bị rất nhiều tiện ích như chụp ảnh, quay phim, định vị, ghi nhận tình trạng sức khoẻ.
Do tính di động mà hệ điều hành cho thiết bị di động chú trọng đến khả năng kết nối mạng không dây như wifi, Internet di động (dịch vụ 3G, 4G, 5G,...), bluetooth hay giao tiếp gần NFC.
Các thiết bị di động phần lớn nhỏ, gọn và giao tiếp phổ biến nhờ các thao tác vuốt, chạm, lắc,... Chúng thường được trang bị màn hình cảm ứng, bàn phím ảo và nhiều cảm biến để tạo các giao tiếp hay ứng dụng độc đáo.
Có nhiều hệ điều hành cho các thiết bị di động nhưng phổ biến hơn cả là iOS của Apple dùng cho iPhone, iPad và Android của Google dùng cho hầu hết các dòng điện thoại khác.

Một số khác biệt của hệ điều hành cho thiết bị di động so với hệ điều hành cho máy cá nhân:
* Giao diện đặc biệt thân thiện nhờ nhận dạng hành vi của người dùng thông qua các cảm biến.
* Dễ dàng kết nối mạng di động.
* Nhiều tiện ích hỗ trợ cá nhân.
* Hai hệ điều hành phổ biến cho thiết bị di động là iOS của Apple và Android của Google.

1. Vì sao hệ điều hành di động ưu tiên cao cho giao tiếp thân thiện và kết nối mạng di động?
2. Kể tên ba tiện ích thường có trên thiết bị di động và chức năng của nó.
