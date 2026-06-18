---
title: OpenAI
created: 2026-06-16
updated: 2026-06-18
type: entity
tags:
  - organization
sources:
  - "[OpenAI — Wikipedia](raw/articles/openai-wikipedia.md)"
  - "[Training language models to follow instructions with human feedback](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)"
confidence: high
---

# OpenAI

American AI research organization. Founded in 2015 as a nonprofit, converted to a capped-profit structure in 2019, and further restructured into a Public Benefit Corporation (OpenAI Group PBC) in 2025. Developer of the GPT family of large language models, ChatGPT, DALL-E, Sora, and OpenAI Codex.

## Key Papers in This Wiki

| Paper                                                                                                                                 | Year | Significance                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------- | ---- | ----------------------------------------------------------------------------------------------------------------- |
| [Scaling Laws for Neural Language Models](raw/papers/2020-01-kaplan-scaling-laws/kaplan2020scaling.md)                                | 2020 | First comprehensive scaling laws for LMs (Kaplan et al.)                                                          |
| [Training language models to follow instructions with human feedback](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md) | 2022 | InstructGPT — first large-scale [[rlhf\|RLHF]] application for instruction-following                              |
| [Generating Long Sequences with Sparse Transformers](raw/papers/2019-04-child-sparse-transformer/child2019sparse.md)                  | 2019 | Sparse attention reducing O(n²) to O(n√n)                                                                         |
| [Language Models are Few-Shot Learners](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)                                               | 2020 | GPT-3 — 175B parameter model demonstrating [[in-context-learning\|in-context learning]] at scale                  |
| [Evaluating Large Language Models Trained on Code](raw/papers/2021-07-chen-codex/chen2021codex.md)                                    | 2021 | [[codex\|Codex]] — GPT fine-tuned on GitHub code; introduced [[humaneval\|HumanEval]] benchmark and pass@k metric |
| [Attention Is All You Need](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md)                             | 2017 | Transformer architecture (Google Research/NIPS, several co-authors later joined OpenAI)                           |

## Key People in This Wiki

- [[dario-amodei|Dario Amodei]] — VP of Research (2016–2021); left to co-found [[anthropic|Anthropic]]
- John Schulman — co-founder, Alignment team lead (left for Anthropic in 2024)
- Ilya Sutskever — co-founder, Chief Scientist (left in 2024)
- Jan Leike — Alignment team co-lead, primary author of InstructGPT (left for Anthropic in 2024)

## Known Works

- **GPT-3** (Brown et al., 2020) — 175B parameter LM that demonstrated few-shot learning at scale
- **Codex** (Chen et al., 2021) — GPT fine-tuned on GitHub code; introduced HumanEval benchmark; powers GitHub Copilot
- **InstructGPT** (Ouyang et al., 2022) — first application of RLHF to broad instruction-following; 1.3B model preferred over 175B GPT-3
- **Scaling Laws** (Kaplan et al., 2020) — empirical framework for predicting LM performance vs scale

## Related

- [[codex|Codex]] — GPT fine-tuned on GitHub code; introduced HumanEval benchmark
- [[gpt-3|GPT-3]] — the 175B model that demonstrated in-context learning at scale
- [[microsoft|Microsoft]] — major investor (27% stake), cloud infrastructure partner
- [[anthropic|Anthropic]] — competitor founded by former OpenAI researchers
- [[rlhf|RLHF]] — technique pioneered at scale by OpenAI for aligning LMs with human intent
- [[scaling-laws|Scaling Laws]] — foundational research published by OpenAI
- [[dario-amodei|Dario Amodei]] — former VP of Research
- [[transformer|Transformer]] — underlying architecture of all GPT models
- [[v4a-diff-format|V4A Diff Format]] — prompting technique from OpenAI's GPT-4.1 Prompting Guide
