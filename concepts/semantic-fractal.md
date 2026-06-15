---
title: Semantic Fractal
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [architecture, methodology]
sources:
  - "[AI угрожает программистам могуществом параллелизма](raw/articles/2025-06-30-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/index.md)"
---

# Semantic Fractal

A metaphor proposed by Vladimir Ivanov to describe how large language models internally represent code: not as a linear sequence of instructions, but as branching "vectors of plan" embedded in a high-dimensional semantic space, connected by thousands of relationships.

## The Metaphor

Where a human sees `Block A → Block B`, an LLM sees two nodes linked by many possible relations — sequence, parallelism, dependency, data flow, mutual exclusion. Sequential execution is just one of thousands of edges the model could traverse between them. ^[raw/articles/2025-06-30-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/index.md]

The term "fractal" captures the recursive, self-similar structure: at every level of granularity (function, module, system), the same branching semantic graph applies. The model does not impose a single traversal order; the order emerges from the specific task.

## Connection to Transformer Architecture

The metaphor maps naturally onto transformer internals: attention layers compute pairwise relationships between all token representations simultaneously. The residual stream maintains a distributed, high-dimensional representation where no single "current state" dominates — consistent with the idea of parallel semantic branches rather than a sequential program counter.

## Why It Matters

If the semantic fractal is a faithful model of how LLMs represent code, then:
- Asking an LLM to produce sequential code is a projection of a richer internal structure onto a linear surface — the model is underemployed.
- Parallelizing generated output is not an extra step; it is closer to the native representation.
- Our current metrics and prompts may be systematically obscuring this capability.

## Related

- [[innate-parallelism|Innate Parallelism]] — the broader thesis built on this metaphor
- [[vladimir-ivanov|Vladimir Ivanov]] — author who introduced the concept
