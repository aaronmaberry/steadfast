# S01 animated proof v6 (branch proof-v6, not merged to main)

Length 3:05.6, 1920x1080 30 fps, -14.3 LUFS integrated.

## What changed from v5
1. **Screen/logo lock.** One canonical background (bg/room69_clean.png) built from plate 69: Wes removed with an AI edit, graded back to plate 69, and the plate-69 letter pixels stamped once, centered on the screen. Each camera angle is a fixed crop of that one image (a1–a8, plus sp for the split), so every shot from the same angle has a pixel-identical background. The full STEADFAST / MEN logo is visible in every Wes shot. Wes is matted out of each HeyGen clip (rembg human-seg) and composited on top, so he is the only thing that can cover the logo. No logo drift, no "STEA…" crops.
2. **Mouth.** No Avatar IV. Each line uses HeyGen create_lipsync (precision) over a calm, mouth-closed image_to_video idle clip (plates 72, 73, 80, 89). Mouth movement is small, with no wide vowels in the checks. The old plate-89 Avatar IV takes are gone.
3. **Angles.** 21 Wes shots, 2.6–10.5 s each (most 5–9.5 s). 9 composited framings plus a split, used in mixed order. 72 shots are a zoomed chest-up framing. The angle after a board is never the angle before it.
4. **Walking.** There are 2 walk beats (85.3 s and 160.3 s). They are a real profile stride from a HeyGen walk clip (plate 80 source), matted and moved across the fixed room. Both are silent, so no lip-sync is needed.
5. **Boards.** Boards, split boards and the end card are the exact v5 code (luke / point / door / small).

## Timeline (t0, dur, shot, angle, plate)
0.0 W1 a7 73 | 6.8 W2 a1 80 | 13.2 W3 a5 72 | 22.9 BOARD luke | 44.3 W4 a3 89 | 50.2 W5 a8 73 | 55.8 W6 a6 80 | 64.3 W7 a4 72 | 72.5 BOARD point | 85.3 WALK | 87.9 W8 a2 89 | 97.8 W9 a5 72 | 105.6 W10 a3 80 | 110.4 SPLIT door 89 | 119.0 SPLIT small 73 | 128.8 W11 a1 80 | 138.3 W12 a4 72 | 144.7 W13 a6 89 | 149.8 W14 a7 73 | 160.3 WALK | 163.3 C1 a3 80 | 170.8 C2 a2 89 | 175.5 C3 a5 72 | 183.0 end card

## Weaknesses (honest)
- **Compositing.** The matte edges are rembg-quality. A faint edge or halo can show on hair against the bright screen, and there is no light wrap or contact shadow.
- **Walks.** The walks are short (2.6 s and 3.0 s) and waist-up only. The horizontal move is synthetic: a linear slide driven by the source stride, so a slight skate is possible.
- **No new plates.** No 116+ plates were generated. The angle variety comes from crop and scale of 4 existing plates, so the same 4 poses repeat.
- **Plate 72 ring.** Plate 72 has a ring on the clasped hands, so those shots are zoomed 1.75× to keep the hands out of frame. That makes them a little softer.
- **Background.** There is a faint smudge in the upper-left of the screen where the AI's original letters were inpainted.
- **Idle reuse.** Each angle's idle motion is reused with different offsets, so there are some repeated micro-motions.
- **Charge VO.** The charge VO is the v5 ElevenLabs Option D render. The tool exposes no stability or style controls for eleven_v4.
