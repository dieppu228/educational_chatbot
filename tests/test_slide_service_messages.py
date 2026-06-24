from src.llm.services.slide_service import SlideService


def test_quality_block_message_is_user_facing_for_slide():
    message = SlideService._quality_block_user_message("slide")

    assert "slide" in message
    assert "quality review failed" not in message.lower()
    assert "FORMAT_INVALID" not in message
    assert "range()" not in message


def test_quality_block_message_is_user_facing_for_lesson_plan():
    message = SlideService._quality_block_user_message("lesson_plan")

    assert "giáo án" in message
    assert "quality review failed" not in message.lower()
