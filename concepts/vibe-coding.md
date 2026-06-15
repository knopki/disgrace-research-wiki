---
title: Vibe Coding
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [agent, tool-use, prediction]
sources:
  - "[AI угрожает программистам могуществом параллелизма](raw/articles/2025-06-30-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/index.md)"
---

# Vibe Coding

A term popularized by Andrej Karpathy (2025) describing a programming paradigm where the developer defines high-level intent, structure, and constraints — the "vibe" — while delegating implementation details to an AI. In the context of [[innate-parallelism|Innate Parallelism]], this extends specifically to delegating parallel logic.

## In the Context of Parallelism

Vladimir Ivanov frames vibe coding as the natural adaptation to AI's structural advantage in parallelism: if AI inherently handles concurrent code better than humans, then the programmer's role shifts from writing threads to directing purpose. ^[raw/articles/2025-06-30-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/index.md]

The programmer becomes an architect and conductor — defining the app's structure, constraints, and "atmosphere" — while the AI handles the "highest pilotage" of deadlock-free, efficiently parallelized implementation.

## Implications for Software Engineering

- The bottleneck shifts from "how to implement parallelism" to "what should the system do"
- Value of a programmer is determined less by low-level implementation skill and more by problem-framing ability
- Tooling for expressing intent (prompts, specs, guardrails) becomes more critical than tooling for expressing implementation
- Current tools (OpenMP, MPI, CUDA) designed for human workflows may become obsolete or be replaced by AI-native abstractions ^[raw/articles/2025-06-30-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/index.md]

## Open Questions

- Does vibe coding reduce or increase the need for deep systems knowledge? (You still need to recognize when the AI produces wrong parallel logic.)
- How do you debug, test, and audit AI-generated concurrent code at scale?
- Karpathy's original framing was about casual prototyping — extending it to production-grade parallel systems is a stronger claim.

## Related

- [[innate-parallelism|Innate Parallelism]] — the architectural advantage that makes vibe coding viable for parallelism
- [[human-sequential-bottleneck|Human Sequential Bottleneck]] — the human limitation vibe coding circumvents
