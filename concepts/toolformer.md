---
title: Toolformer
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - tool-use
  - fine-tuning
  - training
sources:
  - "[Toolformer: Language Models Can Teach Themselves to Use Tools](raw/papers/2023-02-schick-toolformer/schick2023toolformer.md)"
confidence: high
---

# Toolformer

A language model trained to **teach itself to use external tools** via simple text-based API calls, in a fully self-supervised way. Introduced by Schick et al. (Meta AI, 2023) on top of a 6.7B-parameter GPT-J base; Toolformer decides autonomously *which* API to call, *when*, *with what arguments*, and *how to fold the result* into future token prediction. It targets the gap where large LMs hallucinate facts, miscalculate, can't reach up-to-date information, or lack temporal awareness — while much smaller, task-specific systems handle those well.

## Method in five steps

The core pipeline augments a plain-text LM dataset `C` into `C*` containing useful API calls, then fine-tunes the LM on `C*`.

1. **Sampling.** For each API, a handful of human-written demonstrations seed an in-context prompt `P(x)`. The LM samples candidate call positions (where `p(<API> | ...)` exceeds a sampling threshold `τs`) and, per position, up to `m` candidate API calls `c_i` ([Schick et al., 2023](raw/papers/2023-02-schick-toolformer/schick2023toolformer.md)).
2. **Executing.** Each sampled call `c_i` is run against the real tool; every response must be a single text string `r_i`.
3. **Filtering.** An API call is kept only if adding it *and* its result reduces the weighted cross-entropy loss over future tokens by at least a filtering threshold `τf`: `L⁻_i − L⁺_i ≥ τf`, where `L⁺_i = L_i(e(c_i, r_i))` and `L⁻_i = min(L_i(ε), L_i(e(c_i, ε)))`. Calls that don't help predict future tokens are discarded — the model's own likelihood, not human judgement, decides usefulness.
4. **Fine-tuning.** Surviving calls are interleaved with the original text (`x* = x1:i−1, e(c_i, r_i), xi:n`) and the LM is fine-tuned on `C*` with a standard LM objective. Because `C*` contains the same texts as `C` (just with API calls inserted where they help), the model keeps its generality and core language-modelling ability.
5. **Inference.** During generation, after the LM emits `→` it is paused, the API is called, and the result + `</API>` are inserted before decoding resumes.

API calls are linearized with special tokens `<API> ac(ic) → r </API>` (implemented as `[`, `]`, `->` to avoid extending the vocabulary).

## Tools incorporated

Five tools, all with text-in/text-out interfaces and a few demonstrations each:

- **Question Answering** — Atlas, a retrieval-augmented LM fine-tuned on Natural Questions ([Schick et al., 2023](raw/papers/2023-02-schick-toolformer/schick2023toolformer.md)).
- **Calculator** — four basic arithmetic ops, results rounded to 2 decimals.
- **Wikipedia Search** — BM25 retriever over the KILT Wikipedia dump, returning short snippets.
- **Machine Translation** — NLLB (600M params), 200 languages → English, with fastText language detection.
- **Calendar** — returns the current date; gives temporal context.

## Key results (zero-shot)

Evaluated prompted zero-shot (no in-context task examples), contrasting with prior tool-use work that supplies task-specific demonstrations. Base model GPT-J (6.7B) vs much larger OPT-66B and GPT-3-175B.

| Task | Toolformer | GPT-J + CC | GPT-3 (175B) | Notes |
|------|:---:|:---:|:---:|------|
| LAMA (SQuAD / Google-RE / T-REx) | **33.8 / 11.5 / 53.5** | 19.2 / 5.6 / 22.1 | 26.8 / 7.0 / 39.8 | QA tool used for 98.1% of examples |
| Math (ASDiv / SVAMP / MAWPS) | **40.4 / 29.4 / 44.0** | 9.6 / 14.0 / 5.0 | 19.8 / 19.8 / 19.8 | Calculator used for 97.9% |
| QA (WebQS / NQ / TriviaQA) | 26.3 / 17.7 / 48.8 | 18.5 / 12.8 / 43.9 | **29.0 / 22.6 / 65.9** | Wikipedia Search (99.3%); still lags GPT-3 |
| Temporal (TEMPLAMA / DATESET) | **16.3 / 27.3** | 13.7 / 3.9 | 15.5 / 0.8 | Calendar used for 54.8% on DATESET |

Toolformer (disabled — API calls suppressed at decode time) still beats the GPT-J baseline on math (e.g. ASDiv 14.8 vs 9.6), suggesting fine-tuning on API-call examples also improves the model's intrinsic capability. On perplexity (WikiText 10.3, CCNet 10.5) Toolformer (disabled) matches GPT-J + CC, confirming **no degradation** of core language modelling.

## Scaling behaviour

Applying the method to GPT-2 family sizes (124M–1.6B) with three tools shows tool-use ability **emerges around 775M parameters**: smaller models gain nothing from API calls, while at 775M+ the gap between with-tool and without-tool performance stays large even as the model grows ([Schick et al., 2023](raw/papers/2023-02-schick-toolformer/schick2023toolformer.md)). This mirrors the broader pattern that tool-augmented behaviour, like other LM capabilities, is scale-dependent (see [[scaling-laws|Scaling Laws]]).

## Relationship to other approaches

- Prior tool-use methods either need large human annotation (e.g. BlenderBot, WebGPT, LaMDA) or are locked to task-specific few-shot prompts (e.g. PAL, ReAct-style). Toolformer's self-supervised filtering removes both constraints.
- Closest prior is **TALM** (Parisi et al., 2022) — same self-supervised objective for calculator + search, but only explored in downstream-task fine-tuning settings, not general zero-shot tool use.
- The sampling+finetune loop is a bootstrapping technique, related to self-training literature; the filter step is the distinguishing perplexity-based gate.
- The [[in-context-learning|in-context learning]] ability of the base LM is what makes the initial API-call sampling possible from only a few demonstrations.
- The QA and Wikipedia-Search tools are themselves retrieval systems (Atlas = RAG; BM25 over Wikipedia), connecting Toolformer to [[retrieval-augmented-generation|Retrieval-Augmented Generation]].

## Limitations

1. **No chained tool use** — calls for each tool are sampled independently, so the output of one tool can't feed another; at most one API call per example is allowed at inference.
2. **No interactive use** — the model can't reformulate a search query or browse multiple results; this is why it lags GPT-3 on open QA.
3. **Prompt sensitivity** — API-call decisions are sensitive to exact input wording, consistent with known LM prompt fragility.
4. **Sample inefficiency** — processing >1M CCNet documents yields only a few thousand useful calculator calls; iteration (like other bootstrapping methods) is a candidate fix.
5. **No cost awareness** — the decision to call an API ignores the tool's computational cost.

## Related concepts

- [[in-context-learning|In-Context Learning]] — the capability Toolformer exploits to bootstrap API calls from few demos
- [[retrieval-augmented-generation|Retrieval-Augmented Generation]] — the retrieval backbone behind Toolformer's QA and search tools
- [[scaling-laws|Scaling Laws]] — tool-use emergence threshold (~775M) is a scale-dependent phenomenon
- [[entities/gpt-3|GPT-3]] — the 175B baseline Toolformer frequently beats at 1/26th the size
