---
title: Contract Programming
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [technique, methodology, agent, tool-use]
sources:
  - "[Контрактное программирование: Ваш семантический щит в эпоху искусственного интеллекта](raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md)"
confidence: medium
---

# Contract Programming

**Contract Programming** is the adaptation of Bertrand Meyer's Design by Contract (DbC) methodology for the era of AI-assisted software development. Where traditional DbC used formal preconditions, postconditions, and invariants to guarantee correctness, AI-era contracts embed rich natural-language semantic specifications directly in code comments — serving as a "semantic shield" that prevents LLM agents from making destructive modifications.

## Motivation: The Problem of Semantic Incompleteness

When an LLM agent modifies code it does not fully understand, it has no way to distinguish essential invariants from implementation details. Without explicit semantic guardrails, the agent treats all code as equally modifiable — leading to what the article calls the "skyscraper collapse": the AI removes a load-bearing wall while "improving" the facade, and the entire structure collapses. ^[raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md]

Traditional solutions — unit tests, type annotations, formal verification — layer *more code* into the model's context, creating [[semantic-interference|semantic noise]] that obscures the core logic. Contracts solve this by being semantically explicit rather than syntactically executable.

## Core Elements

### Preconditions, Postconditions, Invariants

Following Meyer's original DbC, AI-era contracts specify:

- **Preconditions** — what must be true *before* a function executes (e.g., "input argument must not be empty")
- **Postconditions** — what the function guarantees *after* execution (e.g., "return value will be a positive integer")
- **Invariants** — conditions that remain true throughout the object's lifecycle

The critical shift: these are written in **natural language**, not formal logic. An LLM understands "the user must be authenticated before calling this endpoint" as directly as it understands `assert user.is_authenticated`. The semantic form activates the model's internal reasoning more effectively than executable assertions. ^[raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md]

### Semantic Coherence: The Spec-Contract-Code Trinity

The article introduces **semantic coherence** as the key operational principle: technical specification (ТЗ), contracts in code, and the implementation itself must speak the same language and not contradict each other. This is achieved through inline semantic markup:

```python
# SPECIFICATION: REQ-42 — data must be deduplicated before aggregation
# PRECONDITION: input is a non-empty list of records
# POSTCONDITION: result has no duplicate rows
def load_and_parse(data_source):
    ...
```

A function's contract links it to specific spec items. Log statements like `logger.debug("generating test stubs")` become **belief state declarations** — the model uses them to track *where in its semantic plan* it currently is. ^[raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md]

## Scientific Basis: Belief State Geometry

The article grounds contract programming's effectiveness in a specific transformer property discovered by Adam Shai and colleagues ([arxiv 2405.15943](https://arxiv.org/abs/2405.15943)): as an LLM generates output, it constructs a complex **belief state geometry** in its residual stream — an internal fractal plan where each node is the model's "belief" about which semantic state it occupies, and edges are transitions between states.

Contracts act as **belief state refiners**. When the model encounters a contract, it does not simply read instructions — the contract *forces* the model to narrow its belief state to exactly what the contract specifies: "Right now your belief state should be: you are writing a payment validation function. Your goal is to return True or False. Your input is a card number and an amount. Nothing else exists." ^[raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md]

This connects contract programming directly to the [[semantic-fractal|Semantic Fractal]] model — contracts are a navigation mechanism for the model's internal semantic graph.

## Contract Structure: Fractal Self-Similarity

Contracts are themselves fractal (self-similar across scales):

- **Module-level contract** — describes the file's overall purpose, dependencies, key functions, usage scenarios
- **Function-level contract** — details the specific task, inputs, outputs, side effects, test conditions

This self-similar structure lets the model "compress" the semantics of a large codebase. Instead of holding 100,000 lines in context, it operates at the concept level: "This is the payments module, I understand its contract. This function inside it is a special case of the module contract." ^[raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md]

## Contract-Driven Agent Navigation

For RAG-based AI agents (like Cursor) that read code in small fragments (100-200 lines per window), contracts solve the "seeing the trees but not the forest" problem:

1. **Read module contract** — agent gets strategic context: file role, connections, key entities
2. **Jump to function contract** — agent reads the local contract for tactical understanding
3. **Edit with context** — armed with both levels, the agent makes correct changes within a small visible window

The article claims >90% success on first attempt with this two-level contract structure, eliminating the need for the agent to request additional context. ^[raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md]

## Semantic Specifications vs. Code Tests

A provocative claim: in the AI era, executable tests may do more harm than good. For an LLM, test code is "just more code" — it creates [[semantic-interference|semantic noise]] that blurs the core logic. Because an LLM can "simulate" execution mentally, a natural-language test specification inside the contract is more effective:

> "Given an empty array, the function must return 0."
> "If the user is unauthenticated, throw AuthError."

These textual invariants sharply **narrow the solution space** to only valid outputs, without the cognitive overhead of parsing test framework boilerplate. ^[raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/index.md]

## The New Role: Semantic Architecture Engineer

The article argues that prompt engineering alone is insufficient for building reliable AI-assisted systems. A new discipline is emerging — **semantic annotation architecture** — encompassing:

1. Designing fractal semantic templates for a specific language and project
2. Writing contracts understood by both humans and machines
3. Building logging systems integrated with code for navigation and debugging
4. Training AI agents (like Cursor) to work with the markup rules

## Related Concepts

- [[semantic-anchors|Semantic Anchors]] — lower-level, function-specific markers that work *within* the contract framework; anchors target specific edit sites, contracts define the semantic boundaries
- [[semantic-fractal|Semantic Fractal]] — the internal representation that makes contract-based navigation natural for LLMs
- [[semantic-interference|Semantic Interference]] — contracts are the antidote: they reduce ambiguity and prevent the "skyscraper collapse"
- [[vibe-coding|Vibe Coding]] — contract programming is a concrete methodology for implementing the vibe coding paradigm
- [[retrieval-augmented-generation|RAG]] — the agent navigation described above depends on RAG for its fragment-based reading
