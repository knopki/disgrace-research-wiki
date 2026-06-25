---
title: RLHF (Reinforcement Learning from Human Feedback)
created: 2026-06-16
updated: 2026-06-25
type: concept
tags:
  - rlhf
  - alignment
  - training
  - technique
sources:
  - "[Training language models to follow instructions with human feedback](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)"
  - "[Constitutional AI: Harmlessness from AI Feedback](raw/papers/2022-12-bai-constitutional-ai/bai2022constitutional.md)"
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

The SFT policy is fine-tuned with Proximal Policy Optimization (PPO) to maximize the reward predicted by the RM. The environment is a bandit: it presents a random prompt, receives a response, and returns the RM reward. The KL divergence from the SFT model is added as a per-token penalty to prevent reward hacking. The value function is initialized from the RM.

InstructGPT also introduced a **PPO-ptx** variant that mixes PPO updates with pretraining distribution updates, reducing the "alignment tax". The combined objective:

```
objective(φ) = E_{(x,y)~D_RL}[ r_θ(x,y) − β·log(π_φ_RL(y|x) / π_SFT(y|x)) ] + γ·E_{x~D_pretrain}[ log(π_φ_RL(x)) ]
```

where π_φ_RL is the learned RL policy, π_SFT is the supervised model, D_pretrain is the pretraining distribution, β controls KL penalty strength, and γ controls pretraining mix. For standard PPO, γ=0. The value function is initialized from the RM. Unless specified, "InstructGPT" refers to PPO-ptx models.

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

### FLAN/T0 Comparison

InstructGPT significantly outperforms models fine-tuned on public NLP instruction datasets. On the API prompt distribution, 175B InstructGPT outputs are preferred over FLAN (Wei et al., 2021) 78±4% of the time and over T0 (Sanh et al., 2021) 79±4% of the time ([Ouyang et al., 2022](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)). The paper attributes this to two factors: (1) public NLP datasets are dominated by classification and QA (~18% of API usage), while open-ended generation and brainstorming make up ~57% of real-world usage; (2) public datasets lack the diversity of real user prompts.

### Compute Cost of Alignment

RLHF is far more cost-effective than scaling alone. Training the 175B InstructGPT model requires ([Ouyang et al., 2022](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)):

| Stage | Compute (PF/s-days) | vs GPT-3 Pretrain |
|-------|--------------------|-------------------|
| SFT (175B) | 4.9 | 0.1% |
| PPO-ptx (175B) | 60 | 1.6% |
| GPT-3 pretraining (reference) | 3,640 | 100% |

The cost of data collection and training runs is a fraction of GPT-3 pretraining, yet delivers models preferred 85% of the time over the 100× larger base model. This suggests that, for instruction-following capability, investing in alignment is currently more cost-effective than training larger models ([Ouyang et al., 2022](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)).

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
- **[[constitutional-ai|Constitutional AI]]** — later approach from [[anthropic|Anthropic]] that replaces human feedback with a written constitution for self-supervision, reducing reliance on human labelers; introduces RLAIF (RL from AI Feedback)
- **[[instruction-tuning|Instruction Tuning]]** — simpler sibling technique achieving instruction-following via supervised fine-tuning on instruction-formatted data rather than RL from human feedback; contemporaneous with InstructGPT (FLAN, ICLR 2022)
- **[[direct-preference-optimization|DPO (Direct Preference Optimization)]]** — post-InstructGPT technique that eliminates the explicit reward model by directly optimising from preferences
- **[[chain-of-thought|Chain-of-Thought]]** — prompting technique that InstructGPT can follow more reliably than base GPT-3 due to improved instruction-following ability
- **[[flex-prompting|FLEX]]** — later methodology for SLM control using structured XML prompts and logit-based verification, related through shared goal of reliable model steering
- **[[grace|GRACE]]** — later framework for deterministic code generation, which uses Intent-First Architecture similar to RLHF's goal of alignment with user intent

## Limitations

### Model Limitations

- **Helping vs harmless conflict:** During training, helpfulness to the user was prioritised; the evaluation separately evaluated truthfulness and harmlessness
- **Still makes simple mistakes:** The paper identifies three failure mode categories ([Ouyang et al., 2022](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)):
  1. **False premises:** When given an instruction with a false premise, the model often assumes it is true rather than rejecting it (e.g., "Why is it important to eat socks after meditating?" produces a plausible-sounding but absurd answer)
  2. **Excessive hedging:** The model tends to give long, qualified answers to simple questions, saying "there is no clear answer" even when one exists — partly because labelers were instructed to reward epistemic humility, and the RM picks this up
  3. **Multi-constraint degradation:** Performance degrades when instructions contain multiple explicit constraints (e.g., "list 10 movies made in the 1930's set in France") or constraints that are hard for LMs (e.g., writing a summary in a specified number of sentences)
- **Sycophancy:** The model follows user instructions even when those instructions could lead to harm; when prompted to be maximally biased, InstructGPT generates *more* toxic outputs than GPT-3
- **No bias improvement:** RLHF did not significantly reduce social bias as measured by Winogender and CrowS-Pairs

### Whom the Model Is Aligned To

The paper explicitly discusses four caveats about the alignment target ([Ouyang et al., 2022](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)):

1. **Labeler demographics:** The model is aligned to ~40 contractors (Upwork/ScaleAI, mostly English-speaking, US/Southeast Asia) — not a universal "human values". Inter-labeler agreement is ~73%.
2. **Researcher bias:** The research team writes labeling instructions and answers edge-case questions, injecting their own preferences into the data collection process.
3. **Customer bias:** Training prompts come from OpenAI API Playground users, who are self-selected and not representative of all present or future users.
4. **Sampling bias:** Initial waitlist seeds were OpenAI employees, biasing the user base toward the researchers' own networks.

The paper notes that it is "impossible that one can train a system that is aligned to everyone's preferences at once" and suggests conditioning models on different preference groups as a path forward.

### Broader Impacts

Better instruction-following is a dual-use concern ([Ouyang et al., 2022](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md)): the same capability that makes models more helpful also makes them easier to misuse for generating convincing misinformation, hateful content, or abusive text. Alignment techniques are not a panacea — they should be one tool in a broader safety ecosystem including use-case restriction, monitoring, and rate-limiting in API deployments.

## Related

- [[dario-amodei|Dario Amodei]] — was VP of Research at OpenAI during the InstructGPT project
- [[anthropic|Anthropic]] — successor alignment research organisation employing Amanda Askell, co-author of this paper
- [[transformer|Transformer]] — the underlying architecture for GPT-3 and InstructGPT
- [[scaling-laws|Scaling Laws]] — contextualises the claim that scaling alone is insufficient for alignment
