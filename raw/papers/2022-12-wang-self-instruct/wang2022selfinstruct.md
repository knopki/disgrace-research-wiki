---
source_url: https://arxiv.org/abs/2212.10560
title: "Self-Instruct: Aligning Language Models with Self-Generated Instructions"
authors:
  - Yizhong Wang
  - Yeganeh Kordi
  - Swaroop Mishra
  - Alisa Liu
  - Noah A. Smith
  - Daniel Khashabi
  - Hannaneh Hajishirzi
affiliations: University of Washington / Allen Institute for AI
date: 2022-12-20
venue: arXiv preprint; ACL 2023
ingested: 2026-06-25
---
# Self-Instruct: Aligning Language Models with Self-Generated Instructions

**PDF:** [2212.10560.pdf](2212.10560.pdf)

## Abstract

Large "instruction-tuned" language models (Finetuned Language Nets, T0, InstructGPT, etc.) have shown remarkable zero-shot generalization across a wide range of tasks by training on collections of human-written instruction data. However, such human-written data is often limited in quantity, diversity, and creativity. We introduce SELF-INSTRUCT, a framework for improving the instruction-following capabilities of pretrained language models by bootstrapping off their own generations. Our pipeline generates instructions, inputs, and outputs from the LM itself, then filters invalid or similar ones before using them to fine-tune the original model. Applying our method to vanilla GPT-3, we achieve a 33% absolute improvement over the original model on SUPER-NATURALINSTRUCTIONS, on par with the performance of InstructGPT_001, which is trained with private user data and human-annotated labels. Human evaluation on a set of expert-created novel tasks shows that our model outperforms models trained on existing public instruction datasets, leaving only a 5% absolute gap behind InstructGPT_001.
