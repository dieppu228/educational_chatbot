from src.llm.action_planner import Action, ActionPlanner
from src.llm.intent_router import IntentResult
from src.llm.memory import QuestionRecord, QuizRound, QuizSessionState, Session


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
