---
title: Chain-of-Thought Prompting (CoT)
created: 2026-06-15
updated: 2026-06-15
type: concept
tags:
  - technique
  - prompting
sources:
  - "[CoT Harms Performance of Rather Smaller Language Models](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.md)"
  - "[GPT-4.1 Prompting Guide](raw/articles/2025-04-14-openai-gpt41-prompting-guide.md)"
  - "[Оптимизация управления ИИ агентами на SLM через методологию Few-shot Logit-Enabled XML (FLEX)](raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/ivanov2025flex.md)"
---

# Chain-of-Thought Prompting (CoT)

Chain-of-Thought (CoT) prompting instructs a language model to articulate intermediate reasoning steps before producing a final answer. Introduced by Wei et al. (2022), it has become a standard component of LLM prompting.

## Effect by Model Size

CoT benefit scales with model size. Shim et al. (IEOM, 2024) tested GPT-2 (117M–1558M) and GPT-Neo (125M–2.7B) on GSM8K and found that CoT **degrades** accuracy for all models below ~3B parameters:

| Model | Standard → CoT | Relative Δ |
|-------|---------------|------------|
| GPT-2 117M | 3.5 → 3.5 | 0% |
| GPT-2 345M | 12.5 → 6.8 | −45.6% |
| GPT-2 774M | 20.8 → 13.7 | −34.1% |
| GPT-2 1558M | 38.0 → 20.1 | −47.1% |
| GPT-Neo 125M | 1.7 → 0 | −100% |
| GPT-Neo 1.3B | 14.5 → 8.8 | −39.3% |
| GPT-Neo 2.7B | 20.0 → 13.7 | −31.5% |

([Shim et al., 2024](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.md))

## Criticism: CoT as Post-Hoc Rationalization

Ivanov (2025) argues that CoT for SLMs is not genuine reasoning but **post-hoc rationalization** — the model arrives at a decision in its hidden state, then generates CoT as a plausible-sounding justification. His argument rests on two points:

1. **Hidden state precedes explanation:** The model's logit distribution at the final layer determines the output before any CoT tokens are generated. SLMs lack the capacity for multi-step internal deliberation that CoT simulates superficially.

2. **No direct verification:** Traditional prompt evaluation judges correctness, not process. Two models producing the same correct answer may have arrived via entirely different mechanisms — one through genuine understanding, one through pattern matching. Only logit analysis reveals the difference. ([Ivanov, 2025](raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/ivanov2025flex.md))

This critique aligns with the [[flex-prompting|FLEX methodology]] he proposes as an alternative: replace CoT with structured XML prompts + few-shot examples + logit-based verification as an empirically verifiable control method for SLMs.

The loss is multiplicative (proportional to baseline accuracy), and a convergence effect emerges — CoT scores cluster tighter than standard scores, suggesting a CoT-induced performance ceiling. GPT-Neo shows slightly more resilience than GPT-2 at similar sizes.

## Usage in Practice

The GPT-4.1 Prompting Guide recommends:
- Start with basic CoT: `"Let's think step by step"`
- Iteratively improve by auditing failures and codifying successful strategies
- Structured CoT with explicit sub-goals and verification steps

## Relationship to Continuous Reasoning

[[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] replaces language-space CoT with reasoning directly in the continuous latent space. Coconut outperforms standard CoT on logical reasoning tasks while using far fewer tokens, and the finding that CoT harms SLMs suggests Coconut's latent approach may be particularly valuable for smaller models.

## Related

- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — latent-space alternative
- [[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]] — CoT harming SLMs is evidence in this debate
- [[flex-prompting|FLEX (Few-shot Logit-Enabled XML Prompting)]] — alternative methodology for SLMs that replaces CoT with XML structure + logit verification
