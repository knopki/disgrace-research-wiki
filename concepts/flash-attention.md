---
title: FlashAttention
created: 2026-06-16
updated: 2026-07-15
type: concept
tags:
  - architecture
  - optimization
  - inference
  - training
  - gpu
  - hardware
sources:
  - "[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](raw/papers/2022-05-dao-flashattention/dai2022flashattention.md)"
  - "[FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](raw/papers/2023-07-dao-flashattention-2/dao2023flashattention2.md)"
confidence: high
---

# FlashAttention

**FlashAttention** is an IO-aware exact attention algorithm that accelerates [[transformer|Transformer]] training and inference by tiling the attention computation to fit on GPU on-chip SRAM, dramatically reducing slow reads/writes to GPU HBM (high bandwidth memory). Developed by Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré (Stanford / University at Buffalo), published at NeurIPS 2022. **FlashAttention-2** (Dao, 2023) is the refined successor: it keeps the same IO-aware tiling but reworks GPU work partitioning (parallelism across thread blocks and warps, fewer non-matmul FLOPs) to lift utilization from 25–40% to 50–73% of theoretical peak — roughly a 2× wall-clock speedup over FlashAttention-1 at no loss of accuracy.

## The Problem: Attention Is Memory-Bound, Not Compute-Bound

Standard attention computes S = QK^T, applies softmax, then P = softmax(S)V. For a sequence of length N with head dimension d, this requires O(N² + Nd) HBM accesses — the intermediate attention matrix S and P (N² elements) must be written to HBM and read back. Since GPU HBM bandwidth (~1.5 TB/s on A100) is an order of magnitude slower than on-chip SRAM bandwidth (~19 TB/s), the standard implementation is bottlenecked by memory, not FLOPs.

Previous approximate attention methods ([[sparse-transformer|Sparse Transformer]], [[longformer|Longformer]], [[big-bird|BigBird]]) focused on reducing FLOPs via sparse patterns but ignored the IO bottleneck, which is why many failed to achieve wall-clock speedup. ([Dao et al., 2022](raw/papers/2022-05-dao-flashattention/dai2022flashattention.md))

## The Solution: IO-Aware Tiling

FlashAttention computes exact attention in a **tiled** fashion: the Q, K, V matrices are divided into blocks that fit in GPU on-chip SRAM (typically 192 KB on A100), and each block operation is performed entirely on SRAM before writing the result back to HBM.

### Forward Pass (Simplified)

1. Divide Q, K, V into blocks of size B_c × d (K, V) and B_r × d (Q), sized to fit on SRAM
2. For each K, V block (outer loop): load from HBM to SRAM
3. For each Q block (inner loop): load from HBM, compute S_block = Q_block × K_block^T, apply softmax incrementally, compute P_block × V_block, accumulate output
4. Write the output block back to HBM

The key algorithmic contribution is an **online softmax** that computes the correct softmax incrementally across blocks — standard softmax requires the full row of S to be materialised, which would force an HBM round-trip.

### IO Complexity

Standard attention: O(Nd + N²) HBM accesses (the N² comes from the intermediate S and P matrices). FlashAttention: O(N²d² / M) where M is SRAM size — a reduction by a factor of M/d² ≈ 9× on A100 for d=64. The paper proves this is optimal: no exact attention algorithm can asymptotically reduce HBM access further for a given SRAM size. ([Dao et al., 2022](raw/papers/2022-05-dao-flashattention/dai2022flashattention.md))

## Block-Sparse FlashAttention

An extension replacing dense block multiplication with block-sparse masking: given a predefined sparsity pattern (e.g., from [[sparse-transformer|Sparse Transformer]] or [[longformer|Longformer]]), only non-zero blocks are loaded from HBM. This combines the IO-awareness of FlashAttention with the compute reduction of sparse patterns, yielding faster approximate attention than any prior method.

## Results (FlashAttention-1)

| Model | Seq len | Speedup | Metric |
|-------|---------|---------|--------|
| BERT-large | 512 | 1.15× (MLPerf 1.1 baseline) | MLM accuracy 72.0% |
| GPT-2 | 1,024 | 3× | Validation perplexity (identical) |
| LRA (Long Range Arena) | 1K-4K | 2.4× | Task accuracy |
| Path-X | 16,384 | 61.4% (first >chance) | Accuracy |
| Path-256 | 65,536 | 63.1% (first >chance) | Accuracy |

Beyond speed, FlashAttention's memory efficiency — O(N) instead of O(N²) memory for the attention matrix — enables processing sequences that previously required sparse approximation or were simply impossible. The Path-X and Path-256 results are landmark: prior Transformer architectures could not exceed random-chance accuracy on these long-context benchmarks. ([Dao et al., 2022](raw/papers/2022-05-dao-flashattention/dai2022flashattention.md))

## Why FlashAttention Works Where Sparse Patterns Didn't

The key insight is that attention is **memory-bound**, not compute-bound, for most practical sequence lengths. Sparse attention methods optimise for FLOPs but, on modern GPUs, the bottleneck is moving data between memory levels. FlashAttention addresses the actual bottleneck — once the memory problem is solved, even dense exact attention runs faster than approximate methods that still pay the IO tax.

This insight is why FlashAttention saw rapid adoption while many sparse attention papers remained academic curiosities. It is now the default attention implementation in PyTorch (scaled_dot_product_attention), Hugging Face Transformers, and practically every major training and inference framework.

## FlashAttention-2: Better Parallelism and Work Partitioning

FlashAttention-1 already delivered 2–4× wall-clock speedup over optimized baselines, but profiling showed it reached only 30–50% of peak FLOPs/s on the forward pass and 25–35% on the backward pass on A100 — versus 80–90% for optimized GEMM. The gap is structural: FlashAttention-1 has suboptimal **work partitioning** between thread blocks and warps, causing either low GPU occupancy or excess shared-memory reads/writes. FlashAttention-2 (Dao, 2023) attacks exactly that. ([Dao, 2023](raw/papers/2023-07-dao-flashattention-2/dao2023flashattention2.md))

### Why non-matmul FLOPs matter

Modern GPUs have dedicated matrix-multiply units (Tensor Cores). On A100 the FP16/BF16 matmul ceiling is 312 TFLOPs/s, but non-matmul FP32 throughput is only 19.5 TFLOPs/s — each non-matmul FLOP is ~16× more expensive than a matmul FLOP. To stay above 50% of peak, the kernel must spend as much time as possible in matmul. FlashAttention-2 therefore reduces non-matmul FLOPs while leaving the output mathematically identical.

### Three changes

1. **Fewer non-matmul FLOPs via online-softmax tweak.** Instead of rescaling both output terms by `diag(ℓ)⁻¹` every block, FlashAttention-2 keeps an *un-scaled* accumulator `Õ` and only applies the final `diag(ℓ)⁻¹` once at the end of the loop. It also stores only the **logsumexp** `L = m + log(ℓ)` (not both the running max `m` and the sum of exponentials `ℓ`) for the backward pass. ([Dao, 2023](raw/papers/2023-07-dao-flashattention-2/dao2023flashattention2.md))
2. **Parallelize over the sequence-length dimension.** FlashAttention-1 schedules one thread block per (batch, head) and parallelizes only over batch × heads. For long sequences (small batch / few heads) that under-utilizes the 108 SMs of an A100. FlashAttention-2 additionally splits the outer row-block loop across thread blocks (forward) and the column-block loop across thread blocks (backward, using atomic adds to accumulate `dQ`). This raises occupancy in the long-context regime. The sequence-length-parallelism idea and the swapped loop order were first implemented by Phil Tillet in the Triton attention kernel. ([Dao, 2023](raw/papers/2023-07-dao-flashattention-2/dao2023flashattention2.md))
3. **Better warp-level work partitioning.** FlashAttention-1 used a "split-K" scheme: split K and V across 4 warps, each writes its partial `QKᵀ·V` slice to shared memory, then all warps synchronize and sum — costly shared-memory traffic. FlashAttention-2 instead **splits Q** across warps while keeping K and V shared; each warp computes its `QKᵀ` slice, multiplies by its shared V slice, and needs no inter-warp communication. The backward pass同样 avoids split-K (some sync remains due to the Q/K/V/dO/dQ/dK/dV dependency graph). ([Dao, 2023](raw/papers/2023-07-dao-flashattention-2/dao2023flashattention2.md))

### Causal masking and MQA/GQA

- **Causal mask:** for auto-regressive LMing, blocks whose column indices all exceed the row indices (~half of blocks at long context) are skipped entirely → ~1.7–1.8× speedup over the unmasked case; the mask is only applied to one block per row.
- **MQA / GQA:** FlashAttention-2 supports [[multi-query-attention|Multi-Query Attention]] and [[grouped-query-attention|Grouped-Query Attention]] by implicitly remapping head indices instead of duplicating K/V, and sums `dK`/`dV` gradients across the heads that were implicitly replicated in the backward pass. ([Dao, 2023](raw/papers/2023-07-dao-flashattention-2/dao2023flashattention2.md))

### Results (FlashAttention-2)

Micro-benchmarks on A100 80GB SXM4 (varying seq len 0.5k–16k, head dim 64/128, with/without causal mask):

- **1.7–3.0× faster than FlashAttention-1**, 1.3–2.5× faster than the Triton FlashAttention, and **3–10× faster than a standard PyTorch attention** implementation.
- Forward pass reaches up to **73%** of theoretical peak TFLOPs/s; backward up to **63%**. Peak measured **230 TFLOPs/s** on A100.
- On H100 80GB SXM5 (reusing the same kernel, no new TMA / 4th-gen Tensor Core instructions) up to **335 TFLOPs/s**; the paper expects another 1.5–2× from H100-specific instructions + FP8.

End-to-end GPT-style training (8×A100, 1.3B / 2.7B params, 2k and 8k context), TFLOPs/s per GPU:

| Model | Without FlashAttention | FlashAttention-1 | FlashAttention-2 |
|-------|------------------------|------------------|------------------|
| GPT-style 1.3B, 2k ctx | 142 | 189 | 196 |
| GPT-style 1.3B, 8k ctx | 72 | 170 | 220 |
| GPT-style 2.7B, 2k ctx | 149 | 189 | 205 |
| GPT-style 2.7B, 8k ctx | 80 | 175 | **225** (72% model FLOPs utilization) |

FlashAttention-2 yields up to **1.3×** over FlashAttention-1 and **2.8×** over the no-FlashAttention baseline. The 8k-context rows show the biggest wins because attention dominates more of the runtime at longer sequence length. ([Dao, 2023](raw/papers/2023-07-dao-flashattention-2/dao2023flashattention2.md))

> Note: the paper's Table 1 caption says FlashAttention-2 is "1.3× speedup compared to FlashAttention-2", which is a self-referential typo — the Abstract and surrounding text establish the intended comparison is "1.3× compared to FlashAttention-1".

## Relationship to Other Concepts

- **[[spargeattn|SpargeAttn]]** — builds directly on FlashAttention's tiled architecture, adding dynamic sparsity prediction within the inner loop. SpargeAttn's Stage 1 and Stage 2 filters operate inside FlashAttention's fused kernel, making it a true extension rather than an alternative. ([Zhang et al., 2025](raw/papers/2025-02-zhang-spargeattention/zhang2025spargeattn.md))
- **[[sparse-transformer|Sparse Transformer]]** — both address transformer O(n²) scaling; Sparse Transformer via fixed sparse attention patterns (reducing FLOPs), FlashAttention via IO-aware tiling (reducing memory traffic). Orthogonal and complementary.
- **[[longformer|Longformer]] and [[big-bird|BigBird]]** — linear-complexity attention architectures that prescribe sparse patterns. FlashAttention's dense IO-aware approach differs philosophically: it doesn't change the attention pattern, just makes it faster.
- **[[kv-caching|KV Caching]]** — complementary inference optimisation. KV caching avoids recomputation across decoding steps; FlashAttention accelerates the per-step attention computation. Both are now standard in production systems.
- **[[speculative-decoding|Speculative Decoding]]** — complementary inference acceleration. FlashAttention reduces per-step compute cost via IO-aware tiling; speculative decoding reduces the number of serial steps by verifying multiple candidates in parallel. Both can be applied to the same model simultaneously.
- **[[multi-query-attention|Multi-Query Attention (MQA)]] and [[grouped-query-attention|Grouped-Query Attention (GQA)]]** — FlashAttention-2 adds native support for both by remapping head indices instead of duplicating K/V; this matters because GQA/MQA shrink the KV cache and pair naturally with FlashAttention's memory savings at long context.
- **[[transformer|Transformer]]** — FlashAttention is the practical solution to the Transformer's O(n²) memory bottleneck, enabling the long-context capabilities that the original architecture promised but couldn't deliver.
- **[[mamba|Mamba / SSM]]** — FlashAttention extended the practical context length of Transformers significantly, which partly motivated the search for alternatives like Mamba (SSMs offer constant-memory state). The Mamba vs. FlashAttention comparison is a central axis in the efficient architecture discussion.
- **[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]]** — long-context Transformers enabled by FlashAttention make latent-space reasoning over longer horizons practical, though Coconut sidesteps the token-by-token bottleneck altogether.
