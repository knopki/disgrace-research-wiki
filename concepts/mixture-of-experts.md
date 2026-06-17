---
title: Mixture-of-Experts (MoE)
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - architecture
  - model
  - mixture-of-experts
  - training
sources:
  - "[Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md)"
  - "[Switch Transformers: Scaling to Trillion Parameter Models](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md)"
confidence: high
---

# Mixture-of-Experts (MoE)

A neural network architecture paradigm that scales model capacity by **sparsely activating only a subset of parameters per input**. Instead of a single dense feed-forward network processing every token, MoE layers contain many parallel "expert" sub-networks, and a learned **gating/routing mechanism** selects which experts handle each input. This decouples parameter count from computational cost — models can have trillions of parameters while using only a fraction per forward pass.

## Core Idea

The fundamental MoE equation ([Shazeer et al., 2017](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md)):

y = Σᵢ G(x)ᵢ · Eᵢ(x)

Where Eᵢ are expert networks (typically feed-forward FFNs) and G(x) is a sparse gating vector. For most inputs, G(x)ᵢ = 0 for the vast majority of experts, so only a handful are computed — typically k=1-4 out of hundreds or thousands.

## The Sparsely-Gated MoE (Shazeer et al., 2017)

The foundational formulation introduced by Noam Shazeer, Azalia Mirhoseini, Geoffrey Hinton, Jeff Dean and co-authors (Google Brain, ICLR 2017) established the template for all subsequent MoE architectures.

### Noisy Top-K Gating

H(x)ᵢ = (x · Wg)ᵢ + ε · Softplus((x · Wnoise)ᵢ), where ε ~ N(0,1)

G(x) = Softmax(KeepTopK(H(x), k))

Key design choices:
- **Top-k sparsity** — only the k experts with the highest gating scores are activated; the rest contribute zero
- **Tunable Gaussian noise** — added before softmax to enable load-balancing gradients through a smooth estimator (Gaussian CDF) of the discrete expert selection
- **Fully differentiable** — unlike prior REINFORCE-based conditional computation, all parts train via standard backpropagation

### Balancing Expert Utilization

Without constraints, the gating network converges on a few experts — a self-reinforcing imbalance (favored experts train faster, get selected more). Two auxiliary losses prevent this:

- **Importance loss:** L_imp = w_imp · CV(Σ_x G(x))² — equalises the total gate weight per expert
- **Load loss (Appendix A):** Smooth estimator using Φ ((x·Wg) − kth_excluding) / Softplus(x·Wnoise) to approximate the discrete number of examples routed to each expert, then L_load = w_load · CV(Load)²

Both losses are applied per-batch. Combinations with at least one loss performed similarly; no loss caused severe degradation.

### Performance Engineering

MoE at scale required solving three key challenges:

| Challenge | Solution | Mechanism |
|-----------|----------|-----------|
| **Shrinking batch** (each expert sees ~kb/n examples) | Mixed data+model parallelism | Standard layers: data-parallel replicas; experts: model-parallel shards — per-expert batch = kbd/n (d = device count) |
| **Network bandwidth** (expert compute/comm ratio) | Large hidden layers | Expert hidden size ≥2048; compute/IO ratio = hidden_size |
| **Small per-step batch** | Convolutional application | MoE processes all timesteps together (one big batch) instead of per-step |

### Results

On the 1 Billion Word Language Modeling benchmark: **MoE-143M achieved perplexity 28.0** — 18% better than the best published LSTM (34.7) at comparable computational cost. On WMT'14 En→Fr translation: **BLEU 40.42** with an 85M ops/timestep budget, surpassing prior SOTA. The largest model had **137 billion parameters** across 131K experts.

## Evolution After Shazeer et al. (2017)

### Switch Transformer (Fedus et al., 2021)

Simplified MoE to **k=1 routing** — each token goes to exactly one expert. This cuts router computation in half, halves expert capacity requirements, and reduces communication by 50%. Introduced **expert capacity** as an explicit hyperparameter (tokens_per_batch / num_experts × capacity_factor) with token dropping for overflow. Achieved 7× pre-training speedups over dense T5 models and demonstrated **trillion-parameter models**. ([switch-transformer](concepts/switch-transformer.md))

Key differences from Shazeer et al.:
- k=1 vs k≥2
- Explicit expert capacity with token dropping vs implicit capacity
- Selective float32 precision (router only, rest in bfloat16) vs full-precision
- Simplified load balancing: α · N · Σ fᵢ · Pᵢ vs dual importance+load losses
- Transformer backbone vs LSTM backbone

### Modern MoE Architectures

All major post-2023 MoE models descend from the Shazeer et al. (2017) + Switch Transformer lineage:

- **Mixtral 8×7B** (Mistral, 2023) — 8 experts, k=2, 47B total / 13B active
- **DeepSeek MoE-V2** (2024) — fine-grained expert segmentation with shared experts
- **Qwen2.5-MoE** (2024) — MoE with fine-grained routing
- **GPT-4** (reported) — unknown expert count, MoE architecture widely reported

## Scaling Properties

MoE provides a **distinct scaling dimension** — expert count — that is independent of model depth and width. The marginal gain per expert follows a sub-linear curve: doubling experts improves quality less than doubling model width at the same compute budget, but the capital cost is lower since only active parameters consume inference compute.

### Theoretical Scaling

The Shazeer et al. paper demonstrated that expert count scales with hardware: **adding devices proportionally to expert count** keeps per-expert batch size, per-device memory/bandwidth, and step time constant. This makes MoE primarily an **infrastructure-scaling strategy** — the upper bound is set by cluster size, not architectural constraints.

## Training Considerations

- **Load balancing** is critical — without auxiliary losses, gating collapses to a few experts
- **Expert capacity** (Switch Transformer innovation) controls memory usage and load balance
- **Precision** — Shazeer et al. used full precision; Switch Transformer showed float32 router + bfloat16 rest works
- **Expert dropout** — higher dropout rates on expert FFNs prevent overfitting, especially in fine-tuning
- **Initialization** — gate weights initialized to zero for balanced initial load

## Inference Considerations

- **Memory overhead** — all expert parameters must be loaded (e.g., 1.6T parameters for Switch-C), making MoE models expensive to serve despite low per-token FLOPs
- **Distribution** — experts can be sharded across devices; all-to-all communication is the bottleneck
- **KV caching** — independent of MoE (applies to attention, not experts); MoE adds no KV cache overhead
- **Distillation** — MoE quality is partially compressible into dense models (~30% gain retention at 99% compression)

## Relationship to Other Concepts

- [[switch-transformer|Switch Transformer]] — direct simplification of this architecture with k=1 routing, expert capacity, and trillion-parameter scaling
- [[transformer|Transformer]] — modern MoE replaces the dense FFN sub-layer in each transformer block with an MoE layer; Shazeer et al. originally demonstrated MoE between stacked LSTM layers
- [[scaling-laws|Scaling Laws]] — MoE provides a scaling dimension (expert count) not captured by Chinchilla-optimal N-D-C scaling; sub-linear quality gains per added expert
- [[knowledge-distillation|Knowledge Distillation]] — Hinton et al. (2015) distillation is used to compress MoE quality into dense student models
- [[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]] — modern debate about whether sparse MoE models or dense SLMs are better economics for AI agents
- [[mamba|Mamba / SSM]] — alternative scaling strategy (fixed-size state) that competes with MoE on long-context efficiency
- [[kv-caching|KV Caching]] — orthogonal inference optimization; MoE affects FFN parameters, KV caching affects attention state

## References

- ([Shazeer et al., 2017](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md)) — Original paper: "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer"
- ([Fedus et al., 2022](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md)) — Switch Transformer: simplified MoE with k=1 routing
