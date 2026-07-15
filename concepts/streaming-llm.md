---
title: StreamingLLM and Attention Sinks
created: 2026-07-15
updated: 2026-07-15
type: concept
tags: [inference, serving, technique]
sources:
- "[Efficient Streaming Language Models with Attention Sinks](raw/papers/2023-09-xiao-streamingllm/xiao2023streamingllm.md)"
---

# StreamingLLM and Attention Sinks

## Attention sink phenomenon

Autoregressive LLMs concentrate a surprisingly large fraction of attention mass on the **initial tokens** of a sequence, independent of their semantic relevance to the current prediction (Xiao et al., ICLR 2024). The authors term these tokens **attention sinks**.

Root cause: the SoftMax in attention forces all attention scores over the context to sum to 1. When the current query has no strong match among prior tokens, the model must still "dump" the unneeded probability mass somewhere. Initial tokens are visible to *every* subsequent token by the autoregressive causal mask, so they are the natural, consistently-available place to absorb that mass — the model learns them as sinks during pre-training.

Evidence:
- In Llama-2-7B, beyond the bottom two layers, all heads attend heavily to the first token regardless of content (Figure 2).
- Replacing the first four tokens with linebreak `\n` tokens preserves perplexity (Llama-2-13B: 5.60 vs 5.40 with original initial tokens), proving the effect is positional, not semantic (Table 1).
- A single initial token is *not* enough: 1–2 initial tokens don't fully restore perplexity; **4 initial tokens suffice**, further additions have diminishing returns (Table 2). Reason: training samples lacked a uniform starting token, so the model spreads the sink role across several initial tokens.

## StreamingLLM framework

StreamingLLM (Xiao et al., ICLR 2024) is a training-free method that lets an LLM pre-trained with a finite attention window generate on **infinite-length** inputs.

The KV cache is split into two parts (Figure 4):
1. **Attention sinks** — KV of the first ~4 tokens, kept permanently to anchor the attention-score distribution.
2. **Rolling KV cache** — KV of the most recent tokens, evicted oldest-first as generation proceeds.

Key implementation details:
- Compatible with relative position encodings [[rotary-position-embedding|RoPE]] and [[alibi|ALiBi]]. For RoPE, keys are cached *before* the rotary transform, then the rotation is applied within the cache at each decode step.
- **Positional assignment is within the cache, not the original text.** If the cache holds tokens [0,1,2,3,6,7,8] while decoding token 9, positions are [0,1,2,3,4,5,6,7], not [0,1,2,3,6,7,8,9]. This is essential for stable extrapolation past the pre-training window.
- Decouples the model's pre-training window size from its actual generation length.

## Pre-training with a dedicated sink token

The authors pre-trained 160M-param models from scratch (Pythia recipe, deduplicated Pile) with a learnable **sink token** prepended to every sample. Result: a *single* sink token suffices for stable streaming perplexity, versus the multiple initial tokens required by vanilla models (Table 3). Adding the sink token does **not** harm normal performance — zero-shot accuracy on 7 NLP benchmarks (ARC, HellaSwag, LAMBADA, OpenbookQA, PIQA, Winogrande) is statistically identical (Table 4). They recommend all future LLMs prepend a sink token.

A related, training-free variant is **Zero Sink** (= SoftMax-Off-by-One, Miller 2023), equivalent to prepending an all-zero K/V token; it partially alleviates the sink problem but still needs other initial tokens.

## Results

- **Language modeling:** stable perplexity across Llama-2-[7,13,70]B, MPT-[7,30]B, Falcon-[7,40]B, Pythia-[2.8,6.9,12]B on concatenated PG19 for **>4 million tokens**. Window attention collapses (PPL 5158 on Llama-2-13B at cache config 0+1024) the moment initial tokens are evicted; StreamingLLM (4+1020) holds PPL 5.40.
- **Streaming QA:** on StreamEval (query every 10 lines, answer 20 lines prior) accuracy stays reasonable to ~120K tokens, while dense attention OOMs and window attention collapses. On ARC-[E,C] in a streaming multi-round setup, StreamingLLM matches one-shot sample-by-sample accuracy.
- **Efficiency:** up to **22.2× per-token speedup** over sliding-window-with-recomputation, with similar memory footprint (Figure 10). Decode latency grows linearly with cache size vs quadratically for recomputation.
- **Composes with context extension:** pairing with LongChat-7b-v1.5-32k / Llama-2-7B-32K-Instruct widens the attendable recent context.
- **Adoption:** NVIDIA TensorRT-LLM, Intel Extension for Transformers, HuggingFace Transformers, MLC LLM.

## Open questions / limitations

- Increasing the rolling cache size does **not** consistently lower perplexity (Table 6) — models under-use the long context they are given. The paper flags better long-context utilization as future work.
- StreamingLLM does not *extend* the context window or improve long-context *reasoning*; it only stabilizes generation. It is orthogonal to (and composable with) [[positional-encoding|relative-position context extension]] and long-context-utilization work.
- The 4-million-token stability is perplexity / language-modeling stability, not guaranteed factual retention of early content.

## Related

- The KV-cache memory pressure StreamingLLM sidesteps is the same problem addressed by [[kv-caching|KV caching]] and [[flash-attention|FlashAttention]] at the systems level.
- The positional-within-cache trick relies on relative position encodings: [[rotary-position-embedding|RoPE]] and [[alibi|ALiBi]].

Sources: [[Efficient Streaming Language Models with Attention Sinks](raw/papers/2023-09-xiao-streamingllm/xiao2023streamingllm.md)]
