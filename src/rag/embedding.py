import json
import logging
import numpy as np
import torch
from pathlib import Path
from typing import List, Optional
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("chatbot")


# ============================================================
# EMBEDDING MODEL
# ============================================================

class EmbeddingModel:
    
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
    
    def _load_model(self):
        if self.load_failed:
            raise RuntimeError(f"Embedding model unavailable: {self.model_name}")
        if self.model is None:
            try:
                print(f"Loading embedding model: {self.model_name}...")
                self.model = SentenceTransformer(
                    self.model_name,
                    trust_remote_code=True,
                    device=self.device
                )
                self._repair_position_ids()
                print(f"Model loaded on {self.device}")
            except Exception:
                self.load_failed = True
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
    
    def encode(self, texts: List[str], show_progress: bool = True) -> np.ndarray:
        self._load_model()
        
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,  # Cần thiết cho cosine similarity
            show_progress_bar=show_progress
        )
        
        return np.array(embeddings, dtype=np.float32)
    
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
            context = chunk.get("context", "")
            # Ghép context vào đầu content nếu có
            text = f"{context}\n{content}" if context else content
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
