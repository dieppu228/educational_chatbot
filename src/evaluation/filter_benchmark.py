"""Deterministic filters for retrieval benchmark candidates.

This script implements Step 2:
- remove exact/normalized duplicate questions;
- remove template-shaped questions;
- remove title leakage only when a long phrase overlaps with lesson/breadcrumb text.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)

TEMPLATE_PATTERNS = [
    re.compile(r"^trong bai hoc ve\b", re.IGNORECASE),
    re.compile(r"^hay neu cac y chinh\b.*\bkhi hoc ve\b", re.IGNORECASE),
    re.compile(r"^neu gap mot tinh huong thuc te lien quan den\b", re.IGNORECASE),
    re.compile(r"^khi thuc hien yeu cau lien quan den\b", re.IGNORECASE),
]


def strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFD", text or "")
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.replace("đ", "d").replace("Đ", "D")


def normalize_text(text: str) -> str:
    text = strip_accents(text).lower()
    return " ".join(TOKEN_RE.findall(text))


def tokens(text: str) -> list[str]:
    norm = normalize_text(text)
    return norm.split() if norm else []


def token_ngrams(text: str, n: int = 5) -> set[str]:
    ts = tokens(text)
    return {" ".join(ts[i : i + n]) for i in range(0, max(0, len(ts) - n + 1))}


def has_template_shape(question: str) -> bool:
    norm = normalize_text(question)
    return any(pattern.search(norm) for pattern in TEMPLATE_PATTERNS)


def has_title_leakage(question: str, title_texts: list[str], min_ngram: int) -> bool:
    q_ngrams = token_ngrams(question, min_ngram)
    if not q_ngrams:
        return False

    for text in title_texts:
        title_ngrams = token_ngrams(text, min_ngram)
        if q_ngrams & title_ngrams:
            return True
    return False


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def build_seed_index(chunks_path: Path) -> dict[str, dict[str, Any]]:
    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    return {chunk["chunk_id"]: chunk for chunk in chunks if "chunk_id" in chunk}


def title_texts_for(row: dict[str, Any], seed_index: dict[str, dict[str, Any]]) -> list[str]:
    seed = seed_index.get(row.get("seed_chunk_id", ""), {})
    gold = row.get("gold_lesson_key") or {}
    candidates = [
        seed.get("breadcrumb", ""),
        seed.get("lesson_name", ""),
        gold.get("lesson_name", ""),
    ]
    # Section titles are intentionally ignored: they often contain legitimate
    # content terms and are not part of the strict title-leak rule for Step 2.
    return [text for text in candidates if text]


def filter_rows(
    rows: list[dict[str, Any]],
    seed_index: dict[str, dict[str, Any]],
    min_title_ngram: int,
) -> tuple[list[dict[str, Any]], Counter[str], list[dict[str, str]]]:
    kept: list[dict[str, Any]] = []
    dropped: list[dict[str, str]] = []
    reasons: Counter[str] = Counter()
    seen_questions: set[str] = set()

    for row in rows:
        question = row.get("question", "")
        q_norm = normalize_text(question)

        reason = ""
        if not q_norm:
            reason = "empty_question"
        elif q_norm in seen_questions:
            reason = "duplicate_exact_normalized"
        elif has_template_shape(question):
            reason = "template_question"
        elif has_title_leakage(question, title_texts_for(row, seed_index), min_title_ngram):
            reason = "title_leakage"

        if reason:
            reasons[reason] += 1
            dropped.append(
                {
                    "id": str(row.get("id", "")),
                    "seed_chunk_id": str(row.get("seed_chunk_id", "")),
                    "reason": reason,
                    "question": question,
                }
            )
            continue

        seen_questions.add(q_norm)
        kept.append(row)

    return kept, reasons, dropped


def lesson_key(row: dict[str, Any], seed_index: dict[str, dict[str, Any]]) -> tuple[str, str, str, str, str]:
    gold = row.get("gold_lesson_key") or {}
    seed = seed_index.get(row.get("seed_chunk_id", ""), {})
    return (
        gold.get("book") or seed.get("book", ""),
        gold.get("grade") or seed.get("grade", ""),
        gold.get("topic_name") or seed.get("topic_name", ""),
        gold.get("lesson") or seed.get("lesson", ""),
        gold.get("lesson_name") or seed.get("lesson_name", ""),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="data/eval/retrieval/benchmark_raw.jsonl",
        help="Raw Step 1 JSONL file.",
    )
    parser.add_argument(
        "--chunks",
        default="data/rag_chunks_v2.json",
        help="Chunk database JSON file.",
    )
    parser.add_argument(
        "--output",
        default="data/eval/retrieval/benchmark_filtered.jsonl",
        help="Filtered Step 2 JSONL file.",
    )
    parser.add_argument(
        "--report",
        default="data/eval/retrieval/benchmark_filtered_report.json",
        help="Filter report JSON file.",
    )
    parser.add_argument(
        "--dropped",
        default="data/eval/retrieval/benchmark_dropped.jsonl",
        help="Dropped rows with reasons.",
    )
    parser.add_argument("--min-title-ngram", type=int, default=5)
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))
    seed_index = build_seed_index(Path(args.chunks))
    kept, reasons, dropped = filter_rows(rows, seed_index, args.min_title_ngram)

    output = Path(args.output)
    report_path = Path(args.report)
    dropped_path = Path(args.dropped)
    write_jsonl(output, kept)
    write_jsonl(dropped_path, dropped)

    report = {
        "input": args.input,
        "output": args.output,
        "dropped": args.dropped,
        "input_count": len(rows),
        "kept_count": len(kept),
        "dropped_count": len(rows) - len(kept),
        "drop_reasons": dict(sorted(reasons.items())),
        "covered_lessons": len({lesson_key(row, seed_index) for row in kept}),
        "min_title_ngram": args.min_title_ngram,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
