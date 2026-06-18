---
title: GPT-3
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - model
  - architecture
  - training
  - benchmark
  - paper
sources:
  - "[Language Models are Few-Shot Learners](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)"
confidence: high
---
# GPT-3

Generative Pre-trained Transformer 3 — a 175 billion parameter autoregressive language model developed by [[openai|OpenAI]], introduced in the paper "Language Models are Few-Shot Learners" ([Brown et al., 2020](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)). At the time of release it was the largest non-sparse language model ever trained, with 10× more parameters than any predecessor. The paper's central finding is that scaling up language models dramatically improves task-agnostic [[in-context-learning|in-context learning]] performance, sometimes reaching competitiveness with prior state-of-the-art fine-tuned models.

## Architecture

GPT-3 uses the same decoder-only [[transformer|Transformer]] architecture as GPT-2 ([Radford et al., 2019](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md)), with modified initialization, pre-normalization, and reversible tokenization. Two architectural differences:

- Alternating dense and locally banded sparse attention patterns in transformer layers, similar to the [[sparse-transformer|Sparse Transformer]] ([Child et al., 2019](raw/papers/2019-04-child-sparse-transformer/child2019sparse.md)).
- Context window of nctx = 2048 tokens for all model sizes.

Eight model sizes were trained to study scaling:

| Model | Parameters | Layers | d_model | Heads | Batch Size | LR |
|-------|-----------|--------|---------|-------|-----------|-----|
| GPT-3 Small | 125M | 12 | 768 | 12 | 0.5M | 6.0e-4 |
| GPT-3 Medium | 350M | 24 | 1024 | 16 | 0.5M | 3.0e-4 |
| GPT-3 Large | 760M | 24 | 1536 | 16 | 0.5M | 2.5e-4 |
| GPT-3 XL | 1.3B | 24 | 2048 | 24 | 1M | 2.0e-4 |
| GPT-3 2.7B | 2.7B | 32 | 2560 | 32 | 1M | 1.6e-4 |
| GPT-3 6.7B | 6.7B | 32 | 4096 | 32 | 2M | 1.2e-4 |
| GPT-3 13B | 13.0B | 40 | 5140 | 40 | 2M | 1.0e-4 |
| **GPT-3 175B** | **175.0B** | **96** | **12288** | **96** | **3.2M** | **6.0e-5** |

All models use d_ff = 4 × d_model and d_head = 64–128. Models were partitioned across V100 GPUs using both depth-wise and width-wise model parallelism on a Microsoft-provided high-bandwidth cluster ([Brown et al., 2020](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)).

## Training Data

Training data was sourced from filtered Common Crawl (2016–2019, 45TB compressed → 570GB after filtering) plus curated high-quality corpora:

| Dataset | Tokens | Training Mix Weight | Epochs (300B tokens) |
|---------|-------:|--------------------:|---------------------:|
| Common Crawl (filtered) | 410B | 60% | 0.44 |
| WebText2 | 19B | 22% | 2.9 |
| Books1 | 12B | 8% | 1.9 |
| Books2 | 55B | 8% | 0.43 |
| Wikipedia | 3B | 3% | 3.4 |

Higher-quality datasets were sampled more frequently, accepting minor overfitting for better data quality. Data was deduplicated at document level. A 13-gram overlap filter was applied to reduce test set contamination, but a bug caused only partial removal ([Brown et al., 2020](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)).

Training ran for 300 billion tokens. Validation loss followed a smooth power-law with compute, extending the trend from [[scaling-laws|Scaling Laws]] ([Kaplan et al., 2020](raw/papers/2020-01-kaplan-scaling-laws/kaplan2020scaling.md)) by two more orders of magnitude with minimal departure.

## In-Context Learning Paradigm

GPT-3 introduced the systematic study of [[in-context-learning|in-context learning]] across three settings, none involving gradient updates:

- **Zero-shot:** natural language instruction only, no demonstrations
- **One-shot:** one demonstration + task description
- **Few-shot:** K demonstrations (typically 10–100, limited by 2048-token context)

A key finding: the gap between zero-, one-, and few-shot performance grows with model size, suggesting larger models are more proficient meta-learners ([Brown et al., 2020](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)).

## Key Results

| Task | Setting | Score | Comparison |
|------|---------|-------:|-----------|
| LAMBADA (accuracy) | Few-shot | **86.4%** | +18% over prior SOTA |
| PTB (perplexity) | Zero-shot | **20.5** | New SOTA, 15 pts improvement |
| TriviaQA (accuracy) | Few-shot | **71.2%** | SOTA in closed-book setting, matching RAG open-domain |
| SuperGLUE | Few-shot | **71.8** avg | Outperforms fine-tuned BERT-Large (69.0) on 4/8 tasks |
| COPA (accuracy) | Few-shot | **92.0%** | Near SOTA, second on leaderboard |
| Winogrande (accuracy) | Few-shot | **77.7%** | Competitive with fine-tuned RoBERTa-large |
| Arithmetic (2D+) | Few-shot | **100%** | Perfect on 2-digit addition |
| News article detection | — | **52% human accuracy** | Near chance — humans struggle to distinguish GPT-3 articles |

### Weaknesses

GPT-3 struggled on tasks requiring sentence comparison: WiC (49.4%, near random), ANLI (just above chance), RACE (46.8%, 45% below SOTA). It showed difficulty with common sense physics, semantic coherence over long passages, and NLI tasks ([Brown et al., 2020](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)).

## Data Contamination

A systematic contamination analysis was conducted per benchmark by creating "clean" subsets removing examples with ≥13-gram overlaps with training data. Most benchmarks showed negligible impact. Flagged datasets: PIQA (~3 pp decrease), Winograd (2.6 pp decrease). Language modeling benchmarks derived from Wikipedia were entirely contained in training data and not reported. LAMBADA showed substantial genuine contamination but <0.5% impact on clean subset ([Brown et al., 2020](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)).

## Limitations (from the paper)

1. **No bidirectionality** — autoregressive-only; some tasks benefit from bidirectional architectures
2. **Weak on comparison tasks** — WiC, ANLI, RACE, QuAC underperform
3. **Sample inefficient pre-training** — sees far more text than a human in a lifetime
4. **Ambiguity of few-shot learning** — unclear whether the model learns tasks de novo or recognizes patterns from pre-training
5. **Inference cost** — 175B parameters is expensive and inconvenient to serve
6. **Not interpretable, not well-calibrated** — high variance on novel inputs
7. **Bias and fairness** — retains biases from training data

## Broader Impacts

The paper includes an extensive broader impacts section covering:
- **Misuse potential:** synthetic news articles indistinguishable from human-written text; risk of generating misinformation, spam, phishing, and propaganda at scale
- **Bias:** stereotypical associations (gender, race, religion) amplified by scale; model generates more toxic text than smaller models even with curated datasets
- **Energy:** estimated 3.1e5 MWh for GPT-3 175B training; ~0.4% of US annual electricity (compared to 0.0002% for a typical LM)

## Related

- [[codex|Codex]] — GPT-3 fine-tuned on GitHub code; powers GitHub Copilot
- [[in-context-learning|In-Context Learning]] — the paradigm GPT-3 systematically studied
- [[openai|OpenAI]] — the organization that developed GPT-3
- [[scaling-laws|Scaling Laws]] — GPT-3 confirmed power-law scaling extends 2 orders of magnitude
- [[transformer|Transformer]] — underlying architecture
- [[rlhf|RLHF]] — InstructGPT built on GPT-3 to align with human preferences via RLHF; 1.3B InstructGPT preferred over 175B GPT-3
- [[chain-of-thought|Chain-of-Thought]] — prompting technique that later improved GPT-3's reasoning
- [[flan|FLAN]] — instruction-tuned 137B model (Google, 2022) that outperformed zero-shot GPT-3 on 20/25 datasets despite 38B fewer parameters
- [[instruction-tuning|Instruction Tuning]] — the technique FLAN introduced; demonstrated that supervised data at scale can bridge the gap from zero-shot to few-shot performance
- [[sparse-transformer|Sparse Transformer]] — sparse attention patterns adopted in GPT-3
- [[dario-amodei|Dario Amodei]] — co-author, VP of Research at OpenAI during GPT-3 development
- [[gelu|GELU]] — activation function used across all GPT models
