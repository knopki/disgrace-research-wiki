---
title: Backpropagation
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - model
  - training
  - technique
sources:
  - "[История ИИ: бунтари, гении и научные войны](raw/articles/2025-07-03-ivanov-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/ivanoc2025istoriya.md)"
confidence: high
---

## Definition

**Backpropagation** (backward propagation of errors) is the fundamental algorithm for training multi-layer neural networks. It computes the gradient of the loss function with respect to each weight by applying the chain rule from calculus, propagating the error signal backwards from the output layer through the hidden layers to the input.

## History

The concept was first described by **Paul Werbos** in his 1974 PhD dissertation, but remained largely unnoticed. The algorithm was independently rediscovered by **Alexandr Galushkin** in the USSR. It was not until **1986** that **David Rumelhart**, **Geoffrey Hinton** (then at Carnegie Mellon), and **Ronald Williams** popularised backpropagation by demonstrating a working neural network that could learn the XOR function — directly answering the challenge posed by Minsky and Papert in their 1969 book *Perceptrons*. ([Ivanov, 2025](raw/articles/2025-07-03-ivanov-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/ivanoc2025istoriya.md))

## How It Works

1. **Forward pass** — input data propagates through the network layer by layer, producing a prediction at the output
2. **Loss computation** — the error (difference between prediction and ground truth) is calculated
3. **Backward pass** — the algorithm computes how much each neuron at each layer contributed to the total error by applying the chain rule
4. **Weight update** — each weight is adjusted proportionally to its contribution, so the network makes a smaller error next time

## Significance

- Directly refuted Minsky and Papert's claim that multi-layer networks could not be trained
- Enabled the training of networks with hidden layers, solving the XOR problem that defeated single-layer [[perceptron|perceptrons]]
- Laid the foundation for all subsequent deep learning (including [[lstm|LSTM]], [[residual-connection|ResNet]], and [[transformer|Transformers]])
- Its limitation — the vanishing gradient problem in very deep networks — later motivated residual connections and other architectural innovations

## The Vanishing Gradient Problem

As the error signal propagates backwards through many layers, it tends to shrink exponentially, making early layers learn very slowly or not at all. This capped the depth of networks trainable with vanilla backpropagation to a few layers until solutions like [[residual-connection|residual connections]] and normalisation techniques emerged.

## Cross-Links

- [[perceptron|Perceptron]] — the architecture backpropagation was designed to train
- [[frank-rosenblatt|Frank Rosenblatt]] — his perceptron theorems implicitly assumed multi-layer networks
- [[lstm|LSTM]] — introduced gating to control gradient flow
- [[residual-connection|Residual Connection]] — solved vanishing gradients for very deep networks
- [[transformer|Transformer]] — the dominant modern architecture, trained with backpropagation