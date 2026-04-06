from typing import List, Dict, Optional, Any
import json
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import PromptTemplate

KNOWLEDGE_RELATION_PROMPT = """Bạn là chuyên gia xây dựng bản đồ kiến thức Tin học THPT.

=== NỘI DUNG BÀI HỌC HIỆN TẠI ===
{context}

=== NHIỆM VỤ ===
Xác định các kiến thức liên quan hoặc kiến thức tiên quyết (prerequisites) cần có để hiểu bài này.

YÊU CẦU:
1. Tìm các khái niệm/thuật ngữ quan trọng trong bài.
2. Liên hệ với các bài học khác trong chương trình Tin học THPT (nếu có thể).
3. Đưa ra gợi ý "Nếu bạn chưa biết về X, hãy xem lại bài Y".

ĐỊNH DẠNG JSON:
{{
  "related_topics": [
    {{
      "topic": "Tên chủ đề",
      "relation": "prerequisite | related | extension",
      "reason": "Giải thích ngắn gọn mối liên hệ"
    }}
  ]
}}

VALIDATION:
- Trả về tối đa 3-5 chủ đề quan trọng nhất.
- CHỈ trả về JSON thuần túy.

=== BẮT ĐẦU PHÂN TÍCH ==="""

class KnowledgeMap(BaseHandler):
    """
    Xây dựng mối liên hệ giữa các bài học/kiến thức.
    Giúp gợi ý bài học cũ hoặc mở rộng kiến thức mới.
    """
    
    def find_relations(self, context: str) -> List[Dict[str, str]]:
        """
        Tìm kiếm các chủ đề liên quan từ nội dung bài học.
        
        Args:
            context: Nội dung bài học hiện tại (từ RAG)
            
        Returns:
            List[Dict]: Danh sách các chủ đề liên quan
        """
        prompt = KNOWLEDGE_RELATION_PROMPT.format(context=context)
        
        response = self._call_api(
            prompt,
            temperature=0.0,
            response_mime="application/json"
        )
        
        try:
            data = json.loads(response)
            return data.get("related_topics", [])
        except:
            return []

    def handle(self, query: str, **kwargs):
        """KnowledgeMap không dùng handle trực tiếp."""
        pass

