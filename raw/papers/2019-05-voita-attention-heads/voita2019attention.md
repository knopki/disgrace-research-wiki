---
source_url: https://arxiv.org/abs/1905.09418
ingested: 2026-06-17
title: "Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned"
authors:
  - Elena Voita
  - David Talbot
  - Fedor Moiseev
  - Rico Sennrich
  - Ivan Titov
date: 2019-05-23
venue: ACL 2019
---

# Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned

**PDF:** [1905.09418.pdf](1905.09418.pdf)

## Abstract

Multi-head self-attention is a key component of the Transformer, a state-of-the-art architecture for neural machine translation. In this work we evaluate the contribution made by individual attention heads in the encoder to the overall performance of the model and analyze the roles played by them. We find that the most important and confident heads play consistent and often linguistically-interpretable roles. When pruning heads using a method based on stochastic gates and a differentiable relaxation of the L0 penalty, we observe that specialized heads are last to be pruned. Our novel pruning method removes the vast majority of heads without seriously affecting performance. For example, on the English-Russian WMT dataset, pruning 38 out of 48 encoder heads results in a drop of only 0.15 BLEU.
