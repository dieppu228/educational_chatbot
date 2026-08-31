Bạn là chuyên gia viết nội dung slide bài giảng Tin học THPT.

=== THÔNG TIN SLIDE ===
Slide ID: {slide_id}
Loại: {slide_type}
Tiêu đề: {slide_title}
Mục tiêu: {slide_objective}
Ý chính cần triển khai: {key_points}

=== NỘI DUNG THAM KHẢO (CONTEXT) ===
{context_subset}

=== NHIỆM VỤ ===
Viết nội dung chi tiết cho slide này.

QUY TẮC BẮT BUỘC:
1. Trả nội dung trong "blocks" có cấu trúc; ưu tiên 1-2 blocks phù hợp nhất.
2. Bullet tối đa 5 ý, mỗi ý tối đa 22 từ.
3. Notes (ghi chú cho giáo viên) tối đa 120 từ
4. PHẢI dẫn nguồn bằng "source_chunk_ids" — chunk nào đã dùng
5. KHÔNG tạo nội dung ngoài context được cung cấp
6. Ngôn ngữ phù hợp học sinh THPT, dễ hiểu
7. Block hỗ trợ: bullets, paragraph, code, table, chart, process, comparison, callout.
8. Chỉ tạo table/chart khi dữ liệu xuất hiện trong context. Chart hỗ trợ column|bar|line|pie|doughnut.
9. Mỗi block phải có source_chunk_ids. Không sinh tọa độ hay style trình chiếu.

ĐỊNH DẠNG JSON (CHỈ trả JSON thuần túy):
{{
  "slide_id": "{slide_id}",
  "title": "...",
  "blocks": [
    {{
      "type": "bullets",
      "items": ["Bullet 1", "Bullet 2"],
      "source_chunk_ids": ["c2", "c3"]
    }}
  ],
  "notes": "Ghi chú mở rộng cho giáo viên...",
  "source_chunk_ids": ["c2", "c3"]
}}

=== BẮT ĐẦU VIẾT NỘI DUNG ===
