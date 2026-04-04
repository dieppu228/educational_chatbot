import json
import re
import os
from typing import List, Optional
from google import genai
from google.genai.types import GenerateContentConfig


# ============================================================
# PROMPT
# ============================================================

REWRITE_PROMPT = """Bạn là hệ thống viết lại truy vấn cho chatbot sách giáo khoa Tin học THPT (lớp 10-12).

Nhiệm vụ: Từ câu hỏi gốc của học sinh, sinh ra 2-3 truy vấn tìm kiếm mới để tìm tài liệu trong sách giáo khoa.

Câu hỏi gốc: "{query}"
{memory_context}
Quy tắc:
1. Mỗi truy vấn mới phải:
   - Dạng cụm từ khóa (8-15 token), KHÔNG viết thành câu hoàn chỉnh
   - Bám sát nội dung SGK Tin học THPT
   - Bổ sung thuật ngữ kỹ thuật liên quan mà học sinh có thể không biết
2. Truy vấn 1: Giữ nguyên ý chính, bổ sung từ khóa đồng nghĩa / liên quan
3. Truy vấn 2: Mở rộng sang khía cạnh khác của chủ đề (ví dụ, phân loại, so sánh)
4. Truy vấn 3 (optional): Nếu chủ đề đủ rộng, thêm truy vấn về ứng dụng / ví dụ thực tế
5. Hạn chế trùng lặp từ khóa giữa các truy vấn (dưới 40%)

CHỈ trả về JSON, KHÔNG giải thích:
{{"queries": ["truy vấn 1", "truy vấn 2", "truy vấn 3"]}}"""


# ============================================================
# QUERY REWRITER CLASS
# ============================================================

class QueryRewriter:
    """
    Viết lại query dùng Gemini Flash Lite.
    
    Input: query (str) + memory_state (list hội thoại trước)
    Output: List[str] gồm 2-3 query mới
    """
    
    def __init__(self, api_key: str = None, model_name: str = "models/gemini-2.5-flash-lite"):
        """
        Args:
            api_key: Gemini API key (nếu None, lấy từ env GENAI_API_KEY)
            model_name: Tên model Gemini
        """
        self.api_key = api_key or os.getenv("GENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("GENAI_API_KEY chưa được set")
        
        self.model_name = model_name
        self.client = genai.Client(api_key=self.api_key)
    
    def rewrite(self, query: str, memory_state: Optional[List[dict]] = None) -> List[str]:
        """
        Viết lại query thành 2-3 truy vấn mới.
        
        Args:
            query: Câu hỏi gốc từ người dùng
            memory_state: Lịch sử hội thoại (list dict có "role" và "content")
                          Để rỗng nếu chưa có.
                          
        Returns:
            List[str]: 2-3 query đã viết lại. Nếu API lỗi, trả fallback.
        """
        try:
            # Build memory context string
            memory_context = self._format_memory(memory_state)
            
            # Build prompt
            prompt = REWRITE_PROMPT.format(
                query=query,
                memory_context=memory_context
            )
            
            # Call Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(temperature=0.3)
            )
            
            # Parse response
            raw_text = self._extract_text(response)
            queries = self._parse_queries(raw_text)
            
            return queries if queries else self._fallback(query)
            
        except Exception as e:
            print(f"QueryRewriter error: {e}")
            return self._fallback(query)
    
    def _format_memory(self, memory_state: Optional[List[dict]]) -> str:
        """Format memory state thành context string cho prompt."""
        if not memory_state:
            return ""
        
        # Lấy 3 tin nhắn gần nhất
        recent = memory_state[-3:]
        lines = []
        for msg in recent:
            role = msg.get("role", "user")
            content = msg.get("content", "")[:200]  # Giới hạn độ dài
            lines.append(f"  - {role}: {content}")
        
        return "\nNgữ cảnh hội thoại trước:\n" + "\n".join(lines) + "\n"
    
    def _extract_text(self, response) -> str:
        """Trích xuất text từ Gemini response."""
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    return part.text.strip()
        return ""
    
    def _parse_queries(self, raw_text: str) -> List[str]:
        """Parse JSON response, xử lý cả markdown code block."""
        # Clean markdown
        text = raw_text.strip()
        text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        text = text.strip()
        
        try:
            data = json.loads(text)
            queries = data.get("queries", [])
            
            # Validate: phải là list string, 2-3 phần tử
            if isinstance(queries, list) and 2 <= len(queries) <= 3:
                return [q for q in queries if isinstance(q, str) and q.strip()]
            
            # Nếu có nhiều hơn 3, lấy 3 cái đầu
            if isinstance(queries, list) and len(queries) > 3:
                return [q for q in queries[:3] if isinstance(q, str)]
                
        except json.JSONDecodeError:
            pass
        
        return []
    
    def _fallback(self, query: str) -> List[str]:
        """Fallback khi API lỗi — sinh query đơn giản từ rule-based."""
        return [
            query,
            f"{query} khái niệm định nghĩa SGK tin học",
        ]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    rewriter = QueryRewriter()
    
    test_queries = [
        "mạng LAN là gì",
        "cách mã hóa dữ liệu",
        "hệ điều hành",
    ]
    
    for q in test_queries:
        print(f"\nOriginal query: '{q}'")
        results = rewriter.rewrite(q, memory_state=[])
        for i, r in enumerate(results, 1):
            print(f"  [{i}] {r}")
