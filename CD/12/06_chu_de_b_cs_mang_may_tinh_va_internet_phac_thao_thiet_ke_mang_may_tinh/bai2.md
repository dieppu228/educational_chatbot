# Bài 2: THIẾT BỊ MẠNG

Học xong bài này, em sẽ:
*   Nhận diện hình dạng và phân biệt được chức năng của các thiết bị mạng: Switch, Router, Access Point, Modem, Server.

Theo em, các thiết bị như điện thoại, laptop, máy tính có thể kết nối tới Internet bằng cách nào?

## 1. Switch

Hãy miêu tả thiết bị trung tâm được tất cả các máy tính trong phòng thực hành Tin học của trường em kết nối tới.

**Switch** hay còn gọi là **bộ chuyển mạch** được sử dụng để kết nối nhiều thiết bị khác nhau trong một mạng LAN. Switch có thể được sử dụng trong các mạng gia đình, mạng văn phòng hoặc mạng trong cùng một toà nhà. Các thông số kĩ thuật chính khi lựa chọn Switch bao gồm:
*   Số lượng cổng kết nối: có thể là 4, 8, 16, 24, 48 cổng.
*   Công nghệ kết nối và tốc độ truyền tải dữ liệu: Fast Ethernet (lên tới 100 Mbps), Gigabit Ethernet (lên tới 1 000 Mbps), Ten Gigabit Ethernet (lên tới 10 000 Mbps).
Ngoài ra, còn một số thông số kĩ thuật của Switch như: bộ nhớ RAM, bộ nhớ Flash, kích thước, trọng lượng,... Ví dụ, một số thông số kĩ thuật của Switch Catalyst 2960 được trình bày trong Bảng 1.

Bảng 1. Một số thông số kĩ thuật của Switch Catalyst 2960
*   Dòng sản phẩm: Catalyst 2960
*   Mã sản phẩm: WS-C2960+48TC-S
*   Tổng số cổng kết nối: 48
*   Tốc độ: 100 Mbps
*   Bộ nhớ RAM: 128 MB
*   Bộ nhớ Flash: 64 MB
*   Kích thước: 4.4cm × 45.0 cm × 24.2 cm
*   Trọng lượng: 8.0 kg

Trong thiết kế mạng LAN, Switch được lựa chọn để phù hợp với yêu cầu về tốc độ và số lượng thiết bị người dùng. Ví dụ, để thiết kế mạng LAN cho một văn phòng

có 10 chiếc máy tính sử dụng cổng kết nối có dây thì có thể chọn Switch có ít nhất 12 cổng kết nối. Trong quá trình thiết kế mạng, để vẽ sơ đồ kết nối giữa các thiết bị, ta dùng kí hiệu Switch.

Để chuyển tiếp dữ liệu qua các cổng kết nối, Switch xây dựng một **bảng chuyển mạch**, hay còn gọi là **bảng địa chỉ MAC**, để lưu trữ thông tin địa chỉ MAC của các thiết bị kết nối trực tiếp tới Switch.

**Bảng địa chỉ MAC** trên chứa hai hàng, mỗi hàng là địa chỉ MAC của một thiết bị kết nối trực tiếp với Switch. Các cột trong bảng MAC có ý nghĩa như sau:
*   **Địa chỉ MAC** là địa chỉ của thiết bị kết nối trực tiếp với Switch.
*   **Cổng** là số của cổng kết nối trên Switch mà thiết bị đã kết nối tới.

Khi nhận được một gói tin, Switch sẽ kiểm tra địa chỉ MAC của gói tin và tìm kiếm trong bảng địa chỉ MAC để xác định cổng đích mà gói tin cần được gửi đến. Nếu địa chỉ MAC của gói tin không có trong bảng địa chỉ MAC, Switch sẽ chuyển tiếp gói tin qua tất cả các cổng ngoại trừ cổng mà nó đã nhận được gói tin.

**Địa chỉ MAC** là một dãy số 12 kí tự được biểu diễn bằng 6 cặp số khác nhau trong hệ thập lục phân (dãy số từ 0 – 9, A – F) và được ngăn cách nhau bằng dấu hai chấm hoặc dấu gạch nối (ví dụ: CC:46:D6:F1:F1:C6 hoặc CC-46-D6-F1-F1-C6). Trong đó, 6 kí tự đầu tiên định danh cho nhà sản xuất thiết bị hay còn gọi là **OUI (Organizationally Unique Identifier)**, 6 kí tự tiếp theo đại diện cho bộ giao tiếp mạng **NIC (Network Interface Card)** được gán bởi nhà sản xuất. Mỗi cổng kết nối mạng chỉ có một địa chỉ MAC duy nhất và riêng biệt. Ví dụ: Máy tính

xách tay có hai cổng kết nối có dây và không dây thì có hai địa chỉ MAC tương ứng; mỗi cổng kết nối trên Switch có một địa chỉ MAC riêng.

## Router

**Router** hay còn gọi là bộ định tuyến được sử dụng để kết nối nhiều mạng cho phép trao đổi dữ liệu giữa các thiết bị ở các mạng LAN khác nhau. Các thông số kĩ thuật chính để lựa chọn Router bao gồm:
*   Số lượng cổng kết nối: có thể là 2 hoặc 4 cổng để kết nối với các mạng khác nhau.
*   Tốc độ truyền dữ liệu: có thể lên tới 100 Mbps hoặc hàng chục Gbps.
*   Chuẩn kết nối: Router có thể hỗ trợ nhiều chuẩn kết nối mạng khác nhau như Ethernet, Wi-Fi, 3G/4G.

Ngoài ra, còn một số thông số kĩ thuật của Router như: bộ nhớ RAM, bộ nhớ Flash, kích thước, trọng lượng,... Ví dụ, một số thông số kĩ thuật của Router CISCO2921/k9 được trình bày trong Bảng 3.

Bảng 3. Một số thông số kĩ thuật của Router CISCO2921/k9
*   Dòng sản phẩm: Router
*   Mã sản phẩm: CISCO2921/k9
*   Tổng số cổng Ethernet: 4
*   Tốc độ: 10/100/1000 Mbps
*   Bộ nhớ RAM: 512 MB (installed)/2 GB (max)
*   Bộ nhớ Flash: 256 MB (installed)/8 GB (max)
*   Kích thước: 47 cm × 43.8 cm × 8.9 cm
*   Trọng lượng: 18.93 kg

Ví dụ: Khi thiết kế mạng cho một toà nhà 5 tầng, mỗi tầng tương ứng với một mạng LAN bao gồm 15 máy tính để bàn và 1 Switch có 24 cổng mạng, trong đó Switch là thiết bị kết nối tới các máy tính; Switch của mỗi tầng sẽ được kết nối với nhau và được kết nối tới Router. Tiếp theo, Router được cài đặt giao thức định tuyến cho phép các mạng LAN có thể truy cập mạng Internet hoặc kết nối giữa các mạng cục bộ với nhau.

Hình 3a là hình ảnh thực tế của một số Router và Hình 3b là kí hiệu Router khi vẽ sơ đồ mạng. So với các loại Switch thì Router có ít cổng kết nối hơn. Các gói tin trao đổi giữa các mạng sẽ được chuyển tiếp qua Router. Mỗi gói tin sẽ được định danh bởi địa chỉ IP của máy gửi và máy nhận.

Để chuyển tiếp gói tin giữa các mạng với nhau, **Router** xây dựng một **bảng định tuyến** cho phép lưu trữ thông tin về các đường đi mà Router có thể sử dụng để chuyển tiếp các gói tin đến địa chỉ đích. Bảng định tuyến được cập nhật định kì để đảm bảo Router luôn biết được đường đi tốt nhất đến các mạng khác.

Minh hoạ về bảng định tuyến đơn giản:
*   Địa chỉ mạng đích: 10.11.0.0/16, Địa chỉ cổng chuyển tiếp: 10.1.1.2, Giao diện/Cổng: Eth1
*   Địa chỉ mạng đích: 10.12.0.0/16, Địa chỉ cổng chuyển tiếp: 10.2.2.2, Giao diện/Cổng: Eth2
*   Địa chỉ mạng đích: 10.13.0.0/16, Địa chỉ cổng chuyển tiếp: 10.3.3.3, Giao diện/Cổng: Eth3

Bảng định tuyến trên chứa ba hàng, mỗi hàng là một đường đi đến một mạng khác nhau. Các cột trong bảng định tuyến có ý nghĩa như sau:
*   Địa chỉ mạng đích là địa chỉ mạng mà đường đi này áp dụng.
*   Địa chỉ cổng chuyển tiếp là địa chỉ IP của Router kế tiếp để chuyển tiếp gói tin đến đích. Nếu đích là một mạng trực tiếp kết nối thì đây sẽ là địa chỉ IP của thiết bị đó.
*   Giao diện/Cổng là cổng kết nối trên Router mà gói tin sẽ được chuyển tiếp để đến đích.

Khi nhận được một gói tin, Router sẽ kiểm tra địa chỉ máy nhận của gói tin và tìm kiếm trong bảng định tuyến nhằm xác định đường đi tốt nhất để chuyển tiếp gói tin đến. Router sẽ sử dụng địa chỉ IP của giao diện và địa chỉ IP của Router tiếp theo (next-hop) để chuyển tiếp gói tin đến đích. Nếu không có thông tin nào tìm được trong bảng định tuyến có thể áp dụng cho địa chỉ máy nhận của gói tin thì Router sẽ chuyển tiếp gói tin này đến cổng mặc định đã được cài đặt trước.

## Access Point

**Access Point (AP** hay còn gọi là điểm truy cập không dây) là một thiết bị mạng được trang bị các bộ giao tiếp mạng có dây và không dây (xem lại Chủ đề B, Bài 1). Bộ giao tiếp mạng không dây của AP được trang bị ăng-ten để thu phát sóng vô tuyến. Tuy nhiên, do thiết kế của nhà sản xuất mà ăng-ten có thể được giấu bên trong hộp hoặc để bên ngoài. Trong quá trình thiết kế sơ đồ mạng, kí hiệu AP có thể được sử dụng.

Trong điều kiện bình thường và ít vật cản, trung bình AP có phạm vi phủ sóng Wi-Fi tối đa trong khoảng từ 30 m đến 50 m. Phạm vi này phụ thuộc rất lớn vào các yếu tố khách quan khác như: chuẩn Wi-Fi, số lượng ăng-ten, công suất phát sóng, vật cản xung quanh thiết bị.
Các chuẩn Wi-Fi được phát triển bởi Viện Kĩ sư Điện và Điện tử IEEE có những đặc điểm chính.

Ngoài hỗ trợ kết nối không dây, một số AP còn có các cổng kết nối có dây như cổng kết nối LAN và cổng kết nối WAN. Các cổng kết nối LAN được dùng để chia sẻ mạng với các thiết bị đầu cuối kết nối tới AP. Trong trường hợp này, AP đóng vai trò như một Switch. Ngoài ra, AP có thêm cổng kết nối WAN được dùng để kết nối tới mạng khác, ví dụ như Internet. Do đó, một AP cũng có chức năng của một bộ định tuyến và được gọi là Router Wi-Fi.

## Modem

Để có thể sử dụng Internet, cần phải đăng kí gói cước với nhà mạng hay còn gọi là nhà cung cấp dịch vụ Internet (ISP). Để kết nối tới nhà cung cấp dịch vụ Internet, cần có một thiết bị không thể thiếu là **Modem**.

Modem thực hiện chức năng truyền và nhận dữ liệu từ ISP, sau đó Router sẽ nhận và truyền dữ liệu từ Modem đến các thiết bị sử dụng Internet thông qua dây cáp hoặc sóng Wi-Fi. Sự khác biệt giữa vai trò của Modem và Router là: Modem có vai trò kết nối Internet từ ISP, còn Router giúp truyền Internet từ Modem sang các thiết bị người dùng như: máy tính, điện thoại, laptop,...

Một Modem sử dụng một trong hai cổng Phone và PON để kết nối tới ISP, các cổng LAN Ports còn lại được dùng để chia sẻ và kết nối mạng cục bộ tới

Internet. Ngoài ra, đây là một ví dụ Modem đặc biệt được tích hợp thêm bộ giao tiếp mạng không dây để trở thành một AP. Với công nghệ ngày nay, cổng ADSL được thay thế bởi cổng cáp quang đảm bảo tốc độ đường truyền nhanh và ổn định hơn. Trong quá trình thiết kế sơ đồ mạng, kí hiệu Modem có thể được sử dụng.

## Server

**Máy chủ** hay **Server** là một thiết bị được sử dụng để lưu trữ và chia sẻ dữ liệu hoặc dịch vụ cho các thiết bị khác trong một mạng máy tính. Một số dịch vụ được máy chủ cung cấp là: lưu trữ dữ liệu, thư điện tử, trang web, trò chuyện trực tuyến,...

Máy chủ đóng vai trò quan trọng trong việc quản lí, lưu trữ thông tin và vận hành phần mềm cho doanh nghiệp. Khi sử dụng, doanh nghiệp có thể tập trung tối ưu hoá phần cứng cho hệ thống máy chủ, giảm đầu tư cho các máy trạm cá nhân khác ngoài máy chủ. Ngay cả đối với người dùng cá nhân, máy chủ cũng đóng vai trò quan trọng trong việc lưu trữ, xử lí và vận hành dữ liệu chính của hệ thống.

* Máy chủ dạng tháp (Tower Server) có kích thước giống như một case máy tính để bàn, được đặt đứng trên một mặt phẳng.

*   Máy chủ dạng rack (Rack Server) là dạng máy chủ được thiết kế đặt trong một giá đỡ. Các máy chủ được xếp chồng lên nhau để tiết kiệm không gian trên mặt đất.
*   Máy chủ Blade (Blade Server) là loại máy chủ có các khay chứa nhiều bảng mạch mô đun tách rời. Máy chủ Blade được thiết kế để tiết kiệm không gian và tối ưu hoá hiệu suất, với các bộ xử lí, bộ nhớ và các thành phần khác được gắn cứng trên các thanh và lắp vào một khung chung.

## Luyện tập

*   **Câu 1.** Hãy phân biệt chức năng của Switch và Router.
*   **Câu 2.** Hãy nêu chức năng của các thiết bị mạng: Access Point, Modem.
*   **Câu 3.** Hãy mô tả đặc điểm của một số loại máy chủ phổ biến.

Một ngôi nhà ba tầng, mỗi tầng có hai máy tính để bàn và một số thiết bị không dây khác. Em hãy đề xuất các thiết bị mạng cần thiết để máy tính và các thiết bị không dây trong nhà có thể truy cập Internet.

Trong các câu sau, những câu nào sai?
*   a) Switch chứa bảng định tuyến để chuyển tiếp các gói dữ liệu.
*   b) Router sử dụng địa chỉ IP của gói tin để xác định cổng chuyển tiếp gói tin.
*   c) Modem và Router là hai thiết bị mạng có cùng chức năng.
*   d) AP là một Router dùng để kết nối mạng không dây và mạng có dây.
*   e) Bảng địa chỉ MAC là bảng định tuyến trong Router.
*   f) Bảng định tuyến chứa địa chỉ IP và địa chỉ MAC.
*   g) Máy chủ được dùng để lưu trữ và chia sẻ dữ liệu.

## Tóm tắt bài học

*   **Switch** được sử dụng để tổ chức một mạng cục bộ, hỗ trợ nhiều cổng kết nối và xây dựng bảng địa chỉ MAC để chuyển tiếp dữ liệu qua các cổng kết nối tới thiết bị.
*   **Router** là thiết bị bị để kết nối các mạng với nhau. Router xây dựng bảng định tuyến để đảm bảo dữ liệu được trao đổi giữa các mạng với nhau.
*   **Modem** là thiết bị để kết nối tới nhà cung cấp dịch vụ Internet.
*   **AP** là thiết bị mạng được sử dụng để tạo mạng cục bộ không dây cho điện thoại, laptop có thể truy cập Internet.
*   **Server** được dùng để lưu trữ và chia sẻ dữ liệu hoặc các dịch vụ trong mạng máy tính như: thư điện tử, lưu trữ dữ liệu, lưu trữ web,...
