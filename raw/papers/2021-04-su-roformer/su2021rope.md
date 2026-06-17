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

**PDF:** [2104.09864.pdf](2104.09864.pdf)

## Abstract

Position encoding recently has shown effective in the transformer architecture. It enables valuable supervision for dependency modeling between elements at different positions of the sequence. In this paper, we first investigate various methods to integrate positional information into the learning process of transformer-based language models. Then, we propose a novel method named Rotary Position Embedding(RoPE) to effectively leverage the positional information. Specifically, the proposed RoPE encodes the absolute position with a rotation matrix and meanwhile incorporates the explicit relative position dependency in self-attention formulation. Notably, RoPE enables valuable properties, including the flexibility of sequence length, decaying inter-token dependency with increasing relative distances, and the capability of equipping the linear self-attention with relative position encoding. Finally, we evaluate the enhanced transformer with rotary position embedding, also called RoFormer, on various long text classification benchmark datasets. Our experiments show that it consistently overcomes its alternatives. Furthermore, we provide a theoretical analysis to explain some experimental results. RoFormer is already integrated into Huggingface: https://huggingface.co/docs/transformers/model_doc/roformer.
