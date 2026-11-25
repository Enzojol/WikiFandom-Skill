# fandom-kb

**Lets Claude actually read a wiki.** `fandom-kb` is a Claude skill and CLI. It downloads a Fandom or MediaWiki wiki into a local knowledge base on your machine. Claude can then search the pages, read them and query their data with SQL, instead of guessing from search snippets.

## The problem

Ask Claude about a game, show or book, and it has two sources: what it remembers, and web search. On Fandom both are weak:

- **Claude can't open Fandom pages.** In our tests, Claude's web fetch got `HTTP 402` whenever it tried to open a Fandom page. It fell back to search-result snippets, mirror sites and memory.
- **Snippets are fine for famous facts and bad at numbers.** A unit's cost, a weapon's damage at max rank, "how many units need the Barracks" are niche, change with patches and rarely show up in a snippet.
- **Rankings and counts need the whole dataset.** "Which shotgun deals the most damage?" means comparing every shotgun. No snippet holds that, so Claude guesses.

## What fandom-kb changes

| | Claude alone | Claude with fandom-kb |
|---|---|---|
| Source | search snippets, mirrors, memory | the wiki's own pages, downloaded through its official API |
| "What does X do?" | usually right for famous things | read from the page, with the link |
| Exact stats, costs, requirements | often slightly wrong or outdated | read from the page's infobox |
| Rank, count, filter, compare many pages | guesses from a few pages | one SQL query over every page |
| Sources | sometimes a mirror site | the exact wiki page URL |
| Freshness | whatever the web search returns | the date of your last sync, updated incrementally |

## Example

> *In Battle Nations, among the units trained at the Barracks, which attack has the highest maximum damage?*

Without the skill, Claude found the right unit on a mirror site, but compared it with only one other unit and gave the wrong damage range. With the skill, it joined two tables built from the wiki's templates and checked every Barracks unit:

```sql
SELECT p.title, a.name AS attack, a.mindmg, a.maxdmg
FROM attackbox a JOIN unitprofile p ON p.title = a.title
WHERE p.building_required LIKE 'Barracks%'
ORDER BY a.maxdmg DESC LIMIT 3;
```

```
title          | attack             | mindmg | maxdmg
---------------+--------------------+--------+-------
Railgun Sniper | High Velocity Bolt | 150.0  | 250.0
The Wimp       | Juiced Clap        | 144.0  | 216.0
Guerrilla      | C4                 | 144.0  | 216.0
```

These tables came out of a single command, `kb fetch battlenations --category Units`: 299 pages in 10 API requests, no setup.

## Results

We asked 21 questions about 3 wikis (Battle Nations, Jujutsu Kaisen, Warframe) and checked every answer on the live wiki. Claude Sonnet answered each question twice: once with web search only, once with web search plus fandom-kb. Claude Opus graded the answers.

| | web search only | with fandom-kb |
|---|---|---|
| **overall** | 62% | **98%** |
| lookup (one fact) | 67% | 100% |
| compare (two things) | 92% | 100% |
| aggregate (rank, count, filter) | 33% | 92% |
| multi-hop (combine facts) | 50% | 100% |
| average time per answer | 24 s | 13 s |
| average cost per answer | $0.053 | $0.061 |

The gain is biggest on rankings, counts and niche stats. Comparing two well-known things already works fairly well without the skill. Each answer costs slightly more, because Claude reads real data instead of snippets.

This is one run of 21 questions, not a benchmark, and the grading moves a few points between runs. Every question, answer and verdict is in [`evals/results/`](evals/results/), and [`evals/`](evals/) explains how to re-run it.

## Install

**Claude Code** (plugin):
```
/plugin marketplace add Enzojol/Fandom-Skill
/plugin install fandom-kb@fandom-kb
```
Then ask a question about any franchise. Claude loads the skill and fetches the pages it needs.

**Claude apps** (claude.ai, Desktop): zip the `skills/fandom-kb/` folder and upload it in *Settings → Capabilities → Skills*. The app's sandbox may not be allowed to reach fandom.com. If so, run `kb fetch` on your machine, or build the knowledge base from an XML dump with `kb import`.

**Command line only.** With [uv](https://docs.astral.sh/uv/), the dependencies install on first run:
```bash
alias kb="uv run $PWD/skills/fandom-kb/scripts/fandom_kb.py"
```
Without uv: `pip install -r skills/fandom-kb/requirements.txt`, then `alias kb="python3 $PWD/skills/fandom-kb/scripts/fandom_kb.py"`.

Requires Python 3.9+.

## Commands

```bash
kb fetch battlenations                     # whole wiki (incremental, 1 request per second)
kb fetch battlenations --category Units    # one category
kb fetch battlenations --pages "Sniper,Heavy Tank"
kb list                                    # local knowledge bases and their sync date
kb search battlenations "anti-armor"       # full-text search
kb show battlenations "Heavy Gunner"       # read a page as Markdown (--section, --json)
kb schema battlenations                    # SQL tables, columns and common values
kb sql battlenations "SELECT title, hp_last FROM unitranksbox ORDER BY hp_last DESC LIMIT 10"
kb export battlenations --template "UnitProfile" -o units.csv
kb profile-init battlenations              # draft a profile, edit it, then: kb build-db battlenations
```

The wiki can be named several ways: `battlenations`, `battlenations.fandom.com`, any page URL, `kb fetch onepiece --lang fr` for a language edition, `--api https://terraria.wiki.gg/api.php` for a MediaWiki site outside Fandom, or `kb import pages_current.xml.gz` for a dump.

## How it works

1. **Fetch.** Downloads page wikitext through the MediaWiki API, 50 pages per request. On Fandom it also reads each page's rendered infobox data, which covers infoboxes built by Lua modules. Later runs download only the pages that changed.
2. **Parse.** A real wikitext parser (`mwparserfromhell`) turns each page into clean Markdown and structured JSON. It handles infoboxes, nested templates, tabbers, references and redirects.
3. **Build tables.** Each infobox, and each data template used on 2 or more pages (stats, costs, attacks), becomes a SQLite table with one column per field. Templates nested inside another template are linked to their parent row. Per-rank values like `70; 85; 105` also get numeric columns (`hp_1`, `hp_2`, …, `hp_last`).
4. **Answer.** Claude follows [`SKILL.md`](skills/fandom-kb/SKILL.md): search or read pages for single facts, SQL for anything that compares many pages, and always cite the page URL.

Everything for one wiki lives in one folder:

```
~/.fandom-kb/battlenations/
  kb.sqlite        full-text index, one table per template, plus pages, categories, links, aliases
  pages/*.md       readable pages, each with its source URL and licence
  pages/*.json     structured pages: infoboxes, templates, sections, links
  raw/*.wiki       original wikitext, so the KB can be rebuilt without downloading again
  index.jsonl      one line per page
  meta.json        site info, licence, sync state
```

Set `FANDOM_KB_DIR` to store knowledge bases somewhere else.

## Profiles

Out of the box, columns keep the wiki's own field names, and values like `1,200 Gold` stay as text (with a numeric `_num` column next to them). A profile ([example](skills/fandom-kb/profiles/_example.yaml)) renames fields, sets types, splits per-rank lists and drops noise. `kb profile-init` drafts one from the data. Profiles in `skills/fandom-kb/profiles/` are applied automatically, so one good profile helps everyone who uses that wiki. **Profile pull requests are the most useful contribution.**

## Compatibility

Every wiki structures its data differently, so compatibility is measured rather than assumed. [`docs/compatibility.md`](docs/compatibility.md) runs the full pipeline on 20 random articles from each of 31 Fandom wikis: games, anime, TV, film and books, in English, French, Spanish and German.

All 31 work end to end. Of the articles that show an infobox, fandom-kb extracts it on 98%, and on 28 of the 31 wikis it extracts every one. Each miss is checked against the wiki's own rendered page.

Other MediaWiki sites (wiki.gg, self-hosted wikis) work through `--api`, but they are less tested.

## Limits

- **Claude needs a shell and network access** to fetch. That works in Claude Code. In the Claude apps, the sandbox may block fandom.com.
- **The data is a snapshot.** Run `kb fetch` again to update it. Only changed pages are downloaded.
- **Some data isn't in tables yet:** free-form wikitables in page bodies, and data stored in Lua `Module:` pages. That data is still searchable and readable as text.
- **XML dumps lack Fandom's rendered infoboxes,** so infoboxes built by Lua come out empty. Prefer `fetch` when the wiki is small enough.

## Being a good citizen

- 1 request per second by default, a User-Agent that links to this repo, `maxlag`, and backoff on 429/503 errors. Downloads over 3,000 pages ask for confirmation (`--yes`).
- Wiki text is usually licensed **CC BY-SA**. Every page keeps its source URL and the wiki's licence. The code in this repo is MIT; the data you download keeps its own licence.
- For very large wikis, prefer the official XML dumps.

## Roadmap

- [ ] MCP server (`search`, `show`, `sql`, `schema`) for Claude Desktop, Cursor and other clients
- [ ] `kb pull <wiki>`: download prebuilt, versioned knowledge bases instead of fetching
- [ ] Wikitables, Lua `Module:` data and Cargo/SMW tables as SQL tables
- [ ] Profiles for popular wikis
- [ ] More eval questions and wikis

## Development

```bash
python -m pytest tests/                 # offline tests: fake API client and XML dump fixtures
uv run tools/compat.py                  # live scorecard → docs/compatibility.md (~3 min, 1 request/s)
uv run tools/compat.py naruto -n 10     # one wiki, printed only
```

## License

MIT © Enzo Jolivet
