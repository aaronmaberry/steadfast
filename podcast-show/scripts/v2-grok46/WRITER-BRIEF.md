# v2-grok46 writer brief

Write Walk Steadfast v2 scripts for your assigned episodes only. Do not edit E001, E002, E007, `tools/`, or this brief. Do not git commit or push.

## Output (all three for every episode)

`/workspace/podcast-show/scripts/v2-grok46/`

- `E0xx-<slug>.md` — use the v1 slug from `/workspace/podcast-show/scripts/E0xx-*.md`
- `E0xx-show-notes.md`
- `E0xx-check.log` — full checker stdout

Pass `python3 podcast-show/scripts/v2-grok46/tools/check_script.py <script>` with **0 fail and 0 warn**. Then `fill_stats.py`, re-check, write the log.

## Voice and form

Match locked pilot `/workspace/podcast-show/scripts/v2-grok46/E007-waiting-is-not-peace.md` and launch `/workspace/podcast-show/scripts/v2-grok46/E001-the-man-you-keep-saying-youll-be.md`. Field Notes pattern: `E002-field-notes-the-first-check.md`.

Header line (must match exactly at start of that line):

- Main: `Walk Steadfast · main episode · script v2 (rewrite of v1)`
- Field Notes: `Walk Steadfast · Field Notes · script v2 (rewrite of v1)`

Do **not** use `launch episode` except E001 (already done).

Spoken windows (150 wpm): mains **2800–3200**; Field Notes **1900–2400**. E001 launch 4500–5250 is already done.

Aim Wes **52–56%** / Jonathon **44–48%** (checker allows Jonathon 35–50). Jonathon lines under 12 words **<20%**. Write his color lines at 12+ words. Longest turn ≤170. Segments except OPEN/CLOSE ≤900. CLOSE ≤130. Hook before first STING ≤75 words. First words are spoken (no cue first). First STING inside OPEN. End: last spoken line in CLOSE has both `walksteadfast.com` and `@steadfastwalk`, then `[STING 2s]`.

Wes time-checks ≥2 (`halfway`, `about X minutes`, `last few minutes`, `before we're done`, etc.). 3–5 `[BOARD:]` cues. Idea boards must not share a 4-word spoken gram. Scripture boards: `Ref (NIV) · "exact NIV text"` and not overlapping spoken 4-grams.

Every episode **reads at least one exact NIV verse** on air (Field Notes: one verse). Header Scripture row must include `verified 2026-10-19` and the refs. Cache: `tools/niv-cache/`. Add missing verses with `python3 tools/niv.py "Book C:V"`. Quote the verse words exactly like E001/E007.

`[SLATE: E0xx · Title]` unspoken, after the OPEN sting. **Skip SLATE only on E007** (already copied). Never say the episode number.

OPEN and CLOSE are word-for-word. After STING: `WES: This is Walk Steadfast. I'm Wes Hart.` / `JONATHON: And I'm Jonathon.` (not Hale after E001). Wes names the question and a specific tease.

No subscribe asks, no standing outro, no on-mic book/training tour. One book name max if the calendar plug is B, under 20s, present tense, no prices, no "out now." Prefer putting plugs in show-notes **Mentioned**. Never mention AI. Never say "you all," "segment," off-air/studio/camera/producer/mic, "as you know," "last week we," "last episode," "back in episode."

Jonathon: no y'all / reckon / fixin / yonder / ain't / feed store / lord willin. He is 36 at launch, February birthday, from Pasadena, HVAC sales, wife Dani (nights), Ruby 7, Theo 4. Never "Jonathan."

Wes wardrobe only in the unspoken header from `/workspace/podcast-show/production/WARDROBE.md`.

## Continuity (do not contradict)

Read `STATUS.md` and `/workspace/podcast-show/research/opus55/pack/evidence/CONTINUITY-ROWS-E001-E080.md` for your range. Apply Aaron overrides:

- Jonathon Hale, 36, February birthday.
- Nephew (22, unnamed, sister’s son in Pasadena) **text only**.
- **Gutter fixed E004/E005.** After that the delay item is the **youngest’s clicking ceiling fan**, **fixed Sat Feb 27**, reported in **E018**. Do not keep the v1 gutter running through spring.
- E007 locked: Thanksgiving cease-fire; older brother 58; little brother 47 Fort Worth; Mom 78 hip; Wes call Wednesday 7 PM; pending dad friend request; October Dani fight unfinished until Easter season; Pancake after Theo turns five in August; PT Tuesdays since August (wife, then Wes takes them from E002).

Source pack: v1 scripts in `/workspace/podcast-show/scripts/E0xx-*.md`, calendar `/workspace/podcast-show/CALENDAR-104.md` (2027, Tue/Fri). Use v1 stories, then rewrite to v2. Fix contradictions per STATUS.

Show notes: copy the E002/E007 notes shape. Title ≤60 chars, meta ≤160. Include `https://www.walksteadfast.com`, `@steadfastwalk`, `#WalkSteadfast`, `**Keywords**`, and the NIV notice paragraph. Chapter table times must match every script `##` section including OPEN and CLOSE. `fill_stats.py` updates counts and times.

## Loop

For each episode: draft → `fill_stats.py` → `check_script.py` → fix until **RESULT … PASS (0 fail, 0 warn)** → write `E0xx-check.log`. Then the next episode. Update the episode table rows in `STATUS.md` for the episodes you finished (only those rows).
