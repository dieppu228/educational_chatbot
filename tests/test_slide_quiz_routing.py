from src.llm.graphs.content_supervisor import (
    route_after_post_tool,
    route_after_quiz_direct,
)
from src.llm.services.slide_merger import SlideMerger
from src.schemas.slide_schemas import AgentResult


def test_slide_content_routes_to_quiz_before_merge():
    state = {
        "task_type": "slide",
        "content_payload": {"slides": []},
        "quiz_payload": None,
        "media_payload": None,
        "messages": [],
        "query": "sinh slide bài giảng có ảnh minh họa",
    }

    assert route_after_post_tool(state) == "quiz_direct"


def test_quiz_direct_routes_to_media_when_query_requests_media():
    state = {
        "task_type": "slide",
        "content_payload": {"slides": []},
        "quiz_payload": {"quiz_items": [{"question": "Q?", "options": {}, "correct_answer": "A"}]},
        "media_payload": None,
        "query": "sinh slide có hình minh họa",
    }

    assert route_after_quiz_direct(state) == "media_direct"


def test_quiz_direct_routes_to_merge_without_media_request():
    state = {
        "task_type": "slide",
        "content_payload": {"slides": []},
        "quiz_payload": {"quiz_items": [{"question": "Q?", "options": {}, "correct_answer": "A"}]},
        "media_payload": None,
        "query": "sinh slide bài giảng",
    }

    assert route_after_quiz_direct(state) == "merge_direct"


def test_slide_merger_replaces_default_exercise_bullets_with_quiz_items():
    slides = SlideMerger().merge(
        outline_result=AgentResult(
            agent="outline",
            status="success",
            latency_ms=0,
            payload={
                "lesson_title": "Máy tính",
                "slides": [
                    {"slide_id": "s1", "slide_type": "title", "title": "Mở đầu"},
                    {
                        "slide_id": "s2",
                        "slide_type": "exercise",
                        "title": "Bài tập củng cố",
                        "key_points": ["Nêu ví dụ tự luận"],
                    },
                ],
            },
        ),
        content_result=AgentResult(
            agent="content",
            status="success",
            latency_ms=0,
            payload={"slides": []},
        ),
        media_result=AgentResult(agent="media", status="failed", latency_ms=0, payload={}),
        quiz_result=AgentResult(
            agent="quiz",
            status="success",
            latency_ms=0,
            payload={
                "quiz_items": [
                    {
                        "question": "Thiết bị nào dùng để kết nối mạng?",
                        "options": {"A": "Router", "B": "Bàn phím", "C": "Chuột", "D": "Màn hình"},
                        "correct_answer": "A",
                        "explanation": "Router kết nối và định tuyến giữa các mạng.",
                    }
                ]
            },
        ),
    )

    exercise_slide = slides[1]
    assert exercise_slide.questions
    assert exercise_slide.questions[0].correct_answer == "A"
    assert exercise_slide.bullets == ["Trả lời các câu hỏi trắc nghiệm sau"]
