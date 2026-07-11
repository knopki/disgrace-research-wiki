---
title: Anthropic
created: 2026-06-17
updated: 2026-06-17
type: entity
tags:
  - paper
  - methodology
  - organization
sources:
  - "[Toy Models of Superposition](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md)"
  - "[Constitutional AI: Harmlessness from AI Feedback](raw/papers/2022-12-bai-constitutional-ai/bai2022constitutional.md)"
  - "[Towards Monosemanticity: Decomposing Language Models With Dictionary Learning](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md)"
confidence: high
---

# Anthropic

An AI safety research company, founded in 2021, best known for the Claude family of language models and foundational work in mechanistic interpretability. Led by co-founder and CEO [[dario-amodei|Dario Amodei]]. The Transformer Circuits Thread — their interpretability research programme led by Christopher Olah — published the seminal *Toy Models of Superposition* paper in 2022, which systematically demonstrated the [[superposition]] phenomenon.

## Key People (Superposition Paper)

The paper *Toy Models of Superposition* was authored by Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Tom Henighan, Shauna Kravec, Zac Hatfield-Dodds, Robert Lasenby, Dawn Drain, Carol Chen, Roger Grosse, Sam McCandlish, Jared Kaplan, Dario Amodei, Martin Wattenberg, and Christopher Olah.

Core research contributors: Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Martin Wattenberg, Christopher Olah (correspondence).

## Key Publications

- **Toy Models of Superposition** (Sept 2022) — demonstrated superposition in small ReLU networks, establishing [[superposition]], [[polysemantic-neurons|polysemantic neurons]], and the [[privileged-basis|privileged basis]] framework. Published under Transformer Circuits Thread.
- **[[sparse-autoencoders|Towards Monosemanticity]]** (Oct 2023) — applied sparse autoencoders (dictionary learning) to extract thousands of monosemantic features from a one-layer transformer's 512-neuron MLP; demonstrated features are more interpretable than neurons, universal across independently-trained models, and explain up to 94.5% of MLP loss; refuted the "eliminate superposition architecturally" strategy. Published under Transformer Circuits Thread.
- **[[constitutional-ai|Constitutional AI: Harmlessness from AI Feedback]]** (Dec 2022) — introduced CAI, a method for training harmless AI assistants via self-critique, revision, and RLAIF using only a short list of written principles; the foundation of Claude's safety training; significantly reduces reliance on human harmlessness labels.
- The Circuits Thread includes earlier work on interpretability of InceptionV1 neurons, feature visualisation, and universality.

## Research Programme

Anthropic's interpretability work is distinguished by:

1. **Toy models as proxies** — studying small, synthetic setups where ground truth is known (e.g., features are known to the experimenter), then generalising to real networks.
2. **Linear representation hypothesis** — features correspond to directions in activation space, a claim with significant empirical support from their work.
3. **Safety-motivated** — the explicit goal is "solving superposition" to enable enumerative safety claims about model behaviour.

## Relevance to This Wiki

Anthropic provided the theoretical and empirical foundations for understanding how neural networks pack more features than dimensions. Their concepts — superposition, privileged basis, polysemanticity — explain both the successes and failure modes of [[word-embeddings|word embeddings]], [[distributional-semantics|distributional semantics]], and [[retrieval-augmented-generation|RAG]].

## Related

- [[superposition]] — the central phenomenon demonstrated in their toy models
- [[polysemantic-neurons|Polysemantic Neurons]] — the neuron-level manifestation
- [[privileged-basis|Privileged Basis]] — the architectural condition they formalised
- [[word-embeddings|Word Embeddings]] — where superposition catastrophe was independently observed
