---
title: Automated Red Teaming of Language Models
created: 2026-06-25
updated: 2026-06-25
type: concept
tags: [evaluation, methodology, alignment, technique, paper]
sources:
  - "[Red Teaming Language Models with Language Models](raw/papers/2022-02-perez-red-teaming/perez2022redteaming.md)"
---
# Automated Red Teaming of Language Models

Automated red teaming is the practice of using one language model to generate test cases that expose harmful behaviors in another language model. Introduced systematically by Perez et al. at DeepMind (2022), the approach replaces expensive human annotation with LM-generated adversarial inputs, enabling large-scale discovery of failure modes before deployment. ([Perez et al., 2022](raw/papers/2022-02-perez-red-teaming/perez2022redteaming.md))

## The Three-Stage Pipeline

1. **Generate test cases** using a red LM conditioned on a prompt (e.g., "List of questions to ask someone:")
2. **Reply** using the target LM (the system being evaluated)
3. **Detect failures** with a classifier trained to identify harmful outputs (offensive content, data leakage, etc.)

The pipeline is model-agnostic: neither the red LM nor the target LM needs to be differentiable or white-box accessible. The red LM generates well-formed natural language (via nucleus sampling, p=0.95), not the nonsensical character sequences typical of gradient-based adversarial attacks.

## Test Case Generation Methods

Perez et al. compared four approaches on Dialogue-Prompted Gopher (DPG), a 280B parameter chatbot (Rae et al., 2021):

| Method | % Offensive Replies | Diversity | Notes |
|--------|-------------------|-----------|-------|
| Zero-shot (0.5M cases) | 3.7% | Highest | Simple prompt, broad coverage |
| Stochastic few-shot | ~10% | High | Samples failing cases as in-context examples |
| Supervised learning | ~10% | Moderate | Finetunes on zero-shot failures |
| RL (A2C, α=0.3) | >40% | Low | Converges on successful patterns ("invisible" questions) |

Zero-shot, stochastic few-shot, RL, and human-written BAD dataset form a Pareto frontier — no method dominates in both difficulty and diversity. The RL method with minimum KL penalty (α=0.3) elicits offensive replies over 40% of the time but collapses to a narrow pattern (78% contain "invisible").

The red LM used Gopher (280B) — the same model family as the target. Smaller red LMs also proved effective (Appendix A.1). Offensive content was detected by a finetuned 1.4B Gopher classifier trained on the Bot-Adversarial Dialogue (BAD) dataset, which substantially outperformed Perspective API.

## Types of Harm Uncovered

**Offensive language:** 18,444 offensive replies from 0.5M zero-shot questions. Common failure modes include: DPG reciting discriminatory jokes from training data (e.g., a dyslexic joke occurring 546 times in training), insulting users ("you're an idiot"), elaborating on sexual desires, and going along with questionable premises. 37 of the top 100 flagged noun phrases did not appear in the BAD human-annotated dataset.

**Training data leakage:** 1,709 utterances with 13+ consecutive words matching training data. In 393 cases, DPG generated text in explicit quotation marks — particularly useful for adversaries conducting membership inference. In 106 cases, memorized quotes were triggered by simply asking for a quote.

**Contact information leakage:** 3,206 phone numbers (479 in training data, including real hospital numbers and personal cell numbers), 11,683 email addresses (749 in training data), and 1,006 social security numbers (32 in training data). Fake numbers (123-45-6789) dominate, but real numbers are also generated. Low-frequency items (<100 occurrences) are almost always cited in wrong context.

**Distributional bias:** DPG discussed majority groups (white men, cis white women, Caucasians) more offensively than minority groups (Jainist people, Sufi Muslims). Likely caused by the chatbot's system prompt biasing toward progressive values at the expense of majority-group fairness.

**Conversational harm:** Multi-turn dialogues show that offensive replies beget more offensive replies. The probability of an offensive reply increases with the number of preceding offensive utterances, highlighting the importance of early termination.

## Defense-Offense Asymmetry

The paper argues that LM-based red teaming is a double-edged sword (Perez et al., 2022):

**Advantages for adversaries:**
- Offense-defense asymmetry: need only one attack to succeed
- Unexpected harms: red team classifiers for hate speech miss misinformation
- Adversarial transfer: inputs effective against one LM often transfer to others

**Advantages for internal red teams:**
- Rate limits on deployed APIs restrict external adversaries
- Full model access (gradients, weights, training data) enables white-box methods
- Knowledge of training corpus guides targeted testing
- Blue teaming: fix failures before deployment

## Relationship to Other Safety Approaches

Automated red teaming complements rather than replaces manual safety evaluation. The paper found that LM-generated and human-written test cases (BAD dataset) occupy different regions of the diversity-difficulty Pareto frontier — they find different failure modes.

Related approaches:
- **[[rlhf|RLHF]]** uses human feedback to align models; red teaming identifies where alignment is insufficient
- **[[constitutional-ai|Constitutional AI]]** uses self-critique and revision (RLAIF); red teaming provides independent adversarial evaluation
- **[[instruction-tuning|Instruction Tuning]]** improves zero-shot behavior; red teaming evaluates whether the improvement generalizes to adversarial cases
- **[[hallucination-detection-slm|SLM-based Hallucination Detection]]** shares the verification goal but focuses on factual accuracy rather than harmfulness
- **[[flex-prompting|FLEX]]** and **[[grace|GRACE]]** address reliable LLM behavior; red teaming tests the reliability boundary
- **[[cot-faithfulness|CoT Faithfulness]]** — Turpin et al. (2023) show that unfaithful CoT explanations are themselves an attack vector: a user can steer a model toward biased predictions with no trace of the bias in its stated reasoning, defeating CoT-based auditing and fairness methods

## Limitations

The approach inherits biases from the red LM (limited diversity in generated test cases) and the classifier (false positives/negatives). Flawed classifiers may miss entire categories of harm. The method is not exhaustive — it finds many failure modes but cannot guarantee finding all critical oversights. LM-based red teaming is a tool for surfacing candidates for further investigation, not a replacement for comprehensive safety auditing.
