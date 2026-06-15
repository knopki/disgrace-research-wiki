---
title: Transformer
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [model, architecture, benchmark]
sources:
  - "[История ИИ: бунтари, гении и научные войны](raw/articles/2025-07-03-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/index.md)"
  - "[Позиционные кодировки: «объемное зрение» GPT и секреты AI-агентов](raw/articles/2025-07-04-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/index.md)"
confidence: high
---

## Definition

The **Transformer** is a neural network architecture introduced in the 2017 paper **"Attention Is All You Need"** by **Ashish Vaswani**, **Noam Shazeer**, and six other Google researchers. It replaces sequential recurrence (as in [[lstm|LSTM]]) with a parallelisable **self-attention mechanism**, processing all tokens simultaneously rather than one at a time.

## Architecture

The Transformer synthesised several prior innovations:

- **[[perceptron|Perceptron]]** — the fundamental neuron model (Rosenblatt, 1957)
- **[[residual-connection|Residual connections]]** — from ResNet (He et al., 2015), enabling deep stacks
- **Self-attention** — refined from Bahdanau attention and correlation-of-vectors ideas from [[lstm|LSTM]] research
- **Positional encoding** — sine/cosine functions that give each token a "semantic coordinate" in the embedding space, preserving order information without sequential processing

The result: a fully parallelisable architecture where every token can directly attend to every other token in a single forward pass. ^[raw/articles/2025-07-03-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/index.md]

## Key Innovations

- **Self-attention** — each token computes relevance scores against all other tokens, enabling the model to weigh context appropriately
- **Multi-head attention** — multiple attention mechanisms run in parallel, each learning different relationship types
- **Positional encoding** — sinusoidal functions encode position directly into the embedding, eliminating the need for sequential processing
- **Parallelisation** — full sequence processed in one pass, unlike RNNs/LSTMs which process token by token

## Significance

- Foundation of all major modern language models: GPT, BERT, Claude, Gemini, LLaMA
- Enabled scaling to unprecedented sizes (hundreds of billions of parameters)
- Removed the sequential bottleneck of [[lstm|LSTM]], making massively parallel training on GPUs feasible
- The "Attention Is All You Need" paper is one of the most cited in ML history

## Limitations

- Quadratic memory cost in sequence length (O(n²) attention)
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
