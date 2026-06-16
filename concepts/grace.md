---
title: GRACE (Graph-RAG Anchored Code Engineering)
created: 2026-06-15
updated: 2026-06-16
type: concept
tags:
  - methodology
  - agent
  - framework
  - technique
sources:
  - "[GRACE: Фреймворк создания кода LLM в больших контекстах](raw/articles/2025-09-13-ivanov-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/ivanoc2025grace.md)"
  - "[Семантическая разметка GRACE как нативный интерфейс для Mamba-моделей](raw/articles/2025-09-21-ivanov-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m/ivanov2025gracemamba.md)"
confidence: medium
---

# GRACE (Graph-RAG Anchored Code Engineering)

> A system for structuring source code with XML-like tags and contracts for efficient AI-agent navigation via RAG and attention mechanism management.

**GRACE** (Graph-RAG Anchored Code Engineering) — a methodology for deterministic LLM-assisted code development that addresses the fundamental problems of stochasticity, uncontrolled initiative, and context fragmentation. Developed by [[vladimir-ivanov|Vladimir Ivanov]].

The core insight: the same **dual-purpose semantic markup** serves as a top-down synthesis template for large-context generative models (Gemini) and as an indexed navigation map for RAG-based agents (Cursor, Claude Code). This transforms code generation from a probabilistic act into a controlled, traceable engineering process.

## Philosophical Core

The fundamental goal of GRACE is to **extract hidden architectural decisions, business requirements, and intentions** from two sources:
- The developer's mind (tacit knowledge, design rationale)
- The LLM's hidden state (implicit generation plans, belief states)

And capture them in **explicit, structured, machine-readable form** — as XML artifacts, semantic markup, typed contracts, and linked knowledge graph entries.

This extraction and externalisation is what turns stochastic LLM code generation into a repeatable engineering discipline. ([Ivanov, 2025](raw/articles/2025-09-13-ivanov-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/ivanoc2025grace.md))

## The Problem: Semantic Gap

The integration of LLMs into software engineering creates a **semantic gap** between high-level human goals and low-level generated code. LLMs have three interconnected failure modes:

1. **Stochasticity and excessive initiative** — faced with ambiguous tasks, LLMs invent solutions that may not align with the architectural intent, producing code that "works" but violates design assumptions
2. **Hallucination and context fragmentation** — inability to maintain coherent understanding across large projects; the model sees local details but loses the global picture
3. **Semantic gap** — the disconnect between what the developer intends and what the LLM produces is invisible until runtime, making errors expensive and unpredictable

Existing approaches (prompt engineering, RAG agents) address context problems **unsystematically** — they treat symptoms rather than causes. GRACE replaces unstructured interpretation with a **deterministic top-down refinement process** where each step is an approved refinement of the previous one, and the human approves every level before proceeding. ([Ivanov, 2025](raw/articles/2025-09-13-ivanov-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/ivanoc2025grace.md))

## Ten Principles

**1. Intent-First Architecture.** Development begins not with code but with a hierarchy of machine-readable intent artifacts (RequirementsAnalysis.xml → Technology.xml → DevelopmentPlan.xml), created via [[semantic-fractal|fractal prompting]].

**2. Synthesis from Approved Blueprints.** Code generation is a deterministic "compilation" of an approved scaffold, not free-form production.

**3. AI-Readable Scaffolding.** Source code is annotated with paired XML-like semantic anchors and contracts — a structured markup language that guides both generation and navigation.

**4. Context via Knowledge Graph.** All project artifacts are linked into a unified graph via explicit `LINKS` references, supporting the attention mechanism's understanding of cross-component relationships.

**5. Dual-Purpose Semantic Markup.** The same markup serves two distinct AI architectures:
- For **generative models** — a refinable template for controlled top-down synthesis
- For **RAG agents** — an indexed navigation map for instant bottom-up and up-down navigation

**6. Proportional Granularity.** Markup detail is proportional to component criticality and roughly matches the LLM's sliding window (~500 tokens). Not applied where unnecessary.

**7. Code as Living Document.** Any code change requires synchronous contract updates. This is achieved by 100% AI-driven code generation with automatic contract maintenance — contracts and code evolve together as a single, AI-maintained system.

**8. Observable AI Belief State.** Plans verbalised from the LLM's hidden state, the explicit semantic skeleton, and structured logs tied to semantic blocks together make the AI's "belief" about how the code should work visible and auditable — transforming code generation from a black box into a transparent, element-level model of *why* the AI made each generation decision.

**9. End-to-End Traceability.** Full traceability from business requirement to log line, achieved by total graph linkage across all artifacts — every line of generated code can be traced back through its semantic anchors to the originating requirement.

**10. Governed Autonomy.** The human role shifts from code author to architect and verifier. AI has freedom of action within the semantic scaffold, but not beyond it. The contract defines the "playable space."

## Key Artifacts

| Artifact | Purpose |
|----------|---------|
| **RequirementsAnalysis.xml** | Machine-readable use-case model using Actor-Action-Goal (AAG) notation |
| **Technology.xml** | Declared technology stack with versioning guidelines and API compatibility rules |
| **DevelopmentPlan.xml** | Architectural blueprint — the "compilation target" for code generation |
| **Semantic markup** | Paired XML-like tags (`<block_name>...</block_name>`) + MODULE_CONTRACT / MODULE_MAP in source code |
| **Structured logs** | Log format tied to semantic blocks via anchors, serving as belief state declarations |

All planning artifacts are generated via [[semantic-fractal|fractal prompting]] — the method by which the LLM produces structured, self-similar specifications at each layer of the hierarchy.

## Process Model

GRACE defines a five-stage iterative process that systematically reduces uncertainty:

1. **Requirements Analysis.** Formalise user scenarios with Actor-Action-Goal (AAG) notation. Creates unambiguous, machine-readable domain model that serves as the foundation for all subsequent development.

2. **Technology Stack Selection.** Declare languages, frameworks, libraries with explicit versioning guidelines and API compatibility rules. Prevents the common failure mode where LLMs generate code for outdated or incompatible dependency versions, eliminating hours of environment debugging.

3. **Architectural Scaffold Design.** The AI creates a detailed system blueprint (DevelopmentPlan.xml). Two critical sub-steps:
   - **Non-human programming techniques:** AI receives guidelines for patterns optimal for determinism and clarity (avoiding implicit type coercion, using explicit returns over exceptions for flow control) — even if more verbose for humans, these patterns reduce hallucination risk
   - **Mental Tests:** The AI performs step-by-step dry-runs of key algorithms and data flows at pseudocode level. Successful mental tests are mandatory before plan approval — this is the "compile-time" verification of GRACE

4. **Deterministic Code Generation from Semantic Template.** The AI "compiles" the approved DevelopmentPlan.xml using the provided semantic scaffold. Every file, class, and function follows contracts and markup defined in the plan — generation becomes filling in predefined slots, not free creation.

5. **Verification and Maintenance.** Generated code is verified against structured logs. Deviations trigger new cycles starting from the appropriate stage (Stage 3 for logic errors, Stage 1 for misunderstood requirements). This staged rollback is what makes the process robust — errors are caught at the level where they originate. ([Ivanov, 2025](raw/articles/2025-09-13-ivanov-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/ivanoc2025grace.md))

## Dual-Purpose Semantic Markup in Action

The semantic markup is not just comments — it is a structured language that serves two fundamentally different AI architectures:

### Overcoming Sparse Attention Limitations

In large contexts (>100K tokens), the transformer's attention mechanism degrades non-linearly — attention becomes sparse and long-range dependencies are lost. XML-like paired tags act as high-signal "vector beacons" — the model easily establishes correlation between identical tag tokens even at large distances, semantically "stitching" logically related but physically separated code sections. ([Ivanov, 2025](raw/articles/2025-09-13-ivanov-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/ivanoc2025grace.md))

### Materialising the Internal Generation Plan

LLMs form a hidden internal plan before generating text. The GRACE semantic scaffold is an exact, explicit verbalisation of this plan — the model no longer needs to simultaneously hold both plan and implementation details in its hidden state. It focuses on sequentially filling predefined blocks, reducing cognitive load and improving code coherence.

### Belief State Declaration

Working inside a named block lets the AI focus on a single atomic task. The log line created in that block becomes an explicit declaration of the AI's "belief state" — a hypothesis about how the code should behave at that point. This transforms logging from passive fact-recording into **active self-reflection**: the model articulates what it believes the code should do, and the log becomes auditable evidence of that belief. ([Ivanov, 2025](raw/articles/2025-09-13-ivanov-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/ivanoc2025grace.md))

### Hierarchical Navigation for RAG Agents

GRACE provides RAG agents (Cursor, Claude Code) with a highly efficient navigation route:
1. Start at the project-wide knowledge graph
2. Navigate to a specific module's MODULE_CONTRACT
3. Navigate to the target function's contract

This hierarchy lets the agent **progressively collect all relevant context** for modification, rather than scanning the entire codebase. The article reports >90% of cases require no further context-seeking beyond this hierarchical approach. ([Ivanov, 2025](raw/articles/2025-09-13-ivanov-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/ivanoc2025grace.md))

### Direct Navigation and Deterministic Patching

Two mechanisms for precision work:
- **Log-to-code navigation:** Structured logs contain exact coordinates (function name, block name), letting the agent jump instantly to the problem source via anchor search — one search, zero ambiguity
- **Semantic coordinate solution:** GRACE anchors solve the [[positional-encoding|line-number problem]] — they provide stable semantic coordinates (unlike fragile line numbers) for reliable patch application via formats like [[v4a-diff-format|V4A]], making code modification as deterministic as navigation

### Mamba/SSM Synergy: Native Interface

Experimental research on Qwen-3-Next (hybrid Mamba-Transformer, >75K token context) revealed that GRACE's XML-like hierarchical markup functions as a **native interface language** for State Space Models ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m/ivanov2025gracemamba.md)).

**Dual role of the graph.** The GRACE graph plays fundamentally different roles depending on architecture:
- For **Transformers** — a *passive assistant* for sparse attention. Bright, repeating XML tags (START_FUNCTION_A...END_FUNCTION_A) act as beacons that help the attention mechanism establish correlation across long distances, semantically stitching the context.
- For **Mamba/SSM** — an *active verification shield*. Mamba builds its own emergent graph in its compressed state. The explicit GRACE scaffold becomes a "blueprint" against which the model compares its internal graph — any discrepancy triggers correction, fundamentally reducing structural hallucinations.

**Reconstruction vs citation.** Mamba does not "cite" text via attention like a Transformer. With GRACE markup it *reconstructs* code from its internal knowledge graph — a reconstruction query becomes node serialisation. Without GRACE, reconstruction degrades into imprecise paraphrase from the compressed state, losing precision in string literals, escape sequences, and inline comments.

**Semantic slices.** Mamba can perform *semantic slices* on its internal state — answering queries like "show all imports" or "group classes by role" directly from graph nodes, not raw text. This enables RAG agents to execute complex analytical queries orders of magnitude more efficiently than traditional text-based RAG.

**Risk: structural hallucinations.** Accuracy exceeds 99.9% for whole blocks (classes, functions) but varies by slice type. Leaf-level details (string literals, escape sequences) and meta-pattern generalisation are prone to hallucination. The combination therefore requires a **built-in RAG verification cycle**: after generation, the agent must verify key facts using its attention window.

**Three-part symbiosis.** The research proposes a production architecture: (1) Human architect creates machine-readable blueprints (GRACE); (2) Mamba builds a queryable internal graph, using the explicit scaffold as verification tool; (3) Built-in RAG cycle uses attention to verify facts, compensating for SSM's tendency to generalise. ([Ivanov, 2025](raw/articles/2025-09-21-ivanov-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m/ivanov2025gracemamba.md))

## Connections to Other Methodologies

GRACE does not exist in isolation. It is the **code-creation counterpart** to [[pcam|PCAM]]'s agent-management paradigm. Together, they form the two pillars of a coherent engineering shift:

| Dimension | PCAM | GRACE |
|-----------|------|-------|
| Domain | Agent *management* | Code *creation* |
| Problem | Rigid plans waste agent capability | Stochastic generation produces unreliable code |
| Solution | Purpose-driven agents with guides | Scaffold-driven generation with contracts |
| Human role | Goal setter + plan approver | Architect + semantic scaffold designer |
| Key mechanism | Guides + standardized protocols | XML artifacts + dual-purpose markup |
| Scale | Multi-agent team orchestration | Single-project code synthesis |

Both reject the old control-based paradigm (deterministic plans for PCAM, free-form prompting for GRACE) and replace it with a **scaffold-based paradigm** — structured guidance that channels AI capability without constraining it.

### Individual Cross-Links

- [[semantic-anchors|Semantic Anchors]] — GRACE formalises and extends the `# ANCHOR:` pattern into a full XML-like structured markup methodology with dual purpose
- [[contract-programming|Contract Programming]] — MODULE_CONTRACT/MODULE_MAP elements in GRACE are the concrete implementation of contract programming within a top-down scaffold
- [[vibe-coding|Vibe Coding]] — GRACE is a concrete, production-grade methodology for implementing vibe coding's intent-delegation paradigm at enterprise scale
- [[positional-encoding|Positional Encoding]] — GRACE's semantic anchors are a direct response to the line-number problem caused by PE's nested coordinate system; tag beacons leverage PE's correlative ability
- [[belief-state-geometry|Belief State Geometry]] — GRACE's Observable AI Belief State principle operationalises belief state visibility: structured logs become explicit belief declarations, turning the model's hidden state into auditable artifacts
- [[semantic-fractal|Semantic Fractal]] — all GRACE planning artifacts are created via fractal prompting; the hierarchical scaffold (knowledge graph → module contract → function contract) is a concrete engineering instantiation of the fractal structure
- [[semantic-interference|Semantic Interference]] — GRACE's top-down deterministic refinement prevents the "semantic mush" problem by constraining each generation step to a well-defined scope
- [[knowledge-graph|Knowledge Graph]] — the entire project artifact graph is explicitly maintained as a knowledge graph via LINKS references between artifacts, supporting attention-based cross-component reasoning
- [[retrieval-augmented-generation|RAG]] — the dual-purpose markup specifically addresses RAG agent limitations: hierarchical navigation, context collection, and deterministic patching
- [[human-sequential-bottleneck|Human Sequential Bottleneck]] — GRACE's governed autonomy mirrors the shift from human-linear to AI-parallel workflows; the non-human programming techniques in Stage 3 are a concrete example of exploiting this advantage
- [[mamba|Mamba / SSM]] — two dimensions: (1) Mamba+RAG self-correction addresses factual accuracy, the next step after GRACE's structural context integrity; (2) GRACE markup serves as a native interface for Mamba, enabling reconstruction-from-graph, semantic slices, and active verification (vs passive attention assistance for Transformers)