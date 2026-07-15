---
title: Reflexion (Verbal Reinforcement Learning)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags: [agent, technique, prompting, fine-tuning]
sources:
  - "[Reflexion: Language Agents with Verbal Reinforcement Learning](raw/papers/2023-03-shinn-reflexion/shinn2023reflexion.md)"
---
# Reflexion (Verbal Reinforcement Learning)

Reflexion is a framework for LLM-based agents that replaces traditional weight-updating RL with **verbal reinforcement** — the agent verbally reflects on its mistakes, stores reflective text in an episodic memory buffer, and uses it as context in subsequent trials. No gradient updates or fine-tuning required ([Shinn et al., 2023](raw/papers/2023-03-shinn-reflexion/shinn2023reflexion.md)).

## Core Components

Reflexion defines three distinct models:

- **Actor (Ma)** — an LLM prompted to generate text and actions conditioned on state observations. Can be instantiated as [[react|ReAct]], [[chain-of-thought|Chain-of-Thought]], or other generation strategies.
- **Evaluator (Me)** — assesses the Actor's output and produces a reward score: binary success/fail, heuristic rules (e.g., repeated actions >3 cycles or >30 actions → inefficient planning triggers self-reflection), or an LLM-as-judge.
- **Self-Reflection (Msr)** — an LLM that takes the trajectory + reward and produces a natural-language summary of what went wrong and how to improve. This reflective text is appended to the agent's persistent memory.

## Algorithm

The process is iterative ([Shinn et al., 2023](raw/papers/2023-03-shinn-reflexion/shinn2023reflexion.md)):

1. Actor generates trajectory τ₀ by interacting with the environment.
2. Evaluator scores τ₀ producing reward r₀.
3. Self-Reflection model analyzes `{τ₀, r₀}` to produce summary sr₀, stored in memory `mem`.
4. Loop: Actor generates new trajectory using past context + memory; re-evaluate; reflect; append to memory.
5. Repeat until Evaluator deems trajectory correct or max trials reached.

Memory is bounded by a sliding window (Ω = 1-3 experiences) to respect LLM context limits. Both short-term (current trajectory) and long-term (past reflections) memory are maintained.

## Key Results

| Benchmark | Baseline | Reflexion | Gain |
|-----------|----------|-----------|------|
| AlfWorld (134 tasks) | ReAct | +22% solved (130/134) | ~22% |
| HotPotQA (CoT + GT) | CoT (GT) only 61% | +14% to ~75% | +14% |
| HotPotQA (ReAct) | ReAct only | +20% | ~20% |
| HumanEval Python (pass@1) | GPT-4 80.1% | **91.0%** | +11% |
| HumanEval Rust (pass@1) | GPT-4 60.0% | **68.0%** | +8% |
| LeetcodeHard Python (pass@1) | GPT-4 7.5% | **15.0%** | +7.5% |

Reflexion achieved new SOTA on HumanEval Python and Rust, and LeetcodeHard at time of publication ([Shinn et al., 2023](raw/papers/2023-03-shinn-reflexion/shinn2023reflexion.md)).

## Relationship to Other Techniques

- **vs [[self-consistency|Self-Consistency]]** — Self-Consistency samples multiple reasoning paths and marginalises; Reflexion iteratively improves via self-reflection over trials.
- **vs [[tot|Tree of Thoughts]]** — ToT searches a tree of thoughts with self-evaluation as heuristic; Reflexion maintains episodic memory across failed episodes.
- **vs [[react|ReAct]]** — ReAct interleaves reasoning and acting; Reflexion wraps ReAct (or other actors) with a self-reflection + memory loop.
- **vs Self-Refine** — Self-Refine iteratively improves a single generation; Reflexion persists lessons across multiple trials via memory.
- **vs [[toolformer|Toolformer]]** — Toolformer teaches tool use via perplexity-based filtering; Reflexion uses verbal feedback from tool execution outcomes.
- **vs CodeRL** — CodeRL uses actor-critic RL with gradient updates; Reflexion uses only in-context verbal reinforcement, no weight changes.

## Limitations

- Can get stuck in local minima requiring creative exploration — observed on WebShop where Reflexion failed to improve over ReAct ([Shinn et al., 2023](raw/papers/2023-03-shinn-reflexion/shinn2023reflexion.md)).
- Self-reflection quality depends on LLM self-evaluation capability; weaker models (Starchat-beta) showed no improvement.
- Memory is a bounded sliding window (Ω = 1-3), limiting long-term knowledge retention.
- For code generation: flaky/invalid unit tests can cause false positives (pass bad code) or false negatives (reject correct code).

## Introduced Resources

- **LeetcodeHardGym** — a code-generation RL gym of 40 Leetcode hard-rated questions released after GPT-4's training cutoff (Oct 2022), for evaluating genuine generalisation.

## Cross-Links

- [[react|ReAct]] — the Actor backbone most used in Reflexion experiments.
- [[chain-of-thought|Chain-of-Thought]] — alternative Actor strategy for reasoning-only tasks.
- [[humaneval|HumanEval]] — primary code generation benchmark where Reflexion set SOTA.
- [[in-context-learning|In-Context Learning]] — Reflexion operates via in-context learning, not weight updates.
- [[tot|Tree of Thoughts]] — alternative self-evaluation-guided search framework.
- [[toolformer|Toolformer]] — related approach for LLM tool use via self-supervised learning.
