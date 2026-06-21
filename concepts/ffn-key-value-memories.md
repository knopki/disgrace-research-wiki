---
title: Transformer FFN as Key-Value Memories
created: 2026-06-18
updated: 2026-06-18
type: concept
tags:
  - architecture
  - interpretability
  - paper
sources:
  - "[Transformer Feed-Forward Layers Are Key-Value Memories](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md)"
confidence: high
---

## Definition

The feed-forward (FFN) layers in a [[transformer|Transformer]] language model function as **unnormalized key-value memories**, where each hidden dimension in the FFN's inner layer acts as a memory cell with a **key** vector (detecting input patterns) and a **value** vector (inducing an output distribution). ([Geva et al., 2021](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md))

## Mathematical Equivalence

A standard feed-forward layer and a neural memory network differ only in the normalization of memory coefficients:

| Component | Feed-forward layer | Neural memory (softmax) |
|-----------|--------------------|------------------------|
| Equation | `FF(x) = ReLU(x·K^T) · V` | `MN(x) = softmax(x·K^T) · V` |
| Coefficients | Unnormalized, non-negative | Normalized (sum to 1) |
| Hidden dimension d_m | Number of memory cells | Number of memory cells |

- **K** ∈ R^{d_m × d} — the **keys** (first weight matrix)
- **V** ∈ R^{d_m × d} — the **values** (second weight matrix)
- **m = ReLU(x·K^T)** — **memory coefficients** (the hidden activation vector)

([Geva et al., 2021](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md))

## Keys Detect Input Patterns

Each key vector k_i corresponds to a specific pattern (or set of patterns) in the input sequence. A 16-layer transformer LM (Baevski & Auli, 2019) trained on WikiText-103 (d=1024, d_m=4096, 247M params) was analysed:

- **Every sampled key** had at least one human-recognizable pattern (avg. 3.6 patterns per key)
- 65–80% of top trigger prefixes matched identified patterns
- **Lower layers (1–9):** dominated by **shallow** patterns (e.g., ending with the same n-gram like "substitutes")
- **Upper layers (10–16):** dominated by **semantic** patterns (e.g., TV show topics, time ranges, part-of relations)

Removing the last token of a trigger prefix reduced memory coefficients significantly in lower layers but had less effect in upper layers, confirming the shift from surface-form to semantic triggers.

([Geva et al., 2021](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md))

## Values Predict Next Tokens

Each value vector v_i can be projected to a vocabulary distribution via `p_i = softmax(v_i · E)` where E is the output embedding matrix:

- **Lower layers (1–10):** agreement between a key's top trigger and its value's top prediction near 0%
- **Upper layers (11–16):** agreement rises to ~3.5% (vs. 0.0004% random baseline)
- 46 of the top-100 most predictive values (highest max probability) had at least one agreeing trigger

Example predictive values: v15_222 predicts "each" (68% precision@50), v16_752 predicts "played" (16%), v15_881 predicts "part" (92%).

([Geva et al., 2021](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md))

## Composition of Memories

### Intra-Layer Composition
- A typical input activates **10–50%** of the 4096 memories per layer
- Active memory count drops around layer 10 (where semantic patterns dominate)
- In **≥68%** of examples, the layer's final top prediction differs from *every* individual memory's prediction — the output is a composition, not a single dominant memory
- When a single memory dominates, it's often for very common stop words or very short prefixes (≤5 tokens)

### Inter-Layer Refinement via Residual Connections
- The residual vector r_ℓ carries information from previous layers (including self-attention)
- The residual's top prediction matches the final model output in ~33% of examples by layers 4–5, rising to >80% by layer 16
- When the residual's prediction changes after the FFN, it rarely switches directly to the FFN's own prediction — instead, a **compromise** (composition) occurs
- Manual analysis of last-layer composition: 66% of changes shift to a semantically distant word, 34% to a related word

([Geva et al., 2021](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md))

## Significance

- Provides a concrete, interpretable mechanism for the role of FFN layers (which account for **two-thirds** of a transformer's parameters)
- Bridges the conceptual gap between feed-forward networks and [[superposition|superposition]] / [[polysemantic-neurons|polysemantic neurons]] — memory cells encode specific patterns and their predictions, but composition produces the observed polysemantic behavior
- Opens practical research directions: automated pattern identification for interpretability, white-box membership inference for data privacy, and architectural innovations guided by understanding suppression during aggregation
- Establishes a bottom-up view of transformer prediction: patterns are detected, composed into layers, then refined across layers via [[residual-connection|residual connections]]

## Cross-Links

- [[transformer|Transformer]] — the architecture whose FFN sub-layers this work analyses
- [[residual-connection|Residual Connection]] — the mechanism for inter-layer prediction refinement
- [[glu-variants|GLU Variants (GEGLU, SwiGLU, ReGLU)]] — alternative FFN formulations that modify the key-value memory architecture
- [[attention-head-pruning|Attention Head Pruning]] — related interpretability work on the other transformer sub-layer (attention)
- [[bert-attention-analysis|BERT Attention Analysis]] — another lens into transformer internals
- [[superposition|Superposition]] — the feature-representation phenomenon that emerges alongside the key-value memory structure
- [[polysemantic-neurons|Polysemantic Neurons]] — individual neurons responding to multiple features, contextualised by the composition mechanism
- [[knowledge-neurons|Knowledge Neurons]] — Dai et al. build on this framework using integrated gradients to identify specific FFN neurons responsible for particular facts
- [[kv-caching|KV Caching]] — inference optimisation also dealing with key-value storage in transformers
