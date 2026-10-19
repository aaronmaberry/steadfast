# Conversation pass 2 (Aaron 2026-10-19) — live radio, not parallel speeches

Do **not** edit `E007-waiting-is-not-peace.md`. Do **not** git commit. After edits: `fill_stats.py` then `check_script.py` until **PASS (0 fail, 0 warn)**. Stay in the word window.

Model spoken feel: E007 Segment 4 (Pushback) — “Go ahead and push”, “So which is it?”, `[laughs]`, “I don’t totally buy that yet.”
Model close rewrite: E046 `## SEGMENT · Sitting with it` after this pass.

## Feel (hard) — this is the new bar

- Every **4–6 spoken exchanges**, at least one **genuine question one host asks the other**, and the other **actually answers** (not a rhetorical “right?”). A host-to-host question = spoken `?` whose next spoken line is the other host.
- Real reactions: `[laughs]`, teasing, mild disagreement that gets worked out, “Wait, back up”, “No, hold on”, “That’s fair, but—”, interruptions with em dashes that the other finishes or redirects.
- **Cut parallel-confession stacking.** When one says “I did X too / I’ll hold you / I’ve baptized delay”, the other must respond to *that* line. Do not both make matching speeches.
- **Jonathon drives some threads.** He asks Wes hard follow-ups, pokes fun, brings his HVAC/sales-guy / calendar / kids angle. He is not an echo.
- **Replace sermon-ish closing lines** with conversational ones. Keep **one clear takeaway per segment**.
- Delete the reused “Sitting with it” sermon template when you find it. These lines (and near-copies) must become conversation, not stay as stacked I’ll/I’ve:
  - “I want the listener who thinks this doesn’t apply because his house is quieter”
  - “I’ll check the ___ on Friday, which is the only reason I trust myself”
  - “I’ll hold you to …” / “I want somebody holding me to …”
  - “A steadfast man does the small thing while it’s still small”
  - “I forget it by Tuesday afternoon. Ruby doesn’t”
  - “If this feels like too many stories, pick one”
  - “I’ve got a habit of saving the true sentence for a better room”
  - “I’ve rehearsed in better rooms my whole adult life”
  - “Some of you will try to make this spiritual…”
  - “I’ve baptized delay”
  - “HVAC sales doesn’t hand you a quiet month”
- If a late segment **repeats earlier paragraphs** (E051 challenge/sitting-with-it does this), **cut the duplicate** and replace with new back-and-forth. Do not pad word count with copies.

## Keep (hard) — still locked

- Every beat, story, name, date, challenge, and scripture. NIV quotes **exact** (do not contract inside `"..."` / `“...”`).
- `[BOARD:]` `[SLATE:]` `[STING 2s]` unchanged in text (boards must not share a spoken 4-gram).
- Segment headers and OPEN/CLOSE structure. CLOSE ≤130. Last CLOSE line has `walksteadfast.com` and `@steadfastwalk`.
- Jonathon **Hale**, spelled Jonathon. After E001 first full name, first name only.
- Canon: gutter done after E005; fan done after E018 (Sat Feb 27); sticking **back door** thread from E019 through E080, unfinished; E014 title **What Stuck** + spoken season one look-back.
- Word windows: E001 launch 4,500–5,250; Tuesday mains 2,800–3,200; Friday Field Notes 1,900–2,400.
- ≥2 Wes time checks (`last few minutes`, `next few minutes`, `halfway`, `before we're done`, etc.).
- Longest single turn ≤170 words (warn). Segments except OPEN/CLOSE ≤900.
- No AI, episode numbers, “you all,” “segment,” subscribe, studio. Jonathon: no y'all / reckon / ain't.
- Nephew text-only. Do not reopen the gutter or un-fix the fan.
- Max consecutive same-host spoken lines = 2 (E007 is the only exception).
- Jonathon short-line rate (under 12 words) under ~15% (checker fails at 20%). Short reactions are fine if **substantive turns dominate**.
- Contractions stay. Full form only for emphasis or exact NIV.
- Aim Wes 52–56 / Jonathon 44–48. Checker allows J 35–50. Do not dump all new questions onto one host.
- No AI disclosure line. Never mention this pass on air.

## How to rewrite (do not start from scratch)

1. Read the whole script. Keep OPEN/CLOSE structure; you may loosen CLOSE wording so it sounds like two friends, but keep one takeaway and the CTA line.
2. Walk every 4–6 spoken lines. If nobody asked the other a real question, insert one that belongs to **this** episode and make the next line an answer.
3. Convert “I’ll / I’ve / I want the listener” stacks into: question → answer → tease or mild push → one takeaway.
4. Let Jonathon start at least one thread per episode (a hard follow-up, a joke, a sales-calendar beat).
5. Watch the word window. Near the **ceiling** (E005, some mains ~3,170): replace, don’t add; cut duplicates first. Near the **floor** (many FN at 1,900): adding real Q&A is good.
6. Update show notes **only** if chapter timestamps shift after `fill_stats.py`.

## Check (required before you stop)

```
python3 podcast-show/scripts/v2-grok46/tools/fill_stats.py FILE
python3 podcast-show/scripts/v2-grok46/tools/check_script.py FILE
python3 podcast-show/scripts/v2-grok46/tools/measure_convo.py FILE
python3 podcast-show/scripts/v2-grok46/tools/measure_questions.py FILE
```

- `check_script.py`: PASS, 0 fail, 0 warn.
- `measure_convo.py`: max consecutive same-host ≤2; contraction % ≥80.
- `measure_questions.py`: **at least 6** host-to-host questions on a Field Notes, **at least 8** on a Tuesday main / E001. Prefer ~1 per 5–6 spoken lines (E007 is 14 / 82).
- Do **not** git add / commit / push.
