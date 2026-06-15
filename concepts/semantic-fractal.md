---
title: Semantic Fractal
created: 2026-06-16
updated: 2026-06-17
type: concept
tags: [architecture, methodology]
sources:
  - "[AI угрожает программистам могуществом параллелизма](raw/articles/2025-06-30-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/index.md)"
  - "[Позиционные кодировки: «объемное зрение» GPT и секреты AI-агентов](raw/articles/2025-07-04-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/index.md)"
  - "[Контрактное программирование: Ваш семантический щит в эпоху искусственного интеллекта](raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md)"
confidence: medium
---

# Semantic Fractal

A metaphor proposed by Vladimir Ivanov to describe how large language models internally represent code: not as a linear sequence of instructions, but as branching "vectors of plan" embedded in a high-dimensional semantic space, connected by thousands of relationships.

## The Metaphor

Where a human sees `Block A → Block B`, an LLM sees two nodes linked by many possible relations — sequence, parallelism, dependency, data flow, mutual exclusion. Sequential execution is just one of thousands of edges the model could traverse between them. ^[raw/articles/2025-06-30-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/index.md]

The term "fractal" captures the recursive, self-similar structure: at every level of granularity (function, module, system), the same branching semantic graph applies. The model does not impose a single traversal order; the order emerges from the specific task.

## Connection to Transformer Architecture

The metaphor maps naturally onto transformer internals: attention layers compute pairwise relationships between all token representations simultaneously. The residual stream maintains a distributed, high-dimensional representation where no single "current state" dominates — consistent with the idea of parallel semantic branches rather than a sequential program counter.

[[positional-encoding|Positional Encoding]] provides the mechanism that makes the semantic fractal concrete. Sinusoidal PE at multiple frequencies creates a multi-scale coordinate system where each token simultaneously knows its position at the chapter, paragraph, and sentence level — exactly the self-similar nested structure the fractal metaphor describes. When PE vectors are added directly to semantic embeddings, the resulting representation fuses *what* a token means with *where* it sits in every level of the hierarchy simultaneously. ^[raw/articles/2025-07-04-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/index.md]

## Why It Matters

If the semantic fractal is a faithful model of how LLMs represent code, then:
- Asking an LLM to produce sequential code is a projection of a richer internal structure onto a linear surface — the model is underemployed.
- Parallelizing generated output is not an extra step; it is closer to the native representation.
- Our current metrics and prompts may be systematically obscuring this capability.

## Belief State Geometry

A 2024 study by Adam Shai et al. ([arxiv 2405.15943](https://arxiv.org/abs/2405.15943)) discovered that as a transformer generates output, it constructs a measurable **belief state geometry** in its residual stream. The model builds an internal fractal "plan" of the answer: each node is the model's belief about which semantic state it occupies, and edges are transitions between states. When the model writes code, it is effectively unfolding this inner semantic fractal.

Vladimir Ivanov connects this to [[contract-programming|Contract Programming]]: structured code contracts function as **belief state refiners** — they force the model to narrow its belief state precisely, constraining its internal fractal navigation to the correct path. This makes contracts a natural, not an imposed, mechanism for controlling LLM code generation. ^[raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md]

## Related

- [[innate-parallelism|Innate Parallelism]] — the broader thesis built on this metaphor
- [[positional-encoding|Positional Encoding]] — the architectural mechanism that creates the multi-scale nested representations the fractal describes
- [[contract-programming|Contract Programming]] — uses belief state geometry as its scientific foundation; contracts refine the model's internal fractal plan
- [[vladimir-ivanov|Vladimir Ivanov]] — author who introduced the concept
