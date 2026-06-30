# LLM Zoomcamp 2026 — Module 3 Homework
## AI Orchestration with Kestra

This homework covers AI workflow orchestration using Kestra.

The module focuses on:

- Context engineering
- AI Copilot
- RAG-grounded workflows
- AI agents
- Token usage monitoring
- Production workflow best practices

---

# Homework Answers

| Question | Answer |
|---|---|
| Q1 | AI Copilot has access to current Kestra plugin documentation |
| Q2 | Vague, generic, or fabricated — the model guesses from training data |
| Q3 | 200–400 tokens |
| Q4 | About the same — within 20% |
| Q5 | About the same — within 20% |
| Q6 | Use traditional task-based workflows for predictability and auditability |

---

# Flows Used

The original Gemini-based flows were adapted to use OpenAI.

Main flows used:

```text
1_chat_without_rag_openai.yaml
2_chat_with_rag_openai.yaml
4_simple_agent_openai.yaml
```

---

# Observed Results

## Q2 — RAG vs No RAG

The non-RAG response was vague and did not provide grounded, specific information.

Observed log:

```text
❌ Response WITHOUT RAG (no retrieved context):
Do you mean Kestra (the open-source workflow orchestration platform at kestra.io) version 1.1? I can either (A) summarize the official 1.1 release notes and list the major features, or (B) point you to the release notes and highlight the key items — which would you prefer?
```

Selected answer:

```text
Vague, generic, or fabricated — the model guesses from training data
```

---

## Q3 — Token Usage: Short Summary

`4_simple_agent_openai.yaml` was executed with:

```text
summary_length = short
```

Observed token usage:

```text
Multilingual Agent:
- Input tokens: 279
- Output tokens: 407
- Total tokens: 686

English Brevity Agent:
- Input tokens: 160
- Output tokens: 377
- Total tokens: 537
```

Selected answer:

```text
200–400 tokens
```

---

## Q4 — Token Usage: Long Summary

`4_simple_agent_openai.yaml` was executed with:

```text
summary_length = long
```

Observed token usage:

```text
Multilingual Agent:
- Input tokens: 279
- Output tokens: 411
- Total tokens: 690

English Brevity Agent:
- Input tokens: 164
- Output tokens: 441
- Total tokens: 605
```

Comparison:

```text
short output tokens: 407
long output tokens: 411
difference: ~1%
```

Selected answer:

```text
About the same — within 20%
```

---

## Q5 — Modified Flow Prompt

The `english_brevity` task was modified from:

```text
Generate exactly 1 sentence English summary of the following:
```

to:

```text
Generate exactly 3 sentences English summary of the following:
```

The flow was then executed with:

```text
summary_length = long
```

Observed token usage:

```text
Multilingual Agent:
- Input tokens: 279
- Output tokens: 444
- Total tokens: 723

English Brevity Agent:
- Input tokens: 197
- Output tokens: 539
- Total tokens: 736
```

Comparison:

```text
original 1-sentence output tokens: 441
modified 3-sentence output tokens: 539
ratio: 539 / 441 = 1.22x
```

Selected answer:

```text
About the same — within 20%
```

---

# Key Takeaways

- Generic LLMs often produce vague or incorrect workflow definitions without the right context.
- Kestra AI Copilot performs better because it has access to current Kestra plugin documentation.
- RAG improves answer quality by grounding responses in retrieved context.
- Token monitoring is important for understanding cost and prompt efficiency.
- For deterministic and compliance-heavy production workflows, traditional task-based workflows are preferable to autonomous agents.

---

# Final Results

```text
Q1: AI Copilot has access to current Kestra plugin documentation
Q2: Vague, generic, or fabricated — the model guesses from training data
Q3: 200–400 tokens
Q4: About the same — within 20%
Q5: About the same — within 20%
Q6: Use traditional task-based workflows for predictability and auditability
```
