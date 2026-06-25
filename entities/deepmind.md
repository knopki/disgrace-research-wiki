---
title: DeepMind
created: 2026-06-25
updated: 2026-06-25
type: entity
tags: [organization, methodology]
sources:
  - "[Red Teaming Language Models with Language Models](raw/papers/2022-02-perez-red-teaming/perez2022redteaming.md)"
  - "[Training Compute-Optimal Large Language Models](raw/papers/2022-03-hoffmann-chinchilla/hoffmann2022chinchilla.md)"
---

# DeepMind

DeepMind (formerly Google DeepMind) is a British artificial intelligence research laboratory founded in 2010 and acquired by Google in 2014. Known for landmark achievements including AlphaGo (2016), AlphaFold (2020), and foundational contributions to language model scaling laws and safety evaluation.

## Key Papers in This Wiki

- **Chinchilla scaling laws** ([Hoffmann et al., 2022](raw/papers/2022-03-hoffmann-chinchilla/hoffmann2022chinchilla.md)) — established that most LLMs are undertrained and that model size and training data should scale in equal proportion; led to a paradigm shift in training compute allocation
- **Automated red teaming** ([Perez et al., 2022](raw/papers/2022-02-perez-red-teaming/perez2022redteaming.md)) — introduced LM-based automated safety evaluation, replacing human annotation with adversarial LM-generated test cases; discovered diverse failure modes in the 280B Gopher chatbot

## Relationship to Other Entities

DeepMind's safety work connects to [[anthropic|Anthropic]] (both focus on AI safety, though via different approaches — DeepMind's red teaming vs Anthropic's [[constitutional-ai|Constitutional AI]]) and [[openai|OpenAI]] (competitors in scaling laws, with Kaplan et al. at OpenAI preceding Chinchilla).
