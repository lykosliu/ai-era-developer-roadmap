---
name: rag
description: Retrieval-Augmented Generation pattern.
---

# RAG (Retrieval-Augmented Generation): Connecting LLMs to Data

## Overview
Retrieval-Augmented Generation (RAG) is a pattern that combines the reasoning capabilities of a Large Language Model with the information retrieval of a vector database or search engine.

## Why it matters in the AI Era
Standard LLMs are limited to the knowledge they were trained on. RAG allows them to access up-to-date information, internal documentation, and personal data without needing to fine-tune the model.

---

## Key Principles

1. **Retrieval:** Search for relevant context (using vector search or keyword search).
2. **Augmentation:** Combine the retrieved context with the user's query into a prompt.
3. **Generation:** Use the LLM to generate a response based on the augmented prompt.

---

## AI Context: From "Static Knowledge" to "Dynamic Retrieval"
RAG is the primary way that companies are building production-ready AI applications. It's used for:
- **Internal Knowledge Bases:** Searching through millions of documents to answer employee questions.
- **Customer Support Chatbots:** Providing accurate answers based on product documentation.
- **Personalized AI Assistants:** Remembering user preferences and past interactions.

---

## Getting Started
Check out our [demos/](./demos/) directory to see a simple RAG implementation.

## Further Reading
- [OpenAI Guide to RAG](https://platform.openai.com/docs/guides/rag)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
