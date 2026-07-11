---
title: "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints"
authors:
  - Joshua Ainslie
  - James Lee-Thorp
  - Michiel de Jong
  - Yury Zemlyanskiy
  - Federico Lebrón
  - Sumit Sanghai
date: 2023-05-22
source_url: https://arxiv.org/abs/2305.13245
ingested: 2026-07-11
---

# GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints

**PDF:** [2305.13245.pdf](2305.13245.pdf) (7 pages, EMNLP 2023)

## Abstract

Multi-query attention (MQA), which only uses a single key-value head, drastically speeds up decoder inference. However, MQA can lead to quality degradation, and moreover it may not be desirable to train a separate model just for faster inference. We (1) propose a recipe for uptraining existing multi-head language model checkpoints into models with MQA using 5% of original pre-training compute, and (2) introduce grouped-query attention (GQA), a generalization of multi-query attention which uses an intermediate (more than one, less than number of query heads) number of key-value heads. We show that uptrained GQA achieves quality close to multi-head attention with comparable speed to MQA.
