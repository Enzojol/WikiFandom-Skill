"""Synthetic pages in the style of a game wiki (made-up values, not real Battle Nations data)."""

PAGES = {
    "Heavy Gunner": """{{Infobox Unit
|name = Heavy Gunner
|image = HeavyGunner.png
|type = [[Infantry]]
|building = [[Barracks]]
|level = 12
|cost = 1,200 [[Gold]]
|hp = 40 / 46 / 52 / 58 / 64 / 70
|armor = 0
|defense = 10
|dodge = 5%
}}
The '''Heavy Gunner''' is a sturdy [[Infantry]] unit trained at the [[Barracks]].<ref>Patch notes</ref>
__NOTOC__
== Attacks ==
{| class="wikitable"
! Attack !! Damage !! Range
|-
| Machine Gun || 12-18 || 1-3
|-
| Suppressive Fire || 8-10 || 2-4
|}
<tabber>
Machine Gun=
{{WeaponBox
| slot    = primary
| ammo    = 4
| attack1 =
{{AttackBox
| name       = Burst
| damagetype = Piercing
| mindmg     = 12
| maxdmg     = 18
}}
| attack2 =
{{AttackBox
| name       = Suppressive Fire
| damagetype = Piercing
| mindmg     = 8
| maxdmg     = 10
| effects    = {{Stun|chance=25|duration=1}}
}}
}}
</tabber>
{{UnitRanks
| hp    = 40; 46; 52; 58; 64; 70
| armor = 0; 0; 5; 5; 10; 10
| sp2   = 1,500
}}

== Strategy ==
* Strong against [[Raider|raiders]].
** Keep him in the front row.
* Weak against [[Artillery]].

{{Navbox Units}}
[[Category:Units]]
[[Category:Infantry]]
[[File:HeavyGunner_full.png|thumb]]
""",
    "Raider": """{{Infobox Unit
|name = Raider
|type = Vehicle
|building = [[Vehicle Factory]]
|level = 8
|cost = 2.5k
|hp = 30/34/38/42/46/50
|armor = 20
|defense = 5
|dodge = 15%
}}
The '''Raider''' is a fast vehicle. See also [[Heavy Gunner]].
<tabber>
Rank 1=Unlocked at level 8.
|-|
Rank 6=Requires 3 [[Medals]].
</tabber>
== Stats ==
{{WeaponBox
| slot    = primary
| ammo    = 6
| attack1 = {{AttackBox|name=Ram|damagetype=Crushing|mindmg=20|maxdmg=24}}
}}
{{UnitRanks
| hp    = 30; 34; 38; 42; 46; 50
| armor = 20; 22; 24; 26; 28; 30
| sp2   = 2,000
}}
[[Category:Units]]
[[Category:Vehicles]]
""",
    "Barracks": """{{Infobox Building
|name = Barracks
|size = 3x3
|cost = 500
|population = 2
}}
The '''Barracks''' trains [[Heavy Gunner]]s and other infantry.
== Upgrades ==
{{Upgrade|level=1|cost=500|time=1h}}
{{Upgrade|level=2|cost=2,000|time=4h}}
[[Category:Buildings]]
""",
}
REDIRECTS = {"HG": "Heavy Gunner", "Raiders": "Raider"}
# Categories that only the API knows about (added by templates), and hidden maintenance ones
API_CATEGORIES = {"Raider": ["Fast units"], "Heavy Gunner": ["Tier 2"]}
HIDDEN_CATEGORIES = {"Heavy Gunner": ["Pages with broken file links"]}


class FakeClient:
    """Answers the handful of MediaWiki API calls fandom_kb makes."""

    def __init__(self, pages=None, redirects=None, pageprops=None):
        self.pages = dict(pages or PAGES)
        self.redirects = dict(REDIRECTS if redirects is None else redirects)
        self.pageprops = dict(pageprops or {})
        self.revs = {t: 100 + i for i, t in enumerate(sorted(self.pages))}
        self.calls = 0
        self.content_requests = 0

    def _page(self, t, i, content=False):
        p = {"pageid": i + 1, "ns": 0, "title": t, "lastrevid": self.revs[t]}
        if content:
            p["revisions"] = [{"revid": self.revs[t], "timestamp": "2026-01-01T00:00:00Z",
                               "slots": {"main": {"content": self.pages[t]}}}]
            if t in self.pageprops:
                import json
                p["pageprops"] = {"infoboxes": json.dumps(self.pageprops[t])}
        return p

    def _categories(self, t, hidden_ok):
        import re
        cats = re.findall(r"\[\[Category:([^\]|]+)", self.pages[t]) + API_CATEGORIES.get(t, [])
        if hidden_ok:
            cats += HIDDEN_CATEGORIES.get(t, [])
        return [{"ns": 14, "title": f"Category:{c}"} for c in cats]

    def get(self, **q):
        self.calls += 1
        if q.get("meta") == "siteinfo":
            return {"query": {"general": {"sitename": "Sample Wiki", "lang": "en", "generator": "MediaWiki 1.39"},
                              "statistics": {"articles": len(self.pages)},
                              "rightsinfo": {"text": "CC BY-SA", "url": "https://creativecommons.org/licenses/by-sa/3.0/"},
                              "namespaces": {"14": {"id": 14, "name": "Category", "canonical": "Category"}},
                              "namespacealiases": []}}
        titles = sorted(self.pages)
        if q.get("generator") == "allpages":
            if q.get("redirects") and q.get("gapfilterredir") != "nonredirects":
                # real MediaWiki (1.43) rejects this combination
                raise RuntimeError("API error: {'code': 'params', 'info': 'Use \"gapfilterredir=nonredirects\" "
                                   "instead of \"redirects\" when using \"allpages\" as a generator.'}")
            if q.get("gapfilterredir") == "redirects":
                return {"query": {"pages": [{"pageid": 900 + i, "ns": 0, "title": a, "redirect": True}
                                            for i, a in enumerate(self.redirects)]}}
            return {"query": {"pages": [self._page(t, i) for i, t in enumerate(titles)]}}
        if q.get("list") == "allpages" and q.get("apfilterredir") == "redirects":
            return {"query": {"allpages": [{"pageid": 900 + i, "ns": 0, "title": a} for i, a in enumerate(self.redirects)]}}
        if q.get("list") == "allredirects":
            return {"query": {"allredirects": [{"fromid": 900 + i, "ns": 0, "title": b}
                                               for i, b in enumerate(self.redirects.values())]}}
        if q.get("generator") == "categorymembers":
            cat = q["gcmtitle"].split(":", 1)[1]
            sel = [t for t in titles if f"[[Category:{cat}]]" in self.pages[t]]
            return {"query": {"pages": [self._page(t, titles.index(t)) for t in sel]}}
        if "titles" in q:
            req = q["titles"].split("|")
            redir = [{"from": t, "to": self.redirects[t]} for t in req if t in self.redirects]
            req = [self.redirects.get(t, t) for t in req]
            props = (q.get("prop") or "").split("|")
            content = "revisions" in props
            if content:
                self.content_requests += 1
            if content and "categories" in props and "clcontinue" in q:
                # continuation: like MediaWiki, the finished revisions module is not repeated
                hidden_ok = "!hidden" not in (q.get("clshow") or "")
                pages = [{"pageid": titles.index(t) + 1, "ns": 0, "title": t, "categories": self._categories(t, hidden_ok)}
                         for t in req if t in self.pages]
                return {"query": {"pages": pages}}
            pages = [self._page(t, titles.index(t), content) if t in self.pages else {"title": t, "missing": True} for t in req]
            out = {"query": {"pages": pages, "redirects": redir}}
            if content and "categories" in props:
                out["continue"] = {"clcontinue": "1|x", "continue": "||"}
            return out
        raise AssertionError(f"unexpected query {q}")

    def query_all(self, **q):
        yield self.get(action="query", **q)


def to_xml_dump():
    import html
    out = ['<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/" version="0.11">',
           "<siteinfo><sitename>Sample Wiki</sitename><base>https://samplewiki.fandom.com/wiki/Main_Page</base>",
           "<generator>MediaWiki 1.39</generator><namespaces><namespace key=\"14\">Category</namespace>"
           "<namespace key=\"6\">File</namespace></namespaces></siteinfo>"]
    for i, (t, text) in enumerate(sorted(PAGES.items())):
        out.append(f"<page><title>{html.escape(t)}</title><ns>0</ns><id>{i + 1}</id><revision><id>{100 + i}</id>"
                   f"<timestamp>2026-01-01T00:00:00Z</timestamp><text>{html.escape(text)}</text></revision></page>")
    for a, b in REDIRECTS.items():
        out.append(f'<page><title>{a}</title><ns>0</ns><id>99</id><redirect title="{b}" /><revision><id>1</id>'
                   f"<text>#REDIRECT [[{b}]]</text></revision></page>")
    out.append("</mediawiki>")
    return "\n".join(out)
