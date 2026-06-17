---
title: Okapi at TREC-3
source_url: https://www.microsoft.com/en-us/research/publication/okapi-at-trec-3/
authors:
  - Stephen E. Robertson
  - S. Walker
  - S. Jones
  - M. M. Hancock-Beaulieu
  - M. Gatford
date: 1995-01
venue: Proceedings of the Third Text REtrieval Conference (TREC-3), NIST
ingested: 2026-06-17
---

## Abstract

The Okapi IR system's evolution across TREC conferences is described, with emphasis on TREC-3 work: refinement of term-weighting functions (leading to BM25), run-time passage determination and searching, query expansion using top-ranked documents from a trial search, new methods for ranking and selecting expansion terms after relevance feedback, and development of an interactive search interface. The two major successes were query expansion and routing term selection. Modified weighting functions and passage retrieval had small beneficial effects, but combined they substantially compensated for the loss of CONCEPTS fields in TREC-3 topics.

## Key Contributions

1. **BM25 (Best Match 25)** — unified term-weighting function combining BM11 (verbosity hypothesis) and BM15 into a single parameterized function with document length normalization controlled by parameter b (optimal ~0.75)
2. **Query expansion without relevance information** — using top R documents from a trial BM25 search as pseudo-relevance feedback source; unexpectedly successful for TREC-3 ad hoc, compensating for missing CONCEPTS fields
3. **Run-time passage retrieval** — algorithmically determining best-matching sub-document passages (paragraph sequences) at search time rather than using pre-defined passages; modest gains alone but significant in combination with query expansion
4. **Stepwise term selection for routing** — select-or-reject procedure building query term sets by incrementally adding terms and accepting only those that improve average precision on the training set; computationally expensive but highly effective
5. **Interactive routing interface** — X-windows command-driven interface with term-set definition, phrase (adjacency) operators, relevance feedback term extraction, and manual term removal

## BM25 Formulation

The Robertson-Sparck Jones weight:

$$ w^{(1)} = \log \frac{(r+0.5)/(R-r+0.5)}{(n-r+0.5)/(N-n-R+r+0.5)} $$

reduces to inverse collection frequency (ICF) when no relevance information is available (R=r=0).

BM25 combines BM11 and BM15 into a single function with term frequency component:

$$ \frac{tf^c}{K + tf^c} \quad\text{where}\quad K = k_1 \left( (1-b) + b \cdot \frac{dl}{avdl} \right) $$

- c=1, b=1 ⇒ BM11 (verbosity hypothesis, strong document length effect)
- b=0 ⇒ BM15 (no document length normalization)
- b≈0.75 gives best results in practice

Plus within-query frequency factor: $qtf/(k_3+qtf)$ and a global document length correction.

## Results Summary

| Run | Conditions | AveP | P30 |
|-----|-----------|------|-----|
| citya2 (baseline) | BM25, unexpanded | 0.337 | 0.590 |
| citya1 | BM25 + passages + expansion (T=40, R=30) | 0.401 | 0.625 |
| best routing (cityr1) | optimized, maxterms=30 | 0.425 | 0.603 |
| interactive (cityi1) | BM11, searcher-derived | 0.250 | 0.445 |

## System

- **Hardware**: Sun SS10 (64 MB RAM, ~12 GB disk) + two additional Suns
- **Software**: Basic Search System (BSS) in C, with awk/perl scripts
- **Database**: TREC disks 1&2, disk 3; paragraph information retained; 3-field structure (DOCNO, display-only, searchable text)

## Legacy

BM25 became the dominant term-weighting function in information retrieval, adopted by Lucene/Solr (2015+), Elasticsearch (2016+), and virtually all modern search engines. The pseudo-relevance feedback technique (query expansion from top-N retrieved documents) became a standard method in IR and is conceptually ancestral to modern RAG relevance feedback loops. The passage retrieval approach anticipated modern document chunking strategies.

## Full text

PDF: [okapi_trec3.pdf](okapi_trec3.pdf) — 14 pages, 340 KB.
