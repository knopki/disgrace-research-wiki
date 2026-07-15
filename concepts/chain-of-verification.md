---
title: Chain-of-Verification (CoVe)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags: [hallucination, prompting, methodology, paper]
sources:
- "[Chain-of-Verification Reduces Hallucination in Large Language Models](raw/papers/2023-09-dhuliawala-cove/dhuliawala2023cove.md)"
confidence: high
---

# Chain-of-Verification (CoVe)

Chain-of-Verification (CoVe) is a prompting method that reduces factual
hallucination by making a language model deliberate on its own draft response and
self-correct it before emitting a final answer. The core idea: an LLM will often
answer a *single* verification question about one of its own claims more
accurately than it answered the original query that produced the (possibly wrong)
claim in the first place. CoVe was introduced by Dhuliawala et al. (Meta AI,
arXiv:2309.11495, 2023). ([Dhuliawala et al., 2023](raw/papers/2023-09-dhuliawala-cove/dhuliawala2023cove.md))

## The four-step pipeline

1. **Generate Baseline Response** — answer the query left-to-right as usual (this
   also serves as the baseline to beat).
2. **Plan Verifications** — conditioned on the query + baseline, generate a list
   of free-form verification questions that probe the factual claims in the draft
   (e.g. "When did the Mexican–American War start and end?").
3. **Execute Verifications** — answer each verification question.
4. **Generate Final Verified Response** — given any detected inconsistencies, emit
   a revised response that drops/keeps facts per the verification results.

All four steps are implemented by prompting the *same* base LLM; the model checks
its own work with no external tools. ([Dhuliawala et al., 2023](raw/papers/2023-09-dhuliawala-cove/dhuliawala2023cove.md))

## Execution variants (step 3)

The paper studies how much context the verification step is allowed to attend to:

- **Joint** — planning + answering in one prompt; answers condition on the
  baseline, which lets the model repeat its own hallucinations.
- **2-Step** — planning and execution are separate prompts; the execution prompt
  sees only the questions, not the baseline.
- **Factored** — each verification question is answered in its *own* independent
  prompt, neither seeing the baseline nor each other; questions can be batched and
  run in parallel (naming borrowed from concurrent Radhakrishnan et al., 2023).
- **Factor+Revise** — after answering, an extra prompt explicitly cross-checks
  each (question, answer) pair against the original fact and labels it
  CONSISTENT / INCONSISTENT / PARTIALLY CONSISTENT, feeding those labels into the
  final revision.

The central hypothesis: verification questions must *not* attend to the original
baseline response, or they will be prone to copying the same hallucination. The
factored/2-step variants consistently beat joint. ([Dhuliawala et al., 2023](raw/papers/2023-09-dhuliawala-cove/dhuliawala2023cove.md))

## Results

Evaluated on three task families (Llama-65B few-shot baseline):

| Task | Metric | Baseline | CoVe best | Δ |
|------|--------|----------|-----------|---|
| List-based (Wikidata) | precision | 0.17 | 0.36 | >2× |
| Closed-book (MultiSpanQA) | F1 | 0.39 | 0.48 | +23% |
| Longform biographies | FActScore | 55.9 | 71.4 | +28% |

Longform detail: Factored lifts FActScore 60.8→63.7; Factor+Revise adds the
explicit cross-check and reaches 71.4 (facts/response drops only 16.6→12.3). On
list tasks, negatives (hallucinated answers) fall 2.95→0.68 while positives drop
only 0.59→0.38. ([Dhuliawala et al., 2023](raw/papers/2023-09-dhuliawala-cove/dhuliawala2023cove.md))

**CoVe Llama-65B beats InstructGPT, ChatGPT, and PerplexityAI** on FActScore for
biographies, despite PerplexityAI being retrieval-augmented — though PerplexityAI
still wins on *very rare* facts where retrieval is essential. ([Dhuliawala et al., 2023](raw/papers/2023-09-dhuliawala-cove/dhuliawala2023cove.md))

### What helps and what doesn't

- **Shortform beats longform.** On Wikidata only ~17% of baseline answer entities
  are correct in the list, but when each entity is queried individually via a
  verification question ~70% are answered correctly — the model "knows" the fact
  when asked directly.
- **LLM-generated verification questions beat heuristics.** Replacing them with
  templated yes/no questions ("Does X answer the question?") lowers precision on
  the Wiki-Category task (0.13 rule-based → 0.22 for model-generated general
  questions, factored).
- **Open questions beat yes/no.** Asking for the true fact outperforms embedding
  the fact in a yes/no phrasing; ChatGPT tends to agree with a yes/no statement
  whether right or wrong.
- **Instruction-tuning and [[chain-of-thought|CoT]] do not help here.** The
  few-shot pre-trained Llama outperforms Llama-2-Chat across tasks, and standard
  CoT prompting fails to reduce the measured hallucination. ([Dhuliawala et al., 2023](raw/papers/2023-09-dhuliawala-cove/dhuliawala2023cove.md))

## Limitations

- Does **not** eliminate hallucination; only reduces directly stated factual
  inaccuracies (not reasoning errors or opinions).
- Adds computational cost (more generated tokens), like other deliberation
  methods.
- Upper bound set by the model's own capabilities ("knowing what it knows"); the
  obvious extension is equipping CoVe with tool-use / retrieval in step 3.
  ([Dhuliawala et al., 2023](raw/papers/2023-09-dhuliawala-cove/dhuliawala2023cove.md))

## Relation to other work

- **[[chain-of-thought|Chain-of-Thought]]** — CoVe is a deliberation method in the
  same lineage as CoT/self-critique, but the paper shows plain CoT does not reduce
  the targeted hallucination; the *verification* structure (independent
  fact-checking) is what helps.
- **[[factscore|FActScore]]** — the paper's longform experiments are measured with
  FActScore, and CoVe is one of the methods demonstrated to raise it substantially.
- **[[hallucination-llm-survey|Huang et al. hallucination survey]]** — classifies
  CoVe-style self-reflection as an inference-level mitigation strategy.
- **[[retrieval-augmented-generation|Retrieval-Augmented Generation]]** — CoVe uses
  only the base LLM; the authors flag retrieval-augmented verification as the
  natural next step.
- **[[self-consistency|Self-consistency]]** and **[[reflexion|Reflexion]]** — CoVe
  shares the self-checking spirit but, unlike Reflexion, stores no persistent
  memory and, unlike multi-agent self-consistency (Cohen et al. LM-vs-LM), uses a
  single model without debate.
