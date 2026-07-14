---
title: TruthfulQA
created: 2026-06-21
updated: 2026-06-21
type: concept
tags:
  - benchmark
  - evaluation
  - alignment
sources:
  - "[TruthfulQA: Measuring How Models Mimic Human Falsehoods](raw/papers/2021-09-lin-truthfulqa/lin2021truthfulqa.md)"
confidence: high
---

# TruthfulQA

A benchmark for measuring whether language models generate truthful answers. Introduced by Lin, Hilton & Evans ([Oxford / OpenAI, ACL 2022](raw/papers/2021-09-lin-truthfulqa/lin2021truthfulqa.md)). Comprises 817 questions across 38 categories (health, law, finance, politics, misconceptions, conspiracies, fiction, proverbs, etc.), designed to elicit **imitative falsehoods** — false answers that models learn because they have high probability on the human-written training distribution.

## Core Finding: Inverse Scaling

The headline result: **larger models are less truthful**. This is the opposite of typical NLP tasks (including other QA benchmarks). GPT-3-175B with a helpful prompt achieves 58% truthful answers vs human baseline 94%. The inverse scaling trend holds across model families (GPT-3, GPT-Neo/J, GPT-2), in both generation and multiple-choice settings.

The paper explains this as a consequence of the standard LM training objective: imitating human text. Larger models better approximate the training distribution, which includes many popular falsehoods and misconceptions. Smaller models are less capable of generating fluent falsehoods, so they default to safer (less informative) answers.

## Truthfulness vs Informativeness

The benchmark distinguishes between:
- **Truthful** — does not assert a false statement (allows "No comment", "I don't know")
- **Informative** — provides information that reduces uncertainty raised by the question
- **True + informative** — the ideal; human-level performance

Non-committal answers count as truthful. This decouples truthfulness from capability: a model can be truthful while being uninformative.

## GPT-judge

GPT-judge is a [[entities/gpt-3|GPT-3]]-6.7B model finetuned to classify answers as true/false for TruthfulQA questions. Achieves 90-96% validation accuracy on held-out model families, outperforming ROUGE-1, BLEURT, and GPT-3-Sim baselines. Also finetuned for informativeness evaluation (86.3% on UnifiedQA). Provides a cheap, reproducible proxy for human evaluation.

## Relation to Alignment

TruthfulQA results are frequently cited as motivation for [[rlhf|RLHF]] and [[instruction-tuning|instruction tuning]] approaches. [[entities/openai|OpenAI]]'s InstructGPT paper (Ouyang et al., 2022) showed their RLHF-finetuned model generates truthful and informative answers ~2x more often than GPT-3 on TruthfulQA ([RLHF page](concepts/rlhf.md)). The benchmark demonstrated that scaling alone is insufficient for truthfulness — alternative training objectives are necessary.

## Limitations

- Zero-shot setting only — not designed for few-shot evaluation
- General-knowledge questions only — does not test domain-specific truthfulness
- Questions are adversarial by construction, may over- or under-estimate deployed system performance
- Authors note that questions likely contain a mix of imitative and non-imitative falsehoods, though experiments (paraphrases, matched controls) point to imitative as the dominant factor

## See Also

- [[rlhf|RLHF]] — InstructGPT's 2× truthfulness improvement on TruthfulQA  
- [[instruction-tuning|Instruction Tuning]] — complementary approach to improving truthfulness  
- [[humaneval|HumanEval]] — another benchmark showing LM limitations not solved by scale (functional correctness)  
- [[scaling-laws|Scaling Laws]] — the paper's inverse scaling finding contrasts with standard scaling-law improvements  
- [[entities/openai|OpenAI]] — organization behind GPT-3 and InstructGPT models evaluated
- [[hallucination-nlg-survey|Hallucination in NLG (Ji et al.)]] — notes TruthfulQA measures *truthfulness* (imitation of human falsehoods), a different axis from source-faithfulness
