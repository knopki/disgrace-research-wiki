---
title: Tree of Thoughts (ToT)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - prompting
  - planning
sources:
  - "[Tree of Thoughts: Deliberate Problem Solving with Large Language Models](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)"
confidence: high
---

# Tree of Thoughts (ToT)

Tree of Thoughts (ToT) is a language-model inference framework introduced by Yao et al. (Princeton University & Google DeepMind, NeurIPS 2023) that generalizes [[chain-of-thought|Chain-of-Thought (CoT)]] prompting from a single left-to-right reasoning chain into a *tree* of intermediate reasoning steps ("thoughts"). Instead of decoding one path greedily, the model considers multiple candidate thoughts at each step, self-evaluates their promise, and uses search (breadth-first or depth-first) with lookahead and backtracking to reach a global solution ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

The motivation is the *dual-process* view of cognition (Kahneman): autoregressive LMs are "System 1" — fast, associative, token-level. ToT adds a "System 2" — slow, deliberate, planning-based search over high-level semantic units. It draws on Newell, Shaw & Simon's classical characterization of problem solving as search through a combinatorial tree of partial solutions ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

## Framework

Any problem is framed as a search over a tree. A **node** (state) is `s = [x, z₁…ᵢ]` — the input plus the sequence of thoughts so far. A specific ToT instantiation answers four questions ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)):

1. **Thought decomposition** — how to break the intermediate process into steps. A thought should be "small" enough for the LM to sample diverse candidates, yet "big" enough to evaluate its promise (e.g. one word for crosswords, one equation line for Game of 24, one paragraph plan for creative writing).
2. **Thought generator `G(pθ, s, k)`** — produce *k* candidate next thoughts from a state. Two strategies:
   - *(a) Sample* i.i.d. thoughts from a CoT prompt (works when the thought space is rich, e.g. paragraphs).
   - *(b) Propose* sequentially with a "propose prompt" (works when the space is constrained, e.g. a word or equation line — proposing in one context avoids duplication).
3. **State evaluator `V(pθ, S)`** — score a frontier of states as a search heuristic:
   - *(a) Value* each state independently (LM reasons to a scalar 1–10 or a class like *sure/maybe/impossible*).
   - *(b) Vote* across states (LM compares candidates and selects the most promising — a step-wise self-consistency over "which state to explore").
4. **Search algorithm** — plug-and-play. The paper uses two: BFS (breadth limit *b*) and DFS (with backtracking + value-threshold pruning). A* and MCTS are named as future directions ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

### Properties

- **Generality** — IO, CoT, [[self-consistency|CoT-SC]], and self-refinement are special cases of ToT (trees of limited depth/breadth).
- **Modularity** — base LM, thought decomposition, generator, evaluator, and search are independently swappable.
- **Adaptability** — accommodates different problem properties, LM capabilities, and resource constraints.
- **Convenience** — no fine-tuning or training; works off-the-shelf with a pre-trained LM ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

## Experiments

Three tasks were chosen specifically because they defeat GPT-4 + CoT. All use Chat Completion GPT-4 (temperature 0.7) ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

### Game of 24

Goal: combine 4 numbers with `+ − × ÷` to reach 24. 100 hard games (from 4nums.com, indices 901–1000). Three intermediate-equation thought steps; BFS with breadth *b* ∈ {1, 5}; each candidate evaluated *sure/maybe/impossible* (3 samples each) ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

| Method | Success (100 games) |
|--------|:-------------------:|
| IO prompt | 7.3% |
| CoT prompt | 4.0% |
| CoT-SC (k=100) | 9.0% |
| IO + Refine (k=10) | 27% |
| IO (best of 100) | 33% |
| CoT (best of 100) | 49% |
| **ToT (b=1)** | **45%** |
| **ToT (b=5)** | **74%** |

The headline result: GPT-4 + CoT solves only **4%**, ToT reaches **74%**. Error analysis shows ~60% of CoT samples already fail at the *first* step — exposing the brittleness of left-to-right decoding ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

### Creative Writing

Input: 4 random sentences; output: a coherent 4-paragraph passage ending in those sentences. Depth-2 ToT (depth 1 intermediate plan step): sample *k*=5 plans, vote 5× for best, then sample *k*=5 passages, vote 5×. Coherency scored by GPT-4 (1–10, avg of 5) and by human blind pairwise comparison ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

| Method | GPT-4 coherency (1–10) | Human pref. (ToT≻CoT / CoT≻ToT / similar) |
|--------|:----------------------:|:-------------------------------------------:|
| IO | 6.19 | — |
| CoT | 6.93 | — |
| **ToT** | **7.56** | **41 / 21 / 38** |

Humans preferred ToT over CoT in 41 of 100 pairs vs only 21 the other way. Iterative-refine (a third thought-generation mode — refining old thoughts) lifts ToT to 7.91 and IO to 7.67 ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

### Mini Crosswords (5×5)

DFS with backtracking; at most 10 intermediate steps; states pruned when the LM deems any remaining clue "impossible." Metrics: correct letters (25/game), words (10/game), and fully solved games (out of 20). IO/CoT score <16% word-level; ToT reaches **60%** word-level and solves **4/20** games ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

| Method | Letter % | Word % | Games solved (/20) |
|--------|:--------:|:------:|:------------------:|
| IO | 38.7 | 14.0 | 0 |
| CoT | 40.6 | 15.6 | ~1 |
| **ToT (b=5)** | **78.2** | **60.0** | **4** |
| +best state (oracle) | 82.4 | 67.5 | 7 |
| −prune (ablation) | 65.4 | 41.5 | 4 found / 1 output |
| −backtrack (ablation) | 54.6 | 20.0 | 1 |

Ablations confirm both mechanisms matter: removing pruning (−prune) and removing backtracking (−backtrack) each sharply degrade performance. The state evaluator is imperfect (sometimes prunes a genuinely solvable state), so better DFS pruning heuristics are flagged as future work ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

### Extensions (Appendix B)

Zero-shot ToT on easier tasks (GPT-4): GSM8K IO 51 / CoT 86 / **ToT 90**; StrategyQA IO 73 / CoT 82 / **ToT 83** — only slight gains because GPT-4+CoT is already strong there. On GPT-3.5, the "ToT > CoT > IO" ordering still holds (Game of 24: ToT 19% vs CoT 3%), but GPT-3.5+ToT (19%) lags far behind GPT-4+ToT (74%) — the bottleneck is *thought generation*, not evaluation (GPT-4 generation + GPT-3.5 evaluation scores 64%) ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

**Cost** (Game of 24): ToT costs $0.74/case (5.5k completion tokens) vs CoT best-of-100 $0.47 (49% success) — ToT beats even 100 independent CoT trials while using comparable tokens. Creative Writing: ToT $0.32 vs CoT $0.07 (≈5× cost for ≈5× tokens). ToT can need **5–100×** more generated tokens than CoT depending on beam size and voting ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

## Relationship to Other Work

- **Classical search** — ToT is a modern rendition of heuristic search (A*), where the LM's self-assessment supplies the node heuristic. Related: NeuroLogic A*esque decoding (constrained text generation, sentence-level only).
- **Concurrent / related prompting** — RAP (Hao et al., arXiv 2305.14992) treats LM reasoning as planning with an internal world model via MCTS, but lacks ToT's modularity for swapping search algorithms. Self-refine, [[reflexion|Reflexion]], and self-eval-guided decoding also use self-feedback, but ToT's explicit tree + search + voting is more general ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).
- **[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]]** — both enable search-like reasoning, but Coconut does it *implicitly* in latent space (emergent BFS), whereas ToT does it *explicitly* in language space with LM self-evaluation as the heuristic. ToT handles open-ended tasks (creative writing) that code-based latent methods struggle with.
- **[[semantic-superposition]]** — ToT is the explicit "System 2" counterpart to the associative "System 1" of standard decoding; deliberate search over a tree is the algorithmic realization of the planning that superposition-based BFS analogies describe informally.

## Limitations

1. Unnecessary for tasks GPT-4 already solves with CoT; the paper explores only 3 relatively simple tasks that challenge GPT-4.
2. Higher resource cost (GPT-4 API) — 5–100× more tokens than CoT; modularity lets users trade performance vs cost (beam size, vote count, GPT-3.5 vs GPT-4, few- vs zero-shot).
3. Off-the-shelf LM only; fine-tuning LMs with ToT-style counterfactual decision-making is posed as future work.
4. State evaluator is imperfect (occasionally prunes solvable states) ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

## Related

- [[chain-of-thought|Chain-of-Thought (CoT)]] — the single-path method ToT generalizes; ToT replaces greedy decoding with tree search + self-evaluation
- [[self-consistency|Self-Consistency]] — ensemble over CoT paths via majority vote; ToT extends the idea to structured tree search with lookahead/backtracking
- [[bfs-vs-dfs|BFS vs DFS]] — the two search algorithms ToT plugs in; standard decoding is DFS-like, ToT makes search explicit
- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — latent-space search alternative; emergent BFS vs ToT's explicit linguistic tree
- [[semantic-superposition]] — System 1/System 2 framing; ToT is the deliberate "System 2" search layer
- [[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]] — ToT's cost argues for smaller-model + search tradeoffs in agentic systems
- [[react|ReAct (Reasoning + Acting)]] — same lead author (Yao); ReAct is the interleaved thought-action-loop foundation that ToT generalizes into tree search
