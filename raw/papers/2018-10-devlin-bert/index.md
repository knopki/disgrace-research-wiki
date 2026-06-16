---
source_url: https://arxiv.org/abs/1810.04805
ingested: 2026-06-17
title: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
authors: Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
date: 2018-10-11
description: Introduces BERT (Bidirectional Encoder Representations from Transformers), a language representation model pre-trained on unlabeled text using masked language modeling and next sentence prediction. Achieves state-of-the-art on eleven NLP tasks including GLUE (80.5%), SQuAD v1.1 (93.2 F1), and SQuAD v2.0 (83.1 F1).
site: arXiv
word_count: ~14,000
---

# BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

**Authors:** Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova

**Affiliation:** Google AI Language

**Venue:** NAACL 2019 (arXiv:1810.04805v2)

**PDF:** [1810.04805.pdf](1810.04805.pdf)

## Abstract

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pretrain deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications.

BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

## Key Contributions

1. Demonstrates importance of bidirectional pre-training for language representations — unlike unidirectional LM (OpenAI GPT) or shallow bidirectional concatenation (ELMo), BERT uses masked language models for deep bidirectional conditioning.
2. Shows that pre-trained representations "reduce the need for many heavily-engineered task-specific architectures" — first fine-tuning-based representation model to outperform task-specific architectures at scale.
3. Advances SOTA on eleven NLP tasks.

## Architecture

Encoder-only Transformer. Two model sizes:

| Model | Layers (L) | Hidden (H) | Heads (A) | FF filter (4H) | Params |
|-------|--------|--------|-------|-------|------------|
| BERT-Base | 12 | 768 | 12 | 3072 | 110M |
| BERT-Large | 24 | 1024 | 16 | 4096 | 340M |

Key: BERT-Base was chosen to have "the same model size as OpenAI GPT for comparison purposes." The only architectural difference is the attention masking — bidirectional self-attention vs left-context-only.

Activation: GELU. Learned positional embeddings. WordPiece tokenization (30K vocab). Input representation = sum of token embeddings + segment embeddings (A or B) + position embeddings.

## Pre-training

### Masked LM (MLM)
- Randomly mask 15% of WordPiece tokens per sequence
- Predict masked tokens via softmax over vocabulary (cross-entropy)
- To mitigate pre-train/fine-tune mismatch: 80% [MASK], 10% random token, 10% unchanged
- Random replacement "does not seem to harm the model's language understanding capability" because it only affects 1.5% of all tokens

### Next Sentence Prediction (NSP)
- Binary: predict if sentence B follows A (50% IsNext, 50% random NotNext)
- [CLS] final hidden state C used for classification
- Model achieves 97-98% accuracy on NSP
- The paper explicitly notes C "is not a meaningful sentence representation without fine-tuning, since it was trained with NSP"
- NSP removal hurts performance significantly on QNLI, MNLI, SQuAD 1.1

### Pre-training Data
"It is critical to use a document-level corpus rather than a shuffled sentence-level corpus" — BooksCorpus (800M words) + English Wikipedia (2,500M words), extracting only text passages, ignoring lists, tables, headers.

## Training Details

**Pre-training:** 1,000,000 steps. Adam (lr=1e-4, β₁=0.9, β₂=0.999), L2 weight decay 0.01. Dropout 0.1 everywhere. Batch size 256 sequences × 512 tokens = 128K tokens/batch.

BERT-Base: 4 Cloud TPUs (16 TPU chips), ~4 days. BERT-Large: 16 Cloud TPUs (64 TPU chips), ~4 days.

**Fine-tuning:** "All of the results in the paper can be replicated in at most 1 hour on a single Cloud TPU."
- GLUE: batch 32, 3 epochs, lr from {5e-5, 4e-5, 3e-5, 2e-5}
- SQuAD v1.1: 3 epochs, lr=5e-5, batch 32
- SQuAD v2.0: 2 epochs, lr=5e-5, batch 48
- SWAG: 2 epochs, lr=5e-5, batch 48
- BERT-Large fine-tuning unstable on small datasets → random restarts with different data shuffling and classifier initialization, selecting best on Dev set

## Results

### GLUE (Table 1)

| System | MNLI-m | QQP | QNLI | SST-2 | CoLA | STS-B | MRPC | RTE | Avg |
|--------|--------|-----|------|-------|------|-------|------|-----|-----|
| OpenAI GPT | 82.1 | 70.3 | 87.4 | 91.3 | 45.4 | 80.0 | 82.3 | 56.0 | 75.1 |
| BERT-Base | 84.6 | 71.2 | 90.5 | 93.5 | 52.1 | 85.8 | 88.9 | 66.4 | 79.6 |
| BERT-Large | 86.7 | 72.1 | 92.7 | 94.9 | 60.5 | 86.5 | 89.3 | 70.1 | **82.1** |

Official GLUE score (excluding WNLI): BERT-Large 80.5 (OpenAI GPT: 72.8). +4.5 avg over GPT for Base (+7.0 for Large).

BERT-Base vs OpenAI GPT: same model size, only attention masking differs — the gain is attributable almost entirely to bidirectionality.

### SQuAD v1.1

Single BERT-Large with TriviaQA: Test F1 **93.2** (top ensemble system: 91.7). "Single BERT model outperforms the top ensemble system in terms of F1 score."

### SQuAD v2.0

Treats unanswerable questions as span starting and ending at [CLS] token. Compares null-span score to non-null span with threshold τ selected on Dev. Test F1 **83.1** (+5.1 over prior SOTA).

### SWAG

BERT-Large Test Acc **86.3%** (human expert: 85.0%, 5 crowd annotations: 88.0%).

### CoNLL-2003 NER (Feature-based)

Concatenating top 4 hidden layers (without any fine-tuning of BERT) → **96.1 Dev F1** vs BERT-Large fine-tuned → **96.6 Dev F1** — only 0.3 F1 gap.

## Ablation Studies

### Effect of Bidirectionality (Section 5.1)
- MLM vs LTR (left-to-right, no NSP): MLM dominates all tasks
- Adding BiLSTM on top of LTR helps SQuAD but "results are still far worse" than bidirectional
- BiLSTM hurts GLUE performance
- NSP removal hurts QNLI, MNLI, SQuAD 1.1 significantly

### Effect of Model Size (Section 5.2)
"First work to demonstrate convincingly that scaling to extreme model sizes also leads to large improvements on very small scale tasks, provided that the model has been sufficiently pre-trained." Larger → strictly better on all 4 GLUE tasks tested, including MRPC (3,600 examples).

### Feature-based Approach (Section 5.3)
BERT works effectively as frozen feature extractor — concat top 4 hidden layers feeds into 2-layer 768D BiLSTM → within 0.3 F1 of full fine-tuning.

## Limitations (from paper)
- MLM is less sample-efficient per step than standard LM (only 15% prediction)
- Pre-train/fine-tune discrepancy from [MASK]
- 512-token max sequence length
- Encoder-only, not generative


