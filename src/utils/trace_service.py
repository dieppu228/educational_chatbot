
import json
from pathlib import Path
from typing import Dict, Any, Optional

from src.schemas.context import RequestContext
from src.utils.trace_decorator import logger, trace_node

# ============================================================
# TRACE FILE
# ============================================================

_project_root = Path(__file__).resolve().parent.parent.parent
_log_dir = _project_root / "logs"
_log_dir.mkdir(exist_ok=True)
_trace_file = _log_dir / "pipeline_trace.log"


# ============================================================
# TRACE SERVICE
# ============================================================

class TraceService:

    def __init__(self, trace_file: Optional[Path] = None):
        self.trace_file = trace_file or _trace_file
        self.logger = logger

    def write_trace(self, ctx: RequestContext, response_preview: str = ""):
        trace_data = ctx.to_debug_dict()
        trace_data["total_time_s"] = ctx.elapsed_time

        if response_preview:
            trace_data["response"] = {
                "length": len(response_preview),
                "preview": response_preview[:500],
            }

        try:
            with open(str(self.trace_file), 'a', encoding='utf-8') as f:
                f.write(json.dumps(trace_data, indent=2, ensure_ascii=False, default=str))
                f.write("\n---\n")  # Separator giữa các request
        except Exception as e:
            self.logger.error(f"Failed to write JSON trace: {e}")

    def log_step(self, ctx: RequestContext, node: str, **kwargs):
        ctx.add_debug_step(node, **kwargs)

        # Log summary ra console
        summary_parts = [f"{node}"]
        for k, v in kwargs.items():
            if k in ("time_s", "status", "action", "primary_intent", "strategy"):
                summary_parts.append(f"{k}={v}")
        self.logger.info(" | ".join(summary_parts))

    def log_info(self, msg: str):
        self.logger.info(msg)

    def log_error(self, msg: str):
        self.logger.error(msg)

    def log_warning(self, msg: str):
        self.logger.warning(msg)


# Singleton instance cho toàn project
trace_service = TraceService()

__all__ = ["TraceService", "trace_service", "logger", "trace_node"]
