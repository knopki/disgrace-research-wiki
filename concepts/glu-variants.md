---
title: GLU Variants (GEGLU, SwiGLU, ReGLU)
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - architecture
  - technique
sources:
  - "[GLU Variants Improve Transformer](raw/papers/2020-02-shazeer-glu-variants/shazeer2020gluvariants.md)"
confidence: high
---

## Definition

**GLU (Gated Linear Unit)** is a neural network layer introduced by Dauphin et al. (2016) that computes the component-wise product of two linear projections, one of which is passed through a sigmoid: GLU(x) = σ(xW + b) ⊗ (xV + c). Variants replace the sigmoid with other activation functions. **[[noam-shazeer|Noam Shazeer]]** (Google, 2020) proposed applying these variants to the [[transformer|Transformer]] feed-forward sublayer, demonstrating consistent quality improvements over the standard ReLU or GELU activations. The variants are:

| Variant | Gate activation | Formula |
|---------|----------------|---------|
| GLU | Sigmoid | σ(xW) ⊗ (xV) |
| Bilinear | None (linear) | (xW) ⊗ (xV) |
| ReGLU | ReLU | max(0, xW) ⊗ (xV) |
| GEGLU | GELU | GELU(xW) ⊗ (xV) |
| SwiGLU | Swish-1 | Swish₁(xW) ⊗ (xV) |

([Shazeer, 2020](raw/papers/2020-02-shazeer-glu-variants/shazeer2020gluvariants.md))

## Architectural Difference

The standard Transformer FFN has two weight matrices:

> FFN_ReLU(x) = max(xW₁, 0)W₂

The GLU-based FFN replaces the first linear projection and activation with a gated pair, resulting in **three weight matrices** (W, V, W₂):

> FFN_GEGLU(x) = (GELU(xW) ⊗ xV)W₂

To keep the parameter count and computation constant, the hidden dimension d_ff is reduced by a factor of 2/3. In the T5-base setup (d_ff=3072 for 2-matrix FFN), the GLU variants use d_ff=2048. ([Shazeer, 2020](raw/papers/2020-02-shazeer-glu-variants/shazeer2020gluvariants.md))

## Results

### Pre-training Perplexity (C4 span-filling)

| Activation | 65K steps (4-run avg) | 524K steps |
|-----------|----------------------|-----------|
| ReLU (baseline) | 1.997 (σ=0.005) | 1.677 |
| GELU | 1.983 (σ=0.005) | 1.679 |
| Swish | 1.994 (σ=0.003) | 1.683 |
| GLU | 1.982 (σ=0.006) | 1.663 |
| Bilinear | 1.960 (σ=0.005) | 1.648 |
| **GEGLU** | **1.942 (σ=0.004)** | **1.633** |
| **SwiGLU** | 1.944 (σ=0.010) | **1.636** |
| ReGLU | 1.953 (σ=0.003) | 1.645 |

**GEGLU and SwiGLU produce the best perplexities.** On GLUE benchmark, GLU variants dominate, with FFNReGLU achieving the highest average score (84.67 vs baseline 83.80). On SuperGLUE, FFNSwiGLU leads (74.56 vs baseline 72.76). On SQuAD v1.1, GEGLU achieves the best F1 (91.12 vs baseline 90.87). ([Shazeer, 2020](raw/papers/2020-02-shazeer-glu-variants/shazeer2020gluvariants.md))

## Impact

SwiGLU in particular became the default FFN activation in virtually all major post-2022 LLMs:

- **LLaMA / LLaMA 2 / LLaMA 3** (Meta) — SwiGLU in all sizes
- **PaLM / PaLM 2** (Google) — SwiGLU
- **Gemma** (Google) — SwiGLU
- **Mistral / Mixtral** — SwiGLU
- **Qwen / Qwen2** — SwiGLU

GEGLU appears in **T5 v1.1** (Google) and early variants. The widespread adoption makes the GLU-variant FFN the de facto standard architecture for decoder-only Transformer LLMs.

## Limitations

[[noam-shazeer|Shazeer]] explicitly offers no theoretical explanation for why gated variants outperform ReLU/GELU, attributing the success "as all else, to divine benevolence." The three-matrix design increases memory for the FFN weights (by 50% vs 2-matrix at matched d_ff), though the overall parameter count is matched by reducing d_ff.

## Cross-Links

- [[transformer|Transformer]] — the architecture whose FFN sub-layer these variants improve
- [[gelu|GELU]] — the activation used in GEGLU
- [[multi-query-attention|Multi-Query Attention (MQA)]] — another [[noam-shazeer|Shazeer]] contribution to Transformer efficiency
- [[switch-transformer|Switch Transformer]] — Google architecture building on the same T5 codebase
- [[mixture-of-experts|Mixture-of-Experts (MoE)]] — the other major FFN replacement paradigm
