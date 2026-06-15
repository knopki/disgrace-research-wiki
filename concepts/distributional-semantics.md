---
title: Distributional Semantics
created: 2026-06-16
updated: 2026-06-17
type: concept
tags: [methodology]
sources:
  - "[Вектора GPT или почему для GPT ваше слово — пустота без контекста](raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md)"
  - "[Дистрибутивная семантика (Wikipedia)](raw/articles/distributional-semantics-wikipedia/index.md)"
confidence: high
---

# Distributional Semantics

The linguistic theory that a word's meaning is entirely determined by the contexts in which it appears — an isolated word carries no intrinsic meaning. Formally articulated by John Rupert Firth in 1957: *"You shall know a word by the company it keeps."*

Firth's position was considered heretical against traditional linguistics (rooted in Plato's essentialist view of language) in the 1950s. Modern LLMs — with their vector-based representation of word meaning — have validated his theory at industrial scale. ([Ivanov, 2025](raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md))

## Core Principle

A word in isolation has near-zero semantic content. Its meaning crystallises only through combinatorial patterns with surrounding words:

> "Строительный рабочий" → profession, physical labour
> "Рабочий момент" → business process, organisational question

The same word `рабочий` maps to entirely different semantic territories depending on its neighbours. Traditional dictionaries define words in isolation — Firth's thesis denies that such a definition is even possible. ([Ivanov, 2025](raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md))

## Historical Roots

Distributional semantics has deeper roots than Firth:

- **1920s:** Leonard Bloomfield proposed **distributional analysis** — a method studying the environment (distribution) of linguistic units without relying on lexical or grammatical meaning. Applied mainly in phonology and morphology.
- **1930–1950s:** Zellig Harris and the American descriptivist school developed the method further. Similar ideas were advanced by Ferdinand de Saussure and Ludwig Wittgenstein.
- **1950s:** Charles Osgood introduced **context vectors** in psycholinguistics, using antonymic adjective pairs (e.g. *fast-slow*) rated on 7-point scales as vector dimensions.
- **1960s:** S. Gallant formalised the term **context vector** for word sense disambiguation, using hand-picked features (e.g. *human*, *male*, *machine*).
- **2000s:** Word2vec and subsequent embedding methods turned the theoretical principle into a working algorithm.
- **2020s:** GPT-scale models validate the thesis at a level Firth could not have imagined.

([Wikipedia](raw/articles/distributional-semantics-wikipedia/index.md))

## The Distributional Hypothesis

The formal hypothesis: linguistic units that appear in similar contexts have similar meanings. Psychological experiments have confirmed a positive correlation between semantic similarity of words and similarity of their contexts. ([Wikipedia](raw/articles/distributional-semantics-wikipedia/index.md))

## Mathematical Model

Distributional semantics uses **vector spaces** from linear algebra:

- Each word is assigned a **context vector**
- **Dimensions** correspond to contexts (neighbouring words, documents, etc.)
- **Coordinates** are counts of how often the word appears in each context
- **Context window size** depends on the type of relationship being studied: 1-2 words for syntagmatic, 5-10 for paradigmatic, 50+ for thematic.

Semantic distance is most commonly measured via **cosine similarity**:

$cos(A,B) = \frac{\sum_{i=1}^{n} A_i \times B_i}{\sqrt{\sum_{i=1}^{n} (A_i)^2} \times \sqrt{\sum_{i=1}^{n} (B_i)^2}}$

([Wikipedia](raw/articles/distributional-semantics-wikipedia/index.md))

## Predictive Models

Traditional **count models** (LSA, HAL) build large sparse matrices then apply dimensionality reduction (SVD, PCA). **Predictive models** use neural networks to learn dense vectors of a few hundred dimensions directly:

- **Continuous Bag-of-Words (CBOW):** predict the word from its context
- **Continuous Skipgram:** predict the context from the word
- Both first implemented in **word2vec** (2013)

Predictive models represent semantics more accurately than count models and have spawned tools like **Gensim**, **RusVectōrēs** (for Russian), and **WebVectors**. ([Wikipedia](raw/articles/distributional-semantics-wikipedia/index.md))

## Connection to LLMs

GPT and similar models operationalise distributional semantics through vector embeddings:

- Every word/token is mapped to a point in high-dimensional space (10k–14k dimensions for production models)
- The vector does not encode explicit features — it is a compressed archive of correlations with every other token in the training corpus
- Meaning is **emergent**: it arises from the model's analysis of billions of contexts during training, not from any pre-assigned definition

The equivalence of model performance across languages — despite radically different tokenisation (English `[worker]` vs Russian `[Раб][оч][ий]`) — proves that individual tokens carry no Platonic essence. ([Ivanov, 2025](raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md))

## Applications

Distributional models are used for: semantic similarity detection, automatic thesaurus generation, word sense disambiguation, query expansion, document clustering, information extraction, sentiment analysis, machine translation, and semantic mapping of knowledge domains. ([Wikipedia](raw/articles/distributional-semantics-wikipedia/index.md))

## Practical Implications for Prompt Engineering

Stop treating individual words as carrying sacred meaning. Every word is a pointer whose value is determined entirely by its combinatorial context. Skill in prompting is skill in weaving contextual vectors, not in selecting "perfect" words.

## Related

- [[word-embeddings|Word Embeddings]] — the mathematical realisation of distributional semantics in LLMs
- [[superposition]] — why embedding spaces need high dimensionality to avoid feature collapse
- [[semantic-interference|Semantic Interference]] — what happens when context vectors compete destructively
- [[corpus-linguistics|Corpus Linguistics]] — the field that builds and annotates text corpora from which distributional models are trained
- [[vladimir-ivanov|Vladimir Ivanov]] — author who connected distributional semantics to modern LLM embeddings