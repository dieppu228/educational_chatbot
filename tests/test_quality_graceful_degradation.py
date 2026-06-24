from types import SimpleNamespace

from langgraph.graph import END

from src.llm.graphs.content_supervisor import reflection_decision_node, route_after_reflection
from src.llm.memory import Session
from src.llm.services.slide_service import SlideService
from src.schemas.slide_schemas import build_quality_warnings, classify_quality


def _soft_review():
    return {
        "passed": False,
        "score": 6.0,
        "reason_fail": "CONTENT_INCOMPLETE",
        "summary": "Một số slide cần bổ sung ví dụ.",
        "issues": [
            {
                "case": "missing_example",
                "severity": "major",
                "message": "Thiếu ví dụ minh họa vòng lặp for.",
                "suggestion": "Bổ sung ví dụ tính tổng.",
            }
        ],
        "reflection_action": "block",
        "revision_instruction": "Bổ sung ví dụ.",
    }


def _critical_review():
    review = _soft_review()
    review["score"] = 6.0
    review["issues"] = [
        {
            "case": "unsafe",
            "severity": "critical",
            "message": "Nội dung không an toàn.",
        }
    ]
    return review


def _merged_slides():
    return [
        {
            "slide_id": "s1",
            "slide_type": "content",
            "title": "Cấu trúc lặp for",
            "bullets": ["Cú pháp for", "Ví dụ tính tổng"],
            "source_chunk_ids": ["c1"],
        }
    ]


def test_classify_quality_approve_warn_and_block():
    assert classify_quality(
        {"passed": True, "reflection_action": "approve", "score": 9},
        has_deck=True,
        hard_floor=4.0,
    ) == "approve"
    assert classify_quality(_soft_review(), has_deck=True, hard_floor=4.0) == "warn"
    assert classify_quality(_critical_review(), has_deck=True, hard_floor=4.0) == "block"
    assert classify_quality({"score": 3.5}, has_deck=True, hard_floor=4.0) == "block"
    assert classify_quality(_soft_review(), has_deck=False, hard_floor=4.0) == "block"
    assert classify_quality(None, has_deck=True, hard_floor=4.0) == "warn"
    assert classify_quality(
        {
            "passed": False,
            "score": 0,
            "reason_fail": "FORMAT_INVALID",
            "issues": [{"severity": "critical", "message": "Reviewer failed."}],
            "reflection_action": "block",
        },
        has_deck=True,
        hard_floor=4.0,
    ) == "warn"


def test_classify_quality_media_critical_is_warning_when_deck_exists():
    assert classify_quality(
        {
            "passed": False,
            "score": 1.0,
            "reason_fail": "MEDIA_WEAK",
            "issues": [
                {
                    "case": "UNCLEAR_REQUIREMENT",
                    "severity": "critical",
                    "target": "media",
                    "message": "Cùng một ảnh được dùng lại cho nhiều slide.",
                }
            ],
            "reflection_action": "block",
        },
        has_deck=True,
        hard_floor=0.0,
    ) == "warn"


def test_build_quality_warnings_uses_issue_message_and_suggestion():
    warnings = build_quality_warnings(_soft_review())

    assert warnings == ["Thiếu ví dụ minh họa vòng lặp for. Gợi ý: Bổ sung ví dụ tính tổng."]


def test_reflection_decision_soft_fail_keeps_deck():
    result = reflection_decision_node(
        {
            "quality_review": _soft_review(),
            "merged_slides": _merged_slides(),
            "reflection_attempts": 2,
        }
    )

    assert result["status"] == "success"
    assert result["quality_blocked"] is False
    assert "merged_slides" not in result


def test_route_after_reflection_ends_for_soft_degraded_success():
    assert route_after_reflection(
        {
            "status": "success",
            "quality_blocked": False,
            "quality_review": {
                "passed": False,
                "reflection_action": "revise_content",
            },
            "reflection_attempts": 2,
        }
    ) == END


def test_route_after_reflection_revises_before_max_attempts():
    assert route_after_reflection(
        {
            "quality_blocked": False,
            "quality_review": {
                "passed": False,
                "reflection_action": "revise_content",
            },
            "reflection_attempts": 1,
        }
    ) == "supervisor"


def test_reflection_decision_critical_fail_blocks():
    result = reflection_decision_node(
        {
            "quality_review": _critical_review(),
            "merged_slides": _merged_slides(),
            "reflection_attempts": 2,
        }
    )

    assert result["status"] == "failed"
    assert result["quality_blocked"] is True


def test_slide_service_soft_quality_fail_renders_deck_with_warning():
    service = SlideService.__new__(SlideService)
    service._attach_export_if_needed = lambda *args, **kwargs: None
    ctx = SimpleNamespace(debug_steps=[])
    ctx.add_debug_step = lambda name, **data: ctx.debug_steps.append({"name": name, **data})
    session = Session()

    chunks = list(service._process_completed_result(
        {
            "status": "failed",
            "quality_blocked": True,
            "merged_slides": _merged_slides(),
            "outline_payload": {"lesson_title": "Bài lặp for"},
            "quality_review": _soft_review(),
            "reflection_attempts": 2,
        },
        session,
        ctx,
        pipeline_time=1.2,
        task_type="slide",
    ))
    output = "".join(chunks)

    assert "Không thể tạo" not in output
    assert "Đã tạo 1 slide sections" in output
    assert "Slide đã tạo nhưng còn vài điểm nên chỉnh sửa thêm" in output
    assert session.slide_state.slide_output["quality_verdict"] == "warn"
    assert session.slide_state.slide_output["quality_warnings"]


def test_slide_service_critical_quality_fail_blocks_deck():
    service = SlideService.__new__(SlideService)
    ctx = SimpleNamespace(debug_steps=[])
    ctx.add_debug_step = lambda name, **data: ctx.debug_steps.append({"name": name, **data})
    session = Session()
    slide_state = session.ensure_slide_state()
    slide_state.slide_output = {
        "_interrupt": True,
        "_hitl": {"type": "outline_review"},
        "_graph_thread_id": "slide-old",
        "_graph_config": {"configurable": {"thread_id": "slide-old"}},
    }

    chunks = list(service._process_completed_result(
        {
            "status": "failed",
            "quality_blocked": True,
            "merged_slides": _merged_slides(),
            "outline_payload": {"lesson_title": "Bài lặp for"},
            "quality_review": _critical_review(),
            "reflection_attempts": 2,
        },
        session,
        ctx,
        pipeline_time=1.2,
        task_type="slide",
    ))
    output = "".join(chunks)

    assert "Mình chưa tạo được slide đạt chất lượng" in output
    assert "Đã tạo 1 slide sections" not in output
    assert service.get_pending_hitl(session) is None
    assert slide_state.slide_output["_interrupt"] is False
    assert "_hitl" not in slide_state.slide_output


def test_slide_service_success_replaces_pending_hitl_state():
    service = SlideService.__new__(SlideService)
    service._attach_export_if_needed = lambda *args, **kwargs: None
    ctx = SimpleNamespace(debug_steps=[])
    ctx.add_debug_step = lambda name, **data: ctx.debug_steps.append({"name": name, **data})
    session = Session()
    slide_state = session.ensure_slide_state()
    slide_state.slide_output = {
        "_interrupt": True,
        "_hitl": {"type": "outline_review"},
        "_graph_thread_id": "slide-old",
        "_graph_config": {"configurable": {"thread_id": "slide-old"}},
    }

    chunks = list(service._process_completed_result(
        {
            "status": "success",
            "quality_blocked": False,
            "merged_slides": _merged_slides(),
            "outline_payload": {"lesson_title": "Bài lặp for"},
            "quality_review": {
                "passed": True,
                "score": 8,
                "reflection_action": "approve",
                "issues": [],
            },
            "reflection_attempts": 0,
        },
        session,
        ctx,
        pipeline_time=1.2,
        task_type="slide",
    ))

    assert "Đã tạo 1 slide sections" in "".join(chunks)
    assert service.get_pending_hitl(session) is None
    assert slide_state.slide_output["_interrupt"] is False
    assert "_hitl" not in slide_state.slide_output
