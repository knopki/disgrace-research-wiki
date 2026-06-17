---
title: Knowledge Distillation
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [model, training, distillation, technique, optimization, inference]
sources:
- "[Distilling the Knowledge in a Neural Network](raw/papers/2015-03-hinton-distillation/hinton2015distill.md)"
confidence: high
---

## Definition

**Knowledge distillation** is a model compression technique that transfers the "dark knowledge" of a large, cumbersome model (or ensemble) — the *teacher* — into a smaller *student* model suitable for deployment. The student is trained on the soft probability distributions produced by the teacher, which encode class-similarity structure that hard labels cannot convey. ([Hinton, Vinyals & Dean, 2015](raw/papers/2015-03-hinton-distillation/hinton2015distill.md))

## The Core Mechanism

### Temperature in Softmax

Standard softmax produces hard probability distributions where one class dominates. By introducing a temperature parameter T, the softmax can be "softened" to reveal relative probabilities of incorrect classes:

$$ q_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)} $$

- **T = 1** — standard softmax, confident predictions
- **T > 1** — softer distributions, revealing which incorrect classes the teacher considers more plausible
- **T → ∞** — uniform distribution

The same high temperature is used when training the student on soft targets; at inference, the student uses T = 1.

### Dark Knowledge

The relative probabilities of incorrect answers encode rich similarity structure. An image of a BMW may have minuscule probability of being a garbage truck, but that probability is still orders of magnitude larger than being a carrot. These ratios contain the "dark knowledge" — the teacher's learned generalization behavior. ([Hinton, Vinyals & Dean, 2015](raw/papers/2015-03-hinton-distillation/hinton2015distill.md))

### Combined Objective

The student is trained with a weighted average of two objective functions:

1. **Cross-entropy with soft targets** (at temperature T) — transfers generalization patterns
2. **Cross-entropy with hard labels** (at T=1) — retains accuracy on ground truth

Soft-target gradients scale as 1/T², so they must be multiplied by T² to keep contributions stable across temperature changes.

### Matching Logits as a Special Case

At high T (relative to logit magnitudes), distillation reduces to minimizing squared difference between teacher and student logits — equivalent to the earlier approach of Caruana et al. (2006). The temperature controls how much attention is paid to very negative logits (which may be noisy or informative). ([Hinton, Vinyals & Dean, 2015](raw/papers/2015-03-hinton-distillation/hinton2015distill.md))

## Key Findings

### Soft Targets as Regularizers

On a speech recognition task (85M parameters), training with **only 3% of the data**:

| Training setup | Test accuracy |
|---|---|
| Hard targets (3% data) | 44.5% (severe overfitting, early stopping required) |
| Soft targets (3% data) | 57.0% (no early stopping, within 2% of full-data baseline) |
| Full-data baseline | 58.9% |

Soft targets effectively communicate the regularities discovered by a full-data model, making them one of the strongest known regularizers.

### Transfer Without Ever Seeing a Class

On MNIST, a student model trained on a transfer set **completely lacking digit "3"** still correctly classified 98.6% of test 3s after bias correction. This demonstrates that the teacher's soft targets capture the relationship of "3" to other digits purely through relative probabilities.

### Ensemble Compression

An ensemble of 10 DNNs (85M params each, 8 hidden layers × 2560 ReLU) for Android Voice Search was distilled into a single model of the same size:
- **Frame accuracy:** ensemble 61.1% → distilled 60.8% (80% of improvement transferred)
- **WER:** 10.7% for both

## Specialist Models

For very large datasets (JFT: 100M images, 15K labels), the paper proposed an architecture combining:
1. A **generalist model** trained on all data
2. Many **specialist models** — each trained on a confusable class subset (identified by clustering the covariance matrix of generalist predictions), initialized from the generalist weights, with biased class sampling corrected at inference

With 61 specialists: 4.4% relative improvement in top-1 accuracy. Specialists train in days vs months for the full model.

## Relationship to Other Techniques

- **Dropout** — can be viewed as training an implicit ensemble; distillation can compress the effective ensemble into a single model
- **Model Compression** (Caruana et al., 2006) — direct predecessor that used logit matching; distillation generalizes this via temperature control
- **Quantization / Pruning** — orthogonal compression methods; distillation can be combined with them
- **[[rlhf|RLHF]]** — both transfer knowledge from a larger/modelled source (teacher → student, reward model → policy), but RLHF uses preference signals rather than class probabilities
- **[[switch-transformer|Switch Transformer]]** — uses fine-tuned distillation for Mixture-of-Experts model compression

## Open Questions

- Whether specialist knowledge can be distilled back into a single large model (was not demonstrated in the original paper)
- The optimal temperature as a function of student capacity, task, and teacher quality remains empirical
- Whether the "dark knowledge" framework extends beyond classification to generative model knowledge transfer

## References

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network.* arXiv:1503.02531. ([PDF](raw/papers/2015-03-hinton-distillation/1503.02531.pdf))

## Related Pages

- [[geoffrey-hinton|Geoffrey Hinton]] — lead author
- [[backpropagation|Backpropagation]] — Hinton's earlier foundational contribution
- [[switch-transformer|Switch Transformer]] — uses distillation for MoE compression
