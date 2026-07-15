---
title: Self-Consistency
created: 2026-06-25
updated: 2026-07-15
type: concept
tags:
  - technique
  - prompting
sources:
  - "[Self-Consistency Improves Chain of Thought Reasoning in Language Models](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)"
confidence: high
---

# Self-Consistency

Self-consistency is a decoding strategy that replaces greedy decoding in [[chain-of-thought|Chain-of-Thought (CoT)]] prompting. Instead of generating a single reasoning path greedily, it samples multiple diverse reasoning paths from the language model's decoder, then selects the most consistent answer by majority vote (marginalising out the sampled paths). Introduced by Wang et al. (Google, ICLR 2023) ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

## Mechanism

The method follows three steps ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)):

1. **Prompt** the language model with chain-of-thought exemplars (standard few-shot CoT prompting)
2. **Sample** a diverse set of candidate reasoning paths from the decoder using temperature, top-k, or nucleus sampling (the paper samples 40 paths per run, averaged over 10 runs)
3. **Marginalise** by aggregating the final answers — the answer with the highest count (majority vote) is selected as the most consistent

Formally, for m sampled outputs (rᵢ, aᵢ) where rᵢ is the reasoning chain and aᵢ is the parsed answer, self-consistency returns:

`argmax_a Σᵢ 𝟙(aᵢ = a)`

The approach can also weight each (rᵢ, aᵢ) by its length-normalised generation probability P(rᵢ, aᵢ | prompt, question), but in practice unweighted majority vote performs comparably because the model assigns similar normalised probabilities to different reasoning paths ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)). Table 1 of the paper shows normalised weighted-sum and unweighted majority vote give nearly identical accuracy (e.g., GSM8K 74.1 vs 74.4 on PaLM-540B).

### Underlying Intuition

Self-consistency leverages the observation that complex reasoning problems typically admit multiple valid reasoning paths that converge to the same correct answer. Diverse sampling captures different strategies (e.g., different calculation orderings, different decomposition steps). Incorrect paths, even when diverse, tend to cluster on different wrong answers and thus do not outvote the correct one. This is analogous to the human experience that converging independent lines of reasoning increase confidence in an answer.

## Key Properties

- **Unsupervised** — no training, fine-tuning, or human annotation required; works off-the-shelf with any pre-trained model
- **Task-agnostic** — applicable to any reasoning task with a fixed answer set
- **Lossy but robust** — correct reasoning processes tend to agree on the final answer; incorrect ones do not
- **Computational cost** — requires K× more decoding than greedy (K = number of sampled paths). Performance saturates quickly: most gains realised by 5–10 paths, 20–40 paths for near-maximal results
- **Calibration signal** — the consistency score (percentage of decodes agreeing with the final answer) correlates strongly with accuracy, providing a built-in uncertainty estimate (the model "knows when it doesn't know")

## Key Results

The paper evaluates self-consistency over four models in the few-shot setting, sampling 40 paths per run (averaged over 10 runs), against CoT greedy decoding as baseline. Models: UL2-20B, LaMDA-137B, PaLM-540B, and GPT-3 (code-davinci-001 / code-davinci-002) ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

### Headline results (PaLM-540B)

These are the abstract's headline numbers — PaLM-540B, self-consistency (40 paths) vs CoT greedy:

| Task | CoT greedy | +Self-consistency | Δ |
|------|:---------:|:-----------------:|:-:|
| **GSM8K** | 56.5 | 74.4 | **+17.9** |
| **SVAMP** | 79.0 | 86.6 | **+7.6** |
| **AQuA** | 35.8 | 48.3 | **+12.5** |
| **StrategyQA** | 75.3 | 81.6 | **+6.3** |
| **ARC-challenge** | 85.2 | 88.7 | **+3.5** |

(Abstract rounds StrategyQA to +6.4 and ARC-c to +3.9.) Full arithmetic table also includes AddSub (+1.8), MultiArith (+4.6), ASDiv (+7.9); full commonsense table adds CSQA (+1.7), ARC-easy (+1.1).

### Cross-model arithmetic gains (Δ over CoT greedy)

The same +17.9 GSM8K gain also appears on GPT-3 code-davinci-002 (60.1 → 78.0); +12.2 AQuA and +11.0 SVAMP are GPT-3 code-davinci-002 results. Gains grow with model scale and are consistent across all four models.

| Model | GSM8K | SVAMP | AQuA | MultiArith |
|-------|:-----:|:-----:|:----:|:----------:|
| UL2-20B | +3.2 | +6.8 | +3.3 | +4.3 |
| LaMDA-137B | +10.6 | +14.4 | +9.1 | +23.9 |
| PaLM-540B | +17.9 | +7.6 | +12.5 | +4.6 |
| GPT-3 code-davinci-001 | +8.8 | +14.7 | +6.7 | +23.2 |
| GPT-3 code-davinci-002 | +17.9 | +11.0 | +12.2 | +3.8 |

### Scaling Behaviour

Self-consistency gains increase with model scale: +3–6% for UL2-20B vs +9–23% for LaMDA-137B and GPT-3. Larger models already achieve higher accuracy with greedy decoding, but self-consistency provides additional large relative gains on the hardest tasks (AQuA, GSM8K). The method is robust to sampling temperature (T=0.3–0.7), top-k (k=20–40), and nucleus (p=0.9–0.95) parameters ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

### Robustness

Self-consistency improves accuracy even with **imperfect prompts** (randomised numbers in CoT exemplars: LaMDA-137B GSM8K 17.1 → 14.9 greedy, 23.4 with SC), **equation-only prompts** (non-natural-language reasoning: 5.0 → 6.5 on LaMDA-137B GSM8K), and **zero-shot-CoT** (Kojima et al., 2022). On PaLM-540B, zero-shot-CoT + self-consistency reached 69.2% on GSM8K (up from 43.0% zero-shot-CoT alone, +26.2%). It also recovers performance where CoT initially degrades accuracy on certain NLP tasks (BoolQ, e-SNLI, RTE — Table 5) ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

## Comparison to Other Approaches

| Method | Requires training/annotation? | GSM8K vs CoT greedy |
|--------|:---------------------------:|:--------------------|
| **Self-consistency** (40 paths, PaLM-540B) | No | +17.9 |
| Sample-and-rank (40 samples, GPT-3 cd-001) | No | much smaller gain than SC |
| Beam search (≤40 beams, UL2-20B) | No | degrades as beams increase (23.6 → 10.2 on AQuA) |
| Prompt-order ensemble (40 permutations, LaMDA) | No | +2.1 |
| Multi-prompt ensemble (3 sets, LaMDA) | No | +1.5 |
| Fine-tuned verifier (Cobbe et al., 2021) | Yes (7.5k examples) | ~55% absolute on GSM8K (supervised) — SC reaches 74.4% unsupervised on PaLM-540B |

Self-consistency significantly outperforms sample-and-rank (ranking by log probability) and beam search because the key to its effectiveness is **diversity** of reasoning paths — beam search produces homogeneous outputs, and log-probability ranking does not correct for systematic errors. Self-consistency acts as a "self-ensemble" on a single model, unlike typical model-ensembles that require training multiple independent models ([Wang et al., 2022](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md)).

## Limitations

1. **Computational cost** — K-fold decoding overhead. Mitigation: 5–10 paths capture most gains.
2. **Fixed answer set required** — only applicable when answers come from a fixed set (e.g., numbers, multiple choice, yes/no). Not directly applicable to open-ended generation without a consistency metric.
3. **Non-sensical reasoning paths** — language models sometimes generate plausible-sounding but factually incorrect reasoning, even when reaching the correct answer (the paper notes this on StrategyQA, Table 4).
4. **Calibration problem** — the model's own normalised probabilities for different reasoning paths are similar for both correct and incorrect solutions, confirming the need for training-free aggregation instead of internal confidence.

## Related

- [[chain-of-thought|Chain-of-Thought (CoT)]] — predecessor method that self-consistency builds on by replacing greedy decoding with sample-and-marginalise
- [[in-context-learning|In-Context Learning]] — broader paradigm within which self-consistency operates
- [[reward-model-overoptimization|Reward Model Overoptimization]] — similar sample-and-marginalise philosophy applied to generation quality via verifier training, but requires supervised data
- [[entities/gpt-3|GPT-3]] — evaluated on GPT-3 175B (code-davinci-001 and code-davinci-002)
- [[chain-of-thought#zero-shot-cot|Zero-shot-CoT]] (Kojima et al., 2022) — self-consistency works on top of zero-shot CoT; on PaLM-540B this yields +26.2% on GSM8K (43.0 → 69.2, Wang et al. Table 8)
