# S01 animated proof v5 (176.9 s, 1080p, -14.2 LUFS)

## Shot list (master timecodes)
| # | t0–t1 (s) | Shot | Plate | Source |
|---|---|---|---|---|
| 0 | 0.0–12.8 | Open, waist-up, three-quarter left, lower third "Wes Hart" (days nobody photographs / "I call that day a Tuesday") | 80 | HeyGen R1 |
| 1 | 12.8–22.2 | Open cont., tighter punch-in | 80 | HeyGen R2b |
| 2 | 22.2–43.3 | Full board, kicker "LUKE 16:10" + verse (VO reads the verse) | – | board |
| 3–5 | 43.3–71.5 | Three-quarter with open-palm gestures, 3 crops (11.7 / 8.6 / 8.0 s) | 72 | HeyGen R3 |
| 6 | 71.5–83.9 | Key-point board: "THE POINT" / "Name the day. Then show up for it." | – | board |
| 7–8 | 83.9–107.0 | Walk: Wes matted from the plate-89 lip-sync render and composited onto the locked plate-69 room (Wes 69 removed, logo untouched). He moves right to left, the camera half-follows, slight bob and push | 89 on 69 | HeyGen R4b + walk5.py |
| 9–10 | 107.0–125.1 | Split: board on the left ("WEEK ONE" / "The first step is just walking through the door." then "THE POINT" / "Small, faithful, ordinary. That is where a man is built."), Wes talking on the right | 72 (split stamp variant) | HeyGen R5b |
| 11–13 | 125.1–156.0 | Lean-in, profile right, progressive push 1.0 → 1.36 | 73 | HeyGen R6 |
| 14–15 | 156.0–174.4 | Charge, waist-up (new line: "Alright. Let me land this… start with last Tuesday.") | 89 | HeyGen R7b |
| 16 | 174.4–177.0 | Brand end card (v4) | – | v4 s21 |

## Audio
- The voice is v4's Option D audio (krjoGt4x3CttlxSuoDYW, proof_audio.wav), re-cut into new pieces (plan.py). The only new line is the 18.4 s charge, made on ElevenLabs eleven_v4 with the same voice.
- v4 had no separate music bed file, so this cut uses a soft synthesized pad at about -37 dB under the voice. The mix is normalized to -14.2 LUFS integrated.

## Pipeline
- Plates are upscaled with ESRGAN x4 (blended 68/32 with Lanczos). The STEADFAST MEN letters are lifted from LOCKED-stage-screen.jpg and stamped BEFORE HeyGen (stamp5.py: dimmed to 78%, light blur, kept behind Wes).
- HeyGen Avatar IV, low expressiveness, 1080p.
- Logo lock (build5.py): HeyGen animated the stamped rule into a glowing blue bar on plate 73. Wherever rembg finds the logo box free of Wes, every frame gets the stamped plate pixels put back, so the letters never warp.
- Boards are clean: near-black with a faint periwinkle glow, a letter-spaced kicker and one white Geist line. No grid, brackets, footer, ghost word or word-by-word text.
- Assembly is ffmpeg only (no Descript).

## QA (one frame per second, sheets in /workspace/s01v5/qa/sheet0-5.jpg)
- Every Wes frame has the same charcoal henley, and the STEADFAST MEN letters are present and intact. Fixed during QA: the blue bar on 73, and logo cut-offs in the walk and charge crops.
- No blue-only screen, exit sign, ghost or audience. Eyes stay off the lens in every shot used.
- The mouth moves whenever the voice plays on camera. Boards never carry the spoken script word for word.

## Rejected renders (credits spent, not used)
- R2 and R5 on plate 81: he faced the lens with an over-animated smile. 81 stays a non-talking plate.
- R7 and R4 (first takes on 89, made with a motion prompt): a green prop showed up in his hand and a wristwatch appeared. They were re-rendered without a motion prompt. R4b and R7b still grow a watch and ring for a few seconds around 16 s and 8 s, and the crops are set to keep the wrist out of frame.

## Spend
- HeyGen: 71 premium credits (3,960 → 3,889), 11 renders, 210 s total.
- ElevenLabs: 276 credits (~$0.05).
- Image generation: $0.

## Weaknesses
- The plate pool is nearly exhausted. Only 89 was clean and unused, so 80, 72 and 89 are each used twice. They get different crops or treatments, but it is the same angle.
- The walk is a 2D composite (lateral move, bob, half-follow camera), not a real stride. Inpaint smear where Wes 69 was removed is faintly visible behind his right shoulder.
- Plate 89 renders run a little more animated (bigger mouth on some vowels) than 72 and 73.
- Light differs slightly between plates: 80 and 72 read a bit cooler and darker than 73.
- The split panel shows only part of the logo ("STEA…" behind his head).
- On 73, a lean-in shot crops close to the right edge of the logo.
- The bed is a synth pad, not the v4 music. That is because v4 had no separate bed file.
- The script path artifacts/training/W01-A-Quiet-Tuesday-LECTURE.md does not exist on main. I used the canon backup of W01-A-Quiet-Tuesday.txt for the charge line.
