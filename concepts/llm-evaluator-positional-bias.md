---
title: Positional Bias in LLM-as-a-Judge
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - evaluation
  - llm-as-judge
  - technique
sources:
  - "[Large Language Models are not Fair Evaluators](raw/papers/2023-05-wang-fair-evaluators/wang2023fairevaluators.md)"
confidence: high
---

# Positional Bias in LLM-as-a-Judge

When an LLM is used as a referee to score and rank candidate responses (the LLM-as-a-judge paradigm), its verdict is **systematically skewed by the order in which the responses appear in the prompt** ([Wang et al., 2023](raw/papers/2023-05-wang-fair-evaluators/wang2023fairevaluators.md)). Swapping two responses' positions can flip the winner — a manipulation the authors call "hacking" the evaluation. This is a direct reliability threat to any pairwise/single-position LLM judge, including the Vicuna evaluation pipeline ([Zheng et al., 2023](concepts/g-eval.md)) that GPT-4 made popular.

## The phenomenon

Wang et al. evaluate GPT-4 and ChatGPT as judges over the 80-question Vicuna Benchmark, comparing Vicuna-13B against ChatGPT and Alpaca-13B. The **win rate of the same model swings dramatically** depending only on which slot (Assistant 1 vs Assistant 2) it occupies:

| Evaluator | Matchup | Win rate as Asst 1 | Win rate as Asst 2 | Conflict rate |
|---|---|---|---|---|
| GPT-4 | Vicuna-13B v.s. ChatGPT | 51.3% | 23.8% | 37/80 (46.3%) |
| GPT-4 | Vicuna-13B v.s. Alpaca-13B | 92.5% | 92.5% | 4/80 (5.0%) |
| ChatGPT | Vicuna-13B v.s. ChatGPT | 2.5% | 82.5% | 66/80 (82.5%) |
| ChatGPT | Vicuna-13B v.s. Alpaca-13B | 37.5% | 90.0% | 42/80 (52.5%) |

Two clear patterns ([Wang et al., 2023](raw/papers/2023-05-wang-fair-evaluators/wang2023fairevaluators.md)):
- **GPT-4 favors the first-positioned response; ChatGPT favors the second.** The bias is directional and model-specific.
- **Stronger models / larger quality gaps are less hackable.** The conflict rate on "Vicuna v.s. Alpaca" is far lower than on "Vicuna v.s. ChatGPT", because Alpaca's responses are genuinely weaker and positional bias alone can't overturn a large gap. Conflict rate is negatively correlated with the score gap between the two responses (Figure 2).

## Conflict Rate metric

Formally, for N examples each with two responses (r1, r2), query the judge twice — once as T(q, r1, r2) and once as T(q, r2, r1) — and compare the two verdicts:

`Conflict Rate = (1/N) · Σ I(ER_r12_i ≠ ER_r21_i)`

where I(·) is the indicator function. It quantifies how often the same judge self-contradicts purely from a position swap.

## Calibration framework

Three strategies, applied additively:

1. **Multiple Evidence Calibration (MEC).** Inverts the vanilla template (which states a verdict then explains): the judge must generate *evaluation evidence first*, then assign scores. This makes the score conditional on the stated reasoning rather than an uninformed prior. Sampling k=3 evidence sets (temperature 1) and ensembling stabilizes the result; k>3 yields diminishing / slightly worse returns.
2. **Balanced Position Calibration (BPC).** Runs MEC in both positions and averages the 2k scores into a calibrated score `CS_r = (1/2k)·Σ S_r`. This directly cancels the directional position preference.
3. **Human-in-the-Loop Calibration (HITLC).** Introduces **Balanced Position Diversity Entropy (BPDE)** — the entropy of the {win, tie, lose} distribution across the 2k MEC+BPC results — to flag the most position-sensitive examples. A threshold β selects the top-β most-biased cases for human annotation, then merges human majority votes. BPDE outperforms random selection and vanilla diversity entropy for targeting human effort.

## Results

Human annotation: 3 authors independently label win/tie/lose on all 80 Vicuna questions (~3 min each, majority vote). Human Average = 71.7% accuracy, κ=0.54, $30/annotator.

| Evaluator | Method | Accuracy | Kappa | Cost |
|---|---|---|---|---|
| Human Avg | — | 71.7% | 0.54 | $30.0 |
| GPT-4 | Vanilla | 52.7% | 0.24 | $2.00 |
| GPT-4 | EC (k=1) | 56.5% | 0.29 | $2.00 |
| GPT-4 | MEC (k=3) | 58.7% | 0.30 | $3.19 |
| GPT-4 | MEC (k=6) | 60.9% | 0.33 | $6.38 |
| GPT-4 | MEC+BPC (k=3) | 62.5% | 0.37 | $6.38 |
| GPT-4 | MEC+BPC+HITLC (β=20%) | **73.8%** | **0.56** | $23.1 |
| ChatGPT | Vanilla | 44.4% | 0.06 | $0.10 |
| ChatGPT | EC (k=1) | 52.6% | 0.23 | $0.10 |
| ChatGPT | MEC (k=3) | 53.2% | 0.24 | $0.17 |
| ChatGPT | MEC (k=6) | 55.6% | 0.27 | $0.34 |
| ChatGPT | MEC+BPC (k=3) | 58.7% | 0.31 | $0.34 |
| ChatGPT | MEC+BPC+HITLC (β=20%) | **71.3%** | **0.52** | $18.3 |

Key findings ([Wang et al., 2023](raw/papers/2023-05-wang-fair-evaluators/wang2023fairevaluators.md)):
- MEC+BPC lifts GPT-4 and ChatGPT alignment by **+9.8%** and **+14.3%** accuracy over vanilla, respectively.
- HITLC with only 20% human annotation reaches or beats average-human alignment while cutting ChatGPT's cost from $30 to $18.3 (a 39% reduction).
- Temperature matters: both very low (0.2) and very high (1.4) sampling hurt; ~0.6–1.0 is the usable band for MEC.
- The method generalizes to the alternative **COMPARING** template (direct "Assistant 1 / 2 / Same" verdicts, no explicit scores) — MEC+BPC still raises accuracy and cuts conflict rate there too.
- Fine-grained analysis: MEC+BPC helps ChatGPT most on complex categories (common-sense, coding, math); GPT-4 is already a "fairer" evaluator than ChatGPT on those.

## Relationship to the broader judge literature

This is the first paper to rigorously quantify **positional** bias in LLM judges, but it sits in the same lineage as [[g-eval|G-Eval]] (which already flagged that LLM evaluators prefer LLM-generated text) and the Vicuna/MT-Bench judge pipeline ([Zheng et al., 2023](concepts/g-eval.md)). The shared lesson: an LLM judge is an imperfect proxy, and optimizing against it risks the same Goodhart/self-reinforcement failure analyzed in [[reward-model-overoptimization|Reward Model Overoptimization Scaling Laws]]. Position randomization + evidence-first prompting are now standard hygiene for any judge deployment.

## Open questions / limitations

- The study is scoped to the 80-question Vicuna Benchmark and the GPT-4 / ChatGPT evaluators; generalization to other judges and domains is shown only indirectly.
- Positional bias is most dangerous when responses are *close in quality* — meaning leaderboard gaps in that regime may be artifacts of slot order.
- HITLC still needs a human-in-the-loop budget; β trades cost against residual bias and must be tuned per use case.

## Related

- [[g-eval|G-Eval]] — early LLM-as-judge method that independently surfaced LLM-evaluator bias toward LLM text
- [[reward-model-overoptimization|Reward Model Overoptimization Scaling Laws]] — why treating an LLM judge as a reward proxy eventually degrades true quality
- [[factscore|FActScore]] — another reference-free evaluation metric, targeting factual precision rather than pairwise quality
