---
title: ReAct (Reasoning + Acting)
created: 2026-07-15
updated: 2026-07-15
type: concept
tags:
  - technique
  - prompting
  - agent
  - tool-use
  - planning
sources:
  - "[ReAct: Synergizing Reasoning and Acting in Language Models](raw/papers/2022-10-yao-react/yao2023react.md)"
confidence: high
---

# ReAct (Reasoning + Acting)

ReAct is a prompt-based paradigm introduced by Yao et al. (Princeton University & Google Research, ICLR 2023) that synergizes **reasoning** and **acting** in large language models by generating free-form verbal reasoning traces ("thoughts") and task-specific actions in an **interleaved** manner ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)). A ReAct trajectory is a sequence of `Thought → Action → Observation` steps: thoughts plan, track subgoals, and handle exceptions (without affecting the environment), while actions interface with external sources (knowledge bases, APIs, environments) and yield observations that feed back into reasoning.

The core idea is to augment an agent's action space with a language space: Â = A ∪ L, where a thought ā ∈ L is a reasoning trace that updates the agent's context but produces no observation. This lets the model "reason to act" (plan and adjust via internal reasoning) and "act to reason" (retrieve external facts to ground reasoning) ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)).

## Motivation and Positioning

ReAct targets a gap between two prior lines of work. [[chain-of-thought|Chain-of-Thought (CoT)]] reasoning is a "static black box" — it generates thoughts from internal representations with no grounding in the external world, which lets **fact hallucination** and **error propagation** accumulate across the reasoning chain. Conversely, act-only approaches (e.g. WebGPT-style browsing, embodied-action LMs) predict actions from language priors but do not reason abstractly about high-level goals or maintain a working memory to support acting ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)).

ReAct's closest interactive-decision-making predecessor is Inner Monologue (Huang et al., 2022), whose "inner monologue" is limited to restating environment state and what remains to be done. ReAct's thoughts are flexible and sparse, supporting diverse reasoning types (goal decomposition, commonsense injection, observation extraction, exception handling) that Inner Monologue does not ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)). The same authors later generalized single-path reasoning into a search tree in [[tot|Tree of Thoughts (ToT)]] ([Yao et al., 2023](raw/papers/2023-05-yao-tree-of-thoughts/yao2023treeofthoughts.md)).

## Method and Setup

ReAct prompts a frozen LLM (PaLM-540B in the main experiments; GPT-3 results in the appendix) with few-shot in-context trajectories of human-authored `(thought, action, observation)` examples. For knowledge tasks the model alternates thoughts and actions densely; for decision-making tasks with many steps, thoughts appear **sparsely** at the most relevant positions, with the LM deciding their asynchronous occurrence ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)).

For knowledge-intensive reasoning (HotpotQA, FEVER) the external tool is a simple Wikipedia API with three actions:
- `search[entity]` — first 5 sentences of an entity page, or top-5 similar entities if absent
- `lookup[string]` — next sentence containing the string (Ctrl+F simulation)
- `finish[answer]` — terminate with the answer

The authors stress this action space is intentionally far weaker than lexical/neural retrievers, to force retrieval via explicit reasoning in language ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)).

## Results

### Knowledge-intensive reasoning (HotpotQA, FEVER)

PaLM-540B prompting results (EM / Accuracy):

| Method | HotpotQA (EM) | Fever (Acc) |
|--------|:-------------:|:-----------:|
| Standard | 28.7 | 57.1 |
| CoT (Wei et al., 2022) | 29.4 | 56.3 |
| CoT-SC (Wang et al., 2022) | 33.4 | 60.4 |
| Act | 25.7 | 58.9 |
| ReAct | 27.4 | 60.9 |
| CoT-SC → ReAct | 34.2 | 64.6 |
| ReAct → CoT-SC | **35.1** | 62.0 |

ReAct itself only mildly beats Act and roughly matches CoT alone. The key finding: **combining internal (CoT-SC) and external (ReAct) knowledge** is strictly best — ReAct→CoT-SC reaches CoT-SC-level accuracy using only 3–5 samples instead of 21. Human analysis of failure modes (Table 2) shows CoT suffers 56% hallucination-driven failures in its major failure mode, versus 0% for ReAct, while ReAct trades reduced reasoning flexibility (higher "reasoning error" rate, including repetitive-loop failures) for groundedness ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)).

### Decision making (ALFWorld, WebShop)

On ALFWorld (134 unseen text-game tasks), best-of-6 ReAct reaches **71%** success vs Act 45% and BUTLER (imitation learning on ~10⁵ trajectories) 37% — even the worst ReAct trial (48%) beats the best Act/BUTLER trial. Relative gain over Act averages 62% across six controlled trials. On WebShop (500 instructions), one-shot Act already matches imitation/IL+RL baselines (~30% SR); ReAct adds **+10%** absolute success rate (40.0% vs 30.1%) with sparse reasoning, though still far below expert humans (59.6%) ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)).

An ablation against Inner-Monologue-style dense external-feedback thoughts (ReAct-IM) shows ReAct at 71% vs 53% overall on ALFWorld — flexible reasoning (not mere reaction to feedback) is what drives the gain ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)).

### Fine-tuning

With only 3,000 bootstrapped correct trajectories, fine-tuned ReAct (PaLM-8B/62B) becomes the best of four methods and **outperforms all PaLM-540B prompting methods**, whereas fine-tuning Standard/CoT teaches memorization of (possibly hallucinated) facts. This suggests fine-tuning on reasoning+acting trajectories teaches a more generalizable retrieval skill than prompting alone ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)).

## Properties and Limitations

ReAct is the canonical minimal language agent in [[coala|CoALA]]'s taxonomy: it has working memory only (no episodic/semantic memory), an action space of internal reasoning + external grounding, and a fixed propose-only decision cycle with no evaluation/selection stage. CoALA treats it as the baseline that demonstrates the synergizing effect of combined internal and external actions.

ReAct's claimed strengths: (A) intuitive/fast prompt design (annotators just type thoughts atop actions), (B) general/flexible across distinct action spaces, (C) performant/robust from 1–6 exemplars, (D) human-aligned — interpretable, diagnosable, and controllable via "thought editing" at inference time ([Yao et al., 2023](raw/papers/2022-10-yao-react/yao2023react.md)).

Stated limitations:
- Complex tasks with large action spaces need many demonstrations, which can exceed the in-context length limit.
- Under pure prompting, ReAct lags on some reasoning tasks vs CoT-SC; the authors combine the two.
- Repetitive-loop failures (model re-emits prior thoughts/actions) are a frequent ReAct-specific error, suspected to stem from greedy decoding.
- Main experiments use PaLM-540B (not openly accessible at publication); reproducibility rests on released prompts and GPT-3 appendix results.

## Related

- [[chain-of-thought|Chain-of-Thought (CoT)]] — ReAct augments CoT with actions + observations; combining ReAct and CoT-SC is strictly best on knowledge tasks
- [[self-consistency|Self-Consistency]] — CoT-SC supplies the internal-knowledge component of the best ReAct+CoT-SC hybrid
- [[tot|Tree of Thoughts (ToT)]] — same lead author; generalizes single-path reasoning/acting into a search tree with self-evaluation
- [[coala|CoALA]] — ReAct is the canonical minimal agent in CoALA's taxonomy: internal reasoning + external grounding, propose-only decision cycle (Table 2)
- [[retrieval-augmented-generation|Retrieval-Augmented Generation (RAG)]] — ReAct's Wikipedia-API interaction is a sparse, reasoning-driven retrieval loop; complementary to dense-retriever RAG
- [[in-context-learning|In-Context Learning]] — ReAct operates as a frozen-LM few-shot prompting method over a thought-action-observation context
- [[plan-and-solve|Plan-and-Solve (PS) Prompting]] — another CoT variant adding explicit planning; ReAct bakes planning into interleaved thoughts
