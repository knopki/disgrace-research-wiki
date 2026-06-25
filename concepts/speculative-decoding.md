---
title: Speculative Decoding
created: 2026-06-25
updated: 2026-06-25
type: concept
tags:
  - inference
  - technique
sources:
  - "[Fast Inference from Transformers via Speculative Decoding](raw/papers/2022-11-leviathan-speculative-decoding/laviathan2022speculativedecoding.md)"
---
# Speculative Decoding

An inference acceleration technique for autoregressive models that generates multiple tokens per serial model invocation by using a fast approximation model to speculate candidate tokens and a target model to verify them in parallel, while guaranteeing identical output distribution. Introduced by Leviathan, Kalman & Matias (Google Research, ICML 2023).

## Mechanism

Speculative decoding (Algorithm 1 in the paper) operates in three phases per iteration:

1. **Draft:** Run the approximation model $M_q$ (smaller/faster) autoregressively for $\gamma$ steps to produce candidate tokens $x_1, \ldots, x_\gamma$.
2. **Verify:** Run the target model $M_p$ once on each prefix $[x_1], [x_1, x_2], \ldots, [x_1, \ldots, x_\gamma]$ — all $\gamma+1$ calls are **batched into a single parallel computation**, exploiting the fact that Transformer inference is often memory-bandwidth bound, not compute bound.
3. **Accept/Reject:** For each candidate $x_i$, accept it if $p(x_i) \ge q(x_i)$; otherwise reject with probability $1 - p(x_i)/q(x_i)$ where $p, q$ are the target and approximation model distributions. If a token is rejected, sample a replacement from the adjusted distribution $p'(x) = \text{norm}(\max(0, p(x) - q(x)))$.

Each iteration produces at least 1 token (never worse than standard autoregressive decoding) and up to $\gamma+1$ tokens when all candidates are accepted.

## Key Properties

- **Lossless:** The output distribution is proven identical to sampling from $M_p$ alone (Appendix A.1).
- **No retraining required:** Works with off-the-shelf models — any model combination, same architecture or different.
- **No architecture changes:** Standard Transformer inference — no custom kernels, training procedures, or model modifications.
- **Approximation model agnostic:** Can use smaller Transformers, n-gram models, or even random token selection (which guarantees some improvement, however small).

## Analysis

The paper provides theoretical analysis of the expected speedup:

- **Acceptance rate $\alpha$**: $\alpha = \mathbb{E}[\min(p,q)]$ — the expected probability that a candidate from $M_q$ is accepted. Empirically $\alpha \in [0.5, 0.9]$ with approximation models ~100× smaller than the target.
- **DLK divergence**: $D_{LK}(p,q) = 1 - \sum_x \min(p(x), q(x))$ — a symmetric divergence relating to acceptance rate: $\beta = 1 - D_{LK}(p,q)$.
- **Expected tokens per iteration**: $\frac{1 - \alpha^{\gamma+1}}{1 - \alpha}$ (under i.i.d. assumption for $\beta$).
- **Walltime improvement factor**: $\frac{1 - \alpha^{\gamma+1}}{(1-\alpha)(\gamma c + 1)}$ where $c$ is the cost ratio $T_{M_q} / T_{M_p}$.
- **Optimal $\gamma$** can be computed numerically from $\alpha$ and $c$ (see Figure 3 in paper).

## Empirical Results

Demonstrated on T5-XXL (11B parameters) across two tasks:

| Task | $M_q$ | Temp | $\gamma$ | $\alpha$ | Speedup |
|------|-------|------|----------|----------|---------|
| EN→DE translation | T5-small (77M) | 0 | 7 | 0.75 | **3.4×** |
| EN→DE translation | T5-base (250M) | 0 | 7 | 0.80 | 2.8× |
| EN→DE translation | T5-small (77M) | 1 | 7 | 0.62 | **2.6×** |
| CNN/DM summarization | T5-small (77M) | 0 | 5 | 0.65 | **3.1×** |
| CNN/DM summarization | T5-base (250M) | 0 | 5 | 0.73 | 3.0× |

$\alpha$ values measured across model scales (Table 3):

| $M_p$ | $M_q$ | $\alpha$ (T=0) | $\alpha$ (T=1) |
|-------|-------|----------------|----------------|
| GPT-like (97M) | Unigram | 0.03 | 0.03 |
| GPT-like (97M) | Bigram | 0.05 | 0.05 |
| GPT-like (97M) | GPT-like (6M) | **0.88** | **0.89** |
| LaMDA (137B) | LaMDA (100M) | 0.61 | 0.57 |
| LaMDA (137B) | LaMDA (2B) | 0.71 | 0.71 |
| LaMDA (137B) | LaMDA (8B) | 0.75 | 0.74 |

Key observations:
- Argmax sampling (T=0) yields higher $\alpha$ than standard sampling (T=1).
- Approximation models ~100× smaller than the target produce $\alpha \in [0.5, 0.9]$.
- Even trivial n-gram models produce non-negligible $\alpha$ (0.03–0.23), yielding 1.25× speedup for translation with a bigram + T5-XXL.

## Negligible-Cost Approximation Models

A special case where $c \approx 0$: n-gram models (table lookups), context-copying heuristics (useful for summarization/chat where outputs overlap with inputs), and non-autoregressive models. With negligible-cost models the walltime improvement approaches $\frac{1}{1-\alpha}$.

## Lenience

An optional relaxation (Appendix A.5) trades exact distribution matching for higher speed. By multiplying $q(x)$ by $l < 1$ before comparing with $p(x)$, the acceptance rate $\alpha$ increases while guaranteeing no token is sampled with probability greater than $p(x)/l$. With $l=0.1$ (10× bound), T5-small achieves $\alpha=0.84$ and an estimated 5× speedup.

## Limitations

- **Increased arithmetic operations:** Total compute grows by factor $\frac{(1-\alpha)(\gamma\hat{c} + \gamma + 1)}{1-\alpha^{\gamma+1}}$; the method trades compute for latency.
- **Requires spare compute resources:** Only effective when inference is memory-bandwidth bound and additional compute is available — common for large Transformer decoders.
- **Beam search support limited:** Preliminary analysis (Appendix A.4) but no full theoretical treatment.
- **No training benefit:** Accelerates inference only, not training.

## Relationship to Other Inference Methods

- **[[kv-caching|KV Caching]]** — orthogonal and complementary. KV caching reduces recomputation across decoding steps; speculative decoding reduces serial steps. They can be combined: the verification step benefits from KV cache.
- **[[flash-attention|FlashAttention]]** — complementary. FlashAttention reduces per-step compute via IO-aware tiling; speculative decoding reduces the number of serial steps. Both can be applied to the same model.
- **[[multi-query-attention|Multi-Query Attention (MQA)]]** — orthogonal optimization targeting the memory-bandwidth bottleneck. MQA reduces KV cache size by sharing keys/values across heads; speculative decoding exploits available compute for parallel verification.
- **[[sparse-transformer|Sparse Transformer]]** — addresses the O(n²) attention bottleneck via sparsity; speculative decoding addresses the serial decoding bottleneck. Orthogonal.
- **Knowledge Distillation** — trains a compact student to mimic a larger teacher, changing model weights. Speculative decoding keeps both models unchanged and guarantees distributional identity.
- **Adaptive computation methods** (early exits, input-dependent depth) — change model architecture and output distribution; speculative decoding requires neither.

## Subsequent Influence

Speculative decoding became the foundation of a broad family of inference acceleration techniques adopted across the LLM ecosystem. An independent implementation by Chen et al. (DeepMind, arXiv 2302.01318) demonstrated 2–2.5× speedup on Chinchilla 70B shortly after the initial publication. The technique is now standard in production LLM serving systems (TensorRT-LLM, vLLM, llama.cpp) and has been extended to multi-draft, tree-based, and self-speculative variants.

## Open Questions (from the paper)

- Hierarchical speculative decoding (approximation model accelerated by an even faster model)
- Dynamic $\gamma$ selection per prefix (oracle bound suggests up to ~60% additional improvement)
- Custom approximation models trained specifically for high $\alpha$ (e.g. via distillation with soft targets from $M_p$)
- Full beam search integration
- Extension to non-text modalities (images, audio)

([Leviathan, Kalman & Matias, 2023](raw/papers/2022-11-leviathan-speculative-decoding/laviathan2022speculativedecoding.md))
