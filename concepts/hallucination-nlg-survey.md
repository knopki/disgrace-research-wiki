---
title: Survey of Hallucination in NLG (Ji et al.)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags: [survey, evaluation, hallucination, methodology]
sources:
- "[Survey of Hallucination in Natural Language Generation](raw/papers/2022-02-ji-hallucination-nlg/ji2022hallucination.md)"
confidence: high
---

# Survey of Hallucination in NLG (Ji et al.)

First comprehensive survey of the hallucination problem across the full span of
Natural Language Generation tasks, by Ji et al. (Hong Kong University of Science
and Technology / Amazon, ACM Computing Surveys 2023; arXiv:2202.03629, first
submitted Feb 2022). It consolidates previously fragmented per-task studies and
offers a unified definition, taxonomy, catalog of contributors, metrics,
mitigation methods, and future directions, plus task-specific chapters
(abstractive summarization, dialogue, generative QA, data-to-text,
machine translation, vision-language) and — added in a Jan 2024 update — a
section on [[hallucination-llm-survey|hallucinations in LLMs]].

## Definition and taxonomy

The survey adopts the inclusive NLP definition: hallucination is generated
content that is **nonsensical or unfaithful to the provided source content**.
Two categories ([Ji et al., 2022](raw/papers/2022-02-ji-hallucination-nlg/ji2022hallucination.md)):

- **Intrinsic hallucination** — output contradicts the source content (e.g. a
  summary stating "the first Ebola vaccine was approved in 2021" against a source
  saying "approved by the FDA in 2019").
- **Extrinsic hallucination** — output that *cannot* be verified from the source
  (neither supported nor contradicted). Not always erroneous: it may draw on
  factually correct external knowledge, but its unverifiable nature makes it a
  safety risk and is treated with caution in most literature.

The term originated in computer vision (super-resolution, inpainting) with a
*positive* connotation; its negative NLG sense was cemented by Maynez et al.
(2020) on abstractive summarization.

## Contributors to hallucination

The survey groups root causes into two families ([Ji et al., 2022](raw/papers/2022-02-ji-hallucination-nlg/ji2022hallucination.md)):

1. **Data** — source-reference divergence (heuristic data collection, or inherent
   to the task), which trains models to generate text not grounded in the source.
2. **Training and modeling choices** — even with little dataset divergence,
   neural training/inference choices induce hallucination (Parikh et al., 2020):
   exposure bias, inaccurate attention, erroneous parametric knowledge,
   inappropriate training objectives, and decoding artifacts (degeneration /
   likelihood-maximization pitfalls noted by Holtzman et al., 2019 and Welleck
   et al., 2019).

## Metrics

Conventional quality metrics (ROUGE, BLEU, METEOR) correlate poorly with
human judgments of faithfulness — Falke et al. (2019) found SOTA summarizers
hallucinate in ~25% of summaries while still scoring well. The survey catalogs
task-specific faithfulness metrics (e.g. token/entity-level factuality,
information-extraction-based checks) that go beyond surface-overlap scoring.

## Mitigation

Two categories mirroring the contributors ([Ji et al., 2022](raw/papers/2022-02-ji-hallucination-nlg/ji2022hallucination.md)):

- **Data-related methods** — cleaning/aligning source-reference pairs, reducing
  dataset noise (esp. for machine translation), synthetic perturbation for
  robustness.
- **Modeling and inference methods** — constrained decoding, post-editing
  correctors (e.g. SpanFact, Cao et al. 2020's corrector trained on heuristically
  corrupted references, HERMAN for quantity faithfulness), and architectural
  changes to attention/representations.

## LLM section (added Jan 2024)

The updated survey notes LLM hallucinations as a distinct open problem and
highlights open questions: correlation with model/data size (cf.
[[scaling-laws|scaling laws]]), relationship to autoregressive generation,
whether [[rlhf|SFT vs RLHF]] mitigate via different mechanisms, and the lower
bound of hallucination. It also flags the **alignment tax** of mitigation:
safety fine-tuning degrades ChatGPT/GPT-4 over time, and even [[retrieval-augmented-generation|RAG]]
can compromise response quality when retrieved evidence is sub-optimal.

## Relation to other work

- **[[hallucination-llm-survey|Huang et al. survey]]** — a later (2023) survey
  that *redefines* the taxonomy specifically for LLMs (factuality vs faithfulness
  hallucination) rather than task-specific NLG. Ji et al. focus on pre-LLM NLG
  tasks; Huang et al. narrow onto LLMs.
- **[[factscore|FActScore]]** — an instance of the extrinsic/atomic-fact
  evaluation lineage the survey calls for: fine-grained, source-grounded
  factuality measurement.
- **[[truthfulqa|TruthfulQA]]** — benchmarks *truthfulness* (imitation of human
  falsehoods), a different axis from source-faithfulness surveyed here.
