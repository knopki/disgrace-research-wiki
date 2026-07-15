---
title: Direct Preference Optimization (DPO)
created: 2026-06-16
updated: 2026-07-15
type: concept
tags:
  - rlhf
  - alignment
  - training
  - technique
sources:
  - "[Direct Preference Optimization: Your Language Model is Secretly a Reward Model](raw/papers/2023-05-rafailov-dpo/rafailov2023dpo.md)"
confidence: high
---

# Direct Preference Optimization (DPO)

A training algorithm that aligns language models with human preferences using a simple binary cross-entropy loss, eliminating the separate reward model and reinforcement learning loop required by [[rlhf|RLHF]]. Introduced by Rafailov et al. (Stanford, NeurIPS 2023).

## The Key Insight

Standard RLHF optimises a KL-constrained reward maximisation objective:

```
max E[r(x,y)] - β · D_KL(π_θ || π_ref)
```

DPO's key theoretical contribution is a closed-form mapping between reward functions and optimal policies. For any reward function r(x,y), the optimal policy under the KL constraint is:

```
π_r(y|x) = 1/Z(x) · π_ref(y|x) · exp(r(x,y)/β)
```

Rearranging this gives the reward function in terms of the policy:

```
r(x,y) = β · log(π_r(y|x) / π_ref(y|x)) + β · log Z(x)
```

Substituting this into the Bradley-Terry preference model causes the partition function Z(x) to cancel, yielding a preference probability expressed purely in terms of the policy:

```
p*(y1 ≻ y2 | x) = σ(β · log(π*(y1|x)/π_ref(y1|x)) - β · log(π*(y2|x)/π_ref(y2|x)))
```

This leads to the DPO loss:

```
L_DPO = -E[log σ(β · log(π_θ(y_w|x)/π_ref(y_w|x)) - β · log(π_θ(y_l|x)/π_ref(y_l|x)))]
```

Where y_w is the preferred completion and y_l the dispreferred completion. The gradient increases the likelihood of y_w and decreases the likelihood of y_l, weighted by how incorrectly the implicit reward model orders the pair.

## Theoretical Foundation

**Theorem 1** (Rafailov et al., 2023): Under mild assumptions, all reward equivalence classes consistent with the Bradley-Terry (and more generally Plackett-Luce) preference models can be represented with the reparameterization r(x,y) = β · log(π(y|x)/π_ref(y|x)) for some model π(y|x) and a given reference model π_ref(y|x).

This theorem proves that DPO does not constrain the class of representable reward models — it merely selects the unique canonical representative within each equivalence class that makes the partition function equal to 1. The language model itself becomes the reward model ("Your Language Model is Secretly a Reward Model").

## Comparison with RLHF

| Property | RLHF (PPO-based) | DPO |
|----------|-----------------|-----|
| Reward model | Explicit, separate LM with linear head | Implicit — the policy itself is the reward model |
| RL training loop | PPO with value function, advantage estimation, clipping | None — single-stage classification loss |
| Sampling during training | Required (policy rollouts) | Not required (offline preference dataset only) |
| Hyperparameter sensitivity | High (target KL, clipping, value function LR, etc.) | Low (single β parameter) |
| Models tested up to | 175B (InstructGPT) | 6B (GPT-J-6B) |

The DPO objective is equivalent to optimising the same KL-constrained reward maximisation objective as PPO-based RLHF, but achieves a strictly better reward/KL frontier in controlled experiments (Rafailov et al., 2023).

## Key Results

**Sentiment Control (IMDb):** DPO achieves the highest expected reward for all KL values, strictly dominating PPO including PPO with access to ground-truth rewards (PPO-GT).

**Summarization (TL;DR, Reddit):** DPO achieves ~61% win rate vs reference summaries at temperature 0.0, exceeding PPO's ~57%. DPO is substantially more robust to sampling temperature — PPO degrades to baseline GPT-J performance at high temperatures while DPO maintains quality.

**Single-turn Dialogue (Anthropic-HH):** DPO is the only computationally efficient method that improves over the preferred completions in the dataset, matching the performance of the Best-of-128 baseline (which requires 128x more sampling at test time).

**Out-of-Distribution Generalization (CNN/DailyMail):** DPO policies fine-tuned on Reddit TL;DR generalise to news articles better than PPO — 36% vs 26% win rate at temperature 0, 31% vs 23% at temperature 0.25.

**Human Validation:** GPT-4 judgments of summary quality correlate with human judgments approximately as well as humans agree with each other (67-79% GPT-4↔Human agreement vs 65-87% Human↔Human agreement).

## Implementation

The DPO loss is straightforward to implement:

```python
import torch.nn.functional as F

def dpo_loss(pi_logps, ref_logps, yw_idxs, yl_idxs, beta):
    pi_yw_logps, pi_yl_logps = pi_logps[yw_idxs], pi_logps[yl_idxs]
    ref_yw_logps, ref_yl_logps = ref_logps[yw_idxs], ref_logps[yl_idxs]
    pi_logratios = pi_yw_logps - pi_yl_logps
    ref_logratios = ref_yw_logps - ref_yl_logps
    losses = -F.logsigmoid(beta * (pi_logratios - ref_logratios))
    rewards = beta * (pi_logps - ref_logps).detach()
    return losses, rewards
```

Default hyperparameters: β = 0.1 (0.5 for summarization), batch size 64, RMSprop optimizer, learning rate 1e-6, linear warmup over 150 steps.

## Mechanistic notes

### The β-importance weight is load-bearing
The DPO gradient weights each example by how incorrectly the implicit reward model orders the pair — σ of the reversed margin, scaled by β (Rafailov et al., 2023, §4). A naïve contrastive objective that merely maximizes log p(y_w) and minimizes log p(y_l) — i.e. unlikelihood training — collapses: without the reference-conditioned ratio and its β weight, the model degenerates into repetitive loops (e.g. "when when when…", Appendix Table 3 on TL;DR prompts). The dynamic per-example weight is precisely what prevents this mode collapse while still separating preferred from dispreferred completions.

### Reference-policy initialization fallback
DPO requires a fixed reference π_ref. When a separate SFT model is available it sets π_ref = π_SFT; when not (e.g. Anthropic-HH dialogue, where only preferred completions exist), it initializes π_ref by maximum-likelihood over the preferred completions — π_ref = argmax_π E[log π(y_w|x)] — to mitigate distribution shift between the unavailable true reference and the one DPO actually uses (§4).

### Beyond pairwise: Plackett-Luce
Theorem 1 is proved for the full Plackett-Luce ranking family, not just Bradley-Terry pairwise comparisons. The same reparameterization (Eq. 9) recovers the canonical reward representative for k-way ranked preferences, so the DPO formulation extends naturally to ranked (not only paired) data (§5.1, Appendix A.3).

## Limitations

- **Scaling:** Only tested up to 6B parameters (GPT-J-6B). Scaling to state-of-the-art models orders of magnitude larger is an open question.
- **OOD exploration:** Initial results suggest DPO generalises similarly to PPO, but more comprehensive study is needed, particularly for self-labeling and unlabeled prompt utilisation.
- **Reward over-optimisation:** The paper notes a slight decrease in DPO performance over extended training (Figure 3-right) which may be an instance of reward over-optimisation, but this is not well-characterised in the direct preference setting.
- **Factual accuracy:** DPO can produce verbose but factually incorrect responses (see Table 9-10 in the paper), suggesting the implicit reward model does not fully capture correctness.

## Impact

DPO has become the dominant alignment method in open-source and production LLM post-training, largely replacing PPO-based RLHF for preference optimisation due to its simplicity, stability, and lower computational cost. The idea of implicit reward modelling has been extended to iterative/online variants (Iterative DPO, IPO, KTO) and combined with other techniques like [[rotary-position-embedding|RoPE]]-based architectures.

## Related

- [[rlhf|RLHF]] — the framework DPO simplifies
- InstructGPT — the paper that demonstrated RLHF at scale (see [[rlhf|RLHF]])
- [[transformer|Transformer]] — the underlying architecture
- [[flash-attention|FlashAttention]] — another optimisation technique simplifying a complex pipeline
- [[flex-prompting|FLEX]] — related in methodological philosophy of replacing complex pipelines with simple objectives
