---
title: Positional Encoding
created: 2026-06-17
updated: 2026-06-16
type: concept
tags:
  - architecture
  - model
  - training
sources:
  - "[Attention Is All You Need](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md)"
  - "[Позиционные кодировки: «объемное зрение» GPT и секреты AI-агентов](raw/articles/2025-07-04-ivanov-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/ivanoc2025encodings.md)"
confidence: high
---

# Positional Encoding

Positional Encoding (PE) is a technique that injects token order information into the [[transformer|Transformer]] architecture, which otherwise processes all tokens in parallel and has no inherent notion of sequence position. Beyond simple indexing, sinusoidal PE creates a multi-scale coordinate system that gives the model "3D semantic vision" — the ability to perceive nested structural hierarchies in text and code simultaneously.

## Why Positional Encoding Exists

The Transformer processes all tokens in a single parallel pass via self-attention. Unlike [[lstm|LSTM]] or RNNs, it has no sequential state. Without position information, the bag-of-words permutation-invariance problem is fatal: "dog bit man" and "man bit dog" produce identical representations. PE solves this by adding a position-dependent signal to each token's embedding before the first attention layer. ([Ivanov, 2025](raw/articles/2025-07-04-ivanov-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/ivanoc2025encodings.md))

## Sinusoidal Geometry

The original "Attention Is All You Need" paper proposed sine and cosine functions at varying frequencies: ([Vaswani et al., 2017](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md))

- **Position through phase.** Each dimension `i` of the encoding vector uses a wave with a unique frequency. The sin/cos value at position `pos` is the token's **phase** on that wave, encoding where it falls in a structure of that wavelength.
- **Proximity through angle.** Two tokens at a fixed distance `k` have the same angle between their PE vectors regardless of absolute position, letting the model learn relational patterns like "the word three positions after this one."
- **Nesting through frequency bands.** The model uses hundreds of waves with periods ranging from ~2 tokens to thousands of tokens simultaneously, enabling it to see position at multiple scales at once:
  - Low-frequency (long period) waves encode position at the **chapter** level
  - Mid-frequency waves encode position at the **paragraph** level
  - High-frequency (short period) waves encode position at the **sentence** level

Because a single token's PE vector contains values for all these frequencies simultaneously, it carries position information across every level of the hierarchy — creating a [[semantic-fractal|Semantic Fractal]]: a self-similar, multi-scale representation of text structure.

## Rotary Position Embedding (RoPE)

The dominant position encoding in modern LLMs (LLaMA, Mistral, Qwen, Gemma) is not additive sinusoidal PE but **[[rotary-position-embedding|Rotary Position Embedding (RoPE)]]**. Introduced by Su et al. (2021), RoPE encodes absolute position via a rotation matrix applied to query and key vectors, which naturally encodes relative position in the attention score without explicit relative embeddings.

Unlike additive PE, RoPE is:
- **Multiplicative** — the rotation is applied to q and k, not added to the input embedding
- **Length-unbounded** — any position can be encoded without interpolation
- **Compatible with linear attention** — rotation preserves norms, enabling relative position encoding in PerFormer-style linear mechanisms

RoPE has superseded sinusoidal PE as the default choice in most Transformer architectures since 2023. See the [[rotary-position-embedding|RoPE concept page]] for full mechanism, properties, and empirical results. ([Su et al., 2021](raw/papers/2021-04-su-roformer/su2021rope.md))

## Fusion with Semantic Embeddings

Crucially, PE is **not** appended as separate dimensions — it is **added directly** to the token's semantic embedding vector. The resulting vector that enters the first attention layer is a fused representation containing both *what* the token means and *where* it sits in the text hierarchy. This means position and semantics are entangled from the start, not processed separately. ([Ivanov, 2025](raw/articles/2025-07-04-ivanov-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/ivanoc2025encodings.md))

## Code as Nested Structure

PE's multi-scale nature is especially powerful for code. To the model, code is not a flat sequence of lines but a deeply nested structure analogous to an Abstract Syntax Tree (AST), but more flexible:

- A token like `library_name` in `print(f"{library_name}: ...")` has a position at the character level
- That `print` call sits inside an `else` block
- The `if/elif/else` construct lives inside a `try` block
- The `try` block is inside function `print_library_version`

GPT sees all these nesting levels simultaneously, understanding that `library_name` is simultaneously a function argument, a `try`-block local, and part of a format string in an `else` branch. This makes competitive programming (Codeforces-level) problems trivial for LLMs.

## The Line-Number Problem

The same "3D vision" that makes code understanding effortless creates a surprising weakness: **LLMs are bad at line numbers**. A line number is a flat, human-centric abstraction. For a model that thinks in nested semantic coordinates, "replace line 25" is nearly meaningless — that coordinate doesn't exist in its internal space. ([Ivanov, 2025](raw/articles/2025-07-04-ivanov-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/ivanoc2025encodings.md))

This is why tools like Cursor generate patches as semantic descriptions ("find the `validatePassword` call inside the hash-check block") rather than line-number diffs. It also motivates the [[semantic-anchors|Semantic Anchors]] technique — placing stable, unique markers in code that give the model reliable semantic coordinates for patch application.

## Cross-Links

- [[transformer|Transformer]] — the architecture that requires PE
- [[semantic-fractal|Semantic Fractal]] — the multi-scale nested structure PE creates in the model's internal representation
- [[semantic-anchors|Semantic Anchors]] — a technique that exploits PE's weaknesses for reliable code patching
- [[word-embeddings|Word Embeddings]] — PE is added to embeddings, so understanding embeddings is prerequisite
- [[vibe-coding|Vibe Coding]] — the paradigm shift enabled by AI's structural understanding of code, of which PE is a foundational component
- [[grace|GRACE]] — the GRACE framework's semantic anchors address the line-number problem that PE creates; XML-like paired tags leverage PE's ability to correlate identical tokens across large distances to overcome sparse attention degradation
- [[sparse-transformer|Sparse Transformer]] — contrasts with sinusoidal PE: Sparse Transformer uses learned position embeddings (data-dim for images, attention-dim for text) instead of fixed sinusoidal encodings
- [[rotary-position-embedding|Rotary Position Embedding (RoPE)]] — the dominant modern position encoding, using rotation matrices instead of additive sinusoidal functions