"""One-off: bơm field `level` thật (từ heading depth của chunker) vào
data/rag_chunks_v2.json bằng cách match theo chunk_id.

Không đổi type/thứ tự/nội dung; chỉ thêm `level`. Nếu chunk_id không match
được (hiếm), fallback suy ra level từ số tầng breadcrumb để không bỏ trống.
"""
import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from src.rag.chunking import HierarchicalChunker

CHUNKS_PATH = PROJECT_DIR / "data" / "rag_chunks_v2.json"


def infer_level_from_breadcrumb(breadcrumb: str) -> int:
    parts = [p.strip() for p in (breadcrumb or "").split(" > ") if p.strip()]
    return len(parts)


def main() -> None:
    chunker = HierarchicalChunker(min_chunk_chars=100, max_chunk_chars=2000)
    rebuilt = chunker.chunk_structured_books(str(PROJECT_DIR))
    level_by_id = {c.chunk_id: c.metadata.level for c in rebuilt}
    print(f"\nRebuilt {len(rebuilt)} chunks -> {len(level_by_id)} unique ids")

    with CHUNKS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    matched = 0
    fallback = 0
    for c in data:
        cid = c.get("chunk_id")
        if cid in level_by_id:
            c["level"] = level_by_id[cid]
            matched += 1
        else:
            c["level"] = infer_level_from_breadcrumb(c.get("breadcrumb", ""))
            fallback += 1

    print(f"Existing chunks: {len(data)} | matched_by_id={matched} | fallback={fallback}")

    from collections import Counter
    print("Level distribution (real):", dict(sorted(Counter(c["level"] for c in data).items())))

    with CHUNKS_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved -> {CHUNKS_PATH}")


if __name__ == "__main__":
    main()
