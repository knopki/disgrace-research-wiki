# AGENTS.md

This directory is an LLM Wiki — a compounding knowledge base of interlinked markdown files (Karpathy's pattern). This file is the **authoritative operating manual** for THIS wiki. The `llm-wiki` skill is the general pattern reference; everything project-specific lives here.

## Orientation (MANDATORY before any action)

Before ingest, query, lint, or any modification:
1. Read `SCHEMA.md` — domain, conventions, tag taxonomy, page thresholds
2. Read `index.md` — what pages exist, their types and summaries
3. Read `sources.md` — catalog of all ingested raw sources (if adding or referencing sources)
4. Read the last ~30 entries of `log.md` — recent activity

Skipping orientation causes duplicates, missed cross-references, and contradicted schema.

## Language

- All prose: English
- Direct quotes: preserve source language

## Key Rules

- `raw/` is **immutable** — never modify. Corrections go in wiki pages.
- Every wiki page needs YAML frontmatter with all required fields (title, created, updated, type, tags, sources).
- `authors:` in frontmatter MUST be a YAML list (`- name` per line), never a comma-separated string.
- Tags must exist in SCHEMA.md taxonomy before use. New tag → update SCHEMA first.
- Every new/updated page must have 2+ `[[wikilinks]]` to other pages.
- Every new wiki page MUST have inbound wikilinks from at least one other wiki page (orphan guard — see below).
- Every action logged to `log.md`. Every new page added to `index.md`.
- Contradictions: don't silently overwrite. Note both claims, mark in frontmatter, flag for review.
- Pages over 200 lines → split with cross-links.
- Provenance markers (`([Author, Year](raw/...))`) on paragraphs when synthesizing 3+ sources.

## Conventions

- **Wikilinks:** always use `[[kebab-name|Page Title]]` format.
- **`sources:` frontmatter:** use markdown links — `"[Article Title](raw/path/to/article.md)"` — not bare paths or YAML inline array syntax.
- **sources.md Raw Sources:** each raw article listed as `[Title](raw/articles/dir-name/authorYYYYslug.md)` — link to the file, not the directory.
- **Entity Known Works:** each work links to its raw source, matching the title and path used in `sources:` frontmatter.

### raw/ frontmatter — ADD, don't replace

Raw sources arrive with their own frontmatter (`title`, `author`, `date`, `original_url`, etc.). **Never strip or replace these** — they encode provenance and freshness.
- **Defuddle-extracted content:** defuddle generates `title/description/site/domain/word_count`. Replace those with the wiki standard.
- **Hand-authored / author-marked files:** ADD `source_url` + `ingested` alongside existing fields. Keep `title`, `date`, `original_url`, `author`.
- Only ADD two wiki-managed fields:
  ```yaml
  source_url: https://example.com/article   # original URL, if applicable
  ingested: YYYY-MM-DD
  ```
- `ingested` = when the source was last written. On re-ingest: compare body (after `---`) of new vs old. Same → skip, leave `ingested` as-is. Different → save, update `ingested` to today.

### Raw source body format (strict)

```
---
source_url: https://...
ingested: YYYY-MM-DD
title: "Full Paper Title"
authors:
  - First Author
  - Second Author
date: YYYY-MM-DD
venue: Conference Year
---
# Full Paper Title as h1 heading

**PDF:** [arxiv_id.pdf](arxiv_id.pdf)

## Abstract

Verbatim abstract from the paper — plain text, no blockquote.
```

- `authors:` YAML list, NOT a comma-separated string.
- No other sections. No Key Contributions, Key Results, Architecture, Experiments, etc. The abstract is the author's own distillation; everything else belongs in wiki pages where it can be cross-linked and kept current.
- `title:` value must be quoted — titles with `: ` (e.g. "Self-Instruct: Aligning...") break YAML otherwise.
- If the source lacks an explicit abstract, write one brief factual sentence marked `(condensed from source — no explicit abstract)`. Never invent.

### raw/ directory + filename conventions

| Directory | Contents |
|-----------|----------|
| `raw/articles/` | Blog posts, news, Wikipedia, non-academic |
| `raw/papers/` | Academic papers, preprints, theses |

- Paper directory: `raw/papers/YYYY-MM-author-slug/` (e.g., `2022-12-wang-self-instruct/`).
- Article directory: `raw/articles/YYYY-MM-DD-author-slug/`.
- Paper source file: `firstauthorYYYYfeature.md` (e.g., `wang2022selfconsistency.md`). **NEVER `index.md`.**
  **Why:** Obsidian (this wiki's reader) does not resolve `[](path/)` as `path/index.md`. Every link must end in a concrete `.md` filename or it's a dead end for the reader and a lint failure. Hard rule confirmed by multiple corrections.
- PDF link check: before saving, every artifact in the directory (PDF, supplements) must be reachable via a markdown link in the `.md`. Run `ls raw/papers/<dir>/` and verify each file has a link. (PDF link is `[name.pdf](name.pdf)`, NOT a `[[wikilink]]`.)
- Don't save `pdftotext` `.txt` output to `raw/` — it's a temporary working artifact. Read, verify, discard. PDF is canonical.

## Ingest Protocol

**STOP CHECK before any ingest step:** load this section. The most common multi-pass errors happen when it's consulted only at the start and set aside mid-execution.

### PAPER INGEST STOP CHECK (hard rules — not suggestions)

If the source is a paper (arXiv, academic, preprint):
1. **NEVER use `web_extract` on the paper URL.** It truncates to ~5000 chars and may hallucinate. Corrected multiple times — hard rule.
2. **Download the PDF first**, extract with `pdftotext -layout`, read the full extraction end-to-end.
3. **Do NOT write any file** (raw/index.md, concept page, etc.) until the full text is read.
4. **Do NOT save the pdftotext `.txt` to `raw/`.** Read, verify, discard. The PDF is canonical.
5. Only AFTER full text: write the raw markdown file, then create/update wiki pages.

**Known-topic trap:** Famous papers (BERT, Transformer, GPT) are the MOST dangerous to skim — recognition creates false comprehension. Every paper gets the same treatment: download, extract, read end-to-end before writing a single file. Fame is inversely proportional to your need to actually read it.

### Full-Text Gate (STOP if full text is genuinely unavailable)

After exhausting all avenues (PDF download, browser, alternate mirrors, Semantic Scholar, author pages), if full text is **genuinely inaccessible** (paywall, 404, Cloudflare, withdrawn): **DO NOT PROCEED.** Do not create raw sources or wiki pages from abstract + snippet. Report the blocker to the user and ask: metadata-only, another channel, or skip. This overrides the "skip discussion, proceed" heuristic — full text is a prerequisite.

### Step 1: Acquire full text

**Papers (arXiv):**
- Metadata via arXiv API, NOT `web_extract` (web_extract returns only nav chrome):
  `curl -sL "https://export.arxiv.org/api/query?id_list=XXXX.XXXXX"`
- Download PDF: `curl -sL -o /tmp/paper.pdf "https://arxiv.org/pdf/XXXX.XXXXX.pdf"` then `file /tmp/paper.pdf` (must say "PDF document").
- Extract: `pdftotext -layout /tmp/paper.pdf /tmp/paper.txt` (layout preserves two-column structure).
- Verify author names against the PDF title page — the API is reliable but the PDF is ground truth.
- Do NOT rely on `web_extract` for full text — truncation + hallucination.

**Papers (Springer / PMC / other):**
- Springer: needs a real User-Agent or it 303-redirects: `curl -sL -H "User-Agent: Mozilla/5.0" "https://link.springer.com/content/pdf/10.1007/XXXXX-XXX-XXXX-X.pdf" -o /tmp/paper.pdf`
- PMC mirror: find `citation_pdf_url` in `<meta>` of `https://pmc.ncbi.nlm.nih.gov/articles/PMCXXXXXXX/`, download from that URL.
- Always `file` the result. "HTML document" = redirect path broken.

**Articles / blog posts:**
- Preferred: `curl -sL "https://defuddle.md/<domain>/<path>" -o /tmp/article.md` — full markdown, no truncation. Replace defuddle's extraction metadata with `source_url` + `ingested` (but keep authorial `author`/`date`/`original_url` if present).
- Fallback: `web_extract` directly (articles are shorter). Verify no truncation markers.

### Step 2: Save to raw/

- Directory naming per conventions above.
- Paper source file: `firstauthorYYYYfeature.md` (never `index.md`).
- Body format per "Raw source body format" above.
- Run the verification script after writing:
  `python3 scripts/verify-raw-source.py raw/papers/YYYY-MM-slug/`
  (lives in the repo's `scripts/`, not the skill dir). It catches the most common error: a bare `index.md` where a named file is required, breaking `sources:` links everywhere.
- **Trace the pattern, don't just fix the surface:** when you copy a convention from an existing file and it's wrong, the copy-source is still wrong. Fix both. Run `grep` for the bad pattern across the wiki.

### Step 3: Create / update wiki pages

**Page types** (from SCHEMA.md): `entity` (person/org, 2+ sources or central to one), `concept` (idea/technique/debate), `comparison` (neutral dimension-by-dimension), `query` (research findings).

**Orphan page guard (CRITICAL):** every new page MUST have inbound wikilinks from ≥1 other page. After creating, verify:
```bash
grep -rl '\[\[page-slug|' --include='*.md' . | grep -v 'path/to/page-slug.md'
```
Empty = orphaned. Either add wikilinks from related pages, or merge into an existing page. Before creating: ask which existing pages will link to it. If unclear, the page likely fails the 2-source threshold.

**External reference rule (CRITICAL):** every claim/citation/bibliographic entry in a raw source or wiki page must trace to a raw source we actually hold.
- Do NOT include the paper's bibliography/references list in raw markdown (it's in the PDF).
- Do NOT add parenthetical attributions like `(Hendrycks & Gimpel, 2016)` to works we don't have in `raw/`.
- Do NOT write "Related Models"/"Variants" sections about models (RoBERTa, T5, …) unless we have raw sources for each.
- Do NOT add provenance markers pointing to raw paths that don't exist.
- The paper's own internal citations inside a verbatim quote are fine (they're source text). Paraphrasing them into a bullet list of external works crosses the line.
- Test before closing any ingest: `grep` `raw/` for every author/title you mentioned. If absent, remove the reference.

**Entity detection during paper ingest:** check if orgs (OpenAI, DeepMind, Anthropic, …) and lead authors already have entity pages. If a major lab's paper is landmark and the org has no page, create one. `grep` existing pages before creating — the name may already appear in plain text; convert to wikilinks.

**Pre-ingest audit:** check whether existing pages already reference the raw source (body mention but no `sources:` entry, or a `sources:` link to a directory that was never ingested). Backfill the raw source with the matching filename; add `raw_ingested: true` to the concept page; bump `updated`. Don't rename files to match the skill's default — you'd break existing provenance links.

**Rule of thumb (new concept vs update existing):** new concept when the finding is a standalone named contribution with its own results and cross-link network (>~50 lines, avoids orphan status). Update existing when it's a refinement/limitation/additional evidence for a documented concept.

### Step 4: Verify against full text

**Most common failure point.** After writing wiki pages, re-read the COMPLETE text from the canonical source end-to-end (not a spot-check).
- Are model sizes, dataset names, metrics correct?
- Are baseline comparisons from the actual paper, not memory/secondary sources?
- Did you include limitations, caveats, tradeoffs — not just impressive numbers?
- Did the paper make claims you didn't capture?
- Does any number/label/structural feature that *feels* like it belongs actually appear in the source?
- **Hallucination hotspots:** results tables (numbers mangled by extraction), scaling formulas (math garbled), "first/novel/SOTA" inflation, architecture details (layer counts, dims mis-copied).

### Step 5: Update sources.md + index.md + log.md

- Add new page to the correct section in `index.md` (Entities, Concepts, Comparisons, Queries).
- Add raw source to `sources.md` under Articles or Papers as `[Title](raw/articles/dir/authorYYYYslug.md)` — file link.
- Bump "Total pages: N" in `index.md`.
- Append to `log.md`: `## [YYYY-MM-DD] ingest | Title` — list raw path, URL, authors, summary, created/updated pages, cross-links.
- `log.md` is append-only. Never `write_file` over it — use append (Python or `cat >>`). Then verify last 10 lines.

**Post-Ingest Verification (run after all steps):**
```bash
# 1. No pdftotext .txt artifacts in raw/
find raw/ -name '*.txt' | grep -q . && echo "WARNING: txt artifacts" || echo "OK"
# 2. No '|- ' pipe corruption in any .md
grep -rn '^|-' --include='*.md' concepts/ entities/ comparisons/ queries/ sources.md index.md | head -5
# 3. No bare '|' on empty lines in index.md or sources.md
grep -c '^|$' index.md && echo "WARNING: stray pipe in index.md" || echo "OK index"
grep -c '^|$' sources.md && echo "WARNING: stray pipe in sources.md" || echo "OK sources"
# 4. Raw source body has no sections after Abstract
grep -c '^## ' raw/papers/*/$(ls raw/papers/ | tail -1)/*.md | grep -v Abstract && echo "WARNING" || true
```
If check 2 fires, repair with `python3 scripts/fix-pipe-corruption.py <file>` (handles all three corruption patterns, idempotent). Also run it on any other affected file.

### Re-ingest (source already in wiki)

When the user says "сделай ingest X" and the paper is already ingested:
1. **Do NOT ask "do you want updates?"** — the command IS the instruction. Proceed directly.
2. Download fresh (or reuse verified), extract, read end-to-end.
3. **Structured gap scan** vs the existing concept page — gaps cluster predictably: economic/compute data (cost, params, FLOPs), objective-function details (loss, KL coefficients), comparison data vs related methods (not in main table), Discussion-section caveats (alignment target, dual-use, bias), qualitative failure taxonomy, Related Work cross-links, full authorship/affiliations.
4. Apply missing details, bump `updated`, append log, run Post-Ingest Verification.
Treat every re-ingest as a quality audit of the existing page, not confirmation of what it already says.

### Compare vs discuss heuristic

- User says "сделай ingest" / "ingest this" explicitly → check Full-Text Gate first. Full text acquired → skip discussion, proceed. Unavailable → report blocker, don't proceed.
- User shares a link/file with no verb → present takeaways first, ask before creating pages.
- Cron/automated context → always skip discussion, log and go.
- "сразу обрабатывай" / "just process it" / "proceed directly" → skip discussion even in interactive session.
- СТОП / stop → halt immediately, no further changes.

### Pitfalls (consolidated)

- **web_extract truncation trap** on papers — always download+extract PDF separately.
- **Synthesis before full text** — both raw + concept pages share the same blind spots. Read first.
- **Author/venue hallucination in web_extract** — verify against PDF title page, not HTML abstract.
- **arXiv preprint vs published venue** — "arXiv preprint" is not the venue; check PDF footer, update venue in raw + pages.
- **Fabricated data tolerance** — if unverified against full text, it's guesswork. Omit or mark uncertain.
- **No-full-text fabrication** — abstract + snippet is not a source. Stop and report.
- **Ghost wikilinks** — before finalising a wikilink, verify the target slug exists (`search_files(pattern='slug', target='files')` or index.md). Broken link > no link. Create the target in the same pass or use plain text.
- **Ignoring caveats** — capture tradeoffs, not just headline claims.
- **log.md overwrite** — use append only.
- **Pipe corruption via `patch`** — `patch`'s fuzzy matcher can merge a `|` from nearby lines into `- ` / `> ` markers. After any `index.md` patch, run the fix script. Copying `|- ` from `read_file`'s `LINE_NUM|CONTENT` display into a patch introduces a leading pipe — strip the separator pipe mentally.
- **Index desync** — creating pages without index.md entry guarantees orphans on next lint.
- **Plain-text pollution** — don't commit `pdftotext` output to `raw/`.
- **Shell glob/backtick corrosion** — paths with `` ` * ? $ { `` corrupt inline Python in `terminal()`. Prefer `execute_code` for such paths.

## Query

1. Read `index.md` to find relevant pages. `sources.md` has the raw source catalog.
2. For 100+ page wikis, also `search_files` for key terms.
3. Synthesize citing wiki pages: "Based on [[page-a]] and [[page-b]]…".
4. File substantial answers as `queries/` or `comparisons/` pages (not trivial lookups).
5. Update `log.md`: `## [YYYY-MM-DD] query | subject`.

## Lint

Run all checks, report grouped by severity (broken links > orphans > source drift > contested > stale > style):
- Orphan pages (no inbound wikilinks)
- Broken wikilinks (point to non-existent pages)
- Index completeness (every wiki page in index.md, every raw source in sources.md)
- Frontmatter validation (required fields, tags in taxonomy)
- Stale content (>90 days vs newest related source)
- Contradictions (`contested: true`, `contradictions:`)
- Page size (>200 lines → split)
- Tag audit (flag tags outside SCHEMA.md)
- Log rotation (if log.md >500 entries, rename to `log-YYYY.md`, start fresh)
