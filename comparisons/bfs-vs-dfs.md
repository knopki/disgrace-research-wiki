---
title: BFS vs DFS
created: 2026-06-15
updated: 2026-06-15
type: comparison
tags: [comparison, technique]
sources:
  - "[Difference between BFS and DFS](raw/articles/bfs-vs-dfs-gfg/index.md)"
---

# BFS vs DFS

Standard comparison of the two fundamental graph traversal algorithms: Breadth-First Search (BFS) and Depth-First Search (DFS). This page serves as a reference anchor for the BFS/DFS analogies used in the wiki's AI reasoning pages — notably [[chain-of-continuous-thought|Chain of Continuous Thought]] and [[semantic-superposition|Semantic Superposition]].

## Comparison

| Dimension | BFS | DFS |
|-----------|-----|-----|
| Data structure | Queue (FIFO) | Stack (LIFO) |
| Traversal order | Level by level | Sub-tree by sub-tree |
| Builds | Tree level by level | Tree sub-tree by sub-tree |
| Best for | Vertices close to source; unweighted shortest paths | Deep structures; solutions far from source |
| Applications | Bipartite graphs, shortest paths | Acyclic graphs, strongly connected components |

## Relevance to LLM Reasoning

Both algorithms serve as conceptual models for how LLMs explore their solution space during generation:

- **Standard auto-regressive decoding** resembles DFS — the model commits greedily to the first token, then explores ever-deeper conditioned on that choice. This is fast but can miss better solutions that require backtracking.
- **Latent-space reasoning ([[chain-of-continuous-thought|Coconut]])** enables BFS-like behaviour: the model maintains probability mass over multiple candidate reasoning paths simultaneously, dynamically reweighting them as evidence accumulates. ^[raw/papers/2024-12-hao-coconut/index.md]
- **[[semantic-superposition]]** exploits the same BFS analogy — delaying semantic collapse allows breadth-first exploration of reasoning branches before committing to a discrete token. ^[raw/articles/2025-07-06-kot-shredingera-v-golove-u-gpt-kak-superpoziciya-smyslov-men/index.md]

## See Also

- [[bfs|Breadth-First Search (BFS)]] — full BFS algorithm page (mechanics, disconnected graphs, applications)

## Source

GeeksforGeeks — educational computer science resource.
