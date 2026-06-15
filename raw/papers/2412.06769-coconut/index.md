---
source_url: https://arxiv.org/abs/2412.06769
ingested: 2026-06-15
sha256: 6eb32c71eaa571b727ee95bce20396243fd70dc1ee8a37f91a7de717790d5b46
---

# Training Large Language Models to Reason in a Continuous Latent Space

**Authors:** Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li, Zhiting Hu, Jason Weston, Yuandong Tian

**Affiliations:** FAIR at Meta, UC San Diego

**Published:** December 2024 (arXiv:2412.06769)

**Venue:** COLM 2025 (accepted)

**Code:** [github.com/facebookresearch/coconut](https://github.com/facebookresearch/coconut)

## Abstract

Large language models (LLMs) are typically constrained to reason in the language space, where they express the reasoning process through a chain-of-thought (CoT) to solve complex problems. However, the language space may not always be optimal for reasoning. Most word tokens primarily ensure textual coherence and are not essential for reasoning, while some critical tokens require complex planning and pose challenges to LLMs. To explore the potential of reasoning beyond language, we introduce a new paradigm called Coconut (Chain of Continuous Thought). Coconut utilizes the last hidden state of the LLM as a representation of the reasoning state, termed "continuous thought." Instead of decoding this state into words, we feed it back to the model as the next input embedding directly in the continuous space. This latent reasoning paradigm enables an advanced reasoning pattern, where continuous thoughts can encode multiple alternative next steps, allowing the model to perform a breadth-first search (BFS) rather than committing prematurely to a single deterministic path as in CoT. Coconut outperforms CoT on logical reasoning tasks that require substantial search during planning and achieves a better trade-off between accuracy and efficiency.

## 1. Introduction

Standard chain-of-thought forces reasoning into language tokens. The authors argue language space may not be optimal for reasoning:

- Most tokens maintain textual coherence, not reasoning
- Critical decision tokens receive the same compute as filler tokens
- The human language network is largely inactive during reasoning tasks (Fedorenko et al., 2024)

Alternative approaches (Pause Token, iCoT) attempt to internalise reasoning but still operate in the discrete token space. Coconut is the first to perform reasoning entirely in continuous latent space.

## 2. Method

### 2.1 Architecture

- **Language mode:** standard autoregressive generation: token → embedding → hidden → softmax → token
- **Latent mode:** the last hidden state `h_t` is fed directly as the next input embedding, bypassing both the token embedding layer and the language model head

Special tokens:
- `<bot>` — beginning of thought (transition to latent mode)
- `<eot>` — end of thought (transition back to language mode)

Formal description (latent mode positions `i` to `j`):
```
E_t = [e(x_1), ..., e(x_i), h_i, h_{i+1}, ..., h_{t-1}]
```
No decoding occurs between `<bot>` and `<eot>`. The model processes continuous hidden states as if they were token embeddings.

### 2.2 Training Procedure (Multi-stage Curriculum)

Inspired by iCoT (Deng et al., 2024):

1. **Stage 0:** Train on full language CoT chains
2. **Stage k:** Replace the first `k` language reasoning steps with `k × c` continuous thoughts (`c` = latent thoughts per language step, a hyperparameter)
3. Insert `<bot>` and `<eot>` to encapsulate the continuous thought block
4. **Loss:** negative log-likelihood on remaining language tokens only (question and latent thought positions are masked)
5. **No supervision on continuous thoughts** — they learn purely through backpropagation to facilitate future token prediction
6. Optimizer state is reset at each stage switch
7. **Final stage:** all reasoning steps are replaced by continuous thoughts

### 2.3 Inference

- Insert `<bot>` immediately after the question
- Pad continuous thoughts to a constant length (a binary classifier for dynamic termination also works but constant length is simpler and effective)
- Greedy decoding throughout

## 3. Key Findings

### 3.1 Continuous Thoughts Enable BFS-like Reasoning

The central finding: probing the model's hidden states reveals that continuous thoughts encode **multiple alternative next steps simultaneously**, with a natural **value function** (probability distribution over candidates) that emerges without explicit training.

> "The reasoning strategy employed by Coconut is not greedy search: while 'lempus' initially has the highest value (0.33) at the first reasoning step... the model subsequently assigns the highest value (0.87) to 'rorpus,' a child of 'grimpus,' rather than following 'lempus.'"

This demonstrates genuine BFS: the model explores multiple branches and dynamically reweights them as more information is accumulated.

### 3.2 Results

| Method | GSM8k Acc. | GSM8k #Tokens | ProntoQA Acc. | ProntoQA #Tokens | ProsQA Acc. | ProsQA #Tokens |
|--------|-----------|---------------|---------------|------------------|-------------|----------------|
| CoT | 42.9 | 25.0 | 98.8 | 92.5 | 77.5 | 49.4 |
| No-CoT | 16.5 | 2.2 | 93.8 | 3.0 | 76.7 | 8.2 |
| iCoT | 30.0* | 2.2 | 99.8 | 3.0 | 98.2 | 8.2 |
| Pause Token | 16.4 | 2.2 | 77.7 | 3.0 | 75.9 | 8.2 |
| **Coconut** | **34.1** | 8.2 | **99.8** | 9.0 | **97.0** | 14.2 |

Key takeaways:
- Coconut matches or exceeds CoT on logical reasoning (ProntoQA, ProsQA) while using **3-7× fewer tokens**
- On GSM8k (math), Coconut underperforms CoT but still dramatically beats No-CoT baseline
- The multi-stage curriculum is critical: without it, Coconut collapses to No-CoT performance (14.4% on GSM8k)

### 3.3 Ablations

- **w/o curriculum:** no better than No-CoT (14.4% on GSM8k)
- **w/o thought** (just language-mode after mask): 95.5% on ProsQA vs 97.0% — continuous thoughts add 1.5%
- **pause as thought** (learnable `<pause>` tokens): 96.6% — close to 97.0% but lacks BFS structure
- Scaling `c` (continuous thoughts per step) from 0→1→2 steadily improves accuracy on GSM8k

### 3.4 Efficiency

Coconut achieves a **better accuracy-efficiency trade-off** than CoT:
- On ProsQA: 97.0% accuracy at 14.2 tokens vs CoT's 77.5% at 49.4 tokens
- On GSM8k: 34.1% at 8.2 tokens vs CoT's 42.9% at 25.0 tokens (CoT uses 3× more tokens for 8.8% more accuracy)

### 3.5 Scaling to Larger Models

Initial experiments with Llama 3.2-3B and Llama 3-8B show the paradigm transfers: latent reasoning works beyond GPT-2 scale.

## 4. Related Work

- **Internalized chain-of-thought (iCoT)** — Deng et al., 2024: gradually removing language tokens; closest prior work
- **Pause Token** — Goyal et al., 2023: inserting learnable tokens for "thinking time"
- **Thinking LLMs** — Haviv et al., 2024: manipulating hidden states directly without explicit training
- **Continuous Chain-of-Thought** — Yang et al., 2024: compressing CoT reasoning into fewer tokens

## 5. ProsQA Dataset

New dataset introduced in the paper: **Proof with Search QA** (ProsQA). Tasks involve directed acyclic graphs of logical relationships where the model must reason through multiple interdependent steps. Unlike ProntoQA which has a single correct path, ProsQA requires **search** — evaluating multiple candidate paths and pruning dead ends. This is the setting where Coconut's BFS advantage is most pronounced.

## Key Quotes

> "Most word tokens primarily ensure textual coherence and are not essential for reasoning, while some critical tokens require complex planning and pose huge challenges to LLMs."

> "This latent reasoning paradigm leads to the emergence of an advanced reasoning pattern: the continuous thought can encode multiple alternative next reasoning steps, allowing the model to perform a breadth-first search (BFS) to solve the problem, rather than prematurely committing to a single deterministic path like CoT."

## Links

- Paper (arXiv): https://arxiv.org/abs/2412.06769
- PDF: https://arxiv.org/pdf/2412.06769v3
- Code: https://github.com/facebookresearch/coconut

## References

- Deng et al., 2024 — Internalized Chain-of-Thought (iCoT)
- Goyal et al., 2023 — Pause Token: "Think before you speak"
- Haviv et al., 2024 — Thinking LLMs: Direct hidden state manipulation
- Yang et al., 2024 — Continuous Chain-of-Thought
- Fedorenko et al., 2024 — Language network inactivity during reasoning
