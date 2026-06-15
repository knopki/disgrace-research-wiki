---
title: Breadth-First Search (BFS)
created: 2026-06-15
updated: 2026-06-15
type: concept
tags:
  - technique
sources:
  - "[Breadth First Search or BFS for a Graph](raw/articles/2012-bfs-gfg.md)"
  - "[Difference between BFS and DFS](raw/articles/2019-bfs-vs-dfs-gfg.md)"
---

# Breadth-First Search (BFS)

Breadth-First Search is a graph traversal algorithm that explores a graph **level by level** — visiting all vertices at distance $k$ from the source before moving to distance $k+1$. It uses a queue (FIFO) as its primary data structure.

The algorithm serves as the canonical reference for breadth-first exploration strategies, including recent analogies in LLM reasoning — see [[bfs-vs-dfs|BFS vs DFS]] for the comparison with Depth-First Search, and how both map to [[semantic-superposition|Semantic Superposition]] and [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]].

## Algorithm (Single Source)

Given an adjacency list representation of an undirected graph with $V$ vertices, starting from a source vertex `src`:

1. Mark `src` as visited and enqueue it.
2. While the queue is not empty:
   - Dequeue a vertex `curr`.
   - Process `curr` (e.g., append to result list).
   - For each unvisited neighbour of `curr`: mark it visited, enqueue it.
3. The visitation order is level-by-level — all vertices at distance 1, then distance 2, etc.

To prevent infinite loops in cyclic graphs, a **visited array** of size $V$ is used — nodes are marked as soon as they are discovered (enqueued), not when they are processed.

### Complexity
- **Time:** $O(V + E)$ — each vertex and edge is visited exactly once.
- **Space:** $O(V)$ — queue (holds at most one level of the graph) + visited array.

## BFS for Disconnected Graphs

A single-source BFS only visits vertices reachable from `src`. To traverse all components of a disconnected graph, iterate over every vertex and start a BFS from each unvisited vertex:

```
for each vertex v in 0..V-1:
    if not visited[v]:
        bfs_from(v)
```

The complexity remains $O(V + E)$ since each vertex and edge is processed exactly once across all components.

## Applications

- **Shortest path** in unweighted graphs — every edge has equal weight, so the first time BFS reaches a vertex gives the shortest distance from the source.
- **Web crawling** — starts from a seed URL, explores all links on the page before following them deeper.
- **Social networking** — friend-of-friend suggestions (degree-2 connections).
- **GPS navigation** — finding the shortest route when all roads have equal cost.
- **Network broadcasting** — flooding a message to all nodes in a peer-to-peer network.
- **Cycle detection** — if an edge leads to an already-visited node that is not the parent, a cycle exists.
- **Ford-Fulkerson algorithm** — BFS is used to find augmenting paths in the Edmonds-Karp implementation.

## Relevance to LLM Reasoning

BFS serves as a conceptual model for how advanced LLM reasoning methods explore solution space:

- **Standard auto-regressive decoding** resembles DFS — greedy token-by-token commitment along a single path.
- **[[semantic-superposition]]** exploits BFS-like behaviour: maintaining multiple hypotheses in latent space delays semantic collapse, allowing breadth-first exploration before committing to discrete tokens.
- **[[chain-of-continuous-thought|Coconut]]** demonstrates genuine BFS in continuous latent space: the model encodes multiple candidate next steps simultaneously and dynamically reweights them as evidence accumulates — exactly analogous to queue-based level-by-level exploration. ([Hao et al., 2024](raw/papers/2024-12-hao-coconut/hao2025coconut.md))

## See Also

- [[bfs-vs-dfs|BFS vs DFS]] — side-by-side comparison of BFS and DFS
- [[semantic-superposition|Semantic Superposition]] — BFS-like reasoning in LLM prompt engineering
- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — emergent BFS in latent space
- [[kv-caching|KV Caching]] — the mechanism that enforces greedy (DFS-like) token commitment