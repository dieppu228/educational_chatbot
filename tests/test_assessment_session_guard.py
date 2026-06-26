from src.llm.intent_router import IntentResult
from src.llm.memory import Session, SlideSessionState
from src.llm.orchestrator import Orchestrator
from src.schemas.context import RequestContext


class FakeMemory:
    def __init__(self, session):
        self.session = session

    def get_current_session(self, user_id):
        return self.session


def test_preserve_active_slide_exercise_session_for_answer_key_followup():
    session = Session(user_id="student", topic="Mạng máy tính")
    session.slide_state = SlideSessionState()
    session.slide_state.add_exercise(
        question_type="mcq",
        content={
            "question": "Thiết bị nào dùng để kết nối mạng?",
            "correct_answer": "A",
            "explanation": "Router dùng để kết nối mạng.",
        },
        slide_idx=3,
        q_idx=0,
    )

    orchestrator = object.__new__(Orchestrator)
    orchestrator.memory = FakeMemory(session)
    ctx = RequestContext(query="cho tôi đáp án", user_id="student")
    ctx.intent_results = [
        IntentResult(
            primary_intent="chat",
            topic="Đáp án",
            is_new_topic=True,
        )
    ]
    ctx.intent_result = ctx.intent_results[0]

    orchestrator._preserve_active_assessment_session(ctx)

    assert ctx.intent_result.primary_intent == "interact"
    assert ctx.intent_result.is_new_topic is False
    assert ctx.debug_steps[-1]["node"] == "SessionGuard"
