---
title: Gaussian Error Linear Unit (GELU)
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - architecture
  - technique
sources:
  - "[Gaussian Error Linear Units (GELUs)](raw/papers/2016-06-hendrycks-gelu/hendrycks2016gelu.md)"
confidence: high
---

## Definition

The **Gaussian Error Linear Unit (GELU)** is a neural network activation function introduced by Dan Hendrycks and Kevin Gimpel in their 2016 paper "Gaussian Error Linear Units (GELUs)" ([Hendrycks & Gimpel, 2016](raw/papers/2016-06-hendrycks-gelu/hendrycks2016gelu.md)). It is defined as `GELU(x) = xΦ(x)`, where `Φ(x)` is the cumulative distribution function (CDF) of the standard normal distribution `N(0,1)`.

The key insight: GELU weights inputs by their *value relative to other inputs*, rather than gating them by *sign* (as ReLU does) or applying a fixed curvature (as ELU does). Inputs with large positive values are more confidently retained; inputs with large negative values are confidently zeroed; values near zero get a smooth probabilistic transition.

## Formulation

**Exact form:**
```
GELU(x) = x · ½[1 + erf(x/√2)]
```

**Common approximations (for faster computation on GPU/CPU):**
```
GELU(x) ≈ 0.5x (1 + tanh[ √(2/π) (x + 0.044715x³) ])
GELU(x) ≈ xσ(1.702x)                      [σ = sigmoid]
```

The tanh-based approximation is the most widely used in practice. ([Hendrycks & Gimpel, 2016](raw/papers/2016-06-hendrycks-gelu/hendrycks2016gelu.md))

## Interpretation as Stochastic Regularizer

GELU has a probabilistic origin: it is the expectation of a stochastic regularizer that applies a Bernoulli mask `m ∼ Bernoulli(Φ(x))`:

```
GELU(x) = E[m · x + (1-m) · 0] = Φ(x) · x + (1-Φ(x)) · 0 = xΦ(x)
```

This combines properties of **dropout** (stochastic zeroing) and **zoneout** (stochastic identity) into an input-dependent gating mechanism, without introducing new hyperparameters (the Gaussian parameters are fixed at µ=0, σ=1). ([Hendrycks & Gimpel, 2016](raw/papers/2016-06-hendrycks-gelu/hendrycks2016gelu.md))

## Properties

- **Non-convex, non-monotonic** — the function dips below zero for small negative values, then increases, unlike ReLU which is monotonic
- **Non-zero curvature everywhere** — unlike ReLU (zero curvature for x>0) and ELU (zero curvature for large x), GELU bends at all points, enabling it to approximate more complex functions with fewer units
- **Smooth ReLU interpolation** — as `σ → 0`, GELU approaches ReLU; with the standard fixed σ=1, it provides a smooth transition around zero
- **No new hyperparameters** — the Gaussian parameters are fixed, unlike parametric activations (PReLU, ELU with learnable α)

## Experimental Performance

Across all evaluated tasks, GELU consistently outperformed both ReLU and ELU ([Hendrycks & Gimpel, 2016](raw/papers/2016-06-hendrycks-gelu/hendrycks2016gelu.md)):

| Task | GELU error | ReLU error | ELU error |
|------|-----------|-----------|-----------|
| Twitter POS Tagging | **12.57%** | 12.67% | 12.91% |
| TIMIT Frame Recognition | **29.3%** | 29.5% | 29.6% |
| CIFAR-10 (9-layer CNN) | **7.89%** | 8.16% | 8.41% |
| CIFAR-100 (Wide ResNet 40-4) | **20.74%** | 21.77% | 22.98% |

GELU also demonstrated better robustness to input noise than both ReLU and ELU.

## Relation to SiLU / Swish

The same paper introduced and named the **Sigmoid Linear Unit (SiLU)**, defined as `xσ(x)`, which uses the logistic distribution CDF instead of the Gaussian CDF. In 2017, Google Brain independently proposed the same function as "swish" and later added a learnable `β` parameter (`xσ(βx)`). After community discussion, TensorFlow and PyTorch adopted the name SiLU with attribution to this paper. GELU is strictly more performant than SiLU but is also more expensive to compute (requires `erf` or its approximation). ([Hendrycks & Gimpel, 2016](raw/papers/2016-06-hendrycks-gelu/hendrycks2016gelu.md))

## Legacy and Adoption

GELU became the default activation function in:

- **[[bert|BERT]]** — both BERT-Base and BERT-Large use GELU in their feed-forward networks (line 29 of bert.md)
- **GPT series** — all GPT models (GPT-1, GPT-2, GPT-3/4) use GELU
- Virtually all subsequent [[transformer|Transformer]]-based language models adopted GELU as the feed-forward activation

The GELU activation's smooth gradient flow was instrumental in enabling stable training of deep Transformer stacks, complementing other architectural innovations like [[residual-connection|residual connections]] and layer normalization.

## Cross-Links

- [[bert|BERT]] — the first major model to standardize GELU as its activation function
- [[transformer|Transformer]] — the architecture whose feed-forward networks GELU was adopted into
- [[residual-connection|Residual Connection]] — complementary architectural component for stable training of deep models
- [[backpropagation|Backpropagation]] — the training algorithm whose gradient flow benefits from GELU's smooth curvature
- [[glu-variants|GLU Variants (GEGLU, SwiGLU, ReGLU)]] — GEGLU uses GELU as the gate activation in a gated FFN variant
