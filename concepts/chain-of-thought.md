---
title: Chain-of-Thought Prompting (CoT)
created: 2026-06-15
updated: 2026-06-21
type: concept
tags:
  - technique
  - prompting
sources:
  - "[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](raw/papers/2022-01-wei-chain-of-thought/wei2022cot.md)"
  - "[CoT Harms Performance of Rather Smaller Language Models](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.md)"
  - "[GPT-4.1 Prompting Guide](raw/articles/2025-04-14-openai-gpt41-prompting-guide.md)"
  - "[Оптимизация управления ИИ агентами на SLM через методологию Few-shot Logit-Enabled XML (FLEX)](raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/ivanov2025flex.md)"
  - "[Training Large Language Models to Reason in a Continuous Latent Space](raw/papers/2024-12-hao-coconut/hao2025coconut.md)"
---

# Chain-of-Thought Prompting (CoT)

Chain-of-Thought (CoT) prompting instructs a language model to articulate intermediate reasoning steps before producing a final answer. Introduced by Wei et al. (Google Research, NeurIPS 2022), it became a standard component of LLM prompting across reasoning tasks.

## Original Paper

The paper "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" ([Wei et al., 2022](raw/papers/2022-01-wei-chain-of-thought/wei2022cot.md)) demonstrated that providing a few exemplars with intermediate reasoning steps — a chain of thought — dramatically improves performance on arithmetic, commonsense, and symbolic reasoning. The key finding: **CoT is an emergent ability of model scale.** Below ~100B parameters, CoT actually degrades performance; at scale (100B+), it unlocks reasoning that standard prompting cannot elicit.

### Experimental Design

The paper evaluated five models (GPT-3, LaMDA, PaLM, UL2 20B, Codex) across three reasoning domains:

- **Arithmetic:** GSM8K, SVAMP, ASDiv, AQuA, MAWPS — eight manually composed CoT exemplars used across all benchmarks
- **Commonsense:** CSQA, StrategyQA, Date Understanding, Sports Understanding, SayCan
- **Symbolic:** Last letter concatenation, coin flip — with out-of-domain (OOD) length generalization tests

### Key Results

**Arithmetic reasoning** showed the most striking gains ([Wei et al., 2022](raw/papers/2022-01-wei-chain-of-thought/wei2022cot.md)):

- GSM8K: PaLM 540B achieved 58% solve rate with CoT vs 18% standard, surpassing finetuned GPT-3 with verifier
- SVAMP: 79% CoT vs 70% standard
- MAWPS: 88% CoT vs 84% standard
- Gains concentrated on the hardest problems — single-step problems showed minimal improvement

**Commonsense reasoning:** CoT improved performance across all five benchmarks, with PaLM 540B achieving new SOTA on StrategyQA (75.6% vs prior 69.4%) and Sports Understanding (95.4%).

**Symbolic reasoning and OOD generalization:** CoT allowed models to generalize to longer sequences than seen in exemplars — standard prompting failed entirely on OOD cases, while CoT produced upward scaling curves with model size.

### Ablation Studies

Three ablations isolated why CoT works ([Wei et al., 2022](raw/papers/2022-01-wei-chain-of-thought/wei2022cot.md)):

| Variant | Effect on GSM8K |
|---------|:--------------:|
| **Standard prompting** | ~18% (baseline) |
| **Equation only** | No improvement — natural language reasoning is essential, not just equations |
| **Variable compute only** (dot sequence) | No improvement — extra tokens alone aren't the mechanism |
| **Reasoning after answer** | No improvement — the generated chain must precede the answer |
| **Chain-of-thought** | ~58% |

The sequential reasoning embodied in the chain of thought is what matters — not the extra tokens, not the equations produced, and not knowledge activation after the answer.

### Robustness

CoT prompting is robust across ([Wei et al., 2022](raw/papers/2022-01-wei-chain-of-thought/wei2022cot.md)):

- **Different annotators:** Three independent authors wrote CoT exemplars — all outperformed standard prompting
- **Different exemplars:** Random samples from GSM8K training set performed comparably to hand-written ones
- **Concise vs verbose:** Deliberately concise chains of thought also worked well
- **Exemplar order and count:** Varying permutation and number of exemplars showed stable results

### Error Analysis

Manual analysis of model-generated chains of thought for LaMDA 137B on GSM8K ([Wei et al., 2022](raw/papers/2022-01-wei-chain-of-thought/wei2022cot.md)):

- **Correct answers:** 48/50 generated chains were logically and mathematically correct
- **Incorrect answers:** 46% had minor errors (calculator mistake, symbol mapping, single missing step); 54% had major semantic understanding failures
- **Scale helps:** Scaling PaLM from 62B to 540B fixed most one-step-missing and semantic understanding errors

## Effect by Model Size

CoT benefit scales with model size. The original paper established that CoT is an **emergent property** — small models produce fluent but illogical chains of thought, leading to lower performance than standard prompting. Shim et al. (2024) later confirmed and quantified this threshold on GPT-2 and GPT-Neo ([Shim et al., 2024](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.md)):

| Model | Standard → CoT | Relative Δ |
|-------|---------------|------------|
| GPT-2 117M | 3.5 → 3.5 | 0% |
| GPT-2 345M | 12.5 → 6.8 | −45.6% |
| GPT-2 774M | 20.8 → 13.7 | −34.1% |
| GPT-2 1558M | 38.0 → 20.1 | −47.1% |
| GPT-Neo 125M | 1.7 → 0 | −100% |
| GPT-Neo 1.3B | 14.5 → 8.8 | −39.3% |
| GPT-Neo 2.7B | 20.0 → 13.7 | −31.5% |

The loss is multiplicative (proportional to baseline accuracy), with a convergence effect — CoT scores cluster tighter than standard scores, suggesting a CoT-induced performance ceiling. GPT-Neo shows slightly more resilience than GPT-2 at similar sizes.

## Criticism: CoT as Post-Hoc Rationalization

Ivanov (2025) argues that CoT for SLMs is not genuine reasoning but **post-hoc rationalization** — the model arrives at a decision in its hidden state, then generates CoT as a plausible-sounding justification. His argument rests on two points ([Ivanov, 2025](raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/ivanov2025flex.md)):

1. **Hidden state precedes explanation:** The model's logit distribution at the final layer determines the output before any CoT tokens are generated. SLMs lack the capacity for multi-step internal deliberation that CoT simulates superficially.

2. **No direct verification:** Traditional prompt evaluation judges correctness, not process. Two models producing the same correct answer may have arrived via entirely different mechanisms. Only logit analysis reveals the difference.

This critique aligns with the [[flex-prompting|FLEX methodology]]: replace CoT with structured XML prompts + few-shot examples + logit-based verification as an empirically verifiable control method for SLMs.

Notably, the original CoT paper already acknowledged this limitation: "although chain of thought emulates the thought processes of human reasoners, this does not answer whether the neural network is actually 'reasoning,' which we leave as an open question" ([Wei et al., 2022](raw/papers/2022-01-wei-chain-of-thought/wei2022cot.md)).

## Relationship to Continuous Reasoning

[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] replaces language-space CoT with reasoning directly in the continuous latent space. Coconut outperforms standard CoT on logical reasoning tasks while using far fewer tokens, and excels specifically on tasks requiring planning and search (ProsQA: 97.0% vs 77.5%) — precisely where CoT's greedy chain commits to dead-end paths ([Hao et al., 2024](raw/papers/2024-12-hao-coconut/hao2025coconut.md)). The finding that CoT harms SLMs suggests Coconut's latent approach may be particularly valuable for smaller models.

## Usage in Practice

The GPT-4.1 Prompting Guide recommends ([OpenAI, 2026](raw/articles/2025-04-14-openai-gpt41-prompting-guide.md)):
- Start with basic CoT: `"Let's think step by step"`
- Iteratively improve by auditing failures and codifying successful strategies
- Structured CoT with explicit sub-goals and verification steps

## Open Questions (from the original paper)

1. How much more can reasoning ability improve with further model scale?
2. What other prompting methods might expand the range of tasks language models can solve?
3. Does the neural network engaged in chain-of-thought actually "reason" or emulate reasoning?
4. Can reasoning be induced in smaller models to reduce serving cost?

## Related

- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — latent-space alternative that excels where CoT fails
- [[instruction-tuning|Instruction Tuning]] — related technique by the same lead author (Jason Wei); CoT improves reasoning at inference time, instruction tuning improves general instruction-following via training
- [[in-context-learning|In-Context Learning]] — CoT extends ICL by providing reasoning steps as intermediate context
- [[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]] — CoT harming SLMs is evidence in this debate
- [[flex-prompting|FLEX (Few-shot Logit-Enabled XML Prompting)]] — alternative for SLMs that replaces CoT with XML structure + logit verification
- [[scaling-laws|Scaling Laws]] — CoT is an emergent ability of model scale, confirming the scaling-law framework
- [[entities/gpt-3|GPT-3]] — CoT builds on GPT-3's few-shot prompting paradigm
- [[flan|FLAN]] — instruction-tuned model by same lead author; complementary approach to CoT
