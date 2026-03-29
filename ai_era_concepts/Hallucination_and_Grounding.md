---
name: Hallucination and Grounding
description: Managing reliability and factual accuracy.
---

# Hallucination and Grounding

## Overview
**Hallucination** is when an LLM generates confident but incorrect or nonsensical information. **Grounding** is the practice of anchoring model outputs to verifiable facts or data.

## Why it matters in the AI Era
Reliability is the biggest hurdle for production AI. Developers must use techniques like RAG and prompt constraints to minimize hallucinations in critical applications.

---

## Key Principles
1. **Probabilistic Nature:** LLMs predict the "next most likely token," which doesn't always guarantee truth.
2. **Grounding Sources:** Providing a "source of truth" (like a document) for the model to reference.
3. **Verification:** Using external tools or multi-step reasoning to check the model's work.

---

## AI Context
Building "trust" in AI systems requires moving away from pure generation toward grounded reasoning.
