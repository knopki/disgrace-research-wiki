---
source_url: https://arxiv.org/abs/2007.14062
ingested: 2026-06-17
title: "Big Bird: Transformers for Longer Sequences"
authors: Manzil Zaheer, Guru Guruganesh, Avinava Dubey, Joshua Ainslie, Chris Alberti, Santiago Ontanon, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang, Amr Ahmed
date: 2020-07-01
---

# Big Bird: Transformers for Longer Sequences

**Authors:** Manzil Zaheer, Guru Guruganesh, Avinava Dubey, Joshua Ainslie, Chris Alberti, Santiago Ontanon, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang, Amr Ahmed

**Affiliation:** Google Research

**Venue:** Neural Information Processing Systems (NeurIPS) 2020

Full text: [2007.14062.pdf](raw/papers/2020-07-zaheer-big-bird/2007.14062.pdf)

## Abstract

> Transformer-based models, such as BERT, have been one of the most successful deep learning models for NLP. Unfortunately, one of their core limitations is the quadratic dependency (mainly in terms of memory) on the sequence length due to their full attention mechanism. To remedy this, we propose, BIGBIRD, a sparse attention mechanism that reduces this quadratic dependency to linear. We show that BIGBIRD is a universal approximator of sequence functions and is Turing complete, thereby preserving these properties of the quadratic, full attention model. Along the way, our theoretical analysis reveals some of the benefits of having O(1) global tokens (such as CLS), that attend to the entire sequence as part of the sparse attention mechanism. The proposed sparse attention can handle sequences of length up to 8x of what was previously possible using similar hardware. As a consequence of the capability to handle longer context, BIGBIRD drastically improves performance on various NLP tasks such as question answering and summarization. We also propose novel applications to genomics data.

## Architecture

BigBird combines three attention components (all O(n) complexity):

1. **Random attention (r)** — each query attends to r randomly chosen keys (Erdős–Rényi graph). Ensures short average path length (~log n) and fast information flow.

2. **Window attention (w)** — each token attends to w/2 neighbors left and right (sliding window). Captures locality important for NLP and biology.

3. **Global attention (g)** — a set of g global tokens attend to all tokens and vice versa. Two variants:
   - **ITC (Internal Transformer Construction):** select g existing tokens as global
   - **ETC (Extended Transformer Construction):** add extra global tokens (e.g., CLS)

### Ablation (Base-size at seqlen 512)

| Model | MLM | SQuAD | MNLI |
|-------|-----|-------|------|
| BERT-base | 64.2 | 88.5 | 83.4 |
| Random (R) | 60.1 | 83.0 | 80.2 |
| Window (W) | 58.3 | 76.4 | 73.1 |
| R + W | 62.7 | 85.1 | 80.5 |
| **BigBird** | **64.2** | **88.5+** | **83.4+** |

## Theoretical Contributions

- **Universal Approximation (Theorem 1):** Any continuous sequence-to-sequence function can be approximated by a transformer using sparse attention containing the star graph (global token connected to all others). Proof uses a selective shift operator building a unique contextual mapping via multiple layers.

- **Turing Completeness (Theorem 3):** Encoder-decoder transformer with sparse attention can simulate any Turing machine. Symbol retrieval from tape history is done incrementally over multiple decoder steps.

- **Lower bound (Proposition 1):** For the "furthest vector" task, full attention solves it in O(1) layers, while any sparse attention with Õ(n) edges requires Ω̃(n^{1-o(1)}) layers (assuming Orthogonal Vector Conjecture). Shows sparsity has a fundamental cost.

## NLP Results

### Pretraining & MLM

Warm-started from RoBERTa checkpoint, trained on Books, CC-News, Stories, Wikipedia (>19B tokens).

| Model | BPC (Base) | BPC (Large) |
|-------|-----------|-------------|
| RoBERTa (seqlen 512) | 1.846 | 1.496 |
| Longformer (seqlen 4096) | 1.705 | 1.358 |
| BigBird-ITC | 1.678 | 1.456 |
| **BigBird-ETC** | **1.611** | **1.274** |

### Question Answering (Test sets)

| Task | Metric | Previous SOTA | BigBird-ETC |
|------|--------|--------------|-------------|
| Natural Questions (LA) | F1 | — | 73.9 |
| Natural Questions (SA) | F1 | — | 84.5 |
| TriviaQA | F1 | 90.3 | **92.4** |
| WikiHop | Acc | 78.3 | **82.3** |
| HotpotQA (Joint) | F1 | 77.1 | 77.8 |

### Summarization (ROUGE scores, long documents)

| Model | arXiv R-1 | arXiv R-2 | arXiv R-L | PubMed R-1 | PubMed R-2 | PubMed R-L |
|-------|-----------|-----------|-----------|------------|------------|------------|
| BigBird-RoBERTa (Base) | 41.22 | 16.43 | 36.96 | 43.70 | 19.32 | 39.99 |
| BigBird-Pegasus (Large) | **46.63** | **19.02** | **41.77** | **46.32** | **20.65** | **42.33** |

On BigPatent dataset, BigBird-Pegasus achieves R-1=60.64, R-2=42.46, R-L=50.01 — significant gains from longer context.

## Genomics Results

First use of attention-based contextual language models for DNA.

- **Pretraining MLM:** Byte-pair encoding tokenization of DNA (32K vocab, 8.78 bp/token). Human reference genome (GRCh37). BPC improved from 1.23 (BERT, seqlen 512) to 1.12 (BigBird, seqlen 4096).

- **Promoter Region Prediction:** F1=99.9 — near perfect, +4.3% over DeePromoter (95.6).

- **Chromatin-Profile Prediction:** 919 binary classifiers (TF binding, histone marks, DNase sensitivity). AUC: TF=96.1, HM=88.7, DHS=92.1. Significant improvement on histone marks (HM), known to have longer-range correlations.

## Key Takeaways

1. Linear-complexity attention matching full-attention expressiveness (universal approximation, Turing completeness)
2. Global tokens are both theoretically necessary and empirically valuable
3. Longer context (8x) yields substantial QA + summarization gains
4. Novel genomics applications demonstrate cross-domain applicability
5. Random attention component is unique vs. Longformer (window + global only), critical for information flow

Code: http://goo.gle/bigbird-transformer
