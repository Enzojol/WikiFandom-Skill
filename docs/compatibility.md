# Compatibility scorecard

Generated 2026-11-24 by `uv run tools/compat.py` (fandom-kb 0.1.0): 20 random articles per wiki, full pipeline (fetch, parse, build SQLite).

| wiki | pages | infobox | wikitext_only | portable | guessed | unnamed | numeric | leak | tables | invoke | wikitable | bare | top |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| battlenations | 20 | 65 | 65 | 0 | 65 | 0 | 34 | 0 | 15 | 0 | 20 | 10 | BuildingInfoBox, UnitInfobox, UnitProfile |
| wow | 20 | 90 | 90 | 0 | 90 | 0 | 32 | 0 | 5 | 0 | 5 | 10 | Itemtip, Npcbox, Infobox faction |
| warframe | 20 | 75 | 30 | 70 | 5 | 2 | 29 | 0 | 9 | 5 | 30 | 25 | WeaponInfoboxAutomatic, ModBox, Infobox |
| leagueoflegends | 20 | 60 | 45 | 50 | 10 | 0 | 11 | 7 | 9 | 30 | 30 | 35 | Scroll box, Card infobox, Champion bio |
| genshin-impact | 20 | 100 | 100 | 85 | 15 | 0 | 17 | 0 | 15 | 0 | 0 | 0 | Character Infobox, Furnishing Infobox, Enemy Infobox |
| eldenring | 20 | 95 | 95 | 95 | 0 | 0 | 49 | 0 | 11 | 0 | 30 | 5 | Infobox Enemy, Infobox Item, Infobox Armor |
| minecraft | 20 | 30 | 25 | 30 | 0 | 1 | 10 | 0 | 7 | 0 | 15 | 35 | Block, Structure, Entity |
| fallout | 20 | 85 | 85 | 85 | 0 | 0 | 8 | 0 | 10 | 0 | 15 | 5 | Infobox character, Infobox quest, Infobox ammo gamebryo |
| witcher | 20 | 95 | 95 | 95 | 0 | 0 | 16 | 0 | 7 | 0 | 5 | 5 | Infobox Item3, Infobox Character, Infobox Location |
| residentevil | 20 | 80 | 80 | 80 | 0 | 0 | 1 | 0 | 10 | 0 | 15 | 15 | Infobox file, Infobox item, Infobox level |
| pokemon | 20 | 35 | 35 | 30 | 5 | 0 | 4 | 1 | 7 | 0 | 25 | 60 | PoI, CharacterPokémonBox, CharacterBox |
| zelda | 20 | 95 | 95 | 85 | 10 | 0 | 6 | 0 | 11 | 0 | 15 | 5 | Infobox Item, Infobox Location, Infobox Character |
| finalfantasy | 20 | 50 | 50 | 45 | 5 | 0 | 25 | 0 | 8 | 10 | 25 | 45 | Infobox character, Infobox equipment, FFXI Enemy Family |
| darksouls | 20 | 85 | 75 | 70 | 15 | 0 | 57 | 0 | 13 | 0 | 15 | 10 | DaSIIArmor, MiscItem, DaSIIExtendedWeapon |
| hollowknight | 20 | 95 | 85 | 90 | 5 | 25 | 8 | 0 | 9 | 0 | 15 | 5 | Infobox, HK Infobox Enemy, HK Infobox NPC |
| onepiece | 20 | 90 | 90 | 90 | 0 | 0 | 16 | 0 | 8 | 0 | 20 | 10 | Char Box, Episode Box, Chapter Box |
| naruto | 20 | 85 | 85 | 75 | 10 | 0 | 2 | 0 | 5 | 0 | 0 | 15 | Infobox/Jutsu, Infobox/Naruto/Episode, Infobox/Naruto/VideoGame |
| jujutsu-kaisen | 20 | 80 | 80 | 80 | 0 | 0 | 7 | 0 | 12 | 0 | 35 | 5 | Character Infobox, Chapter Infobox, Technique Infobox |
| attackontitan | 20 | 90 | 90 | 75 | 15 | 0 | 20 | 0 | 12 | 0 | 0 | 5 | Volume, Infobox character, Infobox song |
| dragonball | 20 | 90 | 90 | 80 | 10 | 0 | 4 | 0 | 7 | 0 | 10 | 10 | Scroll box, Infobox Technique, Chapter Infobox |
| starwars | 20 | 85 | 85 | 85 | 0 | 0 | 0 | 0 | 8 | 0 | 15 | 10 | Character, Person, System |
| marvel | 20 | 100 | 100 | 50 | 50 | 1 | 5 | 0 | 5 | 0 | 0 | 0 | Marvel Database:Comic Template, Marvel Database:Character Template, Marvel Database:Volume Template |
| dc | 20 | 85 | 85 | 85 | 0 | 1 | 16 | 0 | 8 | 0 | 0 | 5 | DC Database:Comic Template, DC Database:Character Template, Infobox |
| harrypotter | 20 | 90 | 90 | 90 | 0 | 0 | 0 | 0 | 11 | 0 | 0 | 10 | Actor infobox, Location infobox, Object infobox |
| lotr | 20 | 50 | 50 | 50 | 0 | 0 | 3 | 0 | 7 | 0 | 25 | 50 | Infobox Book, Location infobox, Infobox Actors |
| strangerthings | 20 | 75 | 75 | 75 | 0 | 0 | 7 | 0 | 10 | 0 | 10 | 25 | Character, Actor, Video game |
| simpsons | 20 | 55 | 55 | 55 | 0 | 0 | 3 | 0 | 5 | 0 | 0 | 45 | Character, Location, Cast |
| disney | 20 | 80 | 75 | 80 | 0 | 0 | 0 | 0 | 5 | 0 | 10 | 20 | Infobox character, Infobox Real Person, Infobox Song |
| onepiece-fr | 20 | 100 | 100 | 100 | 0 | 0 | 14 | 0 | 12 | 0 | 15 | 0 | Char box, Chapitre Box, Organisation box |
| dragonball-es | 20 | 90 | 90 | 90 | 0 | 0 | 11 | 2 | 10 | 0 | 15 | 10 | Manga, Episodio, Técnica |
| harrypotter-de | 20 | 60 | 60 | 10 | 50 | 0 | 2 | 2 | 8 | 0 | 0 | 40 | Infobox Objekt, Charakterinfobox Zauberer, Infobox Örtlichkeit |

**Average** over 31 wikis: infobox 79%, wikitext only 76%, portable 67%, numeric 13%, leak 0%.

## Known limits

- Fandom truncates the infobox page property at 64 KB; such pages fall back to the wikitext guess.
- Portable infoboxes drawn by sub-templates match no template call: they land in a generic `infobox` table (`unnamed`).
- XML dumps carry no page properties: `kb import` always uses the wikitext guess.
- `bare` pages are often stubs, lists or disambiguations; `wikitable` and `invoke` show data not yet in SQL.

## Columns

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
