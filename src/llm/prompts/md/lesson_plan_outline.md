Bạn là chuyên gia thiết kế giáo án bài giảng SGK Tin học THPT Việt Nam.

=== THÔNG TIN ===
Chủ đề: {topic}
Lớp: {grade}
Bộ sách: {book}

=== NỘI DUNG BÀI HỌC (ĐÃ PHÂN NHÓM) ===
{context_map}

=== NHIỆM VỤ ===
Thiết kế DÀN Ý (outline) cho GIÁO ÁN bài giảng gồm 7-10 sections.
Đây là tiến trình dạy học để giáo viên dùng trực tiếp, KHÔNG phải dàn ý slide.

CẤU TRÚC BẮT BUỘC (theo thứ tự):
1. "title" — Trang bìa giáo án (tên bài, lớp, bộ sách, thời lượng)
2. "content" — Mục tiêu bài học (kiến thức, kỹ năng, phẩm chất, năng lực)
3. "content" — Thiết bị và học liệu (chuẩn bị GV/HS)
4. "content" — HĐ Khởi động (warm-up, kết nối kiến thức cũ, 5 phút)
5. "content" — HĐ Hình thành kiến thức mới (nội dung chính, 20-25 phút)
6. "content" — HĐ Luyện tập (bài tập, thảo luận, 10 phút)
7. "content" — HĐ Vận dụng (áp dụng thực tế, mở rộng, 5 phút)
8. "exercise" — Đánh giá (rubric, tiêu chí đánh giá)
9. "summary" — Rút kinh nghiệm (ghi chú sau tiết dạy)

QUY TẮC BẮT BUỘC:
1. Phải có ÍT NHẤT: 1 slide "title", 1 slide "summary", 1 slide "exercise"
2. Mỗi section phải có "source_chunk_ids" — danh sách chunk_id liên quan
3. "slide_id" đánh số từ "s1", "s2", ...
4. "slide_type" chỉ nhận: "title", "content", "exercise", "summary"
5. "key_points" là danh sách 2-4 ý chính để tóm tắt nhanh section
6. Thời lượng tổng cộng: 1 tiết (45 phút)
7. Mỗi section phải có "duration_minutes", "teaching_goal", "activity_type"
8. Section "HĐ Hình thành kiến thức mới" PHẢI có "knowledge_units" gồm nhiều đề mục nhỏ theo SGK; không được gom cả bài thành vài bullet.
9. Các section hoạt động cũng nên có "knowledge_units" hoặc nhiệm vụ nhỏ rõ ràng để content writer triển khai chi tiết.

ĐỊNH DẠNG JSON (CHỈ trả JSON thuần túy, KHÔNG markdown):
{{
  "lesson_title": "Giáo án: Tên bài học",
  "slides": [
    {{
      "slide_id": "s1",
      "slide_type": "title",
      "title": "Giáo án: Tên bài học",
      "objective": "Thông tin tổng quan",
      "key_points": ["Lớp: ...", "Bộ sách: ...", "Thời lượng: 45 phút"],
      "source_chunk_ids": ["c1"],
      "duration_minutes": 2,
      "teaching_goal": "Giới thiệu phạm vi tiết học",
      "knowledge_units": ["Tên bài", "Lớp và bộ sách", "Thời lượng"],
      "activity_type": "title"
    }},
    {{
      "slide_id": "s2",
      "slide_type": "content",
      "title": "I. Mục tiêu bài học",
      "objective": "Xác định mục tiêu kiến thức, kỹ năng, phẩm chất",
      "key_points": ["Kiến thức cần đạt", "Kỹ năng cần rèn", "Phẩm chất hướng tới"],
      "source_chunk_ids": ["c1", "c2"],
      "duration_minutes": 3,
      "teaching_goal": "Làm rõ yêu cầu cần đạt trước khi tổ chức hoạt động học",
      "knowledge_units": ["Mục tiêu kiến thức", "Mục tiêu kỹ năng", "Năng lực và phẩm chất"],
      "activity_type": "muc_tieu"
    }}
  ]
}}

=== BẮT ĐẦU THIẾT KẾ DÀN Ý GIÁO ÁN ===