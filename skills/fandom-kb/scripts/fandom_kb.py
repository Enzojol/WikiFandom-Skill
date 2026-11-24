#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["mwparserfromhell>=0.6", "requests>=2.28", "pyyaml>=6.0"]
# ///
"""fandom-kb — turn any Fandom / MediaWiki wiki into a local, queryable knowledge base.

One knowledge base per wiki, stored under $FANDOM_KB_DIR (default ~/.fandom-kb/<wiki>/):

    raw/<slug>.wiki      original wikitext (re-parse without re-downloading)
    pages/<slug>.md      clean Markdown for reading
    pages/<slug>.json    structured page: infoboxes, data templates, links, categories
    index.jsonl          one line per page
    aliases.json         redirect -> target
    kb.sqlite            full-text search (FTS5) + one table per infobox and recurring data template
    meta.json            site info, licence, sync state

Commands: fetch, import, list, search, show, sql, schema, export, profile-init, build-db
Run `fandom_kb.py <command> -h` for details.
Easiest: `uv run fandom_kb.py <command>` installs the dependencies declared above on the fly.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import os
import re
import sqlite3
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

try:
    import mwparserfromhell as mwp
    from mwparserfromhell.nodes import (Argument, Comment, ExternalLink, Heading, HTMLEntity,
                                        Tag, Template, Text, Wikilink)
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency. Run with `uv run fandom_kb.py …` (installs them automatically), "
             "or: pip install mwparserfromhell requests pyyaml")

try:
    import yaml  # optional: profiles can also be JSON
except ImportError:  # pragma: no cover
    yaml = None

VERSION = "0.1.0"
USER_AGENT = f"fandom-kb/{VERSION} (+https://github.com/fandom-kb/fandom-kb; personal knowledge base)"
DEFAULT_ROOT = Path(os.environ.get("FANDOM_KB_DIR", Path.home() / ".fandom-kb"))
PROFILES_DIR = Path(__file__).resolve().parent.parent / "profiles"
CONFIRM_THRESHOLD = 3000  # pages; above this `fetch` needs --yes
AUTO_TABLE_MIN_PAGES = 2  # a body or nested data template used on this many pages gets its own SQL table
RANK_SEPARATORS = ("/", ";", "·")  # "40 / 46 / 52", "70; 85; 105" → one column per rank via `split`


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# ---------------------------------------------------------------------------
# Wiki resolution
# ---------------------------------------------------------------------------

LANG_RE = re.compile(r"^[a-z]{2,3}(-[a-z]{2,4})?$")


@dataclass
class Wiki:
    slug: str           # local KB name, e.g. "battlenations" or "onepiece-fr"
    base: str           # https://onepiece.fandom.com/fr
    api: str            # https://onepiece.fandom.com/fr/api.php
    lang: str | None = None
    page: str | None = None  # page title if the input was a page URL

    def page_url(self, title: str) -> str:
        path = quote(title.replace(" ", "_"), safe="/:(),!'")
        return f"{self.base}/wiki/{path}"


def resolve(target: str, lang: str | None = None, api: str | None = None) -> Wiki:
    """Accepts 'battlenations', 'battlenations.fandom.com', a page URL, or any MediaWiki URL with --api."""
    t = target.strip()
    if "://" not in t and "." not in t and "/" not in t:  # bare Fandom name
        l = lang if lang and lang != "en" else None
        base = f"https://{t}.fandom.com" + (f"/{l}" if l else "")
        return Wiki(slug=t + (f"-{l}" if l else ""), base=base, api=api or base + "/api.php", lang=l)
    if "://" not in t:
        t = "https://" + t
    u = urlparse(t)
    host = u.netloc
    parts = [p for p in u.path.split("/") if p]
    l, page = lang, None
    if parts and parts[0] not in ("wiki", "api.php", "w", "index.php") and LANG_RE.match(parts[0]):
        l, parts = parts[0], parts[1:]
    if len(parts) >= 2 and parts[0] == "wiki":
        page = unquote("/".join(parts[1:])).replace("_", " ")
    if l == "en":
        l = None
    base = f"{u.scheme}://{host}" + (f"/{l}" if l else "")
    name = host.split(".")[0] if host.endswith("fandom.com") else re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-")
    return Wiki(slug=name + (f"-{l}" if l else ""), base=base, api=api or base + "/api.php", lang=l, page=page)


# ---------------------------------------------------------------------------
# HTTP client (polite: UA, 1 req/s, maxlag, backoff)
# ---------------------------------------------------------------------------

class Client:
    def __init__(self, api: str, delay: float = 1.0):
        import requests
        self.requests = requests
        self.api = api
        self.delay = delay
        self.s = requests.Session()
        self.s.headers["User-Agent"] = USER_AGENT
        self.last = 0.0
        self.calls = 0

    def get(self, **params) -> dict:
        params = {**params, "format": "json", "formatversion": "2", "maxlag": "5"}
        err = None
        for attempt in range(6):
            wait = self.delay - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
            try:
                r = self.s.get(self.api, params=params, timeout=60)
            except self.requests.RequestException as e:
                err = e
                time.sleep(2 ** attempt)
                continue
            finally:
                self.last = time.time()
                self.calls += 1
            if r.status_code in (429, 500, 502, 503, 504):
                ra = r.headers.get("Retry-After")
                time.sleep(float(ra) if ra and ra.isdigit() else 2 ** attempt * 2)
                err = RuntimeError(f"HTTP {r.status_code}")
                continue
            if r.status_code == 404:
                raise RuntimeError(f"No MediaWiki API at {self.api} (HTTP 404). Check the wiki name/lang or pass --api.")
            r.raise_for_status()
            try:
                data = r.json()
            except ValueError:
                raise RuntimeError(f"{self.api} did not return JSON — is this a MediaWiki api.php URL?")
            if "error" in data:
                if data["error"].get("code") == "maxlag":
                    time.sleep(5)
                    continue
                raise RuntimeError(f"API error: {data['error']}")
            return data
        raise RuntimeError(f"Giving up after retries: {err}")

    def query_all(self, **params):
        cont: dict = {}
        while True:
            data = self.get(action="query", **params, **cont)
            yield data
            if "continue" not in data:
                return
            cont = data["continue"]


# ---------------------------------------------------------------------------
# Wikitext parsing
# ---------------------------------------------------------------------------

DEFAULT_NS = {
    "category": {"category", "catégorie", "categoría", "categoria", "kategorie", "kategoria", "категория"},
    "file": {"file", "image", "fichier", "archivo", "datei", "arquivo", "imagen", "bild", "video", "media", "plik", "файл"},
    "template": {"template", "modèle", "plantilla", "predefinição", "vorlage", "szablon", "шаблон"},
}
INFOBOX_HINT = re.compile(r"infobox|info box|^box\b|\bbox$|^(unit|building|character|item|enemy|mission|personnage)\b", re.I)
SKIP_TEMPLATE = re.compile(r"navbox|^nav\b|stub|clear|clr|^reflist|^toc|^disambig|^delete|^cleanup|^sic$", re.I)
SKIP_TAGS = {"ref", "references", "gallery", "imagemap", "includeonly", "templatedata", "math", "score", "mapframe", "div style"}
MAGIC_RE = re.compile(r"__[A-Z]+__")


class Namespaces:
    def __init__(self, category=None, file=None, template=None):
        self.category = {s.lower() for s in (category or DEFAULT_NS["category"])}
        self.file = {s.lower() for s in (file or DEFAULT_NS["file"])}
        self.template = {s.lower() for s in (template or DEFAULT_NS["template"])}

    @classmethod
    def from_meta(cls, meta: dict | None):
        ns = (meta or {}).get("namespaces") or {}
        return cls(set(ns.get("category", [])) | DEFAULT_NS["category"],
                   set(ns.get("file", [])) | DEFAULT_NS["file"],
                   set(ns.get("template", [])) | DEFAULT_NS["template"])

    def to_meta(self):
        return {"category": sorted(self.category), "file": sorted(self.file), "template": sorted(self.template)}


@dataclass
class Ctx:
    title: str
    ns: Namespaces
    categories: list = field(default_factory=list)
    links: list = field(default_factory=list)
    images: list = field(default_factory=list)
    infoboxes: list = field(default_factory=list)
    templates: list = field(default_factory=list)
    nested: list = field(default_factory=list)   # data templates inside another template's parameter
    parents: list = field(default_factory=list)  # stack of (template, idx, param) while rendering params
    next_idx: int = 0                            # page-local id of each template instance
    seen_heading: bool = False
    depth: int = 0


def clean_ws(s: str) -> str:
    return re.sub(r"[ \t]*\n[ \t]*", " ", s).strip()


def template_name(tpl, ns: Namespaces) -> str:
    name = clean_ws(str(tpl.name.strip_code() if hasattr(tpl.name, "strip_code") else tpl.name)) or clean_ws(str(tpl.name))
    name = MAGIC_RE.sub("", name).replace("_", " ").strip()
    if ":" in name and name.split(":", 1)[0].strip().lower() in ns.template:
        name = name.split(":", 1)[1].strip()
    return name[:1].upper() + name[1:] if name else name


LIST_TAGS = ("li", "dd", "dt")


def render(code, ctx: Ctx) -> str:
    out: list[str] = []
    nodes = code.nodes
    i = 0
    while i < len(nodes):
        n = nodes[i]
        if isinstance(n, Tag) and str(n.tag).lower() in LIST_TAGS and n.wiki_markup:
            # "**" or "*#" are emitted as consecutive list tags: their count is the nesting depth
            markers = [str(n.wiki_markup)]
            while i + 1 < len(nodes) and isinstance(nodes[i + 1], Tag) and str(nodes[i + 1].tag).lower() in LIST_TAGS \
                    and nodes[i + 1].wiki_markup:
                i += 1
                markers.append(str(nodes[i].wiki_markup))
            last = markers[-1]
            bullet = "1." if last == "#" else "-" if last == "*" else ""
            prefix = "  " * (len(markers) - 1) + bullet
            prev = "".join(out[-1:])
            out.append(prefix if (not prev or prev.endswith("\n")) else "\n" + prefix)
        else:
            out.append(render_node(n, ctx))
        i += 1
    return "".join(out)


def render_node(n, ctx: Ctx) -> str:
    if isinstance(n, Text):
        return MAGIC_RE.sub("", str(n))
    if isinstance(n, Comment):
        return ""
    if isinstance(n, HTMLEntity):
        return n.normalize()
    if isinstance(n, Heading):
        if ctx.depth == 0:
            ctx.seen_heading = True
        return "\n\n" + "#" * min(n.level, 6) + " " + clean_ws(render(n.title, ctx)) + "\n"
    if isinstance(n, Wikilink):
        target = str(n.title).strip()
        colon = target.startswith(":")
        target = target.lstrip(":")
        prefix = target.split(":", 1)[0].strip().lower() if ":" in target else ""
        if prefix in ctx.ns.category and not colon:
            ctx.categories.append(target.split(":", 1)[1].split("|")[0].strip())
            return ""
        if prefix in ctx.ns.file and not colon:
            ctx.images.append(target.split(":", 1)[1].strip())
            return ""
        page = target.split("#")[0].strip()
        if page:
            ctx.links.append(page[:1].upper() + page[1:])
        return render(n.text, ctx) if n.text else target
    if isinstance(n, ExternalLink):
        return render(n.title, ctx) if n.title else ""
    if isinstance(n, Template):
        return render_template(n, ctx)
    if isinstance(n, Argument):
        return render(n.default, ctx) if n.default else ""
    if isinstance(n, Tag):
        return render_tag(n, ctx)
    return str(n)


def template_fields(tpl, ctx: Ctx, name: str = "", idx: int | None = None) -> tuple[dict, list]:
    named, positional = {}, []
    ctx.depth += 1
    try:
        for n, p in enumerate(tpl.params, 1):
            key = clean_ws(str(p.name)).strip() if p.showkey else str(n)
            ctx.parents.append((name, idx, key))
            try:
                val = clean_ws(render(p.value, ctx))
            finally:
                ctx.parents.pop()
            if p.showkey:
                if key:
                    named[key] = val
            elif val:
                positional.append(val)
    finally:
        ctx.depth -= 1
    return named, positional


def render_template(tpl, ctx: Ctx) -> str:
    name = template_name(tpl, ctx.ns)
    if not name or name.startswith("#"):
        return ""
    if name.upper() in ("PAGENAME", "FULLPAGENAME", "BASEPAGENAME"):
        return ctx.title
    if SKIP_TEMPLATE.search(name):
        return ""
    idx = ctx.next_idx
    ctx.next_idx += 1
    named, positional = template_fields(tpl, ctx, name, idx)
    is_box = ctx.depth == 0 and named and (INFOBOX_HINT.search(name) or (not ctx.seen_heading and len(named) >= 4))
    if is_box:
        ctx.infoboxes.append({"template": name, "fields": named, "idx": idx})
        return ""
    if len(named) >= 2 and ctx.depth == 0:
        ctx.templates.append({"template": name, "fields": named, "positional": positional, "idx": idx})
        lines = [f"\n**{name}**"] + [f"- {k}: {v}" for k, v in named.items() if v] + [f"- {v}" for v in positional]
        return "\n".join(lines) + "\n"
    if len(named) >= 2 and ctx.parents:
        parent, parent_idx, param = ctx.parents[-1]
        ctx.nested.append({"template": name, "fields": named, "positional": positional, "idx": idx,
                           "parent_template": parent, "parent_idx": parent_idx, "parent_field": param})
    vals = positional + [f"{k}={v}" for k, v in named.items() if v]
    if not vals:
        return ""
    return f"[{name}: {', '.join(vals)}]"


def md_cell(s: str) -> str:
    return clean_ws(s).replace("|", "\\|")


def render_table(n, ctx: Ctx) -> str:
    rows, pending, caption = [], [], ""

    def cell(c):
        return md_cell(render(c.contents, ctx)) if c.contents else ""

    for node in n.contents.nodes:
        if not isinstance(node, Tag):
            continue
        t = str(node.tag).lower()
        if t == "tr":
            if pending:
                rows.append(pending)
                pending = []
            cells = [cell(c) for c in node.contents.nodes if isinstance(c, Tag) and str(c.tag).lower() in ("td", "th")]
            if cells:
                rows.append(cells)
        elif t in ("td", "th"):
            pending.append(cell(node))
        elif t == "caption":
            caption = md_cell(render(node.contents, ctx))
    if pending:
        rows.append(pending)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ([f"\n*{caption}*\n"] if caption else ["\n"])
    out.append("| " + " | ".join(rows[0]) + " |")
    out.append("|" + "---|" * width)
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out) + "\n\n"


def render_tag(n, ctx: Ctx) -> str:
    t = str(n.tag).lower().strip()
    markup = n.wiki_markup or ""
    if t in SKIP_TAGS:
        return ""
    if t == "br":
        return "\n"
    if t == "hr":
        return "\n---\n"
    if t == "table":
        return render_table(n, ctx)
    if t in LIST_TAGS and not markup:  # HTML <li>, <dd>, <dt>
        inner = render(n.contents, ctx).strip() if n.contents else ""
        return f"\n- {inner}" if t == "li" else f"\n{inner}"
    inner = render(n.contents, ctx) if n.contents else ""
    if t in ("b", "strong"):
        return f"**{inner.strip()}**" if inner.strip() else ""
    if t in ("i", "em"):
        return f"*{inner.strip()}*" if inner.strip() else ""
    if t == "tabber":  # Fandom tabs: "Tab A=content|-|Tab B=content"
        parts = re.split(r"\|-\|", inner)
        out = []
        for p in parts:
            if "=" in p:
                label, body = p.split("=", 1)
                out.append(f"\n**{label.strip()}**\n{body.strip()}")
            else:
                out.append(p)
        return "\n".join(out) + "\n"
    return inner


def parse_wikitext(wikitext: str, title: str, ns: Namespaces | None = None) -> dict:
    ctx = Ctx(title=title, ns=ns or Namespaces())
    body = render(mwp.parse(wikitext or ""), ctx)
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    sections, cur = [], {"title": "Intro", "level": 1, "text": []}
    for line in body.split("\n"):
        m = re.match(r"^(#{1,6}) (.*)$", line)
        if m:
            sections.append(cur)
            cur = {"title": m.group(2).strip(), "level": len(m.group(1)), "text": []}
        else:
            cur["text"].append(line)
    sections.append(cur)
    sections = [{**s, "text": "\n".join(s["text"]).strip()} for s in sections]
    sections = [s for s in sections if s["text"] or s["title"] != "Intro"]
    lead = next((s["text"] for s in sections if s["title"] == "Intro"), "")
    summary = clean_ws(re.split(r"\n\s*\n", lead)[0]) if lead else ""
    redirect = None
    m = re.match(r"\s*#redirect\s*\[\[([^\]|#]+)", wikitext or "", re.I)
    if m:
        redirect = m.group(1).strip()
    return {
        "title": title,
        "redirect": redirect,
        "summary": re.sub(r"[*\[\]]", "", summary)[:400],
        "infoboxes": ctx.infoboxes,
        "templates": ctx.templates,
        "nested": ctx.nested,
        "sections": sections,
        "markdown": body,
        "categories": list(dict.fromkeys(ctx.categories)),
        "links": list(dict.fromkeys(ctx.links)),
        "images": list(dict.fromkeys(ctx.images)),
    }


def page_markdown(doc: dict, url: str, license_name: str | None) -> str:
    fm = {"title": doc["title"], "source": url, "categories": doc["categories"],
          "fetched": doc.get("fetched"), "license": license_name or "see source wiki"}
    out = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()] + ["---", "", f"# {doc['title']}", ""]
    for box in doc["infoboxes"]:
        rows = [(k, v) for k, v in box["fields"].items() if v]
        if rows:
            out += [f"*{box['template']}*", "", "| Field | Value |", "|---|---|"]
            out += [f"| {md_cell(k)} | {md_cell(v)} |" for k, v in rows] + [""]
    out.append(doc["markdown"])
    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Profiles: per-wiki normalisation of infobox fields into typed columns
# ---------------------------------------------------------------------------

NUM_RE = re.compile(r"^[^\d\-+.]*([-+]?\d[\d,  ]*(?:\.\d+)?)\s*([kKmM]?)\b")


def parse_number(v):
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    m = NUM_RE.match(s)
    if not m:
        return None
    raw = m.group(1).replace(" ", "").replace(" ", "")
    if re.match(r"^\d{1,3}(,\d{3})+(\.\d+)?$", raw):
        raw = raw.replace(",", "")
    elif "," in raw and "." not in raw:
        raw = raw.replace(",", ".")
    try:
        num = float(raw)
    except ValueError:
        return None
    num *= {"k": 1e3, "m": 1e6}.get(m.group(2).lower(), 1)
    return int(num) if num.is_integer() else num


def sql_ident(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_") or "x"
    return ("t_" + s) if s[0].isdigit() else s


def load_profile(slug: str, kb_dir: Path | None = None) -> dict:
    for d in ([kb_dir] if kb_dir else []) + [PROFILES_DIR]:
        for ext in ("yaml", "yml", "json"):
            p = d / (f"profile.{ext}" if d == kb_dir else f"{slug}.{ext}")
            if p.exists():
                text = p.read_text(encoding="utf-8")
                if ext == "json":
                    return json.loads(text)
                if yaml is None:
                    sys.exit(f"pip install pyyaml to read {p}")
                return yaml.safe_load(text) or {}
    return {}


def normalise_fields(fields: dict, tpl_profile: dict) -> dict:
    """Apply a template profile: rename, drop, type, split per-rank values."""
    spec = tpl_profile.get("fields", {}) or {}
    drop = set(tpl_profile.get("drop", []) or [])
    out = {}
    for k, v in fields.items():
        if k in drop:
            continue
        f = spec.get(k, {}) or {}
        col = sql_ident(f.get("rename", k))
        typ = f.get("type", "auto")
        if f.get("split"):
            parts = [p.strip() for p in re.split(re.escape(f["split"]), v) if p.strip()]
            for i, p in enumerate(parts, 1):
                out[f"{col}_{i}"] = coerce(p, typ)
            continue
        out[col] = coerce(v, typ)
    return out


def coerce(v, typ):
    if typ in ("int", "number", "float"):
        n = parse_number(v)
        return int(n) if (typ == "int" and n is not None) else n
    if typ == "list":
        return json.dumps([x.strip() for x in re.split(r"[,;/]|\n", v) if x.strip()], ensure_ascii=False)
    if typ == "auto" and looks_numeric(v):
        return parse_number(v)
    return v


def looks_numeric(v) -> bool:
    """'1,200', '2.5k', '15%', '1,200 Gold' → True; '12-18', 'Level 5', '3x3' → False."""
    return bool(re.fullmatch(r"[-+]?\d[\d,.  ]*\s*[kKmM%]?(\s+[^\W\d_][\w ]{0,15})?", str(v).strip()))


# ---------------------------------------------------------------------------
# Knowledge base on disk
# ---------------------------------------------------------------------------

class KB:
    def __init__(self, root: Path, slug: str):
        self.slug = slug
        self.dir = root / slug
        self.raw = self.dir / "raw"
        self.pages = self.dir / "pages"
        self.index: dict[str, dict] = {}
        self.aliases: dict[str, str] = {}
        self.meta: dict = {}
        if (self.dir / "index.jsonl").exists():
            for line in (self.dir / "index.jsonl").read_text(encoding="utf-8").splitlines():
                if line.strip():
                    e = json.loads(line)
                    self.index[e["title"]] = e
        if (self.dir / "aliases.json").exists():
            self.aliases = json.loads((self.dir / "aliases.json").read_text(encoding="utf-8"))
        if (self.dir / "meta.json").exists():
            self.meta = json.loads((self.dir / "meta.json").read_text(encoding="utf-8"))
        self._slugs = {e["slug"].lower(): t for t, e in self.index.items()}

    def exists(self):
        return (self.dir / "meta.json").exists()

    def ensure_dirs(self):
        for d in (self.raw, self.pages):
            d.mkdir(parents=True, exist_ok=True)

    def slug_for(self, title: str) -> str:
        if title in self.index:
            return self.index[title]["slug"]
        s = unicodedata.normalize("NFKC", title)
        s = re.sub(r"[^\w\-. ]+", "_", s, flags=re.UNICODE).strip().replace(" ", "_")[:120] or "page"
        owner = self._slugs.get(s.lower())
        if owner and owner != title:
            s = f"{s}-{hashlib.sha1(title.encode()).hexdigest()[:6]}"
        self._slugs[s.lower()] = title
        return s

    def save_page(self, title, pageid, revid, timestamp, wikitext, wiki: Wiki | None, ns: Namespaces,
                  categories: list | None = None):
        """`categories`: the API's list, which includes categories added by templates (wikitext alone misses them)."""
        slug = self.slug_for(title)
        doc = parse_wikitext(wikitext, title, ns)
        if categories:
            doc["categories"] = list(dict.fromkeys(doc["categories"] + categories))
        url = wiki.page_url(title) if wiki else self.meta.get("base", "") + "/wiki/" + quote(title.replace(" ", "_"))
        doc.update(pageid=pageid, revid=revid, timestamp=timestamp, url=url, fetched=now_iso())
        (self.raw / f"{slug}.wiki").write_text(wikitext or "", encoding="utf-8")
        md = page_markdown(doc, url, (self.meta.get("license") or {}).get("text"))
        (self.pages / f"{slug}.md").write_text(md, encoding="utf-8")
        doc.pop("markdown")
        (self.pages / f"{slug}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        self.index[title] = {
            "title": title, "slug": slug, "pageid": pageid, "revid": revid, "timestamp": timestamp, "url": url,
            "categories": doc["categories"], "infobox": doc["infoboxes"][0]["template"] if doc["infoboxes"] else None,
            "summary": doc["summary"],
        }

    def remove(self, title):
        e = self.index.pop(title, None)
        if e:
            for p in (self.raw / f"{e['slug']}.wiki", self.pages / f"{e['slug']}.md", self.pages / f"{e['slug']}.json"):
                p.unlink(missing_ok=True)

    def flush(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        rev_alias: dict[str, list] = {}
        for a, t in self.aliases.items():
            rev_alias.setdefault(t, []).append(a)
        with open(self.dir / "index.jsonl", "w", encoding="utf-8") as f:
            for t in sorted(self.index):
                e = {**self.index[t], "aliases": sorted(rev_alias.get(t, []))}
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        (self.dir / "aliases.json").write_text(json.dumps(self.aliases, ensure_ascii=False, indent=1), encoding="utf-8")
        (self.dir / "meta.json").write_text(json.dumps(self.meta, ensure_ascii=False, indent=1), encoding="utf-8")

    def find(self, query: str) -> dict | None:
        q = query.strip().replace("_", " ")
        if q in self.index:
            return self.index[q]
        if q in self.aliases and self.aliases[q] in self.index:
            return self.index[self.aliases[q]]
        ql = q.lower()
        for t, e in self.index.items():
            if t.lower() == ql or e["slug"].lower() == ql.replace(" ", "_"):
                return e
        for a, t in self.aliases.items():
            if a.lower() == ql and t in self.index:
                return self.index[t]
        return None

    def load_doc(self, entry: dict) -> dict:
        return json.loads((self.pages / f"{entry['slug']}.json").read_text(encoding="utf-8"))

    # -- SQLite ------------------------------------------------------------
    def build_db(self, profile: dict | None = None) -> dict:
        profile = profile if profile is not None else load_profile(self.slug, self.dir)
        tpl_profiles = profile.get("templates", {}) or {}
        db_path = self.dir / "kb.sqlite"
        tmp = db_path.with_suffix(".tmp")
        tmp.unlink(missing_ok=True)
        con = sqlite3.connect(tmp)
        con.executescript("""
            CREATE TABLE pages(title TEXT PRIMARY KEY, slug TEXT, url TEXT, summary TEXT, infobox TEXT,
                               categories TEXT, revid INTEGER, timestamp TEXT);
            CREATE TABLE categories(title TEXT, category TEXT);
            CREATE TABLE links(src TEXT, dst TEXT);
            CREATE TABLE aliases(alias TEXT PRIMARY KEY, title TEXT);
            CREATE TABLE template_tables(template TEXT PRIMARY KEY, table_name TEXT, rows INTEGER, columns TEXT);
            CREATE TABLE template_values(title TEXT, url TEXT, template TEXT, idx INTEGER, parent_template TEXT,
                                         parent_idx INTEGER, field TEXT, value TEXT, num REAL);
            CREATE VIRTUAL TABLE pages_fts USING fts5(title, body, tokenize='unicode61 remove_diacritics 2');
        """)
        rows_by_tpl: dict[str, list] = {}
        pages_by_tpl: dict[str, set] = {}
        infobox_names: set = set()
        for t, e in self.index.items():
            md_path = self.pages / f"{e['slug']}.md"
            body = md_path.read_text(encoding="utf-8").split("\n---\n", 1)[-1] if md_path.exists() else ""
            con.execute("INSERT INTO pages VALUES(?,?,?,?,?,?,?,?)",
                        (t, e["slug"], e["url"], e.get("summary"), e.get("infobox"),
                         json.dumps(e.get("categories", []), ensure_ascii=False), e.get("revid"), e.get("timestamp")))
            con.execute("INSERT INTO pages_fts(title, body) VALUES(?,?)", (t, body))
            con.executemany("INSERT INTO categories VALUES(?,?)", [(t, c) for c in e.get("categories", [])])
            try:
                doc = self.load_doc(e)
            except FileNotFoundError:
                continue
            con.executemany("INSERT INTO links VALUES(?,?)", [(t, l) for l in doc.get("links", [])])
            infobox_names.update(tpl["template"] for tpl in doc.get("infoboxes", []))
            for n, tpl in enumerate(doc.get("infoboxes", []) + doc.get("templates", []) + doc.get("nested", [])):
                name = tpl["template"]
                idx = tpl.get("idx", n)
                parent = (tpl.get("parent_template"), tpl.get("parent_idx"), tpl.get("parent_field"))
                con.executemany("INSERT INTO template_values VALUES(?,?,?,?,?,?,?,?,?)",
                                [(t, e["url"], name, idx, parent[0], parent[1], k, v,
                                  parse_number(v) if looks_numeric(v) else None) for k, v in tpl["fields"].items()])
                pages_by_tpl.setdefault(name, set()).add(t)
                fields = normalise_fields(tpl["fields"], tpl_profiles.get(name) or {})
                rows_by_tpl.setdefault(name, []).append((t, e["url"], idx, parent, fields))
        con.execute("CREATE INDEX template_values_tpl ON template_values(template, field)")
        con.executemany("INSERT OR IGNORE INTO aliases VALUES(?,?)", list(self.aliases.items()))
        summary = {}
        used_names = {"pages", "categories", "links", "aliases", "template_tables", "template_values", "pages_fts"}
        for name, rows in rows_by_tpl.items():
            # infoboxes always get a table; other data templates when a profile lists them or they recur across pages
            if name not in infobox_names and name not in tpl_profiles and len(pages_by_tpl[name]) < AUTO_TABLE_MIN_PAGES:
                continue
            tp = tpl_profiles.get(name, {}) or {}
            table = sql_ident(tp.get("table") or name)
            while table in used_names:
                table += "_t"
            used_names.add(table)
            nested = any(parent[0] is not None for *_, parent, _ in rows)
            fixed = ["title", "url", "idx"] + (["parent_template", "parent_idx", "parent_field"] if nested else [])
            cols: list[str] = []
            for *_, f in rows:
                for c in f:
                    if c not in cols and c not in fixed:
                        cols.append(c)
            types = {}
            for c in cols:
                vals = [f[c] for *_, f in rows if f.get(c) not in (None, "")]
                types[c] = "REAL" if vals and all(isinstance(v, (int, float)) for v in vals) else "TEXT"
            fixed_sql = "title TEXT, url TEXT, idx INTEGER" + (
                ", parent_template TEXT, parent_idx INTEGER, parent_field TEXT" if nested else "")
            con.execute(f'CREATE TABLE "{table}"({fixed_sql}' + "".join(f', "{c}" {types[c]}' for c in cols) + ")")
            con.executemany(f'INSERT INTO "{table}" VALUES(' + ",".join("?" * (len(cols) + len(fixed))) + ")",
                            [(t, u, idx, *(parent if nested else ()),
                              *[f.get(c) if f.get(c) != "" else None for c in cols]) for t, u, idx, parent, f in rows])
            con.execute("INSERT INTO template_tables VALUES(?,?,?,?)",
                        (name, table, len(rows), json.dumps({c: types[c] for c in cols})))
            summary[name] = {"table": table, "rows": len(rows), "columns": len(cols)}
        con.commit()
        con.close()
        tmp.replace(db_path)
        return summary


# ---------------------------------------------------------------------------
# Sync from the live API
# ---------------------------------------------------------------------------

def siteinfo(client) -> dict:
    d = client.get(action="query", meta="siteinfo", siprop="general|statistics|rightsinfo|namespaces|namespacealiases")["query"]
    g, ns = d.get("general", {}), Namespaces()
    names = {6: set(), 10: set(), 14: set()}
    for n in (d.get("namespaces") or {}).values():
        if n.get("id") in names:
            names[n["id"]] |= {n.get("name", ""), n.get("canonical", "")}
    for a in d.get("namespacealiases", []) or []:
        if a.get("id") in names:
            names[a["id"]].add(a.get("alias", ""))
    ns = Namespaces(names[14] | DEFAULT_NS["category"], names[6] | DEFAULT_NS["file"], names[10] | DEFAULT_NS["template"])
    return {
        "sitename": g.get("sitename"), "lang": g.get("lang"), "generator": g.get("generator"),
        "mainpage": g.get("mainpage"), "articles": (d.get("statistics") or {}).get("articles"),
        "license": {"text": (d.get("rightsinfo") or {}).get("text"), "url": (d.get("rightsinfo") or {}).get("url")},
        "namespaces": ns.to_meta(),
    }


def list_remote(client, scope: dict, wiki: Wiki) -> tuple[dict, dict]:
    """Return ({title: (pageid, lastrevid)}, {redirect_from: to}) for the requested scope."""
    remote, redirects = {}, {}

    def absorb(data):
        q = data.get("query", {})
        for r in q.get("redirects", []) or []:
            redirects[r["from"]] = r["to"]
        for p in q.get("pages", []) or []:
            if p.get("missing") or p.get("invalid"):
                log(f"  ! missing page: {p.get('title')}")
                continue
            if p.get("ns", 0) == 0 or scope.get("pages"):
                remote[p["title"]] = (p.get("pageid"), p.get("lastrevid"))

    if scope.get("pages"):
        titles = scope["pages"]
        for i in range(0, len(titles), 50):
            absorb(client.get(action="query", titles="|".join(titles[i:i + 50]), prop="info", redirects=1))
    elif scope.get("categories"):
        for cat in scope["categories"]:
            cat = cat if ":" in cat else f"Category:{cat}"
            for data in client.query_all(generator="categorymembers", gcmtitle=cat, gcmnamespace=0, gcmlimit=500, prop="info"):
                absorb(data)
    else:
        for data in client.query_all(generator="allpages", gapnamespace=0, gapfilterredir="nonredirects", gaplimit=500, prop="info"):
            absorb(data)
            if scope.get("limit") and len(remote) >= scope["limit"]:
                break
        if not scope.get("limit"):
            for data in client.query_all(generator="allpages", gapnamespace=0, gapfilterredir="redirects", gaplimit=500, redirects=1):
                for r in data.get("query", {}).get("redirects", []) or []:
                    redirects[r["from"]] = r["to"]
    if scope.get("limit"):
        remote = dict(list(remote.items())[: scope["limit"]])
    return remote, redirects


def sync(kb: KB, client, wiki: Wiki, scope: dict, yes: bool = False, force: bool = False) -> dict:
    kb.ensure_dirs()
    if not kb.meta.get("sitename") or force:
        kb.meta.update(siteinfo(client))
    kb.meta.update(slug=kb.slug, base=wiki.base, api=wiki.api, tool=f"fandom-kb {VERSION}")
    ns = Namespaces.from_meta(kb.meta)
    log(f"Listing pages on {wiki.base} …")
    remote, redirects = list_remote(client, scope, wiki)
    full_scope = not scope.get("pages") and not scope.get("categories") and not scope.get("limit")
    todo = [t for t, (_, rev) in remote.items() if force or kb.index.get(t, {}).get("revid") != rev]
    deleted = [t for t in kb.index if t not in remote] if full_scope else []
    log(f"  {len(remote)} pages in scope, {len(todo)} new/changed, {len(deleted)} deleted, {len(redirects)} redirects")
    if len(todo) > CONFIRM_THRESHOLD and not yes:
        raise SystemExit(f"{len(todo)} pages to download (~{len(todo) // 50 + 1} requests). Re-run with --yes to confirm, "
                         f"or narrow with --category / --pages / --limit, or use `import` with an XML dump.")
    done = 0
    for i in range(0, len(todo), 50):
        batch = todo[i:i + 50]
        cont: dict = {}
        got: dict[str, dict] = {}  # title → {pageid, rev, categories}, merged across continuation responses
        while True:
            data = client.get(action="query", titles="|".join(batch), prop="revisions|categories",
                              rvprop="content|ids|timestamp", rvslots="main", clshow="!hidden", cllimit="max", **cont)
            for p in data.get("query", {}).get("pages", []) or []:
                g = got.setdefault(p["title"], {"pageid": p.get("pageid"), "rev": None, "categories": []})
                if p.get("revisions"):
                    g["rev"] = p["revisions"][0]
                g["categories"] += [c["title"].split(":", 1)[-1] for c in p.get("categories", []) or []]
            if "continue" in data:
                cont = data["continue"]
            else:
                break
        for title, g in got.items():
            rev = g["rev"]
            if not rev:
                continue
            text = (rev.get("slots", {}).get("main", {}) or {}).get("content", rev.get("content", ""))
            kb.save_page(title, g["pageid"], rev.get("revid"), rev.get("timestamp"), text, wiki, ns, g["categories"])
            done += 1
        log(f"  {done}/{len(todo)} saved")
        if done and done % 500 < 50:
            kb.flush()
    for t in deleted:
        kb.remove(t)
    if full_scope:
        kb.aliases = redirects
    else:
        kb.aliases.update(redirects)
    kb.meta["synced_at"] = now_iso()
    kb.meta["pages"] = len(kb.index)
    kb.flush()
    tables = kb.build_db()
    return {"pages": len(kb.index), "downloaded": done, "deleted": len(deleted), "tables": tables,
            "requests": getattr(client, "calls", None), "dir": str(kb.dir)}


# ---------------------------------------------------------------------------
# Import from an XML dump (Special:Export or the wiki's database dump)
# ---------------------------------------------------------------------------

def import_dump(kb: KB, path: Path, wiki: Wiki | None, all_ns: bool = False) -> dict:
    opener = gzip.open if path.suffix == ".gz" else open
    if path.suffix in (".7z", ".bz2", ".zip"):
        raise SystemExit(f"Extract {path.name} first (e.g. `7z x {path.name}`), then import the .xml file.")
    kb.ensure_dirs()
    tagname = lambda el: el.tag.rsplit("}", 1)[-1]
    nsnames = {6: set(), 10: set(), 14: set()}
    count, redirects = 0, {}
    ns = Namespaces.from_meta(kb.meta)
    with opener(path, "rb") as f:
        for ev, el in ET.iterparse(f, events=("end",)):
            t = tagname(el)
            if t == "siteinfo":
                info = {tagname(c): (c.text or "") for c in el}
                for n in el.iter():
                    if tagname(n) == "namespace" and n.get("key") and int(n.get("key")) in nsnames:
                        nsnames[int(n.get("key"))].add(n.text or "")
                base_url = info.get("base", "")
                if wiki is None and base_url:
                    wiki = resolve(base_url)
                kb.meta.update(sitename=info.get("sitename"), generator=info.get("generator"))
                ns = Namespaces(nsnames[14] | DEFAULT_NS["category"], nsnames[6] | DEFAULT_NS["file"], nsnames[10] | DEFAULT_NS["template"])
                kb.meta["namespaces"] = ns.to_meta()
                el.clear()
            elif t == "page":
                title = pns = pid = None
                redirect, rev = None, None
                for c in el:
                    ct = tagname(c)
                    if ct == "title":
                        title = c.text
                    elif ct == "ns":
                        pns = int(c.text or 0)
                    elif ct == "id":
                        pid = int(c.text or 0)
                    elif ct == "redirect":
                        redirect = c.get("title")
                    elif ct == "revision":
                        rev = c
                if title and (pns == 0 or all_ns):
                    if redirect:
                        redirects[title] = redirect
                    elif rev is not None:
                        r = {tagname(c): c for c in rev}
                        text = r["text"].text if "text" in r else ""
                        kb.save_page(title, pid, int(r["id"].text) if "id" in r else None,
                                     r["timestamp"].text if "timestamp" in r else None, text or "", wiki, ns)
                        count += 1
                        if count % 500 == 0:
                            log(f"  {count} pages imported")
                el.clear()
    if wiki:
        kb.meta.update(slug=kb.slug, base=wiki.base, api=wiki.api)
    kb.aliases.update(redirects)
    kb.meta.update(synced_at=now_iso(), pages=len(kb.index), source=f"dump:{path.name}", tool=f"fandom-kb {VERSION}")
    kb.flush()
    tables = kb.build_db()
    return {"pages": len(kb.index), "imported": count, "redirects": len(redirects), "tables": tables, "dir": str(kb.dir)}


# ---------------------------------------------------------------------------
# Query commands
# ---------------------------------------------------------------------------

def open_kb(root: Path, name: str) -> KB:
    kb = KB(root, name)
    if not kb.exists():
        kb2 = KB(root, resolve(name).slug)
        if kb2.exists():
            return kb2
        avail = ", ".join(sorted(p.name for p in root.glob("*") if (p / "meta.json").exists())) or "none"
        raise SystemExit(f"No knowledge base '{name}' in {root}. Available: {avail}. Create it with `fetch {name}`.")
    return kb


def fts_query(q: str) -> str:
    terms = re.findall(r"\w+", q, re.UNICODE)
    return " ".join(f'"{t}"*' if len(t) > 2 else f'"{t}"' for t in terms)


def search(kb: KB, query: str, limit: int = 10) -> list[dict]:
    db = kb.dir / "kb.sqlite"
    results: dict[str, dict] = {}
    exact = kb.find(query)
    if exact:
        results[exact["title"]] = {"title": exact["title"], "url": exact["url"], "score": 1000.0,
                                   "snippet": exact.get("summary", ""), "match": "title"}
    if db.exists() and fts_query(query):
        con = sqlite3.connect(db)
        try:
            rows = con.execute(
                "SELECT title, snippet(pages_fts, 1, '«', '»', ' … ', 24), bm25(pages_fts, 10.0, 1.0) "
                "FROM pages_fts WHERE pages_fts MATCH ? ORDER BY 3 LIMIT ?", (fts_query(query), limit * 2)).fetchall()
        except sqlite3.OperationalError:
            rows = []
        for t, snip, score in rows:
            if t not in results:
                results[t] = {"title": t, "url": kb.index.get(t, {}).get("url"), "score": round(-score, 3),
                              "snippet": clean_ws(snip), "match": "fts"}
        con.close()
    else:  # fallback: substring scan
        terms = [w.lower() for w in re.findall(r"\w+", query)]
        for t, e in kb.index.items():
            text = (kb.pages / f"{e['slug']}.md").read_text(encoding="utf-8").lower()
            if all(w in text for w in terms):
                score = sum(text.count(w) for w in terms) + 20 * sum(w in t.lower() for w in terms)
                results.setdefault(t, {"title": t, "url": e["url"], "score": float(score), "snippet": e.get("summary", ""), "match": "scan"})
    return sorted(results.values(), key=lambda r: -r["score"])[:limit]


def run_sql(kb: KB, query: str, limit: int = 200) -> tuple[list, list]:
    db = kb.dir / "kb.sqlite"
    if not db.exists():
        kb.build_db()
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cur = con.execute(query)
    cols = [d[0] for d in cur.description or []]
    rows = cur.fetchmany(limit)
    con.close()
    return cols, rows


def schema(kb: KB) -> dict:
    stats: dict[str, dict] = {}
    for e in kb.index.values():
        try:
            doc = kb.load_doc(e)
        except FileNotFoundError:
            continue
        seen: set = set()
        for kind, label in (("infoboxes", "infobox"), ("templates", "template"), ("nested", "nested")):
            for tpl in doc.get(kind, []):
                s = stats.setdefault(tpl["template"], {"kind": label, "pages": 0, "fields": {}, "examples": {}, "samples": {}})
                if tpl["template"] not in seen:
                    s["pages"] += 1
                    seen.add(tpl["template"])
                for k, v in tpl["fields"].items():
                    s["fields"][k] = s["fields"].get(k, 0) + 1
                    if v and k not in s["examples"]:
                        s["examples"][k] = v[:60]
                    if v and len(s["samples"].setdefault(k, [])) < 50:
                        s["samples"][k].append(v)
    return dict(sorted(stats.items(), key=lambda kv: -kv[1]["pages"]))


def plural(word: str) -> str:
    if word.endswith("s"):
        return word
    if word.endswith(("x", "ch", "sh", "z")):
        return word + "es"
    if re.search(r"[^aeiou]y$", word):
        return word[:-1] + "ies"
    return word + "s"


def rank_separator(samples: list) -> str | None:
    """Return the separator of per-rank values ('70; 85; 105') if most samples are such lists of numbers."""
    for sep in RANK_SEPARATORS:
        hits = 0
        for v in samples:
            parts = [x.strip() for x in v.split(sep)]
            if len(parts) >= 2 and all(looks_numeric(x) for x in parts):
                hits += 1
        if samples and hits >= 0.8 * len(samples):
            return sep
    return None


def column_values(kb: KB, max_distinct: int = 15, top: int = 6, max_len: int = 40) -> dict:
    """Most common values of the low-cardinality TEXT columns of each template table: {table: {column: [(value, n)]}}.

    These are the values to use verbatim in WHERE clauses (a wiki may say 'Soldier' where you'd guess 'Infantry').
    Skipped: numeric columns, long text, and columns whose values are all different (names, ids)."""
    out: dict[str, dict] = {}
    db = kb.dir / "kb.sqlite"
    if not db.exists():
        return out
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        for table, columns in con.execute("SELECT table_name, columns FROM template_tables").fetchall():
            for col, typ in json.loads(columns).items():
                if typ != "TEXT":
                    continue
                q = f'SELECT COUNT(*), COUNT(DISTINCT "{col}"), AVG(LENGTH("{col}")) FROM "{table}" WHERE "{col}" IS NOT NULL'
                n, distinct, avg_len = con.execute(q).fetchone()
                if not distinct or distinct > max_distinct or (avg_len or 0) > max_len or (distinct == n and n > 2):
                    continue
                rows = con.execute(f'SELECT "{col}", COUNT(*) AS c FROM "{table}" WHERE "{col}" IS NOT NULL '
                                   f'GROUP BY 1 ORDER BY c DESC, 1 LIMIT ?', (top + 1,)).fetchall()
                out.setdefault(table, {})[col] = [tuple(r) for r in rows]
    finally:
        con.close()
    return out


def profile_init(kb: KB, min_pages: int = 3) -> str:
    sc = schema(kb)
    out = {"wiki": kb.slug, "sitename": kb.meta.get("sitename"),
           "notes": "Auto-generated draft. Rename tables/fields, set types, add `split: '/'` for per-rank stats, drop noise.",
           "templates": {}}
    for name, s in sc.items():
        if s["pages"] < min_pages:
            continue
        fields = {}
        for k, n in sorted(s["fields"].items(), key=lambda kv: -kv[1]):
            ex = s["examples"].get(k, "")
            spec = {"type": "number" if looks_numeric(ex) else "text", "example": ex}
            sep = rank_separator(s["samples"].get(k, []))
            if sep:
                spec.update(type="number", split=sep)
            fields[k] = spec
        drop = [k for k in fields if re.search(r"image|caption|imagewidth|icon|^img", k, re.I)]
        out["templates"][name] = {"table": plural(sql_ident(re.sub(r"(?i)infobox|template", "", name).strip() or name)),
                                  "pages": s["pages"], "drop": drop, "fields": fields}
    if yaml:
        return yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=120)
    return json.dumps(out, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def print_table(cols, rows, fmt="table"):
    if fmt == "json":
        print(json.dumps([dict(zip(cols, r)) for r in rows], ensure_ascii=False, indent=1))
        return
    if fmt == "csv":
        w = csv.writer(sys.stdout)
        w.writerow(cols)
        w.writerows(rows)
        return
    widths = [min(max([len(str(c))] + [len(str(r[i])) for r in rows]), 40) for i, c in enumerate(cols)]
    fmt_row = lambda r: " | ".join(str(v if v is not None else "")[:40].ljust(widths[i]) for i, v in enumerate(r))
    print(fmt_row(cols))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(fmt_row(r))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="fandom_kb", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help=f"KB root dir (default {DEFAULT_ROOT}, env FANDOM_KB_DIR)")
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fetch", help="create or update a KB from the live API (incremental)")
    p.add_argument("wiki", help="fandom name, wiki URL or page URL")
    p.add_argument("--lang"); p.add_argument("--api", help="explicit api.php URL (non-Fandom MediaWiki)")
    p.add_argument("--category", action="append", help="only pages in this category (repeatable)")
    p.add_argument("--pages", help="comma-separated page titles")
    p.add_argument("--limit", type=int, help="at most N pages (testing)")
    p.add_argument("--delay", type=float, default=1.0, help="seconds between requests (default 1.0)")
    p.add_argument("--yes", action="store_true", help=f"confirm downloads above {CONFIRM_THRESHOLD} pages")
    p.add_argument("--force", action="store_true", help="re-download everything")

    p = sub.add_parser("import", help="build a KB from a MediaWiki XML dump (.xml or .xml.gz)")
    p.add_argument("dump", type=Path); p.add_argument("--name", help="KB name (default: from dump siteinfo)")
    p.add_argument("--all-namespaces", action="store_true")

    sub.add_parser("list", help="list local knowledge bases")

    p = sub.add_parser("search", help="full-text search (FTS5, BM25)")
    p.add_argument("wiki"); p.add_argument("query"); p.add_argument("-n", type=int, default=10)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("show", help="print a page (Markdown or JSON)")
    p.add_argument("wiki"); p.add_argument("title"); p.add_argument("--json", action="store_true")
    p.add_argument("--section", help="only this section title")

    p = sub.add_parser("sql", help="read-only SQL over kb.sqlite")
    p.add_argument("wiki"); p.add_argument("query"); p.add_argument("--format", choices=["table", "json", "csv"], default="table")
    p.add_argument("--limit", type=int, default=200)

    p = sub.add_parser("schema", help="infobox/data templates and their fields; SQL tables")
    p.add_argument("wiki"); p.add_argument("--json", action="store_true")

    p = sub.add_parser("export", help="infobox template → CSV/JSONL")
    p.add_argument("wiki"); p.add_argument("--template", required=True)
    p.add_argument("--format", choices=["csv", "jsonl"], default="csv"); p.add_argument("-o", type=Path)

    p = sub.add_parser("profile-init", help="draft a profile (YAML) from the KB's schema")
    p.add_argument("wiki"); p.add_argument("-o", type=Path, help="write to file (default: <kb>/profile.yaml)")
    p.add_argument("--min-pages", type=int, default=3)

    p = sub.add_parser("build-db", help="rebuild kb.sqlite (after editing a profile)")
    p.add_argument("wiki")

    a = ap.parse_args(argv)
    root: Path = a.root.expanduser()

    if a.cmd == "fetch":
        wiki = resolve(a.wiki, a.lang, a.api)
        scope = {"categories": a.category, "limit": a.limit,
                 "pages": [x.strip() for x in a.pages.split(",") if x.strip()] if a.pages else ([wiki.page] if wiki.page else None)}
        kb = KB(root, wiki.slug)
        res = sync(kb, Client(wiki.api, a.delay), wiki, scope, yes=a.yes, force=a.force)
        print(json.dumps(res, ensure_ascii=False, indent=1))
    elif a.cmd == "import":
        wiki = None
        name = a.name
        if not name:
            with (gzip.open if a.dump.suffix == ".gz" else open)(a.dump, "rb") as f:
                head = f.read(20000).decode("utf-8", "ignore")
            m = re.search(r"<base>([^<]+)</base>", head)
            if not m:
                raise SystemExit("Could not detect the wiki from the dump; pass --name.")
            wiki = resolve(m.group(1))
            name = wiki.slug
        res = import_dump(KB(root, name), a.dump, wiki, a.all_namespaces)
        print(json.dumps(res, ensure_ascii=False, indent=1))
    elif a.cmd == "list":
        rows = []
        for d in sorted(root.glob("*")):
            if (d / "meta.json").exists():
                m = json.loads((d / "meta.json").read_text(encoding="utf-8"))
                rows.append((d.name, m.get("sitename"), m.get("pages"), m.get("synced_at"), m.get("base")))
        print_table(["kb", "sitename", "pages", "synced_at", "base"], rows) if rows else print(f"No knowledge bases in {root}")
    elif a.cmd == "search":
        kb = open_kb(root, a.wiki)
        res = search(kb, a.query, a.n)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            for r in res:
                print(f"{r['title']}  [{r['match']} {r['score']}]\n  {r['url']}\n  {r['snippet']}\n")
            if not res:
                print("No results.")
    elif a.cmd == "show":
        kb = open_kb(root, a.wiki)
        e = kb.find(a.title)
        if not e:
            hits = search(kb, a.title, 5)
            raise SystemExit(f"Page not found: {a.title}. Did you mean: " + ", ".join(h["title"] for h in hits))
        if a.json:
            print(json.dumps(kb.load_doc(e), ensure_ascii=False, indent=1))
        elif a.section:
            doc = kb.load_doc(e)
            s = [x for x in doc["sections"] if x["title"].lower() == a.section.lower()]
            print(f"# {doc['title']} — {a.section}\nSource: {doc['url']}\n\n" + (s[0]["text"] if s else "(section not found: " + ", ".join(x["title"] for x in doc["sections"]) + ")"))
        else:
            print((kb.pages / f"{e['slug']}.md").read_text(encoding="utf-8"))
    elif a.cmd == "sql":
        kb = open_kb(root, a.wiki)
        if not re.match(r"^\s*(select|with|pragma\s+table_info|explain)\b", a.query, re.I):
            raise SystemExit("Only SELECT / WITH / PRAGMA table_info queries are allowed.")
        cols, rows = run_sql(kb, a.query, a.limit)
        print_table(cols, rows, a.format)
    elif a.cmd == "schema":
        kb = open_kb(root, a.wiki)
        sc = schema(kb)
        for s_ in sc.values():
            s_.pop("samples", None)  # only used to draft profiles; too long for the output
        tables = run_sql(kb, "SELECT template, table_name, rows, columns FROM template_tables ORDER BY rows DESC", 1000)[1]
        values = column_values(kb)
        if a.json:
            print(json.dumps({"templates": sc, "sql_tables": [
                {**dict(zip(["template", "table", "rows"], t[:3])), "columns": json.loads(t[3]), "values": values.get(t[1], {})}
                for t in tables]}, ensure_ascii=False, indent=1))
        else:
            print(f"{kb.meta.get('sitename')} — {len(kb.index)} pages\n\nSQL tables (query with `sql`):")
            for t in tables:
                cols = json.loads(t[3])
                print(f"  {t[1]}  ({t[2]} rows, from {{{{{t[0]}}}}}): " + ", ".join(f"{c}:{ty[0]}" for c, ty in list(cols.items())[:25]))
                for c, vals in list(values.get(t[1], {}).items())[:8]:
                    shown = ", ".join(f"{v} ({n})" for v, n in vals[:6]) + (", …" if len(vals) > 6 else "")
                    print(f"      {c}: {shown}")
            print("  + pages, categories(title,category), links(src,dst), aliases(alias,title), pages_fts(title,body),\n"
                  "    template_values(title,template,idx,parent_template,parent_idx,field,value,num): every template field\n")
            print("Templates:")
            for name, s in list(sc.items())[:30]:
                top = sorted(s["fields"].items(), key=lambda kv: -kv[1])[:15]
                print(f"  {{{{{name}}}}} [{s['kind']}] on {s['pages']} pages: " + ", ".join(k for k, _ in top))
    elif a.cmd == "export":
        kb = open_kb(root, a.wiki)
        rows, cols = [], []
        for e in kb.index.values():
            doc = kb.load_doc(e)
            for tpl in doc.get("infoboxes", []) + doc.get("templates", []) + doc.get("nested", []):
                if tpl["template"].lower() == a.template.lower():
                    rows.append({"title": e["title"], "url": e["url"], **tpl["fields"]})
                    cols += [k for k in tpl["fields"] if k not in cols]
        out = open(a.o, "w", encoding="utf-8", newline="") if a.o else sys.stdout
        if a.format == "jsonl":
            for r in rows:
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
        else:
            w = csv.DictWriter(out, fieldnames=["title", "url"] + cols)
            w.writeheader()
            w.writerows(rows)
        if a.o:
            out.close()
            log(f"{len(rows)} rows → {a.o}")
    elif a.cmd == "profile-init":
        kb = open_kb(root, a.wiki)
        text = profile_init(kb, a.min_pages)
        target = a.o or (kb.dir / "profile.yaml")
        target.write_text(text, encoding="utf-8")
        log(f"Draft profile → {target}. Edit it, then run `build-db {kb.slug}`. Share it upstream in profiles/{kb.slug}.yaml!")
    elif a.cmd == "build-db":
        kb = open_kb(root, a.wiki)
        print(json.dumps(kb.build_db(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
