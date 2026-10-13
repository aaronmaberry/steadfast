# S01 animated proof v8 (branch proof-v8 from proof-v7)
Length 3:08.0, 1920x1080 30 fps, -14 LUFS mix (same VO + bed).
- Talking shots: 12 HeyGen Avatar IV photo+audio clips (720p, low expressiveness, calm chest-up motion prompt) from chest-up crops of the v8 start images. Lip-sync is native, so no create_lipsync step. Mouth-region motion is 11-21 on every shot (gate is 10). The final mp4 uses each clip's own audio, and cross-correlation shows 0 ms offset on all 12 shots.
- Composite comp8 (comp7 with no letter removal, so no holes): Wes is matted onto fixed angle crops of room69_clean_v7. The logo pixels are identical in every shot and the full STEADFAST/MEN logo stays visible, with Wes framed right. Torso-track stabilisation is on (W1 at 0% drift kept). dering runs on every clip with visible hands; the rings in W12m and C1 are removed.
- Angles: W1 a3, W2 a6, W3 a2 | board | W5 a8, W6 a4 | board, walk1 | W8 a5, W9 a7 | boards | W11 a1, W12m a3, W14 a6 | walk2 | C1 a4, C2 a2. No two consecutive shots share an angle, including across cutaways.
- Boards: luke (B1+W4 VO), point (W7+B2), door (W10+S1), small (S2). Each is a periwinkle kicker plus one white line. C3 VO plays over the end card.
- Walks are silent cutaways (bed only). walk1 is v7 walkB 3.4-8.0 (L->R, a1). walk2 is training-locked/35-wes-walk-stage 0.5-5.0 with a smooth L->R drift (a8). No source range is used twice.
