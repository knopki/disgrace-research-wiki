---
title: Outrageously Large Neural Networks — The Sparsely-Gated Mixture-of-Experts Layer
authors:
  - Noam Shazeer
  - Azalia Mirhoseini
  - Krzysztof Maziarz
  - Andy Davis
  - Quoc Le
  - Geoffrey Hinton
  - Jeff Dean
source_url: https://arxiv.org/abs/1701.06538
date: 2017-01-23
venue: ICLR 2017 (under review)
tags:
  - mixture-of-experts
  - architecture
  - training
  - distributed
description: Introduces the Sparsely-Gated Mixture-of-Experts (MoE) layer — a general-purpose neural network component with up to thousands of feed-forward experts, noisy top-k gating, and load-balancing losses. Achieves 137B parameters with practical training, SOTA on language modeling and machine translation.
ingested: 2026-06-17
---
# Outrageously Large Neural Networks — The Sparsely-Gated Mixture-of-Experts Layer

**PDF:** [1701.06538.pdf](1701.06538.pdf)

## Abstract

The capacity of a neural network to absorb information is limited by its number of parameters. Conditional computation, where parts of the network are active on a per-example basis, has been proposed in theory as a way of dramatically increasing model capacity without a proportional increase in computation. This work addresses the algorithmic and performance challenges of conditional computation, achieving >1000x improvements in model capacity with only minor losses in computational efficiency on modern GPU clusters. The Sparsely-Gated Mixture-of-Experts layer (MoE) consists of up to thousands of feed-forward sub-networks with a trainable gating network determining a sparse combination of experts per example. Applied to language modeling and machine translation between stacked LSTM layers, models with up to 137 billion parameters achieve significantly better results than state-of-the-art at lower computational cost.
