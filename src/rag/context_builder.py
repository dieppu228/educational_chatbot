
import time
import logging
from typing import List, Dict, Optional

from src.config.config import settings
from src.llm.prompts import CONTEXT_BUILD_TEMPLATE

logger = logging.getLogger("chatbot.context_builder")


class ContextBuilder:

    def __init__(self):
        try:
            from google import genai
            self.client = genai.Client(api_key=settings.GENAI_API_KEY)
        except ImportError:
            raise ImportError("google-generativeai not installed")

    def build(
        self,
        query: str,
        chunks: List[Dict],
        action: Optional[str] = None,
        max_chunks: int = 15,
    ) -> str:
        if not chunks:
            return "[Không có context]"

        # Giới hạn số chunks
        selected = chunks[:max_chunks]

        # Format chunks thành input cho LLM
        raw_context = self._format_raw_chunks(selected)

        # Xác định task description cho LLM
        task_desc = self._get_task_description(action)

        # Build prompt
        prompt = CONTEXT_BUILD_TEMPLATE.format(
            query=query,
            raw_context=raw_context,
            task_description=task_desc,
            num_chunks=len(selected),
        )

        # Call LLM
        try:
            t0 = time.time()
            response = self.client.models.generate_content(
                model=settings.LLM_MODEL,
                contents=prompt,
                config={
                    "temperature": 0.1,  # Low temp → faithful synthesis
                    "response_mime_type": "text/plain",
                    "top_p": 0.9,
                },
            )
            build_time = time.time() - t0

            result = response.text.strip()
            logger.info(
                f"ContextBuilder: {len(selected)} chunks → "
                f"{len(result)} chars ({build_time:.2f}s) "
                f"[action={action}]"
            )
            return result

        except Exception as e:
            logger.warning(
                f"ContextBuilder LLM call failed: {e}. "
                f"Falling back to raw concatenation."
            )
            # Fallback: trả về raw chunks nối lại (behavior cũ)
            return self._fallback_concatenate(selected)

    def _format_raw_chunks(self, chunks: List[Dict]) -> str:
        formatted = []
        for i, chunk in enumerate(chunks, 1):
            content = chunk.get("content", "")
            meta = chunk.get("metadata", {})
            score = chunk.get("rerank_score")

            # Header với metadata nếu có
            header_parts = [f"[Chunk {i}]"]
            if meta.get("topic_name"):
                header_parts.append(f"Chủ đề: {meta['topic_name']}")
            if meta.get("lesson_name"):
                header_parts.append(f"Bài: {meta['lesson_name']}")
            if meta.get("grade"):
                header_parts.append(f"Lớp: {meta['grade']}")
            if score is not None:
                header_parts.append(f"Score: {score:.4f}")

            header = " | ".join(header_parts)
            formatted.append(f"{header}\n{content}")

        return "\n\n---\n\n".join(formatted)

    def _fallback_concatenate(self, chunks: List[Dict]) -> str:
        parts = []
        for i, chunk in enumerate(chunks, 1):
            parts.append(f"Context {i}:\n{chunk.get('content', '')}")
        return "\n\n---\n\n".join(parts)

    @staticmethod
    def _get_task_description(action: Optional[str]) -> str:
        descriptions = {
            # Quiz-related
            "generate_quiz": "Tạo câu hỏi trắc nghiệm/tự luận — cần giữ chi tiết kiến thức chính xác, số liệu, định nghĩa.",
            "mcq": "Tạo câu hỏi trắc nghiệm — cần giữ chi tiết kiến thức chính xác, số liệu, định nghĩa.",
            "essay": "Tạo câu hỏi tự luận — cần giữ khái niệm sâu và ví dụ minh họa.",
            "fill_blank": "Tạo câu điền khuyết — cần giữ các cụm từ then chốt và định nghĩa.",
            "true_false": "Tạo câu đúng/sai — cần giữ sự chính xác của mọi phát biểu.",
            # Explain
            "explain_concept": "Giải thích khái niệm — cần tổ chức logic: khái niệm → chi tiết → ví dụ → so sánh.",
            "explain": "Giải thích khái niệm — cần tổ chức logic: khái niệm → chi tiết → ví dụ → so sánh.",
            # Content generation
            "generate_slide": "Tạo slide bài giảng — cần giữ flow SGK: mở đầu → kiến thức → ví dụ → bài tập.",
            "slide": "Tạo slide bài giảng — cần giữ flow SGK: mở đầu → kiến thức → ví dụ → bài tập.",
            "generate_lesson_plan": "Tạo giáo án — cần đầy đủ: mục tiêu, nội dung, phương pháp, đánh giá.",
            "lesson_plan": "Tạo giáo án — cần đầy đủ: mục tiêu, nội dung, phương pháp, đánh giá.",
            # Chat
            "chat": "Trả lời câu hỏi — cần tổng hợp thông tin liên quan nhất.",
        }
        return descriptions.get(
            action,
            "Tổng hợp kiến thức — giữ nguyên nội dung chính xác từ tài liệu."
        )


__all__ = ["ContextBuilder"]
