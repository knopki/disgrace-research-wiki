---
title: Neural Machine Translation of Rare Words with Subword Units
source_url: https://arxiv.org/abs/1508.07909
authors:
  - Rico Sennrich
  - Barry Haddow
  - Alexandra Birch
date: 2016-06-10
venue: ACL 2016
ingested: 2026-06-16
---

## Abstract

Neural machine translation (NMT) models typically operate with a fixed vocabulary, but translation is an open-vocabulary problem. Previous work addresses the translation of out-of-vocabulary words by backing off to a dictionary. In this paper, we introduce a simpler and more effective approach, making the NMT model capable of open-vocabulary translation by encoding rare and unknown words as sequences of subword units. This is based on the intuition that various word classes are translatable via smaller units than words, for instance names (via character copying or transliteration), compounds (via compositional translation), and cognates and loanwords (via phonological and morphological transformations). We discuss the suitability of different word segmentation techniques, including simple character n-gram models and a segmentation based on the byte pair encoding compression algorithm, and empirically show that subword models improve over a back-off dictionary baseline for the WMT 15 translation tasks English→German and English→Russian by up to 1.1 and 1.3 BLEU, respectively.

## Key Contributions

1. First application of Byte Pair Encoding (BPE) to subword segmentation for NMT — adapted from Gage (1994) compression algorithm
2. Demonstration that open-vocabulary NMT is achievable by encoding rare/unknown words as variable-length subword sequences, eliminating the need for back-off dictionaries
3. Two BPE variants: independent encoding (separate source/target vocabularies) and joint encoding (union vocabulary for consistent segmentation)
4. Empirical validation: WMT 2015 EN→DE and EN→RU, up to +1.1 and +1.3 BLEU over dictionary back-off baseline
5. Analysis of different segmentation strategies: character n-grams, Morfessor, compound splitting, hyphenation, BPE

## Architecture

The paper follows the Bahdanau et al. (2015) attention-based NMT architecture: bidirectional GRU encoder, GRU decoder with attention. No architectural modifications — contribution is entirely in the representation layer (subword units replacing word units).

## BPE Algorithm

BPE iteratively replaces the most frequent pair of characters/character sequences with a new symbol. Steps:

1. Initialize vocabulary with character-level representation of words (plus end-of-word marker `</w>`)
2. Count all adjacent symbol pairs across word-tokenized corpus
3. Replace the most frequent pair ('A','B') with a new symbol 'AB'
4. Repeat until desired vocabulary size is reached
5. Final vocabulary size = initial character vocabulary + number of merge operations

Key properties: fixed-size vocabulary, open-vocabulary encoding at test time, variable-length subword units, interpretable merges.

## Results

| System | EN→DE BLEU | EN→DE CHR F3 | EN→RU BLEU | EN→RU CHR F3 |
|--------|-----------|-------------|-----------|-------------|
| WDict (word + back-off dict) | 24.2 | 52.4 | 22.8 | 51.0 |
| C2-50k (char bigram + 50k shortlist) | 25.3 | 53.5 | 24.1 | 51.6 |
| BPE-60k (independent) | 24.5 | 53.9 | 23.6 | 52.7 |
| BPE-J90k (joint) | 24.7 | 54.1 | 24.1 | 53.0 |

All ensemble (8 models) results. BPE-J90k achieves best CHR F3 across both language pairs. C2-50k best BLEU for EN→DE. Subword models particularly effective for OOV transliteration between different alphabets (EN→RU).

## Legacy

This paper established BPE as the dominant subword tokenization method for neural NLP. BPE (and its successor SentencePiece, Kudo & Richardson 2018) became the standard tokenization in GPT, BERT, RoBERTa, T5, LLaMA, and virtually all subsequent transformer-based models. The concept of learning a fixed-size vocabulary of variable-length subword units from data eliminated the closed-vocabulary bottleneck that plagued word-level models.

## Full text

PDF: [1508.07909.pdf](1508.07909.pdf) — 7 pages, 189 KB.
