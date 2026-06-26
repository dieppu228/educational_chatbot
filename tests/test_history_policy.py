import asyncio

from src.llm.context_analyzer import ContextAnalyzer
from src.llm.intent_router import IntentResult
from src.llm.memory import Session, SlideSessionState
from src.llm.orchestrator import Orchestrator
from src.schemas.context import RequestContext


class FakeMemory:
    def __init__(self, session):
        self.session = session

    def get_current_session(self, user_id):
        return self.session


def _orchestrator_with_session(session):
    orchestrator = object.__new__(Orchestrator)
    orchestrator.memory = FakeMemory(session)
    orchestrator.context_analyzer = ContextAnalyzer()
    return orchestrator


class CapturingIntentRouter:
    def __init__(self):
        self.session_messages = "not-called"

    async def detect_multi_async(self, query, current_topic=None, session_messages=None):
        self.session_messages = session_messages
        return [IntentResult(primary_intent="chat", is_new_topic=False)]


def test_history_resets_for_explicit_generate_with_different_topic():
    session = Session(user_id="student", topic="Dữ liệu và thông tin")
    session.add_message("user", "tạo quiz về dữ liệu và thông tin")
    session.add_message("assistant", "OLD_QUIZ_MARKER")
    orchestrator = _orchestrator_with_session(session)
    ctx = RequestContext(query="sinh slide về mạng máy tính", user_id="student")

    orchestrator._prepare_history_context(ctx)

    assert ctx.history_mode == "reset"
    assert ctx.history_reason == "topic_changed"
    assert ctx.history_context == ""
    assert ctx.debug_steps[-1]["node"] == "HistoryPolicy"
    assert ctx.debug_steps[-1]["messages_used"] == 0


def test_history_kept_for_explicit_generate_with_same_topic():
    session = Session(user_id="student", topic="Dữ liệu và thông tin")
    session.add_message("user", "tạo quiz về dữ liệu và thông tin")
    session.add_message("assistant", "OLD_QUIZ_MARKER")
    orchestrator = _orchestrator_with_session(session)
    ctx = RequestContext(query="sinh slide về dữ liệu và thông tin", user_id="student")

    orchestrator._prepare_history_context(ctx)

    assert ctx.history_mode == "same_topic"
    assert "OLD_QUIZ_MARKER" in ctx.history_context
    assert ctx.debug_steps[-1]["messages_used"] == 2


def test_history_kept_for_assessment_followup():
    session = Session(user_id="student", topic="Mạng máy tính")
    session.slide_state = SlideSessionState()
    session.slide_state.add_exercise(
        question_type="mcq",
        content={"question": "Router dùng để làm gì?", "correct_answer": "A"},
        slide_idx=3,
        q_idx=0,
    )
    session.add_message("assistant", "SLIDE_EXERCISE_MARKER")
    orchestrator = _orchestrator_with_session(session)
    ctx = RequestContext(query="cho tôi đáp án", user_id="student")

    orchestrator._prepare_history_context(ctx)

    assert ctx.history_mode == "same_topic"
    assert ctx.history_reason == "assessment_followup"
    assert "SLIDE_EXERCISE_MARKER" in ctx.history_context


def test_intent_router_does_not_receive_messages_when_history_resets():
    session = Session(user_id="student", topic="Dữ liệu và thông tin")
    session.add_message("assistant", "OLD_QUIZ_MARKER")
    orchestrator = _orchestrator_with_session(session)
    orchestrator.intent_router = CapturingIntentRouter()
    ctx = RequestContext(query="sinh slide về mạng máy tính", user_id="student")

    orchestrator._prepare_history_context(ctx)
    asyncio.run(orchestrator._detect_intent_async(ctx))

    assert ctx.history_mode == "reset"
    assert orchestrator.intent_router.session_messages is None


def test_intent_router_receives_messages_when_history_is_same_topic():
    session = Session(user_id="student", topic="Dữ liệu và thông tin")
    session.add_message("assistant", "OLD_QUIZ_MARKER")
    orchestrator = _orchestrator_with_session(session)
    orchestrator.intent_router = CapturingIntentRouter()
    ctx = RequestContext(query="sinh slide về dữ liệu và thông tin", user_id="student")

    orchestrator._prepare_history_context(ctx)
    asyncio.run(orchestrator._detect_intent_async(ctx))

    assert ctx.history_mode == "same_topic"
    assert orchestrator.intent_router.session_messages is not None
