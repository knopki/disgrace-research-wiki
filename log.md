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
- Raw source: raw/papers/2022-09-elhage-toy-models-superposition/ (index.html + index.txt + index.md)
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

## [2026-06-17] ingest | Microsoft insider article (Vladimir Ivanov, 2025-07-10)

- Raw source: raw/articles/2025-07-10-za-kulisami-microsoft-tainye-elitnye-partnerskie-programmy-i/ (index.md + 4 images)
- Source: vk.com/@turboplanner
- Author: Vladimir Ivanov (2025-07-10)
- Content: insider perspective on Microsoft's elite partnership programs — MVP (Most Valuable Professional), Partner Engagement Board, Technology Adoption Program (TAP) — and their roles in product Vision validation and code review; 2010 partner network reform stripping Gold status from major Russian integrators; dual programming model's natural transition to AI operator model; AI replacing closed expert boards with large-scale sentiment analysis
- Created entity: microsoft (partnership programs, AI transformation, dual programming case study)
- Updated entity: vladimir-ivanov (added known work + source)
- Updated concept: vibe-coding (added Microsoft dual programming → AI operator transition as real-world case study, added source to frontmatter)
- Cross-links: microsoft ↔ vladimir-ivanov, vibe-coding

## [2026-06-15] ingest | Training Large Language Models to Reason in a Continuous Latent Space (Coconut)

- Raw source: raw/papers/2024-12-hao-coconut/ (index.md + PDF)
- Source: Shibo Hao et al., FAIR at Meta / UC San Diego, arXiv:2412.06769, COLM 2025
- Content: Chain of Continuous Thought (Coconut) — training paradigm replacing language chain-of-thought with reasoning directly in the continuous latent space of LLMs; enables emergent BFS-like reasoning via multi-stage curriculum; outperforms CoT on logical reasoning tasks with far fewer tokens
- Created concept: chain-of-continuous-thought (Coconut paradigm, latent reasoning, BFS emergence, ProsQA dataset)
- Updated concept: semantic-superposition (added as source + wikilink, bumped confidence to high)
- Updated concept: kv-caching (added cross-link: latent reasoning sidesteps KV-cache rigidity)
- Updated concept: transformer (added cross-link: latent reasoning exploits any-vector input capability)
- Cross-links: chain-of-continuous-thought ↔ semantic-superposition, kv-caching, superposition, belief-state-geometry, transformer, word-embeddings, vibe-coding

## [2026-06-15] ingest | Rational Unified Process Wikipedia article

- Raw source: raw/articles/rational-unified-process-wikipedia/ (index.md)
- Source: https://en.wikipedia.org/wiki/Rational_unified_process
- Content: iterative software development process framework by Rational/IBM; four life-cycle phases (Inception, Elaboration, Construction, Transition), nine disciplines, six best practices, RUP building blocks (roles, tasks, artifacts, guidance), certification, and relationship to UML
- Created concept: rational-unified-process (methodology, iterative risk mitigation, contrasts with vibe-coding and connects to contract-programming through shared emphasis on explicit specification)
- Cross-links: rational-unified-process ↔ contract-programming, vibe-coding


## [2026-06-15] ingest | BFS vs DFS (GeeksforGeeks)

- Raw source: raw/articles/bfs-vs-dfs-gfg/ (index.md)
- Source: https://www.geeksforgeeks.org/dsa/difference-between-bfs-and-dfs/
- Content: classic comparison of Breadth-First Search and Depth-First Search; queue vs stack, level-by-level vs sub-tree-by-sub-tree
- Created comparison: bfs-vs-dfs (reference anchor for BFS/DFS analogies in LLM reasoning pages)
- Updated concept: semantic-superposition (wikilinked BFS/DFS mentions to new comparison page)
- Updated concept: chain-of-continuous-thought (wikilinked BFS mention to new comparison page)
|||Cross-links: bfs-vs-dfs ↔ semantic-superposition, chain-of-continuous-thought

## [2026-06-15] ingest | BFS for a Graph (GeeksforGeeks)

- Raw source: raw/articles/bfs-gfg/ (index.md)
- Source: https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/
- Content: full BFS algorithm — queue-based level-by-level traversal, visited array, O(V+E) complexity, disconnected graph handling, applications (shortest path, web crawling, social networks, GPS, cycle detection, Ford-Fulkerson)
- Created concept: bfs (algorithm mechanics, disconnected graphs, applications, LLM reasoning relevance)
- Updated comparison: bfs-vs-dfs (added See Also section with wikilink to new bfs page)
- Cross-links: bfs ↔ bfs-vs-dfs, semantic-superposition, chain-of-continuous-thought, kv-caching

||## [2026-06-15] schema | schema audit and fixes
|- SCHEMA.md: added `technique` to tag taxonomy under Techniques (was in use on 8 pages but missing from schema)
|- SCHEMA.md: updated `sources:` frontmatter example to YAML block list with markdown links (was inline array with bare paths)
|- SCHEMA.md: fixed provenance marker convention to `^[raw/*/dir-name/index.md]` (was `source.md`; actual raw sources are directories)
|- entities/vladimir-ivanov.md: removed 9 duplicate article sources (duplicated Known Works); replaced with LinkedIn profile as biographical source
|- entities/vladimir-ivanov.md: added wikilinks to vibe-coding and contract-programming (was 1 wikilink, below min 2 rule)

## [2026-06-15] ingest | PCAM methodology article (Vladimir Ivanov, 2025-09-11)

- Raw source: raw/articles/2025-09-11-metodologiya-pcam-prevraschaem-ai-agentov-iz-rabov-v-partner/ (index.md + 4 images)
- Source: vk.com/@turboplanner
- Author: Vladimir Ivanov (2025-09-11)
- Content: introduces Purpose Centric Agent Methodology (PCAM) — paradigm shift from deterministic step-by-step plans to goal-oriented guidance; six principles (goal primacy, contextual guides, standardized protocols, plugin architecture, self-healing, integrated feedback loop); practical implementation in multi-agent teams with guides, PLAN-CONFIRM workflow, and plugin-based scalability
- Created concept: pcam (six principles, plugin architecture, self-healing, feedback loop)
- Updated entity: vladimir-ivanov (added known work + topics + Related wikilink)
- Cross-links: pcam ↔ vladimir-ivanov, vibe-coding, contract-programming, semantic-anchors, semantic-superposition, human-sequential-bottleneck

## [2026-06-15] ingest | GRACE framework article (Vladimir Ivanov, 2025-09-13)

- Raw source: raw/articles/2025-09-13-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/ (index.md + images/)
- Source: vk.com/@turboplanner
- Author: Vladimir Ivanov (2025-09-13)
- Content: introduces GRACE (Graph-RAG Anchored Code Engineering) — framework for deterministic LLM code generation in large contexts addressing sparse attention and RAG agent limitations; ten principles (Intent-First Architecture, Synthesis from Approved Blueprints, AI-Readable Scaffolding, Context via Knowledge Graph, Dual-Purpose Semantic Markup, Proportional Granularity, Code as Living Document, Observable AI Belief State, End-to-End Traceability, Governed Autonomy); five-stage process model (Requirements Analysis → Technology Stack → Architectural Scaffold → Code Generation → Verification); dual-purpose semantic markup for generative models (top-down template) vs RAG agents (navigation map); sparse attention mitigation via XML tag beacons; belief state declaration via structured logging
- Created concept: grace (ten principles, five-stage process, dual-purpose markup, sparse attention mitigation, knowledge graph linking)
- Updated entity: vladimir-ivanov (added known work, GRACE to topics, wikilink to grace)
- Updated concepts: semantic-anchors, contract-programming, pcam, vibe-coding, positional-encoding, belief-state-geometry, semantic-fractal, semantic-interference, knowledge-graph, retrieval-augmented-generation (added cross-link to grace)
- Cross-links: grace ↔ vladimir-ivanov, semantic-anchors, contract-programming, pcam, vibe-coding, positional-encoding, belief-state-geometry, semantic-fractal, semantic-interference, knowledge-graph, retrieval-augmented-generation, human-sequential-bottleneck

## [2026-06-15] ingest | Sparse Transformer paper (Child et al., OpenAI, 2019)
- Raw source: raw/papers/sparse-transformer/ (index.md + full-text.txt)
- Source: https://arxiv.org/abs/1904.10509
- Authors: Rewon Child, Scott Gray, Alec Radford, Ilya Sutskever (OpenAI)
- Content: Introduces sparse factorized self-attention reducing Transformer O(n²) to O(n√n); two patterns (strided for periodic data, fixed for text); pre-activation residual blocks with 1/√(2N) initialization for deep stacks; gradient checkpointing for attention; block-sparse kernels; SOTA on Enwik8 (0.99 bpb, 95M), CIFAR-10 (2.80 bpd, 59M), ImageNet-64 (3.44 bpd, 152M); self-attention shown on sequences up to 1M+ tokens at 3M params
- Created concept: sparse-transformer (attention sparsity, two factorization patterns, deep transformer scaling, gradient checkpointing legacy)
- Updated concept: transformer (added cross-link in Limitations — sparse attention addresses O(n²) bottleneck)
- Updated concepts: kv-caching, chain-of-continuous-thought, positional-encoding (added cross-link to sparse-transformer)
- Cross-links: sparse-transformer ↔ transformer, kv-caching, chain-of-continuous-thought, positional-encoding, residual-connection

## [2026-06-15] fix | Sparse Transformer raw + concept page corrections
- **Problem:** raw/index.md was written from partial web_extract (~5K chars truncated summary) instead of full PDF text. Results tables contained fabricated data (wrong model sizes, wrong baselines).
- **Fix:** Extracted full 36K chars from PDF via pdftotext → saved as full-text.txt alongside raw. Rewrote raw/index.md as proper condensation grounded in full text. Corrected concept page results tables — Enwik8: removed fake "12L/24L sparse" entries, replaced with actual paper data (Sparse Transformer 95M at 0.99 bpb). ImageNet-64: added proper baseline table from paper. Audio: added scalability study with 1M+ token caveat. Added key finding about sparse patterns outperforming dense attention.

## [2026-06-15] reimport | Sparse Transformer paper — proper naming + PDF + synthesis audit
- **Renamed:** raw/papers/sparse-transformer/ → raw/papers/2019-04-child-sparse-transformer/ (date-prefix + author + slug convention)
- **Original PDF saved:** raw/papers/2019-04-child-sparse-transformer/1904.10509.pdf (6 pages, 4.4 MB, SHA256: 5b6a655a)
- **New raw/index.md:** includes abstract from PDF, key contributions summary, architecture overview, and results table — links to PDF for full content
- **index.md:** Papers entry now links directly to PDF (1904.10509.pdf) with abstract+details link to index.md
- **Concept page fixes (3 hallucinations fixed after full PDF read-through):**
  - Gradient checkpointing: removed "first application" claim — paper does not assert this
  - ImageNet-64: removed "first autoregressive on raw bytes at this scale" — unsupported by paper
  - Audio capacity scaling: corrected ∜4 ≈ 1.4x → 8x per 4x length increase (O(n√n) scaling)
- Sources updated in concept page: sparse-transformer/index.md → 2019-04-child-sparse-transformer/index.md
- Old raw/papers/sparse-transformer/ directory removed

## [2026-06-15] reimport | Coconut paper — proper naming + PDF + synthesis audit
- **Renamed:** raw/papers/2412.06769-coconut/ → raw/papers/2024-12-hao-coconut/ (date-prefix + author + slug convention)
- **Original PDF saved:** raw/papers/2024-12-hao-coconut/2412.06769.pdf (3.2 MB, 18 pages, SHA256: 6eb32c71)
- **New raw/index.md:** abstract only, links to PDF for full content — no synthetic summary in raw/
- **Hallucinations fixed (2) after full PDF read-through:**
  - "Haviv et al., 2024 (Thinking LLMs)" — removed from related work; never cited in actual paper
  - "Yang et al., 2024 (Continuous Chain-of-Thought)" — corrected description; actual Yang 2024 work is about latent multi-hop reasoning, not "compressing CoT"
- **Typo fixed:** "the the transformer" → "the transformer" in concept page
- **References updated:** Fedorenko 2024 and Deng 2024 corrected to proper titles; added Zhu et al. 2025a, 2025b (theoretical follow-ups cited in paper)
- Updated index.md entry to link PDF + index.md
- Updated wikilinks in 5 pages (bfs-vs-dfs, bfs, semantic-superposition, chain-of-continuous-thought, index.md)
- Old raw/papers/2412.06769-coconut/ removed

## [2026-06-17] reingest | belief state geometry paper (Shai et al., 2024)

- **Renamed:** raw/papers/belief-state-geometry-residual-stream/ → raw/papers/2024-05-shai-belief-state-geometry/ (date-prefix + author + slug convention)
- **Original PDF saved:** raw/papers/2024-05-shai-belief-state-geometry/2405.15943.pdf (3.1 MB, 15 pages + appendix, SHA256: a4d7ea3269)
- **New raw/index.md:** abstract + PDF link only — no synthetic summary
- **Hallucination fixed (major) after full PDF read-through:**
  - Old raw/index.md listed authors as "Adam Shai, Kathryn Br_rewards, Sam Buchanan, Daniel L. K. Yamins, M. I. Jordan, Michael W. DeWeese, Sandra J. Berman, Christopher J. Cueva" — **none of these except Shai are on the paper**
  - Correct authors: Adam S. Shai, Sarah E. Marzen, Lucas Teixeira, Alexander Gietelink Oldenziel, Paul M. Riechers
- **Venue corrected:** "arXiv preprint" → **NeurIPS 2024** (paper was accepted at NeurIPS)
- **Synthesis verified against full PDF:** existing belief-state-geometry.md content is accurate — no further hallucination found (MSP mechanism, Mess3 fractal, RRXOR degeneracy with R² values, distributed layers, architecture independence, linearity as empirical finding from SGD, limitations all confirmed)
- Updated references in: belief-state-geometry.md (7 references), semantic-fractal.md (2), contract-programming.md (2), index.md
- Old raw/papers/belief-state-geometry-residual-stream/ removed

## [2026-06-15] schema | provenance markers migrated to clickable links
- Convention: `^[raw/...]` → `([Author, Year](raw/...))` (clickable markdown link in parentheses)
- SCHEMA.md and AGENTS.md updated
- 116 markers migrated across 30 wiki pages
- Labels: Ivanov, 2025 (articles); Hao et al. 2024, Shai et al. 2024, Garagnani 2024, Anthropic 2022 (papers); Wikipedia (encyclopedic)

## [2026-06-15] re-ingest | Garagnani cognitive superposition paper
- **Corrected naming:** `raw/papers/cognitive-superposition-garagnani/` → `raw/papers/2024-02-garagnani-cognitive-superposition/`
- **Added PDF:** downloaded original PDF (11571_2023_Article_10061.pdf, Open Access CC BY 4.0) from Springer
- **New index.md:** frontmatter + abstract only, no transcription — links to PDF for full text
- **Old directory removed:** `raw/papers/cognitive-superposition-garagnani/` deleted
- **Fixes to concepts/cognitive-superposition.md:**
  - Bowers violation corrected: condition (1), not (2) — items co-activated during training, violating the independently-acquired requirement
  - Fabricated "thousands to tens of thousands of neurons per CA" claim removed — model has 6×625 = 3,750 cells total, no such claim in the PDF
  - All provenance markers updated to new path
- Updated: index.md (link path), concepts/cognitive-superposition.md (sources + provenance paths)

## [2026-06-16] re-ingest | Toy Models of Superposition (Elhage et al., 2022)
- Raw source renamed: `raw/papers/toy-models-superposition/` → `raw/papers/2022-09-elhage-toy-models-superposition/`
- raw/index.md rewritten: now contains the paper's original abstract (verbatim from HTML) instead of a summary
- Full source read (1023-line extraction from index.html); all 4 wiki pages cross-checked against source — no hallucinations found
- All 6 wiki page references updated (superposition, polysemantic-neurons, privileged-basis, anthropic, index.md, log.md)
|- index.md paper entry link updated

## [2026-06-15] ingest | SLM vs MoE for Agentic AI article (Vladimir Ivanov, 2025-09-14)
- Raw source: raw/articles/2025-09-14-ivanov-prichiny-nabludaemogo-provala-malyh-slm-protiv-llm-na-moe-v/ (ivanov2025slmvsllm.md + 2 images)
- Source: vk.com/@turboplanner
- Author: Vladimir Ivanov (2025-09-14)
- Content: rebuttal of Belcak et al. (2025, NVIDIA Research) SLM-centric thesis; three arguments — (1) OpenRouter market data shows tool-use dominated by medium models, not SLM; (2) MoE + MTP (Qwen3-Next-80B-A3B) eliminates SLM cost advantage with 3B active params at LLM quality; (3) free API tiers (Gemini Flash) commoditize low-intensity tasks, making self-hosted SLM uneconomical
- Created concept: slm-moe-agentic-ai (market data, MoE+MTP argument, free tier commoditization, synthesis)
- Updated entity: vladimir-ivanov (added Known Work, topics, wikilink to new concept)
- Cross-links: slm-moe-agentic-ai ↔ vladimir-ivanov, vibe-coding, kv-caching, chain-of-continuous-thought, sparse-transformer

## [2026-06-17] ingest | Longformer (Beltagy et al., 2020)
- Raw source: `raw/papers/2020-04-beltagy-longformer/` (2004.05150.pdf + index.md)
- Source: arXiv:2004.05150 — "Longformer: The Long-Document Transformer"
- Authors: Iz Beltagy, Matthew E. Peters, Arman Cohan (Allen Institute for AI, 2020)
- Content: linear-complexity attention combining sliding window + dilated window + task-specific global attention; pretrained from RoBERTa, finetuned on long-document tasks; LED variant for seq2seq summarization
- Created concept: longformer (attention mechanism, three implementations, pretraining strategy, LED, ablation insights, results on text8, enwik8, WikiHop, TriviaQA, HotpotQA, arXiv summarization)
- Updated concept: sparse-transformer (added [[wikilink]] to longformer in Significance & Legacy)
- Cross-links: longformer ↔ sparse-transformer, transformer, kv-caching, chain-of-continuous-thought

## [2026-06-17] ingest | BigBird (Zaheer et al., 2020)
- Raw source: `raw/papers/2020-07-zaheer-big-bird/` (2007.14062.pdf + zaheer2020bigbird.md)
- Source: arXiv:2007.14062 -- "Big Bird: Transformers for Longer Sequences"
- Authors: Manzil Zaheer et al. (Google Research, NeurIPS 2020)
- Content: linear-complexity attention combining random + window + global tokens; theoretical guarantees (universal approximation, Turing completeness); SOTA on TriviaQA, WikiHop, Natural Questions; summarization via RoBERTa/Pegasus warm-start; first genomics application of transformer-based DNA MLM
- Created concept: big-bird (three-component attention, theoretical proofs, NLP results, genomics)
- Updated concept: sparse-transformer (added [[wikilink]] to big-bird in Relationship and Legacy)
- Updated concept: longformer (added [[wikilink]] to big-bird in table + Relationship)
- Cross-links: big-bird ↔ sparse-transformer, longformer, transformer, kv-caching, chain-of-continuous-thought

## [2026-06-15] ingest | Small Language Models are the Future of Agentic AI (Belcak et al., NVIDIA, 2025)
- Raw source: `raw/papers/2025-06-belcak-slm-agentic-ai/` (2506.02153.pdf + index.md)
- Source: arXiv:2506.02153v1 — "Small Language Models are the Future of Agentic AI"
- Authors: Peter Belcak, Greg Heinrich, Shizhe Diao, Yonggan Fu, Xin Dong, Saurav Muralidharan, Yingyan Celine Lin, Pavlo Molchanov (NVIDIA Research)
- Content: position paper arguing SLMs (<10B) are sufficiently powerful, inherently more suitable, and necessarily more economical for most agentic AI invocations; explicitly advocates heterogeneous systems (LLM orchestrator + SLM workers) where general conversation is needed; includes A1 benchmark table, A2–A7 supporting arguments, and AV1–AV3 rebuttal of counter-views
- Updated comparison: slm-moe-agentic-ai (retrofitted from concept→comparison; added Belcak raw source; nuanced position as heterogeneous not SLM-only; added A1 table; marked contested/medium-confidence; balanced synthesis)
- Raw source: `raw/papers/2025-02-zhang-spargeattention/` (2502.18137.pdf + zhang2025spargeattn.md)
- Source: arXiv:2502.18137 — "SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference"
- Authors: Jintao Zhang, Chendong Xiang, Haofeng Huang, Jia Wei, Haocheng Xi, Jun Zhu, Jianfei Chen (Tsinghua University / UC Berkeley, ICML 2025)
- Content: universal training-free sparse attention operator with two-stage online filter — (1) selective token compression for sparse mask prediction, (2) sparse warp online softmax to skip P̃V products; self-similarity judge for fix block protection; HilbertCurve permutation for visual tokens; integrated with SageAttention (8-bit quantized); 1.83× speedup on Mochi (L40), 4.5× speed on Llama3.1 128K, up to 54% sparsity
- Created concept: spargeattn (two-stage filter, selective token compression, sparse warp online softmax, HilbertCurve permutation, self-similarity judge, SageAttention integration, hyper-parameter tuning, results table, comparison with architectural sparse methods)
- Updated concept: sparse-transformer (added [[wikilink]] to spargeattn)
- Updated concept: longformer (added [[wikilink]] to spargeattn)
- Updated concept: big-bird (added [[wikilink]] to spargeattn)
- Updated concept: kv-caching (added [[wikilink]] to spargeattn)
- Cross-links: spargeattn ↔ sparse-transformer, longformer, big-bird, kv-caching, transformer
