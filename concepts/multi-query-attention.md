---
title: Multi-Query Attention (MQA)
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - architecture
  - inference
  - optimization
sources:
  - "[Fast Transformer Decoding: One Write-Head is All You Need](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md)"
  - "[KV Caching Explained](raw/articles/2023-kv-caching-explained/joaolages2023kvcache.md)"
confidence: high
---

# Multi-Query Attention (MQA)

An architectural variant of Transformer multi-head attention introduced by [Noam Shazeer](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md) (Google, 2019) where the **keys (K) and values (V) are shared across all attention heads**, while queries (Q) retain per-head projections. This reduces the memory footprint of the KV cache by a factor of `h` (number of heads), directly addressing the memory-bandwidth bottleneck of incremental autoregressive decoding.

## Motivation: The Incremental Decoding Bottleneck

Standard [[transformer|Transformer]] multi-head attention maintains separate key and value projections for each of `h` heads. During training and batched inference this is efficient — the attention computation is compute-bound and parallelisable across the sequence length `n`. However, during incremental (autoregressive) decoding, each step processes one token at a time, and the complexity analysis reveals a fundamentally different bottleneck ([Shazeer, 2019](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md)).

Under typical assumptions (`k=v=d_model/h`, `n ≤ d`), the ratio of memory access to arithmetic operations per decoding step is:

| Attention Variant | Memory/Access Ratio | Bottleneck Condition |
|---|---|---|
| Multi-head (incremental) | Θ(n/d + 1/b) | Memory-bandwidth bound when n ≈ d |
| Multi-query (incremental) | Θ(1/d + d/(hn) + 1/b) | Compute-bound for large batches |

The `n/d` term in multi-head attention comes from repeatedly loading the full per-head K and V tensors (shape `[b, h, m, k/v]`) at each step. Multi-query attention eliminates the `h` dimension from K and V (shape becomes `[b, m, k/v]`), reducing the term from `n/d` to `d/(hn)` — a factor of `h` improvement. ([Shazeer, 2019](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md))

## Implementation

In multi-head attention, the K and V projections are tensors of shape `[h, d, k/v]`. In multi-query attention, each attention head still has its own Q projection (`[h, d, k]`), but K and V share a single projection each (`[d, k]` and `[d, v]`):

```python
# Multi-head: K, V each have heads dimension
K = einsum("bmd, hdk->bhmk", M, P_k)
V = einsum("bmd, hdv->bhmv", M, P_v)

# Multi-query: K, V have no heads dimension
K = einsum("bmd, dk->bmk", M, P_k)
V = einsum("bmd, dv->bmv", M, P_v)
```

The attention computation broadcasts the shared K/V across heads: the query still sees `h` sets of Q, but they all attend to the same K and V. ([Shazeer, 2019](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md))

## Experimental Results

Evaluated on WMT14 EN-DE translation (6-layer Transformer, d_model=1024, h=8, d_k=d_v=128) and the Billion-Word Language Modeling Benchmark.

### Machine Translation (WMT14 EN-DE)

| Attention Type | h | d_k, d_v | d_ff | ln(PPL) | BLEU (dev) | BLEU test (beam 1/4) |
|---|---|---|---|---|---|---|
| Multi-head | 8 | 128 | 4096 | 1.424 | 26.7 | 27.7 / 28.4 |
| Multi-query | 8 | 128 | 5440 | 1.439 | 26.5 | 27.5 / **28.5** |
| Multi-head h=1 | 1 | 128 | 6784 | 1.518 | 25.8 | 26.8 / 27.9 |
| Multi-head d_v=32 | 8 | 16 | 6784 | 1.513 | 25.8 | — |

The multi-query model was widened (d_ff=5440 vs 4096) to match the baseline's 211M parameters. It slightly underperforms the baseline by 0.2 BLEU (greedy), but actually achieves the **highest BLEU score with beam-4 decoding** (28.5 vs 28.4). Simply reducing `h` or `d_k/d_v` hurts quality far more. ([Shazeer, 2019](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md))

### Language Modeling (Billion-Word Benchmark)

| Attention Type | dev PPL |
|---|---|
| Multi-head (h=8, d_k=128) | 29.9 |
| Multi-query | 30.2 |
| Multi-head h=1 | 31.2 |
| Multi-head h=2 | 31.1 |

The multi-query model (30.2 PPL) is again much closer to the baseline (29.9) than any alternative reduction strategy. ([Shazeer, 2019](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md))

### Speedup

Measured on TPUv2 (8 cores), amortized per-token times on WMT14 EN-DE (seq len 128):

| Configuration | Encoder | Decoder (greedy) | Decoder (beam-4) | Training |
|---|---|---|---|---|
| Multi-head | 1.7 µs/tok | 46 µs/tok | 203 µs/tok | 13.2 µs/tok |
| Multi-query | 1.5 µs/tok | **3.8 µs/tok** | **32 µs/tok** | 13.0 µs/tok |
| **Speedup** | 1.1× | **12.1×** | **6.3×** | ~1× |

The decoder speedup is dramatic: 12× for greedy decoding, 6.3× for beam search. Training speed is essentially unchanged. ([Shazeer, 2019](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md))

## Orthogonality to Other Techniques

The paper demonstrates that multi-query attention is orthogonal to **local (sliding-window) attention** — combining both yields further gains (multi-query local: 3.3 µs/tok decoder vs 23 µs/tok for multi-head local). Local attention reduces the `n` term, MQA reduces the `h` term; they address different components of the memory-bandwidth ratio. ([Shazeer, 2019](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md))

## Legacy and Impact

MQA directly inspired **Grouped-Query Attention (GQA)** ([Ainslie et al., 2023](https://arxiv.org/abs/2305.13245)), which generalises the idea by partitioning heads into groups, each sharing one K/V head. GQA is used in LLaMA 2/3, Mistral, and many modern open LLMs as a middle ground between full multi-head (maximum quality) and MQA (maximum efficiency).

MQA also provides the theoretical foundation for understanding why [[kv-caching|KV caching]] is memory-bound in the first place — the paper's performance analysis is the canonical explanation of the memory-bandwidth bottleneck in incremental transformer decoding.

The relationship between query heads and key/value heads forms a spectrum:
- **Multi-head attention** — `h_q = h_k = h_v` (full separation)
- **Grouped-query attention** — `h_q = g × h_k = g × h_v` (groups share K/V)
- **Multi-query attention** — `h_q = h`, `h_k = h_v = 1` (all share one K/V)

## Cross-Links

- [[kv-caching|KV Caching]] — MQA is both the motivation (KV cache memory-bandwidth bottleneck) and a solution (reduced KV cache size via shared K/V)
- [[transformer|Transformer]] — the architecture that MQA modifies
- [[attention-head-pruning|Attention Head Pruning]] — another approach to reducing attention overhead, focused on encoder heads
- [[flash-attention|FlashAttention]] — complementary IO-aware attention that also addresses memory-bandwidth but at the per-step level rather than across decoding steps
- [[sparse-transformer|Sparse Transformer]] — orthogonal efficiency technique addressing the `n` term via sparse attention patterns
