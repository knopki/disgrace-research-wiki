---
title: Residual Connection (Skip Connection)
created: 2026-06-17
updated: 2026-06-18
type: concept
tags:
  - model
  - architecture
  - training
  - optimization
sources:
  - "[История ИИ: бунтари, гении и научные войны](raw/articles/2025-07-03-ivanov-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/ivanoc2025istoriya.md)"
  - "[Transformer Feed-Forward Layers Are Key-Value Memories](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md)"
confidence: high
---

## Definition

A **residual connection** (also called a skip connection or shortcut connection) is an architectural pattern where the input to a neural network layer is added directly to its output. Instead of learning a full transformation $F(x)$, the layer learns only the residual $\Delta = F(x) - x$, so the output becomes $x + \Delta$.

## Origin: ResNet

Residual connections were introduced in the 2015 paper **"Deep Residual Learning for Image Recognition"** by **Kaiming He**, **Xiangyu Zhang**, **Shaoging Ren**, and **Jian Sun** (Microsoft Research). Their model, **ResNet** (Residual Network), won the ImageNet 2015 classification competition with a staggering 152-layer network — dramatically deeper than anything previously trainable. ([Ivanov, 2025](raw/articles/2025-07-03-ivanov-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/ivanoc2025istoriya.md))

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

### Inter-Layer Prediction Refinement

Geva et al. (2021) demonstrated that residual connections in transformer LMs serve not only gradient flow but also **sequential prediction refinement**: the residual vector r_ℓ carries the aggregated prediction from all previous layers, and each feed-forward layer tunes it. Key findings:

- The residual's top prediction matches the model's final output in ~33% of examples by layers 4–5, rising to >80% by layer 16
- Probability mass on the final output token increases monotonically through layers
- When the FFN modifies the residual's prediction (composition cases), it rarely overrides it directly — instead it produces a **compromise**, suggesting the FFN acts as a "veto" mechanism that shifts probability mass toward other candidates in the residual's distribution head
- In the final layer, 66% of composition changes shift to a semantically distant word, 34% to a related word

([Geva et al., 2021](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md))

[[ffn-key-value-memories|FFN as key-value memories]] provides the mechanistic explanation for this refinement behavior.

## Cross-Links

- [[backpropagation|Backpropagation]] — the problem residual connections solve
- [[transformer|Transformer]] — the dominant architecture that depends on residual connections
- [[ffn-key-value-memories|FFN as Key-Value Memories]] — mechanistic explanation for how residuals refine predictions across layers
- [[lstm|LSTM]] — a gating approach to the same gradient-flow problem
- [[perceptron|Perceptron]] — the simplest building block that residual connections extend