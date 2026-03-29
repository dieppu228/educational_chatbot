"""
Answer scoring prompts for grading user responses.
"""

from src.prompts.base import PromptTemplate

# ============================================================
# UTILITY/SCORING PROMPT
# ============================================================

UTILITY_SCORING_PROMPT = """
Bạn là công cụ hỗ trợ chấm trắc nghiệm thông minh.

=== NHIỆM VỤ ===
1. Đọc session state (danh sách câu hỏi và lịch sử)
2. Xác định user đang trả lời câu hỏi nào
3. Chuẩn hóa và trích xuất đáp án của user
4. So sánh với đáp án đúng trong session state
5. Trả về JSON với kết quả chấm điểm

=== SESSION STATE ===
{state_text}

=== USER QUERY ===
{query}

=== HƯỚNG DẪN CHUẨN HÓA CÂU TRẢ LỜI ===

User có thể nói đáp án theo nhiều cách khác nhau:
- "A", "a", "đáp án A", "phương án A", "chọn A"
- "đáp án đầu tiên", "cái thứ hai", "B. ..."
- "tôi chọn cái về mã hóa đối xứng" (mô tả nội dung)
- "No. 3, A" (kết hợp index và đáp án)

Bạn phải:
1. Tìm và chuẩn hóa đáp án về "A", "B", "C" hoặc "D"
2. Nếu user mô tả nội dung, so khớp với nội dung trong options
3. Nếu user nói "câu thứ X", xác định index tương ứng
4. Chấp nhận lỗi chính tả nhỏ (Fuzzy matching)

=== LOGIC XÁC ĐỊNH CÂU HỎI ===

QUAN TRỌNG: User nói "câu N" nhưng question_index = N-1 (trong JSON)
- User nói "câu 1" → question_index = 0
- User nói "câu 2" → question_index = 1
- User nói "câu thứ nhất" → question_index = 0

=== OUTPUT JSON FORMAT ===
Luôn trả về JSON dòng đơn (không prettified) với cấu trúc CHÍNH XÁC sau:

{{
  "status": "found|not_found|ambiguous",
  "question_index": <int hoặc null>,
  "question_text": "<text của question hoặc null>",
  "user_answer": "<A/B/C/D hoặc null>",
  "correct_answer": "<A/B/C/D hoặc null>",
  "is_correct": <true/false hoặc null>,
  "explanation": "<lời giải thích hoặc null>",
  "confidence": <0.0-1.0 hoặc null>
}}

=== QUY TẮC XỬ LÝ ===

1. STATUS = "found":
   - User rõ ràng trả lời 1 câu cụ thể
   - question_index, question_text, user_answer, correct_answer phải set
   - is_correct = true/false (so sánh user_answer vs correct_answer)
   - Fuzzy matching cho nội dung: nếu user mô tả option, so khớp nội dung
   - confidence ≈ độ chắc chắn

2. STATUS = "not_found":
   - User không nói rõ câu nào
   - Hoặc user không đưa ra đáp án rõ ràng
   - Ví dụ: "mình không biết", "tôi chưa trả lời"
   - question_index, user_answer có thể null

3. STATUS = "ambiguous":
   - User nói không rõ hoặc mơ hồ
   - Có thể user nói nhiều câu cùng lúc
   - Hoặc user nói 1 câu nhưng không chắc
   - confidence < 0.5

=== THÊM YÊU CẦU ===
- CHỈ trả JSON thuần, KHÔNG thêm markdown, KHÔNG thêm ```json
- KHÔNG thêm text trước/sau JSON
- Luôn valid JSON format
- question_index bắt đầu từ 0 (trong JSON array index)
"""

# ============================================================
# TEMPLATE OBJECT
# ============================================================

SCORING_TEMPLATE = PromptTemplate(
    name="answer_scoring",
    template=UTILITY_SCORING_PROMPT,
    required_vars=["state_text", "query"],
    version="1.0",
    description="Score user's answer against stored questions"
)


__all__ = ["UTILITY_SCORING_PROMPT", "SCORING_TEMPLATE"]
