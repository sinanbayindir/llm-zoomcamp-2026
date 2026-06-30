# LLM Zoomcamp 2026 — Module 4 Homework

## Evaluation

This homework evaluates keyword search, vector search, and hybrid search over the LLM Zoomcamp lesson pages.

The goal is to replace intuition with measurable retrieval quality using a fixed ground truth dataset.

---

# Homework Answers

| Question | Answer |
|---|---|
| Q1 | 1400 |
| Q2 | `01-agentic-rag/lessons/03-rag.md` |
| Q3 | `01-agentic-rag/lessons/01-intro.md` |
| Q4 | 0.76 |
| Q5 | 0.55 |
| Q6 | 1 |

---

# Implementation

The solution is implemented in:

```text
experiments/04-evaluation/minimal-evaluation/
```

Main files:

```text
homework.py                 Runs Q2–Q6 search evaluation
q1_generate_questions.py    Generates Q1 questions and measures token usage
ground-truth.csv            Provided ground truth dataset
download.py                 Downloads the ONNX embedding model
embedder.py                 Lightweight ONNX embedder
```

---

# Technologies Used

- Python 3.12
- uv
- OpenAI API
- Pydantic
- pandas
- NumPy
- minsearch
- gitsource
- ONNX Runtime

---

# Q1 — Ground Truth Generation Token Usage

Generated 5 questions for each of the first 3 lesson pages:

```text
01-agentic-rag/lessons/01-intro.md
01-agentic-rag/lessons/02-environment.md
01-agentic-rag/lessons/03-rag.md
```

Observed input tokens:

```text
1016
1282
1749
```

Average:

```text
1349
```

Selected answer:

```text
1400
```

---

# Q2 — First Result with Text Search

First ground truth question:

```text
What exactly is a retrieval-augmented generation system, and why does it help with answers that the model wouldn't know on its own?
```

First text search result:

```text
01-agentic-rag/lessons/03-rag.md
```

---

# Q3 — First Result with Vector Search

Using the same question, the first vector search result was:

```text
01-agentic-rag/lessons/01-intro.md
```

---

# Q4 — Evaluating Text Search

Text search metrics:

```text
Hit Rate: 0.7583333333333333
MRR: 0.5942592592592594
```

Selected answer:

```text
0.76
```

---

# Q5 — Evaluating Vector Search

Vector search metrics:

```text
Hit Rate: 0.725
MRR: 0.5486111111111112
```

Selected answer:

```text
0.55
```

---

# Q6 — Tuning Hybrid Search

Hybrid search was evaluated with RRF using:

```text
k = 1, 50, 100, 200
```

Results:

```text
k=1:
Hit Rate: 0.8388888888888889
MRR: 0.6481944444444449

k=50:
Hit Rate: 0.8361111111111111
MRR: 0.637916666666667

k=100:
Hit Rate: 0.8361111111111111
MRR: 0.637916666666667

k=200:
Hit Rate: 0.8361111111111111
MRR: 0.637916666666667
```

Best MRR:

```text
k = 1
```

---

# Final Results

```text
Q1: 1400
Q2: 01-agentic-rag/lessons/03-rag.md
Q3: 01-agentic-rag/lessons/01-intro.md
Q4: 0.76
Q5: 0.55
Q6: 1
```

---

# Key Takeaways

- Search quality should be measured, not guessed.
- A fixed ground truth dataset enables fair comparison between retrieval methods.
- Hit Rate measures whether the correct document appears in the result list.
- MRR rewards retrieving the correct document near the top.
- Vector search is not automatically better than keyword search.
- Hybrid search can outperform both keyword-only and vector-only approaches.
