---
title: KV Caching
created: 2026-06-17
updated: 2026-06-15
type: concept
tags: [inference, optimization, architecture]
sources:
  - "[Transformers KV Caching Explained](raw/articles/kv-caching-explained/index.md)"
confidence: high
---

# KV Caching

An inference optimization technique for generative transformers that caches the **Key (K)** and **Value (V)** attention states from previous tokens, avoiding redundant recomputation during auto-regressive generation.

## The Problem

During auto-regressive generation, a decoder-only model (like GPT) predicts one token at a time, appending each new token to the input sequence for the next forward pass. Without KV caching, every generation step recomputes the attention for all tokens in the sequence from scratch — including the Key and Value vectors for tokens that have already been processed and will not change.

For a sequence of length \(n\), this means each new token triggers \(O(n^2)\) attention computation even though only the newest token contributes new information. The computational cost grows quadratically with sequence length.

The auto-regressive generation loop:

1. Given input tokens, the model predicts one token at a time
2. That token is appended to the input
3. The model runs again to predict the next token
4. Repeat

This is illustrated in the GPT-2 generation example in the source article: each step feeds the entire sequence through the model, recalculating the same previous-token attention values.

## The Solution

KV caching stores the Key and Value matrices from previous tokens after their initial computation. When a new token arrives, the model only needs to:

1. Compute the Query, Key, and Value for the **new token** only
2. Retrieve the cached K and V from all previous tokens
3. Compute attention using the new Q against the combined (cached K + new K, cached V + new V)

The attention matrices become significantly smaller because only the new token's Query dimension participates, while the cached K and V are already materialised. This replaces \(O(n^2)\) per-step computation with \(O(n)\) — a linear rather than quadratic cost per token.

The step-by-step attention computation in the decoder: at each step, without cache, the full attention matrix for all tokens must be recomputed. With cache, only the new token's contributions are computed and the prior ones are read from memory.

## Performance Impact

Empirical results from the source, measured on GPT-2 with a Tesla T4 GPU generating 1000 new tokens:

| Configuration | Mean time | Std dev |
|---|---|---|
| With KV caching | 11.885 s | ±0.272 s |
| Without KV caching | 56.197 s | ±0.272 s |

KV caching yields approximately **4.7× speedup** for 1000-token generation. The memory overhead is described as "neglectable" for typical use cases, as the cached K and V values are compact relative to model weights.

## Constraints

- **Only applies to decoder or decoder-only models** (GPT, LLaMA, Claude, etc.). Encoder-only models like BERT process the full sequence in one pass and are not generative.
- **Requires additional GPU/CPU memory** to store the cached states. The cache grows linearly with sequence length.
- **The causal mask is still applied** — the decoder retains its auto-regressive property, with each token only attending to its predecessors.

## Relationship to Other Concepts

- **[[transformer|Transformer]]** — KV caching is a property of the decoder-side self-attention mechanism; it does not apply to encoder self-attention or cross-attention in the same way.
- **[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]]** — a training paradigm that treats reasoning as a continuous latent loop, sidestepping KV-cache-induced rigidity by never committing to discrete tokens during reasoning.
- **[[semantic-superposition|Semantic Superposition]]** — the KV Cache is the mechanism that makes semantic collapse irreversible: once a reasoning path is chosen and its tokens are generated, the cached K and V cement that trajectory, making it costly to backtrack. The cache also serves as a "stabilizer of structured thought" in superposition prompting by encoding the direction of investigation.
- **[[positional-encoding|Positional Encoding]]** — positional information is embedded in the cached K and V representations, so the cache preserves each token's position-sensitive vector context.
- **[[residual-connection|Residual Connection]]** — the cached K and V states come from specific attention layers, and the residual stream carries information up through the network independently of the cache.
- **[[sparse-transformer|Sparse Transformer]]** — orthogonal efficiency approach: KV caching avoids recomputation across inference steps, sparse attention reduces per-step complexity. Can be combined.
