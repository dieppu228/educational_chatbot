"""Light Step 3 validation and final sampling for retrieval benchmark.

This is intentionally pragmatic: it does not call any LLM. It applies the
deterministic Step 2 filters, then keeps questions that are self-contained enough
and whose anchor is present in the seed content. The final benchmark removes
answer-only fields and samples 250 rows stratified by book-grade and lesson.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from filter_benchmark import (
    build_seed_index,
    filter_rows,
    load_jsonl,
    normalize_text,
)


VAGUE_PATTERNS = [
    re.compile(r"\b(phần này|đoạn trên|ở trên|nó|chúng nó|điều này)\b", re.IGNORECASE),
    re.compile(r"\b(trong bài này|bài học này|bài học về)\b", re.IGNORECASE),
]

QUESTION_TEMPLATE_PATTERNS = [
    re.compile(r"^trong bài học về\b", re.IGNORECASE),
    re.compile(r"^hãy nêu các ý chính\b.*\bkhi học về\b", re.IGNORECASE),
    re.compile(r"^nếu gặp một tình huống thực tế liên quan đến\b", re.IGNORECASE),
    re.compile(r"^khi thực hiện yêu cầu liên quan đến\b", re.IGNORECASE),
]

QUESTION_TYPE_ORDER = {
    "application": 0,
    "process": 1,
    "definition": 2,
    "list": 3,
    "compare": 4,
}


def strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFD", text or "")
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.replace("đ", "d").replace("Đ", "D")


def norm(text: str) -> str:
    return normalize_text(text)


def contains_normalized(haystack: str, needle: str) -> bool:
    n = norm(needle)
    return bool(n) and n in norm(haystack)


def is_self_contained(question: str) -> bool:
    question = question.strip()
    if len(question) < 18 or not question.endswith("?"):
        return False
    if any(pattern.search(question) for pattern in VAGUE_PATTERNS):
        return False
    if any(pattern.search(question) for pattern in QUESTION_TEMPLATE_PATTERNS):
        return False
    return True


def anchor_valid(row: dict[str, Any]) -> bool:
    anchor = str(row.get("anchor", "")).strip()
    seed_content = str(row.get("seed_content", "")).strip()
    if len(norm(anchor).split()) > 10:
        return False
    if len(norm(anchor)) < 2:
        return False
    return contains_normalized(seed_content, anchor)


def answerable(row: dict[str, Any]) -> bool:
    # Light validation: if the anchor and expected answer both come from
    # seed_content, the question is answerable enough for retrieval testing.
    seed_content = str(row.get("seed_content", ""))
    expected_answer = str(row.get("expected_answer", ""))
    anchor = str(row.get("anchor", ""))
    if not contains_normalized(seed_content, anchor):
        return False
    answer_tokens = set(norm(expected_answer).split())
    content_tokens = set(norm(seed_content).split())
    if not answer_tokens:
        return False
    overlap = len(answer_tokens & content_tokens) / max(1, len(answer_tokens))
    return overlap >= 0.6


def lesson_key(row: dict[str, Any]) -> tuple[str, str, str, str, str]:
    key = row.get("gold_lesson_key") or {}
    return (
        str(key.get("book", "")),
        str(key.get("grade", "")),
        str(key.get("topic_name", "")),
        str(key.get("lesson", "")),
        str(key.get("lesson_name", "")),
    )


def book_grade(row: dict[str, Any]) -> str:
    key = row.get("gold_lesson_key") or {}
    return f"{key.get('book', '')}-{key.get('grade', '')}"


def question_score(row: dict[str, Any]) -> tuple[int, int, int, str]:
    qtype = str(row.get("question_type", ""))
    difficulty = str(row.get("difficulty", ""))
    question = str(row.get("question", ""))
    # Prefer a useful mix but keep deterministic ordering.
    diff_score = {"medium": 0, "easy": 1, "hard": 2}.get(difficulty, 3)
    return (QUESTION_TYPE_ORDER.get(qtype, 9), diff_score, len(question), str(row.get("id", "")))


def validate_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], Counter[str]]:
    accepted = []
    rejected = []
    reasons: Counter[str] = Counter()
    seen_questions = set()

    for row in rows:
        q_norm = norm(str(row.get("question", "")))
        reason = ""
        if q_norm in seen_questions:
            reason = "duplicate_question"
        elif not anchor_valid(row):
            reason = "anchor_invalid"
        elif not is_self_contained(str(row.get("question", ""))):
            reason = "not_self_contained"
        elif not answerable(row):
            reason = "not_answerable"

        if reason:
            reasons[reason] += 1
            rejected.append(
                {
                    "id": row.get("id"),
                    "reason": reason,
                    "question": row.get("question"),
                    "anchor": row.get("anchor"),
                }
            )
            continue

        seen_questions.add(q_norm)
        validated = dict(row)
        validated["validation"] = {
            "answerable": True,
            "self_contained": True,
            "anchor_valid": True,
            "validator": "codex_light_rules_v1",
        }
        accepted.append(validated)

    return accepted, rejected, reasons


def target_by_group(groups: list[str], total: int) -> dict[str, int]:
    base = total // len(groups)
    remainder = total % len(groups)
    return {group: base + (1 if idx < remainder else 0) for idx, group in enumerate(groups)}


def target_by_type(rows: list[dict[str, Any]], total: int) -> dict[str, int]:
    counts = Counter(str(row.get("question_type", "")) for row in rows)
    raw_targets = {
        qtype: max(1, round(total * count / max(1, len(rows))))
        for qtype, count in counts.items()
    }
    while sum(raw_targets.values()) > total:
        qtype = max(raw_targets, key=lambda key: (raw_targets[key], counts[key]))
        raw_targets[qtype] -= 1
    while sum(raw_targets.values()) < total:
        qtype = max(counts, key=lambda key: counts[key] - raw_targets.get(key, 0))
        raw_targets[qtype] = raw_targets.get(qtype, 0) + 1
    return raw_targets


def choose_balanced_row(
    bucket: list[dict[str, Any]],
    selected_type_counts: Counter[str],
    type_targets: dict[str, int],
) -> dict[str, Any]:
    def balance_key(row: dict[str, Any]) -> tuple[float, tuple[int, int, int, str]]:
        qtype = str(row.get("question_type", ""))
        target = max(1, type_targets.get(qtype, 1))
        fill_ratio = selected_type_counts[qtype] / target
        return (fill_ratio, question_score(row))

    return min(bucket, key=balance_key)


def stratified_sample(rows: list[dict[str, Any]], total: int) -> list[dict[str, Any]]:
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[book_grade(row)].append(row)

    groups = sorted(by_group)
    targets = target_by_group(groups, total)
    type_targets = target_by_type(rows, total)
    selected_type_counts: Counter[str] = Counter()
    selected: list[dict[str, Any]] = []
    selected_ids = set()

    # First pass: keep at most one item per lesson per group until the group
    # quota is mostly filled. This preserves coverage.
    for group in groups:
        lesson_buckets: dict[tuple[str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
        for row in by_group[group]:
            lesson_buckets[lesson_key(row)].append(row)
        for bucket in lesson_buckets.values():
            bucket.sort(key=question_score)

        for key in sorted(lesson_buckets):
            if sum(1 for row in selected if book_grade(row) == group) >= targets[group]:
                break
            row = choose_balanced_row(lesson_buckets[key], selected_type_counts, type_targets)
            selected.append(row)
            selected_ids.add(row["id"])
            selected_type_counts[str(row.get("question_type", ""))] += 1

    # Second pass: fill remaining quotas with best remaining rows.
    for group in groups:
        current = sum(1 for row in selected if book_grade(row) == group)
        remaining = [row for row in by_group[group] if row["id"] not in selected_ids]
        remaining.sort(key=lambda row: (
            selected_type_counts[str(row.get("question_type", ""))] / max(1, type_targets.get(str(row.get("question_type", "")), 1)),
            question_score(row),
        ))
        for row in remaining:
            if current >= targets[group]:
                break
            selected.append(row)
            selected_ids.add(row["id"])
            selected_type_counts[str(row.get("question_type", ""))] += 1
            current += 1

    # If a group did not have enough rows, fill globally.
    if len(selected) < total:
        remaining = [row for row in rows if row["id"] not in selected_ids]
        remaining.sort(key=lambda row: (book_grade(row), question_score(row)))
        for row in remaining[: total - len(selected)]:
            selected.append(row)

    selected.sort(key=lambda row: str(row.get("id", "")))
    return selected[:total]


def final_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "query_id": row["id"],
        "query": row["question"],
        "question_type": row["question_type"],
        "difficulty": row["difficulty"],
        "anchor": row.get("anchor", ""),
        "seed_chunk_id": row["seed_chunk_id"],
        "source_level": row.get("source_level"),
        "gold_lesson_key": row["gold_lesson_key"],
        "gen_meta": row.get("gen_meta", {}),
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/eval/benchmark_raw.jsonl")
    parser.add_argument("--chunks", default="data/rag_chunks_v2.json")
    parser.add_argument("--validated", default="data/eval/benchmark_validated.jsonl")
    parser.add_argument("--rejected", default="data/eval/benchmark_rejected.jsonl")
    parser.add_argument("--final", default="data/eval/benchmark_eval.jsonl")
    parser.add_argument("--report", default="data/eval/benchmark_validate_report.json")
    parser.add_argument("--sample-size", type=int, default=250)
    args = parser.parse_args()

    raw_rows = load_jsonl(Path(args.input))
    seed_index = build_seed_index(Path(args.chunks))
    step2_rows, step2_reasons, step2_dropped = filter_rows(raw_rows, seed_index, min_title_ngram=5)
    accepted, rejected, step3_reasons = validate_rows(step2_rows)
    sampled = stratified_sample(accepted, args.sample_size)

    write_jsonl(Path(args.validated), accepted)
    write_jsonl(Path(args.rejected), step2_dropped + rejected)
    write_jsonl(Path(args.final), [final_row(row) for row in sampled])

    report = {
        "input": args.input,
        "raw_count": len(raw_rows),
        "after_step2_count": len(step2_rows),
        "validated_count": len(accepted),
        "final_count": len(sampled),
        "step2_drop_reasons": dict(sorted(step2_reasons.items())),
        "step3_drop_reasons": dict(sorted(step3_reasons.items())),
        "validated_covered_lessons": len({lesson_key(row) for row in accepted}),
        "final_covered_lessons": len({lesson_key(row) for row in sampled}),
        "final_by_group": dict(sorted(Counter(book_grade(row) for row in sampled).items())),
        "final_by_type": dict(sorted(Counter(row["question_type"] for row in sampled).items())),
        "final_by_difficulty": dict(sorted(Counter(row["difficulty"] for row in sampled).items())),
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
