---
Description: ref for build_index.py
Tags:
  - RAG
  - Configuration
  - Embeddings
  - ai/tools
Related: "[[build_index.py]]"
index_date: 2025-12-25
---

# RAG Configuration for Semantic Search

## Configuration Parameters
- **Vault Path**: `C:\Vault\Apothecary`
- **Index Path**: `vault.index`
- **Meta Path**: `vault_meta.json`
- **Model Name**: `BAAI/bge-m3`
- **Chunk Size**: `800` characters
- **Chunk Overlap**: `100` characters

## Model Information
- **Description**: BGE-M3 provides good multilingual support and retrieval performance.
- **Alternatives**: 
  - `all-MiniLM-L6-v2` (faster)
  - `all-mpnet-base-v2` (balanced)
  - `BAAI/bge-large-en-v1.5` (best quality)

## Chunking Information
- **Chunk Size**: 800 characters ≈ 150-200 words. Larger chunks provide more context but fewer results; smaller chunks offer better precision but more results.
- **Chunk Overlap**: 100 characters ≈ 20-25 words overlap between chunks. Prevents losing context at boundaries. Typically 10-20% of chunk size.

## Performance Metrics
- **Model Download Size**: ~2 GB initial download
- **Indexing Speed**: ~100-500 files/minute (depends on hardware)
- **Search Speed**: ~10-50 ms per query
- **Memory Usage**: ~2-4 GB for large vaults

## Current Limitations
- Rebuilds entire index (no incremental updates)
- Only indexes `.md` files
- No filtering of system/template files
- Fixed chunking (no sentence boundary awareness)

## Planned Improvements
- Incremental indexing for changed files
- Smart chunking with sentence boundaries
- File type filtering and exclusion patterns
- Index compression and optimization
- Parallel processing for faster indexing