---
title: SLM-based Hallucination Detection (Multi-SLM Verifier)
created: 2026-06-16
updated: 2026-06-16
type: concept
tags:
  - technique
  - evaluation
  - agent
sources:
  - "[Hallucination Detection with Small Language Models](raw/papers/2025-06-24-cheung-hallucination-detection-slm/cheung2025hallucination.md)"
confidence: medium
---

# SLM-based Hallucination Detection

A framework for verifying LLM-generated responses against retrieved context using an ensemble of Small Language Models (SLM), introduced by Ming Cheung (dBeta Labs, ICDE Workshop 2025). Rather than detecting hallucinations during generation, the framework evaluates the final response post-hoc by decomposing it into sentences and scoring each against the question, context, and answer.

## Motivation

Hallucinations in LLM responses are hard to detect without ground truth. Traditional metrics like ROUGE and BLEU require reference answers. Prompting the same LLM to self-verify is circular and unreliable. Using a separate large model for verification defeats the cost savings.

SLMs (100M–5B params) offer a middle ground: deployable locally, fast enough for real-time verification, and cheap enough to run multiple models in ensemble ([Cheung, 2025](raw/papers/2025-06-24-cheung-hallucination-detection-slm/cheung2025hallucination.md)).

## Framework Architecture

The pipeline has three components:

### Splitter
Takes the LLM's full response `r_i` and decomposes it into individual sentences `r_{i,j}`. Each sentence is evaluated independently so partial hallucinations can be caught without polluting correct segments.

### SLM Ensemble
Multiple small language models (Qwen2-1.5B-Instruct and MiniCPM-2B in the paper) each score every sentence. Each SLM receives a prompt with the question `q_i`, the context `c_i`, and the sentence `r_{i,j}`, and is asked to generate a "Yes" or "No" answer indicating factual consistency. The score for model `m` on sentence `j` of response `i` is:

`s^{(m)}_{i,j} = P(token_1 = yes | q_i, c_i, r_{i,j})`

Only the log-probability of the first generated token matters — no need for full response generation.

### Checker
Combines scores across models and sentences:

1. **Per-model normalization**: SLMs have different calibration scales. Raw P(yes) scores are z-scored per model:

   `\tilde{s}^{(m)}_{i,j} = (s^{(m)}_{i,j} - \mu_m) / \sigma_m`

2. **Cross-model aggregation**: Normalized scores from all `M` models are averaged per sentence:

   `s_{i,j} = (1/M) \sum_{m=1}^{M} \tilde{s}^{(m)}_{i,j}`

3. **Cross-sentence aggregation**: Sentence scores are combined via **harmonic mean** (outperformed arithmetic, geometric, min, and max):

   `s_i = |S(r_i)| / \sum_{j} (1 / s_{i,j})`

   Scores ≤ 0 are clamped to a small positive value to avoid division errors.

4. **Threshold decision**: If `s_i` exceeds a threshold, the response is labeled "correct"; otherwise "hallucinated".

## Results

Tested on a real dataset from the Lane Crawford employee handbook: 100+ QA triples across HR topics (employment, policy, media, devices). Each triple had correct, partially correct, and wrong responses.

| Approach | F1 (correct vs wrong) | F1 (correct vs partial) |
|----------|----------------------|------------------------|
| ChatGPT P(True) | baseline | baseline |
| P(yes) (single SLM, no splitter) | +~3% | — |
| Qwen2 only | — | — |
| MiniCPM only | — | — |
| **Proposed (Qwen2 + MiniCPM + Splitter + Normalization + Harmonic Mean)** | **~10% better** | **~10% better** |

The proposed framework achieved approximately 11% improvement over ChatGPT and 6.6% over the P(yes) baseline for detecting correct vs wrong responses. The distribution analysis shows that "wrong" responses cluster at low `s_i` values while "correct" responses cluster at high values, with the geometric and harmonic means providing the cleanest separation.

## Key Insights

- **SLMs as verifiers, not generators**: A 1.5B–2B parameter model too weak for free-text generation can reliably perform binary verification when given structured Yes/No prompts with context. This aligns with the [[flex-prompting|FLEX methodology]] principle that controlled prompting extracts reliable behaviour from small models. ([Cheung, 2025](raw/papers/2025-06-24-cheung-hallucination-detection-slm/cheung2025hallucination.md))

- **Sentence-level decomposition matters**: Scoring the entire response as one blob produces poorer separation. Splitting isolates hallucinated segments so they aren't masked by correct nearby text.

- **Ensemble helps**: Multiple SLMs with different inductive biases (Qwen2 vs MiniCPM) produce better-calibrated scores than either alone. The z-score normalization step is critical because raw P(yes) probabilities are not comparable across models.

- **Harmonic mean penalises weak segments**: Unlike arithmetic mean, harmonic mean is dominated by the smallest score — a single bad sentence drags the whole response score down, which is the desired behaviour for hallucination detection.

## Connections to Other Concepts

- [[retrieval-augmented-generation|RAG]] — the framework operates in a RAG context: the LLM generates from retrieved context, and the verifier checks the response against that same context
- [[slm-moe-agentic-ai|SLM vs MoE]] — provides experimental evidence that SLMs can outperform large models on specific verification tasks, strengthening the case for heterogeneous agentic systems
- [[flex-prompting|FLEX]] — both use structured prompting of SLMs with probability-based output analysis; FLEX focuses on tool selection while this method targets factual verification
- [[chain-of-thought|Chain-of-Thought]] — this framework explicitly avoids CoT, using P(yes) directly; aligns with findings that CoT harms SLM performance on factual tasks
- [[contract-programming|Contract Programming]] — the verifier acts as a post-condition checker for LLM-generated responses, executing the "assert" step of Design by Contract for AI
- [[grace|GRACE]] — the verification stage in GRACE's five-stage process could incorporate this SLM-based checking
