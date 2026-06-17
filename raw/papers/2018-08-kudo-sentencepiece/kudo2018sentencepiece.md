---
title: SentencePiece — A simple and language independent subword tokenizer and detokenizer for Neural Text Processing
authors:
  - Taku Kudo
  - John Richardson
source_url: https://arxiv.org/abs/1808.06226
date: 2018-08-18
venue: EMNLP 2018 (demo paper)
description: SentencePiece is a language-independent subword tokenizer and detokenizer for neural text processing. It trains subword models directly from raw sentences without pre-tokenization, supporting both byte-pair-encoding (BPE) and unigram language model segmentation. Provides open-source C++ and Python implementations under Apache 2.0 license.
ingested: 2026-06-17
---

**PDF:** [1808.06226.pdf](1808.06226.pdf)

## Abstract

This paper describes SentencePiece, a language-independent subword tokenizer and detokenizer designed for Neural-based text processing, including Neural Machine Translation. It provides open-source C++ and Python implementations for subword units. While existing subword segmentation tools assume that the input is pre-tokenized into word sequences, SentencePiece can train subword models directly from raw sentences, which allows us to make a purely end-to-end and language independent system. We perform a validation experiment of NMT on English-Japanese machine translation, and find that it is possible to achieve comparable accuracy to direct subword training from raw sentences. We also compare the performance of subword training and segmentation with various configurations. SentencePiece is available under the Apache 2 license at <https://github.com/google/sentencepiece>.
