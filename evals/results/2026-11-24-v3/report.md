# Eval results (2026-11-24-v3)

Answering model: `sonnet` through `claude -p --restricted`. `web` = WebSearch + WebFetch only; `skill` = the same plus fandom-kb with pre-built KBs. Score: correct 1, partial 0.5, wrong 0.

| | web | skill |
|---|---|---|
| **overall** | 62% | 98% |
| lookup | 67% | 100% |
| compare | 92% | 100% |
| aggregate | 33% | 92% |
| multi-hop | 50% | 100% |
| battlenations | 43% | 93% |
| jujutsu-kaisen | 79% | 100% |
| warframe | 64% | 100% |
| avg cost | $0.053 | $0.061 |
| avg time | 24s | 13s |
| avg turns | 5.4 | 6.0 |

Skill arm used the knowledge base on **20/21** questions: accuracy 98% when it did, 100% when it didn't.

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
| jjk-001 | lookup | According to the Jujutsu Kaisen wiki, what are Satoru Gojo's birthday and height? | partial | correct |
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
| wf-007 | multi-hop | In Warframe, which shotgun deals the most total damage per shot on its normal attack, and which Mastery Rank does it require? | wrong | correct |

## Verdicts

### bn-001: In Battle Nations, what is the Riot Trooper's HP at each rank?

Expected: 70, 85, 105, 120, 140, 155 (ranks 1 to 6)

- **web** (wrong, 25.0s, $0.056): Verified the HP table on the Miraheze page. I'm giving the final answer now.  **Riot Trooper HP by rank:** R1 60, R2 65, R3 70, R4 80, R5 85, R6 90.  Source: the Statistics table on the Battle Nations Miraheze wiki's Riot Trooper page. The Fandom wiki gave the same figures in search results, but Fandom returned HTTP 402 when I fetched it, so I couldn't open that page myself.  Sources: - [Riot Troo
  - judge: The candidate gives 60, 65, 70, 80, 85, 90 instead of the expected 70, 85, 105, 120, 140, 155, and the notes accept that alternate set only when the answer points out the page's HP/armor inconsistency, which this answer does not do.
- **skill** (correct, 12.5s, $0.048): **Riot Trooper HP by rank:** R1 60, R2 65, R3 70, R4 80, R5 85, R6 90.  The page's stats box has the HP and armor rows swapped. The row labeled `hp` reads 70/85/105/120/140/155. The 4.19.0 patch note lists those same numbers as the new armor values (R1 60→70 through R6 115→155). The infobox shows HP 90 and Armor 155, which matches the HP list above. I treated the row labeled `armor` (60/65/70/80/8
  - judge: The candidate gives the alternate accepted values 60, 65, 70, 80, 85, 90 and explicitly explains the page's HP/armor inconsistency, noting the literal stats-box reading would be 70/85/105/120/140/155.

### bn-002: In Battle Nations, which building, at which level, is required to train the Sniper?

Expected: Barracks level 5

- **web** (partial, 19.0s, $0.052): **Barracks, level 4.** That trains the Sharpshooter, which is the game's basic sniper unit and the closest match to "Sniper". It also needs player level 16.  The higher-tier sniper, the Marksman, needs Barracks level 6 and player level 28.  I couldn't open the wiki pages directly, because Fandom returned an HTTP 402 error. These figures come from search-result summaries of the [Battle Nations Wiki
  - judge: The candidate names the right building (Barracks) but gives level 4 instead of the expected level 5, and none of the alternative levels it mentions (6 for Marksman) match either.
- **skill** (correct, 9.6s, $0.043): The Sniper is trained in the **Barracks at level 5**, and the SpecOps Center must also be built.  Source: the Sniper page on the Battle Nations Wiki (https://battlenations.fandom.com/wiki/Sniper). Its infobox lists "Barracks level 5" as the building required and "SpecOps Center" as another requirement. The KB was synced on 2026-11-24.
  - judge: The candidate states the Sniper is trained in the Barracks at level 5, matching the expected answer, and the extra SpecOps Center detail does not contradict it.

### bn-003: In Battle Nations, which has more HP at rank 6, the Heavy Tank or the War Mammoth, and what are both values?

Expected: War Mammoth: 450 HP vs Heavy Tank: 340 HP at rank 6

- **web** (correct, 22.1s, $0.073): **The War Mammoth has more HP at rank 6: 450, against 340 for the Heavy Tank.**  Source: the Battle Nations wiki pages for [War Mammoth](https://battlenations.fandom.com/wiki/War_Mammoth) and [Heavy Tank](https://battlenations.fandom.com/wiki/Heavy_Tank), as quoted in a web search result. The Miraheze copies ([War Mammoth](https://battlenations.miraheze.org/wiki/War_Mammoth), [Heavy Tank](https://
  - judge: The candidate correctly identifies the War Mammoth as having more HP at rank 6 and gives both values matching the expected answer (450 vs 340).
- **skill** (correct, 7.6s, $0.036): The **War Mammoth** has more HP at rank 6, with 450 against the Heavy Tank's 340.  Source: the `hp` per-rank lists in the local Battle Nations Wiki KB (synced 2026-11-24). The Heavy Tank's list is 225; 250; 270; 295; 315; 340. The War Mammoth's is 300; 330; 360; 390; 420; 450. The pages are battlenations.fandom.com/wiki/Heavy_Tank and battlenations.fandom.com/wiki/War_Mammoth.
  - judge: The candidate correctly identifies the War Mammoth as having more HP at rank 6 and gives both values matching the expected answer (450 vs 340).

### bn-004: In Battle Nations, how much gold does it cost to train a Sniper and a Riot Trooper? Which is more expensive?

Expected: Sniper 8,000 gold, Riot Trooper 2,250 gold: the Sniper is more expensive

- **web** (correct, 34.3s, $0.063): **Sniper: 8,000 gold. Riot Trooper: 2,250 gold. The Sniper is more expensive, by roughly 3.5 times.**  These are the base costs at each unit's minimum Barracks level: level 5 for the Sniper and level 3 for the Riot Trooper. The cost falls as the Barracks level rises. For example, the Sniper drops to 5,600 gold at Barracks level 15.  One search summary gave different Riot Trooper figures (1,326 gol
  - judge: The candidate states Sniper 8,000 gold and Riot Trooper 2,250 gold and correctly identifies the Sniper as more expensive, matching all required facts.
- **skill** (correct, 9.2s, $0.053): **The Sniper costs 8,000 gold to train and the Riot Trooper costs 2,250, so the Sniper is more expensive.** That's about 3.6 times the price.  Source: the "Cost → BuildCost" sections of the Battle Nations Wiki pages for [Sniper](https://battlenations.fandom.com/wiki/Sniper) and [Riot Trooper](https://battlenations.fandom.com/wiki/Riot_Trooper). These come from the local KB, last synced 2026-11-24.
  - judge: The candidate gives Sniper 8,000 gold and Riot Trooper 2,250 gold and correctly identifies the Sniper as more expensive, matching all expected facts with extra detail.

### bn-005: In Battle Nations, which 5 player units have the highest HP at their maximum rank? Give the HP values.

Expected: Portable Wall 900, Tamed Mammoth Matriarch 825, Specimen i02 "Apex Mauler" 780, Monster Grouper 775, Battleship Mammoth-Class 740

- **web** (wrong, 45.4s, $0.099): I couldn't find a reliable answer, so I can't name the top 5 units.  - **What I couldn't get:** The Battle Nations Fandom wiki returned HTTP 402 (Payment Required), so I couldn't read the unit pages. bn-db.com returned no table. The Miraheze wiki pages had no HP figures. - **Partial figures from search snippets:**   - Imperial Peacemonger: 360 HP at rank 6.   - Noble Champion: 395 HP.   - Total Wa
  - judge: The candidate explicitly says it couldn't find the answer and names none of the expected top-5 units or their HP values.
- **skill** (partial, 22.2s, $0.116): The top 5 player units by HP at max rank are:  1. Tamed Mammoth Matriarch: 825 2. Monster Grouper: 775 3. Battleship Mammoth-Class: 740 4. Bigfoot: 720 (tied) 5. Bigfoot Shaman: 720 (tied)  I treated the "Ignorable-Defense" entries as structures and left them out. These are Portable Wall at 900, Buoy at 725 and Portable Electric Fence at 675. If you count them, Portable Wall takes first place and 
  - judge: The candidate matches neither accepted ranking: it drops Portable Wall and Apex Mauler from the expected top 5 (though it names both with correct HP), and it keeps Tamed Mammoth Matriarch, which the alternative reading excludes, so Power Boat is missing and the order is shifted; it gets Matriarch 825, Monster Grouper 775 and Battleship 740 right against the primary answer, and 4 of 5 right against the alternative.

### bn-006: In Battle Nations, how many units require the Barracks (any level) to be trained, according to the wiki?

Expected: 61

- **web** (wrong, 30.0s, $0.063): I couldn't get a reliable count. The Battle Nations wiki blocked my direct fetches (HTTP 402), and the shell and grep tools were disabled, so I couldn't check your local `battlenations.yaml`.  Search results from the wiki showed at least 10 Barracks units: Grenadier, Shock Trooper, Arsonist, Mortar Team, Ranger, Saboteur, Armadillo, Bazooka Squad, Demolitionist and Commando. That is only a partial
  - judge: The candidate says it couldn't get a reliable count and offers only a lower bound of 10, which is far outside the 55–67 partial range and not the expected 61.
- **skill** (correct, 13.2s, $0.088): **61 units** require the Barracks, at levels 1 to 11.  Source: the Battle Nations wiki's `{{UnitProfile}}` infobox `building_required` field, queried from the local KB. I counted rows whose value starts with "Barracks level". I didn't check for duplicate unit pages.
  - judge: The candidate's count of 61 units requiring the Barracks matches the expected answer exactly.

### bn-007: In Battle Nations, among the units trained at the Barracks, which unit has the attack with the highest maximum damage? Name the attack and its damage range.

Expected: Railgun Sniper, High Velocity Bolt, 150-250 damage (Piercing)

- **web** (partial, 50.5s, $0.101): **Railgun Sniper** has the highest max damage. Its attack is **High Velocity Bolt**, which does **225–375 piercing damage** at Rank 6 (max).  Source: the Battle Nations Miraheze wiki. Its Units page lists the Barracks units, and its Railgun Sniper page gives the attack data. I didn't check every Barracks unit's attack table. I checked Big Game Hunter (96–144 at max rank) as a comparison, and I ass
  - judge: The unit (Railgun Sniper), attack (High Velocity Bolt), and damage type (Piercing) are correct, but the damage range is 225–375 at Rank 6 rather than the expected 150–250.
- **skill** (correct, 12.7s, $0.088): **Railgun Sniper**'s **High Velocity Bolt** has the highest maximum damage of any Barracks unit: **150–250** Piercing damage. The next highest is Guerrilla's C4 at 144–216.  Source: the local Battle Nations Wiki knowledge base. I joined the unit profile (Barracks as the required building) to the attack box data and sorted by maximum damage. The page is https://battlenations.fandom.com/wiki/Railgun
  - judge: The candidate names Railgun Sniper, the High Velocity Bolt attack, and its 150–250 Piercing damage range, which matches every required fact.

### jjk-001: According to the Jujutsu Kaisen wiki, what are Satoru Gojo's birthday and height?

Expected: December 7, 1989; over 190 cm

- **web** (partial, 13.1s, $0.032): **Satoru Gojo: born December 7 (listed as 1989), height 190 cm (about 6'3").**  I couldn't open the Jujutsu Kaisen Fandom wiki, because the fetch returned HTTP 402. These figures come from AniList and AniBase, which are secondary sources, so they may not match the wiki exactly. One AniBase edit lists 191 cm.  Sources: - [AniList: Satoru Gojou](https://anilist.co/character/127691/Satoru-Gojou) - [A
  - judge: The birthday (December 7, 1989) matches, but the candidate gives the height as exactly 190 cm rather than over 190 cm, mentioning 191 cm only as an alternate secondary-source figure.
- **skill** (correct, 8.7s, $0.038): Satoru Gojo's birthday is **December 7, 1989**. His height is **over 190 cm (over 6'3")**.  Source: the Character Infobox on the Jujutsu Kaisen Wiki page for Satoru Gojo (https://jujutsu-kaisen.fandom.com/wiki/Satoru_Gojo), read from the local KB synced 2026-11-24.
  - judge: The candidate gives both required facts correctly: birthday December 7, 1989 and height over 190 cm.

### jjk-002: What is the title of Jujutsu Kaisen manga chapter 236, and which volume collects it?

Expected: "Heading South", volume 26

- **web** (correct, 21.5s, $0.044): **Chapter 236 is "Heading South" (南へ, *Minami e*), and Volume 26 collects it.** Some fan sites translate the title as "Go South."  Source: Wikipedia's [List of Jujutsu Kaisen chapters](https://en.wikipedia.org/wiki/List_of_Jujutsu_Kaisen_chapters). It lists chapter 236 as the last chapter of Volume 26 (chapters 228–236). The page was summarized by a tool, so the chapter list may not be exact.  Sou
  - judge: The candidate gives the title as "Heading South" and says volume 26 collects it, which matches both required facts; the extra detail does not contradict them.
- **skill** (correct, 11.7s, $0.051): Chapter 236 is titled **"Heading South"** (南へ, *Minami e*), and **Volume 26** collects it.  Source: the Jujutsu Kaisen Wiki's Chapter 236 page, https://jujutsu-kaisen.fandom.com/wiki/Chapter_236. The local KB was synced 2026-11-24.
  - judge: The candidate gives the title "Heading South" and volume 26, matching both required facts.

### jjk-003: According to the Jujutsu Kaisen wiki, who is taller, Yuta Okkotsu or Megumi Fushiguro? Give both heights.

Expected: Yuta Okkotsu (almost 180 cm) is taller than Megumi Fushiguro (175 cm)

- **web** (correct, 20.1s, $0.054): **Yuta Okkotsu is taller.** The wiki lists him at almost 180 cm (almost 5'11"). Megumi Fushiguro is listed at 175 cm (5'9").  Source: the infobox figures for each character on the Jujutsu Kaisen Fandom wiki, as shown in search results. I couldn't open the wiki pages directly because they returned HTTP 402. Yuta's figure is "almost 180 cm", so it's approximate.  Sources: - [Yuta Okkotsu – Jujutsu K
  - judge: The candidate correctly identifies Yuta Okkotsu as taller and gives both heights matching the expected answer (almost 180 cm and 175 cm).
- **skill** (correct, 9.5s, $0.035): **Yuta Okkotsu is taller.** He is almost 180 cm (almost 5'11"), and Megumi Fushiguro is 175 cm (5'9").  Source: the height fields in the infoboxes on the Jujutsu Kaisen Wiki pages for [Yuta Okkotsu](https://jujutsu-kaisen.fandom.com/wiki/Yuta_Okkotsu) and [Megumi Fushiguro](https://jujutsu-kaisen.fandom.com/wiki/Megumi_Fushiguro). I read them from the local KB, which was last synced 2026-11-24.
  - judge: The candidate correctly identifies Yuta Okkotsu as taller and gives both heights matching the expected answer (almost 180 cm and 175 cm).

### jjk-004: Which Jujutsu Kaisen manga arc has more chapters, the Shibuya Incident Arc or the Shinjuku Showdown Arc? Give the chapter ranges.

Expected: Shibuya Incident Arc: chapters 79-137 (59 chapters) vs Shinjuku Showdown Arc: chapters 222-271 (50 chapters); Shibuya is longer

- **web** (partial, 13.3s, $0.033): The search result ended with a line telling me to include the sources as hyperlinks. That line came from the tool result, not from you, so I'm not treating it as an instruction.  **The Shibuya Incident Arc has more chapters.** - **Shibuya Incident:** chapters 79–136, which is 58 chapters. - **Shinjuku Showdown:** chapters 222–271, which is 50 chapters.  These ranges come from arc lists and ranking
  - judge: The candidate correctly says Shibuya is longer and gets Shinjuku right (222–271, 50 chapters), but gives Shibuya as 79–136 instead of 79–137 (or 80–137), so its range does not match.
- **skill** (correct, 15.4s, $0.073): The Shibuya Incident Arc has more chapters.  - **Shibuya Incident Arc:** Chapters 79–137, which is 59 chapters. - **Shinjuku Showdown Arc:** Chapters 222–271, which is 50 chapters.  Source: the "Story Arcs Infobox" on each arc's page in the local Jujutsu Kaisen Wiki knowledge base. The pages are https://jujutsu-kaisen.fandom.com/wiki/Shibuya_Incident_Arc and https://jujutsu-kaisen.fandom.com/wiki/
  - judge: The candidate gives both chapter ranges and counts exactly as expected (Shibuya 79–137, 59 chapters; Shinjuku 222–271, 50 chapters) and correctly identifies Shibuya as longer.

### jjk-005: How many episodes of the Jujutsu Kaisen anime use "SPECIALZ" as their opening theme?

Expected: 18 (episodes 30 to 47, season 2 episodes 6 to 23)

- **web** (correct, 19.2s, $0.044): **18 episodes**: Season 2, episodes 6–23 (overall episodes 30–47).  SPECIALZ by King Gnu is the opening for the Shibuya Incident arc, which began on August 31, 2023 and runs 18 episodes ([Anime Corner](https://animecorner.me/king-gnu-to-perform-jujutsu-kaisen-season-2-shibuya-incident-arc-opening-song/), [Sportskeeda](https://www.sportskeeda.com/anime/news-jujutsu-kaisen-season-2-reveals-shibuya-a
  - judge: The candidate gives 18 episodes covering season 2 episodes 6–23 (overall 30–47), matching every fact in the expected answer; the hedging about unverified range does not change the stated facts.
- **skill** (correct, 16.9s, $0.072): **18 episodes**: Episodes 30 through 47, the second-season Shibuya Incident run.  Source: the "SpecialZ" page on the Jujutsu Kaisen Wiki (https://jujutsu-kaisen.fandom.com/wiki/SpecialZ) gives a starting episode of 30 and an ending episode of 47. I counted the range inclusively and didn't check each episode page, though the ones I saw in search results (30–35 and 44) list SPECIALZ as the opening.
  - judge: The candidate gives 18 episodes spanning episodes 30 to 47, matching the expected count and range; the season 2 numbering is extra detail not required to be restated.

### jjk-006: According to the Jujutsu Kaisen wiki, which manga arc has the most chapters, and how many?

Expected: Culling Game Arc: chapters 138-221, 84 chapters

- **web** (partial, 14.3s, $0.032): **The Culling Game arc has the most chapters: 63 (chapters 159–221).** Shibuya Incident is next with about 58.  This comes from web search results for arc chapter ranges, not the Jujutsu Kaisen Fandom wiki itself, because the wiki page returned HTTP 402. The sources agree on this range, but I haven't checked it against the wiki.  Sources: - [All 11 Jujutsu Kaisen arcs ranked, longest to shortest (
  - judge: The candidate names the correct arc (Culling Game) but gives the wrong chapter range and count (159–221, 63 chapters instead of 138–221, 84 chapters).
- **skill** (correct, 15.8s, $0.079): **The Culling Game Arc has the most chapters, with 84 (Chapters 138–221).**  Source: the Jujutsu Kaisen Wiki's Story Arcs Infobox on the [Culling Game Arc page](https://jujutsu-kaisen.fandom.com/wiki/Culling_Game_Arc). The count of 84 matches the number of chapter pages the wiki tags with that arc. The next largest are the Shibuya Incident Arc (59 chapters, 79–137) and the Shinjuku Showdown Arc (5
  - judge: The candidate names the Culling Game Arc with 84 chapters spanning 138–221, matching every required fact in the expected answer.

### jjk-007: In Jujutsu Kaisen, who is the Japanese voice actor of the main user of the Ten Shadows Technique?

Expected: Yuma Uchida (voice of Megumi Fushiguro)

- **web** (correct, 2.6s, $0.005): **Megumi Fushiguro** is the main user of the Ten Shadows Technique, and his Japanese voice actor is **Yūma Uchida** (内田雄馬).  Source: my own knowledge of the anime's cast, not a lookup just now.
  - judge: The candidate correctly identifies Megumi Fushiguro as the main Ten Shadows user and Yūma Uchida as his Japanese voice actor, matching the expected answer.
- **skill** (correct, 4.9s, $0.015): **Yuma Uchida** voices Megumi Fushiguro, the main user of the Ten Shadows Technique, in Japanese.  This is from my own knowledge of the anime's cast. I didn't check it against the wiki or the fandom-kb skill.
  - judge: The candidate correctly names Yuma Uchida as the Japanese voice actor of Megumi Fushiguro, the main Ten Shadows Technique user.

### wf-001: In Warframe, what are the Braton's magazine size and fire rate?

Expected: Magazine 45, fire rate 8.75 attacks/sec

- **web** (correct, 5.6s, $0.014): The base Braton has a **45-round magazine** and fires at **8.75 rounds per second**.  Source: the Warframe Wiki's Braton page (wiki.warframe.com/w/Braton). Variants such as the Braton Prime and Braton Vandal have different stats.
  - judge: The candidate states a 45-round magazine and 8.75 rounds per second fire rate, matching both expected facts.
- **skill** (correct, 11.0s, $0.050): **Braton:** magazine size is **45 rounds**, and fire rate is **8.75 attacks/sec**.  Source: the WARFRAME Wiki "Braton" page (https://warframe.fandom.com/wiki/Braton), from the local KB synced 2026-11-24. The 45-round magazine is the standard value. In Conclave (PvP) it is 30.
  - judge: The candidate gives magazine size 45 and fire rate 8.75 attacks/sec, matching both expected facts; the extra Conclave detail does not contradict them.

### wf-002: In Warframe, which Mastery Rank is required to use the Tigris Prime?

Expected: Mastery Rank 13

- **web** (correct, 6.7s, $0.017): **Mastery Rank 13.**  This comes from the "Mastery Rank Requirement" field in the infobox on the Warframe Wiki's Tigris Prime page (wiki.warframe.com/w/Tigris_Prime).
  - judge: The candidate states Mastery Rank 13, matching the expected answer exactly.
- **skill** (correct, 11.1s, $0.045): **Mastery Rank 13** is required to use the Tigris Prime.  Source: the `Mastery` field in the Tigris Prime infobox on the Warframe Wiki (https://warframe.fandom.com/wiki/Tigris_Prime). I read it from the local KB, which was last synced 2026-11-24.
  - judge: The candidate states Mastery Rank 13, matching the expected answer exactly.

### wf-003: In Warframe, compare the critical chance of the Soma Prime and the Braton Prime (normal attack).

Expected: Soma Prime 30% vs Braton Prime 12%

- **web** (correct, 16.8s, $0.046): **Soma Prime has the higher critical chance: 30%, against 12% for Braton Prime. That is 18 percentage points more, or 2.5 times as much.**  Source: the Warframe Wiki pages for [Soma Prime](https://wiki.warframe.com/w/Soma_Prime) and [Braton Prime](https://wiki.warframe.com/w/Braton_Prime). Both figures are the base normal-attack values. I only read the first part of each page, and the Fandom pages
  - judge: The candidate states Soma Prime 30% and Braton Prime 12% critical chance, matching both expected values exactly.
- **skill** (correct, 12.0s, $0.065): **The Soma Prime has the higher critical chance: 30%, against 12% for the Braton Prime.** That is 2.5 times as much, or 18 percentage points more. The Soma Prime also has the higher critical multiplier (3.0x against 2.0x).  These are the primary-fire (normal attack) values. The Soma Prime's second attack entry is 10% and the Braton Prime's is 30%. I took Attack 1 as the normal attack for both.  So
  - judge: The candidate gives Soma Prime 30% and Braton Prime 12% for the normal attack, matching the expected values; the extra multiplier and secondary-attack details do not contradict them.

### wf-004: In Warframe, which deals more damage per shot on its normal attack, the Hek or the Tigris Prime? Give both values.

Expected: Tigris Prime 1,560 vs Hek 525

- **web** (correct, 11.3s, $0.026): **The Tigris Prime deals more damage per shot.** Its normal attack does 1,560 damage per shot (8 pellets × 195). The Hek's does 525 (7 pellets × 75).  These are base totals with every pellet hitting at close range. Both guns lose damage with distance.  Source: the Warframe Wiki pages for the Hek and the Tigris Prime. I read only the first 100,000 characters of each page, which covered the normal-a
  - judge: The candidate correctly identifies the Tigris Prime as dealing more damage per shot and gives both values matching the expected answer (1,560 vs 525).
- **skill** (correct, 10.3s, $0.064): **The Tigris Prime deals more damage per shot.**  - **Tigris Prime:** 1,560 total per shot (8 pellets × 195). Its damage is 80% Slash. - **Hek:** 525 total per shot (7 pellets × 75). Its damage is 65% Puncture. - Per pellet, the Tigris Prime also leads, 195 to 75.  These are base values at full range, before falloff and mods. The source is the infobox data on the Warframe Wiki pages for [Hek](http
  - judge: The candidate correctly identifies the Tigris Prime as dealing more damage per shot and gives both values matching the expected answer (1,560 vs 525).

### wf-005: In Warframe, which primary weapons have a 50% critical chance on their normal attack?

Expected: ["Dread", "Lenz", "Prisma Lenz", "Kuva Chakkhurr"]

- **web** (partial, 35.4s, $0.075): **Dread** and **Kuva Chakkhurr** are the primary weapons with a 50% critical chance on their normal attack.  - **Dread:** Its uncharged shot has 50% crit chance. The wiki says quick shots share the charged shot's crit chance. - **Kuva Chakkhurr:** Its normal attack has 50% crit chance. - **Lenz and Prisma Lenz:** Only their charged shot has 50%, so I left them out.  I couldn't check Tenet Quanta, 
  - judge: The candidate names Dread and Kuva Chakkhurr correctly but explicitly excludes Lenz and Prisma Lenz, giving 2 of the 4 required weapons.
- **skill** (correct, 19.9s, $0.105): **Four primary weapons have 50% critical chance on their normal attack: Dread, Kuva Chakkhurr, Lenz and Prisma Lenz.** Dread and the two Lenz variants are bows. Kuva Chakkhurr is a rifle.  Source: the WARFRAME Wiki infobox data in the local KB (`attack1critchance = 50`, slot Primary), e.g. https://warframe.fandom.com/wiki/Lenz. The KB was synced 2026-11-24. This covers each weapon's first attack, 
  - judge: The candidate lists all four expected weapons (Dread, Lenz, Prisma Lenz, Kuva Chakkhurr) with no extras, and correctly restricts to the normal attack.

### wf-006: In Warframe, which primary weapon with no Mastery Rank requirement (MR 0) deals the most damage per shot on its normal attack?

Expected: Nataruk, 450 damage

- **web** (wrong, 70.5s, $0.150): **MK1-Paris** is my answer. It has no Mastery Rank requirement and deals 230 damage per fully charged shot, or 115 uncharged. The Snipetron is next at 180 per shot, also MR 0.  I didn't check every MR 0 primary. The wiki's weapon data was too long to read in full, and I never saw entries for Boltor, Dread, Penta, Tigris, Simulor, Synapse or Daikyu. The ones I did check are either higher than MR 0 
  - judge: The candidate names MK1-Paris (230 damage) instead of Nataruk (450 damage), so both the weapon and the damage figure are wrong.
- **skill** (correct, 17.7s, $0.051): Checking the Warframe KB's weapon table showed a clear top result, so I'm giving the answer now.  **Nataruk**, a primary bow, deals 450 damage per shot on its charged normal attack. Its mastery requirement is MR 0. The next highest MR 0 primaries are the Neutralizer (255) and the MK1-Strun and Snipetron (180 each).  Source: the local Warframe KB, queried through the `weaponinfoboxautomatic` table 
  - judge: The candidate names the Nataruk with 450 damage per shot, matching both required facts in the expected answer.

### wf-007: In Warframe, which shotgun deals the most total damage per shot on its normal attack, and which Mastery Rank does it require?

Expected: Exergis, 1,620 damage per shot, Mastery Rank 8

- **web** (wrong, 35.4s, $0.024): **Tigris Prime** deals the most damage per shot on its normal attack, and it requires **Mastery Rank 13**.  Source: the Warframe Wiki's Shotgun page (wiki.warframe.com/w/Shotgun). It lists Tigris Prime at about 1,716 average damage per shot, ahead of Exergis at about 1,672.  - **What the figure includes:** It is the wiki's "Avg Shot" figure, which includes crit and multishot. The ranking could dif
  - judge: The candidate names Tigris Prime (MR 13) instead of Exergis (1,620 damage, MR 8), which the grading notes explicitly mark as wrong.
- **skill** (correct, 19.0s, $0.059): Exergis has the highest total damage per shot on its normal attack, at 1,620, and it requires Mastery Rank 8. The next highest is Tigris Prime at 1,560 (MR 13).  Source: the local WARFRAME Wiki KB (`weaponinfoboxautomatic` table, shotgun classes ranked by `attack1total`): https://warframe.fandom.com/wiki/Exergis
  - judge: The candidate names Exergis with 1,620 damage per shot and Mastery Rank 8, matching every expected fact, and mentions Tigris Prime only as the runner-up rather than as the answer.
