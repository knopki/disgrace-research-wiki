---
title: ROME (Rank-One Model Editing)
created: 2026-06-25
updated: 2026-07-11
type: concept
tags:
  - technique
  - interpretability
  - paper
  - training
sources:
  - "[Locating and Editing Factual Associations in GPT](raw/papers/2022-02-meng-rome/meng2022rome.md)"
confidence: high
---

## Definition

**ROME (Rank-One Model Editing)** is a method for modifying specific factual associations in autoregressive transformer language models by directly computing a rank-one update to the MLP weight matrix at a single mid-layer feed-forward module. Introduced by Meng et al. (MIT / Northeastern / Technion, NeurIPS 2022), ROME is both a practical model-editing technique and a causal test of the hypothesis that factual associations correspond to localized computations in middle-layer MLP modules. ([Meng et al., 2022](raw/papers/2022-02-meng-rome/meng2022rome.md))

## Mechanism

ROME operates in three steps, each informed by the Causal Tracing analysis that identified mid-layer MLP modules processing the subject's last token as the decisive site for factual recall:

### Step 1: Key Selection (k∗)

The key vector k∗ encodes the subject entity. At a chosen layer l∗ and the last subject token index i, the input after the MLP's non-linearity is read: `k∗ = σ(W_fc · γ(a_i + h_i))`. To make k∗ robust to different contexts, it is averaged over N=20 random prefix texts ending with the subject.

### Step 2: Value Optimization (v∗)

The value vector v∗ is optimized via gradient descent to satisfy two objectives simultaneously:

1. **Maximize target object probability** — when the MLP output at token i is replaced by z, the model should predict o∗ in response to the factual prompt p.
2. **Minimize essence drift** — a KL divergence term preserves the model's understanding of the subject's essence (e.g., that the Space Needle is still a landmark, just located somewhere else).

The combined objective is: `L(z) = −log P[o∗ | z] + λ · D_KL(P(z)[x] || P[x])`.

### Step 3: Rank-One Insertion

The MLP's second layer `W_proj` is treated as a linear associative memory (following [[ffn-key-value-memories|Geva et al.'s key-value memory framework]], but at the matrix level rather than per-neuron). A new key-value pair (k∗, v∗) is inserted by solving a constrained least-squares problem:

```
Ŵ = W + Λ · (C⁻¹k∗)ᵀ,   where  Λ = (v∗ − Wk∗) / ((C⁻¹k∗)ᵀ · k∗)
```

Here C = E[kkᵀ] is the uncentered covariance of MLP hidden states, pre-cached from 100,000 Wikipedia text samples. The update is rank-one — it modifies the matrix along a single direction, minimising interference with other stored associations. The entire edit takes ~2 seconds on an NVIDIA A6000 GPU for GPT-2 XL.

([Meng et al., 2022](raw/papers/2022-02-meng-rome/meng2022rome.md))

## Causal Tracing

Before editing, the paper develops **Causal Tracing**, a causal intervention method that identifies which hidden states are decisive for factual predictions. By comparing three runs (clean, corrupted subject embedding, and corrupted-with-single-state-restored), the method measures the Average Indirect Effect (AIE) of each hidden state. Key findings across GPT-2 XL, GPT-J, and GPT-NeoX:

- **Early site:** Middle-layer MLP modules (around layer 15-18 in GPT-2 XL) processing the *last token of the subject* have the strongest causal effect on factual predictions (AIE = 8.7% for individual states, 6.6% for MLP modules).
- **Late site:** Higher-layer attention at the last token of the prompt is also important (AIE = 1.6% at the subject token, but dominates at the last prediction token).
- Causal Tracing is more informative than gradient-based salience (Integrated Gradients), which produces scattered heatmaps that do not reveal the localized pattern.

([Meng et al., 2022](raw/papers/2022-02-meng-rome/meng2022rome.md))

## The COUNTERFACT Dataset

To evaluate model editing with sufficient sensitivity, the paper introduces **COUNTERFACT** — a dataset of 21,919 records derived from [[ffn-key-value-memories|ParaRel]] (Elazar et al., 2021), containing counterfactual statements (s, r, o∗) with low pre-edit probability compared to the true answer (s, r, oc). Each record includes:

- Requested rewrite prompt p∗
- 2 paraphrase prompts (generalization)
- 10 neighbourhood prompts from related entities (specificity/bleedover)
- 3 generation prompts (open-ended text consistency)
- Reference texts for TF-IDF consistency scoring

Metrics: Efficacy Score (ES), Paraphrase Score (PS), Neighbourhood Score (NS), and their harmonic mean Score (S), plus fluency (GE) and consistency (RS) from generated text.

([Meng et al., 2022](raw/papers/2022-02-meng-rome/meng2022rome.md))

## Key Results

### GPT-2 XL on COUNTERFACT

| Editor | Score S ↑ | Efficacy ES ↑ | Paraphrase PS ↑ | Neighbourhood NS ↑ | Fluency GE ↑ |
|--------|-----------|--------------|-----------------|-------------------|-------------|
| FT (fine-tuning) | 65.1 | 100.0 | 87.9 | 40.4 | 607.1 |
| FT+L (constrained) | 66.9 | 99.1 | 48.7 | 70.3 | 621.4 |
| KN (Knowledge Neurons) | 35.6 | 28.7 | 28.0 | 72.9 | 570.4 |
| KE (Knowledge Editor) | 52.2 | 84.3 | 75.4 | 30.9 | 586.6 |
| MEND | 57.9 | 99.1 | 65.4 | 37.9 | 624.2 |
| **ROME** | **89.2** | **100.0** | **96.4** | **75.4** | **621.9** |

### GPT-J (6B) on COUNTERFACT

| Editor | Score S ↑ | Efficacy ES ↑ | Paraphrase PS ↑ | Neighbourhood NS ↑ |
|--------|-----------|--------------|-----------------|-------------------|
| FT | 25.5 | 100.0 | 96.6 | 10.3 |
| FT+L | 68.7 | 99.6 | 47.9 | 78.6 |
| MEND | 63.2 | 97.4 | 53.6 | 53.9 |
| **ROME** | **91.5** | **99.9** | **99.1** | **78.9** |

Key patterns:

- **Most methods suffer from one of two failure modes:** (F1) overfitting to the counterfactual prompt (failing to generalise to paraphrases), or (F2) underfitting (bleedover — changing predictions for unrelated subjects that share the same relation). ROME avoids both simultaneously.
- [[knowledge-neurons|Knowledge Neurons (KN)]] — the closest interpretability-based baseline — is unable to make effective edits (28.7% efficacy on GPT-2 XL), indicating that per-neuron gradient attribution alone is insufficient for reliable editing.
- Human evaluation (15 volunteers, 150 comparisons) rated ROME 1.8× more consistent with the inserted fact than FT+L, though 1.3× less fluent.

([Meng et al., 2022](raw/papers/2022-02-meng-rome/meng2022rome.md))

## Limitations

- **Single-fact editing only:** ROME edits one association at a time. Its direct successor [[memit-mass-editing|MEMIT]] (Meng et al., ICLR 2023) scales the same causal-localization premise to thousands of edits by spreading batched least-squares updates across the range of mediating MLP layers ℛ.
- **Directional associations:** "The iconic landmark in Seattle is the Space Needle" and "The Space Needle is the iconic landmark in Seattle" are stored separately — both require independent edits.
- **Incomplete vector space understanding:** the structure of vector spaces representing learned attributes remains unclear.
- **Guessing behaviour:** successfully edited models may generate plausible but false new facts.
- **Fluency cost:** human evaluators rated ROME-edited text as slightly less fluent than FT+L, a subtle degradation not captured by automated metrics.
- **Scope:** only factual associations were studied; logical, spatial, and numerical knowledge were not investigated.

([Meng et al., 2022](raw/papers/2022-02-meng-rome/meng2022rome.md))

## Significance

ROME provides both a practical tool and a mechanistic hypothesis: factual associations in GPT are stored as localized computations in mid-layer feed-forward modules. By demonstrating that a single rank-one weight update can insert a generalised and specific new fact, the paper validates the causal role of MLP modules in factual recall that was identified by Causal Tracing. This contrasts with [[knowledge-neurons|Knowledge Neurons]] (Dai et al.), which edit at the per-neuron level with limited success, and with hypernetwork methods (KE, MEND) that trade specificity for generalisation or vice versa. ROME established the foundation for a line of work on mechanistic model editing, including MEMIT (mass-editing) and subsequent methods.

## Cross-Links

- [[knowledge-neurons|Knowledge Neurons]] — alternative interpretability-based model editing method compared against ROME; uses integrated gradients for neuron-level attribution rather than matrix-level associative memory
- [[ffn-key-value-memories|FFN as Key-Value Memories]] — Geva et al.'s framework that ROME builds on by treating W_proj as a linear associative memory
- [[transformer|Transformer]] — the architecture being edited
- [[gpt-3|GPT-3]] — the model family (GPT-2 XL / GPT-J) that ROME is evaluated on
- [[scaling-laws|Scaling Laws]] — relevant context for why model editing matters (retraining large models is expensive)
- [[memit-mass-editing|MEMIT]] — direct successor (Meng et al., ICLR 2023); generalizes ROME's causal-localization premise to batched multi-layer mass editing of thousands of facts
