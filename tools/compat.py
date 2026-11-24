#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["mwparserfromhell>=0.6", "requests>=2.28", "pyyaml>=6.0"]
# ///
"""Compatibility scorecard: run the real pipeline on random pages of many wikis and measure what it extracts.

    uv run tools/compat.py                      # all wikis in tools/compat_wikis.txt → docs/compatibility.md
    uv run tools/compat.py warframe naruto -n 10

Each wiki costs ~4 API requests at 1 request/second. Random pages change between runs, so compare
trends, not single numbers. Every regression found here should become an offline test in tests/.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "fandom-kb" / "scripts"))
import fandom_kb as fk  # noqa: E402

LEAK = ("{{", "}}", "[[", "<", "|}", "{|")


def random_titles(client, n: int) -> list:
    data = client.get(action="query", list="random", rnnamespace=0, rnlimit=n, rnfilterredir="nonredirects")
    return [r["title"] for r in data["query"]["random"]]


def score(name: str, n: int, root: Path, delay: float) -> dict:
    wname, lang = (name.split("/", 1) + [None])[:2]
    wiki = fk.resolve(wname, lang)
    client = fk.Client(wiki.api, delay)
    kb = fk.KB(root, wiki.slug)
    res = fk.sync(kb, client, wiki, {"pages": random_titles(client, n)})
    pages = list(kb.index.values())
    docs = [kb.load_doc(e) for e in pages]
    raws = [(kb.raw / f"{e['slug']}.wiki").read_text(encoding="utf-8") for e in pages]
    ns = fk.Namespaces.from_meta(kb.meta)
    guess_only = [fk.parse_wikitext(r, e["title"], ns)["infoboxes"] for e, r in zip(pages, raws)]
    boxes = [b for d in docs for b in d["infoboxes"]]
    values = [v for b in boxes for v in b["fields"].values() if v]
    names: dict = {}
    for b in boxes:
        names[b["template"]] = names.get(b["template"], 0) + 1
    pct = lambda k: round(100 * k / len(pages)) if pages else 0
    vpct = lambda k: round(100 * k / len(values)) if values else 0
    return {
        "wiki": wiki.slug, "pages": len(pages),
        "infobox": pct(sum(bool(d["infoboxes"]) for d in docs)),
        "wikitext_only": pct(sum(bool(g) for g in guess_only)),
        "portable": pct(sum(any(b.get("source") == "portable" for b in d["infoboxes"]) for d in docs)),
        "guessed": pct(sum(bool(d["infoboxes"]) and not any(b.get("source") == "portable" for b in d["infoboxes"])
                           for d in docs)),
        "unnamed": sum(b["template"] == "Infobox" for b in boxes),
        "numeric": vpct(sum(fk.looks_numeric(v) for v in values)),
        "leak": vpct(sum(any(t in v for t in LEAK) for v in values)),
        "tables": len(res["tables"]),
        "invoke": pct(sum("#invoke:" in r.lower() for r in raws)),
        "wikitable": pct(sum("{|" in r for r in raws)),
        "bare": pct(sum(not (d["infoboxes"] or d["templates"]) for d in docs)),
        "requests": res["requests"],
        "top": ", ".join(k for k, _ in sorted(names.items(), key=lambda kv: -kv[1])[:3]),
    }


COLUMNS = ["wiki", "pages", "infobox", "wikitext_only", "portable", "guessed", "unnamed", "numeric", "leak", "tables",
           "invoke", "wikitable", "bare", "top"]

LEGEND = """\
| column | meaning |
|---|---|
| pages | random articles fetched |
| infobox | % of pages with at least one infobox extracted |
| wikitext_only | same, if the infobox were only guessed from wikitext (what fandom-kb did before reading portable infoboxes) |
| portable | % of pages whose infobox came from Fandom's rendered portable infobox (page property) |
| guessed | % of pages whose infobox was guessed from wikitext (no portable infobox on the page) |
| unnamed | portable infoboxes that matched no template call (table falls back to `infobox`) |
| numeric | % of infobox values that parse as numbers |
| leak | % of infobox values still containing markup (`{{`, `[[`, `<`, table syntax): should be ~0 |
| tables | SQL tables built from this sample |
| invoke | % of pages calling a Lua module (`#invoke`): data may live in `Module:` pages |
| wikitable | % of pages with a wikitable: data the SQL tables don't capture yet |
| bare | % of pages with no infobox and no data template (prose, lists, stubs) |
| top | most common infobox templates |
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("wikis", nargs="*", help="wiki names (default: tools/compat_wikis.txt)")
    ap.add_argument("-n", type=int, default=20, help="random pages per wiki (default 20)")
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("-o", type=Path, help="write Markdown here (default: docs/compatibility.md when no wikis given)")
    a = ap.parse_args(argv)
    wikis = a.wikis or [l.strip() for l in (ROOT / "tools" / "compat_wikis.txt").read_text().splitlines()
                        if l.strip() and not l.startswith("#")]
    out = a.o or (None if a.wikis else ROOT / "docs" / "compatibility.md")
    rows, failures = [], []
    with tempfile.TemporaryDirectory() as d:
        for w in wikis:
            t = time.time()
            try:
                r = score(w, a.n, Path(d), a.delay)
                rows.append(r)
                print(" | ".join(str(r[c]) for c in COLUMNS) + f"   ({time.time() - t:.0f}s)", flush=True)
            except (Exception, SystemExit) as e:  # noqa: BLE001
                failures.append((w, str(e)[:200]))
                print(f"{w}: FAILED {e}", flush=True)
    if out:
        lines = [f"# Compatibility scorecard", "",
                 f"Generated {date.today().isoformat()} by `uv run tools/compat.py` (fandom-kb {fk.VERSION}): "
                 f"{a.n} random articles per wiki, full pipeline (fetch, parse, build SQLite).", "",
                 "| " + " | ".join(COLUMNS) + " |", "|" + "---|" * len(COLUMNS)]
        lines += ["| " + " | ".join(str(r[c]).replace("|", "\\|") for c in COLUMNS) + " |" for r in rows]
        lines += ["", f"**Average** over {len(rows)} wikis: infobox {avg(rows, 'infobox')}%, "
                  f"wikitext only {avg(rows, 'wikitext_only')}%, portable {avg(rows, 'portable')}%, numeric {avg(rows, 'numeric')}%, leak {avg(rows, 'leak')}%.", ""]
        if failures:
            lines += ["**Failed:**", ""] + [f"- `{w}`: {e}" for w, e in failures] + [""]
        lines += ["## Known limits", "",
                  "- Fandom truncates the infobox page property at 64 KB; such pages fall back to the wikitext guess.",
                  "- Portable infoboxes drawn by sub-templates match no template call: they land in a generic `infobox` "
                  "table (`unnamed`).",
                  "- XML dumps carry no page properties: `kb import` always uses the wikitext guess.",
                  "- `bare` pages are often stubs, lists or disambiguations; `wikitable` and `invoke` show data not yet in SQL.",
                  "", "## Columns", "", LEGEND]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines), encoding="utf-8")
        print(f"→ {out}")


def avg(rows, k):
    return round(sum(r[k] for r in rows) / len(rows)) if rows else 0


if __name__ == "__main__":
    main()
