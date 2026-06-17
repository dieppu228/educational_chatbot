import json
import logging
import numpy as np
import torch
import threading
from pathlib import Path
from typing import List, Optional
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("chatbot")


# ============================================================
# EMBEDDING MODEL
# ============================================================

class EmbeddingModel:
    _MODEL_CACHE = {}
    _LOAD_FAILED = set()
    _CACHE_LOCK = threading.RLock()
    _ENCODE_LOCK = threading.RLock()
    
    def __init__(
        self, 
        model_name: str = "dangvantuan/vietnamese-document-embedding",
        device: Optional[str] = None,
        batch_size: int = 64
    ):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.batch_size = batch_size
        self.model = None  # Lazy load
        self.load_failed = False
    
    def _cache_key(self):
        return (self.model_name, self.device)

    def _load_model(self):
        key = self._cache_key()
        with self._CACHE_LOCK:
            if self.load_failed or key in self._LOAD_FAILED:
                raise RuntimeError(f"Embedding model unavailable: {self.model_name}")

            cached = self._MODEL_CACHE.get(key)
            if cached is not None:
                self.model = cached
                return

            try:
                logger.info(
                    "Loading embedding model | model=%s device=%s",
                    self.model_name,
                    self.device,
                )
                try:
                    self.model = SentenceTransformer(
                        self.model_name,
                        trust_remote_code=True,
                        device=self.device,
                        local_files_only=True,
                    )
                except Exception as local_error:
                    logger.info(
                        "Local embedding model load failed, trying online load | model=%s error=%s",
                        self.model_name,
                        str(local_error)[:200],
                    )
                    self.model = SentenceTransformer(
                        self.model_name,
                        trust_remote_code=True,
                        device=self.device
                    )
                self._repair_position_ids()
                self._MODEL_CACHE[key] = self.model
                logger.info(
                    "Embedding model loaded | model=%s device=%s",
                    self.model_name,
                    self.device,
                )
            except Exception:
                self.load_failed = True
                self._LOAD_FAILED.add(key)
                raise

    def _repair_position_ids(self):
        transformer = self.model._modules.get("0") if hasattr(self.model, "_modules") else None
        auto_model = getattr(transformer, "auto_model", None)
        embeddings = getattr(auto_model, "embeddings", None)
        position_ids = getattr(embeddings, "position_ids", None)
        config = getattr(auto_model, "config", None)
        max_positions = getattr(config, "max_position_embeddings", None)

        if position_ids is None or max_positions is None:
            return

        expected_prefix = torch.arange(
            min(8, max_positions),
            device=position_ids.device,
            dtype=position_ids.dtype,
        )
        current_prefix = position_ids[: expected_prefix.numel()]
        if torch.equal(current_prefix, expected_prefix):
            return

        repaired = torch.arange(
            max_positions,
            device=position_ids.device,
            dtype=torch.long,
        )
        embeddings.register_buffer("position_ids", repaired, persistent=False)
        logger.warning(
            "Repaired embedding model position_ids buffer | model=%s max_positions=%s",
            self.model_name,
            max_positions,
        )

    def _record_bad_text(self, idx: int, text: str) -> None:
        try:
            log_path = Path(__file__).resolve().parents[2] / "logs" / "embedding_failures.txt"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as f:
                f.write(f"index={idx}\n")
                f.write(text)
                f.write("\n" + "-" * 40 + "\n")
        except Exception:
            logger.exception("Failed to record bad embedding text")
    
    def encode(self, texts: List[str], show_progress: bool = True) -> np.ndarray:
        self._load_model()

        with self._ENCODE_LOCK:
            embeddings = self.model.encode(
                texts,
                batch_size=self.batch_size,
                convert_to_numpy=True,
                normalize_embeddings=False,  # Normalize safely below for cosine similarity
                show_progress_bar=show_progress
            )

        embeddings = np.array(embeddings, dtype=np.float32)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        small_norms = norms < 1e-12
        if np.any(small_norms):
            logger.warning(
                "Embedding batch returned near-zero vectors; skipping normalization for %s rows",
                int(np.sum(small_norms)),
            )
            norms[small_norms] = 1.0
        embeddings = embeddings / norms
        if np.isfinite(embeddings).all():
            return embeddings

        logger.warning(
            "Embedding batch returned non-finite vectors; retrying one text at a time"
        )
        rows = []
        for idx, text in enumerate(texts):
            row = None
            try:
                with self._ENCODE_LOCK:
                    candidate = self.model.encode(
                        [text],
                        batch_size=1,
                        convert_to_numpy=True,
                        normalize_embeddings=False,
                        show_progress_bar=False,
                    )
            except Exception:
                logger.exception("Embedding single-text retry failed at index %s", idx)
                candidate = None

            if candidate is not None:
                candidate = np.array(candidate, dtype=np.float32)
                norm = np.linalg.norm(candidate, axis=1, keepdims=True)
                norm_value = float(norm[0, 0])
                if norm_value < 1e-12:
                    logger.warning(
                        "Embedding produced near-zero norm at text index %s; skipping normalization",
                        idx,
                    )
                    norm_value = 1.0
                candidate = candidate / norm_value
                if np.isfinite(candidate).all():
                    row = candidate[0]

            if row is None:
                self._record_bad_text(idx, text)
                dim = None
                if hasattr(self.model, "get_sentence_embedding_dimension"):
                    try:
                        dim = int(self.model.get_sentence_embedding_dimension())
                    except Exception:
                        dim = None
                if dim is None:
                    raise RuntimeError(
                        f"Embedding produced non-finite vector at text index {idx}"
                    )
                logger.error(
                    "Embedding produced non-finite vector at text index %s; using zero vector",
                    idx,
                )
                row = np.zeros(dim, dtype=np.float32)
            rows.append(row)

        return np.vstack(rows).astype(np.float32)
    
    def encode_query(self, query: str) -> np.ndarray:
        return self.encode([query], show_progress=False)[0]


# ============================================================
# EMBED CHUNKS PIPELINE
# ============================================================

def load_chunks(chunks_path: str) -> list:
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    print(f"Loaded {len(chunks)} chunks from {chunks_path}")
    return chunks


def prepare_texts(chunks: list, use_context: bool = True) -> List[str]:
    texts = []
    for chunk in chunks:
        content = chunk.get("content", "")
        if use_context:
            full_content = chunk.get("full_content", "")
            if full_content:
                texts.append(full_content)
                continue
            context = chunk.get("breadcrumb") or chunk.get("context", "")
            # Ghép context vào đầu content nếu có
            text = f"{context} : {content}" if context else content
        else:
            text = content
        texts.append(text)
    
    return texts


def embed_and_save(
    chunks_path: str,
    embeddings_path: str,
    model_name: str = "dangvantuan/vietnamese-document-embedding",
    device: str = "cpu",
    batch_size: int = 64,
    use_context: bool = True
):
    print("=" * 60)
    print("EMBEDDING CHUNKS PIPELINE")
    print("=" * 60)
    
    # 1. Load chunks
    chunks = load_chunks(chunks_path)
    
    # 2. Chuẩn bị texts
    texts = prepare_texts(chunks, use_context=use_context)
    print(f"Prepared {len(texts)} texts (use_context={use_context})")
    
    # 3. Embed
    model = EmbeddingModel(model_name=model_name, device=device, batch_size=batch_size)
    embeddings = model.encode(texts)
    print(f"Embeddings shape: {embeddings.shape}")
    
    # 4. Save
    output_path = Path(embeddings_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, embeddings)
    
    # 5. Verify
    loaded = np.load(output_path)
    assert loaded.shape == embeddings.shape, "Verification failed!"
    
    print(f"\nSaved embeddings -> {embeddings_path}")
    print(f"   Shape: {loaded.shape} | Dtype: {loaded.dtype}")
    print(f"   Size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
    print("=" * 60)
    
    return embeddings




# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # === Cấu hình ===
    PROJECT_DIR = Path(__file__).resolve().parent.parent
    
    CHUNKS_PATH = str(PROJECT_DIR / "data" / "rag_chunks_v2.json")
    EMBEDDINGS_PATH = str(PROJECT_DIR / "data" / "embeddings.npy")
    
    # === Chạy pipeline ===
    embed_and_save(
        chunks_path=CHUNKS_PATH,
        embeddings_path=EMBEDDINGS_PATH,
        device="cpu",
        batch_size=64,
        use_context=True,  # Embed context + content
    )
