---
name: Memory
description: Persistent memory patterns for AI agents and applications.
---

# Overview

Memory in AI applications is the capability to retain, retrieve, and use relevant past information across turns, sessions, and tasks.  
For modern AI agents, memory is not only conversation history. It is a state layer that helps systems adapt over time, personalize behavior, and make better decisions with less repeated context.

This topic is central to moving from stateless assistants to stateful, long-lived agent systems.

# Why It Matters

- Continuity: users should not repeat preferences and prior decisions in every session.
- Quality: agents can use prior outcomes (successes/failures) to improve future actions.
- Efficiency: retrieving small, relevant memories reduces prompt bloat, latency, and token cost.
- Personalization: systems can align outputs to user style, goals, and domain context.
- Reliability: memory supports multi-step tasks where progress spans time.

# Key Principles

## 1. Memory Is Different from Context Window

A large context window helps only within the current prompt/session.  
Memory is persistent and selective across time.

Practical implication:
- Use context windows for immediate reasoning.
- Use memory stores for durable, high-value facts and experiences.

## 2. Memory Is Different from RAG

RAG mainly injects external knowledge for answer grounding.  
Memory captures interaction history and behavioral continuity.

Practical implication:
- RAG answers “What does the world know?”
- Memory answers “What has this user/agent already learned or decided?”
- Production systems usually need both.

## 3. Memory Requires Selection, Not Raw Logging

Storing everything creates noise and cost. Effective memory layers use:
- Salience scoring (importance)
- Recency and frequency signals
- Metadata tagging (user/task/topic/tool)
- Consolidation and summarization
- Forgetting/decay policies

This enables fast retrieval and reduces stale or irrelevant recall.

## 4. Memory Is a Lifecycle

Memory design should define end-to-end flow:
1. Capture: what events become candidate memories.
2. Transform: deduplicate, summarize, classify (fact/episode/procedure).
3. Store: choose suitable indices and retention rules.
4. Retrieve: fetch by intent, relevance, and scope.
5. Update/Forget: strengthen useful items and retire low-value ones.

# Memory Taxonomy for AI Applications

## Short-Term / Working Memory

- Scope: current interaction or session.
- Role: maintain coherence and immediate task state.
- Typical data: recent turns, active plan, current tool outputs.

## Long-Term Memory

- Scope: cross-session and long-horizon tasks.
- Role: adaptation, personalization, and cumulative learning.
- Typical forms:
  - Factual memory: preferences, stable profile/context.
  - Episodic memory: prior tasks, actions, outcomes.
  - Semantic memory: generalized patterns and abstractions.
  - Procedural memory: reusable rules/workflows.

# AI Context

## Where Memory Fits in Agent Architecture

A common agent stack includes:
- LLM (reasoning/generation)
- Planner/policy
- Tool/API layer
- Retriever
- Memory layer

Without memory, the stack remains largely stateless across sessions.  
With memory, the same stack becomes adaptive: it can reuse lessons, maintain user continuity, and plan with historical context.

## Design Guidance for Builders

- Start with concrete memory goals: personalization, task continuity, or self-improvement.
- Define scopes explicitly: user-level, session-level, org/shared memory.
- Keep write paths strict: only store high-signal events.
- Keep retrieval scoped: avoid over-retrieval that crowds reasoning context.
- Add governance early: retention windows, redaction, and sensitive data controls.
- Evaluate memory quality: precision of recall, usefulness, freshness, and behavioral impact.

## Common Failure Modes

- “Big prompt = memory” misconception.
- Unbounded memory growth with no decay/archival.
- Weak retrieval ranking (relevant memory exists but is not surfaced).
- Cross-user leakage due to poor namespace isolation.
- No feedback loop to reinforce useful memories and suppress bad ones.

# References

- IBM Think: https://www.ibm.com/think/topics/ai-agent-memory
- Mem0 Blog: https://mem0.ai/blog/memory-in-agents-what-why-and-how
