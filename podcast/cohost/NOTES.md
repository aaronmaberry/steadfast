# Jonathon (co-host) face-master options — NOT LOCKED, for Aaron's pick

Base: the curly-haired co-host in the gray tee from img/LOCKED-podcast-table.jpg, cropped and upscaled 4x with Real-ESRGAN (reference: the co_ref crop). img/hero-studio.jpg shows the same man (gray tee), but it's lower resolution, so I didn't use it as the reference.
Tool: ElevenLabs Flows, gemini-3-pro-image edit with the reference wired in (identity-consistency model). 1 generation per frame, 12 frames. Output is 1376x768 (16:9).
Flow: https://elevenlabs.io/app/flows/bdY0urK9oEVJ5OSnsTns

| Option | Change from site look |
|---|---|
| 1 Site-faithful | Hair and beard as on the site (short full curls, short trimmed beard) |
| 2 Tidy | Curls a bit shorter and neater on the sides, beard trimmed with a clean cheek line |
| 3 Fuller beard | Same hair, beard ~1.5 cm, kept neat |
| 4 Rugged | Looser, longer curls, scruffier beard, faint gray at the temples |

Each option: optN-waist (waist-up, front three-quarter), optN-profile, optN-close. Same foam studio, boom mic, heather gray tee.

## Voice
Locked voice: uiUeT7adTSLnHQ91QHdW ('Jonathon - Option L'), sample jonathon-voice-LOCKED.mp3. Relaxed, crisp, neutral American accent, median pitch ~122 Hz. Replaces DUD6Dsyq6xCL5Xqppm7R ("Jonathon - Podcast"); the older sample remains as jonathon-voice-sample.mp3 for reference. See voice-options-NOTES.md for the A–L comparison.
There's no Jonathon script in the repo (rg 'jonathon' found nothing), so I wrote the line myself around a site line (index.html: "A son should be able to copy your walk."):
"You know what gets me? Most of us aren't failing at the big stuff. It's the little things... the phone at dinner, the promise we let slide. A son should be able to copy your walk. And that starts right here at the table, man. Not on a stage."

## Spend
12 images x ~$0.30 = $3.62, plus voice 249 credits (~$0.04). Total ~$3.66 of the $8 cap.

## Known weaknesses
- "Profile" frames came out as a strong three-quarter, not a true 90° side profile.
- Generated at 1376x768 native; needs an upscale (Real-ESRGAN) before 4K use.
- Waist-up shots frame him on the right with the mic boom crossing his chest; usable for the bubble cams but tighter than Wes's crop.
