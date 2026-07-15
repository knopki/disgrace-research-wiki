---
title: CoALA (Cognitive Architectures for Language Agents)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - agent
  - framework
  - planning
  - orchestration
  - methodology
sources:
  - "[Cognitive Architectures for Language Agents (CoALA)](raw/papers/2023-09-sumers-coala/sumers2023coala.md)"
confidence: high
---

# CoALA (Cognitive Architectures for Language Agents)

CoALA is a conceptual framework proposed by Sumers, Yao, Narasimhan & Griffiths (Princeton University; TMLR 2024) for organizing and designing LLM-based language agents. It draws an explicit analogy between large language models and production systems, and imports the modular structure of classical cognitive architectures (notably Soar) to decompose a language agent into three axes: **memory modules**, a **structured action space**, and a **decision-making procedure** ([Sumers et al., 2023](raw/papers/2023-09-sumers-coala/sumers2023coala.md)).

Unlike empirical agent papers, CoALA is a taxonomy/theory: it retroactively classifies existing agents (SayCan, [[react|ReAct]], Voyager, [[generative-agents|Generative Agents]], [[tot|Tree of Thoughts]]) and prospectively identifies under-explored directions (adaptive retrieval, meta-learning of agent code, metareasoning for planning budgets).

## Motivation and Positioning

Modern language agents augment LLMs with external resources (web, APIs) or internal control flows (prompt chaining). Individually, works use ad-hoc terminology ("tool use", "grounding", "actions") that makes comparison hard. CoALA argues these are recapitulations of two older ideas:

- **Production systems** — rule sets mapping strings to strings; LLMs are *probabilistic* production systems defining a distribution over completions P(Yᵢ | X) ([Sumers et al., 2023](raw/papers/2023-09-sumers-coala/sumers2023coala.md)).
- **Cognitive architectures** — e.g., Soar, which augments a production system with working/long-term memory and a decision procedure selecting actions. LLMs are well-posed to fix two classic limits of symbolic cognitive architectures: they operate over arbitrary text (not just logical predicates) and learn their "productions" from pre-training rather than requiring hand-specified rules.

The resulting analogy: the agent's **source code** (prompt templates, parsers, memory interfaces) is procedural memory; the **decision cycle** is the agent's "main" loop.

## Three Axes of the Framework

### 1. Memory

Language models are stateless; agents persist state in modular memory:

- **Working memory** — symbolic variables for the current decision cycle (perceptual input, active goals, reasoning output). Persists across LLM calls; the central hub connecting components.
- **Episodic memory** — past experience (event flows, trajectories) retrievable for reasoning.
- **Semantic memory** — knowledge about the world/self; can be read-only (a fixed corpus) or incrementally written via learning.
- **Procedural memory** — two forms: implicit (LLM weights) and explicit (the agent's code: action procedures + the decision procedure). Must be initialized by the designer; writing to it is the riskiest form of learning.

### 2. Action space

Divided into **internal** actions (interact with memory) and **external** actions (interact with environments via grounding):

| Type | Read/Write | Examples |
|------|-----------|----------|
| Reasoning | read+write working memory | summarize observation, distill trajectory ([Shinn et al., 2023](raw/papers/2023-03-shinn-reflexion/shinn2023reflexion.md)) |
| Retrieval | read long-term memory | dense/sparse/rule-based fetch into working memory |
| Learning | write long-term memory | store experience (episodic), infer knowledge (semantic), fine-tune or rewrite code (procedural) |
| Grounding (external) | read env, write env | physical control, dialogue, digital APIs/tools ([Yao et al., 2022](raw/papers/2022-10-yao-react/yao2023react.md)) |

Reasoning and retrieval support **planning**; learning and grounding are the actions ultimately executed.

### 3. Decision-making (decision cycle)

The top-level "main" procedure loops:

1. **Planning stage** — reasoning + retrieval propose, evaluate, and select candidate actions (can interleave/iterate, build multi-step simulations).
2. **Execution stage** — apply the selected action (external grounding or internal learning); make an observation; loop.

Simple agents ([[react|ReAct]]) use a single reasoning action then a grounding action with no evaluation/selection. More deliberate agents ([[tot|ToT]], RAP) implement propose–evaluate–select with BFS/DFS or MCTS. CoALA flags that most agents still only *propose* a single action — deliberate decision-making is the most under-explored axis.

## Surveyed Agents (Table 2)

| Agent | Long-term memory | Grounding | Internal actions | Decision |
|-------|------------------|-----------|------------------|----------|
| SayCan (Ahn et al., 2022) | procedural only | physical | — | evaluate |
| [[react|ReAct]] (Yao et al., 2022) | — | digital | reason | propose |
| Voyager (Wang et al., 2023) | procedural | digital | reason/retrieve/learn | propose |
| [[generative-agents|Generative Agents]] (Park et al., 2023) | episodic/semantic | digital/agent | reason/retrieve/learn | propose |
| [[tot|Tree of Thoughts]] (Yao et al., 2023) | — | digital | reason | propose, evaluate, select |

Voyager and [[generative-agents|Generative Agents]] are the most capable in this taxonomy because they possess all four action types plus long-term memory; their gains are empirically verified against ReAct/AutoGPT baselines via ablation of procedural memory.

## Actionable Insights

CoALA's prospective recommendations:

- **Modular agents** — build reusable `Memory`/`Action`/`Agent` abstractions (the MDP/Gym analogy for agents).
- **LLMs vs code** — use deterministic code sparingly for generic algorithms (e.g., tree search) that complement LLM limits; LLM params give zero-shot flexibility but are opaque.
- **Beyond retrieval augmentation** — agents can *write* self-generated content to memory, enabling lifelong learning; integrate retrieval + reasoning for grounded planning.
- **Learning** — extends beyond in-context learning/finetuning to storing experience/knowledge and rewriting agent code; meta-learning of retrieval is under-studied and risky.
- **Action-space safety** — learning (esp. procedural deletion/modification) risks internal harm; grounding risks external harm ("rm" in bash, harmful speech). Worst-case ablation of the action space is recommended.
- **Metareasoning** — LLM calls are slow/costly; agents should adaptively allocate planning compute rather than fixing a reasoning depth; calibration/alignment gaps (over-confidence, hallucinated self-evaluation) bottleneck complex decision-making.

## Open Questions

- LLM-only vs VLM multimodal reasoning (modular captioning vs integrated projection).
- Boundary between agent and environment (controllability/coupling criterion: Wikipedia is external; a write-only offline copy is internal memory).
- Physical vs digital (digital allows parallel/resettable trials → different decision procedures).
- Learning vs acting (treat learning as an action on par with grounding, deferrable until appropriate).
- How agent design shifts as LLMs become more capable (will coded rules/extra models become unnecessary?).

## Relationship to Other Techniques

- [[react|ReAct]] — CoALA's minimal internal+external agent; surveyed in Table 2 as reasoning+grounding with propose-only decision.
- [[reflexion|Reflexion]] — exemplifies the learning action: reflecting on failed episodes writes semantic knowledge to memory ([Shinn et al., 2023](raw/papers/2023-03-shinn-reflexion/shinn2023reflexion.md)).
- [[tot|Tree of Thoughts]] — exemplifies deliberate propose–evaluate–select decision-making via search.
- [[toolformer|Toolformer]] — external tool use is a "single-use digital environment" under CoALA's grounding axis.
- [[retrieval-augmented-generation|Retrieval-Augmented Generation]] — classic RAG is a read-only semantic-memory retrieval; CoALA generalizes to read+write memory.
- [[chain-of-thought|Chain-of-Thought]] — reasoning action without grounding/observation; a building block CoALA situates within the broader agent loop.

## Cross-Links

- [[react|ReAct]] — surveyed agent; reasoning+grounding, propose-only decision.
- [[reflexion|Reflexion]] — learning-by-reflection instance of CoALA's learning action.
- [[tot|Tree of Thoughts]] — deliberate decision-making instance (propose–evaluate–select).
- [[toolformer|Toolformer]] — tool use as single-use digital grounding environment.
- [[retrieval-augmented-generation|RAG]] — read-only semantic memory; CoALA generalizes to writable memory.
- [[chain-of-thought|Chain-of-Thought]] — reasoning building block situated in the agent loop.
