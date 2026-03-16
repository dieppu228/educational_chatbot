"""All LLM prompt templates for the application"""

# ===== QUESTION GENERATION PROMPT =====
QUESTION_GENERATION_PROMPT = """
Bạn là trợ lý giáo dục chuyên tạo câu hỏi trắc nghiệm chất lượng cao.

=== YÊU CẦU CỦA NGƯỜI DÙNG ===
{query}

=== KIẾN THỨC TỪ TÀI LIỆU (RAG) ===
{context}

=== NHIỆM VỤ ===
Dựa trên yêu cầu của người dùng và kiến thức được cung cấp, hãy tạo **chính xác {num_questions} câu hỏi** trắc nghiệm theo các quy tắc sau:

1. CHẤT LƯỢNG CÂU HỎI:
- Câu hỏi phải dựa trên kiến thức được cung cấp ở trên
- Mỗi câu hỏi có đúng 1 đáp án đúng duy nhất
- Các phương án nhiễu (sai) phải hợp lý, không quá dễ loại trừ
- Câu hỏi phải rõ ràng, không mơ hồ
- Độ khó phù hợp với nội dung kiến thức

2. CẤU TRÚC OUTPUT:
- CHỈ trả về JSON thuần túy
- KHÔNG thêm markdown, KHÔNG thêm ```json
- KHÔNG thêm lời giải thích bên ngoài JSON
- KHÔNG thêm text mở đầu hoặc kết thúc

3. ĐỊNH DẠNG JSON BẮT BUỘC:
{{
"mcq": [
    {{
    "index": 1,
    "question": "Nội dung câu hỏi đầy đủ, rõ ràng?",
    "options": {{
        "A": "Phương án A",
        "B": "Phương án B",
        "C": "Phương án C",
        "D": "Phương án D"
    }},
    "correct_answer": "A",
    "explanation": "Giải thích chi tiết tại sao đáp án này đúng, dẫn chứng từ kiến thức đã cung cấp"
    }},
    {{
    "index": 2,
    "question": "Câu hỏi thứ hai...",
    "options": {{
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
    }},
    "correct_answer": "B",
    "explanation": "..."
    }}
]
}}

4. QUY TẮC VALIDATION:
- "index" BẮT ĐẦU TỪ 1 và tăng dần (1, 2, 3, ..., {num_questions})
- PHẢI CÓ ĐÚNG {num_questions} CÂU HỎI trong mảng
- "correct_answer" CHỈ nhận: "A", "B", "C", hoặc "D"
- "options" PHẢI có đúng 4 key: A, B, C, D
- "explanation" PHẢI rõ ràng, tham chiếu đến kiến thức đã cho
- Mỗi phương án phải khác biệt rõ ràng

5. XỬ LÝ TRƯỜNG HỢP ĐẶC BIỆT:
- Nếu kiến thức không đủ để tạo {num_questions} câu chất lượng → giảm số lượng xuống
- Nếu yêu cầu không rõ ràng → tạo câu hỏi tổng quát về nội dung chính
- Nếu tạo {num_questions} câu hỏi → tạo đa dạng về góc độ kiến thức

=== BẮT ĐẦU TẠO {num_questions} CÂU HỎI ===
"""

# ===== RESPONSE FORMATTING PROMPT =====
RESPONSE_FORMATTING_PROMPT = """
Bạn là công cụ định dạng câu hỏi trắc nghiệm.

=== INPUT FORMAT ===
JSON string chứa danh sách câu hỏi:
{{
  "mcq": [
    {{
      "index": 1,
      "question": "Nội dung câu hỏi",
      "options": {{
        "A": "Phương án A",
        "B": "Phương án B",
        "C": "Phương án C",
        "D": "Phương án D"
      }},
      "correct_answer": "C",
      "explanation": "Giải thích chi tiết"
    }},
    {{
      "index": 2,
      "question": "Câu hỏi thứ 2",
      ...
    }}
  ]
}}

INPUT DATA:
{options}

=== NHIỆM VỤ ===
Định dạng lại các câu hỏi thành TEXT READABLE format (KHÔNG JSON).

=== OUTPUT FORMAT ===

Câu hỏi 1:
<Nội dung câu hỏi đầy đủ>

A. <Phương án A>
B. <Phương án B>
C. <Phương án C>
D. <Phương án D>

________________________________________

Câu hỏi 2:
<Nội dung câu hỏi>

A. <Phương án A>
B. <Phương án B>
C. <Phương án C>
D. <Phương án D>

________________________________________

=== YÊU CẦU ===
1. KHÔNG bao gồm correct_answer hoặc explanation trong output
2. KHÔNG in đáp án đúng hoặc giải thích
3. KHÔNG trả về JSON - chỉ text thuần
4. Mỗi câu hỏi cách nhau bằng dòng gạch ngang
5. Format: "Câu hỏi N:" rồi nội dung, rồi 4 options A, B, C, D
6. Giữ nguyên nội dung câu hỏi và options từ input
7. KHÔNG thêm text trước hoặc sau danh sách câu hỏi
8. Đảm bảo đầy đủ tất cả câu hỏi từ input
"""

# ===== UTILITY/SCORING PROMPT =====
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

=== QUY TẮC XỨ LÝ ===

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

# ===== FALLBACK/CHITCHAT PROMPT =====
FALLBACK_PROMPT = """
Bạn là trợ lý hỗ trợ học tập thân thiện.

User vừa hỏi:
{query}

Đây là câu hỏi không liên quan đến hệ thống học tập trắc nghiệm của chúng ta (hay là user đang trò chuyện thoải mái).

=== NHIỆM VỤ ===
1. Nếu là câu hỏi chung chung hoặc thoại lại chào hỏi → trả lời thân thiện ngắn gọn
2. Nếu user hỏi về các tính năng của hệ thống → hướng dẫn cách sử dụng
3. Nếu user muốn quay lại làm bài → khuyến khích họ

=== GỢI Ý TRƯỢ CHUYỆN ===
- Hỏi người dùng muốn làm bài của khối nào (10, 11, 12)
- Hỏi họ muốn bao nhiêu câu hỏi
- Khuyến khích tiếp tục học tập

=== OUTPUT ===
Trả lời thân thiện, ngắn gọn (1-3 câu), không quá dài
"""

# ===== FEEDBACK GENERATION PROMPT =====
FEEDBACK_GENERATION_PROMPT = """
Bạn là giáo viên tạo phản hồi giáo dục tích cực.

=== THÔNG TIN CÂU HỎI ===
Câu hỏi #{question_index}:
{question_text}

Phương án đúng: {correct_answer}
Phương án người dùng chọn: {user_answer}
Kết quả: {'✓ ĐÚNG' if is_correct else '✗ SAI'}

Giải thích đáp án:
{explanation}

=== NHIỆM VỤ ===
Tạo phản hồi giáo dục tích cực:
1. Nếu ĐÚNG: khích lệ, giải thích tại sao đúng
2. Nếu SAI: giải thích lỗi sai, hướng dẫn lại kiến thức

=== OUTPUT ===
Phản hồi ngắn gọn, rõ ràng, có tính xây dựng
"""


# # ===== EXTRACT PROMPT TEMPLATE =====

EXTRACT_PROMPT = """
Bạn là hệ thống trích xuất metadata cho hệ thống RAG sách giáo khoa THPT.

Nhiệm vụ:
Từ câu hỏi của người dùng, hãy trích xuất:
- lesson: tên bài học (string bất kỳ) hoặc null

Yêu cầu:
- Chỉ trả về JSON hợp lệ
- Không giải thích
- Không thêm text ngoài JSON

Câu hỏi:
"{query}"
"""



__all__ = [
    "QUESTION_GENERATION_PROMPT",
    "RESPONSE_FORMATTING_PROMPT",
    "UTILITY_SCORING_PROMPT",
    "FALLBACK_PROMPT",
    "FEEDBACK_GENERATION_PROMPT",
    "EXTRACT_PROMPT_TEMPLATE",
]



