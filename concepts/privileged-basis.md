---
title: Privileged Basis
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [model, architecture, paper]
sources:
  - "[Toy Models of Superposition](raw/papers/2022-09-elhage-toy-models-superposition/index.md)"
confidence: high
---

# Privileged Basis

An architectural property of certain neural network layers where the basis directions (neurons) are structurally special, encouraging features to align with them rather than arbitrary directions in activation space. ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/index.md))

A privileged basis is created when an activation function is applied to the hidden layer — ReLU in particular breaks the rotational symmetry of the representation. Without this symmetry-breaking, any rotation of the activation space produces an identical model, and it is meaningless to ask whether a specific "neuron" is interpretable.

## Privileged vs Non-Privileged

| Property | Privileged Basis | Non-Privileged Basis |
|---|---|---|
| Example | MLP hidden layers, conv net feature maps | Word embeddings, transformer residual stream |
| Symmetry | Broken by activation function | Rotational (any rotation yields equivalent model) |
| Meaningful unit | Neuron (basis direction) | Any direction in activation space |
| Superposition manifests as | Polysemantic neurons | Feature directions with interference |
| Interpretability approach | Inspect individual neurons | Find meaningful directions (e.g., embedding arithmetic) |

In a non-privileged basis, applying a random linear transformation `M` to the representation and `M^{-1}` to the downstream weights produces an identical model. This means basis directions have no special status — the interpretable structure is in the *directions*, not the basis. ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/index.md))

## Role in Superposition

[[superposition]] can occur in both privileged and non-privileged bases, but its manifestation differs:

- **In a privileged basis** (e.g., the ReLU hidden layer model): features align with basis directions to take advantage of the activation function. This creates [[polysemantic-neurons|polysemantic neurons]] — individual neurons that respond to multiple features. The toy model visualisation of `W` (features × neurons) directly shows which features each neuron encodes.

- **Without a privileged basis** (e.g., the ReLU output model): features can be any direction. The model prefers negative interference (antipodal pairs) because ReLU at the output makes it free. Visualisation requires examining `W^TW` rather than `W`. ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/index.md))

## The ReLU Hidden Layer Limitation

In the toy model where a ReLU hidden layer creates a privileged basis, the model will try to *circumvent* the activation function if given any opportunity. For example, setting hidden biases all positive shifts neurons into the linear regime. When biases are removed, the model simulates a bias by averaging over many features. The model only uses the ReLU when absolutely forced to. ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/index.md))

The "computation in superposition" model (computing absolute value) does not have this issue because it *needs* the ReLU to compute absolute value, making the privileged basis genuinely functional.

## Linear Representation Hypothesis

The broader claim underlying the privileged basis framework: features in neural networks are represented as **directions in activation space**, regardless of whether the basis is privileged. This is hypothesised to be widespread because: ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/index.md))

- Linear transformations dominate neural network computation (measured in FLOPs)
- Linear representations make features "linearly accessible" to the next layer
- They provide statistical efficiency through non-local generalisation

## Implications

- In a privileged basis, it makes sense to study individual neurons. In a non-privileged basis, it does not — you must identify directions.
- The term "neuron" is typically reserved for basis directions in a privileged basis.
- [[superposition]] can be more easily detected in a privileged basis because it manifests as obvious polysemanticity.
- Solving superposition for interpretability may require different strategies depending on whether the target representation has a privileged basis.

## Related

- [[superposition]] — the phenomenon that pushes features away from basis alignment
- [[polysemantic-neurons|Polysemantic Neurons]] — what superposition looks like in a privileged basis
- [[word-embeddings|Word Embeddings]] — canonical example of a representation without a privileged basis
- [[anthropic|Anthropic]] — the research group that formalised this framework