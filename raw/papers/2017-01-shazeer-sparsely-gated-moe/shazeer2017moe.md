---
title: Outrageously Large Neural Networks — The Sparsely-Gated Mixture-of-Experts Layer
authors:
  - Noam Shazeer
  - Azalia Mirhoseini
  - Krzysztof Maziarz
  - Andy Davis
  - Quoc Le
  - Geoffrey Hinton
  - Jeff Dean
source_url: https://arxiv.org/abs/1701.06538
date: 2017-01-23
venue: ICLR 2017 (under review)
tags:
  - mixture-of-experts
  - architecture
  - training
  - distributed
description: Introduces the Sparsely-Gated Mixture-of-Experts (MoE) layer — a general-purpose neural network component with up to thousands of feed-forward experts, noisy top-k gating, and load-balancing losses. Achieves 137B parameters with practical training, SOTA on language modeling and machine translation.
ingested: 2026-06-17
---

# Outrageously Large Neural Networks — The Sparsely-Gated Mixture-of-Experts Layer

## Abstract

The capacity of a neural network to absorb information is limited by its number of parameters. Conditional computation, where parts of the network are active on a per-example basis, has been proposed in theory as a way of dramatically increasing model capacity without a proportional increase in computation. This work addresses the algorithmic and performance challenges of conditional computation, achieving >1000x improvements in model capacity with only minor losses in computational efficiency on modern GPU clusters. The Sparsely-Gated Mixture-of-Experts layer (MoE) consists of up to thousands of feed-forward sub-networks with a trainable gating network determining a sparse combination of experts per example. Applied to language modeling and machine translation between stacked LSTM layers, models with up to 137 billion parameters achieve significantly better results than state-of-the-art at lower computational cost.

## Key Contributions

1. **Sparsely-Gated MoE Layer** — a general-purpose neural network component with up to thousands of feed-forward experts and differentiable gating
2. **Noisy Top-K Gating** — trainable gating with Gaussian noise and top-k sparsity; backpropagatable unlike prior REINFORCE-based approaches
3. **Shrinking Batch Problem Solution** — mixing data parallelism (standard layers) with model parallelism (expert shards) keeps per-expert batch sizes practical
4. **Expert Utilization Balancing** — importance loss (CV of batchwise gate sums) + load loss (smooth estimator using Gaussian CDF) prevents expert collapse
5. **Hierarchical MoE** — two-level gating (primary + secondary) for very large expert counts (up to 131K experts)

## Architecture

### MoE Layer

The MoE layer consists of n expert networks E₁…Eₙ (each a feed-forward network with one hidden layer) and a gating network G(x). The output is:

y = Σᵢ G(x)ᵢ · Eᵢ(x)

Computation is saved by sparsity: wherever G(x)ᵢ = 0, Eᵢ(x) is not computed. Typically k=2-4 experts are active per example out of hundreds to thousands.

### Noisy Top-K Gating

H(x)ᵢ = (x · Wg)ᵢ + StandardNormal() · Softplus((x · Wnoise)ᵢ)

G(x) = Softmax(KeepTopK(H(x), k))

The noise term enables load balancing via a smooth estimator (Gaussian CDF) for the discrete expert assignment. All parts trained via backpropagation — no REINFORCE needed.

### Performance Engineering

**Shrinking Batch Problem:** Each expert receives ~kb/n examples per batch — too small for efficient GPU computation. Solution: standard layers are data-parallel replicas, MoE experts are model-parallel shards hosted on dedicated devices. With d devices processing batch b each, each expert receives ~kbd/n examples — a factor of d improvement.

**Network Bandwidth:** Expert computation/communication ratio = hidden layer size. Larger hidden layers (2048+) improve efficiency by increasing compute relative to input/output data transfer.

**Convolutionality:** The MoE is applied to all time steps simultaneously (after the previous layer finishes), increasing effective batch size by the number of unrolled timesteps.

### Expert Balancing

Two auxiliary losses prevent the gating network from converging on a few experts:

**Importance Loss:** L_importance = w_importance · CV(Importance(X))² where Importance(X)ᵢ = Σ_x G(x)ᵢ

**Load Loss (Appendix A):** Smooth estimator using Gaussian CDF — P(x,i) = Pr(H(x)ᵢ > kth_excluding(H, k, i)). L_load = w_load · CV(Load(X))²

All combinations with at least one loss gave similar quality; no loss was much worse.

## Key Results

### 1 Billion Word Language Modeling (Chelba et al., 2013)

| Model | Test PPL | Params (MoE) | Total Params | ops/timestep |
|-------|----------|--------------|--------------|-------------|
| 2xLSTM-8192 (best published) | 34.7 | — | 151M | 30.6M |
| MoE-4096-h | **34.1** | 4.3B | 5.1B | 8.9M |
| MoE-34M | 31.3 | 4B | 6.0B | 33.8M |
| MoE-143M | **28.0** | 4B | 6.0B | 142.7M |

MoE-143M achieves 18% lower perplexity than the best published model at similar computational budget.

### 100 Billion Word Google News Corpus

| Model | Test PPL (1 epoch) | Total Params |
|-------|--------------------|--------------|
| 4xLSTM-512 | 47.0 | 8.4M |
| MoE-32 | 40.4 | 37.8M |
| MoE-4096-h | 30.9 | 4.4B |
| MoE-65536-h | **28.9** | 68.9B |
| MoE-131072-h | 29.2 | 137.7B |

Scaling to 137B parameters shows continued improvement up to 68B; beyond that, computational efficiency drops due to insufficient batch size scaling.

### Machine Translation (WMT'14 En→Fr)

| Model | BLEU | ops/timestep |
|-------|------|-------------|
| GNMT (Wu et al., 2016) | 38.95 | — |
| Deep Attention (Zhou et al., 2016) | 39.23 | — |
| MoE Baseline (0 experts) | 37.04 | 85M |
| MoE-32 | 38.93 | 85M |
| MoE-512-h | 40.36 | 85M |
| MoE-2048-h | **40.42** | 85M |

MoE models match or exceed prior SOTA at the same computational budget. Expert specialization by syntax/semantics was observed empirically (Appendix E, Table 9).

## Expert Specialization

The paper qualitatively demonstrates that experts learn specialized roles (Table 9) — e.g., one expert activates for phrases involving the indefinite article "a" introducing direct objects in leadership/importance contexts. This specialization emerges naturally from the sparsity constraint and load-balancing losses, without explicit supervision.

## Significance & Legacy

- **First practical demonstration of conditional computation at scale** — prior work failed to deliver on the promise of conditional computation due to GPU branching costs, shrinking batches, and network bandwidth constraints
- **Foundational paper for the MoE architecture family** — directly inspired Switch Transformer (Fedus et al., 2021), Mixtral 8x7B, DeepSeek MoE, GPT-4's reported MoE structure, and most modern sparse expert models
- **Established the training infrastructure template** — mixing data/model parallelism for experts, load-balancing via auxiliary loss, noisy top-k gating became standard practice
- **137B parameters (2017)** — at the time the largest neural network trained, demonstrating that parameter count could be decoupled from computational cost

## Technical Limitations

- Hierarchical MoE at extreme scales (131K experts) showed reduced computational efficiency (0.30 TFLOPS/GPU) — insufficient batch size per expert for the hardware
- Models used LSTM base (not Transformer) — the MoE layer was applied convolutionally between stacked LSTMs
- No analysis of inference costs or memory overhead for deployment
- Expert capacity (number of examples per expert per batch) was not explicitly controlled — later work (Switch Transformer) formalized expert capacity as a key hyperparameter

