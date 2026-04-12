"""
Error Handling Utilities — Standardized error wrapper.

Thay thế try-catch rải rác trong từng handler.
Chuẩn hóa format error response cho user-facing messages.
"""

import logging
import functools
from typing import Generator, Callable, Any

logger = logging.getLogger("chatbot.error")


def safe_execute(
    fallback_message: str = "Đã xảy ra lỗi. Vui lòng thử lại.",
    log_prefix: str = "",
) -> Callable:
    """
    Decorator wrap handler methods để catch exceptions thống nhất.

    Usage:
        @safe_execute(fallback_message="Lỗi sinh câu hỏi", log_prefix="QuizService")
        def generate_quiz(self, ctx, ...):
            ...

    Hỗ trợ cả generator functions (yield) và regular functions (return).
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            prefix = log_prefix or func.__qualname__
            try:
                result = func(*args, **kwargs)
                # Nếu là generator, wrap trong try-except
                if hasattr(result, '__next__'):
                    return _safe_generator(result, prefix, fallback_message)
                return result
            except Exception as e:
                logger.error(f"[{prefix}] {e}", exc_info=True)
                return fallback_message
        return wrapper
    return decorator


def _safe_generator(
    gen: Generator,
    prefix: str,
    fallback_message: str,
) -> Generator:
    """Wrap generator trong try-except để catch lỗi giữa chừng."""
    try:
        yield from gen
    except Exception as e:
        logger.error(f"[{prefix}] Generator error: {e}", exc_info=True)
        yield f"\n\n⚠️ {fallback_message}: {str(e)[:100]}"


def format_error_response(error: Exception, max_length: int = 100) -> str:
    """
    Chuẩn hóa error message cho user-facing response.

    Không leak stack trace hay internal details.
    """
    error_str = str(error)
    if len(error_str) > max_length:
        error_str = error_str[:max_length] + "..."
    return f"⚠️ Đã xảy ra lỗi: {error_str}"


__all__ = ["safe_execute", "format_error_response"]
