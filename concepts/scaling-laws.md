---
title: Scaling Laws (Neural Language Models)
created: 2026-06-16
updated: 2026-06-16
raw_ingested: true
type: concept
tags:
  - scaling-law
  - training
  - model
  - methodology
sources:
  - "[Scaling Laws for Neural Language Models](raw/papers/2020-01-kaplan-scaling-laws/kaplan2020scaling.md)"
  - "[Training Compute-Optimal Large Language Models](raw/papers/2022-03-hoffmann-chinchilla/hoffmann2022chinchilla.md)"
confidence: high
---

# Scaling Laws (Neural Language Models)

Empirical power-law relationships between [[transformer|Transformer]] language model performance and three scale factors: model size (N), dataset size (D), and training compute (C). First formalized by Kaplan et al. at OpenAI in January 2020 ([Kaplan et al., 2020](raw/papers/2020-01-kaplan-scaling-laws/kaplan2020scaling.md)).

## Core Equations

The cross-entropy loss L follows smooth power laws spanning 7+ orders of magnitude:

**Loss vs. model size** (large dataset, converged):

- L(N) = (N_c / N)^α_N, where α_N ≈ 0.076, N_c ≈ 8.8 × 10^13

**Loss vs. dataset size** (large model, early-stopped):

- L(D) = (D_c / D)^α_D, where α_D ≈ 0.095, D_c ≈ 5.4 × 10^13

**Combined dependence** (overfitting model):

- L(N, D) = [(N_c / N)^(α_N/α_D) + D_c / D]^α_D

**Loss vs. compute** (optimal allocation):

- L(C_min) = (C_c^min / C_min)^(α_C^min), where α_C^min ≈ 0.050, C_c^min ≈ 3.1 × 10^8 PF-days

**Training curve** (infinite data):

| L(N, S) = (N_c / N)^α_N + (S_c / S_min(S))^α_S, where α_S ≈ 0.76, S_c ≈ 2.1 × 10^3

**Critical batch size**:

- B_crit(L) = B_*/L^(1/α_B), where α_B ≈ 0.21, B_* ≈ 2 × 10^8 tokens

## GPT-3 Validation

GPT-3 (175B) confirmed the Kaplan scaling trends extend smoothly for two more orders of magnitude. Training curves for 8 model sizes (125M to 175B) showed validation loss following a power-law with only slight departure from the predicted curve ([Brown et al., 2020](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)).

**Fig 3.1 of the GPT-3 paper** shows cross-entropy validation loss vs training compute following the power-law trend from Kaplan et al. across the full range from 100K to 175B parameters. The GPT-3 175B point aligns closely with the extrapolated curve, confirming the scaling law holds at unprecedented model sizes. This was the largest empirical validation of the Kaplan scaling laws before Chinchilla's refinement.

## Chinchilla Scaling Laws

Refined by [[deepmind|Hoffmann et al. at DeepMind]] (2022) — the "Chinchilla scaling laws" — which found that most existing LLMs (including GPT-3) were undertrained, and that model size and training data should scale in equal proportion ([Hoffmann et al., 2022](raw/papers/2022-03-hoffmann-chinchilla/hoffmann2022chinchilla.md)).

### Core Result: N ∝ D

Three independent approaches converged on the same compute-optimal allocation:

1. **Fixed parameter count:** Train models of varying sizes with different numbers of tokens, fit a parametric loss function L(N, D) and minimize under a compute budget C
2. **Fixed FLOPs:** Train models of varying shapes but identical total FLOPs, find the best loss
3. **Large model on reduced data:** Train a very large model on varying fractions of data, extrapolate the trend

All three methods agree: for compute-optimal training, model size N and dataset size D should be scaled in equal proportion — doubling N requires doubling D. The optimal parameter count for a given compute budget C follows:

- N_opt(C) ∝ C^a, D_opt(C) ∝ C^b, where a ≈ b ≈ 0.50

This directly contradicts the Kaplan finding that N ∝ C^0.73 (favoring larger models with less data).

### Key Equations

**Parametric loss fit:**

- L(N, D) = E + A/N^α + B/D^β

Where E = 1.69 (irreducible loss), A = 406.4, B = 410.7, α ≈ 0.34, β ≈ 0.28.

**Optimal allocation:**

- N_opt ≈ (C/6)^0.5, D_opt ≈ (C/6)^0.5

### Chinchilla Model

The prediction was validated by training **Chinchilla** — a 70B-parameter transformer on 1.4 trillion tokens:

| Model | Parameters | Training Tokens | Compute Budget |
|-------|-----------|----------------|----------------|
| Gopher | 280B | 300B | ~ same FLOPs |
| GPT-3 | 175B | 300B | — |
| Chinchilla | **70B** | **1.4T** | same as Gopher |

Chinchilla outperformed Gopher on every evaluated task despite 4x fewer parameters, achieving:

- **MMLU:** 67.5% (vs Gopher 60.0%, +7.5%)
- Superior performance on: LAMBADA, RACE-h, Math, Wikipedia perplexity, BIG-bench tasks
- Substantially cheaper inference and fine-tuning due to smaller model size

### Implication

The Chinchilla scaling laws shifted the industry consensus from "bigger models with moderate data" (Kaplan) to "balanced scaling of model and data." Following Chinchilla, subsequent models (LLaMA, GPT-4, DeepSeek) adopted data-rich training regimes, often training smaller models on 2T+ tokens.

## Key Findings

### Performance depends on scale, not shape

Model performance depends strongly on three scale factors (N, D, C) but very weakly on architectural hyperparameters. Aspect ratio (d_model / n_layer) can vary 40x with only ~3% loss difference. Feed-forward ratio and attention head count similarly have minimal effect.

### Non-embedding parameters are the right metric

Including embedding parameters in the count obscures the scaling trend. Embeddings can be shrunk without performance loss. The cleanest power-law uses N = non-embedding parameters only: N ≈ 12 n_layer d_model^2.

### Overfitting follows a simple ratio

The overfitting penalty depends only on the ratio N^0.74 / D, meaning every 8x increase in model size requires only ~5x more data to avoid a penalty. The rule to stay within 0.02 nats of converged loss: D ≳ (5 × 10^3) × N^0.74.

### Large models are more sample-efficient

Larger models reach a fixed loss target with fewer optimization steps and fewer tokens processed. This is not a small effect — sample efficiency improves by a factor of almost 100x when comparing the smallest to the largest model studied.

### Transfer follows in-distribution performance with constant offset

When evaluating on different text distributions (Books, Wikipedia, Common Crawl), the loss improves smoothly with model size, maintaining a roughly constant offset from the WebText2 training distribution. Generalization depends only on in-distribution validation loss, not training duration or depth.

### Transformers outperform LSTMs on long-range dependencies

[[lstm|LSTMs]] match Transformers on early tokens in context but plateau, while Transformers continue improving through the full 1024-token context. Larger Transformers are more efficient at detecting patterns with less contextual information.

### Convergence is inefficient — train big, stop early

Compute-optimal training allocates the budget predominantly to larger model size (N ∝ C_min^0.73), with batch size scaling via B_crit (B ∝ C_min^0.24) and negligible increase in serial steps (S_min ∝ C_min^0.03). Models should be trained to ~10% above converged loss, not to convergence. This yields 65% less compute for the same loss compared to training to 2% of convergence.

### Critical batch size depends only on loss, not model size

B_crit approximately doubles for every 13% decrease in loss. It is independent of model size and predicted by the gradient noise scale.

## Predicted Breakdown Point

The compute-efficient and data-limited scaling laws contradict each other at very large scales, yielding a predicted intersection at C* ~ 10^4 PF-days, N* ~ 10^12 parameters, D* ~ 10^12 tokens, L* ~ 1.7 nats/token. Kaplan et al. conjecture this intersection estimates the entropy-per-token of natural language — the point where all reliable information in language data has been extracted.

## Historical Impact

These scaling laws were the first comprehensive empirical framework for predicting LLM performance as a function of scale. Key influence:

- Justified the training of extremely large models (GPT-3, 175B parameters) on relatively modest data
- Later contradicted by Hoffmann et al. (2022) — the "Chinchilla scaling laws" — which showed Kaplan et al. overestimated optimal model size for a given compute budget, underestimating optimal data requirements by ~2x
- Both sets of laws coexist: Kaplan explains the loss-vs-scale relationship for fixed models, Chinchilla corrects the compute-optimal allocation guidance, and later work (DeepSeek, LLaMA) largely follow the Chinchilla regime

## Notation

| Symbol | Meaning |
|--------|---------|
| L | Cross-entropy loss (nats) |
| N | Non-embedding parameters |
| C ≈ 6NBS | Total non-embedding compute (PF-days) |
| D | Dataset size (tokens) |
| B_crit | Critical batch size |
| C_min | Minimum compute to reach L (batch << B_crit) |
| S_min | Minimum steps to reach L (batch >> B_crit) |
| α_X | Power-law exponent for L(X) ∝ 1/X^α_X |

## Caveats ([Kaplan et al., 2020](raw/papers/2020-01-kaplan-scaling-laws/kaplan2020scaling.md), Appendix C)

- No solid theoretical understanding for the scaling laws, especially with respect to D at large model size
- B_crit predictions unverified outside explored loss range
- Fits break down for very small datasets (epoch < 40 steps)
- Regularization (dropout, augmentation) not systematically explored
- Compute estimate C ≈ 6NBS ignores context-length-dependent terms (relevant when n_ctx > 12 d_model)
- Learning rate tuning not exhaustive — initialization scale and momentum not systematically varied

## Related

- [[transformer|Transformer]] — architecture these laws were discovered for
- [[lstm|LSTM]] — recurrent baseline that Transformers asymptotically outperform on long-range dependencies
- [[kv-caching|KV Caching]] — inference optimization whose relevance grows with model scale
- [[sparse-transformer|Sparse Transformer]] — cited by Kaplan et al. as enabling large model parallelism
- [[switch-transformer|Switch Transformer]] — demonstrates a distinct scaling dimension (number of experts) orthogonal to N-D-C; expert count provides quality gains beyond model depth/width scaling
- [[instruction-tuning|Instruction Tuning]] — technique whose benefits emerge only at sufficient scale (≥68B parameters), confirming and extending the scaling-law framework; models below 8B are harmed by instruction tuning
- [[chain-of-thought|Chain-of-Thought Prompting]] — another emergent ability of model scale; improves multi-step reasoning only at ~100B+ parameters, with flat or negative impact below the threshold
- [[dario-amodei|Dario Amodei]] — senior author of the paper; provided guidance throughout the project
