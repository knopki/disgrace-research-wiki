---
title: V4A Diff Format
created: 2026-06-15
updated: 2026-06-15
type: concept
tags:
  - technique
sources:
  - "[GPT-4.1 Prompting Guide](raw/articles/2025-04-14-openai-gpt41-prompting-guide.md)"
confidence: high
---

# V4A Diff Format

> A context-based, line-number-free diff format that OpenAI trained GPT-4.1 on for reliable code patch application by LLM agents.

**V4A** (sometimes called the *apply_patch* format) is a structured plain-text diff format designed specifically for LLM-based coding agents. Unlike traditional unified diffs (which use line numbers and @@ offset/context hunks), V4A relies entirely on **semantic context** — surrounding code lines — to identify the location of a change. This makes it robust to line-number shifts caused by prior edits in the same session.

## Origins

OpenAI developed V4A as part of GPT-4.1 training data for agentic coding tasks. The model was trained on trajectories that use V4A patches via an `apply_patch` tool. The GPT-4.1 family achieves state-of-the-art 55% pass rate on SWE-bench Verified for non-reasoning models, partly attributed to improved diff generation capabilities ([OpenAI, 2026](raw/articles/2025-04-14-openai-gpt41-prompting-guide.md)).

## Format Specification

A V4A patch document is wrapped in sentinel markers:

```
*** Begin Patch
[content]
*** End Patch
```

Inside, each operation targets one file with one of three action types:

| Marker | Action |
|--------|--------|
| `*** Update File: path/to/file` | Modify an existing file |
| `*** Add File: path/to/file` | Create a new file |
| `*** Delete File: path/to/file` | Remove a file |

### Context Anchoring

Instead of line numbers, V4A uses **context lines** before and after each change (default: 3 lines). The tool searches for the context in the target file and applies the +/- diff at the matching location. If 3 lines of context are insufficient to uniquely identify the target, `@@` markers disambiguate:

```
*** Update File: pygorithm/searching/binary_search.py
@@ class BaseClass
@@     def search():
3 lines of pre-context
-        pass
+        raise NotImplementedError()
3 lines of post-context
```

Multiple `@@` markers can be stacked (e.g., `@@ class BaseClass` then `@@ def method()`) to navigate nested scopes.

### Chunk Operations

Each chunk has three line types:

| Prefix | Meaning |
|--------|---------|
| ` ` (space) | Context — must match the surrounding code |
| `-` | Line(s) to delete |
| `+` | Line(s) to insert |

### Reference Implementation

OpenAI provides a complete pure-Python reference implementation of the `apply_patch` tool (approximately 250 lines, no external dependencies, Python 3.9+) in the GPT-4.1 Prompting Guide appendix. It consists of three stages:

1. **Parser** — tokenises the patch text into `PatchAction` objects (ADD / DELETE / UPDATE with chunks)
2. **Commit builder** — converts the patch into a `Commit` with file-level changes using fuzzy context matching (rstrip, then strip, with fuzz tracking)
3. **Executor** — applies the commit to the filesystem (write, remove, or move)

OpenAI also reports that the **SEARCH/REPLACE** format (used by Aider) and a **pseudo-XML** format without internal escaping both had high success rates in testing. The shared success factors: no line numbers, exact old-code + exact new-code with clear delimiters.

## Relationship to Other Approaches

- [[contract-programming|Contract Programming]] — V4A's context-based patching aligns with GRACE's semantic coordinate solution: both avoid fragile line-number references
- [[grace|GRACE]] — The XML-like structure of V4A (`*** Begin Patch`, `*** Update File: path`, `@@ class`) mirrors GRACE's own XML-like semantic markup. Both exploit the principle that XML-based syntax gives stronger semantic convergence than JSON: paired open/close markers (implicit in V4A's `***` lines, explicit in GRACE's `<block>...</block>`) let the model correlate identical tokens across long distances, while JSON's escaping and nesting degrades reliability at scale. OpenAI's own testing confirms XML outperforms JSON for long-context document retrieval ([OpenAI, 2026](raw/articles/2025-04-14-openai-gpt41-prompting-guide.md)). GRACE uses V4A as one concrete format for deterministic patch delivery in its code generation stage.
- **Standard unified diff** — V4A trades compactness (no line counting, no @@ offset math) for LLM-generator friendliness (natural language style, context-based matching). The tool's fuzziness (rstrip → strip matching) makes it forgiving of minor whitespace differences during generation
