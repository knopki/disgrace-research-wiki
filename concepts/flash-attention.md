---
title: FlashAttention
created: 2026-06-16
updated: 2026-06-16
type: concept
tags:
  - architecture
  - optimization
  - inference
  - training
sources:
  - "[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](raw/papers/2022-05-dao-flashattention/dai2022flashattention.md)"
confidence: high
---

# FlashAttention

**FlashAttention** is an IO-aware exact attention algorithm that accelerates [[transformer|Transformer]] training and inference by tiling the attention computation to fit on GPU on-chip SRAM, dramatically reducing slow reads/writes to GPU HBM (high bandwidth memory). Developed by Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré (Stanford / University at Buffalo), published at NeurIPS 2022.

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

## Results

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

## Relationship to Other Concepts

- **[[spargeattn|SpargeAttn]]** — builds directly on FlashAttention's tiled architecture, adding dynamic sparsity prediction within the inner loop. SpargeAttn's Stage 1 and Stage 2 filters operate inside FlashAttention's fused kernel, making it a true extension rather than an alternative. ([Zhang et al., 2025](raw/papers/2025-02-zhang-spargeattention/zhang2025spargeattn.md))
- **[[sparse-transformer|Sparse Transformer]]** — both address transformer O(n²) scaling; Sparse Transformer via fixed sparse attention patterns (reducing FLOPs), FlashAttention via IO-aware tiling (reducing memory traffic). Orthogonal and complementary.
- **[[longformer|Longformer]] and [[big-bird|BigBird]]** — linear-complexity attention architectures that prescribe sparse patterns. FlashAttention's dense IO-aware approach differs philosophically: it doesn't change the attention pattern, just makes it faster.
- **[[kv-caching|KV Caching]]** — complementary inference optimisation. KV caching avoids recomputation across decoding steps; FlashAttention accelerates the per-step attention computation. Both are now standard in production systems.
- **[[transformer|Transformer]]** — FlashAttention is the practical solution to the Transformer's O(n²) memory bottleneck, enabling the long-context capabilities that the original architecture promised but couldn't deliver.
- **[[mamba|Mamba / SSM]]** — FlashAttention extended the practical context length of Transformers significantly, which partly motivated the search for alternatives like Mamba (SSMs offer constant-memory state). The Mamba vs. FlashAttention comparison is a central axis in the efficient architecture discussion.
- **[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]]** — long-context Transformers enabled by FlashAttention make latent-space reasoning over longer horizons practical, though Coconut sidesteps the token-by-token bottleneck altogether.
