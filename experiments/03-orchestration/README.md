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
|----------|--------|
| Q1 | AI Copilot has access to current Kestra plugin documentation |
| Q2 | Vague, generic, or fabricated — the model guesses from training data |
| Q3 | 500+ tokens |
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

## Q3 — Token Usage (Short Summary)

`4_simple_agent_openai.yaml` was executed with:

```text
summary_length = short
```

Observed token usage:

```text
Multilingual Agent:
- Input tokens: 279
- Output tokens: 532
- Total tokens: 811

English Brevity Agent:
- Input tokens: 157
- Output tokens: 532
- Total tokens: 689
```

Selected answer:

```text
500+ tokens
```

---

## Q4 — Token Usage (Long Summary)

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
Short summary output tokens: 532
Long summary output tokens: 411

Although the long summary produced fewer output tokens in this execution, the homework answer is selected from the closest available option provided in the course.
```

Selected answer:

```text
About the same — within 20%
```

---

## Q5 — Modified Flow Prompt

The `english_brevity` task prompt was changed from:

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
Original (1 sentence): 441 output tokens
Modified (3 sentences): 539 output tokens

Increase ≈ 22%
```

Selected answer:

```text
About the same — within 20%
```

---

# Key Takeaways

- Generic LLMs often produce vague or incorrect workflow definitions when they lack sufficient context.
- Kestra AI Copilot performs better because it has access to current Kestra plugin documentation.
- RAG improves response quality by grounding answers in retrieved information.
- Monitoring token usage is important for understanding both cost and prompt efficiency.
- For deterministic, repeatable, and compliance-sensitive production systems, traditional task-based workflows are preferable to autonomous agents.

---

# Final Results

```text
Q1: AI Copilot has access to current Kestra plugin documentation
Q2: Vague, generic, or fabricated — the model guesses from training data
Q3: 500+ tokens
Q4: About the same — within 20%
Q5: About the same — within 20%
Q6: Use traditional task-based workflows for predictability and auditability
```
