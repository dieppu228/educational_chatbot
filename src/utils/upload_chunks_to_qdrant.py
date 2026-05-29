import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

import numpy as np


PROJECT_DIR = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from src.config.config import settings
from src.rag.chunking import (
    ChunkTypeClassifier,
    HierarchicalChunker,
    chunks_to_json,
    save_chunks,
)
from src.rag.embedding import embed_and_save
from src.rag.split_clean_books import main as split_clean_books


def require_qdrant_client():
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.http import models
    except ImportError as exc:
        raise SystemExit(
            "Missing qdrant-client. Install it with:\n"
            "  venv/bin/python -m pip install qdrant-client\n"
            "or:\n"
            "  venv/bin/python -m pip install -r requirements.txt"
        ) from exc
    return QdrantClient, models


def load_chunks(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def iter_batches(items: list, batch_size: int) -> Iterable[list]:
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]


def rebuild_chunks(chunks_path: Path, classify_with_llm: bool = True) -> list[dict]:
    print("Splitting clean book files into structured Markdown...")
    split_clean_books()

    print("\nRebuilding chunks from structured CD/KNTT folders...")
    chunker = HierarchicalChunker(min_chunk_chars=100, max_chunk_chars=2000)
    chunks = chunker.chunk_structured_books(str(PROJECT_DIR))

    if classify_with_llm:
        classifier = ChunkTypeClassifier(
            cache_path=str(PROJECT_DIR / settings.DATA_DIR / settings.CHUNK_TYPE_CACHE_FILE),
            model_name=settings.CHUNK_TYPE_MODEL,
            batch_size=settings.CHUNK_TYPE_BATCH_SIZE,
            timeout_seconds=settings.CHUNK_TYPE_TIMEOUT_SECONDS,
            enabled=True,
        )
        chunks = classifier.classify(chunks)

    save_chunks(chunks, str(chunks_path))
    return chunks_to_json(chunks)


def ensure_embeddings(
    chunks_path: Path,
    embeddings_path: Path,
    expected_count: int,
    force: bool,
) -> np.ndarray:
    if embeddings_path.exists() and not force:
        embeddings = np.load(embeddings_path)
        if embeddings.shape[0] == expected_count:
            print(f"Using existing embeddings: {embeddings_path} shape={embeddings.shape}")
            return np.asarray(embeddings, dtype=np.float32)
        print(
            f"Embedding count mismatch: chunks={expected_count}, "
            f"embeddings={embeddings.shape[0]}. Rebuilding embeddings..."
        )

    embeddings = embed_and_save(
        chunks_path=str(chunks_path),
        embeddings_path=str(embeddings_path),
        model_name=settings.EMBEDDING_MODEL,
        device="cpu",
        batch_size=64,
        use_context=True,
    )
    return np.asarray(embeddings, dtype=np.float32)


def create_or_recreate_collection(
    client,
    models,
    collection_name: str,
    vector_size: int,
    recreate: bool,
) -> None:
    existing = {collection.name for collection in client.get_collections().collections}

    if collection_name in existing and recreate:
        print(f"Deleting existing Qdrant collection: {collection_name}")
        client.delete_collection(collection_name=collection_name)
        existing.remove(collection_name)

    if collection_name not in existing:
        print(f"Creating Qdrant collection: {collection_name} vector_size={vector_size}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )
        return

    info = client.get_collection(collection_name=collection_name)
    current_size = info.config.params.vectors.size
    if current_size != vector_size:
        raise SystemExit(
            f"Collection '{collection_name}' has vector size {current_size}, "
            f"but embeddings have size {vector_size}. Re-run with --recreate."
        )
    print(f"Using existing Qdrant collection: {collection_name}")


def build_point(models, idx: int, chunk: dict, vector: np.ndarray):
    payload = {
        "chunk_id": chunk.get("chunk_id", ""),
        "content": chunk.get("content", ""),
        "breadcrumb": chunk.get("breadcrumb", ""),
        "book": chunk.get("book", ""),
        "grade": chunk.get("grade", ""),
        "topic": chunk.get("topic", ""),
        "topic_name": chunk.get("topic_name", ""),
        "lesson": chunk.get("lesson", ""),
        "lesson_name": chunk.get("lesson_name", ""),
        "section_title": chunk.get("section_title", ""),
        "type": chunk.get("type", ""),
    }
    point_id = chunk.get("chunk_id") or idx
    return models.PointStruct(id=point_id, vector=vector.tolist(), payload=payload)


def upload_to_qdrant(
    chunks: list[dict],
    embeddings: np.ndarray,
    qdrant_url: str,
    collection_name: str,
    batch_size: int,
    recreate: bool,
) -> None:
    if len(chunks) != embeddings.shape[0]:
        raise SystemExit(
            f"Chunks and embeddings mismatch: chunks={len(chunks)}, embeddings={embeddings.shape}"
        )

    QdrantClient, models = require_qdrant_client()
    client = QdrantClient(url=qdrant_url, timeout=60)
    vector_size = int(embeddings.shape[1])

    create_or_recreate_collection(
        client=client,
        models=models,
        collection_name=collection_name,
        vector_size=vector_size,
        recreate=recreate,
    )

    point_indexes = list(range(len(chunks)))
    total = len(point_indexes)
    uploaded = 0

    print(f"Uploading {total} chunks to {qdrant_url}/{collection_name}...")
    for batch_indexes in iter_batches(point_indexes, batch_size):
        points = [
            build_point(models, idx, chunks[idx], embeddings[idx])
            for idx in batch_indexes
        ]
        client.upsert(collection_name=collection_name, points=points, wait=True)
        uploaded += len(points)
        print(f"  uploaded {uploaded}/{total}")

    info = client.get_collection(collection_name=collection_name)
    print(
        "Qdrant upload completed | "
        f"collection={collection_name} points={info.points_count} vectors={vector_size}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild SGK chunks and upload them to Qdrant as a storage collection."
    )
    parser.add_argument("--qdrant-url", default=settings.QDRANT_URL)
    parser.add_argument("--collection", default=settings.QDRANT_COLLECTION)
    parser.add_argument("--batch-size", type=int, default=settings.QDRANT_UPLOAD_BATCH_SIZE)
    parser.add_argument("--skip-chunking", action="store_true")
    parser.add_argument("--skip-llm-classification", action="store_true")
    parser.add_argument("--force-embeddings", action="store_true")
    parser.add_argument("--no-recreate", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = PROJECT_DIR / settings.DATA_DIR
    chunks_path = data_dir / settings.CHUNKS_FILE
    embeddings_path = data_dir / settings.EMBEDDINGS_FILE

    if args.skip_chunking:
        chunks = load_chunks(chunks_path)
        print(f"Loaded existing chunks: {chunks_path} count={len(chunks)}")
    else:
        chunks = rebuild_chunks(
            chunks_path,
            classify_with_llm=not args.skip_llm_classification,
        )

    embeddings = ensure_embeddings(
        chunks_path=chunks_path,
        embeddings_path=embeddings_path,
        expected_count=len(chunks),
        force=args.force_embeddings,
    )

    upload_to_qdrant(
        chunks=chunks,
        embeddings=embeddings,
        qdrant_url=args.qdrant_url,
        collection_name=args.collection,
        batch_size=args.batch_size,
        recreate=not args.no_recreate,
    )

    print("\nCustomSearch remains file-backed:")
    print(f"  chunks={chunks_path}")
    print(f"  embeddings={embeddings_path}")
    print("Qdrant is used only as a storage mirror by this script.")


if __name__ == "__main__":
    main()
