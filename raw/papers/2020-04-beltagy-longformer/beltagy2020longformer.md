---
source_url: https://arxiv.org/abs/2004.05150
ingested: 2026-06-17
---

# Longformer: The Long-Document Transformer

**Authors:** Iz Beltagy, Matthew E. Peters, Arman Cohan (equal contribution)
**Affiliation:** Allen Institute for Artificial Intelligence (AI2)
**Venue:** arXiv preprint, 2004.05150v2 (Dec 2, 2020)

Full text: [2004.05150.pdf](raw/papers/2020-04-beltagy-longformer/2004.05150.pdf) (17 pages)

## Abstract

> Transformer-based models are unable to process long sequences due to their self-attention operation, which scales quadratically with the sequence length. To address this limitation, we introduce the Longformer with an attention mechanism that scales linearly with sequence length, making it easy to process documents of thousands of tokens or longer. Longformer's attention mechanism is a drop-in replacement for the standard self-attention and combines a local windowed attention with a task motivated global attention. Following prior work on long-sequence transformers, we evaluate Longformer on character-level language modeling and achieve state-of-the-art results on text8 and enwik8. In contrast to most prior work, we also pretrain Longformer and finetune it on a variety of downstream tasks. Our pretrained Longformer consistently outperforms RoBERTa on long document tasks and sets new state-of-the-art results on WikiHop and TriviaQA. We finally introduce the Longformer-Encoder-Decoder (LED), a Longformer variant for supporting long document generative sequence-to-sequence tasks, and demonstrate its effectiveness on the arXiv summarization dataset.

## Key Results

| Task | Metric | Longformer-base | RoBERTa-base | Longformer-large |
|------|--------|----------------|--------------|------------------|
| WikiHop | F1 | 75.0 | 72.4 | 81.9 (SOTA) |
| TriviaQA | F1 | 75.2 | 74.3 | 77.3 (SOTA) |
| HotpotQA | joint F1 | 64.4 | 63.5 | 73.2 |
| OntoNotes (coref) | avg F1 | 78.6 | 78.4 | — |
| IMDB | accuracy | 95.7 | 95.3 | — |
| Hyperpartisan | F1 | 94.8 | 87.4 | — |
| text8 | BPC | — | — | 1.10 (small model) |
| enwik8 | BPC | — | — | 0.99 (small), 0.99 (large 102M) |

| Model | enwik8 BPC | Params |
|-------|-----------|--------|
| Transformer-XL (24L) | 0.99 | 277M |
| Sparse Transformer | 0.99 | ≈100M |
| Compressive Transformer | 0.97 | 277M |
| **Longformer** | **0.99** | **102M** |

| LED model | arXiv R-1 | arXiv R-2 | arXiv R-L |
|-----------|-----------|-----------|-----------|
| LED-large (seqlen 4096) | 44.40 | 17.94 | 39.76 |
| LED-large (seqlen 16384) | **46.63** | **19.62** | **41.83** |

## Attention Mechanism

Three patterns combined:
1. **Sliding window** — each token attends to w/2 tokens on each side (O(n × w))
2. **Dilated sliding window** — gaps of size d in the window to increase receptive field without extra compute (receptive field = l × d × w)
3. **Global attention** — few pre-selected tokens (task-specific: [CLS] for classification, question tokens for QA) attend to all tokens and vice versa

Three implementations: loop (testing only), chunks (vectorized, pretrain/finetune), CUDA kernel via TVM (LM experiments).

## Additional Details

- Pretrained from RoBERTa checkpoint with continued MLM on a long-document corpus (Books, Wikipedia, subset of Realnews >1200 tokens, Stories)
- Position embeddings extended from 512 to 4096 by copying the 512 embeddings multiple times
- Staged training: 5 phases, starting at seqlen 2048/window 32, ending at seqlen 23040/window 512→8192
- LED initialized from BART, extends position embeddings to 16K tokens
- Code: https://github.com/allenai/longformer
