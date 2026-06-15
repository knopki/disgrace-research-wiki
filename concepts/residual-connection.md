---
title: Residual Connection (Skip Connection)
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [model, architecture, training, optimization]
sources:
  - "[История ИИ: бунтари, гении и научные войны](raw/articles/2025-07-03-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/index.md)"
confidence: high
---

## Definition

A **residual connection** (also called a skip connection or shortcut connection) is an architectural pattern where the input to a neural network layer is added directly to its output. Instead of learning a full transformation $F(x)$, the layer learns only the residual $\Delta = F(x) - x$, so the output becomes $x + \Delta$.

## Origin: ResNet

Residual connections were introduced in the 2015 paper **"Deep Residual Learning for Image Recognition"** by **Kaiming He**, **Xiangyu Zhang**, **Shaoging Ren**, and **Jian Sun** (Microsoft Research). Their model, **ResNet** (Residual Network), won the ImageNet 2015 classification competition with a staggering 152-layer network — dramatically deeper than anything previously trainable. ^[raw/articles/2025-07-03-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/index.md]

## Why It Works

The [[backpropagation|vanishing gradient]] problem makes training very deep networks difficult because the gradient signal decays before reaching early layers. A residual connection creates a direct gradient highway from the output back to the input, bypassing the intervening transformations. This allows:

- Training networks with hundreds of layers
- Gradients to flow unimpeded to early layers
- The network to learn identity mappings when deeper representations offer no benefit

The insight: each layer only needs to learn the *correction* to its input, not a complete new representation.

## Significance

- Enabled the era of truly deep learning (50+ layers, then 100+)
- Without residual connections, training networks like GPT would be impossible
- Adopted by virtually all modern architectures, including [[transformer|Transformers]], CNNs, and diffusion models
- Principle: identity shortcuts preserve information and gradient flow

## Usage in Transformers

Every Transformer block consists of two sub-layers, each wrapped in a residual connection: (1) multi-head self-attention and (2) feed-forward network. Each sub-layer's output is $LayerNorm(x + Sublayer(x))$, keeping the gradient path open through the full depth of the model.

## Cross-Links

- [[backpropagation|Backpropagation]] — the problem residual connections solve
- [[transformer|Transformer]] — the dominant architecture that depends on residual connections
- [[lstm|LSTM]] — a gating approach to the same gradient-flow problem
- [[perceptron|Perceptron]] — the simplest building block that residual connections extend
