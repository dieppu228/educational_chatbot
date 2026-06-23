
import logging
import functools
import inspect
from typing import AsyncGenerator, Generator, Callable, Any

logger = logging.getLogger("chatbot.error")

GENERIC_USER_ERROR_MESSAGE = (
    "Hệ thống đang gặp lỗi tạm thời khi xử lý yêu cầu. "
    "Bạn thử lại sau ít phút nhé."
)


def user_facing_error_message(error: Exception | None = None) -> str:
    if error is None:
        return GENERIC_USER_ERROR_MESSAGE

    error_text = str(error).lower()
    if any(token in error_text for token in ("503", "unavailable", "overloaded")):
        return (
            "Dịch vụ AI đang quá tải hoặc tạm thời không sẵn sàng. "
            "Bạn thử lại sau ít phút nhé."
        )
    if any(token in error_text for token in ("429", "rate limit", "quota")):
        return (
            "Dịch vụ AI đang bị giới hạn tần suất. "
            "Bạn chờ một lát rồi thử lại nhé."
        )
    if "timeout" in error_text or "timed out" in error_text:
        return (
            "Yêu cầu xử lý quá lâu nên hệ thống đã dừng tác vụ. "
            "Bạn thử lại với yêu cầu ngắn hơn nhé."
        )
    if any(token in error_text for token in ("api key", "unauthenticated", "401", "403", "permission")):
        return (
            "Cấu hình dịch vụ AI chưa hợp lệ hoặc chưa đủ quyền. "
            "Vui lòng kiểm tra lại cấu hình hệ thống."
        )
    return GENERIC_USER_ERROR_MESSAGE


def safe_execute(
    fallback_message: str = "Đã xảy ra lỗi. Vui lòng thử lại.",
    log_prefix: str = "",
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            prefix = log_prefix or func.__qualname__
            try:
                result = func(*args, **kwargs)
                # Nếu là generator, wrap trong try-except
                if hasattr(result, '__next__'):
                    return _safe_generator(result, prefix, fallback_message)
                if inspect.isasyncgen(result):
                    return _safe_async_generator(result, prefix, fallback_message)
                return result
            except Exception as e:
                logger.error(f"[{prefix}] {e}", exc_info=True)
                return f"{fallback_message}. {user_facing_error_message(e)}"
        return wrapper
    return decorator


def _safe_generator(
    gen: Generator,
    prefix: str,
    fallback_message: str,
) -> Generator:
    try:
        yield from gen
    except Exception as e:
        logger.error(f"[{prefix}] Generator error: {e}", exc_info=True)
        yield f"\n\n{fallback_message}. {user_facing_error_message(e)}"


async def _safe_async_generator(
    gen: AsyncGenerator,
    prefix: str,
    fallback_message: str,
) -> AsyncGenerator[str, None]:
    try:
        async for chunk in gen:
            yield chunk
    except Exception as e:
        logger.error(f"[{prefix}] Async generator error: {e}", exc_info=True)
        yield f"\n\n{fallback_message}. {user_facing_error_message(e)}"


def format_error_response(error: Exception, max_length: int = 100) -> str:
    return user_facing_error_message(error)


__all__ = ["safe_execute", "format_error_response", "user_facing_error_message"]
