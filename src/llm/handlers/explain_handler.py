
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import EXPLAIN_PROMPT


class ExplainHandler(BaseHandler):
    
    def handle(self, query: str, context: str = "", **kwargs) -> str:
        if not context:
            context = "[Không tìm thấy tài liệu liên quan — sẽ giải thích dựa trên kiến thức chung]"
        
        prompt = EXPLAIN_PROMPT.format(query=query, context=context)
        
        try:
            response = self._call_api(
                prompt,
                temperature=0.4,
                response_mime="text/plain"
            )
            return response
        except Exception as e:
            return "Không thể giải thích lúc này. Vui lòng thử lại sau."


__all__ = ["ExplainHandler"]
