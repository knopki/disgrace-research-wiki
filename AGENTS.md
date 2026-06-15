# AGENTS.md

This directory is an LLM Wiki — a compounding knowledge base of interlinked markdown files.

## Orientation (MANDATORY before any action)

Before ingest, query, lint, or any modification:
1. Read `SCHEMA.md` — domain, conventions, tag taxonomy, page thresholds
2. Read `index.md` — what pages exist, their types and summaries
3. Read the last ~30 entries of `log.md` — recent activity

Skipping orientation causes duplicates, missed cross-references, and contradicted schema.

## Language

- All prose: English
- Direct quotes: preserve source language

## Key Rules

- `raw/` is **immutable** — never modify. Corrections go in wiki pages.
- Every wiki page needs YAML frontmatter with all required fields (title, created, updated, type, tags, sources).
- Tags must exist in SCHEMA.md taxonomy before use. New tag → update SCHEMA first.
- Every new/updated page must have 2+ `[[wikilinks]]` to other pages.
- Every action logged to `log.md`. Every new page added to `index.md`.
- Contradictions: don't silently overwrite. Note both claims, mark in frontmatter, flag for review.
- Pages over 200 lines → split with cross-links.
- Provenance markers (`^[raw/...]`) on paragraphs when synthesizing 3+ sources.

## Workflow

### Ingest a source
1. Save to `raw/` with frontmatter (source_url, ingested, sha256 of body)
2. If same URL re-ingested: compare sha256 — skip if identical, flag drift if different
3. Discuss takeaways with user (skip in automated/cron contexts)
4. Check existing pages — search index.md and grep for entities/concepts
5. Create or update wiki pages following schema rules
6. Update index.md and log.md
7. Report all files created/updated

### Query
1. Read index.md to find relevant pages
2. For 100+ page wikis, also grep for key terms
3. Synthesize answer citing wiki pages
4. File substantial answers as queries/ or comparisons/ pages
5. Update log.md

### Lint
Run all checks: orphan pages, broken wikilinks, index completeness, frontmatter validation, stale content (>90 days), contested pages, source drift, page size (>200 lines), tag audit, log rotation. Report grouped by severity.
