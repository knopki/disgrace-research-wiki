---
title: In-Context Learning
created: 2026-06-17
updated: 2026-06-17
type: concept
tags:
  - technique
  - training
  - methodology
sources:
  - "[Language Models are Few-Shot Learners](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)"
confidence: high
---
# In-Context Learning

A paradigm in which a language model adapts to a task purely through conditioning context at inference time, without any gradient updates or fine-tuning. The model is given a natural language instruction and/or task demonstrations as part of its input sequence, and generates completions for new instances. Systematically defined and studied at scale in the [[entities/gpt-3|GPT-3]] paper ([Brown et al., 2020](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)), building on earlier observations in GPT-2 and meta-learning literature.

## Spectrum of Settings

In-context learning spans a spectrum from most to least task-specific data:

| Setting | Demonstrations | Task Description | Gradient Updates |
|---------|:-------------:|:----------------:|:---------------:|
| Fine-tuning | Thousands+ | Yes | Yes |
| Few-shot (FS) | 10–100 | Optional | No |
| One-shot (1S) | 1 | Yes | No |
| Zero-shot (0S) | 0 | Yes | No |

- **Zero-shot:** only a natural language instruction; no examples. Closest to how humans perform some tasks (e.g., translation from an instruction).
- **One-shot:** one demonstration plus task description. Matches how tasks are often communicated to humans (e.g., Mechanical Turk).
- **Few-shot:** K demonstrations (limited by context window, typically 10–100 for nctx=2048). The model infers the task pattern from examples.

All three are contrasted with **fine-tuning**, which updates model weights on task-specific supervised data. The GPT-3 paper's core finding is that few-shot performance scales strongly with model size — larger models make increasingly efficient use of in-context information ([Brown et al., 2020](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md)).

## Meta-Learning Framing

The paper frames in-context learning as a form of **meta-learning**: the outer loop (pre-training) develops a broad set of skills and pattern recognition abilities, while the inner loop (in-context conditioning) rapidly adapts to specific tasks at inference time. The term "in-context learning" describes the inner loop of this process, which occurs entirely within the forward pass. The paper notes ambiguity about whether the model learns tasks de novo or recognizes patterns from pre-training — this likely varies by task (Brown et al., 2020).

## Scaling Trend

A principal finding: the gap between zero-, one-, and few-shot performance **grows with model capacity**. For most tasks, few-shot performance increases more rapidly with scale than zero-shot, suggesting larger models are intrinsically better meta-learners. GPT-3 175B showed this effect dramatically on synthetic tasks (word scrambling, arithmetic) where smaller models performed at chance but GPT-3 achieved strong results. This scaling trend was observed across language modeling, QA, translation, reading comprehension, and SuperGLUE tasks.

## Key Empirical Findings

### Strong ICL performance
- LAMBADA: 76.2% zero-shot → 86.4% few-shot (+10 pts for largest model, −20% for smallest)
- TriviaQA: 64.3% zero-shot → 71.2% few-shot
- Translation: +7 BLEU from zero-shot to one-shot on multiple language pairs
- Word scrambling: near-zero zero-shot performance, strong few-shot (e.g., 67.2% on symbol insertion)

### Weak ICL performance
- Sentence comparison tasks (WiC, ANLI, RTE): little to no ICL benefit, often near random
- Reading comprehension requiring multi-sentence reasoning (RACE, QuAC): modest gains
- The paper hypothesizes this may relate to the autoregressive architecture lacking bidirectionality

### In-context learning curves
Performance as a function of K (number of demonstrations) shows:
- Larger models benefit more from additional examples
- The trend is approximately log-linear in K for most tasks
- K > 32 provides diminishing returns within the 2048-token context window

## Relationship to Other Concepts

- **[[chain-of-thought|Chain-of-Thought]]** — extends in-context learning by providing reasoning steps as intermediate context, improving multi-step reasoning primarily at large model scales
- **[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]]** — replaces text-based in-context conditioning with latent-space reasoning
- **[[rlhf|RLHF]]** — fine-tuning technique that aligns models post-hoc; orthogonal to in-context learning but both can be applied to the same base model
- **[[toolformer|Toolformer]]** — uses ICL directly as the bootstrapping mechanism: a few API demonstrations in-context let the LM propose tool calls, which are then self-supervised-filtered and fine-tuned in
- **[[flex-prompting|FLEX]]** — structured prompting methodology using XML + logit verification, operating within the in-context learning paradigm
- **[[grace|GRACE]]** — semantic markup framework providing navigable in-context structure for large-context tasks
- **[[instruction-tuning|Instruction Tuning]]** — complementary paradigm that achieves task generalization via supervised fine-tuning on instructions rather than inference-time conditioning; instruction tuning works at large scale (≥68B) while ICL works at all scales
- **[[lost-in-the-middle|Lost in the Middle]]** — boundary condition on ICL: a demonstration/fact in the prompt is in principle attendable, but its effective use depends on where it sits (beginning/end ≫ middle)
- **[[v4a-diff-format|V4A Diff Format]]** — a format specifically designed for in-context code editing tasks

## Open Questions

1. Does in-context learning truly learn new tasks or retrieve previously seen patterns? Likely task-dependent.
2. What architectural properties enable strong ICL? Bidirectionality may help for comparison tasks.
3. Can ICL be improved beyond what scaling provides — through better prompting, structured context, or different training objectives?
