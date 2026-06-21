# LLM Zoomcamp 2026 — Module 2 Homework
## Vector Search

This homework implements the concepts covered in Module 2 of the LLM Zoomcamp course.

The goal of this module is to understand semantic search using embeddings and compare it with traditional keyword search.

The implementation includes:

- ONNX-based embeddings
- Cosine similarity search
- Manual vector search with NumPy
- Vector search using minsearch
- Keyword search using minsearch
- Hybrid search with Reciprocal Rank Fusion (RRF)

---

# Homework Answers

| Question | Answer |
|-----------|-----------|
| Q1 | -0.02 |
| Q2 | 0.37 |
| Q3 | `02-vector-search/lessons/07-sqlitesearch-vector.md` |
| Q4 | `04-evaluation/lessons/05-search-metrics.md` |
| Q5 | `02-vector-search/lessons/08-pgvector.md` |
| Q6 | `01-agentic-rag/lessons/13-function-calling.md` |

---

# Technologies Used

- Python 3.12
- uv
- ONNX Runtime
- NumPy
- minsearch
- gitsource
- tokenizers

---

# Project Structure

```text
minimal-vector-search/
├── download.py
├── embedder.py
├── homework.py
├── README.md
├── pyproject.toml
└── uv.lock
```

---

# Setup

Create and synchronize the environment:

```bash
uv sync
```

Download the ONNX embedding model:

```bash
uv run python download.py
```

---

# Running the Homework

Execute:

```bash
uv run python homework.py
```

The script automatically:

1. Downloads and loads lesson pages from the course repository
2. Generates embeddings with the ONNX embedder
3. Calculates cosine similarity
4. Performs manual vector search
5. Runs vector search with minsearch
6. Compares text search and vector search
7. Executes hybrid search using Reciprocal Rank Fusion

---

# What Was Implemented

## Q1 — Embedding a Query

Generated a 384-dimensional embedding vector for:

> How does approximate nearest neighbor search work?

Result:

```text
v[0] = -0.02058
```

Selected answer:

```text
-0.02
```

---

## Q2 — Cosine Similarity

Computed the cosine similarity between:

- the query embedding from Q1
- the lesson page:

```text
02-vector-search/lessons/07-sqlitesearch-vector.md
```

Result:

```text
0.36107
```

Selected answer:

```text
0.37
```

---

## Q3 — Manual Vector Search

Chunked all lesson pages using:

```python
chunk_documents(documents, size=2000, step=1000)
```

Embedded every chunk and performed vector search manually with NumPy:

```python
scores = X.dot(v)
```

Highest-scoring chunk:

```text
02-vector-search/lessons/07-sqlitesearch-vector.md
```

---

## Q4 — Vector Search with minsearch

Built a VectorSearch index and queried:

> What metric do we use to evaluate a search engine?

Top result:

```text
04-evaluation/lessons/05-search-metrics.md
```

---

## Q5 — Text Search vs Vector Search

Compared:

- VectorSearch
- Index (keyword search)

Query:

> How do I store vectors in PostgreSQL?

File appearing only in vector search results:

```text
02-vector-search/lessons/08-pgvector.md
```

---

## Q6 — Hybrid Search

Combined vector search and keyword search using Reciprocal Rank Fusion:

```python
results = rrf([vector_results, text_results])
```

Query:

> How do I give the model access to tools?

Top hybrid result:

```text
01-agentic-rag/lessons/13-function-calling.md
```

---

# Key Learnings

This module demonstrated the differences between:

- Keyword Search
- Vector Search
- Hybrid Search

Key takeaways:

- Vector search captures semantic meaning.
- Keyword search performs better for exact terms.
- Hybrid search often provides the most balanced retrieval quality.
- Chunking significantly improves retrieval precision.
- ONNX embeddings offer a lightweight alternative to PyTorch-based sentence-transformers.

---

# Final Results

```text
Q1: -0.02
Q2: 0.37
Q3: 02-vector-search/lessons/07-sqlitesearch-vector.md
Q4: 04-evaluation/lessons/05-search-metrics.md
Q5: 02-vector-search/lessons/08-pgvector.md
Q6: 01-agentic-rag/lessons/13-function-calling.md
```
