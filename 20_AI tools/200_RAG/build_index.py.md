---
Description: FAISS vector index builder for Obsidian vault semantic search
Tags:
  - RAG
  - Indexing
  - Embeddings
  - FAISS
  - Sentence-transformers
  - ai/tools
Vault_path: C:\Vault\Apothecary
Index_path: vault. Index
Meta_path: vault_meta. Json
Model_name: BAAI/bge-m 3
Chunk_size: 800
Chunk_overlap: 100
File_type: .md
index_date: 2025-12-25
Related: "[[build_index.py - ref]]"
---

```python

from pathlib import Path
import json
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# -------- configuration --------
VAULT_PATH = Path(r"C:\Vault\Apothecary")
INDEX_PATH = Path("vault.index")
META_PATH = Path("vault_meta.json")
MODEL_NAME = "BAAI/bge-m3"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
# --------------------------------

def chunk_text(text, size, overlap):
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
    return chunks

def main():
    model = SentenceTransformer(MODEL_NAME)

    texts = []
    metadata = []

    md_files = list(VAULT_PATH.rglob("*.md"))

    for path in tqdm(md_files, desc="Reading files"):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        chunks = chunk_text(content, CHUNK_SIZE, CHUNK_OVERLAP)

        for i, chunk in enumerate(chunks):
            texts.append(chunk)
            metadata.append({
                "path": str(path),
                "chunk_id": i,
                "text": chunk
            })

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    with META_PATH.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print("Done.")
    print(f"Chunks: {len(texts)}")
    print(f"Index saved to: {INDEX_PATH}")
    print(f"Metadata saved to: {META_PATH}")

if __name__ == "__main__":
    main()
```
