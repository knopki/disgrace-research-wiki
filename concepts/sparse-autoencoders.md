---
title: Sparse Autoencoders (for Feature Extraction)
created: 2026-07-11
updated: 2026-07-11
type: concept
tags:
  - technique
  - interpretability
  - paper
  - model
sources:
  - "[Towards Monosemanticity: Decomposing Language Models With Dictionary Learning](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md)"
  - "[Toy Models of Superposition](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md)"
confidence: high
---

# Sparse Autoencoders (for Feature Extraction)

A sparse autoencoder (SAE) is a dictionary-learning method used to decompose a neural network's activations into an overcomplete set of interpretable **features** — directions in activation space that are far more monosemantic than the model's individual neurons. Popularised for mechanistic interpretability by [[anthropic|Anthropic]] in *Towards Monosemanticity* (Bricken et al., 2023), it is the post-hoc "approach 2" to [[superposition]] identified in [[superposition|their earlier toy-model work]]: rather than engineering models to avoid superposition, find an overcomplete feature basis after training. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

## Setup

The flagship demonstration trains SAEs on the **MLP activations** (post-ReLU) of a single-layer transformer:

- **Model:** one-layer attention + ReLU MLP, residual-stream dim 128, MLP inner dim **512 neurons**, trained on the Pile for 100B tokens. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))
- **Autoencoder data:** 8 billion MLP activation vectors sampled from 40M contexts. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))
- **Expansion factor:** dictionary width ranges from **1× (512 features)** to **256× (131,072 features)**. The primary analysis focuses on run **A/1** with **4,096 features**. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

Two identically-configured transformers (A and B), differing only in random seed, were trained to study feature universality.

## Architecture

The SAE is a one-hidden-layer autoencoder. Given input activation `x` (length n = 512):

```
x_bar = x - b_d
f     = ReLU(W_e · x_bar + b_e)     # feature activations
x_hat = W_d · f + b_d               # reconstruction
L     = MSE(x, x_hat) + λ · ||f||_1
```

- `W_d` columns (unit-norm) are the **feature directions**; `f_i` is feature *i*'s activation. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))
- **Bias terms matter:** a tied pre-encoder / post-decoder bias (subtracted before the encoder, added back after) substantially improves results. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))
- **Decoder weights NOT tied** to the encoder transpose — they diverge (median cosine ~0.5) because the encoder detects features while the decoder approximates the "true" feature direction; untied weights increase representational capacity. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))
- **Neuron resampling:** "dead" autoencoder neurons (inactive over many steps) are periodically re-initialised to data points the current autoencoder represents poorly, recovering more interpretable features and lowering loss. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))
- A simple MSE + L1 loss (not cross-entropy) is used so that sparsity inhibits superposition from re-forming in the learned dictionary ("superposition all the way down"). ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

## Key Findings

### The feature is not a neuron

Detailed case studies (Arabic script `A/1/3450`, DNA `A/1/2937`, base64 `A/1/2357`, Hebrew `A/1/416`) show features that are:
- **Specific & sensitive** to a context (Arabic script is only 0.13% of training tokens but 81% of `A/1/3450`'s active tokens).
- **Causal**: ablating the feature hurts predictions of in-context tokens; *pinning* it high steers generation (pinning base64 → base64 text; pinning Arabic → Arabic text).
- **Not aligned to any neuron**: the most-correlated neuron for `A/1/3457` is polysemantic (responds to many non-Arabic languages). Some features are "effectively invisible" in the neuron basis. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

### Features are more interpretable than neurons

- **Human rubric** (blinded annotator, scored uniformly across the activation spectrum to avoid top-activation bias): median neuron scored **0** (no hypothesis formable); median feature interval scored **12** (max 14). ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))
- **Automated interpretability** (Claude 2 generates explanations, predicts activations): features beat neurons on both activation-prediction correlation and logit-weight prediction (74% vs 58% average accuracy, vs 50% chance). ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))
- Out of 4,096 A/1 features, 168 are dead and 292 are "ultralow density"; both groups are excluded from interpretation. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

### Loss explained

- A/1 recovers **79%** of the log-likelihood loss reduction provided by the MLP layer (i.e. replacing MLP activations with the autoencoder costs only 21% of the loss from zero-ablating the MLP).
- A/5 (131,072 features, lower L1) recovers **94.5%**. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

### Universality

Features recur across independently-trained models. The most-similar feature in B/1 to each A/1 feature has a **median activation correlation of 0.72** (vs **0.46** for the most-similar *neuron* between the two models). The base64 feature is so universal it was previously found in SoLU models and used as a debugging heuristic; Arabic `A/1/3450` ↔ `B/1/1334` corr 0.91, DNA 0.92, Hebrew 0.92, base64 0.85. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

### Feature splitting

As dictionary size grows, features **split into families**. The single base64 feature in a 512-feature dictionary (`A/0/45`) splits into three in A/1: one for base64 letters (`A/1/2357`), one for digits (`A/1/2364`), and one for base64 encoding ASCII text (`A/1/1544`) — a tokenization artifact. The authors conjecture an idealised set of "true features" that dictionary learning approximates at coarser resolutions, which they call "failing gracefully." ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

### Finite-state-automata feature assemblies

Features chain through the token stream: one feature increases the probability of tokens that re-activate another feature on the next step. Examples: self-exciting base64 loops, all-caps-snake-case (two nodes), Unicode prefix/suffix pairs for Tamil and Chinese, and a four-node HTML generator (`<div>\n\t\t<span>`). These arise from dataset structure, not learned cooperation. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

### Token-in-context features

A striking motif: hundreds of features for a single common token in different contexts (e.g. "the" in physics vs mathematics). The authors note this is a *local code* rather than the *compositional code* one might expect, and may partly be a quirk of the L1 penalty pushing toward sparsity. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

## Why architectural approaches fail

The paper explicitly tested "approach 1" (eliminate superposition by encouraging activation sparsity, including 1-hot activations and the SoLU activation). Even with superposition removed, individual neurons remain **polysemantic** — a toy example shows a neuron achieves *lower* cross-entropy by representing multiple features ambiguously than by representing one monosemantically. Hence they conclude architectural changes cannot produce fully monosemantic language models (language models are trained on cross-entropy, not MSE). This is the empirical defeat of the "create models without superposition" branch of the [[superposition|superposition solution space]]. ([Bricken et al., 2023](raw/papers/2023-10-bricken-monosemanticity/bricken2023monosemanticity.md))

## Relationship to other concepts

- Extends [[superposition]] and [[polysemantic-neurons|polysemantic neurons]]: SAEs are the practical realisation of the "find an overcomplete basis post-hoc" strategy, converting polysemantic neuron activations into monosemantic feature directions.
- Operates on a [[privileged-basis|privileged basis]] (the ReLU MLP layer), where the neuron/feature distinction is meaningful — but the *features* it finds are arbitrary directions, not neurons.
- Reinforces the **linear representation hypothesis**: features are directions, and in a one-layer model their effect on logits is approximately linear.
- Followed by *Scaling Monosemanticity* (Templeton et al., 2024), which applies SAEs to Claude 3 Sonnet at 1M–34M features.

## Open questions & scaling challenges

- No trusted automatic metric for "good features" (information-based metrics did not correlate with interpretability).
- Scaling SAEs to frontier models is an engineering problem: a 100× SAE on a 10,000-wide MLP ≈ 20B parameters, and rare features may need training on a large fraction of the base model's corpus.
- Unknown scaling laws for dictionary learning (ideal expansion factor, data requirements).

## Related

- [[superposition]] — the phenomenon SAEs decompose
- [[polysemantic-neurons|Polysemantic Neurons]] — what SAEs replace as the unit of analysis
- [[privileged-basis|Privileged Basis]] — why the MLP layer is the natural target
- [[anthropic|Anthropic]] — the research group behind the method
- [[cognitive-superposition|Cognitive Superposition]] — separate concept; see note on [[superposition]]
- [[word-embeddings|Word Embeddings]] — another setting where linear feature directions matter
