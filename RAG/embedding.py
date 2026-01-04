from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from tqdm import tqdm
from underthesea import word_tokenize

def encode_and_save_embeddings(
    texts, 
    model_name="dangvantuan/vietnamese-document-embedding",
    embedding_path="data/embeddings.npy",
    batch_size=64,
    device="cpu"
):
    # Load model
    model = SentenceTransformer(model_name, trust_remote_code=True, device=device)
    
    # Encode với batch, normalize, show progress
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    
    embeddings = np.array(embeddings, dtype=np.float32)
    np.save(embedding_path, embeddings)
    print(f"✅ Saved embeddings to {embedding_path}")
    return embeddings
