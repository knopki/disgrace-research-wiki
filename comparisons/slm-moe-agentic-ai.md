---
title: SLM vs MoE for Agentic AI
created: 2026-06-15
updated: 2026-06-15
type: comparison
tags:
  - model
  - architecture
  - comparison
  - debate
confidence: medium
contested: true
contradictions: []
sources:
  - "[Small Language Models are the Future of Agentic AI](raw/papers/2025-06-belcak-slm-agentic-ai/belcak2025slm.md)"
  - "[Причины наблюдаемого провала малых SLM против LLM на MoE в AI-агентах](raw/articles/2025-09-14-ivanov-prichiny-nabludaemogo-provala-malyh-slm-protiv-llm-na-moe-v/ivanov2025slmvsllm.md)"
  - "[CoT Harms Performance of Rather Smaller Language Models](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.md)"
  - "[Hallucination Detection with Small Language Models](raw/papers/2025-06-24-cheung-hallucination-detection-slm/cheung2025hallucination.md)"
  - "[Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md)"
---

# SLM vs MoE for Agentic AI

The debate over whether Small Language Models (SLM, <10B parameters) or large Mixture-of-Experts (MoE) models will dominate AI agent workloads. Belcak et al. (NVIDIA Research, June 2025) argue SLMs are the future of agentic AI with significant caveats for heterogeneous systems. Ivanov (September 2025) counters with market data and architectural arguments. The two positions are not fully opposed — Belcak explicitly argues for heterogeneous systems (SLMs for subordinate tasks, LLMs for orchestration), while Ivanov argues MoE + MTP collapses the cost-quality gap to favor large models even at SLM-level compute.

## Belcak et al. (2025) Position

### Core Thesis (V1–V3)
- **V1** — SLMs are sufficiently powerful for agentic language modeling errands
- **V2** — SLMs are inherently more operationally suitable (lower latency, less memory, better behavioral alignment)
- **V3** — SLMs are necessarily more economical (10–30× cheaper per inference vs. 70–175B LLMs)

> "The dominance of LLMs in the design of AI agents is both excessive and misaligned with the functional demands of most agentic use cases."

### A1: SLMs Are Already Sufficiently Powerful

| Model | Size | Key Comparison |
|-------|------|----------------|
| Microsoft Phi-2 | 2.7B | On par with 30B models (commonsense, code), ~15× faster |
| Phi-3 small | 7B | Matches 70B (language understanding, code) |
| Nemotron-H (hybrid Mamba-Transformer) | 2/4.8/9B | Accuracy comparable to dense 30B LLMs, order-of-magnitude fewer FLOPs |
| SmolLM2 | 125M–1.7B | Matches 14B contemporaries, 70B models of 2 years prior |
| Hymba-1.5B | 1.5B | Best instruction accuracy, 3.5× token throughput vs. comparable [[transformer|transformers]]; outperforms 13B models |
| DeepSeek-R1-Distill | 1.5–8B | 7B outperforms Claude-3.5-Sonnet-1022 and GPT-4o-0513 |
| RETRO-7.5B | 7.5B | Comparable to GPT-3 (175B) with 25× fewer parameters |
| xLAM-2-8B | 8B | SOTA tool calling, surpasses GPT-4o and Claude 3.5 |

Capability — not parameter count — is the binding constraint, they argue.

### A2–A7: Supporting Arguments
- **A2 — More economical:** 10–30× cheaper serving cost, fine-tuning agility (LoRA/DoRA), edge deployment (ChatRTX), modular "Lego-like" composition of specialized SLMs
- **A3 — More flexible:** Rapid iteration for evolving user needs, democratizes AI agent development
- **A4 — Narrow LM functionality exposed by agents:** Agents restrict a generalist LLM to a small subset of its skills — a SLM fine-tuned for specific prompts suffices
- **A5 — Behavioral alignment:** Strict formatting (JSON/XML/Python) is required for tool calls; SLMs trained with a single formatting decision are less prone to hallucinatory format drift
- **A6 — Natural heterogeneity:** Agentic systems can invoke different LMs for different sub-tasks; LLM for root orchestrator, SLMs for subordinates; or all SLMs if code agency is used
- **A7 — Natural data sources:** Each tool/model call collects specialized instruction data for future fine-tuning of expert SLMs

### Alternative Views and Rebuttals
- **AV1 — LLM generalists always have better language understanding** → rebutted (A8–A11): new SLM architectures (hybrid Mamba-Transformer) break scaling law assumptions; SLMs can be fine-tuned for specific tasks; test-time compute scaling is more affordable for SLMs; complex inputs are decomposed into sub-tasks by the agent — the "semantic hub" is unnecessary
- **AV2 — LLM inference is cheaper via economy of scale** → rebutted (A12–A13): NVIDIA Dynamo scheduler and other tools offer flexibility; setup costs for inference infrastructure are falling
- **AV3 — Equally possible worlds, LLM has head start** → **acknowledged.** The paper does not claim SLM-only dominance — it explicitly argues for heterogeneous systems where general-purpose conversational abilities are essential

([Belcak et al., 2025](raw/papers/2025-06-belcak-slm-agentic-ai/belcak2025slm.md))

## Ivanov (2025) Counter-Position

**Source:** VK/Turboplanner. September 2025.

### 1. Market Data Contradicts SLM Adoption

OpenRouter tool-call usage (as of September 2025):

| # | Model | Provider | Tool Calls | Share |
|---|-------|----------|------------|-------|
| 1 | GPT-4.1 Mini | OpenAI | 10.4M | 32.7% |
| 2 | GPT-4-mini | OpenAI | 7.08M | 22.3% |
| 3 | Claude Sonnet 4 | Anthropic | 3.35M | 10.5% |
| 4 | Gemini 1.5 Flash | Google | 2.91M | 9.1% |
| 5 | Gemini 2.0 Flash | Google | 2.1M | 6.6% |

All top models are medium-sized (7–70B), not SLM (<7B). In verticals like finance and healthcare, SLMs are completely absent — developers use heterogeneous stacks with Qwen3-235B and Llama 3 70B alongside efficient medium models.

### 2. MoE + MTP Levels the Cost Field

High-sparsity MoE architectures with Multi-Token Prediction (MTP) eliminate the SLM cost advantage. **Qwen3-Next-80B-A3B-Instruct**:
- Total parameters: 80B — LLM-level knowledge and reasoning
- Active parameters per token: ~3B — same FLOPs as a 3B SLM
- MTP generates multiple tokens per forward pass, reducing latency and increasing throughput

The foundation for this architecture was laid by the [[switch-transformer|Switch Transformer]] (Fedus et al., Google, 2021), which demonstrated that simplified single-expert MoE routing enabled trillion-parameter sparse models with constant compute cost. Modern MoE models (Mixtral, Qwen MoE, DeepSeek MoE) are direct architectural descendants.

For cloud-accessible developers, the same compute cost buys incomparably higher quality from MoE. MTP is unavailable in SLMs, compounding the gap.

### 3. Free Tiers Commoditize Low-Intensity Tasks

Belcak et al. see SLM fitting low-intensity use cases. Ivanov counters that self-hosting even a small SLM incurs TCO (setup, monitoring, updates, fine-tuning), while Gemini Flash and other models offer generous free tiers.

([Ivanov, 2025](raw/articles/2025-09-14-ivanov-prichiny-nabludaemogo-provala-malyh-slm-protiv-llm-na-moe-v/ivanov2025slmvsllm.md))

## Synthesis

The two positions overlap more than they conflict.

| Dimension | Belcak et al. | Ivanov |
|-----------|--------------|--------|
| **Optimal model for narrow agentic tasks** | SLM (<10B) | MoE (80B total, 3B active) or medium (7–70B) |
| **Heterogeneous systems** | Explicitly advocated (LLM orchestrator + SLM workers) | Implicitly practiced (developers use mixed stacks) |
| **Cost-compute ratio** | SLMs win on absolute cost | MoE wins on quality-per-FLOP at similar active-parameter count |
| **Edge deployment** | Critical advantage for SLMs | Acknowledged niche, not mainstream |
| **Key evidence** | Benchmarks showing SLMs match larger models | Market usage data showing no SLM adoption |
| **Prompting robustness** | Not addressed | CoT prompting — standard for LLMs — degrades SLM accuracy by 15–30%+, with losses of 31–47% on GPT-2 and up to 100% on GPT-Neo 125M (Shim et al., 2024) |
| **Verification performance** | Not addressed | SLM ensemble (1.5B + 2B) outperforms ChatGPT by ~10% F1 for hallucination detection in RAG context (Cheung, 2025) |
| **Time horizon** | Forward-looking (SLM capabilities improving) | Present-day (what developers actually use) |

**Key tension:** Both sides agree that agents expose narrow functionality. Belcak concludes "therefore SLM suffices." Ivanov counters "therefore why would I self-host a SLM when a free API gives me a better model?" The unresolved question is whether MoE + MTP can sustain its cost-quality advantage as SLM architectures continue to improve.

**Bottom line:** The agentic AI future is unlikely to be SLM-dominant, but Belcak et al.'s heterogeneous system view is consistent with current practice (medium models dominate tool-use, large models handle orchestration). Ivanov's strongest counter is that MoE defeats the SLM cost argument — not that SLMs lack capability.

**Additional evidence:** Shim et al. (IEOM, 2024) provide experimental evidence that CoT prompting degrades SLM accuracy by 15–30%+ on GSM8K — with relative losses of 31–47% on GPT-2 (345M–1558M) and up to 100% on GPT-Neo 125M. The loss is multiplicative (proportional to baseline), not additive, and CoT scores converge toward a ceiling, suggesting SLMs lack capacity to benefit from CoT's reasoning decomposition. ([Shim et al., 2024](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.md))

**Cheung (2025)** provides a different kind of SLM evidence: rather than measuring SLM weaknesses, they demonstrate a narrow verification task where SLMs *outperform* ChatGPT. Their multi-SLM framework (Qwen2-1.5B + MiniCPM-2B) detects hallucinations in RAG responses with ~10% higher F1 than ChatGPT P(True) and ~6.6% higher than a single SLM P(yes) baseline. This strengthens the heterogeneous-system view: SLMs can be *better* than LLMs for specific well-scoped verification subtasks, not just cheaper. See [[hallucination-detection-slm|SLM-based Hallucination Detection]] for details. ([Cheung, 2025](raw/papers/2025-06-24-cheung-hallucination-detection-slm/cheung2025hallucination.md))

## Related

- [[vladimir-ivanov|Vladimir Ivanov]] — author of the counter-position
- [[vibe-coding|Vibe Coding]] — agent-driven development context where model choice matters
- [[hallucination-detection-slm|SLM-based Hallucination Detection]] — SLMs outperform ChatGPT for RAG verification, supporting heterogeneous systems
- [[kv-caching|KV Caching]] — inference optimisation; MTP provides orthogonal throughput gains
- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — architectural innovation changing cost-quality landscape
- [[chain-of-thought|Chain-of-Thought Prompting (CoT)]] — CoT harms SLMs, relevant to both sides of the SLM debate
- [[sparse-transformer|Sparse Transformer]] — foundational sparse attention work for MoE architectures
- [[switch-transformer|Switch Transformer]] — foundational MoE architecture that enabled trillion-parameter sparse models with simplified routing; direct predecessor of modern MoE LLMs
