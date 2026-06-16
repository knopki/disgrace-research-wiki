---
title: FLEX (Few-shot Logit-Enabled XML Prompting)
created: 2026-06-16
updated: 2026-06-16
type: concept
tags:
  - technique
  - methodology
  - agent
  - optimization
sources:
  - "[Оптимизация управления ИИ агентами на SLM через методологию Few-shot Logit-Enabled XML (FLEX)](raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/ivanov2025flex.md)"
---

# FLEX (Few-shot Logit-Enabled XML Prompting)

A methodology for controlling Small Language Models (SLM) in agentic tasks, built on three pillars: structured XML prompts, few-shot examples, and logit-based verification. Introduced by Vladimir Ivanov (Turboplanner, September 2025) and validated on Qwen3-0.6B for tool selection.

## Core Principles

### 1. XML over JSON

XML is chosen as the structural format based on empirical findings that JSON produces higher semantic noise in SLM logits and slower few-shot convergence. XML's strict hierarchical structure and unambiguous closing tags provide clean delimiters that SLMs reliably track — the model predicts closing tags with 100% confidence after each block, proving it monitors XML tree structure rather than processing text as a flat sequence. This is consistent with OpenAI's guidance that JSON is not recommended at large context sizes even for LLMs. ([Ivanov, 2025](raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/ivanov2025flex.md))

### 2. Multi-Level Tool Description

Each tool is described at multiple abstraction levels within the XML structure:

- **`<Keywords>`** — lexical-level associations with relevance weights (1–9). Directly appeals to SLMs' low-level pattern-matching mechanisms by providing strong token-level cues (e.g., `buy:9|purchase:9`).
- **`<Trigger>`** — semantic condition in natural language. Helps the model understand context and activates attention correlations that suppress irrelevant tools.
- **`<Description>`** — general functionality overview. Provides deeper semantic understanding.

This layered approach gives SLMs both fast lexical shortcuts and semantic understanding.

### 3. Few-Shot Examples

The `<Examples>` block demonstrates how to apply tool knowledge through structured examples containing `<UserQuery>`, `<SelectedTool>`, and `<Confidence>` tags. Ivanov argues that SLMs are fundamentally **pattern detectors, not instruction followers** — so prompting should match their training paradigm by providing examples rather than abstract instructions. The XML format allows up to 500 examples without degrading attention.

### 4. Logit-Based Verification

The core scientific claim: only direct analysis of the model's hidden state — specifically the logit distribution at the output layer — can prove the model understood the instruction rather than arriving at the correct answer by coincidence. This is FLEX's defining differentiator from heuristic prompt engineering approaches.

## Experimental Validation

Ivanov tested FLEX on Qwen3-0.6B with a three-tool selection task (Order, Status, Cancel) with the following results:

| Signal | Result | Interpretation |
|--------|--------|----------------|
| XML structure learning | 65.74% → 99.98% for next `<Tool>` | Model learns XML hierarchy from the first few examples |
| XML tag closure | 100% confidence on `</Tool>` after content | Model tracks tree structure, not flat text |
| Semantic association (Name→Keywords) | 39–97% probability on tool names | Model links name to associated keywords before seeing examples |
| Clear tool selection (direct keywords present) | 98–99%+ softmax confidence | FLEX achieves near-certain accuracy for straightforward cases |
| Ambiguous selection (no direct keywords) | 84.68% confidence (Cancel for "changed my mind") | Model correctly infers intent even without lexical matches |

The ambiguous case — "I've changed my mind, I don't want this item anymore" → Cancel at 84.68% vs Order at 14.88% — is cited as proof that FLEX promotes genuine semantic understanding, not just string matching. ([Ivanov, 2025](raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/ivanov2025flex.md))

## Logits as a Diagnostic Tool

FLEX leverages logit analysis beyond verification:

- **Monitor learning progress:** Track how probability distributions shift across few-shot examples to determine when the model has learned the task
- **Detect overfitting:** If logit confidence is high but few-shot examples are still being memorized, the model may pattern-match rather than generalize
- **Decision criteria:** Use logit confidence thresholds rather than binary pass/fail — deploy only when the model's internal confidence reaches production level
- **Recommended example count:** 20–50 few-shot examples recommended; beyond that risks overfitting for SLMs

## SLM Ensemble for Hallucination Suppression

FLEX is compatible with ensemble methods. When multiple SLMs are available, their logit distributions can be averaged for more robust decisions. When logit access is restricted (API limitation), the `Confidence` parameter in FLEX prompts serves as a reliable proxy — Ivanov found high correlation between self-reported confidence and actual softmax probability. Low confidence triggers: re-run query on a second SLM, then aggregate through probability averaging.

## Relationship to Other Concepts

- **[[chain-of-thought|Chain-of-Thought (CoT)]]** — FLEX is presented in explicit opposition to CoT for SLMs. Ivanov argues CoT for SLMs is post-hoc rationalization, not genuine reasoning. FLEX avoids CoT entirely, relying on XML structure + few-shots + logit verification instead.

- **[[semantic-interference|Semantic Interference]]** — FLEX's choice of XML over JSON is motivated by the same principle: unambiguous structure prevents the semantic noise (interference) that emerges when models process poorly delimited formats. JSON's complex nesting and quote escaping create noise in logit distributions.

- **[[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]]** — FLEX provides a practical tool for making SLMs reliable in agentic tasks, addressing the capability gap that Ivanov himself identified. If SLMs can be controlled precisely through FLEX, it weakens the argument that only large MoE models are viable for agents.

- **[[grace|GRACE]]** — both are structured prompting methodologies. GRACE targets large-context LLM code generation with dual-purpose semantic markup. FLEX targets SLM tool selection with XML structure and logit verification. The shared DNA is deterministic, verifiable, scaffold-driven prompting.

- **[[pcam|PCAM]]** — PCAM provides the agent architecture philosophy (purpose-driven guidance > deterministic plans); FLEX provides the low-level SLM control technique.
