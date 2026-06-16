---
source_url: https://index.ieomsociety.org/index.cfm/item/55021
ingested: 2026-06-15
title: CoT Harms Performance of Rather Smaller Language Models
authors:
  - Jihoo Shim
  - Shin Dong Ho
  - Jeongwon Kim
date: 2024-10-09
---

# CoT Harms Performance of Rather Smaller Language Models

Full text: [[shim2024cotharms.pdf]] (5 pages, 508).

## Abstract (verbatim)

> We investigate the impact of Chain of Thought (CoT) prompting on smaller language models. While CoT has shown significant improvements in the performance of large language models (LLMs), our research suggests that this technique may be detrimental to the performance of smaller models, showing 15~30% decrease in accuracy for SLMs when using CoT prompting compared to standard prompting. We conducted experiments using a range of model sizes and found that CoT prompting consistently degraded the performance of models below a certain parameter threshold. This work highlights the importance of considering model size when applying prompting techniques and suggests that alternative strategies may be necessary for enhancing the capabilities of smaller language models.

## Metadata

| Field     | Value                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Title     | CoT Harms Performance of Rather Smaller Language Models                                                                             |
| Authors   | Jihoo Shim (Student, My Paul School), Shin Dong Ho (Professor, My Paul School), Jeongwon Kim (Dept. of Economics, Nihon University) |
| Venue     | 1st World Congress on Industrial Engineering and Operations Management, Detroit                                                     |
| Publisher | IEOM Society International                                                                                                          |
| Track     | High School STEM Poster Competition                                                                                                 |
| Date      | October 9–11, 2024                                                                                                                  |
| Pages     | 5 (504–508)                                                                                                                         |
| DOI       | 10.46254/wc01.20240169                                                                                                              |
| ISBN      | 979-8-3507-1740-2                                                                                                                   |
| Keywords  | CoT, Chain of Thought, LLMs, SLMs, GPT-2                                                                                            |

## Models & Benchmark

| Model | Sizes tested |
|-------|-------------|
| GPT-2 | 117M, 345M, 774M, 1558M |
| GPT-Neo | 125M, 1.3B, 2.7B |

Benchmark: GSM8K (grade-school math word problems).

## Key Results

**Absolute accuracy (standard → CoT):**

| Model | Standard | CoT | Δ |
|-------|----------|-----|---|
| GPT-2 117M | 3.5 | 3.5 | 0 |
| GPT-2 345M | 12.5 | 6.8 | −5.7 |
| GPT-2 774M | 20.8 | 13.7 | −7.1 |
| GPT-2 1558M | 38.0 | 20.1 | −17.9 |
| GPT-Neo 125M | 1.7 | 0 | −1.7 |
| GPT-Neo 1.3B | 14.5 | 8.8 | −5.7 |
| GPT-Neo 2.7B | 20.0 | 13.7 | −6.3 |

**Relative decrease:** 31.5–47.1% for GPT-2, 31.5–100% for GPT-Neo.

**Key findings:**
1. Performance loss is proportional/multiplicative (not additive) — larger base scores have more "to lose"
2. Convergence effect: CoT scores cluster closer together than standard scores, suggesting a CoT-induced performance ceiling
3. Architectural differences matter: GPT-Neo models show slightly more resilience than similarly-sized GPT-2
4. Lower-bound threshold effect: GPT-2 117M shows no change; GPT-Neo 125M collapses completely (1.7 → 0)
