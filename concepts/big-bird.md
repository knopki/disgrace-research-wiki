---
title: BigBird
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - model
  - architecture
  - optimization
  - inference
sources:
  - "[Big Bird: Transformers for Longer Sequences](raw/papers/2020-07-zaheer-big-bird/zaheer2020bigbird.md)"
confidence: high
---

# BigBird

A sparse-attention [[transformer|transformer]] architecture introduced by **Manzil Zaheer et al.** (Google Research, NeurIPS 2020) that reduces quadratic self-attention to **linear complexity** by combining three complementary attention patterns: random, window, and global. BigBird is the first sparse-attention model with **proven universal approximation and Turing completeness**, matching the theoretical expressiveness of full-attention transformers.

## Attention Mechanism

BigBird's attention graph combines three sparse patterns, each O(n):

1. **Random attention (r)** — each query attends to r randomly chosen keys (Erdős–Rényi graph). Ensures short average path length (~log n) and fast information flow across the sequence.

2. **Window attention (w)** — each token attends to w/2 neighbors left and right (sliding window). Captures locality critical for NLP and biological sequences.

3. **Global attention (g)** — a set of g tokens attend to all tokens and vice versa. Two construction variants:
   - **ITC (Internal Transformer Construction):** select g existing tokens (e.g., [CLS]) as global
   - **ETC (Extended Transformer Construction):** add g extra global tokens — consistently outperforms ITC

The ablation (Table 1) shows that **none of the three components alone is sufficient** — random-only (60.1 MLM) or window-only (58.3) fall far short of BERT (64.2), but the full combination matches BERT exactly at seqlen 512 while being O(n) instead of O(n²).

## Theoretical Contributions

BigBird is the first sparse-attention model with rigorous theoretical guarantees matching full attention:

- **Universal Approximation (Theorem 1):** Any continuous sequence-to-sequence function can be approximated by a [[transformer|transformer]] whose attention graph contains a star graph (a global token connected to all others). Proved via a sparse shift operator that builds a unique contextual mapping using multiple layers and the global token.

- **Turing Completeness (Theorem 3):** An encoder-decoder [[transformer|transformer]] with sparse attention can simulate any Turing machine. The key challenge — symbol retrieval from tape history — is solved incrementally over multiple decoder steps using associativity of min/argmin, in contrast to full attention's direct lookup.

- **Lower Bound (Proposition 1):** For the task of finding the furthest vector for each input vector, full attention solves it in O(1) layers, but any sparse attention with Õ(n) edges requires Ω̃(n^{1-o(1)}) layers (assuming Orthogonal Vector Conjecture). This demonstrates sparsity has a fundamental cost — more layers are needed for global comparison tasks.

## NLP Results

### Masked Language Modeling

Warm-started from RoBERTa; trained on Books, CC-News, Stories, Wikipedia (>19B tokens).

| Model | BPC (Base) | BPC (Large) |
|-------|-----------|-------------|
| RoBERTa (seqlen 512) | 1.846 | 1.496 |
| Longformer (seqlen 4096) | 1.705 | 1.358 |
| BigBird-ITC | 1.678 | 1.456 |
| **BigBird-ETC** | **1.611** | **1.274** |

### Question Answering (Test set, single model)

| Task | Metric | Previous SOTA | BigBird-ETC |
|------|--------|--------------|-------------|
| Natural Questions (LA) | F1 | — | **73.9** |
| Natural Questions (SA) | F1 | — | 84.5 |
| TriviaQA | F1 | 90.3 | **92.4** |
| WikiHop | Acc | 78.3 | **82.3** |
| HotpotQA (Joint) | F1 | 77.1 | 77.8 |

### Summarization (ROUGE, BigBird-Pegasus Large)

| Dataset | R-1 | R-2 | R-L |
|---------|-----|-----|-----|
| arXiv | 46.63 | 19.02 | 41.77 |
| PubMed | 46.32 | 20.65 | 42.33 |
| BigPatent | **60.64** | **42.46** | **50.01** |

### Document Classification

Improvements are most significant on longer documents: arXiv +5%, Hyperpartisan +4% over RoBERTa. On short tasks (GLUE), matches full-attention models.

## Genomics Applications

A novel contribution — BigBird is the first attention-based contextual language model for DNA.

- **DNA tokenization:** [[byte-pair-encoding|Byte-pair encoding]] with 32K vocab (~8.78 bp/token)
- **Pretraining:** Human reference genome (GRCh37) with MLM objective
- **BPC:** 1.12 at seqlen 4096 vs BERT's 1.23 at seqlen 512
- **Promoter region prediction:** F1=99.9 (+4.3% over DeePromoter's 95.6)
- **Chromatin-profile prediction:** AUC improvements on histone marks (88.7 vs 85.6), which have long-range correlations

## Relationship to Other Concepts

- **[[sparse-transformer|Sparse Transformer]]** — the foundational sparse-attention work. Sparse Transformer proved feasibility of >1M token sequences with O(n√n) factorized patterns; BigBird achieved O(n) with random + window + global and proved this preserves universal approximation and Turing completeness.

- **[[longformer|Longformer]]** — the most closely related contemporary work. Both achieve O(n) attention with window + global components. BigBird uniquely adds random attention and provides theoretical guarantees (universal approximation, Turing completeness) that Longformer lacked. On summarization, LED (seqlen 16K) slightly outperforms BigBird-Pegasus (seqlen 4K), suggesting input length is the binding constraint for both.

- **[[transformer|Transformer]]** — the base architecture. BigBird's attention mechanism is a drop-in replacement for standard self-attention, requiring no other architecture changes.

- **[[kv-caching|KV Caching]]** — complementary inference optimisation compatible with BigBird's O(n) attention.

- **[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]]** — both address transformer efficiency: BigBird via attention sparsity, Coconut via latent-space reasoning.
- **[[spargeattn|SpargeAttn]]** — training-free post-hoc sparse attention operator, orthogonal to BigBird's architectural approach. SpargeAttn can accelerate any pretrained model including BigBird-style architectures.

## Significance & Legacy

- **First sparse-attention model with full theoretical guarantees** (universal approximation + Turing completeness) matching quadratic attention
- **Established the three-component sparse pattern** (random + window + global) that later architectures build on
- **Introduced attention-based genomics modeling** — cross-domain transfer from NLP to DNA sequence analysis, using [[byte-pair-encoding|BPE]] for nucleotide tokenization
- The theoretical proof that global tokens (O(1)) are **sufficient** to preserve universal approximation informed subsequent efficient-transformer design

Code: http://goo.gle/bigbird-transformer
