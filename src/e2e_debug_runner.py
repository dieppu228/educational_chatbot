import argparse
import asyncio
import json
import logging
import multiprocessing
import sys
import time
from pathlib import Path
from typing import Any, Dict


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.config import project_path, settings
from src.rag.retrieve_rebuild import CustomSearch
from src.rag.reranker import Reranker
from src.llm.orchestrator import Orchestrator
from src.utils.trace_decorator import suppress_http_request_logs


LOG_DIR = project_path(settings.E2E_LOG_DIR)
DEFAULT_TIMEOUT_SECONDS = settings.E2E_TIMEOUT_SECONDS


def _json_default(value: Any) -> str:
    return str(value)


def setup_e2e_logging(log_file: Path, verbose: bool = False) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    suppress_http_request_logs()
    return logging.getLogger("e2e_debug_runner")


def validate_runtime_inputs() -> None:
    data_dir = project_path(settings.DATA_DIR)
    chunks_path = data_dir / settings.CHUNKS_FILE
    embeddings_path = data_dir / settings.EMBEDDINGS_FILE

    missing_files = [
        str(path)
        for path in (chunks_path, embeddings_path)
        if not path.is_file()
    ]
    if missing_files:
        raise FileNotFoundError(
            "Missing real RAG data files: " + ", ".join(missing_files)
        )

    if not settings.GENAI_API_KEY:
        raise RuntimeError(
            "GENAI_API_KEY is not set. The E2E runner calls the real LLM service "
            "and does not use mock data."
        )


def init_orchestrator(logger: logging.Logger) -> Orchestrator:
    data_dir = project_path(settings.DATA_DIR)
    chunks_path = data_dir / settings.CHUNKS_FILE
    embeddings_path = data_dir / settings.EMBEDDINGS_FILE

    logger.info("Loading CustomSearch: chunks=%s embeddings=%s", chunks_path, embeddings_path)
    searcher = CustomSearch(
        chunks_path=str(chunks_path),
        embeddings_path=str(embeddings_path),
    )

    logger.info("Initializing Reranker")
    reranker = Reranker()

    logger.info("Initializing Orchestrator")
    return Orchestrator(retriever=searcher, reranker=reranker)


async def run_query(args: argparse.Namespace, logger: logging.Logger) -> Dict[str, Any]:
    orchestrator = init_orchestrator(logger)

    logger.info("Starting E2E query")
    logger.info("query=%s", args.query)
    logger.info("book=%s user_id=%s", args.book, args.user_id)

    response_chunks = []
    async for chunk in orchestrator.ask_async(
        args.query,
        ui_book=args.book,
        user_id=args.user_id,
        auto_approve_outline=args.auto_approve_outline,
        graph_debug_stream=args.graph_debug_stream,
    ):
        response_chunks.append(chunk)
        if args.stream_response:
            print(chunk, end="", flush=True)

    response = "".join(response_chunks)
    debug_info = orchestrator.get_debug_info(args.user_id) or {}

    logger.info("E2E query complete: response_chars=%s", len(response))
    for index, step in enumerate(debug_info.get("steps", []), start=1):
        logger.info(
            "NODE[%02d] %s %s",
            index,
            step.get("node", "?"),
            json.dumps(step, ensure_ascii=False, default=_json_default)[:2000],
        )

    return {
        "query": args.query,
        "book": args.book,
        "user_id": args.user_id,
        "response": response,
        "debug": debug_info,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the educational chatbot end-to-end and write node-level debug logs."
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="Tạo 3 câu trắc nghiệm bài biến và kiểu dữ liệu Tin học 10 bộ KNTT",
        help="User query to send through the full orchestrator pipeline.",
    )
    parser.add_argument(
        "--book",
        choices=["CD", "KNTT"],
        default="KNTT",
        help="Book filter passed as ui_book.",
    )
    parser.add_argument(
        "--user-id",
        default="e2e-debug",
        help="Stable user id for the test session.",
    )
    parser.add_argument(
        "--no-auto-approve-outline",
        action="store_false",
        dest="auto_approve_outline",
        help="Do not auto-approve slide/lesson-plan outline HITL interrupts.",
    )
    parser.add_argument(
        "--no-graph-debug-stream",
        action="store_false",
        dest="graph_debug_stream",
        help="Use normal graph invoke instead of streaming LangGraph node logs.",
    )
    parser.add_argument(
        "--stream-response",
        action="store_true",
        help="Print response chunks as they are produced.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print debug logs to console.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Maximum seconds to wait for the full E2E run.",
    )
    parser.set_defaults(auto_approve_outline=True, graph_debug_stream=True)
    return parser.parse_args()


def execute(args: argparse.Namespace, log_file: Path, json_file: Path) -> int:
    logger = setup_e2e_logging(log_file, verbose=args.verbose)

    try:
        validate_runtime_inputs()
        result = asyncio.run(run_query(args, logger))
        json_file.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=_json_default),
            encoding="utf-8",
        )
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130
    except Exception as exc:
        logger.exception("E2E run failed: %s", exc)
        return 1

    if not args.stream_response:
        print(result["response"])
    print(f"\n\nDebug log: {log_file}")
    print(f"Debug JSON: {json_file}")
    return 0


def _execute_child(
    args: argparse.Namespace,
    log_file: Path,
    json_file: Path,
    result_queue: multiprocessing.Queue,
) -> None:
    result_queue.put(execute(args, log_file, json_file))


def main() -> int:
    args = parse_args()
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_file = LOG_DIR / f"e2e-{timestamp}.log"
    json_file = LOG_DIR / f"e2e-{timestamp}.json"

    if args.timeout <= 0:
        return execute(args, log_file, json_file)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    result_queue: multiprocessing.Queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=_execute_child,
        args=(args, log_file, json_file, result_queue),
    )
    process.start()
    process.join(args.timeout)

    if process.is_alive():
        process.terminate()
        process.join(5)
        if process.is_alive():
            process.kill()
            process.join()
        with log_file.open("a", encoding="utf-8") as f:
            f.write(f"\nE2E run timed out after {args.timeout} seconds\n")
        print(f"E2E run timed out after {args.timeout} seconds")
        print(f"Debug log: {log_file}")
        return 124

    if not result_queue.empty():
        return result_queue.get()
    return process.exitcode if process.exitcode is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
