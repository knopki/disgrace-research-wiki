# Wiki Schema

## Domain
LLM, ML, AI agents, research methodologies, and related infrastructure.
Covers: model architectures, training techniques, alignment, inference optimization,
agent frameworks, evaluation benchmarks, and research methodology.

## Conventions
- Language: all wiki prose in English. Direct quotes from sources preserve the original language.
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
|- **Provenance markers:** On pages that synthesize 3+ sources, append
  `([Author, Year](raw/path/to/index.md))` at the end of paragraphs whose claims come from a
  specific source. The short label follows "Author, Year" format (e.g., `Ivanov, 2025`,
  `Hao et al., 2024`, `Anthropic, 2022`), and links to the raw source. This lets a reader
  trace each claim back without re-reading the whole raw file. Optional on single-source
  pages where the `sources:` frontmatter is enough.

## Frontmatter
  ```yaml
  ---
  title: Page Title
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: entity | concept | comparison | query | summary
  tags: [from taxonomy below]
  sources:
  - "[Article Title](raw/articles/dir-name/index.md)"
  # Optional quality signals:
  confidence: high | medium | low        # how well-supported the claims are
  contested: true                        # set when the page has unresolved contradictions
  contradictions: [other-page-slug]      # pages this one conflicts with
  ---
  ```

`confidence` and `contested` are optional but recommended for opinion-heavy or fast-moving
topics. Lint surfaces `contested: true` and `confidence: low` pages for review so weak claims
don't silently harden into accepted wiki fact.

### raw/ Frontmatter

Raw sources already have their own frontmatter from the author or ingestion tool
(title, author, date, original_url, description, site, word_count, etc.).
**NEVER strip or replace these fields** — they encode source freshness and provenance.

Only **add** two wiki-managed fields:

```yaml
---
source_url: https://example.com/article   # original URL, if applicable
ingested: YYYY-MM-DD
---
```

The existing `title`, `author`, `date` (publication date, not ingested), etc. all stay
as-is. `date` is especially important — it tells you how fresh the fact is.

### raw/ Structure

| Directory | Contents |
|-----------|----------|
| `raw/articles/` | Blog posts, news, Wikipedia pages, and other non-academic sources |
| `raw/papers/` | Academic papers, preprints, conference publications, and theses |

## Tag Taxonomy
- Models: model, architecture, benchmark, training, inference, mixture-of-experts
- Agents: agent, framework, tool-use, planning, orchestration, multi-agent
- Techniques: optimization, fine-tuning, alignment, rlhf, distillation, quantization, data, technique
- Infrastructure: serving, deployment, hardware, gpu, distributed
- Research: methodology, evaluation, reproducibility, scaling-law, paper, interpretability
- Meta: comparison, timeline, controversy, prediction, survey, organization
- Knowledge: knowledge-graph, search, information-retrieval

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it. This prevents tag sprawl.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages
One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
