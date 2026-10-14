# v8 progress (workdir /workspace/s01v8; tools reuse /workspace/s01v7 comp7/b5lib; repo worktree to be /workspace/sf-v8 branch proof-v8 from proof-v7)
- HeyGen start balance 3553. HARD STOP at 3403 (150 cap).
- Structure: 12 talking: W1 W2 W3 W5 W6 W8 W9 W11 W12+W13(merged "W12") W14 C1 C2. VO-on-board: W4 (luke, after B1), W7 (point, before B2), W10+S1 (door full), S2 (small full), C3 over end card.
- Start images = frames of paid v7 clips, Wes matted onto logo-free room (no letters anywhere).
- W1 i2v 768p 7s = 4 credits (video 4f7219bcb55445c2864403d056ef23df, asset 346f5c43). balance 3549. plan8.json has shot->start image map; aud/K.wav = 0.15s lead + line, length L
- assets: W2 dc44c0fa(start00) W3 6b1c598e(05) W5 bd8d8d00(03) W6 22cf1034(11) W8 6cb87796(01) W9 7373e84d(10) W11 57473718(06) W12m fc385b2c(04) W14 67029f89(07) C1 6ada6751(08) C2 6a6ca9ee(02). submitting i2v 768p batch
- i2v vids: W2 9f09992c06694fd0a34d3ea806356dec W3 2d7ecf373e4641a9a9351293724e4a3c W5 8af18ea1855c4a36a622469fa243d101 W6 94eb1165ccff42ebb3c56331729538c7 W8 ca7338d1a9274edc88c76b716e0f5813 W9 c6803f78f8a349d1b5335aad46c5f7ca W11 c82571eabce946648bb30b0a51a61734 W12m be1d19b2f17c4bc3911ab8326581706d W14 58a735f619b24610b399a867f74b7669 C1 ebc547e973b345869e7a6e46c3610f5a C2 23257a32f6834b2da34b25ee46b50f1e
- balance 3482 after i2v (spent 71). cap leaves 79.
- regen (ring reject) W9 1a5e2f157e12479c8b9ae2369e8c406c W11 2983d73e20c74ff3bf338e81183ae811 C2 096bb0f5f4434285970d63fcaaaf5071. trimmed exact-L clips in trim/; uploading for lipsync
- trimmed video assets: W1 038d413c W2 0d1eceb0 W3 ca90699c W5 9e915336 W6 d362793c W8 a06af8d9 W12m 2f983437 W14 cdc7332d C1 0732b221
- audio assets: W1 3d48d459 W2 ac5147b5 W3 8f5646a5 W5 0bc051f5 W6 d42033e2 W8 34982229 W12m 4d81602f W14 d84d31d6 C1 b7d23b40 W9 cd526827 W11 5e98d2f7 C2 d2a04b84
- bal 3437 after regens+W1 lipsync submit (expected ~3466)

## 2026-10-13 ~15:35 CT — HALTED: hard cap reached
- Regens W9/W11/C2 accepted (mean speed 2.8/2.0/3.2, no rings visible). Trimmed: trim/, with-audio trimA/, silent-track trimS/.
- Lipsync attempt 1 W1 (cd441b55, no audio track in video) -> FAILED "audio missing".
- Lipsync attempt 2 W1 (2cc32fe6, video muxed with the line audio, 768p) -> "completed" but NO-OP (max diff vs source ~4, = re-encode noise).
- Lipsync attempt 3 W1 (aea15511, head crop 800x400 upscaled to 1920x960) -> "completed" but NO-OP again.
- Balance 3400 (start 3553) => 153 spent, 3 over the 150 hard cap (lagged charge for attempt 3, ~36 cr). All paid work stopped.
- Untested hypothesis: precision skips when video already carries the target speech; trimS/ (silent track) is ready to test.
- 11 with-audio clip assets uploaded (batch a025810e) — unused.
- 15:32 v8b: W1 silentS lipsync ef88f524a5624b058dda26e603b2dc19 (video asset 1b63fc06, audio asset 919da54d, precision). bal before 3400
- 15:34 ef88f524 FAILED: 'video's audio track is silent ... needs original speech'. bal still 3400 (0 spent this session). STOPPED per plan; HeyGen lipsync ruled out (silent=reject, with speech=no-op). Fallback: Avatar IV photo+audio per line.
- 15:37 FALLBACK A4 (cap 100, start bal 3400): W1 video 7274cf484f425dbd9e9b9b8899ef9de9 (img asset 11cffab5 start09, aud 919da54d, 720p low expr)
- 15:42 W1 A4 #1 7274cf48: lips OK (mouth 12.2, audio 0ms) but RING visible at 5.25s + broad arm gestures -> reject. bal 3373 (mixed w/ pp2b jobs L05/L07/L08/L10/L11). Retake chest-up (img b5da4499): 07b00ae9a68aca738def1d4f267a42fa
- 15:51 W1b 07b00ae9 PASS (mouth 14.2, audio 0ms, no ring; hands only fingertips ~6s). bal 3370. Inputs batch 2a06f103 (ids in s01v8/a4/ids.json). 11-shot Avatar IV batch 86dfb49fa3ee4d2ca960f38f0faec43b (chest-up crops a4/*chest.jpg)
- 15:52 batch video ids in s01v8/a4/vids.json
- 16:28 RESUME STATE: all 12 Avatar IV clips done+downloaded (s01v8/a4/*.mp4, ids vids.json), no jobs pending. QA: mouth diff 11-21 all >=10; HeyGen audio = input +23ms (use shot's own audio in mix => 0ms). Rings in W12m, C1 -> dering in comp. bal 3331 (3400 start; 69 drop incl. concurrent pp2b jobs) -> cap not exceeded.
- comp: /workspace/s01v7/comp8.py (no letter removal), runner s01v8/runall8.py -> s01v8/shots/*.mp4 ALL 12 DONE + walk1 (v7 walkB 3.4-8.0 comp). walk2 from walkA 4-8 jumps (source pans) -> redo from walkB 0.2-3.3.
- build: s01v8/build8.py (timeline8.json, seg8/, mix8.wav) -> tmp-send/.../S01-anim-proof-v8-share.mp4
- 16:30 walk2 redone: training-locked/35-wes-walk-stage.mp4 0.5-5.0 (unused elsewhere), stab+drift L->R smooth. building.
- 16:33 DONE: share mp4 188.0s, 0ms offset all 12 talking shots, stills still_*.jpg, NOTES.md. pushed proof-v8 739d03c. bal 3331 stable.
- 17:02 v9 DIAGNOSIS written (DIAGNOSIS-v9.md + v9diag-*.jpg), no credits spent
- 17:36 v9 W1 test PAUSED by Aaron before any paid call. Prepared s01v9/w1/master_wes.png (right half of WES-FACE-MASTER) + plate69.png as edit refs. Nothing spent.

## v9 stills (Oct 13 CT)
- EL flow TNSzKsAmdPYNoOaML4yJ; refs master node ybzBGvE7tnVAMd37rzOY, plate69 node KUVvYGHC2zeYcbGJIeP8. Estimate: $0.402/generation (gemini-3-pro-image). Plan 7 gens (~$2.81) + <=2 retries, cap $4.
- 7 gens started (S1-S7), $2.81 committed. sessions: NTU40EfXO7ArQ5qamO60 SqJaeYDEclcKkWGerIKV GMhmj6sOXrtkXlFF2Wug 7rlTVjda5ubigrwB3lsQ HBA0m9S6AjUS1vJ9CS5O cRn282afDYVd1axztC6E fDUUMWfzlwVVUdwGQAoq. DO NOT re-run.
- Gens done. Raw id 0.45-0.62 (all fail). Local inswapper (master face) -> 0.90-0.92. Hair fail S2,S3,S5,S7. Sleeves not pushed in any. Logo regenerated (composite not done). Candidates + contact sheet in s01-anim-proof-v9/stills/. Spent $2.81 EL. Stopped: $1.19 left can't fix sleeves on 7.
- Oct13 5:54PM CT: fix pass approved (+$4, cap $7). Inswapper approved, 9% resize ok.
- Fix pass: 7 edits started ($2.51; total EL $5.32). sessions DgC5mi5AHic64twgu8Rh 74UqWpeqbavEWR5iRByH AWLjUH5GCTJJgrnDIvJq FlZa0xWeQrXyOo2XtCNd l2iuxH3eBtO5d9dDm9qt POndx9970IHxhwdoFo0q GjhVINEaevFWyyFvfIQ8 (S1..S7). DO NOT re-run.
- Fix pass done 6:05PM CT: all 7 pass (id .886-.917, hair 1.96-3.86, sleeves pushed, no ring/watch, logo px-identical). Delivered LOCK-CANDIDATE-S1..S7 + contact_sheet.jpg. EL total $5.32.

## v9 W1 clip (Oct 13 6:2x PM CT)
- Locked stills committed 9b5b204 (training-locked/v9-face-master). HeyGen bal 3331 before.
- W1 Avatar IV video 103df5ae7e561a46a5c91259a66f25a9 (S2-medium, img faf4b2ea, aud 7bb2d940). DO NOT resubmit.
- 6:35PM CT W1 done: HeyGen 3 credits (3331->3328). Raw heygen face min .66/mean .80 FAIL -> per-frame inswapper -> min .906 mean .920 PASS; hair max +2.3%; logo identical all frames; hands out of frame. Delivered W1-test-v9.mp4 + sidebyside.
- 6:5x PM CT: W1 arm diag = hard binary rembg matte flickering at arm-torso gap (gap alternately filled w/ HeyGen bg / opened to plate floor glow) + unfeathered dark fringe. Uploaded batch a5d4fe7f (hg_ids.json). Video batch bbd0aada2dca43dc84dcdb8eece576f5 (11 shots, s01v9/batch9.json). bal before 3328. DO NOT resubmit.
- 11 shots completed (vids9.json). W1 recomposited with comp9 (bg-chroma kill + temporal median matte) PASS all gates incl edge.
- 7:20PM CT downloaded 11 raw clips (p9/hg). running comp9+gate9 all (p9/runall9.log). HeyGen bal 3289 (39 used for 11).
- 7:5x PM CT: comp9 v2 (bg chroma key widened to catch HeyGen ghost arms/bluish leaks), gate9 v2 (flicker=temporal 2nd diff, hair matte-restricted+5f median, leak). Re-running W1 + all 11 sequentially (OOM at -P2).
- 7:52PM CT resumed after interrupt: no new HeyGen jobs since batch bbd0aada (bal 3289; 42/60+ W1 3 = cap use 39 of 60 for this order). runner still alive.
- 8:2x PM CT: diag2: purple on arms in W2 = real rim light (present in locked still) -> leak gate now baselined vs still; W3 had HeyGen 'ghost arm' smear in bg -> killed by chroma key. Added adaptive hair softening in hair zone only (Gaussian, never sharpen) to keep hair <= still*1.05. Re-running all 12 (runall9.log).
- 8:42PM CT resumed; runner pid 1552033 alive at W9; W1-W3,W6 pass all; W5,W8 fail face+edge (investigating).
- 8:46PM CT W8-walk fails face gate (wide/tiny face 0.78-0.85 except frames 64-115). Submitted W8b on S2-medium: video f596e8eb013c5dac17382b8a3b488c4e (~4-5 cr, bal before 3289). DO NOT resubmit. Plan: W8-walk frames 64-115 as 2s music-only wide walk cutaway; W5 frame55 hold-fix.
- 8:52PM W8b done (bal check later), downloaded hg/W8b.mp4; queued run_w8b.sh (nohup, waits for runall9). W5 edge sheet eyeballed: clean, patch flag = natural forearm shading.
- 8:57PM build9 edited (W8 walk -> WK 2s music-only wide cutaway frames64-115 + W8b talking on S2). post9.sh queued nohup (W5 f55 hold, WK cut, build9).
- 9:10PM W9 PASS face/hair/logo, edge flagged on patch count only (eyeballed clean). W11 same, but faint thin grey contour line beside right-of-frame sleeve on dark bg in some frames - flagged for review.
- 9:25PM W12m comp OOM-died silently; re-queued in post9 (killed+restarted post9, no dupes). W14 single frame 202 at .844 -> held frame 201 (W14_orig kept). W14 edge flag = patch count only (n4 vs base1+2).
- 9:58PM DISK FULL (0B) + host balloon squeezing RAM caused W12m/C2/W8b comp/gate deaths and build9 fail. Freed 4.7G (deleted v9 work/*/fr + alpha.npy for gated shots). comp9 memory cut (uint8 masks). run_rest.sh nohup: W12m, C2, W8b.
- 9:36PM CT W12m gated: face .864 PASS, hair PASS, logo PASS, edge = patch count only. Freed disk (W12m alpha, w1clip frame caches). C2 comp running (pid 1582379).
- 9:42PM C2 PASS all (sim .874). W8b running.
- 9:46PM W11 grey contour: brightened 2x crop of composite shows no line at sleeve edge; QA-sheet contour is the plate's own stage-riser edge, not a matte artifact. No fix needed.
- 9:51PM W8b PASS all. W5 f55 held (done), WK cut done. build9 started nohup.
