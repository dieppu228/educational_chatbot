from src.llm.action_planner import Action, ActionPlanner
from src.llm.intent_router import IntentResult
from src.llm.memory import QuestionRecord, QuizRound, QuizSessionState, Session, SlideSessionState


def test_plan_all_drops_chat_when_content_action_exists():
    planner = ActionPlanner()
    plans = planner.plan_all(
        [
            IntentResult(primary_intent="generate", task_type="mcq"),
            IntentResult(primary_intent="chat"),
        ],
        session=None,
        message="cho tôi bài tập",
    )

    assert [plan.action for plan in plans] == [Action.GENERATE_QUIZ]


def test_plan_all_keeps_chat_when_it_is_the_only_action():
    planner = ActionPlanner()
    plans = planner.plan_all(
        [IntentResult(primary_intent="chat")],
        session=None,
        message="xin chào",
    )

    assert [plan.action for plan in plans] == [Action.CHAT]


def test_explain_intent_with_quiz_state_routes_to_explain_question():
    planner = ActionPlanner()
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
                        "correct_answer": "A",
                        "explanation": "Vì dữ liệu là dạng biểu diễn của thông tin.",
                    },
                )
            ],
        )
    ])

    plan = planner.plan(
        IntentResult(primary_intent="explain"),
        session,
        "giải thích giúp tôi câu 1",
    )

    assert plan.action == Action.EXPLAIN_QUESTION


def test_interact_with_slide_exercises_routes_to_answer_exercise():
    planner = ActionPlanner()
    session = Session()
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

    plan = planner.plan(
        IntentResult(primary_intent="interact"),
        session,
        "câu 1 A",
    )

    assert plan.action == Action.ANSWER_EXERCISE


def test_chat_answer_key_followup_with_slide_exercises_routes_to_answer_exercise():
    planner = ActionPlanner()
    session = Session()
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

    plan = planner.plan(
        IntentResult(primary_intent="chat", is_new_topic=True),
        session,
        "cho tôi đáp án",
    )

    assert plan.action == Action.ANSWER_EXERCISE
