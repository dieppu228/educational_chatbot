from src.llm.action_planner import Action, ActionPlanner
from src.llm.intent_router import IntentResult


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
