# Walk Steadfast podcast, PROOF 01 (do not post or publish)

File: `walk-steadfast-podcast-proof-01.mp4`, 1920x1080, 24 fps, 2:54, 47.6 MB. Stills 1–4 show idle conversation, full-frame Wes, split + board, full board.

## Script used
`/workspace/biblical-manhood/studio/podcast-show/scripts/E007-waiting-is-not-peace.md` (E007 "Waiting Is Not Peace", v1).
The excerpt is the chapter "The brothers" (the goat, Thanksgiving, "no traffic in the Hill Country", cease-fire, "I've got the words") plus the opening of "Why we wait" ("who's paying for yours?"). I made light trims only. The closing line "Patience picks a time. Waiting doesn't pick a time." is spliced in from the Pushback chapter. The full excerpt text is in `tools/script.txt` (28 lines, 13 Jonathon, 15 Wes). The script contains no AI mentions. The disclosure "Produced with AI voice and video tools." appears only on the end card.

## Locked assets used (unchanged)
- Plate: Option 7 hybrid, built with the comp.py functions from /workspace/tmp-send/podcast-plates at 1080 (K=1). Idle (glass bubbles plus brand card) is used for conversation. Split (bubbles plus board) and full (board) use the bottom bar. Bubble labels read WES and JONATHON. Full-frame host shots use the same bottom bar. Icons are the Simple Icons SVGs, rasterized white.
- Wes: host bubble crop from img/LOCKED-podcast-table.jpg (charcoal henley, foam, boom mic). Voice Option D krjoGt4x3CttlxSuoDYW, eleven_v4.
- Jonathon: cohost/opt1-waist.jpg (heather gray tee, foam, boom mic). Voice uiUeT7adTSLnHQ91QHdW, eleven_v4.
- Outfits: one per host for the whole episode (Wes charcoal henley, Jonathon gray tee). I found no "this week's look pack" file in either repo, so I used the locked site looks.
- Audio: E001 theme-D sting at the open and theme-D outro bed under the end card. There is no stage sound.

## Method (cost-saving pipeline)
1. Motion library: HeyGen image_to_video (heygen-video-1), silent, 10 s each. Per host: 2 talking bases with torso sway, weight shifts, breathing, head turns and hand gestures on the table, plus 1 listen/nod/laugh clip and 1 sit-back + coffee sip clip. That is 8 clips in total, 1 at 1080p (the cost test) and 7 at 768p. I reviewed all 8 and found none stiff.
2. Speaking base per host: the talking clips ping-ponged without mirroring (forward then reversed, so loops join on the same frame), trimmed to that host's total speech length.
3. Lip-sync: ONE HeyGen create_lipsync (precision) per host over the concatenated speaking lines, Wes 121 s and Jonathon 33 s. Audio alignment checked by cross-correlation: 0.0 s offset. The output is cut back into lines by offset. The listener is never lip-synced.
4. Listener cover: listen/nod/laugh and sip clips ping-ponged. They are cut in at every speaker change, so pose jumps hide behind a framing cut.
5. Angles: 4 framings per bubble (wide, medium, close, offset), picked at random at each speaker change and about every 6.5 s inside long turns, with a slow 4% push-in. Three full-frame single-host shots (Wes x2, Jonathon x1). 8-frame crossfades between plate states.
6. Boards: Matthew 5:9 (split, 16 s), "The first mark / Stop waiting." (split, 9 s), Galatians 6:2 (full, 9 s), James 4:17 (full, 10.7 s, the episode verse). That is about 45 s of 174 s, roughly 26% (about 22% excluding fades). None repeats the spoken words.
7. Voice: one eleven_v4 take per host, with all lines separated by [long pause], then split on silence. Post chain: high-pass, gentle gate on tails, light denoise, small presence boost on Wes. Loudness normalized to -16 LUFS.
8. Batch: all 7 cheap clips submitted in one batch, two lip-sync jobs in parallel, then one local compositing pass (PIL + ffmpeg) at 1080p and a 2-pass encode.

## Spend (measured from the HeyGen balance: 3688 -> 3575)
| Item | Cost |
|---|---|
| i2v 1080p 10 s test (used as Wes talk base) | 37 cr |
| i2v 768p 10 s x7 | ~33 cr (~4.7 each) |
| Lip-sync precision, 154 s total (billed partly at submit, rest on completion) | ~43 cr (~0.28 cr/s) |
| **HeyGen total** | **113 cr** (cap 150) |
| ElevenLabs TTS (2,722 cr) | $0.45 (cap $5) |
| Images, plate, compositing, music | $0 (local and existing assets) |

Per finished minute (2.9 min): about 39 HeyGen cr/min plus $0.16/min. Without the avoidable 1080p test: about 26 cr/min.

## 20-minute episode projection
Method (this pipeline):
- Motion library: about 12 clips at 768p (6 per host, made once per outfit/week and reusable across that week's episodes): about 56 cr.
- Lip-sync: about 16 min of on-camera speech (full boards carry about 4 min as voice-over) x 60 x 0.28 = about 270 cr.
- TTS: about $3.
- **Total: about 325 HeyGen cr plus about $3** per 20-min episode, or about 270 cr per episode once the week's library exists.

Brute force alternatives:
- Both hosts as Avatar IV for the full runtime (listener animated too): 2,400 s x 0.35–0.44 cr/s = **about 840–1,060 cr**.
- Full 1080p image-to-video for all footage (3.7 cr/s measured) plus lip-sync: **about 9,200 cr**.
- The method costs roughly 3x less than Avatar IV brute force and 25x+ less than 1080p video gen.

## Honest weaknesses
- Source res: the motion clips are 768p, upscaled in the full-frame shots, which are slightly soft next to the 1080p plate. In the bubbles they look sharp. Fix: 1080p only for the 2 talking bases, which adds about 70 cr/episode.
- Ping-pong: reversed gestures are detectable if you watch the hands closely in long Wes turns (only 2 talking bases per host). A 3rd and 4th base per host would hide it (+10 cr).
- Pose jumps: switching from speaking to listening is a hard pose change hidden by an angle cut. It reads like a multicam edit, but both bubbles cut at the same moment.
- Wes sip clip: the mug appears from below frame without being seen picked up. Jonathon's mug is cleaner.
- Wes dry voice: Option D still carries some room tone. Gating and denoise removed most tails but did not truly de-reverb it. A dedicated dry style or a podcast voice would be cleaner. Note: biblical-manhood logs list a separate "Wes Hart - Podcast" voice (LxMQekBDeYENHe7wI9hA) for conversations. I used Option D as instructed.
- No cross-talk or overlap: lines are butt-joined with a 0.18 s gap, so the rhythm is tidier than a real conversation. Laughs come only from visuals (no audio laughs).
- Eye-lines: the hosts look off-frame toward each other (matching the table photo), not at each other's bubbles. That is fine, but it isn't eye contact.
- The lip-sync jobs took about 5–9 min. Earlier notes warned of 2-hour stalls, but they did not happen this time.
- The plate files comp7.py and icons/ are not on origin/main under podcast/plates/ (only 4k/, LOCKED.md, NOTES.md). I used the local copies in /workspace/tmp-send/podcast-plates as instructed.
