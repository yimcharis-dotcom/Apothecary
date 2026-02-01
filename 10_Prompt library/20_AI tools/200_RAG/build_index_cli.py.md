``` python

from pathlib import Path
import argparse
import json
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def chunk_text(text: str, size: int, overlap: int):
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = start + size
        chunks.append(text[start:end])
        start = max(0, end - overlap)
        if start == 0 and end >= n:
            break
    return chunks

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--vault", required=True, help="Folder to index")
    p.add_argument("--out", required=True, help="Output prefix")
    p.add_argument("--model", default="BAAI/bge-m3")
    p.add_argument("--chunk_size", type=int, default=800)
    p.add_argument("--overlap", type=int, default=100)
    args = p.parse_args()

    vault_path = Path(args.vault)
    index_path = Path(f"{args.out}.index")
    meta_path = Path(f"{args.out}_meta.json")

    model = SentenceTransformer(args.model)

    md_files = list(vault_path.rglob("*.md"))

    texts = []
    metadata = []

    for path in tqdm(md_files, desc="Reading files"):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for i, chunk in enumerate(chunk_text(content, args.chunk_size, args.overlap)):
            texts.append(chunk)
            metadata.append({"path": str(path), "chunk_id": i, "text": chunk})

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, str(index_path))
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Done.")
    print(f"Vault: {vault_path}")
    print(f"Chunks: {len(texts)}")
    print(f"Index: {index_path}")
    print(f"Meta:  {meta_path}")

if __name__ == "__main__":
    main()

```