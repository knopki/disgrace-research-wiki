---
title: LoRA (Low-Rank Adaptation)
created: 2026-06-18
updated: 2026-06-18
type: concept
tags:
  - technique
  - fine-tuning
  - training
  - inference
sources:
  - "[LoRA: Low-Rank Adaptation of Large Language Models](raw/papers/2021-06-hu-lora/hu2021lora.md)"
confidence: high
---

## Definition

**LoRA (Low-Rank Adaptation)** is a parameter-efficient fine-tuning method that freezes pre-trained weights and injects trainable low-rank decomposition matrices into each layer of a [[transformer|Transformer]] architecture. Introduced by Hu et al. (Microsoft Research, ICLR 2022), it reduces trainable parameters by up to 10,000× on GPT-3 175B while matching or exceeding full fine-tuning quality, with zero additional inference latency. ([Hu et al., 2021](raw/papers/2021-06-hu-lora/hu2021lora.md))

## Formulation

For a pre-trained weight matrix W₀ ∈ ℝ^{d×k}, LoRA constrains the update ΔW to a low-rank decomposition:

```
W₀ + ΔW = W₀ + BA
```

where B ∈ ℝ^{d×r}, A ∈ ℝ^{r×k}, and rank r ≪ min(d, k). During training:
- **W₀ is frozen** — no gradient updates
- **A and B are trainable** — A initialized with random Gaussian, B initialized to zero (so ΔW=0 at start)
- Forward pass: h = W₀x + BAx = (W₀ + BA)x

During inference, the merged weight W = W₀ + BA is computed explicitly — no latency overhead compared to a fully fine-tuned model. Task switching only requires swapping the small BA product (e.g., 35MB vs 350GB for GPT-3).

The update is scaled by α/r, where α is a constant. With Adam, tuning α ≈ tuning learning rate; α defaults to the first r tried.

## Key Results

### Memory and Throughput

| Metric | Full Fine-Tuning | LoRA (GPT-3 175B, r=4, Wq+Wv) |
|--------|-----------------|-------------------------------|
| Trainable parameters | 175B | 4.7M (37.7M with all 4 attn weights) |
| VRAM during training | 1.2TB | 350GB |
| Checkpoint size | 350GB | 35MB |
| Training throughput | 32.5 tok/s/V100 | 43.1 tok/s/V100 (+25%) |

### Model Quality

**RoBERTa base/large on GLUE:** LoRA (0.3M params) matches full fine-tuning (125-355M) across 8 tasks, averaging 91.5 (base) and 88.6/92.6 (large, two setups). On average LoRA matches or exceeds all adapter and prefix-tuning baselines.

**DeBERTa XXL (1.5B) on GLUE:** LoRA (4.7M params, 0.3% of total) achieves 91.3 avg vs 91.1 for full fine-tuning — statistically tied or slightly better.

**GPT-2 medium/large on E2E NLG:** LoRA (0.35M/0.77M params) matches or beats full fine-tuning, adapter, and prefix-tuning baselines across all 5 metrics.

**GPT-3 175B:** LoRA matches or exceeds full fine-tuning on WikiSQL (73.4% vs 73.8%), MultiNLI (91.7% vs 89.5%), and SAMSum (53.8/29.8/45.9 R1/R2/RL vs 52.0/28.0/44.5).

### Optimal Configuration

- **Which weights to adapt:** Wq and Wv together yields the best results per parameter budget. Adapting only Wk or Wo underperforms significantly.
- **Rank selection:** r=1 to r=4 suffices for Wq+Wv on the tested datasets. Higher ranks (r=8, 64) do not meaningfully improve performance — the top singular directions overlap substantially between r=8 and r=64 runs.
- **Parameter budget saturation:** Unlike prefix-tuning (which degrades with too many tokens), LoRA improves monotonically with more parameters and saturates without degrading.

## Understanding the Low-Rank Updates

The paper's analysis reveals three properties of ΔW:

1. **ΔW has very low intrinsic rank.** Subspace similarity between A_{r=8} and A_{r=64} shows the top singular vectors overlap significantly — the first singular direction alone achieves φ>0.5 normalized similarity. More directions contain mostly random training noise.

2. **ΔW amplifies W's latent features.** The projection of W onto ΔW's top singular directions has Frobenius norm 21.5× larger than random directions (for r=4), indicating ΔW amplifies features already present in W but not emphasized during pre-training.

3. **ΔW does not repeat W's top directions.** The amplification targets directions orthogonal to W's dominant singular vectors — it picks up features that were "learned but not emphasized."

## Comparison to Other Adaptation Methods

| Method | Latency overhead | Sequence length impact | Scaling to 175B |
|--------|-----------------|----------------------|-----------------|
| Full fine-tuning | None | None | 350GB checkpoint |
| **LoRA** | **None** | **None** | **35MB delta** |
| Adapters (Houlsby et al.) | +2-30% (batch/seq dependent) | None | Matches at 40M params |
| Prefix-tuning (Li & Liang) | None | Reduced (special tokens) | Non-monotonic, degrades >256 tokens |
| BitFit (bias-only) | None | None | 14.2M params, underperforms |

Adapters add inference latency because they must be computed sequentially with the base model — noticeable in online inference (batch size 1). Prefix-tuning reduces the usable sequence length and its performance degrades with too many special tokens. LoRA avoids both problems by construction.

## Limitations

- Not straightforward to batch inputs for different tasks with different A/B matrices in a single forward pass (unless weights aren't merged and dynamic routing is used).
- Small r may not work for tasks in a language different from the pre-training data — full-rank adaptation may be necessary in that case.
- The paper limited study to self-attention weights only; MLP layers, LayerNorm, and biases were left for future work.

## Relationship to Other Concepts

- [[transformer|Transformer]] — LoRA is applied to Transformer attention weights (Wq, Wk, Wv, Wo)
- [[kv-caching|KV Caching]] — both address inference efficiency; LoRA reduces train-time memory and model storage
- [[multi-query-attention|Multi-Query Attention]] — another efficiency-oriented modification to Transformer attention (Shazeer, 2019), contemporaneous with LoRA's direction
- [[rlhf|RLHF]] — an alternative adaptation paradigm (human-preference fine-tuning); LoRA is often used as the training method within RLHF pipelines
- [[scaling-laws|Scaling Laws]] — LoRA addresses the practical deployment problem created by scaling: enormous checkpoints make full fine-tuning of large models prohibitive
- [[ffn-key-value-memories|FFN as Key-Value Memories]] — both reveal low-rank structure in Transformer layers; LoRA exploits it for efficiency, Geva et al. for interpretability
- [[switch-transformer|Switch Transformer]] — alternative approach to scaling model capacity; LoRA focuses on efficient adaptation rather than efficient training

## References

- Hu et al. (2021) — "LoRA: Low-Rank Adaptation of Large Language Models" ICLR 2022. ([raw](raw/papers/2021-06-hu-lora/hu2021lora.md))
