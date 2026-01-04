import google.generativeai as genai
from RAG.retriever import Retriever
from LLM.format_context import format_context
from RAG.reranker import RerankerModule
import re

genai.configure(api_key="API_KEY")


# Response with term memory



def generate_response_rag_stream(query, retriever, reranker_mod, chat_history: str = "", stream: bool = True):
   """
   Generate RAG response với chat history support
   
   Args:
      query: Câu hỏi hiện tại
      retriever: Hybrid retriever
      reranker_mod: Reranker model
      chat_history: Lịch sử hội thoại đã format (default: "")
   """
    

   def needs_contextualization(q: str, history: str) -> bool:
      if not history:
         return False
      
      q_lower = q.lower()
      
      # Pronouns & References 
      pronouns = [
         # General reference pronouns
         "nó", "điều này", "điều đó", "những điều này", "những điều đó",
         "chúng", "chúng ta", "chúng tôi",

         # Lesson / textbook references
         "bài này", "bài đó", "bài học này", "bài học đó",
         "chương này", "chương đó",
         "phần này", "phần đó", "mục này", "mục đó",

         # Content references
         "đoạn này", "đoạn trên", "đoạn dưới",
         "nội dung này", "kiến thức này", "ý này", "ý đó",

         # Question / exercise references
         "câu này", "câu trên", "câu dưới", "câu hỏi này", "câu hỏi đó",
         "bài tập này", "bài tập trên",
         "đáp án này", "đáp án đó",

         # Concept / definition references
         "khái niệm này", "định nghĩa này", "định luật này",
         "công thức này", "biểu thức này",
         "quy tắc này", "phương pháp này",

         # Example / illustration references
         "ví dụ này", "ví dụ trên",
         "hình này", "hình vẽ này",
         "bảng này", "sơ đồ này",

         # Contextual references
         "phần trước", "phần sau",
         "ở trên", "ở dưới",
         "như đã nói", "đã đề cập"
      ]
        
      # Comparative & Follow-up words
      # Từ so sánh & câu hỏi tiếp nối (domain SGK THPT)
      comparative = [
         # So sánh kiến thức
         "so sánh", "khác nhau", "giống nhau", "khác gì",
         "so với", "so sánh với",
         "hơn", "kém", "tương đương",
         "thay vì", "không giống",

         # Lựa chọn / giả định
         "còn", "thế còn", "vậy còn",
         "nếu", "giả sử",
         "trường hợp khác",

         # Câu hỏi tiếp nối
         "ngoài ra", "thêm nữa", "bên cạnh đó",
         "tiếp theo", "hơn nữa"
      ]

      
      # Cụm từ thường bắt đầu câu follow-up (SGK)
      ellipsis_starts = [
         "và", "nhưng", "hoặc", "còn", "thế", "vậy",
         "ngoài ra", "thêm nữa",

         # Dạng câu hỏi ngắn tiếp lời
         "tại sao", "vì sao",
         "như thế nào", "ra sao",
         "có phải", "có đúng không",
         "làm sao", "bằng cách nào",

         # Câu hỏi yêu cầu làm rõ
         "giải thích", "chứng minh",
         "phân tích", "nhận xét"
      ]

      
      # Shopify-specific indicators 
      # Chỉ báo follow-up theo domain sách giáo khoa
      followup = [
         # Hỏi thêm / mở rộng
         "còn gì nữa", "còn không", "còn trường hợp nào",
         "có trường hợp nào khác",
         "liên quan không",

         # Hỏi chọn đối tượng
         "cái nào", "ý nào", "phần nào",
         "đoạn nào", "chương nào", "bài nào",

         # Hỏi về kết quả / đáp án
         "đáp án là gì", "kết quả là gì",
         "tính như thế nào",
         "ra bao nhiêu",

         # Hỏi về phương pháp / cách làm
         "làm thế nào", "cách giải",
         "giải ra sao", "làm như thế nào",

         # Hỏi phạm vi kiến thức
         "thuộc phần nào",
         "liên quan đến bài nào",
         "áp dụng công thức nào",

         # Hỏi mức độ hiểu
         "có đúng không",
         "hiểu đúng không",
         "ý này đúng không"
      ]

      
      # Kiểm tra các điều kiện
      has_pronoun = any(p in q_lower for p in pronouns)
      has_comparative = any(c in q_lower for c in comparative)
      has_followup = any(f in q_lower for f in followup)
      
      # Kiểm tra bắt đầu bằng ellipsis
      words = q_lower.split()
      starts_ellipsis = len(words) > 0 and any(
         q_lower.startswith(e) for e in ellipsis_starts
      )
      
      # Câu ngắn (<6 từ) + có history thường là follow-up
      is_short_followup = len(words) < 6 and history
      
      return (has_pronoun or has_comparative or has_followup or 
               starts_ellipsis or is_short_followup)

   def contextualize_question(q: str, history: str) -> str:
      """Chuyển câu hỏi phụ thuộc ngữ cảnh thành standalone question"""
      
      contextualize_prompt = f"""
      Cho lịch sử hội thoại và câu hỏi mới nhất của người dùng liên quan đến nội dung sách giáo khoa THPT,
      hãy viết lại câu hỏi sao cho:
      - Tự đầy đủ ngữ nghĩa
      - Rõ ràng
      - Phù hợp để dùng cho tìm kiếm hoặc truy xuất kiến thức
      - KHÔNG trả lời câu hỏi

      Nếu câu hỏi có sử dụng đại từ mơ hồ (như: "cái này", "điều đó", "bài này", "câu trên")
      hoặc là câu hỏi tiếp nối dựa vào ngữ cảnh trước đó,
      hãy viết lại câu hỏi với đầy đủ bối cảnh (bài, chương, nội dung kiến thức liên quan).

      Nếu câu hỏi đã rõ ràng và độc lập, hãy giữ nguyên, không thay đổi.

      Lịch sử hội thoại:
      {history}

      Câu hỏi hiện tại:
      {q}

      Câu hỏi sau khi viết lại (ngắn gọn, rõ ràng, phù hợp để tìm kiếm):
      """


      model = genai.GenerativeModel(
         model_name='models/gemini-2.5-flash',
         system_instruction="You are a query reformulation assistant. Make questions clear and standalone for search."
      )
      
      response = model.generate_content(contextualize_prompt)
      return response.text.strip()
   
   if needs_contextualization(query, chat_history):
      retrieval_query = contextualize_question(query, chat_history)
      print(f"[DEBUG] Contextualized: '{query}' -> '{retrieval_query}'")  # Debug log
   else:
      retrieval_query = query
   

   # Retrieval & Reranking 
   results_full = retriever.hybrid_search_RRF(retrieval_query, top_k=5, k=60)
   results_reranked = reranker_mod.rerank(retrieval_query, results_full, top_n=10)
   context_texts = format_context(results_reranked)

   # Add Chat History to Prompt
   history_section = ""
   if chat_history:
      history_section = f"""
   [Previous Conversation]:
   {chat_history}
   
   (Use this conversation context to understand follow-up questions and references, but base your answer on the documentation context below.)
   """

   # System Prompt
   SYSTEM_ROLE = """Bạn là EduQuestionGPT – một trợ lý AI đóng vai trò giáo viên Tin học THPT (lớp 10),
   chuyên tạo câu hỏi trắc nghiệm và đánh giá câu trả lời của học sinh
   dựa CHẶT CHẼ vào nội dung sách giáo khoa được cung cấp.

   Bạn KHÔNG tự suy đoán kiến thức ngoài tài liệu.
   Bạn làm việc theo từng bước: tạo câu hỏi → ghi nhớ → chờ học sinh trả lời → đánh giá.
   """

   # Updated Response Prompt with Chat History
   RESPONSE_PROMPT = f"""
   **Nhiệm vụ của bạn:**
   Dựa vào [Ngữ cảnh kiến thức], [Lịch sử hội thoại], [Bộ nhớ câu hỏi] và [Yêu cầu hiện tại],
   hãy phản hồi ĐÚNG theo ý định của người dùng.

   ---

   ## 1️⃣ QUY TẮC CỐT LÕI (BẮT BUỘC)

   1. **Dựa hoàn toàn vào ngữ cảnh:**
   - Mọi câu hỏi, đáp án, và giải thích PHẢI dựa trên [Ngữ cảnh kiến thức]
   - KHÔNG thêm kiến thức ngoài, kể cả khi bạn biết

   2. **Tách rõ 2 giai đoạn:**
   - GIAI ĐOẠN A: Sinh câu hỏi (KHÔNG kèm đáp án)
   - GIAI ĐOẠN B: Đánh giá câu trả lời (dùng bộ nhớ đã lưu)

   3. **Không đủ thông tin → phải nói rõ**
   - Nếu ngữ cảnh không đủ để tạo câu hỏi chất lượng, hãy nêu thiếu gì
   - KHÔNG bịa, KHÔNG suy diễn

   ---

   ## 2️⃣ NHẬN DIỆN Ý ĐỊNH NGƯỜI DÙNG

   ### 🔹 Trường hợp 1: Người dùng YÊU CẦU TẠO CÂU HỎI
   (Ví dụ: “Tạo 1 câu trắc nghiệm”, “Ra câu hỏi về nội dung trên”)

   ➡️ Thực hiện:
   - Tạo **CHỈ 1 câu hỏi trắc nghiệm**
   - 4 phương án A, B, C, D
   - KHÔNG hiển thị đáp án đúng
   - KHÔNG giải thích
   - Lưu vào **Bộ nhớ câu hỏi**:
   • Nội dung câu hỏi
   • Các đáp án
   • Đáp án đúng
   • Chủ đề
   • Độ khó (nếu có)

   ➡️ Định dạng trả lời:
   Câu hỏi: ...

   A. ...
   B. ...
   C. ...
   D. ...

   ### 🔹 Trường hợp 2: Người dùng TRẢ LỜI CÂU HỎI
   (Ví dụ: “Em chọn A”, “Đáp án là C”)

   ➡️ Thực hiện:
   - Lấy **câu hỏi gần nhất trong Bộ nhớ**
   - So sánh câu trả lời của học sinh với đáp án đúng
   - Phản hồi theo cấu trúc:
   1. Đúng / Sai
   2. Nêu đáp án đúng
   3. Giải thích NGẮN GỌN, dễ hiểu, dựa trên ngữ cảnh

   ➡️ KHÔNG tạo câu hỏi mới trừ khi được yêu cầu

   ---

   ### 🔹 Trường hợp 3: Câu hỏi mơ hồ / follow-up
   (Ví dụ: “Câu này khó quá”, “Tại sao đáp án đó đúng?”)

   ➡️ Thực hiện:
   - Dùng **term memory + lịch sử hội thoại**
   - Resolve các tham chiếu như: “câu này”, “ý đó”, “đáp án trên”
   - Chỉ giải thích dựa trên câu hỏi đang được lưu trong bộ nhớ

   ---

   ## 3️⃣ PHẠM VI KIẾN THỨC (TIN HỌC 10)

   - Chỉ xoay quanh:
   • Biểu diễn thông tin
   • Hệ điều hành
   • Mạng máy tính
   • An toàn thông tin

   - KHÔNG hỏi về lập trình (Python, C++, thuật toán…)

   - Ngôn ngữ:
   • Dễ hiểu
   • Phù hợp học sinh 15–16 tuổi
   • Tránh thuật ngữ quá hàn lâm

   ---

   ## 4️⃣ NGỮ CẢNH & DỮ LIỆU

   **[Ngữ cảnh kiến thức – Sách giáo khoa]:**
   {context_texts}

   **[Lịch sử hội thoại]:**
   {history_section}

   **[Yêu cầu hiện tại của người dùng]:**
   {query}

   ---

   **Hãy phản hồi đúng theo ý định người dùng, tuân thủ toàn bộ quy tắc trên.**
   """

   # Generate Response
   model = genai.GenerativeModel(
      model_name='models/gemini-2.5-flash-lite',
      system_instruction=SYSTEM_ROLE  
   )


   if stream:
         # Return generator cho streaming
         response_stream = model.generate_content(
               RESPONSE_PROMPT,
               stream=True  
         )
         
         for chunk in response_stream:
               if chunk.text:
                  yield chunk.text
   else:
      # Non-streaming 
      response = model.generate_content(RESPONSE_PROMPT)
      return response.text 
