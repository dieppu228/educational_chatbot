from typing import Optional, List, Dict, Any
from src.llm.handlers.base_handler import BaseHandler
from src.llm.handlers.question.mcq_handler import MCQHandler
from src.llm.prompts import SLIDE_GENERATION_TEMPLATE
from src.schemas.llm_outputs import SlideGenerationOutput, SlideItem, MCQGenerationOutput
from src.config.config import settings

class SlideHandler(BaseHandler):
    """
    Sinh cấu trúc bài giảng (Slides) từ nội dung bài học.
    Tích hợp sinh bài tập tự động cho các slide củng cố.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sử dụng MCQHandler để sinh bài tập khi cần
        self.mcq_handler = MCQHandler(*args, **kwargs)

    def handle(
        self, 
        book: str,
        grade: str,
        lesson: str,
        context: str,
        include_exercises: bool = True,
        **kwargs
    ) -> SlideGenerationOutput:
        """
        Sinh bài giảng.
        
        Args:
            book: Tên bộ sách
            grade: Khối lớp
            lesson: Tên bài học
            context: Nội dung bài học từ RAG
            include_exercises: Có tự động sinh bài tập trong slide không
            
        Returns:
            SlideGenerationOutput: Object chứa danh sách slide
        """
        # 1. Build prompt sinh cấu trúc slide
        prompt = SLIDE_GENERATION_TEMPLATE.format(
            book=book,
            grade=grade,
            lesson=lesson,
            context=context
        )
        
        # 2. Call API
        response = self._call_api(
            prompt,
            temperature=settings.QUESTION_GENERATION_TEMPERATURE,
            response_mime="application/json"
        )
        
        # 3. Parse structure
        try:
            slide_output = SlideGenerationOutput.from_json_string(response)
            
            # 4. Nếu có slide exercise, tự động sinh bài tập
            if include_exercises:
                self._inject_exercises(slide_output, context)
            
            return slide_output
            
        except Exception as e:
            self._handle_error(f"Lỗi sinh Slide JSON: {e}")

    def _inject_exercises(self, slide_output: SlideGenerationOutput, context: str):
        """Duyệt các slide và sinh câu hỏi cho slide type 'exercise'."""
        for slide in slide_output.slides:
            if slide.slide_type == "exercise":
                try:
                    # Sinh 2 câu trắc nghiệm cho mỗi slide bài tập
                    mcq_result = self.mcq_handler.handle(
                        query=f"Sinh câu hỏi luyện tập cho: {slide.title}",
                        context=context,
                        num_questions=2
                    )
                    # Chuyển đổi sang list dict để lưu vào SlideItem
                    slide.questions = [q.model_dump() for q in mcq_result.mcq]
                except:
                    slide.questions = []
