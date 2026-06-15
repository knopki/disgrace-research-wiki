---
title: LSTM (Long Short-Term Memory)
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [model, architecture, training]
sources:
  - "[История ИИ: бунтари, гении и научные войны](raw/articles/2025-07-03-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/index.md)"
confidence: high
---

## Definition

**Long Short-Term Memory (LSTM)** is a recurrent neural network architecture designed to handle the [[backpropagation|vanishing gradient problem]] in sequential data processing. It introduces gating mechanisms that allow the network to selectively remember or forget information over long time horizons.

## History

LSTM was invented by **Sepp Hochreiter** as a student of **Jürgen Schmidhuber** in 1991, published as his diploma thesis. Hochreiter and Schmidhuber formally published the architecture in 1997. LSTM dominated natural language processing from the late 1990s until the rise of the [[transformer|Transformer]] around 2017 — roughly 15 years of supremacy in machine translation, speech recognition, and text generation. ^[raw/articles/2025-07-03-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/index.md]

## Architecture: The Gates

The core innovation is three specialised neural subnetworks (gates) that regulate information flow:

- **Forget Gate** — decides which information from the previous state to discard
- **Input Gate** — determines what new information is worth storing
- **Output Gate** — controls what stored information is used for the current output

This structure lets the network maintain a **cell state** — an internal memory channel that persists across many time steps, only modified by learned write/erase operations rather than by the direct output path.

## Significance

- Solved the long-range dependency problem that plagued vanilla RNNs
- Became the gold standard for sequence modelling for over a decade
- The concept of gated information flow influenced later architectures, including the [[transformer|Transformer]]'s attention mechanism
- Demonstrated that architectural innovations (gating) can overcome fundamental training limitations

## Limitations

- Sequential computation: processes tokens one at a time, making parallelisation difficult
- Still suffers from gradient issues in very long sequences (100+ steps)
- Context window effectively limited by the cell state capacity

## Cross-Links

- [[backpropagation|Backpropagation]] — the training algorithm LSTM relies on
- [[transformer|Transformer]] — the architecture that replaced LSTM as the NLP dominant paradigm
- [[residual-connection|Residual Connection]] — a different solution to the vanishing gradient problem
- [[perceptron|Perceptron]] — the foundational architecture all neural networks descend from
