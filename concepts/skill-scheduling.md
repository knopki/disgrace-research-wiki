---
title: Skill Scheduling
created: 2026-06-16
updated: 2026-06-16
type: concept
tags:
  - agent
  - planning
  - optimization
sources:
  - "[AI в управлении проектами — теперь Resource Leveling уже работает](raw/articles/2025-07-01-ivanov-ai-v-upravlenii-proektami-teper-resource-leveling-uzhe-rab/ivanov2025aiinpm.md)"
---

# Skill Scheduling

Flexible qualification management powered by AI: instead of assigning fixed roles, the system analyzes project context and recommends which specialist profiles to add or replace to accelerate work.

## Core Idea

Traditional resource scheduling assigns people to tasks based on role. Skill scheduling goes a step further — the AI understands the full context of a project from its documentation and proposes concrete staffing changes:

- What type of specialist would accelerate the current bottleneck
- Who on the existing team could be swapped for someone with better-suited qualifications
- How the team composition should evolve as the project progresses through different phases

## Prerequisites

Skill scheduling depends on the AI first being able to [[ai-resource-leveling|AI Resource Leveling]] — without that foundation, staffing recommendations are disconnected from actual work requirements.

## Relationship to Other Concepts

- Enables the [[vibe-coding|Vibe Coding]] pattern in project management: the human directs team composition strategy, the AI handles the detailed qualification analysis
- Authored by [[vladimir-ivanov|Vladimir Ivanov]]
