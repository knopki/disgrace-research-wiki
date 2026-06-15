---
title: Contract Programming
created: 2026-06-15
updated: 2026-06-16
type: concept
tags:
  - technique
  - methodology
  - agent
  - tool-use
sources:
  - "[Контрактное программирование: Ваш семантический щит в эпоху искусственного интеллекта](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md)"
  - "[Design by Contract (Wikipedia)](raw/articles/design-by-contract-wikipedia.md)"
  - "[Transformers Represent Belief State Geometry in their Residual Stream](raw/papers/2024-05-shai-belief-state-geometry/shai2025belief.md)"
confidence: medium
---

# Contract Programming

**Contract Programming** is the adaptation of Bertrand Meyer's Design by Contract (DbC) methodology for the era of AI-assisted software development.

## Historical Background: Meyer's Original DbC

The original Design by Contract was introduced by **Bertrand Meyer** between 1986 and 1988 in connection with the **Eiffel** programming language. Meyer formalised the concept in his book *Object-Oriented Software Construction* (1988, 2nd ed. 1997), and "Design by Contract" was later registered as a trademark by Eiffel Software in 2004. The roots of DbC lie in Hoare logic (C. A. R. Hoare, 1969) — the formal verification framework that treats programs as triples of preconditions, computation, and postconditions. ([Wikipedia](raw/articles/design-by-contract-wikipedia.md))

### The Core Metaphor

Meyer's model uses a business contract between a **client** and a **supplier** (or **server**), defining mutual obligations and benefits:

- The supplier may **require** certain conditions to be met (precondition) — the client's obligation.
- The supplier **guarantees** certain results (postcondition) — the client's benefit.
- The supplier must **maintain** a property throughout (invariant) — checked before and after every public method.

This is semantically equivalent to a Hoare triple `{P} C {Q}`.

### The Three Questions

Every designer must answer three questions for each routine:

1. **What does the contract expect?** (precondition)
2. **What does the contract guarantee?** (postcondition)
3. **What does the contract maintain?** (invariant)

### Inheritance Rules (Behavioural Subtyping)

Following the Liskov substitution principle:
- Subclasses may **weaken** preconditions (accept wider input), not strengthen them.
- Subclasses may **strengthen** postconditions and invariants (guarantee more), not weaken them. ([Wikipedia](raw/articles/design-by-contract-wikipedia.md))

These rules ensure that a subclass object can always substitute its parent without violating client expectations — a concern that becomes critical when [[vibe-coding|vibe-coding]] agents inherit and extend code without understanding the original contract. Where traditional DbC used formal preconditions, postconditions, and invariants to guarantee correctness, AI-era contracts embed rich natural-language semantic specifications directly in code comments — serving as a "semantic shield" that prevents LLM agents from making destructive modifications.

## Motivation: The Problem of Semantic Incompleteness

When an LLM agent modifies code it does not fully understand, it has no way to distinguish essential invariants from implementation details. Without explicit semantic guardrails, the agent treats all code as equally modifiable — leading to what the article calls the "skyscraper collapse": the AI removes a load-bearing wall while "improving" the facade, and the entire structure collapses. ([Ivanov, 2025](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md))

Traditional solutions — unit tests, type annotations, formal verification — layer *more code* into the model's context, creating [[semantic-interference|semantic noise]] that obscures the core logic. Contracts solve this by being semantically explicit rather than syntactically executable.

## Core Elements

### Preconditions, Postconditions, Invariants

Following Meyer's original DbC, AI-era contracts specify:

- **Preconditions** — what must be true *before* a function executes (e.g., "input argument must not be empty")
- **Postconditions** — what the function guarantees *after* execution (e.g., "return value will be a positive integer")
- **Invariants** — conditions that remain true throughout the object's lifecycle

The critical shift: these are written in **natural language**, not formal logic. An LLM understands "the user must be authenticated before calling this endpoint" as directly as it understands `assert user.is_authenticated`. The semantic form activates the model's internal reasoning more effectively than executable assertions. ([Ivanov, 2025](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md))

### Semantic Coherence: The Spec-Contract-Code Trinity

The article introduces **semantic coherence** as the key operational principle: technical specification (ТЗ), contracts in code, and the implementation itself must speak the same language and not contradict each other. This is achieved through inline semantic markup:

```python
# SPECIFICATION: REQ-42 — data must be deduplicated before aggregation
# PRECONDITION: input is a non-empty list of records
# POSTCONDITION: result has no duplicate rows
def load_and_parse(data_source):
    ...
```

A function's contract links it to specific spec items. Log statements like `logger.debug("generating test stubs")` become **belief state declarations** — the model uses them to track *where in its semantic plan* it currently is. ([Ivanov, 2025](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md))

## Scientific Basis: Belief State Geometry

The article grounds contract programming's effectiveness in a specific transformer property discovered by Adam Shai and colleagues: [[belief-state-geometry|belief state geometry]] (Shai et al., 2024). As an LLM generates output, it constructs a complex belief state geometry in its [[residual-connection|residual stream]] — an internal fractal plan where each node is the model's "belief" about which semantic state it occupies, and edges are transitions between states. ([Shai et al., 2024](raw/papers/2024-05-shai-belief-state-geometry/shai2025belief.md))

Contracts act as **belief state refiners**. When the model encounters a contract, it does not simply read instructions — the contract *forces* the model to narrow its belief state to exactly what the contract specifies: "Right now your belief state should be: you are writing a payment validation function. Your goal is to return True or False. Your input is a card number and an amount. Nothing else exists." ([Ivanov, 2025](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md))

This connects contract programming directly to the [[semantic-fractal|Semantic Fractal]] model — contracts are a navigation mechanism for the model's internal semantic graph.

## Contract Structure: Fractal Self-Similarity

Contracts are themselves fractal (self-similar across scales):

- **Module-level contract** — describes the file's overall purpose, dependencies, key functions, usage scenarios
- **Function-level contract** — details the specific task, inputs, outputs, side effects, test conditions

This self-similar structure lets the model "compress" the semantics of a large codebase. Instead of holding 100,000 lines in context, it operates at the concept level: "This is the payments module, I understand its contract. This function inside it is a special case of the module contract." ([Ivanov, 2025](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md))

## Contract-Driven Agent Navigation

For RAG-based AI agents (like Cursor) that read code in small fragments (100-200 lines per window), contracts solve the "seeing the trees but not the forest" problem:

1. **Read module contract** — agent gets strategic context: file role, connections, key entities
2. **Jump to function contract** — agent reads the local contract for tactical understanding
3. **Edit with context** — armed with both levels, the agent makes correct changes within a small visible window

The article claims >90% success on first attempt with this two-level contract structure, eliminating the need for the agent to request additional context. ([Ivanov, 2025](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md))

## Semantic Specifications vs. Code Tests

A provocative claim: in the AI era, executable tests may do more harm than good. For an LLM, test code is "just more code" — it creates [[semantic-interference|semantic noise]] that blurs the core logic. Because an LLM can "simulate" execution mentally, a natural-language test specification inside the contract is more effective:

> "Given an empty array, the function must return 0."
> "If the user is unauthenticated, throw AuthError."

These textual invariants sharply **narrow the solution space** to only valid outputs, without the cognitive overhead of parsing test framework boilerplate. ([Ivanov, 2025](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md))

## The New Role: Semantic Architecture Engineer

The article argues that prompt engineering alone is insufficient for building reliable AI-assisted systems. A new discipline is emerging — **semantic annotation architecture** — encompassing:

1. Designing fractal semantic templates for a specific language and project
2. Writing contracts understood by both humans and machines
3. Building logging systems integrated with code for navigation and debugging
4. Training AI agents (like Cursor) to work with the markup rules

## Offensive vs. Defensive Programming

Meyer distinguished two philosophical approaches to contracts that carry forward into the AI era:

**DbC (offensive programming):** The supplier assumes the client meets preconditions. If not, the supplier "fails hard" (assertion failure). This catches contract violations at their source — a LLM agent that calls a function without satisfying its precondition gets an immediate assertion error, making the failure obvious and localised. ([Wikipedia](raw/articles/design-by-contract-wikipedia.md))

**Defensive programming:** The supplier tests preconditions and handles failures gracefully (exceptions, error codes). Used in distributed systems where client behaviour cannot be guaranteed.

The AI-era shift: contracts in natural language make the *offensive* approach viable even with imprecise LLM agents. The contract explicitly states the precondition, and the LLM can reason about it before making the call — so "fail hard" becomes a clean signal rather than a crash. ([Ivanov, 2025](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md))

## Performance and Testing Implications

Traditional DbC disables contract checks in production (via `assert` removal or compiler flags) to avoid runtime overhead. AI-era contracts invert this: they are **never executed** — they live as comments and documentation — so there is zero runtime cost by design. This makes them strictly additive: they improve LLM reasoning without any performance tradeoff. ([Wikipedia](raw/articles/design-by-contract-wikipedia.md))

DbC does not replace testing — contracts act as **test oracles**, specifying expected behaviour so both human-written and AI-generated tests can automatically verify correctness. However, the AI-era critique challenges this: for LLM agents, executable tests create [[semantic-interference|semantic noise]] that competes with core logic for context window space, while natural-language contract specifications serve as more direct reasoning anchors. ([Ivanov, 2025](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md))

## Related Concepts

- [[semantic-anchors|Semantic Anchors]] — lower-level, function-specific markers that work *within* the contract framework; anchors target specific edit sites, contracts define the semantic boundaries
- [[semantic-fractal|Semantic Fractal]] — the internal representation that makes contract-based navigation natural for LLMs
- [[semantic-interference|Semantic Interference]] — contracts are the antidote: they reduce ambiguity and prevent the "skyscraper collapse"
- [[vibe-coding|Vibe Coding]] — contract programming is a concrete methodology for implementing the vibe coding paradigm
- [[retrieval-augmented-generation|RAG]] — the agent navigation described above depends on RAG for its fragment-based reading
- [[grace|GRACE]] — the GRACE framework's MODULE_CONTRACT/MODULE_MAP elements are the concrete implementation of contract programming within a top-down scaffold for deterministic code synthesis
- [[semantic-superposition|Semantic Superposition]] — contracts function as a practical mechanism for controlling *when* and *how* semantic collapse happens; a well-structured contract scopes the model's belief state without forcing premature commitment to implementation