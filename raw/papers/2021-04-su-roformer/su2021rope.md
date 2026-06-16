---
title: "RoFormer: Enhanced Transformer with Rotary Position Embedding"
authors:
  - Jianlin Su
  - Yu Lu
  - Shengfeng Pan
  - Ahmed Murtadha
  - Bo Wen
  - Yunfeng Liu
affiliations: Zhuiyi Technology Co., Ltd.
date: 2021-04-20
source_url: https://arxiv.org/abs/2104.09864
pdf: 2104.09864.pdf
description: >
  Introduces Rotary Position Embedding (RoPE) — a multiplicative position encoding
  that rotates query and key vectors by angles proportional to their position index,
  naturally encoding relative position in the attention score. Enables long-term decay,
  sequence-length flexibility, and linear attention compatibility. RoPE has become the
  dominant position encoding in post-2023 LLMs (LLaMA, Mistral, Qwen, Gemma).
ingested: 2026-06-16
tags:
  - architecture
  - technique
  - training
  - paper
---

# RoFormer: Enhanced Transformer with Rotary Position Embedding

Full text: [2104.09864.pdf](2104.09864.pdf) (14 pages, arXiv v5)

**Authors:** Jianlin Su, Yu Lu, Shengfeng Pan, Ahmed Murtadha, Bo Wen, Yunfeng Liu (Zhuiyi Technology Co., Ltd.)

**Submitted:** 2021-04-20 (v5: 2023-11-08) | **Category:** cs.CL

## Abstract

Position encoding recently has shown effective in the transformer architecture. It enables valuable supervision for dependency modeling between elements at different positions of the sequence. In this paper, we first investigate various methods to integrate positional information into the learning process of transformer-based language models. Then, we propose a novel method named Rotary Position Embedding(RoPE) to effectively leverage the positional information. Specifically, the proposed RoPE encodes the absolute position with a rotation matrix and meanwhile incorporates the explicit relative position dependency in self-attention formulation. Notably, RoPE enables valuable properties, including the flexibility of sequence length, decaying inter-token dependency with increasing relative distances, and the capability of equipping the linear self-attention with relative position encoding. Finally, we evaluate the enhanced transformer with rotary position embedding, also called RoFormer, on various long text classification benchmark datasets. Our experiments show that it consistently overcomes its alternatives. Furthermore, we provide a theoretical analysis to explain some experimental results. RoFormer is already integrated into Huggingface: https://huggingface.co/docs/transformers/model_doc/roformer.

## Key Contributions

1. **Rotary Position Embedding (RoPE)** — encodes absolute position via a rotation matrix while incorporating explicit relative position dependency in the self-attention formulation. Unlike additive PE (Vaswani et al.), RoPE is multiplicative: it rotates the query and key vectors by an angle proportional to their position index.
2. **Theoretical derivation** — proves that relative position encoding can be formulated as rotating the affine-transformed word embeddings, formalized through 2D complex number multiplication, then generalized to d-dimensions via d/2 rotation sub-spaces.
3. **Properties** — long-term decay (inner-product decays with relative distance), sequence length flexibility (no maximum length bound), compatibility with linear self-attention (PerFormer-style).
4. **Experimental validation** — RoFormer achieves 27.5 vs 27.3 BLEU on WMT 2014 EN-DE translation; faster MLM convergence vs BERT; outperforms BERT on 3/6 GLUE tasks; enables relative position encoding in PerFormer linear attention; demonstrates 1.5% absolute improvement on Chinese long-text CAIL2019-SCM at 1024 tokens vs WoBERT.

## Limitations (from paper)

- No thorough explanation of why RoPE converges faster than other position encoding strategies.
- No faithful explanation for superior long-text performance despite long-term decay property being similar to existing position encoding mechanisms.
- Requires Transformer-based hardware resources for pre-training.

## Architecture Detail

RoPE operates by dividing the d-dimensional space into d/2 sub-spaces, each rotated by a different frequency θ_i = 10000^{-2(i-1)/d} (same schedule as sinusoidal PE). For each 2D sub-space at position m, the rotation is:

```
R(m) = [[cos(mθ_i), -sin(mθ_i)],
        [sin(mθ_i),  cos(mθ_i)]]
```

The query and key at position m are computed as:

```
q_m = R_Θ,m · W_q · x_m
k_n = R_Θ,n · W_k · x_n
```

The attention score q_m^T k_n then naturally encodes the relative position (n-m) through the rotation matrix product, without explicit relative position embeddings.
