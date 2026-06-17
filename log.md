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

## [2026-06-15] ingest | GPT-4.1 Prompting Guide (OpenAI Cookbook)

- Raw source: `raw/articles/2026-06-15-openai-gpt41-prompting-guide/`
- Source: https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
- Imported via defuddle.md (full markdown extraction, 1150 lines)
- Content: comprehensive prompting guide covering Agentic Workflows (three-reminder system: persistence, tool-calling, planning; SWE-bench Verified at 55% SOTA for non-reasoning models), Long Context (1M tokens, two-pass re-ranking, batching patterns), Structured Outputs, Customer Service Agent example, General Advice (prompt structure, delimiters), Appendix: V4A Diff Format with reference apply_patch.py implementation
- Created concept: v4a-diff-format (format spec, context anchoring, reference implementation, relationship to GRACE/contract-programming)
- Updated concept: grace (added [[wikilink]] to v4a-diff-format in Direct Navigation and Deterministic Patching section)
- Cross-links: v4a-diff-format ↔ grace, contract-programming

## [2026-06-15] ingest | CoT Harms Performance of Rather Smaller Language Models (Shim et al., IEOM 2024)
- Raw source: `raw/papers/2024-10-09-ship-cot-harms/` (shim2024cotharms.pdf + shim2024cotharms.md)
- Source: https://index.ieomsociety.org/index.cfm/item/55021 — IEOM 1st World Congress 2024 Detroit
- Authors: Jihoo Shim, Shin Dong Ho (My Paul School), Jeongwon Kim (Nihon University)
- Track: High School STEM Poster Competition
- Content: investigates CoT prompting on SLMs (GPT-2 117M–1558M, GPT-Neo 125M–2.7B) on GSM8K. CoT degrades accuracy by 15–30%+ with relative losses of 31–47% (GPT-2) and up to 100% (GPT-Neo 125M). Loss is multiplicative (proportional to baseline), not additive. Convergence effect: CoT scores cluster toward a ceiling. GPT-Neo shows slightly more resilience than GPT-2.
- Created concept: chain-of-thought (CoT definition, effect by model size with results table, usage patterns, relationship to Continuous Thought)
- Updated comparison: slm-moe-agentic-ai (added raw source + synthesis table row "Prompting robustness" + additional evidence paragraph)
- Updated concept: chain-of-continuous-thought (added [[wikilink]] to chain-of-thought in Relationship to Other Concepts)
- Cross-links: chain-of-thought ↔ chain-of-continuous-thought, slm-moe-agentic-ai

## [2026-06-16] ingest | FLEX: Few-shot Logit-Enabled XML Prompting (Vladimir Ivanov, 2025-09-18)
- Raw source: `raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/` (ivanov2025flex.md + 01.jpg)
- Source: https://vk.com/@turboplanner-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog
- Author: Vladimir Ivanov (Turboplanner)
- Content: introduces FLEX — methodology for reliable SLM control via structured XML prompts, few-shot learning, and logit-based verification. Validated on Qwen3-0.6B for tool selection (99%+ accuracy, 84% in ambiguous cases). Argues CoT for SLMs is post-hoc rationalization, not genuine reasoning. XML preferred over JSON due to lower logit noise. Multi-level tool description (Keywords, Trigger, Description). Confidence parameter correlates with actual logit probability. Compatible with SLM ensembles for hallucination suppression.
- Created concept: flex-prompting (three pillars: XML > JSON, multi-level tool description, few-shot + logit verification; experimental results table; logit-based diagnostics; ensemble compatibility)
- Updated entity: vladimir-ivanov (added FLEX work to Known Works + Topics + Related)
- Updated concept: chain-of-thought (added Criticism: CoT as Post-Hoc Rationalization section with Ivanov's argument)
- Cross-links: flex-prompting ↔ chain-of-thought, vladimir-ivanov, slm-moe-agentic-ai, semantic-interference, grace, pcam

## [2026-06-16] ingest | Hallucination Detection with SLMs (Ming Cheung, IEEE ICDE Workshop 2025)
- Raw source: raw/papers/2025-06-24-cheung-hallucination-detection-slm/ (2506.22486.pdf + index.md)
- Source: https://arxiv.org/abs/2506.22486
- Author: Ming Cheung (dBeta Labs, The Lane Crawford Joyce Group, Hong Kong)
- Content: proposes a framework integrating multiple SLMs (Qwen2-1.5B + MiniCPM-2B) for post-hoc hallucination verification of LLM responses in RAG context. Pipeline: Splitter (sentence decomposition) → SLM ensemble (P(yes) token probability per sentence) → Checker (z-score normalization per model, harmonic mean across sentences, threshold decision). Validated on real dataset from Lane Crawford employee handbook (100+ QA triples). Proposed approach outperforms ChatGPT by ~11% F1 and single-model P(yes) by ~6.6% F1 for detecting correct vs wrong responses.
- Created concept: hallucination-detection-slm (framework architecture: Splitter, SLM ensemble, Checker; sentence-level P(yes) scoring; per-model normalization; harmonic mean aggregation; experimental results; connections to RAG, FLEX, GRACE)
- Updated comparison: slm-moe-agentic-ai (added source, "Verification performance" row to synthesis table, evidence paragraph: SLMs outperforming ChatGPT on verification task supports heterogeneous system view)
- Updated concept: retrieval-augmented-generation (added cross-link to hallucination-detection-slm)
- Cross-links: hallucination-detection-slm ↔ retrieval-augmented-generation, slm-moe-agentic-ai, flex-prompting, chain-of-thought, contract-programming, grace

## [2026-06-16] ingest | Mamba/SSM RAG Self-Correction (Vladimir Ivanov, 2025-09-21)
- Raw source: `raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/` (ivanov2015hallucinations.md + 01.jpg)
- Source: https://vk.com/@turboplanner-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i
- Author: Vladimir Ivanov (Turboplanner)
- Content: experimental study on Mamba/SSM hallucination mitigation through RAG-driven self-correction. Qwen-Next-80B-A3B-Instruct hybrid Mamba-Transformer model demonstrated ability to identify and correct anthropomorphisms, logical exaggerations, and factual inaccuracies with 100% success rate via belief state overwriting. KV cache memory wall comparison (Table: LLaMA-3.3-70B 32.6 GB vs Mamba ~24 MB at 100K tokens). Frames Mamba+RAG as "liquid + crystallised intelligence" — Mamba provides rapid reasoning and plasticity, RAG provides external fact verification.
- Created concept: mamba (SSM architecture, memory wall comparison, plasticity, hybrid models, RAG-driven self-correction, liquid+crystallised intelligence framing, limitations)
- Updated entity: vladimir-ivanov (added Mamba+RAG study to Known Works + Topics + Related)
- Updated concept: retrieval-augmented-generation (added oracle/verification paradigm + cross-link to mamba)
- Updated concept: kv-caching (added Mamba memory comparison data + cross-link to mamba)
- Updated concept: grace (added cross-link to mamba as next logical step: structural integrity → factual accuracy)
- Updated concept: hallucination-detection-slm (added cross-link to mamba as complementary approach: post-hoc verification vs in-generation self-correction)
- Cross-links: mamba ↔ kv-caching, retrieval-augmented-generation, grace, hallucination-detection-slm, transformer, sparse-transformer, vladimir-ivanov

## [2026-06-16] ingest | GRACE as Native Interface for Mamba (Vladimir Ivanov, 2025-09-21)
- Raw source: `raw/articles/2025-09-21-ivanov-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m/` (ivanov2025gracemamba.md + 01.jpg)
- Source: https://vk.com/@turboplanner-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m
- Author: Vladimir Ivanov (Turboplanner)
- Content: demonstrates GRACE semantic markup as a native interface for Mamba/SSM models. Qwen-3-Next hybrid Mamba-Transformer achieves >99.9% context reconstruction accuracy with GRACE markup. Key findings: (1) dual graph role — passive attention assistance for Transformers vs active verification shield for Mamba; (2) reconstruction from internal knowledge graph vs citation; (3) semantic slices as unique Mamba capability for RAG agents; (4) risk of structural hallucinations in leaf-level details and meta-pattern generalisation; (5) three-part symbiosis: GRACE blueprint → Mamba internal graph → RAG verification cycle
- Updated concept: grace (added Mamba/SSM Synergy section about dual graph role, reconstruction vs citation, semantic slices, structural hallucination risks, three-part symbiosis; added source to frontmatter)
- Updated concept: mamba (added GRACE as Native Interface section about reconstruction mechanism, dual graph role, semantic slices, symbiotic architecture; added source to frontmatter; updated cross-link)
- Updated entity: vladimir-ivanov (added GRACE-Mamba study to Known Works)
- Cross-links: grace ↔ mamba (deepened: native interface + verification synergy)

## [2026-06-16] ingest | Attention Is All You Need (Vaswani et al., Google/NIPS, 2017)
- Raw source: `raw/papers/2017-06-vaswani-attention-is-all-you-need/` (1706.03762.pdf + vaswani2017attention.md)
- Source: https://arxiv.org/abs/1706.03762 (v7, Aug 2023)
- Authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin (equal contribution, random listing order)
- Venue: NIPS 2017 (31st Conference on Neural Information Processing Systems)
- Content: Proposes the Transformer — first sequence transduction model based entirely on self-attention, dispensing with recurrence and convolutions. Introduces Scaled Dot-Product Attention, Multi-Head Attention (h=8, d_k=d_v=d_model/h=64), sinusoidal Positional Encoding, N=6 encoder/decoder stacks with d_model=512, d_ff=2048. Achieves SOTA on WMT 2014 EN-DE (28.4 BLEU) and EN-FR (41.8 BLEU) translation. Generalizes to English constituency parsing (WSJ 91.3 F1, semi-supervised 92.7 F1).
- Updated concept: transformer (added primary source, architecture details — N=6, d_model=512, d_ff=2048, h=8; training regime — 100K steps base/300K steps big, 8×P100 GPUs, Adam lr schedule; results tables — EN-DE 27.3/28.4, EN-FR 38.1/41.8 BLEU; English constituency parsing results)
- Updated concept: positional-encoding (added paper as primary source, provenance marker in body)
- Updated wiki pages converted plain-text "transformer" → [[wikilinks]]: kv-caching, privileged-basis, semantic-fractal, grace, belief-state-geometry, longformer, big-bird (3 mentions), slm-moe-agentic-ai, README (2 mentions)
- Cross-links: transformer ↔ raw source (primary provenance); 9 pages updated with transformer wikilinks

## [2026-06-16] ingest | Dario Amodei Wikipedia article
- Raw source: raw/articles/dario-amodei-wikipedia/index.md
- Source: Wikipedia (English), page "Dario Amodei"
- Entity page created: entities/dario-amodei.md
- Key facts: co-founder/CEO of Anthropic, former VP Research at OpenAI, author of "Machines of Loving Grace" and "The Adolescence of Technology", Pentagon dispute (2026)
- Cross-links: anthropic, superposition, polysemantic-neurons, vladimir-ivanov

|## [2026-06-16] ingest | Scaling Laws for Neural Language Models (Kaplan et al., OpenAI, 2020)
|- Raw source: `raw/papers/2020-01-kaplan-scaling-laws/` (2001.08361.pdf + index.md)
|- Source: https://arxiv.org/abs/2001.08361
|- Authors: Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, Dario Amodei (equal contribution, random order)
|- Venue: arXiv preprint, January 2020
|- Content: Empirical scaling laws for LM performance — power-law relationships with model size (α_N ≈ 0.076), dataset size (α_D ≈ 0.095), and training compute (α_C ≈ 0.050). Larger models are more sample-efficient. Compute-optimal allocation trains large models to ~10% above converged loss. Predicted breakdown at C* ~ 10^4 PF-days, N* ~ 10^12 params.
|- Raw directory created (was referenced by existing concept page but missing)
|- Updated concept: scaling-laws (added raw_ingested: true flag, source now resolves)
|- Updated index.md: added concept entry and raw source under Papers
|- Cross-links: transformer, lstm, kv-caching, sparse-transformer, dario-amodei
|
|## [2026-06-16] ingest | Training Compute-Optimal Large Language Models (Hoffmann et al., DeepMind, 2022)
|- Raw source: `raw/papers/2022-03-hoffmann-chinchilla/` (2203.15556.pdf + hoffmann2022chinchilla.md)
|- Source: https://arxiv.org/abs/2203.15556
|- Authors: Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, Laurent Sifre (22 authors, DeepMind)
|- Venue: arXiv preprint, March 2022
|- Content: Landmark study establishing that current LLMs are undertrained. For compute-optimal training, model size and training tokens should scale equally (N ∝ D), contradicting Kaplan et al.'s earlier finding (N ∝ C^0.73). Validated by training Chinchilla (70B, 1.4T tokens) which outperforms Gopher (280B), GPT-3 (175B), Jurassic-1 (178B), and MT-NLG (530B) across all evaluated tasks. Chinchilla achieves 67.5% on MMLU (+7% over Gopher).
|- Updated concept: scaling-laws (added Chinchilla section with equations, model comparison table, and implication paragraph; updated Historical Impact to note contradiction rather than refinement)
|- Updated index.md: added raw source under Papers
||- Cross-links: scaling-laws, transformer
|
|## [2026-06-16] ingest | Training language models to follow instructions with human feedback (InstructGPT)
|
|- Raw source: `raw/papers/2022-03-ouyang-instructgpt/` (2203.02155.pdf + index.md)
|- Source: https://arxiv.org/abs/2203.02155 — Long Ouyang et al., OpenAI, NeurIPS 2022
|- Content: RLHF fine-tuning applied to GPT-3 for instruction-following; three-step procedure (SFT → RM → PPO); 1.3B InstructGPT preferred to 175B GPT-3; truthfulness improvements, toxicity reduction, alignment tax mitigation via PPO-ptx
|- New tag: `rlhf` (already in SCHEMA.md taxonomy)
|- Created concept: rlhf (RLHF technique, three-step procedure, InstructGPT model family, alignment tax, PPO-ptx, key results)
|- Updated entity: dario-amodei (added InstructGPT to context: was VP of Research at OpenAI during this project)
|- Created entity: openai (organization page with key papers table, key people, known works)
|- Raw source added: raw/articles/openai-wikipedia.md (Wikipedia summary)
|- Cross-links: rlhf ↔ transformer, scaling-laws, chain-of-thought, dario-amodei, anthropic, flex-prompting, grace

## [2026-06-16] ingest | FlashAttention (Dao et al., Stanford, NeurIPS 2022)

- Raw source: `raw/papers/2022-05-dao-flashattention/` (2205.14135.pdf + index.md)
- Source: https://arxiv.org/abs/2205.14135 — "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
- Authors: Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré (Stanford / University at Buffalo)
- Venue: NeurIPS 2022
- Content: IO-aware exact attention algorithm using tiling to reduce GPU HBM↔SRAM reads/writes; online softmax for incremental block computation; O(N²d²/M) IO complexity proven optimal; block-sparse extension; 15% speedup on BERT-large, 3× on GPT-2, 2.4× on LRA; first Transformer to beat chance on Path-X (16K, 61.4%) and Path-256 (64K, 63.1%)
- Created concept: flash-attention (IO-aware principle, tiling algorithm, online softmax, IO complexity optimality, block-sparse extension, results table, relationship to sparse attention methods, adoption as default attention implementation)
- Updated concept: spargeattn (added source + 3 wikilinks: intro, Stage 1, Stage 2)
- Updated concept: transformer (added FlashAttention as practical breakthrough in Limitations)
- Updated concept: kv-caching (added wikilink entry)
- Updated concept: sparse-transformer (added wikilink entry in Relationship)
- Removed from TODO.md (was pending)
- Cross-links: flash-attention ↔ spargeattn, sparse-transformer, longformer, big-bird, kv-caching, transformer, mamba, chain-of-continuous-thought

## [2026-06-16] ingest | RoFormer: Rotary Position Embedding (Su et al., Zhuiyi Technology, arXiv 2021)

- Raw source: `raw/papers/2021-04-su-roformer/` (2104.09864.pdf + su2021rope.md)
- Source: https://arxiv.org/abs/2104.09864 — "RoFormer: Enhanced Transformer with Rotary Position Embedding"
- Authors: Jianlin Su, Yu Lu, Shengfeng Pan, Ahmed Murtadha, Bo Wen, Yunfeng Liu (Zhuiyi Technology Co., Ltd.)
- Venue: arXiv preprint, April 2021 (v5 Nov 2023)
- Content: Introduces Rotary Position Embedding (RoPE) — encodes absolute position via rotation matrices while incorporating explicit relative position dependency in self-attention. Multiplicative (not additive) position encoding with long-term decay, sequence-length flexibility, and linear attention compatibility. RoFormer achieves 27.5 BLEU on WMT EN-DE (+0.2 over Transformer-base), faster BERT MLM convergence, outperforms on 3/6 GLUE tasks. RoPE has become the dominant position encoding in virtually all post-2023 LLMs (LLaMA, Mistral, Qwen, Gemma).
- Created concept: rotary-position-embedding (mechanism, key properties — long-term decay, sequence-length flexibility, linear attention compatibility; empirical results table; relationship to sinusoidal PE, learned PE, relative bias, Transformer-XL styles; adoption in modern LLMs; limitations)
- Updated concept: positional-encoding (added Rotary Position Embedding section with cross-link, added wikilink in Cross-Links)
- Updated concept: transformer (added wikilink to rotary-position-embedding in Cross-Links)
- Removed from TODO.md (was pending)
- Cross-links: rotary-position-embedding ↔ positional-encoding, transformer, kv-caching, semantic-fractal, sparse-transformer

## [2026-06-16] ingest | Switch Transformers (Fedus et al., Google, JMLR 2022)

- Raw source: `raw/papers/2021-01-fedus-switch-transformers/` (2101.03961.pdf + fedus2022switch.md)
- Source: https://arxiv.org/abs/2101.03961 — "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity"
- Authors: William Fedus, Barret Zoph, Noam Shazeer (Google)
- Venue: Journal of Machine Learning Research 23 (2022) 1-40
- Content: Simplifies MoE to single-expert routing (k=1), enabling sparsely-activated models with constant compute cost but vastly more parameters. Up to 7× pre-training speedup over T5-Base, 4× over T5-XXL. Trained up to 1.6T parameter models. Introduces selective precision (bfloat16 + float32 router), smaller initialization, expert dropout. All 101 languages improved in multilingual setting.
- New tag: mixture-of-experts (added to SCHEMA.md Models taxonomy)
- Concept page created: switch-transformer (architecture, single-expert routing, load balancing loss, expert capacity, training stability techniques, scaling results, distillation, multilingual results, significance)
- Updated concept: transformer (added cross-link in Limitations — MoE as alternative scaling dimension)
- Updated concept: scaling-laws (added cross-link — expert count as orthogonal scaling dimension)
- Updated concept: sparse-transformer (added cross-link — attention sparsity vs parameter sparsity)
- Updated concept: kv-caching (added cross-link — MoE memory pressure vs KV cache wall)
- Updated comparison: slm-moe-agentic-ai (added raw source, added Switch Transformer as foundational MoE work in Ivanov MoE+MTP section, added cross-link in Related)
- Removed from TODO.md (was pending)
- Cross-links: switch-transformer ↔ transformer, scaling-laws, sparse-transformer, kv-caching, flash-attention, slm-moe-agentic-ai

## [2026-06-16] ingest | Direct Preference Optimization (Rafailov et al., Stanford, NeurIPS 2023)

## [2026-06-17] ingest | BERT (Devlin et al., Google, NAACL 2019)

- Raw source: `raw/papers/2018-10-devlin-bert/` (1810.04805.pdf + index.md)
- Source: https://arxiv.org/abs/1810.04805 — "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
- Authors: Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova (Google AI Language)
- Venue: NAACL 2019
- Content: Introduces BERT — bidirectional encoder-only Transformer pre-trained with Masked Language Model (15% tokens predicted) and Next Sentence Prediction objectives. BERT-Base (110M) and BERT-Large (340M). Achieves SOTA on 11 NLP tasks: GLUE 80.5% (+7.7%), SQuAD v1.1 93.2 F1 (+1.5), SQuAD v2.0 83.1 F1 (+5.1). Established pre-train/fine-tune paradigm; encoder-only architecture (no KV caching, non-generative); 512-token limit drove sparse-attention successors.
- Created concept: bert (bi-directional pre-training, MLM/NSP objectives, architecture table, training details, results summary, impact/legacy, limitations, related models)
- Updated concept: transformer (added wikilink to bert)
- Updated concept: kv-caching (added wikilink to bert)
- Updated concept: longformer (added wikilink to bert in both 512-limit reference and attention bias context)
- *Rewritten after full paper read:* raw/index.md expanded with per-task GLUE breakdown, SQuAD 2.0 approach, ablation results (bidirectionality, model size, feature-based), fine-tuning hyperparameters per task, BERT-Base vs OpenAI GPT controlled comparison, corpus choice rationale. Concept page rewritten with exact ablation numbers, GLUE table, SWAG/CoNLL NER results, and key paper claims attributed.

- Raw source: `raw/papers/2023-05-rafailov-dpo/` (2305.18290.pdf + rafailov2023dpo.md)
- Source: https://arxiv.org/abs/2305.18290 — "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
- Authors: Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn (Stanford University / CZ Biohub)
- Venue: NeurIPS 2023
- Content: Introduces Direct Preference Optimization (DPO) — reparameterises the RLHF objective to eliminate explicit reward modelling and RL loop. Key theoretical result: all reward equivalence classes under Bradley-Terry can be represented as r(x,y) = β·log(π/π_ref). DPO optimises the same KL-constrained reward maximisation objective as PPO-based RLHF using a simple binary cross-entropy loss. Achieves strictly better reward/KL frontier on IMDb sentiment; ~61% win rate on TL;DR summarisation (vs PPO ~57%); only efficient method to improve over chosen completions on Anthropic-HH dialogue. More robust to sampling temperature. Validated via human study (GPT-4↔human agreement ≈ human↔human agreement).
- Created concept: direct-preference-optimization (key insight — closed-form reward↔policy mapping, Bradley-Terry reparameterisation, Theorem 1, gradient analysis, results table, comparison with RLHF, known limitations)
- Updated concept: rlhf (added wikilink to direct-preference-optimization)
- Removed from TODO.md (was pending)
- Cross-links: direct-preference-optimization ↔ rlhf, instructgpt, transformer, flashattention, flex-prompting

## [2026-06-16] ingest | Neural Machine Translation of Rare Words with Subword Units (Sennrich, Haddow, Birch, ACL 2016)

- Raw source: `raw/papers/2016-06-sennrich-bpe-subword/` (1508.07909.pdf + sennrich2016bpe.md)
- Source: https://arxiv.org/abs/1508.07909 — "Neural Machine Translation of Rare Words with Subword Units"
- Authors: Rico Sennrich, Barry Haddow, Alexandra Birch (University of Edinburgh)
- Venue: ACL 2016
- Content: Introduces Byte Pair Encoding (BPE) for subword tokenization in NMT — adapting Gage (1994) compression algorithm to word segmentation. Demonstrates open-vocabulary NMT without back-off dictionaries. Two variants: independent BPE (separate source/target vocabularies) and joint BPE (union vocabulary). Achieves +1.1 BLEU (EN→DE) and +1.3 BLEU (EN→RU) over dictionary back-off baseline. Shows subword models learn compounding and transliteration.
- Created concept: byte-pair-encoding (algorithm, key properties, variants table, impact on rare word translation, limitations, relationship to other concepts)
- Updated concept: bert (added wikilink: WordPiece as BPE variant)
- Updated concept: big-bird (added wikilinks: BPE for DNA tokenization, BPE in Significance & Legacy)
- Updated index.md: added concept entry and raw source under Papers
- Removed from TODO.md (was pending)

## [2026-06-17] ingest | Okapi at TREC-3 — Robertson et al. (City University, TREC-3 1995)

- Raw source: `raw/papers/1995-01-robertson-okapi-trec3/` (okapi_trec3.pdf + robertson1995okapi.md)
- Source: https://www.microsoft.com/en-us/research/publication/okapi-at-trec-3/ — "Okapi at TREC-3"
- Authors: Stephen E. Robertson, S. Walker, S. Jones, M. M. Hancock-Beaulieu, M. Gatford (City University, London)
- Venue: Proceedings of the Third Text REtrieval Conference (TREC-3), NIST 1995
- Content: Describes the Okapi IR system participation in TREC-3. Introduces BM25 — unified term-weighting function combining BM11 and BM15 with tunable document length normalization b (optimal ~0.75). Demonstrates query expansion without relevance information (pseudo-relevance feedback from top R documents), run-time passage retrieval (best-matching paragraph sequences), and stepwise term selection for routing (incremental select-or-reject based on average precision improvement). Interactive search interface with phrase operators (ADJ) and term-set manipulation.
- Created concepts: bm25 (BM25 formulation, history from TREC-1→2→3, saturation property, length normalization, impact on search engines and RAG, limitations)
- Created entities: stephen-robertson (RSJ weight, BM25, Okapi, probabilistic IR, PRP), karen-sparck-jones (IDF, RSJ weight, probabilistic IR, academic legacy)
- Cross-links: bm25 ↔ stephen-robertson, karen-sparck-jones, retrieval-augmented-generation, knowledge-graph, byte-pair-encoding
- Updated index.md: added entities, concept, raw paper source

## [2026-06-17] ingest | Distilling the Knowledge in a Neural Network (Hinton, Vinyals & Dean, 2015)

- Raw source: raw/papers/2015-03-hinton-distillation/ (hinton2015distill.md + PDF)
- Source: https://arxiv.org/abs/1503.02531
- Authors: Geoffrey Hinton, Oriol Vinyals, Jeff Dean (Google Inc.)
- Created entity: geoffrey-hinton (backpropagation co-popularizer, knowledge distillation inventor, dropout co-author, Turing Award 2018, Nobel Prize in Physics 2024)
- Created concept: knowledge-distillation (temperature-based softmax, dark knowledge, soft targets as regularizers, specialist models, ensemble compression)
- Cross-links: knowledge-distillation ↔ geoffrey-hinton, backpropagation, switch-transformer, rlhf
- Updated TODO.md: removed both duplicate entries for this paper
- Updated index.md: added entity, concept, raw paper source, bumped total pages to 56

## [2026-06-17] ingest | Gaussian Error Linear Units (GELUs) (Hendrycks & Gimpel, 2016)

- Raw source: `raw/papers/2016-06-hendrycks-gelu/` (hendrycks2016gelu.md + PDF 1606.08415.pdf)
- Source: https://arxiv.org/abs/1606.08415
- Authors: Dan Hendrycks, Kevin Gimpel
- Created concept: gelu (activation function xΦ(x), probabilistic interpretation as stochastic regularizer expectation, smooth curvature, empirical gains over ReLU/ELU across vision, NLP, speech; SiLU/swish origin)
- Updated concept: bert (added GELU paper as source, wikilinked GELU activation in architecture section)
- Cross-links: gelu ↔ bert, transformer, residual-connection, backpropagation
- Updated index.md: added concept, raw paper source, bumped total pages to 57

## [2026-06-17] ingest | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer (Shazeer et al., 2017)

- Raw source: `raw/papers/2017-01-shazeer-sparsely-gated-moe/` (shazeer2017moe.md + 1701.06538.pdf)
- Source: https://arxiv.org/abs/1701.06538
- Authors: Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, Jeff Dean (Google Brain)
- Venue: ICLR 2017
- Content: Introduces the Sparsely-Gated Mixture-of-Experts (MoE) layer with up to thousands of feed-forward experts and a trainable gating network. Proposes Noisy Top-K Gating (gaussian noise + top-k sparsity), mixes data+model parallelism to solve the shrinking batch problem, uses importance and load losses for expert balancing. Achieves up to 137B parameters, SOTA on 1B Word Language Modeling (perplexity 28.0) and WMT'14 En→Fr translation (BLEU 40.42). Demonstrates expert specialization by syntax/semantics. Foundational paper for all subsequent MoE architectures (Switch Transformer, Mixtral, DeepSeek MoE, GPT-4).
- Created concept: mixture-of-experts (sparsely-gated architecture with noisy top-k gating, importance/load losses, hierarchical MoE, performance engineering; scaling properties, training/inference considerations, relationship to other concepts)
- Updated concept: switch-transformer (added Shazeer et al. as source, wikilinked to mixture-of-experts in intro and Significance & Legacy)
- Cross-links: mixture-of-experts ↔ switch-transformer, transformer, scaling-laws, knowledge-distillation, mamba, kv-caching, slm-moe-agentic-ai

## [2026-06-17] ingest | SentencePiece (Kudo & Richardson, 2018)

- Raw source: `raw/papers/2018-08-kudo-sentencepiece/` (kudo2018sentencepiece.md + 1808.06226.pdf)
- Source: https://arxiv.org/abs/1808.06226
- Authors: Taku Kudo, John Richardson (Google)
- Venue: EMNLP 2018 (demo paper)
- Content: Language-independent subword tokenizer training directly on raw Unicode without pre-tokenization. Implements BPE (O(N log N) via binary heap) and Unigram LM (probabilistic segmentation via EM, subword regularization). Lossless tokenization via whitespace-as-character (U+2581). Self-contained Protocol Buffer models with frozen Unicode normalizer.
- Created concept: sentencepiece (raw-text training, two-algorithm design, subword regularization, lossless encoding/decoding, adoption in T5/XLNet/ALBERT/Gemma)
- Updated concept: byte-pair-encoding (added wikilinks to sentencepiece in intro, Variants table rows for Unigram LM and SentencePiece, bumped updated date)
- Cross-links: sentencepiece ↔ byte-pair-encoding, transformer, bert, distributional-semantics
- Updated index.md: added concept entry and raw paper source, bumped total pages to 59

## [2026-06-17] update | paper raw sources unified format
- Rewrote all 26 raw/papers/*.md to a single uniform template:
  `frontmatter → blank → # Title → blank → **PDF:** link → blank → ## Abstract → blank → abstract text`
- Added missing h1 title headings from frontmatter `title:` field where absent
- Added missing **PDF:** links where PDF file existed in directory
- Converted wikilink `[[...pdf]]` references to proper `[...](...)` markdown links
- Stripped all extra sections (h2/h3) after Abstract — no conspectus, no summaries
- Exception: anthropic2022toy (HTML article, no PDF)

## [2026-06-17] ingest | What Does BERT Look At? An Analysis of BERT's Attention (Clark et al., 2019)

- Raw source: `raw/papers/2019-06-clark-bert-attention/` (clark2019bertattention.md + 1906.04341.pdf)
- Source: https://arxiv.org/abs/1906.04341
- Authors: Kevin Clark, Urvashi Khandelwal, Omer Levy, Christopher D. Manning (Stanford / Facebook AI Research)
- Venue: BlackBoxNLP 2019
- Content: Systematic analysis of BERT-base's 144 attention heads. Identifies three surface patterns (positional, delimiter-attending, broad-attending). Shows [SEP] attention as learned no-op via gradient analysis. Maps individual heads to specific dependency relations with high accuracy (det 94%, dobj 87%, pobj 76%, poss 81%, auxpass 83%). Head 5-4 achieves 65% coreference antecedent selection. Proposes attention-based probing classifiers: Attn+GloVe achieves 77 UAS on dependency parsing. Heads cluster by layer (same-layer heads have similar attention distributions).
- Created concept: bert-attention-analysis (surface patterns, syntactic head specialization table, coreference results, probing classifiers, head clustering, relationship to Voita et al. attention-head-pruning)
- Updated concept: bert (added Attention Analysis section with wikilink to bert-attention-analysis)
- Updated concept: attention-head-pruning (added cross-link to bert-attention-analysis in Cross-Links)
- Cross-links: bert-attention-analysis ↔ bert, attention-head-pruning, transformer, positional-encoding
- Updated index.md: added concept entry + raw paper source, bumped total pages to 61



- Raw source: `raw/papers/2019-05-voita-attention-heads/` (voita2019attention.md + 1905.09418.pdf)
- Source: https://arxiv.org/abs/1905.09418
- Authors: Elena Voita, David Talbot, Fedor Moiseev, Rico Sennrich, Ivan Titov (Yandex / UvA / Edinburgh)
- Venue: ACL 2019
- Content: Evaluates contribution of individual encoder self-attention heads to Transformer NMT performance. Uses LRP for head importance ranking. Identifies three interpretable head functions: positional (adjacent token), syntactic (dependency relations nsubj/dobj/amod/advmod), and rare words (first-layer head pointing to least frequent tokens). Introduces pruning method based on Hard Concrete L0 relaxation — stochastic gates per head with differentiable regularization. Key results: 38/48 encoder heads pruned on EN-RU WMT with only 0.15 BLEU drop; 44/48 on OpenSubtitles with 0.25 BLEU drop. Specialized heads are last to be pruned. Encoder self-attention is most redundant; decoder-encoder attention most critical. Pruned architectures cannot be trained from scratch to same quality.
- Created concept: attention-head-pruning (head functions, L0-relaxation pruning method, results, function drift under pruning)
- Updated concept: transformer (added wikilink to attention-head-pruning in Cross-Links section)
- Cross-links: attention-head-pruning ↔ transformer, kv-caching, sparse-transformer, knowledge-distillation
- Updated index.md: added concept entry + raw paper source + fixed accumulated pipe contamination; bumped total pages to 60
|
|## [2026-06-17] ingest | Multi-Query Attention (Shazeer, 2019)
|
|- Raw source: `raw/papers/2019-11-shazeer-multi-query-attention/` (shazeer2019multiquery.md + 1911.02150.pdf)
|- Source: https://arxiv.org/abs/1911.02150
|- Authors: Noam Shazeer (Google)
|- Venue: arXiv preprint (cs.NE), November 2019
|- Content: Proposes Multi-Query Attention (MQA), a Transformer attention variant where keys and values are shared across all attention heads, while queries retain per-head projections. Identifies that incremental autoregressive decoding is memory-bandwidth bound (ratio Θ(n/d + 1/b)) due to repeatedly loading large per-head K/V tensors. MQA eliminates the heads dimension from K/V, reducing the memory ratio to Θ(1/d + d/(hn) + 1/b) — a factor of h improvement. Evaluation on WMT14 EN-DE: BLEU 27.5/28.5 (greedy/beam-4) vs baseline 27.7/28.4. Decoder speedup: 12× greedy (46→3.8 µs/tok), 6.3× beam search (203→32 µs/tok) on TPUv2. Training speed unchanged. Multi-query attention orthogonal to local (sliding-window) attention. Simply reducing h or d_k/d_v hurts quality far more than MQA. Laid foundation for Grouped-Query Attention (GQA) used in LLaMA 2/3, Mistral, and modern LLMs.
|- Created concept: multi-query-attention (memory-bandwidth analysis, shared K/V projections, performance table and speedup results, comparison with h/d_k/d_v reduction, relationship to GQA)
|- Updated concept: kv-caching (added MQA as architectural origin of KV cache memory-bandwidth bottleneck analysis and as a solution reducing KV cache size by factor h)
|- Updated concept: transformer (added cross-link to multi-query-attention in Cross-Links)
|- Cross-links: multi-query-attention ↔ kv-caching, transformer, attention-head-pruning, flash-attention, sparse-transformer
|- Updated index.md: added concept entry + raw paper source, bumped total pages to 62

## [2026-06-17] ingest | GLU Variants Improve Transformer (Shazeer, 2020)

- Raw source: `raw/papers/2020-02-shazeer-glu-variants/` (shazeer2020gluvariants.md + 2002.05202.pdf)
- Source: https://arxiv.org/abs/2002.05202
- Author: Noam Shazeer (Google)
- Venue: arXiv preprint (cs.LG), February 2020
- Content: Proposes applying Gated Linear Unit variants (GLU, Bilinear, ReGLU, GEGLU, SwiGLU) to the Transformer feed-forward sublayer. GLU variants use 3 weight matrices (vs 2 for standard FFN), with hidden size reduced by 2/3 to match parameters. GEGLU and SwiGLU achieve best pre-training perplexity (1.633 and 1.636 vs ReLU baseline 1.677 at 524K steps). GLU variants dominate downstream GLUE/SuperGLUE/SQuAD. SwiGLU became the default FFN activation in virtually all post-2022 LLMs (LLaMA, PaLM, Gemma, Mistral, Qwen).
- Created concept: glu-variants (GLU definitions, architectural difference, parameter-matched setup, perplexity/results tables, impact section, limitations)
- Created entity: noam-shazeer (Google researcher; co-inventor of Transformer, MoE, MQA, GLU variants, Switch Transformer, Adafactor)
- Updated concept: transformer (added cross-link to glu-variants in Cross-Links)
- Updated concept: gelu (added cross-link to glu-variants in Cross-Links)
- Cross-links: glu-variants ↔ transformer, gelu, multi-query-attention, switch-transformer, mixture-of-experts
- Updated index.md: added concept entry + entity entry + raw paper source, bumped total pages to 64

## [2026-06-17] ingest | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., FAIR, NeurIPS 2020)

- Raw source: `raw/papers/2020-05-lewis-rag/` (2005.11401.pdf + index.md)
- Source: https://arxiv.org/abs/2005.11401
- Authors: Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela (Facebook AI Research / UCL / NYU)
- Venue: NeurIPS 2020
- Content: Introduces Retrieval-Augmented Generation (RAG) — combining pre-trained parametric memory (BART-large seq2seq) with non-parametric memory (DPR dense vector index of 21M Wikipedia chunks). Two formulations: RAG-Sequence (same document for whole output) and RAG-Token (different document per token). SOTA on Natural Questions (44.5 EM), WebQuestions (45.5/45.2 EM), CuratedTrec (52.2/50.0 EM). RAG generates more factual, specific, diverse text than parametric-only BART baseline. Non-parametric memory hot-swappable without retraining. Retrieval collapse observed on knowledge-light tasks (story generation). Open-sourced via HuggingFace Transformers.
- Updated concept: retrieval-augmented-generation (added Original Paper section with architecture, two formulations, results, retrieval collapse, legacy; added paper as second source to frontmatter)
- Cross-links: retrieval-augmented-generation ↔ bm25, bert, word-embeddings, distributional-semantics, grace, hallucination-detection-slm, mamba (existing cross-links deepened; DPR + BART as plain-text references)
- Updated index.md: updated concept entry description, added raw paper source under Papers
