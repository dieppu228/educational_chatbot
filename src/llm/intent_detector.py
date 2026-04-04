"""
Intent Detector — Phân loại intent + task_type bằng Gemini Flash Lite.

Thay thế router.py (PhoBERT 3 labels) bằng LLM-based detection linh hoạt.
Thêm intent mới chỉ cần sửa prompt, không cần retrain.
"""

import json
import re
import os
from typing import Optional
from google import genai
from google.genai.types import GenerateContentConfig


# ============================================================
# PROMPT
# ============================================================

INTENT_DETECT_PROMPT = """Bạn là hệ thống phân loại intent cho chatbot giáo dục SGK Tin học THPT.

Phân loại câu truy vấn sau:
Query: "{query}"
{memory_context}
CÁC INTENT hợp lệ:
- "generate_question": Yêu cầu sinh câu hỏi (trắc nghiệm, tự luận, đục lỗ, đúng/sai)
- "check_answer": Trả lời hoặc chọn đáp án cho câu hỏi đã sinh trước đó
- "generate_slide": Yêu cầu tạo nội dung slide bài giảng
- "generate_lesson_plan": Yêu cầu tạo giáo án
- "explain": Yêu cầu giải thích chuyên sâu một khái niệm
- "chat": Hỏi đáp chung, chào hỏi, hoặc câu không rõ ràng

CÁC TASK_TYPE (chỉ dùng khi intent = "generate_question"):
- "mcq": Trắc nghiệm ABCD
- "essay": Tự luận  
- "fill_blank": Đục lỗ / điền khuyết
- "true_false": Đúng/Sai

CHỈ trả về JSON, KHÔNG giải thích:
{{"intent": "...", "task_type": "..." hoặc null, "topic": "chủ đề chính nếu có" hoặc null}}"""


from src.config.config import settings


# ============================================================
# INTENT DETECTOR CLASS
# ============================================================

class IntentDetector:
    """
    Phát hiện intent + task_type từ query bằng Gemini Flash Lite.
    
    Output: dict {"intent": str, "task_type": str|None, "topic": str|None}
    """
    
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or settings.GENAI_API_KEY or os.getenv("GENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("GENAI_API_KEY chưa được set. Vui lòng kiểm tra file .env hoặc settings.")
        
        self.model_name = model_name or settings.LLM_MODEL or "models/gemini-2.5-flash-lite"
        self.client = genai.Client(api_key=self.api_key)
    
    def detect(self, query: str, memory_state: Optional[list] = None) -> dict:
        """
        Phân loại intent từ query.
        
        Returns:
            {"intent": str, "task_type": str|None, "topic": str|None}
        """
        try:
            memory_context = self._format_memory(memory_state)
            prompt = INTENT_DETECT_PROMPT.format(
                query=query,
                memory_context=memory_context
            )
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(temperature=0.1)
            )
            
            raw = self._extract_text(response)
            result = self._parse_result(raw)
            
            return result if result else self._fallback(query)
            
        except Exception as e:
            print(f"⚠️ IntentDetector error: {e}")
            return self._fallback(query)
    
    def _format_memory(self, memory_state: Optional[list]) -> str:
        if not memory_state:
            return ""
        recent = memory_state[-3:]
        lines = [f"  - {m.get('role','user')}: {m.get('content','')[:150]}" for m in recent]
        return "\nNgữ cảnh hội thoại:\n" + "\n".join(lines) + "\n"
    
    def _extract_text(self, response) -> str:
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    return part.text.strip()
        return ""
    
    def _parse_result(self, raw: str) -> dict:
        text = raw.strip()
        text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        
        try:
            data = json.loads(text.strip())
            intent = data.get("intent", "chat")
            
            valid_intents = {"generate_question", "check_answer", "generate_slide",
                           "generate_lesson_plan", "explain", "chat"}
            if intent not in valid_intents:
                intent = "chat"
            
            return {
                "intent": intent,
                "task_type": data.get("task_type"),
                "topic": data.get("topic"),
            }
        except json.JSONDecodeError:
            return None
    
    def _fallback(self, query: str) -> dict:
        return {"intent": "chat", "task_type": None, "topic": None}


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    detector = IntentDetector()
    
    tests = [
        "Tạo 5 câu trắc nghiệm về mạng LAN",
        "Cho tôi 3 câu tự luận về hệ điều hành",
        "Đáp án câu 1 là A",
        "Tạo slide bài 1 lớp 12 Cánh Diều",
        "Mạng máy tính là gì?",
        "Xin chào",
    ]
    
    for q in tests:
        r = detector.detect(q)
        print(f"  '{q}' → {r}")
