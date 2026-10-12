# Steadfast daily shorts — Wes bank + build

One-time bank of **42 photoreal Wes stills** (7 outfits × 6 angles) in the clean plate-69 stage, so every daily short pulls Wes with **zero image spend**. Per-day cost is the voice only (~$0.10 ElevenLabs VO).

## Layout
```
social-daily/
  wes-bank/<outfit>/<angle>.jpg   1376x768 JPEG q92
  wes-bank/bank.json              outfit/angle lists + head_x (0-1) used for auto-cropping
  wes-bank/spec.json, prompts/    exact generation prompts (for re-rolls/extension)
  daily_wes.py                    date -> outfit + hook/CTA stills + 3 room angles
  daily_style.py                  date -> palette (ord%6) + treatment (ord%5)
  build.py                        PIL frame renderer -> ffmpeg (1080x1920, 30fps, 44s)
  mix.py                          VO + music bed @0.12 + whoosh/hit SFX, loudnorm -14
  assets/                         Geist fonts, music.mp3, whoosh.mp3, hit.mp3
  example-2026-10-12/             words.json + vo.mp3 for the Luke 16:10 daily (v4)
```
**Outfits:** charcoal-henley, navy-henley, olive-henley, flannel (buffalo check over charcoal tee), quarter-zip (heather grey), denim (rolled sleeves), crewneck (oatmeal).
**Angles:** `cam-medium` (chest-up, to camera — hook), `cam-close` (stage-right close, to camera — CTA), `three-quarter` (waist-up, palms open), `side-close` (close three-quarter profile), `low-angle` (knees-up from low), `walk` (mid-thigh up, mid-stride). No wide/far shot by design: Wes stays large in frame.

## Rotation (deterministic by date)
- outfit = `outfits[date.toordinal() % 7]`
- hook = `cam-medium`, CTA = `cam-close` (closed-mouth still with a slow push)
- room shots = 3 of the 4 room angles, `ROOM[(ord//7 + i) % 4]`, so each outfit shows a different trio each week
- `python3 daily_wes.py 2026-10-12` prints the next 8 days

## Daily build
```
mkdir day-YYYY-MM-DD && cd day-YYYY-MM-DD
# put vo.mp3 (Wes voice Option D) + words.json ([word,start,end] list) here
DAY=YYYY-MM-DD python3 ../build.py 1 16 30 41   # QA frames
DAY=YYYY-MM-DD python3 ../build.py              # -> video.mp4
python3 ../mix.py                               # -> final mp4
```
The on-screen copy/shot timing in `build.py` is the v4 Luke 16:10 layout; edit the SHOTS/eyebrow strings per day's script.
Optional: `HOOKDIR=idle_hook CTADIR=idle_cta` uses HeyGen idle-take frame dirs (plan credits, no $) instead of the bank stills.

## QA + provenance
Generated 2026-10-12 with ElevenLabs Flows, gemini-3-pro-image, references = master face plate 69 (`training-locked/69-wes-screen-lock-plate.jpg`), lens ref, clean stage plate.
Every image passed master-face QA and the hard rules: no Bible, podium, chairs, audience, stands, overhead light rigs, ghosts, or screen text; empty hands.
4 navy shots are reused from the approved v4 short. Re-rolled: charcoal + denim `cam-medium` (framed too wide).
Cost: 40 generations × ~$0.50 = ~$20.10.
