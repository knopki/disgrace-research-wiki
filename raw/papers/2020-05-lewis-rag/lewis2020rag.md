---
title: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
authors:
  - Patrick Lewis
  - Ethan Perez
  - Aleksandra Piktus
  - Fabio Petroni
  - Vladimir Karpukhin
  - Naman Goyal
  - Heinrich Küttler
  - Mike Lewis
  - Wen-tau Yih
  - Tim Rocktäschel
  - Sebastian Riedel
  - Douwe Kiela
source_url: https://arxiv.org/abs/2005.11401
date: 2020-05-22
venue: NeurIPS 2020
tags:
  - architecture
  - evaluation
  - data
  - technique
description: Introduces Retrieval-Augmented Generation (RAG) — combining pre-trained parametric (BART seq2seq) and non-parametric (DPR dense vector index of Wikipedia) memory for language generation. Two formulations — RAG-Sequence (same document for whole output) and RAG-Token (different document per token). Sets SOTA on three open-domain QA tasks; generates more factual and diverse text than parametric-only baselines.
ingested: 2026-06-17
---
# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

**PDF:** [2005.11401.pdf](2005.11401.pdf)

## Abstract

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) — models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, and another which can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state of the art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.
