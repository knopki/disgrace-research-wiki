---
title: Superposition
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [model, paper, methodology]
sources:
  - "[Toy Models of Superposition](raw/papers/toy-models-superposition/index.md)"
  - "[Вектора GPT или почему для GPT ваше слово — пустота без контекста](raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md)"
confidence: high
---

# Superposition

> **Note:** This page covers superposition as a *representational* phenomenon — packing more features than dimensions in activation space (from Anthropic's *Toy Models*). See [[cognitive-superposition|Cognitive Superposition]] for the separate but related concept of maintaining multiple *conceptual representations* simultaneously in working memory (from Garagnani 2024).

A phenomenon in neural network representations where more features are encoded than available dimensions. Features are stored as non-orthogonal directions in activation space, tolerating mutual interference that is filtered out by nonlinear activation functions (typically ReLU). ^[raw/papers/toy-models-superposition/index.md]

Superposition was systematically demonstrated and studied by [[anthropic|Anthropic]] in their 2022 paper *Toy Models of Superposition*, which showed that small ReLU networks trained on sparse synthetic data reliably exhibit this behaviour.

## Mechanism

Superposition arises from a trade-off between two competing forces:

- **Feature benefit** — representing a feature reduces the loss proportionally to its importance
- **Interference** — non-orthogonal features create cross-talk; when one feature activates, it slightly activates other features sharing its dimension

In linear models, interference always outweighs benefit for extra features — the optimal solution is PCA (keep only the top-*m* features). Adding a ReLU activation function changes this: negative interference becomes free (clipped to zero), so the model can pack more features by tolerating only positive interference. ^[raw/papers/toy-models-superposition/index.md]

Two parameters govern the trade-off:

- **Feature sparsity** — how often a feature is non-zero. Sparse features rarely co-activate, greatly reducing expected interference.
- **Feature importance** — how much the loss benefits from representing this feature. More important features get cleaner representations.

## Phase Change

There are three regimes for any feature, with sharp transitions between them: ^[raw/papers/toy-models-superposition/index.md]

1. **Not learned** — feature importance so low or density so high that the model ignores it entirely.
2. **Superposition** — feature is represented, but shares dimensions with others. This is the intermediate regime, governed by sparsity.
3. **Dedicated dimension** — the feature gets its own orthogonal dimension (a "monosemantic neuron" if in a [[privileged-basis|privileged basis]]).

The transition between these regimes is a **first-order phase change**: the optimal weight configuration changes discontinuously. This mirrors the Thomson problem in chemistry, where points on a sphere repel each other under a force law.

## Geometry of Superposition

When many equally important, equally sparse features are packed into fewer dimensions, they self-organise into geometric structures — uniform polytopes on the surface of a hypersphere: ^[raw/papers/toy-models-superposition/index.md]

| Dimensionality | Structure | Description |
|---|---|---|
| 1 | Dedicated dimension | One feature per dimension |
| 3/4 | Tetrahedron | 4 features in 3D |
| 2/3 | Triangle | 3 features in 2D |
| 1/2 | Antipodal pair | Two features as opposite vectors |
| 2/5 | Pentagon | 5 features in 2D |
| 3/8 | Square antiprism | 8 features in 3D |
| 0 | Not learned | Feature ignored |

The model "sticks" at these fractional dimensionalities — it prefers exact polytope geometries over intermediate arrangements. This connects to the **tegum product** operation: superposition solutions are often products of lower-dimensional uniform polytopes embedded in orthogonal subspaces. ^[raw/papers/toy-models-superposition/index.md]

### Non-Uniform Superposition

When features have varying importance, sparsity, or correlational structure, the geometry deforms smoothly until a critical breaking point where it snaps to a different polytope. Key observations: ^[raw/papers/toy-models-superposition/index.md]

- **Correlated features** prefer orthogonality (separate tegum factors), forming local almost-orthogonal bases.
- **Anti-correlated features** prefer negative interference (antipodal pairs in the same tegum factor).
- **Sufficiently correlated features collapse** into their principal component — a trade-off between PCA and superposition.

## Computation in Superposition

Superposition is not just storage — models can perform computation on features represented in superposition. ^[raw/papers/toy-models-superposition/index.md]

The primary example is computing absolute value: a model with fewer neurons than features can learn `abs(x) = ReLU(x) + ReLU(-x)` for each feature, even when features share neurons. This requires the hidden-layer ReLU, which also creates a [[privileged-basis|privileged basis]] aligning features with neurons.

An **asymmetric superposition motif** emerges where two neurons work together: one stores features with unequal magnitudes (asymmetric superposition), and the other inhibits the feature that would otherwise suffer positive interference. This converts harmful interference into harmless negative interference.

## Relationship to Adversarial Examples

Superposition creates off-diagonal interference terms in `W^TW` that adversaries can exploit. A feature in superposition has weight vector:
`(W^TW)_0 = (1, ε, -ε, ε, ...)`

The epsilon entries — pure artifacts of superposition — are attack vectors. Empirical results show vulnerability to adversarial examples increases sharply (>3x) as superposition forms, closely tracking the number of features per dimension. ^[raw/papers/toy-models-superposition/index.md]

## Strategic Implications for Interpretability

"Solving superposition" — being able to enumerate all features — is described as necessary for mechanistic interpretability to support safety claims. Three approaches are identified: ^[raw/papers/toy-models-superposition/index.md]

1. **Create models without superposition** — L1 regularization on activations, adversarial training, or MoE architectures that exploit the same sparsity gap that superposition uses.
2. **Find an overcomplete basis post-hoc** — sparse coding / dictionary learning on layer activations.
3. **Hybrid approaches** — reduce superposition partially, then decode the remainder.

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
