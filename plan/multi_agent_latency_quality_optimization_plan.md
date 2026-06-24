# Kế hoạch Tối ưu hóa Độ trễ & Chất lượng Luồng Multi-Agent (Slide & Lesson Plan)

Kế hoạch này đề xuất các phương án tối ưu hóa kiến trúc đồ thị LangGraph supervisor và luồng xử lý của specialist agents nhằm giảm độ trễ (latency) và nâng cao chất lượng nội dung cho cả **Slide bài giảng** và **Giáo án (Lesson Plan)**. 

Do cả hai dịch vụ đều dùng chung đồ thị `ContentSupervisor` và có cấu trúc lưu trữ tương đồng dưới dạng danh sách các phân đoạn (Slide/Section), các giải pháp dưới đây sẽ được áp dụng đồng bộ cho cả hai nghiệp vụ.

---

## 1. Các Nút Thắt Cổ Chai Hiện Tại (Current Bottlenecks)

1. **Tái sinh toàn bộ (Full Regeneration)**: Khi quality check báo lỗi ở bất kỳ Slide (đối với slide bài giảng) hoặc Section/Hoạt động (đối với giáo án), hệ thống gán `content_payload = None` và gọi `ContentAgent` viết lại toàn bộ nội dung từ đầu (mất ~10-15s).
2. **Quá nhiều bước LLM trung gian**: LLM Supervisor được gọi để định tuyến lại sau mỗi lần chạy tool, làm tăng 2-3s overhead vô ích.
3. **Phân mảnh ngữ cảnh (Context Fragmentation)**: Slide/Lesson Plan Agent chỉ nhận ngữ cảnh tương ứng với `source_chunk_ids` từ outline. Nếu gán thiếu/sai ID ở outline, Writer Agent sẽ thiếu thông tin trầm trọng $\to$ dẫn tới slide rỗng hoặc giáo án phải dùng nội dung fallback mặc định rập khuôn.
4. **Quality Gate nặng nề**: LLM Quality Reviewer phải đọc toàn bộ context (12k ký tự) và merged output (16k ký tự) dẫn đến thời gian phản hồi chậm (3-5s) và dễ lỗi phân tích cú pháp JSON.

---

## 2. Các Giải Pháp Đề Xuất (Proposed Optimizations)

### 💡 Giải pháp 1: Sửa đổi Cục bộ theo Slide/Section (Local Slide/Section Revision)
Thay vì xóa toàn bộ `content_payload` để sinh lại từ đầu, hệ thống sẽ chỉ viết lại (regenerate) các Slide hoặc Section giáo án cụ thể bị đánh dấu chất lượng kém.

* **Cơ chế**:
  1. `QualityReviewerAgent` trả về danh sách các Slide/Section ID bị lỗi kèm chỉ dẫn chỉnh sửa chi tiết (ví dụ: `[{"slide_id": "s3", "reason": "thiếu mục tiêu chi tiết của hoạt động", "suggestion": "Lập bảng hoạt động GV/HS..."}]`).
  2. Tại `reflection_decision_node`, lưu danh sách ID bị lỗi này vào state (ví dụ: `failed_slide_ids`). **Không** xóa sạch `content_payload`.
  3. `ContentAgent` đọc `failed_slide_ids`. Nếu có giá trị, nó chỉ chạy ThreadPoolExecutor cho các Slide/Section ID này và giữ nguyên nội dung của các phần đạt yêu cầu.
  4. Hợp nhất (merge) kết quả sửa đổi vào payload cũ.

---

### 💡 Giải pháp 2: Định tuyến phản hồi trực tiếp (Direct Reflection Routing)
Bỏ qua bước gọi LLM Supervisor định tuyến lại sau khi có phản hồi của Quality Reviewer.

* **Cơ chế**:
  * Cập nhật điều kiện chuyển hướng trong `route_after_reflection`.
  * Nếu quality check fail và cần sửa content (`action == "revise_content"`): Đồ thị sẽ bỏ qua `supervisor_node` và đi thẳng tới node `tools` (hoặc một node wrapper riêng như `revise_content_node`) để kích hoạt trực tiếp `generate_content` với input là phản hồi của reviewer.
  * Tiết kiệm được **1.5 - 2.5 giây** thời gian LLM Supervisor reasoning.

---

### 💡 Giải pháp 3: Xử lý lỗi "Thiếu thông tin" qua 2 tầng (Local Lookup vs Targeted RAG Loop)
Giải quyết triệt để lỗi slide bị thiếu thông tin hoặc giáo án bị rập khuôn bằng cách mở rộng vùng tìm kiếm ngữ cảnh một cách tối ưu nhất.

#### Tầng 1: Tìm kiếm cục bộ (Local Lookup) - *Thời gian: < 1s*
* **Khi nào dùng**: Khi slide/section bị báo thiếu thông tin, nhưng thông tin thực chất nằm trong các chunk khác của tập RAG ban đầu mà bước lập Outline gán thiếu.
* **Cách chạy**: 
  1. Writer Agent sẽ nhận toàn bộ `chunk_map` (15-25 chunks đã được tải về ở preprocess node).
  2. Chạy thuật toán tìm kiếm từ khóa hoặc so khớp vector cục bộ (local similarity) để quét tất cả các chunks.
  3. Nếu tìm thấy chunk có chứa từ khóa liên quan, tự động bổ sung ID của chunk đó vào danh sách `source_chunk_ids` của slide/section đó và tiến hành viết lại.

#### Tầng 2: Vòng lặp RAG thu hẹp (Targeted RAG Loop) - *Thời gian: ~3-5s*
* **Khi nào dùng**: Khi đã chạy **Tầng 1** nhưng vẫn không tìm thấy thông tin cần thiết trong tập RAG ban đầu.
* **Cách chạy**:
  1. Kích hoạt một node phụ: `targeted_rag_node`.
  2. Sử dụng feedback của Quality Reviewer để viết lại một query phụ rất hẹp (ví dụ: *"Tiến trình dạy học Khóa ngoài môn Tin 11"*).
  3. Truy vấn trực tiếp RAG Service để lấy thêm 3-5 chunks. **Bypass bước Reranker** để giảm thời gian xử lý.
  4. Cập nhật các chunks mới này vào `chunk_map` của Graph State, liên kết chúng với slide/section bị lỗi, và kích hoạt Writer Agent sinh lại nội dung.
  5. Đặt giới hạn nghiêm ngặt: Tối đa **1 lần** RAG Loop cho mỗi lượt sinh bài học để tránh vòng lặp vô hạn.

---

### 💡 Giải pháp 4: Bộ kiểm tra định dạng nhanh (Fast Rule-based Validator)
* **Cơ chế**: Trước khi chuyển slide/giáo án sang LLM Quality Reviewer nặng nề, chạy một bộ validation bằng code thuần Python (ví dụ: kế thừa và mở rộng [SlideQualityGate](file:///home/dieppu/educational_chatbot/src/llm/services/slide_merger.py#L180)) để kiểm tra nhanh các lỗi cấu trúc:
  - Slide/Section có bị rỗng content/bullets không?
  - Số lượng bullets của slide có vượt quá giới hạn (max 6) không?
  - Giáo án có đủ các mục hoạt động GV/HS và đánh giá bắt buộc không?
  - Có bị thiếu phần tiêu đề hay tóm tắt bắt buộc không?
* Nếu phát hiện lỗi định dạng rõ ràng, trả ngược trực tiếp cho Writer Agent sửa đổi mà không tốn chi phí gọi LLM Quality Reviewer.

---

## 3. Kế hoạch Triển khai Chi tiết (Implementation Phase)

### Phase 1: Cơ sở hạ tầng & Định tuyến phản hồi trực tiếp (Direct Routing)
- [ ] Thêm trường `failed_slide_ids` vào `ContentSupervisorState`.
- [ ] Cập nhật logic `route_after_reflection` trong `content_supervisor.py` để nhảy trực tiếp sang tool node thay vì quay lại supervisor node khi cần sửa đổi.

### Phase 2: Sửa đổi cục bộ & Tìm kiếm cục bộ (Local Revision & Local Lookup)
- [ ] Điều chỉnh `ContentAgent._execute` để chỉ submit các slide/section nằm trong `failed_slide_ids` lên ThreadPoolExecutor.
- [ ] Triển khai hàm quét từ khóa / tìm kiếm cục bộ trên toàn bộ `chunk_map` trong `ContentAgent` để tự động vá các `source_chunk_ids` bị thiếu trước khi gọi LLM viết nội dung chi tiết.

### Phase 3: Vòng lặp RAG thu hẹp (Targeted RAG Loop)
- [ ] Xây dựng node `targeted_rag_node` trong đồ thị LangGraph.
- [ ] Tích hợp API gọi RAG không có reranker từ `RAGService`.
- [ ] Giới hạn cơ chế retry tối đa 1 lần thông qua biến đếm `rag_retry_attempts` trong state.

---

## 4. Kế hoạch Kiểm thử & Xác minh (Verification)

* **Kiểm thử Latency**: Đo lường tổng thời gian chạy luồng tạo bài học/giáo án khi có lỗi quality review xảy ra. Kỳ vọng giảm thời gian phản hồi của vòng lặp sửa lỗi xuống <6 giây.
* **Kiểm thử chất lượng**: Kiểm tra đầu ra của các slide/giáo án từng bị đánh dấu "thiếu thông tin" xem đã được điền thông tin thực tế thay vì các đoạn text mặc định/fallback hay chưa.
