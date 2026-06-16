---
title: Mamba / State Space Models (SSM)
created: 2026-06-16
updated: 2026-06-16
type: concept
tags:
  - model
  - architecture
  - inference
  - technique
sources:
  - "[Преодоление галлюцинаций в Mamba-моделях: Экспериментальное исследование RAG-управляемой самокоррекции на примере Qwen 3 Next](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md)"
confidence: medium
---

# Mamba / State Space Models (SSM)

**State Space Models** — a class of sequence architectures that process tokens by iteratively updating a hidden state of fixed size, offering linear-time inference and constant memory relative to sequence length. **Mamba** is the most prominent SSM architecture, designed to rival Transformers on long-context tasks at a fraction of the memory cost.

The core architectural bet: instead of the Transformer's attention over all previous tokens (requiring O(n) growing KV cache per step), Mamba compresses the entire sequence history into a compact, fixed-dimensional state vector at each layer.

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

## Architectural Plasticity

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

## RAG Synergy: "Liquid + Crystallised Intelligence"

Ivanov frames the Mamba+RAG combination as a cognitive complement:

- **Mamba provides "liquid intelligence"** — rapid reasoning, analysis, hypothesis formulation, and belief revision. The plastic state lets it iterate quickly on ideas.
- **RAG provides "crystallised intelligence"** — factual knowledge on demand from external, verifiable sources. The oracle role eliminates the need for SSMs to store precise facts in their compressed state.

This symbiosis lets Mamba compensate for its architectural weakness (hallucination from over-generalisation) without sacrificing its strengths (speed, efficiency, plasticity) ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md)).

## Limitations

- The experimental RAG oracle was an idealised "perfect source" (Grok 3). Real RAG systems have variable retrieval quality — the agent would need additional verification skills to handle noisy sources.
- SSMs generally underperform Transformers on exact-match recall tasks (e.g., looking up a specific fact from context), which is why hybrid architectures are emerging.
- The constant-state property, while memory-efficient, means information can be lost through compression — there is no "attention over history" to recover forgotten details.
- Tested only on one model family (Qwen-Next) and one topic domain (biology). Generality across tasks and models remains open.

## Relationship to Other Concepts

- [[kv-caching|KV Caching]] — Mamba eliminates the KV cache entirely, replacing O(n) memory with O(1) state. The comparison table above quantifies this gap.
- [[retrieval-augmented-generation|RAG]] — RAG is the "oracle" that compensates for Mamba's hallucination tendency. This article positions RAG not as context augmentation but as an external verifier — a role shift from the standard RAG paradigm.
- [[grace|GRACE]] — This work is framed as the next logical step after GRACE: GRACE solved structural context integrity, this addresses factual accuracy through Mamba+RAG self-correction.
- [[hallucination-detection-slm|SLM-based Hallucination Detection]] — a complementary approach: SLM ensemble verifies LLM output post-hoc, while the Mamba+RAG approach corrects the model's own beliefs during generation.
- [[transformer|Transformer]] — the architectural alternative; the comparison is the central framing device of the article.
- [[sparse-transformer|Sparse Transformer]] — like Mamba, aims to overcome the O(n²) attention bottleneck, but via sparse attention patterns rather than state compression.
