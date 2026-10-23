- 2026-10-22 18:01 fal-ai/latentsync P05 10s test (env key, empty account; not run, $0)
- 2026-10-22 18:03 fal-ai/latentsync P05 test: REJECTED by fal before running, 'User is locked. Reason: Exhausted balance.' (storage upload 403 earlier). Spend $0.00
- 2026-10-22 19:00 CDT fal-ai/latentsync P05 10s test (steadfast key) est $0.20
  result: FAIL (corr 0.016 / best 0.184; mouth motion damped std 0.026 vs src 0.038)
- 2026-10-22 19:05 CDT fal-ai/musetalk P05 10s test est ~$0
  result: FAIL (soft face, beard erased, mouth std 0.0167; landmark corr NaN)
- 2026-10-22 19:09 CDT fal-ai/sync-lipsync/v2 (lipsync-2) P05 10s test est $0.50
  result: NOT CLEAR PASS (corr 0.148 @0; mouth std 0.027; mostly static smile shapes, tooth artifact ~4.5-4.6s). 99s run NOT started. Session total est ~$0.70
- 2026-10-23 07:42 CDT Q02 closed-mouth: fal-ai/sync-lipsync/v2 est $0.50 + fal-ai/latentsync est $0.20
  result: Q02+lipsync-2 corr 0.008, mouth std 0.013, ArcFace mean 0.867 (81%>=0.85) - mouth nearly static, FAIL. Q02+LatentSync corr -0.062/best 0.036, std 0.015, ArcFace 0.832 (16%>=0.85) - FAIL. 99s NOT run.
- 2026-10-23 07:53 CDT Q02 lipsync-2-pro est $0.83; omnihuman v1.5 from P05@1.92s 10s 720p est $1.60
  result: lipsync-2-pro on Q02: corr -0.033/best 0.016, mouth std 0.015, ArcFace 0.873 (88%) - mouth static, FAIL.
  result: OmniHuman v1.5 (billed duration 10.0s = $1.60): raw ArcFace 0.726 (2%); after inswapper->v10 0.953 min 0.936 (100%). Clearly articulated speech shapes; energy corr 0.066 (best 0.236). Gestures: both hands raised, fingers spread toward camera, repeated ~0-4s and later -> violates no-open-palms / non-repeating. PROMISING, NOT PASS.
Round total ~$2.43.
- 2026-10-23 08:44 CDT OmniHuman v1.5 retest from Q02@2.0s (hands low), 720p 10s $1.60
  result: REJECT. Hands on hips entire clip (static), wristwatch added, fixed wide grin. ArcFace raw 0.751 -> v10 swap 0.952 min 0.924 (100%). (Box restore ~08:50 CDT wiped local omni2 files; restored from Drive.)
- 2026-10-23 11:40 CDT OM03: fal-ai/bytedance/omnihuman/v1.5 720p, Q02@2.0s chest-up crop (no wrists) + p05.wav 0-8.0s. First attempt with text prompt rejected by content checker (not run, $0). Billed 8.0s = $1.28 (cap $1.50).
  result: raw ArcFace vs v13 mean 0.788; after v13 swap mouth-kept min 0.880 but FAILED independent review (face/neck seam, rubbery mouth, eye widening 5-6s); harmonized 5.2s local fix = candidate.
- 2026-10-23 13:50 CDT OM04: fal-ai/bytedance/omnihuman/v1.5 720p, v13 LOCKED M1 chest-up crop (640x360 -> 1280x720, 50/50 lanczos+Real-ESRGAN, still ArcFace 0.940) + a8.wav 0-5.18s, NO swap. Billed 5.18s = $0.8288 (cap $0.83).
  result: FAIL identity - ArcFace vs v13 per-frame n129 mean 0.856 min 0.734 (53/129 <0.85; worst 2.1-2.6s and 3.8-4.6s wide-eye moments); sync corr@0 0.102 best 0.219 lag +5; no seam, uniform texture, no hands/wrists.
Day total fal 2026-10-23 (this session): $2.11.
- 2026-10-23 14:14 CDT T03 redub: fal-ai/kling-video/lipsync/audio-to-video, video T03-talk-P03-trim0-5.5-v10 (5.5s, billed as 10s @ $0.014/s) = $0.14; audio lesson-01.mp3 (f9d374a) 192.70-198.20s "So here's the thing I wish somebody had told me, plain, a long time ago."
  result: FAIL - ArcFace vs v13 n163 mean 0.880 min 0.790 (12 <0.85); sync corr@0 0.106 best 0.171; output re-timed to 30fps/5.43s; blob single-tooth artifacts ~1.6s, 2.1s.
- 2026-10-23 14:19 CDT T03 redub: fal-ai/sync-lipsync/v3 (sync-3), same inputs, sync_mode cut_off, 5.5s x $8/min = $0.733
  result: ArcFace vs v13 n132 mean 0.899 min 0.860 (0 <0.85); sync corr@0 0.316 best 0.353 (v10 original 0.107); mouth std 0.039; but face-box sharpness drops ~45% (Laplacian var 513 -> 285 = added smoothing) and gap/single-tooth artifacts at ~0.75s and ~2.25s. NOT a clean pass. Local mouth-only composite onto v10 raised sync to 0.355 but dropped ArcFace min to 0.772 -> rejected.
Session total 14:14-14:21 CDT: $0.873 (cap $0.90). Day total fal: $2.98.
- 2026-10-23 14:48 CDT X1 close-up redub: fal-ai/sync-lipsync/v3, video x1-raw 6.917-8.292s (33 fr, longest no-hands stretch by skin check; face ~265px), audio lesson-01.mp3 (f9d374a) 37.55-38.925s "That counts." -> 1.375s x $8/min = $0.18 (cap $0.75).
  result: ArcFace vs v13 n33 mean 0.906 min 0.885 (raw window 0.878); sync corr@0 0.287 best 0.696 lag -2 (raw 0.043/0.422) - too short to be a reliable measure; face sharpness 154 -> 72 (-53%, softening again); teeth natural off-white on crops; last frame had hand onset -> final trimmed to 32 fr / 1.33s. Day total fal: $3.16.
