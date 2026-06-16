---
title: SpargeAttn
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - model
  - architecture
  - optimization
  - inference
sources:
  - "[SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference](raw/papers/2025-02-zhang-spargeattention/zhang2025spargeattn.md)"
  - "[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](raw/papers/2022-05-dao-flashattention/dai2022flashattention.md)"
confidence: high
---

# SpargeAttn

A **universal, training-free sparse attention operator** that accelerates inference across language, image, and video generation models without sacrificing end-to-end metrics. Developed by Jintao Zhang, Chendong Xiang, Haofeng Huang et al. (Tsinghua University / UC Berkeley), published at ICML 2025.

Unlike prior sparse attention methods that rely on fixed task-specific patterns (sliding windows, attention sinks), SpargeAttn predicts sparse regions in the attention map on-the-fly, making it universally applicable. It builds directly on [[flash-attention|FlashAttention]]'s tiled architecture, adding dynamic sparsity prediction within the fused kernel.

## Core Techniques

### Two-Stage Online Filter

**Stage 1 — Selective Token Compression ([Zhang et al., 2025](raw/papers/2025-02-zhang-spargeattention/zhang2025spargeattn.md)):** Each block of Q and K is evaluated for intra-block cosine similarity. Blocks with high similarity ("selective blocks") are compressed to a single mean token. A compressed attention map `P̂` is computed on these reduced sequences, and a `TopCdf` mask identifies which blocks to skip during the [[flash-attention|FlashAttention]] tiled loop. Blocks with low self-similarity ("fix blocks") are always computed — a critical guard against information loss.

**Stage 2 — Sparse Warp Online Softmax:** During the [[flash-attention|FlashAttention]] inner loop, `Sij` is partitioned across GPU warps. When `max(mlocal[Iw] − mij[Iw]) < λ`, all values in `P̃ij[Iw]Vj` are near zero and the computation is skipped — no extra kernel launch, no I/O overhead.

### HilbertCurve Permutation

Visual tokens (video/image) have a 3D spatial structure (T×H×W). SpargeAttn reorders them using the Hilbert Curve before attention, which maximises adjacency similarity in 1D sequence without requiring row/column boundaries. This increases block self-similarity and thus sparsity during the Stage 1 prediction.

### Self-Similarity Judge

A guarding mechanism: any Q or K block falling below the self-similarity threshold θ is marked as "fix block" and exempted from sparse skipping. Ablation shows this prevents extreme precision loss in difficult cases (e.g., randomly permuted visual tokens).

### Integration with SageAttention

SpargeAttn is implemented on top of SageAttention's 8-bit quantized attention framework — quantization and sparsity are orthogonal, so both can be applied simultaneously. An updated implementation (SpargeAttn on SageAttention2) offers an additional ~30% speedup.

## Hyper-Parameter Determination

Three hyper-parameters control the method per attention layer:

- `τ ∈ (0, 1)` — fraction of cumulative attention mass to retain (TopCdf)
- `θ ∈ (-1, 1)` — minimum block self-similarity for selective compression
- `λ < 0` — online softmax skip threshold

These are found via a two-step grid search: first find (τ, θ) that maximise sparsity with relative L1 error < l1, then find λ with L1 < l2. The search uses 5 sample inputs per model. The resulting hyper-parameters are then fixed for all inference runs.

## Results

| Model | Seq len | Sparsity | Speedup over Full | Key metric |
|-------|---------|----------|-------------------|------------|
| Llama3.1 (8B) | 128K | 54% | 4.5× (708 vs 157 1/t) | Ppl 6.020 vs 6.013 |
| Llama3.1 (8B) | 24K | 36% | 2.8× (444 vs 157 TOPS) | NIAH 0.863 vs 0.838 |
| CogVideoX (2B) | 17K | 46% | 3.1× | CLIPSIM ±0.002 |
| Mochi | 22K | 47% | 3.5× | FScore 5.03 vs 5.34 |
| Flux.1-dev | 4.5K | 38% | 1.8× | FID 164 vs 166 |
| SD3.5 Large | 4.5K | 31% | 1.8× | FID 166.2 vs 166.1 |
| Open-Sora-Plan | 38K | 34% | 1.6× latency | CLIPSIM 0.169 vs 0.165 |

Sparsity scales with sequence length: from 6.8% at 8K to 54% at 128K on Llama3.1. Prediction overhead is under 4% at 8K and drops below 1% at 32K+.

## Relationship to Other Sparse Attention Methods

SpargeAttn differs from [[sparse-transformer|Sparse Transformer]] (OpenAI, 2019), [[longformer|Longformer]] (Beltagy et al., 2020), and [[big-bird|BigBird]] (Zaheer et al., 2020) in a fundamental way: those methods prescribe **fixed sparse patterns** at the architecture level, trading off model capacity for longer sequences. SpargeAttn is a **post-hoc inference accelerator** — it operates on any pretrained model without retraining and predicts sparsity dynamically per input.

This makes SpargeAttn more similar to [[kv-caching|KV Caching]] in spirit: an inference optimisation that exploits existing structure rather than changing the model. While KV caching eliminates redundant re-computation of key/value states across decoding steps, SpargeAttn skips computations within a single attention pass by predicting near-zero entries.

Related dynamic sparse attention baselines compared in the paper: MInference, FlexPrefill, SparQAttn, LokiAttn, SeerAttention. SpargeAttn consistently outperforms them in both speed and metric retention across all tested models.

## Limitations

- Requires a per-layer, per-model hyper-parameter search (5 inputs, grid search), though this is a one-time cost
- Sparsity varies significantly across layers and heads (from 9% to 60% on CogVideoX), requiring per-layer hyper-parameter tuning
- The method still computes full Q/K/V — sparse prediction happens within the inner loop, so it cannot benefit I/O-bound scenarios where full attention is already bottlenecked elsewhere
- Diffution model sparsity increases with denoising timestep — early timesteps benefit less
