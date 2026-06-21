---
title: "Knowledge Neurons in Pretrained Transformers"
authors:
  - Damai Dai
  - Li Dong
  - Yaru Hao
  - Zhifang Sui
  - Baobao Chang
  - Furu Wei
date: 2021-04-17
venue: ACL 2022
source_url: https://arxiv.org/abs/2104.08696
ingested: 2026-06-21
description: "Introduces knowledge neurons — specific FFN intermediate neurons responsible for expressing factual knowledge in pretrained Transformers. Proposes knowledge attribution via integrated gradients to identify which neurons encode which relational facts. Demonstrates that suppressing/amplifying knowledge neurons predictably affects fact expression, with case studies on fact updating and relation erasing."
---

# Knowledge Neurons in Pretrained Transformers

**PDF:** [2104.08696.pdf](2104.08696.pdf)

**Authors:** Damai Dai (Peking University / Microsoft Research), Li Dong (Microsoft Research), Yaru Hao (Microsoft Research), Zhifang Sui (Peking University), Baobao Chang (Peking University), Furu Wei (Microsoft Research)

Venue: ACL 2022

*Damai Dai contributed during internship at Microsoft Research.*

## Abstract

Large-scale pretrained language models are surprisingly good at recalling factual knowledge presented in the training corpus. In this paper, we present preliminary studies on how factual knowledge is stored in pretrained Transformers by introducing the concept of knowledge neurons. Specifically, we examine the fill-in-the-blank cloze task for BERT. Given a relational fact, we propose a knowledge attribution method to identify the neurons that express the fact. We find that the activation of such knowledge neurons is positively correlated to the expression of their corresponding facts. In our case studies, we attempt to leverage knowledge neurons to edit (such as update, and erase) specific factual knowledge without fine-tuning. Our results shed light on understanding the storage of knowledge within pretrained Transformers.
