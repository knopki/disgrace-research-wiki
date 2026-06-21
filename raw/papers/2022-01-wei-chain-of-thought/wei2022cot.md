---
title: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
authors:
  - Jason Wei
  - Xuezhi Wang
  - Dale Schuurmans
  - Maarten Bosma
  - Brian Ichter
  - Fei Xia
  - Ed H. Chi
  - Quoc V. Le
  - Denny Zhou
date: 2022-01-28
source_url: https://arxiv.org/abs/2201.11903
ingested: 2026-06-21
description: Introduces chain-of-thought prompting — a simple method eliciting multi-step reasoning in large language models by providing intermediate reasoning step exemplars.
---
# Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

**PDF:** [2201.11903.pdf](2201.11903.pdf)

## Abstract

We explore how generating a chain of thought — a series of intermediate reasoning steps — significantly improves the ability of large language models to perform complex reasoning. In particular, we show how such reasoning abilities emerge naturally in sufficiently large language models via a simple method called chain-of-thought prompting, where a few chain of thought demonstrations are provided as exemplars in prompting.

Experiments on three large language models show that chain-of-thought prompting improves performance on a range of arithmetic, commonsense, and symbolic reasoning tasks. The empirical gains can be striking. For instance, prompting a PaLM 540B with just eight chain-of-thought exemplars achieves state-of-the-art accuracy on the GSM8K benchmark of math word problems, surpassing even finetuned GPT-3 with a verifier.
