from google import genai
from RAG.retriever import Retriever
from LLM.format_context import format_context
from RAG.reranker import RerankerModule
import re, json
from dotenv import load_dotenv
import os
import random

load_dotenv()  

api_key = os.getenv("GENAI_API_KEY")

client = genai.Client(api_key=api_key)


def extract_num_questions(query: str) -> int | None:
    """
    Trích xuất số lượng câu hỏi từ query
    VD: "cho 3 câu hỏi" → 3, "cho 5 câu" → 5
    
    Returns:
        int nếu tìm thấy, None nếu không
    """
    # Pattern: "N câu" hoặc "N question" hoặc "N bài"
    patterns = [
        r'(\d+)\s*(?:câu|bài|question)',
        r'(?:cho|tạo)\s+(\d+)\s*(?:câu|bài)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            num = int(match.group(1))
            # Validate: từ 1-10 câu
            return max(1, min(10, num))
    
    return None


def calculate_adaptive_questions(context_count: int) -> int:
    """
    Tính số lượng câu hỏi adaptive dựa trên số context
    
    - Nếu context <= 5 → random 2-3 câu
    - Nếu context 6-15 → random 3-4 câu  
    - Nếu context > 15 → random 4-5 câu
    
    Args:
        context_count: Số lượng context từ RAG
    
    Returns:
        Số lượng câu hỏi random
    """
    if context_count <= 5:
        return random.randint(2, 3)
    elif context_count <= 15:
        return random.randint(3, 4)
    else:
        return random.randint(4, 5)


# Hàm tạo câu hỏi trắc nghiệm từ query và tài liệu RAG

def generate_question(query: str, retriever, reranker_mod):
    results_full = retriever.hybrid_search_RRF(query, top_k=60, k=60)
    context_texts = reranker_mod.rerank(query, results_full, top_n=10)
    
    # Xác định số lượng câu hỏi
    num_questions = extract_num_questions(query)
    if num_questions is None:
        # Nếu user không chỉ định → tính adaptive
        context_count = len(context_texts)
        num_questions = calculate_adaptive_questions(context_count)
    
    prompt = f"""
    Bạn là trợ lý giáo dục chuyên tạo câu hỏi trắc nghiệm chất lượng cao.

    === YÊU CẦU CỦA NGƯỜI DÙNG ===
    {query}

    === KIẾN THỨC TỪ TÀI LIỆU (RAG) ===
    {context_texts}

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
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'temperature': 0.5,  # Nâng từ 0.0 → 0.5: sáng tạo hơn nhưng vẫn tập trung
            'top_p': 0.95,
        },
    )
    
    return response.text



# Hàm định dạng câu hỏi trắc nghiệm từ JSON sang text readable format

def generate_response(options: str, max_index: int):
    """
    Format câu hỏi trắc nghiệm từ JSON sang text readable format.
    
    Args:
        options: JSON string có format {"mcq": [{index, question, options, correct_answer, explanation}, ...]}
        max_index: Số lượng câu hỏi - dùng cho validation
    
    Returns:
        String formatted output (text, không JSON)
    """

    prompt = f"""
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

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={
            'temperature': 0.0,
            'top_p': 0.95,
        },
    )
    
    return response.text
    
# Hàm xác định và chấm điểm câu trả lời của user dựa trên session state

def utility_node(query: str, state_text: str) -> str:
    """
    Xác định và chấm điểm câu trả lời của user.
    
    Args:
        query: phát biểu của user (VD: 'đáp án câu an toàn thông tin là B - tấn công dò mật khẩu')
        state_text: session_state dưới dạng string JSON
    
    Returns:
        JSON string với kết quả xác định
    """

    prompt = f"""
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
    
    QUAN TRỌNG: User nói "câu N" nhưng index = N-1
    - User nói "câu 1" → question_index = 0
    - User nói "câu 2" → question_index = 1
    - User nói "câu 3" → question_index = 2
    
    Ưu tiên từ cao đến thấp:
    1. User ghi explicit index ("câu 1", "câu 2", "question 3")
       → Chuyển đổi: question_index = (số user nói) - 1
    2. User mô tả nội dung câu (so khớp với question text)
    3. Nếu user không specify → câu hỏi cuối cùng trong session
    4. Nếu chỉ 1 câu hỏi trong session → đó là câu đang trả lời
    
    === VÍ DỤ ===
    User query: "đáp án câu 1 là A"
    → question_index = 1 - 1 = 0
    → Tìm questions[0] trong session state
    
    === FORMAT OUTPUT JSON BẮT BUỘC ===

    CASE 1: Xác định thành công
    {{
      "status": "found",
      "question_index": 0,
      "question_text": "Câu hỏi đầy đủ từ session",
      "user_answer": "A",
      "correct_answer": "B",
      "is_correct": false,
      "explanation": "Giải thích chi tiết tại sao đáp án B đúng, dẫn chứng từ tài liệu",
      "confidence": 0.95
    }}

    CASE 2: Xác định nhưng không chắc (fuzzy)
    {{
      "status": "found",
      "question_index": 1,
      "question_text": "...",
      "user_answer": "A",
      "correct_answer": "C",
      "is_correct": false,
      "explanation": "Giải thích từ tài liệu...",
      "confidence": 0.65,
      "note": "User nói 'cái thứ 3' nhưng không rõ chỉ đáp án hay câu"
    }}

    CASE 3: Không tìm được câu hỏi
    {{
      "status": "not_found",
      "reason": "Không có câu hỏi nào trong session",
      "suggestion": "Hãy tạo câu hỏi trước"
    }}

    CASE 4: Mơ hồ - nhiều khả năng
    {{
      "status": "ambiguous",
      "candidates": [
        {{
          "question_index": 0,
          "question_text": "...",
          "match_reason": "User mô tả giống câu này"
        }},
        {{
          "question_index": 1,
          "question_text": "...",
          "match_reason": "Có từ khóa trùng"
        }}
      ],
      "clarification_needed": "Bạn đang trả lời câu nào? Câu 1 hay câu 2?"
    }}

    === YÊU CẦU BẮT BUỘC ===
    - CHỈ trả về JSON thuần túy, KHÔNG có markdown hay text khác
    - "question_index" bắt đầu từ 0 (tương ứng với mảng)
    - "user_answer" và "correct_answer" phải là "A", "B", "C", hoặc "D"
    - "confidence" từ 0.0 đến 1.0 (0.9+ là rất chắc chắn)
    - KHÔNG tạo câu hỏi mới, KHÔNG bịa dữ liệu
    - Nếu có note/reason, hãy rõ ràng và hữu ích
    - Luôn kiểm tra lại đáp án người dùng so với options trong session
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'temperature': 0.0,
            'top_p': 0.95,
        },
    )

    return response.text




# Hàm tạo feedback/giải thích chi tiết dựa trên kết quả chấm điểm

def generate_answer(utility_result: str) -> str:
    """
    Tạo feedback chi tiết dựa trên kết quả từ utility_node.
    
    Args:
        utility_result: JSON string từ utility_node() có chứa:
                       - question_text
                       - user_answer
                       - correct_answer
                       - explanation
                       - is_correct
                       - question_index (bắt đầu từ 0)
    
    Returns:
        String feedback cho user (không JSON)
    """
    prompt = f"""
    Bạn là trợ lý phản hồi giáo dục.
    
    === THÔNG TIN KẾT QUẢ ===
    {utility_result}
    
    === NHIỆM VỤ ===
    Tạo feedback tích cực cho user dựa trên kết quả chấm điểm:
    - Nếu đúng: Khen ngợi và nhấn mạnh điểm học được
    - Nếu sai: Giải thích lý do tại sao sai, cách khắc phục
    
    === OUTPUT ===
    Chỉ trả về text phản hồi (KHÔNG JSON):
    
    QUAN TRỌNG: Khi hiển thị câu hỏi, PHẢI cộng thêm 1 vào question_index từ dữ liệu JSON
    - Trích xuất giá trị "question_index" từ JSON input (bắt đầu từ 0)
    - Tính toán số câu = question_index + 1 (để hiển thị từ 1)
    Ví dụ: nếu JSON có "question_index": 0 → hiển thị "câu 1"
           nếu JSON có "question_index": 1 → hiển thị "câu 2"
           nếu JSON có "question_index": 2 → hiển thị "câu 3"
    
    Format output:
    "Với câu [số tính được] bạn trả lời là [user_answer]..."
    
    <Nếu đúng>:
    "Với câu [số]: Chính xác! Bạn đã hiểu đúng về [chủ đề].... [nhấn mạnh điểm học] và có thể giải thích ngắn gọn tại sao đúng"
    
    <Nếu sai>:
    "Với câu [số]: Bạn chọn [user_answer] nhưng đáp án đúng là [correct_answer]. 
    Lý do: [explanation]. 
    Gợi ý để nhớ lâu: ..."
    
    === YÊU CẦU ===
    1. Tạo feedback ngắn (2-3 câu), dễ hiểu
    2. Sử dụng tiếng Việt tự nhiên
    3. Khuyến khích và tích cực
    4. KHÔNG dùng JSON format
    5. KHÔNG thêm text trước/sau feedback
    6. LUÔN hiển thị số câu ở đầu feedback (tính từ question_index + 1)
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={
            'temperature': 0.7,  # Cao hơn để feedback đa dạng
        },
    )
    return response.text



# Hàm xử lý các câu hỏi ngoài domain hoặc không được nhận diện

def fall_back(query: str) -> str:
    
    prompt = f"""
   Bạn là trợ lý chatbot giáo dục.

    === QUERY ===
    {query}

    === NHIỆM VỤ CHÍNH ===
    Nhận diện loại tin nhắn và phản hồi phù hợp, tránh làm gián đoạn hội thoại khi không cần thiết.

    === PHÂN LOẠI ===

    1) CHITCHAT / CẢM THÁN / PHẢN ỨNG TỰ NHIÊN (KHÔNG FALLBACK)
    Ví dụ:
    - à thế à, ồ vậy hả
    - dễ vậy mà mình làm sai
    - hóa ra là vậy
    - ok hiểu rồi, cảm ơn
    - trời 😭
    - haha, =)), vâng ạ

    👉 Cách phản hồi:
    - đồng cảm ngắn gọn
    - khuyến khích tiếp tục học hoặc đặt câu hỏi tiếp
    Ví dụ:
    - "Không sao đâu, sai là chuyện bình thường khi học. Bạn muốn thử thêm câu nữa không?"
    - "Tuy hơi dễ nhưng bạn đang tiến bộ rồi đó! Muốn làm câu khó hơn không?"
    - "Mình hiểu rồi. Bạn muốn tiếp tục với câu hỏi khác chứ?"

    2) CÂU HỎI CƠ BẢN VỀ CHATBOT
    Ví dụ:
    - bạn là ai
    - bạn làm gì
    - bạn giúp được gì

    👉 Trả lời giới thiệu ngắn gọn, thân thiện.

    3) NGOÀI DOMAIN (THỰC SỰ KHÔNG LIÊN QUAN)
    Ví dụ:
    - giá vàng hôm nay bao nhiêu
    - làm sao để giàu
    - đá bóng ai thắng
    - dự báo thời tiết

    👉 Nhắc nhẹ nhàng quay lại chủ đề trắc nghiệm/giáo dục.

    === QUAN TRỌNG ===
    - KHÔNG xử lý chitchat như lỗi ngoài domain
    - KHÔNG tỏ ra cứng nhắc
    - KHÔNG rập khuôn
    - KHÔNG dùng emoji quá nhiều

    === OUTPUT ===
    Chỉ trả về một câu trả lời tự nhiên, thân thiện, đúng nhóm đã nhận diện.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={
            'temperature': 0.7,
        },
    )
    return response.text
    