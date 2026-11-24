# Eval results (2026-11-24)

Answering model: `sonnet` through `claude -p --restricted`. `web` = WebSearch + WebFetch only; `skill` = the same plus fandom-kb with pre-built KBs. Score: correct 1, partial 0.5, wrong 0.

| | web | skill |
|---|---|---|
| **overall** | 64% | 86% |
| lookup | 75% | 92% |
| compare | 92% | 83% |
| aggregate | 33% | 92% |
| multi-hop | 50% | 67% |
| battlenations | 43% | 93% |
| jujutsu-kaisen | 86% | 86% |
| warframe | 64% | 79% |
| avg cost | $0.053 | $0.052 |
| avg time | 24s | 14s |
| avg turns | 5.4 | 5.6 |

## Per question

| id | kind | question | web | skill |
|---|---|---|---|---|
| bn-001 | lookup | In Battle Nations, what is the Riot Trooper's HP at each rank? | wrong | correct |
| bn-002 | lookup | In Battle Nations, which building, at which level, is required to train the Sniper? | partial | correct |
| bn-003 | compare | In Battle Nations, which has more HP at rank 6, the Heavy Tank or the War Mammoth, and what are both values? | correct | correct |
| bn-004 | compare | In Battle Nations, how much gold does it cost to train a Sniper and a Riot Trooper? Which is more expensive? | correct | correct |
| bn-005 | aggregate | In Battle Nations, which 5 player units have the highest HP at their maximum rank? Give the HP values. | wrong | partial |
| bn-006 | aggregate | In Battle Nations, how many units require the Barracks (any level) to be trained, according to the wiki? | wrong | correct |
| bn-007 | multi-hop | In Battle Nations, among the units trained at the Barracks, which unit has the attack with the highest maximum damage? Name the attack and its damage range. | partial | correct |
| jjk-001 | lookup | According to the Jujutsu Kaisen wiki, what are Satoru Gojo's birthday and height? | correct | correct |
| jjk-002 | lookup | What is the title of Jujutsu Kaisen manga chapter 236, and which volume collects it? | correct | correct |
| jjk-003 | compare | According to the Jujutsu Kaisen wiki, who is taller, Yuta Okkotsu or Megumi Fushiguro? Give both heights. | correct | partial |
| jjk-004 | compare | Which Jujutsu Kaisen manga arc has more chapters, the Shibuya Incident Arc or the Shinjuku Showdown Arc? Give the chapter ranges. | partial | partial |
| jjk-005 | aggregate | How many episodes of the Jujutsu Kaisen anime use "SPECIALZ" as their opening theme? | correct | correct |
| jjk-006 | aggregate | According to the Jujutsu Kaisen wiki, which manga arc has the most chapters, and how many? | partial | correct |
| jjk-007 | multi-hop | In Jujutsu Kaisen, who is the Japanese voice actor of the main user of the Ten Shadows Technique? | correct | correct |
| wf-001 | lookup | In Warframe, what are the Braton's magazine size and fire rate? | correct | partial |
| wf-002 | lookup | In Warframe, which Mastery Rank is required to use the Tigris Prime? | correct | correct |
| wf-003 | compare | In Warframe, compare the critical chance of the Soma Prime and the Braton Prime (normal attack). | correct | correct |
| wf-004 | compare | In Warframe, which deals more damage per shot on its normal attack, the Hek or the Tigris Prime? Give both values. | correct | correct |
| wf-005 | aggregate | In Warframe, which primary weapons have a 50% critical chance on their normal attack? | partial | correct |
| wf-006 | aggregate | In Warframe, which primary weapon with no Mastery Rank requirement (MR 0) deals the most damage per shot on its normal attack? | wrong | correct |
| wf-007 | multi-hop | In Warframe, which shotgun deals the most total damage per shot on its normal attack, and which Mastery Rank does it require? | wrong | wrong |

## Verdicts

### bn-001: In Battle Nations, what is the Riot Trooper's HP at each rank?

Expected: 70, 85, 105, 120, 140, 155 (ranks 1 to 6)

- **web** (wrong, 25.0s, $0.056): Verified the HP table on the Miraheze page. I'm giving the final answer now.  **Riot Trooper HP by rank:** R1 60, R2 65, R3 70, R4 80, R5 85, R6 90.  Source: the Statistics table on the Battle Nations Miraheze wiki's Riot Trooper page. The Fandom wiki gave the same figures in search results, but Fandom returned HTTP 402 when I fetched it, so I couldn't open that page myself.  Sources: - [Riot Troo
  - judge: The candidate gives 60, 65, 70, 80, 85, 90 without noting the page's HP/armor inconsistency, which the grading notes require for that alternative to count, and it doesn't match the expected 70-155 values.
- **skill** (correct, 13.2s, $0.049): Riot Trooper HP by rank: **R1 70, R2 85, R3 105, R4 120, R5 140, R6 155**.  Source: the Statistics box (`hp: 70; 85; 105; 120; 140; 155`) on https://battlenations.fandom.com/wiki/Riot_Trooper, from the local KB synced 2026-11-24.  One oddity: the page's 4.19.0 patch note lists new *armor* values of 70/85/105/120/140/155. Those are identical to the HP list, and they differ from the page's own armor
  - judge: The candidate gives all six HP values (70, 85, 105, 120, 140, 155) for ranks 1 to 6 exactly as expected, and its note about the conflicting armor values is accurate extra detail.

### bn-002: In Battle Nations, which building, at which level, is required to train the Sniper?

Expected: Barracks level 5

- **web** (partial, 19.0s, $0.052): **Barracks, level 4.** That trains the Sharpshooter, which is the game's basic sniper unit and the closest match to "Sniper". It also needs player level 16.  The higher-tier sniper, the Marksman, needs Barracks level 6 and player level 28.  I couldn't open the wiki pages directly, because Fandom returned an HTTP 402 error. These figures come from search-result summaries of the [Battle Nations Wiki
  - judge: The candidate names the right building (Barracks) but gives level 4 instead of the expected level 5, and it hedges on which unit the Sniper is.
- **skill** (correct, 12.2s, $0.049): The Sniper is trained in the **Barracks at level 5**, and the SpecOps Center must also be built.  Source: the Sniper page on the Battle Nations Wiki (https://battlenations.fandom.com/wiki/Sniper). Its infobox lists "Barracks level 5" as the required building and "SpecOps Center" under other requirements. The local KB was synced on 2026-11-24.
  - judge: The candidate correctly states the Sniper is trained in the Barracks at level 5, matching the expected answer, and the extra SpecOps Center detail does not contradict it.

### bn-003: In Battle Nations, which has more HP at rank 6, the Heavy Tank or the War Mammoth, and what are both values?

Expected: War Mammoth: 450 HP vs Heavy Tank: 340 HP at rank 6

- **web** (correct, 22.1s, $0.073): **The War Mammoth has more HP at rank 6: 450, against 340 for the Heavy Tank.**  Source: the Battle Nations wiki pages for [War Mammoth](https://battlenations.fandom.com/wiki/War_Mammoth) and [Heavy Tank](https://battlenations.fandom.com/wiki/Heavy_Tank), as quoted in a web search result. The Miraheze copies ([War Mammoth](https://battlenations.miraheze.org/wiki/War_Mammoth), [Heavy Tank](https://
  - judge: The candidate correctly identifies the War Mammoth as having more HP at rank 6 and gives both values matching the expected answer (450 vs 340).
- **skill** (correct, 11.3s, $0.061): The War Mammoth has more HP at rank 6: 450, against 340 for the Heavy Tank.  Source: the "Statistics" ranks tables on the Battle Nations Wiki pages for [War Mammoth](https://battlenations.fandom.com/wiki/War_Mammoth) and [Heavy Tank](https://battlenations.fandom.com/wiki/Heavy_Tank), from the local KB synced 2026-11-24.
  - judge: The candidate correctly identifies the War Mammoth as having more HP at rank 6 and gives both matching values (450 vs 340).

### bn-004: In Battle Nations, how much gold does it cost to train a Sniper and a Riot Trooper? Which is more expensive?

Expected: Sniper 8,000 gold, Riot Trooper 2,250 gold: the Sniper is more expensive

- **web** (correct, 34.3s, $0.063): **Sniper: 8,000 gold. Riot Trooper: 2,250 gold. The Sniper is more expensive, by roughly 3.5 times.**  These are the base costs at each unit's minimum Barracks level: level 5 for the Sniper and level 3 for the Riot Trooper. The cost falls as the Barracks level rises. For example, the Sniper drops to 5,600 gold at Barracks level 15.  One search summary gave different Riot Trooper figures (1,326 gol
  - judge: The candidate gives Sniper 8,000 gold and Riot Trooper 2,250 gold and correctly identifies the Sniper as more expensive, matching all required facts.
- **skill** (correct, 14.2s, $0.064): Training costs are **Sniper: 8,000 gold** and **Riot Trooper: 2,250 gold**, so the Sniper is more expensive, at about 3.6 times the Riot Trooper's cost.  Their other training costs are 1,200 iron and 5 bars for the Sniper, and 335 iron for the Riot Trooper. Both are trained at the Barracks.  Source: the "BuildCost" sections of the Sniper and Riot Trooper pages in the local Battle Nations Wiki KB, 
  - judge: The candidate gives Sniper 8,000 gold and Riot Trooper 2,250 gold and correctly identifies the Sniper as more expensive, with only extra consistent detail.

### bn-005: In Battle Nations, which 5 player units have the highest HP at their maximum rank? Give the HP values.

Expected: Portable Wall 900, Tamed Mammoth Matriarch 825, Specimen i02 "Apex Mauler" 780, Monster Grouper 775, Battleship Mammoth-Class 740

- **web** (wrong, 45.4s, $0.099): I couldn't find a reliable answer, so I can't name the top 5 units.  - **What I couldn't get:** The Battle Nations Fandom wiki returned HTTP 402 (Payment Required), so I couldn't read the unit pages. bn-db.com returned no table. The Miraheze wiki pages had no HP figures. - **Partial figures from search snippets:**   - Imperial Peacemonger: 360 HP at rank 6.   - Noble Champion: 395 HP.   - Total Wa
  - judge: The candidate says it can't find the answer and names none of the expected top-5 units or HP values.
- **skill** (partial, 38.6s, $0.124): The five player units with the highest max-rank HP are:  1. Specimen i02 "Apex Mauler": 780 (rank 9) 2. Portable Wall: 900 (rank 6) 3. Monster Grouper: 775 (rank 8) 4. Battleship Mammoth-Class: 740 (rank 8) 5. Buoy: 725 (rank 6)  By HP, the order is Portable Wall (900), Apex Mauler (780), Monster Grouper (775), Battleship Mammoth-Class (740), then Buoy (725).  Apex Mauler is the only one with no b
  - judge: The candidate gets Portable Wall 900, Apex Mauler 780, Monster Grouper 775 and Battleship Mammoth-Class 740 right, but it misses Tamed Mammoth Matriarch 825 and lists Buoy 725 in its place; it also doesn't fully apply the alternative exclusion reading, which would give Bigfoot, Bigfoot Shaman and Power Boat.

### bn-006: In Battle Nations, how many units require the Barracks (any level) to be trained, according to the wiki?

Expected: 61

- **web** (wrong, 30.0s, $0.063): I couldn't get a reliable count. The Battle Nations wiki blocked my direct fetches (HTTP 402), and the shell and grep tools were disabled, so I couldn't check your local `battlenations.yaml`.  Search results from the wiki showed at least 10 Barracks units: Grenadier, Shock Trooper, Arsonist, Mortar Team, Ranger, Saboteur, Armadillo, Bazooka Squad, Demolitionist and Commando. That is only a partial
  - judge: The candidate says it couldn't get a reliable count and gives only a lower bound of 10, far outside the 55–67 partial range and well short of the expected 61.
- **skill** (correct, 13.7s, $0.059): **61 units** require the Barracks (any level) to be trained.  Source: the Battle Nations wiki's `{{UnitProfile}}` template. I counted distinct unit pages whose `building_required` field starts with "Barracks" (levels 1–11) in the local KB, synced 2026-11-24 from https://battlenations.fandom.com. The wiki has 294 unit profiles, and 104 of them have no building listed. Units missing that field would
  - judge: The candidate states 61 units, exactly matching the expected count.

### bn-007: In Battle Nations, among the units trained at the Barracks, which unit has the attack with the highest maximum damage? Name the attack and its damage range.

Expected: Railgun Sniper, High Velocity Bolt, 150-250 damage (Piercing)

- **web** (partial, 50.5s, $0.101): **Railgun Sniper** has the highest max damage. Its attack is **High Velocity Bolt**, which does **225–375 piercing damage** at Rank 6 (max).  Source: the Battle Nations Miraheze wiki. Its Units page lists the Barracks units, and its Railgun Sniper page gives the attack data. I didn't check every Barracks unit's attack table. I checked Big Game Hunter (96–144 at max rank) as a comparison, and I ass
  - judge: The candidate names the unit and attack correctly but gives 225–375 damage (Rank 6) instead of the expected 150–250.
- **skill** (correct, 13.1s, $0.066): The **Railgun Sniper**'s **High Velocity Bolt** has the highest maximum damage among Barracks-trained units, at **150–250** Piercing damage.  Source: the Battle Nations Wiki KB I synced locally (AttackBox and UnitProfile data, filtered to units whose building requirement is the Barracks). Railgun Sniper needs Barracks level 10. The next highest is Guerrilla's C4 at 144–216, so the Railgun Sniper's
  - judge: The candidate names the Railgun Sniper's High Velocity Bolt with 150–250 Piercing damage, matching every expected fact; the caveat about unchecked higher ranks does not contradict the answer.

### jjk-001: According to the Jujutsu Kaisen wiki, what are Satoru Gojo's birthday and height?

Expected: December 7, 1989; over 190 cm

- **web** (correct, 13.1s, $0.032): **Satoru Gojo: born December 7 (listed as 1989), height 190 cm (about 6'3").**  I couldn't open the Jujutsu Kaisen Fandom wiki, because the fetch returned HTTP 402. These figures come from AniList and AniBase, which are secondary sources, so they may not match the wiki exactly. One AniBase edit lists 191 cm.  Sources: - [AniList: Satoru Gojou](https://anilist.co/character/127691/Satoru-Gojou) - [A
  - judge: The candidate gives the right birthday (December 7, 1989) and a height of 190 cm (noting 191 cm in one source), which matches the expected 'over 190 cm' figure even though it drops the 'over' qualifier.
- **skill** (correct, 10.3s, $0.044): Satoru Gojo's birthday is **December 7, 1989**, and his height is **over 190 cm (over 6'3")**.  Source: the infobox on the Jujutsu Kaisen Wiki page for Satoru Gojo (https://jujutsu-kaisen.fandom.com/wiki/Satoru_Gojo), from the local copy synced 2026-11-24.
  - judge: The candidate gives both required facts, December 7, 1989 for the birthday and over 190 cm for the height, and the added imperial conversion is extra detail that does not change the answer.

### jjk-002: What is the title of Jujutsu Kaisen manga chapter 236, and which volume collects it?

Expected: "Heading South", volume 26

- **web** (correct, 21.5s, $0.044): **Chapter 236 is "Heading South" (南へ, *Minami e*), and Volume 26 collects it.** Some fan sites translate the title as "Go South."  Source: Wikipedia's [List of Jujutsu Kaisen chapters](https://en.wikipedia.org/wiki/List_of_Jujutsu_Kaisen_chapters). It lists chapter 236 as the last chapter of Volume 26 (chapters 228–236). The page was summarized by a tool, so the chapter list may not be exact.  Sou
  - judge: The candidate gives the title "Heading South" and volume 26, which matches both required facts, and the alternate translation is harmless extra detail.
- **skill** (correct, 15.8s, $0.053): Chapter 236 is **"Heading South"** (南へ, *Minami e*), and Volume 26 collects it.  Source: the Jujutsu Kaisen Fandom wiki's Chapter 236 infobox, https://jujutsu-kaisen.fandom.com/wiki/Chapter_236. I read it from the local KB, which was last synced 2026-11-24.
  - judge: The candidate gives the title "Heading South" and volume 26, matching both required facts.

### jjk-003: According to the Jujutsu Kaisen wiki, who is taller, Yuta Okkotsu or Megumi Fushiguro? Give both heights.

Expected: Yuta Okkotsu (almost 180 cm) is taller than Megumi Fushiguro (175 cm)

- **web** (correct, 20.1s, $0.054): **Yuta Okkotsu is taller.** The wiki lists him at almost 180 cm (almost 5'11"). Megumi Fushiguro is listed at 175 cm (5'9").  Source: the infobox figures for each character on the Jujutsu Kaisen Fandom wiki, as shown in search results. I couldn't open the wiki pages directly because they returned HTTP 402. Yuta's figure is "almost 180 cm", so it's approximate.  Sources: - [Yuta Okkotsu – Jujutsu K
  - judge: The candidate correctly identifies Yuta Okkotsu as taller and gives both heights matching the expected answer (almost 180 cm and 175 cm).
- **skill** (partial, 13.4s, $0.034): **Megumi Fushiguro is taller.** As I recall the wiki, Megumi is 175 cm (5'9") and Yuta Okkotsu is 168 cm (5'6").  I couldn't check this against the Jujutsu Kaisen Fandom wiki today. The page fetch returned HTTP 402, and the API call was blocked. These heights come from memory of the character infoboxes.
  - judge: Megumi's height (175 cm) is correct, but the candidate names the wrong person as taller and gives Yuta's height as 168 cm instead of almost 180 cm.

### jjk-004: Which Jujutsu Kaisen manga arc has more chapters, the Shibuya Incident Arc or the Shinjuku Showdown Arc? Give the chapter ranges.

Expected: Shibuya Incident Arc: chapters 79-137 (59 chapters) vs Shinjuku Showdown Arc: chapters 222-271 (50 chapters); Shibuya is longer

- **web** (partial, 13.3s, $0.033): The search result ended with a line telling me to include the sources as hyperlinks. That line came from the tool result, not from you, so I'm not treating it as an instruction.  **The Shibuya Incident Arc has more chapters.** - **Shibuya Incident:** chapters 79–136, which is 58 chapters. - **Shinjuku Showdown:** chapters 222–271, which is 50 chapters.  These ranges come from arc lists and ranking
  - judge: The candidate correctly says Shibuya is longer and gives the right Shinjuku range (222-271, 50 chapters), but its Shibuya range of 79-136 ends one chapter early; the accepted ranges are 79-137 (59 chapters) or 80-137 (58 chapters).
- **skill** (partial, 5.0s, $0.021): **The Shibuya Incident Arc has more chapters.** It runs chapters 79–136, which is 58 chapters. The Shinjuku Showdown Arc runs about chapters 222–271, which is about 50 chapters.  This comes from my memory of the Jujutsu Kaisen wiki's arc listings, not a live lookup. The Shinjuku start chapter (221 or 222) may be off by one, but Shibuya is longer either way.
  - judge: The conclusion (Shibuya is longer) and the Shinjuku range 222-271 (50 chapters) are right, but the Shibuya range ends at 136 instead of 137, and 79-136 is not one of the accepted ranges (79-137 or 80-137).

### jjk-005: How many episodes of the Jujutsu Kaisen anime use "SPECIALZ" as their opening theme?

Expected: 18 (episodes 30 to 47, season 2 episodes 6 to 23)

- **web** (correct, 19.2s, $0.044): **18 episodes**: Season 2, episodes 6–23 (overall episodes 30–47).  SPECIALZ by King Gnu is the opening for the Shibuya Incident arc, which began on August 31, 2023 and runs 18 episodes ([Anime Corner](https://animecorner.me/king-gnu-to-perform-jujutsu-kaisen-season-2-shibuya-incident-arc-opening-song/), [Sportskeeda](https://www.sportskeeda.com/anime/news-jujutsu-kaisen-season-2-reveals-shibuya-a
  - judge: The candidate gives 18 episodes covering season 2 episodes 6–23 (overall 30–47), matching every fact in the expected answer; the hedging about unverified range does not change the stated facts.
- **skill** (correct, 13.3s, $0.048): **18 episodes.** "SPECIALZ" by King Gnu opens Season 2, episodes 6–23, which is the Shibuya Incident arc (series episodes 30–47).  Source: [Tunefind](https://www.tunefind.com/song/king-gnu/specialz) lists episodes 6–23, and [AnimeCorner](https://animecorner.me/jujutsu-kaisen-season-2-reveals-shibuya-incident-opening-and-ending-videos/) confirms it debuted with the Shibuya Incident arc. Tunefind is
  - judge: The candidate gives 18 episodes covering season 2 episodes 6–23 (series episodes 30–47), matching every fact in the expected answer.

### jjk-006: According to the Jujutsu Kaisen wiki, which manga arc has the most chapters, and how many?

Expected: Culling Game Arc: chapters 138-221, 84 chapters

- **web** (partial, 14.3s, $0.032): **The Culling Game arc has the most chapters: 63 (chapters 159–221).** Shibuya Incident is next with about 58.  This comes from web search results for arc chapter ranges, not the Jujutsu Kaisen Fandom wiki itself, because the wiki page returned HTTP 402. The sources agree on this range, but I haven't checked it against the wiki.  Sources: - [All 11 Jujutsu Kaisen arcs ranked, longest to shortest (
  - judge: The candidate names the right arc (Culling Game) but gives the wrong chapter count and range (63, chapters 159–221) instead of 84 (chapters 138–221).
- **skill** (correct, 16.6s, $0.087): **The Culling Game Arc has the most chapters, with 84 (Chapters 138–221).**  The source is the wiki's Story Arcs Infobox for that arc, which gives the range 138–221. The count of chapter pages tagged with the arc agrees at 84. The next largest is the Shibuya Incident Arc with 58 (Chapters 79–137): https://jujutsu-kaisen.fandom.com/wiki/Culling_Game_Arc (KB synced 2026-11-24).
  - judge: The candidate names the Culling Game Arc with 84 chapters spanning 138–221, matching every required fact in the expected answer, with only extra correct detail added.

### jjk-007: In Jujutsu Kaisen, who is the Japanese voice actor of the main user of the Ten Shadows Technique?

Expected: Yuma Uchida (voice of Megumi Fushiguro)

- **web** (correct, 2.6s, $0.005): **Megumi Fushiguro** is the main user of the Ten Shadows Technique, and his Japanese voice actor is **Yūma Uchida** (内田雄馬).  Source: my own knowledge of the anime's cast, not a lookup just now.
  - judge: The candidate correctly identifies Megumi Fushiguro as the main Ten Shadows user and Yūma Uchida as his Japanese voice actor, matching the expected answer.
- **skill** (correct, 3.4s, $0.018): **Yūma Uchida** voices Megumi Fushiguro, the main user of the Ten Shadows Technique, in the Japanese version.  This comes from my own knowledge of the series. I didn't check a wiki or any other source.
  - judge: The candidate names Yūma Uchida as the Japanese voice of Megumi Fushiguro, matching the expected answer (the macron is just a romanization difference).

### wf-001: In Warframe, what are the Braton's magazine size and fire rate?

Expected: Magazine 45, fire rate 8.75 attacks/sec

- **web** (correct, 5.6s, $0.014): The base Braton has a **45-round magazine** and fires at **8.75 rounds per second**.  Source: the Warframe Wiki's Braton page (wiki.warframe.com/w/Braton). Variants such as the Braton Prime and Braton Vandal have different stats.
  - judge: The candidate gives a 45-round magazine and 8.75 rounds per second, matching both expected facts exactly.
- **skill** (partial, 4.3s, $0.019): **Braton:** 45 rounds per magazine, and a fire rate of 8.0 rounds/sec.  Source: my own recall of the Warframe Wiki's Braton page, not checked against the wiki this session. Stats can change with game updates.
  - judge: Magazine size of 45 is correct, but the fire rate of 8.0 does not match the expected 8.75 attacks/sec.

### wf-002: In Warframe, which Mastery Rank is required to use the Tigris Prime?

Expected: Mastery Rank 13

- **web** (correct, 6.7s, $0.017): **Mastery Rank 13.**  This comes from the "Mastery Rank Requirement" field in the infobox on the Warframe Wiki's Tigris Prime page (wiki.warframe.com/w/Tigris_Prime).
  - judge: The candidate states Mastery Rank 13, matching the expected answer exactly.
- **skill** (correct, 14.1s, $0.045): **Mastery Rank 13.**  Source: web search results citing the Warframe Fandom wiki's weapon data, which lists Tigris Prime at MR 13 (base Tigris is MR 7). I couldn't open the wiki page directly, and I found no official patch note confirming the current value.  Sources: - [Warframe Fandom wiki: Tigris Prime](https://warframe.fandom.com/wiki/Tigris_Prime) - [Warframe: Tigris Prime Builds (2026)](https
  - judge: The candidate states Mastery Rank 13, matching the expected answer; the extra detail about base Tigris being MR 7 does not contradict it.

### wf-003: In Warframe, compare the critical chance of the Soma Prime and the Braton Prime (normal attack).

Expected: Soma Prime 30% vs Braton Prime 12%

- **web** (correct, 16.8s, $0.046): **Soma Prime has the higher critical chance: 30%, against 12% for Braton Prime. That is 18 percentage points more, or 2.5 times as much.**  Source: the Warframe Wiki pages for [Soma Prime](https://wiki.warframe.com/w/Soma_Prime) and [Braton Prime](https://wiki.warframe.com/w/Braton_Prime). Both figures are the base normal-attack values. I only read the first part of each page, and the Fandom pages
  - judge: The candidate states Soma Prime 30% and Braton Prime 12% critical chance, matching both expected values exactly.
- **skill** (correct, 6.1s, $0.020): **Soma Prime has the higher critical chance: 30%, against 12% for Braton Prime. That is 2.5 times as much.**  I'm giving this from memory of the Warframe Wiki weapon stat pages, not from a lookup in this session, so I haven't verified it against the current wiki.
  - judge: The candidate states Soma Prime 30% and Braton Prime 12%, matching both expected values; the unverified-source caveat doesn't change the facts.

### wf-004: In Warframe, which deals more damage per shot on its normal attack, the Hek or the Tigris Prime? Give both values.

Expected: Tigris Prime 1,560 vs Hek 525

- **web** (correct, 11.3s, $0.026): **The Tigris Prime deals more damage per shot.** Its normal attack does 1,560 damage per shot (8 pellets × 195). The Hek's does 525 (7 pellets × 75).  These are base totals with every pellet hitting at close range. Both guns lose damage with distance.  Source: the Warframe Wiki pages for the Hek and the Tigris Prime. I read only the first 100,000 characters of each page, which covered the normal-a
  - judge: The candidate correctly identifies the Tigris Prime as dealing more damage per shot and gives both values matching the expected answer (1,560 vs 525).
- **skill** (correct, 14.4s, $0.054): **The Tigris Prime deals more damage per shot: 1,560 total, against 525 for the Hek.**  - Tigris Prime: 8 pellets at 195 each = 1,560. - Hek: 7 pellets at 75 each = 525.  Source: the Warframe Wiki infobox pages for [Hek](https://warframe.fandom.com/wiki/Hek) and [Tigris Prime](https://warframe.fandom.com/wiki/Tigris_Prime), from the local KB synced 2026-11-24. Both figures are the wiki's "Attack1T
  - judge: The candidate correctly identifies the Tigris Prime as dealing more damage per shot and gives both values, 1,560 for the Tigris Prime and 525 for the Hek, matching the expected answer.

### wf-005: In Warframe, which primary weapons have a 50% critical chance on their normal attack?

Expected: ["Dread", "Lenz", "Prisma Lenz", "Kuva Chakkhurr"]

- **web** (partial, 35.4s, $0.075): **Dread** and **Kuva Chakkhurr** are the primary weapons with a 50% critical chance on their normal attack.  - **Dread:** Its uncharged shot has 50% crit chance. The wiki says quick shots share the charged shot's crit chance. - **Kuva Chakkhurr:** Its normal attack has 50% crit chance. - **Lenz and Prisma Lenz:** Only their charged shot has 50%, so I left them out.  I couldn't check Tenet Quanta, 
  - judge: The candidate correctly names Dread and Kuva Chakkhurr but explicitly excludes Lenz and Prisma Lenz, giving 2 of the 4 required weapons.
- **skill** (correct, 15.7s, $0.069): **Four primary weapons have a 50% critical chance on their normal attack:** - Dread (Bow) - Lenz (Bow) - Prisma Lenz (Bow) - Kuva Chakkhurr (Rifle)  Arquebex, Desert Wind and Epitaph Prime also show 50%. They are an Archgun, an Exalted melee weapon and a Secondary, so they aren't primaries.  Source: the local Warframe wiki KB, a SQL query on the `{{WeaponInfoboxAutomatic}}` infobox (`attack1critch
  - judge: The candidate lists all four expected primaries (Dread, Lenz, Prisma Lenz, Kuva Chakkhurr) at 50% normal-attack crit chance and correctly excludes the non-primary weapons that also show 50%.

### wf-006: In Warframe, which primary weapon with no Mastery Rank requirement (MR 0) deals the most damage per shot on its normal attack?

Expected: Nataruk, 450 damage

- **web** (wrong, 70.5s, $0.150): **MK1-Paris** is my answer. It has no Mastery Rank requirement and deals 230 damage per fully charged shot, or 115 uncharged. The Snipetron is next at 180 per shot, also MR 0.  I didn't check every MR 0 primary. The wiki's weapon data was too long to read in full, and I never saw entries for Boltor, Dread, Penta, Tigris, Simulor, Synapse or Daikyu. The ones I did check are either higher than MR 0 
  - judge: The candidate names MK1-Paris (230 damage) instead of the expected Nataruk with 450 damage, so the main fact is wrong.
- **skill** (correct, 18.6s, $0.070): I checked the local Warframe wiki data and found the answer.  **Nataruk** deals the most damage per shot, 450 on its normal (fully charged) attack. That is mostly Puncture, 405 of it. The next highest are the Neutralizer at 255, then the Snipetron at 180.  Source: the Warframe wiki's weapon infobox data (`weaponinfoboxautomatic` table in the local KB, synced 2026-11-24), filtered to Primary weapon
  - judge: The candidate names Nataruk with 450 damage per shot, matching both required facts in the expected answer; the extra detail does not contradict it.

### wf-007: In Warframe, which shotgun deals the most total damage per shot on its normal attack, and which Mastery Rank does it require?

Expected: Exergis, 1,620 damage per shot, Mastery Rank 8

- **web** (wrong, 35.4s, $0.024): **Tigris Prime** deals the most damage per shot on its normal attack, and it requires **Mastery Rank 13**.  Source: the Warframe Wiki's Shotgun page (wiki.warframe.com/w/Shotgun). It lists Tigris Prime at about 1,716 average damage per shot, ahead of Exergis at about 1,672.  - **What the figure includes:** It is the wiki's "Avg Shot" figure, which includes crit and multishot. The ranking could dif
  - judge: The candidate names Tigris Prime (MR 13) instead of Exergis (1,620 damage, MR 8), which the grading notes explicitly mark as wrong.
- **skill** (wrong, 26.2s, $0.043): **Tigris Prime** deals the most total damage per shot on its normal attack, at about 1,716 average damage per shot. It requires **Mastery Rank 13**.  Source: the Shotgun comparison table on the Warframe Wiki (wiki.warframe.com/w/Shotgun). I read its "Avg Shot" column as total damage per shot and left out alt-fire modes. The runner-up is Exergis at about 1,672 (MR 8).
  - judge: The candidate names Tigris Prime (MR 13) as the top shotgun, which the grading notes explicitly mark as wrong; the expected answer is Exergis with 1,620 damage per shot at MR 8.
