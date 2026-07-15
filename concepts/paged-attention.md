---
title: PagedAttention & vLLM
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - inference
  - serving
  - optimization
  - gpu
  - hardware
  - distributed
  - architecture
sources:
  - "[Efficient Memory Management for LLM Serving with PagedAttention](raw/papers/2023-09-kwon-pagedattention/kwon2023pagedattention.md)"
confidence: high
---

# PagedAttention & vLLM

**PagedAttention** is an attention algorithm that lets the key-value cache ([[kv-caching|KV cache]]) be stored in **non-contiguous, paged blocks** of GPU memory, instead of one contiguous tensor per request. It is the memory-management analog of OS virtual memory and paging, adapted to the specifics of autoregressive LLM serving. **vLLM** is the high-throughput distributed LLM serving engine built on top of it (Kwon et al., UC Berkeley / UC San Diego, SOSP 2023; arXiv:2309.06180). Together they cut KV-cache memory waste to near zero and raise serving throughput **2–4×** over prior systems (FasterTransformer, Orca) at equal latency.

## The Problem: KV Cache Is the Memory Bottleneck

High-throughput serving batches many requests, but the batch size is bounded by GPU memory — specifically the KV cache. Key facts from the paper:

- For OPT-13B, the KV cache of a single token costs **800 KB** (2 vectors × 5120 hidden × 40 layers × 2 bytes FP16). A 2048-token request needs up to **1.6 GB** of KV cache.
- KV cache grows and shrinks dynamically and its final length is not known a-priori, but existing systems (FasterTransformer, Orca) pre-allocate a **contiguous** chunk sized to the request's *maximum* sequence length — because deep-learning frameworks require contiguous tensors.
- This causes three wastes (Fig. 2): **reserved** slots for future tokens, **internal fragmentation** (request shorter than its reserved max), and **external fragmentation** (different pre-allocated sizes leave gaps). In the baselines, only **20.4%–38.2%** of KV-cache memory actually holds token states.
- Existing systems also **cannot share** KV cache across sequences (e.g. parallel samples of one prompt, or beam candidates), because each sequence's cache sits in its own contiguous region.

The paper argues memory will get *more* binding over time: A100→H100 roughly doubles FLOPS while GPU memory stays at ≤80 GB.

## The Solution: PagedAttention

PagedAttention divides each sequence's KV cache into **KV blocks** (fixed number of tokens per block; vLLM default **block size 16**). Blocks need not be physically contiguous.

- The KV cache manager (Fig. 4) keeps a **block table** mapping each request's *logical* blocks to *physical* GPU blocks, exactly like OS page tables. Requests ≈ processes, tokens ≈ bytes, blocks ≈ pages.
- Blocks are allocated **on demand** as new tokens are generated, filling left-to-right; the last block reserves only its unfilled slots. This eliminates internal fragmentation and all-or-nothing external fragmentation.
- **Reference counting** enables block-level sharing across sequences. When a shared block must be modified by one sequence, vLLM applies a **copy-on-write** (COW) mechanism at block granularity — only that one block is copied, mirroring OS `fork()` COW.

### Decoding scenarios enabled (§4.4)

- **Parallel sampling** — multiple outputs from one prompt share the prompt's KV blocks (one physical copy); only the final divergent block is COW-managed.
- **Beam search** — candidates share prefix blocks; sharing pattern evolves as decoding proceeds (like a process tree). vLLM frees blocks whose refcount hits 0.
- **Shared prefix** — a service provider can pre-cache KV for common system prompts / few-shot examples; user prompts with that prefix map their logical blocks to the cached physical blocks (last block marked COW).

### Scheduling, preemption, distribution (§4.5–4.6)

- **FCFS** scheduling; when GPU blocks run out, requests are preempted. vLLM recovers via **swapping** (copy blocks to CPU RAM; bounded by GPU KV capacity) or **recomputation** (regenerate KV in one prompt-phase pass). Eviction is **all-or-nothing** per sequence and **gang-scheduled** for sequence groups (beam candidates stay together).
- **Distributed**: supports Megatron-LM-style tensor model parallelism (SPMD). A *single* centralized KV cache manager maps logical→physical blocks; all GPU workers share that mapping. (OPT-175B across 8×A100 shown in eval.)
- **Kernel optimizations** (§5): fused reshape+block-write, fused block-read+attention (adapted from FasterTransformer's kernel, one warp per block for coalesced access), and fused block-copy for COW — to amortize the indirection overhead of paged access.

## Results

Evaluation on OPT-13B/66B/175B and LLaMA-13B over ShareGPT and Alpaca traces (Google Cloud A100):

- **Basic sampling**: vLLM sustains **1.7–2.7×** higher request rate than Orca (Oracle) and **2.7–8×** than Orca (Max) at equal latency; up to **22×** vs FasterTransformer (which lacks fine-grained scheduling). On OPT-13B / ShareGPT, vLLM batches **2.2×** more requests than Orca (Oracle), **4.3×** more than Orca (Max).
- **Beam search** (width 6): **2.3×** over Orca (Oracle) on Alpaca, up from 1.3× in basic sampling — more sharing ⇒ bigger win.
- **Memory saving from sharing**: parallel sampling **6.1–9.8%** (Alpaca) / **16.2–30.5%** (ShareGPT); beam search **37.6–55.2%** (Alpaca) / **44.3–66.3%** (ShareGPT).
- **Shared prefix** (translation, few-shot): **1.67×** throughput over Orca (Oracle) at 1 example; **3.58×** at 5 examples.
- **Chatbot** workload: **2×** higher sustainable request rate than all three Orca baselines.
- **Overhead**: PagedAttention's block-table indirection adds **20–26%** attention-kernel latency vs FasterTransformer, but this only affects the attention operator and is dwarfed by end-to-end throughput gains. Default block size **16** balances GPU parallelism vs internal fragmentation (16–128 best on ShareGPT).
- vLLM implements GPT / OPT / LLaMA; ~8.5K lines Python + 2K lines C++/CUDA; OpenAI-compatible API frontend.

## Relationship to Other Concepts

- **[[kv-caching|KV Caching]]** — PagedAttention is the missing *management layer* for the KV cache: caching makes autoregressive generation O(n) per step, but the cached K/V is what consumes GPU memory and fragments it. PagedAttention manages that cache like a paged virtual-memory system.
- **[[flash-attention|FlashAttention]]** — complementary and orthogonal. FlashAttention speeds up the *per-step* attention compute via IO-aware tiling; PagedAttention speeds up *serving* by fitting more requests' KV caches in memory. Both are standard in production stacks.
- **[[transformer|Transformer]]** — PagedAttention operates on the self-attention K/V tensors of a Transformer; it does not alter the model, only how its inference-time state is allocated.
- **[[speculative-decoding|Speculative Decoding]]** & **[[multi-query-attention|MQA]]** / **[[grouped-query-attention|GQA]]** — orthogonal serving/architecture optimizations that reduce KV-cache size or step count; all can stack with PagedAttention.
- **[[mamba|Mamba / SSM]]** — PagedAttention is the Transformer-side answer to the *KV-cache memory wall* that Mamba's constant state sidesteps; both address the same HBM-bound serving limit from opposite directions.
- **[[memgpt|MemGPT (MemoryGPT)]]** — adopts the same OS paging/virtual-memory analogy one level up: where PagedAttention manages the *GPU KV cache* of serving, MemGPT uses paging to manage the *agent's own working context* against external storage, with the LLM as its own memory manager.
