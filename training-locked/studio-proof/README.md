# Lesson 1 STUDIO-format proof, 60s (v1, 2026-10-23)

Cut: Drive 1n7pTBoh-Hf1OWdfQZ-uyPy4ib9GVCQZa (studio-proof-L01-60s-v1.mp4, 63.0s, 1280x720 native, 24fps, AAC). Box: /workspace/artifacts/training/studio-proof/.
Voice: training-locked/audio/poc4-voice.mp3 0-63.0s (Wes Hart - Podcast, LxMQekBDeYENHe7wI9hA, eleven_v3, gen B0px7FdVA9gL6GSIwjHa). No new ElevenLabs credits used. Ends on "...usually in the back."

| Time (s) | Layout | Wes source | B-roll (Pexels id) | Status |
|---|---|---|---|---|
| 0.00-5.70 | PIP bubble over B-roll | X1 raw 0-5.70 | 9945020 lights, 4957763 coffee | real, mouth moves, NOT synced -> sync-3 |
| 5.70-25.48 | PIP | W02 PENDING (labelled still) | 4957763, 8292929 keys/door, 12374854 lot at night | PAID take needed |
| 25.48-26.81 | PIP | X1 sync-3 restored ("That counts.") | 12374854 | done (already paid) |
| 26.81-33.50 | PIP | W04 PENDING | 9843017 boots walking, 9512571 boots standing | PAID take needed |
| 33.50-35.30 | PIP | X1 raw 8.25-10.0 | 9512571 | real, NOT synced -> sync-3 |
| 35.30-38.10 | Board 1 (lands 35.44 "Every man...") | - | - | done |
| 38.10-42.00 | Split: Wes panel / B-roll | W06 PENDING (2nd angle) | 5612232 path walk | PAID take needed |
| 42.00-47.20 | Split | OM03-v13-harm (exact sync) | 3676982 toys | done (candidate; see caution) |
| 47.20-52.40 | Split | W08 PENDING (2nd angle) | 3051693 house at night | PAID take needed |
| 52.40-54.55 | Board 2 (lands 52.50 "Nobody in here is a guest.") | - | - | done |
| 54.55-63.00 | FULL-FRAME Wes (one short full shot) | W09-FULL PENDING | - | PAID clean no-hands take needed |

Angle changes happen only at board cuts. Every transition is a 0.5s crossfade. No scripture falls in 0-63s, so the only boards are two focal-line boards.

## Cost to finish (estimate, NOT spent)
- xAI grok-imagine i2v 10s/720p = $1.41 per take. Pending Wes time is about 44s: W02 19.8s (2 takes), W04 6.7s (1), W06+W08 9.1s 2nd angle (1-2), W09 full-frame 8.5s no-hands (1, plus 1-2 retries likely; X1 raised hands every ~2s). Total 6-9 takes = $8.46-$12.69.
- sync-3 on fal at $8/min ($0.1333/s): 44s pending + 8.0s X1 unsynced = 52s = $6.93.
- 60s total: about $15.40 (range $15.40-$19.60). fal balance is about $1.20, so fal needs at least a $6 top-up.
- Full Lesson 1 (about 25:31): assume Wes on screen about 70% (about 1,070s). That is about 107 usable takes, about 150 with roughly 40% rejects, for $151-$212 xAI. sync-3 on 1,070s is $143. Total about $295-$355. ElevenLabs for the full lesson in the podcast voice is about 30.7k credits at the poc4 rate (4,109 credits/205s). Plan headroom is unchecked; the connector has no usage tool.

---
# v2 (2026-10-23 ~16:45 CT) - placeholders replaced, hard cuts
Cut: Drive 19m3GTozrgG8BlO_pExdQH2aRD872lEnW (steadfast-L01-studio-proof-60s-v2-2026-10-23.mp4, 63.0s, 1280x720 native, 24fps, AAC, no music, no captions). Box: /workspace/artifacts/training/studio-proof/studio-proof-L01-60s-v2.mp4. Scripts/scores: studio-proof/v2/.
New Wes takes: 6 xAI grok-imagine-video-1.5 10s 720p i2v from the v13 still (src13-blend.png; W09 from a tight chest-up crop of it): W02a W02b W04 W06 W08 W09, $1.41 each = $8.46. Each take has an internal camera cut (tight -> wide) at ~2-3.6s; frames within +-1 of it and any frame <0.852 excluded.

| Time (s) | Layout | Wes source (take frames @24fps) |
|---|---|---|
| 0.00-5.70 | PIP | X1 raw 0-5.70 (unchanged) |
| 5.70-25.48 | PIP | W02a 12-55, W02b 57-94, W04 12-65, W02b 100-137, W06 12-53, W02b 139-167, W08 60-113, W02b 171-193, W04 69-131, W02b 196-239, W08 176-232 |
| 25.48-26.81 | PIP | X1 sync-3 restored (unchanged) |
| 26.81-33.50 | PIP | W02a 56-77, W06 187-239, W08 135-164, W02b 12-54, W02a 212-229 |
| 33.50-35.30 | PIP | X1 raw 8.25-10.0 (unchanged) |
| 35.30-38.10 | Board 1 | - |
| 38.10-52.40 | Split (Wes left / B-roll right) | W06 56-186, W04 134-239, W02a 104-212 (replaces W06/W08 placeholders AND OM03, whose source failed review) |
| 52.40-55.04 | Board 2 (extended 0.49s) | - |
| 55.04-63.00 | FULL-FRAME | W09 0-83 (tight) + hard cut + W09 131-239 (wide); no hands/wrists in any frame |

PIP/split crops are face-tracked and scaled to face width (PIP 2.16x, split 2.24x) so hands, palms and wrists stay out of frame; wide-shot frames are upscaled ~1.4x inside the split panel.
All layout transitions are now HARD CUTS (no 0.5s dissolves, no fade in/out). B-roll-to-B-roll crossfades kept (no face involved). 3 single frames (292, 377, 684) that scored 0.847-0.849 are 1-frame holds of the previous frame.
ArcFace vs v13 mean emb, every Wes frame (1381; boards excluded; face picked inside the Wes panel): mean 0.893, median 0.894, min 0.850, 0 frames <0.85, 0 no-face. By section: W02 PIP mean 0.888 min 0.850; W04 PIP 0.892/0.855; split 0.896/0.852; full 0.895/0.860.
KNOWN FLAWS: (1) New takes are NOT lip-synced to the voice - mouth moves continuously and naturally but does not match the words. sync-3 was blocked: fal account locked, "Exhausted balance" (403 at 16:16 CT); the ~$1.20 estimate was wrong. $0 spent on fal. Needs a fal top-up (fal.ai/dashboard/billing) of about $6.70 to sync 50.2s ($8/min). X1a/X1b remain unsynced too. (2) Gestures are out of frame in PIP/split (head-and-shoulders crops); only head nods/sway visible. (3) Many short PIP cuts (1-2.6s) between takes; 5 PIP pieces start near each take's shared opening pose (first 12 frames skipped). (4) Occasional slightly blocky front-teeth frames in split ~41-42s. (5) OM03's exact-sync replaced by unsynced takes.

---
# v3 (2026-10-23 ~20:40 CT) - lip-synced
Cut: Drive 1oNr8e8mH9XsVA06xa-C5n-tUQngdpwaH (steadfast-L01-studio-proof-60s-v3-synced-2026-10-23.mp4). Box: /workspace/artifacts/training/studio-proof/studio-proof-L01-60s-v3.mp4. Same edit/timeline as v2 (render3.py), 63.0s 1280x720 24fps, no music/captions.
- sync-3 (fal-ai/sync-lipsync/v3, cut_off) on every Wes span: 23 pieces (v3/pieces.json; X1a, all W02/W04 PIP pieces, X1b, 3 split pieces, 2 full-frame pieces) = 1,350 frames = 56.25s, each paired with its exact voice slice -> $7.50. The already-synced S3 "That counts." span unchanged.
- Detail restore (rest.py, restore2.py method): raw take pixels outside a feathered mouth/jaw ellipse (0.85 x 1.6 of mouth box, feather 0.12), unsharp inside matched to the raw HF level. No painted texture. Face sharpness (Laplacian) restored from ~45% of raw to ~88% of raw on average.
- Identity fix (fix.py): on frames where the restored frame scored <0.86, the synced mouth region was blended back toward raw (w 0.75/0.5/0.25/0). 146 of 1,350 frames reduced, 38 fully raw (unsynced mouth on those frames).
- ArcFace vs v13 mean emb, every Wes frame (n1381, boards excluded, face picked in the Wes panel): mean 0.888, median 0.889, min 0.852, 0 <0.85, 0 no-face.
- Mouth/audio-envelope corr (best lag): X1a 0.32, W02 0.07, W04 0.09, X1b 0.40, split 0.15, full 0.30 (v2: 0.27/0.15/0.13/0.42/-0.08/0.19). Low in the short-piece PIP/split sections; visual check shows mouth closing on pauses (e.g. 9.7s, 45.6s) with ~2-4 frame lag in split.
- Known flaws: short pieces (0.7-2.6s) give sync-3 little context, so PIP sync is approximate; 38 raw-mouth frames + partial blends can cause brief mouth-shape jumps; occasional gap/single-tooth frames; face still slightly softer than raw.
## fal keys
- Box env FAL_KEY (old): personal fal account aaronmaberry (aaron.maberry@gmail.com, GitHub login) - balance $0, locked "Exhausted balance".
- ~/.secrets/fal_key_box_sync: fal account youtube@walksteadfast.com ("Steadfast Men") - holds the $10 top-up; used for v3.
