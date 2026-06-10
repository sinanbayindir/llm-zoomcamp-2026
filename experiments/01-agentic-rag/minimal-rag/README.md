# LLM Zoomcamp 2026 — Module 1 Homework
## Agentic RAG

Repository: [llm-zoomcamp-2026](https://github.com/sinanbayindir/llm-zoomcamp-2026?utm_source=chatgpt.com)

This homework implements a complete Agentic RAG workflow for Module 1 of the LLM Zoomcamp course by [DataTalksClub](https://github.com/DataTalksClub/llm-zoomcamp?utm_source=chatgpt.com).

The implementation includes:

- Document ingestion from GitHub
- Search indexing with `minsearch`
- Prompt-based RAG pipeline
- Chunked retrieval
- Agentic function-calling loop using OpenAI Responses API

---

# Homework Answers

| Question | Answer |
|---|---|
| Q1 | 72 |
| Q2 | `01-agentic-rag/lessons/14-agentic-loop.md` |
| Q3 | 7000 |
| Q4 | 295 |
| Q5 | 3× fewer |
| Q6 | 4 |

---

# Project Structure

```text
experiments/
└── 01-agentic-rag/
    └── minimal-rag/
        ├── .env
        ├── pyproject.toml
        ├── rag.py
        ├── rag_pipeline.py
        ├── fetch_dataset.py
        ├── search_demo.py
        ├── prompt_demo.py
        ├── inspect_new_dataset.py
        ├── homework.py
        └── agent_homework.py
```

---

# Technologies Used

- Python 3.12
- uv
- OpenAI API
- minsearch
- gitsource
- dotenv

---

# Setup

## Clone repository

```bash
git clone https://github.com/sinanbayindir/llm-zoomcamp-2026.git

cd llm-zoomcamp-2026
```

## Create environment

```bash
cd experiments/01-agentic-rag/minimal-rag

uv sync
```

## Configure environment variables

Create `.env`:

```env
OPENAI_API_KEY=your_api_key
```

---

# Running the Homework

## Q1–Q5

```bash
uv run python homework.py
```

## Q6

```bash
uv run python agent_homework.py
```

---

# What Was Implemented

## Minimal RAG Pipeline

The implementation includes a full Retrieval-Augmented Generation pipeline:

```text
Question
    ↓
Search
    ↓
Retrieved Context
    ↓
Prompt Construction
    ↓
LLM Generation
```

The pipeline uses lesson pages from the LLM Zoomcamp repository as the knowledge base.

---

# Chunking

The lesson pages were chunked using:

```python
chunk_documents(documents, size=2000, step=1000)
```

This significantly reduced prompt size and improved retrieval precision.

---

# Agentic Loop

The agent implementation uses:

- OpenAI Responses API
- Function calling
- Manual agent loop
- Dynamic retrieval iterations

The agent repeatedly decides whether to:

- search again,
- refine the query,
- or answer directly.

The loop terminates when no additional tool calls are returned by the model.

---

# Notes

This repository is structured as a long-term professional learning workspace for the LLM Zoomcamp program.

The goal is not only to complete homework assignments, but also to deeply understand:
- RAG systems
- retrieval pipelines
- chunking strategies
- agent architectures
- function calling
- production-oriented LLM engineering patterns
