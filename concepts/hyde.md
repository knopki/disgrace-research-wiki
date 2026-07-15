---
title: HyDE (Hypothetical Document Embeddings)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - information-retrieval
  - architecture
sources:
  - "[Precise Zero-Shot Dense Retrieval without Relevance Labels](raw/papers/2022-12-gao-hyde/gao2022hyde.md)"
confidence: high
---

# HyDE (Hypothetical Document Embeddings)

**HyDE** is a zero-shot dense retrieval method that pivots relevance modeling from the
retriever onto a generative instruction-following language model. Given a query, HyDE
instructs an LLM to write a *hypothetical* document answering the query, then encodes
that document with an unsupervised contrastive encoder (e.g. Contriever); the resulting
embedding is used for nearest-neighbour search over the corpus. Introduced by Gao et al.
(ACL 2023) from Carnegie Mellon University and the University of Waterloo.

## How it works

The core decomposition splits dense retrieval into two tasks:

1. **Generative step** — an instruction-following LM (e.g. InstructGPT / text-davinci-003)
   is prompted with a task-specific instruction such as *"write a passage to answer the
   question"*. The generated document is unreal and may contain factual errors, but it
   captures the *relevance pattern* of an answer.
2. **Contrastive encoding step** — an unsupervised contrastively trained encoder
   (Contriever for English, mContriever multilingual) maps the hypothetical document into
   an embedding. Its dense bottleneck acts as a lossy compressor: hallucinated details are
   filtered out, and the vector lands near real relevant documents in the corpus embedding
   space. Inner-product similarity does the retrieval.

Crucially, **no model is trained or fine-tuned** in HyDE. The only supervision involved is
the instruction-following capability already present in the backbone LLM. The query–document
similarity is never explicitly modeled — retrieval is cast into NLU (encoding) + NLG
(generation) tasks.

Formally, with instruction LM `g(q, INST)` and document encoder `f`:

```
v_q ≈ (1/N) · Σ_k f(g(q, INST)_k)
```

estimated by sampling N documents (temperature 0.7 in the paper). Optionally the raw query
is folded in: `v_q = (1/(N+1)) · [Σ_k f(d̂_k) + f(q)]`.

## Results

Evaluated on 11 query sets spanning web search, QA, fact verification, and low-resource
languages. Backbone: InstructGPT (175B) + Contriever/mContriever.

- **Web search (TREC DL19/20), nDCG@10:** Contriever 44.5 / 42.1 → **HyDE 61.3 / 57.9**;
  BM25 50.6 / 48.0. HyDE beats BM25 and is competitive with fine-tuned ContrieverFT
  (62.1 / 63.2) and transferred DPR / ANCE.
- **Low-resource BEIR (SciFact, Arguana, TREC-COVID, FiQA, DBPedia, TREC-NEWS):** HyDE
  improves Contriever across the board on nDCG@10. Only on TREC-COVID does BM25 edge it out
  (59.5 vs 59.3, a 0.2 margin), whereas Contriever underperforms BM25 there by >50%.
- **Multilingual (Mr.Tydi: Swahili, Korean, Japanese, Bengali), MRR@100:** mContriever
  38.3 / 22.3 / 19.5 / 35.3 → **HyDE 41.7 / 30.6 / 30.7 / 41.3**. Outperforms mDPR, mBERT,
  and XLM-R (all fine-tuned on MS-MARCO), but trails fine-tuned mContrieverFT.
- **Generative-model scaling (analysis):** larger instruction LMs give larger gains —
  FLAN-T5-11B 48.9 / 52.9, Cohere-52B 53.8 / 53.8, GPT-175B 61.3 / 57.9 nDCG@10 on DL19/20.

## Comparison to concurrent work

Asai et al. (2022), *Task-aware Retrieval with Instructions*, fine-tunes dense encoders that
encode a task-specific instruction prepended to the query. HyDE instead keeps an unsupervised
encoder fixed and handles task variation through the instruction-following generative LM.

## Limitations & open questions

- **Multilingual gap** — HyDE still lags fine-tuned mContrieverFT on non-English; the small
  contrastive encoder saturates as languages scale, and the generative LM is under-trained on
  low-resource languages.
- **Smaller generative LMs can hurt** — weak instruction models can slightly degrade an
  otherwise fine-tuned retriever (HyDE-with-fine-tuned-encoder is *not* the intended use).
- The authors pose a philosophical question left open: *is numerical relevance just a
  statistical artifact of language understanding?* — i.e. as NLU/NLG models strengthen, might
  a relevance-free retriever suffice?

## Relationship to RAG

HyDE is one of the advanced **Generate-Read** interaction patterns in [[retrieval-augmented-generation|RAG]]:
generate a hypothetical answer first, then retrieve evidence grounded in it. It pairs naturally
with [[bm25|BM25]] as a lexical baseline and with dense embedding methods (see
[[word-embeddings|Word Embeddings]]) for the similarity search.

## Related

- [[retrieval-augmented-generation|Retrieval-Augmented Generation (RAG)]] — HyDE is a Generate-Read retrieval pattern feeding RAG pipelines
- [[bm25|BM25]] — classical lexical retriever used as the baseline HyDE is compared against
- [[word-embeddings|Word Embeddings]] — the dense embedding space HyDE searches over
