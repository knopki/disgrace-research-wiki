---
title: Self-Consistency
created: 2026-06-25
updated: 2026-06-25
type: concept
tags:
  - technique
  - prompting
sources:
  - "[Self-Consistency Improves Chain of Thought Reasoning in Language Models](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)"
confidence: high
---
# Self-Consistency

Self-consistency is a decoding strategy that replaces greedy decoding in [[chain-of-thought|Chain-of-Thought (CoT)]] prompting. Instead of generating a single reasoning path greedily, it samples multiple diverse reasoning paths from the language model's decoder, then selects the most consistent answer by majority vote (marginalising out the sampled paths). Introduced by Wang et al. (Google, ICLR 2023).

## Mechanism

The method follows three steps ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)):

1. **Prompt** the language model with chain-of-thought exemplars (standard CoT prompting)
2. **Sample** a diverse set of candidate reasoning paths from the decoder using temperature, top-k, or nucleus sampling (typically 10–40 paths)
3. **Marginalise** by aggregating the final answers — the answer with the highest count (majority vote) is selected as the most consistent

Formally, for m sampled outputs (rᵢ, aᵢ) where rᵢ is the reasoning chain and aᵢ is the parsed answer, self-consistency returns:

`argmax_a Σᵢ 𝟙(aᵢ = a)`

The approach can also use a probability-weighted sum (normalised by output length) for aggregation, but in practice unweighted majority vote performs comparably because the language model assigns similar normalised probabilities to different reasoning paths ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

### Underlying Intuition

Self-consistency leverages the observation that complex reasoning problems typically admit multiple valid reasoning paths that converge to the same correct answer. Diverse sampling captures different strategies (e.g., different calculation orderings, different decomposition steps). Incorrect paths, even when diverse, tend to cluster on different wrong answers and thus do not outvote the correct one. This is analogous to the human experience that converging independent lines of reasoning increase confidence in an answer.

## Key Properties

- **Unsupervised** — no training, fine-tuning, or human annotation required; works off-the-shelf with any pre-trained model
- **Task-agnostic** — applicable to any reasoning task with a fixed answer set
- **Lossy but robust** — correct reasoning processes tend to agree on the final answer; incorrect ones do not
- **Computational cost** — requires K× more decoding than greedy (K = number of sampled paths). Performance saturates quickly: most gains realised by 5–10 paths, 20–40 paths for near-maximal results
- **Calibration signal** — the consistency score (percentage of decodes agreeing with the final answer) correlates strongly with accuracy, providing a built-in uncertainty estimate

## Key Results

### Arithmetic Reasoning

| Task | CoT greedy | +Self-consistency | Δ |
|------|:---------:|:-----------------:|:-:|
| **GSM8K** | 56.5 | 74.4 | **+17.9** |
| **SVAMP** | 75.8 | 86.8 | **+11.0** |
| **AQuA** | 39.8 | 52.0 | **+12.2** |
| **MultiArith** | 96.2 | 100.0 | **+3.8** |
| **ASDiv** | 80.1 | 87.8 | **+7.6** |

PaLM-540B results ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)). Similar or larger gains observed across UL2-20B, LaMDA-137B, and GPT-3 175B.

### Commonsense Reasoning

| Task | CoT greedy | +Self-consistency | Δ |
|------|:---------:|:-----------------:|:-:|
| StrategyQA | 73.4 | 79.8 | **+6.4** |
| ARC-challenge | 83.6 | 87.5 | **+3.9** |
| CSQA | 79.0 | 80.7 | **+1.7** |
| ARC-easy | 94.0 | 96.0 | **+2.0** |

PaLM-540B results ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

### Scaling Behaviour

Self-consistency gains increase with model scale: +3–6% for UL2-20B vs +9–23% for LaMDA-137B and GPT-3. Larger models already achieve higher accuracy with greedy decoding, but self-consistency provides additional large relative gains on the hardest tasks (AQuA, GSM8K). The method is robust to sampling temperature (T=0.3–0.7), top-k (k=20–40), and nucleus (p=0.9–0.95) parameters ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

### Robustness

Self-consistency improves accuracy even with **imperfect prompts** (randomised numbers in CoT exemplars), **equation-only prompts** (non-natural-language reasoning), and **zero-shot-CoT** (Kojima et al., 2022). On PaLM-540B, zero-shot-CoT + self-consistency achieved 89.0% on MultiArith and 70.1% on GSM8K. It also recovers performance where CoT initially degrades accuracy on certain NLP tasks (BoolQ, e-SNLI, RTE) ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

## Comparison to Other Approaches

| Method | Requires training/annotation? | Gain vs CoT greedy (GSM8K) |
|--------|:---------------------------:|:--------------------------:|
| **Self-consistency** (40 paths) | No | +17.9 |
| Sample-and-rank (40 samples) | No | ~+3 |
| Beam search (40 beams) | No | Degrades |
| Prompt-order ensemble | No | +2.1 |
| Multi-prompt ensemble | No | +1.5 |
| Fine-tuned verifier (Cobbe et al., 2021) | Yes (7.5k examples) | ~+15 |

Self-consistency significantly outperforms sample-and-rank (ranking by log probability) and beam search because the key to its effectiveness is **diversity** of reasoning paths — beam search produces homogeneous outputs, and log-probability ranking does not correct for systematic errors. Self-consistency acts as a "self-ensemble" on a single model, unlike typical model-ensembles that require training multiple independent models ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

## Limitations

1. **Computational cost** — K-fold decoding overhead. Mitigation: 5–10 paths capture most gains.
2. **Fixed answer set required** — only applicable when answers come from a fixed set (e.g., numbers, multiple choice, yes/no). Not directly applicable to open-ended generation without a consistency metric.
3. **Non-sensical reasoning paths** — language models sometimes generate plausible-sounding but factually incorrect reasoning, even when reaching the correct answer.
4. **Calibration problem** — the model's own normalised probabilities for different reasoning paths are similar for both correct and incorrect solutions, confirming the need for training-free aggregation instead of internal confidence.

## Related

- [[chain-of-thought|Chain-of-Thought (CoT)]] — predecessor method that self-consistency builds on by replacing greedy decoding with sample-and-marginalise
- [[in-context-learning|In-Context Learning]] — broader paradigm within which self-consistency operates
- [[reward-model-overoptimization|Reward Model Overoptimization]] — similar sample-and-marginalise philosophy applied to generation quality via verifier training, but requires supervised data
- [[entities/gpt-3|GPT-3]] — evaluated on GPT-3 175B (code-davinci-001 and code-davinci-002)
- [[chain-of-thought#zero-shot-cot|Zero-shot-CoT]] (Kojima et al., 2022) — self-consistency works on top of zero-shot CoT, yielding +26.2% on GSM8K
