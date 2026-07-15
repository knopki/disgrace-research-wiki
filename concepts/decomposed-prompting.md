---
title: Decomposed Prompting (DecomP)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - prompting
  - agent
  - planning
  - tool-use
sources:
  - "[Decomposed Prompting: A Modular Approach for Solving Complex Tasks](raw/papers/2022-10-khot-decomposed-prompting/khot2023decomp.md)"
confidence: high
---

# Decomposed Prompting (DecomP)

Decomposed Prompting (DecomP) is a few-shot prompting paradigm introduced by Khot et al. (Allen Institute for AI, Stony Brook University, University of Edinburgh, ICLR 2023) that solves complex tasks by **decomposing** them into simpler sub-tasks and **delegating** each sub-task to a dedicated handler — a separate few-shot prompt, a further decomposed sub-task, or a symbolic function ([Khot et al., 2023](raw/papers/2022-10-khot-decomposed-prompting/khot2023decomp.md)).

## Core Architecture

DecomP has two principal components:

1. **Decomposer LLM** — generates a *prompting program* P = (f₁, Q₁, A₁), ..., (fₖ, Qₖ, Aₖ) for a complex query Q. Each step specifies a sub-task function fᵢ and a sub-query Qᵢ. A symbolic controller routes queries to handlers and tracks answers until an `[EOQ]` marker produces the final answer.

2. **Sub-task handlers** — a shared library of modular functions, each operationalised as a separate few-shot prompt. Handlers can be independently optimised, further decomposed, or replaced with trained models or symbolic systems (e.g. Elasticsearch for retrieval) without touching the rest of the system.

The software engineering analogy is explicit: the decomposer defines the top-level program using interfaces to simpler functions; sub-task handlers are modular, debuggable, and upgradable implementations — a software library for LLM prompting ([Khot et al., 2023](raw/papers/2022-10-khot-decomposed-prompting/khot2023decomp.md)).

## Capabilities

**Hierarchical decomposition.** If a sub-task is itself too hard for few-shot prompting (e.g. extracting the k-th letter of a word), it can be further decomposed into even simpler sub-tasks — identify all letters and positions, then select the k-th element. Existing shared sub-task prompts (like `split`) are reused.

**Recursive decomposition.** For tasks where complexity scales with input length (e.g. list reversal), the decomposer can call *itself* recursively, splitting the input into smaller pieces until a base case is reached where a standard prompt (e.g. CoT) is accurate. This enables length generalisation beyond the training distribution — not achievable with standard CoT ([Khot et al., 2023](raw/papers/2022-10-khot-decomposed-prompting/khot2023decomp.md)).

**External API integration.** Sub-tasks infeasible for LLMs alone (e.g. retrieving from large corpora) can be delegated to symbolic systems such as Elasticsearch. The `retrieve_odqa` handler returns both answers and supporting documents, which downstream sub-tasks (like `multihop_rcqa`) consume.

## Key Results

| Task | DecomP | CoT baseline | Gain |
|------|--------|-------------|------|
| k-th letter concat (N=3, k=3) | ~97% EM | ~74% EM | +23 pts |
| k-th letter concat (N=5, OOD) | ~97% EM | ~12% EM | +85 pts |
| List reversal (N=4) | ~76% EM | ~42% EM | +34 pts |
| List reversal (N=10, OOD) | ~59% EM | ~1% EM | +58 pts |
| CommaQA-E (IID) | 64.2 EM | 42.0 EM | +22 pts |
| CommaQA-E (Comp. Gen.) | 59.7 EM | 33.8 EM | +26 pts |
| Open-domain QA (Codex, avg 3 datasets) | 49.9-64.1 F1 | 38.1-47.1 F1 | +11-17 pts |
| MultiArith (post-processing) | 95.0 EM | 78.0 EM | +17 pts |
| GSM8K (post-processing) | 50.6 EM | 36.0 EM | +14 pts |

All results use GPT-3 text-davinci-002 or code-davinci-002, except Flan-T5-XXL which matches Codex scores on open-domain QA ([Khot et al., 2023](raw/papers/2022-10-khot-decomposed-prompting/khot2023decomp.md)).

## Relationship to Other Techniques

- **[[chain-of-thought|Chain-of-Thought (CoT)]]** — DecomP is structurally different from CoT. CoT demonstrates the *entire* reasoning chain in a single prompt, which becomes fragile as task complexity grows. DecomP separates *decomposition* from *sub-task execution*, allowing each sub-task prompt to be independently optimised with richer examples. On k-th letter concatenation, even a "rolled out" CoT containing the same reasoning as DecomP underperforms, showing modularity itself helps ([Khot et al., 2023](raw/papers/2022-10-khot-decomposed-prompting/khot2023decomp.md)).

- **Least-to-Most Prompting** (Zhou et al., 2023) — the closest prior work. Both decompose into sub-questions. Unlike Least-to-Most, DecomP supports non-linear decomposition structures (recursion, iteration, parallel execution), generates sub-questions iteratively (not one-shot), and can have different handlers for each sub-question type ([Khot et al., 2023](raw/papers/2022-10-khot-decomposed-prompting/khot2023decomp.md)).

- **[[tot|Tree of Thoughts (ToT)]]** — ToT generalises CoT to tree search via self-evaluation; DecomP generalises CoT to modular program composition. Both are complementary — ToT could in principle search over DecomP's decomposition space.

- **[[react|ReAct (Reasoning + Acting)]]** — ReAct interleaves reasoning and actions in a single trajectory. DecomP shares the module-swapping philosophy (external tools as handlers) but structures the process as a decomposer-generated program rather than free-form thought-action-observation loops.

## Limitations and Caveats

- Requires manual effort to design decomposer and sub-task prompts. The paper does not address automatic decomposition discovery.
- The decomposer LLM must reliably produce structured outputs with `[subtask]` markers — weaker models (smaller Flan-T5) struggled with this, limiting decomposition to GPT-3-scale models.
- Recursive decomposition adds latency proportional to recursion depth (each recursive call is a full LLM round-trip).
- Evaluated at 2023 model capability levels (GPT-3.5 family, Flan-T5). Later models (GPT-4, Claude 3) may narrow the gap between CoT and DecomP because they handle longer contexts and harder sub-tasks within a single CoT chain.
