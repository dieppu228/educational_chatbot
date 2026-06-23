
import time
from typing import List, Dict, Optional

from src.config.config import settings
from src.config.genai_client import create_genai_client
from src.llm.prompts import CONTEXT_BUILD_TEMPLATE
from src.utils.trace_decorator import trace_node


class ContextBuilder:

    def __init__(self):
        try:
            self.client = create_genai_client()
        except ImportError:
            raise ImportError("google-generativeai not installed")

    @trace_node("ContextBuilder.build")
    def build(
        self,
        query: str,
        chunks: List[Dict],
        action: Optional[str] = None,
        max_chunks: int = 15,
    ) -> str:
        if not chunks:
            return "[Không có context]"

        selected = chunks[:max_chunks]
        raw_context = self._format_raw_chunks(selected)
        task_desc = self._get_task_description(action)

        prompt = CONTEXT_BUILD_TEMPLATE.format(
            query=query,
            raw_context=raw_context,
            task_description=task_desc,
            num_chunks=len(selected),
        )

        try:
            response = self.client.models.generate_content(
                model=settings.LLM_MODEL,
                contents=prompt,
                config={
                    "temperature": 0.1,
                    "response_mime_type": "text/plain",
                    "top_p": 0.9,
                },
            )
            return response.text.strip()

        except Exception as e:
            # Fallback: trả về raw chunks nối lại
            return self._fallback_concatenate(selected)

    @trace_node("ContextBuilder.build_async")
    async def build_async(
        self,
        query: str,
        chunks: List[Dict],
        action: Optional[str] = None,
        max_chunks: int = 15,
    ) -> str:
        if not chunks:
            return "[Không có context]"

        selected = chunks[:max_chunks]
        raw_context = self._format_raw_chunks(selected)
        task_desc = self._get_task_description(action)

        prompt = CONTEXT_BUILD_TEMPLATE.format(
            query=query,
            raw_context=raw_context,
            task_description=task_desc,
            num_chunks=len(selected),
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=settings.LLM_MODEL,
                contents=prompt,
                config={
                    "temperature": 0.1,
                    "response_mime_type": "text/plain",
                    "top_p": 0.9,
                },
            )
            return response.text.strip()

        except Exception as e:
            # Fallback: trả về raw chunks nối lại
            return self._fallback_concatenate(selected)

    def _format_raw_chunks(self, chunks: List[Dict]) -> str:
        formatted = []
        for i, chunk in enumerate(chunks, 1):
            content = chunk.get("content", "")
            meta = chunk.get("metadata", {})
            score = chunk.get("rerank_score")

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
            "generate_quiz": "Tạo câu hỏi trắc nghiệm/tự luận — cần giữ chi tiết kiến thức chính xác, số liệu, định nghĩa.",
            "mcq": "Tạo câu hỏi trắc nghiệm — cần giữ chi tiết kiến thức chính xác, số liệu, định nghĩa.",
            "essay": "Tạo câu hỏi tự luận — cần giữ khái niệm sâu và ví dụ minh họa.",
            "fill_blank": "Tạo câu điền khuyết — cần giữ các cụm từ then chốt và định nghĩa.",
            "true_false": "Tạo câu đúng/sai — cần giữ sự chính xác của mọi phát biểu.",
            "explain_concept": "Giải thích khái niệm — cần tổ chức logic: khái niệm → chi tiết → ví dụ → so sánh.",
            "explain": "Giải thích khái niệm — cần tổ chức logic: khái niệm → chi tiết → ví dụ → so sánh.",
            "generate_slide": "Tạo slide bài giảng — cần giữ flow SGK: mở đầu → kiến thức → ví dụ → bài tập.",
            "slide": "Tạo slide bài giảng — cần giữ flow SGK: mở đầu → kiến thức → ví dụ → bài tập.",
            "generate_lesson_plan": "Tạo giáo án — cần đầy đủ: mục tiêu, nội dung, phương pháp, đánh giá.",
            "lesson_plan": "Tạo giáo án — cần đầy đủ: mục tiêu, nội dung, phương pháp, đánh giá.",
            "chat": "Trả lời câu hỏi — cần tổng hợp thông tin liên quan nhất.",
        }
        return descriptions.get(
            action,
            "Tổng hợp kiến thức — giữ nguyên nội dung chính xác từ tài liệu."
        )


__all__ = ["ContextBuilder"]
