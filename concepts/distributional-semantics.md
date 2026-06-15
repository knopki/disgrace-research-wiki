---
title: Distributional Semantics
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [methodology]
sources:
  - "[Вектора GPT или почему для GPT ваше слово — пустота без контекста](raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md)"
confidence: high
---

# Distributional Semantics

The linguistic theory that a word's meaning is entirely determined by the contexts in which it appears — an isolated word carries no intrinsic meaning. Formally articulated by John Rupert Firth in 1957: *"You shall know a word by the company it keeps."*

Firth's position was considered heretical against traditional linguistics (rooted in Plato's essentialist view of language) in the 1950s. Modern LLMs — with their vector-based representation of word meaning — have validated his theory at industrial scale. ^[raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md]

## Core Principle

A word in isolation has near-zero semantic content. Its meaning crystallises only through combinatorial patterns with surrounding words:

> "Строительный рабочий" → profession, physical labour
> "Рабочий момент" → business process, organisational question

The same word `рабочий` maps to entirely different semantic territories depending on its neighbours. Traditional dictionaries define words in isolation — Firth's thesis denies that such a definition is even possible. ^[raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md]

## Connection to LLMs

GPT and similar models operationalise distributional semantics through vector embeddings:

- Every word/token is mapped to a point in high-dimensional space (10k–14k dimensions for production models)
- The vector does not encode explicit features — it is a compressed archive of correlations with every other token in the training corpus
- Meaning is **emergent**: it arises from the model's analysis of billions of contexts during training, not from any pre-assigned definition

The equivalence of model performance across languages — despite radically different tokenisation (English `[worker]` vs Russian `[Раб][оч][ий]`) — proves that individual tokens carry no Platonic essence. ^[raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md]

## Historical Context

- **1957:** Firth publishes the principle. Dismissed by traditional linguists as reductionist.
- **1960s:** Corpus linguistics (including work by Soviet academic Andrey Ershov) provides statistical evidence that words form stable co-occurrence patterns.
- **2000s:** Word2vec and subsequent embedding methods turn the theoretical principle into a working algorithm.
- **2020s:** GPT-scale models validate the thesis at a level Firth could not have imagined.

## Practical Implications

For prompt engineering: stop treating individual words as carrying sacred meaning. Every word is a pointer whose value is determined entirely by its combinatorial context. Skill in prompting is skill in weaving contextual vectors, not in selecting "perfect" words.

## Related

- [[word-embeddings|Word Embeddings]] — the mathematical realisation of distributional semantics in LLMs
- [[vladimir-ivanov|Vladimir Ivanov]] — author who introduced this connection in the Turboplanner series
