from typing import List, Dict, Optional, Any
import json
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import KNOWLEDGE_RELATION_PROMPT

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

    def lookup_semantic_topic(
        self,
        book_hint: Optional[str],
        lesson_reference: str,
        grade_hint: Optional[str] = None,
    ) -> Optional[str]:
        lesson = self._lookup_lesson(book_hint, lesson_reference, grade_hint)
        if not lesson:
            return None
        if self._extract_lesson_num(lesson_reference):
            return f"{lesson['topic_name']} - {lesson['lesson_name']}"
        return lesson["topic_name"]

    def lookup_lesson_context(
        self,
        book_hint: Optional[str],
        lesson_reference: str,
        grade_hint: Optional[str] = None,
    ) -> Optional[Dict[str, str]]:
        lesson = self._lookup_lesson(book_hint, lesson_reference, grade_hint)
        if not lesson:
            return None
        return {
            "book": lesson["book"],
            "grade": lesson["grade"],
            "topic_ref": lesson["topic_ref"],
            "topic_name": lesson["topic_name"],
            "lesson_num": lesson["lesson_num"],
            "lesson_name": lesson["lesson_name"],
            "query_context": (
                f"{lesson['book']} lớp {lesson['grade']} "
                f"chủ đề {lesson['topic_ref']} {lesson['topic_name']} "
                f"bài {lesson['lesson_num']} {lesson['lesson_name']}"
            ),
        }

    def _lookup_lesson(
        self,
        book_hint: Optional[str],
        lesson_reference: str,
        grade_hint: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        if not lesson_reference:
            return None

        import re
        topic_ref = None
        lesson_num = None

        m_topic = re.search(r'(?:chủ đề|chu de|chương|chuong)\s*([a-zA-Z0-9]+)', lesson_reference, re.IGNORECASE)
        if m_topic:
            topic_ref = self._normalize_topic_ref(book_hint, m_topic.group(1).upper())

        lesson_num = self._extract_lesson_num(lesson_reference)

        if not topic_ref and not lesson_num:
            return None

        for lesson in self.lessons:
            if book_hint and lesson["book"] != book_hint:
                continue
            if grade_hint and lesson["grade"] != grade_hint:
                continue
            if topic_ref and lesson["topic_ref"] != topic_ref:
                continue
            if lesson_num and lesson["lesson_num"] != lesson_num:
                continue
            return lesson
        return None

    @staticmethod
    def _extract_lesson_num(lesson_reference: str) -> Optional[str]:
        import re
        m_lesson = re.search(r'bài\s*(\d+)', lesson_reference, re.IGNORECASE)
        return m_lesson.group(1) if m_lesson else None

    @staticmethod
    def _normalize_topic_ref(book_hint: Optional[str], topic_ref: str) -> str:
        chapter_map = {
            "1": "A", "2": "B", "3": "C", "4": "D",
            "5": "E", "6": "F", "7": "G", "8": "H",
        }
        reverse_map = {value: key for key, value in chapter_map.items()}
        if book_hint == "CD" and topic_ref in chapter_map:
            return chapter_map[topic_ref]
        if book_hint == "KNTT" and topic_ref in reverse_map:
            return reverse_map[topic_ref]
        return topic_ref

    def handle(self, query: str, **kwargs):
        pass
