from src.llm.memory import Session, SlideSessionState
from src.llm.services.slide_service import SlideService
from src.schemas.context import RequestContext


class ExplodingScorer:
    def handle(self, *args, **kwargs):
        raise AssertionError("LLM scorer should not be called for direct MCQ answers")

    async def handle_async(self, *args, **kwargs):
        raise AssertionError("LLM scorer should not be called for direct MCQ answers")


def _ctx_with_slide_exercises(query: str) -> RequestContext:
    session = Session(user_id="student")
    session.topic = "Mạng máy tính"
    session.slide_state = SlideSessionState()
    session.slide_state.add_exercise(
        question_type="mcq",
        content={
            "question": "Thiết bị nào dùng để kết nối mạng?",
            "options": {"A": "Router", "B": "Bàn phím", "C": "Màn hình", "D": "Chuột"},
            "correct_answer": "A",
            "explanation": "Router dùng để định tuyến và kết nối mạng.",
        },
        slide_idx=3,
        q_idx=0,
    )
    session.slide_state.add_exercise(
        question_type="mcq",
        content={
            "question": "WWW là dịch vụ chạy trên môi trường nào?",
            "options": {"A": "Máy tính đơn lẻ", "B": "Internet", "C": "Máy in", "D": "USB"},
            "correct_answer": "B",
            "explanation": "WWW là một dịch vụ phổ biến trên Internet.",
        },
        slide_idx=3,
        q_idx=1,
    )
    return RequestContext(query=query, session=session)


def test_slide_exercise_direct_mcq_answers_are_graded_without_llm():
    service = object.__new__(SlideService)
    service.scorer = ExplodingScorer()
    ctx = _ctx_with_slide_exercises("câu 1 A câu 2 C")

    output = "".join(service.answer_exercise(ctx, ctx.query))

    exercises = ctx.session.slide_state.exercise_questions
    assert exercises[0].user_answer == "A"
    assert exercises[0].is_correct is True
    assert exercises[1].user_answer == "C"
    assert exercises[1].is_correct is False
    assert "Đã chấm 2 câu: 1/2 đúng" in output
    assert "Câu 1: Đúng" in output
    assert "Câu 2: Sai" in output
    assert ctx.debug_steps[-1]["action"] == "answer_exercise"
    assert ctx.debug_steps[-1]["status"] == "direct_mcq"


def test_slide_exercise_answer_key_request_uses_stored_answers_without_llm():
    service = object.__new__(SlideService)
    service.scorer = ExplodingScorer()
    ctx = _ctx_with_slide_exercises("cho tôi đáp án")

    output = "".join(service.answer_exercise(ctx, ctx.query))

    assert "Đáp án bài tập trong slide" in output
    assert "Câu 1: A" in output
    assert "Router dùng để định tuyến và kết nối mạng." in output
    assert "Câu 2: B" in output
    assert ctx.debug_steps[-1]["action"] == "answer_exercise"
    assert ctx.debug_steps[-1]["status"] == "answer_key"


def test_slide_exercise_answer_key_request_can_target_one_question():
    service = object.__new__(SlideService)
    service.scorer = ExplodingScorer()
    ctx = _ctx_with_slide_exercises("đáp án câu 2 là gì")

    output = "".join(service.answer_exercise(ctx, ctx.query))

    assert "Câu 1:" not in output
    assert "Câu 2: B" in output
