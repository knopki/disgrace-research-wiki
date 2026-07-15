---
title: Chain-of-Thought Prompting (CoT)
created: 2026-06-15
updated: 2026-06-25
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
  - "[Large Language Models are Zero-Shot Reasoners](raw/papers/2022-05-kojima-zero-shot-cot/kojima2022zeroshot.md)"
  - "[Self-Consistency Improves Chain of Thought Reasoning in Language Models](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)"
  - "[Measuring Faithfulness in Chain-of-Thought Reasoning](raw/papers/2023-07-lanham-faithful-cot/lanham2023faithfulcot.md)"
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

## Zero-shot-CoT

A companion paper by Kojima et al. (The University of Tokyo / Google Research, NeurIPS 2022) introduced **Zero-shot-CoT** — eliciting chain of thought reasoning without any few-shot examples, using a single task-agnostic prompt ([Kojima et al., 2022](raw/papers/2022-05-kojima-zero-shot-cot/kojima2022zeroshot.md)).

### Method

Zero-shot-CoT uses a two-stage prompting pipeline:

1. **Reasoning extraction** — append `"Let's think step by step"` to the question, generating a free-form reasoning chain
2. **Answer extraction** — concatenate the original question, the generated reasoning, and a format-specific answer trigger (e.g. `"Therefore, the answer (arabic numerals) is"` for arithmetic) to extract a final answer

This contrasts with Few-shot-CoT (Wei et al.) which provides hand-crafted step-by-step exemplars. Zero-shot-CoT trades per-task prompt engineering for a second LLM call.

### Key Results

Zero-shot-CoT evaluated on 12 datasets across arithmetic, commonsense, symbolic, and logical reasoning with 17 model variants (GPT-3, InstructGPT, PaLM) ranging from 0.3B to 540B parameters ([Kojima et al., 2022](raw/papers/2022-05-kojima-zero-shot-cot/kojima2022zeroshot.md)):

| Task | Zero-shot | Zero-shot-CoT | Gain |
|------|:--------:|:------------:|:----:|
| MultiArith | 17.7% | **78.7%** | +61.0 |
| GSM8K | 10.4% | **40.7%** | +30.3 |
| AQUA-RAT | 22.4% | **33.5%** | +11.1 |
| SVAMP | 58.8% | 62.1% | +3.3 |
| Last Letter (4 words) | 0.2% | **57.6%** | +57.4 |
| Coin Flip (4 times) | 12.8% | **91.4%** | +78.6 |
| Date Understanding | 49.3% | **67.5%** | +18.2 |
| Tracking Shuffled Objects | 31.3% | **52.4%** | +21.1 |

Zero-shot-CoT underperforms Few-shot-CoT (e.g., GSM8K 40.7% vs 48.7%) but requires no task-specific exemplars. With self-consistency, PaLM-540B zero-shot-CoT reaches 69.2% on GSM8K (up from 43.0% zero-shot-CoT alone, +26.2%; Wang et al., 2022, Table 8).

### Scaling and Emergence

Like Few-shot-CoT, Zero-shot-CoT is an **emergent ability of model scale** ([Kojima et al., 2022](raw/papers/2022-05-kojima-zero-shot-cot/kojima2022zeroshot.md)). Small models show flat or negative curves; the benefit emerges at 100B+ parameters. This confirms the same scaling pattern across both few-shot and zero-shot CoT variants.

### Template Robustness

The paper systematically evaluated 16 prompt templates across three categories ([Kojima et al., 2022](raw/papers/2022-05-kojima-zero-shot-cot/kojima2022zeroshot.md)):

- **Instructive** (encourage reasoning): `"Let's think step by step"` achieved best (78.7%), followed by `"First,"` (77.3%), `"Let's think about this logically"` (74.5%)
- **Misleading** (discourage or misdirect): all ≤18.8% (near zero-shot baseline)
- **Irrelevant** (no reasoning relation): all ≤17.5% (near zero-shot baseline)

Only instructive templates improved performance. The choice of trigger significantly impacts accuracy even within the instructive category.

### Impact

Zero-shot-CoT established that LLMs' reasoning ability is not contingent on task-specific exemplars — the capacity for structured step-by-step reasoning exists as a zero-shot capability that can be elicited by a single generic prompt. The paper served as the strongest zero-shot baseline for reasoning benchmarks and highlighted the value of probing zero-shot abilities before investing in few-shot crafting or fine-tuning.

## Self-Consistency

A natural extension to chain-of-thought prompting is **[[self-consistency|Self-Consistency]]** — replacing greedy decoding with a sample-and-marginalise strategy ([Wang et al., ICLR 2023](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)). Instead of decoding a single reasoning path greedily, the model samples K diverse reasoning paths (typically 40) using temperature/top-k sampling, then selects the most consistent answer by majority vote.

### Key Results

Self-consistency yields striking gains on top of CoT prompting ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)). GSM8K is PaLM-540B; SVAMP, AQuA, StrategyQA, and ARC-challenge are GPT-3 code-davinci-002 (values match the paper's Table 2/3):

| Task | Model | CoT greedy | +Self-consistency | Δ |
|------|:-----:|:---------:|:-----------------:|:-:|
| GSM8K | PaLM-540B | 56.5 | 74.4 | **+17.9** |
| SVAMP | GPT-3 cd-002 | 75.8 | 86.8 | **+11.0** |
| AQuA | GPT-3 cd-002 | 39.8 | 52.0 | **+12.2** |
| StrategyQA | GPT-3 cd-002 | 73.4 | 79.8 | **+6.4** |
| ARC-challenge | GPT-3 cd-002 | 83.6 | 87.5 | **+3.9** |

The gain increases with model scale (+3–6% for UL2-20B, +9–23% for GPT-3/LaMDA-137B). Self-consistency works robustly across sampling strategies, with imperfect prompts, and with zero-shot CoT (PaLM-540B zero-shot-CoT + self-consistency reaches 69.2% on GSM8K, +26.2% over zero-shot-CoT alone; Wang et al., 2022, Table 8). It significantly outperforms beam search, sample-and-rank, and prompt-order ensemble methods, while requiring no training or human annotation ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

### Properties

- **Unsupervised** — no training, fine-tuning, or human annotation; off-the-shelf with any pre-trained model
- **Fixed-answer tasks only** — requires a parseable answer set (numbers, multiple choice, yes/no)
- **Cost-performance tradeoff** — 5–10 paths capture most gains; 40 paths near-maximal
- **Calibration signal** — consistency score (% of decodes agreeing with the final answer) correlates strongly with accuracy, providing built-in uncertainty estimation

With self-consistency, PaLM-540B zero-shot-CoT reaches 69.2% on GSM8K (+26.2% over zero-shot-CoT alone; Wang et al., 2022, Table 8).

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

Empirically, [[cot-faithfulness|Turpin et al. (2023)]] show CoT explanations are *systematically* unfaithful even for frontier instruction-tuned models (GPT-3.5, Claude 1.0): reordering few-shot options so "(A)" is always correct, or injecting a sycophantic hint, shifts predictions by up to 36% while the generated CoT rationalizes the biased answer without ever mentioning the bias ([Turpin et al., 2023](raw/papers/2023-05-turpin-cot-unfaithfulness/turpin2023cotunfaithful.md)). This is unfaithfulness in the technical sense — the explanation misrepresents the true decision process — distinct from Ivanov's capability-level critique that SLMs lack the latent capacity for genuine multi-step reasoning.

Notably, the original CoT paper already acknowledged this limitation: "although chain of thought emulates the thought processes of human reasoners, this does not answer whether the neural network is actually 'reasoning,' which we leave as an open question" ([Wei et al., 2022](raw/papers/2022-01-wei-chain-of-thought/wei2022cot.md)).

## Faithfulness: is the CoT the real reason?

A rigorous audit by Lanham et al. (Anthropic, 2023) asks whether CoT is a *faithful* explanation of the model's reasoning — i.e. whether the stated steps actually cause the answer, or are post-hoc justification generated after the answer is already fixed in the hidden state ([Lanham et al., 2023](raw/papers/2023-07-lanham-faithful-cot/lanham2023faithfulcot.md)). Four intervention tests (early answering, adding mistakes, filler tokens, paraphrasing) show:

- **Large task variation.** On AQuA the CoT changes the final answer >60% of the time; on ARC-Easy <10%. Post-hoc extent does *not* track CoT's accuracy gain.
- **Test-time compute is not the mechanism.** Replacing the CoT with length-matched "..." gives no accuracy boost — ruling out "extra tokens" as the cause.
- **Phrasing carries no hidden signal.** Paraphrased CoT matches original accuracy, so the boost isn't steganographically encoded in wording.
- **Inverse scaling.** Faithfulness gets monotonically worse from 13B → 175B; on 6/8 tasks the 13B model is the *most* faithful. Larger models more often settle the answer before generating any CoT.

The paper's practical recommendation: for high-stakes settings where faithful explanations matter, prefer a *smaller* model than the strongest available. For the full breakdown see [[cot-faithfulness|CoT Faithfulness]].

## Relationship to Continuous Reasoning

[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] replaces language-space CoT with reasoning directly in the continuous latent space. Coconut outperforms standard CoT on logical reasoning tasks while using far fewer tokens, and excels specifically on tasks requiring planning and search (ProsQA: 97.0% vs 77.5%) — precisely where CoT's greedy chain commits to dead-end paths ([Hao et al., 2024](raw/papers/2024-12-hao-coconut/hao2025coconut.md)). The finding that CoT harms SLMs suggests Coconut's latent approach may be particularly valuable for smaller models.

## Usage in Practice

The GPT-4.1 Prompting Guide recommends ([OpenAI, 2026](raw/articles/2025-04-14-openai-gpt41-prompting-guide.md); originating from [Kojima et al., 2022](raw/papers/2022-05-kojima-zero-shot-cot/kojima2022zeroshot.md)):
- Start with basic CoT: `"Let's think step by step"`
- Iteratively improve by auditing failures and codifying successful strategies
- Structured CoT with explicit sub-goals and verification steps

## Open Questions (from the original paper)

1. How much more can reasoning ability improve with further model scale?
2. What other prompting methods might expand the range of tasks language models can solve?
3. Does the neural network engaged in chain-of-thought actually "reason" or emulate reasoning?
4. Can reasoning be induced in smaller models to reduce serving cost?

## Related

- [[self-consistency|Self-Consistency]] — decoding strategy replacing greedy decoding with sample-and-marginalise for CoT; yields large gains on arithmetic and commonsense reasoning
- [[tot|Tree of Thoughts (ToT)]] — generalizes CoT from a single chain to a search tree with LM self-evaluation; the explicit "System 2" extension beyond self-consistency
- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — latent-space alternative that excels where CoT fails
- [[instruction-tuning|Instruction Tuning]] — related technique by the same lead author (Jason Wei); CoT improves reasoning at inference time, instruction tuning improves general instruction-following via training
- [[in-context-learning|In-Context Learning]] — CoT extends ICL by providing reasoning steps as intermediate context
- [[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]] — CoT harming SLMs is evidence in this debate
- [[flex-prompting|FLEX (Few-shot Logit-Enabled XML Prompting)]] — alternative for SLMs that replaces CoT with XML structure + logit verification
- [[scaling-laws|Scaling Laws]] — CoT is an emergent ability of model scale, confirming the scaling-law framework
- [[cot-faithfulness|CoT Faithfulness]] — empirical audit showing CoT is often post-hoc, with inverse scaling by model size
- [[entities/gpt-3|GPT-3]] — CoT builds on GPT-3's few-shot prompting paradigm
- [[flan|FLAN]] — instruction-tuned model by same lead author; complementary approach to CoT
