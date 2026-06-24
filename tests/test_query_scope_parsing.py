from types import SimpleNamespace

from src.llm.utils import extract_num_questions
from src.schemas.context import RequestContext


def test_extract_num_questions_uses_question_units_only():
    assert extract_num_questions(
        "cho tôi bài tập bài 1 chủ đề C đi nào khoảng 3-4 câu trắc nghiệm nhé"
    ) == 3
    assert extract_num_questions(
        "Bài tập trắc nghiệm Tin học lớp 10 Bài 1 Chủ đề C"
    ) is None
    assert extract_num_questions(
        "Câu hỏi trắc nghiệm 3-4 câu cho Bài 1 Chủ đề C môn Tin học lớp 10"
    ) == 3
    assert extract_num_questions("tạo 5 câu hỏi trắc nghiệm") == 5


def test_resolve_grade_uses_rewrite_when_query_has_no_grade():
    ctx = RequestContext(
        query="cho tôi bài tập bài 1 chủ đề C đi nào khoảng 3-4 câu trắc nghiệm nhé"
    )
    ctx.enriched_query = "Ngữ cảnh trước đó: Tin học lớp 10 Cánh Diều"
    ctx.queries_for_rag = [
        "Bài tập trắc nghiệm Tin học lớp 10 Bài 1 Chủ đề C",
        "Câu hỏi trắc nghiệm 3-4 câu cho Bài 1 Chủ đề C môn Tin học lớp 10",
    ]
    ctx.intent_result = SimpleNamespace(
        topic="TỔ CHỨC LƯU TRỮ, TÌM KIẾM VÀ TRAO ĐỔI THÔNG TIN - Lưu trữ trực tuyến"
    )
    ctx.session = SimpleNamespace(metadata={}, book=None)

    ctx.resolve_grade()

    assert ctx.effective_grade == "10"
    assert ctx.scope_grade_source == "rewrite"
    assert ctx.session.metadata["grade"] == "10"


def test_resolve_grade_prefers_explicit_query_over_rewrite():
    ctx = RequestContext(query="tạo 3 câu trắc nghiệm Tin học lớp 11")
    ctx.enriched_query = "Ngữ cảnh trước đó: Tin học lớp 10"
    ctx.queries_for_rag = ["Câu hỏi trắc nghiệm Tin học lớp 10"]
    ctx.intent_result = SimpleNamespace(topic=None)
    ctx.session = SimpleNamespace(metadata={}, book=None)

    ctx.resolve_grade()

    assert ctx.effective_grade == "11"
    assert ctx.scope_grade_source == "query"
