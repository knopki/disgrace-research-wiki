---
title: FFN as Key-Value Memories vs Mixture-of-Experts
created: 2026-06-18
updated: 2026-06-18
type: comparison
tags:
  - architecture
  - interpretability
  - mixture-of-experts
  - paper
sources:
  - "[Transformer Feed-Forward Layers Are Key-Value Memories](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md)"
  - "[Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md)"
  - "[Switch Transformers: Scaling to Trillion Parameter Models](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md)"
confidence: high
---

# FFN as Key-Value Memories vs Mixture-of-Experts

Two perspectives on the transformer [[transformer|FFN]] layer that operate at complementary levels: Geva et al. (2021) explains **what the existing dense FFN does** (it's a key-value memory), while the MoE line of work (Shazeer et al., 2017; Fedus et al., 2022) proposes **what to replace the FFN with** (sparsely-activated expert networks).

## Side-by-Side

| Dimension | FFN as Key-Value Memory | Mixture-of-Experts (MoE) |
|-----------|-------------------------|--------------------------|
| **Core claim** | Dense FFN layers are unnormalized key-value memories; each hidden dimension stores a pattern→prediction pair | Dense FFN can be replaced by multiple "expert" FFNs with a learned router that activates only a sparse subset per token |
| **Level** | Interpretability / mechanistic understanding | Architecture / scaling strategy |
| **Keys** | Weight matrix W₁ — each row k_i detects textual patterns in the input | Router weights W_g — learns a softmax distribution over experts, with top-k selection |
| **Values** | Weight matrix W₂ — each column v_i induces a vocabulary distribution | Expert FFN parameters E_i — entire feed-forward sub-networks |
| **Memory access** | Unnormalized, non-negative activation (ReLU) — soft competition between memories | Normalized softmax gating with hard top-k — explicit competition between experts |
| **Composition** | Weighted sum of all active memory values (typically 10–50% of d_m) | Weighted sum of k selected expert outputs (k=1 for Switch, k≥2 for Shazeer) |
| **Sparsity** | **Emergent** — natural activation sparsity from ReLU; 50–90% of memories silent per input | **Engineered** — explicit top-k routing; 99%+ of experts silent (when N is large) |
| **Pattern detection** | Each memory cell responds to specific textual patterns (n-grams, topics) — human-identifiable | Experts implicitly specialize (e.g., punctuation, syntax, domain) — less interpretable per-cell |
| **Parameter count** | 2 matrices: 2·d·d_m parameters | N expert matrices: N · 2·d·d_expert + router parameters |
| **Compute per token** | O(d·d_m) — all memories evaluated | O(d·d_expert·k) — only k experts evaluated, but with all-to-all communication |
| **Number of "memories"** | d_m (typically 4× d) — e.g., 4096 per layer in 247M model | N experts (typically 8–131K) — e.g., 8 (Mixtral) to 131K (Shazeer 137B) |
| **Resolution of memory** | Fine-grained: each hidden dimension is one memory cell | Coarse-grained: each expert is a full FFN sub-network |
| **What scales** | Model depth and width (Chinchilla-style) | Expert count — decouples parameters from compute |
| **Interpretability** | High — keys can be annotated by humans; values' top predictions are meaningful | Low — expert specialization is emergent, harder to analyze per-expert |
| **Adoption** | Universal — every transformer has FFN layers (Geva's analysis applies to all of them) | Optional — used in ~10–20% of major LLMs; dominant at extreme scale |
| **Training** | No special considerations | Requires load-balancing auxiliary losses, expert capacity management, distributed all-to-all |

## How They Relate

### Shared Foundation

Both perspectives start from the same observation: the FFN layer is the dominant consumer of parameters (two-thirds of a transformer's budget) and compute, and both frame it as a memory system where the input selects from a set of stored patterns.

### Where They Diverge

**Geva et al. look inside a single FFN.** The key insight is that the hidden dimension d_m is the number of discrete memory cells, each storing a raw pattern (key) → prediction (value) mapping. The ReLU activation provides an implicit sparsity — irrelevant memories get zero coefficient. The output is a weighted sum of all active memories' value vectors.

**MoE replaces the single FFN with multiple FFNs.** Instead of d_m fine-grained memory cells, MoE has N coarse-grained experts (each a full FFN). The router replaces the key matrix as the pattern detector: it learns what kinds of inputs each expert should handle. The softmax top-k provides explicit sparsity.

### Key Insight: Two Forms of Sparsity

The most revealing connection is sparsity:

- **Geva's sparsity:** Natural, unnormalized, per-memory-cell. A typical input activates 10–50% of 4096 memories, but which ones are active depends on the pattern-key dot product. There's no capacity limit — any memory can activate as strongly as the input warrants.

- **MoE sparsity:** Engineered, normalized, per-expert. Top-k gating with softmax forces exactly k experts active per token, with a load-balancing loss to prevent collapse. Expert capacity imposes a hard upper bound on tokens per expert.

Geva's observation that the number of active memories drops around layer 10 (where semantic patterns dominate) suggests a natural load-balancing dynamic that MoE's engineered approach might be mimicking.

### What GLU Variants Add

The [[glu-variants|GLU variant FFN]] sits between these two: it preserves the dense single-FFN architecture (like Geva) but introduces a gated key interaction (W, V pair replacing K) that adds pattern-dependent modulation. The gate can be seen as a primitive router — not selecting between experts, but modulating which memory cells get how much influence before composition.

## Synthesis

| Aspect | Geva (Key-Value Memory) | MoE |
|--------|------------------------|-----|
| Best for | Understanding and interpreting existing models | Scaling models to trillions of parameters with bounded compute |
| Limitation | Only explains, doesn't improve — no architectural change proposed | Expensive to serve (all experts in memory), harder to train, less interpretable |
| When to use this lens | Model analysis, interpretability, data privacy (membership inference), debugging | Production at scale, parameter-efficient training, distributing compute budget |

The two views are not contradictory — they describe different facets of the same architecture. Geva's key-value memory model explains what the FFN computes; MoE explains how to scale that computation. A complete understanding of transformer FFN layers requires both.

## Cross-Links

- [[ffn-key-value-memories|FFN as Key-Value Memories]] — the Geva et al. interpretability framework
- [[mixture-of-experts|Mixture-of-Experts (MoE)]] — the architecture that replaces dense FFNs with sparse expert networks
- [[switch-transformer|Switch Transformer]] — the k=1 simplification of MoE that enabled trillion-parameter models
- [[transformer|Transformer]] — the architecture that contains the FFN layers under both views
- [[glu-variants|GLU Variants (GEGLU, SwiGLU, ReGLU)]] — a middle ground: dense FFN with gated key modulation
- [[scaling-laws|Scaling Laws]] — MoE adds a scaling dimension (expert count) orthogonal to N-D-C
- [[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]] — production economics debate touching on MoE serving costs
- [[kv-caching|KV Caching]] — orthogonal inference optimisation (attention, not FFN)
