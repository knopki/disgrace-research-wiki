---
source_url: https://transformer-circuits.pub/2023/monosemantic-features/
ingested: 2026-07-11
title: "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning"
authors:
  - Trenton Bricken
  - Adly Templeton
  - Joshua Batson
  - Brian Chen
  - Adam Jermyn
  - Tom Henighan
  - Christopher Olah
date: 2023-10-01
venue: Transformer Circuits Thread, 2023
---
# Towards Monosemanticity: Decomposing Language Models With Dictionary Learning

**Full text**: [bricken2023monosemanticity.mhtml](bricken2023monosemanticity.mhtml)

**Source:** [transformer-circuits.pub/2023/monosemantic-features](https://transformer-circuits.pub/2023/monosemantic-features/) (HTML-native publication)

## Abstract

The Transformer Circuits Thread trains a weak sparse autoencoder on the MLP activations of a one-layer transformer (512-neuron MLP, trained on the Pile) to decompose those activations into a larger, overcomplete set of interpretable "features." They demonstrate that these dictionary-learning features are substantially more monosemantic than neurons: individual features (e.g. Arabic script, DNA, base64, Hebrew) are specific and causal, cannot be found by inspecting neurons, and are universal across independently-trained models. The features explain 79% (at 4,096 features) to 94.5% (at 131,072 features) of the MLP layer's loss contribution, and they exhibit phenomena such as feature splitting (one feature refining into families as the dictionary grows), universality, and "finite state automata"-like assemblies that generate coherent structures such as valid HTML. The paper concludes that architectural approaches to eliminating superposition (sparse activations, SoLU) fail to produce monosemantic neurons, whereas post-hoc dictionary learning with sparse autoencoders succeeds. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))
