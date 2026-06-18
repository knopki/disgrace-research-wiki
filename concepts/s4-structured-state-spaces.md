---
title: S4 (Structured State Space Sequence Model)
created: 2026-06-18
updated: 2026-06-18
type: concept
tags:
  - model
  - architecture
  - inference
  - technique
sources:
  - "[Efficiently Modeling Long Sequences with Structured State Spaces](raw/papers/2021-11-gu-s4/gu2021s4.md)"
confidence: high
---

# S4 (Structured State Space Sequence Model)

**S4** — the first computationally practical deep State Space Model (SSM), introduced by Gu, Goel & Ré (Stanford, ICLR 2022 Outstanding Paper HM). S4 reparameterises the SSM state matrix A as **Normal Plus Low-Rank (NPLR)**, enabling stable diagonalisation and reducing SSM computation to a well-studied Cauchy kernel. This makes SSMs feasible for the first time and achieves SotA on long-range dependency benchmarks, including solving the Path-X task (length 16,384) that all prior models failed.

S4 is the foundational architecture that directly led to Mamba and the entire SSM line of sequence models.

## The Problem: LSSL's Computational Infeasibility

Prior SSM work (LSSL, Gu et al., NeurIPS 2021) showed that deep SSMs could theoretically handle long-range dependencies (LRDs) when using HiPPO-initialised state matrices. However, the LSSL required O(N²L) computation and O(NL) memory for state dimension N and sequence length L — compared to a lower bound of Ω(L + N) for both. At practical sizes (N=256), the LSSL used orders of magnitude more memory than comparably sized RNNs or CNNs. Attempted fast algorithms were numerically unstable because the HiPPO matrix is highly non-normal: its diagonalisation produces entries exponentially large in N (`([Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md))`).

## The S4 Parameterization (NPLR)

The core insight: the HiPPO matrix A can be decomposed into a **normal** matrix plus a **low-rank** correction (NPLR). This decomposition allows three simultaneous techniques:

1. **NPLR Theorem:** All HiPPO matrices (LegS, LegT, LagT) have NPLR representations with rank r = 1 or r = 2. The primary LegS matrix A = VΛV* - PQ* is unitarily equivalent to diagonal plus low-rank (DPLR) form ([Theorem 1, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).

2. **SSM Generating Function:** Instead of computing the convolution kernel K directly (which requires O(N²L) matrix powers), S4 computes its truncated generating function — evaluating K̂(z) at roots of unity, then recovering K via inverse FFT. This turns matrix powers into a single matrix inverse resolvent problem ([Definition 2, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).

3. **Woodbury Correction + Cauchy Kernel:** The resolvent of a DPLR matrix (Λ - PQ*) is handled via the Woodbury identity, reducing it to operations on the diagonal Λ. Evaluating the resulting expression at M nodes reduces to a **Cauchy kernel** — a well-studied numerical problem with O((M+N) log²(M+N)) stable algorithms via the Fast Multipole Method ([Algorithm 1 / Theorem 3, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).

**Final complexity:** Õ(N + L) computation and O(N + L) memory per layer — essentially optimal for sequence models.

## Architecture

An S4 layer is defined by 5N trainable parameters: diagonal Λ, vectors P, Q, B, C (all in C^N), and step size Δ. Models handle H-dimensional features by stacking H independent S4 copies with a position-wise linear mixing layer — analogous to depthwise-separable convolutions but with global convolution kernels. Total O(H²) + O(HN) parameters per layer, with nonlinear activations between layers.

The deep S4 model is closely related to a depthwise-separable CNN with global convolution kernels, but can also operate in RNN-like recurrent mode for efficient inference.

## Key Results

### Long Range Arena (LRA)
S4 achieves **86.09% average** across all 6 tasks — outperforming every prior model by over 20 points. On Path-X (128×128 pixel connectivity, 16,384-length sequence), S4 scores **96.35%** — the first model to solve it, where all 11 Transformer variants in the benchmark failed (50% random guessing). High-layer filters span the full 16K context, confirming learned LRD capability ([Table 4, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).

| Task | Transformer | Reformer | BigBird | Performer | S4 |
|------|-------------|----------|---------|-----------|----|
| ListOps | 36.37 | 37.27 | 36.05 | 18.01 | **59.60** |
| Text | 64.27 | 56.10 | 64.02 | 65.40 | **86.82** |
| Retrieval | 57.46 | 53.40 | 59.29 | 53.82 | **90.90** |
| Image | 42.44 | 38.07 | 40.83 | 42.77 | **88.65** |
| Pathfinder | 71.40 | 68.50 | 74.87 | 77.05 | **94.20** |
| Path-X | 7 (OOM) | 7 (OOM) | 7 (OOM) | 7 (OOM) | **96.35** |
| **Avg** | 53.66 | 50.56 | 54.17 | 51.18 | **86.09** |

### Raw Speech Classification
On SC10 raw audio (16,000-step sequences), S4 achieves **98.32%** accuracy — halving the error of the best specialised Speech CNN (WaveGAN-D: 96.25%) while using 90× fewer parameters. All RNN and Transformer baselines fail (≥70% error) on raw audio. S4 also adapts to 0.5× sampling frequency without retraining (96.30% accuracy) ([Table 5, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).

### Sequential Image Classification (sCIFAR)
S4 achieves **91.13%** on sequential CIFAR-10 with no 2D inductive bias, no data augmentation, no auxiliary losses — competitive with a **larger ResNet-18** (7.9M vs 11.0M params). With augmentation: 93.16% vs ResNet-18's 95.62%. Unlike other sequence models (25%+ gap to CNN), S4 closes the gap entirely ([Table 6, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).

### Generative Modeling
- **CIFAR-10 density estimation:** 2.85 bits per dim (S4-large) — competitive with Sparse Transformer (2.80), no 2D bias needed ([Table 7, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).
- **WikiText-103 language modeling:** 20.95 perplexity (247M params) — within 0.44 ppl of Transformer baseline (20.51), SotA for attention-free models by over 2 ppl ([Table 8, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).
- **Autoregressive generation:** 60× faster than Transformers on both CIFAR-10 and WikiText-103 by switching to recurrent mode.

### Time-Series Forecasting
S4 beats the specialised **Informer** architecture on 40/50 settings across 5 forecasting tasks, including 37% lower MSE on 30-day weather forecasting ([Table 9, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).

### Ablation: HiPPO is Critical
Controlled ablation on sCIFAR (≤100K params) demonstrates:
- HiPPO-initialised SSMs outperform random initialisation by **15%+ validation accuracy**, even when all methods reach perfect training accuracy
- Random NPLR matrices still perform poorly — the NPLR algorithm enables HiPPO, it doesn't replace it
- With minor regularisation (Dropout 0.1), S4 achieves **84.27%** test accuracy with just 100K parameters ([Fig 3-4, Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).

## Relationship to Other Concepts

- [[mamba|Mamba / SSM]] — S4 is the direct predecessor to Mamba. Gu et al. (2022) follow-up work (S4D) showed that HiPPO-initialised diagonal SSMs work well, enabling the simplified Mamba architecture with selective state spaces and hardware-aware implementation.
- [[transformer|Transformer]] — S4's primary competitor. Transformers still hold an edge on language modeling (+0.44 ppl on WikiText-103) but S4 is 60× faster at generation and far more efficient at long sequences.
- [[sparse-transformer|Sparse Transformer]] — like S4, addresses O(n²) attention cost; S4 uses state compression rather than sparse attention patterns.
- [[longformer|Longformer]] — linear-complexity attention via sliding windows; S4 achieves stronger LRA results with a principled approach.
- [[big-bird|BigBird]] — linear-complexity attention with random+window+global components; S4 outperforms on all LRA tasks.
- [[flash-attention|FlashAttention]] — complementary approach optimising attention IO rather than replacing it; the dominant implementation in practice.
- [[kv-caching|KV Caching]] — S4 eliminates the growing KV cache entirely, replacing O(n) memory with a constant-size state. This is the core advantage inherited by Mamba.
- [[chain-of-continuous-thought|Chain of Continuous Thought]] — both S4 and Coconut explore alternatives to attention for efficient sequential processing.

## Significance and Legacy

S4 was the first SSM architecture to be computationally practical, establishing that principled state-space models can match or exceed Transformers on long-range tasks while being far more efficient. It won ICLR 2022 Outstanding Paper Honorable Mention.

The S4 paper sparked a wave of follow-up work: S4D (diagonal SSMs), S5 (parallel scan SSMs), and ultimately **Mamba** (selective state spaces with hardware-aware scanning), which became the most prominent SSM architecture. Every subsequent SSM model traces its lineage to the NPLR parameterization and algorithmic techniques introduced in S4.

The paper's influence extends beyond SSMs: the NPLR + Woodbury + Cauchy approach to handling structured matrices is a general numerical analysis technique applicable beyond deep learning.
