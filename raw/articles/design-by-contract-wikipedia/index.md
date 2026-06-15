---
source_url: https://en.wikipedia.org/wiki/Design_by_contract
ingested: 2026-06-15
---

# Design by Contract (Wikipedia)

**Design by Contract (DbC)**, also known as **Contract Programming**, **Programming by Contract**, or **Design-by-Contract Programming**, is a software design approach prescribing formal, precise, and verifiable interface specifications for software components, extending abstract data types with **preconditions**, **postconditions**, and **invariants**. These specifications are referred to as "contracts," based on a metaphor with business contracts.

## Core Metaphor

The central metaphor is a business contract between a **client** and a **supplier** (or **server**), defining mutual obligations and benefits:

- The supplier may **require** certain conditions to be met before providing its service -- this is the **precondition**, and is the client's obligation.
- The supplier **guarantees** certain results after providing its service -- this is the **postcondition**, and is the client's benefit.
- The supplier must **maintain** a certain property throughout the interaction -- this is the **invariant**.

The contract is semantically equivalent to a **Hoare triple**: `{P} C {Q}` where `P` is the precondition, `C` is the computation, and `Q` is the postcondition.

### The Three Questions

Bertrand Meyer identified three questions the designer must answer for every routine:

1. **What does the contract expect?** (precondition)
2. **What does the contract guarantee?** (postcondition)
3. **What does the contract maintain?** (invariant)

## Contract Components

### Preconditions
Conditions that must hold before a method or routine is called. If the precondition is not met, the behaviour of the method is undefined -- typically, it fails fast via an assertion.

### Postconditions
Conditions that must hold after the method returns. They describe the outcome guaranteed by the supplier, assuming the precondition was met.

### Invariants
Conditions that must hold throughout the object's lifetime. They are checked before and after each public method call to ensure the object remains in a consistent state.

### Inheritance Rules (Behavioural Subtyping)
Following the Liskov substitution principle:
- Subclasses may **weaken** preconditions (not strengthen them) -- a subclass can accept a wider range of inputs.
- Subclasses may **strengthen** postconditions and invariants (not weaken them) -- a subclass can guarantee stronger outcomes.

## Offensive vs. Defensive Programming

**DbC (offensive programming):** The supplier assumes the client meets preconditions. If the client fails to do so, the supplier "fails hard" (e.g., via assertion failure). This simplifies debugging by catching contract violations at their source.

**Defensive programming:** The supplier tests preconditions and handles failures gracefully (e.g., by throwing exceptions or returning error codes). Used in distributed or multi-channel systems where clients cannot be trusted.

**Correctness criteria:**
- A routine is **correct** if it guarantees the postcondition whenever the precondition holds.
- A class is **correct** if every routine obeys its contract and the invariant is maintained.

## Performance Implications

Contract checks are typically **disabled in production** to avoid runtime overhead:
- Implemented via `assert` in many languages (C/C++, C#, Java, Python).
- Python: `python -O` removes assert bytecode entirely.
- In Eiffel, contract checking can be selectively enabled (e.g., for debugging, testing, or production).
- The principle: **no runtime cost in production** -- checks are only active in debug/test builds.

## Relationship to Testing

DbC does **not replace** unit, integration, or system testing. It complements external testing with **internal self-tests** that can detect errors before they manifest as invalid results. Contracts act as **test oracles** -- they specify the expected behaviour so tests can automatically verify correctness.

## Language Support

### Native Support
- **Eiffel** -- original language by Bertrand Meyer; full built-in support with keywords `require` (precondition), `ensure` (postcondition), `invariant` (class invariant)
- **Ada 2012** -- preconditions, postconditions, type invariants as first-class language features
- **Clojure** -- `:pre` and `:post` on function definitions
- **D** -- `in`, `out`, `invariant` blocks
- **Racket** -- `contract-out`, `provide/contract`
- **Rust** -- `assert!`, `debug_assert!`, nightly experimental `#[track_caller]`
- **SPARK** (Ada subset) -- contracts designed for formal verification

### Library / Tool Support
- **C / C++** -- `assert()`, Boost.Contract library; C++20 added experimental contract attributes
- **C#** -- `System.Diagnostics.Contracts` namespace with `Contract` class (pre/post/invariant)
- **Java** -- `assert` keyword; frameworks like JML (Java Modeling Language), JContract, CoFoJa
- **JavaScript / TypeScript** -- libraries: `invariant`, `assert`, custom decorators
- **Python** -- `assert` (basic); libraries: `deal`, `icontract`, `PyContract`
- **Ruby** -- Ruby Contracts gem
- **Swift** -- `assert()`, `precondition()`, `postcondition()` (partial DbC support)
- **Common Lisp** -- method qualifiers `:before`, `:after`, `:around` used for contract enforcement

## History

- **1986--1988:** Concept coined by **Bertrand Meyer** in connection with the design of the **Eiffel** language
- **1986:** First described in articles
- **1988:** Formalized in the book *Object-Oriented Software Construction* (2nd ed. 1997)
- **2004:** "Design by Contract" registered as a trademark by Eiffel Software
- Roots in formal verification, formal specification, and **Hoare logic** (C. A. R. Hoare, 1969)

## Key Insights

- DbC advocates **"writing the assertions first"** -- specifying the contract before implementing the body, analogous to test-driven development.
- Contracts serve as **executable documentation** -- they are both human-readable specifications and machine-checkable assertions.
- Facilitates **code reuse** -- fully documented module behaviour makes it safe to use components without reading their implementation.
- Distinct from defensive programming -- DbC places responsibility on the client to ensure preconditions, and on the supplier to guarantee postconditions.
- Contracts are a form of **semantic compression** -- they capture the essential behaviour of a component without the implementation details.
