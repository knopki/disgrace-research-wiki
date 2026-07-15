---
title: G-Eval (NLG Evaluation with LLM + CoT)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - evaluation
  - technique
  - prompting
  - llm-as-judge
sources:
  - "[G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment](raw/papers/2023-03-liu-geval/liu2023geval.md)"
confidence: high
---

# G-Eval (NLG Evaluation with LLM + CoT)

G-Eval is a prompt-based framework for automatically evaluating natural language generation (NLG) outputs using a large language model (GPT-4 in the original paper) with **chain-of-thought (CoT)** and a **form-filling paradigm**. Proposed by Liu et al. at Microsoft Cognitive Services Research ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)). It targets the weakness of conventional reference-based metrics (BLEU, ROUGE) — low correlation with human judgments on open-ended and creative tasks — and the weaker human correspondence of earlier reference-free LLM evaluators.

## Method

G-Eval has three components ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)):

1. **Prompt with task definition + evaluation criteria.** A natural-language instruction defines the evaluation task and custom criteria (e.g. coherence, consistency, fluency, relevance, groundedness). For summarization, criteria are aligned with the DUC quality questions.
2. **Auto chain-of-thought (CoT).** Instead of hand-designing evaluation steps per task, the LLM is asked to generate its own detailed Evaluation Steps from the Task Introduction and Evaluation Criteria. The CoT provides additional context/guidance for the final scoring and makes the evaluation process explainable.
3. **Form-filling scoring function.** The LLM is called with prompt + CoT + input context + target text, and outputs a score in a structured form (one aspect per field, e.g. 1–5 scales).

### Probability-weighted scoring

A key refinement: rather than reading a single integer score (which causes many ties and low variance), G-Eval reads the **token probabilities** the LLM assigns to each possible score value. The final score is the probability-weighted sum:

`score = Σᵢ p(sᵢ) · sᵢ`, over the predefined score set S = {s₁, …, sₙ}.

This yields a continuous, fine-grained score that better captures subtle quality differences between outputs ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)). Implementation note: GPT-4 (at publication) did not expose token probabilities, so the authors sampled n=20 with temperature=1, top-p=1 and estimated the distribution empirically; GPT-3.5 (text-davinci-003) was run at temperature=0.

## Results

Evaluated on three meta-evaluation benchmarks (correlation with human ratings): SummEval (summarization, 4 aspects), Topical-Chat (dialogue response generation, 4 aspects), and QAGS (hallucination/consistency in summarization) ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)).

**SummEval (summary-level Spearman ρ / Kendall-Tau τ, AVG across aspects):**

- G-Eval-4 (with probabilities): ρ=0.514, τ=0.446 — surpasses all prior methods
- G-Eval-3.5 (with probabilities): ρ=0.401, τ=0.320
- UniEval (prior SOTA neural): ρ=0.474, τ=0.377
- BARTScore: ρ=0.385, τ=0.305
- GPTScore (GPT-3 conditional-probability baseline): ρ=0.417
- Reference-based (ROUGE-1/L, BERTScore, MoverScore): ρ≈0.17–0.23

**Topical-Chat (turn-level, AVG ρ):** G-Eval-4 = 0.588, G-Eval-3.5 = 0.585, UniEval = 0.417, USR = 0.403. G-Eval substantially beats prior evaluators on dialogue as well ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)).

**QAGS (consistency/hallucination):** G-Eval-4 AVG ρ=0.611, τ=0.525 — large margin over UniEval (ρ=0.575, τ=0.465) and BARTScore. G-Eval-3.5 *failed* on the abstractive QAGS-Xsum subset, indicating the consistency dimension is sensitive to LLM capacity ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)).

## Analysis

- **CoT helps.** G-Eval-4 with CoT outperforms the no-CoT variant on all SummEval dimensions (notably fluency) — CoT supplies context and guidance for the evaluation ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)). This is a different use of [[chain-of-thought|CoT]] than reasoning: here the model generates the evaluation *procedure*, not a problem-solving trace.
- **Probability normalization helps granularity.** On Spearman (rank-order) correlation, probability-weighted scores beat direct integer scoring; on Kendall-Tau the direct variant looks higher only because ties are uncounted — an artifact, not real ability ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)).
- **Model size matters.** G-Eval-4 > G-Eval-3.5 on most dimensions/datasets, especially harder ones (consistency, relevance) — larger models are better evaluators ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)).

## Bias toward LLM-generated text

A central concern raised by the authors ([Liu et al., 2023](raw/papers/2023-03-liu-geval/liu2023geval.md)): G-Eval-4 assigns *higher* scores to GPT-3.5-generated summaries than to human-written ones — even when human judges prefer the human-written summaries. Two hypothesized causes:

1. High-quality NLG outputs are genuinely hard to evaluate; inter-annotator agreement on human vs LLM summaries in the underlying study was extremely low (Krippendorff's α = 0.07).
2. The evaluator may share the same notion of "quality" it uses when *generating*, creating a self-preference bias.

If an LLM-based evaluator is used as the reward signal for further tuning, this bias can drive **self-reinforcement** — the model overfits to its own evaluation criteria rather than the true task criteria. This is a concrete instance of the proxy-overoptimization risk analysed in [[reward-model-overoptimization|Reward Model Overoptimization Scaling Laws]]: optimizing against an imperfect proxy (here, an LLM judge) eventually degrades true quality. The authors frame this as a preliminary finding requiring further study, not a definitive measurement.

## Relationship to LLM-as-a-Judge

G-Eval is an early, influential reference-free LLM-as-judge method. It predates and differs from later judge frameworks (e.g. MT-bench / Chatbot Arena by Zheng et al., 2023) in that it uses auto-generated CoT + probability-weighted scoring rather than single-shot pairwise or pointwise judging. Its bias finding foreshadows the broader "LLM judges prefer LLM outputs" literature.

## Related

- [[chain-of-thought|Chain-of-Thought Prompting (CoT)]] — G-Eval repurposes CoT to generate evaluation steps; CoT improves evaluator correlation, especially on fluency
- [[reward-model-overoptimization|Reward Model Overoptimization Scaling Laws]] — using LLM-evaluator scores as a reward signal risks the same Goodhart/self-reinforcement failure G-Eval's bias analysis warns about
- [[factscore|FActScore]] — another reference-free evaluation metric, targeting factual precision of long-form generation rather than general NLG quality
- [[chain-of-verification|Chain-of-Verification (CoVe)]] — related evaluation/verification line; contrasts with LLM-judge scoring
- [[llm-evaluator-positional-bias|Positional Bias in LLM-as-a-Judge]] — Wang et al. (2023) quantify the positional bias that also affects the pairwise/pointwise judge setups G-Eval uses
