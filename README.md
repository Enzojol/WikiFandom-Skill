# fandom-kb

**Give Claude a real knowledge base for any wiki.** `fandom-kb` turns a Fandom (or any MediaWiki) wiki into a local knowledge base, one per wiki: clean Markdown, structured JSON and a SQLite database where every infobox and recurring data template (stats, costs, attacks, even when nested) becomes a table.

So instead of "let me search the web…", Claude can answer:

> *Which infantry unit has the best HP at rank 6 for under 2,000 gold?*

```sql
SELECT title, gold_cost, hp_6 FROM units
WHERE type = 'Infantry' AND gold_cost < 2000 ORDER BY hp_6 DESC LIMIT 5;
```

…and cite the wiki pages it used.

## Why not just RAG over scraped pages?

| | Scrape + RAG | fandom-kb |
|---|---|---|
| "What does X do?" | ✅ | ✅ full-text search (FTS5/BM25), redirects and aliases resolved |
| "Rank / compare / filter 200 units" | ❌ the model guesses from chunks | ✅ SQL over typed infobox tables |
| Per-rank stats `40 / 46 / 52` or `70; 85; 105` | ❌ opaque strings | ✅ `hp_1, hp_2, hp_3` via profiles |
| Attacks nested in weapon templates | ❌ flattened text | ✅ child rows linked to their parent (`parent_idx`) |
| Re-sync | re-scrape everything | ✅ incremental: only changed revisions |
| Wiki quirks (tabbers, navboxes, refs, tables) | noise | ✅ handled by a real wikitext parser |

## Install

**Claude Code** (plugin marketplace):
```
/plugin marketplace add Enzojol/Fandom-Skill
/plugin install fandom-kb@fandom-kb
```

**Claude apps**: zip `skills/fandom-kb/` and upload it in *Settings → Capabilities → Skills*. Note: the app sandbox may not be allowed to reach fandom.com. In that case run `fetch` locally, or `import` an XML dump.

**CLI only**:
```bash
pip install -r skills/fandom-kb/requirements.txt
alias kb="python3 $PWD/skills/fandom-kb/scripts/fandom_kb.py"
```

## Usage: Battle Nations example

```bash
kb fetch battlenations                 # whole wiki, incremental, 1 req/s
kb fetch battlenations --category Units
kb search battlenations "anti-armor"
kb show battlenations "Heavy Gunner"
kb schema battlenations                # SQL tables + columns
kb profile-init battlenations          # draft typed columns → edit → kb build-db battlenations
kb sql battlenations "SELECT title, cost FROM units ORDER BY cost DESC LIMIT 10"
kb export battlenations --template "Infobox Unit" -o units.csv
```

Other wikis: `kb fetch onepiece --lang fr`, `kb fetch https://terraria.wiki.gg/wiki/Zenith --api https://terraria.wiki.gg/api.php`, `kb import pages_current.xml.gz`.

## Layout of a KB

```
~/.fandom-kb/battlenations/
  meta.json        site info, licence, sync state
  index.jsonl      one line per page (title, url, categories, infobox, summary, aliases)
  aliases.json     redirects
  raw/*.wiki       original wikitext
  pages/*.md       readable Markdown with front matter (source URL, licence)
  pages/*.json     infoboxes, data templates, sections, links, categories
  profile.yaml     optional local profile
  kb.sqlite        pages, pages_fts, categories, links, aliases, template_values (every field),
                   one table per infobox and per recurring data template
```

## Profiles: the part that compounds

Every wiki names its fields its own way. A profile (`skills/fandom-kb/profiles/<wiki>.yaml`) maps the raw infobox fields to clean, typed columns (see [`_example.yaml`](skills/fandom-kb/profiles/_example.yaml)). `profile-init` drafts one in seconds; a human makes it right once, and then everybody benefits. **PRs adding profiles are the most valuable contribution.**

## Being a good citizen

- 1 request/second by default, descriptive User-Agent, `maxlag`, backoff on 429/503; big jobs require `--yes`.
- Wiki content is usually **CC BY-SA**. Each page keeps its source URL and the wiki's licence. This repo's code is MIT, but the data you download keeps its licence.
- Prefer official XML dumps for very large wikis.

## Roadmap

- [ ] `kb pull <wiki>`: download prebuilt, versioned KBs (GitHub Releases / Hugging Face) instead of scraping
- [ ] MCP server (`search`, `show`, `sql`, `schema` tools) for Claude Desktop, Cursor and others
- [ ] Evals per wiki: questions with known answers, scored with vs. without the skill (`evals/`)
- [ ] Incremental sync via `recentchanges`; Lua `Module:` data tables; cargo/SMW tables when a wiki has them
- [ ] Community profiles for popular wikis

## Development

```bash
python -m pytest tests/      # offline: fake API client + XML dump fixtures
```

MIT © Enzo
