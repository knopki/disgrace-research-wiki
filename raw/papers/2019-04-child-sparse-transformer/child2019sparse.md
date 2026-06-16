---
source_url: https://arxiv.org/abs/1904.10509
ingested: 2026-06-15
authors: Rewon Child, Scott Gray, Alec Radford, Ilya Sutskever
date: 2019-04-01
title: Generating Long Sequences with Sparse Transformers
---

# Generating Long Sequences with Sparse Transformers

**Authors:** Rewon Child, Scott Gray, Alec Radford, Ilya Sutskever (OpenAI)
**Published:** arXiv:1904.10509v1 [cs.LG], 23 Apr 2019
**PDF:** [1904.10509.pdf](1904.10509.pdf) (6 pages, 4.4 MB)

## Abstract

Transformers are powerful sequence models, but require time and memory that grows quadratically with the sequence length. In this paper we introduce sparse factorizations of the attention matrix which reduce this to O(n√n). We also introduce a) a variation on architecture and initialization to train deeper networks, b) the recomputation of attention matrices to save memory, and c) fast attention kernels for training. We call networks with these changes Sparse Transformers, and show they can model sequences tens of thousands of timesteps long using hundreds of layers. We use the same architecture to model images, audio, and text from raw bytes, setting a new state of the art for density modeling of Enwik8, CIFAR-10, and ImageNet-64. We generate unconditional samples that demonstrate global coherence and great diversity, and show it is possible in principle to use self-attention to model sequences of length one million or more.

## Key Contributions

1. **Sparse factorized attention** — two complementary patterns (strided and fixed) reduce O(n²) to O(n√n) while preserving global connectivity across p=2 attention steps
2. **Deep architecture scaling** — pre-activation residual blocks + 1/√(2N) initialization enable hundreds of layers without auxiliary losses
3. **Memory savings** — gradient checkpointing of attention weights and FFN activations during backward pass
4. **Block-sparse GPU kernels** — fused softmax on sliced Q/K/V blocks, upper triangle skipped via autoregressive mask
5. **Mixed-precision training** — fp32 weights, fp16 activations/gradients with dynamic loss scaling on V100 Tensor Cores

## Architecture Summary

**Residual block (pre-activation):**

```
H₀ = embed(X, Wₑ)
Hₖ = Hₖ₋₁ + resblock(Hₖ₋₁)
y  = softmax(norm(Hɴ)·Wₒᵤₜ)

resblock(H) = a(H) + b(H)
a(H) = dropout(attention(norm(H)))
b(H) = dropout(ff(norm(H + a(H))))
```

- Activation: GELU (f(X) = X · σ(1.702·X))
- FFN inner dim: 4× input (2× for half-size variants)
- Weight init: W ~ N(0, 0.125/√dᵢₙ), biases 0. W₂ (FFN output) and Wₚ (post-attention) scaled by 1/√(2N)
- Optimizer: Adam, linear warmup 5000 steps, gradient clipping 1.0, weight decay 0.01, cosine LR schedule

## Results

| Task | Metric | Sparse Transformer | Previous SOTA |
|------|--------|-------------------|---------------|
| CIFAR-10 (seq 3072) | bits/dim | **2.80** (59M, strided) | 2.85 PixelSNAIL |
| Enwik8 (seq 12288) | bits/byte | **0.99** (95M, fixed) | 0.99 Transformer-XL 277M |
| ImageNet-64 (seq 12288) | bits/dim | **3.44** (152M, strided) | 3.52 SPN 150M |
| Classical audio 5s | bits/byte | 1.97 (152M, seq 65536) | — |
| Classical audio (extreme) | bits/byte | 2.99 (3M, seq 1048576) | — |

**Key finding:** Sparse patterns not only ran faster but converged to lower error than dense attention (Table 2), suggesting a useful inductive bias or an underlying optimization issue with full attention.

## Notes

- Strided attention failed on text; fixed patterns recovered and surpassed dense attention
- Longer context monotonically improved Enwik8 performance (0.9952 at 6K → 0.9908 at 12K tokens)
- At 1M+ tokens, model capacity dropped to 3M params and quality degraded significantly
