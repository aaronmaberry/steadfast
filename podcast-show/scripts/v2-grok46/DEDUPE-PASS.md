# De-dupe pass (Aaron 2026-10-19)

Do **not** edit `E007-waiting-is-not-peace.md`. Do **not** git commit.

Regular listeners hear the same jokes and closings week after week. Every duplicated 6+ word spoken sentence (except the host ID and the walksteadfast.com / @steadfastwalk CTA, and except NIV quotes) must become unique to **this** episode’s story.

## Hard

- Rewrite every listed exact/near duplicate in your files. Keep the meaning. Tie it to this episode’s names, objects, and challenge.
- Do not invent a new 6+ word sentence that matches another episode. After you edit, run `tools/find_dupes.py` and keep going until **your** episodes are gone from EXACT and NEAR (E007 collisions: change your file, not E007).
- Segment transitions may keep a recognizable rhythm (`last few minutes`, `halfway`) but the full 6+ word sentence cannot match another episode.
- Canon facts stay: gutter done after E005; fan done Sat Feb 27 / E018; sticking back door unfinished E019–E080 (plane on the bench, swollen jamb). **Vary the wording** of those callbacks.
- Keep beats, NIV exact, boards/slates, word windows, talk split (J 35–50%), max 2 same-host run, J short <15%, host-to-host questions **at least as many as now**, spelling Jonathon, no AI line.
- `fill_stats.py` then `check_script.py` until PASS 0/0.

```
python3 podcast-show/scripts/v2-grok46/tools/fill_stats.py FILE
python3 podcast-show/scripts/v2-grok46/tools/check_script.py FILE
python3 podcast-show/scripts/v2-grok46/tools/find_dupes.py --quiet
python3 podcast-show/scripts/v2-grok46/tools/measure_questions.py FILE
```
