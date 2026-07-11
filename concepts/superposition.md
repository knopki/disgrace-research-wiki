---
title: Superposition
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - model
  - paper
  - methodology
sources:
  - "[Toy Models of Superposition](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md)"
  - "[Вектора GPT или почему для GPT ваше слово — пустота без контекста](raw/articles/2025-07-02-ivanov-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/ivanov2025gpgvectors.md)"
confidence: high
---

# Superposition

> **Note:** This page covers superposition as a *representational* phenomenon — packing more features than dimensions in activation space (from Anthropic's *Toy Models*). See [[cognitive-superposition|Cognitive Superposition]] for the separate but related concept of maintaining multiple *conceptual representations* simultaneously in working memory (from Garagnani 2024).

A phenomenon in neural network representations where more features are encoded than available dimensions. Features are stored as non-orthogonal directions in activation space, tolerating mutual interference that is filtered out by nonlinear activation functions (typically ReLU). ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md))

Superposition was systematically demonstrated and studied by [[anthropic|Anthropic]] in their 2022 paper *Toy Models of Superposition*, which showed that small ReLU networks trained on sparse synthetic data reliably exhibit this behaviour.

## Mechanism

Superposition arises from a trade-off between two competing forces:

- **Feature benefit** — representing a feature reduces the loss proportionally to its importance
- **Interference** — non-orthogonal features create cross-talk; when one feature activates, it slightly activates other features sharing its dimension

In linear models, interference always outweighs benefit for extra features — the optimal solution is PCA (keep only the top-*m* features). Adding a ReLU activation function changes this: negative interference becomes free (clipped to zero), so the model can pack more features by tolerating only positive interference. ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md))

Two parameters govern the trade-off:

- **Feature sparsity** — how often a feature is non-zero. Sparse features rarely co-activate, greatly reducing expected interference.
- **Feature importance** — how much the loss benefits from representing this feature. More important features get cleaner representations.

## Phase Change

There are three regimes for any feature, with sharp transitions between them: ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md))

1. **Not learned** — feature importance so low or density so high that the model ignores it entirely.
2. **Superposition** — feature is represented, but shares dimensions with others. This is the intermediate regime, governed by sparsity.
3. **Dedicated dimension** — the feature gets its own orthogonal dimension (a "monosemantic neuron" if in a [[privileged-basis|privileged basis]]).

The transition between these regimes is a **first-order phase change**: the optimal weight configuration changes discontinuously. This mirrors the Thomson problem in chemistry, where points on a sphere repel each other under a force law.

## Geometry of Superposition

When many equally important, equally sparse features are packed into fewer dimensions, they self-organise into geometric structures — uniform polytopes on the surface of a hypersphere: ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md))

| Dimensionality | Structure | Description |
|---|---|---|
| 1 | Dedicated dimension | One feature per dimension |
| 3/4 | Tetrahedron | 4 features in 3D |
| 2/3 | Triangle | 3 features in 2D |
| 1/2 | Antipodal pair | Two features as opposite vectors |
| 2/5 | Pentagon | 5 features in 2D |
| 3/8 | Square antiprism | 8 features in 3D |
| 0 | Not learned | Feature ignored |

The model "sticks" at these fractional dimensionalities — it prefers exact polytope geometries over intermediate arrangements. This connects to the **tegum product** operation: superposition solutions are often products of lower-dimensional uniform polytopes embedded in orthogonal subspaces. ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md))

### Non-Uniform Superposition

When features have varying importance, sparsity, or correlational structure, the geometry deforms smoothly until a critical breaking point where it snaps to a different polytope. Key observations: ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md))

- **Correlated features** prefer orthogonality (separate tegum factors), forming local almost-orthogonal bases.
- **Anti-correlated features** prefer negative interference (antipodal pairs in the same tegum factor).
- **Sufficiently correlated features collapse** into their principal component — a trade-off between PCA and superposition.

## Computation in Superposition

Superposition is not just storage — models can perform computation on features represented in superposition. ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md))

The primary example is computing absolute value: a model with fewer neurons than features can learn `abs(x) = ReLU(x) + ReLU(-x)` for each feature, even when features share neurons. This requires the hidden-layer ReLU, which also creates a [[privileged-basis|privileged basis]] aligning features with neurons.

An **asymmetric superposition motif** emerges where two neurons work together: one stores features with unequal magnitudes (asymmetric superposition), and the other inhibits the feature that would otherwise suffer positive interference. This converts harmful interference into harmless negative interference.

## Relationship to Adversarial Examples

Superposition creates off-diagonal interference terms in `W^TW` that adversaries can exploit. A feature in superposition has weight vector:
`(W^TW)_0 = (1, ε, -ε, ε, ...)`

The epsilon entries — pure artifacts of superposition — are attack vectors. Empirical results show vulnerability to adversarial examples increases sharply (>3x) as superposition forms, closely tracking the number of features per dimension. ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md))

## Strategic Implications for Interpretability

"Solving superposition" — being able to enumerate all features — is described as necessary for mechanistic interpretability to support safety claims. Three approaches are identified: ([Anthropic, 2022](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md))

1. **Create models without superposition** — L1 regularization on activations, adversarial training, or MoE architectures that exploit the same sparsity gap that superposition uses.
2. **Find an overcomplete basis post-hoc** — sparse coding / dictionary learning on layer activations.
3. **Hybrid approaches** — reduce superposition partially, then decode the remainder.

**Empirical resolution (2023).** *Towards Monosemanticity* (Bricken et al., 2023) tested approach 1 directly and found it insufficient — even models trained with 1-hot or SoLU activations that eliminate superposition still produce [[polysemantic-neurons|polysemantic neurons]], because cross-entropy loss favours representing several features ambiguously in one neuron over ignoring some of them. This refocuses the interpretability programme on approach 2. The paper shows that a [[sparse-autoencoders|sparse autoencoder]] can decompose a one-layer transformer's 512-neuron MLP into thousands of monosemantic features, recovering 79% (at 4k features) to 94.5% (at 131k features) of the MLP's loss contribution. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

Because superposition is a phase change, there exists a regime where it is *totally absent*. The challenge is whether competitive models can operate in that regime.

## Open Questions

- Can feature importance and sparsity curves be estimated for real models?
- Does superposition diminish or increase with model scale?
- What class of computation is amenable to being performed in superposition?
- Is the Thomson problem connection general or idiosyncratic to toy models?
- Are there statistical tests to detect superposition in real networks without ground truth?

## Related

- [[polysemantic-neurons|Polysemantic Neurons]] — the neuron-level manifestation of superposition in [[privileged-basis|privileged bases]]
- [[privileged-basis|Privileged Basis]] — architectural property that determines whether superposition manifests as polysemanticity
- [[word-embeddings|Word Embeddings]] — superposition catastrophe in embedding spaces
- [[anthropic|Anthropic]] — the research organisation behind the Toy Models paper
- [[distributional-semantics|Distributional Semantics]] — sparsity of semantic features in language