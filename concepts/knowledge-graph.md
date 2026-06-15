---
title: Knowledge Graph
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [technique, data, knowledge-graph]
sources:
  - "[Knowledge Graph (Google) — Wikipedia](raw/articles/knowledge-graph-google-wikipedia/index.md)"
confidence: high
---

# Knowledge Graph

A **knowledge graph** is a structured representation of entities (people, places, concepts, objects) and the relationships between them, organised as a graph of interconnected facts. Unlike document retrieval, which returns unstructured text chunks, a knowledge graph returns ground-truth triples — structured facts that can be composed, traced, and verified.

Knowledge graphs are one of two dominant approaches to grounding AI-generated answers in external knowledge, the other being [[retrieval-augmented-generation|Retrieval-Augmented Generation (RAG)]].

## Google's Knowledge Graph

The canonical large-scale implementation. Announced May 16, 2012 as a way to serve direct answers in Google Search results via knowledge panels (infoboxes).

### Scale

| Metric | Value |
|--------|-------|
| Entities at launch (+7 months, 2012) | 570 million |
| Facts at launch (+7 months) | 18 billion |
| Facts by mid-2016 | 70 billion |
| Entities by May 2020 | 5 billion |
| Facts by May 2020 | 500 billion |
| Searches with knowledge boxes (May 2016) | ~1/3 of 100B monthly searches |

### Data Sources

- **Wikipedia** — primary source for entity descriptions and infobox data
- **CIA World Factbook** — factual data about countries (discontinued Feb 2026)
- **Freebase** — crowd-sourced knowledge base; powered the initial Graph
- Automated generation from web crawl (places, people, businesses)

### Knowledge Vault

A separate research project (reported Aug 2014) that automatically extracted facts from the entire web, reaching 1.6 billion collected facts, of which 271 million had >90% confidence. Key difference from the Knowledge Graph: Knowledge Vault was fully automated, while the Graph relied on curated/crowd-sourced sources. The Vault's confidence scoring (factoring source text pattern, page PageRank, domain authority) prefigures modern LLM-based fact extraction.

## Knowledge Graph vs. RAG

| Dimension | Knowledge Graph | RAG |
|-----------|----------------|-----|
| Retrieval target | Structured facts (triples) | Unstructured text chunks |
| Query semantics | Entity + relation resolution | Semantic similarity (embeddings) |
| Response type | Direct fact (single/aggregated) | Generated prose grounded in context |
| Attribution | Historically poor (Google panels lack citations) | Can cite source chunks |
| Update mechanism | Graph maintenance pipeline | Re-index document corpus |
| Latency | Fast (indexed facts) | Slower (retrieval + generation) |

The two approaches are not mutually exclusive — hybrid architectures use a KG to retrieve precise facts and RAG for contextual synthesis. ^[raw/articles/knowledge-graph-google-wikipedia/index.md]

## Criticism of Google's Implementation

- **Lack of source attribution** — knowledge panels present facts without citations, undermining verifiability. Described as "as unsourced and absolute as if handed down by God" (The Washington Post)
- **Wikipedia traffic decline** — knowledge panels caused significant Wikipedia readership drops despite sourcing data from Wikipedia. Dariusz Jemielniak (2020) argued this reduces Wikipedia's ability to raise funds and attract volunteers
- **Algorithmic bias** — inconsistent entity coverage (2014: no Jesus panel vs. Moses/Muhammad/Buddha); high-SEO sources can inject misinformation (2021: Kannada labelled "ugliest language in India")

## See Also

- [[retrieval-augmented-generation|Retrieval-Augmented Generation (RAG)]] — the alternative grounding paradigm
- [[distributional-semantics|Distributional Semantics]] — theoretical basis for entity embeddings in knowledge graphs
- [[word-embeddings|Word Embeddings]] — how entities are represented as vectors in graph space
