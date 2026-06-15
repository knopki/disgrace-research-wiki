---
title: Sparse Transformer
created: 2026-06-15
updated: 2026-06-15
type: concept
tags:
  - model
  - architecture
  - optimization
sources:
  - "[Generating Long Sequences with Sparse Transformers](raw/papers/2019-04-child-sparse-transformer/child2019sparse.md)"
confidence: high
---

# Sparse Transformer

A neural architecture introduced by **Rewon Child, Scott Gray, Alec Radford, and Ilya Sutskever** (OpenAI, 2019) that replaces the quadratic self-attention matrix with **sparse factorized attention patterns**, reducing complexity to **O(n√n)**. The same architecture models text, images, and audio from raw bytes. Self-attention was demonstrated on sequences up to 1M+ tokens, though with heavily reduced capacity (3M params) and degraded quality at that extreme.

## Attention Sparsity: The Core Idea

Standard [[transformer|Transformer]] self-attention computes relevance scores between every pair of positions — O(n²) time and memory. The Sparse Transformer observes that learned attention patterns are naturally sparse (Figure 2 of the paper shows 128-layer CIFAR-10 patterns where deep layers use only local or structured access). Instead of learning which positions to attend to, the architecture **prescribes two complementary sparse patterns** per layer, guaranteeing global connectivity across just two attention steps.

### Strided Attention (periodic data: images, music)

- **Head 1:** local window of `l` previous positions (≈ √n)
- **Head 2:** attends to every `l`-th position

Useful for data with periodic structure — an image pixel needs nearby context (local window) plus periodically sampled distant pixels (stride).

### Fixed Attention (non-periodic data: text)

- **Head 1:** attend within the same block of `l` positions
- **Head 2:** attend to a fixed suffix of each preceding block

Designed for text where no natural periodicity exists.

### Connectivity Guarantee

Any input position can reach any output position within **p+1 = 3 attention steps** (the "valid connectivity" property). This ensures information can flow across the entire sequence even though each individual attention head is sparse.

## Architecture Innovations Beyond Sparsity

### Deep Transformer Scaling

- **Pre-activation residual blocks** (He et al., 2016) with layer norm before attention/FFN
- **Initialization:** W₂ (FFN output) and Wₚ (post-attention projection) scaled by **1/√(2N)** where N is depth — keeps the ratio of input embedding scale to residual block scale invariant
- No auxiliary losses needed, unlike prior deep transformer attempts

### Gradient Checkpointing for Attention

During the backward pass, attention weights and feedforward activations are **recomputed** rather than stored. The paper applies gradient checkpointing (Chen et al., 2016) to self-attention layers specifically, noting the technique is particularly effective when processing long sequences. This enabled dense-attention training on sequences of length 16,384 with hundreds of layers.

### Block-Sparse Attention Kernels

Custom fused softmax kernels compute attention on sliced Q/K/V blocks, skipping the upper triangle (autoregressive mask) to halve operations.

## Results

### CIFAR-10 (bits/dim, sequence length 3072)

| Model | Bits/dim |
|-------|----------|
| PixelCNN | 3.03 |
| PixelCNN++ | 2.92 |
| Image Transformer | 2.90 |
| PixelSNAIL | 2.85 |
| **Sparse Transformer 59M (strided)** | **2.80** |

### Enwik8 (bits/byte, sequence length 12,288)

| Model | Bits/byte | Params |
|-------|-----------|--------|
| Deeper Self-Attention (Al-Rfou et al.) | 1.06 | — |
| Transformer-XL | 1.03 | 88M |
| Transformer-XL | 0.99 | 277M |
| **Sparse Transformer (fixed)** | **0.99** | **95M** |

Sparse Transformer matches the best Transformer-XL with one-third the parameters. Strided attention failed on text; fixed patterns with merged heads succeeded. Longer context consistently improved performance (Table 3: 0.9952 at 6K → 0.9908 at 12K tokens).

### ImageNet-64 (bits/dim, sequence length 12,288)

| Model | Bits/dim |
|-------|----------|
| PixelCNN | 3.57 |
| Parallel Multiscale | 3.70 |
| Glow | 3.81 |
| SPN 150M | 3.52 |
| **Sparse Transformer 152M (strided)** | **3.44** |

Replaced prior SOTA (SPN 150M at 3.52 bits/dim), demonstrating self-attention can scale to full-resolution images from raw bytes.

### Classical Audio — Scalability Study (µ-law 12kHz)

| Sequence length | Params | Bits/byte |
|----------------|--------|-----------|
| 65,536 | 152M | 1.97 |
| 262,144 | 25M | 2.17 |
| 1,048,576 | 3M | 2.99 |

Increasing sequence length by 4× required roughly 8× reduction in model capacity (derived from O(n√n) attention scaling: n×4 → params/8). At 1M+ tokens, the model had only 3M params and quality degraded significantly — proving self-attention can function at that scale, but not without tradeoffs.

### Key Finding

Sparse patterns **converged to lower error than dense attention** while running faster (Table 2), suggesting the predetermined sparsity provides a useful inductive bias or that full attention has an underlying optimization issue.

## Significance & Legacy

- **First demonstration of self-attention at 1M+ tokens**, though with heavily reduced capacity (3M params) and significant quality degradation — proved feasibility, not practicality
- Showed sparse patterns **outperform dense attention** (lower error, faster convergence), suggesting a beneficial inductive bias rather than a compromise
- Established **two sparse attention archetypes** — strided (periodic) and fixed (non-periodic) — that directly informed later architectures: Longformer (sliding window + global), BigBird (random + window + global), and Sparse Sinkhorn
- Showed the **same architecture processes text, images, and audio from raw bytes**, reinforcing the Transformer's universality
- Gradient checkpointing for attention became a standard memory-saving technique in production training

## Relationship to Other Concepts

- **[[transformer|Transformer]]** — the base architecture that Sparse Transformer modifies by introducing sparse attention factorizations
- **[[kv-caching|KV Caching]]** — a complementary inference-time optimisation; sparse attention reduces per-step compute (O(√n) per position), KV caching avoids recomputation across steps. Both can be combined
- **[[positional-encoding|Positional Encoding]]** — Sparse Transformer uses learned positional embeddings (data-dim for images, attention-dim for text), differing from sinusoidal encodings
- **[[residual-connection|Residual Connection]]** — pre-activation residual blocks are the architectural backbone enabling 128+ layer stacks
- **[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]]** — both address transformer efficiency limits: Sparse Transformer via attention sparsity, Coconut via latent-space reasoning that sidesteps token-by-token generation