---
title: RLHF (Reinforcement Learning from Human Feedback)
created: 2026-06-16
updated: 2026-06-16
type: concept
tags:
  - rlhf
  - alignment
  - training
  - technique
sources:
  - "[Training language models to follow instructions with human feedback](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)"
confidence: high
---

# RLHF (Reinforcement Learning from Human Feedback)

A technique for fine-tuning [[transformer|language models]] to align their outputs with human preferences, using human evaluations as a reward signal for reinforcement learning. First applied to broad instruction-following at scale by OpenAI in the InstructGPT paper ([Ouyang et al., 2022](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)), which demonstrated that a 1.3B model fine-tuned with RLHF was preferred by labelers over the 175B GPT-3.

## The Three-Step Procedure

RLHF proceeds in three stages after pretraining:

### Step 1: Supervised Fine-Tuning (SFT)

A pretrained language model is fine-tuned on human-written demonstrations of desired behavior. For InstructGPT, labelers provided ~13k demonstrations on prompts from the OpenAI API and labeler-written prompts. The model is trained for 16 epochs with cosine LR decay and residual dropout of 0.2. Training beyond 1 epoch (when validation loss diverges) empirically improves both reward model scores and human preference ratings ([Ouyang et al., 2022](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)).

### Step 2: Reward Model (RM) Training

A reward model is trained to predict which output a human would prefer. The RM takes a prompt and response and outputs a scalar reward. Training uses pairwise comparisons: labelers rank outputs from the SFT model (typically K=4 to 9 per prompt). The loss is a cross-entropy over the preference labels, where the difference in rewards represents the log-odds of one response being preferred over another.

InstructGPT used a 6B RM (175B RM was unstable during training and less suitable as a value function for RL). The RM dataset contained ~33k training prompts. Labeler agreement was 72.6±1.5% among training labelers and 77.3±1.3% among held-out labelers.

### Step 3: PPO Fine-Tuning

The SFT policy is fine-tuned with Proximal Policy Optimization (PPO) to maximize the reward predicted by the RM. The KL divergence from the SFT model is added as a penalty to prevent the policy from diverging too far (reward hacking). InstructGPT also introduced a **PPO-ptx** variant that mixes PPO updates with pretraining distribution updates (maximising log-likelihood on the pretraining data), which reduces the "alignment tax" — performance regressions on public NLP benchmarks.

## Key Results

### Scale Inefficiency of Raw Size

The headline result: **1.3B InstructGPT (PPO-ptx) outputs are preferred to 175B GPT-3 outputs** despite >100x fewer parameters. 175B InstructGPT is preferred over 175B GPT-3 in 85±3% of evaluations, and 71±4% over few-shot 175B GPT-3. This demonstrates that alignment via human feedback is far more compute-efficient than scaling alone for instruction-following capability.

### Truthfulness

- **[[truthfulqa|TruthfulQA]]:** InstructGPT generates truthful and informative answers ~2x more often than GPT-3
- **Hallucination rate on closed-domain tasks:** 21% (InstructGPT) vs 41% (GPT-3) — roughly halved

### Toxicity and Bias

- **RealToxicityPrompts:** ~25% fewer toxic outputs when prompted to be respectful
- **Winogender / CrowS-Pairs:** No significant improvement over GPT-3 — bias reduction remains an open challenge

### Alignment Tax and Mitigation

RLHF fine-tuning caused regressions on SQuAD, DROP, HellaSwag, and WMT'15 En-Fr translation. The **PPO-ptx** variant (mixing pretraining updates) largely eliminated these regressions without reducing labeler preference scores.

### Generalization

InstructGPT generalizes to held-out labelers (same preference rate) and to out-of-distribution instructions — code summarisation, code QA, and non-English instructions — despite these being rare in the fine-tuning data.

## Dataset

The InstructGPT dataset consisted of prompts from two sources:
- **Labeler-written prompts** (initial bootstrap): plain tasks, few-shot instructions, and user-based prompts derived from API waitlist applications
- **API prompts** from earlier InstructGPT models on the Playground interface

Dataset sizes: SFT ~13k, RM ~33k, PPO ~31k training prompts. Over 96% English. Filtered for PII and deduplicated by user ID.

Use-case distribution: generation (45.6%), open QA (12.4%), brainstorming (11.2%), chat (8.4%), rewrite (6.6%), summarization (4.2%), classification (3.5%), other (3.5%), closed QA (2.6%), extract (1.9%).

## Relationship to Other Techniques

- **Alignment Tax** — RLHF can degrade performance on standard NLP benchmarks; the PPO-ptx variant mitigates this by mixing pretraining updates
- **InstructGPT** — the specific model family produced by applying RLHF to GPT-3; demonstrated that alignment via human feedback is more efficient than scaling alone
- **Constitutional AI** — later approach from [[anthropic|Anthropic]] that replaces human feedback with a written constitution for self-supervision, reducing reliance on human labelers
- **[[instruction-tuning|Instruction Tuning]]** — simpler sibling technique achieving instruction-following via supervised fine-tuning on instruction-formatted data rather than RL from human feedback; contemporaneous with InstructGPT (FLAN, ICLR 2022)
- **[[direct-preference-optimization|DPO (Direct Preference Optimization)]]** — post-InstructGPT technique that eliminates the explicit reward model by directly optimising from preferences
- **[[chain-of-thought|Chain-of-Thought]]** — prompting technique that InstructGPT can follow more reliably than base GPT-3 due to improved instruction-following ability
- **[[flex-prompting|FLEX]]** — later methodology for SLM control using structured XML prompts and logit-based verification, related through shared goal of reliable model steering
- **[[grace|GRACE]]** — later framework for deterministic code generation, which uses Intent-First Architecture similar to RLHF's goal of alignment with user intent

## Limitations

- **Helping vs harmless conflict:** During training, helpfulness to the user was prioritised; the evaluation separately evaluated truthfulness and harmlessness
- **Labeler demographic bias:** The model is aligned to the preferences of ~40 contractors (sourced through Upwork and ScaleAI), not a universal "human values"
- **Still makes simple mistakes:** Fails to follow instructions, makes up facts, gives hedging answers, fails at false-premise detection
- **No bias improvement:** RLHF did not significantly reduce social bias as measured by Winogender and CrowS-Pairs
- **RLHF is expensive:** Collecting human preferences at scale requires significant annotation effort

## Related

- [[dario-amodei|Dario Amodei]] — was VP of Research at OpenAI during the InstructGPT project
- [[anthropic|Anthropic]] — successor alignment research organisation employing Amanda Askell, co-author of this paper
- [[transformer|Transformer]] — the underlying architecture for GPT-3 and InstructGPT
- [[scaling-laws|Scaling Laws]] — contextualises the claim that scaling alone is insufficient for alignment
