
import logging
from typing import Dict
from src.llm.handlers.content.slide_agents.base_slide_agent import BaseSlideAgent
from src.llm.prompts import SLIDE_QUIZ_TEMPLATE

logger = logging.getLogger("chatbot.slide_agent.quiz")


class QuizAgent(BaseSlideAgent):

    agent_name = "quiz"
    max_retries = 1
    error_code = "QUIZ_FAILED"

    def _execute(self, *, topic: str, context: str, **kwargs) -> dict:
        prompt = SLIDE_QUIZ_TEMPLATE.format(
            topic=topic,
            context=context,
        )

        response = self._call_llm(prompt, temperature=0.5)
        payload = self._parse_json(response)

        # Validate
        quiz_items = payload.get("quiz_items", [])
        if not quiz_items:
            raise ValueError("Quiz agent trả về 0 câu hỏi")

        # Giới hạn 3-5 câu
        payload["quiz_items"] = quiz_items[:5]

        # Validate từng câu có đủ options
        for item in payload["quiz_items"]:
            options = item.get("options", {})
            if len(options) != 4:
                raise ValueError(f"Câu hỏi thiếu options: {len(options)}/4")
            if item.get("correct_answer") not in ("A", "B", "C", "D"):
                raise ValueError(f"correct_answer không hợp lệ: {item.get('correct_answer')}")

        logger.info(f"Quiz agent: {len(payload['quiz_items'])} câu hỏi")
        return payload


__all__ = ["QuizAgent"]
