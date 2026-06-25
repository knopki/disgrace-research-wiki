---
title: ALiBi (Attention with Linear Biases)
created: 2026-06-25
updated: 2026-06-25
type: concept
tags:
  - architecture
  - technique
  - training
sources:
  - "[Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](raw/papers/2021-08-press-alibi/press2022alibi.md)"
confidence: high
---

# ALiBi (Attention with Linear Biases)

Attention with Linear Biases (ALiBi) is a position method for [[transformer|Transformer]] language models that eliminates positional embeddings entirely. Instead of adding position information to token or word embeddings, ALiBi directly biases the query-key attention scores with a linearly decreasing penalty proportional to the distance between the query and key. This simple mechanism enables **input length extrapolation** — training on short sequences while maintaining strong performance on arbitrarily longer sequences at inference. (Press et al., Facebook AI Research / UW / AI2, ICLR 2022)

## Mechanism

ALiBi does not modify word embeddings, query/key/value projections, or the attention computation itself. The only change is in how attention scores are computed:

```
attention_scores(q, k) = q^T · k - m_i · |pos_q - pos_k|
```

where `m_i` is a head-specific scalar slope. For a model with `h` attention heads, the slopes form a geometric sequence:

```
m_i = 2^(-(8/(h-1)) · i)   for i = 0, 1, ..., h-1
```

Head 0 gets the largest slope (`m_0 = 2^0 = 1`), and each subsequent head gets an exponentially smaller slope. This creates a hierarchy of recency biases: lower-numbered heads have a strong recency bias (sharp attention focus on nearby tokens), while higher-numbered heads with very small slopes approach standard unmasked attention (≈1/h for all positions beyond ~L). The result is that ALiBi preserves resolution at all distance scales without learned position parameters.

The choice of the base `2^(-8/(h-1))` ensures that the smallest slope among `h` heads is at most `m_(h-1) = 2^(-8) ≈ 0.0039`, essentially flat across any practical sequence length. This specific schedule was empirically determined on WikiText-103 and transfers across domains without further tuning.

## Key Properties

### Zero Additional Parameters

Unlike sinusoidal PE (fixed but requires position vectors), learned embeddings (trainable parameters), or T5 bias (learned per-distance scalars), ALiBi introduces **no learnable parameters**. The slopes are fixed before training, and the bias computation is a simple scalar multiplication and subtraction on the attention score matrix.

### Negligible Computational Overhead

ALiBi adds 0–0.7% memory and 0–3% runtime overhead vs. sinusoidal PE during training and inference — well within noise bounds. The T5 bias, by contrast, is at least 2× slower than sinusoidal.

### Input Length Extrapolation

This is ALiBi's defining property. A model trained on sequences of length `L = 512` with ALiBi maintains stable perplexity even when evaluated on sequences up to 10,000+ tokens — more than 20× the training length. Performance peaks at roughly 2× the training length, but degradation is graceful beyond that, unlike sinusoidal or rotary methods where perplexity explodes once `L_valid > L + 50` (sinusoidal) or `L_valid > L + 200` (rotary).

| Method | Max useful L_valid (trained on L=512) | Max useful L_valid (trained on L=1024) |
|--------|---------------------------------------|----------------------------------------|
| Sinusoidal | L + ~50 tokens | L + ~50 tokens |
| Rotary | L + ~200 tokens | L + ~100 tokens |
| T5 Bias | L + ~600 tokens | L + ~800 tokens |
| ALiBi | > 15,000 tokens | > 15,000 tokens |

### Inductive Bias Towards Recency

By penalising attention scores proportional to distance, ALiBi encodes a strong recency prior — nearby tokens have a larger influence than distant ones. This bias is architectural rather than learned, and the authors argue it is beneficial for language modeling where local context is typically more relevant than long-range dependencies.

## Empirical Results

### WikiText-103 (247M parameter model)

On the WikiText-103 benchmark, ALiBi consistently outperforms sinusoidal, rotary, and T5 bias position methods:

| Model | Training PPL (L_valid = 3072) | Test PPL (sliding window) |
|-------|------|------|
| Sinusoidal, L=3072 | 18.67 | 18.67 |
| Rotary, L=3072 | 18.57 | 18.72 |
| T5 Bias, L=3072 | 18.01 | 18.12 |
| **ALiBi, L=3072** | **17.60** | **17.66** |
| ALiBi, L=512 (extrapolated to 3072) | 18.40 | 19.01 |

Notably, ALiBi trained on L=512 and evaluated at L_valid=3072 (6× extrapolation!) achieves comparable perplexity to the sinusoidal model trained on L=3072 (PPL 18.40 vs 18.67), while training at more than double the speed (28.3k vs 15.3k words/sec).

### CC100+RoBERTa (1.3B parameter model)

A 1.3B parameter ALiBi model trained on L=1024 achieves **better perplexity** on L_valid=2048 than a sinusoidal model trained on L=2048, while being **11% faster and using 11% less memory**.

| Model | Memory | Training Hours | Valid PPL (L_valid=2048) |
|-------|--------|----------------|--------------------------|
| Sinusoidal, L=2048 | 29.3 GB | 5.9k | 9.01 |
| **ALiBi, L=1024** | **26.2 GB** | **5.9k** | **8.92** |

### Toronto BookCorpus

Results replicate across domains without tuning the ALiBi slopes. ALiBi L=512 achieves PPL=13.55 on L_valid=3072, beating sinusoidal L=3072 at PPL=14.46.

## Analysis: Why ALiBi Works

The authors' analysis using sliding window evaluation (stride S=1, giving every prediction maximum context) reveals that ALiBi's perplexity improvements when `L_valid > L` are **primarily due to reducing the early token curse**, not from actually attending to longer-range dependencies.

The *early token curse* occurs during non-overlapping inference: the first tokens in each subsequence have substantially less context. When evaluated with a sliding window (maximal context for every prediction), ALiBi's PPL remains flat as `L_valid` increases, whereas perplexity keeps improving with `L_valid` under non-overlapping evaluation. This suggests that ALiBi's extrapolation ability mitigates the early token curse rather than enabling genuine long-range attention beyond its training length.

This finding does not diminish the practical value of ALiBi: when `L_valid = L`, ALiBi outperforms or matches alternatives while being simpler and parameter-free. When `L_valid > L`, it offers a practical middle ground between cheap-but-limited non-overlapping inference and expensive-but-accurate sliding window evaluation.

## Relationship to Other Position Methods

- **[[positional-encoding|Sinusoidal PE]]** (Vaswani et al., 2017) — additive position vectors at the first layer; ALiBi avoids adding position to embeddings entirely, instead biasing attention scores at every layer
- **[[rotary-position-embedding|RoPE]]** (Su et al., 2021) — multiplicative rotation of q/k vectors; also injects position at every layer but requires the rotation computation; ALiBi is simpler (just scalar bias) and achieves stronger extrapolation
- **T5 Bias** (Raffel et al., 2020) — learned relative position biases added to attention scores; ALiBi achieves superior extrapolation with a fixed (non-learned) bias schedule and is 2×+ faster
- **Learned absolute PE** (BERT, GPT) — trainable position embeddings limited to max training length; inherently cannot extrapolate to longer sequences

## Adoption and Legacy

ALiBi was adopted by several notable models, including:
- **BLOOM** (BigScience, 2022) — 176B parameter multilingual LM uses ALiBi
- **MPT** (MosaicML, 2023) — MPT-7B and MPT-30B use ALiBi
- **XGen** (Salesforce, 2023) — 7B parameter model uses ALiBi

However, RoPE has since become more dominant in the open-source LLM ecosystem (LLaMA, Mistral, Qwen, Gemma), in part because RoPE's rotation mechanism lends itself better to KV cache optimisations like NTK-aware scaling and YaRN. ALiBi remains influential as a demonstration that position information can be removed from embeddings entirely and that length extrapolation is achievable with minimal architectural changes.

## Cross-Links

- [[positional-encoding|Positional Encoding]] — the broader class of techniques ALiBi belongs to; comparison with sinusoidal, learned, and relative methods
- [[rotary-position-embedding|Rotary Position Embedding (RoPE)]] — the dominant modern alternative; contrast with ALiBi's scalar bias approach
- [[transformer|Transformer]] — the architecture requiring position methods
- [[kv-caching|KV Caching]] — ALiBi's simplicity is compatible with KV caching; no position embedding to recompute per cache entry
