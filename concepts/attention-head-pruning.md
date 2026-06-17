---
title: Attention Head Pruning
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - architecture
  - optimization
  - inference
sources:
  - "[Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned](raw/papers/2019-05-voita-attention-heads/voita2019attention.md)"
confidence: high
---

# Attention Head Pruning

Attention head pruning is the finding that the vast majority of multi-head self-attention heads in a Transformer encoder can be removed with minimal impact on translation quality, and that the few surviving heads play specialized, linguistically-interpretable roles. Established by Voita et al. (2019) for neural machine translation using LRP-based head importance analysis and a novel pruning method based on L0 relaxation.

## Head Functions

Three interpretable head roles were identified in the Transformer encoder, each corresponding to surviving heads after aggressive pruning:

- **Positional heads** — attend to an adjacent token (relative position -1 or +1). In all language pairs examined, at least 90% of the time the maximum attention weight lands on the neighbouring token. These are among the most confident heads (average max weight > 0.8) and the most important by LRP.
- **Syntactic heads** — track specific syntactic dependency relations (nominal subject *nsubj*, direct object *dobj*, adjectival modifier *amod*, adverbial modifier *advmod*). Accuracy significantly exceeds a positional baseline for each relation.
- **Rare words head** — in the first encoder layer, one head consistently points to the least frequent tokens in a sentence. On OpenSubtitles, it picks the rarest token in 66% of cases and one of the two rarest in 83%.

## Pruning Method

Stochastic gates with a differentiable L0 relaxation (Hard Concrete distribution) are applied per-head:

```
MultiHead(Q, K, V) = Concat_i(g_i · head_i) W^O
```

Each gate \(g_i\) is a random variable drawn from a Hard Concrete distribution — a stretched-and-rectified version of the Gumbel-Softmax (Concrete) distribution with non-zero probability mass at both 0 and 1. The regularizer term approximates the L0 norm:

\[
L_C(\phi) = \sum_{i=1}^{h} (1 - P(g_i = 0 | \phi_i))
\]

Training starts from a converged full model, gates are added, and the combined objective \(L(\theta, \phi) = L_{\text{xent}}(\theta, \phi) + \lambda L_C(\phi)\) is optimised. Gates converge to either fully open or fully closed — no intermediate values.

## Key Results

| Setting | Heads retained | BLEU drop |
|---------|---------------|-----------|
| EN-RU WMT, encoder-only pruning | 10/48 | −0.15 |
| EN-RU OpenSubtitles, encoder-only | 4/48 | −0.25 |
| EN-RU WMT, all attention types | 14e/31d/30de | 0.0 (≈) |
| EN-RU WMT, all attention types (aggressive) | 5e/9d/12de | −0.7 |

(e = encoder self-attention, d = decoder self-attention, de = decoder-encoder attention)

### What Gets Pruned First

Encoder self-attention heads are the **most redundant**. Decoder-encoder attention heads are the **most critical** — unsurprisingly, as translation requires conditioning on the source. Decoder self-attention importance varies by domain: near-critical for WMT (longer sentences, 24 tokens avg) but less so for OpenSubtitles (8 tokens avg).

### Architecture Matters for Trainability

Models pruned from a converged checkpoint outperform models trained from scratch with the same sparse head configuration — agreeing with the broader pruning literature (Zhu & Gupta, 2017; Gale et al., 2019). The sparse head arrangement itself is learned through joint optimization, not a static architectural choice.

## Function Drift Under Pruning

As heads are removed, surviving heads can take on multiple functions: positional heads start tracking syntactic dependencies, and syntactic heads may cover several dependency relations. Each column in Figure 8 of the paper shows heads with more than one assigned role as pruning becomes more aggressive.

## Significance & Legacy

- Established that multi-head attention is **highly redundant** — most heads can be removed without quality loss in NMT
- Showed that specialised, interpretable heads are the ones that survive pruning, linking interpretability to functional importance
- Introduced a clean L0-relaxation pruning method that became a reference for structured pruning in Transformers
- The finding that encoder self-attention is the most compressible informed later architecture designs (reduced head count in encoder vs decoder stacks)

## Open Questions

- Whether the same redundancy holds for decoder-only LLMs (GPT, LLaMA) — later work suggests decoder heads show different redundancy patterns
- Whether the head specialisation (positional, syntactic, rare words) is learned from scratch or emerges from pre-training objectives
- Whether function drift under pruning generalises to other tasks beyond NMT

## Cross-Links

- [[transformer|Transformer]] — the architecture being analysed; multi-head attention is its key component
- [[bert-attention-analysis|BERT Attention Analysis]] — Clark et al. (2019), contemporaneous work showing BERT's attention heads also specialize to syntactic relations, confirming Voita et al.'s pattern in a pre-trained LM setting
- [[kv-caching|KV Caching]] — another inference optimisation that exploits Transformer structure, orthogonal to head pruning
- [[sparse-transformer|Sparse Transformer]] — reduces per-step attention complexity; head pruning removes entire heads, sparse attention sparsifies within a head
- [[knowledge-distillation|Knowledge Distillation]] — an alternative model compression approach; pruning complements distillation but the paper notes pruned architectures cannot be retrained from scratch to the same quality
