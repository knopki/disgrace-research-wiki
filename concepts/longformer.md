---
title: Longformer
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - model
  - architecture
  - optimization
  - inference
sources:
  - "[Longformer: The Long-Document Transformer](raw/papers/2020-04-beltagy-longformer/beltagy2020longformer.md)"
confidence: high
---

# Longformer

A [[transformer|transformer]] architecture introduced by **Iz Beltagy, Matthew E. Peters, and Arman Cohan** (Allen Institute for AI, 2020) that replaces the quadratic self-attention with a **linear-complexity attention pattern** combining local sliding windows and task-specific global attention. Longformer processes documents up to 4,096 tokens (8× [[bert|BERT]]'s 512 limit) without chunking or task-specific architectural workarounds, and up to 23K tokens for language modeling.

## Attention Pattern

Longformer's attention is a drop-in replacement for standard self-attention with three components:

**Sliding window** — each token attends to w/2 tokens on each side (typically w=512). Multiple stacked layers create a receptive field of l × w, similar to CNNs. Complexity: O(n × w).

**Dilated sliding window** — gaps of size d in the window analogously to dilated CNNs (van den Oord et al., 2016). Receptive field grows to l × d × w. Used only on higher layers with 2 heads; lower layers use full local context without dilation.

**Global attention** — few pre-selected tokens attend symmetrically to all tokens and vice versa. Task-specific:
- [CLS] token for classification
- Question tokens for QA
- No global attention for coreference resolution

Separate linear projections (Q_g, K_g, V_g) for global attention, initialized from sliding-window projections. The ablation study shows removing separate projections drops WikiHop accuracy by 1.6 points; removing both separate projections and global attention drops by 8.3 points — demonstrating both are essential ([Beltagy et al., 2020](raw/papers/2020-04-beltagy-longformer/beltagy2020longformer.md)).

## Three Implementations

| Implementation | Dilation | Speed | Memory | Used for |
|---------------|----------|-------|--------|----------|
| **Longformer-loop** | yes | unusably slow | efficient | testing only |
| **Longformer-chunk** | no | fast (vectorized) | 2× optimal | pretrain/finetune |
| **Longformer-cuda** | yes | fast (custom CUDA) | optimal | language modeling |

The CUDA kernel was built with TVM (Chen et al., 2018), a deep learning compiler that generates device-specific code from a high-level Python description of the banded matrix multiplication.

## Pretraining and Finetuning

Longformer is **not trained from scratch** — it continues MLM pretraining from the RoBERTa checkpoint. Key adaptation steps:

1. **Position embeddings** extended from 512 to 4,096 by **copying** RoBERTa's 512 embeddings multiple times (not random init). This preserves the strong local-attention bias [[bert|BERT]]'s heads learn (Clark et al., 2019). Copy init drops BPC from ~10.3 (random) to ~1.96 — the difference is dramatic.

2. **Staged training** — 5 phases: start with seqlen 2,048 and small windows, double both each phase, halve the learning rate. This lets the model learn local context first before being asked to use longer-range information.

3. **Finetuning on downstream tasks** — the attention mechanism is a drop-in replacement; no architecture changes needed beyond adding global attention on task-appropriate tokens.

## Results

### Long-Document Classification & QA

| Task | Metric | Longformer-base | RoBERTa-base | Longformer-large |
|------|--------|----------------|--------------|------------------|
| WikiHop | F1 | 75.0 | 72.4 | **81.9** (SOTA) |
| TriviaQA | F1 | 75.2 | 74.3 | **77.3** (SOTA) |
| HotpotQA | joint F1 | 64.4 | 63.5 | 73.2 |
| Hyperpartisan | F1 | **94.8** | 87.4 | — |

Gains are largest on tasks that genuinely need long context (WikiHop, Hyperpartisan). On TriviaQA, local context is often sufficient so the gap is smaller. On HotpotQA, supporting-fact supervision lets models find relevant context locally, reducing the long-context advantage.

### Character-Level Language Modeling

| Model | enwik8 BPC | Params |
|-------|-----------|--------|
| Transformer-XL (24L) | 0.99 | 277M |
| Sparse Transformer | 0.99 | ≈100M |
| **Longformer** | **0.99** | **102M** |

Longformer matches the best references with 2.7× fewer parameters than comparable Transformer-XL and roughly the same as Sparse Transformer.

### LED: Longformer-Encoder-Decoder

A seq2seq variant initialized from BART with:
- Encoder: Longformer's local + global attention
- Decoder: full self-attention to the entire encoded sequence
- Position embeddings extended to 16K tokens (copying BART's 1K embeddings 16×)

| Model | arXiv R-1 | arXiv R-2 | arXiv R-L |
|-------|-----------|-----------|-----------|
| LED-large (seqlen 16K) | **46.63** | **19.62** | **41.83** |
| [[big-bird|BigBird]] (seqlen 4K) | 46.63 | 19.02 | 41.77 |

LED slightly outperforms [[big-bird|BigBird]] (which uses task-specific Pegasus initialization) with no pretraining beyond BART init, purely by supporting longer inputs. Longer sequences consistently improve ROUGE scores.

## Ablation Insights

From WikiHop development set ablations (all Longformer-base, 5 epochs):

- **Longer sequences help:** seqlen 4,096 → 75.0, seqlen 2,048 → 73.1, seqlen 512 → 71.7
- **Global attention is critical:** removing both separate projections and global attention → 65.5 (-8.3)
- **MLM pretraining matters:** without it → 73.2 (-0.6)
- **Copy-initialized position embeddings are near-optimal:** training only extra position embeddings → 73.5 (-0.3)
- **Performance gains are NOT from extra pretraining:** Longformer at seqlen 512 with full n² attention → 71.7 (worse than RoBERTa's 72.4)

## Relationship to Other Concepts

- **[[big-bird|BigBird]]** — the closest contemporary (NeurIPS 2020, same venue). Both achieve O(n) attention with window + global components. BigBird uniquely adds random attention and provides theoretical guarantees (universal approximation, Turing completeness). On summarization, LED's advantage (seqlen 16K vs 4K) suggests input length is the binding constraint.

- **[[sparse-transformer|Sparse Transformer]]** — the most closely related predecessor; both use sparse attention patterns for long sequences. Sparse Transformer uses factorized strided/fixed patterns (O(n√n)), while Longformer uses sliding window + global attention (O(n)). Longformer's CUDA kernel was partly inspired by Sparse Transformer's BlockSparse approach but is more flexible and maintainable. Sparse Transformer was the first to demonstrate 1M+ token sequences (at heavily reduced capacity); Longformer focused on practical deployment at 4K-16K tokens with pretrained weights.

- **[[transformer|Transformer]]** — the base architecture Longformer modifies; Longformer's attention mechanism is a drop-in replacement requiring no other architecture changes.

- **[[kv-caching|KV Caching]]** — complementary inference optimisation; Longformer's O(n) attention per layer is compatible with KV caching during auto-regressive generation.
- **[[spargeattn|SpargeAttn]]** — a different paradigm: training-free dynamic sparse attention applied post-hoc to any model, unlike Longformer's built-in architectural sparse patterns. SpargeAttn achieves higher sparsity at long sequences (54% at 128K) but requires no model retraining.

- **[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]]** — both address transformer efficiency limits from different angles: Longformer via attention sparsity, Coconut via latent-space reasoning that sidesteps token-by-token generation.
