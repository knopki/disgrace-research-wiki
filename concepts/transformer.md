---
title: Transformer
created: 2026-06-17
updated: 2026-06-16
type: concept
tags:
  - model
  - architecture
  - benchmark
sources:
  - "[Attention Is All You Need](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md)"
  - "[История ИИ: бунтари, гении и научные войны](raw/articles/2025-07-03-ivanov-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/ivanoc2025istoriya.md)"
  - "[Позиционные кодировки: «объемное зрение» GPT и секреты AI-агентов](raw/articles/2025-07-04-ivanov-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/ivanoc2025encodings.md)"
confidence: high
---

## Definition

The **Transformer** is a neural network architecture introduced in the 2017 paper **"Attention Is All You Need"** by **Ashish Vaswani**, **Noam Shazeer**, and six other Google researchers. It replaces sequential recurrence (as in [[lstm|LSTM]]) with a parallelisable **self-attention mechanism**, processing all tokens simultaneously rather than one at a time.

## Architecture

The Transformer follows an encoder-decoder structure with N=6 identical layers on each side. Both encoder and decoder use stacked self-attention and position-wise feed-forward networks.

### Encoder

Each of the 6 encoder layers has two sub-layers:
1. **Multi-head self-attention** — h=8 parallel heads, each with d_k=d_v=d_model/h=64
2. **Position-wise feed-forward network** — two linear transformations with ReLU: FFN(x) = max(0, xW_1 + b_1)W_2 + b_2, with inner dimension d_ff=2048 and outer d_model=512

Each sub-layer employs a **residual connection** followed by **layer normalization**: LayerNorm(x + Sublayer(x)). All sub-layers and embedding layers produce outputs of dimension d_model=512.

### Decoder

Each of the 6 decoder layers adds a third sub-layer — **encoder-decoder attention** — that performs multi-head attention over the encoder output. The decoder's self-attention is **masked** to prevent positions from attending to subsequent positions, preserving the auto-regressive property.

### Attention

- **Scaled Dot-Product Attention:** Attention(Q,K,V) = softmax(QK^T / √d_k)V. Scaling by 1/√d_k counteracts softmax saturation at large d_k.
- **Three attention types:** encoder-decoder attention (queries from decoder, keys/values from encoder), encoder self-attention, and decoder masked self-attention. ([Vaswani et al., 2017](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md))

### Positional Encoding

Since the model has no recurrence, sinusoidal positional encodings are added to the input embeddings at the bottom of both encoder and decoder stacks. PE(pos,2i) = sin(pos/10000^{2i/d_model}), PE(pos,2i+1) = cos(pos/10000^{2i/d_model}). The wavelengths form a geometric progression from 2π to 10000·2π, allowing the model to extrapolate to longer sequences. ([Vaswani et al., 2017](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md))

The Transformer synthesised several prior innovations:

- **[[perceptron|Perceptron]]** — the fundamental neuron model (Rosenblatt, 1957)
- **[[residual-connection|Residual connections]]** — from ResNet (He et al., 2015), enabling deep stacks
- **Self-attention** — refined from Bahdanau attention and correlation-of-vectors ideas from [[lstm|LSTM]] research
- **Positional encoding** — sine/cosine functions that give each token a "semantic coordinate" in the embedding space, preserving order information without sequential processing

The result: a fully parallelisable architecture where every token can directly attend to every other token in a single forward pass. ([Ivanov, 2025](raw/articles/2025-07-03-ivanov-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/ivanoc2025istoriya.md))

## Key Innovations

- **Self-attention** — each token computes relevance scores against all other tokens, enabling the model to weigh context appropriately
- **Multi-head attention** — multiple attention mechanisms run in parallel, each learning different relationship types
- **Positional encoding** — sinusoidal functions encode position directly into the embedding, eliminating the need for sequential processing
- **Parallelisation** — full sequence processed in one pass, unlike RNNs/LSTMs which process token by token

## Training

The base model was trained for 100,000 steps (~12 hours) on a single machine with 8 NVIDIA P100 GPUs. The big model trained for 300,000 steps (~3.5 days). Optimizer: Adam (β₁=0.9, β₂=0.98, ε=10⁻⁹) with a custom learning rate schedule — linear warmup for 4000 steps followed by inverse square root decay. Regularization: residual dropout P_drop=0.1, label smoothing ε_ls=0.1. Beam search with beam size 4 and length penalty α=0.6. ([Vaswani et al., 2017](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md))

### Machine Translation Results

| Model | EN-DE BLEU | EN-FR BLEU | Training Cost EN-DE | Training Cost EN-FR |
|-------|-----------|-----------|-------------------|-------------------|
| Transformer (base) | 27.3 | 38.1 | 3.3×10¹⁸ FLOPs | 2.3×10¹⁹ FLOPs |
| Transformer (big) | **28.4** | **41.8** | 2.3×10¹⁹ FLOPs | 2.3×10¹⁹ FLOPs |

The big model outperformed all previously published models and ensembles on EN-DE (by >2 BLEU) and established a new single-model SOTA on EN-FR at less than 1/4 the training cost of the previous best model. ([Vaswani et al., 2017](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md))

### English Constituency Parsing

A 4-layer Transformer (d_model=1024) trained on WSJ (40K sentences) achieved 91.3 F1, outperforming all previously reported models except the RNN Grammar ([Dyer et al., 2016]). Semi-supervised training on 17M sentences reached 92.7 F1, demonstrating generalization beyond translation. ([Vaswani et al., 2017](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md))

## Significance

- Foundation of all major modern language models: GPT, BERT, Claude, Gemini, LLaMA
- Enabled scaling to unprecedented sizes (hundreds of billions of parameters)
- Removed the sequential bottleneck of [[lstm|LSTM]], making massively parallel training on GPUs feasible
- The "Attention Is All You Need" paper is one of the most cited in ML history

## Limitations

- Quadratic memory cost in sequence length (O(n²) attention) — partially addressed by [[sparse-transformer|Sparse Transformer]] architectures and later efficient-attention variants
- No inherent notion of order (positional encoding is added externally)
- Requires enormous amounts of training data and compute

## Cross-Links

- [[backpropagation|Backpropagation]] — the training algorithm that makes Transformer learning possible
- [[lstm|LSTM]] — the architecture Transformers superseded
- [[residual-connection|Residual Connection]] — essential architectural component enabling depth
- [[perceptron|Perceptron]] — the foundational unit of all neural networks
- [[superposition|Superposition]] — the feature-representation phenomenon that emerges in trained Transformers
- [[positional-encoding|Positional Encoding]] — the component that gives tokens their "semantic coordinates," enabling the Transformer to process text in parallel
- [[semantic-anchors|Semantic Anchors]] — a technique exploiting a practical consequence of positional encoding for AI-assisted code editing
- [[kv-caching|KV Caching]] — inference optimisation that caches Key and Value states during auto-regressive generation, avoiding redundant recomputation
- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — a training paradigm that exploits the transformer's ability to process any vector as input, not just token embeddings