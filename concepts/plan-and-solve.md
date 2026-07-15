---
title: Plan-and-Solve Prompting (PS)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - prompting
sources:
  - "[Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models](raw/papers/2023-05-wang-plan-and-solve/wang2023planandsolve.md)"
confidence: high
---

# Plan-and-Solve Prompting (PS)

Plan-and-Solve (PS) Prompting is a zero-shot chain-of-thought method by Wang et al. (Singapore Management University et al., ACL 2023) that improves on [[chain-of-thought#zero-shot-cot|Zero-shot-CoT]] by replacing the bare trigger "Let's think step by step" with an explicit plan-then-solve instruction ([Wang et al., 2023](raw/papers/2023-05-wang-plan-and-solve/wang2023planandsolve.md)).

## Motivation: the three pitfalls of Zero-shot-CoT

Error analysis of 46 GSM8K problems answered incorrectly by Zero-shot-CoT on GPT-3 (Figure 1) isolated three failure modes:

- **Calculation errors** — 7% of incorrect examples
- **Missing-step errors** — 12% of incorrect examples (intermediate steps dropped, especially when many steps are required)
- **Semantic misunderstanding** — 27% of incorrect examples (the dominant source of error)

PS Prompting targets the *missing-step* failure; the extended **PS+** variant additionally targets *calculation* errors.

## Method

Like Zero-shot-CoT, PS prompting is a two-step pipeline:

1. **Reasoning generation** — prepend a trigger sentence to the input ("Q: [X]. A: [T]") and decode greedily (1 chain).
2. **Answer extraction** — append an answer-extraction prompt (e.g. "Therefore, the answer (arabic numerals) is") and let the model return the final answer.

The trigger for PS replaces "Let's think step by step" with:

> "Let's first understand the problem and devise a plan to solve the problem. Then, let's carry out the plan and solve the problem step by step."

This explicitly induces the model to (a) **devise a plan** decomposing the task into subtasks, then (b) **carry out the plan**. Unlike few-shot CoT, no demonstration examples are needed.

### PS+ (detailed instructions)

To address calculation errors and improve reasoning-step quality, PS is extended with more detailed instructions:

> "Let's first understand the problem, extract relevant variables and their corresponding numerals, and devise a complete plan. Then, let's carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and commonsense), solve the problem step by step, and show the answer."

The authors hypothesise that instructing the model to extract relevant variables reduces missing-step errors — a correlation analysis of variable extraction vs missing-step errors (Figure 5) supports this (correlation < 0).

## Experimental setup

- **Backbone:** public GPT-3 (text-davinci-003, 175B), temperature 0 (greedy).
- **Benchmarks (10 datasets):** arithmetic (GSM8K, SVAMP, MultiArith, AddSub, AQuA, SingleEq), commonsense (CommonsenseQA, StrategyQA), symbolic (Last Letter Concatenation, Coin Flip).
- **Baselines:** Zero-shot-CoT (Kojima et al., 2022), Zero-shot-PoT (Chen et al., 2022), Manual-CoT (8-shot), Auto-CoT (Zhang et al., 2022).

## Key results

**Arithmetic reasoning** (Table 2, text-davinci-003). PS+ consistently beats Zero-shot-CoT across all six datasets; PoT (Program-of-Thought, runs Python via Codex) is the strongest zero-shot competitor:

| Method | MultiArith | GSM8K | AddSub | AQuA | SingleEq | SVAMP | Avg |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Zero-shot-CoT | 83.8 | 56.4 | 85.3 | 38.9 | 88.1 | 69.9 | 70.4 |
| PoT | 92.2 | 57.0 | 85.1 | 43.9 | 91.7 | 70.8 | 73.5 |
| PS | 87.2 | 58.2 | 88.1 | 42.5 | 89.2 | 72.0 | 72.9 |
| PS+ | 91.8 | 59.3 | 92.2 | 46.0 | 94.7 | 75.7 | 76.7 |
| Manual-CoT (8-shot) | 93.6 | 58.4 | 91.6 | 48.4 | 93.5 | 80.3 | 77.6 |
| Auto-CoT | 95.5 | 57.1 | 90.8 | 41.7 | 92.1 | 78.1 | 75.9 |

PS+ outperforms PoT on five of six arithmetic datasets. Its average (76.7%) is slightly below Manual-CoT (77.6%) but above Auto-CoT (75.9%).

**Commonsense reasoning** (Table 3): PS+ 71.9% (CSQA) and 65.4% (StrategyQA) vs Zero-shot-CoT 65.2% / 63.8%; underperforms Few-Shot Manual-CoT (78.3% / 71.2%). PoT excluded (not applicable).

**Symbolic reasoning** (Table 4): PS+ 75.2% (Last Letter) and 99.6% (Coin Flip) vs Zero-shot-CoT 64.8% / 96.8% and Manual-CoT 70.6% / 100.0%. PS+ beats Manual-CoT on Last Letter and nearly matches it on Coin Flip.

### With self-consistency

Combining PS+ with [[self-consistency|Self-Consistency]] (temperature 0.7, N=10) on GSM8K and SVAMP (Figure 4): PS+ + SC reaches 73.7% and 84.4% vs 58.7% and 75.7% without SC, and beats Zero-shot-CoT + SC (70.7% / 81.7%).

### Prompt ablations

Appendix A.1 (Tables 7–16) ablates the trigger sentence. Progressive additions — variable/numeral extraction, complete-plan phrasing, intermediate calculation, commonsense attention — steadily raise accuracy (e.g. AQuA 42.5 → 46.0; GSM8K 58.2 → 59.3; MultiArith 87.2 → 91.8; Coin Flip up to 99.6 with explicit per-flip state tracking).

## Significance

PS prompted the line of **plan-and-execute** agent architectures (see index cross-reference at [[chain-of-thought|CoT]]): decomposing a task into a plan then executing it became a core agent pattern. The paper's broader claim — that a carefully worded zero-shot prompt can rival few-shot CoT — motivated subsequent automatic prompt-engineering work.

## Related

- [[chain-of-thought|Chain-of-Thought (CoT)]] — PS replaces Zero-shot-CoT's trigger with plan-then-solve; shares the two-step reasoning+extraction pipeline
- [[self-consistency|Self-Consistency]] — PS+ combined with SC yields further large gains (Figure 4)
- [[in-context-learning|In-Context Learning]] — PS is a zero-shot method (no demonstrations) operating within the ICL paradigm
- [[entities/gpt-3|GPT-3]] — all experiments use GPT-3 (text-davinci-003)
- [[scaling-laws|Scaling Laws]] — PS+ trades off against few-shot CoT, which is an emergent ability of scale
