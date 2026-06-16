---
title: Scaling Laws for Neural Language Models
authors:
  - Jared Kaplan
  - Sam McCandlish
  - Tom Henighan
  - Tom B. Brown
  - Benjamin Chess
  - Rewon Child
  - Scott Gray
  - Alec Radford
  - Jeffrey Wu
  - Dario Amodei
venue: arXiv preprint
date: 2020-01-23
source_url: https://arxiv.org/abs/2001.08361
pdf: 2001.08361.pdf
description: >
  Empirical study establishing power-law scaling relationships between language model
  performance and model size, dataset size, and training compute. Foundational work
  on neural scaling laws.
ingested: 2026-06-16
tags:
  - scaling-law
  - training
  - model
  - methodology
---

# Scaling Laws for Neural Language Models

**Authors:** Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, Dario Amodei

**Venue:** arXiv preprint, January 2020  
**DOI:** [10.48550/arXiv.2001.08361](https://doi.org/10.48550/arXiv.2001.08361)  
**PDF:** [2001.08361.pdf](2001.08361.pdf) (2.4 MB)

## Abstract

We study empirical scaling laws for language model performance on the cross-entropy loss. The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude. Other architectural details such as network width or depth have minimal effects within a wide range. Simple equations govern the dependence of overfitting on model/dataset size and the dependence of training speed on model size. These relationships allow us to determine the optimal allocation of a fixed compute budget. Larger models are significantly more sample-efficient, such that optimally compute-efficient training involves training very large models on a relatively modest amount of data and stopping significantly before convergence.

## Authors (all equal contribution, ordered randomly)

1. **Jared Kaplan** — Johns Hopkins University (at time of publication), later Anthropic
2. **Sam McCandlish** — OpenAI
3. **Tom Henighan** — OpenAI
4. **Tom B. Brown** — OpenAI
5. **Benjamin Chess** — OpenAI
6. **Rewon Child** — OpenAI
7. **Scott Gray** — OpenAI
8. **Alec Radford** — OpenAI
9. **Jeffrey Wu** — OpenAI
10. **Dario Amodei** — OpenAI (later Anthropic)

## Key Claims

- Cross-entropy loss follows smooth power-laws in N (parameters), D (data), and C (compute)
- Architectural details (depth, width, attention heads) have minimal effect — scale dominates
- Larger models are more sample-efficient
- Compute-optimal training: train large models, stop early (~10% above converged loss)
- Predicted breakdown at ~10^4 PF-days (since refined by Chinchilla scaling laws)
