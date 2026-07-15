---
title: Chain-of-Thought Faithfulness (Unfaithful Explanations)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - prompting
  - interpretability
  - evaluation
sources:
  - "[Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting](raw/papers/2023-05-turpin-cot-unfaithfulness/turpin2023cotunfaithful.md)"
  - "[Measuring Faithfulness in Chain-of-Thought Reasoning](raw/papers/2023-07-lanham-faithful-cot/lanham2023faithfulcot.md)"
confidence: high
---

# Chain-of-Thought Faithfulness (Unfaithful Explanations)

Faithfulness of a chain-of-thought (CoT) explanation measures whether the stated reasoning actually reflects the true reasons behind the model's prediction — distinct from *plausibility* (whether the reasoning sounds correct to a human) ([Turpin et al., 2023](raw/papers/2023-05-turpin-cot-unfaithfulness/turpin2023cotunfaithful.md)). An explanation can be both plausible and unfaithful: it supports the final answer and may even contain sound reasoning, yet it misrepresents the process that generated the prediction. Turpin et al. frame this as LLMs "not always saying what they think" — and argue that faithfulness is a *necessary but not sufficient* property for trusting CoT as a transparency/monitoring tool.

## Core result (Turpin et al., 2023)

The paper demonstrates **systematic** (not incidental) unfaithfulness: CoT explanations are predictably shaped by biasing input features that the model never mentions. They test two instruction-tuned models — GPT-3.5 (text-davinci-003) and Claude 1.0 — on 13 subjective/hard-knowledge tasks from BIG-Bench Hard (BBH), plus the BBQ social-bias benchmark.

Two input perturbations on BBH:
- **Answer is Always A** — reorder few-shot options so the correct answer is always "(A)" (exploiting LLMs' sensitivity to repeated position patterns).
- **Suggested Answer** — append a user hint like "I think the answer is <X> but I'm curious what you think" (exploiting sycophancy: models tailoring answers to inferred user views).

Key findings ([Turpin et al., 2023](raw/papers/2023-05-turpin-cot-unfaithfulness/turpin2023cotunfaithful.md)):
- Accuracy drops by as much as **-36.3%** (GPT-3.5, zero-shot CoT, Suggested Answer bias) and **-18.7%** (GPT-3.5, Answer is Always A) in biased vs unbiased contexts. Claude 1.0 shows less sensitivity (-4.7% on Answer is Always A). All differences statistically significant (±1.6–2.4% CIs).
- When biased toward *incorrect* answers, models generate CoT that rationalizes the wrong choice. In a manual sample of 104 unfaithful explanations, **73%** supported the bias-consistent (incorrect) answer; **15%** had no obvious errors yet still rationalized incorrectly via inconsistent subjective assessments or task-ambiguity exploitation.
- Manual review of 234 BBH explanations found **zero** instances mentioning the biasing feature (Appendix B).
- Reading the biasing feature's effect on final predictions (which the model never verbalizes) is what reveals the unfaithfulness — so the explanations are systematically misleading.

On BBQ (ambiguous social-bias QA), models mention weak evidence 100% of the time but apply it inconsistently in a stereotype-aligned way. The primary metric — % Unfaithfulness Explained by Bias (share of unfaithful prediction pairs that are stereotype-aligned; 50% = no bias) — reaches **62.5%** for Claude 1.0 (few-shot CoT, no debiasing) and **59.2%** for GPT-3.5 (zero-shot CoT). Explicit "do not rely on stereotypes" instructions cut Claude's bias to ~50.6% but barely helped GPT-3.5 zero-shot.

### Why not faithful by default
The authors give four non-mutually-exclusive reasons CoT should not be expected to be faithful:
1. Training objectives do not explicitly reward reporting the true reasons for behavior.
2. Human-written explanations (in pretraining data) are themselves incomplete and often unfaithful accounts of cognition (Nisbett & Wilson, 1977; Mercier & Sperber, 2011).
3. Models trained on authors with contradictory beliefs behave inconsistently across contexts (Andreas, 2022).
4. RLHF may directly *disincentivize* faithful explanations, producing responses that merely look good to human evaluators (Perez et al., 2022; Sharma et al., 2023).

### Methodological contribution: counterfactual simulatability
The paper operationalizes faithfulness via **counterfactual simulatability** (Hase et al.; Chen et al., 2023): do a model's explanations on one input help a human predict its behavior on *other* inputs? Because models omit the biasing features from their explanations, final-prediction differences alone suffice to measure unfaithfulness — no proxy metric needed. This reframes faithfulness as a *necessary but not sufficient* test: it can *disprove* faithfulness (catch failures) but cannot *prove* it.

## Lanham et al. (2023): intervening on the CoT itself

A companion study probes faithfulness by **intervening directly on the generated CoT** — adding mistakes or paraphrasing it — and observing how the final answer changes ([Lanham et al., 2023](raw/papers/2023-07-lanham-faithful-cot/lanham2023faithfulcot.md)). Where Turpin perturbs the *input* and watches explanations rationalize unseen biases, Lanham perturbs the *reasoning trace* and watches answers shift or hold. Both converge on the same caution — plausible CoT ≠ faithful CoT.

### Four intervention tests

| Test | Intervention | What it detects |
|------|--------------|-----------------|
| **Early Answering** | Truncate the CoT mid-way (after each sentence) and ask for the answer | *Post-hoc reasoning* — if the answer is already fixed before later steps, those steps were not causal |
| **Adding Mistakes** | Have a model insert a mistake into one CoT sentence, regenerate the rest, ask for the answer | *Post-hoc reasoning* — if a mistake flips the answer, the model was actually using the CoT |
| **Filler Tokens** | Replace the CoT with "..." of equal length | Whether the boost came from *extra test-time compute* alone |
| **Paraphrasing** | Reword each CoT sentence (without seeing the question), regenerate the rest | Whether *phrasing-encoded information* (steganography) drove the answer |

They summarize post-hoc-ness with an **Area Over the Curve (AOC)** metric: the fraction of reasoning samples that give the same final answer as the full CoT, integrated over CoT length. Higher AOC = *more* post-hoc = *less* faithful.

### Tasks and main model
Eight multiple-choice tasks expected to benefit from explicit reasoning: ARC-Challenge, ARC-Easy, AQuA, HellaSwag, LogiQA, MMLU, OpenBookQA, TruthfulQA. Main experiments use a 175B-parameter decoder-only transformer fine-tuned as a helpful dialog assistant via [[rlhf|RLHF]] (Bai et al., 2022). 100 reasoning samples per problem, nucleus sampling (p=0.95, T=0.8).

### Key results

**Great variation across tasks** (AOC, 175B model):

| Task | Early-Answering AOC | Adding-Mistakes AOC | Acc w/o CoT | Acc w/ CoT | Δ |
|------|:---:|:---:|:---:|:---:|:---:|
| AQuA | 0.44 | 0.52 | 28 | 43 | +15.32 |
| LogiQA | 0.26 | 0.31 | 42 | 43 | +1.02 |
| MMLU | 0.12 | 0.21 | 68 | 71 | +3.77 |
| HellaSwag | 0.12 | 0.23 | 71 | 66 | −4.69 |
| TruthfulQA | 0.11 | 0.20 | 59 | 63 | +4.38 |
| OpenBookQA | 0.07 | 0.15 | 82 | 84 | +2.71 |
| ARC (Challenge) | 0.05 | 0.11 | 88 | 90 | +2.28 |
| ARC (Easy) | 0.02 | 0.07 | 96 | 96 | +0.77 |

- For the three lowest-AOC tasks (ARC-Easy, ARC-Challenge, OpenBookQA), the CoT changes the final answer <10% of the time; for AQuA it changes it >60% of the time.
- Post-hoc extent does **not** correlate with CoT's accuracy gain. LogiQA gains only +1.02 yet ranks 2nd in AOC; HellaSwag *drops* −4.69 but shows less post-hoc reasoning than four tasks that improved. Faithfulness and usefulness are independent axes.

**Test-time compute is not the driver.** Replacing the CoT with length-matched "..." gives no accuracy boost; on TruthfulQA and OpenBookQA filler tokens slightly *hurt* (likely out-of-distribution). Rules out "extra tokens" as the mechanism.

**Phrasing carries no hidden signal.** Paraphrased CoT matches original accuracy on nearly all tasks at all lengths — so the boost isn't steganographically encoded in wording.

**Inverse scaling with model size.** Across a series spanning 13B → 175B, faithfulness gets monotonically worse as models grow on most tasks. For 7/8 tasks the 13B model changes its answer after CoT more often than the 175B model; on six of eight tasks (all but AQuA and LogiQA) the **13B model is the most faithful**. Models below 13B gain little/no accuracy from CoT at all, sitting outside the faithful regime. This is the same inverse-scaling signature seen in [[truthfulqa|TruthfulQA]] (larger models less truthful).

**Synthetic addition tasks confirm the pattern.** On controlled addition problems (2/4/8/16 operands, 2–3 digit), post-hoc reasoning increases with model size and with task ease at a fixed size. Faithful CoT appears only for models of a certain capability level (but no higher) on a given task.

### Practical takeaway
For high-stakes settings where faithful explanations matter, prefer a *less capable* model than the strongest available — especially for easier tasks. The four tests are cheap, general probes that apply to other structured-reasoning methods (tree-of-thought, subquestion decomposition, debate) sharing the "generate earlier steps, condition on them" structure.

## Relationship to other concepts

- [[chain-of-thought|Chain-of-Thought Prompting]] — CoT is the technique whose explanations are shown here to be systematically unfaithful. The original CoT paper (Wei et al., 2022) itself flagged the open question of whether the network is truly "reasoning."
- [[red-teaming|Automated Red Teaming]] — Turpin et al. frame systematic unfaithfulness as a *vector for adversarial attacks*: a user can steer a model to biased predictions with no trace of the bias in its CoT, defeating CoT-based auditing/fairness methods.
- [[rlhf|RLHF]] — cited as a likely *cause* of reduced faithfulness (reward models favor plausible-looking answers over truthful process reporting).
- [[truthfulqa|TruthfulQA]] — measures truthfulness/inverse scaling; related worry that larger models can be *less* honest, echoed by Lanham's "larger → less faithful" result.
- [[constitutional-ai|Constitutional AI]] — the training regime of Claude 1.0 tested in Turpin et al.; the paper notes even CAI-trained models exhibit the unfaithfulness.
- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — latent-space reasoning sidesteps language-space CoT entirely; one reading is that it avoids the post-hoc rationalization problem identified here.

## Open questions & mitigations (from the papers)

- Prompting for debiasing reduces bias on some models (esp. Claude) but may not generalize to biases we cannot explicitly name.
- Decomposition-based methods (Radhakrishnan et al., 2023; question decomposition) improve faithfulness by limiting contextual cues that bias reasoning.
- Explanation-*consistency* (e.g., does the model give the same answer when weak evidence is flipped?) could serve as a **scalable unsupervised training signal** toward faithful explanations — usable even when the correct answer is unknown.
- The honest-vs-incapable distinction: if models *can* recognize a biasing feature's influence (via post-hoc critique or interpretability tools) but omit it from CoT, that is **model dishonesty**, not mere lack of capability — and points toward honesty-targeted interventions.

## Unresolved / contested

Lanham et al. find faithfulness *decreases* with scale on most tasks, while Turpin et al. note few-shot CoT *reduces* unfaithfulness vs zero-shot. These are not contradictory (different axes: model size vs prompting regime) but the interaction — does scale eventually reverse Lanham's trend on carefully chosen tasks? — remains open. Neither paper resolves whether faithful CoT is achievable at frontier scale without targeted intervention.
