"""Evaluate retrieval benchmark before and after reranking.

Gold relevance is lesson-level: a retrieved chunk is relevant when its metadata
matches the benchmark item's gold_lesson_key.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config.config import settings
from src.rag.retrieve_rebuild import CustomSearch
from src.rag.reranker import Reranker


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
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


def write_jsonl_row(file_obj, row: dict[str, Any]) -> None:
    file_obj.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    file_obj.flush()


def lesson_key_from_gold(gold: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        str(gold.get("book", "")),
        str(gold.get("grade", "")),
        str(gold.get("topic_name", "")),
        str(gold.get("lesson", "")),
        str(gold.get("lesson_name", "")),
    )


def lesson_key_from_result(result: dict[str, Any]) -> tuple[str, str, str, str, str]:
    metadata = result.get("metadata") or {}
    return (
        str(metadata.get("book", "")),
        str(metadata.get("grade", "")),
        str(metadata.get("topic_name", "")),
        str(metadata.get("lesson", "")),
        str(metadata.get("lesson_name", "")),
    )


def lesson_key_from_chunk(chunk: dict[str, Any]) -> tuple[str, str, str, str, str]:
    metadata = chunk.get("metadata") if isinstance(chunk.get("metadata"), dict) else chunk
    return (
        str(metadata.get("book", "")),
        str(metadata.get("grade", "")),
        str(metadata.get("topic_name", "")),
        str(metadata.get("lesson", "")),
        str(metadata.get("lesson_name", "")),
    )


def build_relevant_counts(chunks_path: Path) -> Counter[tuple[str, str, str, str, str]]:
    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    counts: Counter[tuple[str, str, str, str, str]] = Counter()
    for chunk in chunks:
        counts[lesson_key_from_chunk(chunk)] += 1
    return counts


def is_relevant(result: dict[str, Any], gold_key: tuple[str, str, str, str, str]) -> bool:
    return lesson_key_from_result(result) == gold_key


def dcg(relevances: list[int]) -> float:
    return sum(rel / math.log2(rank + 2) for rank, rel in enumerate(relevances))


def ranking_metrics(
    results: list[dict[str, Any]],
    gold_key: tuple[str, str, str, str, str],
    total_relevant: int,
    ks: list[int],
) -> dict[str, float]:
    rels = [1 if is_relevant(result, gold_key) else 0 for result in results]
    metrics: dict[str, float] = {}
    first_relevant_rank = next((idx + 1 for idx, rel in enumerate(rels) if rel), None)

    for k in ks:
        top_rels = rels[:k]
        relevant_at_k = sum(top_rels)
        ideal_rels = [1] * min(total_relevant, k)
        ideal_dcg = dcg(ideal_rels)

        metrics[f"hit@{k}"] = 1.0 if relevant_at_k > 0 else 0.0
        metrics[f"recall@{k}"] = relevant_at_k / total_relevant if total_relevant else 0.0
        metrics[f"precision@{k}"] = relevant_at_k / k if k else 0.0
        metrics[f"mrr@{k}"] = (
            1.0 / first_relevant_rank
            if first_relevant_rank is not None and first_relevant_rank <= k
            else 0.0
        )
        metrics[f"ndcg@{k}"] = dcg(top_rels) / ideal_dcg if ideal_dcg else 0.0

    return metrics


def compact_result(result: dict[str, Any]) -> dict[str, Any]:
    metadata = result.get("metadata") or {}
    return {
        "doc_id": result.get("doc_id"),
        "score": result.get("score"),
        "rerank_score": result.get("rerank_score"),
        "book": metadata.get("book"),
        "grade": metadata.get("grade"),
        "topic_name": metadata.get("topic_name"),
        "lesson": metadata.get("lesson"),
        "lesson_name": metadata.get("lesson_name"),
        "title": metadata.get("title"),
        "type": metadata.get("type"),
        "level": metadata.get("level"),
    }


def aggregate(rows: list[dict[str, Any]], ks: list[int], metric_prefix: str) -> dict[str, float]:
    if not rows:
        return {f"{metric_prefix}.{metric}@{k}": 0.0 for k in ks for metric in ["hit", "recall", "precision", "mrr", "ndcg"]}

    summary: dict[str, float] = {}
    metric_names = ["hit", "recall", "precision", "mrr", "ndcg"]
    for metric_name in metric_names:
        for k in ks:
            key = f"{metric_prefix}.{metric_name}@{k}"
            summary[key] = sum(float(row["metrics"][metric_prefix][f"{metric_name}@{k}"]) for row in rows) / len(rows)
    return summary


def group_value(row: dict[str, Any], group_by: str) -> str:
    gold = row.get("gold_lesson_key") or {}
    if group_by == "book_grade":
        return f"{gold.get('book', '')}-{gold.get('grade', '')}"
    return str(row.get(group_by) or gold.get(group_by) or "")


def write_summary_csv(path: Path, summaries: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summaries:
            writer.writerow(row)


def evaluate(args: argparse.Namespace) -> dict[str, Any]:
    benchmark_path = Path(args.benchmark)
    chunks_path = Path(args.chunks)
    embeddings_path = Path(args.embeddings)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    benchmark = load_jsonl(benchmark_path)
    if args.limit:
        benchmark = benchmark[: args.limit]

    ks = sorted({int(k) for k in args.ks.split(",") if k.strip()})
    if not ks:
        raise ValueError("--ks must contain at least one integer")

    retrieve_top_k = max(args.retrieve_top_k, max(ks))
    search_pool = max(args.search_pool, retrieve_top_k)
    after_top_n = args.after_top_n or retrieve_top_k

    relevant_counts = build_relevant_counts(chunks_path)
    retriever = CustomSearch(chunks_path=str(chunks_path), embeddings_path=str(embeddings_path))
    reranker = None if args.skip_rerank else Reranker(model_name=args.reranker_model, device=args.reranker_device)

    per_query_path = output_dir / args.per_query_name
    per_query_rows = []
    started = time.time()

    with per_query_path.open("w", encoding="utf-8") as per_query_file:
        for idx, item in enumerate(benchmark, start=1):
            query = item["query"]
            gold_key = lesson_key_from_gold(item["gold_lesson_key"])
            total_relevant = relevant_counts.get(gold_key, 0)

            t0 = time.time()
            before_results = retriever.search(query, top_k=retrieve_top_k, top_n=search_pool)
            retrieve_s = time.time() - t0

            t1 = time.time()
            if reranker is None:
                after_results = before_results[:after_top_n]
                rerank_s = 0.0
                rerank_status = "skipped"
            else:
                after_results = reranker.rerank(query, [dict(result) for result in before_results], top_n=after_top_n)
                rerank_s = time.time() - t1
                rerank_status = (
                    "ok"
                    if any(result.get("rerank_score") is not None for result in after_results)
                    else "fallback_no_scores"
                )

            before_metrics = ranking_metrics(before_results, gold_key, total_relevant, ks)
            after_metrics = ranking_metrics(after_results, gold_key, total_relevant, ks)

            row = {
                "query_id": item["query_id"],
                "query": query,
                "question_type": item.get("question_type"),
                "difficulty": item.get("difficulty"),
                "anchor": item.get("anchor"),
                "seed_chunk_id": item.get("seed_chunk_id"),
                "gold_lesson_key": item["gold_lesson_key"],
                "total_relevant_chunks": total_relevant,
                "metrics": {
                    "before_rerank": before_metrics,
                    "after_rerank": after_metrics,
                },
                "timing": {
                    "retrieve_s": round(retrieve_s, 4),
                    "rerank_s": round(rerank_s, 4),
                },
                "retriever_stats": getattr(retriever, "last_search_stats", {}),
                "rerank_status": rerank_status,
                "before_rerank_results": [compact_result(result) for result in before_results[: max(ks)]],
                "after_rerank_results": [compact_result(result) for result in after_results[: max(ks)]],
            }
            per_query_rows.append(row)
            write_jsonl_row(per_query_file, row)

            if args.progress_every and (idx % args.progress_every == 0 or idx == len(benchmark)):
                print(f"[{idx}/{len(benchmark)}] evaluated query_id={item['query_id']}")

    overall = {
        "group": "overall",
        "group_value": "all",
        "count": len(per_query_rows),
        **aggregate(per_query_rows, ks, "before_rerank"),
        **aggregate(per_query_rows, ks, "after_rerank"),
    }

    grouped_summaries = [overall]
    for group_by in ["book_grade", "question_type", "difficulty"]:
        buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in per_query_rows:
            buckets[group_value(row, group_by)].append(row)
        for value in sorted(buckets):
            grouped_summaries.append(
                {
                    "group": group_by,
                    "group_value": value,
                    "count": len(buckets[value]),
                    **aggregate(buckets[value], ks, "before_rerank"),
                    **aggregate(buckets[value], ks, "after_rerank"),
                }
            )

    fieldnames = list(grouped_summaries[0].keys())
    summary_csv_path = output_dir / args.summary_csv_name
    write_summary_csv(summary_csv_path, grouped_summaries, fieldnames)

    summary = {
        "benchmark": str(benchmark_path),
        "per_query": str(per_query_path),
        "summary_csv": str(summary_csv_path),
        "count": len(per_query_rows),
        "ks": ks,
        "retrieve_top_k": retrieve_top_k,
        "search_pool": search_pool,
        "after_top_n": after_top_n,
        "skip_rerank": args.skip_rerank,
        "elapsed_s": round(time.time() - started, 3),
        "overall": overall,
    }
    summary_json_path = output_dir / args.summary_json_name
    summary_json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default="data/eval/retrieval_benchmark_final_250_v1.jsonl")
    parser.add_argument("--chunks", default=f"{settings.DATA_DIR}/{settings.CHUNKS_FILE}")
    parser.add_argument("--embeddings", default=f"{settings.DATA_DIR}/{settings.EMBEDDINGS_FILE}")
    parser.add_argument("--output-dir", default="data/eval/retrieval_eval")
    parser.add_argument("--ks", default="1,3,5,10")
    parser.add_argument("--retrieve-top-k", type=int, default=settings.RETRIEVER_TOP_K)
    parser.add_argument("--search-pool", type=int, default=50)
    parser.add_argument("--after-top-n", type=int, default=0, help="0 means keep retrieve_top_k after rerank.")
    parser.add_argument("--skip-rerank", action="store_true")
    parser.add_argument("--reranker-model", default=settings.RERANKER_MODEL)
    parser.add_argument("--reranker-device", default=None)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--per-query-name", default="retrieval_eval_per_query.jsonl")
    parser.add_argument("--summary-csv-name", default="retrieval_eval_summary.csv")
    parser.add_argument("--summary-json-name", default="retrieval_eval_summary.json")
    args = parser.parse_args()

    evaluate(args)


if __name__ == "__main__":
    main()
