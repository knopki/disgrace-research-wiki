---
title: Grouped-Query Attention (GQA)
created: 2026-07-11
updated: 2026-07-11
type: concept
tags:
  - architecture
  - inference
  - optimization
authors:
  - Joshua Ainslie
  - James Lee-Thorp
  - Michiel de Jong
  - Yury Zemlyanskiy
  - Federico Lebrón
  - Sumit Sanghai
sources:
  - "[GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](raw/papers/2023-05-ainslie-grouped-query-attention/ainslie2023gqa.md)"
confidence: high
---

# Grouped-Query Attention (GQA)

An attention architecture introduced by [Ainslie et al. (Google Research, EMNLP 2023)](raw/papers/2023-05-ainslie-grouped-query-attention/ainslie2023gqa.md) that interpolates between [[multi-query-attention|multi-head attention (MHA)]] and [[multi-query-attention|multi-query attention (MQA)]]. Query heads are partitioned into `G` groups; all query heads within a group share a single key head and a single value head. This shrinks the KV cache proportionally to `H/G` (where `H` is the number of query heads), trading a fraction of MQA's speed for quality much closer to full MHA.

`GQA-G` notation: `GQA-1` = MQA (one group, single K/V head); `GQA-H` = MHA (groups = heads). The paper selected `G = 8` as a favorable middle ground for T5-XXL.

## Motivation

Autoregressive decoder inference is bottlenecked by the memory-bandwidth cost of loading decoder weights and all attention keys/values at every decoding step ([Shazeer, 2019](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md)). MQA cuts this by sharing one K/V head across all query heads, but it can degrade quality and is training-unstable during fine-tuning. It is also wasteful to train two separate models (one optimized for quality, one for speed). Many widely used models (T5, LLaMA 1) used full MHA, leaving their inference unoptimized.

GQA's two contributions:
1. **Uptraining recipe** — convert an existing MHA checkpoint to MQA/GQA and continue pre-training for only ~5% of the original compute, yielding fast and high-quality checkpoints from already-trained models.
2. **GQA itself** — an interpolation that avoids MQA's worst quality loss while retaining most of its speed.

## Method

### Uptraining
Converting an MHA checkpoint to MQA/GQA is a two-step process:
1. **Checkpoint conversion** — for each (group of) K/V head(s), mean-pool the corresponding original per-head K/V projection matrices. The paper finds mean-pooling beats both "select the first head" and "random init from scratch" (ordered by how much pretrained information is preserved).
2. **Continued pre-training** — train for a proportion `α` of the original pre-training steps on the same recipe. With `α = 0.05` on T5-XXL this cost ~600 TPUv3 chip-days.

GQA is applied to decoder self-attention and cross-attention, **not** encoder self-attention (encoder representations are computed in parallel, so memory bandwidth is not the primary bottleneck).

### GQA structure
Divide the `H` query heads into `G` groups; each group shares one K head and one V head. Going from MHA (`H` K/V heads) to MQA (1 K/V head) reduces KV-cache size — and the data loaded per step — by a factor of `H`. Larger models scale head count, so MQA is an increasingly aggressive cut in both bandwidth and capacity; GQA lets you keep the same *proportional* decrease as model size grows. GQA also removes waste from standard model sharding, which otherwise replicates the single MQA K/V head across all `P` model partitions.

## Experimental Results

Based on T5.1.1 (JAX/Flax/Flaxformer), eval on summarization (CNN/DM, arXiv, PubMed, MediaSum, Multi-News), WMT14 En-De translation, and TriviaQA. Greedy decoding; inference timed per sample on TPUv4.

| Model | T_infer (s/sample) | Avg. dev | CNN/DM | arXiv | PubMed | MediaSum | MultiNews | WMT BLEU | TriviaQA F1 |
|---|---|---|---|---|---|---|---|---|---|
| MHA-Large | 0.37 | 46.0 | 42.9 | 44.6 | 46.2 | 35.5 | 46.6 | 27.7 | 78.2 |
| MHA-XXL | 1.51 | 47.2 | 43.8 | 45.6 | 47.5 | 36.4 | 46.9 | 28.4 | 81.9 |
| MQA-XXL (5% uptrained) | 0.24 | 46.6 | 43.0 | 45.0 | 46.9 | 36.1 | 46.5 | 28.5 | 81.3 |
| **GQA-8-XXL (5% uptrained)** | **0.28** | **47.1** | 43.5 | 45.4 | 47.7 | 36.3 | 47.2 | 28.4 | 81.6 |

GQA-8-XXL delivers quality essentially equal to MHA-XXL (47.1 vs 47.2 avg) at ~5.4× faster inference (0.28 vs 1.51 s/sample), and only marginally slower than MQA (0.28 vs 0.24) while clearly beating it on quality (47.1 vs 46.6). Uptrained MQA-XXL also beats MHA-Large on both quality and speed.

## Ablations

- **Conversion method** — mean-pooling > first-head selection > random init.
- **Uptraining proportion** — GQA is usable right after conversion; MQA needs uptraining to be useful. Both gain from 5% uptraining, with diminishing returns by 10%.
- **Number of groups** — for large models the KV-cache bandwidth overhead is less constraining (KV cache scales with model dimension, FLOPs/params with its square), so going from 1 (MQA) to 8 groups adds only modest slowdown; cost grows as groups approach `H`. 8 groups chosen as the middle ground.

## Why GQA Favors Larger Models

Larger models scale head count (sharpening the KV-size reduction) while suffering relatively less from attention memory-bandwidth overhead; GQA keeps the proportional bandwidth/capacity cut constant as size grows and avoids sharding waste. The authors note decoder-only models (no separate cross-attention) are expected to show an even stronger GQA-over-MQA advantage.

## Relationship to Other Attention Variants

The query/key/value head-count spectrum:
- **MHA** — `h_q = h_k = h_v` (full separation)
- **GQA** — `h_q = g × h_k = g × h_v` (groups share K/V)
- **MQA** — `h_q = h`, `h_k = h_v = 1` (all share one K/V)

GQA is orthogonal to and combinable with other bandwidth-reduction techniques: [[flash-attention|FlashAttention]] (avoids materializing quadratic attention scores), [[kv-caching|KV caching]] (still benefits — smaller KV cache loaded per step), quantization (lowers KV precision), and [[speculative-decoding|speculative decoding]] (parallel scoring amortizes the same bottleneck).

## Legacy and Impact

GQA became the de-facto attention variant for post-2023 open LLMs seeking the MHA-quality / MQA-speed trade-off: LLaMA 2, LLaMA 3, Mistral, and many others use GQA. Rabe (2023) independently developed GQA with a public implementation in Flaxformer. The uptraining recipe lets teams retrofit existing MHA checkpoints rather than train fast models from scratch.

## Limitations (per paper)

- Trade-offs evaluated mainly via ROUGE, a flawed proxy for long-sequence quality.
- No comparison of uptrained XXL GQA against a from-scratch GQA model (uptrain vs train-from-scratch relative quality unknown).
- Evaluated only on encoder-decoder (T5) models; decoder-only behavior hypothesized but not tested.

## Cross-Links

- [[multi-query-attention|Multi-Query Attention]] — GQA generalizes MQA; the original 2019 formulation is the GQA-1 endpoint of the spectrum
- [[kv-caching|KV Caching]] — GQA shrinks the KV cache (the load that dominates incremental decoding); both motivated by the same bandwidth bottleneck
- [[transformer|Transformer]] — the architecture GQA modifies (decoder self/cross-attention)
- [[flash-attention|FlashAttention]] — complementary IO-aware attention; both reduce attention memory cost at different levels
- [[speculative-decoding|Speculative Decoding]] — another bandwidth-bottleneck amelioration cited in the paper's related work
