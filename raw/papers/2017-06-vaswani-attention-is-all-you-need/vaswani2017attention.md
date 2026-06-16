---
title: "Attention Is All You Need"
source_url: https://arxiv.org/abs/1706.03762
date: 2017-06-12
authors: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin"
venue: "NIPS 2017 (31st Conference on Neural Information Processing Systems)"
ingested: 2026-06-16
---

Full text: [[1706.03762.pdf]] (15 pages, v7 Aug 2023)

## Abstract

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

## Key Contributions

- **Scaled Dot-Product Attention:** `Attention(Q,K,V) = softmax(QK^T / √d_k)V` — scaling by `1/√d_k` prevents softmax saturation for large d_k
- **Multi-Head Attention:** h=8 parallel heads, d_k = d_v = d_model / h = 64, total cost similar to single-head attention
- **Positional Encoding:** sinusoidal functions P E(pos,2i) = sin(pos/10000^{2i/d_model}), P E(pos,2i+1) = cos(pos/10000^{2i/d_model}) for order information without recurrence
- **Encoder-Decoder Stack:** N=6 identical layers each; each layer has multi-head self-attention + position-wise FFN with residual connections and layer normalization
- **Position-wise FFN:** two linear transformations with ReLU, d_model=512, d_ff=2048
- **No recurrence, no convolution** — first transduction model relying entirely on self-attention

## Results

| Task | Model | BLEU | Training Cost |
|------|-------|------|---------------|
| WMT 2014 EN-DE | Transformer (base) | 27.3 | 3.3×10^18 FLOPs |
| WMT 2014 EN-DE | Transformer (big) | 28.4 | 2.3×10^19 FLOPs |
| WMT 2014 EN-FR | Transformer (big) | 41.8 | 2.3×10^19 FLOPs |

Training: base model — 100K steps (~12h) on 8×P100 GPUs; big model — 300K steps (~3.5 days). Adam optimizer with custom learning rate schedule (linear warmup + inverse square root decay), residual dropout P_drop=0.1, label smoothing ε_ls=0.1.

## Significance

The Transformer established self-attention as the dominant paradigm in sequence modeling, superseding RNNs and CNNs for NLP. It became the foundation of GPT, BERT, T5, and virtually all subsequent large language models. The paper introduced Key/Value/Query attention formulation, pre-LN residual placement, tied embedding weights, and sinusoidal positional encodings — all still in wide use.
