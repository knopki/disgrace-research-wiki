---
title: Semantic Anchors
created: 2026-06-17
updated: 2026-06-17
type: concept
tags: [agent, tool-use, technique]
sources:
  - "[Позиционные кодировки: «объемное зрение» GPT и секреты AI-агентов](raw/articles/2025-07-04-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/index.md)"
confidence: medium
---

# Semantic Anchors

**Semantic Anchors** are stable, unique markers placed in source code (e.g. `# ANCHOR: password_check_start`) that give AI coding agents precise semantic coordinates for patching and editing. They solve a fundamental mismatch between how LLMs and humans reference code locations.

## The Problem

Due to [[positional-encoding|Positional Encoding]], LLMs perceive code as a multi-scale nested semantic structure — not as a flat sequence of line numbers. Asking a model to "replace line 25" is like asking someone to navigate a 3D building using only street addresses: the coordinate system doesn't align with the model's internal representation. ^[raw/articles/2025-07-04-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/index.md]

This is why tools like Cursor generate patches as semantic descriptions ("find the `validatePassword` call inside the hash-check block and replace it") rather than line-number diff formats. Semantic descriptions work, but they are fragile — ambiguous if multiple matching contexts exist.

## The Solution

Anchors are deliberately placed comments that create unique, stable semantic landmarks:

```python
# ANCHOR: password_check_start
if not check_password_strength(password):
    return False
# ANCHOR: password_check_end
```

These markers:
- Create **unique semantic signatures** that are unambiguous in the model's high-dimensional space
- **Survive code drift** — unlike line numbers, they move with the code
- **Reduce token budget** for sparsely-attended large contexts by giving the model a precise focus point
- Work with the model's native PE-based representation rather than fighting it

## Evidence

When Vladimir Ivanov tested this hypothesis by asking Claude 4 Opus (Anthropic) to generate a patch example, the model independently proposed the `# ANCHOR:` format without prompting. The author reports extracting this as Anthropic's "secret sauce" for achieving top results on the [[superposition|SWE Bench]] benchmark — their AI agents likely use a system of semantic anchors to reliably locate patch sites and focus their sparse attention budget. ^[raw/articles/2025-07-04-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/index.md]

## Distinction

Semantic anchors differ from:
- **Line numbers** — flat, PE-incompatible coordinate system
- **Semantic descriptions** (e.g. "find the function call in the else block") — fragile, ambiguous in repeated structures
- **Conventional comments** — no consistent naming scheme, no guarantee of uniqueness
- **Tags/todos** — no standard machine-readable format

## Cross-Links

- [[positional-encoding|Positional Encoding]] — the architectural feature that necessitates semantic anchors
- [[vibe-coding|Vibe Coding]] — anchors are part of the tooling shift toward AI-native programming
- [[innate-parallelism|Innate Parallelism]] — the broader context of AI-adapted development workflows
- [[contract-programming|Contract Programming]] — the higher-level semantic framework that anchors fit into; modular contracts → function contracts → ANCHOR markers form a navigation hierarchy
