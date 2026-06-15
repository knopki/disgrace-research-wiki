# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-06-16] create | Wiki initialized
- Domain: LLM, ML, AI agents, research methodologies
- Structure created with SCHEMA.md, index.md, log.md

## [2026-06-16] ingest | vk-turboplanner AI parallelism article
- Raw source: raw/articles/2025-06-30-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/ (index.md + 2 images)
- Author: Vladimir Ivanov (2025-06-30)
- Entity page created: entities/vladimir-ivanov.md
- Concept pages created: innate-parallelism, semantic-fractal, human-sequential-bottleneck, vibe-coding

## [2026-06-16] ingest | AI Resource Leveling article
- Raw source: raw/articles/2025-07-01-ai-v-upravlenii-proektami-teper-resource-leveling-uzhe-rab/ (index.md + 2 images)
- Author: Vladimir Ivanov (2025-07-01)
- Updated entity: entities/vladimir-ivanov.md
- Created concepts: ai-resource-leveling, skill-scheduling

## [2026-06-16] ingest | Semantic Interference article
- Raw source: raw/articles/2025-07-01-semanticheskaya-interferenciya-ili-nazhat-gaz-i-tormoz-srazu/ (index.md + empty images/)
- Author: Vladimir Ivanov (2025-07-01)
- Created concept: semantic-interference
- Updated entity: vladimir-ivanov (added known work + source)

## [2026-06-16] ingest | Word Embeddings / Distributional Semantics article
- Raw source: raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/ (index.md + 5 images)
- Author: Vladimir Ivanov (2025-07-02)
- Updated entity: vladimir-ivanov (added known work + source)
- Created concepts: distributional-semantics, word-embeddings

## [2026-06-16] ingest | Retrieval-Augmented Generation (RAG) Wikipedia article
- Raw source: raw/articles/rag-wikipedia/ (index.md)
- Source: Wikipedia (Russian), page "Генерация с дополненной выборкой"
- Created concept: retrieval-augmented-generation
- Cross-links: word-embeddings, distributional-semantics

## [2026-06-16] ingest | Knowledge Graph (Google) Wikipedia article
- Raw source: raw/articles/knowledge-graph-google-wikipedia/ (index.md)
- Source: Wikipedia (English), page "Knowledge Graph (Google)"
- Created concept: knowledge-graph
- Cross-links: retrieval-augmented-generation, distributional-semantics, word-embeddings
- New tag added: knowledge-graph (Knowledge category in SCHEMA.md)

## [2026-06-17] ingest | Corpus Linguistics Wikipedia article
- Raw source: raw/articles/corpus-linguistics-wikipedia/ (index.md)
- Source: Wikipedia (Russian), page "Корпусная лингвистика"
- Created concept: corpus-linguistics
- Cross-links: distributional-semantics, retrieval-augmented-generation, word-embeddings, knowledge-graph
- Updated: distributional-semantics (added cross-link to corpus-linguistics)

## [2026-06-17] ingest | Frank Rosenblatt Wikipedia article
- Raw source: raw/articles/frank-rosenblatt-wikipedia/ (index.md)
- Source: Wikipedia (English), page "Frank Rosenblatt"
- Created entity: frank-rosenblatt
- Created concept: perceptron
- Updated concept: word-embeddings (added wikilink to frank-rosenblatt)
- Cross-links: perceptron ↔ frank-rosenblatt, word-embeddings, distributional-semantics
