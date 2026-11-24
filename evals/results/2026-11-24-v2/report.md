# Eval results (2026-11-24-v2)

Answering model: `sonnet` through `claude -p --restricted`. `web` = WebSearch + WebFetch only; `skill` = the same plus fandom-kb with pre-built KBs. Score: correct 1, partial 0.5, wrong 0.

| | web | skill |
|---|---|---|
| **overall** | 64% | 95% |
| lookup | 75% | 100% |
| compare | 92% | 100% |
| aggregate | 33% | 100% |
| multi-hop | 50% | 67% |
| battlenations | 43% | 100% |
| jujutsu-kaisen | 86% | 100% |
| warframe | 64% | 86% |
| avg cost | $0.053 | $0.068 |
| avg time | 24s | 13s |
| avg turns | 5.4 | 6.2 |

Skill arm used the knowledge base on **21/21** questions: accuracy 95% when it did, – when it didn't.

## Per question

| id | kind | question | web | skill |
|---|---|---|---|---|
| bn-001 | lookup | In Battle Nations, what is the Riot Trooper's HP at each rank? | wrong | correct |
| bn-002 | lookup | In Battle Nations, which building, at which level, is required to train the Sniper? | partial | correct |
| bn-003 | compare | In Battle Nations, which has more HP at rank 6, the Heavy Tank or the War Mammoth, and what are both values? | correct | correct |
| bn-004 | compare | In Battle Nations, how much gold does it cost to train a Sniper and a Riot Trooper? Which is more expensive? | correct | correct |
| bn-005 | aggregate | In Battle Nations, which 5 player units have the highest HP at their maximum rank? Give the HP values. | wrong | correct |
| bn-006 | aggregate | In Battle Nations, how many units require the Barracks (any level) to be trained, according to the wiki? | wrong | correct |
| bn-007 | multi-hop | In Battle Nations, among the units trained at the Barracks, which unit has the attack with the highest maximum damage? Name the attack and its damage range. | partial | correct |
| jjk-001 | lookup | According to the Jujutsu Kaisen wiki, what are Satoru Gojo's birthday and height? | correct | correct |
| jjk-002 | lookup | What is the title of Jujutsu Kaisen manga chapter 236, and which volume collects it? | correct | correct |
| jjk-003 | compare | According to the Jujutsu Kaisen wiki, who is taller, Yuta Okkotsu or Megumi Fushiguro? Give both heights. | correct | correct |
| jjk-004 | compare | Which Jujutsu Kaisen manga arc has more chapters, the Shibuya Incident Arc or the Shinjuku Showdown Arc? Give the chapter ranges. | partial | correct |
| jjk-005 | aggregate | How many episodes of the Jujutsu Kaisen anime use "SPECIALZ" as their opening theme? | correct | correct |
| jjk-006 | aggregate | According to the Jujutsu Kaisen wiki, which manga arc has the most chapters, and how many? | partial | correct |
| jjk-007 | multi-hop | In Jujutsu Kaisen, who is the Japanese voice actor of the main user of the Ten Shadows Technique? | correct | correct |
| wf-001 | lookup | In Warframe, what are the Braton's magazine size and fire rate? | correct | correct |
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
  - judge: The candidate gives 60, 65, 70, 80, 85, 90 rather than the expected 70–155 values, and it does not mention the page's HP/armor inconsistency, which the grading notes require before that alternative set can count as correct.
- **skill** (correct, 11.9s, $0.051): **Riot Trooper HP by rank: 60, 65, 70, 80, 85, 90 (ranks 1–6).**  The wiki page has a labeling problem. Its stats box lists `hp: 70; 85; 105; 120; 140; 155` and `armor: 60; 65; 70; 80; 85; 90`. I think those two rows are swapped, for two reasons: - The infobox shows HP 90 and Armor 155, which are the rank 6 values of the two rows as I've swapped them. - The 4.19.0 patch note says armor rose to 70,
  - judge: The candidate gives 60, 65, 70, 80, 85, 90 and explicitly explains the page's HP/armor labeling inconsistency, which the grading notes accept as correct.

### bn-002: In Battle Nations, which building, at which level, is required to train the Sniper?

Expected: Barracks level 5

- **web** (partial, 19.0s, $0.052): **Barracks, level 4.** That trains the Sharpshooter, which is the game's basic sniper unit and the closest match to "Sniper". It also needs player level 16.  The higher-tier sniper, the Marksman, needs Barracks level 6 and player level 28.  I couldn't open the wiki pages directly, because Fandom returned an HTTP 402 error. These figures come from search-result summaries of the [Battle Nations Wiki
  - judge: The candidate names the right building (Barracks) but gives level 4 instead of the expected level 5.
- **skill** (correct, 8.2s, $0.046): **The Barracks at level 5 trains the Sniper.** It also needs the SpecOps Center to be built first.  Source: the Sniper page on the Battle Nations Wiki (https://battlenations.fandom.com/wiki/Sniper), from the local KB synced 2026-11-24. Its infobox says "building required: Barracks level 5" and "other requirements: SpecOps Center".
  - judge: The candidate correctly states the Barracks at level 5 is required; the extra SpecOps Center requirement is additional detail that does not contradict the expected answer.

### bn-003: In Battle Nations, which has more HP at rank 6, the Heavy Tank or the War Mammoth, and what are both values?

Expected: War Mammoth: 450 HP vs Heavy Tank: 340 HP at rank 6

- **web** (correct, 22.1s, $0.073): **The War Mammoth has more HP at rank 6: 450, against 340 for the Heavy Tank.**  Source: the Battle Nations wiki pages for [War Mammoth](https://battlenations.fandom.com/wiki/War_Mammoth) and [Heavy Tank](https://battlenations.fandom.com/wiki/Heavy_Tank), as quoted in a web search result. The Miraheze copies ([War Mammoth](https://battlenations.miraheze.org/wiki/War_Mammoth), [Heavy Tank](https://
  - judge: The candidate correctly identifies the War Mammoth as having more HP at rank 6 and gives both values, 450 and 340, matching the expected answer.
- **skill** (correct, 14.4s, $0.096): **The War Mammoth has more HP at rank 6: 450, against 340 for the Heavy Tank.**  The figures come from the `UnitRanksBox` HP lists on the Battle Nations Wiki pages for [Heavy Tank](https://battlenations.fandom.com/wiki/Heavy_Tank) and [War Mammoth](https://battlenations.fandom.com/wiki/War_Mammoth), in the local KB synced 2026-11-24. Each unit has six ranks listed, and rank 6 is the last entry (He
  - judge: The candidate correctly identifies the War Mammoth as having more HP at rank 6 and gives both values matching the expected answer (450 vs 340).

### bn-004: In Battle Nations, how much gold does it cost to train a Sniper and a Riot Trooper? Which is more expensive?

Expected: Sniper 8,000 gold, Riot Trooper 2,250 gold: the Sniper is more expensive

- **web** (correct, 34.3s, $0.063): **Sniper: 8,000 gold. Riot Trooper: 2,250 gold. The Sniper is more expensive, by roughly 3.5 times.**  These are the base costs at each unit's minimum Barracks level: level 5 for the Sniper and level 3 for the Riot Trooper. The cost falls as the Barracks level rises. For example, the Sniper drops to 5,600 gold at Barracks level 15.  One search summary gave different Riot Trooper figures (1,326 gol
  - judge: The candidate gives Sniper 8,000 gold and Riot Trooper 2,250 gold and correctly says the Sniper is more expensive; the extra Barracks-level detail does not contradict the expected answer.
- **skill** (correct, 10.1s, $0.058): **Sniper: 8,000 gold. Riot Trooper: 2,250 gold. The Sniper is more expensive, by 5,750 gold (about 3.6 times the cost).**  These are the base training costs (BuildCost) in the Barracks. The Sniper also costs 1,200 iron and 5 bars, and the Riot Trooper costs 335 iron.  Source: the Battle Nations Wiki pages https://battlenations.fandom.com/wiki/Sniper and https://battlenations.fandom.com/wiki/Riot_T
  - judge: The candidate gives Sniper 8,000 gold and Riot Trooper 2,250 gold and correctly identifies the Sniper as more expensive, matching all expected facts with only extra correct detail.

### bn-005: In Battle Nations, which 5 player units have the highest HP at their maximum rank? Give the HP values.

Expected: Portable Wall 900, Tamed Mammoth Matriarch 825, Specimen i02 "Apex Mauler" 780, Monster Grouper 775, Battleship Mammoth-Class 740

- **web** (wrong, 45.4s, $0.099): I couldn't find a reliable answer, so I can't name the top 5 units.  - **What I couldn't get:** The Battle Nations Fandom wiki returned HTTP 402 (Payment Required), so I couldn't read the unit pages. bn-db.com returned no table. The Miraheze wiki pages had no HP figures. - **Partial figures from search snippets:**   - Imperial Peacemonger: 360 HP at rank 6.   - Noble Champion: 395 HP.   - Total Wa
  - judge: The candidate says it couldn't find the answer and names none of the expected top-5 units or HP values; the scattered snippet figures it lists don't match either the expected list or the alternative accepted ranking.
- **skill** (correct, 25.9s, $0.129): **The top 5 player units by HP at max rank:**  1. Monster Grouper: 775 2. Battleship Mammoth-Class: 740 3. Bigfoot: 720 4. Bigfoot Shaman: 720 (tied with Bigfoot) 5. Power Boat: 705  I counted only units you can build or train from a player building. I left out four kinds of entry that rank higher on raw HP: - Defensive structures: Portable Wall (900), Buoy (725), Portable Electric Fence (675) and
  - judge: The candidate explicitly excludes defensive structures and units with no building requirement, names them with correct HP values (Portable Wall 900, Matriarch 825, Apex Mauler 780), and then gives the alternate ranking exactly as listed in the grading notes (Monster Grouper 775, Battleship Mammoth-Class 740, Bigfoot 720, Bigfoot Shaman 720, Power Boat 705).

### bn-006: In Battle Nations, how many units require the Barracks (any level) to be trained, according to the wiki?

Expected: 61

- **web** (wrong, 30.0s, $0.063): I couldn't get a reliable count. The Battle Nations wiki blocked my direct fetches (HTTP 402), and the shell and grep tools were disabled, so I couldn't check your local `battlenations.yaml`.  Search results from the wiki showed at least 10 Barracks units: Grenadier, Shock Trooper, Arsonist, Mortar Team, Ranger, Saboteur, Armadillo, Bazooka Squad, Demolitionist and Commando. That is only a partial
  - judge: The candidate says it couldn't get a reliable count and gives only a lower bound of 10, which is far outside the 55–67 partial range and does not match the expected 61.
- **skill** (correct, 9.1s, $0.092): Sum: 23+4+2+4+4+2+6+3+4+6+3 = 61.  **61 units** require the Barracks (levels 1–11).  Source: the Battle Nations wiki KB (synced 2026-11-24), counting `building_required` = "Barracks level N" in the `{{UnitProfile}}` infobox across unit pages (https://battlenations.fandom.com). The count only covers the 294 unit pages that have a UnitProfile.
  - judge: The candidate's count of 61 units requiring the Barracks matches the expected answer exactly, and its component sum adds up to 61.

### bn-007: In Battle Nations, among the units trained at the Barracks, which unit has the attack with the highest maximum damage? Name the attack and its damage range.

Expected: Railgun Sniper, High Velocity Bolt, 150-250 damage (Piercing)

- **web** (partial, 50.5s, $0.101): **Railgun Sniper** has the highest max damage. Its attack is **High Velocity Bolt**, which does **225–375 piercing damage** at Rank 6 (max).  Source: the Battle Nations Miraheze wiki. Its Units page lists the Barracks units, and its Railgun Sniper page gives the attack data. I didn't check every Barracks unit's attack table. I checked Big Game Hunter (96–144 at max rank) as a comparison, and I ass
  - judge: The candidate names the right unit (Railgun Sniper), the right attack (High Velocity Bolt) and the right damage type (Piercing), but gives 225–375 damage at Rank 6 where 150–250 is expected.
- **skill** (correct, 11.3s, $0.091): **Railgun Sniper's High Velocity Bolt** has the highest maximum damage among Barracks-trained units, at **150–250 damage**.  The next highest are Guerrilla's C4 and The Wimp's Juiced Clap and Juiced Hook, all at 144–216.  Source: the Battle Nations Wiki (battlenations.fandom.com), "Railgun Sniper" page. I found it by joining the local copy's AttackBox data to UnitProfile entries whose building req
  - judge: The candidate names the Railgun Sniper's High Velocity Bolt with 150–250 damage, which covers everything the question asks for; the omitted 'Piercing' damage type was not requested.

### jjk-001: According to the Jujutsu Kaisen wiki, what are Satoru Gojo's birthday and height?

Expected: December 7, 1989; over 190 cm

- **web** (correct, 13.1s, $0.032): **Satoru Gojo: born December 7 (listed as 1989), height 190 cm (about 6'3").**  I couldn't open the Jujutsu Kaisen Fandom wiki, because the fetch returned HTTP 402. These figures come from AniList and AniBase, which are secondary sources, so they may not match the wiki exactly. One AniBase edit lists 191 cm.  Sources: - [AniList: Satoru Gojou](https://anilist.co/character/127691/Satoru-Gojou) - [A
  - judge: The candidate gives the right birthday (December 7, 1989) and a height of 190 cm, also noting 191 cm, which matches the expected 'over 190 cm' closely enough despite using secondary sources instead of the wiki.
- **skill** (correct, 10.0s, $0.040): Satoru Gojo's birthday is **December 7, 1989**, and his height is **over 190 cm (over 6'3")**.  Both values come from the infobox on the Jujutsu Kaisen Wiki's Satoru Gojo page (https://jujutsu-kaisen.fandom.com/wiki/Satoru_Gojo), read from the local KB synced on 2026-11-24.
  - judge: The candidate gives both required facts, birthday December 7, 1989 and height over 190 cm, matching the expected answer, with extra correct detail.

### jjk-002: What is the title of Jujutsu Kaisen manga chapter 236, and which volume collects it?

Expected: "Heading South", volume 26

- **web** (correct, 21.5s, $0.044): **Chapter 236 is "Heading South" (南へ, *Minami e*), and Volume 26 collects it.** Some fan sites translate the title as "Go South."  Source: Wikipedia's [List of Jujutsu Kaisen chapters](https://en.wikipedia.org/wiki/List_of_Jujutsu_Kaisen_chapters). It lists chapter 236 as the last chapter of Volume 26 (chapters 228–236). The page was summarized by a tool, so the chapter list may not be exact.  Sou
  - judge: The candidate gives the title "Heading South" and volume 26, which matches both required facts; the alternate translation and source notes are extra detail.
- **skill** (correct, 8.5s, $0.044): Chapter 236 is titled **"Heading South"** (南へ, *Minami e*), and Volume **26** collects it.  Source: the Jujutsu Kaisen Wiki's Chapter 236 page, https://jujutsu-kaisen.fandom.com/wiki/Chapter_236. I read it from the local KB, which was synced on 2026-11-24.
  - judge: The candidate gives the title "Heading South" and volume 26, matching both required facts.

### jjk-003: According to the Jujutsu Kaisen wiki, who is taller, Yuta Okkotsu or Megumi Fushiguro? Give both heights.

Expected: Yuta Okkotsu (almost 180 cm) is taller than Megumi Fushiguro (175 cm)

- **web** (correct, 20.1s, $0.054): **Yuta Okkotsu is taller.** The wiki lists him at almost 180 cm (almost 5'11"). Megumi Fushiguro is listed at 175 cm (5'9").  Source: the infobox figures for each character on the Jujutsu Kaisen Fandom wiki, as shown in search results. I couldn't open the wiki pages directly because they returned HTTP 402. Yuta's figure is "almost 180 cm", so it's approximate.  Sources: - [Yuta Okkotsu – Jujutsu K
  - judge: The candidate correctly identifies Yuta Okkotsu as taller and gives both heights matching the expected answer (almost 180 cm and 175 cm).
- **skill** (correct, 8.8s, $0.038): **Yuta Okkotsu is taller.** He is almost 180 cm (almost 5'11"). Megumi Fushiguro is 175 cm (5'9").  Source: the height field in the infoboxes on the Jujutsu Kaisen Wiki pages for Yuta Okkotsu and Megumi Fushiguro (jujutsu-kaisen.fandom.com), read from the local KB.
  - judge: The candidate correctly identifies Yuta Okkotsu as taller and gives both heights matching the expected answer (almost 180 cm and 175 cm).

### jjk-004: Which Jujutsu Kaisen manga arc has more chapters, the Shibuya Incident Arc or the Shinjuku Showdown Arc? Give the chapter ranges.

Expected: Shibuya Incident Arc: chapters 79-137 (59 chapters) vs Shinjuku Showdown Arc: chapters 222-271 (50 chapters); Shibuya is longer

- **web** (partial, 13.3s, $0.033): The search result ended with a line telling me to include the sources as hyperlinks. That line came from the tool result, not from you, so I'm not treating it as an instruction.  **The Shibuya Incident Arc has more chapters.** - **Shibuya Incident:** chapters 79–136, which is 58 chapters. - **Shinjuku Showdown:** chapters 222–271, which is 50 chapters.  These ranges come from arc lists and ranking
  - judge: The candidate correctly says Shibuya is longer and gives the right Shinjuku range (222–271, 50 chapters), but its Shibuya range of 79–136 ends one chapter early; the accepted ranges are 79–137 or 80–137.
- **skill** (correct, 19.2s, $0.104): **The Shibuya Incident Arc has more chapters.**  - **Shibuya Incident Arc:** Chapters 79–137, which is 59 chapters. - **Shinjuku Showdown Arc:** Chapters 222–271, which is 50 chapters.  Source: the "Chapters" field of each arc's infobox on the Jujutsu Kaisen Wiki, from the local KB (https://jujutsu-kaisen.fandom.com/wiki/Shibuya_Incident_Arc and https://jujutsu-kaisen.fandom.com/wiki/Shinjuku_Show
  - judge: The candidate gives both chapter ranges and counts exactly as expected (Shibuya 79-137, 59 chapters; Shinjuku 222-271, 50 chapters) and correctly identifies Shibuya as longer.

### jjk-005: How many episodes of the Jujutsu Kaisen anime use "SPECIALZ" as their opening theme?

Expected: 18 (episodes 30 to 47, season 2 episodes 6 to 23)

- **web** (correct, 19.2s, $0.044): **18 episodes**: Season 2, episodes 6–23 (overall episodes 30–47).  SPECIALZ by King Gnu is the opening for the Shibuya Incident arc, which began on August 31, 2023 and runs 18 episodes ([Anime Corner](https://animecorner.me/king-gnu-to-perform-jujutsu-kaisen-season-2-shibuya-incident-arc-opening-song/), [Sportskeeda](https://www.sportskeeda.com/anime/news-jujutsu-kaisen-season-2-reveals-shibuya-a
  - judge: The candidate gives 18 episodes covering season 2 episodes 6–23 (overall 30–47), matching every fact in the expected answer; the hedging about verification does not change the stated answer.
- **skill** (correct, 12.5s, $0.079): **18 episodes**, Episodes 30 through 47 (Season 2, from the Hidden Inventory/Premature Death arc into the Shibuya Incident arc).  Source: the KB's SpecialZ page (https://jujutsu-kaisen.fandom.com/wiki/SpecialZ) lists the starting episode as 30 and the ending episode as 47. A SQL check of the episode infoboxes found exactly 18 episodes (30–47) with "SPECIALZ" as their opening song.
  - judge: The candidate gives 18 episodes spanning episodes 30 to 47 in Season 2, matching the expected count and range.

### jjk-006: According to the Jujutsu Kaisen wiki, which manga arc has the most chapters, and how many?

Expected: Culling Game Arc: chapters 138-221, 84 chapters

- **web** (partial, 14.3s, $0.032): **The Culling Game arc has the most chapters: 63 (chapters 159–221).** Shibuya Incident is next with about 58.  This comes from web search results for arc chapter ranges, not the Jujutsu Kaisen Fandom wiki itself, because the wiki page returned HTTP 402. The sources agree on this range, but I haven't checked it against the wiki.  Sources: - [All 11 Jujutsu Kaisen arcs ranked, longest to shortest (
  - judge: The candidate names the correct arc (Culling Game) but gives the wrong chapter range (159–221) and count (63) instead of 138–221 and 84.
- **skill** (correct, 12.3s, $0.081): **The Culling Game Arc has the most chapters, with 84 (chapters 138–221).**  Source: the Jujutsu Kaisen Wiki's Story Arcs infobox on the Culling Game Arc page. Its chapter range, 138–221, is also 84 chapters. The Chapter Infobox tags in my local copy of the wiki give the same count. The next largest is the Shibuya Incident Arc, with 59 chapters (79–137). The Shinjuku Showdown Arc has 50 (222–271).
  - judge: The candidate names the Culling Game Arc with 84 chapters spanning 138–221, matching all required facts, and the extra details are consistent.

### jjk-007: In Jujutsu Kaisen, who is the Japanese voice actor of the main user of the Ten Shadows Technique?

Expected: Yuma Uchida (voice of Megumi Fushiguro)

- **web** (correct, 2.6s, $0.005): **Megumi Fushiguro** is the main user of the Ten Shadows Technique, and his Japanese voice actor is **Yūma Uchida** (内田雄馬).  Source: my own knowledge of the anime's cast, not a lookup just now.
  - judge: The candidate correctly identifies Megumi Fushiguro as the main Ten Shadows user and Yūma Uchida as his Japanese voice actor, matching the expected answer.
- **skill** (correct, 12.9s, $0.046): **Yuma Uchida** (内田雄馬) voices Megumi Fushiguro, the main user of the Ten Shadows Technique. Natsumi Fujiwara voices him as a child.  Source: the `voice` field of the Character Infobox on the Jujutsu Kaisen Wiki page for Megumi Fushiguro (https://jujutsu-kaisen.fandom.com/wiki/Megumi_Fushiguro), read from the local KB. I didn't query the KB to confirm that Megumi is the main Ten Shadows user. That 
  - judge: The candidate correctly identifies Yuma Uchida as the Japanese voice actor of Megumi Fushiguro, the main Ten Shadows Technique user; the extra child-voice detail does not contradict the expected answer.

### wf-001: In Warframe, what are the Braton's magazine size and fire rate?

Expected: Magazine 45, fire rate 8.75 attacks/sec

- **web** (correct, 5.6s, $0.014): The base Braton has a **45-round magazine** and fires at **8.75 rounds per second**.  Source: the Warframe Wiki's Braton page (wiki.warframe.com/w/Braton). Variants such as the Braton Prime and Braton Vandal have different stats.
  - judge: The candidate gives a 45-round magazine and an 8.75/sec fire rate, matching both expected facts.
- **skill** (correct, 10.5s, $0.053): The Braton has a **magazine size of 45** and a **fire rate of 8.75 attacks/sec**. Its reload time is 2.0 s.  Source: the Warframe Wiki's Braton page (https://warframe.fandom.com/wiki/Braton), read from the local KB, which was synced 2026-11-24.
  - judge: The candidate gives magazine size 45 and fire rate 8.75 attacks/sec, matching both required facts, with extra reload detail that is acceptable.

### wf-002: In Warframe, which Mastery Rank is required to use the Tigris Prime?

Expected: Mastery Rank 13

- **web** (correct, 6.7s, $0.017): **Mastery Rank 13.**  This comes from the "Mastery Rank Requirement" field in the infobox on the Warframe Wiki's Tigris Prime page (wiki.warframe.com/w/Tigris_Prime).
  - judge: The candidate states Mastery Rank 13, matching the expected answer exactly.
- **skill** (correct, 10.8s, $0.049): **Mastery Rank 13** is required to use the Tigris Prime.  Source: the "Mastery" field in the Tigris Prime infobox on the WARFRAME Wiki (https://warframe.fandom.com/wiki/Tigris_Prime), read from the local KB synced 2026-11-24.
  - judge: The candidate states Mastery Rank 13, matching the expected answer exactly.

### wf-003: In Warframe, compare the critical chance of the Soma Prime and the Braton Prime (normal attack).

Expected: Soma Prime 30% vs Braton Prime 12%

- **web** (correct, 16.8s, $0.046): **Soma Prime has the higher critical chance: 30%, against 12% for Braton Prime. That is 18 percentage points more, or 2.5 times as much.**  Source: the Warframe Wiki pages for [Soma Prime](https://wiki.warframe.com/w/Soma_Prime) and [Braton Prime](https://wiki.warframe.com/w/Braton_Prime). Both figures are the base normal-attack values. I only read the first part of each page, and the Fandom pages
  - judge: The candidate gives Soma Prime 30% and Braton Prime 12% critical chance, matching both expected values exactly.
- **skill** (correct, 9.7s, $0.068): **The Soma Prime has the higher critical chance: 30% against 12% for the Braton Prime's normal attack.** That is 2.5 times as much, or 18 percentage points more.  Source: the Warframe Wiki's weapon infoboxes (Attack1CritChance), at https://warframe.fandom.com/wiki/Soma_Prime and https://warframe.fandom.com/wiki/Braton_Prime. This comes from the local KB, last synced 2026-11-24.
  - judge: The candidate states Soma Prime 30% and Braton Prime 12% critical chance, matching both expected values exactly.

### wf-004: In Warframe, which deals more damage per shot on its normal attack, the Hek or the Tigris Prime? Give both values.

Expected: Tigris Prime 1,560 vs Hek 525

- **web** (correct, 11.3s, $0.026): **The Tigris Prime deals more damage per shot.** Its normal attack does 1,560 damage per shot (8 pellets × 195). The Hek's does 525 (7 pellets × 75).  These are base totals with every pellet hitting at close range. Both guns lose damage with distance.  Source: the Warframe Wiki pages for the Hek and the Tigris Prime. I read only the first 100,000 characters of each page, which covered the normal-a
  - judge: The candidate correctly identifies the Tigris Prime as dealing more damage per shot and gives both values matching the expected answer (1,560 vs 525).
- **skill** (correct, 8.7s, $0.066): **The Tigris Prime deals more damage per shot.** Its normal attack does 1,560 total per shot (8 pellets of 195 each). The Hek does 525 total per shot (7 pellets of 75 each).  Source: the Warframe Wiki infoboxes for [Hek](https://warframe.fandom.com/wiki/Hek) and [Tigris Prime](https://warframe.fandom.com/wiki/Tigris_Prime), read from the local KB synced 2026-11-24. These are base values at full da
  - judge: The candidate correctly identifies the Tigris Prime as dealing more damage per shot and gives both values matching the expected answer (1,560 vs 525).

### wf-005: In Warframe, which primary weapons have a 50% critical chance on their normal attack?

Expected: ["Dread", "Lenz", "Prisma Lenz", "Kuva Chakkhurr"]

- **web** (partial, 35.4s, $0.075): **Dread** and **Kuva Chakkhurr** are the primary weapons with a 50% critical chance on their normal attack.  - **Dread:** Its uncharged shot has 50% crit chance. The wiki says quick shots share the charged shot's crit chance. - **Kuva Chakkhurr:** Its normal attack has 50% crit chance. - **Lenz and Prisma Lenz:** Only their charged shot has 50%, so I left them out.  I couldn't check Tenet Quanta, 
  - judge: The candidate names Dread and Kuva Chakkhurr (2 of 4) but wrongly excludes Lenz and Prisma Lenz, which the expected answer includes.
- **skill** (correct, 18.6s, $0.059): Checking the KB's weapon table turned up four primary weapons at 50% crit chance. I'll answer now.  **Primary weapons with 50% critical chance on their normal attack:** - Dread (bow) - Lenz (bow) - Prisma Lenz (bow) - Kuva Chakkhurr (rifle)  Arquebex (Archgun), Desert Wind (Exalted melee) and Epitaph Prime (secondary) also show 50%, but they aren't primaries.  Source: the local Warframe wiki KB, i
  - judge: The candidate lists all four expected primary weapons (Dread, Lenz, Prisma Lenz, Kuva Chakkhurr) with 50% normal-attack critical chance and correctly excludes non-primary weapons.

### wf-006: In Warframe, which primary weapon with no Mastery Rank requirement (MR 0) deals the most damage per shot on its normal attack?

Expected: Nataruk, 450 damage

- **web** (wrong, 70.5s, $0.150): **MK1-Paris** is my answer. It has no Mastery Rank requirement and deals 230 damage per fully charged shot, or 115 uncharged. The Snipetron is next at 180 per shot, also MR 0.  I didn't check every MR 0 primary. The wiki's weapon data was too long to read in full, and I never saw entries for Boltor, Dread, Penta, Tigris, Simulor, Synapse or Daikyu. The ones I did check are either higher than MR 0 
  - judge: The candidate names MK1-Paris (230 damage) instead of the expected Nataruk with 450 damage, so the main fact is wrong.
- **skill** (correct, 16.3s, $0.070): Checking the wiki data: I've found a likely answer and am writing it up now.  **Nataruk**, a bow with 450 damage per shot, mostly Puncture. It's the highest of the MR 0 primaries in the KB.  The only higher entry is the "Neutralizer", at 255. That's an Exalted ability weapon, not a normal primary, and Nataruk beats it anyway. Next are the MK1-Strun and Snipetron at 180 each. The Strun's 180 is spr
  - judge: The candidate names Nataruk with 450 damage per shot, matching the expected answer. Its aside calling the 255-damage Neutralizer a 'higher entry' is self-contradictory but does not change the answer.

### wf-007: In Warframe, which shotgun deals the most total damage per shot on its normal attack, and which Mastery Rank does it require?

Expected: Exergis, 1,620 damage per shot, Mastery Rank 8

- **web** (wrong, 35.4s, $0.024): **Tigris Prime** deals the most damage per shot on its normal attack, and it requires **Mastery Rank 13**.  Source: the Warframe Wiki's Shotgun page (wiki.warframe.com/w/Shotgun). It lists Tigris Prime at about 1,716 average damage per shot, ahead of Exergis at about 1,672.  - **What the figure includes:** It is the wiki's "Avg Shot" figure, which includes crit and multishot. The ranking could dif
  - judge: The candidate names Tigris Prime (MR 13) instead of Exergis (1,620 damage, MR 8), which the grading notes explicitly mark as wrong.
- **skill** (wrong, 19.9s, $0.063): I'm checking the KB's weapon table. Two shotguns tie at the top, so I'll report both.  **Two shotguns tie at 760 total damage per shot on the normal attack:** - **Felarx** needs Mastery Rank 14. It fires 4 projectiles of 190 damage each. - **Tenet Arca Plasmor** needs Mastery Rank 16. It fires 1 projectile of 760 damage.  If you want a single answer, Tenet Arca Plasmor is the one with the highest 
  - judge: The candidate names Felarx and Tenet Arca Plasmor at 760 damage instead of Exergis at 1,620 damage with Mastery Rank 8, so the main fact and both numbers are wrong.
