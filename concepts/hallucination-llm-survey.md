---
title: Survey on Hallucination in LLMs (Huang et al.)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags: [survey, hallucination, evaluation, methodology, alignment]
sources:
- "[A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions](raw/papers/2023-11-huang-hallucination-llm/huang2023hallucination.md)"
confidence: high
---

# Survey on Hallucination in LLMs (Huang et al.)

A comprehensive survey of hallucination *specific to* large language models, by
Huang et al. (Harbin Institute of Technology / Tencent AI Lab, ACM TOIS;
arXiv:2311.05232, Nov 2023). It argues that the open-ended, general-purpose
nature of LLMs makes hallucination a distinct challenge from the task-specific
NLG settings covered by [[hallucination-nlg-survey|Ji et al.'s earlier survey]],
and proposes a **redefined taxonomy**, a layered causal analysis, detection
methods + benchmarks, mitigation strategies tied to those causes, and an
analysis of limitations in [[retrieval-augmented-generation|RAG]].

## Redefined taxonomy

Huang et al. recast hallucination for the LLM era into two primary types
([Huang et al., 2023](raw/papers/2023-11-huang-hallucination-llm/huang2023hallucination.md)):

- **Factuality hallucination** — discrepancy between generated content and
  verifiable real-world facts. Subtypes: *factual inconsistency* (contradicts
  grounded facts) and *factual fabrication* (unverifiable / invented content).
- **Faithfulness hallucination** — divergence from user input or internal
  self-consistency. Subtypes: *instruction inconsistency* (deviates from the
  user's directive), *context inconsistency* (contradicts provided context),
  and *logical inconsistency* (internal contradictions within the output).

This reframing absorbs Ji et al.'s intrinsic/extrinsic split but extends it to
instruction- and logic-level failures that arise only in open-ended assistants.

## Causes (three-stage framing)

Root causes span the entire capability-acquisition pipeline
([Huang et al., 2023](raw/papers/2023-11-huang-hallucination-llm/huang2023hallucination.md)):

1. **Data** — misinformation/biases in pre-training corpora; knowledge-boundary
   gaps; inferior alignment data.
2. **Training** — pre-training (parametric knowledge errors), SFT (supervised
   signal noise), and [[rlhf|RLHF]] (preference-model limitations, over-
   optimization).
3. **Inference** — imperfect decoding strategies (e.g. likelihood-maximization
   degeneration, Holtzman et al. 2020) and over-confidence (models emit false
   content with high asserted certainty).

## Detection and benchmarks

Detection splits along the taxonomy: **factuality detection** (identify factual
inaccuracies) and **faithfulness detection** (evaluate consistency with context
/ self-consistency). Benchmarks divide into *hallucination evaluation* (measure
extent on cutting-edge LLMs) and *hallucination detection* (testbeds for
detectors). The survey notes representative benchmarks such as TruthfulQA-style
and factuality-oriented suites (e.g. related to [[factscore|FActScore]]'s
atomic-fact precision lineage).

## Mitigation

Strategies are organized by cause: data-level (cleaning, knowledge-boundary
awareness), training-level (better SFT/RLHF, alignment-data quality), and
inference-level (controlled decoding, self-reflection, self-consistency
decoding). The survey stresses that mitigation should map to the identified
cause — its organizing principle versus prior surveys.

## RAG limitations

Despite [[retrieval-augmented-generation|RAG]]'s promise in reducing
hallucination, the survey details two bottleneck classes
([Huang et al., 2023](raw/papers/2023-11-huang-hallucination-llm/huang2023hallucination.md)):

- **Retrieval failure** — flawed query formulation, unreliable/narrow retrieval
  sources, weak retriever.
- **Generation bottleneck** — the LLM's contextual awareness and contextual
  alignment fail to faithfully reflect retrieved evidence.

## Open questions and future directions

- **Hallucination in large vision-language models (LVLMs)** — object/attribute
  fabrication; mitigated by truthful fine-tuning, post-hoc expert correction, or
  LVLM-self utilisation (Leng et al., Huang et al., Zhao et al., 2023/2024).
- **Knowledge boundaries** — LLMs struggle to recognize their own limits and
  confidently produce falsehoods. Latent truthfulness probes (Burns et al. 2022,
  Azaria & Mitchell 2023) show promise but Levinstein & Herrmann (2023) argue
  current lie-detector methods do not yet generalize reliably.
- **Theoretical foundations** — absence of rigorous mathematical formulations
  for *why* hallucination occurs (links to [[scaling-laws|scaling laws]],
  compression, compositionality).

## Relation to other work

- **[[hallucination-nlg-survey|Ji et al. survey]]** — Huang et al. position
  theirs as complementary: Ji et al. cover pre-LLM task-specific NLG; Huang et
  al. narrow onto LLMs with a factuality/faithfulness taxonomy and cause-linked
  mitigation.
- **[[rlhf|RLHF]]** and **[[retrieval-augmented-generation|RAG]]** — two of the
  three training/inference pillars the survey implicates in (and offers
  remediation for) hallucination.
- **[[factscore|FActScore]]** — an evaluation instrument in the factuality-detection
  lineage the survey surveys.
