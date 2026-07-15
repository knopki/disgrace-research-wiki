---
source_url: https://arxiv.org/abs/2210.02406
ingested: 2026-07-15
title: "Decomposed Prompting: A Modular Approach for Solving Complex Tasks"
authors:
  - Tushar Khot
  - Harsh Trivedi
  - Matthew Finlayson
  - Yao Fu
  - Kyle Richardson
  - Peter Clark
  - Ashish Sabharwal
date: 2022-10-05
venue: ICLR 2023
---
# Decomposed Prompting: A Modular Approach for Solving Complex Tasks

**PDF:** [2210.02406.pdf](2210.02406.pdf)

## Abstract

Few-shot prompting is a surprisingly powerful way to use Large Language Models (LLMs) to solve various tasks. However, this approach struggles as the task complexity increases or when the individual reasoning steps of the task themselves are hard to learn, especially when embedded in more complex tasks. To address this, we propose Decomposed Prompting, a new approach to solve complex tasks by decomposing them (via prompting) into simpler sub-tasks that can be delegated to a shared library of prompting-based LLMs dedicated to these sub-tasks. This modular structure allows each prompt to be optimized for its specific sub-task, further decomposed if necessary, and even easily replaced with more effective prompts, trained models, or symbolic functions if desired. We show that the flexibility and modularity of Decomposed Prompting allows it to outperform prior work on few-shot prompting using GPT-3. On symbolic reasoning tasks, we can further decompose sub-tasks that are hard for LLMs into even simpler solvable sub-tasks. When the complexity comes from the input length, we can recursively decompose the task into the same task but with smaller inputs. We also evaluate our approach on textual multi-step reasoning tasks: on long-context multi-hop QA, we can more effectively teach the sub-tasks via our separate sub-tasks prompts; and on open-domain multi-hop QA, we can easily incorporate a symbolic information retrieval module within our decomposition framework, leading to improved performance on both tasks.
