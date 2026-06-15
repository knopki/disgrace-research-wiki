---
source_url: https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/
ingested: 2026-06-15
sha256: 923a354be31a87334d69d849fb1c1dc435c3977e5d1bfe5763c99ccf93b67318
---

# Breadth First Search (BFS) for a Graph — GeeksforGeeks

## Overview
BFS is a graph traversal algorithm that starts from a source node and explores the graph **level by level**. It visits all nodes directly adjacent to the source first, then moves to their neighbours, continuing until all reachable nodes are visited.
To prevent revisiting nodes (important in cyclic graphs), a **visited array** is used.

---

## BFS from a Given Source (Undirected Graph)

### Algorithm
1. Start from a given source vertex (e.g., `src = 0`).
2. Mark it as visited and push it into a queue.
3. While queue is not empty:
   - Dequeue a node `curr`.
   - Process `curr` (append to result list).
   - For each unvisited neighbour of `curr`, mark it visited and enqueue it.
4. The order of visitation is level-by-level (increasing distance from source).

### Example
**Input:** `adj = [[1, 2], [0, 2], [0, 1, 3, 4], [2], [2]]`
**Output:** `[0, 1, 2, 3, 4]`
**Explanation:** Starting from 0 → 1,2 → 3,4 (level order).

### Complexity
- **Time:** O(V + E) — each vertex and edge visited once.
- **Space:** O(V) — queue and visited array.

---

## BFS for Disconnected Graphs
If the graph is disconnected, a single-source BFS will only visit one component. To cover **all vertices**, iterate over every vertex and start a BFS from each unvisited vertex.

### Algorithm
1. Create a visited array (all false).
2. For each vertex `i` from 0 to V-1:
   - If `visited[i]` is false, perform BFS starting from `i` (using the same level-by-level logic).
3. This ensures every connected component is traversed.

### Complexity
- **Time:** O(V + E) — each vertex and edge is processed exactly once across all components.
- **Space:** O(V) — queue and visited array.

---

## Applications of BFS
- Shortest path in unweighted graphs
- Web crawling
- Social networking (friend suggestions)
- GPS navigation
- Broadcasting in networks
- Cycle detection
- Ford-Fulkerson algorithm (finding augmenting paths)
