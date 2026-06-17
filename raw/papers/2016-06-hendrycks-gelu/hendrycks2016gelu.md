---
title: Gaussian Error Linear Units (GELUs)
source_url: https://arxiv.org/abs/1606.08415
authors:
  - Dan Hendrycks
  - Kevin Gimpel
date: 2016-06-27
updated: 2018-07-06
venue: arXiv (Trimmed version of 2016 draft)
ingested: 2026-06-17
---

## Abstract

We propose the Gaussian Error Linear Unit (GELU), a high-performing neural network activation function. The GELU activation function is xΦ(x) where Φ(x) the standard Gaussian cumulative distribution function. The GELU nonlinearity weights inputs by their value, rather than gates inputs by their sign as in ReLUs. We perform an empirical evaluation of the GELU nonlinearity against the ReLU and ELU activations across all tasks. Performance improvements are found across all tasks: MNIST classification (8-layer FC), MNIST autoencoder, Twitter Part-of-Speech tagging, TIMIT frame recognition, CIFAR-10/100 classification, and on the Large Scale Visual Recognition Challenge dataset using deep convolutional neural networks.

## Key Contributions

1. **GELU activation function** — probabilistically motivated: `GELU(x) = xΦ(x) = x · ½[1 + erf(x/√2)]`, where Φ is the standard normal CDF
2. **Interpretation as stochastic regularizer** — GELU is the expectation of a Bernoulli mask m ∼ Bernoulli(Φ(x)), combining dropout-style stochastic zeroing with zoneout-style stochastic identity: `Φ(x) × Ix + (1-Φ(x)) × 0x = xΦ(x)`
3. **Smooth ReLU interpolation** — GELU smoothly interpolates between the identity map (for positive x with high confidence) and zero (for negative x with high confidence), unlike ReLU's hard gating at zero
4. **SiLU (Sigmoid Linear Unit)** — `xσ(x)`, introduced and named in this paper, later rediscovered as "swish" by Google Brain (2017)
5. **Consistent empirical improvement** over ReLU and ELU across vision, NLP, and speech tasks

## Formulation

**Exact:**
```
GELU(x) = xΦ(x) = x · ½[1 + erf(x/√2)]
```

**Popular approximations (faster computation):**
```
GELU(x) ≈ 0.5x (1 + tanh[ √(2/π) (x + 0.044715x³) ])
GELU(x) ≈ xσ(1.702x)
```

**Properties:**
- No new hyperparameters (fixed µ=0, σ=1, unlike parametric activations)
- Non-convex, non-monotonic
- Every point has non-zero curvature (unlike ReLU/ELU which are linear for positive inputs)
- Asymptotically equals ReLU as σ→0
- Can be viewed as a smoothed ReLU

## Experimental Results

| Task | Dataset | GELU | ReLU | ELU |
|------|---------|------|------|-----|
| MNIST Classification (8-layer FC, Adam) | MNIST | **Lowest** training & validation log loss with/without dropout | — | — |
| MNIST Autoencoder (1000-500-250-30) | MNIST | **Significantly lower** reconstruction error | — | — |
| Twitter POS Tagging (2-layer, 256 units, dropout 0.8) | 25 tags | **12.57%** error | 12.67% | 12.91% |
| TIMIT Frame Recognition (5-layer, 2048 units, dropout 0.5) | 39 phones | **29.3%** test error | 29.5% | 29.6% |
| CIFAR-10 (9-layer CNN, no data augmentation) | 10 classes | **7.89%** error | 8.16% | 8.41% |
| CIFAR-100 (Wide ResNet 40-4, dropout 0.7) | 100 classes | **20.74%** error | 21.77% | 22.98% |

GELU also shows improved robustness to input noise (Figure 3).

## Practical Tips

- Use an optimizer with momentum (Adam, Nesterov)
- Prefer the tanh-based approximation for speed/accuracy
- SiLU (xσ(x)) outperforms ReLU/ELU but is worse than GELU
- Works well with dropout — shares the stochastic regularizer "compartment"

## SiLU / Swish Controversy

This paper originally introduced and named the Sigmoid Linear Unit (SiLU, xσ(x)). In 2017, Google Brain published a paper proposing xσ(x) as "swish," later adding a learnable β (xσ(βx)) to claim novelty. After community pushback, TensorFlow and PyTorch renamed the function back to SiLU, and credit was attributed to Hendrycks & Gimpel's prior work.

GELU became the default activation in BERT and GPT and is far more widely used than SiLU.

## Legacy

- **Default activation in BERT** (Devlin et al., 2019) — both BERT-Base and BERT-Large use GELU
- **Default activation in GPT** models (Radford et al., 2018; Brown et al., 2020)
- Adopted by virtually all subsequent Transformer-based language models
- The probabilistic interpretation (stochastic regularizer expectation) influenced later activation function design
- One of the most influential activation functions in deep learning alongside ReLU

## Full text

PDF: [1606.08415.pdf](1606.08415.pdf) — 9 pages, 2.7 MB.
