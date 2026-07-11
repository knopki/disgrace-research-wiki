---
title: MEMIT (Mass-Editing Memory In Transformer)
created: 2026-07-11
updated: 2026-07-11
type: concept
tags:
  - technique
  - interpretability
  - paper
  - training
sources:
  - "[Mass-Editing Memory in a Transformer](raw/papers/2022-10-meng-memit/meng2022memit.md)"
confidence: high
---

## Definition

**MEMIT (Mass-Editing Memory In Transformer)** is a method for inserting *many* factual associations into an autoregressive transformer at once by directly computing parameter updates across a range of mid-layer MLP modules. Introduced by Meng et al. (MIT CSAIL / Northeastern / Technion, ICLR 2023), it is the direct successor to [[rome-model-editing|ROME]] — same authors, same causal-localization premise, but ROME edits one fact at a time whereas MEMIT scales to thousands of edits (orders of magnitude beyond prior work, ~100× the ~10–75 edits ROME/SERAC could handle). ([Meng et al., 2022](raw/papers/2022-10-meng-memit/meng2022memit.md))

## Core Idea

MEMIT builds on the Causal Tracing finding (developed in [[rome-model-editing|ROME]]) that factual recall is mediated by MLP modules processing the subject's last token. The key extension: instead of a *single* decisive layer, ROME's causal-tracing test on the larger GPT-J (6B) reveals a *range* of mediating MLP layers ℛ (for GPT-J, ℛ = {3,4,5,6,7,8}; the mediating gap between single-state and MLP-severed effects diminishes after layer 8).

Each MLP output projection `W_out^l` is treated as a **linear associative memory** (Kohonen 1972; Anderson 1972) mapping subject-key vectors `k_i` to memory-value vectors `m_i`. Because every token state in the residual stream is the sum of contributions from all MLPs (Eqn. 6, `h_L^S = h_0 + Σ a_l + Σ m_l`), new memories can be *spread* across all layers `l ∈ ℛ` rather than crammed into one. ([Meng et al., 2022](raw/papers/2022-10-meng-memit/meng2022memit.md))

## Method

### Single-layer batch update (closed form)

Given pre-existing keys `K0`/memories `M0` and new associations `K1`/`M1`, the optimal additive update `Δ` to `W_out` that inserts the new pairs while preserving old ones is obtained from the normal equations (Eqn. 13):

```
Δ = R · K1ᵀ · (C0 + K1 · K1ᵀ)⁻¹
```

where:
- `C0 = λ · E[kkᵀ]` — uncentered covariance of pre-existing keys, estimated from an empirical sample of layer inputs (pre-training is opaque, so `K0`/`M0` are not directly available).
- `R = M1 − W0·K1` — residual error of the new associations under the old weights.
- `λ` balances old vs. new; typical value `λ = 1.5 × 10⁴`.

This generalises ROME's single-edit rank-one constraint to a batched least-squares insertion. ([Meng et al., 2022](raw/papers/2022-10-meng-memit/meng2022memit.md))

### Multi-layer spreading

1. **Compute target vectors `z_i`.** For each edit `(s_i, r_i, o_i)`, optimise a residual `δ_i` by gradient descent so that substituting `z_i = h_L^S + δ_i` (at the top mediating layer `L = max(ℛ)`, token S) makes the model predict `o_i`. The loss (Eqn. 16) maximises `P[o_i | x_j ⊕ p(s_i,r_i)]` over random prefix texts `x_j` to aid generalization. This "hooking" of the hidden state is the same intervention style as ROME's value optimization.
2. **Distribute across layers.** For each layer `l ∈ ℛ` (in ascending order), contribute an equal fraction of the remaining residual: `r_i^l = (z_i − h_L^S) / (L − l + 1)`. Apply `Δ_l` via Eqn. 14, then **recollect activations** because each layer change shifts downstream states.

Edits are made only to MLP `W_out` weights in ℛ; attention and other components stay fixed. The approach is "embarrassingly parallel" in the `z_i` computations, though the paper's implementation ran them serially. ([Meng et al., 2022](raw/papers/2022-10-meng-memit/meng2022memit.md))

## Evaluation

**Datasets:** zsRE (10k real QA facts) and COUNTERFACT (21,919 counterfactual assertions, introduced in [[rome-model-editing|ROME]]).

**Metrics:** Efficacy Success (ES, does the edit "take"), Paraphrase Success (PS, generalization to rephrasings), Neighborhood Success (NS, specificity — unrelated subjects shouldn't change), Editing Score `S = harmonic_mean(ES, PS, NS)`, plus Reference Score (RS, TF-IDF consistency with Wikipedia) and Generation Entropy (GE, fluency).

### zsRE — 10,000 edits on GPT-J (6B)

| Editor | Score S ↑ | Efficacy ↑ | Paraphrase ↑ | Specificity ↑ |
|--------|-----------|------------|--------------|---------------|
| FT-W | 42.1 | 69.6 | 64.8 | 24.1 |
| MEND | 20.0 | 19.4 | 18.6 | 22.4 |
| ROME (sequential) | 2.6 | 21.0 | 19.6 | 0.9 |
| **MEMIT** | **50.7** | **96.7** | **89.7** | **26.6** |

### COUNTERFACT — 10,000 edits

| Editor | Score S ↑ | ES ↑ | PS ↑ | NS ↑ | GE ↑ | RS ↑ |
|--------|-----------|------|------|------|------|------|
| GPT-J (unedited) | 22.4 | 15.2 | 17.7 | 83.5 | 622.4 | 29.4 |
| FT-W | 67.6 | 99.4 | 77.0 | 46.9 | 293.9 | 15.9 |
| MEND | 23.1 | 15.7 | 18.5 | 83.0 | 618.4 | 31.1 |
| ROME (sequential) | 50.3 | 50.2 | 50.4 | 50.2 | 589.6 | 3.3 |
| **MEMIT (GPT-J)** | **85.8** | **98.9** | **88.6** | **73.7** | **619.9** | **40.1** |
| **MEMIT (GPT-NeoX 20B)** | **82.0** | **97.2** | **82.2** | **70.8** | **606.4** | **36.9** |

**Scaling behaviour:** ROME degrades past n≈32; MEND loses all efficacy before n=1,000 and is nearly inert at n=10,000. MEMIT holds high efficacy + generalization + specificity out to 10,000 edits. FT-W wins probability metrics but suffers *complete generation failure* (model damage). Mixing two relation types yields near-average (near-linear) performance — diversity of edits does not help or hurt. ([Meng et al., 2022](raw/papers/2022-10-meng-memit/meng2022memit.md))

**Runtime (10k edits):** MEND 98s, FT ~29 min, MEMIT 7.44 hr (GPT-J) / 12.29 hr (GPT-NeoX), ROME slowest. MEMIT's implementation is naive (serial `z_i` optimisation); the authors note it could be batched.

## Relationship to ROME

| | ROME | MEMIT |
|---|------|-------|
| Edits per run | 1 | thousands (1k–10k+) |
| Layers modified | single `l*` | range ℛ (e.g. {3..8}) |
| Update form | rank-one constraint | batched least-squares (Eqn. 14) |
| Constraint | hard equality | soft error minimisation |
| Small-n generalization | better (hard constraint) | slightly lower |
| Large-n scaling | fails past ~32 | holds to 10k |

At small `n`, ROME's hard equality constraint gives marginally better generalization; MEMIT trades that for massive scalability via soft minimisation spread over layers. ([Meng et al., 2022](raw/papers/2022-10-meng-memit/meng2022memit.md))

## Limitations

- **Directional (s, r, o) relations only.** No spatial/temporal reasoning, mathematics, linguistic or procedural knowledge, nor symmetric relations — "Tim Cook is CEO of Apple" and "The CEO of Apple is Tim Cook" must be edited separately.
- **Trade-offs on hard relations.** Some relations (P127 "product owned by company", P641 "athlete plays sport") still show a generalization↔specificity tension, though MEMIT still beats all baselines.
- **Runtime cost.** Current implementation is far slower than MEND/FT at 10k edits.
- **Ethical risk.** The same method can be abused to insert false/damaging information not present in training data. ([Meng et al., 2022](raw/papers/2022-10-meng-memit/meng2022memit.md))

## Significance

MEMIT shows that large-scale model updates can be built from explicit analysis of internal computations rather than opaque fine-tuning. Together with [[rome-model-editing|ROME]] it validates the mechanistic-model-editing programme: factual knowledge in GPT is localised in mid-layer MLPs (per [[ffn-key-value-memories|FFN as Key-Value Memories]]) and can be written directly. This contrasts with meta-learning editors (MEND, SERAC) and per-neuron methods like [[knowledge-neurons|Knowledge Neurons]], which fail to scale. The paper poses an open question: whether interpretability-based editing can become a standard, auditable alternative to retraining.

## Cross-Links

- [[rome-model-editing|ROME]] — single-edit predecessor; MEMIT generalises its causal-localization premise to batched multi-layer updates
- [[ffn-key-value-memories|FFN as Key-Value Memories]] — Geva et al.'s framework; MEMIT treats each MLP `W_out` as a linear associative memory
- [[knowledge-neurons|Knowledge Neurons]] — per-neuron editing baseline that fails to scale, contrasted in MEMIT's experiments
- [[transformer|Transformer]] — the architecture being edited
- [[gpt-3|GPT-3]] — model family context (GPT-J 6B / GPT-NeoX 20B evaluated)
