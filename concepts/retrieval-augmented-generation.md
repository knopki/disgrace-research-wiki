---
title: Retrieval-Augmented Generation (RAG)
created: 2026-06-16
updated: 2026-06-17
type: concept
tags:
  - architecture
  - technique
  - evaluation
  - data
sources:
  - "[Wikipedia: Генерация с дополненной выборкой](raw/articles/rag-wikipedia.md)"
  - "[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](raw/papers/2020-05-lewis-rag/lewis2020rag.md)"
confidence: high
---

# Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation (RAG)** — an architectural pattern where an LLM generates responses grounded in data retrieved from external knowledge sources (document corpora, databases, the web) at inference time, rather than relying solely on parametric memory.

## Original Paper: Lewis et al. (NeurIPS 2020)

The RAG framework was introduced by Patrick Lewis et al. at Facebook AI Research in their 2020 NeurIPS paper *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. The core idea: combine a pre-trained parametric memory (a seq2seq model) with a non-parametric memory (a dense vector index of Wikipedia accessed via a neural retriever) — and fine-tune the whole system end-to-end. ([Lewis et al., 2020](raw/papers/2020-05-lewis-rag/lewis2020rag.md))

### Architecture

Two components:

- **Retriever** `p_η(z|x)` — Dense Passage Retriever (DPR) bi-encoder built on BERTBASE. The query encoder `BERTq` is fine-tuned during training; the document encoder `BERTd` and document index are kept fixed. Retrieval is a Maximum Inner Product Search (MIPS) over 21M 100-word Wikipedia chunks using FAISS with HNSW approximation.
- **Generator** `p_θ(y_i|x, z, y_{1:i-1})` — BART-large (400M parameters). Input = concatenation of query `x` and retrieved passage `z`.

### Two Formulations

The retrieved document `z` is treated as a latent variable. Lewis et al. propose two marginalisation strategies:

1. **RAG-Sequence** — a single retrieved document is used for the entire output sequence. The probability is marginalised over top-K documents before generation: `p(y|x) ≈ Σ_{z∈top-k} p_η(z|x) · p_θ(y|x, z)`. Decoding requires either "Thorough" (beam search per document + re-forwarding) or "Fast" approximation.

2. **RAG-Token** — a different document can be used per token. Marginalisation happens at each decoding step: `p(y|x) ≈ ∏_i Σ_{z∈top-k} p_η(z|x) · p_θ(y_i|x, z, y_{1:i-1})`. Decodes with standard beam search using a marginalised per-token transition probability.

For sequence classification (length-1 target), both formulations are equivalent.

### Key Results

- **Open-domain QA:** SOTA on Natural Questions (44.5 EM, RAG-Seq), WebQuestions (45.5 EM, RAG-Token), CuratedTrec (52.2 EM, RAG-Seq). RAG generates correct answers even when the answer is not present in any retrieved document (11.8% of NQ cases).
- **Abstractive QA (MS-MARCO NLG):** RAG-Seq achieves 44.2 Rouge-L without gold passages, approaching task-specific systems that use them.
- **Jeopardy question generation:** RAG generates more factual (42.7% vs 7.1% in human eval) and more specific (37.4% vs 16.8%) responses than BART baseline.
- **Fact verification (FEVER):** 72.5% 3-way accuracy without any retrieval supervision, within 4.3% of pipeline models with strong retrieval supervision.
- **Knowledge hot-swapping:** non-parametric memory can be replaced to update world knowledge without retraining.

### Retrieval Collapse

On tasks with less explicit knowledge requirements (e.g., story generation), the retriever would "collapse" — learning to retrieve the same documents regardless of input. The generator would then learn to ignore them, making RAG equivalent to BART. This was attributed to less informative gradients for the retriever on tasks with longer target sequences or weaker factual grounding. ([Lewis et al., 2020](raw/papers/2020-05-lewis-rag/lewis2020rag.md))

### Legacy

The RAG paper established the hybrid parametric/non-parametric paradigm for seq2seq models. It demonstrated that models with far fewer trainable parameters (626M vs T5-11B's 11B) could match or exceed purely parametric approaches on knowledge-intensive tasks. The work was open-sourced in HuggingFace Transformers, becoming the foundation for the modern RAG ecosystem described below.

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
- [[mamba|Mamba / SSM]] — Mamba's constant-memory state (~24 MB vs GB-scale KV cache) makes it the ideal companion for iterative RAG loops; the article reframes RAG from context augmentation to external "oracle" that compensates for Mamba's hallucination tendency via belief state overwriting
- **Dense Passage Retrieval (DPR)** — the retriever component used in the original RAG paper (Karpukhin et al., 2020)
- [[matryoshka-representation-learning|Matryoshka Representation Learning (MRL)]] — training technique for multi-granularity embeddings enabling adaptive retrieval with up to 14× speedup via low-dim shortlisting + high-dim reranking; directly applicable to improving RAG retrieval efficiency
- **BART** — the seq2seq generator component used in the original RAG paper (Lewis et al., 2019)
- [[bm25|BM25]] — lexical retrieval baseline compared against DPR in the RAG experiments
- [[bert|BERT]] — the encoder architecture underlying DPR's bi-encoder retriever
- [[hallucination-llm-survey|Hallucination in LLMs (Huang et al.)]] — analyses two RAG bottleneck classes (retrieval failure, generation bottleneck) as sources of residual hallucination; surveys RAG limitations beyond the faithfulness gains listed above
