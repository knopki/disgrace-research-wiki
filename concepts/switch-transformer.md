---
title: Switch Transformer
created: 2026-06-16
updated: 2026-06-16
type: concept
tags:
  - architecture
  - model
  - mixture-of-experts
  - training
sources:
  - "[Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md)"
  - "[Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md)"
confidence: high
---

# Switch Transformer

A [[mixture-of-experts|Mixture-of-Experts (MoE)]] [[transformer|Transformer]] architecture introduced by **William Fedus, Barret Zoph, and [[noam-shazeer|Noam Shazeer]]** (Google, 2021, published JMLR 2022) that simplifies MoE routing to a **single expert per token** (k=1), enabling sparsely-activated models with constant computational cost but vastly more parameters. Switch Transformer achieved up to **7× pre-training speedups** over dense T5 models and demonstrated training of **trillion-parameter models**.

## Core Innovations

### Single Expert Routing (Switch Layer)

Traditional MoE routing selects the top-k experts (typically k≥2) for each token. Switch Transformer simplifies this to **k=1** — each token is routed to exactly one expert:

- Router computation halved (no need to compute softmax over all experts and then select top-k)
- Each expert's batch size (capacity) can be halved
- Communication costs reduced by 50%
- Model quality preserved or improved compared to top-2 routing

The router is a learned linear layer that produces a probability distribution over E experts: softmax(W_r · x). The selected expert processes the token; unselected experts contribute nothing.

### Differentiable Load Balancing Loss

To prevent all tokens from routing to the same expert, the paper introduces an auxiliary loss that encourages uniform expert utilization:

```
loss_load_balancing = α · N · Σᵢ fᵢ · Pᵢ
```

Where `fᵢ` is the fraction of tokens dispatched to expert i, `Pᵢ` is the fraction of router probability allocated to expert i, and `α` = 0.01 (swept from 10⁻¹ to 10⁻⁵). The `N` scaling factor ensures the loss magnitude is invariant to the number of experts.

### Expert Capacity

Each expert processes at most:

```
expert_capacity = (tokens_per_batch / num_experts) × capacity_factor
```

- **Capacity factor 1.0–1.25** works best — lower values save memory and compute
- Tokens routed to overflowing experts are **dropped** (passed via residual connection)
- With good load balancing, drop rate stays below 1%

## Training Stability Techniques

| Technique | Detail | Effect |
|-----------|--------|--------|
| **Selective precision** | Router input cast to float32; rest of computation in bfloat16 | Prevents divergence while maintaining throughput (Table 2) |
| **Smaller initialization** | σ = √(s/n) with s=0.1 instead of s=1.0 | Reduces variance, improves final quality (Table 3) |
| **Expert dropout** | Higher dropout in expert FFN layers (e.g., 0.4 vs 0.1 elsewhere) | Prevents expert overfitting, especially on smaller fine-tuning tasks (Table 4) |

Selective precision was a key finding: prior to Switch Transformer, large sparse models could not be trained in lower-precision formats. The router's softmax requires float32 precision to avoid divergence, but all other operations (including all-to-all communication) can use bfloat16.

## Scaling Results

### Step-Basis (Perplexity vs Training Steps)

Switch-Base (64 experts) matches T5-Base perplexity at step **60k vs 450k** — a **7.5× step speedup**.

### Time-Basis (Wall Clock)

For fixed wall-clock time, Switch-Base (64 experts) trains in **1/7th the time** of T5-Base for equivalent perplexity.

### vs Larger Dense Model

Switch-Base (FLOP-matched to T5-Base) **outperforms T5-Large** (3.5× more FLOPs) with a **2.5× time speedup**.

## Downstream Results (Fine-Tuning)

| Model | GLUE | SQuAD | SuperGLUE | Winogrande | TriviaQA |
|-------|------|-------|-----------|------------|----------|
| T5-Base | 84.3 | 85.5 | 75.1 | 66.6 | 24.5 |
| Switch-Base | **86.7** | **87.2** | **79.5** | **73.3** | **30.7** |
| T5-Large | 87.8 | 88.1 | 82.7 | 79.1 | 29.5 |
| **Switch-Large** | **88.5** | **88.6** | **84.7** | **83.0** | **36.9** |

Consistent improvements across reasoning (SuperGLUE, Winogrande), knowledge (TriviaQA), and language understanding (GLUE, SQuAD) tasks.

## Model Distillation

Large sparse models can be compressed into dense models while preserving much of the quality gain:

- **Technique:** Initialize student dense model with teacher's non-expert weights; train with mixed loss (0.75 hard / 0.25 soft targets)
- **99% compression** retains **28% of teacher quality gain**
- **Fine-tuned distillation:** 7.4B teacher → 223M student preserves **30% of SuperGLUE gain**

This demonstrates that MoE quality gains are partially compressible into dense models, making deployment more practical.

## Multilingual Learning

Evaluated on mC4 (101 languages) with mSwitch-Base (FLOP-matched to mT5-Base):

- **All 101 languages** improved in perplexity
- Mean speedup over mT5-Base: **5×**
- **91% of languages** achieved ≥4× speedup

## Trillion-Parameter Models

Switch Transformer scales to the largest neural networks trained at the time using three combined parallelism strategies:

| Parallelism | Dimension | Communication |
|-------------|-----------|---------------|
| Data | Batch (n) | Gradient all-reduce |
| Model | `d_ff` (m) | All-reduce forward/backward |
| Expert | Experts (E) | All-to-all token routing |

Key models trained:

- **Switch-XXL** (395B params, FLOP-matched to T5-XXL) — 4× speedup over T5-XXL
- **Switch-C** (1.6T params) — demonstrated feasibility of trillion-parameter language models

## Significance & Legacy

- **Simplified MoE to the point of practical adoption** — prior [[mixture-of-experts|MoE approaches]] (top-k routing, complex balancing losses, [Shazeer et al., 2017](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md)) were too fragile for production use. Switch Transformer's k=1 routing, selective precision, and load balancing loss became the template for subsequent MoE architectures.
- **First demonstration of bfloat16 training for sparse models** — removed the requirement for float32-only training that had limited MoE scalability.
- **Empirical foundation for the modern MoE renaissance** — Switch Transformer directly enabled architectures like Mixtral 8x7B, Qwen MoE, DeepSeek MoE, and GPT-4's reported MoE structure. The sparse expert pattern became the dominant scaling strategy after the Chinchilla era.
- **Distillation findings** showed MoE quality is partially but not fully compressible — important for deployment decisions.
- **JMLR publication** (2022) — the paper was invited to JMLR after initial arXiv release (2021), a rare distinction indicating high impact.

## Relationship to Other Concepts

- **[[transformer|Transformer]]** — the base architecture that Switch Transformer extends with MoE layers, replacing dense feed-forward networks with expert-switched FFNs
- **[[scaling-laws|Scaling Laws]]** — Switch Transformer demonstrates a distinct scaling dimension (number of experts) not captured by the N-D-C scaling paradigm. Expert count provides sub-linear quality gains independent of model depth/width scaling
- **[[sparse-transformer|Sparse Transformer]]** — a different form of sparsity: Sparse Transformer sparsifies the *attention matrix*, Switch Transformer sparsifies the *parameter access*. The two are orthogonal and could complement each other
- **[[kv-caching|KV Caching]]** — inference optimization for dense attention; MoE introduces additional memory overheads (storing all expert parameters) that KV caching doesn't address
- **[[flash-attention|FlashAttention]]** — IO-aware exact attention; complementary to MoE (one addresses attention compute, the other parameter access)
- **[[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]]** — Switch Transformer is the foundational paper for the modern MoE architecture that Ivanov argues gives MoE models a decisive cost-quality advantage over SLMs

## References

- ([Shazeer et al., 2017](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md)) — Foundational MoE paper: noisy top-k gating, importance/load losses, 137B parameter models
- ([Fedus et al., 2022](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md)) — Original paper, JMLR 2022
- Mixtral 8x7B, Qwen MoE, DeepSeek MoE — direct architectural descendants
