
from typing import Optional
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import FALLBACK_PROMPT
from src.config.config import settings


class FallbackHandler(BaseHandler):
    
    def handle(self, query: str) -> str:
        try:
            prompt = FALLBACK_PROMPT.format(query=query)
            
            response = self._call_api(
                prompt,
                temperature=0.7,
                response_mime='text/plain'
            )
            
            return response
        
        except Exception as e:
            # Return default friendly response
            return (
                "Xin chào! Tôi là trợ lý hỗ trợ học tập. "
                "Bạn muốn làm bài trắc nghiệm về khối nào? (10, 11, hay 12) "
                "Hoặc tôi có thể giúp bạn với những câu hỏi khác!"
            )


__all__ = ["FallbackHandler"]
