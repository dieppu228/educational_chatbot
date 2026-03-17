"""
Embedding module cho RAG pipeline.

Chức năng:
    - Encode văn bản tiếng Việt thành vector 768 chiều
    - Hỗ trợ embed chunks từ file JSON (context + content)
    - Lưu/load embeddings dạng numpy (.npy)

Model: dangvantuan/vietnamese-document-embedding (SentenceTransformer)
Không dùng FAISS — vector search sẽ dùng numpy cosine similarity.

Author: KhacDiep
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Optional
from sentence_transformers import SentenceTransformer


# ============================================================
# EMBEDDING MODEL
# ============================================================

class EmbeddingModel:
    """
    Wrapper cho SentenceTransformer embedding model.
    
    Tại sao cần wrapper:
        - Tập trung cấu hình model 1 chỗ (model_name, device, batch_size)
        - Chuẩn hóa normalize embeddings cho cosine similarity
        - Hàm tiện ích: embed_chunks, embed_query
    """
    
    def __init__(
        self, 
        model_name: str = "dangvantuan/vietnamese-document-embedding",
        device: str = "cpu",
        batch_size: int = 64
    ):
        """
        Khởi tạo embedding model.
        
        Args:
            model_name: Tên model trên HuggingFace
            device: "cpu" hoặc "cuda"
            batch_size: Số text encode cùng lúc (giảm nếu thiếu RAM)
        """
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        self.model = None  # Lazy load
    
    def _load_model(self):
        """Load model lần đầu khi cần (lazy loading để tiết kiệm RAM)."""
        if self.model is None:
            print(f"🔄 Loading embedding model: {self.model_name}...")
            self.model = SentenceTransformer(
                self.model_name, 
                trust_remote_code=True, 
                device=self.device
            )
            print(f"✅ Model loaded on {self.device}")
    
    def encode(self, texts: List[str], show_progress: bool = True) -> np.ndarray:
        """
        Encode danh sách text thành embeddings.
        
        Args:
            texts: Danh sách văn bản cần encode
            show_progress: Hiện progress bar
            
        Returns:
            np.ndarray: shape (n_texts, 768), dtype float32, L2-normalized
        """
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
        """
        Encode 1 câu query (không hiện progress bar).
        
        Returns:
            np.ndarray: shape (768,)
        """
        return self.encode([query], show_progress=False)[0]


# ============================================================
# EMBED CHUNKS PIPELINE
# ============================================================

def load_chunks(chunks_path: str) -> list:
    """Load chunks từ file JSON."""
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    print(f"📦 Loaded {len(chunks)} chunks từ {chunks_path}")
    return chunks


def prepare_texts(chunks: list, use_context: bool = True) -> List[str]:
    """
    Chuẩn bị text để embed từ chunks.
    
    Tại sao embed context + content:
        Khi user hỏi "Bài 3 lớp 10 nói về gì?", context chứa thông tin
        "Bài 3: MỘT SỐ KIỂU DỮ LIỆU" giúp match tốt hơn so với chỉ
        embed nội dung bên trong.
    
    Args:
        chunks: List dict từ JSON
        use_context: Nếu True, ghép context + content
        
    Returns:
        List[str]: Danh sách text đã chuẩn bị
    """
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
    """
    Pipeline đầy đủ: Load chunks → Embed → Save.
    
    Args:
        chunks_path: Đường dẫn file JSON chunks
        embeddings_path: Đường dẫn lưu file .npy
        model_name: Tên model embedding
        device: "cpu" hoặc "cuda"
        batch_size: Batch size khi encode
        use_context: Ghép context vào text trước khi embed
    """
    print("=" * 60)
    print("🚀 EMBEDDING CHUNKS PIPELINE")
    print("=" * 60)
    
    # 1. Load chunks
    chunks = load_chunks(chunks_path)
    
    # 2. Chuẩn bị texts
    texts = prepare_texts(chunks, use_context=use_context)
    print(f"📝 Prepared {len(texts)} texts (use_context={use_context})")
    
    # 3. Embed
    model = EmbeddingModel(model_name=model_name, device=device, batch_size=batch_size)
    embeddings = model.encode(texts)
    print(f"📐 Embeddings shape: {embeddings.shape}")
    
    # 4. Save
    output_path = Path(embeddings_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, embeddings)
    
    # 5. Verify
    loaded = np.load(output_path)
    assert loaded.shape == embeddings.shape, "Verification failed!"
    
    print(f"\n✅ Đã lưu embeddings → {embeddings_path}")
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
