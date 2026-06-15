---
title: Rational Unified Process (RUP)
created: 2026-06-15
updated: 2026-06-15
type: concept
tags:
  - methodology
  - planning
sources: "[Rational unified process - Wikipedia](raw/articles/rational-unified-process-wikipedia.md)"
confidence: high
---

The **Rational Unified Process (RUP)** is an iterative software development process framework created by Rational Software Corporation (acquired by IBM in 2003). It is an adaptable framework, not a single prescriptive process — project teams select and tailor elements appropriate to their context.

RUP is the most well-known implementation of the Unified Process methodology.

## History

- **Origins:** Combined Rational's field experience with Objectory's use-case practices, Rumbaugh's OMT, Booch's method, and UML 0.8. Led by Philippe Kruchten.
- **1997–1999:** Added requirements, test, configuration management, project management disciplines. First book published by Jacobson, Booch, Rumbaugh.
- **2003:** IBM acquired Rational Software.
- **2006:** IBM created OpenUP, an open-source agile subset of RUP, released via Eclipse.

## Structure

### Building Blocks

- **Roles** — who performs work
- **Tasks** — what work is performed (step-by-step)
- **Artifacts** — what is produced (documents, models, code)
- **Guidance** — how tasks are performed (templates, checklists, examples)

### Nine Disciplines

Business Modeling, Requirements, Analysis & Design, Implementation, Test, Deployment, Configuration & Change Management, Project Management, Environment.

### Four Life-Cycle Phases

1. **Inception** — scope the system, validate costing. Milestone: Lifecycle Objective.
2. **Elaboration** — mitigate key risks, establish architecture baseline. Milestone: Lifecycle Architecture.
3. **Construction** — build the system through multiple iterations.
4. **Transition** — deploy into production. Milestone: Product Release.

### Six Best Practices

1. Develop software iteratively
2. Manage requirements
3. Use component-based architectures
4. Visually model software (using UML)
5. Verify software quality continuously
6. Control changes to software

## Relationship to the Wiki

RUP represents the mature, pre-AI era of systematic software development methodology — use-case driven, architecture-centric, iterative and risk-mitigating. It provides a contrast to [[vibe-coding|Vibe Coding]], where the programmer shifts from directing detailed process work to directing intent. Where RUP prescribes explicit roles, artifacts, and phase gates, [[vibe-coding|Vibe Coding]] collapses many of these into AI-mediated feedback loops.

RUP's emphasis on visual modeling (UML) and formal use-case specification shares DNA with [[contract-programming|Contract Programming]]'s approach to specifying preconditions, postconditions, and invariants — both seek to make software semantics explicit and verifiable before implementation.

The RUP principle of iterative risk mitigation maps to a pattern in modern AI agent development: agents explore multiple approaches within a single turn, validate architecture early (elaboration phase of thought), then construct incrementally.

## Related

- Unified Process — the general methodology RUP implements
- [[contract-programming|Contract Programming]] — shared emphasis on explicit specification
- [[vibe-coding|Vibe Coding]] — contrasting paradigm where process structure is delegated to AI
