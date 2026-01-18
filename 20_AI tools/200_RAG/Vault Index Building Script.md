---
Tags:
  - scripts
  - FAISS
  - ai
Created: 2023-10-01
Updated: 2023-10-01
---

This note documents a Python script for building a FAISS index from an Obsidian vault. The script embeds content from all `.md` files in the vault located at `C:\Vault\Apothecary` and saves the index and metadata for use in similarity searches or AI applications.

## Purpose

The script processes markdown files in the vault, generates embeddings using a sentence transformer model, and creates a FAISS index for efficient similarity search. This enables advanced querying or AI-driven analysis of vault content.

## Setting Up the Environment

To run the script, you need an isolated Python environment to manage dependencies. Follow these steps:

1. **Create a Virtual Environment**:

   - Open a terminal or PowerShell in your working directory (e.g., `C:\Users\YC\OneDrive\Desktop\LocalDocs\`).
   - Run the following command to create a virtual environment named `.venv`:

     ```bash
     python -m venv .venv
     ```

2. **Activate the Virtual Environment**:

   - Activate the environment so that `python` and `pip` commands use the isolated setup:

     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```

   - Your terminal prompt should now show `(.venv)` to indicate the environment is active.

3. **Run the Script**:
   - Ensure the script file is in your working directory.

- **Hard-Coded Script (`build_index.py`)**:  
   Uses fixed inputs and outputs, always indexing the vault at `C:\Vault\Apothecary` and saving to `vault.index` and `vault_meta.json`. - Execute it with:

  ```bash
  python build_index.py
  ```

- **Parameterized Script (`build_index_cli.py`)**:  
   Allows customization at runtime. Specify the vault path and output names using command-line arguments like `--vault` and `--out`.

  ```
  python build_index_cli.py --<<vault "C:\Vault\ObsidianTemplateVaultV2-main">> --out <<templates>>
  ```

## Script Details: [[build_index.py]]

Below is the full script for building the FAISS index with hard-coded paths and settings.

```python
from pathlib import Path
import json
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# -------- Configuration --------
VAULT_PATH = Path(r"C:\Vault\Apothecary")  # Path to the Obsidian vault
INDEX_PATH = Path("vault.index")               # Output path for FAISS index
META_PATH = Path("vault_meta.json")            # Output path for metadata
MODEL_NAME = "BAAI/bge-m3"                     # Embedding model to use
CHUNK_SIZE = 800                               # Size of text chunks for embedding
CHUNK_OVERLAP = 100                            # Overlap between chunks to preserve context
# --------------------------------

def chunk_text(text, size, overlap):
    """Split text into chunks of specified size with overlap."""
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
    """Build a FAISS index from markdown files in the vault."""
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

## **Parameterized Script**: [[build_index_cli.py]]

```

From pathlib import Path
Import argparse
Import json
Import faiss
From sentence_transformers import SentenceTransformer
From tqdm import tqdm

Def chunk_text (text: str, size: int, overlap: int):
    Chunks = []
    Start = 0
    N = len (text)
    While start < n:
        End = start + size
        Chunks.Append (text[start: end])
        Start = max (0, end - overlap)
        If start == 0 and end >= n:
            Break
    Return chunks

Def main ():
    P = argparse.ArgumentParser ()
    p.add_argument ("--vault", required=True, help="Folder to index")
    p.add_argument ("--out", required=True, help="Output prefix")
    p.add_argument ("--model", default="BAAI/bge-m 3")
    p.add_argument ("--chunk_size", type=int, default=800)
    p.add_argument ("--overlap", type=int, default=100)
    args = p.parse_args ()

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

If __name__ == "__main__":
    Main ()


```

## Long-Running Indexing

For large vaults where indexing takes significant time, use this PowerShell script to prevent your laptop from sleeping during the process:

```powershell
try {
    powercfg /change standby-timeout-ac 0
    powercfg /change monitor-timeout-ac 0
    python build_index_cli.py --vault "C:\Vault\automators-main" --out automators-mainTemplate
}
finally {
    powercfg /change standby-timeout-ac 15
    powercfg /change monitor-timeout-ac 10
}
```

## Key Notes

- **Virtual Environment**: Activation determines which Python interpreter runs; the working directory determines file locations.
- **Vault Path**: Ensure `VAULT_PATH` in the script points to `C:\Vault\Apothecary` for the hard-coded version.
- **Next Steps**: Place the script in the working directory, navigate to it with `cd`, run it, and report the directory and result (e.g., started embedding or any errors).

## Related Notes

- [FAISS Overview](app://obsidian.md/FAISS%20Overview) (placeholder for a note explaining FAISS and its use in similarity search)
- [Vault Automation Scripts](app://obsidian.md/Vault%20Automation%20Scripts) (placeholder for a hub of related automation scripts)
