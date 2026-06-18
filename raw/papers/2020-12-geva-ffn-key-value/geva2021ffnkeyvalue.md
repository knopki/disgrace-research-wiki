---
title: "Transformer Feed-Forward Layers Are Key-Value Memories"
authors:
  - Mor Geva
  - Roei Schuster
  - Jonathan Berant
  - Omer Levy
date: 2020-12-29
venue: EMNLP 2021
source_url: https://arxiv.org/abs/2012.14913
ingested: 2026-06-18
description: "Shows that transformer feed-forward layers operate as key-value memories where keys detect human-interpretable patterns (n-grams, topics) and values induce distributions over the output vocabulary — lower layers capture shallow patterns, upper layers semantic ones."
---

# Transformer Feed-Forward Layers Are Key-Value Memories

**PDF:** [2012.14913.pdf](2012.14913.pdf)

**Authors:** Mor Geva (Tel-Aviv University, Allen Institute for AI), Roei Schuster (Tel-Aviv University, Cornell Tech), Jonathan Berant (Tel-Aviv University, Allen Institute for AI), Omer Levy (Tel-Aviv University)

## Abstract

Feed-forward layers constitute two-thirds of a transformer model's parameters, yet their role in the network remains under-explored. We show that feed-forward layers in transformer-based language models operate as key-value memories, where each key correlates with textual patterns in the training examples, and each value induces a distribution over the output vocabulary. Our experiments show that the learned patterns are human-interpretable, and that lower layers tend to capture shallow patterns, while upper layers learn more semantic ones. The values complement the keys' input patterns by inducing output distributions that concentrate probability mass on tokens likely to appear immediately after each pattern, particularly in the upper layers. Finally, we demonstrate that the output of a feed-forward layer is a composition of its memories, which is subsequently refined throughout the model's layers via residual connections to produce the final output distribution.
