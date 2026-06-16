---
title: Training Compute-Optimal Large Language Models
authors:
  - Jordan Hoffmann
  - Sebastian Borgeaud
  - Arthur Mensch
  - Elena Buchatskaya
  - Trevor Cai
  - Eliza Rutherford
  - Diego de Las Casas
  - Lisa Anne Hendricks
  - Johannes Welbl
  - Aidan Clark
  - Tom Hennigan
  - Eric Noland
  - Katie Millican
  - George van den Driessche
  - Bogdan Damoc
  - Aurelia Guy
  - Simon Osindero
  - Karen Simonyan
  - Erich Elsen
  - Jack W. Rae
  - Oriol Vinyals
  - Laurent Sifre
venue: arXiv preprint
date: 2022-03-29
source_url: https://arxiv.org/abs/2203.15556
pdf: 2203.15556.pdf
description: >
  Landmark study establishing that current large language models are significantly undertrained,
  and that for compute-optimal training, model size and training tokens should be scaled equally.
  Introduces the Chinchilla model (70B parameters, 1.4T tokens) which outperforms much larger models.
ingested: 2026-06-16
tags:
  - scaling-law
  - training
  - model
  - methodology
  - paper
---

# Training Compute-Optimal Large Language Models

**Authors:** Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, Laurent Sifre

**Venue:** arXiv preprint, March 2022  
**DOI:** [10.48550/arXiv.2203.15556](https://doi.org/10.48550/arXiv.2203.15556)  
**PDF:** [2203.15556.pdf](2203.15556.pdf) (5.7 MB)

## Abstract

We investigate the optimal model size and number of tokens for training a transformer language model under a given compute budget. We find that current large language models are significantly undertrained, a consequence of the recent focus on scaling language models whilst keeping the amount of training data constant. By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find that for compute-optimal training, the model size and the number of training tokens should be scaled equally: for every doubling of model size the number of training tokens should also be doubled. We test this hypothesis by training a predicted compute-optimal model, Chinchilla, that uses the same compute budget as Gopher but with 70B parameters and 4x more data. Chinchilla uniformly and significantly outperforms Gopher (280B), GPT-3 (175B), Jurassic-1 (178B), and Megatron-Turing NLG (530B) on a large range of downstream evaluation tasks. This also means that Chinchilla uses substantially less compute for fine-tuning and inference, greatly facilitating downstream usage. As a highlight, Chinchilla reaches a state-of-the-art average accuracy of 67.5% on the MMLU benchmark, greater than a 7% improvement over Gopher.

## Key Claims

- Current LLMs (GPT-3, Gopher, Jurassic-1, MT-NLG) are significantly undertrained — they would achieve better performance per compute unit if trained on more data with fewer parameters
- For compute-optimal training, model size N and training tokens D should scale equally: N ∝ D, doubling model size requires doubling training tokens
- Three independent approaches (fixed parameter count, fixed FLOPs, training large model on reduced data) converge on the same optimal allocation
- Chinchilla (70B params, 1.4T tokens) outperforms Gopher (280B), GPT-3 (175B), Jurassic-1 (178B), and MT-NLG (530B) across a broad evaluation suite
- Chinchilla achieves 67.5% on MMLU — at the time a state-of-the-art result, +7% over Gopher
