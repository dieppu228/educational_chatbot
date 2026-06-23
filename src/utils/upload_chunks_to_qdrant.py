import argparse
import hashlib
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


def chunk_full_content(chunk: dict) -> str:
    content = chunk.get("content", "")
    breadcrumb = chunk.get("breadcrumb", "")
    return chunk.get("full_content") or (f"{breadcrumb} : {content}" if breadcrumb else content)


def embedding_source_fingerprint(chunks: list[dict]) -> str:
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(str(chunk.get("chunk_id", "")).encode("utf-8"))
        digest.update(b"\0")
        digest.update(chunk_full_content(chunk).encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def load_embeddings_meta(meta_path: Path) -> dict:
    if not meta_path.exists():
        return {}
    try:
        with meta_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_embeddings_meta(meta_path: Path, chunks: list[dict], embeddings: np.ndarray) -> None:
    meta = {
        "text_field": "full_content",
        "chunk_count": len(chunks),
        "embedding_shape": list(embeddings.shape),
        "source_fingerprint": embedding_source_fingerprint(chunks),
    }
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


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
    chunks: list[dict],
    chunks_path: Path,
    embeddings_path: Path,
    meta_path: Path,
    expected_count: int,
    force: bool,
    device: str,
    batch_size: int,
) -> np.ndarray:
    if embeddings_path.exists() and not force:
        embeddings = np.load(embeddings_path)
        meta = load_embeddings_meta(meta_path)
        expected_fingerprint = embedding_source_fingerprint(chunks)
        meta_matches = (
            meta.get("text_field") == "full_content"
            and meta.get("chunk_count") == expected_count
            and meta.get("source_fingerprint") == expected_fingerprint
        )
        finite_vectors = np.isfinite(embeddings).all()
        if embeddings.shape[0] == expected_count and meta_matches and finite_vectors:
            print(f"Using existing embeddings: {embeddings_path} shape={embeddings.shape}")
            return np.asarray(embeddings, dtype=np.float32)
        print(
            "Embedding source mismatch. Rebuilding embeddings from full_content..."
        )

    embeddings = embed_and_save(
        chunks_path=str(chunks_path),
        embeddings_path=str(embeddings_path),
        model_name=settings.EMBEDDING_MODEL,
        device=device,
        batch_size=batch_size,
        use_context=True,
    )
    save_embeddings_meta(meta_path, chunks, embeddings)
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
    content = chunk.get("content", "")
    breadcrumb = chunk.get("breadcrumb", "")
    full_content = chunk_full_content(chunk)
    payload = {
        "chunk_id": chunk.get("chunk_id", ""),
        "content": content,
        "full_content": full_content,
        "breadcrumb": breadcrumb,
        "book": chunk.get("book", ""),
        "grade": chunk.get("grade", ""),
        "topic": chunk.get("topic", ""),
        "topic_name": chunk.get("topic_name", ""),
        "lesson": chunk.get("lesson", ""),
        "lesson_name": chunk.get("lesson_name", ""),
        "section_title": chunk.get("section_title", ""),
        "type": chunk.get("type", ""),
        "level": chunk.get("level", ""),
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
    client = QdrantClient(url=qdrant_url, timeout=settings.QDRANT_TIMEOUT_SECONDS)
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
    parser.add_argument("--embedding-device", default=settings.EMBEDDING_DEVICE)
    parser.add_argument("--embedding-batch-size", type=int, default=settings.EMBEDDING_BATCH_SIZE)
    parser.add_argument("--no-recreate", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = PROJECT_DIR / settings.DATA_DIR
    chunks_path = data_dir / settings.CHUNKS_FILE
    embeddings_path = data_dir / settings.EMBEDDINGS_FILE
    embeddings_meta_path = data_dir / settings.EMBEDDINGS_META_FILE

    if args.skip_chunking:
        chunks = load_chunks(chunks_path)
        print(f"Loaded existing chunks: {chunks_path} count={len(chunks)}")
    else:
        chunks = rebuild_chunks(
            chunks_path,
            classify_with_llm=not args.skip_llm_classification,
        )

    embeddings = ensure_embeddings(
        chunks=chunks,
        chunks_path=chunks_path,
        embeddings_path=embeddings_path,
        meta_path=embeddings_meta_path,
        expected_count=len(chunks),
        force=args.force_embeddings,
        device=args.embedding_device,
        batch_size=args.embedding_batch_size,
    )

    upload_to_qdrant(
        chunks=chunks,
        embeddings=embeddings,
        qdrant_url=args.qdrant_url,
        collection_name=args.collection,
        batch_size=args.batch_size,
        recreate=not args.no_recreate,
    )

    print("\nCustomSearch can load from local files or Qdrant storage:")
    print(f"  chunks={chunks_path}")
    print(f"  embeddings={embeddings_path}")
    print("  qdrant_loader=CustomSearch.from_qdrant()")


if __name__ == "__main__":
    main()
