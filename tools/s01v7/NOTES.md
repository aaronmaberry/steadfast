# S01 animated proof v7 (branch proof-v7, built from proof-v6 79d34a6; not merged to main)
Length 3:08.9, 1920x1080 30 fps, mix loudnormed to -14 LUFS (audio7.py; same v6 VO + bed, no new ElevenLabs).

## Changes from v6
1. Motion. New HeyGen image_to_video base clips (heygen-video-1, 15 s, 1080p), each starting from the first frame of the v6 idle: g72 and g89 are gesturing clips (open palms, emphasis hands, torso sway, weight shifts, small left/right head turns). idle73 is a sway/head-turn close-up (no arms in frame). 18 of the 19 talking shots use g72/g89. W10 and W11 are mirrored to reduce repetition. The plate-72 1.75x zoom is gone, so the hands are in frame.
2. Lip-sync. HeyGen create_lipsync precision runs on the full 15 s base clip with audio pre-offset (P_*.mp3). Each shot cuts exactly [off, off+dur] from the synced clip, with no loop, reverse or retime. The audio offset was checked by cross-correlation on all 19 synced clips and in the final share mp4: 0 ms (one at -1 ms). A visual frame check at W3 +2.5 s matched the lipsync source.
3. Drift control. comp7 tracks the torso and cancels slow horizontal wander (stab window 2.5 s, keeps 35%; 73 close-ups 1.2 s and 0%), so the sway and head turns stay but he doesn't drift off his mark. Bright static source-logo pixels are masked out of the matte, so no ghost "STE" letters.
4. No rings. The generator added a wedding band in g72 and g89. dering.py (skin-masked median plus inpaint on hands) removes it at comp time.
5. Background. The upper-left smudge and brown blotch are cleaned (smudge.py -> room69_clean_v7.png). The logo rect x560-2440 y230-670 is pixel-identical to v6.
6. Walks are longer: walk1 4.6 s (left to right, a1) and walk2 4.4 s (mirrored, right to left, a6). v6 walks were 2.6 s and 3.0 s.
Boards, splits, end card, angle order, henley: unchanged v6 code.

## Timeline
0 W1 | 6.8 W2 | 13.2 W3 | 22.9 B luke | 44.3 W4 | 50.2 W5 | 55.8 W6 | 64.3 W7 | 72.5 B point | 85.3 walk1 | 89.8 W8 | 99.7 W9 | 107.5 W10 | 112.3 S door | 120.9 S small | 130.7 W11 | 140.2 W12 | 146.7 W13 | 151.8 W14 | 162.2 walk2 | 166.7 C1 | 174.2 C2 | 178.9 C3 | 186.3 end
