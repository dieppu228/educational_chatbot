from src.llm.memory import QuestionRecord, Session
from src.llm.handlers.question.essay_handler import EssayHandler
from src.llm.handlers.question.fill_handler import FillHandler
from src.llm.handlers.question.mcq_handler import MCQHandler
from src.llm.handlers.question.true_false_handler import TrueFalseHandler
from src.llm.services.quiz_service import QuizService
from src.llm.student_profile import StudentProfile
from src.llm.student_tracker import StudentTracker
from src.schemas.context import RequestContext


def test_student_profile_normalizes_scores_and_marks_weak_topics():
    profile = StudentProfile(user_id="student-1")

    profile.record_attempt("Mạng máy tính", 0.0)
    profile.record_attempt("Mạng máy tính", 5.0)
    profile.record_attempt("Cấu trúc lặp", 10.0)
    profile.record_attempt("Cấu trúc lặp", 1.0)

    assert profile.lesson_progress["Mạng máy tính"].scores == [0.0, 0.5]
    assert profile.lesson_progress["Mạng máy tính"].avg_score == 0.25
    assert "Mạng máy tính" in profile.weak_topics

    assert profile.lesson_progress["Cấu trúc lặp"].scores == [1.0, 1.0]
    assert "Cấu trúc lặp" in profile.strong_topics


def test_direct_mcq_answer_updates_student_profile_without_changing_session_scope():
    service = QuizService.__new__(QuizService)
    service.student_tracker = StudentTracker()
    session = Session(user_id="student-1", topic="Mạng máy tính", book="KNTT")
    ctx = RequestContext(query="câu 1 A câu 2 B", user_id="student-1")
    questions = [
        QuestionRecord(
            question_id="q1",
            question_type="mcq",
            content={"question": "A?", "correct_answer": "A"},
        ),
        QuestionRecord(
            question_id="q2",
            question_type="mcq",
            content={"question": "B?", "correct_answer": "C"},
        ),
    ]

    msg = service._try_grade_direct_mcq_answers(
        session=session,
        questions=questions,
        original_query="câu 1 A câu 2 B",
        ctx=ctx,
    )

    profile = service.student_tracker.get_profile("student-1")
    progress = profile.lesson_progress["Mạng máy tính"]

    assert "Đã chấm 2 câu: 1/2 đúng." in msg
    assert progress.scores == [1.0, 0.0]
    assert session.topic == "Mạng máy tính"
    assert session.book == "KNTT"
    assert ctx.debug_steps[-1]["status"] == "direct_mcq"


def test_quiz_difficulty_uses_query_before_profile():
    service = QuizService.__new__(QuizService)
    service.student_tracker = StudentTracker()
    session = Session(user_id="student-1", topic="Mạng máy tính")
    ctx = RequestContext(query="tạo 3 câu trắc nghiệm khó", user_id="student-1")
    ctx.session = session
    service.student_tracker.record_attempt("student-1", "Mạng máy tính", 0.0)
    service.student_tracker.record_attempt("student-1", "Mạng máy tính", 0.0)

    assert service._resolve_quiz_difficulty(ctx) == ("hard", "query")


def test_quiz_difficulty_adapts_from_student_profile():
    service = QuizService.__new__(QuizService)
    service.student_tracker = StudentTracker()
    session = Session(user_id="student-1", topic="Mạng máy tính")
    ctx = RequestContext(query="tạo 3 câu trắc nghiệm", user_id="student-1")
    ctx.session = session

    assert service._resolve_quiz_difficulty(ctx) == ("medium", "default")

    service.student_tracker.record_attempt("student-1", "Mạng máy tính", 0.0)
    service.student_tracker.record_attempt("student-1", "Mạng máy tính", 0.5)
    assert service._resolve_quiz_difficulty(ctx) == ("easy", "student_profile")

    service.student_tracker.record_attempt("student-1", "Mạng máy tính", 1.0)
    service.student_tracker.record_attempt("student-1", "Mạng máy tính", 1.0)
    service.student_tracker.record_attempt("student-1", "Mạng máy tính", 1.0)
    assert service._resolve_quiz_difficulty(ctx) == ("medium", "student_profile")

    strong_session = Session(user_id="student-1", topic="Cấu trúc lặp")
    strong_ctx = RequestContext(query="tạo 3 câu trắc nghiệm", user_id="student-1")
    strong_ctx.session = strong_session
    service.student_tracker.record_attempt("student-1", "Cấu trúc lặp", 1.0)
    service.student_tracker.record_attempt("student-1", "Cấu trúc lặp", 1.0)
    assert service._resolve_quiz_difficulty(strong_ctx) == ("hard", "student_profile")


def test_normalize_attempt_for_tracking_handles_partial_scores():
    assert QuizService._normalize_attempt_for_tracking("mcq", None, True) == (1.0, True)
    assert QuizService._normalize_attempt_for_tracking("mcq", None, False) == (0.0, False)
    assert QuizService._normalize_attempt_for_tracking("essay", 2.0, True) == (0.2, False)
    assert QuizService._normalize_attempt_for_tracking("fill_blank", 4.0, False) == (0.4, True)


def test_mcq_handler_includes_target_difficulty_in_prompt(monkeypatch):
    captured = {}

    def fake_call_api(self, prompt, **kwargs):
        captured["prompt"] = prompt
        return """
        {
          "mcq": [
            {
              "index": 1,
              "question": "Mạng LAN là gì?",
              "options": {"A": "Mạng cục bộ", "B": "Mạng toàn cầu", "C": "CPU", "D": "RAM"},
              "correct_answer": "A",
              "explanation": "LAN là mạng cục bộ."
            }
          ]
        }
        """

    monkeypatch.setattr(MCQHandler, "_call_api", fake_call_api)

    MCQHandler().handle("tạo câu hỏi", "LAN là mạng cục bộ.", num_questions=1, difficulty="hard")

    assert "=== ĐỘ KHÓ MỤC TIÊU ===" in captured["prompt"]
    assert "hard" in captured["prompt"]


def test_non_mcq_handlers_include_target_difficulty_in_prompt(monkeypatch):
    captured = []

    def fake_call_api(self, prompt, **kwargs):
        captured.append(prompt)
        if isinstance(self, EssayHandler):
            return """
            {"essays": [{"index": 1, "question": "Giải thích LAN.", "sample_answer": "LAN là mạng cục bộ.", "rubric": "Đúng khái niệm.", "difficulty": "easy"}]}
            """
        if isinstance(self, FillHandler):
            return """
            {"fill_blanks": [{"index": 1, "text_with_blanks": "LAN là mạng ___.", "answers": ["cục bộ"], "explanation": "LAN là mạng cục bộ."}]}
            """
        return """
        {"true_false": [{"index": 1, "statement": "LAN là mạng cục bộ.", "correct_answer": true, "explanation": "Đúng."}]}
        """

    monkeypatch.setattr(EssayHandler, "_call_api", fake_call_api)
    monkeypatch.setattr(FillHandler, "_call_api", fake_call_api)
    monkeypatch.setattr(TrueFalseHandler, "_call_api", fake_call_api)

    EssayHandler().handle("tạo câu hỏi", "LAN là mạng cục bộ.", num_questions=1, difficulty="easy")
    FillHandler().handle("tạo câu hỏi", "LAN là mạng cục bộ.", num_questions=1, difficulty="easy")
    TrueFalseHandler().handle("tạo câu hỏi", "LAN là mạng cục bộ.", num_questions=1, difficulty="easy")

    assert len(captured) == 3
    assert all("=== ĐỘ KHÓ MỤC TIÊU ===" in prompt for prompt in captured)
    assert all("easy" in prompt for prompt in captured)
