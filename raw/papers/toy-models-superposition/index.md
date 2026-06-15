---
source_url: https://transformer-circuits.pub/2022/toy_model/index.html
ingested: 2026-06-17
---

# Toy Models of Superposition

Note: Full extracted text in `index.txt` (164K chars). Original HTML in [index.html](index.html).

## Key Results

From Transformer Circuits Thread, published Sept 14, 2022 by Anthropic (Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, et al.).

1. **Superposition is a real, observed phenomenon** — small ReLU networks trained on synthetic sparse data represent more features than dimensions.
2. **Both monosemantic and polysemantic neurons can form** in the same model depending on feature sparsity and importance.
3. **Computation can be performed in superposition** — e.g., computing absolute value on features stored in superposition.
4. **Superposition is governed by a phase change** — sharp transitions between regimes (not learned, superposition, dedicated dimension).
5. **Superposition organizes features into geometric structures** — digons, triangles, pentagons, tetrahedrons, connected to the Thomson problem.

## Main Concepts

- **Superposition**: representing more features than available dimensions by tolerating interference. Enabled by sparsity — sparse features rarely co-activate, so interference is manageable.
- **Privileged basis**: when an activation function makes basis directions (neurons) special, encouraging features to align with them. Without a privileged basis (e.g., word embeddings), feature directions can be arbitrary.
- **Linear representation hypothesis**: features correspond to directions in activation space, not necessarily to individual neurons.
- **Feature sparsity & importance**: the two key parameters governing whether a feature gets a dedicated dimension, is stored in superposition, or is not represented at all.
- **Anti-podal pairs**: the simplest form of superposition — two features stored as opposite directions sharing one dimension.
- **Asymmetric superposition**: features stored with unequal magnitudes, with inhibition to neutralize interference.
- **Thomson problem connection**: the geometry of uniform superposition maps to packing points on a sphere, corresponding to uniform polytopes.
- **Connection to adversarial examples**: superposition creates off-diagonal interference terms that adversaries can exploit.

## Strategic Implications for Safety

"Solving superposition" (being able to enumerate all features) is presented as key to mechanistic interpretability safety claims. Three approaches:
1. Create models without superposition (e.g., L1 regularization, MoE architectures)
2. Find an overcomplete basis post-hoc (sparse coding / dictionary learning)
3. Hybrid approaches — reduce superposition, then decode
