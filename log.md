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

## [2026-06-17] ingest | Toy Models of Superposition (Anthropic, 2022)
- Raw source: raw/papers/toy-models-superposition/ (index.html + index.txt + index.md)
- Source: https://transformer-circuits.pub/2022/toy_model/index.html
- Created entity: anthropic
- Created concepts: superposition, polysemantic-neurons, privileged-basis
- Updated: word-embeddings (added wikilinks to superposition, privileged-basis, anthropic)
- Updated: distributional-semantics (added wikilink to superposition)
- New tag added: organization (Meta category in SCHEMA.md)

## [2026-06-17] restructure | raw/ split into articles/ and papers/

- Added `raw/ Structure` section to SCHEMA.md defining `articles/` (blog posts, Wikipedia) vs `papers/` (academic publications).
- Moved `raw/articles/toy-models-superposition/` to `raw/papers/toy-models-superposition/`.
- Updated all 6 wiki pages referencing `raw/articles/toy-models-superposition/` (superposition, polysemantic-neurons, privileged-basis, anthropic, index.md, log.md).
- Updated index.md Raw Sources section: added "Articles" and "Papers" subheadings.

## [2026-06-17] ingest | Cognitive Superposition position paper (Garagnani, 2024)

- Raw source: raw/papers/cognitive-superposition-garagnani/ (index.md)
- Source: https://link.springer.com/article/10.1007/s11571-023-10061-1
- Author: Max Garagnani
- Created concept: cognitive-superposition
- Updated: superposition (added distinguishing note + cross-link)
- Cross-links: cognitive-superposition ↔ superposition, word-embeddings, polysemantic-neurons, anthropic

## [2026-06-17] ingest | AI History overview article (Vladimir Ivanov, 2025-07-03)

- Raw source: raw/articles/2025-07-03-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/ (index.md + 2 images)
- Source: vk.com/@turboplanner
- Author: Vladimir Ivanov (2025-07-03)
- Historical overview: Rosenblatt → Minsky/Papert dark ages → backpropagation → LSTM → ResNet → Transformer
- Updated entity: vladimir-ivanov (added known work + source)
- Updated entity: frank-rosenblatt (added source, updated cross-links)
- Updated concept: perceptron (added cross-links to new pages)
- Created concepts: backpropagation, lstm, residual-connection, transformer
- Cross-links: all 4 new pages interconnected; backpropagation ↔ perceptron ↔ frank-rosenblatt; transformer ↔ residual-connection; lstm ↔ backpropagation
