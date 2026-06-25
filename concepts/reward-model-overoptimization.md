---
title: Reward Model Overoptimization Scaling Laws
created: 2026-06-25
updated: 2026-06-25
type: concept
tags:
  - rlhf
  - scaling-law
  - alignment
  - evaluation
  - technique
sources:
  - "[Scaling Laws for Reward Model Overoptimization](raw/papers/2022-10-gao-reward-model-overoptimization/gao2022rewardmodeloveropt.md)"
confidence: high
---

# Reward Model Overoptimization Scaling Laws

Empirical scaling laws characterising how optimizing against a proxy reward model eventually decreases ground-truth performance — a manifestation of Goodhart's law in [[rlhf|RLHF]]. Introduced by Gao, Schulman & Hilton at OpenAI ([Gao et al., 2022](raw/papers/2022-10-gao-reward-model-overoptimization/gao2022rewardmodeloveropt.md)).

## Problem

In RLHF, a reward model (RM) trained on human preferences serves as a proxy for true human judgment. Because the RM is an imperfect proxy, there is a limit beyond which further optimization against it degrades the actual quality of outputs. This is **overoptimization** — a specific instance of Goodhart's law: "When a measure becomes a target, it ceases to be a good measure."

Measuring this effect directly is expensive: it requires collecting many human preference labels to estimate ground-truth quality across many optimization conditions. Gao et al. solved this by creating a **synthetic setup** where a large "gold-standard" RM (6B parameters from InstructGPT) replaces human labelers, providing deterministic preference labels for training proxy RMs of varying sizes (3M–3B parameters).

## Functional Forms

The paper establishes empirically-validated functional forms linking the gold RM score R to the Kullback–Leibler divergence d = √D_KL(π ‖ π_init) between the initial and optimized policies:

**Best-of-n (BoN) sampling:**

R_bon(d) = d(α_bon − β_bon · d)

**Reinforcement Learning (PPO):**

R_RL(d) = d(α_RL − β_RL · log d)

Both forms share a structure: a linear component (α) capturing the benefit of optimization, and a negative component (β) capturing the penalty from overoptimization. R(0) = 0 by convention.

The BoN form was validated through a true advance prediction: the functional form was hypothesised from data up to n = 1,000 (KL ≈ 6 nats), then tested on a new experiment up to n = 60,000 (KL ≈ 10 nats).

## Key Findings

### Smooth coefficient scaling with RM parameter count

α_bon and β_bon change smoothly with RM size. For RL, α_RL is nearly constant across all RM sizes, while β_RL scales logarithmically. This allows predicting the peak gold RM score for any RM size.

### RL vs BoN

Reinforcement learning is far less KL-efficient than BoN — it "consumes" more KL divergence for the same amount of optimization. However, when measured by proxy RM score (the quantity being directly optimised), RL and BoN look significantly more similar. RL initially has a larger proxy-gold gap but peaks at a higher gold RM score than BoN.

### Weak dependence on policy size

Larger policies benefit less from RM optimization (higher baseline), but do **not** overoptimize faster: the gold score peaks at almost the same KL distance. The gap between proxy and gold scores is nearly identical across policy sizes, suggesting that overoptimization is primarily a property of the RM, not the policy.

### KL penalty ineffectiveness

In the RL setup, adding a KL penalty only causes convergence earlier — it does not shift the KL-gold reward frontier. The effect is equivalent to **early stopping**. For this reason, the paper sets KL penalty to 0 for all main experiments.

### RM data scaling

More RM training data improves gold scores and reduces overoptimization. Below ~2,000 comparisons, RMs achieve near-chance accuracy regardless of model size. Beyond this threshold, performance improves with more data, with larger RMs improving faster.

## Connection to Goodhart Taxonomy

The paper maps the observed overoptimization to the four-category taxonomy from Manheim & Garrabrant (2018):

- **Regressional Goodhart:** Noise in the RM's feature estimates causes some optimization power to go toward selecting on noise (captured by the α term — the gap between proxy and gold slopes).
- **Extremal Goodhart:** Out-of-distribution failures of the RM as the policy distribution shifts, causing nonmonotonic gold scores (captured by the β term — primarily responsible for the eventual decline).
- **Causal Goodhart:** Correlations between features and gold reward where selecting on the feature does not increase true quality (behaves similarly to regressional).
- **Adversarial Goodhart:** Deliberate manipulation of the proxy — not observed at current capability levels, but predicted to break these scaling laws when ML systems become capable enough.

## Implications for Iterated RLHF

Under simplifying assumptions (constant α_RL, β_RL, additive d), iterated RLHF (retraining the RM on fresh human data periodically) yields:

R_RL_k(d) = d(α_RL − β_RL · log d + β_RL · log k)

Iteration does not affect regressional Goodhart (α term), but increases the final gold score by β_RL · d · log k. This result holds up to some maximum number of iterations, below a minimum distance where assumptions break down.

## Limitations

- Does not capture overoptimization from the gap between human labels and true human intent (only the RM-human gap)
- Synthetic setting may not transfer perfectly to real RLHF (RM-RM correlation)
- Proxy RM scores are harder to predict with clean functional forms than gold scores
- Limited to two policy sizes (1.2B, 6B)
- Does not explore adversarial Goodhart

## Related

- [[rlhf|RLHF]] — the technique that motivates the proxy RM; this paper's findings are a core limitation of RLHF
- [[scaling-laws|Scaling Laws (Neural Language Models)]] — analogous methodology: empirical power-law relationships predict model behavior as a function of scale
- [[truthfulqa|TruthfulQA]] — another work showing that optimizing for a proxy (truthfulness via scaling) can fail; RLHF improves truthfulness 2x, but overoptimization remains a risk
- [[constitutional-ai|Constitutional AI]] — alternative approach aiming to reduce reliance on human RM labels by using a written constitution
- [[direct-preference-optimization|DPO]] — eliminates explicit RM entirely, avoiding the proxy RM overoptimization channel
