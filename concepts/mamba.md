---
title: Mamba / Selective State Space Models (SSM)
created: 2026-06-16
updated: 2026-07-15
type: concept
tags:
  - model
  - architecture
  - inference
  - technique
sources:
  - "[Mamba: Linear-Time Sequence Modeling with Selective State Spaces](raw/papers/2023-12-gu-mamba/gu2023mamba.md)"
  - "[Efficiently Modeling Long Sequences with Structured State Spaces](raw/papers/2021-11-gu-s4/gu2021s4.md)"
  - "[Преодоление галлюцинаций в Mamba-моделях: Экспериментальное исследование RAG-управляемой самокоррекции на примере Qwen 3 Next](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md)"
  - "[Семантическая разметка GRACE как нативный интерфейс для Mamba-моделей](raw/articles/2025-09-21-ivanov-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m/ivanov2025gracemamba.md)"
confidence: high
raw_ingested: true
---

# Mamba / Selective State Space Models (SSM)

**Mamba** (Gu & Dao, 2023) is a sequence-modeling architecture built on **selective state space models (SSMs)**. It is the first linear-time (subquadratic) sequence model to match Transformer quality on language while scaling linearly in sequence length and running ~5× faster at inference. The core idea: make the SSM parameters **input-dependent (selective)** so the model can selectively remember or forget along the sequence, instead of using fixed time-invariant (LTI) dynamics. This addresses the central weakness of prior SSMs — their inability to do content-based reasoning on discrete, information-dense data such as text ([Gu & Dao, 2023](raw/papers/2023-12-gu-mamba/gu2023mamba.md)).

## Origin: S4

Mamba's lineage begins with [[s4-structured-state-spaces|S4]] (Gu, Goel & Ré, Stanford, ICLR 2022 Outstanding Paper HM), the first computationally practical deep SSM. S4 introduced the **Normal Plus Low-Rank (NPLR)** parameterization that reduced SSM computation from O(N²L) to Õ(N+L) by decomposing the HiPPO state matrix into normal + low-rank components and reducing the core operation to a Cauchy kernel. This made deep SSMs feasible for the first time.

S4 achieved SotA on the Long Range Arena (86.09% avg, first to solve Path-X), raw speech classification (98.32%), and matched Transformers on WikiText-103 (20.95 ppl) while being 60× faster at generation. Follow-up work (S4D, Gu et al., 2022) showed diagonal SSMs could match S4's performance with further simplification, laying the groundwork for Mamba's selective state space mechanism ([Gu et al., 2021](raw/papers/2021-11-gu-s4/gu2021s4.md)).

The core architectural bet: instead of the Transformer's attention over all previous tokens (requiring an O(n) growing KV cache per step), Mamba compresses the entire sequence history into a compact, fixed-dimensional state vector at each layer.

## The Selection Mechanism (S6)

Prior structured SSMs were **LTI (linear time-invariant)**: the parameters (Δ, A, B, C) were constant over time, which is what made them computable as efficient global convolutions. Mamba's central insight (Section 3.1–3.2) is that **LTI models cannot select** — from the recurrent view, constant dynamics can't let the model focus on a specific token; from the convolutional view, a static kernel can't handle variable spacing (the Selective Copying task fails). The fix is to make the SSM parameters **functions of the input**:

- Δ (discretization step), B, C become input-dependent: `s_B(x)=Linear_N(x)`, `s_C(x)=Linear_N(x)`, `s_Δ(x)=Broadcast_D(Linear_1(x))`, with `τ_Δ = softplus`.
- This lifts the model from time-invariant (convolution + recurrence) to **time-varying (recurrence/scan only)** — it can no longer use convolutions.
- The selection mechanism is formally equivalent to an RNN gating mechanism (Theorem 1): for N=1, the recurrence becomes `h_t = (1−g_t)·h_{t−1} + g_t·x_t` where `g_t = σ(Linear(x_t))`. Large Δ → reset state, focus on current input; small Δ → persist state, ignore input ([Gu & Dao, 2023](raw/papers/2023-12-gu-mamba/gu2023mamba.md)).

Mechanistic effects of selection: **variable spacing** (filter noise tokens between relevant ones), **filtering context** (reset state to drop irrelevant history — performance improves monotonically with context length), and **boundary resetting** (reset state at document/episode boundaries, which LTI models bleed across).

The paper abbreviates selective SSMs as **S6** ("S4 with selection, computed by scan"). Ablations confirm selection is the real driver: switching S4→S6 lifts induction-head and selective-copying performance dramatically, while the gated-architecture trick (H3-style multiplicative interaction) does not solve selective copying because gating doesn't interact along the sequence axis.

## Hardware-Aware Selective Scan

Because selection kills the convolution formulation, Mamba computes the SSM recurrently with a **parallel associative scan**. The challenge: the expanded state (B, L, D, N) is N× larger than input/output, and materializing it in GPU HBM is the bottleneck. Mamba's solution (Section 3.3, Appendix D) uses three classical techniques:

- **Kernel fusion** — discretize, scan, and multiply-by-C are fused into one kernel. Load (Δ, A, B, C) from HBM to SRAM, do all compute in SRAM, write only the (B, L, D) output back to HBM. Cuts IOs by a factor of N, yielding **20–40×** speedup over a naive PyTorch scan.
- **Parallel scan** — despite being non-linear, the recurrence parallelizes via a work-efficient associative scan.
- **Recomputation** — intermediate states are not stored for backward; they're recomputed in the backward pass, so the selective-SSM layer has the **same activation memory as FlashAttention** (~16 bytes/token vs 32 for attention+MLP).

Measured on A100 (N=16): the fused scan beats FlashAttention-2 beyond sequence length 2K, and is up to **7× faster than attention at 32K** and 20–40× faster than a standard scan.

## The Mamba Architecture

Mamba simplifies prior SSM architectures (which interleaved an H3/linear-attention block with an MLP block) by **fusing the two into one homogeneous block** (Section 3.4), inspired by the Gated Attention Unit (GAU). Each block:

- Expands model dimension D by expansion factor E=2 (default).
- Has a main branch: a short convolution → selective SSM, plus a SwiGLU-style gated MLP branch (SiLU activation).
- Uses two stacked blocks to match the 12D² params of a Transformer's MHA+MLP.
- Uses LayerNorm (optional, RetNet-style), SiLU/Swish activation.

Notably there is **no attention and no separate MLP block** — the SSM itself is the sequence-mixing primitive. Real-valued SSMs are the default (complex numbers help only on continuous modalities like audio/video, not discrete text/DNA).

## Memory Wall: SSM vs Transformer

The fundamental difference is memory scaling. Transformers require a KV cache that grows linearly with sequence length, eventually dominating GPU memory. SSMs maintain a constant state size regardless of context length.

For Qwen-Next-80B-A3B-Instruct (a hybrid Mamba-Transformer model), the SSM state occupies ~24 MB. For comparison, Transformer models at 100K token context length ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md)):

| Model | 1K tokens | 10K tokens | 100K tokens | 1M tokens |
|-------|-----------|------------|-------------|-----------|
| **LLaMA-3.3-70B** | 0.326 GB | 3.26 GB | **32.6 GB** | 326 GB |
| **LLaMA-3.1-405B** | 0.516 GB | 5.16 GB | **51.6 GB** | 516 GB |
| **DeepSeek-V3 (MoE)** | 1.748 GB | 17.48 GB | **174.8 GB** | 1,748 GB |
| **Mamba (80B state)** | — | — | **~0.024 GB** | **~0.024 GB** |

At 100K tokens, LLaMA-3.3-70B needs ~1350× more memory for its cache than Mamba's entire hidden state. This gap widens with longer contexts ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md)).

## Empirical Results

**Synthetic tasks.** Mamba solves Selective Copying and Induction Heads perfectly and **extrapolates to 1M-length sequences (4000× longer than training)**, while no other method goes beyond 2×. On induction heads, Mamba (74K params, S6) holds perfect accuracy from sequence length 2⁶ to 2²⁰; MHA-RoPE/xPos collapse past 2¹⁰, H3 and Hyena degrade to ~5–44% ([Gu & Dao, 2023](raw/papers/2023-12-gu-mamba/gu2023mamba.md)).

**Language modeling (scaling laws, Pile, Chinchilla protocol, 125M–1.3B).** Mamba is the first attention-free model to match a strong Transformer++ recipe (RoPE + SwiGLU + RMSNorm, the LLaMA/PaLM recipe) and improves as sequence length grows. Downstream zero-shot (Table 3): **Mamba is best-in-class at every size and generally matches baselines twice its size.** Examples:
- Mamba-1.4B avg 59.7 vs Pythia-1.4B 55.2 / RWKV-1.5B 54.3; Pile ppl 6.80 vs 7.51.
- Mamba-2.8B avg 63.3 vs Pythia-2.8B 59.1 / RWKV-3B 59.6; approaches GPT-J-6B (63.0) and Pythia-6.9B (61.7) at ~2.4× fewer params.
- The abstract's headline: **Mamba-3B outperforms same-size Transformers and matches Transformers twice its size** (e.g. ~4 points higher avg common-sense reasoning than Pythia-3B, exceeding Pythia-7B) ([Gu & Dao, 2023](raw/papers/2023-12-gu-mamba/gu2023mamba.md)).

**DNA (genomics).** On HG38 pretraining, Mamba's perplexity **improves with context up to 1M tokens**, while HyenaDNA gets worse with longer context (LTI can't ignore noise in a huge kernel). On Great Apes species classification fine-tuned at 1M context: Mamba-7M reaches **81.31%** vs HyenaDNA-1.4M 54.87% ([Gu & Dao, 2023](raw/papers/2023-12-gu-mamba/gu2023mamba.md)).

**Audio.** On YouTubeMix autoregressive waveform pretraining, Mamba improves with longer context. On SC09 speech generation, a small Mamba-UNet outperforms much larger GAN/diffusion baselines (WaveNet, DiffWave, SaShiMi); a parameter-matched larger model improves FID dramatically. Caveat: on audio (a uniformly-sampled continuous signal), the LTI (S4→S6 ablation) actually *hurts* — continuous modalities benefit from LTI inductive bias; the paper finds inner U-Net layers need not be selective but outer layers near raw signal should be LTI ([Gu & Dao, 2023](raw/papers/2023-12-gu-mamba/gu2023mamba.md)).

**Efficiency.** The fused scan beats FlashAttention-2 beyond 2K sequence length; end-to-end inference throughput is **4–5× higher than a same-size Transformer** (no KV cache → much higher batch sizes). A Mamba-6.9B (untrained) has higher inference throughput than a 5× smaller Transformer-1.3B. Memory footprint is comparable to a heavily-optimized Transformer (each selective SSM stores ~16 bytes/token) ([Gu & Dao, 2023](raw/papers/2023-12-gu-mamba/gu2023mamba.md)).

## Architectural Plasticity & Hallucination (Ivanov line)

The fixed-size state is both Mamba's strength and its weakness:

- **Strength:** Enables processing of arbitrarily long sequences with bounded memory. Makes iterative agent loops (where the model repeatedly re-reads long contexts) economically viable.
- **Weakness:** The compression into a fixed state forces aggressive semantic generalisation, making SSMs more prone to factual hallucination than Transformers, which can attend to specific tokens in the context.

However, this same compression creates **plasticity** — the ability to rapidly overwrite the internal state when new evidence arrives. Unlike a Transformer whose attention logits are influenced by every cached token, Mamba can fully replace its belief state when presented with authoritative external information ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md)).

## RAG-Driven Self-Correction

An experimental study on **Qwen-Next-80B-A3B-Instruct** (a hybrid Mamba-Transformer model) tested Mamba's plasticity directly. The setup:

1. **Phase 1 — Knowledge Formation.** The agent built a verified description of killer whale biology from a RAG oracle.
2. **Phase 2 — Self-Confrontation.** The agent was shown its own previously generated text containing popular myths, anthropomorphic interpretations, and factual errors.
3. **Phase 3 — Critical Analysis.** The agent identified questionable claims and formulated precise, verifiable scientific queries in JSON format for the RAG tool.
4. **Phase 4 — Belief State Overwrite.** The agent discarded its prior beliefs entirely and synthesised a new, scientifically accurate text from the RAG-verified facts.

The key finding: the model did not simply "add" corrections — it **completely restructured its narrative**. Anthropomorphic concepts (e.g., "grief") were replaced with scientific terminology ("post-mortem attentive behaviour" explained through stress and instinct). A factual error (confusing Project CETI's target species) was identified and corrected. The experiment reported 100% success in identifying and correcting all error types: anthropomorphisms, logical exaggerations, and factual inaccuracies ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md)).

### The Tool-Use Capability

A notable finding was the agent's ability to translate vague intuitions into precise, decomposable scientific queries:

> Intuition: "Is it true that killer whales grieve for dead calves?"
> Formulated RAG query: "Are there scientific publications proving that killer whales experience the emotion of 'grief' as a subjective experience, rather than only exhibiting behaviour interpreted by humans as grief?"

This query formulation — moving from a popular question to a falsifiable scientific hypothesis — is described as critical for effective RAG agents ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md)).

## Hybrid Architectures

The Qwen-Next-80B-A3B-Instruct used in the experiment is a **hybrid Mamba-Transformer** model — combining SSM layers for efficient long-context processing with Transformer attention layers for high-precision retrieval. This hybrid approach addresses Mamba's hallucination tendency by retaining attention-based exact retrieval where needed, while relying on SSM compression for the bulk of computation.

Note: the Mamba paper itself finds that interleaving Mamba blocks with MHA (Mamba-MHA) is only *slightly* better than the homogeneous architecture — somewhat surprising given other works report large gains from SSM+Attention combinations ([Gu & Dao, 2023](raw/papers/2023-12-gu-mamba/gu2023mamba.md)).

## RAG Synergy: "Liquid + Crystallised Intelligence"

Ivanov frames the Mamba+RAG combination as a cognitive complement:

- **Mamba provides "liquid intelligence"** — rapid reasoning, analysis, hypothesis formulation, and belief revision. The plastic state lets it iterate quickly on ideas.
- **RAG provides "crystallised intelligence"** — factual knowledge on demand from external, verifiable sources. The oracle role eliminates the need for SSMs to store precise facts in their compressed state.

This symbiosis lets Mamba compensate for its architectural weakness (hallucination from over-generalisation) without sacrificing its strengths (speed, efficiency, plasticity) ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md)).

## GRACE as Native Interface

Experimental research demonstrated that GRACE (Graph-RAG Anchored Code Engineering) semantic markup functions as a **native interface language** for Mamba models ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m/ivanov2025gracemamba.md)). Qwen-3-Next (hybrid Mamba-Transformer, >75K token context) achieved >99.9% context reconstruction accuracy with GRACE markup.

**Reconstruction from internal graph.** Mamba does not "cite" text via attention like a Transformer. With GRACE, it *reconstructs* code from its internal knowledge graph — a reconstruction query becomes node serialisation, not paraphrase. Without GRACE, reconstruction degrades into imprecise summarisation from the compressed state, losing precision in string literals, escape sequences, and inline comments.

**Dual graph role.** The GRACE graph serves qualitatively different functions depending on architecture:
- For **Transformers** — passive attention assistant. XML tags act as beacons for the attention mechanism to correlate distant code sections.
- For **Mamba** — active verification shield. Mamba builds its own emergent graph in its compressed state; the explicit GRACE scaffold becomes a "ground truth" blueprint that the model can continuously reconcile its internal state against, fundamentally reducing structural hallucinations.

**Semantic slices.** Mamba can perform semantic slices on its internal state — answering analytical queries ("show all imports", "group classes by role", "find functions with database access lacking validation") directly from graph nodes rather than raw text. This enables RAG agents on Mamba to execute complex analytical queries orders of magnitude more efficiently than traditional text-based RAG.

**The symbiotic architecture.** The research proposes a three-component production system: (1) Human architect creates machine-readable code blueprints (GRACE); (2) Mamba builds a queryable internal graph from the blueprint, using the explicit graph as active verification; (3) Built-in RAG cycle uses attention to verify leaf-level facts, compensating for SSM's tendency to generalise. This moves from stochastic generation toward deterministic synthesis. ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m/ivanov2025gracemamba.md))

## Relationship to Other Concepts

- [[s4-structured-state-spaces|S4]] — direct predecessor; S4's NPLR parameterization and Cauchy kernel made deep SSMs computationally feasible. Mamba's selection mechanism (S6) is built on top of the S4 diagonal-SSM formulation, lifting LTI → time-varying.
- [[kv-caching|KV Caching]] — Mamba eliminates the KV cache entirely, replacing O(n) memory with O(1) state. The comparison table above quantifies this gap.
- [[flash-attention|FlashAttention]] — Mamba's fused selective-scan kernel matches FlashAttention's memory/token and beats its speed beyond 2K sequence length; both are IO-aware GPU kernels.
- [[retrieval-augmented-generation|RAG]] — RAG is the "oracle" that compensates for Mamba's hallucination tendency. This article positions RAG not as context augmentation but as an external verifier — a role shift from the standard RAG paradigm.
- [[grace|GRACE]] — two dimensions: (1) GRACE provides a native interface for Mamba: reconstruction-from-graph (vs citation), semantic slice queries, active verification against the model's emergent state; (2) Mamba+RAG self-correction (hallucination study) is the next logical step after GRACE — structural integrity → factual accuracy.
- [[hallucination-detection-slm|SLM-based Hallucination Detection]] — a complementary approach: SLM ensemble verifies LLM output post-hoc, while the Mamba+RAG approach corrects the model's own beliefs during generation.
- [[transformer|Transformer]] — the architectural alternative; the central framing device of the Mamba paper (5× inference throughput, linear vs quadratic scaling, quality match at half the size).
- [[sparse-transformer|Sparse Transformer]] — like Mamba, aims to overcome the O(n²) attention bottleneck, but via sparse attention patterns rather than state compression.
- [[mixture-of-experts|Mixture-of-Experts]] — orthogonal scaling strategy (sparse expert activation); can be combined with Mamba (hybrid backbones).
