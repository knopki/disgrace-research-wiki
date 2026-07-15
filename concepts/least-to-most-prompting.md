---
title: Least-to-Most Prompting
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - prompting
  - planning
sources:
  - "[Least-to-Most Prompting Enables Complex Reasoning in Large Language Models](raw/papers/2022-05-zhou-least-to-most-prompting/zhou2022leasttomost.md)"
confidence: high
---

# Least-to-Most Prompting

Least-to-most prompting is a prompting strategy that enables large language models to solve problems harder than those in the demonstration examples by decomposing them into a series of simpler subproblems and solving them sequentially. Introduced by Zhou et al. (Google Research, ICLR 2023), it directly addresses the **easy-to-hard generalization** failure of [[chain-of-thought|Chain-of-Thought (CoT)]].

## Method

Least-to-most prompting consists of two sequential stages, both implemented via few-shot prompting — no training or fine-tuning required ([Zhou et al., 2023](raw/papers/2022-05-zhou-least-to-most-prompting/zhou2022leasttomost.md)):

1. **Decomposition** — query the language model to break the complex problem into a list of simpler subproblems. The prompt contains constant exemplars demonstrating decomposition, followed by the specific question.
2. **Subproblem solving** — sequentially solve each subproblem, where solving a given subproblem is facilitated by the answers to previously solved subproblems. The prompt consists of: (a) constant exemplars showing how to solve subproblems, (b) a potentially empty list of previously answered subquestions with their solutions, and (c) the next subproblem to be solved.

For some tasks, the two stages can be merged into a single-pass prompt by combining decomposition and subproblem solving in one response.

## Key Results

### Symbolic Manipulation (Last-Letter Concatenation)

Testing lists of words (length 4–12), randomly sampled from Wiktionary (500 lists per length) with code-davinci-002 ([Zhou et al., 2023](raw/papers/2022-05-zhou-least-to-most-prompting/zhou2022leasttomost.md)):

| Method | L=4 | L=6 | L=8 | L=10 | L=12 |
|--------|:---:|:---:|:---:|:----:|:----:|
| Standard prompting | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Chain-of-Thought | 84.2 | 69.2 | 50.2 | 39.8 | 31.8 |
| **Least-to-Most** | **94.0** | **88.4** | **83.0** | **76.4** | **74.0** |

Least-to-most prompting degrades much more slowly with length than CoT (74.0% vs 31.8% at L=12). Most errors are concatenation errors (dropping or duplicating letters), not incorrect last letters.

### Compositional Generalization (SCAN)

On the SCAN benchmark (mapping natural language commands to action sequences) under the challenging **length split**, where test action sequences are longer than training ([Zhou et al., 2023](raw/papers/2022-05-zhou-least-to-most-prompting/zhou2022leasttomost.md)):

| Method | code-davinci-002 | text-davinci-002 | code-davinci-001 |
|--------|:---------------:|:---------------:|:---------------:|
| Standard prompting | 16.7 | 6.0 | 0.4 |
| Chain-of-Thought | 16.2 | 0.0 | 0.0 |
| **Least-to-Most** | **99.7** | **76.0** | **60.7** |

Using just 14 exemplars, least-to-most prompting achieves 99.7% on SCAN length split — matching neural-symbolic models trained on 15,000+ examples. The same accuracy holds across all SCAN splits and the full dataset.

Errors (13 failures total in length split): 6 misinterpretations of "twice"/"thrice" following "around", and 7 misinterpretations of "after" as "and".

### Math Reasoning (GSM8K and DROP)

| Method | DROP (Non-football) | DROP (Football) | GSM8K |
|--------|:------------------:|:---------------:|:----:|
| Zero-Shot | 43.86 | 51.77 | 16.38 |
| Standard prompting | 58.78 | 62.73 | 17.06 |
| Chain-of-Thought | 74.77 | 59.56 | 60.87 |
| **Least-to-Most** | **82.45** | **73.42** | **62.39** |

On GSM8K broken down by reasoning steps ([Zhou et al., 2023](raw/papers/2022-05-zhou-least-to-most-prompting/zhou2022leasttomost.md)):

| Method | All | 2 Steps | 3 Steps | 4 Steps | ≥5 Steps |
|--------|:--:|:-------:|:-------:|:-------:|:--------:|
| Least-to-Most | 62.39 | 74.53 | 68.91 | 59.73 | **45.23** |
| Chain-of-Thought | 60.87 | 76.68 | 67.29 | 59.39 | 39.07 |

The benefit concentrates on the hardest multi-step problems (≥5 steps: +6.16%). For DROP, least-to-most outperforms CoT by a large margin (82.45 vs 74.77 non-football, 73.42 vs 59.56 football) — most DROP problems are trivially decomposable.

## Limitations

- **Decomposition doesn't generalise across domains.** A prompt demonstrating decomposition of math word problems is ineffective for commonsense reasoning (e.g., "Did Aristotle use a laptop?"). New decomposition prompts must be designed per domain ([Zhou et al., 2023](raw/papers/2022-05-zhou-least-to-most-prompting/zhou2022leasttomost.md)).
- **Generalising decomposition within the same domain is also hard.** Almost every GSM8K problem can be solved with a correct decomposition, suggesting the bottleneck is problem decomposition, not subproblem solving — consistent with human math experience.
- Exceptional SCAN/last-letter results rely on tasks where decomposition is straightforward.

## Relationship to Other Methods

- [[chain-of-thought|Chain-of-Thought (CoT)]] — Least-to-most directly addresses CoT's failure on easy-to-hard generalization (problems harder than exemplars). On in-distribution tasks (same difficulty as exemplars), CoT and least-to-most are comparable.
- [[self-consistency|Self-Consistency]] — orthogonal technique; least-to-most can be combined with self-consistency for further gains.
- [[plan-and-solve|Plan-and-Solve (PS) Prompting]] — a zero-shot CoT variant that also uses a plan-then-solve structure, but without explicit problem decomposition into subproblems. Least-to-most is few-shot and explicitly generates dependent subproblem sequences.
- [[react|ReAct (Reasoning + Acting)]] — interleaves reasoning with environment actions; least-to-most is purely internal reasoning without environment interaction.
- [[tot|Tree of Thoughts (ToT)]] — generalises CoT with search trees (BFS/DFS); least-to-most uses a linear sequential decomposition rather than search.
- [[in-context-learning|In-Context Learning]] — least-to-most operates within the ICL paradigm.

## Related

- [[chain-of-thought|Chain-of-Thought (CoT)]]
- [[plan-and-solve|Plan-and-Solve (PS) Prompting]]
- [[self-consistency|Self-Consistency]]
- [[tot|Tree of Thoughts (ToT)]]
- [[react|ReAct (Reasoning + Acting)]]
