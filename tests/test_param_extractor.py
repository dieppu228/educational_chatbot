from types import SimpleNamespace

from src.llm.intent_router import IntentResult
from src.llm.param_extractor import ParamExtractor
from src.schemas.context import RequestContext


def test_param_extractor_deterministic_ignores_grade_and_lesson_numbers_for_count():
    params = ParamExtractor(api_key="").extract(
        query="cho tôi bài tập bài 1 chủ đề C đi nào khoảng 3-4 câu trắc nghiệm nhé",
        enriched_query="",
        rag_queries=["Bài tập trắc nghiệm Tin học lớp 10 Bài 1 Chủ đề C"],
        history_context="",
    )

    assert params["lesson_reference"].lower() == "bài 1 chủ đề c"
    assert params["topic_ref"] == "C"
    assert params["lesson_num"] == "1"
    assert params["question_count"] == 3
    assert params["question_count_range"] == [3, 4]
    assert params["task_type"] == "mcq"
    assert params["grade"] == "10"


def test_param_extractor_does_not_treat_lesson_reference_as_question_count():
    params = ParamExtractor(api_key="").extract(
        query="Bài tập trắc nghiệm Tin học lớp 10 Bài 1 Chủ đề C",
    )

    assert params["grade"] == "10"
    assert params["lesson_num"] == "1"
    assert params["question_count"] is None


def test_request_context_uses_param_book_and_grade_for_shared_scope():
    ctx = RequestContext(query="cho tôi bài tập bài 1 chủ đề C")
    ctx.extracted_params = {
        "book": "CD",
        "grade": "10",
        "lesson_reference": "bài 1 chủ đề C",
    }
    ctx.intent_result = IntentResult(primary_intent="generate", task_type="mcq")
    ctx.session = SimpleNamespace(metadata={}, book=None)

    ctx.resolve_book()
    ctx.resolve_grade()

    assert ctx.effective_book == "CD"
    assert ctx.scope_book_source == "param"
    assert ctx.effective_grade == "10"
    assert ctx.scope_grade_source == "param"
    assert ctx.scope_is_soft is False


def test_request_context_prefers_explicit_query_grade_over_param():
    ctx = RequestContext(query="tạo 3 câu trắc nghiệm Tin học lớp 11")
    ctx.extracted_params = {"grade": "10"}
    ctx.intent_result = IntentResult(primary_intent="generate", task_type="mcq")
    ctx.session = SimpleNamespace(metadata={}, book=None)

    ctx.resolve_grade()

    assert ctx.effective_grade == "11"
    assert ctx.scope_grade_source == "query"
