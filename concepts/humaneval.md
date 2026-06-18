---
title: HumanEval
created: 2026-06-18
updated: 2026-06-18
type: concept
tags:
  - benchmark
  - evaluation
sources:
  - "[Evaluating Large Language Models Trained on Code](raw/papers/2021-07-chen-codex/chen2021codex.md)"
  - "[OpenAI](raw/articles/openai-wikipedia.md)"
confidence: high
---

# HumanEval

A benchmark dataset for measuring functional correctness of program synthesis from docstrings. Introduced by [[openai|OpenAI]] in the [[codex|Codex]] paper ([Chen et al., 2021](raw/papers/2021-07-chen-codex/chen2021codex.md)). Consists of 164 hand-written programming problems, each with a function signature, docstring, a reference solution, and unit tests (average 7.7 tests per problem).

## Design Principles

- **Hand-written** — problems are not scraped from existing sources to avoid data contamination, since models like Codex train on large fractions of GitHub
- **Functional correctness** — a solution is correct if it passes all unit tests, not if it matches a reference solution syntactically
- **Difficulty range** — spans language comprehension, algorithms, and simple mathematics; some comparable to software interview questions
- **Released** at https://www.github.com/openai/human-eval

## pass@k Metric

The primary evaluation metric is pass@k: an unbiased estimator that measures the probability that at least one out of k generated samples passes all unit tests.

```python
def pass_at_k(n, c, k):
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
```

Where n ≥ k samples are generated per problem, c ≤ n pass unit tests. The estimator is unbiased, unlike the naive 1−(1−p̂)ᵏ which consistently underestimates true pass@k.

### Temperature Scaling

- pass@1: optimal temperature ≈ 0.2
- pass@100: optimal temperature ≈ 0.8
- Higher temperatures produce more diverse samples, improving pass@k for larger k

## Key Results

| Model | pass@1 | pass@100 |
|-------|-------:|---------:|
| GPT-3 175B | ~0% | ~0% |
| GPT-J 6B | 11.62% | 27.74% |
| Codex-12B | 28.81% | 72.31% |
| Codex-S-12B | 37.7% | 77.5% (oracle) |

BLEU score is shown to be unreliable for functional correctness — incorrect solutions often have higher BLEU scores than correct ones (Figure 8 in the paper).

## Sample Selection Heuristics

When multiple samples are generated but only one can be evaluated:
- **Random:** baseline
- **Mean log-probability:** selects sample with highest mean token log-probability — improves over random by ~9 pp for Codex-12B, ~11.6 pp for Codex-S-12B
- **Back-translation:** evaluates Codex-D (docstring model) on each sample — underperforms mean log-probability
- **Oracle:** selects the sample that passes unit tests (theoretical upper bound)

## Sandbox

Model-generated code is executed in a gVisor container runtime with eBPF-based firewall rules, preventing:
- Host modification or persistence
- Network access (inbound/outbound) except for experiment control
- Sensitive resource access

Necessary because GitHub contains malicious programs that alter their environments.

## Related Benchmarks

- [[gpt-3|GPT-3]] evaluation — HumanEval tests demonstrate the gap between GPT (near 0%) and code-fine-tuned models
- Used alongside APPS ([Hendrycks et al., 2021]) for measuring coding challenge competence
- Part of the broader shift from match-based metrics (BLEU) to functional correctness in code generation evaluation
