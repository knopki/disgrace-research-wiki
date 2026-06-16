---
title: BERT
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [model, architecture, training, fine-tuning]
sources:
  - "[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](raw/papers/2018-10-devlin-bert/index.md)"
---

# BERT

**BERT (Bidirectional Encoder Representations from Transformers)** — language representation model introduced by Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova (Google AI Language, NAACL 2019). It demonstrated that deep bidirectional pre-training with [[transformer|Transformer]] encoders produces transferable representations that dramatically outperform unidirectional approaches, establishing the pre-train/fine-tune paradigm that dominated NLP for years ([Devlin et al., 2019](raw/papers/2018-10-devlin-bert/index.md)).

## Architecture

BERT is an encoder-only Transformer — it processes input bidirectionally, unlike decoder-only models ([[lstm|GPT-style]]) which are unidirectional. The paper's key architectural comparison: BERT-Base is **identical to OpenAI GPT in model size apart from the attention masking** — making it a controlled experiment on the value of bidirectionality.

| Model | Layers (L) | Hidden (H) | Heads (A) | Feed-forward (4H) | Parameters |
|-------|--------|--------|-------|-------|------------|
| BERT-Base | 12 | 768 | 12 | 3072 | 110M |
| BERT-Large | 24 | 1024 | 16 | 4096 | 340M |

Key architectural choices:
- **GELU activation** — smoother gradient flow than ReLU
- **Learned positional embeddings** (vs sinusoidal in the original Transformer)
- **WordPiece tokenization** with 30K vocabulary
- [[residual-connection|Residual connections]] and layer normalization on every sub-layer
- **Input representation** is the sum of three embeddings: token embeddings + segment embeddings (sentence A/B) + position embeddings (Devlin et al., 2019, Figure 2)

The largest Transformer previously in the literature was (L=64, H=512, A=2) with 235M parameters — BERT-Large at 340M was a significant scale jump.

## Pre-training Objectives

Two unsupervised tasks, trained jointly on unlabeled text:

### Masked Language Model (MLM)

Inspired by the Cloze task. 15% of input WordPiece tokens are randomly chosen for prediction. To bridge the pre-train/fine-tune gap (the [MASK] token never appears during fine-tuning), a three-way strategy:

- 80% of chosen tokens → `[MASK]`
- 10% → random token
- 10% → unchanged (biases representation toward the observed word)

The model predicts the original vocabulary id for each masked position using cross-entropy. Because random replacement only affects ~1.5% of all tokens (10% of 15%), "this does not seem to harm the model's language understanding capability." Only 15% of tokens are predicted per batch, so MLM requires more pre-training steps than standard LM.

The Transformer encoder "does not know which words it will be asked to predict or which have been replaced by random words, so it is forced to keep a distributional contextual representation of every input token."

### Next Sentence Prediction (NSP)

Binary classification: given sentences A and B, predict whether B follows A in the original corpus (50% IsNext, 50% random NotNext). The [CLS] token's final hidden state C is fed to a classifier. The model achieves 97-98% accuracy on NSP.

**Critical corpus choice:** "It is critical to use a document-level corpus rather than a shuffled sentence-level corpus such as the Billion Word Benchmark in order to extract long contiguous sequences." — pre-training uses BooksCorpus (800M words) + English Wikipedia (2,500M words).

The paper's own ablation (Section 5.1) shows NSP removal **hurts performance significantly** on QNLI, MNLI, and SQuAD 1.1. Later work showed that with different hyperparameters, removing NSP produces comparable results; the paper's finding held for its training setup.

## Training

| Detail | Value |
|--------|-------|
| Pre-training data | BooksCorpus (800M words) + English Wikipedia (2,500M words), document-level only |
| BERT-Base hardware | 4 Cloud TPUs (16 TPU chips), ~4 days |
| BERT-Large hardware | 16 Cloud TPUs (64 TPU chips), ~4 days |
| Batch size | 256 sequences × 512 tokens = 128K tokens/batch |
| Optimizer | Adam (lr=1e-4, β₁=0.9, β₂=0.999), L2 weight decay 0.01 |
| Dropout | 0.1 on all layers, attention, and embeddings |
| Pre-training steps | 1,000,000 |
| Max sequence length | 512 tokens |

Fine-tuning is "relatively inexpensive" — all results in the paper "can be replicated in at most 1 hour on a single Cloud TPU, or a few hours on a GPU." Per-task details:
- **GLUE:** batch size 32, 3 epochs, learning rate selected from {5e-5, 4e-5, 3e-5, 2e-5} on Dev set
- **SQuAD v1.1:** 3 epochs, lr=5e-5, batch 32
- **SQuAD v2.0:** 2 epochs, lr=5e-5, batch 48 (no TriviaQA augmentation)
- **SWAG:** 2 epochs, lr=5e-5, batch 48
- BERT-Large fine-tuning was "sometimes unstable on small datasets" — authors ran several random restarts with different data shuffling and classifier initialization, selecting the best on Dev set.

## Results

SOTA on **eleven NLP tasks** at time of publication ([Devlin et al., 2019](raw/papers/2018-10-devlin-bert/index.md)):

### GLUE (Table 1)

| System | MNLI-m | QQP | QNLI | SST-2 | CoLA | STS-B | MRPC | RTE | **Avg** |
|--------|--------|-----|------|-------|------|-------|------|-----|---------|
| Pre-OpenAI SOTA | 80.6 | 66.1 | 82.3 | 93.2 | 35.0 | 81.0 | 86.0 | 61.7 | 74.0 |
| OpenAI GPT | 82.1 | 70.3 | 87.4 | 91.3 | 45.4 | 80.0 | 82.3 | 56.0 | 75.1 |
| BERT-Base | 84.6 | 71.2 | 90.5 | 93.5 | 52.1 | 85.8 | 88.9 | 66.4 | 79.6 |
| BERT-Large | 86.7 | 72.1 | 92.7 | 94.9 | 60.5 | 86.5 | 89.3 | 70.1 | **82.1** |

Official GLUE leaderboard score (excluding WNLI): **80.5** — 7.7% absolute improvement over prior SOTA (= OpenAI GPT 72.8).

BERT-Base and OpenAI GPT are "nearly identical in terms of model architecture apart from the attention masking" — the +4.5 average accuracy gain is attributable almost entirely to bidirectionality.

### SQuAD

| Dataset | Metric | BERT-Large | Previous SOTA | Gain |
|---------|--------|------------|---------------|------|
| SQuAD v1.1 | Test F1 | **93.2** | 91.7 (ensemble nlnet) | +1.5 |
| SQuAD v2.0 | Test F1 | **83.1** | 78.0 (OpenAI GPT) | +5.1 |

SQuAD v2.0 approach: treat unanswerable questions as span starting/ending at `[CLS]` token, compare null-span score to best non-null span with threshold τ selected on Dev set.

### SWAG

| Model | Dev Acc | Test Acc |
|-------|---------|----------|
| BERT-Large | **86.6** | **86.3** |
| Human (expert) | — | 85.0 |
| Human (5 annotations) | — | 88.0 |

### CoNLL-2003 NER (Feature-based)

Feature-based approach — extracting fixed BERT representations without fine-tuning, feeding into a randomly initialized 2-layer 768D BiLSTM:

| Configuration | Dev F1 | Test F1 |
|---------------|--------|---------|
| BERT-Large (fine-tuned) | **96.6** | **92.8** |
| BERT-Base concat top 4 hidden layers | 96.1 | 92.4 |
| BERT-Base weighted sum last 4 hidden | 95.9 | 92.3 |
| BERT-Base embeddings only | 91.0 | — |

Concatenating the top 4 hidden layers comes within **0.3 F1** of full fine-tuning — demonstrating BERT works effectively in either paradigm.

## Ablation Studies

### Effect of Bidirectionality (Section 5.1)

Comparing MLM vs LTR (left-to-right) model, matched on architecture and training data:
- MLM outperforms LTR on **all** tasks
- SQuAD gap is largest — intuitively, "a LTR model will perform poorly at token predictions, since the token-level hidden states have no right-side context"
- Adding a **randomly initialized BiLSTM** on top of LTR helps SQuAD but "results are still far worse than those of the pre-trained bidirectional models" and BiLSTM hurts GLUE performance
- NSP removal hurts QNLI, MNLI, and SQuAD 1.1 significantly

### Effect of Model Size (Section 5.2)

"First work to demonstrate convincingly that scaling to extreme model sizes also leads to large improvements on **very small scale tasks**, provided that the model has been sufficiently pre-trained." Larger BERT models → strict accuracy improvement across all four GLUE tasks tested, including MRPC (only 3,600 training examples).

### Masking Procedure (Appendix C.2)

Full strategy (80% [MASK], 10% random, 10% unchanged) beats:
- Always replacing with [MASK] (creates too large pre-train/fine-tune mismatch)
- Replacing only with [MASK] or random (no unchanged → context less robust)

## Impact and Legacy

- Established the **encoder-only Transformer** as a viable architectural family alongside decoder-only (GPT) and encoder-decoder (T5/BART) designs
- The [[positional-encoding|positional encoding]] and pre-training setup influenced virtually all subsequent encoder models
- **No [[kv-caching|KV caching]] needed** — BERT processes the full input in one forward pass (non-autoregressive), making it faster for understanding tasks but unsuitable for generation
- The 512-token limit motivated sparse-attention successors: [[longformer|Longformer]], [[big-bird|BigBird]], [[sparse-transformer|Sparse Transformer]]
- [[flash-attention|FlashAttention]] demonstrated 15% training speedup on BERT-Large at 512 sequence length
- MLM pre-training was adapted by RoBERTa, ALBERT, DistilBERT, ELECTRA, and encoder-decoder models (T5, BART)
- The pre-train/fine-tune paradigm showed that "pre-trained representations reduce the need for many heavily-engineered task-specific architectures" — one of the paper's stated contributions

## Limitations

- **Pre-train/fine-tune gap:** The `[MASK]` token appears during pre-training but never during fine-tuning (partially mitigated by 80/10/10 strategy)
- **Computationally expensive:** MLM only uses 15% of tokens per step for prediction — less efficient per-step than autoregressive LM
- **Not generative:** Encoder-only architecture produces fixed representations, not token sequences
- **Context limit:** 512 tokens restricts long-document processing without chunking
- **NSP as training signal:** The paper itself notes the [CLS] vector C "is not a meaningful sentence representation without fine-tuning, since it was trained with NSP"

For comparison of attention mechanisms across long-range models, see [[sparse-transformer|Sparse Transformer]].
