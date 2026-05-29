# Bài 9: THỰC HÀNH ĐỊNH DẠNG MỘT SỐ THUỘC TÍNH CSS

Học xong bài này, em sẽ:
*   Khai báo được **bộ chọn phần tử**.
*   Sử dụng được **internal CSS, external CSS**.
*   Sử dụng được một số **thuộc tính CSS**.

## Nhiệm vụ 1. Khai báo và áp dụng quy tắc định dạng internal CSS
### Yêu cầu:
Khai báo định dạng internal CSS cho văn bản HTML "Bai7-NV1.html" mà em đã hoàn thành ở Bài 7 để được trang web như Hình 1.

### Hướng dẫn thực hiện:
*   **Bước 1.** Mở tệp HTML "Bai7-NV1.html", ghi lưu với tên mới "Bai9-NV1.html".
*   **Bước 2.** Khai báo CSS.
    *   Trong nội dung phần tử `head`, khai báo cặp thẻ `<style></style>`.
    *   Trong nội dung phần tử `style`, khai báo các quy tắc định dạng sau:
        *   Quy tắc cho thẻ `h2`: thiết lập màu chữ `firebrick` và phông chữ `Verdana`.
        *   Quy tắc cho thẻ `h3`: thiết lập màu chữ `indianred`.
        *   Quy tắc cho thẻ `label`: thiết lập kích thước chữ `15px` và in đậm.
        *   Quy tắc cho thẻ `input`: thiết lập màu nền `yellow`.
        *   Quy tắc cho thẻ `textarea`: thiết lập màu nền `ivory`.
*   **Bước 3.** Ghi lưu văn bản, mở tệp bằng trình duyệt web và quan sát kết quả.

## Nhiệm vụ 2. Khai báo và áp dụng quy tắc định dạng external CSS

### Yêu cầu 1:

Soạn tệp quy tắc định dạng “Bai9-NV2.css” gồm các quy tắc sau:
*   Phần tử **h2** sử dụng phông chữ **Verdana**, chữ được tô màu **firebrick**.
*   Phần tử **h3** chữ được tô màu **indianred**.
*   Phần tử **label** có cỡ chữ **20px**.
*   Nền của phần tử **input** được tô màu **yellow**.
*   Nền của phần tử **textarea** được tô màu **ivory**.

### Hướng dẫn thực hiện:

*   **Bước 1. Tạo tệp “Bai9-NV2.css”**.
    *   Mở phần mềm Sublime Text.
    *   Tạo tệp mới và ghi lưu với tên “Bai9-NV2.css”.
*   **Bước 2. Khai báo định dạng CSS**.
    Nội dung CSS sau đây định dạng các phần tử HTML như đã nêu trong yêu cầu:
    *   `h2` có màu chữ firebrick và phông chữ Verdana.
    *   `h3` có màu chữ indianred.
    *   `label` có kích thước chữ 20px.
    *   `input` có nền màu vàng.
    *   `textarea` có nền màu ivory.
*   **Bước 3. Ghi lưu tệp định dạng CSS**.

### Yêu cầu 2:

Em hãy áp dụng bảng định dạng “Bai9-NV2.css” đã soạn ở Yêu cầu 1 để trình bày văn bản HTML “Bai7-NV2.html” sao cho khi mở trên màn hình trình duyệt web, kết quả hiển thị một biểu mẫu web với tiêu đề "Đóng góp ý kiến cho thư viện của nhà trường".
Nội dung biểu mẫu bao gồm:
1.  **Thông tin về người góp ý**:
    *   Họ và tên (ô nhập liệu với nền màu vàng)
    *   Địa chỉ email (ô nhập liệu với nền màu vàng)
2.  **Đóng góp ý kiến**:
    *   Ý kiến đóng góp (vùng văn bản lớn với nền màu ivory)
    *   Thể loại cần bổ sung thêm sách (các ô chọn: Truyện ngắn, Kĩ năng sống, Công nghệ thông tin, Truyện tranh, Lịch sử)
    *   Nút "Góp ý"

### Hướng dẫn thực hiện:

*   **Bước 1. Mở tệp HTML “Bai7-NV2.html”**, ghi lưu với tên tệp mới “Bai9-NV2.html”.
*   **Bước 2. Áp dụng định dạng external CSS**.
    *   Mở tệp “Bai9-NV2.html”.
    *   Trong nội dung phần tử **head**, thêm khai báo để liên kết tệp HTML với tệp CSS bên ngoài: `<link rel="stylesheet" href="Bai9-NV2.css">`.
*   **Bước 3. Ghi lưu, mở tệp “Bai9-NV2.html” bằng trình duyệt web và quan sát kết quả**.

## Nhiệm vụ 3: Áp dụng bảng định dạng external CSS đã có cho văn bản HTML

### Yêu cầu

Áp dụng bảng định dạng “Bai9-NV2.css” đã hoàn thành ở Nhiệm vụ 2 để trình bày văn bản HTML “Bai7-NV3.html” sao cho khi mở trên trình duyệt web kết quả hiển thị như ở Hình 3.

**Cảm ơn bạn đã đóng góp ý kiến**
Chúng tôi xin ghi nhận ý kiến của bạn và sẽ cải tiến, nâng cao chất lượng phục vụ hơn nữa trong thời gian sắp tới.

### Hướng dẫn thực hiện

*   Bước 1. Mở tệp “Bai7-NV3.html”, ghi lưu với tên tệp mới là “Bai9-NV3.html”.
*   Bước 2. Áp dụng định dạng external CSS.
    *   Mở tệp “Bai9-NV3.html”.
    *   Khai báo áp dụng định dạng **Bai9-NV2.css** trong nội dung phần tử **head**.
*   Bước 3. Ghi lưu, mở tệp “Bai9-NV3.html” trên trình duyệt web và quan sát kết quả.

### Lưu ý:

Để thêm chú thích cho các quy tắc định dạng CSS, em viết chú thích trong cặp dấu `/*` và `*/`.

## Tạo website cá nhân:

Em hãy hoàn thiện website cá nhân đã tạo từ các bài học trước bằng cách khai báo và áp dụng các quy tắc định dạng trình bày để các tiêu đề sử dụng phông chữ và màu sắc đa dạng.

### Gợi ý thực hiện:

*   Tạo thư mục con **styles** trong thư mục **myHomepage**.
*   Tạo tệp mới và ghi lưu vào thư mục **styles** với tên “**style.css**”.
*   Khai báo các quy tắc định dạng trong tệp “**style.css**” để trình bày, ví dụ: tiêu đề **h1** sử dụng phông chữ **Verdana**, chữ màu đỏ; tiêu đề **h2** sử dụng phông chữ **Verdana**, chữ màu xanh.
*   Bổ sung khai báo tham chiếu sử dụng external CSS vào phần tử **head** của các tệp: “**index.html**”, “**hobbies.html**”, “**album.html**”.
