---
title: "Distilling the Knowledge in a Neural Network"
authors:
  - Geoffrey Hinton
  - Oriol Vinyals
  - Jeff Dean
date: 2015-03-09
source_url: https://arxiv.org/abs/1503.02531
ingested: 2026-06-17
---

> Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network.* arXiv:1503.02531. NIPS 2014 Deep Learning Workshop.
>
> **PDF:** [1503.02531.pdf](1503.02531.pdf)

## Abstract

A very simple way to improve the performance of almost any machine learning algorithm is to train many different models on the same data and then to average their predictions. Unfortunately, making predictions using a whole ensemble of models is cumbersome and may be too computationally expensive to allow deployment to a large number of users, especially if the individual models are large neural nets. Caruana and his collaborators have shown that it is possible to compress the knowledge in an ensemble into a single model which is much easier to deploy and we develop this approach further using a different compression technique. We achieve some surprising results on MNIST and we show that we can significantly improve the acoustic model of a heavily used commercial system by distilling the knowledge in an ensemble of models into a single model. We also introduce a new type of ensemble composed of one or more full models and many specialist models which learn to distinguish fine-grained classes that the full models confuse. Unlike a mixture of experts, these specialist models can be trained rapidly and in parallel.

## Key Contributions

1. **Knowledge Distillation** — formalized the technique of transferring "dark knowledge" from a cumbersome model (or ensemble) to a smaller distilled model using a temperature-parameterized softmax.

2. **Temperature in Softmax** — introduced temperature T in the softmax function (q_i = exp(z_i/T) / Σ_j exp(z_j/T)) to produce softer probability distributions that reveal class similarity structure.

3. **Soft Targets as Regularizers** — demonstrated that soft targets from a teacher model allow a student model to generalize from as little as 3% of training data, achieving near-original performance (57.0% vs 58.9% baseline on speech task), converging without early stopping.

4. **Specialist Models** — proposed a scalable ensemble architecture: one generalist model + many independently trained specialists focused on confusable class subsets, initialized from the generalist to prevent overfitting.

5. **Matching Logits as Special Case** — proved mathematically that at high temperatures, distillation simplifies to minimizing squared logit differences (Caruana's approach), with the temperature controlling how much attention is paid to very negative logits.

## Experiments

- **MNIST:** Distilled net achieves 74 errors (vs 146 for small net trained on hard targets alone). Remarkably, a model never trained on digit "3" correctly classifies 98.6% of test 3s (with bias correction).

- **Speech Recognition (Android Voice Search):** Ensemble of 10 DNNs (8 layers × 2560 ReLU, 85M params each) distilled into single model — 80% of frame accuracy improvement transferred (60.8% vs ensemble 61.1%), same WER (10.7%).

- **JFT Image Dataset (100M images, 15K labels):** Baseline + 61 specialist models gave 4.4% relative improvement in top-1 accuracy. Specialist training took days vs months for full model.

- **Regularization with Soft Targets:** With only 3% of training data: hard targets → 44.5% test accuracy (severe overfitting, early stopping required); soft targets → 57.0% (no early stopping needed, within 2% of full-data baseline 58.9%).

## Open Questions (from paper)

- Distillation of specialist models back into a single large model was not yet demonstrated.
- The interaction between temperature and model capacity for optimal distillation remained empirical.
