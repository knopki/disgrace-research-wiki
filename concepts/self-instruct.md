---
title: Self-Instruct
created: 2026-06-25
updated: 2026-06-25
type: concept
tags:
  - technique
  - fine-tuning
  - alignment
  - data
  - methodology
  - prompting
sources:
  - "[Self-Instruct: Aligning Language Models with Self-Generated Instructions](raw/papers/2022-12-wang-self-instruct/wang2022selfinstruct.md)"
confidence: high
---
# Self-Instruct

Self-Instruct is a framework for bootstrapping instruction-following capabilities in language models using the model's own generations as training data. Introduced by [Wang et al. (University of Washington / AI2, ACL 2023)](raw/papers/2022-12-wang-self-instruct/wang2022selfinstruct.md), it provides an almost annotation-free pipeline for generating large-scale instruction-tuning datasets, reducing dependence on human-written instruction data.

Applied to vanilla GPT-3, Self-Instruct yields a **33% absolute improvement** on SUPER-NATURALINSTRUCTIONS, nearly matching [[rlhf|InstructGPT_001]] — a model trained with private user data and human labels — while using no human annotations beyond 175 seed tasks.

## The Pipeline

The Self-Instruct pipeline (Figure 2 in the paper) consists of four iterative steps:

### 1. Instruction Generation
- Start with a seed task pool of 175 human-written instructions (25 classification, 150 non-classification), covering diverse task types.
- Sample 8 tasks from the pool (6 human-written + 2 from earlier model generations) as in-context examples.
- Prompt the pretrained LM (vanilla GPT-3 "davinci") to generate a new instruction.

### 2. Classification Task Identification
- A few-shot prompt determines whether the generated instruction describes a **classification task** (finite label space) or a **non-classification task** (open-ended generation).
- 12 classification + 19 non-classification examples from seed tasks are used as in-context exemplars.
- This distinction affects how instances are generated in the next step.

### 3. Instance Generation
Two strategies depending on task type:

- **Input-first approach (non-classification tasks):** Generate the input fields first, then condition the output on both instruction + input.
- **Output-first approach (classification tasks):** Generate class labels first, then generate inputs conditioned on each label. This prevents label imbalance — without it, the model would produce mostly "positive" or "true" examples for binary tasks.

### 4. Filtering and Postprocessing
- Remove instructions with **ROUGE-L ≥ 0.7** to any existing instruction in the pool (prevents near-duplicates).
- Exclude instructions mentioning banned keywords ("image", "picture", "graph", etc. — modalities the base LM can't handle).
- Remove instances with empty inputs where one is required, trivial outputs (too short/long), or outputs that simply repeat the input.
- Invalid or low-quality instances are discarded.

After filtering, new tasks are added back to the pool and the process repeats.

### Fine-tuning
The generated data (52k instructions, 82k instances) is used to fine-tune the original GPT-3 model:
- Training format: `{instruction} {input} {output}` with multiple formatting templates for robustness.
- Trained for 2 epochs with `prompt_loss_weight=0` — the model only learns to predict output tokens, not the instruction/input.
- Total API cost: ~$338 for fine-tuning + ~$600 for data generation.

## Key Results

### Experiment 1: Zero-shot on SUPER-NATURALINSTRUCTIONS (119 tasks)

| Model | Params | ROUGE-L |
|-------|--------|---------|
| GPT-3 (vanilla) | 175B | 6.8 |
| T0 | 11B | 33.1 |
| GPT-3 + T0 Training | 175B | 37.9 |
| **GPT-3**Self-Instruct | **175B** | **39.9** |
| InstructGPT_001 | 175B | 40.8 |
| GPT-3 + SuperNI Training | 175B | 49.5 |
| **GPT-3**Self-Instruct **+ SuperNI** | **175B** | **51.6** |

Key finding: Self-Instruct almost matches InstructGPT_001 (39.9 vs 40.8 ROUGE-L) without any human annotations or private user data. Combining with SuperNI yields the best result (51.6), suggesting the two data sources are complementary.

### Experiment 2: User-oriented Novel Tasks (252 instructions, human evaluation)

The authors curated 252 novel task instructions covering email, social media, productivity, entertainment, and programming — tasks unlikely to appear in public datasets. Human evaluators rated outputs on a 4-level scale (A = correct & satisfying, D = irrelevant).

- **GPT-3**Self-Instruct **outperforms** GPT-3 trained on T0 data or SuperNI data by a large margin on novel tasks.
- Only **5% absolute gap** behind InstructGPT_001 in acceptable (A+B) response rate.
- The gap to InstructGPT_002 and _003 is larger, but those models had additional training stages not comparable to a single fine-tuning pass.

## Data Characteristics

| Statistic | Value |
|-----------|-------|
| Total instructions | 52,445 |
| Classification instructions | 11,584 |
| Non-classification instructions | 40,861 |
| Total instances | 82,439 |
| Instances with empty input | 35,878 |
| Avg instruction length (words) | 15.9 |
| Avg non-empty input length | 12.7 |
| Avg output length | 18.9 |

**Diversity:** The top 20 verb-noun pairs account for only 14% of all instructions. Most instructions have complex clause structures or are framed as questions.

**Quality (200 expert-annotated samples):**
- 92% instructions describe a valid task
- 79% of inputs are appropriate
- 58% of outputs are correct (all fields valid: 54%)

The authors note that even partially correct examples provide useful training signal, and that imperfect data can still align the model effectively.

## Relationship to Other Techniques

- **[[instruction-tuning|Instruction Tuning]]** — Self-Instruct is a method for *generating* instruction-tuning data, not a new training objective. It solves the data bottleneck that instruction tuning faces: human-written data is scarce, expensive, and biased toward popular NLP benchmarks. Where FLAN uses 62 curated datasets from the community, Self-Instruct bootstraps from 175 seed tasks to produce 52k diverse instructions.

- **[[rlhf|RLHF (InstructGPT)]]** — Self-Instruct and RLHF attack different parts of the alignment problem. RLHF uses human preference judgments to train a reward model, then optimizes via PPO. Self-Instruct uses the LM's own generations as supervised training data. The two are complementary: Self-Instruct generates diverse instruction data cheaply, RLHF optimizes for human preferences on top of that data.

- **[[constitutional-ai|Constitutional AI]]** — Both use the LM's own generations (self-critique/revision in CAI, instruction-data generation in Self-Instruct) to reduce reliance on human annotation. CAI targets harmlessness via a written constitution; Self-Instruct targets general instruction-following via automatic data generation.

- **[[red-teaming|Automated Red Teaming]]** — Both automate an expensive human process using the LM itself. Red teaming uses one LM to generate adversarial inputs for another; Self-Instruct uses one LM to generate training data for itself.

- **[[flex-prompting|FLEX]]** — Both address data scarcity for instruction-following. FLEX targets the SLM regime where instruction tuning hurts performance; Self-Instruct assumes sufficient scale (175B GPT-3).

## Limitations

- **Quality ceiling:** Only 54% of generated instances are fully valid. While partially correct data still helps, the noise floor limits the maximum achievable performance compared to human-curated datasets.
- **Bias propagation:** The model can only generate instructions within its existing knowledge and capabilities. If the base model lacks competence in a domain, Self-Instruct cannot bootstrap past that gap.
- **Classification task imbalance:** The output-first approach mitigates label imbalance but doesn't eliminate it entirely.
- **Single-model experiment:** Results are demonstrated on GPT-3 (davinci). Generality to other architectures (T5, LLaMA, encoder-decoder models) was not tested in the original paper.
- **No safety alignment:** Self-Instruct improves instruction-following without any guarantees about safety, truthfulness, or toxicity — unlike InstructGPT which included harmlessness training.

## Impact

Self-Instruct became a foundational technique for automatic instruction data generation. Subsequent work built on its core insight — using LMs to generate their own training data — notably:

- **Stanford Alpaca** (2023) replicated Self-Instruct's approach with text-davinci-003 as the teacher model and LLaMA-7B as the student, generating 52k instructions at a cost of ~$500.
- Self-Instruct-style pipelines became standard in post-2023 LLM training, where model-generated data supplements or replaces human annotation for instruction tuning, preference data, and other alignment stages.

The core idea — *bootstrap instruction-following from the model's own generations* — demonstrated that a significant portion of alignment data can be automated, reducing both cost and the bottleneck of human annotation.

## Related

- [[instruction-tuning|Instruction Tuning]] — the broader paradigm Self-Instruct generates data for
- [[rlhf|RLHF (InstructGPT)]] — alternative alignment approach using human preference feedback
- [[constitutional-ai|Constitutional AI]] — contemporaneous self-supervised alignment method
- [[flan|FLAN]] — instruction-tuned model using human-curated datasets
- [[entities/gpt-3|GPT-3]] — the base model Self-Instruct was demonstrated on
