import asyncio
import json
from typing import Optional, Dict, Any, List
from src.llm.handlers.base_handler import BaseHandler
from src.llm.prompts import UTILITY_SCORING_PROMPT, ESSAY_SCORING_TEMPLATE
from src.schemas.llm_outputs import ScoringOutput
from src.llm.memory import TaskItem
from src.config.config import settings

class QuestionScorer(BaseHandler):
    
    def handle(
        self, 
        query: str, 
        items: List[TaskItem],
        **kwargs
    ) -> ScoringOutput:
        # Chuyển items sang text để LLM đọc nội dung session
        state_text = self._format_items_for_scorer(items)
        
        # 1. Sử dụng UTILITY_SCORING_PROMPT để detect câu hỏi và câu trả lời (MCQ, T/F, Fill)
        prompt = UTILITY_SCORING_PROMPT.format(
            query=query,
            state_text=state_text
        )
        
        response = self._call_api(
            prompt,
            temperature=0.0,
            response_mime="application/json"
        )
        
        try:
            result = ScoringOutput.from_json_string(response)
            
            # 2. Xử lý đặc biệt cho Essay (nếu detect được là trả lời Essay)
            if result.status == "found" and result.question_index is not None:
                target_item = items[result.question_index]
                if target_item.type == "essay":
                    return self._score_essay(query, target_item, result)
            
            return result
            
        except Exception as e:
            self._handle_error(f"Lỗi chấm điểm: {e}", raise_error=False)
            return ScoringOutput(status="ambiguous", explanation="Không thể chấm điểm.")

    async def handle_async(
        self, 
        query: str, 
        items: List[TaskItem],
        **kwargs
    ) -> ScoringOutput:
        # Chuyển items sang text để LLM đọc nội dung session
        state_text = self._format_items_for_scorer(items)
        
        # 1. Sử dụng UTILITY_SCORING_PROMPT để detect câu hỏi và câu trả lời (MCQ, T/F, Fill)
        prompt = UTILITY_SCORING_PROMPT.format(
            query=query,
            state_text=state_text
        )
        
        response = await self._call_api_async(
            prompt,
            temperature=0.0,
            response_mime="application/json"
        )
        
        try:
            result = ScoringOutput.from_json_string(response)
            
            # 2. Xử lý đặc biệt cho Essay (nếu detect được là trả lời Essay)
            if result.status == "found" and result.question_index is not None:
                target_item = items[result.question_index]
                if target_item.type == "essay":
                    return await self._score_essay_async(query, target_item, result)
            
            return result
            
        except Exception as e:
            self._handle_error(f"Lỗi chấm điểm: {e}", raise_error=False)
            return ScoringOutput(status="ambiguous", explanation="Không thể chấm điểm.")

    def _score_essay(self, user_answer: str, item: TaskItem, initial_result: ScoringOutput) -> ScoringOutput:
        content = item.content
        prompt = ESSAY_SCORING_TEMPLATE.format(
            question=content.get("question", ""),
            sample_answer=content.get("sample_answer", ""),
            rubric=content.get("rubric", ""),
            user_answer=user_answer
        )
        
        response = self._call_api(
            prompt,
            temperature=0.2,
            response_mime="application/json"
        )
        
        try:
            essay_data = json.loads(response)
            initial_result.is_correct = essay_data.get("is_correct")
            initial_result.score = essay_data.get("score")
            initial_result.explanation = essay_data.get("explanation")
            initial_result.confidence = essay_data.get("confidence", 0.9)
            return initial_result
        except:
            return initial_result

    async def _score_essay_async(self, user_answer: str, item: TaskItem, initial_result: ScoringOutput) -> ScoringOutput:
        content = item.content
        prompt = ESSAY_SCORING_TEMPLATE.format(
            question=content.get("question", ""),
            sample_answer=content.get("sample_answer", ""),
            rubric=content.get("rubric", ""),
            user_answer=user_answer
        )
        
        response = await self._call_api_async(
            prompt,
            temperature=0.2,
            response_mime="application/json"
        )
        
        try:
            essay_data = json.loads(response)
            initial_result.is_correct = essay_data.get("is_correct")
            initial_result.score = essay_data.get("score")
            initial_result.explanation = essay_data.get("explanation")
            initial_result.confidence = essay_data.get("confidence", 0.9)
            return initial_result
        except:
            return initial_result

    def _format_items_for_scorer(self, items: List[TaskItem]) -> str:
        lines = []
        for i, item in enumerate(items):
            type_str = item.type.upper()
            content = item.content
            lines.append(f"[{i}] TYPE: {type_str}")
            
            if item.type == "mcq":
                lines.append(f"Q: {content.get('question')}")
                lines.append(f"ANS: {content.get('correct_answer')}")
            elif item.type == "true_false":
                lines.append(f"S: {content.get('statement')}")
                lines.append(f"ANS: {'Đúng' if content.get('correct_answer') else 'Sai'}")
            elif item.type == "fill_blank":
                lines.append(f"T: {content.get('text_with_blanks')}")
                lines.append(f"ANS: {', '.join(content.get('answers', []))}")
            elif item.type == "essay":
                lines.append(f"Q: {content.get('question')}")
            
            lines.append("-" * 20)
        return "\n".join(lines)
