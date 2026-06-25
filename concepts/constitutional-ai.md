---
title: Constitutional AI (CAI)
created: 2026-06-25
updated: 2026-06-25
type: concept
tags:
  - alignment
  - rlhf
  - technique
  - training
  - methodology
sources:
  - "[Constitutional AI: Harmlessness from AI Feedback](raw/papers/2022-12-bai-constitutional-ai/bai2022constitutional.md)"
confidence: high
---

# Constitutional AI (CAI)

A method for training harmless AI assistants using only AI feedback guided by a written set of principles (a "constitution"), introduced by [[anthropic|Anthropic]] in December 2022. CAI dramatically reduces reliance on human labels for harmlessness training, replacing the tens of thousands of human preference labels used in [[rlhf|RLHF]] with a small set (~10–15) of natural language principles.

## The CAI Method

CAI proceeds in two stages:

### Stage 1: Supervised Learning (SL-CAI)

1. A helpful-only AI assistant generates responses to harmfulness prompts. These initial responses are typically harmful/toxic.
2. The model critiquess its own response according to a randomly drawn principle from the constitution.
3. The model revises the original response based on the critique.
4. Steps 2–3 repeat with random principles drawn at each step.
5. A pretrained language model is fine-tuned via supervised learning on the final revised responses.

The main purpose of this phase is to shift the model's response distribution toward harmlessness, reducing the exploration needed during RL.

### Stage 2: RL from AI Feedback (RL-CAI / RLAIF)

1. The SL-CAI model generates pairs of responses to harmfulness prompts.
2. An AI model evaluates which response is better according to constitutional principles (this replaces human preference labels).
3. A preference model (PM) is trained from this dataset of AI preferences.
4. The SL-CAI model is fine-tuned with PPO using the PM as the reward signal — this is **RLAIF** (Reinforcement Learning from AI Feedback).

Both stages can optionally use [[chain-of-thought|chain-of-thought]] reasoning to improve performance and transparency.

## Key Results

**Pareto improvement in harmlessness vs helpfulness.** RL-CAI models achieve better harmlessness at a given level of helpfulness compared to standard RLHF models (Helpful RLHF, HH RLHF). The RL-CAI points on the helpfulness-harmlessness Elo plot lie strictly above the Pareto frontier of human-feedback-trained models.

**Non-evasive harmless assistant.** Unlike RLHF models that learn to evade harmful queries (which crowdworkers rewarded as "harmless"), CAI models engage with harmful queries by explaining their objections. This reduces the tension between helpfulness and harmlessness.

**Scale trends.** Helpfulness and harmlessness Elo scores for CAI models improve with model size (up to 52B tested), following similar scaling trends to RLHF.

**Chain-of-thought improves transparency.** RL-CAI w/ CoT enables the model to reason explicitly about constitutional principles when making judgments, making AI decision-making more legible.

## Relationship to Other Techniques

- **[[rlhf|RLHF]]** — CAI's direct predecessor. RLHF uses human preference labels for the reward model; CAI replaces human harmlessness labels entirely with AI feedback guided by constitutional principles. Both use the same three-stage architecture (SFT → PM → PPO), but CAI's PM for harmlessness is trained on AI evaluations rather than human comparisons.
- **[[direct-preference-optimization|DPO]]** — Post-CAI technique that eliminates the explicit reward model. DPO is compatible with CAI's constitutional principles (the constitution can guide preference labels for DPO training).
- **[[instruction-tuning|Instruction Tuning]]** — Related approach that also uses explicit written instructions, but for general capability rather than harmlessness.
- **[[chain-of-thought|Chain-of-Thought]]** — CAI leverages CoT during both the critique/revision stage and the AI feedback stage to improve performance.

## Limitations

- The constitution was chosen "in a fairly ad hoc and iterative way for research purposes" — the paper acknowledges principles need broader stakeholder development.
- Ethical concerns: constitution-based training encodes specific value judgments; whose principles are encoded, and who decides, is an open governance question.
- The method reduces human labels but does not eliminate the need for human oversight entirely (principles are still human-written, and helpfulness still uses human feedback).
- Later critiques (e.g., [[dario-amodei|Dario Amodei]]'s Pentagon dispute, 2026) have questioned whether constitution-based training creates a backdoor for CEO-level control of model behavior.

## Significance

Constitutional AI is the foundation of Anthropic's Claude model safety training. It demonstrated that AI systems can supervise other AI systems for harmlessness using only a short list of written principles, paving the way for scaled supervision approaches. The method has been adopted and extended by multiple organizations (NVIDIA NeMo, HuggingFace TRL, etc.) and motivated follow-up work on multi-agent constitutions and AI feedback pipelines.
