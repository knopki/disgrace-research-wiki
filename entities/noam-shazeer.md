---
title: Noam Shazeer
created: 2026-06-17
updated: 2026-06-17
type: entity
tags:
  - model
  - architecture
  - technique
sources:
  - "[Outrageously Large Neural Networks](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md)"
  - "[Fast Transformer Decoding: One Write-Head is All You Need](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md)"
  - "[GLU Variants Improve Transformer](raw/papers/2020-02-shazeer-glu-variants/shazeer2020gluvariants.md)"
  - "[Attention Is All You Need](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md)"
  - "[Switch Transformers](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md)"
---

## Overview

**Noam Shazeer** — Google researcher and one of the most influential architects of modern Transformer-based deep learning. His work spans foundational architectural innovations: the Transformer itself, Mixture-of-Experts scaling, Multi-Query Attention, GLU-based feed-forward variants, and the Adafactor optimizer. Several of his papers are single-authored, reflecting deep and independent contributions to the field.

## Key Contributions

- **[[transformer|Transformer]] (2017):** Co-authored "Attention Is All You Need," the paper that introduced the Transformer architecture and displaced RNNs/LSTMs. ([Vaswani et al., 2017](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md))

- **[[mixture-of-experts|Sparsely-Gated Mixture-of-Experts]] (2017):** Lead author of the foundational MoE paper introducing noisy top-k gating, importance/load balancing losses, and 137B-parameter sparse models. Established the template for all subsequent MoE architectures. ([Shazeer et al., 2017](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md))

- **[[multi-query-attention|Multi-Query Attention (MQA)]] (2019):** Single-author paper identifying the memory-bandwidth bottleneck in autoregressive decoding and proposing shared K/V across heads — achieving 12× decoder speedup and laying the groundwork for GQA. ([Shazeer, 2019](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md))

- **[[glu-variants|GLU Variants (GEGLU, SwiGLU, ReGLU)]] (2020):** Single-author paper proposing gated FFN variants for Transformer — SwiGLU became the default activation in virtually all post-2022 LLMs (LLaMA, PaLM, Gemma, Mistral, Qwen). ([Shazeer, 2020](raw/papers/2020-02-shazeer-glu-variants/shazeer2020gluvariants.md))

- **[[switch-transformer|Switch Transformer]] (2021):** Co-author of the simplified top-1 MoE routing that made trillion-parameter sparse models practical. ([Fedus, Zoph & Shazeer, 2022](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md))

- **Adafactor optimizer (2018):** Co-developed with Mitchell Stern — adaptive learning rates with sublinear memory cost, used in T5 and subsequent Google models.

## Affiliations

- Google (Brain / Research)

## Related

- [[transformer|Transformer]] — co-inventor
- [[mixture-of-experts|Mixture-of-Experts (MoE)]] — foundational formulation
- [[multi-query-attention|Multi-Query Attention (MQA)]] — introduced shared K/V attention
- [[glu-variants|GLU Variants (GEGLU, SwiGLU, ReGLU)]] — proposed gated FFN for Transformer
- [[switch-transformer|Switch Transformer]] — simplified MoE routing
