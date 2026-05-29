# Bài 7: THỰC HÀNH TẠO BIỂU MẪU

**Học xong bài này, em sẽ:**
*   Tạo được biểu mẫu trên trang web.
*   Thêm được các điều khiển thông dụng vào biểu mẫu.
*   Thiết kế được biểu mẫu phù hợp với yêu cầu nhập dữ liệu.

## Nhiệm vụ 1. Tạo biểu mẫu có ô text nhập dữ liệu

**Yêu cầu:**
Soạn văn bản HTML để tạo biểu mẫu như khi hiển thị trên trình duyệt web.

**Hướng dẫn thực hiện:**
*   Bước 1. Tạo tệp “Bai7-NV1.html”.
*   Bước 2. Tạo cấu trúc và khai báo phần tử **head** cho tệp “Bai7-NV1.html”.
*   Bước 3. Tạo biểu mẫu.
    *   Trong nội dung phần tử **body**: Khai báo phần tử **form** bằng cặp thẻ `<form> </form>`.
    *   Trong nội dung phần tử **form**:
        *   Thêm ô text để nhập liệu cho thông tin “Họ và tên” bằng khai báo sau:
            *Mô tả: Đoạn mã HTML này tạo một nhãn "Họ và tên" và một trường nhập liệu dạng văn bản cho tên, sau đó xuống dòng.*
        *   **Chú ý**, phần tử **label** được dùng để tạo nhãn gắn với điều khiển, nhằm làm cho việc truy cập các điều khiển trên biểu mẫu được dễ dàng (nháy chuột vào nhãn là có thể nhập dữ liệu cho ô điều khiển đó). Khai báo này sử dụng phần tử **br** nhằm tạo ngắt dòng để ô text “Địa chỉ email” bắt đầu ở dòng mới.
        *   Thêm ô text để nhập dữ liệu cho thông tin “Địa chỉ email”.
        *   Thêm ô **textarea** để nhập đoạn văn bản thể hiện thông tin “Ý kiến đóng góp”.
        *   Ô **textarea** được khai báo như sau:
            *Mô tả: Đoạn mã HTML này tạo một nhãn "Ý kiến đóng góp" và một vùng văn bản đa dòng cho phép nhập bình luận, với kích thước hiển thị được xác định bởi thuộc tính rows và cols.*
        *   Trong đó, thuộc tính **rows** và **cols** xác định kích thước hiển thị ô nhập dữ liệu.
*   Bước 4. Ghi lưu, mở tệp bằng trình duyệt web và xem kết quả.

## Nhiệm vụ 2. Thêm các điều khiển nhập dữ liệu lựa chọn, gửi dữ liệu vào biểu mẫu

### Yêu cầu:
Soạn văn bản HTML để thêm các điều khiển nhập dữ liệu như minh hoạ ở Hình 2 vào biểu mẫu đã tạo ở Nhiệm vụ 1. Khi mở bằng trình duyệt web, kết quả hiển thị như ở Hình 3.

### Hướng dẫn thực hiện:
*   **Bước 1.** Mở tệp HTML "Bai7-NV1.html" vừa hoàn thành ở Nhiệm vụ 1, ghi lưu tệp với tên mới là "Bai7-NV2.html".
*   **Bước 2.** Cập nhật nội dung phần tử body.
    *   Thêm thể loại sách cần bổ sung bằng cách tạo nhóm các **checkbox** như sau: Thêm các điều khiển **checkbox** cho phép người dùng chọn các thể loại sách bao gồm Truyện ngắn, Kĩ năng sống, Công nghệ thông tin, Truyện tranh và Lịch sử.
    *   Lưu ý: Trong khai báo này sử dụng phần tử br để tạo ngắt dòng, mỗi mục chọn trong danh sách được hiển thị ở một dòng mới.
    *   Thêm một nút **submit** với nội dung là "Góp ý".
*   **Bước 3.** Ghi lưu, mở tệp bằng trình duyệt web và xem kết quả.

## Nhiệm vụ 3: Tạo trang web phản hồi khi người dùng nhấn nút gửi dữ liệu

## Yêu cầu:
Soạn văn bản HTML để khi nhấn nút lệnh “Góp ý” trong biểu mẫu ở Nhiệm vụ 2 thì màn hình trình duyệt web hiển thị như sau:

Cám ơn bạn đã góp ý kiến
Chúng tôi xin ghi nhận ý kiến của bạn và sẽ cải tiến, nâng cao chất lượng phục vụ hơn nữa trong thời gian sắp tới.

## Hướng dẫn thực hiện:
*   **Bước 1**. Tạo tệp “Bai7-NV3.html”.
*   **Bước 2**. Tạo cấu trúc và khai báo phần tử `head` cho tệp “Bai7-NV3.html”.
*   **Bước 3**. Khai báo nội dung phần tử `body` cho tệp “Bai7-NV3.html”.
    *   Soạn nội dung như mô tả trên và ghi lưu.
*   **Bước 4**. Cập nhật khai báo phần tử `form` cho tệp “Bai7-NV2.html”.
    *   Mở tệp “Bai7-NV2.html”, cập nhật thuộc tính **action** trong khai báo phần tử `form` thành: `action = “Bai7-NV3.html”`.
    *   Lưu ý: Tệp “Bai7-NV3.html” được lưu cùng thư mục chứa tệp “Bai7-NV2.html”.
*   **Bước 5**. Ghi lưu, mở tệp “Bai7-NV2.html” bằng trình duyệt web, điền biểu mẫu và nháy chuột vào nút “Góp ý” để quan sát kết quả.

## Vận dụng
Hãy tạo biểu mẫu nhận lời nhắn từ bạn bè để hoàn thiện tiếp website cá nhân đã tạo ở các bài học trước.

Gợi ý thực hiện:
*   Mở tệp “index.html”, thêm tiêu đề mục `h2` “Lời nhắn” để tạo biểu mẫu nhận các lời nhắn từ bạn bè.
*   Biểu mẫu có các điều khiển:
    *   Ô nhập liệu **text** có nhãn “Họ và tên”.
    *   Ô nhập liệu **textarea** có nhãn “Lời nhắn”.
    *   Nút lệnh **submit** có nhãn “Gửi”.
