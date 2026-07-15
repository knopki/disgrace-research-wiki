---
title: MemGPT (MemoryGPT)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - agent
  - memory
  - architecture
  - framework
  - orchestration
sources:
  - "[MemGPT: Towards LLMs as Operating Systems](raw/papers/2023-10-packer-memgpt/packer2023memgpt.md)"
confidence: high
---

# MemGPT (MemoryGPT)

MemGPT is an OS-inspired system that gives a fixed-context LLM the **illusion of unbounded context** via *virtual context management* — an explicit hierarchy of memory tiers that the LLM itself paginates in and out of its own context window through function calls (Packer et al., UC Berkeley, arXiv:2310.08560, 2024). Instead of training longer-context models, MemGPT treats the context window as a constrained memory resource (analogous to physical RAM) and pairs it with external storage (analogous to disk), with the LLM acting as its own memory manager.

The authors' core claim: directly extending transformer context incurs quadratic compute/memory cost and still underperforms once context grows (citing [[lost-in-the-middle|Lost in the Middle]] — models use long context unevenly), so fixed-context models plus hierarchical memory are a more practical path to long-horizon tasks. MemGPT is evaluated on two regimes where finite context caps existing LLMs: **document analysis** (texts far exceeding the window) and **multi-session chat** (conversational agents that remember, reflect, and evolve).

## Memory architecture

Main context (prompt tokens, "physical memory") is split into three contiguous sections:
- **System instructions** — read-only; describe the control flow, memory tiers, and the MemGPT function schema.
- **Working context** — a fixed-size read/write block of unstructured text, writeable only via function calls; holds key facts, preferences, and persona state.
- **FIFO queue** — rolling message history (user↔agent, system alerts, function I/O); its first index holds a recursive summary of already-evicted messages.

External context ("disk") comprises two databases:
- **Recall storage** — append-only log of every message; read via function calls; written by the queue manager.
- **Archival storage** — a read/write database of arbitrarily long text objects; implemented with PostgreSQL + the `pgvector` extension (HNSW index, cosine similarity) for vector search over embeddings (OpenAI `text-embedding-ada-002`).

## Control flow and self-directed memory

The **queue manager** appends incoming events to the FIFO queue, triggers inference, and enforces a **queue eviction policy**: at a *warning token count* (~70% of the window) it injects a "memory pressure" system alert so the LLM can move important FIFO content into working/recall/archival context *before* eviction; at a *flush token count* (100%) it evicts a block of messages, generates a new recursive summary, and drops them from context (they remain in recall storage indefinitely).

The **function executor** parses the LLM's completion string as function calls. Memory edits and retrieval are entirely self-directed — MemGPT autonomously decides when to move data between tiers (e.g., updating working context on a relationship-status change). Functions can set `request_heartbeat=true` to immediately re-enter the LLM processor, enabling **function chaining** (multi-step retrieval/collation) before yielding to the user.

**Events** trigger inference: user messages, system messages (capacity warnings), interaction events (user logged in), and timed events (scheduled unprompted runs).

## Results

- **Deep Memory Retrieval (DMR)** on the Multi-Session Chat (MSC) dataset — MemGPT vs fixed-context baselines (which see only a lossy 5-session summary):
  - GPT-3.5 Turbo: 38.7% → **66.9%** accuracy (ROUGE-L 0.394 → 0.629)
  - GPT-4: 32.1% → **92.5%** (ROUGE-L 0.296 → 0.814)
  - GPT-4 Turbo: 35.3% → **93.4%** (ROUGE-L 0.359 → 0.827)
- **Conversation opener** (engagement, vs gold persona labels and human openers): MemGPT with various backbones matches or exceeds the human-written opener (GPT-4 SIM-H 0.773; human SIM-H 1.000). Storing info in working context is key to engaging openers.
- **Document QA** (retriever-reader over NaturalQuestions-Open): MemGPT's accuracy is unaffected by document count (it paginates through archival storage), whereas fixed-context baselines plateau at retriever quality and degrade under truncation. GPT-4 performs best; **GPT-3.5 is significantly worse** due to weaker function-calling.
- **Nested Key-Value retrieval** (multi-hop, values that are themselves keys, 0–4 nesting levels, 140 UUID pairs ≈ 8k tokens): GPT-4 baselines hit 0% by 3 nesting levels; MemGPT (GPT-4) completes nested lookups at all depths via repeated function queries. MemGPT (GPT-4 Turbo) is worse than MemGPT (GPT-4) on this task — extra base-context does not help, and hurts, multi-hop chaining.

## Relationship to other concepts

- [[paged-attention|PagedAttention & vLLM]] — MemGPT's whole framing ("LLM OS", paging between context and external storage, memory-pressure interrupts) directly borrows the **OS virtual-memory / paging analogy** that PagedAttention pioneered for KV-cache serving, but applies it to the *agent's own working memory* rather than GPU KV-cache allocation.
- [[generative-agents|Generative Agents]] — complementary memory architectures: Generative Agents manage a memory stream via recency/importance/relevance retrieval inside the window; MemGPT generalizes this to an explicit tiered (working/recall/archival) hierarchy with eviction and self-editing beyond the window. The two are frequently built on together (the project later became *Letta*).
- [[coala|CoALA]] — MemGPT is an instance of a cognitive architecture for language agents: working context ≈ working memory, recall/archival ≈ long-term memory, function calls span internal (retrieve/edit) and external (grounding) action space.
- [[retrieval-augmented-generation|Retrieval-Augmented Generation]] — archival storage is a writable, agent-controlled RAG store; unlike static RAG, the agent decides what to write, when to retrieve, and when to evict.
- [[toolformer|Toolformer]] — MemGPT builds on the function-calling ability of LLM agents (Schick et al., 2023) to let the model read/write external state and modify its own context.
- [[lost-in-the-middle|Lost in the Middle]] — cited as the motivation for *not* relying on raw context scaling; MemGPT sidesteps uneven long-context utilization by actively managing what sits in-window.

## Open questions / limitations (from the paper)

- Performance is gated by base-model function-calling quality (GPT-3.5 struggles; GPT-4 best).
- The agent may stop paginating retriever results before exhausting them, hurting recall on hard queries.
- Future work: other unbounded-context domains, richer memory tiers (databases/caches), and improved control-flow/memory policies.
