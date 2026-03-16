"""
Re-embed documents with new chunking and metadata
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

print("=" * 70)
print("RE-EMBEDDING DOCUMENTS WITH NEW METADATA")
print("=" * 70)

# Load new chunks with updated metadata
print("\n[1/4] Loading new chunks...")
try:
    with open("Notebook/rag_chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"✓ Loaded {len(chunks)} chunks")
    
    # Verify metadata structure
    if chunks:
        sample = chunks[0]['metadata']
        print(f"✓ Metadata keys: {list(sample.keys())}")
        print(f"  Sample: grade={sample.get('grade')}, lesson={sample.get('lesson')}, idea={sample.get('idea')}")
except Exception as e:
    print(f"✗ Error loading chunks: {e}")
    exit(1)

# Load embedding model
print("\n[2/4] Loading embedding model...")
try:
    model = SentenceTransformer(
        "dangvantuan/vietnamese-document-embedding",
        device="cpu",
        trust_remote_code=True
    )
    print("✓ Model loaded: dangvantuan/vietnamese-document-embedding")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    exit(1)

# Extract texts and embed
print("\n[3/4] Embedding documents...")
try:
    texts = [chunk.get("content", "") for chunk in chunks]
    
    print(f"  Encoding {len(texts)} documents...")
    embeddings = model.encode(
        texts,
        batch_size=64,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    
    embeddings = np.array(embeddings, dtype=np.float32)
    print(f"✓ Embeddings shape: {embeddings.shape}")
    print(f"✓ Dtype: {embeddings.dtype}")
except Exception as e:
    print(f"✗ Error embedding: {e}")
    exit(1)

# Save embeddings
print("\n[4/4] Saving embeddings...")
try:
    output_path = Path("data/embeddings.npy")
    output_path.parent.mkdir(exist_ok=True)
    
    np.save(output_path, embeddings)
    print(f"✓ Saved embeddings to {output_path}")
    
    # Verify
    loaded = np.load(output_path)
    print(f"✓ Verified: {loaded.shape}")
    
except Exception as e:
    print(f"✗ Error saving: {e}")
    exit(1)

# Copy chunks to data/
print("\n[5/5] Copying chunks to data directory...")
try:
    import shutil
    shutil.copy("Notebook/rag_chunks.json", "data/rag_chunks.json")
    print("✓ Copied rag_chunks.json to data/")
except Exception as e:
    print(f"✗ Error copying: {e}")
    exit(1)

print("\n" + "=" * 70)
print("✅ RE-EMBEDDING COMPLETED SUCCESSFULLY!")
print("=" * 70)
print(f"\nSummary:")
print(f"  • Chunks: {len(chunks)} (with new metadata)")
print(f"  • Embeddings: {embeddings.shape} (768-dimensional)")
print(f"  • Model: dangvantuan/vietnamese-document-embedding")
print(f"  • Files:")
print(f"    - data/embeddings.npy")
print(f"    - data/rag_chunks.json")
print("\n✓ Ready to run pipeline with updated data!")
print("=" * 70)
