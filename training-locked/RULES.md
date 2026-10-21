# Steadfast Men — training video rules

Source of truth for Wes stage plates, Imagine stills, and class-tape video.
Repo: https://github.com/aaronmaberry/steadfast branch main
Folder: training-locked/
Signed 2026-10-09. Do not replace a lock without a new Aaron sign-off.

Anyone picking this up (Grok, Jarvis, Cursor) follows this file. Do not invent a new face, shirt, room, or logo.

## Who is on the tape

- Class tape is Wes Hart only. Jonathon never appears on a lecture.
- Public table show is separate: Wes and Jonathon at the locked oak table. Do not mix those frames into training.
- 24 weekly lectures. 30 minutes, cap 40.
- Paid lectures stay unlisted on the paywall. Public YouTube is the table show, not the class tape.

## Wes — face and body (do not drift)

Wes Hart. Mid-40s. Fair-olive skin. Short dark brown hair with a little lift at the front. Light beard and mustache kept close. Brown eyes. Straight nose. Calm closed-mouth look.

Ordinary man. Not a model. Not a celebrity. Photoreal.

Do not invent a new face. Anchor every new still on a signed plate from this folder.

Negative: different man, younger, older, clean-shaven, long hair, glasses, smile-for-camera, beauty skin, plastic face, extra fingers, melted mouth, celebrity likeness.

## Wardrobe (never change)

Long-sleeve henley. Sleeves pushed up. Same shirt on every plate and every clip.

Never short sleeves. Never a polo on new plates. Never a jacket. Plates 01–02 are older navy-polo frames. Do not use them as the current look.

## Stage (signed 2026-10-09, Aaron confirmed the plate)

Master plate: training-locked/69-wes-screen-lock-plate.jpg

This is the stage. Dark floor. Black curtains. One screen on the left of this frame. No chairs. Phone chrome is not part of the plate.

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

## Descript post rules (hard, check before every cut)

Reference cut: training/w01-poc/best/w01-poc-5min-REFERENCE.mp4 (2026-10-20). Build on this. Do not start over.

### Continuous audio
- Wes talks through every transition. Audio never stops. Boards and new angles fade under him.
- No blank screens. No silent gaps. If a board is up, his voice continues underneath.
- Crossfade duration: 0.6–0.8s. Overlap the clips so the outgoing and incoming have extra frames.

### Movement
- He works the stage. Torso shifts. Hands move. Not static.
- Hands stay consistent. No watch. No extra fingers. No sudden jumps.
- After a board, come back on a different angle. Do not reuse the same angle back-to-back.
- Start on the wider second-half angle from the reference. Use the tighter angle later.

### Boards
- Full-screen only. Use the locked board plate (A6-SCRIPTURE-COVER-FULL-clean.png style).
- Same font, same periwinkle highlight, same dark field, every time.
- Scripture boards: one verse, key phrases highlighted.
- Bullet boards: short points he is saying. Not the whole script.
- Boards stay up long enough to write. Fade in, hold, fade out. He keeps talking.

### Descript workflow
- Import locked audio + stage clips as the script track.
- Boards and new angles go on layers above. Mute their audio.
- Use Crossfade (not Smart Transition) between stage angles and boards.
- Underlord can apply crossfades if prompted: "crossfades only, 0.8s, no smart transitions."
- Regenerate only for lip-sync gaps. Do not regenerate the locked voice.

### Hard checks before generation
1. Read this file.
2. Confirm stage plate is 69-wes-screen-lock-plate.jpg.
3. Confirm Lesson 1 audio is S01-A-Quiet-Tuesday-LOCKED.mp3.
4. Confirm no watch, no new face, no new stage, no new board style.
5. Confirm audio continues under every board.

This is the locked Lesson 1 lecture audio. Use only this file for Lesson 1. Do not generate new audio for Lesson 1. Lip-sync and cut to this file.

Duration: ~25:32. Voice: locked Wes Hart Option C.

## Hard rules (do not break)

- No watch on Wes. Ever. If a plate or clip shows a watch, discard it. He does not wear one. Do not generate a new clip if the source plate has a watch. Edit it out or start over.
- Locked voice only: ElevenLabs Wes Hart Option C, id o4XQFIFZbnVGJNZmuUuK. Do not use any other voice or clone for class tape.
- Do not loop the same speaking clip. If the clip ends, cut to a board, a walk, or a new angle. Never restart the same clip under continuing audio.
- Walking clips (35–38) are used. They are part of the cut. Do not leave them out. Walk 35 has a podium; do not use it for new cuts.
- Board transitions are fades, not hard cuts. Fade in on the line, hold, fade out. No black frames between cuts. Boards are full screen, text only. No Wes on the board. His audio continues underneath.
- Boards only appear when the spoken line matches the text on the board. Do not put up a board that is not in the dialogue.
- Stage is locked to 69-wes-screen-lock-plate.jpg. Black stage. Purple logo screen. No other stage.
- Lip sync must match the locked voice. If the mouth is off, regenerate the clip. Do not ship a mismatch.
- Audio has natural pauses. He is delivering a training talk, not reading a script at constant speed. Pause before key lines.


Pipeline locked 2026-10-05:

- Locked still, then a short image-to-video, 6–15 seconds, one spoken line.
- Cut every 4–8 seconds in Descript.
- Descript pans and punches (full, half, screen) to fake movement across the stage. That is the movement. Do not ask one shot to walk, talk, and show the room.
- CapCut is for Shorts only.

Imagine Video 1.5 on the Grok app / grok.com/imagine is the mouth path. Aaron generates those. Jarvis does not have Imagine Video on the bot computer. Jarvis owns the shot list, the prompts, and the Descript order.

HeyGen mouth is rejected. Test 766a54b213eb4f6797607ff3b25293db melted the face. Do not retry HeyGen for mouth.

HeyGen image-to-video was used only for the four signed walks (35–38), 8 seconds each. Clip 35 invented a podium and a guitar. Aaron signed it anyway. Do not repeat that. No new props.

## Voice

ElevenLabs Voice Design. Wes Hart - Option C.
Voice id: o4XQFIFZbnVGJNZmuUuK

Use this id for lecture lines and for Wes on the table show.
Eleven v3 for YouTube and dialogue. Multilingual v2 for long chapters.
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
- 69-wes-screen-lock-plate.jpg — locked 2026-10-09. Aaron confirmed this plate. Stage master and screen master. Next new plate is 70.

## Prompt block (paste under a signed plate)

Keep this exact face. Wes Hart, mid-40s, fair-olive skin, short dark brown hair with a little lift at the front, light beard and mustache kept close, brown eyes, straight nose, calm closed-mouth look. Same long-sleeve henley, sleeves pushed up. Same dark stage: dark floor, black curtains, one screen, no chairs. Eyes on the room, not the camera. No audience. No podium. Photoreal, ordinary man, not a model, not a celebrity. Do not change the background. Do not redraw the logo. Stamp training-locked/LOCKED-stage-screen.jpg on the screen after. Negative: different man, younger, older, clean-shaven, long hair, glasses, smile-for-camera, beauty skin, plastic face, extra fingers, melted mouth, celebrity likeness, short sleeves, podium, audience, chairs.

## Descript mastery (2026-10-21)

### Crossfade rules
- Crossfade needs extra frames beyond the visible cut. Trim clips so both sides have room.
- Clips must be on the same layer to crossfade. Drag one onto the other until the red line appears, then drop.
- Scene-level crossfade applies to all layers in the scene. Clip-level crossfade is per clip.
- Audio and video fades can be separated: click the white handle, then remove the audio component if Wes should keep talking.

### Board overlay method
- Put the board on a layer above the script track.
- Mute that layer so Wes's voice continues underneath.
- Crossfade the board in and out. Do not cut hard to black.
- Hold the board long enough for the point (scripture ~12–18s, bullets ~8–12s).

### Underlord prompts that work
- "Make all transitions crossfades, not smart transitions."
- "Apply 0.8s crossfades between every scene."
- "Mute the board layers so the script track stays audible."
- "Add a fade in and fade out on the board layers."

### Professional edit rules
- J-cut: next clip's audio starts before its picture. Use for board entries.
- L-cut: current audio continues after the picture changes. Use for board exits.
- Cut on motion (hand, torso, step) not on stillness.
- Change the visual every 10–20 seconds for retention, but only when it serves the point.
- Hard cut is the default. Crossfade only for board entry/exit or angle change.
- No watch. Hands consistent. Torso moves. Eyes on the room.

### Pre-generation check
Read this file before any training video generation. Do not start clips until the board timings and angle plan are written.

## Steadfast video rules (all formats, hard)

Applies to training lectures, YouTube table show, podcast, Shorts, Reels, and any other Steadfast video.

## W01 POC feedback (2026-10-20, hard rules)

Reference cut: training/w01-poc/best/w01-poc-5min-REFERENCE.mp4

### Audio continuity
- No blank screens. Audio starts immediately. Wes talks through every transition.
- Gaps found at ~1:35, ~2:30, ~3:15. These must not recur.
- At ~3:32 the return clip did not match the dialogue. Match the angle to the point.
- At ~4:22 the hand motion was too fast. Hands move naturally, never snap.

### Movement and hands
- He is not static. Torso shifts. Hands are used. He works the stage.
- Hands stay consistent. No watch. No extra fingers. No sudden jumps.
- After a board, return on a different angle. Do not reuse the same angle back-to-back.
- Start on the wider second-half angle from the reference. Use the tighter angle later.

### Board consistency
- Same font, same periwinkle highlight, same dark field, every board.
- Scripture: one verse, key phrases highlighted.
- Bullets: short points he is saying, not the whole script.
- Boards stay up long enough to write. Fade in, hold, fade out. Audio continues underneath.

### Pre-cut check
Before any generation, confirm:
1. Stage plate is 69-wes-screen-lock-plate.jpg.
2. Audio is the locked Lesson 1 file.
3. No watch, no new face, no new stage, no new board style.
4. Audio continues under every board.
5. Angle plan is written and randomized.
