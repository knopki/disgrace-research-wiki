---
title: SLM vs MoE for Agentic AI
created: 2026-06-15
updated: 2026-06-15
type: concept
tags:
  - model
  - architecture
  - comparison
sources:
  - "[Причины наблюдаемого провала малых SLM против LLM на MoE в AI-агентах](raw/articles/2025-09-14-ivanov-prichiny-nabludaemogo-provala-malyh-slm-protiv-llm-na-moe-v/ivanov2025slmvsllm.md)"
---

# SLM vs MoE for Agentic AI

The debate over whether Small Language Models (SLM, <7B parameters) or large Mixture-of-Experts (MoE) models will dominate AI agent workloads. Belcak et al. (2025, NVIDIA Research) argued that SLMs are the future of agentic AI due to operational efficiency and cost. Ivanov (2025) counters with three arguments based on market data and architectural innovation.

## Belcak et al. (2025) Thesis

NVIDIA Research proposed that SLMs are sufficiently capable, operationally superior, and economically advantageous for most agent-system tasks. The argument rests on:

- SLM inference cost is a fraction of large models
- SLM can be fine-tuned per-agent more easily
- Edge deployment of SLM avoids API dependency

## Ivanov (2025) Counter-Arguments

### 1. Market Data Contradicts SLM Adoption

OpenRouter tool-call usage data shows:

| # | Model | Provider | Tool Calls | Share |
|---|-------|----------|------------|-------|
| 1 | GPT-4.1 Mini | OpenAI | 10.4M | 32.7% |
| 2 | GPT-4-mini | OpenAI | 7.08M | 22.3% |
| 3 | Claude Sonnet 4 | Anthropic | 3.35M | 10.5% |
| 4 | Gemini 1.5 Flash | Google | 2.91M | 9.1% |
| 5 | Gemini 2.0 Flash | Google | 2.1M | 6.6% |

All top models are medium-sized (7-70B), not SLM (<7B). In verticals like finance (ERP, accounting) and healthcare (RAG agents), SLM are completely absent — developers use heterogenous stacks with Qwen3-235B and Llama 3 70B alongside efficient medium models.

### 2. MoE + MTP Levels the Cost Field

High-sparsity MoE architectures with Multi-Token Prediction (MTP) eliminate the SLM cost advantage. **Qwen3-Next-80B-A3B-Instruct** exemplifies this:

- **Total parameters:** 80B — LLM-level knowledge and reasoning
- **Active parameters per token:** ~3B — same FLOPs as a 3B SLM
- **MTP:** generates multiple tokens per forward pass, reducing latency and increasing throughput

For developers with cloud access (sufficient VRAM), the choice between a 3B SLM and an 80B MoE with 3B active parameters is clear: the same compute cost buys incomparably higher quality. MTP is unavailable in SLMs, compounding the gap.

### 3. Free Tiers Commoditize Low-Intensity Tasks

Belcak et al. see SLM fitting low-intensity use cases (prototypes, education, internal tools). Ivanov counters that self-hosting even a small SLM incurs TCO (setup, monitoring, updates, fine-tuning), while Gemini Flash and other models offer generous free tiers. OpenRouter data confirms developers choose zero-cost, zero-maintenance APIs over self-hosted SLMs.

([Ivanov, 2025](raw/articles/2025-09-14-ivanov-prichiny-nabludaemogo-provala-malyh-slm-protiv-llm-na-moe-v/ivanov2025slmvsllm.md))

## Synthesis

The future of agentic AI is unlikely to be SLM-dominant. Instead:

- **High-efficiency MoE LLMs** (80B total, 3B active) claim the mainstream — they offer LLM quality at SLM compute cost
- **Medium-sized dense models** (GPT-4.1 Mini, Claude Sonnet, Gemini Flash) dominate tool-use workloads today
- **SLM survives** only in edge-computing and extreme-privacy niches

The debate mirrors a broader theme: architectural innovation (MoE, MTP, sparse attention) is collapsing the cost-quality distinction between small and large models faster than the SLM thesis anticipated.

## Related

- [[vladimir-ivanov|Vladimir Ivanov]] — author of the counter-position
- [[vibe-coding|Vibe Coding]] — agent-driven development context where model choice matters for agent capability
- [[kv-caching|KV Caching]] — inference optimisation technique; MTP is another orthogonal approach to throughput
- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — another architectural innovation changing the cost-quality landscape
- [[sparse-transformer|Sparse Transformer]] — foundational sparse attention work that MoE builds upon
