# Bài 3: TẠO ẢNH ĐỘNG

Học xong bài này, em sẽ:
* Tạo được ảnh động với hiệu ứng tự thiết kế.
* Tạo được ảnh động từ các hiệu ứng có sẵn trong phần mềm.

Hình 1 minh hoạ một dãy các lớp ảnh tĩnh trong GIMP. Ảnh thứ nhất là hình con bướm đang dang cánh rộng nhất. Ảnh thứ ba là hình con bướm đó với cánh được gập hẹp lại. Ảnh thứ hai và thứ tư là hình nền màu vàng.
Ta sẽ nhìn thấy điều gì nếu dãy ảnh này xuất hiện liên tục, từ ảnh thứ nhất đến ảnh thứ tư rồi quay về ảnh thứ nhất? Tại sao lại cần lớp ảnh nền vàng xen giữa các lớp ảnh hình con bướm?

## 1. Ảnh động, kịch bản và hiệu ứng của ảnh động

Ảnh động được tạo từ các ảnh tĩnh. Các ảnh tĩnh này được gọi là các **khung hình** của ảnh động. Khi ảnh động được kích hoạt, các khung hình xuất hiện trong những khoảng thời gian xác định, làm cho nội dung bên trong ảnh thay đổi liên tục và tạo ra cảm giác đối tượng trong ảnh cử động hoặc chuyển động.
Ví dụ, dãy 4 khung hình trong Hình 1 sẽ tạo được một ảnh động mà đối tượng cử động là con bướm vỗ cánh. Thứ tự các lớp ảnh trong Hình 1e cho thấy con bướm xuất hiện rồi bị che mất ngay bởi nền màu vàng hiện ra ngay sau đó. Như vậy, cách thức xuất hiện của từng khung hình là nó hiện ra rồi biến mất rất nhanh, thời gian xuất hiện của từng khung hình là không đáng kể. Khi xem ảnh động sẽ thấy con bướm này vỗ cánh liên tục.

Để xem được con bướm vỗ cánh chậm hơn, cần chỉ rõ thời gian xuất hiện của từng khung hình trong các ngoặc đơn và sau tên lớp ảnh, đúng như mẫu mô tả ở Hình 2. Với mẫu mô tả này, cách thức và thời gian xuất hiện của các khung hình là: từng hình con bướm xuất hiện 500 ms, thời gian để mỗi hình này xuất hiện trở lại là 50 ms.

Trong ví dụ trên, “vỗ cánh” được xem là hiệu ứng của ảnh động. Để tạo được hiệu ứng này cần xây dựng các lớp ảnh tĩnh như chỉ ra ở Hình 1 và mô tả kịch bản như ở Hình 2.
Kịch bản hoạt động của đối tượng trong ảnh động được thể hiện qua các khung hình. Hai khung hình liên tiếp biểu thị sự thay đổi (động tác, cử chỉ, trạng thái, vị trí...) trong cùng một hành động của đối tượng. Nếu sự thay đổi này sai khác quá nhiều thì chuyển động của ảnh động sẽ bị giật, ngược lại thì chuyển động đó sẽ mềm mại hơn. Do đó, càng nhiều khung hình biểu thị một hành động của đối tượng thì chuyển động của ảnh động càng mềm mại. Ví dụ, xét ảnh động biểu thị hiệu ứng “trượt dốc” với các khung hình được cho ở Hình 3: Nếu ảnh chỉ có hai khung hình đầu và cuối thì chuyển động của ảnh động sẽ bị giật, nếu ảnh có đủ 4 khung hình thì chuyển động sẽ mềm mại hơn.

## 2. Tạo ảnh động với hiệu ứng tự thiết kế trong GIMP

Tương tự như kịch bản cho hiệu ứng “vỗ cánh” được giới thiệu trên đây, em hãy đề xuất ý tưởng kịch bản cho một hiệu ứng khác, ví dụ hiệu ứng “chữ chạy”, “lá rơi”, “tải dữ liệu”,...

Các bước chung để tạo ảnh động với hiệu ứng tự thiết kế trong GIMP như sau:
### Bước 1. Chuẩn bị các ảnh tĩnh cho ảnh động
Với vai trò là các khung hình của ảnh động, các ảnh tĩnh đã chọn phải giúp xây dựng được kịch bản cho việc tạo hiệu ứng. Ví dụ, từ dãy ảnh tĩnh trong Hình 1, có thể tạo kịch bản cho hiệu ứng vỗ cánh.
Với ảnh tĩnh có sẵn, thường phải chỉnh sửa lại. Ví dụ, sau khi sưu tầm được ảnh con bướm, nó được tách khỏi nền và đổi lại nền ảnh màu vàng để nhận được kết quả như ở Hình 1a. Ảnh này được sao chép và dùng công cụ **Perspective** để co ảnh như ở Hình 1c.

Có thể tự thiết kế hoặc sưu tầm các ảnh tĩnh. Với ảnh có sẵn, thường phải chỉnh sửa lại, chẳng hạn như: tách ảnh khỏi nền, cắt ảnh, biến đổi ảnh, tẩy xoá các chi tiết thừa.

Ví dụ, ảnh con bướm có thể tự thiết kế như ở Hình 4a hoặc sưu tầm được như ở Hình 4b. Sau đó, tách ảnh khỏi nền trắng và đổi lại nền ảnh như ở Hình 1a, dùng công cụ Perspective để co ảnh như ở Hình 1c.

### Bước 2. Xây dựng kịch bản cho hiệu ứng của ảnh động

Ở bước này, cần tưởng tượng ra hoạt động của đối tượng, từ đó tạo nội dung cho từng khung hình cùng với thứ tự và thời gian xuất hiện của chúng.

Ví dụ, hiệu ứng vỗ cánh được thể hiện bởi hai trạng thái dang rộng và thu nhỏ của đôi cánh. Mặt khác, do có hiện tượng lưu ảnh trong võng mạc của mắt người nên khi hình thứ hai của con bướm xuất hiện, mắt người vẫn đồng thời nhìn thấy cả hình thứ nhất của con bướm đó trong 0,04 giây đầu tiên. Để tránh hiện tượng này cần có một “ảnh che” (có màu nền trùng với màu nền ảnh trước đó) xuất hiện trước khi ảnh tiếp theo của con bướm hiện ra. Từ đó, cần tạo dãy 4 khung hình và thứ tự của chúng như ở Hình 1. Hơn nữa, quy định lại thời gian xuất hiện cho từng khung hình như mẫu mô tả ở Hình 2. Trong trường hợp có nhiều khung hình, ví dụ như ở Hình 3, có thể không cần các ảnh che.

Nếu các ảnh tĩnh được chuẩn bị là các tệp ảnh độc lập. Nên mở ảnh tĩnh ứng với khung hình thứ nhất, sau đó mở các ảnh còn lại như một lớp ảnh mới bằng lệnh **File\Open As Layers**.

### Bước 3. Xuất ảnh động

Bật từng lớp ảnh để kiểm tra lại từng khung hình, chẳng hạn kiểm tra xem ảnh có trùng khít với khung ảnh không và các lớp ảnh có kích thước giống nhau không.

Thực hiện lệnh **File\Export As** để mở hộp thoại Export Image (Hình 5), nhập tên tệp ảnh động với đuôi tệp là “.gif” và nhấn phím **Enter**.

Hộp thoại Export Image as GIF xuất hiện ngay sau đó. Nháy chuột chọn ô **As animation** rồi nhấn phím Enter hoặc lệnh Export để xuất dãy khung hình ra một tệp ảnh động (định dạng GIF). Bây giờ có thể mở tệp ảnh động này để xem kết quả.

Chú ý: Trước khi thực hiện Bước 3, có thể xem trước ảnh động bằng lệnh **Filters\Animation\Playback**. Hộp thoại Animation Playback xuất hiện. Có thể sử dụng các lệnh điều hướng như Step back, Step để xem ảnh động, từ đó cân nhắc điều chỉnh thời gian cho từng khung hình.

## Tạo ảnh động từ hiệu ứng có sẵn trong GIMP

Lệnh **Filters\Animation** của GIMP cung cấp một số hiệu ứng để tạo ảnh động. Hãy khám phá các hiệu ứng có sẵn này trong GIMP để tạo ảnh động.

Trong trường hợp nội dung hai khung hình liên tiếp không biểu thị hành động của đối tượng thì nên tạo ảnh động dựa trên hiệu ứng có sẵn trong GIMP. Ví dụ, từ ba ảnh về một cảnh ở Mộc Châu, Sơn La có thể tạo ảnh động với hiệu ứng **Blend** (hiệu ứng mờ dần).

### Cách tạo ảnh động từ một hiệu ứng có sẵn có thể khái quát qua các bước sau:

*   **Bước 1. Chuẩn bị ảnh tĩnh cho ảnh động**
    *   Tạo tệp ảnh mới và thực hiện lệnh **File\Open As Layers** để mở các ảnh tĩnh dưới dạng các lớp ảnh. Ví dụ, mở ba ảnh.
*   **Bước 2. Tạo dãy khung hình cho ảnh động và gán thời gian (nếu cần)**
    *   Thực hiện lệnh **Filters\Animation** để mở ra danh sách các hiệu ứng, chọn tên một hiệu ứng để tạo ảnh động. Theo ví dụ, chọn hiệu ứng **Blend**.
    *   Nếu cần, thực hiện lệnh **Filters\Animation\Optimize (for GIF)** để GIMP tạo dãy khung hình gắn với thời gian. Nháy đúp chuột vào các tên khung hình có ảnh rõ nhất và tăng thời gian hiển thị các chúng.
*   **Bước 3. Xuất ảnh động**
Với dãy khung hình đã tạo, có thể xem trước ảnh động và thực hiện lệnh **File\ExportAs** để xuất ảnh động sang định dạng GIF.

## 4) Thực hành tạo hiệu ứng cho ảnh động

### Yêu cầu:
Hình 9 cho thấy trong nửa đầu chu kì dao động của con lắc, con lắc chuyển động từ A qua O đến B. Trong nửa sau chu kì dao động, con lắc chuyển động ngược lại: từ B qua O về A. Hãy tạo ảnh động biểu thị dao động của một con lắc đơn.

### Hướng dẫn thực hiện:

#### Bước 1. Chuẩn bị các ảnh tĩnh cho ảnh động
Nửa đầu chu kì dao động của con lắc được thể hiện trong Hình 10, gồm các khung hình từ Hình 10a đến Hình 10e. Nửa sau chu kì dao động của con lắc cũng được thể hiện trong Hình 10 nhưng từ khung hình Hình 10e ngược trở về khung hình Hình 10a.

Như vậy, cần thiết kế 5 ảnh tĩnh như trong Hình 10, chúng tương ứng có vai trò là 5 khung hình của ảnh động. Tuy nhiên, chỉ cần thiết kế một ảnh tĩnh. Các ảnh còn lại có thể được tạo bằng ba thao tác chính áp dụng cho ảnh con lắc, đó là: nhân đôi lớp ảnh bằng lệnh, quay ảnh bằng công cụ **Rotate** và lật đối xứng ảnh bằng công cụ **Flip**.

Ảnh tĩnh cần thiết kế bao gồm cảnh nền (thanh gỗ treo và trục đứng màu đỏ) và con lắc (quả lắc và dây lắc). Những đối tượng này có thể được tạo bằng các công cụ chọn **Rectangle Select**, **Ellipse Select** và công cụ tô màu thuần nhất **Bucket Fill**.

#### Bước 2. Xây dựng kịch bản cho hiệu ứng của ảnh động
Giả sử các khung hình trong Hình 10 được thiết kế kế và lần lượt xuất ra các tệp ảnh (đuôi PNG) với tên tệp là “Con lac 1”, “Con lac 2”, “Con lac 3”, “Con lac 4”, “Con lac 5”.

Mở tệp ảnh thứ nhất. Từ tệp ảnh này, mở các tệp ảnh còn lại dưới dạng các lớp ảnh mới bằng lệnh **File\Open as Layers** rồi sắp xếp lại các lớp ảnh như ở Hình 11. Đây là dãy khung hình thể hiện nửa đầu chu kì dao động của con lắc.

Để thể hiện nốt nửa sau chu kì dao động của con lắc, nhân đôi từng lớp ảnh và sắp xếp lại các lớp ảnh.

#### Bước 3. Xuất ảnh động

Chọn tệp ảnh với dãy 10 khung hình rồi thực hiện lệnh **File\Export As** để xuất ảnh động với định dạng GIF.

## Luyện tập
* Hãy tạo một ảnh động với hiệu ứng tự thiết kế để mô phỏng hoạt động của một đối tượng hay hiện tượng nào đó. Hiệu ứng của ảnh động do em tự chọn hoặc sáng tạo, ví dụ hiệu ứng lắc lư của con lật đật.
* Em đồng ý với những phát biểu nào dưới đây? Trong phần mềm thiết kế đồ hoạ GIMP:
    * a) Nguồn ảnh tĩnh của ảnh động luôn phải tự thiết kế.
    * b) Có thể thiết kế ảnh động từ các hiệu ứng có sẵn hoặc tự tạo.
    * c) Có thể xem trước và chỉnh sửa ảnh động khi xuất ảnh động với định dạng GIF.
    * d) Thứ tự các khung hình của ảnh động được sắp xếp tuỳ ý.
    * e) Thời gian xuất hiện của từng khung hình của ảnh động ảnh hưởng đến tốc độ chuyển động của ảnh động.

## Tóm tắt bài học

* **Ảnh động** gồm một dãy các khung hình. Thứ tự các khung hình cùng với thời gian xuất hiện của chúng thể hiện kịch bản tạo ra hiệu ứng của ảnh động.
* GIMP cung cấp một số hiệu ứng để tạo ảnh động, các hiệu ứng khác có thể tự thiết kế theo trí tưởng tượng và sự sáng tạo.
* Khi thiết kế ảnh động với hiệu ứng tự tạo, nguồn ảnh tĩnh cho ảnh động phải được chuẩn bị và sắp xếp theo kịch bản của hiệu ứng cần tạo.
* Nếu tự tạo nguồn ảnh tĩnh, cần đến các kĩ thuật thiết kế đồ hoạ và các thao tác chỉnh sửa ảnh như cắt, biến đổi ảnh, tẩy xoá chi tiết trong ảnh.
