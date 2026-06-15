---
title: Word Embeddings
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [architecture, technique]
sources:
  - "[Вектора GPT или почему для GPT ваше слово — пустота без контекста](raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md)"
confidence: high
---

# Word Embeddings

The representation of words and tokens as vectors in a high-dimensional continuous space. In production LLMs (GPT-class), each token maps to a vector with 10,000–14,000 dimensions. These vectors do not encode explicit features — they are compressed *correlation archives* encoding relationships to every other token in the model's training distribution. ^[raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md]

## Semantic ZIP Archive

The vector is not a feature list but a compressed archive containing potential for correlations. A 10,000-dimensional vector can encode over 100,000 correlation links when unpacked. This is what makes RAG feasible — a document corpus can be compressed into a single dense vector with acceptable semantic fidelity. ^[raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md]

Ivanov's "semantic magnifying glass" (Perceptron in GPT training video) illustrates the unpacking: the model expands a 10k-dimension vector into 40k dimensions during processing, revealing the latent correlations.

## Intuitive Model: Character Profile

The simplest pedagogical example: assign four characters (Knight, Mage, Archer, Dragon) numeric ratings on four axes (Strength, Intelligence, Humanity, Danger):

| Character | Strength | Intelligence | Humanity | Danger |
|-----------|----------|--------------|----------|--------|
| Knight   | 9        | 5            | 10       | 7      |
| Mage     | 3        | 10           | 8        | 6      |
| Archer   | 6        | 7            | 9        | 5      |
| Dragon   | 10       | 3            | 1        | 10     |

Each character's row is a semantic vector in a toy 4-dimensional space. Real GPT vectors have thousands of axes with no human-readable labels, but the principle is identical: any concept is a point in a multidimensional space of meanings, and semantic distance between concepts is measurable. ^[raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md]

## Superposition Catastrophe

Why so many dimensions? When a model tries to encode multiple distinct concepts in a low-dimensional space, they collapse into a blended "mutant" — neither one concept nor the other. This is the **superposition catastrophe**, studied by Anthropic (toy models of superposition) and predicted by Frank Rosenblatt (perceptron inventor).

With low dimensionality, an apple vector and a pear vector merge into a "fruit-mutant" hallucination — the model forgets the originals. High-dimensional space (10k+) prevents this by giving each concept enough orthogonal axes to maintain its distinct correlation structure. ^[raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md]

The practical implication: models with smaller embedding dimensions have a higher risk of superposition-induced hallucinations.

## Tokenisation Independence

Comparing English and Russian tokenisation proves that the token itself carries no intrinsic meaning:

- English: `[The] [worker] [is] [walking]` — 4 tokens, each a whole word
- Russian: `[Раб] [оч] [ий] [ид] [ёт]` — 5 tokens, some meaningless fragments like `[оч]`

Despite Russian breaking words into semantically-empty fragments, GPT performs equivalently on both languages (MMLU benchmarks). This demonstrates that meaning is **emergent** from contextual vector interactions, not stored in individual token vectors — even for English, `[worker]` has no Platonic essence. ^[raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/index.md]

## Relationship to Prompt Engineering

Understanding word embeddings as context-dependent correlation archives rather than fixed definitions is a prerequisite for effective prompting. Every token radically shifts its meaning based on the surrounding vector field. Mastery consists of constructing coherent semantic landscapes, not selecting "powerful" words.

## Limitations

- Embedding vectors cannot encode precise numbers (models use separate "calculator" tools)
- Exact quotes are not preserved — only their semantic gist
- The ZIP archive metaphor breaks down for fine-grained factual recall

## Related

- [[distributional-semantics|Distributional Semantics]] — the linguistic theory that word embeddings operationalise
- [[semantic-interference|Semantic Interference]] — closely related failure mode where superposition creates contradictory "semantic mush" from conflicting prompt vectors
- [[vladimir-ivanov|Vladimir Ivanov]] — author who explains this through the Turboplanner lens
