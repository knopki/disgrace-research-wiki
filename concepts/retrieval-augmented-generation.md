---
title: Retrieval-Augmented Generation (RAG)
created: 2026-06-16
updated: 2026-06-16
type: concept
tags:
  - architecture
  - technique
  - evaluation
  - data
sources:
  - "[Wikipedia: Генерация с дополненной выборкой](raw/articles/rag-wikipedia.md)"
confidence: high
---

# Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation (RAG)** — an architectural pattern where an LLM generates responses grounded in data retrieved from external knowledge sources (document corpora, databases, the web) at inference time, rather than relying solely on parametric memory.

RAG operates in two phases:
1. **Retrieval** — the user query is embedded and used to fetch the top-K relevant chunks from a vector database
2. **Generation** — the retrieved chunks are injected into the LLM's context alongside instructions on how to use them

The output may include citations or source links, improving transparency and verifiability.

## Why RAG Matters

The core insight: RAG decouples knowledge storage from model parameters. Instead of retraining or fine-tuning to inject new information, you just update the external knowledge base. This means the LLM's effective knowledge is bounded only by the external corpus, not by training cutoff dates or model size.

RAG addresses three fundamental LLM failure modes:
- **Staleness** — training data has a cutoff date; external sources can be current
- **Hallucination** — retrieval provides concrete facts, reducing reliance on statistical pattern completion
- **Opacity** — sources can be cited, enabling verification

## Paradigms

### Naive RAG
The simplest pipeline: Index → Retrieve → Generate. Three stages:
1. **Indexing** — clean and chunk source documents, embed each chunk, store in a vector DB
2. **Retrieval** — embed the query with the same model, find top-K nearest neighbours by cosine similarity or dot product
3. **Generation** — concatenate query + retrieved chunks into a prompt, let the LLM produce the answer

**Limitations:** low retrieval precision and recall, no query reformulation, no context compression — the model gets whatever came back, noise and all.

### Advanced RAG
Adds **pre-retrieval** and **post-retrieval** stages:

- **Pre-retrieval optimisation:**
  - Sliding window chunking, fine-grained segmentation
  - Metadata enrichment, hybrid search (BM25 + vector)
  - Query rewriting, transformation, expansion
- **Post-retrieval optimisation:**
  - Re-ranking retrieved chunks by relevance
  - Context compression — extract only the salient parts
  - Re-organising chunks for optimal prompt position

The premise: retrieval quality and context presentation are both first-class problems, not implementation details.

### Modular RAG
The most flexible paradigm — specialised modules orchestrated in different patterns:

| Module | Function |
|--------|----------|
| Search | Direct source lookup across data sources |
| Memory | LLM memory capabilities for contextualisation |
| Routing | Navigate between data sources per query |
| Predict | LLM-generated context used for retrieval |
| Task Adapter | Tune RAG for specific downstream tasks |

**Interaction patterns:**
- **Rewrite-Retrieve-Read** — rewrite query before retrieval
- **Generate-Read** — generate a hypothetical answer first, then retrieve evidence
- **Recite-Read** — extract specific facts, then search for supporting detail
- **HyDE** — generate a hypothetical document, embed it, and use its embedding for retrieval
- **Hybrid search** — combine semantic and lexical retrieval
- **Sub-queries** — decompose complex queries into simpler ones, merge results
- **FLARE / Self-RAG** — adaptive orchestration where the system decides *when* to retrieve during generation

## Evaluation

### Benchmarks
- **RGB, RECALL, CRUD** — basic RAG capability tests
- **RAGAS, ARES, TruLens** — automated LLM-based scoring frameworks

### Quality Dimensions

**Retrieval quality:**
- **Context relevance** — are the retrieved chunks on-topic?
- **Noise robustness** — can the model extract signal from irrelevant documents?

**Generation quality:**
- **Answer faithfulness** — does the output contradict the retrieved context?
- **Answer relevance** — is the answer directly addressing the question?
- **Negative rejection** — can the model decline to answer when information is insufficient?
- **Information integration** — can it synthesise from multiple documents?
- **Counterfactual robustness** — can it ignore deliberately false retrieved content?

Key finding from RGB benchmarks: at 80%+ noise ratio, accuracy drops significantly (ChatGPT: 96% → 76%, ChatGLM2-6B: 57%). Complex questions are more vulnerable to noise interference.

## Limitations

- **Retrieval quality** — bad retrieval produces bad answers; irrelevant documents can degrade output below no-RAG baselines
- **Latency** — extra retrieval step adds response time
- **Context window pressure** — retrieved chunks consume tokens, potentially crowding out the instruction or causing truncation
- **Inference cost** — larger prompts increase per-call cost, especially with paid APIs
- **Data dependency** — the system is only as good as its knowledge base (stale, biased, or poisoned sources propagate)
- **Security** — external sources are vulnerable to data poisoning and prompt injection
- **Knowledge density mismatch** — naive top-K retrieval can return redundant information, reducing effective coverage

## Commercial Implementations

**Perplexity AI** — search engine built on a multi-stage RAG pipeline: hybrid search (BM25 + vector), multi-step re-ranking, strict source adherence, infrastructure on Vespa AI.

## Related

- [[word-embeddings|Word Embeddings]] — RAG depends on embedding models for semantic search; the embedding quality directly determines retrieval precision
- [[distributional-semantics|Distributional Semantics]] — the theoretical foundation for why embedding-based retrieval works (meaning from context)
- [[grace|GRACE]] — the GRACE framework explicitly addresses RAG agent limitations with its dual-purpose semantic markup: hierarchical navigation, progressive context collection, and deterministic patching via stable semantic coordinates for RAG agents
- [[hallucination-detection-slm|SLM-based Hallucination Detection]] — uses RAG context as the basis for SLM-based answer verification; describes a concrete post-hoc verification pipeline for RAG responses
