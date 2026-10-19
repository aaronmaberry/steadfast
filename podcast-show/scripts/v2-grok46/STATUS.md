# Walk Steadfast v2-grok46 · STATUS

Branch: `podcast-scripts-v2-grok46` (from `podcast-scripts-v2`). Output: this folder. No merge to `main`. No audio, no spend, no publish.

## Checker length windows (Aaron)

| Format | Header line | Spoken words | Runtime at 150 wpm |
|---|---|---|---|
| **E001 launch only** | `Walk Steadfast · launch episode` | **4,500–5,250** | **30–35 min** |
| Main (Tue) | `Walk Steadfast · main episode` | 2,800–3,200 | ~19–21 min |
| Field Notes (Fri) | `Walk Steadfast · Field Notes` | 1,900–2,400 | ~13–16 min |

E001 exception logged 2026-10-19 (Aaron): replace the earlier 40–45 min / 6,000–6,750 window with **30–35 min / 4,500–5,250**. Kickoff content is unchanged: introduce Wes and Jonathon Hale, how they know each other, what Walk Steadfast is, who it is for, Tuesday main / Friday Field Notes, then the topic “The Man You Keep Saying You’ll Be.” Set in `tools/check_script.py` as `LAUNCH_WORDS_MIN, LAUNCH_WORDS_MAX = 4500, 5250`. Other episodes use the main / Field Notes windows above. Every script must pass the checker with **0 fails and 0 warnings**.

## Episode table

| Ep | Title | Words | Runtime | Talk (W/J) | Check |
|---|---|---|---|---|---|
| E001 | The Man You Keep Saying You'll Be (launch) | 4,959 | 33:04 | 51 / 49 | PASS 0/0 |
| E002 | Field Notes: The First Check | 2,199 | 14:40 | 53 / 47 | PASS 0/0 |
| E003 | Nobody Ever Gave You the Sentence | 2,934 | 19:34 | 52 / 48 | PASS 0/0 |
| E004 | Field Notes: The Sentence Test | 1,968 | 13:07 | 54 / 46 | PASS 0/0 |
| E005 | What a Steadfast Man Looks Like | 3,173 | 21:09 | 52 / 48 | PASS 0/0 |
| E006 | Field Notes: Saying It Out Loud | 2,204 | 14:42 | 50 / 50 | PASS 0/0 |
| E007 | Waiting Is Not Peace (locked pilot, copied word for word, no SLATE) | 3,138 | 20:55 | 52 / 48 | PASS 0/0 |
| E008–E080 | remaining | — | — | — | pending |

## Continuity ledger (overrides + on-air facts)

Locked host facts (Aaron overrides v2 bible R2):
- Jonathon **Hale**, **36 at launch**, birthday in **February** (not November; not 37 at launch). Surname is Hale, never Reese.
- After first full name on E001, he is Jonathon. Never “Jonathan.”
- Nephew (sister’s son, 22, unnamed) **only checks in by text**. No in-person cameos.
- Wes wardrobe only from `production/WARDROBE.md`. Never spoken.

Household delay item (Aaron, overrides v1):
- **Gutter is fixed in E004/E005** (the 14-month loose back-porch gutter is done then).
- After that, the delay item is the **youngest’s clicking ceiling fan**.
- Fan is **fixed Sat Feb 27**, reported in **E018**.

E001 established (keep):
- Wes 52, Hill Country, married 27 years; kids 25 (daughter, married, teaches second grade), 21 (son, electrical apprenticeship), 16 (just licensed). Fog years. Dad said “I’m proud of you” when Wes was 43. Mr. Abernathy, lineman 40 years, mug at the funeral in a paper towel. Book named once, no tour.
- Jonathon 36, turns 37 in February. Pasadena, TX. Dani (L&D, nights, 3/week), Ruby 7, Theo 4. Dad left when he was 9 (dent in the tailgate; Lake Charles; calls ~twice a year). Mom called him man of the house at 11. HVAC sales. Parking lot 11 minutes. Scariest text. Seven years of Thursdays. Came to faith that year. No weeknight drink in six years. Coach-pitch 0-6 last fall.
- 1604 for two years (Ruby ~4, Theo ~1). Port Aransas, one hardhead catfish. Theo flooded the bathroom. Phone is a recliner you can carry.

E007 locked (do not contradict):
- Thanksgiving cease-fire with older brother (58, dad’s place, handles Mom). Little brother 47, Fort Worth. Mom 78, bad hip, lives alone. Wes left early “to beat the traffic.” Call set Wednesday 7 PM.
- Pending Facebook friend request from Jonathon’s dad (from Christmas; E006). October fight with Dani unfinished; comes back before Easter.
- Pancake after Theo turns five in August. Sales rep review postponed three times.
- PT context: wife has been driving Mom to PT Tuesdays since August (first told on E002). Compatible with E007’s Mom / hip.

v1 contradictions logged:
1. Jonathon age/birthday: v2 bible R2 said November / 37. Aaron: February / 36 at launch.
2. Surname: some packs used Reese. On air: Hale.
3. Gutter arc in v1 ran through E014–E021. Aaron: gutter done E004/E005; fan is the later delay item, fixed Sat Feb 27 / E018.
4. Nephew: v1 had him at games / chili / in-person. Aaron: text only.
5. v1 standing outro, subscribe asks, on-mic book/training plugs, spoken episode numbers, and “Produced with AI…” are gone in v2. Plugs live in show-notes **Mentioned** only.

## Open decisions for Aaron

1. Confirm fan-for-gutter swap is the whole remaining household-delay thread (no third item after E018).
2. E014 calendar title is “Season One Review”; v1 slug is `what-stuck`. Using the v1 slug unless you say otherwise.
3. E025 wardrobe note in WARDROBE.md disagrees with the row (linen vs white oxford). Scripts will follow the table row, not the Notes sentence.
4. Talk-share aim is Wes 52–56 / Jonathon 44–48. Checker allows Jonathon 35–50. E001 landed 51 / 49 (pass). Later mains will aim the tighter split.
5. Field Notes must still read **one exact NIV verse** (checker warns on zero quotes). v1 E002 quoted none; v2 E002 quotes Luke 16:10.

## How to check

```
python3 podcast-show/scripts/v2-grok46/tools/fill_stats.py podcast-show/scripts/v2-grok46/E0xx-….md
python3 podcast-show/scripts/v2-grok46/tools/check_script.py podcast-show/scripts/v2-grok46/E0xx-….md
```
