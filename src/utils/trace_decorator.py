
import time
import logging
import functools
import inspect
from pathlib import Path
from typing import Generator as TypingGenerator

# ============================================================
# LOGGER SETUP (shared with trace_service.py)
# ============================================================

_project_root = Path(__file__).resolve().parent.parent.parent
_log_dir = _project_root / "logs"
_log_dir.mkdir(exist_ok=True)
_log_file = _log_dir / "app.log"

logger = logging.getLogger("chatbot")
logger.setLevel(logging.DEBUG)
logger.propagate = False

_fmt = logging.Formatter(
    "[%(asctime)s] %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S"
)

if not logger.handlers:
    _ch = logging.StreamHandler()
    _ch.setLevel(logging.INFO)
    _ch.setFormatter(_fmt)
    logger.addHandler(_ch)

    _fh = logging.FileHandler(str(_log_file), encoding="utf-8", mode="a")
    _fh.setLevel(logging.DEBUG)
    _fh.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(_fh)


# ============================================================
# TRACE NODE DECORATOR
# ============================================================

def _summarize_arg(val, max_len=200):
    if isinstance(val, str):
        return f'"{val[:max_len]}..."' if len(val) > max_len else f'"{val}"'
    if isinstance(val, list):
        return f"List[{len(val)} items]"
    if isinstance(val, dict):
        return f"Dict[{len(val)} keys]"
    if hasattr(val, '__class__'):
        name = val.__class__.__name__
        if name in ('RequestContext', 'QueryProfile', 'RAGResult', 'ActionPlan'):
            return f"<{name}>"
    return repr(val)[:max_len]


def _summarize_output(val, max_len=300):
    if isinstance(val, str):
        return f"str({len(val)} chars)"
    if isinstance(val, list):
        return f"List[{len(val)} items]"
    if isinstance(val, dict):
        keys = list(val.keys())[:5]
        return f"Dict{keys}"
    if hasattr(val, '__class__'):
        name = val.__class__.__name__
        if hasattr(val, '__dict__'):
            return f"<{name}>"
    return repr(val)[:max_len]


def trace_node(name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Build input summary (skip 'self')
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            input_parts = []
            for i, arg in enumerate(args):
                param_name = params[i] if i < len(params) else f"arg{i}"
                if param_name == "self":
                    continue
                input_parts.append(f"{param_name}={_summarize_arg(arg)}")
            for k, v in kwargs.items():
                input_parts.append(f"{k}={_summarize_arg(v)}")

            input_summary = ", ".join(input_parts) if input_parts else "(no args)"
            logger.info(f"[START] {name} | {input_summary}")

            t0 = time.time()
            try:
                result = func(*args, **kwargs)

                # Handle generator functions
                if inspect.isgeneratorfunction(func) or isinstance(result, TypingGenerator):
                    return _trace_generator(name, result, t0)

                elapsed = time.time() - t0
                logger.info(f"[ DONE] {name} | {_summarize_output(result)} | {elapsed:.2f}s")
                return result

            except Exception as e:
                elapsed = time.time() - t0
                logger.error(f"[ERROR] {name} | {type(e).__name__}: {e} | {elapsed:.2f}s")
                raise

        return wrapper
    return decorator


def _trace_generator(name, gen, t0):
    try:
        for item in gen:
            yield item
    except Exception as e:
        elapsed = time.time() - t0
        logger.error(f"[ERROR] {name} (generator) | {type(e).__name__}: {e} | {elapsed:.2f}s")
        raise
    finally:
        elapsed = time.time() - t0
        logger.info(f"[ DONE] {name} (generator) | {elapsed:.2f}s")


__all__ = ["trace_node", "logger"]
