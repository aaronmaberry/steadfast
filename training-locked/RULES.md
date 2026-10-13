# Steadfast Men — training video rules

Source of truth for Wes stage plates, Imagine stills, and class-tape video.
Repo: https://github.com/aaronmaberry/steadfast branch main
Folder: training-locked/
Signed 2026-10-09. Do not replace a lock without a new Aaron sign-off.

Anyone picking this up (Grok, Jarvis, Cursor) follows this file. Do not invent a new face, shirt, room, or logo.

## Who is on the tape

- Class tape is Wes Hart only. Jonathan never appears on a lecture.
- Public table show is separate: Wes and Jonathan at the locked oak table. Do not mix those frames into training.
- 24 weekly lectures. 30 minutes, cap 40.
- Paid lectures stay unlisted on the paywall. Public YouTube is the table show, not the class tape.

## Wes — face and body (do not drift)

Wes Hart. Mid-40s. Fair-olive skin. Short dark brown hair with a little lift at the front. Light beard and mustache kept close. Brown eyes. Straight nose. Calm closed-mouth look.

Ordinary man. Not a model. Not a celebrity. Photoreal.

Do not invent a new face. Anchor every new still on a signed plate from this folder.

Negative: different man, younger, older, clean-shaven, long hair, glasses, smile-for-camera, beauty skin, plastic face, extra fingers, melted mouth, celebrity likeness.

## Wardrobe (never change)

WARDROBE-LOCK (Aaron, 2026-10-12): training-locked/WARDROBE-LOCK.jpg is the shirt. It is cut from master plate 69.

Identical in every shot and every session: plain charcoal-grey long-sleeve henley, same dark charcoal shade, soft matte slub cotton, four-button placket with the top button open, full-length sleeves down to the wrists, relaxed fit, no logo or print. Small black lav clipped on the placket between the second and third buttons. Dark jeans, black belt.

Note: this file used to say "sleeves pushed up". Master 69 has the sleeves down, so the lock follows 69. Pushed-up sleeves are now a mismatch.

QA every new plate and clip against WARDROBE-LOCK.jpg. Reject any change in shade (navy or blue-grey is a fail), fit, logo, sleeve length or texture. Audit 2026-10-12: plates 75 and 79 have pushed-up sleeves, so they fail the lock and are excluded from new renders.

Never short sleeves. Never a polo on new plates. Never a jacket.

## Stage (signed 2026-10-09, Aaron confirmed the plate)

Master plate: training-locked/69-wes-screen-lock-plate.jpg

This is the stage. Dark floor. Black curtains. One screen on the left of this frame. No chairs. Phone chrome is not part of the plate.

Stills 01–34 and 39–68 were rebuilt 2026-10-09 by cutting each pose onto this plate. The room pixels are the plate. 01 is the plate itself. Do not put a generated room back in this folder.

Every new still starts from this plate. Camera, pose, and his spot may change. The room does not. Do not invent a new stage.

Banned: audience, heads in the foreground, podium, guitar, extra screens, white type on the screen, fellowship-hall tables, round banquet tables, chairs.

Eyes on the room, not the lens. He is a man recorded on stage talking to the people in the room. He is not addressing the camera. No audience is ever visible.

He works the stage. New plates change his spot, his hands, and the camera. They do not change his face, shirt, or the room.

## Screen and logo (stamp, do not redraw)

Screen lock signed 2026-10-09. Aaron confirmed the full plate. The screen on that plate is the screen on every generation.

File to stamp, not redraw:
- training-locked/LOCKED-stage-screen.jpg
- steadfast-locked/LOCKED-stage-screen.jpg
- Full plate with phone chrome removed: training-locked/69-wes-screen-lock-plate.jpg

This is the screen on every generation. Do not swap in the header lockup. Do not redraw the letters.

What the screen shows:

- STEADFAST on the first line.
- First A is the open triangle, same as the site mark.
- Second A is a normal A.
- Thin rule under the word.
- MEN under the rule, tracked out.
- Letters read light on the dark screen, as in the signed still. Not gold. Not white type on a white field.

Imagine redraws the A's wrong. Stamp LOCKED-stage-screen.jpg onto the screen after generation. The header file LOCKED-logo-steadfast-men.jpg stays the site and book mark. It is not the stage screen.

## How a new still is made

1. Start from training-locked/69-wes-screen-lock-plate.jpg. That plate is the stage.
2. Change only pose, spot on the stage, and camera. Same face, same henley, same room.
3. Stamp LOCKED-stage-screen.jpg onto the screen after generation. Do not ask the model to draw the logo.
4. Show Aaron the plate. Do not lock it and do not send it to video until he signs it.
5. Lock only after he says so. Copy into training-locked/ with the next number. Commit and push main.

## How a clip is made

Pipeline locked 2026-10-05:

- Locked still, then a short image-to-video, 6–15 seconds, one spoken line.
- Cut every 4–8 seconds in Descript.
- Descript pans and punches (full, half, screen) to fake movement across the stage. That is the movement. Do not ask one shot to walk, talk, and show the room.
- CapCut is for Shorts only.

Imagine Video 1.5 on the Grok app / grok.com/imagine is the mouth path. Aaron generates those. Jarvis does not have Imagine Video on the bot computer. Jarvis owns the shot list, the prompts, and the Descript order.

HeyGen mouth was rejected 2026-10-09 (test 766a54b213eb4f6797607ff3b25293db melted the face).
Update 2026-10-12, Aaron's direction: HeyGen Avatar IV lip-sync at low expressiveness is allowed for SHORT clips (about 4–10 s) from plates 72–81, with Wes angled to the room. Reject any clip with an unnatural mouth, face drift, halo or glitch.
In training, Wes NEVER talks to the camera. He faces the unseen audience, works the room and walks the stage.

HeyGen image-to-video was used only for the four signed walks (35–38), 8 seconds each. Clip 35 invented a podium and a guitar. Aaron signed it anyway. Do not repeat that. No new props.

## Voice

ElevenLabs Voice Design. Wes Hart - Option D.
Voice id: krjoGt4x3CttlxSuoDYW
Model: eleven_v4, one take per section (generations_count 1). Lecture post: locked/post.sh (atempo 0.93 + retime).

Evidence: the approved S01-v2 recording (training-ep01/rec/S01-v2/S01-full.mp3) was made with this voice. See rec/S01-v2/STATUS-secs03-12.txt ("Voice: Wes Hart Option D krjoGt4x3CttlxSuoDYW, eleven_v4"), locked/LOCKED-LECTURE-STYLE.md, and the S02/S03 RECORD-STEPS files. All 24 session masters use Option D.

Use this id for lectures, shorts, and Wes on the table show.
Option C (o4XQFIFZbnVGJNZmuUuK) is retired. Do not use it for Wes.
Kepler is temp only if this id is missing. No celebrity clone.

## Lecture clock

- 0–1 open
- 1–6 Tuesday
- 6–14 mark and verse
- 14–22 two houses
- 22–28 one act
- 28–32 charge and tables

Guide closes with three blanks plus: Name it / Do this week / Tell a brother / Carry this.

Week map: 01–06 passivity, 07–12 responsibility, 13–18 lead, 19–24 reward.

Week 01 manuscript: artifacts/training/W01-A-Quiet-Tuesday-LECTURE.md. Teacher name on the tape is Wes Hart.

## What is already locked

training-locked/ on main.

- 01–02 older polo frames. Not the current look.
- 03–07 early scripture and close plates.
- 08–34 signed 2026-10-09. 09 is the preferred turn-to-screen plate.
- 35–38 signed walks, 8 seconds, HeyGen. 35 has a podium and a guitar. Leave them.
- 69-wes-screen-lock-plate.jpg — locked 2026-10-09. Aaron confirmed this plate. Stage master and screen master.
- 70–81 — Aaron signed 2026-10-12 as training clip plates (16:9, clean plate-69 stage, blank dark screen, charcoal henley, lav). Source for short training clip renders. 70 and 71 face the camera: non-talking use only, never a talking render. See README for the list. Next new plate is 82.
- 82–115 — waist-up plate pool, 2026-10-12 (S01 proof v2). Each plate is used once, ever. Tracked in training-locked/PLATE-MANIFEST.json (used_in = session and segment). Before a render, pick only plates with empty used_in; after it, write the use. Next new plate id is in the manifest (next_id).

## Plate pool rules (Aaron, 2026-10-12)

1. Waist-up only. No wides, no knees-up, no full body.
2. Lip-synced whenever his voice plays. Silent motion only under a board with no Wes on screen.
3. Never repeat a plate or an angle across the 24 sessions. Same shoot day: same henley, same light.
4. Eyes off the lens. Frontal plates pull HeyGen's eyes to camera, so use three-quarter and profile plates only.

## Prompt block (paste under a signed plate)

Keep this exact face. Wes Hart, mid-40s, fair-olive skin, short dark brown hair with a little lift at the front, light beard and mustache kept close, brown eyes, straight nose, calm closed-mouth look. Same charcoal henley as WARDROBE-LOCK.jpg, sleeves down to the wrists, lav on the placket. Same dark stage: dark floor, black curtains, one screen, no chairs. Eyes on the room, not the camera. No audience. No podium. Photoreal, ordinary man, not a model, not a celebrity. Do not change the background. Do not redraw the logo. Stamp training-locked/LOCKED-stage-screen.jpg on the screen after. Negative: different man, younger, older, clean-shaven, long hair, glasses, smile-for-camera, beauty skin, plastic face, extra fingers, melted mouth, celebrity likeness, short sleeves, podium, audience, chairs.
