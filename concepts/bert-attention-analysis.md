---
title: BERT Attention Analysis
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - architecture
  - analysis
  - interpretation
sources:
  - "[What Does BERT Look At? An Analysis of BERT's Attention](raw/papers/2019-06-clark-bert-attention/clark2019bertattention.md)"
---

# BERT Attention Analysis

**Clark, Khandelwal, Levy & Manning (2019)** — a systematic analysis of BERT's 144 attention heads (12 layers × 12 heads in BERT-Base), proposing methods for probing attention mechanisms and demonstrating that substantial syntactic and coreference information is captured in BERT's attention maps despite purely self-supervised pre-training ([Clark et al., 2019](raw/papers/2019-06-clark-bert-attention/clark2019bertattention.md)).

Key findings: heads specialize to specific syntactic relations (dobj, det, pobj, poss, auxpass, etc.), they cluster by layer, and attention to `[SEP]` functions as a learned no-op.

## Surface-Level Patterns

Three categories of attention behavior emerged across BERT's heads:

- **Positional heads** — attend to fixed offsets (previous/next token), concentrated in early layers. Four heads put >50% attention on the previous token; five put >50% on the next token.
- **Delimiter-attending heads** — a substantial fraction of BERT's attention focuses on `[SEP]`, `[CLS]`, periods, and commas. Over half of BERT's attention in layers 6–10 goes to `[SEP]`.
- **Broad-attending heads** — high-entropy distributions that spread attention across many tokens, effectively producing a bag-of-vectors representation. More common in early layers.

### The [SEP] No-Op Hypothesis

Heads attending to `[SEP]` allocate >90% of that attention to `[SEP]` tokens attending to themselves or each other, not to the rest of the sentence. Gradient-based feature importance (integrated gradients) shows that starting from layer 5, gradients for `[SEP]` attention become very small — changing it does not affect BERT's outputs. Clark et al. argue this is a learned **no-op**: when a head's specialized function is not applicable (e.g., a determiner-finding head processing a non-noun), it defaults to attending to `[SEP]` rather than making spurious predictions.

Supporting evidence: heads with clear syntactic roles (e.g., head 8-10 for direct objects) attend to `[SEP]` when the current word is not a noun — its detector function signals "not applicable" and the head idles.

## Syntactic Head Specialization

Individual attention heads were evaluated as zero-parameter classifiers: for each word, the most-attended other word (ignoring `[SEP]`/`[CLS]`) is taken as the head's prediction. BPE token-to-word conversion: sum attention to split words, average attention from split words.

**Best heads per dependency relation** (WSJ, Stanford Dependencies):

| Relation | Head | Accuracy | Offset Baseline |
|----------|------|----------|-----------------|
| All | 7-6 | 34.5 | 26.3 |
| **det** (determiner) | 8-11 | **94.3** | 51.7 |
| **dobj** (direct object) | 8-10 | **86.8** | 40.0 |
| **auxpass** (passive auxiliary) | 4-10 | **82.5** | 40.5 |
| **poss** (possessive) | 7-6 | **80.5** | 47.7 |
| **pobj** (object of preposition) | 9-6 | **76.3** | 34.6 |
| **amod** (adjectival modifier) | 4-10 | 75.6 | 68.3 |
| **nn** (noun compound modifier) | 4-10 | 70.4 | 70.2 |
| **nsubj** (nominal subject) | 8-2 | 58.5 | 45.5 |

No single head does well at syntax overall (best UAS 34.5, vs right-branching baseline 26.3). Instead, individual heads specialize to specific relations, substantially outperforming fixed-offset baselines. The dependent almost always attends to the head (not the reverse), consistent with each dependent having exactly one head.

For `prt` (phrasal verb particle), head 6-7 achieves an extraordinary 99.1% accuracy, though the baseline is already high at 91.4%.

## Coreference Resolution

Head 5-4 achieves 65.1% antecedent selection accuracy on CoNLL-2012 — outperforming the nearest-mention baseline (27%) and the head-match baseline (52%), competitive with a rule-based sieve system (69%):

| Model | All | Pronoun | Proper | Nominal |
|-------|-----|---------|--------|---------|
| Nearest mention | 27 | 29 | 29 | 19 |
| Head match | 52 | 47 | 67 | 40 |
| Rule-based (Lee et al.) | 69 | 70 | 77 | 60 |
| **Head 5-4** | **65** | **64** | **73** | **58** |

The head is particularly good with nominal mentions, possibly due to fuzzy synonym matching learned during pre-training.

## Attention-Based Probing Classifiers

Two probing classifiers that treat attention maps as input (no backprop into BERT, few trained parameters):

1. **Attention-Only Probe** — linear combination of attention weights from all 144 heads (both directions: head→dependent and dependent→head). Achieves 61 UAS.

2. **Attention-and-Words Probe** — same architecture but weight matrices depend on GloVe embeddings of the candidate word pair. This lets the probe dynamically upweight relevant heads (e.g., when the pair is "the" and "cat", assign most weight to determiner-specialized head 8-11). Achieves **77 UAS** — substantially above the right-branching baseline (26) and the distance+GloVe baseline (58).

A randomly initialized BERT (pre-trained embeddings only) with Attn+GloVe scores only 30 UAS, confirming the attention patterns are learned, not architectural artifacts. The 77 UAS is comparable to Hewitt & Manning's structural probe (80 UUAS), suggesting syntactic information in BERT's attention maps is roughly as rich as in its hidden state vectors.

## Head Clustering

Using Jensen-Shannon divergence between attention distributions pairwise, then embedding heads in 2D via multidimensional scaling: heads in the **same layer tend to cluster together** — their attention distributions are more similar across different inputs than those of heads from different layers.

This contradicts the intuition that multi-head attention captures diverse features within each layer. Clark et al. propose attention dropout as a possible cause: random zeroing forces heads to learn redundant behaviors since any head might be dropped at any step.

## Relationship to Other Work

- [[attention-head-pruning|Attention Head Pruning]] — Voita et al. (2019), contemporaneous work, also identifies positional, syntactic, and rare-word attention heads, but in **machine translation models** (not BERT). Voita et al. additionally demonstrate most heads can be pruned; Clark et al. show syntactic heads exist in a **pre-trained LM** setting. Both confirm that specialized heads are the functionally important ones.
- [[bert|BERT]] — the architecture being analyzed; findings about attention complement the architectural and empirical results of the original BERT paper
- [[transformer|Transformer]] — the general architecture; findings inform understanding of multi-head attention redundancy
- [[positional-encoding|Positional Encoding]] — positional heads in BERT complement the analysis of positional encoding mechanisms

## Key Takeaways

- Self-supervised pre-training alone produces attention heads that specialize to specific syntactic roles without any explicit supervision
- `[SEP]` attention functions as a learned no-op mechanism — one of the earliest documented uses of attention for "negative space" in Transformers
- Heads in the same layer tend to behave similarly, suggesting BERT's multi-head attention is more redundant than diverse within layers
- Attention maps carry syntactic information comparable to hidden state vectors — probing attention is a valid and complementary analysis technique

## Cross-Links

- [[bert|BERT]] — the model being analyzed
- [[attention-head-pruning|Attention Head Pruning]] — complementary analysis on MT models (Voita et al., 2019)
- [[transformer|Transformer]] — multi-head attention architecture
- [[positional-encoding|Positional Encoding]] — connection to positional heads
- [[knowledge-distillation|Knowledge Distillation]] — another lens on model internals via soft target analysis
