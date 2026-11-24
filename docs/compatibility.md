# Compatibility scorecard

Generated 2026-11-24 by `uv run tools/compat.py` (fandom-kb 0.1.0): 20 random articles per wiki, full pipeline (fetch, parse, build SQLite).

| wiki | pages | has_box | infobox | recall | wikitext_only | portable | guessed | unnamed | numeric | leak | tables | invoke | wikitable | bare | top | missed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| battlenations | 20 | 85 | 85 | 100 | 85 | 0 | 85 | 0 | 49 | 0 | 16 | 0 | 0 | 0 | UnitInfobox, BuildingInfoBox, UnitProfile |  |
| wow | 20 | 75 | 75 | 100 | 75 | 0 | 75 | 0 | 27 | 0 | 5 | 0 | 5 | 20 | Itemtip, Npcbox, Questbox |  |
| warframe | 20 | 75 | 75 | 100 | 35 | 65 | 10 | 5 | 26 | 0 | 10 | 5 | 35 | 25 | Infobox, ModBox, WeaponInfoboxAutomatic |  |
| leagueoflegends | 20 | 65 | 60 | 92 | 35 | 55 | 5 | 6 | 13 | 7 | 10 | 15 | 35 | 30 | Card infobox, Ability, Infobox | Azir/LoL/Cosmetics |
| genshin-impact | 20 | 80 | 80 | 100 | 80 | 75 | 5 | 0 | 15 | 0 | 12 | 0 | 5 | 20 | Character Infobox, Act Infobox, Furnishing Infobox |  |
| eldenring | 20 | 90 | 90 | 100 | 90 | 90 | 0 | 0 | 39 | 0 | 9 | 0 | 0 | 10 | Infobox Item, Infobox Armor, Infobox Location |  |
| minecraft | 20 | 35 | 35 | 100 | 30 | 35 | 0 | 1 | 15 | 0 | 8 | 0 | 25 | 35 | Person, Version nav, Block |  |
| fallout | 20 | 75 | 75 | 100 | 75 | 70 | 5 | 0 | 26 | 0 | 13 | 0 | 20 | 20 | Infobox person, Infobox quest, Infobox weapon |  |
| witcher | 20 | 85 | 85 | 100 | 85 | 75 | 10 | 0 | 14 | 0 | 9 | 0 | 0 | 15 | Infobox Item3, Infobox Character, Infobox Item1 |  |
| residentevil | 20 | 90 | 90 | 100 | 90 | 85 | 5 | 0 | 5 | 0 | 13 | 0 | 0 | 10 | Infobox item, Infobox file, Infobox person |  |
| pokemon | 20 | 60 | 60 | 100 | 60 | 50 | 10 | 1 | 11 | 0 | 10 | 0 | 15 | 30 | CharacterBox, CharacterPokémonBox, TCGCardBox |  |
| zelda | 20 | 80 | 80 | 100 | 80 | 65 | 15 | 0 | 5 | 1 | 12 | 0 | 15 | 20 | Infobox Item, Infobox Location, Infobox Character |  |
| finalfantasy | 20 | 45 | 45 | 100 | 45 | 45 | 0 | 0 | 4 | 0 | 8 | 5 | 30 | 55 | Infobox equipment, Infobox race, Infobox organization |  |
| darksouls | 20 | 75 | 75 | 100 | 60 | 60 | 15 | 0 | 49 | 0 | 14 | 0 | 10 | 15 | DaSIIAmmunition, DaSIIIWeapon, DaSIIIArmor |  |
| hollowknight | 20 | 65 | 60 | 92 | 60 | 35 | 25 | 9 | 9 | 0 | 13 | 0 | 5 | 35 | Infobox, Gallery, HK Table Charm Interactions | Ancient Civilisation |
| onepiece | 20 | 90 | 90 | 100 | 90 | 90 | 0 | 0 | 15 | 0 | 9 | 0 | 30 | 5 | Char Box, Island Box, Chapter Box |  |
| naruto | 20 | 85 | 55 | 65 | 55 | 40 | 15 | 0 | 2 | 0 | 5 | 0 | 0 | 45 | Infobox/Jutsu, Infobox/Village, Infobox/Naruto/Episode | Koharu Utatane, Kunugi Mokume, Riichi |
| jujutsu-kaisen | 20 | 85 | 85 | 100 | 85 | 85 | 0 | 0 | 9 | 0 | 7 | 0 | 25 | 0 | Chapter Infobox, Technique Infobox, Character Infobox |  |
| attackontitan | 20 | 80 | 80 | 100 | 80 | 65 | 15 | 0 | 11 | 0 | 11 | 0 | 0 | 15 | Infobox character, Infobox chapter, Volume |  |
| dragonball | 20 | 85 | 85 | 100 | 85 | 85 | 0 | 0 | 2 | 0 | 6 | 0 | 20 | 15 | Character Infobox, Infobox Technique, EpisodeInfobox |  |
| starwars | 20 | 80 | 80 | 100 | 80 | 80 | 0 | 0 | 1 | 0 | 12 | 0 | 10 | 15 | Character, Person, Device |  |
| marvel | 20 | 100 | 100 | 100 | 100 | 50 | 50 | 0 | 4 | 0 | 3 | 0 | 0 | 0 | Marvel Database:Character Template, Marvel Database:Comic Template, Marvel Database:Volume Template |  |
| dc | 20 | 95 | 95 | 100 | 95 | 95 | 0 | 1 | 13 | 0 | 6 | 0 | 0 | 0 | DC Database:Staff Template, DC Database:Comic Template, DC Database:Character Template |  |
| harrypotter | 20 | 85 | 85 | 100 | 85 | 85 | 0 | 0 | 1 | 0 | 10 | 0 | 5 | 15 | Individual infobox, Actor infobox, Location infobox |  |
| lotr | 20 | 40 | 40 | 100 | 40 | 40 | 0 | 0 | 2 | 0 | 7 | 0 | 45 | 60 | Infobox Person Men Dúnedain, Race, Infobox Film |  |
| strangerthings | 20 | 90 | 90 | 100 | 90 | 90 | 0 | 0 | 12 | 0 | 11 | 0 | 15 | 10 | Character, Actor, Episode |  |
| simpsons | 20 | 60 | 60 | 100 | 55 | 60 | 0 | 0 | 1 | 0 | 7 | 0 | 5 | 40 | Character, Episode, Couch Gag |  |
| disney | 20 | 90 | 90 | 100 | 90 | 90 | 0 | 0 | 2 | 0 | 7 | 0 | 15 | 10 | Episode, Infobox Real Person, Infobox character |  |
| onepiece-fr | 20 | 90 | 90 | 100 | 90 | 90 | 0 | 0 | 16 | 0 | 9 | 0 | 5 | 0 | Char box, Chapitre Box, Episode Box |  |
| dragonball-es | 20 | 90 | 90 | 100 | 90 | 90 | 0 | 0 | 5 | 2 | 7 | 0 | 25 | 10 | Técnica, Personaje, Episodio |  |
| harrypotter-de | 20 | 60 | 60 | 100 | 60 | 10 | 50 | 0 | 2 | 0 | 7 | 0 | 5 | 40 | Infobox Pflanze, Charakterinfobox Ravenclaw, Infobox Objekt |  |

**Average** over 31 wikis: recall 98% (pages showing an infobox 77%, extracted 76%), wikitext only 73%, portable 63%, numeric 13%, leak 0%.

## Known limits

- Fandom truncates the infobox page property at 64 KB; such pages fall back to the wikitext guess.
- Portable infoboxes drawn by sub-templates match no template call: they land in a generic `infobox` table (`unnamed`).
- XML dumps carry no page properties: `kb import` always uses the wikitext guess.
- Infoboxes built from data stored elsewhere, without a portable infobox (Naruto: `{{Infobox}}` with no parameters), are missed: reading the rendered HTML would catch them.
- `bare` pages are often stubs, lists or disambiguations; `wikitable` and `invoke` show data not yet in SQL.

## Columns

| column | meaning |
|---|---|
| pages | random articles fetched |
| has_box | % of pages that show an infobox: extracted ones + missed ones (the wiki's rendered HTML has an infobox) |
| infobox | % of pages with at least one infobox extracted |
| recall | extracted / pages that show an infobox: **the number that matters** (the rest of the pages have no infobox to find) |
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
| missed | a few pages that show an infobox we didn't extract |
