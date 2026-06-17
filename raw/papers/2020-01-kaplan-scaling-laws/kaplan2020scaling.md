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

**PDF:** [2001.08361.pdf](2001.08361.pdf)

## Abstract

We study empirical scaling laws for language model performance on the cross-entropy loss. The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude. Other architectural details such as network width or depth have minimal effects within a wide range. Simple equations govern the dependence of overfitting on model/dataset size and the dependence of training speed on model size. These relationships allow us to determine the optimal allocation of a fixed compute budget. Larger models are significantly more sample-efficient, such that optimally compute-efficient training involves training very large models on a relatively modest amount of data and stopping significantly before convergence.
