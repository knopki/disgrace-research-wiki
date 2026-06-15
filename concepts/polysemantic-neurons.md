---
title: Polysemantic Neurons
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [model, architecture, paper]
sources:
  - "[Toy Models of Superposition](raw/papers/toy-models-superposition/index.md)"
confidence: high
---

# Polysemantic Neurons

Neurons that respond to multiple unrelated features. The counterpart is **monosemantic neurons**, which respond to a single interpretable feature. Both types can coexist in the same model, and the ratio between them is governed by feature sparsity. ^[raw/papers/toy-models-superposition/index.md]

Polysemanticity was systematically explained by [[anthropic|Anthropic]] in *Toy Models of Superposition* (2022) as the neuron-level manifestation of [[superposition]] in a [[privileged-basis|privileged basis]].

## Cause

Polysemanticity arises because the model has more features to represent than it has neurons. It packs multiple features into a single neuron by tolerating interference, relying on the fact that sparse features rarely co-activate. The ReLU activation function makes negative interference free, which is key to making this work.

In a [[privileged-basis|privileged basis]] (such as an MLP hidden layer), features tend to align with basis directions (neurons). When superposition forces multiple features into the same direction, that neuron becomes polysemantic.

## Phase Change with Sparsity

In the ReLU hidden layer toy model, there is a clear transition: ^[raw/papers/toy-models-superposition/index.md]

- **Dense features** (low sparsity) → neurons are monosemantic, each dedicated to one feature
- **Moderate sparsity** → mixture of monosemantic and polysemantic neurons in the same layer
- **High sparsity** → most neurons are polysemantic, storing multiple features

The transition mirrors the [[superposition|phase change in superposition]] itself: as sparsity increases, the model shifts from dedicating dimensions to packing features.

## Observations in Real Models

Three empirical observations from real neural networks that are consistent with the toy model: ^[raw/papers/toy-models-superposition/index.md]

1. **InceptionV1**: later layers have a higher fraction of polysemantic neurons. The explanation: higher-level features are sparser (e.g., a floppy ear detector fires much less often than an edge detector), which drives more superposition in later layers.

2. **Early Transformer MLP layers**: neurons are extremely polysemantic. This is consistent with the hypothesis that the first MLP layer disambiguates different interpretations of the same token — a task with very sparse feature structure.

3. **Primary + secondary features**: many neurons encode one "primary" feature with a large weight, plus several "secondary" features with smaller weights. Over a dataset, the neuron's strongest activations all correspond to the primary feature, but lower-magnitude activations are polysemantic. This matches observations from language model interpretability research.

## Asymmetric Superposition Motif

A specific polysemantic pattern discovered in the toy model: two neurons form a pair where one stores features with unequal weights, and the other inhibits the feature that would otherwise experience positive interference. This converts harmful positive interference into harmless negative interference. ^[raw/papers/toy-models-superposition/index.md]

## Implications for Interpretability

Polysemantic neurons are a core challenge for mechanistic interpretability. If a neuron responds to multiple unrelated features, one cannot simply take the neuron's activation as evidence of a single concept. This forces interpretability methods to either:

- Find an overcomplete basis (dictionary learning) that separates the features
- Work with models that have less or no superposition
- Analyse circuits at the level of feature directions rather than individual neurons

## Related

- [[superposition]] — the underlying phenomenon that causes polysemanticity
- [[privileged-basis|Privileged Basis]] — architectural condition that makes the neuron vs feature distinction meaningful
- [[anthropic|Anthropic]] — research organisation that provided the toy model explanation
- [[word-embeddings|Word Embeddings]] — superposition in non-privileged bases (no "neurons" to be polysemantic)
