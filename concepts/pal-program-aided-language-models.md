---
title: PAL (Program-aided Language Models)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - prompting
  - tool-use
sources:
  - "[PAL: Program-aided Language Models](raw/papers/2022-11-gao-pal/gao2022pal.md)"
---

# PAL (Program-aided Language Models)

PAL is a few-shot prompting method by Gao et al. (CMU, ICML 2023) that uses an LLM to read a natural-language problem and generate **programs as intermediate reasoning steps**, but **offloads the solution step to an external runtime** — a Python interpreter ([Gao et al., 2023](raw/papers/2022-11-gao-pal/gao2022pal.md)).

The core idea: in [[chain-of-thought|chain-of-thought (CoT)]] prompting the LLM does both the decomposition *and* the solving, and it frequently makes arithmetic/logic errors in the solving part even when the decomposition is correct. PAL keeps decomposition as the LLM's only learned task and delegates execution to an exact symbolic solver. This makes the final answer correct *by construction*, given a correct program.

## Method

- Each in-context example is a pair `(xᵢ, tᵢ)` where `tᵢ` is a sequence of interleaved **natural-language** steps (as Python comments) and **programming-language** statements. The final answer is *not* provided in the prompt.
- At inference, the LM generates `t_test` (NL steps + code). The program is passed to a Python interpreter; the run result is the answer. The paper uses a standard Python interpreter, but notes any solver/compiler works.
- Prompts reuse existing CoT exemplars where available, augmented into PAL style; 3–6 examples per benchmark. Variable names are chosen to meaningfully reflect entities in the question (`num_apples_in_basket`), which the ablation shows matters.
- NL intermediate steps are emitted as comments (`# ...`) so the interpreter ignores them while keeping the model grounded.

PAL is a form of neuro-symbolic reasoning and a special case of [[toolformer|tool use]] — the model calls an external calculator/interpreter instead of computing internally. Unlike prior calculator-augmented approaches (Cobbe et al.'s verifier calculator, Demeter & Downey's specialized modules), PAL generates general Python code with no task-specific modules or constrained decoders.

## Results

Backbone for PAL, CoT, and Direct was **Codex (code-davinci-002)** unless noted. Greedy decoding, temperature 0.

**Mathematical reasoning (Table 1, solve rate %):**

| Dataset | Direct Codex | CoT Codex | CoT PaLM-540B | PAL |
|---|---|---|---|---|
| GSM8K | 19.7 | 65.6 | 56.9 | **72.0** |
| GSM-HARD | 5.0 | 23.1 | — | **61.2** |
| SVAMP | 69.9 | 74.8 | 79.0 | **79.4** |
| ASDiv | 74.0 | 76.9 | 73.9 | **79.6** |
| SingleEq | 86.8 | 89.1 | 92.3 | **96.1** |
| SingleOp | 93.1 | 91.9 | 94.1 | **94.6** |
| AddSub | 90.9 | 86.0 | 91.9 | **92.5** |
| MultiArith | 44.0 | 95.9 | 94.7 | **99.2** |

**Symbolic & algorithmic (Table 2, solve rate %):**

| Dataset | Direct Codex | CoT Codex | PAL |
|---|---|---|---|
| Colored Objects | 75.7 | 86.3 | **95.1** |
| Penguins | 71.1 | 79.2 | **93.3** |
| Date | 49.9 | 64.8 | **76.2** |
| Repeat Copy | 81.3 | 68.8 | **90.6** |
| Object Counting | 37.6 | 73.0 | **96.7** |

Key takeaways:

- **GSM8K:** PAL reaches 72.0%, surpassing PaLM-540B CoT (56.9%) by **+15.1 absolute** despite PaLM being ~25× larger.
- **GSM-HARD** (numbers swapped for up-to-7-digit integers): Direct drops 74% (19.7→5.0), CoT drops ~70% (65.6→20.1), but **PAL stays at 61.2%** (only −14.3%). The authors analyze 25 CoT cases and find 16 generate nearly identical NL "thoughts" on both versions — i.e. the failure is arithmetic, not comprehension.
- **Multi-sample:** with nucleus sampling (p=0.95, k=40) + majority vote (majority@40), PAL climbs GSM8K to **80.4%**, +1.9% over Minerva-540B (fine-tuned on math) using the same sample count.
- **Generality:** gains hold across math, symbolic, and algorithmic tasks — PAL also improves [[least-to-most-prompting|Least-to-Most]] prompts.

## Analysis / Ablations

- **Weaker code models:** relative PAL-over-CoT improvement is consistent even on code-cushman-001 / code-davinci-001 (lower absolute, same trend).
- **NL vs code LMs:** with text-davinci-001 (weak code ability) CoT beats PAL; once code ability is sufficient (text-davinci-002/003) PAL wins again — PAL is not limited to code LMs, only needs a model with decent code modeling.
- **Interpreter is the point:** forcing the LM to also "execute" the code (no external interpreter, à la scratchpad) gave only 23.2% on GSM8K — 4.5 pts above Direct, far below PAL (72.0). Benefit comes from the synergy with the interpreter, not the code-shaped prompt.
- **Prompt format ablation (Fig 9):** full PAL > PAL−comment (NL comments removed, meaningful var names kept) > PAL−var−comment (random var names) < CoT. Meaningful variable names matter; they ease the model's grounding.

## Relationship to CoT and limitations

PAL is a direct descendent of [[chain-of-thought|CoT]] — it replaces free-text reasoning chains with interleaved NL comments + executable code. It fixes CoT's main failure mode (arithmetic/logic errors in the solution step) by construction, at the cost of requiring a code-capable model and a runtime. It is *not* a faithful-reasoning cure: like CoT, the generated steps can be post-hoc, but the answer is at least arithmetically guaranteed. Closely related contemporaneous work: Chen et al. "Program of Thoughts" (PoT) — conceptually similar but PoT only demonstrated math gains and used benchmark-specific prompts, whereas PAL shows gains on symbolic/algorithmic benchmarks too and reuses prior-work exemplars to isolate the method's benefit ([Gao et al., 2023](raw/papers/2022-11-gao-pal/gao2022pal.md)).

The [[codex|Codex]] family (code-davinci-002) was the default backend in the paper; PAL's effectiveness is tied to the base model's code-modeling ability.

## Related

- [[chain-of-thought|Chain-of-Thought (CoT)]] — the prompting method PAL extends; PAL offloads CoT's solving step to a Python interpreter
- [[self-consistency|Self-Consistency]] — PAL composes with it (majority@40 → 80.4% on GSM8K)
- [[least-to-most-prompting|Least-to-Most Prompting]] — PAL also improves it
- [[toolformer|Toolformer]] — both delegate computation to an external tool; PAL targets a Python interpreter
- [[codex|Codex]] — the code-LM backbone used throughout the PAL paper
- [[react|ReAct]] — interleaves reasoning + acting; PAL interleaves reasoning + code execution
