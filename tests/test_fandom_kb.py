"""Offline tests. Run: python -m pytest tests/  (or python tests/test_fandom_kb.py)"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "skills" / "fandom-kb" / "scripts"))
sys.path.insert(0, str(HERE / "fixtures"))

import fandom_kb as fk  # noqa: E402
from sample_wiki import PAGES, FakeClient, to_xml_dump  # noqa: E402


def test_resolve():
    w = fk.resolve("battlenations")
    assert (w.slug, w.api) == ("battlenations", "https://battlenations.fandom.com/api.php")
    w = fk.resolve("https://onepiece.fandom.com/fr/wiki/Monkey_D._Luffy")
    assert (w.slug, w.lang, w.page, w.api) == ("onepiece-fr", "fr", "Monkey D. Luffy", "https://onepiece.fandom.com/fr/api.php")
    w = fk.resolve("battlenations.fandom.com/wiki/Heavy_Gunner")
    assert w.slug == "battlenations" and w.page == "Heavy Gunner"
    assert fk.resolve("minecraft", lang="de").base == "https://minecraft.fandom.com/de"
    assert fk.resolve("https://terraria.wiki.gg/wiki/Zenith").slug == "terraria-wiki-gg"


def test_parse_page():
    doc = fk.parse_wikitext(PAGES["Heavy Gunner"], "Heavy Gunner")
    box = doc["infoboxes"][0]
    assert box["template"] == "Infobox Unit"
    assert box["fields"]["type"] == "Infantry" and box["fields"]["cost"] == "1,200 Gold"
    assert doc["categories"] == ["Units", "Infantry"]
    assert "Raider" in doc["links"] and "Barracks" in doc["links"]
    assert doc["images"] == ["HeavyGunner_full.png|thumb"] or doc["images"][0].startswith("HeavyGunner_full.png")
    md = doc["markdown"]
    assert "**Heavy Gunner**" in md and "Patch notes" not in md and "NOTOC" not in md and "Navbox" not in md
    assert "| Machine Gun | 12-18 | 1-3 |" in md
    assert "- Strong against raiders." in md and "  - Keep him in the front row." in md
    assert [s["title"] for s in doc["sections"]] == ["Intro", "Attacks", "Strategy"]
    assert doc["summary"].startswith("The Heavy Gunner is a sturdy Infantry unit")


def test_data_templates_and_tabber():
    doc = fk.parse_wikitext(PAGES["Barracks"], "Barracks")
    assert [t["fields"]["level"] for t in doc["templates"]] == ["1", "2"]
    assert "- time: 4h" in doc["markdown"]
    raider = fk.parse_wikitext(PAGES["Raider"], "Raider")
    assert "**Rank 6**" in raider["markdown"] and "Medals" in raider["markdown"]


def test_numbers():
    assert fk.parse_number("1,200 Gold") == 1200
    assert fk.parse_number("2.5k") == 2500
    assert fk.parse_number("15%") == 15
    assert fk.parse_number("3,5") == 3.5
    assert fk.parse_number("Vehicle") is None


def _sync(root, client=None, **scope):
    client = client or FakeClient()
    wiki = fk.resolve("samplewiki")
    kb = fk.KB(root, wiki.slug)
    return fk.sync(kb, client, wiki, scope), client, wiki


def test_sync_incremental_and_queries():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        res, client, wiki = _sync(root)
        assert res["pages"] == 3 and res["downloaded"] == 3
        assert set(res["tables"]) == {"Infobox Unit", "Infobox Building"}
        kb = fk.KB(root, "samplewiki")
        assert kb.find("HG")["title"] == "Heavy Gunner" and kb.find("heavy gunner")
        assert kb.meta["license"]["text"] == "CC BY-SA"
        assert (kb.dir / "pages" / "Heavy_Gunner.md").read_text().startswith("---\ntitle: \"Heavy Gunner\"")

        # second run: nothing changed → no content requests
        res2, client2, _ = _sync(root)
        assert res2["downloaded"] == 0 and client2.content_requests == 0
        # one page edited, one deleted
        c3 = FakeClient()
        c3.revs["Raider"] += 1
        del c3.pages["Barracks"]; del c3.revs["Barracks"]
        res3, _, _ = _sync(root, c3)
        assert res3["downloaded"] == 1 and res3["deleted"] == 1 and res3["pages"] == 2

        kb = fk.KB(root, "samplewiki")
        hits = fk.search(kb, "front row")
        assert hits and hits[0]["title"] == "Heavy Gunner"
        assert fk.search(kb, "HG")[0]["match"] == "title"
        cols, rows = fk.run_sql(kb, "SELECT title, cost, dodge FROM infobox_unit ORDER BY cost DESC")
        assert rows == [("Raider", 2500, 15), ("Heavy Gunner", 1200, 5)]


def test_profile_split_ranks():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _sync(root)
        kb = fk.KB(root, "samplewiki")
        draft = fk.profile_init(kb, min_pages=2)
        assert "Infobox Unit" in draft and "split: /" in draft
        profile = {"templates": {"Infobox Unit": {"table": "units", "drop": ["image", "name"],
                                                  "fields": {"hp": {"type": "int", "split": "/"},
                                                             "cost": {"type": "number", "rename": "gold_cost"}}}}}
        kb.build_db(profile)
        cols, rows = fk.run_sql(kb, "SELECT title, gold_cost, hp_1, hp_6 FROM units ORDER BY hp_6 DESC")
        assert rows == [("Heavy Gunner", 1200, 40, 70), ("Raider", 2500, 30, 50)]
        assert "image" not in cols


def test_category_scope():
    with tempfile.TemporaryDirectory() as d:
        res, _, _ = _sync(Path(d), categories=["Buildings"])
        assert res["pages"] == 1


def test_import_dump():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        dump = root / "dump.xml"
        dump.write_text(to_xml_dump(), encoding="utf-8")
        fk.main(["--root", str(root), "import", str(dump)])
        kb = fk.KB(root, "samplewiki")
        assert len(kb.index) == 3 and kb.aliases["HG"] == "Heavy Gunner"
        assert kb.index["Raider"]["url"] == "https://samplewiki.fandom.com/wiki/Raider"


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print("ok  ", name)
            except Exception as e:  # noqa: BLE001
                fails += 1; print("FAIL", name, repr(e))
    sys.exit(1 if fails else 0)
