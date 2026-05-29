# Bài 6: TRUY VẤN TRONG CƠ SỞ DỮ LIỆU QUAN HỆ (tiếp theo)

Học xong bài này, em sẽ:
*   Đưa ra được một vài ví dụ minh họa cho việc dùng truy vấn để tổng hợp, tìm kiếm dữ liệu trên hơn một bảng.

Theo em, việc khai báo liên kết giữa một số bảng trong một CSDL quan hệ có ý nghĩa gì?

## 1. Câu lệnh truy vấn SQL với liên kết các bảng

1.  Xét CSDL được mô tả như ở Hình 1. Nếu cần biết tên quyển sách mà người có thể thư viện HS-001 đã mượn vào ngày 02/10/2022, ta có thể dùng câu truy vấn trên một bảng được không? Nếu tìm thông tin này bằng cách tra cứu thủ công (không dùng máy tính) thì em sẽ làm như thế nào?

Khi khai thác CSDL quan hệ, nhiều tình huống cần phải kết hợp dữ liệu ở hai hoặc nhiều bảng để đưa ra được dữ liệu cần tìm. Kiểu kết hợp thường gặp là ghép nối một bản ghi của bảng này với một hay nhiều bản ghi của bảng khác tạo nên một hay nhiều bản ghi mới đầy đủ thông tin hơn. Kết quả của các ghép nối là các bản ghi mới được đưa vào một bảng tạm thời. Hệ quản trị CSDL sẽ chọn lựa trong bảng tạm thời này những dữ liệu thoả mãn điều kiện tìm để đưa ra kết quả. Chẳng hạn, để tìm Mã sách của những quyển sách mà học sinh Trần Văn An đã mượn, hệ quản trị CSDL cần kết hợp dữ liệu ở bảng NGƯỜI ĐỌC với dữ liệu ở bảng MƯỢN-TRẢ. Mục đích kết hợp dữ liệu của hai bảng này là để có một bảng dữ liệu tạm thời mà mỗi bản ghi của nó cho ta dữ liệu đúng đắn và đầy đủ gồm Họ và tên, Số thẻ TV,... của một người đọc cùng với Mã sách của quyển sách họ mượn và ngày mượn,... (Hình 2).

Khi kết hợp dữ liệu, hai bản ghi thuộc hai bảng khác nhau trong CSDL chỉ được ghép lại nếu chúng thoả mãn một điều kiện mà ta gọi là **điều kiện kết nối**. Trong tình huống nêu trên, điều kiện kết nối là giá trị ở trường **Số thẻ TV** của hai bản ghi đó phải trùng nhau.

Việc trích rút dữ liệu từ nhiều bảng khác nhau được thực hiện như những truy vấn trên một bảng dữ liệu, đó là bảng dữ liệu tạm thời chứa kết quả kết nối các bản ghi. Trong trường hợp nói đến ở Hình 2, hệ quản trị CSDL chỉ việc lựa chọn dữ liệu trong bảng kết quả kết nối đó để đưa ra “Trần Văn An” đã mượn quyển sách có mã sách “AN-01” và quyển sách có mã sách “TH-02”.

Để kết hợp dữ liệu từ các bảng có trường chung theo cách ghép nối các bản ghi thoả mãn một điều kiện nào đó, SQL sử dụng từ khoá **JOIN** trong mệnh đề **FROM**. Có một số kiểu **JOIN** khác nhau, trong đó **INNER JOIN** được dùng phổ biến nhất. Dưới đây là mẫu viết mệnh đề **FROM** (trong câu truy vấn) sử dụng **INNER JOIN**.

Trong mẫu nêu trên, kí hiệu **Ø** để chỉ bất cứ toán tử so sánh nào: =, <, <=, <>, >, >= (trong đó kí hiệu **<>** thể hiện toán tử so sánh khác). Tuy nhiên, trên thực tế **INNER JOIN** được dùng phổ biến với điều kiện kết nối là sự trùng khớp giá trị trên một trường chung của hai bảng kết nối.

*Ví dụ 1.* Trong một hình minh họa, có một câu truy vấn dùng kết nối hai bảng. Mệnh đề **FROM** yêu cầu kết nối hai bản ghi: một ở bảng **NGƯỜI ĐỌC** và một ở bảng **MƯỢN-TRẢ**. Điều kiện để hai bản ghi được kết nối là giá trị trường **Số thẻ TV** của chúng bằng nhau. Một câu truy vấn SQL mẫu được dùng để tìm mã sách của các quyển sách mà học sinh “Trần Văn An” đã mượn. Thông tin đưa ra gồm có thông tin về Trần Văn An (gồm Họ và tên, Số thẻ TV) và Mã sách của các cuốn sách đã mượn.

Một ví dụ về cấu trúc câu truy vấn SQL sử dụng INNER JOIN:
`SELECT DISTINCT [Họ và tên], [NGƯỜI ĐỌC].[Số thẻ TV], [Mã sách]`
`FROM [NGƯỜI ĐỌC] INNER JOIN [MƯỢN-TRẢ] ON [NGƯỜI ĐỌC].[Số thẻ TV] = [MƯỢN-TRẢ].[Số thẻ TV]`
`WHERE [Họ và tên] = "Trần Văn An"`
Trong đó:
*   Từ khoá **DISTINCT** để quy định: Nếu kết quả có nhiều dòng giống nhau thì chỉ một dòng được đưa vào kết quả.
*   Phần `ON [NGƯỜI ĐỌC].[Số thẻ TV] = [MƯỢN-TRẢ].[Số thẻ TV]` là điều kiện kết nối.

Mỗi giá trị khoá (một **Số thẻ TV**) chỉ xuất hiện trong một bản ghi duy nhất ở bảng **NGƯỜI ĐỌC** nhưng có thể xuất hiện trong nhiều bản ghi ở bảng **MƯỢN-TRẢ**. Do vậy, ta nói quan hệ giữa **NGƯỜI ĐỌC** và **MƯỢN-TRẢ** là quan hệ **một – nhiều**, ý nói một bản ghi trong bảng thứ nhất tương ứng với nhiều bản ghi trong bảng thứ hai và một bản ghi trong bảng thứ hai chỉ tương ứng với một bản ghi trong bảng thứ nhất.
*Chú ý*: Từ khoá **INNER JOIN** nằm giữa tên hai bảng nguồn cho kết nối và từ khoá **ON** đứng ngay trước điều kiện kết nối.

## Kết xuất thông tin bằng báo cáo

Em đã biết, có thể truy vấn CSDL Quản lí học tập 11 để có được thông tin về kết quả học tập của học sinh lớp 11 ở một số môn học. Theo em, với công cụ truy vấn ta có được dữ liệu trình bày như ở một hình minh họa hay không?

Báo cáo CSDL là một văn bản trình bày thông tin kết xuất từ CSDL, có thể xem trực tiếp trên màn hình hoặc in ra. Dữ liệu để đưa vào báo cáo được lấy từ một hay nhiều bảng và truy vấn. Báo cáo trình bày dữ liệu trực quan, làm nổi bật những mục quan trọng và thường theo mẫu quy định. Vì lẽ đó nên nhu cầu xem báo cáo trong công tác quản lí rất lớn.

*Hình 4* là một báo cáo có được từ CSDL của một trường trung học phổ thông ở các ví dụ đã từng nêu. Để có kết quả học tập của học sinh ở một số môn học, ta có thể dùng truy vấn CSDL. Tuy nhiên, dùng hình thức báo cáo thì việc trình bày những thông tin kết xuất được sẽ đạt hiệu quả cao hơn, phù hợp hơn với người cần những thông tin này.

Quan sát một báo cáo ở *Hình 5*, người xem dễ dàng so sánh thực tế mua bán giữa các mặt hàng vì dữ liệu về mỗi mặt hàng được tổng hợp (tính tổng) ở số lượng đã bán và tiền thu được. Rất hữu ích với người làm kinh doanh khi sắp xếp các mặt hàng trong báo cáo theo thứ tự giảm dần của tổng tiền thu được.

Bên cạnh các công cụ tạo biểu mẫu, tạo truy vấn, các hệ quản trị CSDL quan hệ đều cung cấp công cụ tạo báo cáo tự động. Người phát triển ứng dụng CSDL có thể sử dụng công cụ tạo báo cáo tự động rồi tiếp tục chỉnh sửa bố cục, định dạng dữ liệu của báo cáo. Với những ứng dụng CSDL, người phát triển ứng dụng có thể dùng ngôn ngữ lập trình để thiết kế các báo cáo phù hợp với nhu cầu người dùng.

## 3 Thực hành truy vấn trong CSDL quan hệ

Trong CSDL Thư viện được tạo bởi hệ quản trị CSDL Access, giáo viên đã chuẩn bị sẵn một số truy vấn.

a) Em hãy mở xem một truy vấn và chạy thử để biết kết quả.

b) Trong các truy vấn được thiết kế sẵn, em hãy cho biết câu truy vấn nào trả lời cho câu hỏi: Các quyển sách “AI-Trí tuệ nhân tạo” đã được những người nào mượn đọc? Truy vấn đó kết nối những bảng nào của cơ sở dữ liệu? Vì sao em biết điều đó?

Xét CSDL được mô tả. Nếu cần biết tên cuốn sách đã được mượn với ID = 1 trong bảng MUON-TRA, em sẽ viết câu truy vấn như thế nào?

Trong các câu sau, những câu nào đúng?
a) Chỉ có thể viết câu truy vấn SQL trên một bảng của CSDL.
b) Các từ khoá kết nối phải viết trong mệnh đề **FROM** của câu truy vấn SQL.
c) Chỉ có thể kết nối với điều kiện giá trị ở trường chung giữa hai bảng là bằng nhau.
d) Dữ liệu để đưa vào báo cáo được lấy từ một hay nhiều bảng và truy vấn.

## Tóm tắt bài học

*   Để trích rút dữ liệu trong một CSDL quan hệ, có những truy vấn phải thực hiện kết nối dữ liệu của các bảng.
*   Mệnh đề **FROM** có thể chứa từ khoá chỉ định kiểu **JOIN** để thực hiện kết nối các bản ghi ở các bảng khác nhau. **INNER JOIN** là một kiểu kết nối phổ biến.
*   Các hệ quản trị CSDL đều cung cấp công cụ tạo báo cáo tự động và người dùng cũng có thể điều chỉnh bố cục, định dạng báo cáo để nâng cao chất lượng trình bày thông tin.
