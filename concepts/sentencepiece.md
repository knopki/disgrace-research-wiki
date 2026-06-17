---
title: SentencePiece
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [technique, data, architecture]
sources:
- "[SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing](raw/papers/2018-08-kudo-sentencepiece/kudo2018sentencepiece.md)"
---

SentencePiece is a language-independent subword tokenizer and detokenizer for neural text processing, introduced by Taku Kudo and John Richardson (Google, EMNLP 2018). It enables purely end-to-end subword modeling by training directly on raw Unicode sequences without language-specific pre-tokenization.

## Key Innovations

### Raw-Text Training

Unlike earlier subword toolkits (subword-nmt, WordPiece), SentencePiece does not require whitespace-based pre-tokenization. It treats input as a raw character stream and escapes whitespace as `_` (U+2581), making it fully language-independent — a single model handles Chinese (no word boundaries), German (compounds), English, and Japanese alike.

### Two Subword Algorithms

SentencePiece implements two segmentation approaches:

- **[[byte-pair-encoding|BPE]]:** greedy merging of most frequent adjacent character pairs, with O(N log N) complexity via binary heap.
- **Unigram Language Model:** probabilistic segmentation trained via Expectation-Maximization. The vocabulary is built by starting with a large set of candidate subwords and iteratively removing those whose removal least reduces corpus likelihood. This enables **subword regularization** — sampling different segmentations during training as a form of data augmentation controlled by a temperature parameter.

### Lossless Tokenization

The encoder-decoder pair is a true inverse: `Decode(Encode(Normalize(text))) = Normalize(text)`. Whitespace is preserved in the encoded representation, so decoding is a simple concatenation — unlike the `@@` boundary markers used by subword-nmt, which are not fully reversible for consecutive whitespace.

### Self-Contained Models

The model file (Protocol Buffer) bundles vocabulary, segmentation parameters, and a pre-compiled Unicode normalizer (default: NFKC) into a single artifact with no external dependencies. This guarantees deterministic reproduction regardless of the runtime environment.

## Adoption

SentencePiece became the default tokenizer for a generation of [[transformer|Transformer]] models:

- **[[bert|T5]]** (Text-to-Text Transfer Transformer) — used Unigram LM mode
- **XLNet** — autoregressive pretraining with permutation language modeling
- **ALBERT** — parameter-efficient BERT variant
- **ByT5, Gemma** — continued use in Google's later models

It is the most widely deployed subword tokenization library in the post-BERT era, and its two-algorithm design (BPE + Unigram) made it the standard framework for tokenization research.

## Relationship to Other Concepts

- **[[byte-pair-encoding|Byte Pair Encoding (BPE)]]** — SentencePiece is the reference implementation of BPE for neural models, alongside its own Unigram LM approach. Earlier toolkits like subword-nmt used `@@` boundary markers and required pre-tokenization; SentencePiece eliminated both limitations.
- **[[transformer|Transformer]]** — almost all major Transformer-based language models of 2019–2024 use SentencePiece for tokenization.
- **[[bert|BERT]]** — BERT uses WordPiece (a BPE variant with likelihood-based merges), while later encoder-decoder models like T5 standardised on SentencePiece. This represents a shift from frequency-based (BPE) to probability-based (Unigram LM) segmentation.
- **[[distributional-semantics|Distributional Semantics]]** — subword tokenization interacts with distributional semantics at the boundary level: coarser tokenization collapses distributional contexts, while finer tokenization preserves morpheme-level distinctions.

## References

- Kudo, T. & Richardson, J. (2018). *SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing.* EMNLP 2018 (demo paper). [[raw/papers/2018-08-kudo-sentencepiece/kudo2018sentencepiece.md]]
