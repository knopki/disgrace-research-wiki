---
title: Instruction Tuning
created: 2026-06-18
updated: 2026-06-18
type: concept
tags:
  - technique
  - fine-tuning
  - training
sources:
  - "[Finetuned Language Models Are Zero-Shot Learners](raw/papers/2021-09-wei-flan/wei2021flan.md)"
confidence: high
---

# Instruction Tuning

Instruction tuning is a technique for improving the zero-shot learning abilities of language models by fine-tuning a pretrained model on a diverse collection of NLP tasks verbalized as natural language instructions. Introduced and systematically studied in the FLAN paper ([Wei et al., 2022](raw/papers/2021-09-wei-flan/wei2021flan.md)), it bridges the [[gpt-3|pretrain–finetune]] and [[in-context-learning|prompting]] paradigms.

The core idea: by using supervision to teach an LM to perform many tasks described via instructions, the LM learns the **meta-skill of following instructions**, which transfers to tasks it has never seen during training.

## The Method

Instruction tuning proceeds as follows:

1. **Gather existing datasets** from the research community — 62 text datasets in FLAN
2. **Group by task type** into clusters (12 clusters in FLAN: NLI, reading comprehension, translation, commonsense, etc.)
3. **Verbalize each dataset** via natural language instruction templates (10 per dataset in FLAN)
4. **Hold out entire task clusters** for evaluation — ensure truly unseen tasks
5. **Fine-tune the pretrained LM** on the mixture of all other clusters, formatted as instructions

### Key Design Choices

- **Hold-out evaluation:** To measure zero-shot generalization, entire task clusters are held out. This is more conservative than holding out individual datasets, preventing the model from having seen any example of a given task type.
- **Multiple templates per task:** 10 templates per dataset, including "turned-around" tasks (e.g., generating a movie review for a sentiment dataset), to increase diversity and prevent overfitting to any specific phrasing.
- **Options suffix:** For classification tasks, appends `OPTIONS:` with the list of output classes, making the model aware of valid choices rather than relying on rank classification.

## Results

The FLAN paper demonstrated ([Wei et al., 2022](raw/papers/2021-09-wei-flan/wei2021flan.md)):

- FLAN substantially improves zero-shot performance over the base LaMDA-PT model
- Zero-shot FLAN (137B) outperforms zero-shot GPT-3 (175B) on 20/25 datasets
- FLAN even surpasses few-shot GPT-3 on ANLI, RTE, BoolQ, ARC, OpenbookQA, and StoryCloze
- Most effective on tasks verbalized as instructions (NLI, QA, translation, struct-to-text)
- Less effective on sentence-completion-style tasks (commonsense, coreference)

## Critical Ablation: The Scaling Threshold

The most striking finding: **instruction tuning helps models ≥68B parameters but hurts models ≤8B** on unseen tasks. At small scales, the model's entire capacity is consumed learning the instruction-tuning mixture. At large scales, the model has enough capacity to learn the meta-skill of instruction-following alongside the specific tasks ([Wei et al., 2022](raw/papers/2021-09-wei-flan/wei2021flan.md)).

| Model Size | Effect of Instruction Tuning |
|:----------:|:---------------------------:|
| 422M | Negative |
| 2B | Negative |
| 8B | Negative |
| 68B | Positive |
| 137B | Strongly positive |

This finding connects directly to [[scaling-laws|scaling laws]] — the benefits of instruction tuning are gated by model scale, with a threshold somewhere between 8B and 68B parameters.

## Role of Natural Language Instructions

Ablation studies show that training with natural language instructions is crucial ([Wei et al., 2022](raw/papers/2021-09-wei-flan/wei2021flan.md)):

| Fine-tuning Format | Avg Zero-shot Score (4 clusters) |
|:------------------:|:-------------------------------:|
| No template | 37.3 |
| Dataset name | 46.6 |
| Dataset name (eval: dataset name) | 47.0 |
| **Natural instructions (FLAN)** | **55.2** |

Training with just input-output pairs or dataset names does not teach the model to follow instructions — only training on explicit natural language instructions transfers to unseen tasks.

## Relationship to Other Techniques

Instruction tuning occupies a unique position among alignment and prompting techniques:

- **[[in-context-learning|In-Context Learning]]** — both teach LMs to respond to task descriptions; ICL does so via conditioning at inference time, instruction tuning via supervised fine-tuning. They are complementary and can be combined (FLAN + few-shot exemplars improves further).
- **[[rlhf|RLHF (InstructGPT)]]** — contemporaneous technique achieving instruction-following via RL from human feedback rather than supervised fine-tuning on instruction-formatted data. RLHF requires a reward model and PPO training; instruction tuning is simpler (standard fine-tuning) but requires diverse labeled data. Both improve zero-shot generalization.
- **[[chain-of-thought|Chain-of-Thought]]** — by the same lead author (Jason Wei), CoT improves reasoning via intermediate steps at inference time, while instruction tuning improves general instruction-following via training. Applied orthogonally.
- **[[flex-prompting|FLEX]]** — later methodology focusing specifically on SLMs (which fall below the instruction-tuning scale threshold), using structured XML + logit verification instead of natural language instructions.
- **[[grace|GRACE]]** — later Intent-First Architecture for code generation; both share the principle that explicit semantic structure (instructions / blueprints) improves model output.

## Historical Impact

Instruction tuning, as introduced by FLAN, was a pivotal step in the evolution from pure prompting (GPT-3) to aligned instruction-following models (InstructGPT, ChatGPT). It demonstrated that:

1. Supervised data has a role beyond specialist models — it can train generalist models
2. The format of supervision (natural language instructions) is what enables cross-task generalization
3. Scale unlocks this capability with a sharp threshold

Subsequent work expanded instruction tuning to more tasks, larger models, and multilingual settings. Modern LLMs (GPT-4, Claude, Gemini, LLaMA-2/3, Qwen) all include some form of instruction tuning in their training pipeline.

## Related

- [[flan|FLAN]] — the model that introduced instruction tuning
- [[scaling-laws|Scaling Laws]] — instruction tuning benefits emerge only at sufficient scale
- [[gpt-3|GPT-3]] — the baseline FLAN compared against; prior state of zero-shot learning
- [[transformer|Transformer]] — the underlying architecture
- [[rlhf|RLHF]] — alternative approach to instruction-following via human feedback
- [[chain-of-thought|Chain-of-Thought Prompting]] — complementary method by same lead author
- [[flex-prompting|FLEX]] — alternative for SLMs below the instruction-tuning scale threshold
