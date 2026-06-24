from src.llm.memory import QuestionRecord, QuizRound, QuizSessionState, Session
from src.llm.services.quiz_service import QuizService
from src.schemas.context import RequestContext


class RaisingExplainHandler:
    def handle(self, *args, **kwargs):
        raise AssertionError("ExplainHandler should not be called for stored explanations")


def test_explain_question_uses_stored_explanation_without_llm():
    service = QuizService.__new__(QuizService)
    service.explain_handler = RaisingExplainHandler()
    session = Session()
    session.quiz_state = QuizSessionState(rounds=[
        QuizRound(
            round_id=0,
            question_type="mcq",
            query="tạo câu hỏi",
            questions=[
                QuestionRecord(
                    question_id="q1",
                    question_type="mcq",
                    content={
                        "question": "Dữ liệu là gì?",
                        "correct_answer": "B",
                        "explanation": "Vì dữ liệu là các dạng biểu diễn của thông tin.",
                    },
                )
            ],
        )
    ])
    ctx = RequestContext(query="giải thích câu 1")
    ctx.session = session

    output = "".join(service.explain_question(ctx, "giải thích câu 1"))

    assert "Giải thích câu 1" in output
    assert "Đáp án đúng: B" in output
    assert "Vì dữ liệu là các dạng biểu diễn của thông tin." in output
    assert ctx.debug_steps[-1]["source"] == "stored_explanation"


def test_stored_explanation_returns_none_when_question_number_is_unknown():
    session = Session()
    session.quiz_state = QuizSessionState(rounds=[
        QuizRound(
            round_id=0,
            question_type="mcq",
            query="tạo câu hỏi",
            questions=[
                QuestionRecord(
                    question_id="q1",
                    question_type="mcq",
                    content={"question": "A?", "explanation": "A."},
                )
            ],
        )
    ])

    assert QuizService._stored_question_explanation(
        "giải thích câu 2",
        session.get_all_question_records(),
    ) is None
