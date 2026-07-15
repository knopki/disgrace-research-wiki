---
title: Generative Agents
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - agent
  - framework
  - planning
  - memory
  - orchestration
sources:
  - "[Generative Agents: Interactive Simulacra of Human Behavior](raw/papers/2023-04-park-generative-agents/park2023generative.md)"
confidence: high
---

# Generative Agents

Generative agents are computational software agents that simulate **believable human behavior** by fusing a large language model with an architecture for storing, synthesizing, and retrieving memories in natural language (Park et al., Stanford / Google Research / Google DeepMind, UIST 2023; arXiv:2304.03442). The canonical instantiation populates a Sims-style sandbox town ("Smallville") with 25 agents that wake up, work, form opinions, talk, and coordinate group activities driven by a single user-set seed intention.

The paper's central claim: an LLM alone produces plausible single-moment behavior, but cannot maintain long-term coherence, manage a growing memory of experiences, or reflect on the past. The generative-agent architecture supplies exactly those three mechanisms — **memory stream, reflection, planning** — and the authors show via ablation that each is critically load-bearing for believability.

## Architecture

All experience is recorded and reasoned over as natural-language descriptions, which lets the architecture piggyback on the LLM's prompting capabilities. In the original implementation the backbone was `gpt-3.5-turbo` (GPT-4 was invitation-only at writing); the authors expect the three structural components to persist as models improve.

### 1. Memory stream

A long-term memory module: a list of **memory objects**, each a natural-language description plus a creation timestamp and a last-accessed timestamp. The atomic element is an **observation** — an event the agent directly perceived (its own action, another agent's action, or a non-agent object's state change).

Retrieval surfaces a compact subset to condition the LLM's next behavior. The retrieval score is a weighted combination of three signals, each min-max normalized to [0,1]:

- **Recency** — exponential decay over sandbox-game-hours since last retrieval; decay factor 0.995. Recent events stay in the agent's attentional sphere.
- **Importance** — mundane vs core distinction; the LLM rates the memory's "poignancy" 1–10 (e.g., brushing teeth = 2, asking a crush on a date = 8). Generated at memory-creation time.
- **Relevance** — cosine similarity between the query's embedding and the memory's embedding; relevance is "relevant to what?", so it is conditioned on the current situation.

Final score: `score = α_recency·recency + α_importance·importance + α_relevance·relevance`, with all α = 1 in the implementation. Top-ranked memories that fit the context window are injected into the prompt. Naively summarizing the whole stream instead yields uninformative, generic responses.

### 2. Reflection

Higher-level, more abstract memories **generated** by the agent, stored alongside observations and included in retrieval. Reflections let the agent generalize and draw inferences it could not from raw observations alone (e.g., Klaus choosing Maria over his most-frequent-interaction neighbor Wolfgang, because reflection reveals both are research-passionate).

Generation is periodic: the agent identifies salient questions from its 100 most recent records, retrieves relevant memories (including prior reflections), and prompts the LLM to extract insights with citations. Triggered when the sum of importance scores of recently perceived events exceeds a threshold (150 in the implementation); agents reflected roughly 2–3× per day. Reflections form **trees** — leaf nodes are observations, higher nodes are increasingly abstract thoughts — because reflections can cite other reflections.

### 3. Planning and reacting

Plans are future action sequences with a location, start time, and duration, stored in the memory stream and fed into retrieval. Without planning, the LLM optimizes believability-in-the-moment at the cost of believability-over-time (e.g., Klaus eats lunch at 12, 12:30, and 1pm despite having eaten twice).

Plan construction is top-down recursive decomposition: a broad daily agenda in 5–8 chunks → hourly chunks → 5–15 minute chunks, adjustable to desired granularity. Agents **react** in an action loop: each timestep they perceive the world, store the observation, decide whether to continue the plan or react (conditioned on a dynamically generated summary of the agent's goals/disposition and retrieved context), and — for inter-agent interaction — generate dialogue conditioned on memories of the other agent. Plans can change midstream; a reaction regenerates the plan from the reaction point.

## Sandbox grounding

The authors represent the Smallville environment (areas, subareas, objects) as a tree (containment edges), rendered to natural language to condition the LLM, and flatten a subgraph to choose an action's location. Agents build individual environment-subgraph memories as they navigate; they are not omniscient — their subgraph goes stale when they leave an area and is refreshed on re-entry. Actions mutate a JSON world-state (e.g., coffee machine "off" → "brewing coffee"); the sandbox server parses this, moves agents, and pushes perceived objects within visual range back into each agent's memory.

## Evaluation

Two stages, both measuring **believability** (a central dependent variable in prior believable-agent work).

**Controlled evaluation** — agents "interviewed" in natural language across five question categories (self-knowledge, memory, plans, reactions, reflections). 100 Prolific evaluators (US, 18+, ~30 min) ranked five conditions per question: full architecture, three ablations (no observation/reflection/planning; no reflection/planning; no reflection), and a human-crowdworker-authored baseline. Ratings via TrueSkill; significance via Kruskal-Wallis + Dunn post-hoc (Holm-Bonferroni).

Results (TrueSkill μ; σ ≈ 0.7):
- Full architecture — **29.89** (best)
- No reflection — 26.88
- No reflection/planning — 25.64
- Human crowdworker — 22.95
- No memory/planning/reflection (prior SOTA, e.g. Social Simulacra (Park et al., UIST 2022)) — 21.21 (worst)

Full vs prior-SOTA effect size **d = 8.16** (≈ eight standard deviations). All pairwise differences significant (p < 0.001) except crowdworker vs fully-ablated baseline (the two worst). Key failures observed: agents **fail to retrieve** correct instances, and **hallucinate embellishments** (e.g., Isabella claiming Sam "will make an announcement tomorrow" though that was never discussed; Yuriko calling a neighbor "the author of Wealth of Nations" via LM world-knowledge bleed).

**End-to-end evaluation** — 25 agents interact freely over two game days. Measured emergent outcomes:
- **Information diffusion** — Sam's mayoral candidacy spread 1→8 agents (4%→32%); Isabella's Valentine's party 1→13 agents (4%→52%), no user intervention, zero hallucinations of the information.
- **Relationship formation** — network density rose 0.167 → 0.74.
- **Coordination** — from a single seed ("throw a Valentine's party"), agents spread invites, decorated, and 5 of 12 invited showed up together at the right time.

## Limitations and ethics (the authors' own caveats)

- **Retrieval scaling** — larger memory hampers both retrieving the right pieces and choosing an appropriate action location (some agents drift to atypical places).
- **Norm misclassification** — physical/social norms phrased poorly in NL don't percolate (agents enter a one-person dorm bathroom assuming multi-occupancy; enter stores after 5pm close).
- **Instruction-tuning leakage** — dialogue feels overly formal; agents are *overly cooperative*, rarely refusing suggestions misaligned with their character (Isabella ends up "very interested in literature" after others push it).
- **Cost** — 25 agents for 2 days cost thousands of dollars in token credits and multiple days to run; real-time interactivity needs parallelism or agent-specific models.
- **Evaluation scope** — short timescale; crowdworker baseline ≠ maximal human performance; robustness (prompt hacking, **memory hacking** — a crafted conversation convincing an agent of a never-occurred past event, hallucination) largely untested.
- **Ethics** — parasocial relationship risk; errors in ubiquitous-computing inferences; exacerbated deepfake/misinformation/tailored-persuasion risk (mitigate via audit logs); over-reliance displacing real human stakeholders in design. Agents should complement, not replace, humans. LM biases/stereotypes are inherited wholesale.

## Relationship to other techniques

- [[coala|CoALA]] — surveys Generative Agents as the most-capable surveyed agent (episodic+semantic memory, digital/agent grounding, reason/retrieve/learn actions, propose-only decision); gains verified by procedural-memory ablation ([Sumers et al., 2023](raw/papers/2023-09-sumers-coala/sumers2023coala.md)).
- [[memgpt|MemGPT (MemoryGPT)]] — generalizes the in-window memory-stream idea to an explicit tiered hierarchy (working/recall/archival) with eviction and self-editing beyond the window; the two are frequently built on together (the MemGPT project later became *Letta*).
- [[react|ReAct]] — interleaves reasoning + acting; Generative Agents adds the persistent memory/reflection/planning loop on top of the same LLM-backbone idea.
- [[reflexion|Reflexion]] — verbal self-reflection writing to memory; Generative Agents' reflection module is the same family of mechanism, generalized to a tree of self-inferences.
- [[tot|Tree of Thoughts]] — search over reasoning; Generative Agents' reflection tree is a related recursive-synthesis structure, but for self-knowledge rather than problem-solving search.
- [[retrieval-augmented-generation|Retrieval-Augmented Generation]] — the memory-stream retrieval (relevance/recency/importance) is a writable, self-generated RAG over the agent's own experience rather than a fixed external corpus.
- [[chain-of-thought|Chain-of-Thought]] — the planning/decomposition prompts are CoT-style reasoning, recursively applied to action sequencing.
- Social Simulacra (Park et al., UIST 2022) — Park et al.'s own prior (UIST 2022) that used prompt chains to generate stateless personas; Generative Agents extends it with dynamic, evolving memory.

## Open questions

- Scalable, fine-tunable retrieval (the three-score composition is hand-weighted).
- Cost-effective real-time simulation (parallelization, specialized small models).
- Robustness to memory/prompt hacking and hallucination at scale.
- Long-horizon believability and rigorous benchmarks beyond 2-day sandbox runs.
