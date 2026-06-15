---
title: Chain of Continuous Thought (Coconut)
created: 2026-06-15
updated: 2026-06-15
type: concept
tags:
  - training
  - methodology
  - optimization
sources:
  - "[Training Large Language Models to Reason in a Continuous Latent Space](raw/papers/2024-12-hao-coconut/hao2025coconut.md)"
confidence: high
---

# Chain of Continuous Thought (Coconut)

A training paradigm introduced by Shibo Hao et al. (FAIR at Meta, 2024) that replaces language-based chain-of-thought (CoT) reasoning with reasoning directly in the continuous latent space of an LLM. Rather than decoding each reasoning step into a word token, the model feeds its last hidden state back as the next input embedding, creating a fully differentiable reasoning loop.

Published at COLM 2025. Code open-sourced at facebookresearch/coconut. ([Hao et al., 2024](raw/papers/2024-12-hao-coconut/hao2025coconut.md))

## Core Idea

Standard CoT forces reasoning into discrete tokens — most of which maintain textual coherence rather than advancing the computation. Coconut removes this constraint by operating entirely in the continuous hidden state:

| Aspect | Language CoT | Continuous Thought |
|--------|-------------|--------------------|
| Representation | Discrete tokens | Continuous vectors (last hidden state) |
| Supervision | Every reasoning token | Only final answer tokens (thoughts are unsupervised) |
| Search pattern | Greedy depth-first | Emergent breadth-first |
| Token cost | High (proportional to chain length) | Low (constant-length thoughts) |
| Differentiability | Via policy gradient | Fully differentiable |

The last hidden state of the model is fed directly as the next input embedding via special boundary tokens `<bot>` and `<eot>`. ([Hao et al., 2024](raw/papers/2024-12-hao-coconut/hao2025coconut.md))

## Training Procedure

A multi-stage curriculum gradually replaces language reasoning steps with continuous thoughts:

1. Train on full language CoT (stage 0)
2. Stage `k`: replace first `k` language steps with `k × c` continuous thoughts
3. Compute loss only on the remaining language tokens — the continuous thoughts receive **no direct supervision**
4. Reset optimizer at each stage switch
5. Final stage: all reasoning is in latent space

The curriculum is **critical**: training directly in latent mode without it collapses to No-CoT-level performance (14.4% vs 34.1% on GSM8k). ([Hao et al., 2024](raw/papers/2024-12-hao-coconut/hao2025coconut.md))

## Emergent BFS Reasoning

The paper's central finding: continuous thoughts encode **multiple alternative next steps simultaneously**, with a natural value function emerging:

> "While 'lempus' initially has the highest value (0.33) at the first reasoning step... the model subsequently assigns the highest value (0.87) to 'rorpus,' a child of 'grimpus,' rather than following 'lempus.'"

This demonstrates genuine [[bfs-vs-dfs|breadth-first search (BFS)]] — the model maintains probability mass over several candidate branches and dynamically reweights them as more information accumulates. Unlike language CoT which greedily commits to a single path at each step, Coconut explores the reasoning graph in width. ([Hao et al., 2024](raw/papers/2024-12-hao-coconut/hao2025coconut.md))

## Performance

| Dataset | vs CoT | Tokens saved |
|---------|--------|-------------|
| ProntoQA (logical) | 99.8% vs 98.8% (+1%) | 10× fewer |
| ProsQA (logical, with search) | 97.0% vs 77.5% (+19.5%) | 3.5× fewer |
| GSM8k (math) | 34.1% vs 42.9% (−8.8%) | 3× fewer |

Coconut excels on tasks requiring **substantial planning and search** (ProsQA), where CoT's greedy chain frequently commits to dead-end paths. On math (GSM8k), CoT still leads — suggesting continuous latent space is particularly effective for logical/structural reasoning vs arithmetic. ([Hao et al., 2024](raw/papers/2024-12-hao-coconut/hao2025coconut.md))

## Relationship to Other Concepts

- **[[chain-of-thought|Chain-of-Thought Prompting (CoT)]]** — standard CoT that Coconut aims to improve upon; CoT also harms SLM performance (Shim et al., 2024), making Coconut's latent approach potentially valuable for smaller models
- **[[semantic-superposition]]** — cites this paper as empirical basis for BFS-like reasoning in latent space. Coconut provides the mechanism (continuous thought) that enables deliberate delay of semantic collapse.
- **[[kv-caching|KV Caching]]** — in language CoT, the KV Cache freezes the model's trajectory once a token is generated. Coconut avoids this by never committing to a discrete token during reasoning — the latent loop is fully within the hidden state, sidestepping cache-induced rigidity.
- **[[superposition]]** — continuous thoughts encoding multiple alternatives is a direct expression of superposition: the hidden state represents more candidate reasoning paths than it has dimensions, tolerating interference between them.
- **[[belief-state-geometry|Belief State Geometry]]** — both papers examine what the residual stream represents. Shai et al. show belief states are linearly encoded; Coconut shows those same states can be used as **actionable representations** — fed back as input to drive reasoning rather than merely observed.
- **[[transformer]]** — the base architecture. Coconut's latent mode exploits the transformer's ability to process any vector as input, not just token embeddings.
- **[[word-embeddings|Word Embeddings]]** — Coconut bypasses learned token embeddings during reasoning, demonstrating that the embedding layer is not essential for computation — any vector in the representational space suffices.
- **[[vibe-coding]]** — Coconut's BFS pattern is the machine-level analog: the model explores solution branches in parallel before committing, mirroring the shift from "writing code step by step" to "exploring solution space."
- **[[sparse-transformer|Sparse Transformer]]** — both address transformer efficiency limits from different angles: Sparse Transformer reduces attention complexity (O(n²) → O(n√n)), Coconut sidesteps token-by-token generation entirely via latent space reasoning.

## Open Questions

- Does Coconut's approach scale to models beyond 8B parameters? Initial Llama 3 experiments suggest yes, but the gap to CoT on math tasks needs investigation.
- Can continuous thoughts be interpreted or visualized? The paper only probes them indirectly via value distributions.
- Is the BFS pattern a general emergent property or specific to the curriculum design and the logical reasoning datasets used?
- How does Coconut interact with RL-based reasoning (GRPO, PPO)?