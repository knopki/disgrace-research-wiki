---
title: Codex
created: 2026-06-18
updated: 2026-06-18
type: entity
tags:
  - model
  - organization
sources:
  - "[Evaluating Large Language Models Trained on Code](raw/papers/2021-07-chen-codex/chen2021codex.md)"
  - "[Language Models are Few-Shot Learners](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)"
confidence: high
---
# Codex

A family of GPT-based language models developed by [[openai|OpenAI]], fine-tuned on publicly available code from GitHub. Codex demonstrated that fine-tuning large language models on code produces non-trivial program synthesis capabilities from natural language docstrings. A production version of Codex powers GitHub Copilot.

## Model Variants

| Variant | Description | HumanEval pass@1 |
|---------|-------------|-----------------:|
| Codex-12M | Smallest model in the suite | 2.00% |
| Codex-25M | | 3.21% |
| Codex-42M | | 5.06% |
| Codex-85M | Roughly equivalent to GPT-Neo-2.7B (30× fewer params) | 8.22% |
| Codex-300M | Roughly equivalent to GPT-J-6B (20× fewer params) | 13.17% |
| Codex-679M | | 16.22% |
| Codex-2.5B | | 21.36% |
| **Codex-12B** | Largest model in the paper | **28.81%** |
| **Codex-S-12B** | Supervised fine-tuned on standalone functions | **37.7%** |

## Training

- **Data:** 179 GB of unique Python files <1 MB from 54M public GitHub repositories (May 2020). Filtered to 159 GB.
- **Base:** Fine-tuned from the GPT-3 model family. Starting from scratch didn't improve results, but fine-tuning from GPT-3 converged faster.
- **Optimizer:** Adam (β1=0.9, β2=0.95, ε=10⁻⁸, weight decay 0.1)
- **Tokens:** 100B tokens trained. Cosine LR decay with 175-step linear warmup.
- **Tokenizer:** GPT-3 text tokenizer + additional tokens for whitespace runs (~30% fewer tokens for code).

## Supervised Fine-Tuning (Codex-S)

Two data sources:
1. **Competitive programming** — 10,000 problems from contest/interview prep websites with well-written problem statements and excellent test coverage
2. **CI tracing** — 40,000 problems from open-source projects using `sys.setprofile` to capture function inputs/outputs during integration tests (travis/tox pipelines + PyPI packages)

Problems were filtered by generating 100 samples with Codex-12B — only kept if at least one sample passed unit tests. Trained with LR 1/10 of Codex fine-tuning rate until validation loss plateaued (<10B tokens).

## Docstring Generation (Codex-D)

Codex-D was trained on the reverse task: given a function signature + code body, generate the docstring. Human-graded evaluation showed 20.3% pass@1 and 46.5% pass@10 — lower but comparable to Codex-S, potentially due to lower-quality docstrings in training data (developers invest less time writing docstrings than code).

## Limitations

- Not sample efficient — trained on hundreds of millions of lines of code; a strong CS student can solve more problems per amount of code seen
- Performance drops exponentially with chain length in docstrings (factor 2-3 per additional operation)
- Difficulty with variable-to-operation binding when many variables are involved
- Can generate undefined or out-of-scope code (variables, functions, attributes)
- Alignment gap: generates worse code when prompted with subtly buggy code; this gap increases with model size
- Generates insecure code: frequently selects insecure cryptographic parameters (RSA < 2048 bits, AES-ECB)

## Broader Impacts

The paper identifies risks including over-reliance (novice programmers), misalignment (model "chooses" to generate buggy code even when capable of correct code), bias amplification, economic displacement, security vulnerabilities, and environmental costs. Mitigations include careful UI design, content filtering, rate limiting, code review requirements, and RLHF.

## Relationships

- Built on [[entities/gpt-3|GPT-3]] — the base architecture and model family
- Developed by [[openai|OpenAI]]
- Powers GitHub Copilot (via [[microsoft|Microsoft]])
- Evaluated on [[humaneval|HumanEval]] — the 164-problem benchmark introduced in the same paper
- Related to [[in-context-learning|In-Context Learning]] — Codex inherits GPT-3's in-context learning capabilities
