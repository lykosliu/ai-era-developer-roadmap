---
name: ReMe
description: Memory management toolkit for AI agents with file-based and vector-based memory systems.
---

# Overview

ReMe (Remember Me, Refine Me) is an open-source memory management toolkit for AI agents, maintained by AgentScope-AI.  
Its core goal is to make agents stateful across long conversations and multiple sessions, instead of relying only on a single prompt context window.

ReMe provides two complementary memory systems:

- ReMeLight (file-based memory): uses readable local files for context compaction, long-term memory writing, and memory retrieval.
- ReMe (vector-based memory): uses vector stores for structured personal/procedural/tool memory extraction and retrieval.

In practice, ReMe is designed to solve two recurring production problems:

- Context overflow in long interactions.
- Session statelessness where agents cannot inherit useful history.

# Why It Matters

- Continuity across sessions: agents can remember user preferences, prior decisions, and task history.
- Better context quality: old dialogs are compacted into structured summaries, reducing prompt noise.
- Lower token cost: long tool outputs and stale conversation chunks are compressed or externalized.
- Stronger adaptation loop: memory can be updated over time based on outcomes and behavior.
- Flexible deployment: teams can start with file-based memory and evolve to vector-based memory when scale increases.

# Key Principles

## 1. Dual-System Memory Design

ReMe separates memory into two implementation styles rather than enforcing a single storage path:

- File-based (ReMeLight): memory as Markdown/JSONL files under a working directory.
- Vector-based (ReMe): memory as semantic entries in vector stores (local or external backends).

This split allows different trade-offs:

- ReMeLight favors transparency and developer control.
- ReMe favors semantic retrieval and structured memory operations at scale.

## 2. ReMeLight: File-Based Memory as a First-Class Runtime Layer

ReMeLight organizes runtime memory in explicit files:

- `MEMORY.md`: long-term memory anchor.
- `memory/YYYY-MM-DD.md`: daily summarized memory.
- `dialog/YYYY-MM-DD.jsonl`: raw conversation persistence.
- `tool_result/*.txt`: cached long tool outputs with retention cleanup.

Core workflow before each reasoning step:

1. Compact long tool results (`compact_tool_result`).
2. Check token pressure and split old/new messages (`check_context`).
3. Generate structured summary for compacted history (`compact_memory`).
4. Persist high-value memory asynchronously (`summary_memory`).

This pipeline is integrated through `pre_reasoning_hook`, which acts as the orchestration entry point.

## 3. Structured Compaction Instead of Naive Truncation

ReMeLight does not only cut old tokens. It compacts history into a structured checkpoint with fields such as:

- Goal
- Constraints
- Progress
- Key Decisions
- Next Steps
- Critical Context

This improves downstream reasoning quality because agents recover decision state, constraints, and unresolved work, not just short generic summaries.

## 4. Hybrid Retrieval Strategy for Recall Quality

For memory retrieval, ReMeLight exposes `memory_search` with hybrid fusion:

- Vector similarity retrieval.
- BM25 keyword retrieval.
- Weighted merge and filtering.

The intent is to balance semantic matching (concept-level recall) and exact matching (identifier/path/error-string recall), which is important in coding and operations workflows.

## 5. Vector-Based ReMe for Persistent Experience Learning

The vector-based system models three memory categories:

- Personal memory: user preferences and stable profile-like facts.
- Procedural memory: task-level patterns and what worked/failed.
- Tool memory: tool usage strategies and parameter experience.

It supports full CRUD and lifecycle operations:

- `summarize_memory`
- `retrieve_memory`
- `add_memory`
- `get_memory`
- `update_memory`
- `delete_memory`
- `list_memory`

This API shape makes it suitable for multi-session applications that require long-term memory governance, not only passive logging.

## 6. Engineering Implications and Trade-Offs

Practical strengths:

- Observable memory state (especially in file mode).
- Clear hook points for integration into existing agent loops.
- Supports both lightweight local usage and scalable vector backends.
- Includes benchmark-driven positioning in the project documentation.

Potential constraints to evaluate in real deployments:

- Memory quality depends on summarizer and embedding model quality.
- Asynchronous persistence introduces consistency timing considerations.
- Governance design is still needed at application level (privacy, retention, namespace isolation, memory correction).

# AI Context

## Where ReMe Fits

ReMe fits the memory layer of agent architectures, between dialogue/runtime state and retrieval infrastructure.

Typical integration stack:

- LLM + planner/reasoner
- Tool executor
- ReMe pre-reasoning memory pipeline
- Long-term memory store (files and/or vector DB)

## Recommended Adoption Path

1. Start with ReMeLight in local development to validate compaction and recall behavior.
2. Define memory write policies (what is worth persisting).
3. Add retrieval quality checks (precision, freshness, usefulness).
4. Introduce vector-based ReMe when memory volume or multi-user scope grows.
5. Add governance controls (retention, deletion workflows, tenant isolation, sensitive data handling).

## Suitable Use Cases

- Personal coding assistants with persistent style and project context.
- Customer-support agents that need cross-session user continuity.
- Task automation agents that learn from historical execution outcomes.
- Multi-turn workflows with heavy tool outputs and context-window pressure.

# References

- ReMe GitHub repository: https://github.com/agentscope-ai/ReMe
- ReMe documentation site (project citation URL): https://reme.agentscope.io
- AgentScope-AI organization: https://github.com/agentscope-ai
