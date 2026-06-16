---
source_url: https://arxiv.org/abs/2502.18137
ingested: 2026-06-17
date: 2025-02-01
title: "SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference"
authors:
  - Jintao Zhang
  - Chendong Xiang
  - Haofeng Huang
  - Jia Wei
  - Haocheng Xi
  - Jun Zhu
  - Jianfei Chen
---

# SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference

Full text: [[2502.18137.pdf]] (6 pages)

## Abstract

> An efficient attention implementation is essential for large models due to its quadratic time complexity. Fortunately, attention commonly exhibits sparsity, i.e., many values in the attention map are near zero, allowing for the omission of corresponding computations. Many studies have utilized the sparse pattern to accelerate attention. However, most existing works focus on optimizing attention within specific models by exploiting certain sparse patterns of the attention map. A universal sparse attention that guarantees both the speedup and end-to-end performance of diverse models remains elusive. In this paper, we propose SpargeAttn, a universal sparse and quantized attention for any model. Our method uses a two-stage online filter: in the first stage, we rapidly and accurately predict the attention map, enabling the skip of some matrix multiplications in attention. In the second stage, we design an online softmax-aware filter that incurs no extra overhead and further skips some matrix multiplications. Experiments show that our method significantly accelerates diverse models, including language, image, and video generation, without sacrificing end-to-end metrics.

## Key Facts

- **Authors:** Jintao Zhang\*, Chendong Xiang\*, Haofeng Huang\*, Jia Wei, Haocheng Xi, Jun Zhu, Jianfei Chen (\*=equal contribution)
- **Affiliations:** Tsinghua University (Dept. of Comp. Sci. and Tech., Institute for AI, BNRist Center, THBI Lab, Tsinghua-Bosch Joint ML Center); Institute for Interdisciplinary Information Sciences, Tsinghua University; UC Berkeley (EECS)
- **Venue:** ICML 2025 (Proceedings of the 42nd International Conference on Machine Learning, Vancouver, Canada. PMLR 267, 2025)
- **Submitted:** Feb 24, 2025 (v8: Nov 19, 2025)
- **Code:** https://github.com/thu-ml/SpargeAttn
- **Pages:** 6 (main) + appendix (~19 total rendered)

## Method Overview

SpargeAttn builds on FlashAttention tiling and SageAttention (8-bit quantization). It uses three core techniques:

1. **Selective Token Compression (Stage 1):** Compresses only blocks with high intra-block cosine similarity into a single token, computes a compressed attention map `P̂`, and uses TopCdf to select which block computations to skip. Blocks with low self-similarity ("fix blocks") are always computed to prevent information loss.

2. **Sparse Warp Online Softmax (Stage 2):** During the FlashAttention inner loop, partitions `Sij` across GPU warps. If `max(mlocal[Iw] - mij[Iw]) < λ`, all values in `P̃ij[Iw]Vj` ≈ 0 and the computation is skipped.

3. **HilbertCurve Permutation (visual tokens):** Reorders 3D visual tokens along a Hilbert curve to increase adjacency similarity, improving block self-similarity and sparsity.

### Hyperparameters

- `τ ∈ (0, 1)` — TopCdf cumulative threshold for sparse mask
- `θ ∈ (-1, 1)` — Self-similarity threshold
- `λ < 0` — Online softmax skip threshold

Grid-searched with L1 error bounds: first find (τ, θ) maximizing sparsity with L1 < l1, then λ with L1 < l2.

## Results

| Model (seq len) | Sparsity | Speed (1/t) | Metric retention |
|---|---|---|---|
| Llama3.1 8B (128K) | 54% | 708.1 (vs 156.9 full) | Ppl 6.020 (vs 6.013), NIAH 0.909 (vs 0.907) |
| CogVideoX (17K) | 46% | 507.9 (vs 166.0 full) | CLIPSIM 0.1798 (vs 0.1819) |
| Mochi (22K) | 47% | 582.4 (vs 164.2 full) | FScore 1.807 (vs 1.681) |
| Flux (4.5K) | 38% | 280.3 (vs 158.2 full) | FID 163.98 (vs 166.10) |
| SD3.5 (4.5K) | 31% | 293.0 (vs 164.2 full) | FID 166.19 (vs 166.10) |

**End-to-end speedup:** 1.83x on Mochi (L40 GPU), Llama3.1 128K from 52s → 29.98s.

**Prediction overhead:** 3.78% at 8K, dropping to 0.516% at 128K.

**Sparsity scales with sequence length:** 6.8% at 8K → 54% at 128K on Llama3.1.

## Relationships

- Builds on [[SageAttention]] (8-bit quantized attention by same group)
- Compares against MInference and FlexPrefill (dynamic sparse attention baselines)
- Related to pattern-based sparse attention (StreamingLLM, H2O, DUOAttention), dynamic sparse attention (SparQAttn, LokiAttn, SeerAttention), and training-based sparse attention (Reformer, FastAttention)
- Orthogonal to kernel optimizations (FlashAttention 1/2/3), other quantization methods, and linear attention
