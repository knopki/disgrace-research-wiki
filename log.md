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

## [2026-06-17] ingest | Positional Encodings / Semantic Anchors article (Vladimir Ivanov, 2025-07-04)

- Raw source: raw/articles/2025-07-04-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/ (index.md + 3 images)
- Source: vk.com/@turboplanner
- Author: Vladimir Ivanov (2025-07-04)
- Content: deep dive into sinusoidal PE geometry (sin/cos, frequency nesting, phase/angle), the semantic fractal as a concrete PE phenomenon, the line-number problem, and the `# ANCHOR:` semantic anchor pattern as Anthropic's "secret sauce"
- Created concept: positional-encoding (PE geometry, frequency nesting, code-as-AST, line-number problem)
- Created concept: semantic-anchors (anchor markers, SWE Bench implications, relation to PE)
- Updated entity: vladimir-ivanov (added known work + source)
- Updated concept: semantic-fractal (added PE mechanism section, expanded cross-links)
- Updated concept: transformer (added source, cross-links to positional-encoding and semantic-anchors)
- Updated concept: vibe-coding (added source, cross-links to positional-encoding and semantic-anchors)
- Cross-links: positional-encoding ↔ transformer, semantic-fractal, word-embeddings, vibe-coding, semantic-anchors

## [2026-06-15] ingest | Design by Contract Wikipedia article

- Raw source: raw/articles/design-by-contract-wikipedia/ (index.md)
- Source: https://en.wikipedia.org/wiki/Design_by_contract
- Content: Original DbC by Bertrand Meyer (1986-1988): client/supplier metaphor, Hoare triple, three questions, inheritance rules, offensive vs defensive programming, language support, history
- Updated concept: contract-programming (added historical background, offensive vs defensive, performance/testing sections; added Wikipedia as second source; added wikilinks to vibe-coding, semantic-interference)
- Cross-links: contract-programming ↔ vibe-coding, semantic-interference

## [2026-06-15] ingest | Contract Programming article (Vladimir Ivanov, 2025-07-05)

- Raw source: raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ (index.md + 1 image)
- Source: vk.com/@turboplanner
- Author: Vladimir Ivanov (2025-07-05)
- Content: Design by Contract adapted for AI-assisted coding: pre/post conditions as semantic shields; semantic coherence (spec-contract-code trinity); belief state geometry (arxiv 2405.15943) as scientific basis; fractal contract structure; natural-language test specs vs executable tests; RAG-based agent navigation via two-level contracts; semantic annotation architecture as new discipline
- Created concept: contract-programming (contracts as AI semantic shields, semantic coherence, semantic specs vs tests, fractal contract structure, contract-driven RAG agent navigation)
- Updated entity: vladimir-ivanov (added known work + source)
- Updated concept: semantic-fractal (added belief state geometry section, cross-link to contract-programming)
- Updated concept: semantic-anchors (added cross-link to contract-programming)
- Updated concept: semantic-interference (added cross-link: contracts as structural antidote)
- Updated concept: vibe-coding (added cross-link: contract programming as methodology)
- Cross-links: contract-programming ↔ semantic-fractal, semantic-anchors, semantic-interference, vibe-coding, retrieval-augmented-generation, vladimir-ivanov

## [2026-06-16] ingest | Transformers Represent Belief State Geometry in their Residual Stream
- Raw source: raw/papers/belief-state-geometry-residual-stream/ (index.md)
- Source: Adam Shai et al., arXiv:2405.15943 (cs.LG, cs.CL), May 2024
- Created concept: belief-state-geometry
- Updated concept: semantic-fractal (added source, wikilink to belief-state-geometry, replaced bare arxiv link with wikilink + provenance marker)
- Updated concept: contract-programming (added source, wikilinks to belief-state-geometry and residual-connection, provenance marker)
- Cross-links: belief-state-geometry ↔ semantic-fractal, contract-programming, residual-connection, transformer, superposition, cognitive-superposition

## [2026-06-17] ingest | Semantic Superposition article (Vladimir Ivanov, 2025-07-06)

- Raw source: raw/articles/2025-07-06-kot-shredingera-v-golove-u-gpt-kak-superpoziciya-smyslov-men/ (index.md + 5 images)
- Source: vk.com/@turboplanner
- Author: Vladimir Ivanov (2025-07-06)
- Content: introduces semantic superposition as a prompt engineering paradigm; LLMs naturally hold multiple competing hypotheses in vector space; semantic collapse is the moment of commitment frozen by KV Cache; describes the Semantic Casino anti-pattern; BFS-like reasoning by delaying collapse; cites Meta's arXiv:2412.06769 on continuous latent space reasoning; two case studies (multithreading in RAG, plugin architecture)
- Created concept: semantic-superposition (superposition/collapse, KV Cache freezing, semantic casino, BFS reasoning, practical technique)
- Updated entity: vladimir-ivanov (added known work + source)
- Updated concept: semantic-interference (added cross-link contrasting deliberate superposition vs accidental mush)
- Updated concept: semantic-fractal (added cross-link to semantic-superposition as operational technique)
- Updated concept: vibe-coding (added cross-link to semantic-superposition as a concrete prompting methodology)
- Updated concept: contract-programming (added cross-link: contracts control when/how collapse happens)
- Cross-links: semantic-superposition ↔ semantic-interference, semantic-fractal, superposition, cognitive-superposition, word-embeddings, contract-programming, vibe-coding, vladimir-ivanov

## [2026-06-17] ingest | KV Caching Explained (João Lages, Medium, 2023-10-08)

- Raw source: raw/articles/kv-caching-explained/ (index.md + 4 images)
- Source: https://medium.com/@joaolages/transformers-kv-caching-explained-8e8f3d9e7b5e
- Author: João Lages (2023-10-08)
- Content: inference optimisation for generative transformers; KV cache stores Key/Value states from previous tokens to avoid redundant recomputation during auto-regressive generation; 4.7× speedup on GPT-2 for 1000-token generation; memory overhead is minimal; only applies to decoder/decoder-only models
- Created concept: kv-caching (inference optimisation, auto-regressive generation bottleneck, K/V caching mechanism, performance impact)
- Updated concept: semantic-superposition (added direct wikilink to kv-caching as the mechanism behind semantic collapse)
- Updated concept: transformer (added cross-link to kv-caching)
- Cross-links: kv-caching ↔ transformer, semantic-superposition, positional-encoding, residual-connection

