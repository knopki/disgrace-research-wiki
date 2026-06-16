---
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
authors:
  - Rafael Rafailov
  - Archit Sharma
  - Eric Mitchell
  - Stefano Ermon
  - Christopher D. Manning
  - Chelsea Finn
source_url: https://arxiv.org/abs/2305.18290
ingested: 2026-06-16
---

# Direct Preference Optimization: Your Language Model is Secretly a Reward Model

Full text: [`2305.18290.pdf`](2305.18290.pdf) (27 pages)

Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn. Stanford University / CZ Biohub. 37th Conference on Neural Information Processing Systems (NeurIPS 2023).

## Abstract

> While large-scale unsupervised language models (LMs) learn broad world knowledge and some reasoning skills, achieving precise control of their behavior is difficult due to the completely unsupervised nature of their training. Existing methods for gaining such steerability collect human labels of the relative quality of model generations and fine-tune the unsupervised LM to align with these preferences, often with reinforcement learning from human feedback (RLHF). However, RLHF is a complex and often unstable procedure, first fitting a reward model that reflects the human preferences, and then fine-tuning the large unsupervised LM using reinforcement learning to maximize this estimated reward without drifting too far from the original model. In this paper we introduce a new parameterization of the reward model in RLHF that enables extraction of the corresponding optimal policy in closed form, allowing us to solve the standard RLHF problem with only a simple classification loss. The resulting algorithm, which we call Direct Preference Optimization (DPO), is stable, performant, and computationally lightweight, eliminating the need for sampling from the LM during fine-tuning or performing significant hyperparameter tuning. Our experiments show that DPO can fine-tune LMs to align with human preferences as well as or better than existing methods. Notably, fine-tuning with DPO exceeds PPO-based RLHF in ability to control sentiment of generations, and matches or improves response quality in summarization and single-turn dialogue while being substantially simpler to implement and train.

## Key Results

| Setting | DPO Performance | Baseline Comparison |
|---------|----------------|-------------------|
| IMDb Sentiment | Best reward/KL frontier | Strictly dominates PPO (including PPO-GT with ground-truth rewards) |
| TL;DR Summarization | ~61% win rate (temp 0.0) | PPO ~57% at optimal temp 0.0; more robust to sampling temperature |
| Anthropic-HH Dialogue | Only efficient method that improves over chosen completions | Matches or beats Best of 128 (computationally expensive baseline) |
| CNN/DailyMail OOD | 36% win rate (temp 0), 31% (temp 0.25) | PPO 26% (temp 0), 23% (temp 0.25) |

## Implementation

Default hyperparameters: β = 0.1 (0.5 for summarization), batch size 64, RMSprop optimizer, learning rate 1e-6, linear warmup over 150 steps. Models tested up to 6B parameters (GPT-J-6B).
