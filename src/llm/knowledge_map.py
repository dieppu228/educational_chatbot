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
    
    def __init__(self, table_of_contents_path="data/table_of_contents.md"):
        self.toc_path = table_of_contents_path
        self.lessons = self._parse_toc()
        
    def find_relations(self, context: str) -> List[Dict[str, str]]:
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

    def _parse_toc(self) -> List[Dict[str, Any]]:
        import os
        import re
        lessons = []
        if not os.path.exists(self.toc_path):
            return lessons
            
        with open(self.toc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        current_book = None
        current_grade = None
        current_topic_ref = None
        current_topic_name = None
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Match book
            if "Cánh Diều" in line or "(CD)" in line:
                current_book = "CD"
            elif "Kết Nối Tri Thức" in line or "(KNTT)" in line:
                current_book = "KNTT"
            
            # Match grade
            m_grade = re.match(r'^## Lớp (\d+)', line)
            if m_grade:
                current_grade = m_grade.group(1)
            
            # Match Topic
            m_topic = re.search(r'CHỦ ĐỀ ([A-Z0-9]+)[:.]?\s*(.*)', line, re.IGNORECASE)
            if m_topic:
                current_topic_ref = m_topic.group(1).upper()
                current_topic_name = m_topic.group(2).strip()
                
            # Match Lesson
            m_lesson = re.match(r'^Bài (\d+)[\.\:]\s*(.*)', line, re.IGNORECASE)
            if m_lesson and current_book:
                lessons.append({
                    "book": current_book,
                    "grade": current_grade,
                    "topic_ref": current_topic_ref,
                    "topic_name": current_topic_name,
                    "lesson_num": m_lesson.group(1),
                    "lesson_name": m_lesson.group(2).strip()
                })
        return lessons

    def lookup_semantic_topic(self, book_hint: Optional[str], lesson_reference: str) -> Optional[str]:
        if not lesson_reference:
            return None
            
        import re
        topic_ref = None
        lesson_num = None
        
        m_topic = re.search(r'chủ đề\s*([a-zA-Z0-9]+)', lesson_reference, re.IGNORECASE)
        if m_topic:
            topic_ref = m_topic.group(1).upper()
            
        m_lesson = re.search(r'bài\s*(\d+)', lesson_reference, re.IGNORECASE)
        if m_lesson:
            lesson_num = m_lesson.group(1)
            
        # Nhan dien rieng re
        if not topic_ref and not lesson_num:
            return None
            
        matches = []
        for l in self.lessons:
            if book_hint and l["book"] != book_hint:
                continue
            
            match = True
            if topic_ref and l["topic_ref"] != topic_ref:
                match = False
            if lesson_num and l["lesson_num"] != lesson_num:
                match = False
                
            if match:
                matches.append(l)
                
        if not matches:
            return None
            
        best = matches[0]
        # Return Semantic Topic (Topic Name + Lesson Name)
        return f"{best['topic_name']} - {best['lesson_name']}"

    def handle(self, query: str, **kwargs):
        pass

