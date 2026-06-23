import asyncio

from src.utils.error_handling import safe_execute, user_facing_error_message


def test_user_facing_error_hides_raw_provider_payload():
    message = user_facing_error_message(
        RuntimeError(
            "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently overloaded'}}"
        )
    )

    assert "Dịch vụ AI đang quá tải" in message
    assert "UNAVAILABLE" not in message
    assert "This model" not in message


def test_safe_execute_generator_hides_raw_exception():
    @safe_execute(fallback_message="Lỗi sinh câu hỏi", log_prefix="test")
    def broken_generator():
        yield "Đang xử lý..."
        raise RuntimeError("503 UNAVAILABLE. secret provider payload")

    output = "".join(broken_generator())

    assert "Đang xử lý..." in output
    assert "Lỗi sinh câu hỏi" in output
    assert "Dịch vụ AI đang quá tải" in output
    assert "secret provider payload" not in output


def test_safe_execute_async_generator_hides_raw_exception():
    @safe_execute(fallback_message="Lỗi tạo slide", log_prefix="test_async")
    async def broken_async_generator():
        yield "Đang xử lý..."
        raise RuntimeError("429 rate limit raw payload")

    async def collect_output():
        chunks = []
        async for chunk in broken_async_generator():
            chunks.append(chunk)
        return "".join(chunks)

    output = asyncio.run(collect_output())

    assert "Đang xử lý..." in output
    assert "Lỗi tạo slide" in output
    assert "giới hạn tần suất" in output
    assert "raw payload" not in output
