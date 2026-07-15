---
title: Lost in the Middle
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - evaluation
  - methodology
  - technique
  - benchmark
sources:
  - "[Lost in the Middle: How Language Models Use Long Contexts](raw/papers/2023-07-liu-lost-in-the-middle/liu2023lostinthemiddle.md)"
confidence: high
---

# Lost in the Middle

**Lost in the Middle** is the empirical finding that language models use information in their input context non-uniformly: performance is highest when the relevant information sits at the very **beginning** (primacy bias) or **end** (recency bias) of the context, and degrades sharply when it lands in the **middle** — producing a characteristic **U-shaped performance curve** as a function of the position of the relevant information. Demonstrated by [[liu2023lostinthemiddle|Liu et al. (2023)]] across open (MPT-30B-Instruct, LongChat-13B-16K) and closed (GPT-3.5-Turbo, Claude-1.3) models, including explicitly long-context variants.

## Two Controlled Tasks

The paper studies position-robustness via two tasks where exactly one piece of information in the context is relevant:

- **Multi-document question answering** — a question plus `k` Wikipedia passages (exactly one contains the answer, `k−1` are distractors retrieved by Contriever). The relevant passage is moved to position 1…k to vary its location. Built on NaturalQuestions-Open (2,655 paragraph-answer queries).
- **Key-value retrieval** — a JSON object of `k` unique 128-bit UUID key-value pairs; the model must return the value for a given key. Strips away natural-language semantics (using random UUIDs) to isolate raw retrieval from the context.

For both, accuracy = whether the correct answer/value appears in the output.

## Key Results

- **U-shaped curve is robust.** Across models and both tasks, accuracy is best at the first and last positions and worst in the middle. On 20- and 30-document multi-doc QA, GPT-3.5-Turbo's worst-case performance drops *below its closed-book performance* (56.1%) — i.e., adding distractor documents in the middle actively hurts vs. no context at all.
- **Extended-context ≠ better context use.** When a context fits in both a base and an extended-context model (e.g., GPT-3.5-Turbo 4K vs 16K), their position-performance curves are nearly superimposed. A bigger window does not mechanically fix position bias.
- **Claude-1.3 / Claude-1.3-100K are near-perfect** on the synthetic key-value task at all evaluated lengths (75/140/300 pairs); other models struggle, especially at 140+ pairs, with the same middle degradation.
- **Absolute numbers (closed-book / oracle, multi-doc QA):** MPT-30B-Instruct 31.5% / 81.9%; GPT-3.5-Turbo 56.1% / 88.3%; Claude-1.3 48.3% / 76.1%.

## Why It Happens (Preliminary Investigation)

- **Architecture (§4.1):** Encoder-decoder models (Flan-T5-XXL, Flan-UL2) are relatively position-robust *within their training-time sequence length* (Flan-UL2: 1.9% gap between best/worst case inside 2048 tokens). Beyond that length they too show the U-shape. Hypothesis: the bidirectional encoder lets each document be processed in the context of future documents, improving relative-importance estimation.
- **Query-aware contextualization (§4.2):** Placing the query both before and after the data gives *near-perfect* key-value retrieval for all models (GPT-3.5-Turbo-16K hits 100% at 300 pairs vs 45.6% worst-case without it). But it barely changes multi-doc QA trends — slightly better at the start, slightly worse elsewhere.
- **Instruction fine-tuning (§4.3):** Base models (MPT-30B) already show the U-shape, so SFT is not the root cause. SFT slightly *reduces* the worst-case gap (≈10% → ≈4%) in smaller models but barely affects 70B. Scale matters more: in Llama-2, 7B is purely recency-biased, while 13B/70B show the full U-shape (with or without SFT/RLHF).

## "Is More Context Always Better?" (§5, Open-Domain QA Case Study)

In a retriever-reader setup on NaturalQuestions-Open, reader accuracy **saturates long before retriever recall**. Going from 20 to 50 retrieved documents improves performance only marginally (~1.5% GPT-3.5-Turbo, ~1% Claude-1.3) while substantially increasing context length, latency, and cost. Practical implication: effective **re-ranking** (pushing the relevant passage toward the start) or **ranked-list truncation** (retrieving fewer docs) may help readers more than dumping in more context.

## Connection to Human Memory

The U-shape mirrors the **serial-position effect** in psychology (Ebbinghaus, 1913; Murdock, 1962): humans best recall the first and last items in a list. Surprising in LLMs, since self-attention is in principle equally capable of attending to any token.

## Evaluation Protocol Contribution

To claim a model "robustly uses long context," the paper argues it must show **minimal difference between best- and worst-case performance** as the relevant information's position varies. This became a standard protocol for long-context evaluation (later adopted/extended by benchmarks such as HELMET).

## Relevance to This Wiki

- A central limitation of [[retrieval-augmented-generation|RAG]]: naive top-K retrieval that places the answer mid-context can degrade output below the closed-book baseline — argues for re-ranking and context-position management, exactly what advanced-RAG post-retrieval stages target.
- A boundary condition on [[in-context-learning|in-context learning]]: the model can attend to a demonstration/fact in principle, but its *effective* use depends on where that content sits in the prompt.

## Open Questions

- Whether the bias is best understood as a learned Softmax artifact, positional-encoding distance decay (e.g., [[rotary-position-embedding|RoPE]] — see also [[yarn|YaRN]] for extending RoPE windows), or a deeper architectural property of causal decoders — later theoretical work (2024–2026) derives the U-shape from the causal residual structure even at initialization.
- Mitigations beyond query-aware placement and re-ranking (modified positional encodings, training objectives, architectural changes).

## References

- [[liu2023lostinthemiddle|Liu et al., 2023]] — primary source (TACL 2023, arXiv:2307.03172)
