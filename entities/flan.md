---
title: FLAN (Finetuned Language Net)
created: 2026-06-18
updated: 2026-06-18
type: entity
tags:
  - model
  - technique
sources:
  - "[Finetuned Language Models Are Zero-Shot Learners](raw/papers/2021-09-wei-flan/wei2021flan.md)"
confidence: high
---
# FLAN (Finetuned Language Net)

FLAN (Finetuned Language Net) is a 137B-parameter instruction-tuned language model developed by Google Research. It demonstrates that fine-tuning a pretrained language model on a diverse collection of NLP tasks verbalized as natural language instructions — a procedure called **instruction tuning** — substantially improves zero-shot generalization to unseen task types ([Wei et al., 2022](raw/papers/2021-09-wei-flan/wei2021flan.md)).

FLAN was introduced in the paper "Finetuned Language Models Are Zero-Shot Learners" (Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu et al., Google Research, ICLR 2022). All lead authors contributed equally.

## Architecture

FLAN is an instruction-tuned version of **LaMDA-PT** — a dense left-to-right, decoder-only [[transformer|Transformer]] language model with 137B parameters ([Thoppilan et al., 2022](raw/papers/2021-09-wei-flan/wei2021flan.md)). Key specifications:

- Tokenization: [[sentencepiece|SentencePiece]] with 32k vocabulary
- Pretraining data: 2.49T BPE tokens from web documents (including code), dialog data, and Wikipedia
- ~10% of pretraining data was non-English
- LaMDA-PT is language-model-only (c.f. LaMDA, which was additionally fine-tuned for dialog)

## Instruction Tuning Procedure

FLAN was instruction-tuned on a mixture of **62 publicly available NLP datasets** from TensorFlow Datasets, grouped into **12 task clusters** ([Wei et al., 2022](raw/papers/2021-09-wei-flan/wei2021flan.md)):

- Natural Language Inference (7 datasets)
- Reading Comprehension (5)
- Closed-Book QA (3)
- Translation (8)
- Commonsense Reasoning (4)
- Coreference Resolution (3)
- Sentiment Analysis (4)
- Paraphrase Detection (4)
- Summarization (11)
- Struct-to-Text (4)
- Reading Comp. w/ Commonsense (2)
- Miscellaneous (7)

For each dataset, ten unique instruction templates were manually composed. Training setup:

- 30k gradient steps, batch size 8,192 tokens
- Adafactor optimizer (Shazeer & Stern, 2018), learning rate 3e-5
- Input length 1024, target length 256 tokens
- Training examples capped at 30k per dataset with examples-proportional mixing (max rate 3k)
- Packing (Raffel et al., 2020) to combine multiple examples per sequence
- ~60 hours on TPUv3 with 128 cores

## Key Results

### Zero-Shot Performance

FLAN's zero-shot performance compared to baselines ([Wei et al., 2022](raw/papers/2021-09-wei-flan/wei2021flan.md)):

| Benchmark | FLAN 137B zero-shot | GPT-3 175B zero-shot | GPT-3 175B few-shot |
|-----------|:-------------------:|:--------------------:|:-------------------:|
| ANLI R1 | 47.9 | 34.6 | 36.8 |
| RTE | 84.5 | 50.6 | 55.7 |
| BoolQ | 84.6 | 60.5 | 77.5 |
| ARC-challenge | 63.8 | 25.2 | — |
| ARC-easy | 80.7 | 68.8 | — |
| OBQA | 78.2 | 57.6 | 65.4 |
| StoryCloze | 94.7 | 83.2 | 87.7 |

FLAN surpasses zero-shot GPT-3 on **20 of 25 datasets** and outperforms few-shot GPT-3 on ANLI, RTE, BoolQ, AI2-ARC, OpenbookQA, and StoryCloze.

### Tasks Where Instruction Tuning Shines

Instruction tuning is most effective on tasks naturally verbalized as instructions: NLI, QA, translation, struct-to-text. It is **less effective** on tasks already formulated as language modeling (commonsense reasoning, coreference resolution as sentence completions), where instructions are largely redundant.

## Ablation Findings

Three key ablation results ([Wei et al., 2022](raw/papers/2021-09-wei-flan/wei2021flan.md)):

1. **More clusters → better performance:** Adding task clusters to instruction tuning monotonically improves zero-shot performance on unseen tasks, with no saturation observed at 7 clusters.

2. **Scale is critical:** Instruction tuning helps models at 68B–137B parameters but **hurts** models at 8B and below on unseen tasks — smaller models use all capacity learning the instruction-tuning mixture.

3. **Natural language instructions matter:** Removing instructions during fine-tuning drops average performance from 55.2% (FLAN) to 37.3% (no template) and 46.6% (dataset name only). Instructions during fine-tuning are crucial for zero-shot transfer.

## Compatibility with Other Methods

FLAN is complementary to:
- **Few-shot prompting** — adding exemplars at inference time improves all task clusters (80.8 vs 54.7 on NLI)
- **Prompt tuning** — instruction-tuned models respond substantially better to soft prompts than untuned models, especially in low-resource settings (10%+ improvement with only 32 examples)

## Significance

FLAN was among the first works to systematically demonstrate that **supervised data can improve generalist model performance** on unseen tasks, bridging the [[entities/gpt-3|pretrain–finetune]] and [[in-context-learning|prompting]] paradigms. It laid the groundwork for subsequent instruction-tuned models: InstructGPT/Ouyang et al. (2022), T0/Sanh et al. (2021), and all later instruction-tuned LLMs.

Key insight: cross-task generalization via instructions at scale works because the model learns the meta-skill of following instructions, which transfers to tasks it has never seen.

## Limitations

- Subjective task clustering — uses accepted categorizations but cluster assignment affects results
- Short single-sentence instructions only (c.f. detailed instructions given to crowd-workers)
- Potential pretraining data overlap with evaluation data (post-hoc analysis found no evidence of substantial impact)
- 137B model is expensive to serve

## Related

- [[instruction-tuning|Instruction Tuning]] — the core technique introduced by this paper
- [[entities/gpt-3|GPT-3]] — key baseline; FLAN outperforms GPT-3 zero-shot on most tasks despite 38B fewer parameters
- [[in-context-learning|In-Context Learning]] — the paradigm instruction tuning complements; both teach models to follow task descriptions but via different mechanisms
- [[rlhf|RLHF (InstructGPT)]] — contemporaneous approach to instruction following using human feedback + RL, published shortly after FLAN
- [[chain-of-thought|Chain-of-Thought]] — by the same lead author (Jason Wei); complementary prompting method
- [[flex-prompting|FLEX]] — later SLM control methodology sharing the goal of reliable model behaviour via structured instructions
- [[grace|GRACE]] — later framework for deterministic code generation using Intent-First Architecture, conceptually related
- [[openai|OpenAI]] — developed GPT-3 and InstructGPT, FLAN's key comparators
- [[scaling-laws|Scaling Laws]] — FLAN confirms and extends: instruction tuning only helps at sufficient scale
