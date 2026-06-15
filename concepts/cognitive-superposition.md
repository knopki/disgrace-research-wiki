---
title: Cognitive Superposition
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [model, architecture, methodology, paper]
sources:
  - "[On the ability of standard and brain-constrained DNNs to support cognitive superposition](raw/papers/cognitive-superposition-garagnani/index.md)"
confidence: high
---

# Cognitive Superposition

The capacity of a cognitive system to recall and maintain **simultaneously active** in working memory two or more internal representations while keeping them **distinct and functionally separate**. Defined formally by Garagnani (2024):

> A neural network model supports cognitive superposition **iff**:
> 1. It allows co-activation of any two hidden-node activity vectors associated with distinct input items **never presented together** during training.
> 2. During co-activation, information about the identity and features of the original components is preserved.

This is distinct from [[superposition]] as used in mechanistic interpretability (Anthropic's *Toy Models*), where "superposition" refers to packing more *features* than dimensions in a single layer's activation space. Cognitive superposition is about maintaining multiple distinct *conceptual representations* simultaneously in working memory.

## Why It Matters

| Domain | Role of Cognitive Superposition |
|--------|--------------------------------|
| **Working memory** | Maintain multiple items for simultaneous comparison |
| **Abstract reasoning** | Mental arithmetic, problem solving, planning |
| **Language comprehension** | Co-activate arbitrary concept combinations in sentences ("apple and car") |
| **Social cognition** | Theory of mind (Noguchi et al. 2022) |
| **Creative thinking** | Novel combinations of familiar concepts |

WM capacity correlates with fluid intelligence (Conway et al. 2003); the average person can hold ~4–5 items (Cowan 2001). Garagnani's preliminary simulations suggest this limit may be an architectural upper bound arising from hierarchy depth.

## The Superposition Catastrophe

In standard neural networks, distinct items are encoded as **non-orthogonal vectors** over the same set of processing units. Summing two such vectors produces an ambiguous blend from which original components cannot be uniquely retrieved. This is known as the **superposition catastrophe** (Milner 1974; Page 2000; Rosenblatt 1962). ^[raw/papers/cognitive-superposition-garagnani/index.md]

### Why Backpropagation Fails

Gradient descent creates **uniform weight distributions** — no single node becomes fully selective to one input. All nodes contribute to all learned outputs, producing graded, overlapping representations. ^[raw/papers/cognitive-superposition-garagnani/index.md]

Failed attempts to solve this:
- **Bowers et al. (2014):** Trained recurrent net on superposed inputs — selective nodes emerged, but items were co-activated *during training*, violating condition (2).
- **Martin (2021):** Failed to replicate emergent selectivity.
- **Temporal binding via oscillations:** Proposed rhythmic firing at different phases, but doesn't explain how distant neurons maintain precise synchrony over seconds without interference.

## How Brain-Constrained Networks Support It

### Architecture

- **Multi-area deep hierarchy** (6 layers in Garagnani's simulations) with structure, connectivity, and learning mechanisms mimicking cortical features.
- **Sparse, topographic, reciprocal** between-area projections (not all-to-all).
- **Local Hebbian learning rule** (ABS rule): LTP (Hebbian strengthening) + LTD (anti-Hebbian weakening).

### Emergent Cell Assemblies (CAs)

CAs are sets of strongly and reciprocally connected cells that spontaneously emerge from Hebbian learning:

| Property | Description |
|----------|-------------|
| **Bistability** | Fully "on" (ignited) or "off" — working memory correlate |
| **Quasi-orthogonality** | <5% overlap between any two CA circuits (Fig. 2) |
| **Kernel + halo** | Core cells strongly linked; peripheral cells weakly linked |
| **Self-sustained** | Can reverberate indefinitely without external input |
| **Fault-tolerant** | Thousands to tens of thousands of neurons per CA |

### Mechanism: Recruitment Learning

1. **LTP:** Strengthens links between cells co-activated by the same stimulus → binds them into a CA.
2. **LTD:** Weakens links between cells activated by different stimuli → separates distinct CAs.

"Recruitment learning" (Valiant 2000) ensures each node becomes selectively responsive to one stimulus, and distinct CAs are almost disjoint. ^[raw/papers/cognitive-superposition-garagnani/index.md]

### Proof-of-Concept (Fig. 3B)

CA #5 self-sustained → input for CA #2 presented → CA #2 ignites → both CAs co-exist without blending → external input removed → CA #2 fades, CA #5 remains. The two circuits remained functionally distinct throughout. ^[raw/papers/cognitive-superposition-garagnani/index.md]

## Role of Sparse Connectivity

Sparse between-area projections alone are insufficient — it is the **combination** of:
1. A local learning rule inducing input selectivity
2. Sparse and topographic between-area projections

that enables quasi-orthogonal CA circuits. The deep hierarchy also contributes: patterns initially overlapping in the lowest layer are progressively "pulled apart" in deeper layers (Henningsen-Schomers et al. 2023). ^[raw/papers/cognitive-superposition-garagnani/index.md]

## Two Code Types in Cortex

Graded (overlapping) and discrete (quasi-orthogonal CA) codes may coexist:

| Code Type | Advantages | Disadvantages |
|-----------|------------|---------------|
| Graded (overlapping) | Smooth generalisation based on similarity | Superposition catastrophe |
| Discrete (quasi-orthogonal CAs) | Robust, superposition-capable, noise-resistant | All-or-none — poor similarity generalisation |

## Open Questions

1. **Direct proof of quasi-orthogonal CAs in cortex** remains elusive, though convergent evidence exists (synchronised neural activity, sparse coding, orthogonal codes).
2. **Superposition capacity vs hierarchy depth:** Preliminary results suggest an asymptotic upper bound on the number of coactive CAs, relatable to human WM limits (Cowan's 4–5 items).
3. **Evolutionary implications:** Expansion of cortical-association areas in humans may have been driven by WM advantages.
4. **Cognitive AI:** Exploring Hebbian mechanisms and sparse connectivity in deep NNs may be necessary for human-like general intelligence.

## Related

- [[superposition]] — the Mechanistic Interpretability sense (packing features into fewer dimensions)
- [[word-embeddings|Word Embeddings]] — where superposition catastrophe was independently observed
- [[polysemantic-neurons|Polysemantic Neurons]] — overlap between feature-packing and cognitive representations
- [[anthropic|Anthropic]] — published the complementary Toy Models of Superposition
