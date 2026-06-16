---
title: Byte Pair Encoding (BPE)
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [technique, model, architecture]
sources:
- "[Neural Machine Translation of Rare Words with Subword Units](raw/papers/2016-06-sennrich-bpe-subword/sennrich2016bpe.md)"
---

Byte Pair Encoding (BPE) is a subword tokenization algorithm that learns a fixed-size vocabulary of variable-length character sequences from data. Introduced to neural machine translation by ([Sennrich, Haddow & Birch, ACL 2016](raw/papers/2016-06-sennrich-bpe-subword/sennrich2016bpe.md)), BPE adapts a data compression technique from Gage (1994): iteratively merging the most frequent pair of adjacent symbols, building a vocabulary from characters up through frequent character n-grams to whole words.

BPE became the dominant tokenization method for virtually all post-2018 neural language models — including [[gpt|GPT]], [[bert|BERT]], [[roberta|RoBERTa]], [[t5|T5]], and [[llama|LLaMA]] — and remains the foundation of most modern LLM tokenizers, despite later refinements like WordPiece, Unigram, and SentencePiece.

## Algorithm

BPE for text tokenization proceeds as follows:

1. **Initialise vocabulary** with the set of all individual characters that appear in the corpus, plus an end-of-word marker (`</w>`)
2. **Tokenise the corpus** as sequences of these atomic symbols per word
3. **Count all adjacent symbol pairs** across the entire corpus (weighted by word frequency)
4. **Merge the most frequent pair** (A, B) into a new symbol 'AB', adding it to the vocabulary
5. **Repeat step 3–4** until the desired vocabulary size is reached (the only hyperparameter)

The final vocabulary size = initial character vocabulary + number of merge operations. At test time, unseen words are segmented by applying the learned merge operations in order — starting from characters and greedily merging. This guarantees open-vocabulary encoding with a fixed symbol set.

## Key Properties

- **Open-vocabulary:** any word can be represented, even if never seen during training
- **Fixed-size vocabulary:** the number of merge operations controls the trade-off between vocabulary size and sequence length
- **Variable-length units:** subword spans range from single characters to whole words, allowing the attention mechanism to allocate computation where needed
- **Interpretable merges:** unlike Huffman coding, the merged symbols remain human-readable subword units
- **Deterministic:** given the same merge operations, segmentation is deterministic and reversible

## Variants

| Variant | Description | Used By |
|---------|-------------|---------|
| **Independent BPE** | Separate vocabularies learned for source and target languages | Standard in NMT research |
| **Joint BPE** | Single vocabulary learned on the union of source and target text, improving cross-lingual segmentation consistency | Sennrich et al. (2016), best results in paper |
| **WordPiece** | Similar merge principle but merges based on likelihood gain under a language model, not raw frequency | [[bert\|BERT]], [[roberta\|RoBERTa]] |
| **Unigram LM** | Probabilistic subword model trained via EM, selects vocabulary by removing low-probability units | SentencePiece (Kudo & Richardson, 2018), T5, LLaMA |
| **SentencePiece** | Framework supporting both BPE and Unigram; operates on raw text without pre-tokenization | [[by-t5|ByT5]], [[gemma|Gemma]] |

## Impact on Translation of Rare Words

The critical insight of the original BPE paper is that word classes challenging for word-level NMT — names, compounds, cognates, loanwords, morphologically complex forms — are translatable through smaller units. An analysis of 100 rare German tokens found 56 compounds, 21 names, 6 loanwords, 5 transparent affixations, 1 number, and 1 programming-language identifier — all potentially decomposable into subword units ([Sennrich, Haddow & Birch, 2016](raw/papers/2016-06-sennrich-bpe-subword/sennrich2016bpe.md)).

For [[English]]→[[German]], the BPE-ensemble improved OOV recall from 0% (word-level with UNK) to ~30%, with joint BPE reaching 38.6% precision and 29.8% recall. For English→Russian (different alphabets), BPE was essential: the back-off dictionary baseline achieved only 5.2% OOV recall, while BPE-J90k reached 15.6% recall and 21.9% precision.

## Limitations

- **Suboptimal for character-level tasks:** BPE's variable-length units can mask character-level patterns needed for spelling-sensitive tasks
- **Segmentation inconsistency:** the same word can be segmented differently in source vs target when using independent BPE, complicating transliteration learning
- **No language-universal guarantee:** joint BPE improves consistency but cannot fully resolve alphabet mismatches (Sennrich et al. used ISO-9 transliteration as a workaround)
- **Hyperparameter sensitivity:** optimal vocabulary size depends on language pair, corpus size, and task — no automatic criterion in the original formulation
- **Oversplitting robustness:** BPE can produce linguistically implausible segmentations (e.g., `Forsch|ungsinstitu|ten` rather than `Forschungs|instituten`), but NMT models show surprising robustness to such splits

## Relationship to Other Concepts

BPE operates on a fundamentally different axis from architectural innovations like [[transformer|Transformer]], [[kv-caching|KV Caching]], or [[flash-attention|FlashAttention]]: it changes the input representation rather than the computation. It is complementary to:

- **[[word-embeddings|Word Embeddings]]** — BPE replaces word-level embeddings with subword-level representations
- **[[bert|BERT]]** — uses WordPiece, a BPE variant with likelihood-based merge criterion
- **[[big-bird|BigBird]]** — applied BPE for DNA sequence tokenization (32K vocab, ~8.78 bp/token)
- **[[vibe-coding|Vibe Coding]]** — tokenization choice affects how the LLM "sees" code (whitespace, punctuation, variable names)
- **[[semantic-fractal|Semantic Fractal]]** — BPE's variable-length units interact with the positional encoding geometry in ways that affect the line-number problem

## References

- Sennrich, R., Haddow, B., & Birch, A. (2016). *Neural Machine Translation of Rare Words with Subword Units.* ACL 2016. [[raw/papers/2016-06-sennrich-bpe-subword/sennrich2016bpe.md]]
- Gage, P. (1994). *A New Algorithm for Data Compression.* C Users J., 12(2):23–38.
- Kudo, T. & Richardson, J. (2018). *SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing.*
