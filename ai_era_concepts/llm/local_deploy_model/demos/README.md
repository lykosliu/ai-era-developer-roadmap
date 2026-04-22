---
name: Demos
description: Hands-on examples and runnable code.
---

# Sentence Transformers Demos

This directory contains a runnable demo focused on the core collection-level embedding capabilities with Sentence Transformers.

## Demos Included

1. `demo_sentence_transformers_embedding_collection.py`
   - Build an embedding collection from a document list.
   - Given one query, return Top-K most similar documents.

## How to Run

1. Setup environment and install dependencies:

```bash
bash setup.sh
```

2. Activate virtual environment:

```bash
source .venv/bin/activate
```

3. Run the demo:

```bash
python demo_sentence_transformers_embedding_collection.py
```

4. Run with a custom embedding model:

```bash
python demo_sentence_transformers_embedding_collection.py --model sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

5. Run with custom query and Top-K:

```bash
python demo_sentence_transformers_embedding_collection.py --query "How to improve RAG retrieval?" --top-k 2
```

## Model Cache Directory

- Default cache path on macOS/Linux: `~/.cache/huggingface/hub`
- For this machine, it is typically: `/Users/lykos/.cache/huggingface/hub`
- You can change cache path before running the demo:

```bash
export HF_HOME=/data/hf_cache
# or
export HF_HUB_CACHE=/data/hf_cache/hub
```

## Model Lists

- Sentence Transformers pretrained models: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
- Hugging Face Sentence Transformers collection: https://huggingface.co/models?library=sentence-transformers
- ModelScope sentence-transformers keyword search: https://www.modelscope.cn/models?name=sentence-transformers
- ModelScope text-embedding task search: https://www.modelscope.cn/models?name=text-embedding

## Prerequisites

- Python 3.9+
- `pip`
- Internet access for first-time model download
