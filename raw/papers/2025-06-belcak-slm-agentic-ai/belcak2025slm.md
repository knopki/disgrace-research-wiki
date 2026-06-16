---
source_url: https://arxiv.org/abs/2506.02153v1
ingested: 2026-06-15
authors: Peter Belcak, Greg Heinrich, Shizhe Diao, Yonggan Fu, Xin Dong, Saurav Muralidharan, Yingyan Celine Lin, Pavlo Molchanov
title: Small Language Models are the Future of Agentic AI
date: 2025-06-01
---

# Small Language Models are the Future of Agentic AI

**Authors:** Peter Belcak, Greg Heinrich, Shizhe Diao, Yonggan Fu, Xin Dong, Saurav Muralidharan, Yingyan Celine Lin, Pavlo Molchanov  
**Institution:** NVIDIA Research  
**arXiv:** [2506.02153v1](https://arxiv.org/abs/2506.02153v1) [cs.AI]  
**License:** CC BY 4.0

## Abstract

Large language models (LLMs) are often praised for exhibiting near-human performance on a wide range of tasks and valued for their ability to hold a general conversation. The rise of agentic AI systems is, however, ushering in a mass of applications in which language models perform a small number of specialized tasks repetitively and with little variation. Here we lay out the position that small language models (SLMs) are sufficiently powerful, inherently more suitable, and necessarily more economical for many invocations in agentic systems, and are therefore the future of agentic AI. Our argumentation is grounded in the current level of capabilities exhibited by SLMs, the common architectures of agentic systems, and the economy of LM deployment. We further argue that in situations where general-purpose conversational abilities are essential, heterogeneous agentic systems (i.e., agents invoking multiple different models) are the natural choice. We discuss the potential barriers for the adoption of SLMs in agentic systems and outline a general LLM-to-SLM agent conversion algorithm. Our position, formulated as a value statement, highlights the significance of the operational and economic impact even a partial shift from LLMs to SLMs is to have on the AI agent industry.

## Key Arguments

### V1–V3: Core Statements
- **V1** — SLMs are sufficiently powerful for agentic language modeling errands.
- **V2** — SLMs are inherently more operationally suitable (lower latency, less memory, better alignment).
- **V3** — SLMs are necessarily more economical (10–30× cheaper per inference vs. 70–175B LLMs).

### A1: SLMs are already sufficiently powerful
| Model | Size | Key Comparison |
|-------|------|----------------|
| Microsoft Phi-2 | 2.7B | On par with 30B models |
| Phi-3 small | 7B | Matches 70B |
| Nemotron-H (hybrid Mamba-Transformer) | 2/4.8/9B | Accuracy comparable to dense 30B |
| SmolLM2 | 125M–1.7B | Matches 14B contemporaries, 70B models of 2 years prior |
| Hymba-1.5B | 1.5B | Best instruction accuracy, 3.5× token throughput |
| DeepSeek-R1-Distill | 1.5–8B | 7B outperforms Claude-3.5-Sonnet-1022 and GPT-4o-0513 |
| RETRO-7.5B | 7.5B | Comparable to GPT-3 (175B) with 25× fewer parameters |
| xLAM-2-8B | 8B | SOTA tool calling, surpasses GPT-4o and Claude 3.5 |

### A2–A7: Supporting Arguments
- **A2** — More economical (10–30× cheaper, fine-tuning agility, edge deployment, modular design)
- **A3** — More flexible (rapid iteration, democratization)
- **A4** — Agents expose only narrow LM functionality (SLM fine-tuned for specific prompts suffices)
- **A5** — Agentic interactions need close behavioral alignment (strict formatting, less hallucinatory drift)
- **A6** — Natural heterogeneity (LLM for orchestrator, SLMs for subordinates)
- **A7** — Agentic interactions are natural data sources (collect specialized instruction data for fine-tuning)

### Alternative Views and Rebuttals
- **AV1** — LLM generalists always have better language understanding → rebutted via A8–A11 (new architectures, fine-tuning, test-time compute scaling, sub-task decomposition)
- **AV2** — LLM inference cheaper via economy of scale → rebutted via A12–A13 (NVIDIA Dynamo scheduler, falling infra costs)
- **AV3** — Equally possible worlds, LLM has head start → acknowledged

## PDF

[2506.02153.pdf](2506.02153.pdf) (325KB)
