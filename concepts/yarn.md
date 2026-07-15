---
title: YaRN (Yet another RoPE extensioN)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - inference
  - training
sources:
  - "[YaRN: Efficient Context Window Extension of Large Language Models](raw/papers/2023-08-peng-yarn/peng2023yarn.md)"
confidence: high
---

# YaRN (Yet another RoPE extensioN)

YaRN is a compute-efficient method for extending the context window of [[rotary-position-embedding|RoPE]]-based transformers (LLaMA, GPT-NeoX, PaLM families) via a small amount of fine-tuning — or, in its Dynamic variant, with no fine-tuning at all. Introduced by Peng, Quesnelle, Fan & Shippole (Nous Research / EleutherAI / Univ. Geneva, arXiv 2309.00071, 2023), it requires **~10× fewer tokens and ~2.5× fewer training steps** than the prior Position Interpolation (PI) method (Chen et al., 2023) to reach the same extended context, while surpassing all earlier RoPE-interpolation techniques on perplexity and passkey retrieval. ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

## Why RoPE needs extension

RoPE encodes absolute position via per-dimension rotation frequencies θ_d = 10000^{-2d/d_model}, so the attention dot product q_m^T k_n depends only on relative distance (m−n). This gives RoPE no built-in maximum length — yet in practice models trained with RoPE **fail to generalize past their pre-trained context length L**. Among earlier position encodings, only [[alibi|ALiBi]] (Press et al., 2022) extrapolated at all, and only limitedly; none scaled far beyond L without fine-tuning (Kazemnejad et al., 2023). ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

## The two ingredients of YaRN

YaRN combines two independently-motivated fixes to Position Interpolation:

### 1. NTK-by-parts interpolation (fixes high-frequency loss)

Position Interpolation naively scales every RoPE dimension by the same factor s = L′/L (g(m)=s·m). This stretches high-frequency dimensions, destroying the fine positional signal; PI fine-tunes topped out around s≈8 before output degraded. The earlier "NTK-aware" fix spread interpolation pressure across dimensions (scale high frequencies less, low frequencies more) but demanded an empirically-tuned base b.

YaRN's "NTK-by-parts" makes this explicit via each dimension's wavelength λ_d = 2πb^{d/d_model} and the ratio r(d) = L / λ_d:
- if **λ_d ≪ L** (r < α): do **not** interpolate — these dims carry only relative position, crucial for nearby-token ordering;
- if **λ_d ≥ L** (r > β): **fully** interpolate by scale s (avoid extrapolation, unlike NTK-aware);
- in-between (α ≤ r ≤ β): linear ramp γ(r) blends the two.

For the LLaMA family good values are α=1, β=32. ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

### 2. Attention temperature scaling (fixes attention entropy)

YaRN reparametrizes the attention softmax (Eq. 14) as softmax(q_m^T k_n / (t·√d_model)), where the temperature **t** counteracts the increased entropy of interpolated embeddings. By writing RoPE as 2D rotation matrices, this scaling reduces to a **"length-scaling" trick**: multiply both q and k by 1/√t. That means YaRN alters the attention mechanism *without touching attention code* and with **zero overhead** at inference/training, since rotary embeddings are precomputed and reused. ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

For LLaMA and Llama-2 the recommended t comes from a fit on perplexity vs scale:

```
1/√t = 0.1·ln(s) + 1
```

found by fitting on LLaMA 7B/13B/33B/65B without fine-tuning; the same t transfers well to Llama-2 (7B/13B/70B), suggesting a degree of universality. ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

## Training efficiency

YaRN fine-tunes on **< 0.1 % of original pre-training data**. The 128k models extended Llama-2 7B/13B (s=16 then s=32) on PG19 chunked into 64k segments, using AdamW (lr 2e-5), global batch 64, [[flash-attention|FlashAttention-2]], for 400 steps at s=16 and an extra 200 steps at s=32. ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

Compute vs prior open methods (7B, A100-hours):

| Method | Extends to | A100-hrs |
|--------|-----------|----------|
| PI (Chen et al., 2023) | 16k | 640 |
| NTK-aware (CodeLlama) | ~100k | 6400 |
| **YaRN (this work)** | **32k (s=16)** | **128** |

YaRN converges fastest and is the most compute-efficient of the four interpolation families. ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

## Results

- **Long-sequence perplexity (Proof-pile, 128k docs, sliding window S=256):** Llama-2 13B YaRN at s=32 reaches 2.24 at 131072 tokens; 7B YaRN s=32 reaches 2.37. The s=16 models degenerate (>101) at 131072, showing YaRN's interpolation (not extrapolation) is what enables clean 128k.
- **Extrapolation / "trains short, tests long":** the s=32 model, further trained only 200 steps on 64k data from the s=16 checkpoint, extrapolates to 128k context — transfer learning across context scales.
- **Passkey retrieval:** YaRN beats PI, NTK-aware, and NTK-by-parts at equal training budget (32k LLaMA 7B, 400 steps).
- **Short-context preservation:** on the Hugging Face Open LLM suite (ARC-c, HellaSwag, MMLU, TruthfulQA) YaRN models show minimal degradation vs Llama-2 baselines; average 0.49% score drop between s=16 and s=32 models. ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

## Dynamic Scaling (Dynamic-YaRN) — zero-shot extension

Instead of fixing the scale s = L′/L for the whole session, **Dynamic Scaling** sets s = max(1, l′/L) per forward pass, where l′ is the current sequence length. This lets the model degrade gracefully past L′ rather than break abruptly. Combined with "NTK-aware" it is the "Dynamic NTK" method (emozilla, 2023); with YaRN it is **Dynamic-YaRN**, giving **>2× context extension with no fine-tuning** on models pre-trained at L.

**KV-cache caveat:** when RoPE is cached, cache the **kv-embeddings before applying RoPE** — because every token's RoPE changes as s changes each step. ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

## Compatibility

Because YaRN is a pure embedding-interpolation method (it only rescales RoPE frequencies and q/k magnitudes), it stays compatible with attention-mechanism optimizers such as [[flash-attention|FlashAttention-2]]. This distinguishes it from ReRoPE (Su, 2023) and LM-Infinite (Han et al., 2023), which modify the attention mechanism itself, need two attention passes, and break FlashAttention-2 compatibility. ([Peng et al., 2023](raw/papers/2023-08-peng-yarn/peng2023yarn.md))

## Cross-Links

- [[rotary-position-embedding|Rotary Position Embedding (RoPE)]] — the position encoding YaRN extends
- [[alibi|ALiBi]] — the other position method with any native extrapolation ability
- [[positional-encoding|Positional Encoding]] — the broader class
- [[kv-caching|KV Caching]] — Dynamic-YaRN's caching caveat
- [[flash-attention|FlashAttention]] — YaRN's drop-in compatibility target
