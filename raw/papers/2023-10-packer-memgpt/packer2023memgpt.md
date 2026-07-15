---
title: MemGPT
authors:
  - Charles Packer
  - Sarah Wooders
  - Kevin Lin
  - Vivian Fang
  - Shishir G. Patil
  - Ion Stoica
  - Joseph E. Gonzalez
date: 2024-02-12
source_url: https://arxiv.org/abs/2310.08560
arxiv: 2310.08560
ingested: 2026-07-15
type: paper
venue: arXiv preprint (v2), 2024-02-12
---

# MemGPT: Towards LLMs as Operating Systems

**PDF:** [2310.08560.pdf](2310.08560.pdf)

## Abstract

Large language models (LLMs) have revolutionized AI, but are constrained by limited context windows, hindering their utility in tasks like extended conversations and document analysis. To enable using context beyond limited context windows, we propose virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems which provide the illusion of an extended virtual memory via paging between physical memory and disk. Using this technique, we introduce MemGPT (MemoryGPT), a system that intelligently manages different storage tiers in order to effectively provide extended context within the LLM's limited context window. We evaluate our OS-inspired design in two domains where the limited context windows of modern LLMs severely handicaps their performance: document analysis, where MemGPT is able to analyze large documents that far exceed the underlying LLM's context window, and multi-session chat, where MemGPT can create conversational agents that remember, reflect, and evolve dynamically through long-term interactions with their users. We release MemGPT code and data for our experiments at https://research.memgpt.ai.
