---
title: Ring Attention
created: 2026-07-15
updated: 2026-07-15
type: concept
tags: [architecture, training, inference, serving, hardware, gpu, distributed, optimization]
sources:
  - "[Ring Attention with Blockwise Transformers for Near-Infinite Context](raw/papers/2023-10-liu-ring-attention/liu2023ringattention.md)"
confidence: high
---

# Ring Attention

**Ring Attention** (Liu, Zaharia & Abbeel, UC Berkeley, arXiv Oct 2023) distributes a [[transformer|Transformer's]] long sequence across multiple devices and **fully overlaps the communication of key-value blocks with their blockwise computation**, removing the per-device memory ceiling on context length. Because the redistribution is exact (no approximation) and the comms are hidden behind compute, the achievable context length scales **linearly with the number of devices** — up to device-count × the length possible on a single device. The paper reports 30M+ token contexts in practice and argues the ceiling is effectively "near-infinite" as device count grows.

## The memory wall

Self-attention is O(n²) in sequence length *and* every layer must store its full output for the next layer's attention (n-to-n interactions). Even at batch size 1, processing 100M tokens with a modest hidden size of 1024 needs **>1000 GB** of activation memory — far beyond the <100 GB HBM on a single GPU/TPU. [[flash-attention|FlashAttention]] and its successor **blockwise parallel transformers (BPT)** already cut per-layer activation to `2bsh` bytes (blockwise attention + blockwise FFN), but they still store the whole sequence on one device, so they cap out at the single-device limit.

Ring Attention's core observation: because **blockwise attention is invariant to the order in which query blocks process their key-value blocks** (each block's online-softmax statistics combine correctly regardless of order), the KV blocks can be *rotated* through a ring of hosts instead of being gathered onto each one.

## Method

- The input sequence is split into `N` blocks, one per host. Each host owns one iteration of the outer loop (its query block) and its blockwise FFN — no communication needed for those.
- Each host holds one K/V block. During the inner loop it computes blockwise attention against its current K/V block, then **sends its K/V block to the next host while simultaneously receiving the previous host's K/V block** (`jax.lax.ppermute` between adjacent ring neighbours). After `N−1` rotations, every host has attended to all K/V blocks.
- The overlap is exact for both forward and backward passes. Prior ring-topology attention work ([Beltagy et al. sequence parallelism, 2021](https://arxiv.org/abs/2104.08378)) had **non-overlapped** comms overhead, which is what made it infeasible at large context.

### Arithmetic-intensity condition

Let `F` = per-host FLOPs, `B` = interconnect bandwidth (NVLink/InfiniBand/TPU ICI), `c` = block size, `d` = head dim. Blockwise self-attention costs `4dc²` FLOPs and moves `4cd` bytes. Communication is fully hidden iff `4dc²/F ≥ 4cd/B`, i.e. **block size `c ≥ F/B`** (compute time ≥ transfer time). Required minimal sequence length per host is `s = 6c`. For typical hardware the minimal block size is ~1K tokens and the minimal per-host sequence ~6–10K tokens — easily met once data/tensor parallelism is also applied (Table 2).

### Memory cost

A host stores 6 blocks total (query block + 2 for current K/V + 2 for incoming K/V + 1 for output) → **`6bch` bytes**, linear in block size `c` and **independent of sequence length `s`** (Table 1). This is the property that lets context scale with device count instead of HBM.

## Results

- **Max context (Table 3, FSDP, end-to-end):** with `n` devices, Ring Attention trains context `n ×` the blockwise-parallel-transformer baseline. Highlights: 8×A100 3B → 512K (8× SOTA); 32×A100 7B → **1M+ tokens (32×)**; TPUv4-1024 3B → 16.4M tokens (512×), 7B → 8.2M (512×); **TPUv4-512 → 30M+ tokens (256×)**. The paper concludes 100M+ tokens are feasible as device count rises.
- **Model FLOPs utilization:** slightly *lower* than the BPT baseline (longer sequences mean more self-attention FLOPs, which have lower MFU than FFN), but the overhead is negligible — 7B–65B models train at 4M+ context with MFU essentially preserved (Table 4).
- **LLM finetuning:** LLaMA-13B finetuned to **512K context** on 32×A100 (ShareGPT) and evaluated on long-range line retrieval (needle-in-a-haystack). Ring-Attention-13B-512K holds high accuracy deep into the context where GPT-3.5-turbo-16K, Vicuna-16B-16K, and Claude-2-100K collapse.
- **In-context RL (ExoRL):** AT + Ring Attention (113.66 avg return) beats AT + BPT (111.13) and, crucially, *runs* at 128 trajectories where BPT OOMs — the longer effective horizon helps.

## Relationship to other concepts

- **[[flash-attention|FlashAttention / BPT]]** — Ring Attention is a *distributed* layer on top of blockwise exact attention. It reuses whatever memory-efficient attention runs locally on each host and only adds the ring communication; the two are complementary, not competing.
- **[[streaming-llm|StreamingLLM]]** — both target "infinite context" but solve opposite problems. StreamingLLM is an *inference-time* cache-eviction trick (keep sink tokens + rolling window) for a fixed-size model; Ring Attention is a *training/inference* memory-distribution scheme that removes the per-device ceiling so the model actually sees the whole long sequence. They can stack: a Ring-Attention backbone could feed a streaming cache at decode time.
- **[[kv-caching|KV Caching]]** — Ring Attention's ring shuttles K/V blocks between hosts; KV caching avoids recomputing them within a decode step. Related but orthogonal memory optimizations.
- **[[sparse-transformer|Sparse / Longformer / BigBird attention]]** — those reduce *FLOPs* via sparse patterns (often approximate). Ring Attention keeps attention exact and instead attacks the *memory/communication* axis, overlapping comm with compute.
- **[[mamba|Mamba / SSMs]]** — constant-memory state-space models are an architectural alternative to the O(n²) attention wall; Ring Attention instead keeps dense exact attention but distributes the O(n) memory across devices, pushing the wall outward rather than removing it.
- **[[transformer|Transformer]]** — directly addresses the architecture's quadratic activation-memory bottleneck that caps context length on a single device.
