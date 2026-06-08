# Lesson 01 — Introduction to Agentic RAG

## Key Idea

Large Language Models are powerful text generation systems, but they are not reliable knowledge systems.

LLMs have three major limitations:

1. Knowledge cutoff
2. No access to private/internal data
3. Hallucinations

Retrieval-Augmented Generation (RAG) solves this by injecting external context into the prompt before generation.

---

## Basic RAG Architecture

```text
User Question
    ↓
Retriever / Search
    ↓
Relevant Documents
    ↓
Prompt Construction
    ↓
LLM
    ↓
Grounded Answer
```

The model no longer relies only on memorized knowledge.

Instead:

- retrieve relevant information first
- augment the prompt
- generate grounded output

---

## Why This Matters

RAG is still one of the most common production patterns for LLM systems because:

- cheaper than fine-tuning
- easier to update
- works with private/company data
- reduces hallucinations
- easier to maintain

---

## Important Engineering Insight

The course intentionally avoids frameworks at the beginning.

This is important because frameworks like:

- LangChain
- LlamaIndex
- Haystack
- DSPy

are abstractions on top of the same underlying pipeline.

Understanding the raw pipeline first is critical for production engineering.

---

## Agentic RAG

Traditional RAG:

```text
Search → Prompt → LLM
```

Agentic RAG:

```text
LLM decides:
- when to search
- what to search
- whether another search is needed
```

This introduces:

- tool usage
- function calling
- iterative reasoning loops
- agents
